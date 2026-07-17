from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Iterable

import yaml

from .contribution_sources import public_contribution_records
from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl
from .paths import REPO_ROOT
from .publish import public_export_manifest, public_export_text_for_public_path
from .rock_issues import attach_issue_enrichments, issue_enrichments_by_id, normalize_version, version_line


SERVICE_DIR = REPO_ROOT / "service"
SERVICE_DIST_DIR = SERVICE_DIR / "dist"
SERVICE_ARTIFACTS_DIR = SERVICE_DIST_DIR / "artifacts"
SERVICE_ARTIFACT_SHARDS_DIR = SERVICE_DIST_DIR / "artifact-shards"
SERVICE_SQL_PATH = SERVICE_DIST_DIR / "d1-seed.sql"
SERVICE_PROJECTION_PATH = SERVICE_DIST_DIR / "projection.json"
SERVICE_SEARCH_ROWS_PATH = SERVICE_DIST_DIR / "search-rows.jsonl"
SERVICE_RETRIEVAL_DOCUMENTS_PATH = SERVICE_DIST_DIR / "retrieval-documents.jsonl"
SERVICE_RETRIEVAL_CHANGE_REPORT_PATH = SERVICE_DIST_DIR / "retrieval-change-report.json"
ORG_REGISTRY_PATH = SERVICE_DIST_DIR / "org-registry.json"
D1_SEARCH_BODY_CHAR_LIMIT = 75_000
ARTIFACT_SHARD_PREFIX_LENGTH = 2


CLAIM_TIER_RANK = {
    "routing_context_only": 0,
    "source_backed": 1,
    "answer_pack_approved": 2,
    "live_verified": 3,
}

AUTHORITY_TIER_RANK = {
    "community-unreviewed": 0,
    "community-reviewed": 1,
    "official": 2,
    "rocku-confirmed": 2,
    "release-note-confirmed": 3,
    "source-code-confirmed": 3,
    "live-verified": 4,
}


@dataclass(frozen=True)
class ServiceProjection:
    version: str
    generated_at: str
    artifact_count: int
    search_row_count: int
    retrieval_document_count: int
    org_count: int
    dist: Path
    sql_path: Path

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "rock-kb-service-projection-v1",
            "version": self.version,
            "generated_at": self.generated_at,
            "artifact_count": self.artifact_count,
            "search_row_count": self.search_row_count,
            "retrieval_document_count": self.retrieval_document_count,
            "org_count": self.org_count,
            "dist": str(self.dist),
            "sql_path": str(self.sql_path),
        }


