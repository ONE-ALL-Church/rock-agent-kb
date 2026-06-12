from __future__ import annotations

from typing import Any

import httpx

from .extract import USER_AGENT, now_iso, sha256_text
from .normalize import canonical_record_id, infer_audience, summarize_locally
from .sources import Source

GITHUB_API = "https://api.github.com"

SEARCH_QUERIES = [
    "topic:rock-rms",
    '"Rock RMS" in:name,description,readme',
    '"RockRMS" in:name,description,readme',
    '"Rock RMS" "Lava" in:readme',
    '"Rock RMS" "SQL" in:readme',
]


def discover_github_repositories(max_repos: int = 75) -> list[dict[str, Any]]:
    repos: dict[str, dict[str, Any]] = {}
    with httpx.Client(timeout=30, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}) as client:
        for query in SEARCH_QUERIES:
            response = client.get(
                f"{GITHUB_API}/search/repositories",
                params={"q": query, "sort": "updated", "order": "desc", "per_page": min(50, max_repos)},
            )
            response.raise_for_status()
            for item in response.json().get("items", []):
                full_name = item.get("full_name")
                if not full_name:
                    continue
                existing = repos.setdefault(full_name, item)
                reasons = set(existing.get("_discovery_queries", []))
                reasons.add(query)
                existing["_discovery_queries"] = sorted(reasons)
                if len(repos) >= max_repos:
                    break
            if len(repos) >= max_repos:
                break
    return sorted(repos.values(), key=lambda item: (-(item.get("stargazers_count") or 0), item.get("full_name") or ""))


def normalize_github_search_records(source: Source, repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for repo in repos:
        repo_url = repo.get("html_url") or source.root_url
        license_info = repo.get("license") or {}
        full_name = repo.get("full_name") or repo_url
        topics = sorted(set(source.topics + list(repo.get("topics") or [])))
        description = repo.get("description") or ""
        records.append(
            {
                "id": canonical_record_id(source.id, full_name),
                "source_id": source.id,
                "source_url": repo_url,
                "source_title": full_name,
                "source_kind": source.kind,
                "retrieved_at": now_iso(),
                "updated_at": repo.get("pushed_at") or repo.get("updated_at"),
                "license_status": license_info.get("spdx_id") or "NOASSERTION",
                "allowed_extraction_mode": source.allowed_extraction_mode,
                "content_hash": sha256_text(str(repo)),
                "extraction_tool": "github_search_api",
                "extraction_mode": source.allowed_extraction_mode,
                "summary_model": None,
                "topics": topics,
                "rock_version_min": None,
                "rock_version_max": None,
                "rock_versions": [],
                "audience": infer_audience(source),
                "summary": summarize_locally(description or "Public GitHub repository discovered by Rock-related search."),
                "excerpt": description,
                "canonical_path": f"knowledge/development/repos/{full_name.lower().replace('/', '-')}.md",
                "citations": [{"source_id": source.id, "url": repo_url}],
                "repo_url": repo_url,
                "repo": full_name,
                "license": license_info.get("spdx_id"),
                "default_branch": repo.get("default_branch"),
                "commit_sha": None,
                "file_path": None,
                "language": repo.get("language"),
                "file_hash": None,
                "inclusion_reason": "github search: " + "; ".join(repo.get("_discovery_queries", [])),
                "publishability_status": "metadata-only until license review",
                "stargazers_count": repo.get("stargazers_count"),
                "forks_count": repo.get("forks_count"),
                "open_issues_count": repo.get("open_issues_count"),
                "needs_review": True,
            }
        )
    return records
