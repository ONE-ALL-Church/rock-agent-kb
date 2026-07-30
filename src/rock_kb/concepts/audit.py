from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

from ..claims import approved_claim_rows
from ..paths import AGENT_DIR
from ._shared import generated_at_iso, write_json
from .registry import Concept, load_concept_registry_metadata, load_concepts
from .synthesize import (
    concept_has_path_constraints,
    concept_source_records,
    ensure_weighted_source_coverage,
    rank_records_for_concept,
    record_constraint_values,
    record_matches_path_constraints,
)


ANSWER_BEARING_TIERS = {"source_backed", "answer_pack_approved", "live_verified"}
ROUTING_ROLES = {"primary", "cross_cutting", "aggregate"}
OFFICIAL_DOCUMENT_SOURCE_IDS = {"rock_documentation", "rock_developer", "rock_mobile_docs"}


def concept_taxonomy_audit(
    *,
    records: list[dict[str, Any]] | None = None,
    claims: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    concepts = load_concepts()
    concept_ids = [concept.id for concept in concepts]
    known_ids = set(concept_ids)
    source_records = records if records is not None else concept_source_records()
    claim_rows = list(claims) if claims is not None else approved_claim_rows()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    for concept_id, count in Counter(concept_ids).items():
        if count > 1:
            errors.append(issue(concept_id, "duplicate_concept_id", f"Concept ID appears {count} times."))

    branch_owners: dict[str, list[Concept]] = defaultdict(list)
    selected_by_record: dict[str, list[str]] = defaultdict(list)
    concept_rows = []
    for concept in concepts:
        validate_concept_shape(concept, known_ids, errors)
        branches = record_constraint_values(concept.raw, "documentation_branches")
        for branch in branches:
            branch_owners[branch].append(concept)

        ranked = rank_records_for_concept(concept, source_records)
        selected = ensure_weighted_source_coverage(concept, ranked, concept.max_records)
        official_selected = [
            record for record in selected if str(record.get("source_id") or "") in OFFICIAL_DOCUMENT_SOURCE_IDS
        ]
        for record in official_selected:
            if record.get("id"):
                selected_by_record[str(record["id"])].append(concept.id)

        routed_claims = [
            row for row in claim_rows if concept.id in {str(value) for value in row.get("concept_ids") or []}
        ]
        answer_bearing = [
            row for row in routed_claims if str(row.get("claim_tier") or "") in ANSWER_BEARING_TIERS
        ]
        routing_context = [
            row for row in routed_claims if str(row.get("claim_tier") or "") == "routing_context_only"
        ]
        branch_records = [
            record
            for record in source_records
            if str(record.get("source_id") or "") in OFFICIAL_DOCUMENT_SOURCE_IDS
            and record_matches_path_constraints(record, concept.raw)
        ] if concept_has_path_constraints(concept) else []

        concept_warnings: list[str] = []
        if (
            concept.routing_role == "primary"
            and int(concept.source_weights.get("rock_documentation") or 0) >= 4
            and not concept_has_path_constraints(concept)
        ):
            concept_warnings.append("official_document_routing_is_keyword_only")
        if not answer_bearing:
            concept_warnings.append("no_answer_bearing_claims")
        elif len(answer_bearing) < 5:
            concept_warnings.append("thin_answer_bearing_claim_coverage")
        if routed_claims and len(routing_context) / len(routed_claims) >= 0.9:
            concept_warnings.append("routing_context_dominates_claim_facets")
        if branches and not branch_records:
            errors.append(
                issue(
                    concept.id,
                    "empty_documentation_branch",
                    "No official source record matches the configured documentation branch.",
                )
            )
        for code in concept_warnings:
            warnings.append(issue(concept.id, code, taxonomy_warning_message(code)))

        concept_rows.append(
            {
                "concept_id": concept.id,
                "title": concept.title,
                "routing_role": concept.routing_role,
                "parent_concept_id": concept.parent_concept_id,
                "path_constrained": bool(concept_has_path_constraints(concept)),
                "documentation_branches": branches,
                "selected_record_count": len(selected),
                "selected_official_document_count": len(official_selected),
                "matching_branch_record_count": len(branch_records),
                "claim_facet_count": len(routed_claims),
                "answer_bearing_claim_count": len(answer_bearing),
                "routing_context_claim_count": len(routing_context),
                "answer_bearing_ratio": round(len(answer_bearing) / len(routed_claims), 4) if routed_claims else 0.0,
                "warnings": concept_warnings,
            }
        )

    for branch, owners in sorted(branch_owners.items()):
        primary_owners = [concept.id for concept in owners if concept.routing_role == "primary"]
        if len(primary_owners) > 1:
            errors.append(
                issue(
                    ",".join(primary_owners),
                    "duplicate_primary_branch_owner",
                    f"{branch} has multiple primary concept owners.",
                )
            )

    overlap_counts = Counter(len(set(values)) for values in selected_by_record.values())
    overlapping = [
        {
            "source_record_id": record_id,
            "concept_ids": sorted(set(concept_ids_for_record)),
        }
        for record_id, concept_ids_for_record in selected_by_record.items()
        if len(set(concept_ids_for_record)) > 1
    ]
    overlapping.sort(key=lambda row: (-len(row["concept_ids"]), row["source_record_id"]))
    metadata = load_concept_registry_metadata()
    if metadata["version"] < 2:
        errors.append(issue("registry", "legacy_registry_version", "Concept registry version must be at least 2."))

    return {
        "schema": "rock-kb-concept-taxonomy-audit-v1",
        "generated_at": generated_at_iso(),
        "status": "fail" if errors else "needs_review" if warnings else "pass",
        "registry_version": metadata["version"],
        "taxonomy": metadata["taxonomy"],
        "concept_count": len(concepts),
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "explicit_branch_count": len(branch_owners),
            "selected_official_record_count": len(selected_by_record),
            "selected_official_record_overlap_distribution": {
                str(key): value for key, value in sorted(overlap_counts.items())
            },
            "overlapping_selected_official_record_count": len(overlapping),
        },
        "concepts": sorted(concept_rows, key=lambda row: row["concept_id"]),
        "highest_overlap_records": overlapping[:25],
    }


