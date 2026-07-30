from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import quote, urlparse

import httpx
from bs4 import BeautifulSoup

from .community import (
    ROCKUMENTATION_API_TOOL,
    extract_rockumentation_fields,
    fetch_rockumentation_payload,
    rockumentation_readable_text,
)
from .concepts import (
    Concept,
    claims_for_concept_synthesis,
    compact_record_for_synthesis,
    concept_synthesis_evidence_policy,
    get_concept,
    record_constraint_values,
    selected_records_for_concept,
)
from .contribution_sources import private_draft_contribution_records, public_contribution_records
from .extract import USER_AGENT, main_markdown, now_iso, page_title, sha256_text

TEXT_EXTENSIONS = {
    ".ascx",
    ".aspx",
    ".cs",
    ".cshtml",
    ".css",
    ".js",
    ".json",
    ".lava",
    ".liquid",
    ".md",
    ".razor",
    ".sql",
    ".ts",
    ".tsx",
    ".vue",
    ".xaml",
    ".xml",
    ".yml",
    ".yaml",
}

DEFAULT_CODE_REPOS = ["SparkDevNetwork/Rock"]


def hydrated_concept_synthesis_pack(
    concept_id: str,
    limit: int = 40,
    max_page_chars: int = 6000,
    max_code_chars: int = 3200,
    github_file_limit: int = 18,
    include_github: bool = True,
    include_contributions: bool = True,
    include_private_drafts: bool = False,
    private_draft_paths: Optional[list[Path]] = None,
) -> dict[str, Any]:
    concept = get_concept(concept_id)
    records = selected_records_for_concept(concept_id, limit=limit)
    contribution_records = public_contribution_records(concept_id) if include_contributions else []
    private_drafts = (
        private_draft_contribution_records(concept_id, private_draft_paths)
        if include_private_drafts
        else []
    )
    approved_claims, routing_context = claims_for_concept_synthesis(concept_id)
    keywords = concept_search_terms(concept)
    hydrated_sources = hydrate_source_records(records, keywords, max_chars=max_page_chars)
    github_files = (
        discover_github_source_files(concept, limit=github_file_limit, max_chars=max_code_chars)
        if include_github
        else []
    )
    return {
        "concept": {
            "id": concept.id,
            "title": concept.title,
            "description": concept.description,
            "depends_on_topics": concept.depends_on_topics,
            "subguides": concept.subguides,
            "routing_role": concept.routing_role,
            "parent_concept_id": concept.parent_concept_id,
            "documentation_branches": record_constraint_values(concept.raw, "documentation_branches"),
            "guide_status": "llm_generated_needs_review",
        },
        "approved_claims": approved_claims,
        "routing_context": routing_context,
        "source_records": [compact_record_for_synthesis(record) for record in records],
        "contribution_records": [compact_record_for_synthesis(record) for record in contribution_records],
        "private_draft_contribution_records": [compact_record_for_synthesis(record) for record in private_drafts],
        "hydrated_sources": hydrated_sources,
        "github_source_files": github_files,
        "hydrated_at": now_iso(),
        "hydration_policy": (
            "Approved answer-bearing claims are the factual spine. Public source excerpts and "
            "source-code snippets are bounded inputs for synthesis, citation, and refresh "
            "dependency tracking, not full-text redistribution."
        ),
        "evidence_policy": concept_synthesis_evidence_policy(),
    }


def concept_search_terms(concept: Concept) -> list[str]:
    terms = list(concept.keywords) + list(concept.depends_on_topics)
    for subguide in concept.subguides:
        terms.extend(str(value) for value in subguide.get("keywords") or [])
    expanded = []
    for term in terms:
        expanded.append(term)
        if "-" in term:
            expanded.append(term.replace("-", " "))
            expanded.append(term.replace("-", ""))
        if " " in term:
            expanded.append(term.replace(" ", ""))
    return unique_normalized_terms(expanded)


def hydrate_source_records(
    records: list[dict[str, Any]],
    keywords: list[str],
    max_chars: int = 2600,
    timeout: float = 30.0,
) -> list[dict[str, Any]]:
    hydrated = []
    seen: set[str] = set()
    with httpx.Client(follow_redirects=True, timeout=timeout, headers={"User-Agent": USER_AGENT}) as client:
        for record in records:
            url = str(record.get("source_url") or "")
            if not is_fetchable_http_url(url) or url in seen:
                continue
            seen.add(url)
            hydrated.append(hydrate_source_record(client, record, keywords, max_chars=max_chars))
    return hydrated


