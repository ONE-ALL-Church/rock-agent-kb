from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .audit import audit_license_records
from .claims import approved_claims_path, validate_claim_file
from .concepts import REQUIRED_AGENT_ENTRYPOINT_FILES, load_concepts, report_concept_staleness, report_guide_refresh_plan
from .jsonl import read_jsonl
from .lava_capabilities import (
    AGENT_CAPABILITY_JSONL,
    AGENT_SUMMARY_JSON,
    CAPABILITY_INDEX,
    CAPABILITY_JSONL,
    DEPENDENCY_JSON,
    LAVA_CAPABILITY_SCHEMA,
    LAVA_DEPENDENT_CONCEPTS,
    SAFETY_MATRIX,
    USAGE_EXAMPLES,
)
from .lava_contexts import (
    AGENT_CONTEXT_JSONL,
    AGENT_CONTEXT_SUMMARY_JSON,
    CONTEXT_DEPENDENCY_JSON,
    CONTEXT_INDEX,
    CONTEXT_JSONL,
    LAVA_CONTEXT_SCHEMA,
)
from .media import media_global_index_path, media_priority_queue_path, media_priority_report_path, media_status_report
from .mobile_selector_audit import mobile_selector_audit_status
from .paths import AGENT_DIR, DATA_DIR, KNOWLEDGE_DIR, NORMALIZED_DIR, REPO_ROOT
from .publish import audit_public_export_manifest, audit_source_policy, iter_public_files, public_export_manifest
from .sources import load_sources, validate_registry

READINESS_SCHEMA = "rock-kb-goal-readiness-v1"


def goal_readiness_report(include_private: bool = True) -> dict[str, Any]:
    checks = [
        source_registry_check(),
        claim_graph_check(),
        public_policy_check(),
        public_export_check(),
        agent_manifest_check(),
        concept_artifacts_check(),
        lava_capability_reference_check(),
        lava_context_reference_check(),
        rebuild_metadata_check(),
    ]
    has_private = private_processing_artifacts_available()
    if include_private and has_private:
        checks.extend(
            [
                normalized_corpus_check(),
                concept_staleness_check(),
                guide_refresh_plan_check(),
                mobile_selector_audit_check(),
                private_media_check(),
                private_public_boundary_check(),
            ]
        )
    else:
        if include_private:
            checks.append(private_corpus_absent_check())
        checks.append(private_public_boundary_check())
    return {
        "schema": READINESS_SCHEMA,
        "scope": "full" if include_private and has_private else "public",
        "status": readiness_status(checks),
        "summary": readiness_summary(checks),
        "checks": checks,
    }


def readiness_status(checks: list[dict[str, Any]]) -> str:
    if any(check["status"] == "fail" for check in checks):
        return "fail"
    if any(check["status"] == "warn" for check in checks):
        return "incomplete"
    return "pass"


def readiness_summary(checks: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "pass": sum(1 for check in checks if check["status"] == "pass"),
        "warn": sum(1 for check in checks if check["status"] == "warn"),
        "fail": sum(1 for check in checks if check["status"] == "fail"),
    }


def check(check_id: str, status: str, message: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "id": check_id,
        "status": status,
        "message": message,
        "evidence": evidence or {},
    }


def source_registry_check() -> dict[str, Any]:
    errors = validate_registry()
    sources = load_sources()
    return check(
        "source_registry",
        "fail" if errors else "pass",
        "Source registry is valid." if not errors else "Source registry has validation errors.",
        {"source_count": len(sources), "errors": errors},
    )


def claim_graph_check() -> dict[str, Any]:
    path = approved_claims_path()
    errors = []
    rows = []
    if not path.exists():
        errors.append("claims/approved-claims.jsonl is missing; run kb build --stage claims")
    else:
        rows = list(read_jsonl(path))
        errors.extend(validate_claim_file(path, public=True))
    authority_tiers = sorted({str(row.get("authority_tier")) for row in rows if row.get("authority_tier")})
    missing_traceability = [
        row.get("claim_id")
        for row in rows
        if not (row.get("source_refs") or row.get("source_record_ids"))
    ]
    if missing_traceability:
        errors.append(f"{len(missing_traceability)} claims lack source traceability")
    status = "fail" if errors else "pass"
    return check(
        "claim_graph",
        status,
        "Approved claim graph exists and validates." if status == "pass" else "Approved claim graph is missing or invalid.",
        {
            "path": str(path),
            "claim_count": len(rows),
            "authority_tiers": authority_tiers,
            "errors": errors[:50],
            "error_count": len(errors),
        },
    )


