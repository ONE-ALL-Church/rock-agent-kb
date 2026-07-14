from __future__ import annotations

import gzip
import hashlib
import json
import os
import posixpath
import re
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
KIND_CONFIG = {
    "concept": ("Concept", "concepts"),
    "answer": ("Agent Answer", "answers"),
    "claim": ("Claim", "claims"),
    "model_map": ("Rock Model", "models"),
    "lava_context": ("Lava Context", "lava-contexts"),
    "recipe": ("Community Recipe", "recipes"),
    "source_summary": ("Source Summary", "source-summaries"),
}


def build_okf_export(
    destination: Path | None = None,
    *,
    distribution_version: str | None = None,
    source_commit: str | None = None,
    archive_dir: Path | None = None,
) -> dict[str, Any]:
    destination = (destination or DEFAULT_OKF_EXPORT_DIR).resolve()
    ensure_safe_destination(destination)
    if destination.exists():
        import shutil

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
    full_models = {
        str((row.get("identity") or {}).get("model_slug") or ""): row
        for row in read_jsonl(REPO_ROOT / "agent" / "model-map-digests.jsonl")
    }
    full_lava_contexts = {
        str(row.get("id") or row.get("context_id") or ""): row
        for row in read_jsonl(REPO_ROOT / "agent" / "lava-contexts.jsonl")
    }
    for row in search_rows:
        if row.get("kind") == "model_map":
            slug = str((row.get("payload") or {}).get("identity", {}).get("model_slug") or "")
            if slug in full_models:
                row["payload"] = full_models[slug]
        elif row.get("kind") == "lava_context" and str(row.get("id") or "") in full_lava_contexts:
            row["payload"] = full_lava_contexts[str(row["id"])]
    contribution_rows = contribution_okf_rows(public_contribution_records())
    task_rows = task_card_okf_rows(read_jsonl(REPO_ROOT / "agent" / "concept-task-cards.jsonl"))
    rows = sorted([*search_rows, *contribution_rows, *task_rows], key=lambda row: str(row.get("id") or ""))
    duplicate_ids = sorted(row_id for row_id, count in Counter(str(row.get("id") or "") for row in rows).items() if row_id and count > 1)
    if duplicate_ids:
        raise ValueError(f"Duplicate canonical OKF record ids: {', '.join(duplicate_ids[:10])}")

    path_by_id = {str(row["id"]): row_path(row) for row in rows}
    model_path_by_slug = {
        str((row.get("payload") or {}).get("identity", {}).get("model_slug") or ""): path_by_id[str(row["id"])]
        for row in rows
        if row.get("kind") == "model_map"
    }
    reference_paths = {source_id: PurePosixPath("references") / f"{safe_slug(source_id)}.md" for source_id in public_sources}
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
            *related_link_lines(path, related[:500], path_by_id),
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
        body = render_row_body(
            row,
            current_path=path,
            related=related,
            commit=commit,
        )
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        frontmatter = compact_frontmatter(
            {
                "type": kind_type,
                "id": row_id,
                "title": title,
                "description": description,
                "resource": primary_resource_url(row),
                "tags": row_tags(row, concept_ids),
                "timestamp": row_timestamp(row),
                "authority_tier": row.get("authority_tier") or payload.get("authority_tier"),
                "claim_tier": row.get("claim_tier") or payload.get("claim_tier"),
                "rock_versions": rock_versions_for_row(row),
                "source_path": row.get("path") or payload.get("path") or payload.get("source_file"),
                "relationships": row_relationships,
            }
        )
        write_typed_markdown(destination / path, frontmatter, body)
        index_entries[path.parent].append((path, title, description))

    write_directory_indexes(destination, index_entries)
    write_root_index(destination, generated_at=generated_at, version=version, commit=commit, rows=rows)
    (destination / "log.md").write_text(
        f"# Directory Update Log\n\n## {generated_at[:10]}\n\n* **Creation**: Generated Rock KB OKF distribution v{version}.\n",
        encoding="utf-8",
    )

    relationship_rows = sorted(
        {json.dumps(row, ensure_ascii=False, sort_keys=True) for row in relationships}
    )
    (destination / "relationships.jsonl").write_text(
        "".join(line + "\n" for line in relationship_rows), encoding="utf-8"
    )

    counts = Counter(row_kind_count_key(row) for row in rows)
    counts["references"] = len(public_sources)
    write_file_manifest(destination)
    report = {
        "schema": "rock-kb-okf-distribution-v1",
        "okf_version": OKF_VERSION,
        "distribution_version": version,
        "generated_at": generated_at,
        "source_commit": commit,
        "read_only": True,
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
        ],
        "excluded_scope": [
            "private organization overlays",
            "raw transcripts and media",
            "review queues and live-instance evidence",
            "evaluation and telemetry artifacts",
            "redundant generated indexes",
        ],
        "counts": dict(sorted(counts.items())),
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
        result["archives"] = create_okf_archives(destination, archive_dir.resolve(), version)
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
    row_id = str(row.get("id") or "unknown")
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    filename = f"{safe_slug(row_id)}.md"
    if kind == "claim":
        return PurePosixPath("claims") / safe_slug(row_id)[0:2] / filename
    if kind == "source_summary":
        return PurePosixPath("source-summaries") / safe_slug(str(payload.get("source_id") or "unknown")) / filename
    if kind in {"answer", "task_card"}:
        return PurePosixPath("answers" if kind == "answer" else "task-cards") / safe_slug(first_concept_id(row) or "unrouted") / filename
    if kind == "lava_context":
        return PurePosixPath("lava-contexts") / safe_slug(str(payload.get("context_family") or "other")) / filename
    if kind in {"recipe", "contribution"}:
        return PurePosixPath("recipes" if kind == "recipe" else "contributions") / safe_slug(str(payload.get("org_id") or "community")) / filename
    if kind == "model_map":
        category = safe_slug(str(payload.get("identity", {}).get("model_category") or "other"))
        return PurePosixPath("models") / category / filename
    if kind == "concept":
        return PurePosixPath("concepts") / f"{safe_slug(first_concept_id(row) or row_id)}.md"
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
    }.get(str(row.get("kind") or ""), f"{row.get('kind')}s")