def hydrate_source_record(
    client: httpx.Client,
    record: dict[str, Any],
    keywords: list[str],
    max_chars: int = 2600,
) -> dict[str, Any]:
    url = str(record.get("source_url") or "")
    base = {
        "source_record_id": record.get("id"),
        "source_id": record.get("source_id"),
        "source_url": url,
        "source_title": record.get("source_title"),
        "license_status": record.get("license_status"),
        "allowed_extraction_mode": record.get("allowed_extraction_mode"),
        "retrieved_at": now_iso(),
        "hydration_tool": "static_http_bounded_excerpt",
    }
    try:
        rockumentation_payload = fetch_rockumentation_payload(client, url)
        if rockumentation_payload:
            text = normalize_text(rockumentation_readable_text(rockumentation_payload))
            excerpt = relevant_excerpt(text, keywords, max_chars=max_chars)
            fields = extract_rockumentation_fields(rockumentation_payload, url, text)
            soup = BeautifulSoup(rockumentation_payload.get("initialContent") or "", "html.parser")
            return {
                **base,
                "status": "ok",
                "status_code": 200,
                "final_url": url,
                "content_type": "application/json; rockumentation=1",
                "content_hash": sha256_text(json.dumps(rockumentation_payload, ensure_ascii=False, sort_keys=True)),
                "page_title": fields.get("source_title") or record.get("source_title"),
                "headings": extract_headings(soup),
                "excerpt": excerpt,
                "excerpt_hash": sha256_text(excerpt),
                "hydration_tool": ROCKUMENTATION_API_TOOL,
                "documentation_path": fields.get("documentation_path"),
                "documentation_article_id": fields.get("documentation_article_id"),
                "documentation_current_version": fields.get("documentation_current_version"),
            }
        response = client.get(url)
        html = response.text
        markdown = normalize_text(main_markdown(html))
        soup = BeautifulSoup(html, "html.parser")
        headings = extract_headings(soup)
        excerpt = relevant_excerpt(markdown, keywords, max_chars=max_chars)
        return {
            **base,
            "status": "ok",
            "status_code": response.status_code,
            "final_url": str(response.url),
            "content_type": response.headers.get("content-type", ""),
            "content_hash": sha256_text(html),
            "page_title": page_title(html),
            "headings": headings,
            "excerpt": excerpt,
            "excerpt_hash": sha256_text(excerpt),
        }
    except Exception as exc:  # pragma: no cover - exercised by live CLI, kept non-fatal by design
        return {
            **base,
            "status": "error",
            "error": str(exc),
        }


def extract_headings(soup: BeautifulSoup, limit: int = 30) -> list[dict[str, str]]:
    headings = []
    for node in soup.find_all(re.compile("^h[1-4]$")):
        text = normalize_text(node.get_text(" ", strip=True))
        if text:
            headings.append({"level": node.name, "text": text})
        if len(headings) >= limit:
            break
    return headings


def relevant_excerpt(text: str, keywords: list[str], max_chars: int = 2600) -> str:
    text = normalize_text(text)
    if len(text) <= max_chars:
        return text
    chunks = split_excerpt_chunks(text)
    scored = []
    for index, chunk in enumerate(chunks):
        score = score_chunk(chunk, keywords)
        if score:
            scored.append((score, index, chunk))
    if not scored:
        return text[:max_chars].rstrip()
    scored.sort(key=lambda item: (-item[0], item[1]))
    selected = sorted(scored[:8], key=lambda item: item[1])
    output = ""
    for _, _, chunk in selected:
        addition = chunk if not output else "\n\n...\n\n" + chunk
        if len(output) + len(addition) > max_chars:
            remaining = max_chars - len(output)
            if not output:
                output = chunk[:max_chars].rstrip()
            elif remaining > 200:
                output += addition[:remaining].rstrip()
            break
        output += addition
    return output.strip()


def split_excerpt_chunks(text: str) -> list[str]:
    parts = re.split(r"\n{2,}|(?<=\.)\s+(?=[A-Z#])", text)
    chunks = []
    current = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(current) + len(part) < 700:
            current = f"{current}\n\n{part}".strip()
        else:
            if current:
                chunks.append(current)
            current = part
    if current:
        chunks.append(current)
    return chunks


def discover_github_source_files(
    concept: Concept,
    repos: Optional[list[str]] = None,
    limit: int = 18,
    max_chars: int = 3200,
    timeout: float = 60.0,
) -> list[dict[str, Any]]:
    repos = repos or DEFAULT_CODE_REPOS
    keywords = concept_search_terms(concept)
    files = []
    with httpx.Client(follow_redirects=True, timeout=timeout, headers={"User-Agent": USER_AGENT}) as client:
        for repo in repos:
            files.extend(discover_repo_source_files(client, repo, keywords, limit=limit, max_chars=max_chars))
    files.sort(key=lambda row: (-int(row.get("score") or 0), row.get("path") or ""))
    return files[:limit]


