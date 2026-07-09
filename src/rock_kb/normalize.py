from __future__ import annotations

import json
import re
from typing import Any, Iterable, Optional
from urllib.parse import urljoin
from urllib.parse import urlparse

import feedparser
from bs4 import BeautifulSoup

from .extract import canonicalize_url, main_markdown, now_iso, sha256_text
from .sources import Source

RELEASE_HEADING_RE = re.compile(
    r"Rock(?: Mobile)? v(?P<version>[0-9]+(?:\.[0-9]+)*) Released (?P<date>[A-Za-z]+ [0-9]{1,2}, [0-9]{4})(?: \((?P<status>[^)]+)\))?"
)
MODULE_HEADING_RE = re.compile(r"^(?P<module>[A-Za-z /&-]+) v(?P<version>[0-9]+(?:\.[0-9]+)*)$")
ISSUE_RE = re.compile(r"#(?P<number>[0-9]{2,})")
VERSION_RE = re.compile(r"\bv(?P<version>[0-9]+(?:\.[0-9]+)*)\b", re.IGNORECASE)


def canonical_record_id(source_id: str, value: str) -> str:
    digest = sha256_text(value)[:16]
    return f"{source_id}:{digest}"


def infer_rock_versions(text: str) -> list[str]:
    return sorted({match.group("version") for match in VERSION_RE.finditer(text)})


def normalize_raw_record(source: Source, raw: dict[str, Any]) -> dict[str, Any]:
    text = raw.get("markdown") or raw.get("excerpt") or raw.get("source_title") or ""
    return {
        "id": canonical_record_id(source.id, raw.get("source_url", source.root_url)),
        "source_id": source.id,
        "source_url": raw.get("source_url", source.root_url),
        "source_title": raw.get("source_title", source.name),
        "source_kind": source.kind,
        "retrieved_at": raw.get("retrieved_at", now_iso()),
        "updated_at": raw.get("updated_at"),
        "license_status": source.license_status,
        "allowed_extraction_mode": source.allowed_extraction_mode,
        "content_hash": raw.get("content_hash", sha256_text(text)),
        "extraction_tool": raw.get("extraction_tool", "static_http"),
        "extraction_mode": source.allowed_extraction_mode,
        "summary_model": None,
        "topics": source.topics,
        "rock_version_min": None,
        "rock_version_max": None,
        "rock_versions": infer_rock_versions(text),
        "audience": infer_audience(source),
        "summary": summarize_locally(text),
        "excerpt": text[:800],
        "canonical_path": canonical_path_for(source, raw),
        "citations": [{"source_id": source.id, "url": raw.get("source_url", source.root_url)}],
        "needs_review": source.allowed_extraction_mode in {"metadata_then_license_gate", "reviewed_summaries_only"},
    }


def infer_audience(source: Source) -> list[str]:
    if source.kind in {"github_repo", "rock_developer", "rock_model_map"}:
        return ["developer", "technical-admin"]
    if "mobile" in source.kind:
        return ["mobile-developer", "technical-admin"]
    if source.kind == "rock_recipes":
        return ["rock-admin", "developer"]
    return ["rock-admin", "agent"]


def canonical_path_for(source: Source, raw: dict[str, Any]) -> str:
    topic = source.topics[0] if source.topics else "general"
    parsed = urlparse(raw.get("source_url", source.root_url))
    slug = parsed.path.strip("/").replace("/", "-") or source.id
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", slug).strip("-").lower()
    return f"knowledge/{topic}/{slug or source.id}.md"


def summarize_locally(text: str, max_chars: int = 360) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rsplit(" ", 1)[0] + "..."