def row_title(row: dict[str, Any]) -> str:
    return compact_text(str(row.get("title") or row.get("id") or "Untitled"), 140)


def row_description(row: dict[str, Any]) -> str:
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", str(row.get("body") or ""))
    body = re.sub(r"[#*_`>|\[\]]", " ", body)
    return compact_text(body, 240)


def row_timestamp(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    for key in ("updated_at", "retrieved_at", "created_at", "timestamp", "last_built"):
        if payload.get(key):
            return str(payload[key])
    return ""


def row_tags(row: dict[str, Any], known_concepts: set[str]) -> list[str]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    values = [str(row.get("kind") or "")]
    values.extend(concept_ids_for_row(row, known_concepts))
    values.extend(str(value) for value in payload.get("topics") or [])
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
    for concept_id in concept_ids_for_row(row, concept_ids):
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
) -> list[str]:
    title = row_title(row)
    source_path = str(row.get("path") or "")
    if row.get("kind") == "concept":
        concept_id = first_concept_id(row)
        guide_path = REPO_ROOT / "knowledge" / "concepts" / concept_id / "guide.md"
        if guide_path.exists():
            body_text = strip_frontmatter(guide_path.read_text(encoding="utf-8"))
            source_path = guide_path.relative_to(REPO_ROOT).as_posix()
        else:
            body_text = str(row.get("body") or "")
    else:
        body_text = narrative_body(row)
    if row.get("kind") == "concept":
        body_text = rewrite_repo_relative_links(body_text, source_path, commit)
    else:
        body_text = rewrite_source_relative_links(body_text, primary_resource_url(row))
    lines = [f"# {title}", "", body_text.strip() or "No narrative summary is available."]

    if related:
        lines.extend(["", "## Related Knowledge", ""])
        for relation_type, target in related:
            relative = posixpath.relpath(target.as_posix(), current_path.parent.as_posix())
            lines.append(f"- `{relation_type}`: [{target.stem}]({relative})")

    citations = citations_for_row(row)
    if citations:
        lines.extend(["", "## Citations", ""])
        for index, citation in enumerate(citations, 1):
            lines.append(f"[{index}] [{markdown_label(citation['title'])}](<{citation['url']}>)")

    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    if payload:
        lines.extend(
            [
                "",
                "## Structured Record",
                "",
                "~~~~json",
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
                "~~~~",
            ]
        )
    return lines


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

    def add(title: Any, url: Any) -> None:
        clean_url = str(url or "").strip()
        if not clean_url or not re.match(r"^https?://", clean_url):
            return
        candidate = {"title": str(title or clean_url).strip(), "url": clean_url}
        if candidate not in citations:
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
        relative = posixpath.relpath(target.as_posix(), current_path.parent.as_posix())
        lines.append(f"- [{markdown_label(row_title(row))}]({relative})")
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
            lines.extend(["## Documents", ""])
            for path, row_title_value, description in rows:
                relative = posixpath.relpath(path.as_posix(), relative_dir.as_posix())
                suffix = f" - {description}" if description else ""
                lines.append(f"- [{markdown_label(row_title_value)}]({relative}){suffix}")
        (directory / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_root_index(
    destination: Path,
    *,
    generated_at: str,
    version: str,
    commit: str,
    rows: list[dict[str, Any]],
) -> None:
    counts = Counter(row_kind_count_key(row) for row in rows)
    frontmatter = yaml.safe_dump(
        {
            "okf_version": OKF_VERSION,
            "title": "Rock RMS Agent Knowledge Base",
            "description": "Read-only, portable distribution of the canonical public Rock KB.",
            "timestamp": generated_at,
            "distribution_version": version,
            "source_commit": commit,
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
        "This is the complete read-only Open Knowledge Format distribution of the canonical public Rock KB. The source registries, JSONL records, hosted search service, and MCP server remain canonical.",
        "",
        "## Browse",
        "",
        "- [Concept guides](concepts/)",
        "- [Agent answers](answers/)",
        "- [Approved claims](claims/)",
        "- [Community contribution provenance](contributions/)",
        "- [Community recipes](recipes/)",
        "- [Lava contexts](lava-contexts/)",
        "- [Rock models](models/)",
        "- [Source summaries](source-summaries/)",
        "- [Agent task cards](task-cards/)",
        "- [Evidence sources](references/)",
        "",
        "## Counts",
        "",
        *[f"- {key.replace('_', ' ').title()}: {value}" for key, value in sorted(counts.items())],
        "",
        "## Distribution Metadata",
        "",
        f"- OKF version: `{OKF_VERSION}`",
        f"- Distribution version: `{version}`",
        f"- Source commit: `{commit}`",
        f"- Generated at: `{generated_at}`",
        f"- Manifest: [`{MANIFEST_NAME}`]({MANIFEST_NAME})",
        f"- Checksums: [`{CHECKSUMS_NAME}`]({CHECKSUMS_NAME})",
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


def create_okf_archives(destination: Path, archive_dir: Path, version: str) -> list[dict[str, Any]]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"rock-agent-kb-okf-v{version}"
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
                    import io

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
        for target in markdown_targets(text):
            resolved = resolve_markdown_target(relative, target)
            if resolved and not (destination / resolved).exists():
                errors.append(f"{relative} has unresolved link: {target}")
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
        except (OSError, json.JSONDecodeError):
            errors.append(f"{MANIFEST_NAME} is not valid JSON")

    errors.extend(audit_checksums(destination))
    return sorted(set(errors))


def audit_checksums(destination: Path) -> list[str]:
    checksum_path = destination / CHECKSUMS_NAME
    if not checksum_path.exists():
        return [f"missing {CHECKSUMS_NAME}"]
    errors = []
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid checksum row: {line}")
            continue
        target = destination / relative
        if not target.exists():
            errors.append(f"checksum target missing: {relative}")
        elif sha256_file(target) != expected:
            errors.append(f"checksum mismatch: {relative}")
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