def validate_concept_shape(concept: Concept, known_ids: set[str], errors: list[dict[str, str]]) -> None:
    if concept.routing_role not in ROUTING_ROLES:
        errors.append(
            issue(
                concept.id,
                "invalid_routing_role",
                f"routing_role must be one of {', '.join(sorted(ROUTING_ROLES))}.",
            )
        )
    if concept.parent_concept_id and concept.parent_concept_id not in known_ids:
        errors.append(issue(concept.id, "unknown_parent_concept", concept.parent_concept_id))
    if concept.parent_concept_id == concept.id:
        errors.append(issue(concept.id, "self_parent_concept", "A concept cannot be its own parent."))
    subguide_ids = [str(row.get("id") or "") for row in concept.subguides]
    for subguide_id, count in Counter(subguide_ids).items():
        if not subguide_id:
            errors.append(issue(concept.id, "missing_subguide_id", "Every subguide needs an ID."))
        elif count > 1:
            errors.append(issue(concept.id, "duplicate_subguide_id", subguide_id))


def issue(concept_id: str, code: str, message: str) -> dict[str, str]:
    return {"concept_id": concept_id, "code": code, "message": message}


def taxonomy_warning_message(code: str) -> str:
    return {
        "official_document_routing_is_keyword_only": (
            "A primary concept with official documentation weight has no structured path constraint."
        ),
        "no_answer_bearing_claims": "No approved answer-bearing claim is routed to this concept.",
        "thin_answer_bearing_claim_coverage": "Fewer than five approved answer-bearing claims are routed here.",
        "routing_context_dominates_claim_facets": "At least 90 percent of routed claims are context-only.",
    }[code]


def write_concept_taxonomy_audit() -> dict[str, Any]:
    report = concept_taxonomy_audit()
    write_json(AGENT_DIR / "concept-taxonomy-report.json", report)
    return report
