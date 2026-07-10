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


SERVICE_DIR = REPO_ROOT / "service"
SERVICE_DIST_DIR = SERVICE_DIR / "dist"
SERVICE_ARTIFACTS_DIR = SERVICE_DIST_DIR / "artifacts"
SERVICE_ARTIFACT_SHARDS_DIR = SERVICE_DIST_DIR / "artifact-shards"
SERVICE_SQL_PATH = SERVICE_DIST_DIR / "d1-seed.sql"
SERVICE_PROJECTION_PATH = SERVICE_DIST_DIR / "projection.json"
SERVICE_SEARCH_ROWS_PATH = SERVICE_DIST_DIR / "search-rows.jsonl"
ORG_REGISTRY_PATH = SERVICE_DIST_DIR / "org-registry.json"
D1_SEARCH_BODY_CHAR_LIMIT = 75_000
ARTIFACT_SHARD_PREFIX_LENGTH = 2


CLAIM_TIER_RANK = {
    "routing_context_only": 0,
    "source_backed": 1,
    "answer_pack_approved": 2,
    "live_verified": 3,
}


@dataclass(frozen=True)
class ServiceProjection:
    version: str
    generated_at: str
    artifact_count: int
    search_row_count: int
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
            "org_count": self.org_count,
            "dist": str(self.dist),
            "sql_path": str(self.sql_path),
        }


def build_service_projection(destination: Path | None = None) -> ServiceProjection:
    dist = destination or SERVICE_DIST_DIR
    artifacts_dir = dist / "artifacts"
    if dist.exists():
        shutil.rmtree(dist)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    generated_at = generated_at_iso()
    manifest = public_export_manifest()
    version_manifest = dict(manifest)
    version_manifest.pop("generated_at", None)
    version = sha256_text(json.dumps(version_manifest, sort_keys=True, ensure_ascii=False))[:16]
    files = manifest.get("files") or []
    for row in files:
        public_path = str(row["path"])
        target = artifacts_dir / public_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(public_export_text_for_public_path(public_path), encoding="utf-8")
    write_artifact_shards(artifacts_dir=artifacts_dir, shards_dir=dist / "artifact-shards")

    search_rows = build_search_rows()
    write_jsonl_text(dist / "search-rows.jsonl", search_rows)
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
    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        deduped[str(row["id"])] = row
    return sorted(deduped.values(), key=lambda row: str(row.get("id") or ""))


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
        for concept_id in claim.get("concept_ids") or []:
            rows.append(
                {
                    "id": f"claim:{claim_id}:{concept_id}",
                    "kind": "claim",
                    "title": claim.get("claim_type") or claim_id,
                    "body": claim.get("claim") or "",
                    "path": "claims/approved-claims.jsonl",
                    "url": first_source_url(claim),
                    "concept": concept_id,
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
        for concept_id in contribution.get("topics") or []:
            row_id = f"community_contribution:{contribution_id}:{concept_id}"
            payload = {
                **contribution,
                "claim_id": row_id,
                "claim": contribution.get("summary") or "",
                "concept_ids": [concept_id],
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
                    "concept": concept_id,
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
        for concept_id in recipe.get("concept_ids") or [""]:
            rows.append(
                {
                    "id": f"recipe:{recipe_id}:{concept_id}",
                    "kind": "recipe",
                    "title": recipe.get("title") or recipe_id,
                    "body": " ".join(str(part) for part in parts if part),
                    "path": f"knowledge/recipes/{recipe.get('org_id')}/{recipe_id.split(':', 1)[-1]}.md",
                    "url": f"{implementation.get('repository_url', '')}/tree/{implementation.get('commit_sha', '')}/{implementation.get('source_path', '')}",
                    "concept": concept_id,
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
        concepts = list(source.get("concept_ids") or source.get("topics") or [""])
        rows.append(
            {
                "id": f"source:{source_record_id}",
                "kind": "source_summary",
                "title": title,
                "body": source_summary_search_body(source),
                "path": "agent/source-summaries.jsonl",
                "url": source.get("source_url") or source.get("url") or source.get("root_url") or "",
                "concept": concepts[0] if concepts else "",
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
        concepts = context.get("concept_ids") or ["lava"]
        body = lava_context_search_body(context)
        for concept_id in concepts:
            rows.append(
                {
                    "id": f"{context_id}:{concept_id}",
                    "kind": "lava_context",
                    "title": f"{context.get('surface_name') or context.get('context_id')} - {context.get('root_key')}",
                    "body": body,
                    "path": "agent/lava-contexts.jsonl",
                    "url": context.get("source_url") or "",
                    "concept": concept_id,
                    "authority_tier": "source-code-confirmed",
                    "claim_tier": "source_backed",
                    "source_id": context.get("source_id") or "sparkdevnetwork_rock",
                    "payload": compact_lava_context_search_payload(context),
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
  payload_json TEXT NOT NULL
);""",
        "DROP TABLE IF EXISTS search_rows_fts;",
        "CREATE VIRTUAL TABLE search_rows_fts USING fts5(id UNINDEXED, title, body, concept, tokenize='porter');",
        "DROP TABLE IF EXISTS org_registry;",
        "CREATE TABLE org_registry (org_id TEXT PRIMARY KEY, display_name TEXT, status TEXT, payload_json TEXT NOT NULL);",
    ]
    for row in search_rows:
        tier = str(row.get("claim_tier") or "")
        body = d1_search_body(row.get("body") or "")
        lines.append(
            "INSERT INTO search_rows VALUES ("
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
                    sql_string(row.get("concept") or ""),
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