def normalized_corpus_check() -> dict[str, Any]:
    paths = sorted(NORMALIZED_DIR.glob("*.jsonl"))
    rows = []
    for path in paths:
        rows.extend(read_jsonl(path))
    source_ids = sorted({str(row.get("source_id")) for row in rows if row.get("source_id")})
    status = "pass" if len(rows) >= 100 and len(source_ids) >= 10 else "warn"
    return check(
        "normalized_corpus",
        status,
        "Normalized corpus has broad source coverage." if status == "pass" else "Normalized corpus is still shallow.",
        {"record_count": len(rows), "source_count": len(source_ids), "normalized_files": len(paths)},
    )


def private_processing_artifacts_available() -> bool:
    return any(NORMALIZED_DIR.glob("*.jsonl")) or media_global_index_path().exists() or any((DATA_DIR / "review").glob("**/*"))


def private_corpus_absent_check() -> dict[str, Any]:
    return check(
        "private_corpus",
        "pass",
        "Private corpus is not mounted; validated committed public artifacts only.",
        {
            "normalized_files": 0,
            "media_index_exists": False,
            "review_artifacts_present": False,
        },
    )


def public_policy_check() -> dict[str, Any]:
    errors = audit_source_policy()
    errors.extend(audit_license_records())
    return check(
        "public_policy",
        "fail" if errors else "pass",
        "Source policy and license audits pass." if not errors else "Source policy or license audit failed.",
        {"errors": errors[:50], "error_count": len(errors)},
    )


def public_export_check() -> dict[str, Any]:
    errors = audit_public_export_manifest()
    manifest = public_export_manifest()
    manifest_files = len(manifest.get("files") or [])
    return check(
        "public_export",
        "fail" if errors else "pass",
        "Public export exists and audits pass." if not errors else "Public export is not currently publishable.",
        {
            "manifest_source": "in_memory_public_surface",
            "file_count": manifest_files,
            "errors": errors[:50],
            "error_count": len(errors),
        },
    )


def agent_manifest_check() -> dict[str, Any]:
    manifest_path = AGENT_DIR / "rock-kb-manifest.json"
    errors = []
    manifest: dict[str, Any] = {}
    if not manifest_path.exists():
        errors.append("agent/rock-kb-manifest.json is missing")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("agent/rock-kb-manifest.json is invalid JSON")
    concepts = load_concepts()
    manifest_concepts = {row.get("concept_id"): row for row in manifest.get("concepts") or []}
    for concept in concepts:
        row = manifest_concepts.get(concept.id)
        if not row:
            errors.append(f"manifest missing concept {concept.id}")
            continue
        for field in REQUIRED_AGENT_ENTRYPOINT_FILES:
            key = field.replace(".md", "").replace(".jsonl", "").replace(".json", "").replace("-", "_")
            if field == "quickstart.md":
                key = "quickstart"
            elif field == "task-cards.jsonl":
                key = "task_cards"
            elif field == "release-caveats.jsonl":
                key = "release_caveats"
            elif field == "section-source-map.jsonl":
                key = "section_source_map"
            elif field == "section-status.jsonl":
                key = "section_status"
            elif field == "troubleshooting-tree.json":
                key = "troubleshooting_tree"
            elif field == "open-questions.md":
                key = "open_questions"
            if not row.get(key):
                errors.append(f"manifest concept {concept.id} missing {key}")
        for key in ["approved_claims", "approved_media", "live_inspection_checklist", "live_probe_recipes", "answers"]:
            if not row.get(key):
                errors.append(f"manifest concept {concept.id} missing {key}")
    if not (manifest.get("agent_entrypoints") or {}).get("private_media"):
        errors.append("manifest missing private_media entrypoint")
    entrypoints = manifest.get("agent_entrypoints") or {}
    if not entrypoints.get("source_summaries"):
        errors.append("manifest missing source_summaries entrypoint")
    if not entrypoints.get("source_summary_report"):
        errors.append("manifest missing source_summary_report entrypoint")
    if not entrypoints.get("approved_claims"):
        errors.append("manifest missing approved_claims entrypoint")
    for field in [
        "answer_pack",
        "live_checklists",
        "live_probe_recipes",
        "claim_review_queue",
        "source_conflicts",
        "distilled_claims",
        "source_authority_rules",
        "evaluation_set",
        "evaluation_results",
        "evaluation_report",
        "claim_review_dashboard",
        "lava_capabilities",
        "lava_capability_summary",
        "lava_contexts",
        "lava_context_summary",
        "lava_context_directory",
        "lava_reference_index",
        "lava_safety_matrix",
        "lava_agent_usage_examples",
    ]:
        if not entrypoints.get(field):
            errors.append(f"manifest missing {field} entrypoint")
    source_summaries = manifest.get("source_summaries") or {}
    if not source_summaries.get("path"):
        errors.append("manifest missing source_summaries path")
    if not source_summaries.get("report"):
        errors.append("manifest missing source_summaries report")
    approved_claims = manifest.get("approved_claims") or {}
    if not approved_claims.get("path"):
        errors.append("manifest missing approved_claims path")
    for path in [
        "agent/answer-pack.jsonl",
        "agent/live-inspection-checklists.jsonl",
        "agent/live-probe-recipes.jsonl",
        "agent/claim-review-queue.jsonl",
        "agent/source-conflicts.jsonl",
        "agent/distilled-claims.jsonl",
        "agent/source-authority-rules.jsonl",
        "agent/evaluation-set.jsonl",
        "agent/evaluation-results.jsonl",
        "agent/evaluation-report.json",
        "agent/claim-review-dashboard.md",
    ]:
        if not (AGENT_DIR.parent / path).exists():
            errors.append(f"{path} is missing")
    return check(
        "agent_manifest",
        "fail" if errors else "pass",
        "Agent manifest exposes required entrypoints." if not errors else "Agent manifest is missing required entrypoints.",
        {"concept_count": len(manifest_concepts), "expected_concepts": len(concepts), "errors": errors[:50], "error_count": len(errors)},
    )


