from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

from .claims import approved_claims_path
from .concepts import load_concepts, report_guide_refresh_plan
from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, MEDIA_DIR, NORMALIZED_DIR, REPO_ROOT, REVIEW_DIR
from .publish import public_export_manifest
from .sources import load_sources

SOURCE_SCAN_SCHEMA = "rock-kb-source-scan-v1"
SOURCE_SNAPSHOT_SCHEMA = "rock-kb-source-snapshot-v1"
REBUILD_PLAN_SCHEMA = "rock-kb-rebuild-plan-v1"
REFRESH_DASHBOARD_SCHEMA = "rock-kb-refresh-dashboard-v1"

DEFAULT_SOURCE_SCAN_DIR = REVIEW_DIR / "source-scan"
DEFAULT_REBUILD_PLAN_DIR = REVIEW_DIR / "rebuild-plan"
DEFAULT_REFRESH_DASHBOARD_DIR = REVIEW_DIR / "refresh-dashboard"

PUBLIC_PAYLOAD_FORBIDDEN_TERMS = [
    "transcript_text",
    "raw_transcript",
    "transcript_path",
    "downloaded_media_path",
    "tokenized_media_url",
    "private repo path",
    "private_storage_path",
    "signed url",
    "sig=",
    "x-amz-signature",
    "access_token=",
]
PUBLIC_PAYLOAD_FORBIDDEN_PATTERNS = [
    re.compile(r"\bhttps?://(?:localhost|127\.0\.0\.1|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b", re.IGNORECASE),
    re.compile(r"\bfile://", re.IGNORECASE),
    re.compile(r"/Users/[^\s`]+"),
    re.compile(r"\b[A-Z]:\\\\Users\\\\", re.IGNORECASE),
]


