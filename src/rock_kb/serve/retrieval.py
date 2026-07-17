from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from ..jsonl import read_jsonl
from ..paths import REPO_ROOT
from ..rock_issues import (
    assess_catalog,
    attach_issue_enrichments,
    extract_issue_ref_from_query,
    find_issue_row,
    investigation_plan,
    issue_enrichment_search_values,
    issue_enrichments_by_id,
    issue_matches_version,
    parse_issue_ref,
)

PUBLIC_SEARCH_PREFIXES = ("knowledge/", "agent/", "claims/")
PRIVATE_PATH_PREFIXES = ("data/review/", "data/media/", "data/normalized/", "data/raw-manifests/", "data/index/")


def search(query: str, limit: int = 10, root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    rows = search_recipes(query, root)
    db_path = root / "data" / "index" / "kb.sqlite"
    if not db_path.exists():
        return rows[:limit]
    if len(rows) >= limit:
        return rows[:limit]
    fts_query = build_fts_query(query)
    if not fts_query:
        return []
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        for row in connection.execute(
            """
            SELECT
              r.id,
              r.source_id,
              r.source_url,
              r.source_title,
              r.topics,
              r.summary,
              r.excerpt,
              r.canonical_path,
              snippet(records_fts, 3, '', '', '...', 16) AS snippet
            FROM records_fts
            JOIN records r ON r.id = records_fts.id
            WHERE records_fts MATCH ?
            LIMIT ?
            """,
            (fts_query, max(limit * 4, limit)),
        ):
            item = dict(row)
            if not is_public_artifact_path(str(item.get("canonical_path") or "")):
                continue
            rows.append(
                {
                    "id": item.get("id"),
                    "title": item.get("source_title"),
                    "path": item.get("canonical_path"),
                    "url": item.get("source_url"),
                    "concept": first_topic(item.get("topics")),
                    "topics": split_topics(item.get("topics")),
                    "snippet": item.get("snippet") or item.get("summary") or item.get("excerpt"),
                    "source_id": item.get("source_id"),
                }
            )
            if len(rows) >= limit:
                break
    return rows[:limit]


def search_recipes(query: str, root: Path) -> list[dict[str, Any]]:
    terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_-]+", query) if len(term) > 2}
    if not terms:
        return []
    matches = []
    for recipe in read_jsonl(root / "agent" / "recipes.jsonl"):
        haystack = json.dumps(recipe, ensure_ascii=False).lower()
        score = sum(1 for term in terms if term in haystack)
        if score == 0:
            continue
        implementation = recipe.get("implementation") or {}
        recipe_id = str(recipe.get("recipe_id") or "")
        matches.append(
            (
                score,
                {
                    "id": f"recipe:{recipe_id}",
                    "kind": "recipe",
                    "title": recipe.get("title"),
                    "path": f"knowledge/recipes/{recipe.get('org_id')}/{recipe_id.split(':', 1)[-1]}.md",
                    "url": f"{implementation.get('repository_url', '')}/tree/{implementation.get('commit_sha', '')}/{implementation.get('source_path', '')}",
                    "concept": (recipe.get("concept_ids") or [None])[0],
                    "topics": recipe.get("concept_ids") or [],
                    "snippet": recipe.get("summary"),
                    "source_id": recipe.get("org_id"),
                    "authority_tier": recipe.get("authority_tier"),
                },
            )
        )
    return [row for _, row in sorted(matches, key=lambda item: (-item[0], str(item[1].get("id") or "")))]