def parse_release_notes(source: Source, html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("main") or soup
    records: list[dict[str, Any]] = []
    current_release: Optional[dict[str, Any]] = None
    current_module: Optional[str] = None
    full_text = container.get_text("\n", strip=True)
    for node in container.find_all(["h2", "h3", "li"]):
        if _inside_page_chrome(node):
            continue
        line = " ".join(node.get_text(" ", strip=True).split())
        if not line:
            continue
        heading = line
        release_match = RELEASE_HEADING_RE.search(heading)
        if node.name == "h2" and release_match:
            current_release = {
                "version": release_match.group("version"),
                "release_date": release_match.group("date"),
                "release_status": release_match.group("status"),
            }
            current_module = None
            continue
        module_match = MODULE_HEADING_RE.match(heading)
        if node.name == "h3" and module_match:
            current_module = module_match.group("module").strip()
            continue
        if current_release and node.name == "li":
            change = line.strip()
            if not _looks_like_release_change(change):
                continue
            if re.match(r"^\[Rock(?: Mobile)? v[0-9.]+\]", change):
                continue
            issue_refs = [match.group("number") for match in ISSUE_RE.finditer(change)]
            release_family = "mobile" if "mobile" in source.kind else "core"
            record_id = canonical_record_id(source.id, f"{current_release['version']}:{current_module}:{change}")
            records.append(
                {
                    "id": record_id,
                    "source_id": source.id,
                    "source_url": source.root_url,
                    "source_title": source.name,
                    "source_kind": source.kind,
                    "retrieved_at": now_iso(),
                    "updated_at": None,
                    "license_status": source.license_status,
                    "allowed_extraction_mode": source.allowed_extraction_mode,
                    "content_hash": sha256_text(change),
                    "extraction_tool": "release_parser",
                    "extraction_mode": source.allowed_extraction_mode,
                    "summary_model": None,
                    "topics": source.topics,
                    "rock_version_min": None,
                    "rock_version_max": None,
                    "rock_versions": [current_release["version"]],
                    "audience": infer_audience(source),
                    "summary": summarize_locally(change),
                    "excerpt": change,
                    "canonical_path": f"knowledge/releases/{release_family}-v{current_release['version']}.md",
                    "citations": [{"source_id": source.id, "url": source.root_url}],
                    "release_family": release_family,
                    "version": current_release["version"],
                    "release_date": current_release["release_date"],
                    "release_status": current_release["release_status"],
                    "module": current_module,
                    "change_type": infer_change_type(change),
                    "severity": infer_severity(change),
                    "minimum_os": parse_minimum_os(full_text) if release_family == "mobile" else None,
                    "minimum_rock_version": parse_minimum_rock_version(full_text) if release_family == "mobile" else None,
                    "issue_refs": issue_refs,
                    "bulletin_refs": [],
                    "needs_review": False,
                }
            )
    return records


def _inside_page_chrome(node: Any) -> bool:
    for parent in node.parents:
        if getattr(parent, "name", None) in {"nav", "footer"}:
            return True
        classes = parent.get("class") if hasattr(parent, "get") else None
        if classes and any(value in {"navbar", "community-sidebar", "breadcrumb"} for value in classes):
            return True
    return False


def _looks_like_release_change(change: str) -> bool:
    lowered = change.lower()
    return lowered.startswith(
        (
            "added",
            "fixed",
            "improved",
            "updated",
            "removed",
            "deprecated",
            "renamed",
            "changed",
        )
    ) or "fixes:" in lowered


def infer_change_type(change: str) -> str:
    lowered = change.lower()
    if lowered.startswith("added") or "new " in lowered:
        return "new_feature"
    if lowered.startswith("removed") or "deprecated" in lowered:
        return "breaking_or_deprecated"
    if lowered.startswith("improved") or lowered.startswith("updated"):
        return "improvement"
    if lowered.startswith("fixed") or "fixes:" in lowered:
        return "bug_fix"
    return "note"


def infer_severity(change: str) -> str:
    lowered = change.lower()
    if any(word in lowered for word in ["security", "authorization", "permission", "removed", "deprecation"]):
        return "high"
    if any(word in lowered for word in ["performance", "timeout", "failed", "crash"]):
        return "medium"
    return "normal"


def parse_minimum_os(text: str) -> Optional[dict[str, str]]:
    match = re.search(r"Minimum OS Versions:\s*iOS version (?P<ios>[^,]+), Android version (?P<android>[^\n]+)", text)
    if not match:
        return None
    return {"ios": match.group("ios").strip(), "android": match.group("android").strip()}


def parse_minimum_rock_version(text: str) -> Optional[str]:
    match = re.search(r"Minimum Rock Version:\s*v?(?P<version>[0-9]+(?:\.[0-9]+)*)", text)
    return match.group("version") if match else None


def parse_mobile_doc_children(source: Source, html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    records: list[dict[str, Any]] = []
    for anchor in soup.find_all("a", href=True):
        title = " ".join(anchor.get_text(" ", strip=True).split())
        if not title:
            continue
        url = canonicalize_url(urljoin(source.root_url, str(anchor["href"])))
        if "mobile-docs" not in url:
            continue
        records.append(
            {
                "id": canonical_record_id(source.id, url),
                "source_id": source.id,
                "source_url": url,
                "source_title": title,
                "source_kind": source.kind,
                "retrieved_at": now_iso(),
                "updated_at": None,
                "license_status": source.license_status,
                "allowed_extraction_mode": source.allowed_extraction_mode,
                "content_hash": sha256_text(url),
                "extraction_tool": "mobile_doc_nav_parser",
                "extraction_mode": source.allowed_extraction_mode,
                "summary_model": None,
                "topics": source.topics,
                "rock_version_min": None,
                "rock_version_max": None,
                "rock_versions": [],
                "audience": infer_audience(source),
                "summary": f"Mobile documentation page: {title}",
                "excerpt": "",
                "canonical_path": "knowledge/mobile/" + re.sub(r"[^A-Za-z0-9._-]+", "-", title).strip("-").lower() + ".md",
                "citations": [{"source_id": source.id, "url": url}],
                "doc_path": title,
                "nav_parent": None,
                "nav_depth": None,
                "component_type": infer_mobile_component_type(title),
                "platform_scope": ["ios", "android"],
                "related_release_versions": [],
                "needs_review": False,
            }
        )
    deduped = {record["source_url"]: record for record in records}
    return list(deduped.values())


def infer_mobile_component_type(title: str) -> Optional[str]:
    lowered = title.lower()
    if "command" in lowered:
        return "command"
    if "control" in lowered or "view" in lowered or "picker" in lowered or "button" in lowered:
        return "control"
    if "block" in lowered:
        return "block"
    if "xaml" in lowered:
        return "xaml"
    return None


def parse_rss(source: Source, xml: str) -> list[dict[str, Any]]:
    parsed = feedparser.parse(xml)
    records: list[dict[str, Any]] = []
    for entry in parsed.entries:
        link = canonicalize_url(urljoin(source.root_url, entry.get("link", source.root_url)))
        summary = BeautifulSoup(
            entry.get("summary") or entry.get("media_description") or "",
            "html.parser",
        ).get_text(" ", strip=True)
        enclosure = next((item for item in entry.get("enclosures", []) if item.get("href")), None)
        media_content = next((item for item in entry.get("media_content", []) if item.get("url")), None)
        video_id = entry.get("yt_videoid")
        channel_id = entry.get("yt_channelid")
        if video_id:
            media_url = f"https://www.youtube.com/watch?v={video_id}"
            media_type = "video/youtube"
        elif enclosure:
            media_url = canonicalize_url(enclosure.get("href"))
            media_type = enclosure.get("type")
        elif media_content:
            media_url = canonicalize_url(media_content.get("url"))
            media_type = media_content.get("type")
        else:
            media_url = None
            media_type = None
        raw = {"source_url": link, "source_title": entry.get("title", "") or source.name}
        records.append(
            {
                "id": canonical_record_id(source.id, entry.get("id", link)),
                "source_id": source.id,
                "source_url": link,
                "source_title": entry.get("title", ""),
                "source_kind": source.kind,
                "retrieved_at": now_iso(),
                "updated_at": entry.get("updated") or entry.get("published"),
                "license_status": source.license_status,
                "allowed_extraction_mode": source.allowed_extraction_mode,
                "content_hash": sha256_text(summary + link),
                "extraction_tool": "rss_parser",
                "extraction_mode": source.allowed_extraction_mode,
                "summary_model": None,
                "topics": source.topics,
                "rock_version_min": None,
                "rock_version_max": None,
                "rock_versions": infer_rock_versions(summary),
                "audience": ["rock-admin", "leader", "agent"],
                "summary": summarize_locally(summary),
                "excerpt": summary[:800],
                "canonical_path": "knowledge/operations/rock-cast.md"
                if source.kind == "podcast_rss"
                else canonical_path_for(source, raw),
                "citations": [{"source_id": source.id, "url": link}],
                "episode_number": entry.get("itunes_episode"),
                "published_at": entry.get("published"),
                "duration": entry.get("itunes_duration"),
                "media_url": media_url,
                "media_type": media_type,
                "media_length": enclosure.get("length") if enclosure else None,
                "video_id": video_id,
                "channel_id": channel_id,
                "needs_review": False,
            }
        )
    return records


def parse_model_map(source: Source, html: str) -> list[dict[str, Any]]:
    match = re.search(r'"configurationValues":(?P<payload>\{"categories":.*?\}),"initialContent"', html)
    if not match:
        return [
            normalize_raw_record(
                source,
                {
                    "source_url": source.root_url,
                    "source_title": source.name,
                    "content_hash": sha256_text(html),
                    "markdown": "",
                    "excerpt": summarize_locally(BeautifulSoup(html, "html.parser").get_text(" ", strip=True)),
                    "extraction_tool": "model_map_parser",
                },
            )
        ]
    payload = json.loads(match.group("payload"))
    records: list[dict[str, Any]] = []
    for category in payload.get("categories") or []:
        category_name = category.get("name") or "Uncategorized"
        models = category.get("models") or []
        for model in models:
            model_name = model.get("text") or ""
            model_guid = model.get("value") or model_name
            text = f"{model_name} is a Rock model in the {category_name} category."
            records.append(
                {
                    "id": canonical_record_id(source.id, str(model_guid)),
                    "source_id": source.id,
                    "source_url": source.root_url,
                    "source_title": model_name,
                    "source_kind": source.kind,
                    "retrieved_at": now_iso(),
                    "updated_at": None,
                    "license_status": source.license_status,
                    "allowed_extraction_mode": source.allowed_extraction_mode,
                    "content_hash": sha256_text(str(model)),
                    "extraction_tool": "model_map_embedded_config_parser",
                    "extraction_mode": source.allowed_extraction_mode,
                    "summary_model": None,
                    "topics": sorted(set(source.topics + [category_name.lower().replace(" ", "-")])),
                    "rock_version_min": None,
                    "rock_version_max": None,
                    "rock_versions": [],
                    "audience": infer_audience(source),
                    "summary": text,
                    "excerpt": text,
                    "canonical_path": f"knowledge/model-map/{model_name.lower().replace(' ', '-')}.md",
                    "citations": [{"source_id": source.id, "url": source.root_url}],
                    "model_guid": model_guid,
                    "model_name": model_name,
                    "model_category": category_name,
                    "disabled": model.get("disabled"),
                    "needs_review": False,
                }
            )
    return records


def normalize_github_repo_metadata(source: Source, repo_api: dict[str, Any]) -> dict[str, Any]:
    repo_url = repo_api.get("html_url") or source.root_url
    license_info = repo_api.get("license") or {}
    default_branch = repo_api.get("default_branch")
    return {
        "id": canonical_record_id(source.id, repo_url),
        "source_id": source.id,
        "source_url": repo_url,
        "source_title": repo_api.get("full_name", source.name),
        "source_kind": source.kind,
        "retrieved_at": now_iso(),
        "updated_at": repo_api.get("pushed_at"),
        "license_status": license_info.get("spdx_id") or source.license_status,
        "allowed_extraction_mode": source.allowed_extraction_mode,
        "content_hash": sha256_text(str(repo_api)),
        "extraction_tool": "github_api",
        "extraction_mode": source.allowed_extraction_mode,
        "summary_model": None,
        "topics": source.topics,
        "rock_version_min": None,
        "rock_version_max": None,
        "rock_versions": [],
        "audience": infer_audience(source),
        "summary": summarize_locally(repo_api.get("description") or source.description),
        "excerpt": repo_api.get("description") or "",
        "canonical_path": f"knowledge/development/{source.id}.md",
        "citations": [{"source_id": source.id, "url": repo_url}],
        "repo_url": repo_url,
        "repo": repo_api.get("full_name", source.raw.get("repo")),
        "license": license_info.get("spdx_id"),
        "default_branch": default_branch,
        "commit_sha": None,
        "file_path": None,
        "language": repo_api.get("language"),
        "file_hash": None,
        "inclusion_reason": "registered source repository",
        "publishability_status": "license-gated",
        "needs_review": source.allowed_extraction_mode != "source_allowed_by_license",
    }


def records_from_source_content(source: Source, content: str) -> list[dict[str, Any]]:
    if source.kind == "rock_model_map":
        return parse_model_map(source, content)
    if source.kind in {"rock_release_notes", "rock_mobile_release_notes"}:
        return parse_release_notes(source, content)
    if source.kind == "rock_mobile_docs":
        return parse_mobile_doc_children(source, content)
    if source.kind in {"podcast_rss", "rss"}:
        return parse_rss(source, content)
    return []


def frontmatter_fields() -> set[str]:
    return {
        "id",
        "source_ids",
        "license_status",
        "last_verified",
        "topics",
        "rock_versions",
        "agent_notes",
    }