def build_service_projection(destination: Path | None = None) -> ServiceProjection:
    dist = destination or SERVICE_DIST_DIR
    artifacts_dir = dist / "artifacts"
    previous_retrieval_documents = list(read_jsonl(dist / "retrieval-documents.jsonl")) if (dist / "retrieval-documents.jsonl").exists() else []
    if dist.exists():
        shutil.rmtree(dist)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    generated_at = generated_at_iso()
    manifest = public_export_manifest()
    search_rows = build_search_rows()
    retrieval_documents = build_retrieval_documents(search_rows)
    version_manifest = dict(manifest)
    version_manifest.pop("generated_at", None)
    version_manifest["search_projection_hash"] = rows_content_hash(search_rows)
    version_manifest["retrieval_projection_hash"] = rows_content_hash(retrieval_documents)
    version = sha256_text(json.dumps(version_manifest, sort_keys=True, ensure_ascii=False))[:16]
    files = manifest.get("files") or []
    for row in files:
        public_path = str(row["path"])
        target = artifacts_dir / public_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(public_export_text_for_public_path(public_path), encoding="utf-8")
    write_artifact_shards(artifacts_dir=artifacts_dir, shards_dir=dist / "artifact-shards")

    write_jsonl_text(dist / "search-rows.jsonl", search_rows)
    write_jsonl_text(dist / "retrieval-documents.jsonl", retrieval_documents)
    (dist / "retrieval-change-report.json").write_text(
        json.dumps(
            retrieval_projection_diff(previous_retrieval_documents, retrieval_documents),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    org_rows = load_org_registry()
    (dist / "org-registry.json").write_text(
        json.dumps({"schema": "rock-kb-org-registry-v1", "orgs": org_rows}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sql_text = build_d1_seed_sql(version=version, generated_at=generated_at, search_rows=search_rows, org_rows=org_rows)
    (dist / "d1-seed.sql").write_text(sql_text, encoding="utf-8")
    projection = ServiceProjection(
        version=version,
        generated_at=generated_at,
        artifact_count=len(files),
        search_row_count=len(search_rows),
        retrieval_document_count=len(retrieval_documents),
        org_count=len(org_rows),
        dist=dist,
        sql_path=dist / "d1-seed.sql",
    )
    (dist / "projection.json").write_text(json.dumps(projection.as_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return projection


def build_search_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(concept_search_rows())
    rows.extend(answer_search_rows())
    rows.extend(claim_search_rows())
    rows.extend(contribution_search_rows())
    rows.extend(model_map_search_rows())
    rows.extend(lava_context_search_rows())
    rows.extend(recipe_search_rows())
    rows.extend(source_summary_search_rows())
    rows.extend(rock_issue_search_rows())
    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        concepts = normalize_concept_ids(row.get("concepts") or [row.get("concept") or ""])
        topics = normalize_concept_ids(row.get("topics") or [])
        row["concepts"] = concepts
        row["topics"] = topics
        row["concept"] = first_concept(concepts)
        row["legacy_ids"] = sorted(
            {
                str(value).strip()
                for value in row.get("legacy_ids") or []
                if str(value).strip() and str(value).strip() != str(row["id"])
            }
        )
        row_id = str(row["id"])
        existing = deduped.get(row_id)
        candidate_rank = AUTHORITY_TIER_RANK.get(str(row.get("authority_tier") or ""), 0)
        existing_rank = AUTHORITY_TIER_RANK.get(str((existing or {}).get("authority_tier") or ""), 0)
        if existing is None or candidate_rank >= existing_rank:
            deduped[row_id] = row
    return sorted(deduped.values(), key=lambda row: str(row.get("id") or ""))


def build_retrieval_documents(search_rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    documents = [retrieval_document(row) for row in search_rows]
    return sorted(documents, key=lambda row: str(row.get("id") or ""))


def retrieval_document(row: dict[str, Any]) -> dict[str, Any]:
    concepts = normalize_concept_ids(row.get("concepts") or [row.get("concept") or ""])
    topics = normalize_concept_ids(row.get("topics") or [])
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    kind = str(row.get("kind") or "")
    authority_tier = str(row.get("authority_tier") or "")
    claim_tier = str(row.get("claim_tier") or "")
    rock_versions = retrieval_rock_versions(payload)
    index_policy = retrieval_index_policy(row)
    text = contextual_retrieval_text(row, concepts=concepts, topics=topics, rock_versions=rock_versions)
    metadata = {
        "kind": kind,
        "namespace": index_policy,
        "authority_rank": AUTHORITY_TIER_RANK.get(authority_tier, 0),
        "claim_tier_rank": CLAIM_TIER_RANK.get(claim_tier, 0),
        "concepts": "|".join(concepts)[:500],
    }
    return {
        "schema": "rock-kb-retrieval-document-v1",
        "id": str(row.get("id") or ""),
        "kind": kind,
        "title": str(row.get("title") or ""),
        "text": text,
        "concepts": concepts,
        "topics": topics,
        "authority_tier": authority_tier,
        "authority_rank": metadata["authority_rank"],
        "claim_tier": claim_tier,
        "claim_tier_rank": metadata["claim_tier_rank"],
        "source_id": str(row.get("source_id") or ""),
        "source_url": str(row.get("url") or ""),
        "source_path": str(row.get("path") or ""),
        "source_content_hash": str(payload.get("content_hash") or payload.get("source_content_hash") or ""),
        "content_hash": sha256_text(text),
        "rock_versions": rock_versions,
        "temporal_status": str(payload.get("temporal_status") or "unspecified"),
        "needs_review": bool(payload.get("needs_review") or payload.get("needs_live_verification")),
        "index_policy": index_policy,
        "metadata": metadata,
    }


def contextual_retrieval_text(
    row: dict[str, Any], *, concepts: list[str], topics: list[str], rock_versions: list[str]
) -> str:
    lines = [f"Rock KB {str(row.get('kind') or 'knowledge').replace('_', ' ')}: {row.get('title') or row.get('id') or ''}."]
    if concepts:
        lines.append(f"Concepts: {', '.join(concepts)}.")
    if topics:
        lines.append(f"Topics: {', '.join(topics)}.")
    authority = str(row.get("authority_tier") or "")
    claim_tier = str(row.get("claim_tier") or "")
    if authority or claim_tier:
        lines.append(f"Authority: {authority or 'unspecified'}; claim tier: {claim_tier or 'unspecified'}.")
    if rock_versions:
        lines.append(f"Rock versions: {', '.join(rock_versions)}.")
    source_id = str(row.get("source_id") or "")
    if source_id:
        lines.append(f"Evidence source: {source_id}.")
    body = d1_search_body(row.get("body") or "").strip()
    if body:
        lines.extend(["Content:", body])
    return "\n".join(lines).strip()


def retrieval_index_policy(row: dict[str, Any]) -> str:
    kind = str(row.get("kind") or "")
    if kind == "model_map":
        return "exact_lexical_only"
    if kind in {"source_summary", "community_contribution", "rock_issue"}:
        return "semantic_secondary"
    return "hybrid_primary"


def retrieval_rock_versions(payload: dict[str, Any]) -> list[str]:
    values: list[Any] = []
    for key in ["rock_versions", "versions", "tested_rock_versions"]:
        value = payload.get(key)
        values.extend(value if isinstance(value, list) else [value] if value else [])
    for key in ["rock_version", "version"]:
        if payload.get(key):
            values.append(payload[key])
    compatibility = payload.get("compatibility")
    if isinstance(compatibility, dict):
        tested = compatibility.get("tested_rock_versions")
        values.extend(tested if isinstance(tested, list) else [tested] if tested else [])
    return normalize_concept_ids(values)


def rows_content_hash(rows: Iterable[dict[str, Any]]) -> str:
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    return sha256_text(text)


def retrieval_projection_diff(
    previous: Iterable[dict[str, Any]], current: Iterable[dict[str, Any]]
) -> dict[str, Any]:
    previous_by_id = {str(row.get("id") or ""): row for row in previous if row.get("id")}
    current_by_id = {str(row.get("id") or ""): row for row in current if row.get("id")}
    previous_ids = set(previous_by_id)
    current_ids = set(current_by_id)
    changed_source = sorted(
        row_id
        for row_id in previous_ids & current_ids
        if str(previous_by_id[row_id].get("source_content_hash") or "")
        != str(current_by_id[row_id].get("source_content_hash") or "")
    )
    changed_content = sorted(
        row_id
        for row_id in previous_ids & current_ids
        if str(previous_by_id[row_id].get("content_hash") or "") != str(current_by_id[row_id].get("content_hash") or "")
    )
    changed_policy = sorted(
        row_id
        for row_id in previous_ids & current_ids
        if str(previous_by_id[row_id].get("index_policy") or "") != str(current_by_id[row_id].get("index_policy") or "")
    )
    review_required = sorted(
        set(changed_source)
        | set(changed_policy)
        | {row_id for row_id in current_ids if current_by_id[row_id].get("needs_review")}
    )
    return {
        "schema": "rock-kb-retrieval-change-report-v1",
        "baseline_available": bool(previous_by_id),
        "counts": {
            "previous": len(previous_by_id),
            "current": len(current_by_id),
            "new": len(current_ids - previous_ids),
            "removed": len(previous_ids - current_ids),
            "changed_source": len(changed_source),
            "changed_content": len(changed_content),
            "changed_policy": len(changed_policy),
            "review_required": len(review_required),
        },
        "new_ids": sorted(current_ids - previous_ids),
        "removed_ids": sorted(previous_ids - current_ids),
        "changed_source_ids": changed_source,
        "changed_content_ids": changed_content,
        "changed_policy_ids": changed_policy,
        "review_required_ids": review_required,
    }


def concept_search_rows() -> list[dict[str, Any]]:
    rows = []
    for concept in read_jsonl(REPO_ROOT / "agent" / "concept-index.jsonl"):
        concept_id = str(concept.get("concept_id") or "")
        if not concept_id:
            continue
        concept_dir = REPO_ROOT / "knowledge" / "concepts" / concept_id
        body_parts = [
            read_text(concept_dir / "quickstart.md"),
            read_text(concept_dir / "index.md"),
            read_text(concept_dir / "open-questions.md"),
        ]
        rows.append(
            {
                "id": f"concept:{concept_id}",
                "kind": "concept",
                "title": concept.get("title") or concept_id,
                "body": "\n\n".join(part for part in body_parts if part),
                "path": f"knowledge/concepts/{concept_id}/index.md",
                "url": "",
                "concept": concept_id,
                "authority_tier": "official",
                "claim_tier": "source_backed",
                "source_id": "",
                "payload": concept,
            }
        )
    return rows


def answer_search_rows() -> list[dict[str, Any]]:
    rows = []
    checklists = live_checklists_by_id()
    for answer in read_jsonl(REPO_ROOT / "agent" / "answer-pack.jsonl"):
        answer_id = str(answer.get("id") or answer.get("answer_id") or "")
        concept_id = str(answer.get("concept_id") or "")
        if not answer_id or not concept_id:
            continue
        checklist = checklists.get(str(answer.get("live_checklist_id") or ""))
        rows.append(
            {
                "id": f"answer:{answer_id}",
                "kind": "answer",
                "title": answer.get("title") or answer_id,
                "body": answer_search_body(answer, checklist),
                "path": f"knowledge/concepts/{concept_id}/answers/first-checks.md",
                "url": "",
                "concept": concept_id,
                "authority_tier": answer.get("authority_tier") or "community-reviewed",
                "claim_tier": answer.get("claim_tier") or "answer_pack_approved",
                "source_id": "",
                "payload": answer,
            }
        )
    return rows


def live_checklists_by_id() -> dict[str, dict[str, Any]]:
    rows = read_jsonl(REPO_ROOT / "agent" / "live-inspection-checklists.jsonl")
    return {str(row.get("id") or ""): row for row in rows if row.get("id")}


def answer_search_body(answer: dict[str, Any], checklist: dict[str, Any] | None) -> str:
    parts = [str(answer.get(key) or "") for key in ["question", "answer", "summary", "first_checks", "risks_caveats"]]
    for citation in answer.get("citations") or []:
        if isinstance(citation, dict):
            parts.extend(str(citation.get(key) or "") for key in ["title", "url", "source_timestamp_url"])
    if checklist:
        parts.extend(str(value) for value in checklist.get("inspection_targets") or [])
        parts.extend(str(value) for value in checklist.get("steps") or [])
        for probe in checklist.get("probes") or []:
            if isinstance(probe, dict):
                parts.extend(str(probe.get(key) or "") for key in ["label", "sql", "check"])
    return " ".join(part for part in parts if part)


def claim_search_rows() -> list[dict[str, Any]]:
    rows = []
    for claim in read_jsonl(REPO_ROOT / "claims" / "approved-claims.jsonl"):
        claim_id = str(claim.get("claim_id") or "")
        if not claim_id:
            continue
        concepts = normalize_concept_ids(claim.get("concept_ids") or [])
        row_id = f"claim:{claim_id}"
        rows.append(
            {
                "id": row_id,
                "kind": "claim",
                "title": claim.get("claim_type") or claim_id,
                "body": claim.get("claim") or "",
                "path": "claims/approved-claims.jsonl",
                "url": first_source_url(claim),
                "concept": first_concept(concepts),
                "concepts": concepts,
                "legacy_ids": [f"{row_id}:{concept_id}" for concept_id in concepts],
                "authority_tier": claim.get("authority_tier") or "",
                "claim_tier": claim.get("claim_tier") or "",
                "source_id": ",".join(str(value) for value in claim.get("source_record_ids") or []),
                "payload": claim,
            }
        )
    return rows


def contribution_search_rows() -> list[dict[str, Any]]:
    rows = []
    recipes = list(read_jsonl(REPO_ROOT / "agent" / "recipes.jsonl"))
    canonical_recipe_ids = {
        str(recipe.get("recipe_id") or "")
        for recipe in recipes
        if recipe.get("recipe_id")
    }
    superseded_contribution_ids = {
        str(contribution_id)
        for recipe in recipes
        for contribution_id in recipe.get("supersedes_contribution_ids") or []
        if contribution_id
    }
    for contribution in public_contribution_records():
        contribution_id = str(contribution.get("contribution_id") or "")
        if not contribution_id:
            continue
        if contribution_id in superseded_contribution_ids:
            continue
        if contribution.get("contribution_type") == "recipe" and contribution_id in canonical_recipe_ids:
            continue
        concepts = normalize_concept_ids(contribution.get("topics") or contribution.get("concept_ids") or [])
        row_id = f"community_contribution:{contribution_id}"
        payload = {
            **contribution,
            "claim_id": row_id,
            "claim": contribution.get("summary") or "",
            "concept_ids": concepts,
            "authority_tier": contribution.get("authority_tier") or "community-unreviewed",
            "claim_tier": contribution.get("claim_tier") or "routing_context_only",
        }
        rows.append(
            {
                "id": row_id,
                "kind": "community_contribution",
                "title": contribution.get("source_title") or contribution_id,
                "body": contribution.get("summary") or "",
                "path": contribution.get("bundle_path") or "",
                "url": contribution.get("source_url") or "",
                "concept": first_concept(concepts),
                "concepts": concepts,
                "legacy_ids": [f"{row_id}:{concept_id}" for concept_id in concepts],
                "authority_tier": contribution.get("authority_tier") or "community-unreviewed",
                "claim_tier": contribution.get("claim_tier") or "routing_context_only",
                "source_id": contribution.get("org_id") or contribution.get("source_id") or "",
                "payload": payload,
            }
        )
    return rows


def recipe_search_rows() -> list[dict[str, Any]]:
    rows = []
    for recipe in read_jsonl(REPO_ROOT / "agent" / "recipes.jsonl"):
        recipe_id = str(recipe.get("recipe_id") or "")
        if not recipe_id:
            continue
        implementation = recipe.get("implementation") or {}
        parts = [
            recipe.get("summary") or "",
            " ".join(recipe.get("use_cases") or []),
            " ".join(recipe.get("outcomes") or []),
            " ".join(recipe.get("learnings") or []),
            " ".join(recipe.get("known_limitations") or []),
            " ".join(item.get("description") or "" for item in recipe.get("adaptation_points") or [] if isinstance(item, dict)),
        ]
        concepts = normalize_concept_ids(recipe.get("concept_ids") or [])
        row_id = f"recipe:{recipe_id}"
        rows.append(
            {
                "id": row_id,
                "kind": "recipe",
                "title": recipe.get("title") or recipe_id,
                "body": " ".join(str(part) for part in parts if part),
                "path": f"knowledge/recipes/{recipe.get('org_id')}/{recipe_id.split(':', 1)[-1]}.md",
                "url": f"{implementation.get('repository_url', '')}/tree/{implementation.get('commit_sha', '')}/{implementation.get('source_path', '')}",
                "concept": first_concept(concepts),
                "concepts": concepts,
                "legacy_ids": [f"{row_id}:{concept_id}" for concept_id in concepts],
                "authority_tier": recipe.get("authority_tier") or "community-unreviewed",
                "claim_tier": "answer_pack_approved" if recipe.get("review_status") == "community_reviewed" else "routing_context_only",
                "source_id": recipe.get("org_id") or "",
                "payload": recipe,
            }
        )
    return rows


def source_summary_search_rows() -> list[dict[str, Any]]:
    rows = []
    for source in read_jsonl(REPO_ROOT / "agent" / "source-summaries.jsonl"):
        source_id = str(source.get("source_id") or "")
        source_record_id = str(source.get("source_record_id") or source.get("id") or source_id)
        title = str(source.get("source_title") or source.get("title") or source.get("name") or source_record_id)
        concepts = normalize_concept_ids(source.get("concept_ids") or [])
        topics = normalize_concept_ids(source.get("topics") or [])
        rows.append(
            {
                "id": f"source:{source_record_id}",
                "kind": "source_summary",
                "title": title,
                "body": source_summary_search_body(source),
                "path": "agent/source-summaries.jsonl",
                "url": source.get("source_url") or source.get("url") or source.get("root_url") or "",
                "concept": first_concept(concepts),
                "concepts": concepts,
                "topics": topics,
                "authority_tier": source.get("authority_tier") or "official",
                "claim_tier": "routing_context_only",
                "source_id": source_id,
                "payload": source,
            }
        )
    return rows


def source_summary_search_body(source: dict[str, Any]) -> str:
    parts = [
        str(source.get("summary") or source.get("description") or ""),
        " ".join(str(value) for value in source.get("concept_ids") or source.get("topics") or []),
        str(source.get("documentation_path") or ""),
        str(source.get("documentation_branch") or ""),
    ]
    for item in source.get("key_insights") or []:
        if isinstance(item, dict):
            parts.extend(str(item.get(key) or "") for key in ["topic", "insight", "timestamp"])
        else:
            parts.append(str(item or ""))
    agent_use = source.get("agent_use")
    if isinstance(agent_use, dict):
        parts.extend(str(value or "") for value in agent_use.values())
    elif agent_use:
        parts.append(str(agent_use))
    return " ".join(part for part in parts if part)


def model_map_search_rows() -> list[dict[str, Any]]:
    rows = []
    digests_by_slug = {
        str((row.get("identity") or {}).get("model_slug") or ""): row
        for row in read_jsonl(REPO_ROOT / "agent" / "model-map-digests.jsonl")
    }
    for model in read_jsonl(REPO_ROOT / "knowledge" / "model-map" / "stable-models.jsonl"):
        model_slug = str(model.get("model_slug") or "")
        detail_path = str(model.get("model_detail_path") or "")
        if not model_slug or not detail_path:
            continue
        digest = digests_by_slug.get(model_slug)
        body_parts = [
            str(model.get("model_name") or ""),
            str(model.get("model_title") or ""),
            str(model.get("model_category") or ""),
            str(model.get("description") or ""),
            f"{model.get('model_name') or model_slug} model map exact slug {model_slug}",
            read_text(REPO_ROOT / detail_path),
        ]
        rows.append(
            {
                "id": f"model_map:stable:{model_slug}",
                "kind": "model_map",
                "title": f"{model.get('model_name') or model_slug} Model Map",
                "body": "\n\n".join(part for part in body_parts if part),
                "path": detail_path,
                "url": model.get("source_url") or "",
                "concept": "model-map",
                "authority_tier": "official",
                "claim_tier": "source_backed",
                "source_id": "rock_model_map",
                "payload": compact_model_map_search_payload(digest or model),
            }
        )
    return rows


def lava_context_search_rows() -> list[dict[str, Any]]:
    rows = []
    for context in read_jsonl(REPO_ROOT / "agent" / "lava-contexts.jsonl"):
        context_id = str(context.get("id") or context.get("context_id") or "")
        if not context_id:
            continue
        concepts = normalize_concept_ids(context.get("concept_ids") or ["lava"])
        body = lava_context_search_body(context)
        rows.append(
            {
                "id": context_id,
                "kind": "lava_context",
                "title": f"{context.get('surface_name') or context.get('context_id')} - {context.get('root_key')}",
                "body": body,
                "path": "agent/lava-contexts.jsonl",
                "url": context.get("source_url") or "",
                "concept": first_concept(concepts),
                "concepts": concepts,
                "legacy_ids": [f"{context_id}:{concept_id}" for concept_id in concepts],
                "authority_tier": "source-code-confirmed",
                "claim_tier": "source_backed",
                "source_id": context.get("source_id") or "sparkdevnetwork_rock",
                "payload": compact_lava_context_search_payload(context),
            }
        )
    return rows


def rock_issue_search_rows() -> list[dict[str, Any]]:
    rows = []
    enrichments = issue_enrichments_by_id(REPO_ROOT)
    for raw_issue in read_jsonl(REPO_ROOT / "agent" / "rock-issues.jsonl"):
        issue = attach_issue_enrichments(raw_issue, enrichments)
        issue_id = str(issue.get("issue_id") or "")
        if not issue_id:
            continue
        concepts = normalize_concept_ids(issue.get("concept_ids") or [])
        labels = [str(value) for value in issue.get("labels") or []]
        versions = [
            str(value)
            for evidence in issue.get("version_evidence") or []
            for value in [evidence.get("normalized_version"), evidence.get("version_line")]
            if value
        ]
        model_links = [str(value) for value in issue.get("model_map_links") or []]
        release_note_summaries = [
            str(value.get("summary") or "")
            for value in issue.get("release_note_refs") or []
            if isinstance(value, dict)
        ]
        enrichment_text = [
            str(value)
            for enrichment in issue.get("reviewed_enrichments") or []
            if isinstance(enrichment, dict)
            for value in [
                enrichment.get("diagnosis_summary"),
                *(enrichment.get("workaround_summaries") or []),
                *(
                    version
                    for assertion in enrichment.get("applicability") or []
                    if isinstance(assertion, dict)
                    for version in assertion.get("versions") or []
                ),
            ]
            if value
        ]
        body = " ".join(
            value
            for value in [
                str(issue.get("title") or ""),
                spaced_search_alias(str(issue.get("title") or "")),
                " ".join(labels),
                " ".join(versions),
                " ".join(concepts),
                " ".join(model_links),
                " ".join(release_note_summaries),
                " ".join(enrichment_text),
                str(issue.get("repository") or ""),
                f"issue {issue.get('number')}",
                str(issue.get("state") or ""),
                str(issue.get("remediation_state") or ""),
            ]
            if value
        )
        rows.append(
            {
                "id": issue_id,
                "kind": "rock_issue",
                "title": issue.get("title") or issue_id,
                "body": body,
                "path": "agent/rock-issues.jsonl",
                "url": issue.get("url") or "",
                "concept": first_concept(concepts),
                "concepts": concepts,
                "topics": normalize_concept_ids(issue.get("topic_labels") or []),
                "legacy_ids": [
                    f"rock_issue:{'mobile' if issue.get('component') == 'mobile_shell' else 'core'}:{issue.get('number')}",
                    *[f"rock_issue:{location}" for location in issue.get("location_aliases") or []],
                ],
                "authority_tier": issue.get("authority_tier") or "community-unreviewed",
                "claim_tier": "routing_context_only",
                "source_id": issue.get("source_id") or "",
                "payload": issue,
            }
        )
    return rows


def lava_context_search_body(context: dict[str, Any]) -> str:
    root_key = str(context.get("root_key") or "")
    context_id = str(context.get("context_id") or "")
    surface_name = str(context.get("surface_name") or "")
    surface_type = str(context.get("surface_type") or "")
    parts = [
        context_id,
        context.get("context_family"),
        surface_name,
        surface_type,
        root_key,
        spaced_search_alias(root_key),
        spaced_search_alias(context_id),
        spaced_search_alias(surface_name),
        spaced_search_alias(surface_type),
        context.get("root_type"),
        context.get("nested_path"),
        context.get("value_kind"),
        context.get("availability"),
        context.get("source_symbol"),
        context.get("source_file"),
        context.get("notes"),
    ]
    for link in context.get("model_map_links") or []:
        if isinstance(link, dict):
            parts.extend(str(link.get(key) or "") for key in ["model_slug", "model_name", "model_title", "model_detail_path"])
            parts.append(spaced_search_alias(str(link.get("model_slug") or "")))
            parts.append(spaced_search_alias(str(link.get("model_title") or "")))
    return " ".join(str(part) for part in parts if part)


def spaced_search_alias(value: str) -> str:
    """Add natural-language tokens for compact ids and PascalCase/CamelCase keys."""
    if not value:
        return ""
    spaced = re.sub(r"[-_/]+", " ", value)
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", spaced)
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)
    return re.sub(r"\s+", " ", spaced).strip()


def compact_lava_context_search_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": row.get("schema", "rock-kb-lava-context-v1"),
        "id": row.get("id"),
        "context_id": row.get("context_id"),
        "context_family": row.get("context_family"),
        "surface_name": row.get("surface_name"),
        "surface_type": row.get("surface_type"),
        "concept_ids": row.get("concept_ids") or [],
        "root_key": row.get("root_key"),
        "root_type": row.get("root_type"),
        "model_slug": row.get("model_slug"),
        "value_kind": row.get("value_kind"),
        "nested_path": row.get("nested_path"),
        "availability": row.get("availability"),
        "source_url": row.get("source_url"),
        "source_file": row.get("source_file"),
        "source_symbol": row.get("source_symbol"),
        "source_line_start": row.get("source_line_start"),
        "source_ref": row.get("source_ref"),
        "model_map_links": row.get("model_map_links") or [],
        "needs_live_verification": row.get("needs_live_verification"),
        "notes": row.get("notes"),
    }


def compact_model_map_search_payload(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("identity"):
        identity = row.get("identity") or {}
        counts = row.get("counts") or {}
        property_groups = row.get("property_groups") or {}
        return {
            "schema": "rock-kb-model-map-search-payload-v1",
            "identity": identity,
            "counts": counts,
            "property_group_counts": {
                key: len(value) if isinstance(value, list) else 0
                for key, value in property_groups.items()
            },
            "required_fields": row.get("required_fields") or [],
            "relationships": row.get("relationships") or [],
            "version_diff_count": len(row.get("version_diffs") or []),
            "operational_notes": row.get("operational_notes") or [],
            "paths": row.get("paths") or {},
        }
    return row


def load_org_registry() -> list[dict[str, Any]]:
    org_dir = REPO_ROOT / "orgs"
    rows = []
    for path in sorted(org_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict):
            data.setdefault("org_id", path.stem)
            rows.append(data)
    return rows


def build_d1_seed_sql(version: str, generated_at: str, search_rows: list[dict[str, Any]], org_rows: list[dict[str, Any]]) -> str:
    lines = [
        "DROP TABLE IF EXISTS kb_meta;",
        "CREATE TABLE kb_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);",
        "INSERT INTO kb_meta (key, value) VALUES ('current_version', " + sql_string(version) + ");",
        "INSERT INTO kb_meta (key, value) VALUES ('generated_at', " + sql_string(generated_at) + ");",
        "DROP TABLE IF EXISTS search_rows;",
        """CREATE TABLE search_rows (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  path TEXT NOT NULL,
  url TEXT,
  concept TEXT,
  authority_tier TEXT,
  claim_tier TEXT,
  claim_tier_rank INTEGER NOT NULL,
  source_id TEXT,
  concepts_json TEXT NOT NULL DEFAULT '[]',
  topics_json TEXT NOT NULL DEFAULT '[]',
  payload_json TEXT NOT NULL
);""",
        "DROP TABLE IF EXISTS search_row_concepts;",
        "CREATE TABLE search_row_concepts (row_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (row_id, concept));",
        "CREATE INDEX search_row_concepts_concept_idx ON search_row_concepts (concept, row_id);",
        "DROP TABLE IF EXISTS search_row_aliases;",
        "CREATE TABLE search_row_aliases (alias_id TEXT PRIMARY KEY, canonical_id TEXT NOT NULL);",
        "DROP TABLE IF EXISTS search_rows_fts;",
        "CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept, tokenize='porter');",
        "DROP TABLE IF EXISTS org_registry;",
        "CREATE TABLE org_registry (org_id TEXT PRIMARY KEY, display_name TEXT, status TEXT, payload_json TEXT NOT NULL);",
        "DROP TABLE IF EXISTS rock_issues;",
        """CREATE TABLE rock_issues (
  issue_id TEXT PRIMARY KEY,
  github_node_id TEXT NOT NULL UNIQUE,
  repository TEXT NOT NULL,
  number INTEGER NOT NULL,
  component TEXT NOT NULL,
  state TEXT NOT NULL,
  validation_state TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  evidence_state TEXT NOT NULL,
  payload_json TEXT NOT NULL
);""",
        "CREATE UNIQUE INDEX rock_issues_repository_number_idx ON rock_issues (repository, number);",
        "CREATE UNIQUE INDEX rock_issues_github_node_idx ON rock_issues (github_node_id);",
        "CREATE INDEX rock_issues_state_updated_idx ON rock_issues (state, updated_at DESC);",
        "DROP TABLE IF EXISTS rock_issue_locations;",
        "CREATE TABLE rock_issue_locations (location_id TEXT PRIMARY KEY, issue_id TEXT NOT NULL, is_current INTEGER NOT NULL);",
        "CREATE INDEX rock_issue_locations_issue_idx ON rock_issue_locations (issue_id);",
        "DROP TABLE IF EXISTS rock_issue_versions;",
        """CREATE TABLE rock_issue_versions (
  issue_id TEXT NOT NULL,
  component TEXT NOT NULL,
  relationship TEXT NOT NULL,
  version TEXT NOT NULL,
  version_line TEXT NOT NULL,
  source_kind TEXT NOT NULL,
  authority_tier TEXT NOT NULL,
  confidence TEXT NOT NULL,
  source_ref TEXT NOT NULL,
  observed_at TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (issue_id, component, relationship, version, source_ref, observed_at)
);""",
        "CREATE INDEX rock_issue_versions_lookup_idx ON rock_issue_versions (component, version_line, version, relationship);",
        "DROP TABLE IF EXISTS rock_issue_concepts;",
        "CREATE TABLE rock_issue_concepts (issue_id TEXT NOT NULL, concept TEXT NOT NULL, PRIMARY KEY (issue_id, concept));",
        "CREATE INDEX rock_issue_concepts_lookup_idx ON rock_issue_concepts (concept, issue_id);",
        "DROP TABLE IF EXISTS rock_issue_enrichments;",
        """CREATE TABLE rock_issue_enrichments (
  enrichment_id TEXT PRIMARY KEY,
  issue_id TEXT NOT NULL,
  diagnosis_status TEXT NOT NULL,
  reviewed_at TEXT NOT NULL,
  payload_json TEXT NOT NULL
);""",
        "CREATE INDEX rock_issue_enrichments_issue_idx ON rock_issue_enrichments (issue_id, reviewed_at DESC);",
    ]
    for row in search_rows:
        tier = str(row.get("claim_tier") or "")
        body = d1_search_body(row.get("body") or "")
        concepts = normalize_concept_ids(row.get("concepts") or [row.get("concept") or ""])
        topics = normalize_concept_ids(row.get("topics") or [])
        concepts_json = json.dumps(concepts, ensure_ascii=False, separators=(",", ":"))
        topics_json = json.dumps(topics, ensure_ascii=False, separators=(",", ":"))
        concept_search_text = " ".join([*concepts, *topics])
        lines.append(
            "INSERT INTO search_rows (id, kind, title, body, path, url, concept, authority_tier, claim_tier, claim_tier_rank, source_id, concepts_json, topics_json, payload_json) VALUES ("
            + ", ".join(
                [
                    sql_string(row["id"]),
                    sql_string(row["kind"]),
                    sql_string(row["title"]),
                    sql_string(body),
                    sql_string(row["path"]),
                    sql_string(row.get("url") or ""),
                    sql_string(row.get("concept") or ""),
                    sql_string(row.get("authority_tier") or ""),
                    sql_string(tier),
                    str(CLAIM_TIER_RANK.get(tier, 0)),
                    sql_string(row.get("source_id") or ""),
                    sql_string(concepts_json),
                    sql_string(topics_json),
                    sql_string(json.dumps(row.get("payload") or {}, ensure_ascii=False, sort_keys=True)),
                ]
            )
            + ");"
        )
        lines.append(
            "INSERT INTO search_rows_fts (id, title, body, concept) VALUES ("
            + ", ".join(
                [
                    sql_string(row["id"]),
                    sql_string(row["title"]),
                    sql_string(body),
                    sql_string(concept_search_text),
                ]
            )
            + ");"
        )
        for concept_id in concepts:
            lines.append(
                "INSERT INTO search_row_concepts (row_id, concept) VALUES ("
                + ", ".join([sql_string(row["id"]), sql_string(concept_id)])
                + ");"
            )
        for alias_id in row.get("legacy_ids") or []:
            lines.append(
                "INSERT INTO search_row_aliases (alias_id, canonical_id) VALUES ("
                + ", ".join([sql_string(alias_id), sql_string(row["id"])])
                + ");"
            )
        if row.get("kind") == "rock_issue":
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            lines.append(
                "INSERT INTO rock_issues VALUES ("
                + ", ".join(
                    [
                        sql_string(payload.get("issue_id") or row["id"]),
                        sql_string(payload.get("github_node_id") or ""),
                        sql_string(payload.get("repository") or ""),
                        str(int(payload.get("number") or 0)),
                        sql_string(payload.get("component") or ""),
                        sql_string(payload.get("state") or ""),
                        sql_string(payload.get("validation_state") or "reported"),
                        sql_string(payload.get("title") or row.get("title") or ""),
                        sql_string(payload.get("url") or row.get("url") or ""),
                        sql_string(payload.get("updated_at") or ""),
                        sql_string(payload.get("evidence_state") or "report_only"),
                        sql_string(json.dumps(payload, ensure_ascii=False, sort_keys=True)),
                    ]
                )
                + ");"
            )
            current_location = str(payload.get("location_id") or f"{payload.get('repository')}#{payload.get('number')}")
            locations = [(current_location, 1)]
            locations.extend((str(value), 0) for value in payload.get("location_aliases") or [])
            for location_id, is_current in locations:
                lines.append(
                    "INSERT INTO rock_issue_locations VALUES ("
                    + ", ".join(
                        [
                            sql_string(location_id),
                            sql_string(payload.get("issue_id") or row["id"]),
                            str(is_current),
                        ]
                    )
                    + ");"
                )
            for evidence in payload.get("version_evidence") or []:
                if not isinstance(evidence, dict):
                    continue
                lines.append(
                    "INSERT INTO rock_issue_versions VALUES ("
                    + ", ".join(
                        [
                            sql_string(payload.get("issue_id") or row["id"]),
                            sql_string(evidence.get("component") or ""),
                            sql_string(evidence.get("relationship") or ""),
                            sql_string(evidence.get("normalized_version") or ""),
                            sql_string(evidence.get("version_line") or ""),
                            sql_string(evidence.get("source_kind") or ""),
                            sql_string(evidence.get("authority_tier") or ""),
                            sql_string(evidence.get("confidence") or ""),
                            sql_string(evidence.get("source_ref") or ""),
                            sql_string(evidence.get("observed_at") or ""),
                        ]
                    )
                    + ");"
                )
            for concept_id in concepts:
                lines.append(
                    "INSERT INTO rock_issue_concepts VALUES ("
                    + ", ".join([sql_string(payload.get("issue_id") or row["id"]), sql_string(concept_id)])
                    + ");"
                )
            for enrichment in payload.get("reviewed_enrichments") or []:
                if not isinstance(enrichment, dict):
                    continue
                lines.append(
                    "INSERT INTO rock_issue_enrichments VALUES ("
                    + ", ".join(
                        [
                            sql_string(enrichment.get("enrichment_id") or ""),
                            sql_string(payload.get("issue_id") or row["id"]),
                            sql_string(enrichment.get("diagnosis_status") or ""),
                            sql_string(enrichment.get("reviewed_at") or ""),
                            sql_string(json.dumps(enrichment, ensure_ascii=False, sort_keys=True)),
                        ]
                    )
                    + ");"
                )
                relationship_by_status = {
                    "affected": "known_affected",
                    "fixed": "fixed",
                    "not_affected": "known_not_affected",
                    "under_investigation": "under_investigation",
                    "unknown": "under_investigation",
                }
                for assertion in enrichment.get("applicability") or []:
                    if not isinstance(assertion, dict):
                        continue
                    relationship = relationship_by_status.get(str(assertion.get("status") or ""), "under_investigation")
                    source_ref = (
                        f"reviewed_enrichment:{enrichment.get('enrichment_id')}#"
                        f"{assertion.get('assertion_id')}"
                    )
                    for raw_version in assertion.get("versions") or []:
                        normalized = normalize_version(str(raw_version))
                        if not normalized:
                            continue
                        lines.append(
                            "INSERT INTO rock_issue_versions VALUES ("
                            + ", ".join(
                                [
                                    sql_string(payload.get("issue_id") or row["id"]),
                                    sql_string(assertion.get("component") or payload.get("component") or ""),
                                    sql_string(relationship),
                                    sql_string(normalized),
                                    sql_string(version_line(normalized)),
                                    sql_string("reviewed_enrichment"),
                                    sql_string(assertion.get("authority_tier") or enrichment.get("authority_tier") or "community-reviewed"),
                                    sql_string(assertion.get("confidence") or enrichment.get("confidence") or "medium"),
                                    sql_string(source_ref),
                                    sql_string(assertion.get("assessed_at") or enrichment.get("reviewed_at") or ""),
                                ]
                            )
                            + ");"
                        )
    for row in org_rows:
        org_id = str(row.get("org_id") or "")
        if not org_id:
            continue
        lines.append(
            "INSERT INTO org_registry VALUES ("
            + ", ".join(
                [
                    sql_string(org_id),
                    sql_string(row.get("display_name") or org_id),
                    sql_string(row.get("status") or "reviewed"),
                    sql_string(json.dumps(row, ensure_ascii=False, sort_keys=True)),
                ]
            )
            + ");"
        )
    return "\n".join(lines) + "\n"


def deploy_service_projection(
    *,
    apply: bool = False,
    env: str | None = None,
    bucket: str | None = None,
    database: str | None = None,
) -> dict[str, Any]:
    projection = build_service_projection()
    result = projection.as_dict()
    result["applied"] = False
    if not apply:
        result["next_commands"] = [
            f"cd service && find dist/artifact-shards -type f -print | sed 's#dist/artifact-shards/##' | xargs -I {{}} npx wrangler r2 object put {bucket or '<bucket-name>'}/versions/{projection.version}/artifact-shards/{{}} --remote --file dist/artifact-shards/{{}}",
            f"cd service && npx wrangler d1 execute {database or '<database-name>'} --remote --file dist/d1-seed.sql --yes",
            "cd service && npx wrangler deploy" + (f" --env {env}" if env else ""),
        ]
        return result
    apply_projection_to_cloudflare(projection, env=env, bucket=bucket, database=database)
    result["applied"] = True
    return result


def apply_projection_to_cloudflare(
    projection: ServiceProjection,
    *,
    env: str | None,
    bucket: str | None,
    database: str | None,
) -> None:
    env_args = ["--env", env] if env else []
    bucket_name = bucket or "rock-agent-kb-artifacts"
    upload_artifacts_to_r2(projection=projection, bucket_name=bucket_name, env_args=env_args)
    d1_target = database or "rock-agent-kb"
    run(["npx", "wrangler", "d1", "execute", d1_target, "--remote", "--file", str(projection.sql_path), "--yes", *env_args], cwd=SERVICE_DIR)
    run(["npx", "wrangler", "deploy", *env_args], cwd=SERVICE_DIR)


def write_artifact_shards(*, artifacts_dir: Path, shards_dir: Path) -> None:
    if shards_dir.exists():
        shutil.rmtree(shards_dir)
    grouped: dict[str, dict[str, str]] = {}
    for path in sorted(item for item in artifacts_dir.rglob("*") if item.is_file()):
        rel = path.relative_to(artifacts_dir).as_posix()
        shard = artifact_shard_for_path(rel)
        grouped.setdefault(shard, {})[rel] = path.read_text(encoding="utf-8")
    shards_dir.mkdir(parents=True, exist_ok=True)
    for shard, artifacts in sorted(grouped.items()):
        payload = {
            "schema": "rock-kb-artifact-shard-v1",
            "shard": shard,
            "artifacts": artifacts,
        }
        (shards_dir / f"{shard}.json").write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )


def artifact_shard_for_path(path: str) -> str:
    return sha256_text(path)[:ARTIFACT_SHARD_PREFIX_LENGTH]


def upload_artifacts_to_r2(*, projection: ServiceProjection, bucket_name: str, env_args: list[str]) -> None:
    shard_dir = projection.dist / "artifact-shards"
    paths = sorted(path for path in shard_dir.rglob("*") if path.is_file())
    total = len(paths)
    workers = max(1, int(os.getenv("ROCK_KB_R2_UPLOAD_WORKERS", "8")))
    print(f"Uploading {total} R2 artifact shards with {workers} workers.", flush=True)
    completed = 0
    progress_lock = Lock()

    def upload_with_progress(path: Path) -> None:
        nonlocal completed
        upload_artifact_shard_to_r2(projection, bucket_name, env_args, path)
        with progress_lock:
            completed += 1
            if completed == total or completed % 50 == 0:
                print(f"Uploaded {completed}/{total} R2 artifact shards.", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(upload_with_progress, path) for path in paths]
        for future in as_completed(futures):
            future.result()


def upload_artifact_shard_to_r2(projection: ServiceProjection, bucket_name: str, env_args: list[str], path: Path) -> None:
    rel = path.relative_to(projection.dist / "artifact-shards").as_posix()
    run_with_retries(
        [
            "npx",
            "wrangler",
            "r2",
            "object",
            "put",
            f"{bucket_name}/versions/{projection.version}/artifact-shards/{rel}",
            "--remote",
            "--file",
            str(path),
            *env_args,
        ],
        cwd=SERVICE_DIR,
    )


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def run_with_retries(command: list[str], cwd: Path, attempts: int = 3) -> None:
    timeout_seconds = int(os.getenv("ROCK_KB_WRANGLER_COMMAND_TIMEOUT_SECONDS", "300"))
    for attempt in range(1, attempts + 1):
        try:
            result = subprocess.run(command, cwd=cwd, check=False, timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            result = subprocess.CompletedProcess(command, returncode=124)
        if result.returncode == 0:
            return
        if attempt == attempts:
            raise subprocess.CalledProcessError(result.returncode, command)
        time.sleep(min(2**attempt, 10))


def first_source_url(claim: dict[str, Any]) -> str:
    for ref in claim.get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("url"):
            return str(ref["url"])
    return ""


def normalize_concept_ids(values: Iterable[Any]) -> list[str]:
    concepts: list[str] = []
    seen: set[str] = set()
    for value in values:
        concept_id = str(value or "").strip()
        if not concept_id or concept_id in seen:
            continue
        seen.add(concept_id)
        concepts.append(concept_id)
    return concepts


def first_concept(concepts: list[str]) -> str:
    return concepts[0] if concepts else ""


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def sql_string(value: Any) -> str:
    if value is None:
        return "''"
    return "'" + str(value).replace("'", "''") + "'"


def d1_search_body(value: Any) -> str:
    body = str(value)
    if len(body) <= D1_SEARCH_BODY_CHAR_LIMIT:
        return body
    return body[:D1_SEARCH_BODY_CHAR_LIMIT].rstrip() + "\n\n[Search body truncated; full document is available in R2 artifacts.]"


def write_jsonl_text(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
