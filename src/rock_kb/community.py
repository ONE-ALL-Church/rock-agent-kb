from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Optional
from urllib.parse import quote, urljoin, urlparse, urlunparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

from .extract import USER_AGENT, canonicalize_url, discover_links, main_markdown, now_iso, page_title, sha256_text
from .normalize import canonical_path_for, canonical_record_id, infer_audience, infer_rock_versions, summarize_locally
from .sources import Source

COMMUNITY_HOST = "community.rockrms.com"
ROCKUMENTATION_HOME_PAGE_GUID = "85750a25-e864-4938-bde7-09cd32146a18"
ROCKUMENTATION_HOME_BLOCK_GUID = "d30514c6-b51f-40b4-aa77-4108b35b7f13"
ROCKUMENTATION_BOOK_PAGE_GUID = "6d657cde-b3b9-4acd-9cab-928234ab0fae"
ROCKUMENTATION_BOOK_BLOCK_GUID = "a6f974bc-6d59-46e7-a832-37525a343706"
ROCKUMENTATION_API_TOOL = "rockumentation_block_action"

IGNORED_EXTENSIONS = {
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".map",
    ".zip",
}

KIND_PATH_PREFIXES = {
    "rock_documentation": ["/documentation", "/documentation/bookcontent"],
    "rock_recipes": ["/recipes"],
    "rock_qa": ["/ask"],
    "rocku": ["/rocku"],
    "rock_developer": ["/developer", "/api-docs", "/lava"],
    "rock_mobile_docs": ["/developer/mobile-docs"],
    "rock_community_hubs": ["/community-hubs"],
    "rock_community_blog": ["/connect"],
    "rock_community_site": [
        "/api-docs",
        "/ask",
        "/community-hubs",
        "/developer",
        "/documentation",
        "/lava",
        "/learn",
        "/podcast",
        "/recipes",
        "/rocku",
        "/styling",
    ],
    "rock_api_docs": ["/api-docs"],
    "rock_lava_docs": ["/lava"],
    "rock_shop_plugins": ["/rockshop"],
}


@dataclass(frozen=True)
class ProbeTarget:
    url: str
    method: str = "GET"
    expected: str = "unknown"


def community_prefixes(source: Source) -> list[str]:
    raw_prefixes = source.raw.get("path_prefixes") or []
    if raw_prefixes:
        return [normal_path_prefix(prefix) for prefix in raw_prefixes]
    return KIND_PATH_PREFIXES.get(source.kind, [urlparse(source.root_url).path or "/"])


def community_excluded_prefixes(source: Source) -> list[str]:
    return [normal_path_prefix(prefix) for prefix in source.raw.get("excluded_path_prefixes") or []]


def normal_path_prefix(prefix: str) -> str:
    if prefix.startswith("http"):
        prefix = urlparse(prefix).path
    if not prefix.startswith("/"):
        prefix = "/" + prefix
    return prefix.rstrip("/") or "/"


def is_html_candidate(url: str, source: Source) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.netloc.lower() != source_host(source):
        return False
    if parsed.path.lower().endswith(tuple(IGNORED_EXTENSIONS)):
        return False
    if parsed.path.lower() in {"/login", "/logout"}:
        return False
    if parsed.path.lower().endswith("/q/new"):
        return False
    if parsed.path.lower().startswith(("/getimage.ashx", "/getfile.ashx", "/content/", "/scripts/", "/themes/", "/obsidian/", "/styles/")):
        return False
    if "returnurl=" in parsed.query.lower():
        return False
    prefixes = community_prefixes(source)
    path = parsed.path.rstrip("/") or "/"
    for excluded in community_excluded_prefixes(source):
        if path == excluded or path.startswith(excluded + "/"):
            return False
    return any(path == prefix or path.startswith(prefix + "/") for prefix in prefixes)


def clean_url_for_fetch(url: str) -> str:
    parsed = urlparse(canonicalize_url(url))
    scheme = "https" if parsed.netloc.lower() == COMMUNITY_HOST else parsed.scheme
    if parsed.query.lower().startswith("q="):
        return urlunparse((scheme, parsed.netloc, parsed.path, "", parsed.query, ""))
    return urlunparse((scheme, parsed.netloc, parsed.path, "", "", ""))


def source_host(source: Source) -> str:
    return urlparse(source.root_url).netloc.lower()


def discover_community_urls(
    source: Source,
    max_pages: int = 250,
    id_sweep: bool = False,
    sweep_window: int = 75,
    known_urls: Optional[Iterable[str]] = None,
) -> list[str]:
    seen: set[str] = set()
    queue: list[str] = [clean_url_for_fetch(source.root_url)]
    discovered: set[str] = set(queue)
    for known_url in known_urls or []:
        cleaned = clean_url_for_fetch(str(known_url))
        if is_html_candidate(cleaned, source):
            discovered.add(cleaned)

    with httpx.Client(follow_redirects=True, timeout=20, headers={"User-Agent": USER_AGENT}) as client:
        while queue and len(seen) < max_pages:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            try:
                response = client.get(url)
            except httpx.HTTPError:
                continue
            if response.status_code >= 400 or "text/html" not in response.headers.get("content-type", ""):
                continue
            for link in discover_links(response.text, str(response.url), same_host=True):
                cleaned = clean_url_for_fetch(link)
                if is_html_candidate(cleaned, source) and cleaned not in discovered:
                    discovered.add(cleaned)
                    queue.append(cleaned)

    if id_sweep and source.kind in {"rock_recipes", "rock_qa"}:
        discovered.update(probe_numeric_detail_urls(source, discovered, sweep_window=sweep_window))
    return sorted(discovered)


