from __future__ import annotations

import hashlib
import re
from typing import Any, Iterable, Optional
from urllib.parse import urljoin, urlparse, urlunparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

from .sources import Source
from .timestamps import generated_at_iso, now_iso

USER_AGENT = "RockGeneralKnowledgeBase/0.1 (+https://github.com/ONE-ALL-Church/Rock-General-Knowledge-Base)"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    query = parsed.query
    return urlunparse((scheme, netloc, path, "", query, ""))


def choose_extraction_tier(source: Source) -> int:
    if source.raw.get("requires_manual_review"):
        return 4
    if "firecrawl" in source.preferred_tooling or "crawlee" in source.preferred_tooling:
        return max(source.extraction_tier, 3)
    if "crawl4ai" in source.preferred_tooling:
        return max(source.extraction_tier, 2)
    return source.extraction_tier


def fetch_url(url: str, timeout: float = 30.0) -> dict[str, Any]:
    with httpx.Client(
        follow_redirects=True,
        timeout=timeout,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        response = client.get(url)
    text = response.text
    return {
        "url": url,
        "final_url": str(response.url),
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "retrieved_at": now_iso(),
        "content_hash": sha256_text(text),
        "content": text,
    }


def page_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return " ".join(soup.title.string.split())
    h1 = soup.find("h1")
    return " ".join(h1.get_text(" ", strip=True).split()) if h1 else ""


def main_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for selector in ["script", "style", "noscript", "svg"]:
        for node in soup.select(selector):
            node.decompose()
    main = soup.find("main") or soup.find(id="zone-main") or soup.body or soup
    return html_to_markdown(str(main), heading_style="ATX").strip()


def discover_links(html: str, base_url: str, same_host: bool = True) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    base_host = urlparse(base_url).netloc.lower()
    links: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"]).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = canonicalize_url(urljoin(base_url, href))
        if same_host and urlparse(absolute).netloc.lower() != base_host:
            continue
        links.add(absolute)
    return sorted(links)


def child_links_for_source(source: Source, html: str) -> list[str]:
    links = discover_links(html, source.root_url, same_host=True)
    if not source.raw.get("discover_children"):
        return []
    allowlist = [canonicalize_url(item) for item in source.raw.get("child_url_allowlist", [])]
    if not allowlist:
        return links
    return [
        link
        for link in links
        if any(link.startswith(prefix.rstrip("/")) for prefix in allowlist)
    ]


def build_raw_manifest(source: Source, fetched: dict[str, Any]) -> dict[str, Any]:
    html = fetched.get("content", "")
    discovered = child_links_for_source(source, html)
    return {
        "id": source.id,
        "source_id": source.id,
        "source_kind": source.kind,
        "source_url": canonicalize_url(fetched["final_url"]),
        "requested_url": fetched["url"],
        "source_title": page_title(html),
        "retrieved_at": fetched["retrieved_at"],
        "status_code": fetched["status_code"],
        "content_type": fetched["content_type"],
        "content_hash": fetched["content_hash"],
        "license_status": source.license_status,
        "allowed_extraction_mode": source.allowed_extraction_mode,
        "extraction_tool": "static_http",
        "extraction_tier": choose_extraction_tier(source),
        "topics": source.topics,
        "discovered_urls": discovered,
        "markdown": main_markdown(html) if source.permits_full_text else "",
        "excerpt": main_markdown(html)[:600] if not source.permits_full_text else "",
    }


def grep_sensitive_values(lines: Iterable[str]) -> list[str]:
    patterns = [
        re.compile(r"(?i)(?:^|[^A-Za-z0-9_-])(password|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[^'\"\s]+"),
        re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}(?![A-Za-z0-9_-])"),
        re.compile(r"(?i)connectionstring\s*[:=]"),
    ]
    findings: list[str] = []
    for line in lines:
        for pattern in patterns:
            if pattern.search(line):
                findings.append(line.strip())
                break
    return findings


def optional_command(name: str) -> Optional[str]:
    from shutil import which

    return which(name)
