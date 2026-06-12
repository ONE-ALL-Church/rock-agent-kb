from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Optional

from .extract import sha256_text
from .jsonl import read_jsonl
from .paths import REPO_ROOT, REVIEW_DIR

PUBLIC_CONTRIBUTION_REVIEW_STATUSES = {"redaction_reviewed", "approved_for_public_distillation"}
EXAMPLE_BUNDLE_SUFFIX = ".example.jsonl"


def contribution_bundle_paths(root: Optional[Path] = None) -> list[Path]:
    base = root or REPO_ROOT / "contributions"
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.jsonl") if not path.name.endswith(EXAMPLE_BUNDLE_SUFFIX))


def public_contribution_records(concept_id: Optional[str] = None, root: Optional[Path] = None) -> list[dict[str, Any]]:
    records = []
    for path in contribution_bundle_paths(root):
        for row in read_jsonl(path):
            if row.get("review_status") not in PUBLIC_CONTRIBUTION_REVIEW_STATUSES:
                continue
            concept_ids = [str(value) for value in row.get("concept_ids") or []]
            if concept_id and concept_id not in concept_ids:
                continue
            records.append(public_contribution_record(row, path))
    records.sort(key=lambda row: (row.get("source_id") or "", row.get("source_title") or ""))
    return records


def public_contribution_record(row: dict[str, Any], path: Path) -> dict[str, Any]:
    contribution_id = str(row.get("contribution_id") or "")
    urls = [str(value) for value in row.get("source_urls") or [] if value]
    source_record_ids = [str(value) for value in row.get("source_record_ids") or [] if value]
    content_hash = sha256_text(
        "|".join(
            [
                contribution_id,
                str(row.get("title") or ""),
                str(row.get("distilled_summary") or ""),
                ",".join(urls),
                ",".join(source_record_ids),
            ]
        )
    )
    return {
        "id": f"org_contribution:{contribution_id}",
        "source_id": "org_contribution",
        "source_title": row.get("title"),
        "source_url": urls[0] if urls else "",
        "summary": row.get("distilled_summary"),
        "excerpt": row.get("distilled_summary"),
        "topics": row.get("concept_ids") or [],
        "content_hash": content_hash,
        "license_status": "contributor_attested",
        "allowed_extraction_mode": "reviewed_summaries_only",
        "org_id": row.get("org_id"),
        "org_display_name": row.get("org_display_name"),
        "contribution_id": contribution_id,
        "contribution_type": row.get("contribution_type"),
        "confidence": row.get("confidence"),
        "needs_live_verification": row.get("needs_live_verification"),
        "source_urls": urls,
        "source_record_ids": source_record_ids,
        "source_review_origin": row.get("source_review_origin"),
        "bundle_path": relative_path(path),
    }


def private_draft_contribution_records(
    concept_id: Optional[str] = None,
    paths: Optional[Iterable[Path]] = None,
) -> list[dict[str, Any]]:
    records = []
    for path in private_draft_paths(paths):
        for row in read_jsonl(path):
            if row.get("review_status") != "draft_private":
                continue
            concept_ids = [str(value) for value in row.get("concept_ids") or []]
            if concept_id and concept_id not in concept_ids:
                continue
            records.append(private_draft_contribution_record(row, path))
    records.sort(key=lambda row: row.get("source_title") or "")
    return records


def private_draft_paths(paths: Optional[Iterable[Path]] = None) -> list[Path]:
    if paths:
        return sorted(paths)
    base = REVIEW_DIR / "private-distill"
    if not base.exists():
        return []
    return sorted(base.glob("*.jsonl"))


def private_draft_contribution_record(row: dict[str, Any], path: Path) -> dict[str, Any]:
    contribution_id = str(row.get("contribution_id") or "")
    return {
        "id": f"private_org_contribution:{contribution_id}",
        "source_id": "private_org_contribution",
        "source_title": row.get("title"),
        "summary": row.get("distilled_summary"),
        "excerpt": row.get("distilled_summary"),
        "topics": row.get("concept_ids") or [],
        "content_hash": sha256_text(f"{contribution_id}|{row.get('distilled_summary') or ''}"),
        "license_status": "private_restricted",
        "allowed_extraction_mode": "reviewed_summaries_only",
        "org_id": row.get("org_id"),
        "contribution_id": contribution_id,
        "contribution_type": row.get("contribution_type"),
        "confidence": row.get("confidence"),
        "needs_live_verification": True,
        "private_source_hash_count": len(row.get("private_source_hashes") or []),
        "private_path_hash_count": len(row.get("private_path_hashes") or []),
        "bundle_path": relative_path(path),
        "publishability_status": "private_draft_not_public",
    }


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)