def probe_numeric_detail_urls(source: Source, known_urls: Iterable[str], sweep_window: int = 75) -> set[str]:
    ids = []
    for url in known_urls:
        parsed = urlparse(url)
        match = re.search(r"/(?P<id>[0-9]{2,})(?:/|$)", parsed.path)
        if match:
            ids.append(int(match.group("id")))
    if not ids:
        return set()
    low = max(1, min(ids) - max(10, sweep_window // 3))
    high = max(ids) + sweep_window
    if source.kind == "rock_recipes":
        candidates = [f"https://community.rockrms.com/recipes/{value}" for value in range(low, high + 1)]
    else:
        categories = ["using", "troubleshooting", "websites", "developing"]
        candidates = [
            f"https://community.rockrms.com/ask/{category}/{value}"
            for value in range(low, high + 1)
            for category in categories
        ]
    valid: set[str] = set()

    def probe_one(url: str) -> Optional[str]:
        try:
            with httpx.Client(follow_redirects=True, timeout=10, headers={"User-Agent": USER_AGENT}) as client:
                response = client.get(url)
        except httpx.HTTPError:
            return None
        final_url = clean_url_for_fetch(str(response.url))
        if response.status_code == 200 and is_html_candidate(final_url, source) and not is_not_found_page(response.text):
            return final_url
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        for future in as_completed([executor.submit(probe_one, url) for url in candidates]):
            result = future.result()
            if result:
                valid.add(result)
    return valid


def is_not_found_page(html: str) -> bool:
    title = page_title(html).lower()
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True).lower()
    return (
        "404 page" in title
        or "page not found" in title
        or "that recipe does not exist" in text
        or "article was not found" in text
    )


def fetch_community_pages(urls: Iterable[str], workers: int = 8, source: Optional[Source] = None) -> list[dict[str, Any]]:
    unique_urls = sorted({clean_url_for_fetch(url) for url in urls})
    rows: list[dict[str, Any]] = []

    def fetch_one(url: str) -> dict[str, Any]:
        with httpx.Client(follow_redirects=True, timeout=25, headers={"User-Agent": USER_AGENT}) as client:
            if source and source_uses_rockumentation_api(source):
                payload = fetch_rockumentation_payload(client, url)
                if payload:
                    content = payload.get("initialContent") or ""
                    configuration = payload.get("configurationValues") or {}
                    payload_url = rockumentation_payload_url(url, configuration)
                    return {
                        "requested_url": url,
                        "url": payload_url,
                        "status_code": 200,
                        "content_type": "application/json; rockumentation=1",
                        "retrieved_at": now_iso(),
                        "content_hash": rockumentation_content_hash(payload, payload_url),
                        "content": content,
                        "rockumentation_payload": payload,
                        "extraction_tool": ROCKUMENTATION_API_TOOL,
                    }
            response = client.get(url)
        return {
            "requested_url": url,
            "url": clean_url_for_fetch(str(response.url)),
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "retrieved_at": now_iso(),
            "content_hash": sha256_text(response.text),
            "content": response.text,
        }

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {executor.submit(fetch_one, url): url for url in unique_urls}
        for future in as_completed(futures):
            try:
                rows.append(future.result())
            except Exception as exc:  # pragma: no cover - diagnostic path
                rows.append({"requested_url": futures[future], "error": str(exc), "retrieved_at": now_iso()})
    return sorted(rows, key=lambda row: row.get("url") or row.get("requested_url") or "")


def source_uses_rockumentation_api(source: Source) -> bool:
    return ROCKUMENTATION_API_TOOL in source.preferred_tooling


def fetch_rockumentation_payload(
    client: httpx.Client,
    url: str,
    attempts: int = 3,
) -> Optional[dict[str, Any]]:
    parsed = urlparse(clean_url_for_fetch(url))
    if parsed.netloc.lower() != COMMUNITY_HOST:
        return None
    path = parsed.path.rstrip("/") or "/"
    if path == "/documentation":
        api_url = rockumentation_home_api_url()
    else:
        slug = rockumentation_slug_from_url(url)
        if not slug:
            return None
        api_url = rockumentation_book_api_url(slug)
    for attempt in range(max(1, attempts)):
        try:
            response = client.post(api_url, headers={"Accept": "application/json"})
        except httpx.HTTPError:
            response = None
        if response is not None and response.status_code < 400 and "json" in response.headers.get("content-type", ""):
            try:
                payload = response.json()
            except json.JSONDecodeError:
                payload = None
            if isinstance(payload, dict):
                content = payload.get("initialContent") or ""
                configuration = payload.get("configurationValues") or {}
                if path == "/documentation" and "topic-card" in content:
                    return payload
                if path != "/documentation" and (configuration.get("slug") or "rockumentation-article" in content):
                    return payload
        if attempt + 1 < max(1, attempts):
            time.sleep(0.15 * (attempt + 1))
    return None


def rockumentation_home_api_url() -> str:
    return (
        f"https://{COMMUNITY_HOST}/api/v2/BlockActions/"
        f"{ROCKUMENTATION_HOME_PAGE_GUID}/{ROCKUMENTATION_HOME_BLOCK_GUID}/RefreshObsidianBlockInitialization"
    )


def rockumentation_book_api_url(slug: str) -> str:
    encoded_slug = quote(slug.strip("/"), safe="")
    return (
        f"https://{COMMUNITY_HOST}/api/v2/BlockActions/"
        f"{ROCKUMENTATION_BOOK_PAGE_GUID}/{ROCKUMENTATION_BOOK_BLOCK_GUID}/"
        f"RefreshObsidianBlockInitialization?slug={encoded_slug}"
    )


def documentation_slug_from_url(url: str) -> Optional[str]:
    return rockumentation_slug_from_url(url, prefix="documentation")


def developer_slug_from_url(url: str) -> Optional[str]:
    return rockumentation_slug_from_url(url, prefix="developer")


def rockumentation_slug_from_url(url: str, prefix: Optional[str] = None) -> Optional[str]:
    parsed = urlparse(clean_url_for_fetch(url))
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None
    if prefix and parts[0] != prefix:
        return None
    if parts[0] not in {"documentation", "developer"}:
        return None
    if len(parts) == 1 or (parts[0] == "documentation" and len(parts) > 1 and parts[1].lower() == "bookcontent"):
        return None
    return "/".join(parts[1:])


def rockumentation_payload_url(fallback_url: str, configuration: dict[str, Any]) -> str:
    requested = clean_url_for_fetch(fallback_url)
    slug = documentation_slug_from_url(requested)
    if slug:
        return f"https://{COMMUNITY_HOST}/documentation/{slug}"
    slug = developer_slug_from_url(requested)
    if slug:
        return f"https://{COMMUNITY_HOST}/developer/{slug}"
    config_slug = str(configuration.get("slug") or "").strip("/")
    if config_slug:
        return f"https://{COMMUNITY_HOST}/documentation/{config_slug}"
    return requested


def normalize_community_fetch(source: Source, fetched: dict[str, Any]) -> Optional[dict[str, Any]]:
    rockumentation_payload = fetched.get("rockumentation_payload") if source_uses_rockumentation_api(source) else None
    html = fetched.get("content") or ""
    if fetched.get("status_code", 0) >= 400 or is_not_found_page(html):
        return None
    title = rockumentation_title(rockumentation_payload) or readable_title(html, source)
    text = rockumentation_readable_text(rockumentation_payload) or readable_text(html)
    if not title and not text:
        return None
    source_url = clean_url_for_fetch(fetched.get("url") or fetched.get("requested_url") or source.root_url)
    requested_url = clean_url_for_fetch(fetched.get("requested_url") or source_url)
    raw = {
        "source_url": source_url,
        "location_aliases": [requested_url] if requested_url != source_url else [],
        "source_title": title or source.name,
    }
    detail_type = infer_detail_type(source, source_url)
    rockumentation_fields = extract_rockumentation_fields(rockumentation_payload, source_url, text) if rockumentation_payload else {}
    record = {
        "id": rockumentation_record_id(source, rockumentation_fields) or canonical_record_id(source.id, source_url),
        "source_id": source.id,
        "source_url": source_url,
        "location_aliases": [requested_url] if requested_url != source_url else [],
        "source_title": title or source.name,
        "source_kind": source.kind,
        "retrieved_at": fetched.get("retrieved_at") or now_iso(),
        "updated_at": None,
        "license_status": source.license_status,
        "allowed_extraction_mode": source.allowed_extraction_mode,
        "content_hash": (
            rockumentation_content_hash(rockumentation_payload, source_url)
            if rockumentation_payload
            else community_content_hash(source_url, title or source.name, text)
        ),
        "extraction_tool": fetched.get("extraction_tool") or "community_static_discovery",
        "extraction_mode": source.allowed_extraction_mode,
        "summary_model": None,
        "topics": sorted(set(source.topics + infer_topics_from_url(source_url, text))),
        "rock_version_min": None,
        "rock_version_max": None,
        "rock_versions": infer_rock_versions(text),
        "audience": infer_audience(source),
        "summary": summarize_locally(text or title, max_chars=420),
        "excerpt": text[:800],
        "canonical_path": canonical_path_for(source, raw),
        "citations": [{"source_id": source.id, "url": source_url}],
        "detail_type": detail_type,
        "needs_review": source.allowed_extraction_mode in {"metadata_then_license_gate", "reviewed_summaries_only"},
    }
    record.update(extract_structured_fields(source, source_url, html, text, detail_type))
    record.update(rockumentation_fields)
    return record


def rockumentation_title(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    configuration = payload.get("configurationValues") or {}
    title = configuration.get("title")
    return " ".join(str(title).split()) if title else ""


def rockumentation_readable_text(payload: Any) -> str:
    article = rockumentation_article_soup(payload)
    if not article:
        return ""
    for selector in ["script", "style", "noscript", "svg", ".js-menu-container", ".article-edit-panel"]:
        for node in article.select(selector):
            node.decompose()
    markdown = html_to_markdown(str(article), heading_style="ATX").strip()
    markdown = clean_rockumentation_markdown(markdown)
    return " ".join(markdown.split())


def rockumentation_content_hash(payload: Any, source_url: str) -> str:
    """Hash stable upstream article content, excluding Obsidian request metadata."""
    configuration = payload.get("configurationValues") if isinstance(payload, dict) else {}
    configuration = configuration if isinstance(configuration, dict) else {}
    article = rockumentation_article_soup(payload)
    raw_article_id = article.get("data-article-id") if article else None
    article_id = int(raw_article_id) if raw_article_id and str(raw_article_id).isdigit() else None
    stable_payload = {
        "source_url": clean_url_for_fetch(source_url),
        "title": rockumentation_title(payload),
        "text": rockumentation_readable_text(payload),
        "article_id": article_id,
        "current_version": configuration.get("currentVersion"),
        "version_id": configuration.get("versionId"),
        "versions": configuration.get("versions") or [],
        "page_id": configuration.get("pageId"),
        "entity_guid": configuration.get("entityGuid"),
        "entity_type_guid": configuration.get("entityTypeGuid"),
        "is_searchable": configuration.get("isSearchable"),
    }
    return sha256_text(json.dumps(stable_payload, ensure_ascii=False, sort_keys=True))


def community_content_hash(source_url: str, title: str, text: str) -> str:
    """Hash normalized public content instead of volatile rendered page chrome."""
    stable_payload = {
        "source_url": clean_url_for_fetch(source_url),
        "title": " ".join(title.split()),
        "text": " ".join(text.split()),
    }
    return sha256_text(json.dumps(stable_payload, ensure_ascii=False, sort_keys=True))


def clean_rockumentation_markdown(markdown: str) -> str:
    markdown = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", markdown)
    markdown = re.sub(r"\bti\s+ti-[A-Za-z0-9_-]+\b", " ", markdown)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    return markdown.strip()


def rockumentation_article_soup(payload: Any) -> Optional[Any]:
    if not isinstance(payload, dict):
        return None
    soup = BeautifulSoup(payload.get("initialContent") or "", "html.parser")
    return soup.select_one('article.rockumentation-article[data-main-article="true"]') or soup.select_one("article.rockumentation-article")


def extract_rockumentation_fields(payload: dict[str, Any], source_url: str, text: str) -> dict[str, Any]:
    configuration = payload.get("configurationValues") or {}
    article = rockumentation_article_soup(payload)
    article_id = None
    article_classes: list[str] = []
    if article:
        raw_article_id = article.get("data-article-id")
        if raw_article_id and str(raw_article_id).isdigit():
            article_id = int(raw_article_id)
        article_classes = list(article.get("class") or [])
    toc_html = configuration.get("tableOfContents") or ""
    toc_links = rockumentation_links_from_html(toc_html, source_url)
    content_links = rockumentation_links_from_html(payload.get("initialContent") or "", source_url)
    detail_type = infer_rockumentation_detail_type(source_url, article_id)
    family = rockumentation_family_from_url(source_url)
    slug = rockumentation_slug_from_url(source_url) or configuration.get("slug")
    path_parts = [part for part in str(slug or "").split("/") if part]
    documentation_path = "/".join([family, *path_parts]) if family and path_parts else None
    branch_depth = 2 if family == "documentation" else 1
    documentation_branch = (
        "/".join([family, *path_parts[:branch_depth]])
        if family and len(path_parts) >= branch_depth
        else documentation_path
    )
    documentation_branches = []
    if family:
        for index in range(1, len(path_parts) + 1):
            documentation_branches.append("/".join([family, *path_parts[:index]]))
    return {
        "detail_type": detail_type,
        "documentation_article_id": article_id,
        "documentation_article_key": f"{family}:{article_id}" if family and article_id else None,
        "documentation_family": family,
        "documentation_slug": slug,
        "documentation_path": documentation_path,
        "documentation_branch": documentation_branch,
        "documentation_branches": documentation_branches,
        "documentation_path_parts": path_parts,
        "documentation_parent_slugs": ["/".join(path_parts[:index]) for index in range(1, len(path_parts))],
        "documentation_current_version": configuration.get("currentVersion"),
        "documentation_version_id": configuration.get("versionId"),
        "documentation_versions": configuration.get("versions") or [],
        "documentation_version_links": rockumentation_version_links(configuration.get("versions") or [], source_url),
        "documentation_page_id": configuration.get("pageId"),
        "documentation_entity_guid": configuration.get("entityGuid"),
        "documentation_entity_type_guid": configuration.get("entityTypeGuid"),
        "documentation_is_searchable": configuration.get("isSearchable"),
        "documentation_table_of_contents_links": toc_links[:250],
        "documentation_table_of_contents_link_count": len(toc_links),
        "documentation_content_links": content_links[:80],
        "documentation_article_classes": article_classes,
        "rock_versions": infer_rock_versions(" ".join([text, str(configuration.get("currentVersion") or "")])),
    }


def rockumentation_record_id(source: Source, fields: dict[str, Any]) -> Optional[str]:
    article_id = fields.get("documentation_article_id")
    return f"{source.id}:article:{article_id}" if article_id else None


def rockumentation_family_from_url(url: str) -> Optional[str]:
    parsed = urlparse(clean_url_for_fetch(url))
    parts = [part for part in parsed.path.split("/") if part]
    if parts and parts[0] in {"documentation", "developer"}:
        return parts[0]
    return None


def rockumentation_version_links(versions: list[dict[str, Any]], source_url: str) -> list[dict[str, Any]]:
    family = rockumentation_family_from_url(source_url) or "documentation"
    links: list[dict[str, Any]] = []
    for version in versions:
        if not isinstance(version, dict):
            continue
        value = str(version.get("value") or "").strip()
        slug = rockumentation_slug_from_url(urljoin(f"https://{COMMUNITY_HOST}", value)) if value.startswith("/") else None
        if not slug:
            slug = str(version.get("slug") or "").strip("/")
        links.append(
            {
                "text": version.get("text"),
                "url": f"https://{COMMUNITY_HOST}/{family}/{slug}" if slug else None,
                "raw_value": value,
                "category": version.get("category"),
                "disabled": version.get("disabled"),
            }
        )
    return links


def infer_rockumentation_detail_type(source_url: str, article_id: Optional[int]) -> str:
    path = urlparse(source_url).path.lower()
    if path.startswith("/developer/"):
        return "developer_doc" if article_id else "developer_index"
    return "documentation_article" if article_id else "documentation_index"


def rockumentation_links_from_html(html: str, base_url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"]).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = clean_url_for_fetch(urljoin(base_url, href))
        if urlparse(absolute).netloc.lower() != COMMUNITY_HOST:
            continue
        article_id = None
        parent = anchor.find_parent(attrs={"data-article-id": True})
        if parent and str(parent.get("data-article-id")).isdigit():
            article_id = int(parent.get("data-article-id"))
        parent_article_id = None
        depth = 0
        if parent:
            for ancestor in parent.find_parents("li"):
                if ancestor.get("data-article-id") and parent_article_id is None and str(ancestor.get("data-article-id")).isdigit():
                    parent_article_id = int(ancestor.get("data-article-id"))
                depth += 1
        classes = []
        if parent:
            classes = list(parent.get("class") or [])
        links.append(
            {
                "url": absolute,
                "text": " ".join(anchor.get_text(" ", strip=True).split())[:160],
                "article_id": article_id,
                "parent_article_id": parent_article_id,
                "depth": depth,
                "trailblazer": "trailblazer" in classes,
            }
        )
    deduped = {item["url"]: item for item in links}
    return list(deduped.values())


def readable_title(html: str, source: Source) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if source.kind == "rock_lava_docs":
        title = clean_lava_heading_text(page_title(html))
        if title:
            return title
    for selector in ["h1", ".page-title", ".title", "h2"]:
        node = soup.select_one(selector)
        if node:
            title = " ".join(node.get_text(" ", strip=True).split())
            if title and title.lower() not in {"recipe", "question", "community hubs"}:
                return title
    title = page_title(html)
    for suffix in [" | Rock Community", " | RockU", " | Rock RMS", " - Archive"]:
        title = title.replace(suffix, "")
    return title.strip() or source.name


def readable_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for selector in [
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        ".navbar",
        ".breadcrumb",
        ".loginstatus",
        ".js-notification-container",
    ]:
        for node in soup.select(selector):
            node.decompose()
    selectors = [
        "article",
        ".content-body",
        ".page-content",
        '[itemprop="mainEntityOfPage"]',
        ".question-detail",
        ".recipe-detail",
        ".documentation",
        ".document-content",
        ".main-content",
        "#zone-main",
        "main",
    ]
    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            text = " ".join(node.get_text(" ", strip=True).split())
            if len(text) > 80:
                return text
    markdown = main_markdown(str(soup))
    return " ".join(markdown.split())


def extract_structured_fields(source: Source, url: str, html: str, text: str, detail_type: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    breadcrumb = first_texts(soup, ".breadcrumb")
    headings = {
        "h1": first_texts(soup, "h1", limit=8),
        "h2": first_texts(soup, "h2", limit=12),
        "h3": first_texts(soup, "h3", limit=12),
    }
    fields: dict[str, Any] = {
        "breadcrumb": breadcrumb[0] if breadcrumb else None,
        "headings": headings,
    }
    fields.update(extract_common_links(source, soup, url))
    if detail_type == "recipe":
        fields.update(extract_recipe_fields(soup, url, text))
    elif detail_type == "question":
        fields.update(extract_question_fields(soup, url, text))
    elif detail_type == "training":
        fields.update(extract_training_fields(soup, url, text))
    elif detail_type == "developer_doc":
        fields.update(extract_developer_doc_fields(soup, url, text))
    elif detail_type == "community_hub":
        fields.update(extract_community_hub_fields(soup, url, text))
    elif detail_type == "community_blog_article":
        fields.update(extract_community_blog_fields(soup, url, text))
    elif detail_type == "rock_shop_plugin":
        fields.update(extract_rock_shop_plugin_fields(soup, url, text))
    if source.kind == "rock_lava_docs":
        fields.update(extract_lava_doc_fields(soup, url, text))
    return fields


def extract_lava_doc_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    category = infer_lava_doc_category(url)
    elements = lava_elements_from_page(soup, url, category)
    return {
        "lava_doc_category": category,
        "lava_elements": elements,
        "lava_element_count": len(elements),
    }


def infer_lava_doc_category(url: str) -> str:
    path = urlparse(url).path.strip("/").lower()
    if path == "lava":
        return "overview"
    if path == "lava/commands":
        return "command_overview"
    if path.startswith("lava/commands/"):
        return "command"
    if path == "lava/filters":
        return "filter_overview"
    if path.startswith("lava/filters/"):
        return "filter"
    if path == "lava/fluid":
        return "fluid_overview"
    if path.startswith("lava/fluid/"):
        return "fluid_migration"
    if path == "lava/lava-api":
        return "lava_api"
    if path == "lava/obsidian":
        return "obsidian"
    if path == "lava/remote-lava":
        return "remote_lava"
    if path.startswith("lava/shortcodes/"):
        return "shortcode"
    if path.startswith("lava/tags/"):
        return "tag"
    if path == "lava/workflows":
        return "workflow"
    return "reference"


def lava_elements_from_page(soup: BeautifulSoup, url: str, category: str) -> list[dict[str, Any]]:
    page_title_text = clean_lava_heading_text(page_title(str(soup)) or first_heading_text(soup))
    if category == "filter":
        return lava_heading_elements(soup, url, category, page_title_text)
    if category in {"command", "tag"}:
        return lava_page_elements(soup, url, category, page_title_text)
    if category in {"lava_api", "obsidian", "remote_lava", "shortcode", "fluid_migration", "fluid_overview", "workflow"}:
        return lava_page_elements(soup, url, category, page_title_text)
    return []


def lava_heading_elements(soup: BeautifulSoup, url: str, category: str, page_title_text: str) -> list[dict[str, Any]]:
    elements = []
    seen: set[str] = set()
    for heading in soup.find_all("h1"):
        name = clean_lava_heading_text(heading.get_text(" ", strip=True))
        if not is_lava_element_heading(name, page_title_text):
            continue
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        block_text = lava_item_container_text(heading, max_chars=1800) or following_text_until_heading(heading, "h1", max_chars=1800)
        elements.append(lava_element_metadata(name, category, url, block_text))
    return elements


def lava_page_elements(soup: BeautifulSoup, url: str, category: str, page_title_text: str) -> list[dict[str, Any]]:
    names = [page_title_text] if page_title_text else []
    if category == "tag" and "assign / capture" in page_title_text.lower():
        names = ["Assign", "Capture"]
    elements = []
    page_text = " ".join(soup.get_text(" ", strip=True).split())[:2400]
    for name in names:
        if not name:
            continue
        elements.append(lava_element_metadata(clean_lava_heading_text(name), category, url, page_text))
    return elements


def clean_lava_heading_text(value: str) -> str:
    value = " ".join(value.split())
    value = re.sub(r"(?:\s*\|\s*Rock Community)+$", "", value)
    return value.strip()


def first_heading_text(soup: BeautifulSoup) -> str:
    node = soup.find("h1")
    return " ".join(node.get_text(" ", strip=True).split()) if node else ""


def is_lava_element_heading(name: str, page_title_text: str) -> bool:
    if not name:
        return False
    lowered = name.lower()
    skipped = {
        page_title_text.lower(),
        "show details",
        "additional details",
        "example",
        "note",
        "tip",
    }
    if lowered in skipped:
        return False
    if lowered.endswith("filters") or lowered.startswith("intro to"):
        return False
    return True


def following_text_until_heading(node: Any, heading_name: str, max_chars: int = 1800) -> str:
    chunks = []
    for sibling in node.next_siblings:
        name = getattr(sibling, "name", None)
        if name == heading_name:
            break
        if name in {"script", "style", "noscript", "svg"}:
            continue
        text = " ".join(getattr(sibling, "get_text", lambda *_args, **_kwargs: str(sibling))(" ", strip=True).split())
        if text:
            chunks.append(text)
        if len(" ".join(chunks)) >= max_chars:
            break
    if chunks:
        return " ".join(chunks)[:max_chars]
    parent = getattr(node, "parent", None)
    if parent:
        return " ".join(parent.get_text(" ", strip=True).split())[:max_chars]
    return ""


def lava_item_container_text(node: Any, max_chars: int = 1800) -> str:
    parent = getattr(node, "parent", None)
    while parent:
        classes = parent.get("class") if hasattr(parent, "get") else []
        if classes and "panel-lavaitem" in classes:
            return " ".join(parent.get_text(" ", strip=True).split())[:max_chars]
        parent = getattr(parent, "parent", None)
    return ""


def lava_element_metadata(name: str, category: str, url: str, text: str) -> dict[str, Any]:
    server_versions = sorted({match.group("version") for match in re.finditer(r"\bServer:\s*v(?P<version>[0-9]+(?:\.[0-9]+)*)", text, re.IGNORECASE)})
    mobile_versions = sorted({match.group("version") for match in re.finditer(r"\bMobile:\s*v(?P<version>[0-9]+(?:\.[0-9]+)*)", text, re.IGNORECASE)})
    aliases = alias_names(text)
    return {
        "category": category,
        "name": name,
        "aliases": aliases,
        "official_url": url,
        "server_versions": server_versions,
        "mobile_versions": mobile_versions,
        "summary_hint": lava_summary_hint(text),
        "source_fragment_hash": sha256_text(name + "\n" + text),
    }


def alias_names(text: str) -> list[str]:
    values = []
    for match in re.finditer(r"\baka\s+(?P<alias>[A-Za-z][A-Za-z0-9_-]+)", text):
        values.append(match.group("alias"))
    return sorted(set(values))


def lava_summary_hint(text: str, max_chars: int = 180) -> str:
    cleaned = " ".join(text.split())
    cleaned = re.sub(r"^Show Details\s*", "", cleaned)
    cleaned = re.sub(r"^Server:\s*v[0-9.]+(?:\s+Mobile:\s*v[0-9.]+)?\s*", "", cleaned)
    cleaned = re.split(r"\bAdditional Details\b|\bExample:\b|\bNote:\b|\bTip\b", cleaned)[0].strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rsplit(" ", 1)[0] + "..."


def first_texts(soup: BeautifulSoup, selector: str, limit: int = 5) -> list[str]:
    values = []
    for node in soup.select(selector)[:limit]:
        value = " ".join(node.get_text(" ", strip=True).split())
        if value:
            values.append(value)
    return values


def extract_common_links(source: Source, soup: BeautifulSoup, base_url: str) -> dict[str, Any]:
    links = []
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"]).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = clean_url_for_fetch(urljoin(base_url, href))
        text = " ".join(anchor.get_text(" ", strip=True).split())
        if absolute.startswith("http") and absolute != base_url:
            links.append({"url": absolute, "text": text[:120]})
    deduped = {item["url"]: item for item in links}
    return {"related_links": list(deduped.values())[:30]}


def extract_recipe_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    labels = first_texts(soup, ".label", limit=12)
    recipe_id = numeric_id_from_url(url)
    rock_versions = [label for label in labels if re.match(r"^[0-9]+(?:\.[0-9]+)*$", label)]
    difficulty = next((label for label in labels if label.lower() in {"beginner", "intermediate", "advanced"}), None)
    categories = [label for label in labels if label not in rock_versions and label != difficulty]
    author = first_value(soup, ".author")
    shared_at = first_value(soup, "time")
    return {
        "recipe_id": recipe_id,
        "recipe_rock_versions": rock_versions,
        "recipe_categories": categories,
        "difficulty": difficulty,
        "author": author,
        "organization": extract_organization_after_author(text, author),
        "shared_at": shared_at,
        "community_notice": "Community recipe; not reviewed or endorsed by the Rock core team.",
    }


def extract_question_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    category = parts[1] if len(parts) > 2 else None
    answers = [value for value in first_texts(soup, ".answer", limit=20) if "replied" in value.lower()]
    question_author = None
    match = re.search(r"(?P<author>[A-Z][A-Za-z .'-]+) posted ", text)
    if match:
        question_author = match.group("author").strip()
    return {
        "question_id": numeric_id_from_url(url),
        "question_category": category,
        "answer_count": len(answers),
        "has_answer": bool(answers),
        "question_author": question_author,
        "posted_at": first_value(soup, "time"),
        "community_notice": "Community Q&A; verify accepted guidance before applying changes.",
    }


def extract_training_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    parts = [part for part in urlparse(url).path.split("/") if part]
    section = parts[1].replace("-", " ").title() if len(parts) > 1 else None
    lesson_slug = parts[2] if len(parts) > 2 else None
    duration = extract_regex(text, r"Length:\s*(?P<value>[0-9]+:[0-9]{2})")
    presenter = extract_regex(text, r"Presenter:\s*(?P<value>[^.]+?)(?:\s+Length:|$)")
    return {
        "training_section": section,
        "lesson_slug": lesson_slug,
        "duration": duration,
        "presenter": presenter,
    }


def extract_developer_doc_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    parts = [part for part in urlparse(url).path.split("/") if part]
    doc_path = parts[1:] if parts and parts[0] == "developer" else parts
    series = doc_path[0] if doc_path else None
    code_like = bool(re.search(r"\b(class|public|private|protected|SELECT|UPDATE|Lava|{%|{{)\b", text))
    return {
        "developer_doc_path": doc_path,
        "developer_series": series,
        "contains_code_like_content": code_like,
        "api_related": "api" in url.lower() or " api" in text[:1500].lower() or "rest" in text[:1500].lower(),
    }


def extract_community_hub_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    return {
        "hub_key": urlparse(url).path.rstrip("/").split("/")[-1],
        "media_count_hint": len(re.findall(r"/media/", text + " " + str(soup))),
    }


def extract_rock_shop_plugin_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    return {
        "plugin_id": numeric_id_from_url(url),
        "required_rock_version": extract_regex(text, r"Required Rock Version\s*(?P<value>[0-9]+(?:\.[0-9]+)*)"),
        "price": extract_regex(text, r"(?:Free|\$[0-9][0-9.,]*)"),
        "publisher": extract_regex(text, r"by\s+(?P<value>[A-Z][A-Za-z0-9 &.'-]+)"),
    }


def numeric_id_from_url(url: str) -> Optional[int]:
    match = re.search(r"/([0-9]+)(?:/|$)", urlparse(url).path)
    return int(match.group(1)) if match else None


def first_value(soup: BeautifulSoup, selector: str) -> Optional[str]:
    values = first_texts(soup, selector, limit=1)
    return values[0] if values else None


def extract_organization_after_author(text: str, author: Optional[str]) -> Optional[str]:
    if not author:
        return None
    pattern = re.escape(author) + r"\s*,\s*(?P<org>[^,]+?)\s+(?:yesterday|[0-9]+ Days Ago|[0-9]+ Months Ago|[0-9]+ Years Ago)"
    match = re.search(pattern, text)
    return match.group("org").strip() if match else None


def extract_regex(text: str, pattern: str) -> Optional[str]:
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    if "value" in match.groupdict():
        return " ".join(match.group("value").split())
    return " ".join(match.group(0).split())


def infer_detail_type(source: Source, url: str) -> str:
    path = urlparse(url).path.lower()
    if "/documentation/bookcontent" in path:
        return "documentation_bookcontent"
    if source.kind == "rock_documentation" and path.startswith("/documentation/"):
        return "documentation_article"
    if "/recipes/" in path:
        return "recipe"
    if "/ask/" in path and re.search(r"/[0-9]+(?:/|$)", path):
        return "question"
    if "/community-hubs/" in path:
        return "community_hub"
    if source.kind == "rock_community_blog" and path.startswith("/connect/"):
        return "community_blog_article"
    if "/rockshop/plugin/" in path:
        return "rock_shop_plugin"
    if "/rocku/" in path:
        return "training"
    if "/developer/" in path or "/api-docs" in path:
        return "developer_doc"
    return source.kind


def extract_community_blog_fields(soup: BeautifulSoup, url: str, text: str) -> dict[str, Any]:
    path_parts = [part for part in urlparse(url).path.split("/") if part]
    published_match = re.search(
        r"\bPublished\s+(?P<date>[A-Z][a-z]{2}\s+[0-9]{1,2},\s+[0-9]{4})\b",
        text,
    )
    published_label = published_match.group("date") if published_match else None
    published_at = None
    if published_label:
        try:
            published_at = datetime.strptime(published_label, "%b %d, %Y").date().isoformat()
        except ValueError:
            published_at = None
    return {
        "blog_slug": path_parts[1] if len(path_parts) > 1 else None,
        "blog_published_label": published_label,
        "published_at": published_at,
        "updated_at": published_at,
    }


def infer_topics_from_url(url: str, text: str) -> list[str]:
    lowered = (url + " " + text[:1200]).lower()
    topics = []
    for topic, needles in {
        "api": ["api", "rest", "webhook"],
        "lava": ["lava"],
        "workflow": ["workflow"],
        "mobile": ["mobile", "maui", "xaml"],
        "sql": ["sql", "database"],
        "security": ["security", "permission", "auth"],
        "finance": ["finance", "giving", "transaction"],
        "check-in": ["check-in", "attendance"],
    }.items():
        if any(needle in lowered for needle in needles):
            topics.append(topic)
    return topics


def endpoint_probe_targets() -> list[ProbeTarget]:
    base = "https://community.rockrms.com"
    paths = [
        "/api/docs",
        "/api/docs/index",
        "/api/doc/v1",
        "/api/RestControllers/RestControllerNames?includeObsolete=false&v=v1",
        "/api/RestControllers/EnsureRestControllers",
        "/api/ContentChannelItems",
        "/api/EntityTypes",
        "/api/Recipes",
        "/api/Questions",
        "/api/DocumentationArticles",
        "/api-docs",
        "/documentation/bookcontent/1/358",
        "/recipes/543",
        "/ask/using/2872",
    ]
    return [ProbeTarget(base + path) for path in paths]


def probe_endpoints(targets: Optional[list[ProbeTarget]] = None) -> list[dict[str, Any]]:
    targets = targets or endpoint_probe_targets()
    rows: list[dict[str, Any]] = []
    with httpx.Client(follow_redirects=True, timeout=20, headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/html"}) as client:
        for target in targets:
            try:
                response = client.request(target.method, target.url)
                text = response.text
                rows.append(
                    {
                        "url": target.url,
                        "method": target.method,
                        "status_code": response.status_code,
                        "final_url": str(response.url),
                        "content_type": response.headers.get("content-type", ""),
                        "content_length": len(text),
                        "content_hash": sha256_text(text),
                        "title": page_title(text) if "html" in response.headers.get("content-type", "") else "",
                        "body_preview": text[:280],
                        "classification": classify_probe_response(response),
                        "retrieved_at": now_iso(),
                    }
                )
            except httpx.HTTPError as exc:
                rows.append(
                    {
                        "url": target.url,
                        "method": target.method,
                        "status_code": None,
                        "error": str(exc),
                        "classification": "error",
                        "retrieved_at": now_iso(),
                    }
                )
    return rows


def classify_probe_response(response: httpx.Response) -> str:
    content_type = response.headers.get("content-type", "").lower()
    text = response.text[:1000].lower()
    if response.status_code in {401, 403}:
        return "auth_required"
    if response.status_code == 404:
        return "not_found"
    if response.status_code >= 400:
        return "error"
    if "application/json" in content_type:
        try:
            payload = response.json()
        except json.JSONDecodeError:
            return "json"
        if isinstance(payload, dict) and payload.get("paths") == {}:
            return "empty_swagger"
        return "json"
    if "swagger" in text or "rock rest api documentation" in text:
        return "api_docs"
    if "text/html" in content_type:
        return "html"
    return "other"
