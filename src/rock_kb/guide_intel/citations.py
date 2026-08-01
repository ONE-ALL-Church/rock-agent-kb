from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def build_source_index(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for record in pack.get("source_records") or []:
        add_source(sources, source_from_record(record, "normalized_record"))
    for record in pack.get("contribution_records") or []:
        add_source(sources, source_from_contribution_record(record))
    for record in pack.get("hydrated_sources") or []:
        add_source(sources, source_from_record(record, "hydrated_page"))
    for record in pack.get("github_source_files") or []:
        add_source(sources, source_from_github_file(record))
    return sources

def source_from_record(record: dict[str, Any], kind: str) -> dict[str, Any]:
    source_id = record.get("source_id") or kind
    url = record.get("source_url") or record.get("url") or ""
    title = record.get("source_title") or record.get("page_title") or record.get("title") or url
    authority = authority_for_source_id(str(source_id))
    return {
        "source_key": stable_source_key(url, record.get("id") or record.get("source_record_id") or title),
        "source_record_id": record.get("id") or record.get("source_record_id"),
        "source_id": source_id,
        "kind": kind,
        "title": title,
        "url": url,
        "content_hash": record.get("content_hash"),
        "excerpt_hash": record.get("excerpt_hash"),
        "version": record.get("version"),
        "release_date": record.get("release_date"),
        "change_type": record.get("change_type"),
        "severity": record.get("severity"),
        "topics": record.get("topics") or [],
        "authority": authority,
        "authority_score": SOURCE_PRIORITY.get(authority, 0),
    }

def source_from_contribution_record(record: dict[str, Any]) -> dict[str, Any]:
    contribution_id = record.get("contribution_id") or record.get("id") or record.get("source_title")
    source_urls = record.get("source_urls") or []
    url = record.get("source_url") or (source_urls[0] if source_urls else "")
    return {
        "source_key": stable_source_key("", f"org_contribution:{contribution_id}"),
        "source_record_id": record.get("id") or f"org_contribution:{contribution_id}",
        "source_id": "org_contribution",
        "kind": "org_contribution",
        "title": record.get("source_title") or record.get("title") or contribution_id,
        "url": url,
        "content_hash": record.get("content_hash"),
        "topics": record.get("topics") or [],
        "org_id": record.get("org_id"),
        "contribution_id": contribution_id,
        "contribution_type": record.get("contribution_type"),
        "source_urls": source_urls,
        "source_record_ids": record.get("source_record_ids") or [],
        "needs_live_verification": record.get("needs_live_verification"),
        "authority": "org-contribution",
        "authority_score": SOURCE_PRIORITY["org-contribution"],
    }

def source_from_github_file(record: dict[str, Any]) -> dict[str, Any]:
    repo = record.get("repo") or ""
    path = record.get("path") or ""
    url = record.get("url") or ""
    return {
        "source_key": stable_source_key(url, f"{repo}:{path}"),
        "source_record_id": f"{repo}:{path}" if repo and path else None,
        "source_id": "sparkdevnetwork_rock" if repo == "SparkDevNetwork/Rock" else "github_source",
        "kind": "github_file",
        "title": path or url,
        "url": url,
        "repo": repo,
        "path": path,
        "language": record.get("language"),
        "content_hash": record.get("content_hash"),
        "excerpt_hash": record.get("excerpt_hash"),
        "matched_terms": record.get("matched_terms") or [],
        "authority": "source-code",
        "authority_score": SOURCE_PRIORITY["source-code"],
    }

def add_source(sources: dict[str, dict[str, Any]], source: dict[str, Any]) -> None:
    key = source["source_key"]
    if key not in sources:
        sources[key] = source
        return
    existing = sources[key]
    for field in ["source_record_id", "content_hash", "excerpt_hash", "version", "release_date", "change_type", "severity"]:
        if not existing.get(field) and source.get(field):
            existing[field] = source[field]
    if source.get("kind") == "hydrated_page":
        existing["hydrated"] = True

def extract_citations(text: str) -> list[tuple[str, str]]:
    return [(label.strip(), url.strip()) for label, url in LINK_RE.findall(text)]

def match_source_for_url(url: str, source_index: dict[str, dict[str, Any]]) -> Optional[dict[str, Any]]:
    normalized = normalize_url_for_match(url)
    candidates = [
        (source, normalize_url_for_match(str(source.get("url") or "")))
        for source in source_index.values()
        if source.get("url")
    ]
    for source, source_url in candidates:
        if normalized == source_url:
            return source
    prefix_matches = [
        (abs(len(normalized) - len(source_url)), source)
        for source, source_url in candidates
        if normalized.startswith(source_url) or source_url.startswith(normalized)
    ]
    if prefix_matches:
        return min(prefix_matches, key=lambda item: item[0])[1]
    return {
        "source_key": stable_source_key(url, url),
        "source_record_id": "",
        "source_id": source_id_for_url(url),
        "kind": "citation_only",
        "title": url,
        "url": url,
        "authority": authority_for_source_id(source_id_for_url(url)),
        "authority_score": SOURCE_PRIORITY.get(authority_for_source_id(source_id_for_url(url)), 0),
    }

def authority_for_source_id(source_id: str) -> str:
    return AUTHORITY_BY_SOURCE_ID.get(source_id, "unknown")

def source_id_for_url(url: str) -> str:
    if "triumph.tech/resources" in url:
        return "triumph_resources"
    if "github.com/SparkDevNetwork/Rock" in url:
        return "sparkdevnetwork_rock"
    if "rockrms.com/releasenotes" in url:
        return "rock_core_release_notes"
    if "rockrms.com/mobilereleasenotes" in url:
        return "rock_mobile_release_notes"
    if "community.rockrms.com/documentation" in url:
        return "rock_documentation"
    if "community.rockrms.com/developer" in url:
        return "rock_developer"
    if "community.rockrms.com/rocku" in url:
        return "rock_rocku"
    if "community.rockrms.com/recipes" in url:
        return "rock_recipes"
    if "community.rockrms.com/ask" in url:
        return "rock_qa"
    if "community.rockrms.com/ModelMap" in url:
        return "rock_model_map"
    return "citation"

def stable_source_key(url: str, fallback: Any) -> str:
    if url:
        return sha256_text(normalize_url_for_match(url))[:16]
    return sha256_text(str(fallback))[:16]

def normalize_url_for_match(url: str) -> str:
    return url.strip().rstrip("/").replace("http://", "https://")