def discover_repo_source_files(
    client: httpx.Client,
    repo: str,
    keywords: list[str],
    limit: int = 18,
    max_chars: int = 3200,
) -> list[dict[str, Any]]:
    metadata = client.get(f"https://api.github.com/repos/{repo}").json()
    branch = metadata.get("default_branch") or "develop"
    tree_url = f"https://api.github.com/repos/{repo}/git/trees/{quote(branch, safe='')}?recursive=1"
    tree_response = client.get(tree_url)
    if tree_response.status_code >= 400:
        return []
    tree_payload = tree_response.json()
    source_ref = str(tree_payload.get("sha") or branch)
    candidates = score_github_tree(tree_payload.get("tree") or [], keywords)
    rows = []
    for candidate in candidates[: limit * 3]:
        path = candidate["path"]
        raw_url = f"https://raw.githubusercontent.com/{repo}/{source_ref}/{quote(path, safe='/')}"
        try:
            response = client.get(raw_url)
        except Exception:
            continue
        if response.status_code >= 400 or not response.text:
            continue
        excerpt = relevant_code_excerpt(response.text, keywords, max_chars=max_chars)
        if not excerpt:
            continue
        rows.append(
            {
                "kind": "github_file",
                "repo": repo,
                "branch": branch,
                "source_ref": source_ref,
                "path": path,
                "language": language_for_path(path),
                "url": f"https://github.com/{repo}/blob/{source_ref}/{quote(path, safe='/')}",
                "raw_url": raw_url,
                "score": candidate["score"],
                "matched_terms": candidate["matched_terms"],
                "content_hash": sha256_text(response.text),
                "excerpt": excerpt,
                "excerpt_hash": sha256_text(excerpt),
                "retrieved_at": now_iso(),
            }
        )
        if len(rows) >= limit:
            break
    return rows


def score_github_tree(tree: Iterable[dict[str, Any]], keywords: list[str]) -> list[dict[str, Any]]:
    rows = []
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = str(item.get("path") or "")
        if Path(path).suffix.lower() not in TEXT_EXTENSIONS:
            continue
        score, matched = score_path(path, keywords)
        if score:
            rows.append({"path": path, "score": score, "matched_terms": matched})
    rows.sort(key=lambda row: (-row["score"], row["path"]))
    return rows


def score_path(path: str, keywords: list[str]) -> tuple[int, list[str]]:
    normalized_path = normalize_for_match(path)
    matched = []
    score = 0
    for keyword in keywords:
        normalized_keyword = normalize_for_match(keyword)
        if not normalized_keyword:
            continue
        if normalized_keyword in normalized_path:
            matched.append(keyword)
            score += 6 if len(normalized_keyword) > 7 else 3
    path_lower = path.lower()
    if "/blocks/" in path_lower or "/model/" in path_lower or "/models/" in path_lower:
        score += 2
    if "/test" in path_lower or path_lower.endswith(".spec.ts"):
        score -= 1
    return max(score, 0), matched[:12]


def relevant_code_excerpt(text: str, keywords: list[str], max_chars: int = 3200, context: int = 5) -> str:
    lines = text.splitlines()
    match_lines = []
    for index, line in enumerate(lines):
        if score_chunk(line, keywords):
            match_lines.append(index)
    if not match_lines:
        return ""
    ranges = []
    for index in match_lines[:40]:
        start = max(0, index - context)
        end = min(len(lines), index + context + 1)
        if ranges and start <= ranges[-1][1] + 1:
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
        else:
            ranges.append((start, end))
    chunks = []
    for start, end in ranges:
        chunk = "\n".join(f"{line_no + 1}: {lines[line_no]}" for line_no in range(start, end))
        chunks.append(chunk)
    excerpt = "\n\n...\n\n".join(chunks)
    return excerpt[:max_chars].rstrip()


def score_chunk(text: str, keywords: list[str]) -> int:
    normalized = normalize_for_match(text)
    score = 0
    for keyword in keywords:
        term = normalize_for_match(keyword)
        if not term:
            continue
        if len(term) > 6:
            score += normalized.count(term) * 3
        else:
            score += len(re.findall(rf"\b{re.escape(term)}\b", normalized))
    return score


def language_for_path(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".ascx": "ASP.NET Web Forms",
        ".aspx": "ASP.NET Web Forms",
        ".cs": "C#",
        ".cshtml": "Razor",
        ".css": "CSS",
        ".js": "JavaScript",
        ".json": "JSON",
        ".lava": "Lava",
        ".liquid": "Liquid",
        ".md": "Markdown",
        ".razor": "Razor",
        ".sql": "SQL",
        ".ts": "TypeScript",
        ".tsx": "TypeScript React",
        ".vue": "Vue",
        ".xaml": "XAML",
        ".xml": "XML",
        ".yaml": "YAML",
        ".yml": "YAML",
    }.get(suffix, suffix.lstrip("."))


def unique_normalized_terms(terms: Iterable[str]) -> list[str]:
    seen = set()
    output = []
    for term in terms:
        value = normalize_text(str(term))
        key = value.lower()
        if value and key not in seen:
            seen.add(key)
            output.append(value)
    return output


def normalize_for_match(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def normalize_text(value: str) -> str:
    return re.sub(r"[ \t\r\f\v]+", " ", value).strip()


def is_fetchable_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