def concept_artifacts_check() -> dict[str, Any]:
    errors = []
    quality_scores = []
    for concept in load_concepts():
        concept_dir = KNOWLEDGE_DIR / "concepts" / concept.id
        for filename in REQUIRED_AGENT_ENTRYPOINT_FILES:
            if not (concept_dir / filename).exists():
                errors.append(f"{concept.id}/{filename} missing")
        quality_path = concept_dir / "guide-quality.json"
        if not quality_path.exists():
            errors.append(f"{concept.id}/guide-quality.json missing")
            continue
        quality = json.loads(quality_path.read_text(encoding="utf-8"))
        quality_scores.append(int(quality.get("score") or 0))
        if quality.get("status") != "pass":
            errors.append(f"{concept.id} guide quality status is {quality.get('status')}")
    return check(
        "concept_artifacts",
        "fail" if errors else "pass",
        "All concept agent entrypoints and guide-quality records pass." if not errors else "Concept artifacts are incomplete.",
        {"concept_count": len(load_concepts()), "min_quality_score": min(quality_scores) if quality_scores else 0, "errors": errors[:50], "error_count": len(errors)},
    )


def concept_staleness_check() -> dict[str, Any]:
    rows = report_concept_staleness()
    stale = [row for row in rows if row.get("needs_rebuild")]
    return check(
        "concept_staleness",
        "warn" if stale else "pass",
        "Concept source hashes are current." if not stale else "Some concept guides need rebuild.",
        {"concept_count": len(rows), "stale_concepts": [row.get("concept_id") for row in stale]},
    )


def guide_refresh_plan_check() -> dict[str, Any]:
    plan = report_guide_refresh_plan()
    needs_index = plan.get("needs_generated_index_rebuild") or []
    needs_guide = plan.get("needs_long_form_guide_refresh") or []
    stale = sorted(set(needs_index) | set(needs_guide))
    return check(
        "guide_refresh_plan",
        "warn" if stale else "pass",
        "Approved media dependencies are reflected in generated indexes and long-form guides."
        if not stale
        else "Approved media dependencies require generated index rebuilds or long-form guide refreshes.",
        {
            "concept_count": plan.get("concept_count"),
            "needs_generated_index_rebuild": needs_index,
            "needs_long_form_guide_refresh": needs_guide,
        },
    )


