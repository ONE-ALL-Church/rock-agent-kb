from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import tarfile
import tomllib
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urljoin

import yaml

from .concepts import load_concepts
from .contribution_sources import public_contribution_records
from .jsonl import read_jsonl
from .paths import DATA_DIR, REPO_ROOT
from .service_projection import build_search_rows
from .sources import load_sources
from .timestamps import generated_at_iso


OKF_VERSION = "0.1"
OKF_SPEC_COMMIT = "ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a"
OKF_PROFILE_SCHEMA = "rock-kb-okf-profile-v1"
OKF_PROFILES = {"full", "core"}
DEFAULT_OKF_EXPORT_DIR = DATA_DIR / "okf-export"
MANIFEST_NAME = "okf-manifest.json"
FILE_MANIFEST_NAME = "file-manifest.jsonl"
CHECKSUMS_NAME = "checksums.sha256"
RESERVED_FILENAMES = {"index.md", "log.md"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOG_DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})$")
PRIVATE_MARKERS = (
    "/Users/",
    "data/review/",
    "data/normalized/",
    "private_corpus_pointer",
    "rockproduction_docs_private_candidates",
    "private_rock_repo_candidates",
    "outside_org_contribution_candidates",
)
MAX_INDEX_ENTRIES = 200
MAX_INDEX_BYTES = 64 * 1024
KIND_CONFIG = {
    "concept": ("Concept", "concepts"),
    "answer": ("Agent Answer", "answers"),
    "claim": ("Claim", "claims"),
    "model_map": ("Rock Model", "models"),
    "lava_context": ("Lava Context", "lava-contexts"),
    "recipe": ("Community Recipe", "recipes"),
    "source_summary": ("Source Summary", "source-summaries"),
    "rock_issue": ("Rock Issue", "rock-issues"),
}


def build_okf_export(
    destination: Path | None = None,
    *,
    distribution_version: str | None = None,
    source_commit: str | None = None,
    archive_dir: Path | None = None,
    profile: str = "full",
    previous_bundle: Path | None = None,
) -> dict[str, Any]:
    if profile not in OKF_PROFILES:
        raise ValueError(f"Unknown OKF profile: {profile}")
    destination = (destination or DEFAULT_OKF_EXPORT_DIR).resolve()
    ensure_safe_destination(destination)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    generated_at = generated_at_iso()
    version = distribution_version or current_release_version()
    commit = source_commit or current_source_commit()
    concepts = load_concepts()
    concept_ids = {concept.id for concept in concepts}
    public_sources = {
        source.id: source
        for source in load_sources()
        if source.public_publish_mode != "private_only"
        and "private" not in source.id
        and not source.id.endswith("_candidates")
    }

    search_rows = [row for row in build_search_rows() if row.get("kind") != "community_contribution"]
    concept_descriptions = {concept.id: concept.description for concept in concepts}
    for row in search_rows:
        if row.get("kind") == "concept":
            row["okf_description"] = concept_descriptions.get(first_concept_id(row), "")
    search_rows = rows_for_profile(search_rows, profile)
    full_models = {
        str((row.get("identity") or {}).get("model_slug") or ""): row
        for row in read_jsonl(REPO_ROOT / "agent" / "model-map-digests.jsonl")
    }
    full_lava_contexts = {
        str(row.get("id") or row.get("context_id") or ""): row
        for row in read_jsonl(REPO_ROOT / "agent" / "lava-contexts.jsonl")
    }
    for row in search_rows:
        if profile == "full" and row.get("kind") == "model_map":
            slug = str((row.get("payload") or {}).get("identity", {}).get("model_slug") or "")
            if slug in full_models:
                row["payload"] = full_models[slug]
        elif row.get("kind") == "lava_context" and str(row.get("id") or "") in full_lava_contexts:
            row["payload"] = full_lava_contexts[str(row["id"])]
    contribution_rows = contribution_okf_rows(public_contribution_records()) if profile == "full" else []
    task_rows = task_card_okf_rows(read_jsonl(REPO_ROOT / "agent" / "concept-task-cards.jsonl"))
    rows = sorted([*search_rows, *contribution_rows, *task_rows], key=lambda row: str(row.get("id") or ""))
    duplicate_ids = sorted(row_id for row_id, count in Counter(str(row.get("id") or "") for row in rows).items() if row_id and count > 1)
    if duplicate_ids:
        raise ValueError(f"Duplicate canonical OKF record ids: {', '.join(duplicate_ids[:10])}")

    path_by_id = {str(row["id"]): row_path(row) for row in rows}
    assert_unique_paths(path_by_id, "knowledge records")
    model_path_by_slug = {
        str((row.get("payload") or {}).get("identity", {}).get("model_slug") or ""): path_by_id[str(row["id"])]
        for row in rows
        if row.get("kind") == "model_map"
    }
    reference_paths = {source_id: PurePosixPath("references") / f"{safe_slug(source_id)}.md" for source_id in public_sources}
    assert_unique_paths(reference_paths, "references")
    concept_paths = {
        concept.id: PurePosixPath("concepts") / f"{safe_slug(concept.id)}.md" for concept in concepts
    }

    relationships: list[dict[str, str]] = []
    index_entries: dict[PurePosixPath, list[tuple[PurePosixPath, str, str]]] = defaultdict(list)

    for source_id, source in sorted(public_sources.items()):
        path = reference_paths[source_id]
        related = [row for row in rows if source_id in source_ids_for_row(row)]
        body = [
            f"# {source.name}",
            "",
            source.description,
            "",
            "## Source Policy",
            "",
            f"- Owner: {source.owner}",
            f"- Kind: `{source.kind}`",
            f"- License status: `{source.license_status}`",
            f"- Public mode: `{source.public_publish_mode}`",
            f"- Extraction mode: `{source.allowed_extraction_mode}`",
            f"- Refresh cadence: `{source.refresh_cadence}`",
            "",
            "## Resource",
            "",
            f"- [Open the canonical source](<{source.root_url}>)",
            "",
            "## Related Knowledge",
            "",
            *related_link_lines(path, related[:50], path_by_id),
        ]
        frontmatter = compact_frontmatter(
            {
                "type": "Reference",
                "id": source_id,
                "title": source.name,
                "description": source.description,
                "resource": source.root_url,
                "tags": sorted(set(source.topics + [source.kind, "reference"])),
                "source_path": "sources/registry.yaml",
            }
        )
        write_typed_markdown(destination / path, frontmatter, body)
        index_entries[path.parent].append((path, source.name, source.description))

    for row in rows:
        row_id = str(row["id"])
        path = path_by_id[row_id]
        related = related_paths_for_row(
            row,
            concept_ids=concept_ids,
            concept_paths=concept_paths,
            reference_paths=reference_paths,
            model_path_by_slug=model_path_by_slug,
            path_by_id=path_by_id,
        )
        row_relationships = []
        for relation_type, target in related:
            row_relationships.append({"type": relation_type, "target": f"/{target.as_posix()}"})
            relationships.append(
                relationship(
                    relation_type,
                    source=path.with_suffix("").as_posix(),
                    target=target.with_suffix("").as_posix(),
                )
            )

        title = row_title(row)
        description = row_description(row)
        kind_type = kind_type_for_row(row)
        body, rendered_source_path = render_row_body(
            row,
            current_path=path,
            related=related,
            commit=commit,
            profile=profile,
        )
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        canonical_id = canonical_record_id(row)
        record_path = write_structured_record(destination, row, profile=profile)
        frontmatter = compact_frontmatter(
            {
                "type": kind_type,
                "id": canonical_id,
                "canonical_id": canonical_id,
                "result_id": row_id if row_id != canonical_id else "",
                "title": title,
                "description": description,
                "resource": primary_resource_url(row),
                "tags": row_tags(row, concept_ids),
                "timestamp": row_timestamp(row),
                "retrieved_at": payload.get("retrieved_at"),
                "content_hash": row_content_hash(row),
                "source_content_hash": payload.get("source_content_hash") or payload.get("safe_evidence_hash"),
                "authority_tier": row.get("authority_tier") or payload.get("authority_tier"),
                "claim_tier": row.get("claim_tier") or payload.get("claim_tier"),
                "rock_versions": rock_versions_for_row(row),
                "source_path": rendered_source_path,
                "structured_record": f"/{record_path.as_posix()}",
                "okf_profile": OKF_PROFILE_SCHEMA,
                "relationships": row_relationships,
            }
        )
        write_typed_markdown(destination / path, frontmatter, body)
        index_entries[path.parent].append((path, title, description))

    write_directory_indexes(destination, index_entries)
    copy_distribution_licenses(destination)
    write_profile_document(destination, generated_at=generated_at)
    write_root_index(
        destination,
        generated_at=generated_at,
        version=version,
        commit=commit,
        rows=rows,
        profile=profile,
    )
    relationship_rows = sorted(
        {json.dumps(row, ensure_ascii=False, sort_keys=True) for row in relationships}
    )
    (destination / "relationships.jsonl").write_text(
        "".join(line + "\n" for line in relationship_rows), encoding="utf-8"
    )
    changes = write_update_log(
        destination,
        generated_at=generated_at,
        version=version,
        previous_bundle=previous_bundle,
    )

    counts = Counter(row_kind_count_key(row) for row in rows)
    counts["references"] = len(public_sources)
    write_file_manifest(destination)
    report = {
        "schema": "rock-kb-okf-distribution-v1",
        "okf_version": OKF_VERSION,
        "okf_spec_commit": OKF_SPEC_COMMIT,
        "okf_profile": OKF_PROFILE_SCHEMA,
        "profile": profile,
        "distribution_version": version,
        "generated_at": generated_at,
        "source_commit": commit,
        "read_only": True,
        "license": {
            "code": "MIT",
            "original_content": "CC-BY-4.0",
            "notice": "NOTICE.txt",
        },
        "canonical_scope": [
            "concept guides",
            "agent answers",
            "approved claims",
            "public contribution provenance",
            "reviewed community recipes",
            "Lava contexts",
            "stable Rock model digests",
            "source summaries",
            "agent task cards",
            "public evidence-source policies",
            "public Rock issue routing metadata",
        ],
        "excluded_scope": [
            "private organization overlays",
            "raw transcripts and media",
            "review queues and live-instance evidence",
            "evaluation and telemetry artifacts",
            "redundant generated indexes",
        ],
        "counts": dict(sorted(counts.items())),
        "changes": changes,
        "markdown_files": len(list(destination.rglob("*.md"))),
        "relationships": len(relationship_rows),
        "file_manifest": FILE_MANIFEST_NAME,
        "file_manifest_sha256": sha256_file(destination / FILE_MANIFEST_NAME),
        "checksums": CHECKSUMS_NAME,
        "status": "pending_audit",
        "errors": [],
    }
    manifest_path = destination / MANIFEST_NAME
    manifest_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_checksums(destination)

    errors = audit_okf_export(destination)
    report["status"] = "ok" if not errors else "failed"
    report["errors"] = errors
    manifest_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_checksums(destination)

    result = dict(report)
    if archive_dir and not errors:
        result["archives"] = create_okf_archives(destination, archive_dir.resolve(), version, profile=profile)
    return result


