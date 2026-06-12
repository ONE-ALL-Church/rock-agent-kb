from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Optional

from .jsonl import read_jsonl
from .paths import REVIEW_DIR

PRIVATE_PROMOTION_DEPENDENCY_SCHEMA = "rock-kb-private-promotion-dependency-v1"


def private_promotion_dependency_dir() -> Path:
    return REVIEW_DIR / "private-promotion-dependencies"


def private_promotion_dependency_path(org_id: str) -> Path:
    return private_promotion_dependency_dir() / f"{org_id}.jsonl"


def private_promotion_dependency_paths(path: Optional[Path] = None) -> list[Path]:
    if path:
        return [path] if path.is_file() else sorted(path.glob("*.jsonl"))
    base = private_promotion_dependency_dir()
    if not base.exists():
        return []
    return sorted(base.glob("*.jsonl"))


def private_scan_paths(path: Optional[Path] = None) -> list[Path]:
    if path:
        return [path] if path.is_file() else sorted(path.glob("private-scan-*.jsonl"))
    if not REVIEW_DIR.exists():
        return []
    return sorted(REVIEW_DIR.glob("private-scan-*.jsonl"))


def private_scan_hashes(scan_path: Path, source_id: Optional[str] = None, org_id: Optional[str] = None) -> set[str]:
    hashes = set()
    for row in read_jsonl(scan_path):
        if source_id and row.get("source_id") != source_id:
            continue
        if org_id and row.get("org_id") != org_id:
            continue
        content_hash = row.get("content_hash")
        if content_hash:
            hashes.add(str(content_hash))
    return hashes


def report_private_impact(
    scan_path: Path,
    dependency_path: Optional[Path] = None,
    source_id: Optional[str] = None,
    org_id: Optional[str] = None,
) -> dict[str, Any]:
    current_hashes = private_scan_hashes(scan_path, source_id=source_id, org_id=org_id)
    dependencies = list(iter_private_promotion_dependencies(dependency_path, source_id=source_id, org_id=org_id))
    rows = [private_dependency_impact_row(dependency, current_hashes) for dependency in dependencies]
    impacted = [row for row in rows if row.get("needs_rebuild")]
    concept_ids = sorted({concept for row in impacted for concept in row.get("concept_ids") or []})
    artifact_paths = sorted({str(row.get("public_artifact_path")) for row in impacted if row.get("public_artifact_path")})
    return {
        "schema": "rock-kb-private-impact-report-v1",
        "scan_path": str(scan_path),
        "dependency_paths": [str(path) for path in private_promotion_dependency_paths(dependency_path)],
        "source_filter": source_id,
        "org_filter": org_id,
        "records": len(rows),
        "impacted": len(impacted),
        "impacted_concepts": concept_ids,
        "impacted_public_artifacts": artifact_paths,
        "rows": rows,
    }


def iter_private_promotion_dependencies(
    dependency_path: Optional[Path] = None,
    source_id: Optional[str] = None,
    org_id: Optional[str] = None,
) -> Iterable[dict[str, Any]]:
    for path in private_promotion_dependency_paths(dependency_path):
        for row in read_jsonl(path):
            if source_id and row.get("source_id") != source_id:
                continue
            if org_id and row.get("org_id") != org_id:
                continue
            yield row


def private_dependency_impact_row(dependency: dict[str, Any], current_hashes: set[str]) -> dict[str, Any]:
    hashes = [str(value) for value in dependency.get("private_source_hashes") or [] if value]
    missing = sorted(value for value in hashes if value not in current_hashes)
    return {
        "public_contribution_id": dependency.get("public_contribution_id"),
        "private_contribution_id": dependency.get("private_contribution_id"),
        "source_id": dependency.get("source_id"),
        "org_id": dependency.get("org_id"),
        "concept_ids": dependency.get("concept_ids") or [],
        "public_artifact_path": dependency.get("public_artifact_path"),
        "needs_rebuild": bool(missing),
        "reason": "private_source_hash_missing_or_changed" if missing else "current",
        "private_source_hash_count": len(hashes),
        "missing_private_source_hashes": missing,
    }


def private_impacts_by_concept(scan_path: Optional[Path] = None) -> dict[str, list[dict[str, Any]]]:
    paths = private_promotion_dependency_paths()
    scan_paths = [path for path in private_scan_paths(scan_path) if path.exists()]
    if not paths or not scan_paths:
        return {}
    current_hashes: set[str] = set()
    for current_scan_path in scan_paths:
        current_hashes.update(private_scan_hashes(current_scan_path))
    impacts: dict[str, list[dict[str, Any]]] = {}
    for dependency in iter_private_promotion_dependencies():
        row = private_dependency_impact_row(dependency, current_hashes)
        if not row.get("needs_rebuild"):
            continue
        row = {**row, "scan_paths": [str(path) for path in scan_paths]}
        for concept_id in row.get("concept_ids") or []:
            impacts.setdefault(str(concept_id), []).append(row)
    return impacts
