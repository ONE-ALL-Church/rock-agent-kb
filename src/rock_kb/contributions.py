from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Optional

from pydantic import ValidationError

from .concepts import load_concepts
from .extract import grep_sensitive_values, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT, REVIEW_DIR
from .private_dependencies import PRIVATE_PROMOTION_DEPENDENCY_SCHEMA, private_promotion_dependency_path
from .private_leakage import find_leaks
from .private_scan import private_risk_flags
from .schemas import ContributionRow
from .schemas.contribution import ALLOWED_TRANSITIONS, PROMOTABLE_STATUSES

CONTRIBUTION_SCHEMA = "rock-kb-org-contribution-v1"
ALLOWED_CONTRIBUTION_TYPES = {
    "task_card",
    "troubleshooting_pattern",
    "release_caveat",
    "entity_note",
    "guide_section",
    "source_link",
    "open_question",
}
ALLOWED_REVIEW_STATUSES = {
    "draft_private",
    "redaction_reviewed",
    "approved_for_public_distillation",
    "rejected_private",
    "needs_followup",
}
PUBLIC_REVIEW_STATUSES = {"redaction_reviewed", "approved_for_public_distillation"}
ALLOWED_CONFIDENCE = {"low", "medium", "high", "needs_review"}
EXAMPLE_BUNDLE_SUFFIX = ".example.jsonl"
REQUIRED_CONTRIBUTION_FIELDS = {
    "schema",
    "contribution_id",
    "org_id",
    "concept_ids",
    "contribution_type",
    "title",
    "distilled_summary",
    "source_urls",
    "source_record_ids",
    "redaction_attestation",
    "review_status",
    "license_attestation",
    "confidence",
    "needs_live_verification",
}
PROHIBITED_PUBLIC_FIELDS = {"private_source_paths", "raw_text", "content", "full_text", "transcript", "private_path"}
DEFAULT_PROMOTION_REVIEW_STATUS = "redaction_reviewed"
PUBLIC_COMMUNITY_CONTRIBUTION_DIR = "community-contributions"


def validate_contribution_paths(paths: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_contribution_file(path))
    return errors


def contribution_check_report(path: Optional[Path] = None) -> dict[str, Any]:
    target = path or REPO_ROOT / "contributions"
    next_validation_target = target
    if target.is_file() and target.name.endswith(EXAMPLE_BUNDLE_SUFFIX):
        paths: list[Path] = []
        example_paths = [target]
        next_validation_target = target.parent
    elif target.is_file():
        paths = [target]
        example_paths = []
    else:
        paths = contribution_paths(target)
        example_paths = contribution_example_paths(target)
    errors = validate_contribution_paths(paths)
    rows = list(iter_contribution_rows(paths))
    return {
        "schema": "rock-kb-contribution-check-v1",
        "status": "fail" if errors else "ok",
        "path": relative_path(target),
        "bundle_files": [relative_path(path) for path in paths],
        "example_files": [relative_path(path) for path in example_paths],
        "bundle_count": len(paths),
        "example_count": len(example_paths),
        "row_count": len(rows),
        "contribution_types": counted_values(row.get("contribution_type") for _, row in rows),
        "concept_ids": counted_values(concept for _, row in rows for concept in row.get("concept_ids") or []),
        "review_statuses": counted_values(row.get("review_status") for _, row in rows),
        "org_ids": counted_values(row.get("org_id") for _, row in rows),
        "errors": errors,
        "next_commands": [
            f"uv run kb contributions validate --path {relative_path(next_validation_target)}",
            "uv run kb audit public-export",
        ],
    }