def get_result(result_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    db_path = root / "data" / "index" / "kb.sqlite"
    if not db_path.exists():
        return {"schema": "rock-kb-result-v1", "status": "not_found", "result_id": result_id}
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT id, source_id, source_url, source_title, topics, summary,
                   excerpt, canonical_path, json
            FROM records WHERE id = ? LIMIT 1
            """,
            (result_id,),
        ).fetchone()
    if not row or not is_public_artifact_path(str(row["canonical_path"] or "")):
        return {"schema": "rock-kb-result-v1", "status": "not_found", "result_id": result_id}
    item = dict(row)
    return {
        "schema": "rock-kb-result-v1",
        "status": "ok",
        "result": {
            "id": item["id"],
            "kind": "source_record",
            "title": item["source_title"],
            "body": item["summary"] or item["excerpt"] or "",
            "path": item["canonical_path"],
            "url": item["source_url"],
            "concept": first_topic(item["topics"]),
            "source_id": item["source_id"],
            "payload": json.loads(item["json"] or "{}"),
        },
    }


def get_claim(claim_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    normalized = claim_id if claim_id.startswith("claim:") else f"claim:{claim_id}"
    row = next((item for item in read_jsonl(root / "claims" / "approved-claims.jsonl") if item.get("claim_id") == normalized), None)
    if not row:
        return {"schema": "rock-kb-claim-result-v1", "status": "not_found", "claim_id": normalized}
    return {
        "schema": "rock-kb-claim-result-v1",
        "status": "ok",
        "claim_id": normalized,
        "concepts": sorted(set(row.get("concept_ids") or [])),
        "claim": row,
    }


def get_manifest(root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    path = root / "agent" / "rock-kb-manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def list_concepts(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    return list(read_jsonl(root / "agent" / "concept-index.jsonl"))


def get_concept(concept_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    concept_dir = root / "knowledge" / "concepts" / concept_id
    index_row = next((row for row in list_concepts(root) if row.get("concept_id") == concept_id), None)
    return {
        "concept_id": concept_id,
        "title": (index_row or {}).get("title"),
        "index": index_row,
        "quickstart": read_text_if_public(concept_dir / "quickstart.md", root),
        "guide_path": public_relpath(concept_dir / "index.md", root),
        "answers": [row for row in read_jsonl(root / "agent" / "answer-pack.jsonl") if row.get("concept_id") == concept_id],
        "task_cards": [row for row in read_jsonl(root / "agent" / "concept-task-cards.jsonl") if row.get("concept_id") == concept_id],
        "release_caveats": [row for row in read_jsonl(root / "agent" / "concept-release-caveats.jsonl") if row.get("concept_id") == concept_id],
        "recipes": [row for row in read_jsonl(root / "agent" / "recipes.jsonl") if concept_id in (row.get("concept_ids") or [])],
    }


def get_claims(concept_id: str, tier: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    rows = []
    for row in read_jsonl(root / "claims" / "approved-claims.jsonl"):
        if concept_id not in (row.get("concept_ids") or []):
            continue
        if tier and row.get("claim_tier") != tier:
            continue
        rows.append(row)
    return rows


def list_recipes(concept_id: str | None = None, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    rows = list(read_jsonl(root / "agent" / "recipes.jsonl"))
    if concept_id:
        rows = [row for row in rows if concept_id in (row.get("concept_ids") or [])]
    return {
        "schema": "rock-kb-recipe-list-v1",
        "count": len(rows),
        "recipes": [
            {
                "recipe_id": row.get("recipe_id"),
                "title": row.get("title"),
                "summary": row.get("summary"),
                "version": row.get("version"),
                "recipe_kind": row.get("recipe_kind"),
                "concept_ids": row.get("concept_ids") or [],
                "authority_tier": row.get("authority_tier"),
            }
            for row in rows
        ],
    }


def get_recipe(recipe_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    normalized = recipe_id.removeprefix("recipe:")
    row = next((row for row in read_jsonl(root / "agent" / "recipes.jsonl") if row.get("recipe_id") == normalized), None)
    if row is None:
        return {"schema": "rock-kb-recipe-result-v1", "status": "not_found", "recipe_id": normalized}
    return {"schema": "rock-kb-recipe-result-v1", "status": "ok", "recipe": row}


def search_rock_issues(query: str, limit: int = 10, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    enrichments = issue_enrichments_by_id(root)
    terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_.-]+", query) if len(term) > 1}
    exact_ref = extract_issue_ref_from_query(query)
    query_version = re.search(r"(?<!\d)(\d{1,2}(?:\.\d+){1,3})(?!\d)", query)
    distinctive = terms - {"affect", "affected", "bug", "bugs", "fixed", "github", "issue", "issues", "regression", "version", "reported", "public", "tracker", "rock"}
    matches = []
    for raw_issue in read_jsonl(root / "agent" / "rock-issues.jsonl"):
        issue = attach_issue_enrichments(raw_issue, enrichments)
        searchable = " ".join(
            [
                str(issue.get("title") or ""),
                " ".join(str(value) for value in issue.get("labels") or []),
                " ".join(str(value) for value in issue.get("concept_ids") or []),
                " ".join(
                    str(value)
                    for row in issue.get("version_evidence") or []
                    for value in [row.get("normalized_version"), row.get("version_line")]
                    if value
                ),
                " ".join(
                    value
                    for enrichment in issue.get("reviewed_enrichments") or []
                    if isinstance(enrichment, dict)
                    for value in issue_enrichment_search_values(enrichment)
                ),
                str(issue.get("number") or ""),
            ]
        ).lower()
        score = sum(1 for term in terms if term in searchable)
        natural_title = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", str(issue.get("title") or ""))
        title_terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_.-]+", natural_title)}
        title_overlap = len(distinctive.intersection(title_terms))
        score += title_overlap * title_overlap * 12
        if query_version and issue_matches_version(issue, query_version.group(1)):
            score += 140
        if exact_ref and find_issue_row([issue], *exact_ref) is not None:
            score += 1200
        if score:
            matches.append((score, compact_rock_issue(issue)))
    results = [row for _, row in sorted(matches, key=lambda item: (-item[0], str(item[1].get("issue_id") or "")))[:limit]]
    return {"schema": "rock-kb-rock-issue-search-v1", "query": query, "results": results}


def list_rock_issues(
    repository: str | None = None,
    state: str | None = None,
    concept: str | None = None,
    version: str | None = None,
    limit: int = 50,
    offset: int = 0,
    root: Path | None = None,
) -> dict[str, Any]:
    root = root or REPO_ROOT
    enrichments = issue_enrichments_by_id(root)
    aliases = {
        "core": "SparkDevNetwork/Rock",
        "mobile": "SparkDevNetwork/Rock.Mobile-Issues",
    }
    repository = aliases.get(str(repository or "").lower(), repository)
    rows = []
    for raw_issue in read_jsonl(root / "agent" / "rock-issues.jsonl"):
        issue = attach_issue_enrichments(raw_issue, enrichments)
        if repository and issue.get("repository") != repository:
            continue
        if state and issue.get("state") != state:
            continue
        if concept and concept not in (issue.get("concept_ids") or []):
            continue
        if version and not issue_matches_version(issue, version):
            continue
        rows.append(compact_rock_issue(issue))
    rows.sort(key=lambda row: str(row.get("updated_at") or ""), reverse=True)
    selected = rows[offset : offset + max(1, min(limit, 100))]
    return {
        "schema": "rock-kb-rock-issue-list-v1",
        "count": len(selected),
        "offset": offset,
        "next_offset": offset + len(selected) if len(selected) == limit else None,
        "issues": selected,
    }


def get_rock_issue(issue_ref: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    try:
        repository, number = parse_issue_ref(issue_ref)
    except ValueError:
        return {"schema": "rock-kb-rock-issue-result-v1", "status": "not_found", "issue_ref": issue_ref}
    issue_id = f"rock_issue:{repository}#{number}"
    issue = find_issue_row(read_jsonl(root / "agent" / "rock-issues.jsonl"), repository, number)
    if issue is None:
        return {"schema": "rock-kb-rock-issue-result-v1", "status": "not_found", "issue_id": issue_id}
    issue = attach_issue_enrichments(issue, issue_enrichments_by_id(root))
    return {
        "schema": "rock-kb-rock-issue-result-v1",
        "status": "ok",
        "requested_issue_id": issue_id,
        "issue_id": issue.get("issue_id"),
        "issue": issue,
    }


def assess_rock_issues(
    profile: dict[str, Any],
    limit: int = 100,
    offset: int = 0,
    root: Path | None = None,
) -> dict[str, Any]:
    root = root or REPO_ROOT
    enrichments = issue_enrichments_by_id(root)
    rows = (attach_issue_enrichments(issue, enrichments) for issue in read_jsonl(root / "agent" / "rock-issues.jsonl"))
    return assess_catalog(rows, profile, limit=limit, offset=offset)


def plan_rock_issue_investigation(
    issue_ref: str,
    include_private_instance: bool = False,
    root: Path | None = None,
) -> dict[str, Any]:
    result = get_rock_issue(issue_ref, root=root)
    if result.get("status") != "ok":
        return result
    return investigation_plan(result["issue"], include_private_instance=include_private_instance)


def compact_rock_issue(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        key: issue.get(key)
        for key in [
            "issue_id",
            "repository",
            "number",
            "title",
            "url",
            "state",
            "validation_state",
            "updated_at",
            "concept_ids",
            "version_evidence",
            "remediation_state",
            "evidence_state",
        ]
    } | {"reviewed_enrichment_count": len(issue.get("reviewed_enrichments") or [])}


def list_models(root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    digests = list(read_jsonl(root / "agent" / "model-map-digests.jsonl"))
    models = []
    for digest in digests:
        identity = digest.get("identity") or {}
        counts = digest.get("counts") or {}
        models.append(
            {
                "model_slug": identity.get("model_slug"),
                "model_name": identity.get("model_name"),
                "model_title": identity.get("model_title"),
                "model_category": identity.get("model_category"),
                "rock_version": identity.get("rock_version"),
                "property_count": counts.get("properties") or 0,
                "method_count": counts.get("methods") or 0,
                "model_detail_path": identity.get("model_detail_path"),
            }
        )
    return {
        "schema": "rock-kb-model-map-model-list-v1",
        "count": len(models),
        "models": sorted(models, key=lambda row: str(row.get("model_name") or "")),
    }


def get_model(model: str, fields: str | None = None, property: str | None = None, root: Path | None = None) -> dict[str, Any] | None:
    root = root or REPO_ROOT
    digests = list(read_jsonl(root / "agent" / "model-map-digests.jsonl"))
    digest = next((row for row in digests if model_digest_matches(row, model)), None)
    if not digest:
        return None
    selected = select_model_digest(digest, fields)
    if property:
        selected = {**selected, "property_matches": find_model_properties(digest, property)}
    identity = digest.get("identity") or {}
    return {
        "schema": "rock-kb-model-map-model-result-v1",
        "status": "ok",
        "query": model,
        "matched_model": {
            "model_slug": identity.get("model_slug"),
            "model_name": identity.get("model_name"),
            "model_title": identity.get("model_title"),
        },
        "model": selected,
    }


def build_fts_query(query: str) -> str:
    terms = re.findall(r"[A-Za-z0-9_]+", query)
    return " ".join(terms)


def model_digest_matches(digest: dict[str, Any], query: str) -> bool:
    identity = digest.get("identity") or {}
    normalized = normalize_model_lookup(query)
    candidates = [
        identity.get("model_slug"),
        identity.get("model_name"),
        identity.get("model_title"),
        f"{identity.get('model_name') or ''} Model Map",
    ]
    return normalized in {normalize_model_lookup(str(candidate or "")) for candidate in candidates}


def select_model_digest(digest: dict[str, Any], fields: str | None) -> dict[str, Any]:
    requested = [part.strip().lower() for part in str(fields or "").split(",") if part.strip()]
    if not requested:
        return dict(digest)
    aliases = {
        "required": "required_fields",
        "relationships": "relationships",
        "diffs": "version_diffs",
        "properties": "property_groups",
        "property_groups": "property_groups",
        "methods": "methods",
        "notes": "operational_notes",
    }
    selected: dict[str, Any] = {
        "schema": digest.get("schema", "rock-kb-agent-model-map-digest-v1"),
        "identity": digest.get("identity"),
    }
    for requested_field in requested:
        field = aliases.get(requested_field, requested_field)
        if field in digest:
            selected[field] = digest[field]
    return selected


def find_model_properties(digest: dict[str, Any], property_name: str) -> list[dict[str, Any]]:
    normalized = normalize_model_lookup(property_name)
    matches = []
    for group, rows in ((digest.get("property_groups") or {}).items()):
        if not isinstance(rows, list):
            continue
        for row in rows:
            candidates = {normalize_model_lookup(str(row.get("name") or "")), normalize_model_lookup(str(row.get("slug") or ""))}
            if normalized in candidates or any(normalized and normalized in candidate for candidate in candidates):
                matches.append({"group": group, **row})
    return matches


def normalize_model_lookup(value: str) -> str:
    terms = [
        term.lower()
        for term in re.findall(r"[A-Za-z0-9_]+", value)
        if term.lower() not in {"model", "map", "modelmap"}
    ]
    return " ".join(terms).strip()


def is_public_artifact_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("/")
    if any(normalized.startswith(prefix) for prefix in PRIVATE_PATH_PREFIXES):
        return False
    return any(normalized.startswith(prefix) for prefix in PUBLIC_SEARCH_PREFIXES)


def split_topics(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [part for part in str(value or "").split(",") if part]


def first_topic(value: Any) -> str | None:
    topics = split_topics(value)
    return topics[0] if topics else None


def read_text_if_public(path: Path, root: Path) -> str | None:
    if not path.exists():
        return None
    rel = public_relpath(path, root)
    if not is_public_artifact_path(rel):
        return None
    return path.read_text(encoding="utf-8")


def public_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)