def lava_capability_reference_check() -> dict[str, Any]:
    required_paths = [
        CAPABILITY_JSONL,
        CAPABILITY_INDEX,
        SAFETY_MATRIX,
        USAGE_EXAMPLES,
        DEPENDENCY_JSON,
        AGENT_CAPABILITY_JSONL,
        AGENT_SUMMARY_JSON,
    ]
    errors = [f"{path.relative_to(REPO_ROOT)} is missing" for path in required_paths if not path.exists()]
    rows = list(read_jsonl(CAPABILITY_JSONL)) if CAPABILITY_JSONL.exists() else []
    categories = sorted({str(row.get("category")) for row in rows if row.get("category")})
    risk_tiers = sorted({str(row.get("risk_tier")) for row in rows if row.get("risk_tier")})
    if len(rows) < 50:
        errors.append(f"lava capability row count is too low: {len(rows)}")
    for index, row in enumerate(rows):
        if row.get("schema") != LAVA_CAPABILITY_SCHEMA:
            errors.append(f"lava capability row {index} has wrong schema")
        if not (row.get("official_url") and row.get("source_record_id") and row.get("source_content_hash")):
            errors.append(f"lava capability row {index} lacks source traceability")
        if not isinstance(row.get("requires_security_review"), bool):
            errors.append(f"lava capability row {index} lacks boolean security review flag")
    dependency: dict[str, Any] = {}
    if DEPENDENCY_JSON.exists():
        try:
            dependency = json.loads(DEPENDENCY_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("lava capability dependency file is invalid JSON")
    dependent_concepts = set(dependency.get("dependent_concepts") or [])
    missing_dependents = sorted(LAVA_DEPENDENT_CONCEPTS - dependent_concepts)
    if missing_dependents:
        errors.append(f"lava capability dependencies missing concepts: {', '.join(missing_dependents)}")
    return check(
        "lava_capability_reference",
        "fail" if errors else "pass",
        "Lava capability reference layer exists and is source-traceable."
        if not errors
        else "Lava capability reference layer is missing or invalid.",
        {
            "capability_count": len(rows),
            "categories": categories,
            "risk_tiers": risk_tiers,
            "dependency_path": str(DEPENDENCY_JSON.relative_to(REPO_ROOT)),
            "dependent_concepts": sorted(dependent_concepts),
            "errors": errors[:50],
            "error_count": len(errors),
        },
    )


def lava_context_reference_check() -> dict[str, Any]:
    required_paths = [
        CONTEXT_JSONL,
        CONTEXT_INDEX,
        CONTEXT_DEPENDENCY_JSON,
        AGENT_CONTEXT_JSONL,
        AGENT_CONTEXT_SUMMARY_JSON,
    ]
    errors = [f"{path.relative_to(REPO_ROOT)} is missing" for path in required_paths if not path.exists()]
    rows = list(read_jsonl(CONTEXT_JSONL)) if CONTEXT_JSONL.exists() else []
    families = sorted({str(row.get("context_family")) for row in rows if row.get("context_family")})
    surface_types = sorted({str(row.get("surface_type")) for row in rows if row.get("surface_type")})
    if len(rows) < 20:
        errors.append(f"lava context row count is too low: {len(rows)}")
    for index, row in enumerate(rows):
        if row.get("schema") != LAVA_CONTEXT_SCHEMA:
            errors.append(f"lava context row {index} has wrong schema")
        if not (row.get("source_url") and row.get("source_file") and row.get("source_line_start")):
            errors.append(f"lava context row {index} lacks source traceability")
        if not isinstance(row.get("needs_live_verification"), bool):
            errors.append(f"lava context row {index} lacks boolean live verification flag")
    dependency: dict[str, Any] = {}
    if CONTEXT_DEPENDENCY_JSON.exists():
        try:
            dependency = json.loads(CONTEXT_DEPENDENCY_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("lava context dependency file is invalid JSON")
    if not dependency.get("source_dependencies"):
        errors.append("lava context dependencies lack source_dependencies")
    return check(
        "lava_context_reference",
        "fail" if errors else "pass",
        "Lava data-context directory exists and is source-traceable."
        if not errors
        else "Lava data-context directory is missing or invalid.",
        {
            "context_count": len(rows),
            "families": families,
            "surface_types": surface_types,
            "dependency_path": str(CONTEXT_DEPENDENCY_JSON.relative_to(REPO_ROOT)),
            "errors": errors[:50],
            "error_count": len(errors),
        },
    )


def mobile_selector_audit_check() -> dict[str, Any]:
    status = mobile_selector_audit_status()
    missing_paths = status.get("missing_paths") or []
    inventory_errors = status.get("inventory_errors") or []
    stale = status.get("stale_dependencies") or []
    dependency = status.get("dependency") or {}
    if missing_paths or inventory_errors:
        check_status = "fail"
        message = "Mobile selector audit resources are missing or invalid."
    elif stale:
        check_status = "warn"
        message = "Mobile selector audit source hashes changed; rerun kb build --stage mobile-selector-audit after review."
    else:
        check_status = "pass"
        message = "Mobile selector audit resources and source dependencies are current."
    return check(
        "mobile_selector_audit",
        check_status,
        message,
        {
            "missing_paths": missing_paths,
            "inventory_error_count": len(inventory_errors),
            "inventory_errors": inventory_errors[:50],
            "stale_dependency_count": len(stale),
            "stale_dependencies": stale[:25],
            "selector_row_count": dependency.get("selector_row_count"),
            "source_url_count": dependency.get("source_url_count"),
            "dependency_path": str(dependency.get("resource_paths", {}).get("selector_dependencies") or ""),
        },
    )


def rebuild_metadata_check() -> dict[str, Any]:
    concept_count = len(load_concepts())
    dependency_rows = list(read_jsonl(AGENT_DIR / "concept-dependencies.jsonl"))
    section_rows = list(read_jsonl(AGENT_DIR / "section-source-map.jsonl"))
    task_rows = list(read_jsonl(AGENT_DIR / "concept-task-cards.jsonl"))
    status = "pass" if len(dependency_rows) >= concept_count and section_rows and task_rows else "fail"
    return check(
        "rebuild_metadata",
        status,
        "Source-hash dependency and section metadata exists." if status == "pass" else "Rebuild metadata is missing or incomplete.",
        {"dependency_rows": len(dependency_rows), "section_rows": len(section_rows), "task_rows": len(task_rows), "concept_count": concept_count},
    )


def private_media_check() -> dict[str, Any]:
    media_sources = [source for source in load_sources() if source.kind == "podcast_rss" or "media_discovery" in source.preferred_tooling or "local_transcription" in source.preferred_tooling]
    reports = [media_status_report(source) for source in media_sources]
    media_rows = sum(report["media_rows"] for report in reports)
    sidecar_rows = sum(report["sidecar_rows"] for report in reports)
    transcribed_rows = sum(report["transcribed_rows"] for report in reports)
    pending = sum(report["pending_transcription"] for report in reports)
    index_exists = media_global_index_path().exists()
    queue_exists = media_priority_queue_path().exists()
    status = "pass"
    message = "Private media corpus has sidecars and transcript coverage."
    if not index_exists or media_rows == 0 or sidecar_rows == 0:
        status = "fail"
        message = "Private media discovery/indexing is missing."
    elif transcribed_rows == 0 or pending > transcribed_rows:
        status = "warn"
        message = "Private media discovery works, but transcription coverage is still partial."
    elif pending and not queue_exists:
        status = "warn"
        message = "Private media has pending rows but no prioritized transcription queue."
    return check(
        "private_media",
        status,
        message,
        {
            "media_sources": len(media_sources),
            "media_rows": media_rows,
            "sidecar_rows": sidecar_rows,
            "transcribed_rows": transcribed_rows,
            "pending_transcription": pending,
            "global_index": str(media_global_index_path()),
            "priority_queue": str(media_priority_queue_path()) if queue_exists else "",
            "priority_report": str(media_priority_report_path()) if media_priority_report_path().exists() else "",
        },
    )


def private_public_boundary_check() -> dict[str, Any]:
    markers = ["derived_from_private_transcript", "Private transcript-derived insight", "private_transcript_only"]
    findings = public_marker_findings(markers)
    normalized_private_rows = [
        row
        for path in sorted(NORMALIZED_DIR.glob("*.jsonl"))
        for row in read_jsonl(path)
        if row.get("derived_from_private_transcript") or (row.get("private_storage") and row.get("needs_review"))
    ]
    return check(
        "private_public_boundary",
        "fail" if findings else "pass",
        "Private-derived rows are absent from public artifacts." if not findings else "Private-derived markers appear in public artifacts.",
        {"public_marker_findings": findings[:50], "private_normalized_rows": len(normalized_private_rows)},
    )


def public_marker_findings(markers: Iterable[str]) -> list[str]:
    findings: list[str] = []
    for path in iter_public_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in markers:
            if marker in text:
                findings.append(f"{rel}: contains {marker}")
    public_export = DATA_DIR / "public-export"
    if public_export.exists():
        for path in sorted(public_export.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in markers:
                if marker in text:
                    findings.append(f"{rel}: contains {marker}")
    return findings