def import_public_contribution_bundles(
    public_repo: Path,
    output_root: Optional[Path] = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Import reviewed public-community contribution bundles into the build repo."""
    intake_root = public_repo / PUBLIC_COMMUNITY_CONTRIBUTION_DIR
    output_root = output_root or REPO_ROOT / "contributions"
    source_paths = contribution_paths(intake_root)
    errors = validate_contribution_paths(source_paths)
    copied: list[dict[str, str]] = []
    if not intake_root.exists():
        errors.append(f"{relative_path(intake_root)} does not exist")
    for source_path in source_paths:
        try:
            rel = source_path.relative_to(intake_root)
        except ValueError:
            errors.append(f"{source_path} is not under {intake_root}")
            continue
        if len(rel.parts) < 2:
            errors.append(f"{source_path} must be under {PUBLIC_COMMUNITY_CONTRIBUTION_DIR}/<org-id>/")
            continue
        org_id = rel.parts[0]
        if not safe_org_id(org_id):
            errors.append(f"{source_path} has invalid org directory {org_id}")
            continue
        for row in read_jsonl(source_path):
            if row.get("org_id") != org_id:
                errors.append(f"{source_path} row {row.get('contribution_id')} org_id does not match directory {org_id}")
        target = output_root / rel
        if target.exists() and not overwrite:
            errors.append(f"{relative_path(target)} already exists; use --overwrite to replace it")
            continue
        copied.append({"source": str(source_path), "destination": str(target)})
    if not dry_run and not errors:
        for row in copied:
            source_path = Path(row["source"])
            target = Path(row["destination"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
        errors.extend(validate_contribution_paths([Path(row["destination"]) for row in copied]))
    return {
        "schema": "rock-kb-public-contribution-import-v1",
        "status": "fail" if errors else "ok",
        "public_repo": str(public_repo),
        "intake_root": str(intake_root),
        "output_root": str(output_root),
        "dry_run": dry_run,
        "overwrite": overwrite,
        "source_count": len(source_paths),
        "imported_count": len(copied) if not errors and not dry_run else 0,
        "planned_import_count": len(copied) if not errors else 0,
        "imports": copied if not errors else [],
        "errors": errors,
        "next_commands": [
            "uv run kb contributions check --path contributions",
            "uv run kb build --stage concepts",
            "uv run kb build --stage refresh-claims",
            "uv run kb build --stage agent-pack",
            "uv run kb publish export",
            "uv run kb audit public-export",
        ],
    }


def validate_contribution_file(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path} does not exist"]
    if path.suffix != ".jsonl":
        return [f"{relative_path(path)} must be a JSONL file"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative_path(path)}:{line_number} invalid JSONL: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{relative_path(path)}:{line_number} row must be an object")
            continue
        errors.extend(validate_contribution_row(row, f"{relative_path(path)}:{line_number}", public=True))
    return errors


def validate_contribution_row(row: dict[str, Any], label: str = "row", public: bool = True) -> list[str]:
    errors: list[str] = []
    try:
        ContributionRow.model_validate(row)
    except ValidationError as exc:
        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc") or [])
            errors.append(f"{label} schema error at {location or '$'}: {error.get('msg')}")
    missing = sorted(field for field in REQUIRED_CONTRIBUTION_FIELDS if field not in row or row.get(field) is None)
    missing.extend(field for field in ["concept_ids", "title", "distilled_summary"] if empty(row.get(field)) and field not in missing)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if row.get("schema") != CONTRIBUTION_SCHEMA:
        errors.append(f"{label} schema must be {CONTRIBUTION_SCHEMA}")
    if row.get("contribution_type") not in ALLOWED_CONTRIBUTION_TYPES:
        errors.append(f"{label} invalid contribution_type")
    if row.get("review_status") not in ALLOWED_REVIEW_STATUSES:
        errors.append(f"{label} invalid review_status")
    if public and row.get("review_status") not in PUBLIC_REVIEW_STATUSES:
        errors.append(f"{label} public contribution must be redaction reviewed or approved")
    if row.get("confidence") not in ALLOWED_CONFIDENCE:
        errors.append(f"{label} invalid confidence")
    if not isinstance(row.get("needs_live_verification"), bool):
        errors.append(f"{label} needs_live_verification must be true or false")
    errors.extend(validate_concept_ids(row, label))
    if not row.get("source_urls") and not row.get("source_record_ids"):
        errors.append(f"{label} must include source_urls or source_record_ids")
    if public:
        errors.extend(f"{label} {message}" for message in find_leaks(row))
        for field in prohibited_field_paths(row):
            errors.append(f"{label} contains prohibited public field: {field}")
        for finding in grep_sensitive_values(json.dumps(row, ensure_ascii=False).splitlines()):
            errors.append(f"{label} contains sensitive-looking value: {finding[:120]}")
        if private_risk_flags(json.dumps(public_marker_scan_payload(row), ensure_ascii=False)):
            errors.append(f"{label} contains private instance markers")
        if row.get("private_source_hashes"):
            errors.append(f"{label} private_source_hashes are private review metadata, not public bundle fields")
    if not truthy_attestation(row.get("redaction_attestation")):
        errors.append(f"{label} redaction_attestation must be true or an affirmative string")
    if not truthy_attestation(row.get("license_attestation")):
        errors.append(f"{label} license_attestation must be true or an affirmative string")
    return errors


def validate_concept_ids(row: dict[str, Any], label: str) -> list[str]:
    values = row.get("concept_ids")
    if not isinstance(values, list) or not values:
        return [f"{label} concept_ids must be a non-empty list"]
    known = {concept.id for concept in load_concepts()}
    unknown = sorted(str(value) for value in values if str(value) not in known)
    if unknown:
        return [f"{label} unknown concept_ids: {', '.join(unknown)}"]
    return []


def prohibited_field_paths(value: Any, prefix: str = "$") -> list[str]:
    paths = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{prefix}.{key}"
            if key in PROHIBITED_PUBLIC_FIELDS:
                paths.append(key_path)
            paths.extend(prohibited_field_paths(nested, key_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            paths.extend(prohibited_field_paths(nested, f"{prefix}[{index}]"))
    return paths


def public_marker_scan_payload(row: dict[str, Any]) -> dict[str, Any]:
    allowed_identity_fields = {
        "contribution_id",
        "org_id",
        "org_display_name",
        "source_review_origin",
        "created_at",
        "publishability_status",
    }
    return {key: value for key, value in row.items() if key not in allowed_identity_fields}


def distill_private_scan(
    scan_path: Path,
    source_id: str,
    concept_id: str,
    org_id: str,
    output_path: Optional[Path] = None,
    dependency_output_path: Optional[Path] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    rows = [
        row
        for row in read_jsonl(scan_path)
        if row.get("source_id") == source_id
        and concept_id in (row.get("candidate_concepts") or [])
        and row.get("review_classification") == "generalizable_pattern"
        and row.get("public_contribution_mode") == "distill_then_review"
        and not row.get("risk_flags")
        and not row.get("sensitive_findings")
        and row.get("summary_candidate")
    ]
    rows = rows[: limit or None]
    contributions = [private_scan_row_to_contribution(row, concept_id, org_id) for row in rows]
    output = output_path or private_distill_path(source_id, concept_id)
    write_jsonl(output, contributions)
    dependency_output = dependency_output_path or private_dependency_path(source_id, concept_id)
    write_jsonl(dependency_output, private_dependency_rows(contributions))
    return contributions


def private_scan_row_to_contribution(row: dict[str, Any], concept_id: str, org_id: str) -> dict[str, Any]:
    summary = sanitize_distilled_summary(str(row.get("summary_candidate") or ""))
    title = title_from_scan_row(row)
    contribution_id = "private-distill:" + sha256_text(f"{row.get('source_id')}:{row.get('content_hash')}:{concept_id}")[:16]
    return {
        "schema": CONTRIBUTION_SCHEMA,
        "contribution_id": contribution_id,
        "org_id": org_id,
        "org_display_name": "private",
        "source_id": row.get("source_id"),
        "concept_ids": [concept_id],
        "contribution_type": "guide_section",
        "title": title,
        "distilled_summary": summary,
        "source_urls": [],
        "source_record_ids": [],
        "private_source_hashes": [row.get("content_hash")],
        "private_path_hashes": [row.get("private_path_hash")],
        "redaction_attestation": False,
        "review_status": "draft_private",
        "license_attestation": False,
        "confidence": "needs_review",
        "needs_live_verification": True,
        "created_at": now_iso(),
        "publishability_status": "private_draft_not_public",
    }


def title_from_scan_row(row: dict[str, Any]) -> str:
    path = str(row.get("path") or "Private source")
    stem = Path(path).stem.replace("-", " ").replace("_", " ").strip() or "Private source"
    title = re.sub(r"\s+", " ", stem).title()
    return f"Draft Private Pattern: {title}"


def sanitize_distilled_summary(text: str, max_chars: int = 700) -> str:
    cleaned = " ".join(text.split())
    cleaned = re.sub(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[redacted-email]", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:Page|Block|Group|Workflow Type|DataView|AttributeValue|DefinedValue|PersonAlias|Campus)Id\s*[=:]\s*\d+\b", "[redacted-rock-id]", cleaned, flags=re.IGNORECASE)
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rsplit(" ", 1)[0] + "..."


def private_distill_path(source_id: str, concept_id: str) -> Path:
    return REVIEW_DIR / "private-distill" / f"{source_id}-{concept_id}.jsonl"


def private_dependency_path(source_id: str, concept_id: str) -> Path:
    return REVIEW_DIR / "private-dependencies" / f"{source_id}-{concept_id}.jsonl"


def private_dependency_rows(contributions: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for contribution in contributions:
        rows.append(
            {
                "schema": "rock-kb-private-dependency-v1",
                "contribution_id": contribution.get("contribution_id"),
                "source_id": contribution.get("source_id"),
                "org_id": contribution.get("org_id"),
                "concept_ids": contribution.get("concept_ids") or [],
                "private_source_hashes": contribution.get("private_source_hashes") or [],
                "private_path_hashes": contribution.get("private_path_hashes") or [],
                "created_at": now_iso(),
                "public_artifact_path": None,
                "publishability_status": "private_dependency_only",
            }
        )
    return rows


def report_private_staleness(scan_path: Path, dependency_path: Path) -> list[dict[str, Any]]:
    scan_hashes = {row.get("content_hash") for row in read_jsonl(scan_path) if row.get("content_hash")}
    rows = []
    for dependency in read_jsonl(dependency_path):
        hashes = [value for value in dependency.get("private_source_hashes") or [] if value]
        missing = sorted(value for value in hashes if value not in scan_hashes)
        rows.append(
            {
                "contribution_id": dependency.get("contribution_id"),
                "source_id": dependency.get("source_id"),
                "org_id": dependency.get("org_id"),
                "concept_ids": dependency.get("concept_ids") or [],
                "needs_rebuild": bool(missing),
                "reason": "private_source_hash_missing_or_changed" if missing else "current",
                "private_source_hash_count": len(hashes),
                "missing_private_source_hashes": missing,
                "public_artifact_path": dependency.get("public_artifact_path"),
            }
        )
    return rows


def private_review_report(
    scan_path: Path,
    source_id: Optional[str] = None,
    org_id: Optional[str] = None,
) -> dict[str, Any]:
    records = [
        row
        for row in read_jsonl(scan_path)
        if (source_id is None or row.get("source_id") == source_id) and (org_id is None or row.get("org_id") == org_id)
    ]
    classifications: dict[str, int] = {}
    publishability: dict[str, int] = {}
    contribution_modes: dict[str, int] = {}
    concepts: dict[str, int] = {}
    risk_flags: dict[str, int] = {}
    source_ids: dict[str, int] = {}
    org_ids: dict[str, int] = {}
    eligible = 0
    blocked = 0
    needs_review = 0
    redaction_required = 0
    for row in records:
        increment(classifications, str(row.get("review_classification") or "unknown"))
        increment(publishability, str(row.get("publishability_status") or "unknown"))
        increment(contribution_modes, str(row.get("public_contribution_mode") or "unknown"))
        increment(source_ids, str(row.get("source_id") or "unknown"))
        increment(org_ids, str(row.get("org_id") or "unknown"))
        for concept_id in row.get("candidate_concepts") or []:
            increment(concepts, str(concept_id))
        for flag in row.get("risk_flags") or []:
            increment(risk_flags, str(flag))
        sensitive_findings = row.get("sensitive_findings") or []
        if str(row.get("publishability_status") or "").startswith("blocked") or sensitive_findings:
            blocked += 1
        if row.get("redaction_required"):
            redaction_required += 1
        if row.get("review_classification") == "needs_human_review":
            needs_review += 1
        if (
            row.get("review_classification") == "generalizable_pattern"
            and row.get("public_contribution_mode") == "distill_then_review"
            and not row.get("risk_flags")
            and not sensitive_findings
            and row.get("summary_candidate")
        ):
            eligible += 1
    return {
        "schema": "rock-kb-private-review-report-v1",
        "scan_path": relative_path(scan_path),
        "source_filter": source_id,
        "org_filter": org_id,
        "records": len(records),
        "eligible_for_private_distill": eligible,
        "blocked_or_sensitive": blocked,
        "needs_human_review": needs_review,
        "redaction_required": redaction_required,
        "source_ids": sorted_counts(source_ids),
        "org_ids": sorted_counts(org_ids),
        "review_classifications": sorted_counts(classifications),
        "publishability_statuses": sorted_counts(publishability),
        "public_contribution_modes": sorted_counts(contribution_modes),
        "candidate_concepts": sorted_counts(concepts),
        "risk_flags": sorted_counts(risk_flags),
    }


def promote_private_contributions(
    draft_path: Path,
    org_id: str,
    output_path: Optional[Path] = None,
    rewrite_path: Optional[Path] = None,
    reviewed: bool = False,
    redaction_attestation: bool = False,
    license_attestation: bool = False,
    contribution_ids: Optional[list[str]] = None,
    concept_id: Optional[str] = None,
    limit: Optional[int] = None,
    append: bool = False,
    review_status: str = DEFAULT_PROMOTION_REVIEW_STATUS,
) -> dict[str, Any]:
    if review_status not in ALLOWED_REVIEW_STATUSES:
        raise ValueError(f"review_status must be one of: {', '.join(sorted(ALLOWED_REVIEW_STATUSES))}")
    drafts = select_private_drafts(draft_path, contribution_ids=contribution_ids, concept_id=concept_id, limit=limit)
    rewrites = load_rewrite_rows(rewrite_path)
    if reviewed and not rewrite_path:
        raise ValueError("reviewed promotion requires --rewrite-file")
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for draft in drafts:
        contribution_id = str(draft.get("contribution_id") or "")
        if reviewed:
            errors.extend(
                validate_public_promotion_gate(
                    draft,
                    target_review_status=review_status,
                    reviewed=reviewed,
                    redaction_attestation=redaction_attestation,
                    license_attestation=license_attestation,
                )
            )
        rewrite = rewrites.get(contribution_id)
        if reviewed and not rewrite:
            errors.append(f"{contribution_id} missing reviewer rewrite")
            continue
        row = reviewed_public_row_from_draft(
            draft,
            org_id=org_id,
            rewrite=rewrite,
            reviewed=reviewed,
            redaction_attestation=redaction_attestation,
            license_attestation=license_attestation,
            review_status=review_status,
        )
        if reviewed:
            errors.extend(validate_reviewer_rewrite(draft, row, contribution_id))
            errors.extend(validate_contribution_row(row, contribution_id, public=True))
        rows.append(row)
    if errors:
        raise ValueError("\n".join(errors))
    output = output_path or default_promotion_path(org_id, reviewed=reviewed)
    existing = list(read_jsonl(output)) if append else []
    duplicate_errors = duplicate_public_rows(existing + rows)
    if duplicate_errors:
        raise ValueError("\n".join(duplicate_errors))
    write_jsonl(output, existing + rows)
    dependency_output = None
    if reviewed:
        dependency_output = write_private_promotion_dependencies(org_id, output, drafts, rows, append=append)
    return {
        "schema": "rock-kb-contribution-promotion-result-v1",
        "status": "public_bundle" if reviewed else "private_staging",
        "reviewed": reviewed,
        "records": len(rows),
        "output": str(output),
        "private_dependency_output": str(dependency_output) if dependency_output else None,
        "append": append,
        "requires_human_rewrite": not reviewed,
        "validated_public": reviewed,
    }


def validate_public_promotion_gate(
    draft: dict[str, Any],
    target_review_status: str,
    reviewed: bool,
    redaction_attestation: bool,
    license_attestation: bool,
) -> list[str]:
    contribution_id = str(draft.get("contribution_id") or "<unknown>")
    source_status = str(draft.get("review_status") or "")
    errors: list[str] = []
    if source_status not in ALLOWED_TRANSITIONS:
        errors.append(f"{contribution_id} promotion gate failed from status {source_status or '<missing>'}: invalid source review_status")
        return errors
    if target_review_status not in ALLOWED_TRANSITIONS[source_status]:
        errors.append(f"{contribution_id} illegal review_status transition: {source_status} -> {target_review_status}")
    if target_review_status not in PROMOTABLE_STATUSES:
        errors.append(f"{contribution_id} promotion gate failed from status {source_status}: target review_status {target_review_status} is not promotable")
    missing = []
    if not reviewed:
        missing.append("reviewed")
    if not redaction_attestation:
        missing.append("redaction_attestation")
    if not license_attestation:
        missing.append("license_attestation")
    if missing:
        errors.append(f"{contribution_id} promotion gate failed from status {source_status}: missing {', '.join(missing)}")
    return errors


def select_private_drafts(
    draft_path: Path,
    contribution_ids: Optional[list[str]] = None,
    concept_id: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    wanted = set(contribution_ids or [])
    rows = []
    for row in read_jsonl(draft_path):
        if wanted and row.get("contribution_id") not in wanted:
            continue
        if concept_id and concept_id not in (row.get("concept_ids") or []):
            continue
        if row.get("review_status") != "draft_private":
            continue
        rows.append(row)
    return rows[: limit or None]


def load_rewrite_rows(path: Optional[Path]) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(path):
        contribution_id = str(row.get("contribution_id") or "")
        if contribution_id:
            rows[contribution_id] = row
    return rows


def reviewed_public_row_from_draft(
    draft: dict[str, Any],
    org_id: str,
    rewrite: Optional[dict[str, Any]],
    reviewed: bool,
    redaction_attestation: bool,
    license_attestation: bool,
    review_status: str,
) -> dict[str, Any]:
    rewrite = rewrite or {}
    source_private_id = str(draft.get("contribution_id") or "")
    public_id = str(rewrite.get("public_contribution_id") or rewrite.get("new_contribution_id") or public_contribution_id(org_id, source_private_id))
    public_row = {
        "schema": CONTRIBUTION_SCHEMA,
        "contribution_id": public_id,
        "org_id": org_id,
        "org_display_name": rewrite.get("org_display_name") or public_org_display_name(draft, org_id),
        "concept_ids": rewrite.get("concept_ids") or draft.get("concept_ids") or [],
        "contribution_type": rewrite.get("contribution_type") or draft.get("contribution_type") or "guide_section",
        "title": rewrite.get("title") or f"Rewrite Needed: {draft.get('title') or 'Private Pattern'}",
        "distilled_summary": rewrite.get("distilled_summary")
        or "Reviewer must replace this private staging row with newly written public-safe guidance before publication.",
        "source_urls": rewrite.get("source_urls") or [],
        "source_record_ids": rewrite.get("source_record_ids") or [],
        "redaction_attestation": bool(redaction_attestation) if reviewed else False,
        "review_status": review_status if reviewed else "needs_followup",
        "license_attestation": bool(license_attestation) if reviewed else False,
        "confidence": rewrite.get("confidence") or ("medium" if reviewed else "needs_review"),
        "needs_live_verification": bool(rewrite.get("needs_live_verification", True)),
        "created_at": now_iso(),
        "publishability_status": "public_reviewed" if reviewed else "private_staging_needs_rewrite",
    }
    if reviewed:
        public_row["source_review_origin"] = "private_distillation"
    else:
        public_row["source_private_contribution_id"] = source_private_id
    if rewrite.get("reviewer_notes"):
        public_row["reviewer_notes"] = rewrite.get("reviewer_notes")
    return public_row


def public_org_display_name(draft: dict[str, Any], org_id: str) -> str:
    value = str(draft.get("org_display_name") or "").strip()
    if not value or value == "private":
        return org_id
    return value


def validate_reviewer_rewrite(draft: dict[str, Any], row: dict[str, Any], private_id: str) -> list[str]:
    errors: list[str] = []
    draft_summary = " ".join(str(draft.get("distilled_summary") or "").split())
    row_summary = " ".join(str(row.get("distilled_summary") or "").split())
    if not row_summary or row_summary == draft_summary:
        errors.append(f"{private_id} distilled_summary must be a reviewer-supplied rewrite, not the private draft summary")
    if len(row_summary) < 80:
        errors.append(f"{private_id} distilled_summary is too short for reviewed promotion")
    if not row.get("source_urls") and not row.get("source_record_ids"):
        errors.append(f"{private_id} reviewed promotion requires source_urls or source_record_ids")
    return errors


def public_contribution_id(org_id: str, private_contribution_id: str) -> str:
    suffix = sha256_text(f"{org_id}:{private_contribution_id}")[:16]
    return f"{org_id}:{suffix}"


def default_promotion_path(org_id: str, reviewed: bool = False) -> Path:
    if reviewed:
        return REPO_ROOT / "contributions" / org_id / "bundle.jsonl"
    return REVIEW_DIR / "contribution-promotion" / f"{org_id}.staging.jsonl"


def duplicate_public_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: dict[str, int] = {}
    seen_titles: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    for index, row in enumerate(rows, start=1):
        contribution_id = str(row.get("contribution_id") or "")
        title_key = normalize_for_duplicate(str(row.get("title") or ""))
        for value in row.get("source_urls") or []:
            url = str(value).strip().lower()
            if url:
                if url in seen_urls:
                    errors.append(f"duplicate source_url {url} at rows {seen_urls[url]} and {index}")
                seen_urls[url] = index
        if contribution_id:
            if contribution_id in seen_ids:
                errors.append(f"duplicate contribution_id {contribution_id} at rows {seen_ids[contribution_id]} and {index}")
            seen_ids[contribution_id] = index
        if title_key:
            if title_key in seen_titles:
                errors.append(f"duplicate normalized title {title_key} at rows {seen_titles[title_key]} and {index}")
            seen_titles[title_key] = index
    return errors


def normalize_for_duplicate(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def write_private_promotion_dependencies(
    org_id: str,
    public_output_path: Path,
    drafts: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    append: bool = False,
) -> Path:
    output = private_promotion_dependency_path(org_id)
    existing = list(read_jsonl(output)) if append else []
    rows = existing + private_promotion_dependency_rows(org_id, public_output_path, drafts, public_rows)
    write_jsonl(output, rows)
    return output


def private_promotion_dependency_rows(
    org_id: str,
    public_output_path: Path,
    drafts: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    public_path = relative_path(public_output_path)
    rows = []
    for draft, public_row in zip(drafts, public_rows):
        rows.append(
            {
                "schema": PRIVATE_PROMOTION_DEPENDENCY_SCHEMA,
                "public_contribution_id": public_row.get("contribution_id"),
                "private_contribution_id": draft.get("contribution_id"),
                "source_id": draft.get("source_id"),
                "org_id": org_id,
                "concept_ids": public_row.get("concept_ids") or draft.get("concept_ids") or [],
                "private_source_hashes": draft.get("private_source_hashes") or [],
                "private_path_hashes": draft.get("private_path_hashes") or [],
                "public_artifact_path": public_path,
                "created_at": now_iso(),
                "publishability_status": "private_dependency_only",
            }
        )
    return rows


def create_contribution_template(
    org_id: str,
    root: Optional[Path] = None,
    org_display_name: Optional[str] = None,
    overwrite: bool = False,
) -> Path:
    if not safe_org_id(org_id):
        raise ValueError("org_id must contain only lowercase letters, numbers, dashes, or underscores")
    base = root or REPO_ROOT / "contributions"
    output = base / org_id / "bundle.example.jsonl"
    if output.exists() and not overwrite:
        raise FileExistsError(output)
    write_jsonl(output, [contribution_template_row(org_id, org_display_name or "Example Church")])
    return output


def contribution_template_row(org_id: str, org_display_name: str) -> dict[str, Any]:
    return {
        "schema": CONTRIBUTION_SCHEMA,
        "contribution_id": f"{org_id}:replace-with-stable-id",
        "org_id": org_id,
        "org_display_name": org_display_name,
        "concept_ids": ["workflows"],
        "contribution_type": "troubleshooting_pattern",
        "title": "Replace with a public-safe title",
        "distilled_summary": "Replace with newly written public-safe guidance. Do not copy private docs, transcripts, staff notes, SQL exports, or internal runbooks.",
        "source_urls": ["https://community.rockrms.com/documentation"],
        "source_record_ids": [],
        "redaction_attestation": False,
        "review_status": "draft_private",
        "license_attestation": False,
        "confidence": "needs_review",
        "needs_live_verification": True,
    }


def safe_org_id(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]*", value))


def increment(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def sorted_counts(counts: dict[str, int]) -> list[dict[str, Any]]:
    return [{"value": key, "count": value} for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def counted_values(values: Iterable[Any]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for value in values:
        if value in (None, "", [], {}):
            continue
        increment(counts, str(value))
    return sorted_counts(counts)


def contribution_paths(root: Optional[Path] = None) -> list[Path]:
    base = root or REPO_ROOT / "contributions"
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.jsonl") if not path.name.endswith(EXAMPLE_BUNDLE_SUFFIX))


def contribution_example_paths(root: Optional[Path] = None) -> list[Path]:
    base = root or REPO_ROOT / "contributions"
    if not base.exists():
        return []
    if base.is_file():
        return [base] if base.name.endswith(EXAMPLE_BUNDLE_SUFFIX) else []
    return sorted(path for path in base.rglob(f"*{EXAMPLE_BUNDLE_SUFFIX}"))


def iter_contribution_rows(paths: Iterable[Path]) -> Iterable[tuple[Path, dict[str, Any]]]:
    for path in paths:
        for row in read_jsonl(path):
            yield path, row


def empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def truthy_attestation(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "reviewed", "attested", "approved"}
    return False


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)