def contribution_okf_rows(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("contribution_id"):
            grouped[str(record["contribution_id"])].append(record)

    rows = []
    for contribution_id, candidates in sorted(grouped.items()):
        selected = max(
            candidates,
            key=lambda record: (
                record.get("authority_tier") == "community-reviewed",
                str(record.get("bundle_path") or ""),
            ),
        )
        payload = {
            **selected,
            "provenance_paths": sorted(
                {str(record.get("bundle_path") or "") for record in candidates if record.get("bundle_path")}
            ),
        }
        rows.append(
            {
                "id": f"contribution:{contribution_id}",
                "kind": "contribution",
                "title": selected.get("source_title") or contribution_id,
                "body": selected.get("summary") or "",
                "path": selected.get("bundle_path") or "",
                "url": selected.get("source_url") or "",
                "concepts": selected.get("topics") or [],
                "authority_tier": selected.get("authority_tier") or "community-unreviewed",
                "claim_tier": selected.get("claim_tier") or "routing_context_only",
                "payload": payload,
            }
        )
    return rows


def rows_for_profile(rows: Iterable[dict[str, Any]], profile: str) -> list[dict[str, Any]]:
    if profile == "full":
        return list(rows)
    selected = []
    for row in rows:
        kind = str(row.get("kind") or "")
        if kind in {"source_summary", "community_contribution", "rock_issue"}:
            continue
        if kind == "claim" and str(row.get("claim_tier") or "") == "routing_context_only":
            continue
        selected.append(row)
    return selected


def canonical_record_id(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    kind = str(row.get("kind") or "")
    candidates = {
        "answer": payload.get("id"),
        "claim": payload.get("claim_id"),
        "concept": payload.get("concept_id") or first_concept_id(row),
        "contribution": payload.get("contribution_id"),
        "lava_context": payload.get("id") or payload.get("context_id"),
        "recipe": payload.get("recipe_id"),
        "source_summary": payload.get("id"),
        "rock_issue": payload.get("issue_id"),
        "task_card": f"{payload.get('concept_id')}:{payload.get('task_id')}"
        if payload.get("concept_id") and payload.get("task_id")
        else "",
    }
    value = str(candidates.get(kind) or row.get("id") or "unknown")
    prefixes = {
        "concept": "concept:",
        "contribution": "contribution:",
        "recipe": "recipe:",
        "source_summary": "source_summary:",
        "task_card": "task_card:",
    }
    prefix = prefixes.get(kind, "")
    return value if not prefix or value.startswith(prefix) else f"{prefix}{value}"


def row_content_hash(row: dict[str, Any]) -> str:
    value = {
        "body": row.get("body") or "",
        "payload": row.get("payload") if isinstance(row.get("payload"), dict) else {},
    }
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def stable_document_name(row: dict[str, Any]) -> str:
    canonical_id = canonical_record_id(row)
    digest = hashlib.sha256(canonical_id.encode("utf-8")).hexdigest()[:10]
    slug = safe_slug(canonical_id)[:160].rstrip("-.") or "record"
    return f"{slug}-{digest}.md"


def structured_record_path(row: dict[str, Any]) -> PurePosixPath:
    kind = safe_slug(str(row.get("kind") or "knowledge"))
    canonical_id = canonical_record_id(row)
    digest = hashlib.sha256(canonical_id.encode("utf-8")).hexdigest()
    return PurePosixPath("records") / kind / digest[:2] / stable_document_name(row).replace(".md", ".json")


def write_structured_record(destination: Path, row: dict[str, Any], *, profile: str) -> PurePosixPath:
    path = structured_record_path(row)
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    value = {
        "schema": "rock-kb-okf-structured-record-v1",
        "profile": profile,
        "kind": row.get("kind") or "knowledge",
        "canonical_id": canonical_record_id(row),
        "result_id": row.get("id") or "",
        "payload": payload,
    }
    target = destination / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def assert_unique_paths(mapping: dict[str, PurePosixPath], label: str) -> None:
    by_path: dict[PurePosixPath, list[str]] = defaultdict(list)
    for key, path in mapping.items():
        by_path[path].append(key)
    collisions = {path: keys for path, keys in by_path.items() if len(keys) > 1}
    if collisions:
        path, keys = sorted(collisions.items(), key=lambda item: item[0].as_posix())[0]
        raise ValueError(f"Colliding OKF {label} path {path}: {', '.join(sorted(keys))}")


def task_card_okf_rows(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": f"task_card:{record.get('concept_id')}:{record.get('task_id')}",
            "kind": "task_card",
            "title": record.get("title") or record.get("task_id"),
            "body": task_card_body(record),
            "path": record.get("path") or "agent/concept-task-cards.jsonl",
            "url": "",
            "concepts": [record.get("concept_id")] if record.get("concept_id") else [],
            "authority_tier": "community-reviewed",
            "claim_tier": "answer_pack_approved",
            "payload": record,
        }
        for record in records
        if record.get("task_id") and record.get("concept_id")
    ]


def task_card_body(record: dict[str, Any]) -> str:
    lines = [str(record.get("goal") or "")]
    if record.get("steps"):
        lines.extend(["", "## Steps", *[f"{index}. {step}" for index, step in enumerate(record["steps"], 1)]])
    if record.get("do_not_assume"):
        lines.extend(["", "## Do Not Assume", *[f"- {item}" for item in record["do_not_assume"]]])
    return "\n".join(lines).strip()


def ensure_safe_destination(destination: Path) -> None:
    if destination in {Path("/").resolve(), Path.home().resolve(), REPO_ROOT.resolve()} or (destination / ".git").exists():
        raise ValueError(f"Refusing to replace unsafe OKF export destination: {destination}")


def current_release_version() -> str:
    with (REPO_ROOT / "clients" / "python" / "pyproject.toml").open("rb") as handle:
        return str(tomllib.load(handle)["project"]["version"])


def current_source_commit() -> str:
    configured = os.environ.get("GITHUB_SHA") or os.environ.get("ROCK_KB_SOURCE_COMMIT")
    if configured:
        return configured
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def row_path(row: dict[str, Any]) -> PurePosixPath:
    kind = str(row.get("kind") or "")
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    canonical_id = canonical_record_id(row)
    digest = hashlib.sha256(canonical_id.encode("utf-8")).hexdigest()
    filename = stable_document_name(row)
    if kind == "claim":
        concept = safe_slug(str(payload.get("primary_concept_id") or first_concept_id(row) or "unrouted"))
        return PurePosixPath("claims") / concept / digest[:1] / filename
    if kind == "source_summary":
        source_id = safe_slug(str(payload.get("source_id") or "unknown"))
        return PurePosixPath("source-summaries") / source_id / digest[:1] / filename
    if kind in {"answer", "task_card"}:
        return PurePosixPath("answers" if kind == "answer" else "task-cards") / safe_slug(first_concept_id(row) or "unrouted") / filename
    if kind == "lava_context":
        return PurePosixPath("lava-contexts") / safe_slug(str(payload.get("context_family") or "other")) / filename
    if kind == "rock_issue":
        repository = "mobile" if payload.get("component") == "mobile_shell" else "core"
        return PurePosixPath("rock-issues") / repository / digest[:1] / digest[1:2] / filename
    if kind in {"recipe", "contribution"}:
        return PurePosixPath("recipes" if kind == "recipe" else "contributions") / safe_slug(str(payload.get("org_id") or "community")) / filename
    if kind == "model_map":
        category = safe_slug(str(payload.get("identity", {}).get("model_category") or "other"))
        return PurePosixPath("models") / category / filename
    if kind == "concept":
        return PurePosixPath("concepts") / f"{safe_slug(first_concept_id(row) or canonical_id)}.md"
    return PurePosixPath(safe_slug(kind or "knowledge")) / filename


def kind_type_for_row(row: dict[str, Any]) -> str:
    kind = str(row.get("kind") or "")
    if kind == "contribution":
        return "Contribution Provenance"
    if kind == "task_card":
        return "Agent Task Card"
    return KIND_CONFIG.get(kind, ("Knowledge", "knowledge"))[0]


def row_kind_count_key(row: dict[str, Any]) -> str:
    return {
        "model_map": "models",
        "lava_context": "lava_contexts",
        "source_summary": "source_summaries",
        "task_card": "task_cards",
        "rock_issue": "rock_issues",
    }.get(str(row.get("kind") or ""), f"{row.get('kind')}s")


def row_title(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    if row.get("kind") == "claim":
        return compact_text(str(payload.get("title") or payload.get("claim") or row.get("title") or "Claim"), 120)
    return compact_text(str(row.get("title") or row.get("id") or "Untitled"), 140)


def row_description(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    candidates = (
        row.get("okf_description"),
        payload.get("description"),
        payload.get("distilled_summary"),
        payload.get("summary"),
        payload.get("claim"),
        payload.get("answer"),
        payload.get("goal"),
        row.get("body"),
    )
    body = next((str(value) for value in candidates if value), "")
    body = strip_frontmatter(body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"[#*_`>|\[\]]", " ", body)
    return compact_text(body, 240)


def row_timestamp(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    for key in ("updated_at", "created_at", "timestamp", "last_built", "retrieved_at"):
        if payload.get(key):
            return str(payload[key])
    return ""


def row_tags(row: dict[str, Any], known_concepts: set[str]) -> list[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values = [str(row.get("kind") or "")]
    values.extend(concept_ids_for_row(row, known_concepts))
    values.extend(str(value) for value in payload.get("topics") or [])
    values.extend(str(value) for value in payload.get("topic_labels") or [])
    return sorted({safe_slug(value) for value in values if value})


def rock_versions_for_row(row: dict[str, Any]) -> list[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values: list[Any] = []
    for key in ("rock_versions", "tested_rock_versions"):
        value = payload.get(key)
        values.extend(value if isinstance(value, list) else [value] if value else [])
    for key in ("rock_version",):
        if payload.get(key):
            values.append(payload[key])
    identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
    if identity.get("rock_version"):
        values.append(identity["rock_version"])
    compatibility = payload.get("compatibility") if isinstance(payload.get("compatibility"), dict) else {}
    values.extend(compatibility.get("tested_rock_versions") or [])
    for evidence in payload.get("version_evidence") or []:
        if isinstance(evidence, dict) and evidence.get("normalized_version"):
            values.append(evidence["normalized_version"])
    return sorted({str(value) for value in values if value})


def concept_ids_for_row(row: dict[str, Any], known_concepts: set[str]) -> list[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values: list[Any] = []
    for value in (row.get("concepts"), payload.get("concept_ids"), payload.get("topics")):
        values.extend(value if isinstance(value, list) else [value] if value else [])
    for value in (row.get("concept"), payload.get("concept_id"), payload.get("primary_concept_id")):
        if value:
            values.append(value)
    return sorted({str(value) for value in values if str(value) in known_concepts})


def first_concept_id(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    for value in (row.get("concept"), payload.get("concept_id"), payload.get("primary_concept_id")):
        if value:
            return str(value)
    for values in (row.get("concepts"), payload.get("concept_ids"), payload.get("topics")):
        if isinstance(values, list) and values:
            return str(values[0])
    return ""


def source_ids_for_row(row: dict[str, Any]) -> set[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values: set[str] = set()
    if payload.get("source_id"):
        values.add(str(payload["source_id"]))
    for item in payload.get("source_refs") or []:
        if isinstance(item, dict) and item.get("source_id"):
            values.add(str(item["source_id"]))
    for item in payload.get("citations") or []:
        if isinstance(item, dict) and item.get("source_id"):
            values.add(str(item["source_id"]))
    if row.get("kind") == "model_map":
        values.add("rock_model_map")
    return values


def model_slugs_for_row(row: dict[str, Any]) -> set[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values: set[str] = set()
    for item in payload.get("model_map_links") or []:
        if isinstance(item, dict) and item.get("model_slug"):
            values.add(str(item["model_slug"]))
        elif isinstance(item, str) and item.startswith("model_map:stable:"):
            values.add(item.removeprefix("model_map:stable:"))
    if row.get("kind") == "model_map":
        for item in payload.get("relationships") or []:
            if isinstance(item, dict) and item.get("target_model_slug"):
                values.add(str(item["target_model_slug"]))
    if row.get("kind") == "task_card":
        values.update(safe_slug(str(value)) for value in payload.get("entities") or [])
    return values


def related_paths_for_row(
    row: dict[str, Any],
    *,
    concept_ids: set[str],
    concept_paths: dict[str, PurePosixPath],
    reference_paths: dict[str, PurePosixPath],
    model_path_by_slug: dict[str, PurePosixPath],
    path_by_id: dict[str, PurePosixPath],
) -> list[tuple[str, PurePosixPath]]:
    related: list[tuple[str, PurePosixPath]] = []
    current_path = path_by_id.get(str(row.get("id") or ""))
    for concept_id in concept_ids_for_row(row, concept_ids):
        if concept_paths[concept_id] != current_path:
            related.append(("about", concept_paths[concept_id]))
    for source_id in sorted(source_ids_for_row(row)):
        if source_id in reference_paths:
            related.append(("supported_by", reference_paths[source_id]))
    for slug in sorted(model_slugs_for_row(row)):
        if slug in model_path_by_slug and model_path_by_slug[slug] != path_by_id.get(str(row.get("id") or "")):
            related.append(("uses_model" if row.get("kind") != "model_map" else "related_model", model_path_by_slug[slug]))
    if row.get("kind") == "recipe":
        payload = row.get("payload") or {}
        for contribution_id in payload.get("supersedes_contribution_ids") or []:
            target_id = f"contribution:{contribution_id}"
            if target_id in path_by_id:
                related.append(("supersedes", path_by_id[target_id]))
    return sorted(set(related), key=lambda item: (item[0], item[1].as_posix()))


def render_row_body(
    row: dict[str, Any],
    *,
    current_path: PurePosixPath,
    related: list[tuple[str, PurePosixPath]],
    commit: str,
    profile: str,
) -> tuple[list[str], str]:
    title = row_title(row)
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    source_path = str(row.get("path") or payload.get("path") or payload.get("source_file") or "")
    if row.get("kind") == "concept":
        concept_id = first_concept_id(row)
        guide_path = REPO_ROOT / "knowledge" / "concepts" / concept_id / "guide.md"
        if guide_path.exists():
            body_text = strip_frontmatter(guide_path.read_text(encoding="utf-8"))
            source_path = guide_path.relative_to(REPO_ROOT).as_posix()
        else:
            body_text = str(row.get("body") or "")
    elif row.get("kind") == "model_map":
        detail_path = str((payload.get("identity") or {}).get("model_detail_path") or "")
        if profile == "full" and detail_path and (REPO_ROOT / detail_path).exists():
            body_text = strip_frontmatter((REPO_ROOT / detail_path).read_text(encoding="utf-8"))
            source_path = detail_path
        else:
            body_text = render_compact_model_body(payload)
    else:
        body_text = narrative_body(row)
    if row.get("kind") == "concept":
        body_text = rewrite_repo_relative_links(body_text, source_path, commit)
    else:
        body_text = rewrite_source_relative_links(body_text, primary_resource_url(row))
    body_text = strip_duplicate_title(body_text, title)
    lines = [f"# {title}", "", body_text.strip() or "No narrative summary is available."]

    if related:
        lines.extend(["", "## Related Knowledge", ""])
        for relation_type, target in related:
            lines.append(f"- `{relation_type}`: [{target.stem}](/{target.as_posix()})")

    citations = citations_for_row(row)
    if citations:
        lines.extend(["", "## Citations", ""])
        for index, citation in enumerate(citations, 1):
            lines.append(f"[{index}] [{markdown_label(citation['title'])}](<{citation['url']}>)")

    return lines, source_path


def strip_duplicate_title(body: str, title: str) -> str:
    lines = body.lstrip().splitlines()
    if lines and lines[0].strip().lstrip("#").strip().casefold() == title.strip().casefold():
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines)


def render_compact_model_body(payload: dict[str, Any]) -> str:
    identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
    counts = payload.get("counts") if isinstance(payload.get("counts"), dict) else {}
    lines = [
        str(identity.get("description") or payload.get("description") or "Rock model reference."),
        "",
        "## Identity",
        "",
        f"- Model: `{identity.get('model_title') or identity.get('model_name') or 'unknown'}`",
        f"- Slug: `{identity.get('model_slug') or 'unknown'}`",
        f"- Category: `{identity.get('model_category') or 'unknown'}`",
        f"- Rock version: `{identity.get('rock_version') or 'unknown'}`",
        f"- Table: `{identity.get('table_name') or 'not provided'}`",
        "",
        "## Counts",
        "",
        *[f"- {str(key).replace('_', ' ').title()}: {value}" for key, value in sorted(counts.items())],
    ]
    required = payload.get("required_fields") or []
    if required:
        lines.extend(["", "## Required Fields", ""])
        for item in required:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('name') or item.get('property_name') or 'unknown'}`: {item.get('description') or ''}")
    notes = payload.get("operational_notes") or []
    if notes:
        lines.extend(["", "## Operational Notes", "", *[f"- {note}" for note in notes]])
    relationships = payload.get("relationships") or []
    if relationships:
        lines.extend(["", "## Relationships", ""])
        for item in relationships:
            if isinstance(item, dict):
                target = item.get("target_model_name") or item.get("target_model_slug") or item.get("name") or "unknown"
                prop = item.get("property_name") or item.get("name") or "relationship"
                lines.append(f"- `{prop}` -> `{target}`")
    diffs = payload.get("version_diffs") or []
    if diffs:
        lines.extend(["", "## Version Diffs", ""])
        for item in diffs:
            lines.append(f"- {item if isinstance(item, str) else json.dumps(item, sort_keys=True)}")
    return "\n".join(lines).strip()


def narrative_body(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    if row.get("kind") != "source_summary":
        return str(row.get("body") or "")
    lines = [str(payload.get("summary") or row.get("body") or "")]
    insights = [str(value) for value in payload.get("key_insights") or [] if value]
    if insights:
        lines.extend(["", "## Key Insights", *[f"- {value}" for value in insights]])
    if payload.get("agent_use"):
        lines.extend(["", "## Agent Use", "", str(payload["agent_use"])])
    return "\n".join(lines).strip()


def citations_for_row(row: dict[str, Any]) -> list[dict[str, str]]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    citations: list[dict[str, str]] = []
    by_url: dict[str, int] = {}

    def add(title: Any, url: Any) -> None:
        clean_url = str(url or "").strip()
        if not clean_url or not re.match(r"^https?://", clean_url):
            return
        candidate = {"title": str(title or clean_url).strip(), "url": clean_url}
        if clean_url in by_url:
            index = by_url[clean_url]
            current_title = citations[index]["title"]
            if current_title in {clean_url, str(row.get("title") or "")} and candidate["title"] != clean_url:
                citations[index] = candidate
            return
        by_url[clean_url] = len(citations)
        citations.append(candidate)

    add(row.get("title"), row.get("url"))
    for key in ("citations", "source_refs"):
        for item in payload.get(key) or []:
            if isinstance(item, dict):
                add(item.get("title") or item.get("source_id"), item.get("source_timestamp_url") or item.get("url"))
    for url in payload.get("source_urls") or payload.get("evidence_urls") or []:
        add("Evidence", url)
    for key in ("source_url",):
        add(payload.get("source_title") or payload.get("title"), payload.get(key))
    identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
    add("Rock Model Map", identity.get("source_url"))
    implementation = payload.get("implementation") if isinstance(payload.get("implementation"), dict) else {}
    add("Implementation repository", implementation.get("repository_url"))
    add("Implementation manifest", implementation.get("manifest_url"))
    return citations


def primary_resource_url(row: dict[str, Any]) -> str:
    citations = citations_for_row(row)
    return citations[0]["url"] if citations else ""


def related_link_lines(
    current_path: PurePosixPath,
    rows: Iterable[dict[str, Any]],
    path_by_id: dict[str, PurePosixPath],
) -> list[str]:
    lines = []
    for row in rows:
        target = path_by_id[str(row["id"])]
        lines.append(f"- [{markdown_label(row_title(row))}](/{target.as_posix()})")
    return lines or ["No related canonical records."]


def write_directory_indexes(
    destination: Path,
    entries: dict[PurePosixPath, list[tuple[PurePosixPath, str, str]]],
) -> None:
    all_directories: set[Path] = set()
    for path in destination.rglob("*.md"):
        parent = path.parent
        while parent != destination:
            all_directories.add(parent)
            parent = parent.parent
    for directory in sorted(all_directories, key=lambda path: path.relative_to(destination).as_posix()):
        relative_dir = PurePosixPath(directory.relative_to(destination).as_posix())
        rows = sorted(entries.get(relative_dir, []), key=lambda item: (item[1].lower(), item[0].as_posix()))
        title = relative_dir.name.replace("-", " ").title()
        lines = [f"# {title}", ""]
        child_dirs = sorted(
            child
            for child in directory.iterdir()
            if child.is_dir() and any(path.suffix == ".md" for path in child.rglob("*.md"))
        )
        if child_dirs:
            lines.extend(["## Groups", ""])
            for child in child_dirs:
                lines.append(f"- [{child.name.replace('-', ' ').title()}]({child.name}/)")
            lines.append("")
        if rows:
            if len(rows) > MAX_INDEX_ENTRIES:
                raise ValueError(f"OKF index {relative_dir}/index.md has {len(rows)} entries; maximum is {MAX_INDEX_ENTRIES}")
            lines.extend(["## Documents", ""])
            for path, row_title_value, description in rows:
                relative = posixpath.relpath(path.as_posix(), relative_dir.as_posix())
                suffix = f" - {description}" if description else ""
                lines.append(f"- [{markdown_label(row_title_value)}]({relative}){suffix}")
        content = "\n".join(lines).rstrip() + "\n"
        if len(content.encode("utf-8")) > MAX_INDEX_BYTES:
            raise ValueError(f"OKF index {relative_dir}/index.md exceeds {MAX_INDEX_BYTES} bytes")
        (directory / "index.md").write_text(content, encoding="utf-8")


def copy_distribution_licenses(destination: Path) -> None:
    for source_name, target_name in (("LICENSE", "LICENSE.txt"), ("NOTICE", "NOTICE.txt")):
        source = REPO_ROOT / source_name
        if not source.exists():
            raise ValueError(f"Missing repository licensing file required for OKF export: {source_name}")
        shutil.copyfile(source, destination / target_name)


def write_profile_document(destination: Path, *, generated_at: str) -> None:
    source = REPO_ROOT / "docs" / "specs" / "rock-kb-okf-profile-v1.md"
    if not source.exists():
        raise ValueError(f"Missing Rock OKF extension profile: {source.relative_to(REPO_ROOT)}")
    text = source.read_text(encoding="utf-8")
    metadata = read_frontmatter(text)
    metadata["timestamp"] = generated_at
    write_typed_markdown(destination / "profile.md", metadata, strip_frontmatter(text).strip().splitlines())


def snapshot_hashes(destination: Path) -> dict[str, str]:
    excluded = {MANIFEST_NAME, FILE_MANIFEST_NAME, CHECKSUMS_NAME, "log.md"}
    return {
        path.relative_to(destination).as_posix(): sha256_file(path)
        for path in sorted(path for path in destination.rglob("*") if path.is_file())
        if path.relative_to(destination).as_posix() not in excluded
    }


def previous_snapshot(bundle: Path | None) -> tuple[str, dict[str, str]]:
    if bundle is None or not bundle.exists():
        return "", {}
    files: dict[str, bytes]
    if bundle.is_dir():
        files = {
            path.relative_to(bundle).as_posix(): path.read_bytes()
            for path in bundle.rglob("*")
            if path.is_file()
        }
    elif zipfile.is_zipfile(bundle):
        with zipfile.ZipFile(bundle) as archive:
            files = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    elif tarfile.is_tarfile(bundle):
        files = {}
        with tarfile.open(bundle, "r:*") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                extracted = archive.extractfile(member)
                if extracted is not None:
                    files[member.name] = extracted.read()
    else:
        return "", {}

    manifest_name = next((name for name in files if PurePosixPath(name).name == MANIFEST_NAME), "")
    file_manifest_name = next((name for name in files if PurePosixPath(name).name == FILE_MANIFEST_NAME), "")
    if not manifest_name or not file_manifest_name:
        return "", {}
    root = PurePosixPath(manifest_name).parent
    manifest = json.loads(files[manifest_name].decode("utf-8"))
    hashes: dict[str, str] = {}
    excluded = {MANIFEST_NAME, FILE_MANIFEST_NAME, CHECKSUMS_NAME, "log.md"}
    for line in files[file_manifest_name].decode("utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        relative = PurePosixPath(str(row.get("path") or ""))
        try:
            normalized = relative.relative_to(root).as_posix() if root.parts else relative.as_posix()
        except ValueError:
            normalized = relative.as_posix()
        if normalized not in excluded:
            hashes[normalized] = str(row.get("sha256") or "")
    return str(manifest.get("distribution_version") or ""), hashes


def write_update_log(
    destination: Path,
    *,
    generated_at: str,
    version: str,
    previous_bundle: Path | None,
) -> dict[str, Any]:
    previous_version, old_hashes = previous_snapshot(previous_bundle)
    new_hashes = snapshot_hashes(destination)
    added = sorted(set(new_hashes) - set(old_hashes))
    removed = sorted(set(old_hashes) - set(new_hashes))
    changed = sorted(path for path in set(new_hashes) & set(old_hashes) if new_hashes[path] != old_hashes[path])
    change_type = "Update" if old_hashes else "Creation"
    lines = [
        "# Directory Update Log",
        "",
        f"## {generated_at[:10]}",
        "",
        f"* **{change_type}**: Generated Rock KB OKF distribution v{version}.",
        f"* **Profile delta**: {len(added)} added, {len(changed)} changed, and {len(removed)} removed files.",
    ]
    if previous_version:
        lines.append(f"* **Previous version**: v{previous_version}.")
    for heading, paths in (("Added", added), ("Changed", changed), ("Removed", removed)):
        if not paths:
            continue
        lines.extend(["", f"### {heading}", ""])
        lines.extend(f"- `{path}`" for path in paths[:50])
        if len(paths) > 50:
            lines.append(f"- ...and {len(paths) - 50} more; see `{FILE_MANIFEST_NAME}` for the complete snapshot.")
    (destination / "log.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {
        "previous_version": previous_version,
        "added": len(added),
        "changed": len(changed),
        "removed": len(removed),
    }


def write_root_index(
    destination: Path,
    *,
    generated_at: str,
    version: str,
    commit: str,
    rows: list[dict[str, Any]],
    profile: str,
) -> None:
    counts = Counter(row_kind_count_key(row) for row in rows)
    browse_options = [
        ("concepts", "Concept guides", "concepts/"),
        ("answers", "Agent answers", "answers/"),
        ("claims", "Approved claims", "claims/"),
        ("contributions", "Community contribution provenance", "contributions/"),
        ("recipes", "Community recipes", "recipes/"),
        ("lava_contexts", "Lava contexts", "lava-contexts/"),
        ("models", "Rock models", "models/"),
        ("rock_issues", "Rock issues", "rock-issues/"),
        ("source_summaries", "Source summaries", "source-summaries/"),
        ("task_cards", "Agent task cards", "task-cards/"),
    ]
    browse_lines = [
        f"- [{label}]({path})"
        for count_key, label, path in browse_options
        if counts.get(count_key, 0) > 0
    ]
    browse_lines.extend(
        [
            "- [Evidence sources](references/)",
            "- [Rock OKF extension profile](profile.md)",
        ]
    )
    frontmatter = yaml.safe_dump(
        {
            "okf_version": OKF_VERSION,
            "title": "Rock RMS Agent Knowledge Base",
            "description": "Read-only, portable distribution of the canonical public Rock KB.",
            "timestamp": generated_at,
            "distribution_version": version,
            "source_commit": commit,
            "profile": profile,
            "okf_profile": OKF_PROFILE_SCHEMA,
        },
        allow_unicode=False,
        sort_keys=False,
    ).strip()
    lines = [
        "---",
        frontmatter,
        "---",
        "",
        "# Rock RMS Agent Knowledge Base",
        "",
        f"This is the complete read-only Open Knowledge Format distribution ({profile} profile) of the canonical public Rock KB. The source registries, JSONL records, hosted search service, and MCP server remain canonical.",
        "",
        "## Browse",
        "",
        *browse_lines,
        "",
        "## Counts",
        "",
        *[f"- {key.replace('_', ' ').title()}: {value}" for key, value in sorted(counts.items())],
        "",
        "## Distribution Metadata",
        "",
        f"- OKF version: `{OKF_VERSION}`",
        f"- Distribution version: `{version}`",
        f"- Distribution profile: `{profile}`",
        f"- Source commit: `{commit}`",
        f"- Generated at: `{generated_at}`",
        f"- Manifest: [`{MANIFEST_NAME}`]({MANIFEST_NAME})",
        f"- Checksums: [`{CHECKSUMS_NAME}`]({CHECKSUMS_NAME})",
        "- Licensing: [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt)",
    ]
    (destination / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_typed_markdown(path: Path, frontmatter: dict[str, Any], body: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_text = yaml.safe_dump(frontmatter, allow_unicode=False, sort_keys=False).strip()
    path.write_text(f"---\n{yaml_text}\n---\n\n" + "\n".join(body).rstrip() + "\n", encoding="utf-8")


def compact_frontmatter(frontmatter: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in frontmatter.items() if value not in (None, "", [], {})}


def write_file_manifest(destination: Path) -> None:
    rows = []
    for path in sorted(path for path in destination.rglob("*") if path.is_file()):
        relative = path.relative_to(destination).as_posix()
        if relative in {MANIFEST_NAME, FILE_MANIFEST_NAME, CHECKSUMS_NAME}:
            continue
        rows.append({"path": relative, "sha256": sha256_file(path), "bytes": path.stat().st_size})
    (destination / FILE_MANIFEST_NAME).write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8"
    )


def write_checksums(destination: Path) -> None:
    paths = sorted(
        path
        for path in destination.rglob("*")
        if path.is_file() and path.name != CHECKSUMS_NAME
    )
    (destination / CHECKSUMS_NAME).write_text(
        "".join(f"{sha256_file(path)}  {path.relative_to(destination).as_posix()}\n" for path in paths),
        encoding="utf-8",
    )


def create_okf_archives(
    destination: Path,
    archive_dir: Path,
    version: str,
    *,
    profile: str = "full",
) -> list[dict[str, Any]]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"rock-agent-kb-okf-v{version}" if profile == "full" else f"rock-agent-kb-okf-{profile}-v{version}"
    zip_path = archive_dir / f"{base_name}.zip"
    tar_path = archive_dir / f"{base_name}.tar.gz"
    root_name = base_name
    epoch = archive_epoch()
    zip_datetime = datetime.fromtimestamp(max(epoch, 315532800), tz=timezone.utc).timetuple()[:6]

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(path for path in destination.rglob("*") if path.is_file()):
            relative = path.relative_to(destination).as_posix()
            info = zipfile.ZipInfo(f"{root_name}/{relative}", date_time=zip_datetime)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)

    with tar_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for path in sorted(path for path in destination.rglob("*") if path.is_file()):
                    relative = path.relative_to(destination).as_posix()
                    data = path.read_bytes()
                    info = tarfile.TarInfo(f"{root_name}/{relative}")
                    info.size = len(data)
                    info.mode = 0o644
                    info.mtime = epoch
                    archive.addfile(info, io.BytesIO(data))

    checksum_path = archive_dir / f"{base_name}.sha256"
    checksum_path.write_text(
        f"{sha256_file(zip_path)}  {zip_path.name}\n{sha256_file(tar_path)}  {tar_path.name}\n",
        encoding="utf-8",
    )
    return [
        {"path": str(path), "name": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in (zip_path, tar_path, checksum_path)
    ]


def archive_epoch() -> int:
    if os.environ.get("SOURCE_DATE_EPOCH"):
        return int(os.environ["SOURCE_DATE_EPOCH"])
    return int(datetime.now(timezone.utc).timestamp())


def audit_okf_export(destination: Path) -> list[str]:
    errors: list[str] = []
    root_index = destination / "index.md"
    root_log = destination / "log.md"
    if not root_index.exists():
        errors.append("missing reserved root file: index.md")
    else:
        root_meta = read_frontmatter(root_index.read_text(encoding="utf-8"))
        if str(root_meta.get("okf_version") or "") != OKF_VERSION:
            errors.append(f"index.md must declare okf_version {OKF_VERSION}")
    if not root_log.exists():
        errors.append("missing reserved root file: log.md")

    structured_paths: set[str] = set()
    for path in sorted(destination.rglob("*.md")):
        relative = path.relative_to(destination).as_posix()
        text = path.read_text(encoding="utf-8")
        if path.name in RESERVED_FILENAMES:
            if relative != "index.md" and text.startswith("---\n"):
                errors.append(f"reserved file must not have frontmatter: {relative}")
            if path.name == "log.md":
                for line in text.splitlines():
                    if line.startswith("## ") and not LOG_DATE_RE.match(line):
                        errors.append(f"{relative} has non-ISO date heading: {line}")
        else:
            frontmatter = read_frontmatter(text)
            if not frontmatter.get("type"):
                errors.append(f"{relative} missing non-empty type frontmatter")
            structured_record = str(frontmatter.get("structured_record") or "").lstrip("/")
            if structured_record and not (destination / structured_record).exists():
                errors.append(f"{relative} has missing structured record: {structured_record}")
            elif structured_record:
                if structured_record in structured_paths:
                    errors.append(f"duplicate structured record reference: {structured_record}")
                structured_paths.add(structured_record)
                try:
                    record = json.loads((destination / structured_record).read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                    errors.append(f"{structured_record} is not valid structured-record JSON")
                else:
                    if record.get("schema") != "rock-kb-okf-structured-record-v1":
                        errors.append(f"{structured_record} has unexpected structured-record schema")
                    if str(record.get("canonical_id") or "") != str(
                        frontmatter.get("canonical_id") or frontmatter.get("id") or ""
                    ):
                        errors.append(f"{relative} canonical ID does not match {structured_record}")
            for relation in frontmatter.get("relationships") or []:
                if isinstance(relation, dict) and str(relation.get("target") or "").lstrip("/") == relative:
                    errors.append(f"{relative} has self relationship")
        for target in markdown_targets(text):
            resolved = resolve_markdown_target(relative, target)
            if resolved:
                try:
                    exists = len(resolved) <= 4096 and (destination / resolved).exists()
                except OSError:
                    exists = False
                if not exists:
                    errors.append(f"{relative} has unresolved link: {target[:500]}")
        for marker in PRIVATE_MARKERS:
            if marker.lower() in text.lower():
                errors.append(f"{relative} contains private marker: {marker}")

    record_paths = {
        path.relative_to(destination).as_posix()
        for path in destination.glob("records/**/*.json")
        if path.is_file()
    }
    for relative in sorted(record_paths - structured_paths):
        errors.append(f"unreferenced structured record: {relative}")

    for path in sorted(path for path in destination.rglob("*") if path.is_file() and path.suffix != ".md"):
        relative = path.relative_to(destination).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in PRIVATE_MARKERS:
            if marker.lower() in text.lower():
                errors.append(f"{relative} contains private marker: {marker}")

    manifest_path = destination / MANIFEST_NAME
    if not manifest_path.exists():
        errors.append(f"missing {MANIFEST_NAME}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("schema") != "rock-kb-okf-distribution-v1":
                errors.append(f"{MANIFEST_NAME} has unexpected schema")
            if str(manifest.get("okf_version") or "") != OKF_VERSION:
                errors.append(f"{MANIFEST_NAME} has unexpected okf_version")
            if manifest.get("read_only") is not True:
                errors.append(f"{MANIFEST_NAME} must declare read_only true")
            if manifest.get("profile") not in OKF_PROFILES:
                errors.append(f"{MANIFEST_NAME} has unexpected profile")
            if manifest.get("okf_profile") != OKF_PROFILE_SCHEMA:
                errors.append(f"{MANIFEST_NAME} has unexpected OKF extension profile")
            if manifest.get("okf_spec_commit") != OKF_SPEC_COMMIT:
                errors.append(f"{MANIFEST_NAME} has unexpected OKF specification commit")
            license_info = manifest.get("license") if isinstance(manifest.get("license"), dict) else {}
            if license_info.get("code") != "MIT" or license_info.get("original_content") != "CC-BY-4.0":
                errors.append(f"{MANIFEST_NAME} has incomplete distribution licensing")
            file_manifest_path = destination / FILE_MANIFEST_NAME
            if not file_manifest_path.exists():
                errors.append(f"missing {FILE_MANIFEST_NAME}")
            elif manifest.get("file_manifest_sha256") != sha256_file(file_manifest_path):
                errors.append(f"{FILE_MANIFEST_NAME} does not match the manifest digest")
            relationships_path = destination / "relationships.jsonl"
            if not relationships_path.exists():
                errors.append("missing relationships.jsonl")
            else:
                relationship_count = sum(
                    1 for line in relationships_path.read_text(encoding="utf-8").splitlines() if line.strip()
                )
                if manifest.get("relationships") != relationship_count:
                    errors.append(
                        f"relationship count mismatch: expected {manifest.get('relationships')}, found {relationship_count}"
                    )
        except (OSError, json.JSONDecodeError):
            errors.append(f"{MANIFEST_NAME} is not valid JSON")

    errors.extend(audit_checksums(destination))
    return sorted(set(errors))


def audit_checksums(destination: Path) -> list[str]:
    checksum_path = destination / CHECKSUMS_NAME
    if not checksum_path.exists():
        return [f"missing {CHECKSUMS_NAME}"]
    errors = []
    seen: set[str] = set()
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid checksum row: {line}")
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"invalid checksum digest: {line}")
            continue
        if relative in seen:
            errors.append(f"duplicate checksum target: {relative}")
            continue
        seen.add(relative)
        relative_path = PurePosixPath(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            errors.append(f"unsafe checksum target: {relative}")
            continue
        target = destination / relative
        if not target.exists():
            errors.append(f"checksum target missing: {relative}")
        elif sha256_file(target) != expected:
            errors.append(f"checksum mismatch: {relative}")
    expected_paths = {
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file() and path.name != CHECKSUMS_NAME
    }
    for relative in sorted(expected_paths - seen):
        errors.append(f"file missing checksum: {relative}")
    return errors


def read_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    try:
        value = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    return text[end + 5 :] if end >= 0 else text


def markdown_targets(text: str) -> list[str]:
    targets = []
    without_fences = strip_fenced_blocks(text)
    for match in MARKDOWN_LINK_RE.finditer(without_fences):
        target = match.group(1).strip().strip("<>").split("#", 1)[0].strip()
        if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            targets.append(target)
    return targets


def strip_fenced_blocks(text: str) -> str:
    kept: list[str] = []
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if not fence and marker:
            fence = marker.group(1)[0]
            continue
        if fence and re.match(rf"^{re.escape(fence)}{{3,}}\s*$", stripped):
            fence = ""
            continue
        if not fence:
            kept.append(line)
    return "\n".join(kept)


def resolve_markdown_target(source_relative: str, target: str) -> str:
    if target.startswith("/"):
        candidate = posixpath.normpath(target.lstrip("/"))
    else:
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source_relative), target))
    if candidate.startswith("../") or candidate == "..":
        return ""
    return candidate


def rewrite_repo_relative_links(text: str, source_path: str, commit: str) -> str:
    if not source_path or not text:
        return text

    source_dir = PurePosixPath(source_path).parent

    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(1).strip().strip("<>")
        if not raw_target or raw_target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", raw_target, re.IGNORECASE):
            return match.group(0)
        path_part, separator, anchor = raw_target.partition("#")
        repo_target = posixpath.normpath(posixpath.join(source_dir.as_posix(), path_part))
        if repo_target.startswith("../"):
            return match.group(0)
        url = f"https://github.com/ONE-ALL-Church/rock-agent-kb/blob/{commit}/{repo_target}"
        if separator:
            url += f"#{anchor}"
        return match.group(0).replace(match.group(1), f"<{url}>")

    return MARKDOWN_LINK_RE.sub(replace, text)


def rewrite_source_relative_links(text: str, base_url: str) -> str:
    if not text:
        return text

    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(1).strip().strip("<>")
        if not raw_target or raw_target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", raw_target, re.IGNORECASE):
            return match.group(0)
        if not base_url:
            return match.group(0).replace(f"]({match.group(1)})", f"] (`{raw_target}`)")
        return match.group(0).replace(match.group(1), f"<{urljoin(base_url, raw_target)}>")

    return MARKDOWN_LINK_RE.sub(replace, text)


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", value.lower()).strip("-") or "unknown"


def compact_text(value: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def markdown_label(value: str) -> str:
    return value.replace("[", "(").replace("]", ")")


def relationship(relation_type: str, source: str, target: str) -> dict[str, str]:
    return {
        "schema": "rock-kb-okf-relationship-v1",
        "type": relation_type,
        "source": source,
        "target": target,
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