def build_source_scan_report(
    output_dir: Path = DEFAULT_SOURCE_SCAN_DIR,
    baseline_snapshot_path: Optional[Path] = None,
    snapshot_output_path: Optional[Path] = None,
    source_status_path: Optional[Path] = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    current = build_source_snapshot()
    if source_status_path and source_status_path.exists():
        current["source_refresh_status"] = read_json(source_status_path)
    baseline = read_json(baseline_snapshot_path) if baseline_snapshot_path and baseline_snapshot_path.exists() else None
    diff = diff_source_snapshots(baseline, current)
    impacts = map_source_scan_impacts(diff, current, baseline)
    report = {
        "schema": SOURCE_SCAN_SCHEMA,
        "generated_at": generated_at_iso(),
        "baseline_snapshot": relpath(baseline_snapshot_path) if baseline_snapshot_path else "",
        "source_status": relpath(source_status_path) if source_status_path else "",
        "snapshot_path": relpath(snapshot_output_path or (output_dir / "source-snapshot.json")),
        "summary": scan_summary(current, diff, impacts),
        "sources": current["sources"],
        "diff": diff,
        "impacts": impacts,
        "safety": {
            "public_payload_errors": public_payload_safety_errors(
                {
                    "summary": scan_summary(current, diff, impacts),
                    "diff": diff,
                    "impacts": impacts,
                }
            )
        },
    }
    snapshot_path = snapshot_output_path or output_dir / "source-snapshot.json"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(current, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report_bundle(output_dir, "source-scan", report, render_source_scan_markdown(report), source_scan_jsonl_rows(report))
    return report


def build_source_snapshot() -> dict[str, Any]:
    sources = {source.id: source for source in load_sources()}
    records = read_normalized_record_index()
    media_items = read_media_item_index()
    claims = read_claim_snapshot()
    public_files = read_public_export_file_snapshot()
    source_rows = {}
    for source_id, source in sorted(sources.items()):
        source_records = [row for row in records.values() if row.get("source_id") == source_id]
        retrieved = sorted(str(row.get("retrieved_at") or "") for row in source_records if row.get("retrieved_at"))
        urls = sorted({str(row.get("source_url") or "") for row in source_records if row.get("source_url")})
        normalized_path = NORMALIZED_DIR / f"{source_id}.jsonl"
        status = source_artifact_status(source, normalized_path)
        source_rows[source_id] = {
            "source_id": source_id,
            "kind": source.kind,
            "root_url": source.root_url,
            "private_storage": source.private_storage,
            "requires_human_review": source.requires_human_review,
            "public_publish_mode": source.public_publish_mode,
            "normalized_path": relpath(normalized_path),
            "normalized_exists": normalized_path.exists(),
            "record_count": len(source_records),
            "url_count": len(urls),
            "retrieved_at_min": retrieved[0] if retrieved else "",
            "retrieved_at_max": retrieved[-1] if retrieved else "",
            "status": status,
        }
    return {
        "schema": SOURCE_SNAPSHOT_SCHEMA,
        "generated_at": generated_at_iso(),
        "sources": source_rows,
        "source_records": records,
        "media_items": media_items,
        "claims": claims,
        "public_export_files": public_files,
        "model_map": model_map_snapshot(records),
    }


def read_normalized_record_index(normalized_dir: Path = NORMALIZED_DIR) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not normalized_dir.exists():
        return rows
    for path in sorted(normalized_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            record_id = str(row.get("id") or "")
            if not record_id:
                continue
            rows[record_id] = compact_source_record(row)
    return rows


def source_artifact_status(source: Any, normalized_path: Path) -> str:
    if normalized_path.exists():
        return "ok"
    if source.private_storage or source.requires_human_review or source.public_publish_mode in {"private_only", "manual_review_required"}:
        return "manual_review_only"
    return "skipped"


def compact_source_record(row: dict[str, Any]) -> dict[str, Any]:
    source_url = str(row.get("source_url") or "")
    return {
        "id": row.get("id"),
        "source_id": row.get("source_id"),
        "source_kind": row.get("source_kind"),
        "source_title": row.get("source_title"),
        "source_url": source_url,
        "content_hash": source_record_hash(row),
        "retrieved_at": row.get("retrieved_at"),
        "topics": row.get("topics") or [],
        "rock_versions": row.get("rock_versions") or [],
        "release_family": row.get("release_family"),
        "version": row.get("version"),
        "model_name": row.get("model_name"),
        "model_category": row.get("model_category"),
        "summary_hash": sha256_text(str(row.get("summary") or "")) if row.get("summary") else "",
    }


def source_record_hash(row: dict[str, Any]) -> str:
    if row.get("content_hash"):
        return str(row["content_hash"])
    stable = {
        key: row.get(key)
        for key in [
            "id",
            "source_id",
            "source_url",
            "source_title",
            "summary",
            "topics",
            "rock_versions",
            "version",
            "release_family",
            "model_name",
            "model_category",
        ]
        if row.get(key) not in (None, "", [], {})
    }
    return sha256_text(json.dumps(stable, ensure_ascii=False, sort_keys=True))


def read_media_item_index() -> dict[str, dict[str, Any]]:
    path = MEDIA_DIR / "index" / "media-index.jsonl"
    if not path.exists():
        return {}
    rows = {}
    for row in read_jsonl(path):
        media_id = str(row.get("media_id") or row.get("id") or "")
        if not media_id:
            continue
        rows[media_id] = {
            "media_id": media_id,
            "source_id": row.get("source_id"),
            "title": row.get("title") or row.get("source_title"),
            "status": row.get("status") or row.get("transcript_status") or "",
            "transcribed": bool(
                row.get("transcript_path")
                or row.get("transcribed")
                or row.get("has_transcript")
                or row.get("has_private_transcript")
                or row.get("transcript_status") == "transcribed"
                or row.get("transcribed_at")
            ),
            "content_hash": str(row.get("content_hash") or row.get("media_hash") or ""),
        }
    return rows


def read_claim_snapshot() -> dict[str, dict[str, Any]]:
    path = approved_claims_path()
    if not path.exists():
        return {}
    rows = {}
    for row in read_jsonl(path):
        claim_id = str(row.get("claim_id") or "")
        if not claim_id:
            continue
        rows[claim_id] = {
            "claim_id": claim_id,
            "claim_hash": row.get("claim_hash") or sha256_text(str(row.get("claim") or "")),
            "source_record_ids": row.get("source_record_ids") or [],
            "concept_ids": row.get("concept_ids") or [],
            "claim_tier": row.get("claim_tier"),
            "authority_tier": row.get("authority_tier"),
            "needs_live_verification": bool(row.get("needs_live_verification")),
            "answer_candidate": bool(row.get("answer_candidate")),
        }
    return rows


def read_public_export_file_snapshot() -> dict[str, dict[str, Any]]:
    manifest = public_export_manifest()
    return {
        str(row.get("path")): {"path": row.get("path"), "sha256": row.get("sha256"), "bytes": row.get("bytes")}
        for row in manifest.get("files") or []
        if row.get("path")
    }


def model_map_snapshot(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    model_rows = [row for row in records.values() if row.get("source_id") == "rock_model_map"]
    return {
        "record_count": len(model_rows),
        "model_names": sorted({str(row.get("model_name") or row.get("source_title") or "") for row in model_rows if row.get("model_name") or row.get("source_title")}),
        "hash": sha256_text(json.dumps(sorted((row.get("id"), row.get("content_hash")) for row in model_rows), sort_keys=True)),
    }


def diff_source_snapshots(previous: Optional[dict[str, Any]], current: dict[str, Any]) -> dict[str, Any]:
    previous = previous or {}
    old_records = previous.get("source_records") or {}
    new_records = current.get("source_records") or {}
    old_urls = url_index(old_records)
    new_urls = url_index(new_records)
    old_media = previous.get("media_items") or {}
    new_media = current.get("media_items") or {}
    old_claims = previous.get("claims") or {}
    new_claims = current.get("claims") or {}
    changed_record_ids = sorted(
        record_id
        for record_id in set(old_records) & set(new_records)
        if old_records[record_id].get("content_hash") != new_records[record_id].get("content_hash")
    )
    new_record_ids = sorted(set(new_records) - set(old_records)) if old_records else []
    removed_record_ids = sorted(set(old_records) - set(new_records)) if old_records else []
    changed_claim_ids = sorted(
        claim_id
        for claim_id in set(old_claims) & set(new_claims)
        if old_claims[claim_id].get("claim_hash") != new_claims[claim_id].get("claim_hash")
    )
    source_status = current.get("sources") or {}
    refresh_status = current.get("source_refresh_status") or {}
    return {
        "source_record_changes": {
            "new": new_record_ids,
            "removed": removed_record_ids,
            "changed_hash": changed_record_ids,
        },
        "source_hash_changes": source_hash_changes(changed_record_ids, old_records, new_records),
        "url_changes": {
            "new": sorted(set(new_urls) - set(old_urls)) if old_urls else [],
            "removed": sorted(set(old_urls) - set(new_urls)) if old_urls else [],
        },
        "release_note_changes": changed_records_by_kind(new_record_ids + removed_record_ids + changed_record_ids, new_records, old_records, "release"),
        "model_map_changes": changed_records_by_source(new_record_ids + removed_record_ids + changed_record_ids, new_records, old_records, "rock_model_map"),
        "media_changes": {
            "new_media_items": sorted(set(new_media) - set(old_media)) if old_media else [],
            "removed_media_items": sorted(set(old_media) - set(new_media)) if old_media else [],
            "pending_transcription": sorted(media_id for media_id, row in new_media.items() if not row.get("transcribed")),
        },
        "claim_changes": {
            "new": sorted(set(new_claims) - set(old_claims)) if old_claims else [],
            "removed": sorted(set(old_claims) - set(new_claims)) if old_claims else [],
            "changed_hash": changed_claim_ids,
        },
        "source_family_status": {
            "failed": sorted(set(refresh_status.get("failed") or [])),
            "skipped": sorted(
                set(source_id for source_id, row in source_status.items() if row.get("status") == "skipped")
                | set(refresh_status.get("skipped") or [])
            ),
            "manual_review_only": sorted(source_id for source_id, row in source_status.items() if row.get("status") == "manual_review_only"),
        },
    }


def source_hash_changes(record_ids: list[str], old_records: dict[str, Any], new_records: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for record_id in record_ids:
        rows.append(
            {
                "source_record_id": record_id,
                "source_id": str((new_records.get(record_id) or old_records.get(record_id) or {}).get("source_id") or ""),
                "old_hash": str((old_records.get(record_id) or {}).get("content_hash") or ""),
                "new_hash": str((new_records.get(record_id) or {}).get("content_hash") or ""),
            }
        )
    return rows


def changed_records_by_kind(record_ids: list[str], new_records: dict[str, Any], old_records: dict[str, Any], kind_term: str) -> list[str]:
    rows = []
    for record_id in record_ids:
        row = new_records.get(record_id) or old_records.get(record_id) or {}
        haystack = " ".join(str(row.get(key) or "") for key in ["source_id", "source_kind", "release_family"])
        if kind_term in haystack:
            rows.append(record_id)
    return sorted(rows)


def changed_records_by_source(record_ids: list[str], new_records: dict[str, Any], old_records: dict[str, Any], source_id: str) -> list[str]:
    return sorted(
        record_id
        for record_id in record_ids
        if (new_records.get(record_id) or old_records.get(record_id) or {}).get("source_id") == source_id
    )


def url_index(records: dict[str, dict[str, Any]]) -> dict[str, str]:
    return {str(row.get("source_url")): record_id for record_id, row in records.items() if row.get("source_url")}


def map_source_scan_impacts(diff: dict[str, Any], snapshot: dict[str, Any], previous_snapshot: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    changed_ids = set(all_changed_source_record_ids(diff))
    records = snapshot.get("source_records") or {}
    claim_rows = claim_impacts(
        changed_ids,
        snapshot.get("claims") or {},
        (previous_snapshot or {}).get("claims") or {},
        diff.get("claim_changes") or {},
    )
    concept_rows = merge_claim_concept_impacts(concept_impacts(changed_ids, records), claim_rows)
    summary_rows = source_summary_impacts(changed_ids)
    claim_diff_changed = any((diff.get("claim_changes") or {}).get(key) for key in ["new", "removed", "changed_hash"])
    public_files = affected_public_export_files(concept_rows, bool(changed_ids), bool(claim_rows) or claim_diff_changed, bool(summary_rows))
    return {
        "affected_concepts": concept_rows,
        "affected_claims": claim_rows,
        "affected_source_summaries": summary_rows,
        "affected_guides": [row["guide_path"] for row in concept_rows if row.get("guide_path")],
        "affected_public_export_files": public_files,
    }


def all_changed_source_record_ids(diff: dict[str, Any]) -> list[str]:
    changes = diff.get("source_record_changes") or {}
    return sorted(set(changes.get("new") or []) | set(changes.get("removed") or []) | set(changes.get("changed_hash") or []))


def concept_impacts(changed_ids: set[str], records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    dependency_rows = list(read_jsonl(AGENT_DIR / "concept-dependencies.jsonl")) if (AGENT_DIR / "concept-dependencies.jsonl").exists() else []
    dependency_by_concept = {row.get("concept_id"): row for row in dependency_rows}
    rows = []
    for concept in load_concepts():
        dependency = dependency_by_concept.get(concept.id) or {}
        dependency_ids = set(dependency.get("source_record_ids") or [])
        direct = sorted(changed_ids & dependency_ids)
        inferred = sorted(
            record_id
            for record_id in changed_ids
            if record_id not in direct and record_matches_concept(records.get(record_id) or {}, concept)
        )
        if not direct and not inferred:
            continue
        rows.append(
            {
                "concept_id": concept.id,
                "title": concept.title,
                "direct_source_record_ids": direct,
                "inferred_source_record_ids": inferred,
                "guide_path": f"knowledge/concepts/{concept.id}/index.md",
                "long_form_guide_path": f"knowledge/concepts/{concept.id}/guide.md",
                "needs_generated_index_rebuild": bool(direct or inferred),
                "needs_authored_synthesis_review": bool(inferred),
            }
        )
    return rows


def record_matches_concept(record: dict[str, Any], concept: Any) -> bool:
    text = " ".join(
        str(value or "")
        for value in [
            record.get("source_title"),
            record.get("source_url"),
            record.get("source_id"),
            " ".join(record.get("topics") or []),
            " ".join(record.get("rock_versions") or []),
            record.get("documentation_branch"),
            record.get("documentation_path"),
            " ".join(record.get("documentation_branches") or []),
            " ".join(record.get("documentation_path_parts") or []),
        ]
    ).lower()
    needles = {concept.id.replace("-", " "), *[keyword.lower() for keyword in concept.keywords], *[topic.lower() for topic in concept.depends_on_topics]}
    return any(needle and needle in text for needle in needles)


def claim_impacts(
    changed_source_record_ids: set[str],
    current_claims: dict[str, dict[str, Any]],
    previous_claims: Optional[dict[str, dict[str, Any]]] = None,
    claim_changes: Optional[dict[str, list[str]]] = None,
) -> list[dict[str, Any]]:
    rows = []
    previous_claims = previous_claims or {}
    claim_changes = claim_changes or {}
    explicit_claim_ids = set(claim_changes.get("new") or []) | set(claim_changes.get("removed") or []) | set(claim_changes.get("changed_hash") or [])
    for claim in current_claims.values():
        source_ids = set(claim.get("source_record_ids") or [])
        matched = sorted(changed_source_record_ids & source_ids)
        claim_id = str(claim.get("claim_id") or "")
        if not matched and claim_id not in explicit_claim_ids:
            continue
        rows.append(
            {
                "claim_id": claim_id,
                "change_type": claim_change_type(claim_id, claim_changes),
                "claim_tier": claim.get("claim_tier"),
                "authority_tier": claim.get("authority_tier"),
                "concept_ids": claim.get("concept_ids") or [],
                "source_record_ids": matched,
                "needs_live_verification": bool(claim.get("needs_live_verification")),
                "answer_candidate": bool(claim.get("answer_candidate")),
            }
        )
    for claim_id in sorted(set(claim_changes.get("removed") or []) - set(current_claims)):
        claim = previous_claims.get(claim_id) or {"claim_id": claim_id}
        rows.append(
            {
                "claim_id": claim_id,
                "change_type": "removed",
                "claim_tier": claim.get("claim_tier"),
                "authority_tier": claim.get("authority_tier"),
                "concept_ids": claim.get("concept_ids") or [],
                "source_record_ids": claim.get("source_record_ids") or [],
                "needs_live_verification": bool(claim.get("needs_live_verification")),
                "answer_candidate": bool(claim.get("answer_candidate")),
            }
        )
    return sorted(rows, key=lambda row: str(row.get("claim_id") or ""))


def claim_change_type(claim_id: str, claim_changes: dict[str, list[str]]) -> str:
    if claim_id in set(claim_changes.get("new") or []):
        return "new"
    if claim_id in set(claim_changes.get("removed") or []):
        return "removed"
    if claim_id in set(claim_changes.get("changed_hash") or []):
        return "changed_hash"
    return "source_record_changed"


def merge_claim_concept_impacts(concept_rows: list[dict[str, Any]], claim_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(row.get("concept_id")): dict(row) for row in concept_rows}
    concept_titles = {concept.id: concept.title for concept in load_concepts()}
    for claim in claim_rows:
        for concept_id in claim.get("concept_ids") or []:
            row = by_id.setdefault(
                str(concept_id),
                {
                    "concept_id": str(concept_id),
                    "title": concept_titles.get(str(concept_id), str(concept_id)),
                    "direct_source_record_ids": [],
                    "inferred_source_record_ids": [],
                    "claim_change_ids": [],
                    "guide_path": f"knowledge/concepts/{concept_id}/index.md",
                    "long_form_guide_path": f"knowledge/concepts/{concept_id}/guide.md",
                    "needs_generated_index_rebuild": True,
                    "needs_authored_synthesis_review": False,
                },
            )
            row.setdefault("claim_change_ids", []).append(claim.get("claim_id"))
            row["needs_generated_index_rebuild"] = True
    return sorted(by_id.values(), key=lambda row: str(row.get("concept_id") or ""))


def source_summary_impacts(changed_ids: set[str]) -> list[dict[str, Any]]:
    path = AGENT_DIR / "source-summaries.jsonl"
    if not path.exists():
        return []
    rows = []
    for row in read_jsonl(path):
        source_record_id = str(row.get("source_record_id") or "")
        if source_record_id in changed_ids:
            rows.append(
                {
                    "source_summary_id": row.get("id"),
                    "source_record_id": source_record_id,
                    "source_id": row.get("source_id"),
                    "source_url": row.get("source_url"),
                }
            )
    return rows


def affected_public_export_files(concepts: list[dict[str, Any]], source_changed: bool, claims_changed: bool, summaries_changed: bool) -> list[str]:
    files = set()
    for row in concepts:
        for key in ["guide_path", "long_form_guide_path"]:
            path = row.get(key)
            if path:
                files.add(path)
    if source_changed or summaries_changed:
        files.update(
            [
                "agent/source-summaries.jsonl",
                "agent/source-citations.jsonl",
                "agent/rock-kb-manifest.json",
            ]
        )
    if claims_changed:
        files.add("claims/approved-claims.jsonl")
    if files:
        files.add("public-export-manifest.json")
    return sorted(files)


def scan_summary(snapshot: dict[str, Any], diff: dict[str, Any], impacts: dict[str, Any]) -> dict[str, Any]:
    records = snapshot.get("source_records") or {}
    by_source = Counter(row.get("source_id") for row in records.values())
    changes = diff.get("source_record_changes") or {}
    return {
        "registered_sources": len(snapshot.get("sources") or {}),
        "normalized_source_records": len(records),
        "records_by_source": dict(sorted(by_source.items())),
        "changed_source_records": len(changes.get("changed_hash") or []),
        "new_source_records": len(changes.get("new") or []),
        "removed_source_records": len(changes.get("removed") or []),
        "new_urls": len((diff.get("url_changes") or {}).get("new") or []),
        "removed_urls": len((diff.get("url_changes") or {}).get("removed") or []),
        "changed_release_notes": len(diff.get("release_note_changes") or []),
        "changed_model_map_rows": len(diff.get("model_map_changes") or []),
        "new_media_items": len((diff.get("media_changes") or {}).get("new_media_items") or []),
        "pending_media_items": len((diff.get("media_changes") or {}).get("pending_transcription") or []),
        "affected_concepts": len(impacts.get("affected_concepts") or []),
        "affected_claims": len(impacts.get("affected_claims") or []),
        "claims_added": len((diff.get("claim_changes") or {}).get("new") or []),
        "claims_changed": len((diff.get("claim_changes") or {}).get("changed_hash") or []),
        "claims_removed": len((diff.get("claim_changes") or {}).get("removed") or []),
        "affected_source_summaries": len(impacts.get("affected_source_summaries") or []),
        "skipped_source_families": len((diff.get("source_family_status") or {}).get("skipped") or []),
        "failed_source_families": len((diff.get("source_family_status") or {}).get("failed") or []),
        "manual_review_source_families": len((diff.get("source_family_status") or {}).get("manual_review_only") or []),
    }


def build_rebuild_plan(
    scan_report_path: Path,
    output_dir: Path = DEFAULT_REBUILD_PLAN_DIR,
    verification: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scan_report = read_json(scan_report_path)
    guide_plan = report_guide_refresh_plan()
    plan = build_rebuild_plan_from_scan(scan_report, guide_plan, verification=verification)
    write_report_bundle(output_dir, "rebuild-plan", plan, render_rebuild_plan_markdown(plan), rebuild_plan_jsonl_rows(plan))
    (output_dir / "pull-request-body.md").write_text(render_rebuild_pr_body(scan_report, plan), encoding="utf-8")
    return plan


def build_refresh_dashboard(
    scan_report_path: Path = DEFAULT_SOURCE_SCAN_DIR / "source-scan-report.json",
    rebuild_plan_path: Path = DEFAULT_REBUILD_PLAN_DIR / "rebuild-plan-report.json",
    evaluation_report_path: Path = AGENT_DIR / "evaluation-report.json",
    output_dir: Path = DEFAULT_REFRESH_DASHBOARD_DIR,
) -> dict[str, Any]:
    """Build a maintainer-facing refresh dashboard from scan, plan, and answer evaluation state."""
    output_dir.mkdir(parents=True, exist_ok=True)
    scan_report = read_json(scan_report_path) if scan_report_path.exists() else {}
    rebuild_plan = read_json(rebuild_plan_path) if rebuild_plan_path.exists() else {}
    evaluation_report = read_json(evaluation_report_path) if evaluation_report_path.exists() else {}
    dashboard = build_refresh_dashboard_payload(scan_report, rebuild_plan, evaluation_report)
    write_report_bundle(
        output_dir,
        "refresh-dashboard",
        dashboard,
        render_refresh_dashboard_markdown(dashboard),
        refresh_dashboard_jsonl_rows(dashboard),
    )
    return dashboard


def build_refresh_dashboard_payload(
    scan_report: dict[str, Any],
    rebuild_plan: dict[str, Any],
    evaluation_report: dict[str, Any],
) -> dict[str, Any]:
    scan_summary = scan_report.get("summary") or {}
    plan_summary = rebuild_plan.get("summary") or {}
    near_misses = evaluation_report.get("near_misses") or []
    source_changes = sum(
        int(scan_summary.get(key, 0) or 0)
        for key in [
            "changed_source_records",
            "new_source_records",
            "removed_source_records",
            "new_urls",
            "removed_urls",
            "changed_release_notes",
            "changed_model_map_rows",
            "new_media_items",
        ]
    )
    next_actions = []
    if scan_summary.get("failed_source_families", 0):
        next_actions.append("Fix failed source families before publishing refreshed public artifacts.")
    if plan_summary.get("deterministic_step_count", 0):
        next_actions.append("Run or review the deterministic rebuild commands in the rebuild plan.")
    if plan_summary.get("reviewer_step_count", 0):
        next_actions.append("Complete reviewer/AI work before promoting new claims or authored guide prose.")
    if near_misses:
        next_actions.append("Review answer evaluation term misses and patch overrides, claims, or evaluation expectations.")
    if not next_actions and source_changes == 0:
        next_actions.append("No source-driven rebuild work is currently required.")
    return {
        "schema": REFRESH_DASHBOARD_SCHEMA,
        "generated_at": generated_at_iso(),
        "source_scan_path": scan_report.get("report_path") or "",
        "rebuild_plan_path": rebuild_plan.get("report_path") or "",
        "summary": {
            "source_change_count": source_changes,
            "affected_concepts": scan_summary.get("affected_concepts", 0),
            "affected_claims": scan_summary.get("affected_claims", 0),
            "deterministic_step_count": plan_summary.get("deterministic_step_count", 0),
            "reviewer_step_count": plan_summary.get("reviewer_step_count", 0),
            "evaluation_fail_count": evaluation_report.get("fail_count", 0),
            "evaluation_term_miss_count": evaluation_report.get("term_miss_count", len(near_misses)),
        },
        "changed_sources": {
            "changed_source_records": scan_summary.get("changed_source_records", 0),
            "new_source_records": scan_summary.get("new_source_records", 0),
            "removed_source_records": scan_summary.get("removed_source_records", 0),
            "new_urls": scan_summary.get("new_urls", 0),
            "removed_urls": scan_summary.get("removed_urls", 0),
            "changed_release_notes": scan_summary.get("changed_release_notes", 0),
            "changed_model_map_rows": scan_summary.get("changed_model_map_rows", 0),
            "new_media_items": scan_summary.get("new_media_items", 0),
            "failed_source_families": scan_summary.get("failed_source_families", 0),
            "skipped_source_families": scan_summary.get("skipped_source_families", 0),
            "manual_review_source_families": scan_summary.get("manual_review_source_families", 0),
        },
        "affected_concepts": (scan_report.get("impacts") or {}).get("affected_concepts") or [],
        "deterministic_work": rebuild_plan.get("deterministic_work") or [],
        "reviewer_ai_work": rebuild_plan.get("reviewer_ai_work") or [],
        "evaluation_near_misses": near_misses[:50],
        "next_actions": next_actions,
    }


def render_refresh_dashboard_markdown(dashboard: dict[str, Any]) -> str:
    summary = dashboard.get("summary") or {}
    changed = dashboard.get("changed_sources") or {}
    lines = [
        "# Refresh Dashboard",
        "",
        f"- Source change count: `{summary.get('source_change_count', 0)}`",
        f"- Affected concepts: `{summary.get('affected_concepts', 0)}`",
        f"- Affected claims: `{summary.get('affected_claims', 0)}`",
        f"- Deterministic steps: `{summary.get('deterministic_step_count', 0)}`",
        f"- Reviewer/AI steps: `{summary.get('reviewer_step_count', 0)}`",
        f"- Evaluation failures: `{summary.get('evaluation_fail_count', 0)}`",
        f"- Evaluation term misses: `{summary.get('evaluation_term_miss_count', 0)}`",
        "",
        "## Changed Sources",
        "",
    ]
    for key, value in sorted(changed.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- {action}" for action in dashboard.get("next_actions") or [])
    lines.extend(["", "## Deterministic Work", ""])
    for row in dashboard.get("deterministic_work") or []:
        lines.append(f"- `{row.get('id')}`: `{row.get('command')}`")
    if not dashboard.get("deterministic_work"):
        lines.append("- None")
    lines.extend(["", "## Reviewer Or AI Work", ""])
    for row in dashboard.get("reviewer_ai_work") or []:
        suffix = f" (`{row.get('concept_id')}`)" if row.get("concept_id") else ""
        lines.append(f"- `{row.get('id')}`{suffix}: {row.get('description')}")
    if not dashboard.get("reviewer_ai_work"):
        lines.append("- None")
    lines.extend(["", "## Evaluation Term Misses", ""])
    near_misses = dashboard.get("evaluation_near_misses") or []
    if not near_misses:
        lines.append("- None")
    else:
        for row in near_misses:
            missing = ", ".join(str(term) for term in row.get("missing_terms") or [])
            lines.append(f"- `{row.get('id')}` score `{row.get('score')}` missing terms: {missing}")
    lines.append("")
    return "\n".join(lines)


def refresh_dashboard_jsonl_rows(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [{"row_type": "summary", **(dashboard.get("summary") or {})}]
    for row in dashboard.get("affected_concepts") or []:
        rows.append({"row_type": "affected_concept", **row})
    for row in dashboard.get("deterministic_work") or []:
        rows.append({"row_type": "deterministic_work", **row})
    for row in dashboard.get("reviewer_ai_work") or []:
        rows.append({"row_type": "reviewer_ai_work", **row})
    for row in dashboard.get("evaluation_near_misses") or []:
        rows.append({"row_type": "evaluation_near_miss", **row})
    return rows


def build_rebuild_plan_from_scan(
    scan_report: dict[str, Any],
    guide_plan: Optional[dict[str, Any]] = None,
    verification: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    summary = scan_report.get("summary") or {}
    diff = scan_report.get("diff") or {}
    impacts = scan_report.get("impacts") or {}
    guide_plan = guide_plan or {}
    deterministic = deterministic_work(scan_report, guide_plan)
    reviewer = reviewer_work(scan_report, guide_plan)
    return {
        "schema": REBUILD_PLAN_SCHEMA,
        "generated_at": generated_at_iso(),
        "scan_report": scan_report.get("snapshot_path") or "",
        "summary": {
            "deterministic_step_count": len(deterministic),
            "reviewer_step_count": len(reviewer),
            "affected_concepts": summary.get("affected_concepts", 0),
            "affected_claims": summary.get("affected_claims", 0),
            "guides_flagged_for_authored_synthesis": sorted(
                set(guide_plan.get("needs_long_form_guide_refresh") or [])
                | {row.get("concept_id") for row in impacts.get("affected_concepts") or [] if row.get("needs_authored_synthesis_review")}
            ),
            "guides_automatically_refreshed": sorted(set(guide_plan.get("needs_generated_index_rebuild") or [])),
            "media_queued_for_transcription_or_review": len((diff.get("media_changes") or {}).get("new_media_items") or [])
            + len((diff.get("media_changes") or {}).get("pending_transcription") or []),
            "live_verification_needs": sum(1 for row in impacts.get("affected_claims") or [] if row.get("needs_live_verification")),
        },
        "deterministic_work": deterministic,
        "reviewer_ai_work": reviewer,
        "commands": [row["command"] for row in deterministic if row.get("command")],
        "audit_commands": [
            "uv run kb audit public-export",
            "uv run kb audit readiness",
            "uv run --extra dev pytest",
        ],
        "safety": {
            "unreviewed_claim_promotion": "not_allowed",
            "raw_media_publication": "not_allowed",
            "answer_prose_policy": "answer_pack_approved_and_live_verified_only",
            "public_payload_errors": public_payload_safety_errors({"scan": scan_report.get("summary"), "plan": {"summary": {}}}),
        },
        "verification": verification or {},
    }


def deterministic_work(scan_report: dict[str, Any], guide_plan: dict[str, Any]) -> list[dict[str, Any]]:
    summary = scan_report.get("summary") or {}
    claim_changed = any(summary.get(key, 0) for key in ["affected_claims", "claims_added", "claims_changed", "claims_removed"])
    work = []
    if any(summary.get(key, 0) for key in ["changed_source_records", "new_source_records", "removed_source_records"]):
        work.append(step("normalize_sources", "uv run kb sources refresh --skip-indexes", "Refresh normalized public source records after source changes."))
    if claim_changed:
        work.append(step("build_claims", "uv run kb build --stage claims", "Rebuild approved claims from already-approved review data only."))
    if summary.get("changed_model_map_rows", 0):
        work.append(step("build_model_map", "uv run kb modelmap build", "Regenerate model-map artifacts from scraped model-map sources."))
    if summary.get("affected_concepts", 0) or guide_plan.get("needs_generated_index_rebuild"):
        work.append(step("build_concepts", "uv run kb build --stage concepts", "Rebuild generated concept indexes and dependency metadata."))
    if guide_plan.get("needs_generated_index_rebuild") or guide_plan.get("needs_long_form_guide_refresh"):
        work.append(step("refresh_guide_claims", "uv run kb build --stage refresh-claims", "Refresh generated approved-claim and approved-media insert blocks in long-form guides."))
    if any(summary.get(key, 0) for key in ["changed_source_records", "new_source_records", "removed_source_records", "affected_source_summaries", "changed_model_map_rows"]) or claim_changed:
        work.append(step("build_agent_pack", "uv run kb build --stage agent-pack", "Rebuild answer pack, source summaries, citations, model-map/Lava summaries, and agent manifest."))
    if work:
        work.append(step("public_export", "uv run kb publish export", "Rebuild audited public export after generated artifacts change."))
    return dedupe_steps(work)


def reviewer_work(scan_report: dict[str, Any], guide_plan: dict[str, Any]) -> list[dict[str, Any]]:
    summary = scan_report.get("summary") or {}
    impacts = scan_report.get("impacts") or {}
    diff = scan_report.get("diff") or {}
    work = []
    media_count = summary.get("new_media_items", 0) + summary.get("pending_media_items", 0)
    if media_count:
        work.append(review_step("media_review", "Transcribe new media, run Gemma enrichment when useful, create public-safe rewrites, and promote only explicitly reviewed media claims.", media_count))
    live_claims = [row for row in impacts.get("affected_claims") or [] if row.get("needs_live_verification")]
    if live_claims:
        work.append(review_step("live_verification", "Run read-only live verification probes before treating affected operational claims as answer-ready.", len(live_claims)))
    if summary.get("changed_source_records", 0) or summary.get("new_source_records", 0):
        work.append(review_step("source_conflict_review", "Review source conflicts and claim-review candidates; do not promote unreviewed claims automatically.", summary.get("changed_source_records", 0) + summary.get("new_source_records", 0)))
    authored = sorted(
        set(guide_plan.get("needs_long_form_guide_refresh") or [])
        | {row.get("concept_id") for row in impacts.get("affected_concepts") or [] if row.get("needs_authored_synthesis_review")}
    )
    for concept_id in authored:
        work.append(
            review_step(
                "authored_guide_synthesis",
                f"Run `uv run kb concepts synthesize --concept {concept_id} --hydrate-sources --profile comprehensive --model gpt-5.6-sol --reasoning-effort xhigh` locally with Codex/reviewer oversight, then run `uv run kb build --stage guide-intel`.",
                1,
                concept_id=concept_id,
            )
        )
    if (diff.get("source_family_status") or {}).get("failed") or (diff.get("source_family_status") or {}).get("skipped"):
        work.append(review_step("source_family_followup", "Inspect failed or skipped source families before trusting the refresh as complete.", len((diff.get("source_family_status") or {}).get("failed") or []) + len((diff.get("source_family_status") or {}).get("skipped") or [])))
    return work


def step(step_id: str, command: str, reason: str) -> dict[str, Any]:
    return {"id": step_id, "type": "deterministic", "command": command, "reason": reason, "safe_for_ci": True}


def review_step(step_id: str, description: str, count: int, concept_id: str = "") -> dict[str, Any]:
    row = {"id": step_id, "type": "reviewer_or_ai", "description": description, "count": count, "safe_for_ci": False}
    if concept_id:
        row["concept_id"] = concept_id
    return row


def dedupe_steps(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    deduped = []
    for row in rows:
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        deduped.append(row)
    return deduped


def render_source_scan_markdown(report: dict[str, Any]) -> str:
    summary = report.get("summary") or {}
    diff = report.get("diff") or {}
    impacts = report.get("impacts") or {}
    lines = [
        "# Source Scan Summary",
        "",
        f"- Registered sources: `{summary.get('registered_sources', 0)}`",
        f"- Normalized source records: `{summary.get('normalized_source_records', 0)}`",
        f"- Changed source records: `{summary.get('changed_source_records', 0)}`",
        f"- New / removed source records: `{summary.get('new_source_records', 0)}` / `{summary.get('removed_source_records', 0)}`",
        f"- New / removed URLs: `{summary.get('new_urls', 0)}` / `{summary.get('removed_urls', 0)}`",
        f"- Changed release notes: `{summary.get('changed_release_notes', 0)}`",
        f"- Changed model-map rows: `{summary.get('changed_model_map_rows', 0)}`",
        f"- New media items: `{summary.get('new_media_items', 0)}`",
        f"- Pending media items: `{summary.get('pending_media_items', 0)}`",
        f"- Affected concepts: `{summary.get('affected_concepts', 0)}`",
        f"- Affected claims: `{summary.get('affected_claims', 0)}`",
        f"- Claims added / changed / removed: `{summary.get('claims_added', 0)}` / `{summary.get('claims_changed', 0)}` / `{summary.get('claims_removed', 0)}`",
        f"- Skipped source families: `{summary.get('skipped_source_families', 0)}`",
        f"- Failed source families: `{summary.get('failed_source_families', 0)}`",
        f"- Manual-review/private source families: `{summary.get('manual_review_source_families', 0)}`",
        "",
        "## Affected Concepts",
        "",
    ]
    for row in impacts.get("affected_concepts") or []:
        lines.append(f"- `{row.get('concept_id')}`: {len(row.get('direct_source_record_ids') or [])} direct, {len(row.get('inferred_source_record_ids') or [])} inferred")
    if not impacts.get("affected_concepts"):
        lines.append("- None")
    lines.extend(["", "## Source Families Needing Follow-Up", ""])
    status = diff.get("source_family_status") or {}
    for label in ["failed", "skipped"]:
        values = status.get(label) or []
        lines.append(f"- {label}: {', '.join(values) if values else 'none'}")
    lines.append("")
    return "\n".join(lines)


def render_rebuild_plan_markdown(plan: dict[str, Any]) -> str:
    summary = plan.get("summary") or {}
    lines = [
        "# Rebuild Plan",
        "",
        f"- Deterministic steps: `{summary.get('deterministic_step_count', 0)}`",
        f"- Reviewer/AI steps: `{summary.get('reviewer_step_count', 0)}`",
        f"- Affected concepts: `{summary.get('affected_concepts', 0)}`",
        f"- Affected claims: `{summary.get('affected_claims', 0)}`",
        f"- Media queued for transcription/review: `{summary.get('media_queued_for_transcription_or_review', 0)}`",
        f"- Live-verification needs: `{summary.get('live_verification_needs', 0)}`",
        "",
        "## Deterministic Work",
        "",
    ]
    for row in plan.get("deterministic_work") or []:
        lines.append(f"- `{row.get('id')}`: `{row.get('command')}`")
    lines.extend(["", "## Reviewer Or AI Work", ""])
    for row in plan.get("reviewer_ai_work") or []:
        suffix = f" (`{row.get('concept_id')}`)" if row.get("concept_id") else ""
        lines.append(f"- `{row.get('id')}`{suffix}: {row.get('description')}")
    if not plan.get("reviewer_ai_work"):
        lines.append("- None")
    lines.extend(["", "## Audits", ""])
    lines.extend(f"- `{command}`" for command in plan.get("audit_commands") or [])
    lines.append("")
    return "\n".join(lines)


def render_rebuild_pr_body(scan_report: dict[str, Any], plan: dict[str, Any]) -> str:
    scan = scan_report.get("summary") or {}
    plan_summary = plan.get("summary") or {}
    lines = [
        "## Source Scan Summary",
        "",
        f"- Changed source records: `{scan.get('changed_source_records', 0)}`",
        f"- New / removed source records: `{scan.get('new_source_records', 0)}` / `{scan.get('removed_source_records', 0)}`",
        f"- New / removed URLs: `{scan.get('new_urls', 0)}` / `{scan.get('removed_urls', 0)}`",
        f"- Changed release notes: `{scan.get('changed_release_notes', 0)}`",
        f"- Changed model-map rows: `{scan.get('changed_model_map_rows', 0)}`",
        f"- New media items: `{scan.get('new_media_items', 0)}`",
        f"- Affected concepts: `{scan.get('affected_concepts', 0)}`",
        f"- Affected claims: `{scan.get('affected_claims', 0)}`",
        f"- Affected source summaries: `{scan.get('affected_source_summaries', 0)}`",
        f"- Claims added / changed / removed: `{scan.get('claims_added', 0)}` / `{scan.get('claims_changed', 0)}` / `{scan.get('claims_removed', 0)}`",
        f"- Failed / skipped / manual-review source families: `{scan.get('failed_source_families', 0)}` / `{scan.get('skipped_source_families', 0)}` / `{scan.get('manual_review_source_families', 0)}`",
        "",
        "## Rebuild Plan Summary",
        "",
        f"- Deterministic steps: `{plan_summary.get('deterministic_step_count', 0)}`",
        f"- Reviewer/AI steps: `{plan_summary.get('reviewer_step_count', 0)}`",
        f"- Guides automatically refreshed: {format_inline_list(plan_summary.get('guides_automatically_refreshed') or [])}",
        f"- Guides flagged for authored synthesis: {format_inline_list(plan_summary.get('guides_flagged_for_authored_synthesis') or [])}",
        f"- Media queued for transcription/review: `{plan_summary.get('media_queued_for_transcription_or_review', 0)}`",
        f"- Live-verification needs: `{plan_summary.get('live_verification_needs', 0)}`",
        "",
        "## Commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in plan.get("commands") or [])
    lines.extend(["", "## Audits", ""])
    lines.extend(f"- `{command}`" for command in plan.get("audit_commands") or [])
    verification = plan.get("verification") or {}
    if verification:
        lines.extend(["", "## Audit/Test Results", ""])
        for key, value in sorted(verification.items()):
            lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- Unreviewed claims were not promoted automatically.",
            "- Raw media transcripts, downloaded media, tokenized media URLs, private paths, secrets, and copied protected source text are excluded from public artifacts.",
            "- Public answer prose remains limited to approved answer-pack and live-verified claim paths.",
            "",
        ]
    )
    body = "\n".join(lines)
    errors = public_payload_safety_errors(body)
    if errors:
        raise ValueError("PR body failed safety check: " + "; ".join(errors))
    return body


def format_inline_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def source_scan_jsonl_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for source_id, row in (report.get("sources") or {}).items():
        rows.append({"row_type": "source", "source_id": source_id, **row})
    for row in report.get("impacts", {}).get("affected_concepts") or []:
        rows.append({"row_type": "affected_concept", **row})
    for row in report.get("impacts", {}).get("affected_claims") or []:
        rows.append({"row_type": "affected_claim", **row})
    return rows


def rebuild_plan_jsonl_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"row_type": "deterministic_work", **row}
        for row in plan.get("deterministic_work") or []
    ] + [
        {"row_type": "reviewer_ai_work", **row}
        for row in plan.get("reviewer_ai_work") or []
    ]


def write_report_bundle(output_dir: Path, stem: str, payload: dict[str, Any], markdown: str, rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{stem}-report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / f"{stem}-summary.md").write_text(markdown, encoding="utf-8")
    write_jsonl(output_dir / f"{stem}-rows.jsonl", rows)


def public_payload_safety_errors(payload: Any) -> list[str]:
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, sort_keys=True)
    lowered = text.lower()
    errors = [f"payload contains forbidden term: {term}" for term in PUBLIC_PAYLOAD_FORBIDDEN_TERMS if term in lowered]
    errors.extend(f"payload contains forbidden pattern: {pattern.pattern}" for pattern in PUBLIC_PAYLOAD_FORBIDDEN_PATTERNS if pattern.search(text))
    return errors


def read_json(path: Optional[Path]) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def relpath(path: Optional[Path]) -> str:
    if not path:
        return ""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)
