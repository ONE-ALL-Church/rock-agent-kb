from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .paths import REPO_ROOT
from .schemas.knowledge import IngestionMode


@dataclass(frozen=True)
class SourceFamilyContract:
    knowledge_type: str
    ingestion_mode: IngestionMode
    payload_schemas: tuple[str, ...]
    required_freshness_fields: tuple[str, ...]
    mutable: bool
    optional_freshness_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class GeneratedKnowledgeContract:
    source_family: str
    ingestion_mode: IngestionMode
    source_unit_contract: str
    knowledge_unit_contract: str
    review_gate: str
    change_policy: str


SOURCE_FAMILY_CONTRACT_MANIFEST_PATH = (
    REPO_ROOT / "canonical" / "source-family-contracts-v1.json"
)


GENERATED_KNOWLEDGE_CONTRACTS: dict[str, GeneratedKnowledgeContract] = {
    "official_documentation": GeneratedKnowledgeContract(
        source_family="official_documentation",
        ingestion_mode="source_native_distillation",
        source_unit_contract="rock-kb-source-unit-v2",
        knowledge_unit_contract="rock-kb-reviewed-source-native-artifact-v1",
        review_gate="schema_constrained_generation_and_maintainer_approval",
        change_policy="revalidate_only_units_dependent_on_changed_source_units",
    ),
    "reviewed_cross_source": GeneratedKnowledgeContract(
        source_family="reviewed_cross_source",
        ingestion_mode="reviewed_cross_source_synthesis",
        source_unit_contract="rock-kb-source-unit-v2",
        knowledge_unit_contract="rock-kb-reviewed-cross-source-decision-v1",
        review_gate="maintainer_reviewed_multi_source_evidence",
        change_policy="revalidate_when_any_cited_source_revision_changes",
    ),
    "approved_claim": GeneratedKnowledgeContract(
        source_family="approved_claim",
        ingestion_mode="legacy_reviewed_claim_projection",
        source_unit_contract="legacy_source_reference",
        knowledge_unit_contract="rock-kb-approved-claim-v1",
        review_gate="existing_claim_review_and_validation",
        change_policy="legacy_path_pending_source_native_or_typed_migration",
    ),
}


SOURCE_FAMILY_CONTRACTS: dict[str, SourceFamilyContract] = {
    "community_contribution": SourceFamilyContract(
        knowledge_type="community_contribution",
        ingestion_mode="reviewed_typed_record",
        payload_schemas=(),
        required_freshness_fields=("content_hash",),
        mutable=False,
    ),
    "recipe": SourceFamilyContract(
        knowledge_type="recipe",
        ingestion_mode="reviewed_typed_record",
        payload_schemas=("rock-kb-recipe-v1",),
        required_freshness_fields=("implementation.commit_sha", "updated_at"),
        mutable=False,
    ),
    "lava_context": SourceFamilyContract(
        knowledge_type="lava_context",
        ingestion_mode="source_code_derived_record",
        payload_schemas=("rock-kb-lava-context-v2", "rock-kb-lava-context-v3"),
        required_freshness_fields=("source_commit", "last_seen_version"),
        mutable=False,
    ),
    "model_map": SourceFamilyContract(
        knowledge_type="model_map",
        ingestion_mode="official_api_derived_record",
        payload_schemas=("rock-kb-model-map-search-payload-v1",),
        required_freshness_fields=("identity.rock_version", "identity.track"),
        mutable=True,
    ),
    "rock_issue": SourceFamilyContract(
        knowledge_type="rock_issue",
        ingestion_mode="official_api_derived_record",
        payload_schemas=("rock-kb-rock-issue-v1",),
        required_freshness_fields=("updated_at", "source_content_hash"),
        optional_freshness_fields=("timeline_sha256",),
        mutable=True,
    ),
    "rock_idea": SourceFamilyContract(
        knowledge_type="rock_idea",
        ingestion_mode="official_api_derived_record",
        payload_schemas=("rock-kb-rock-idea-v1",),
        required_freshness_fields=(
            "last_checked_at",
            "content_changed_at",
            "content_hash",
        ),
        mutable=True,
    ),
    "source_summary": SourceFamilyContract(
        knowledge_type="source_summary",
        ingestion_mode="legacy_summary_projection",
        payload_schemas=("rock-kb-public-source-summary-v1",),
        required_freshness_fields=("content_hash", "retrieved_at"),
        optional_freshness_fields=("updated_at",),
        mutable=True,
    ),
}


def source_family_contract(kind: str, payload: dict[str, Any]) -> SourceFamilyContract:
    contract = SOURCE_FAMILY_CONTRACTS.get(kind)
    if contract is None:
        raise ValueError(f"no canonical source-family contract for {kind!r}")
    payload_schema = str(payload.get("schema") or "")
    if contract.payload_schemas and payload_schema not in contract.payload_schemas:
        raise ValueError(
            f"{kind} payload schema {payload_schema!r} is not allowed by its "
            "canonical source-family contract"
        )
    missing_fields = [
        path
        for path in contract.required_freshness_fields
        if payload_field_value(payload, path) in (None, "")
    ]
    if missing_fields:
        raise ValueError(
            f"{kind} payload is missing required freshness fields: "
            f"{', '.join(missing_fields)}"
        )
    return contract


def payload_field_value(payload: dict[str, Any], path: str) -> Any:
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def source_family_contract_summary(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    counts: dict[str, int] = {}
    errors: list[str] = []
    for row in rows:
        kind = str(row.get("kind") or "")
        if kind == "claim":
            continue
        try:
            contract = source_family_contract(kind, dict(row.get("payload") or {}))
        except ValueError as exc:
            errors.append(f"{row.get('id') or '<missing-id>'}: {exc}")
            continue
        counts[contract.ingestion_mode] = counts.get(contract.ingestion_mode, 0) + 1
    return {
        "status": "ok" if not errors else "fail",
        "contract_count": len(SOURCE_FAMILY_CONTRACTS),
        "row_count": sum(counts.values()),
        "ingestion_mode_counts": dict(sorted(counts.items())),
        "errors": errors[:50],
    }


def source_family_contract_manifest() -> dict[str, Any]:
    return {
        "schema": "rock-kb-source-family-contracts-v1",
        "status": "reviewed",
        "architecture": (
            "source observation -> deterministic source unit -> reviewed "
            "knowledge unit -> rebuildable projections"
        ),
        "default_retrieval_projection": "legacy",
        "canonical_projection_state": "shadow_and_opt_in_canary",
        "generated_knowledge_contracts": [
            asdict(GENERATED_KNOWLEDGE_CONTRACTS[key])
            for key in sorted(GENERATED_KNOWLEDGE_CONTRACTS)
        ],
        "typed_record_contracts": [
            {
                **asdict(SOURCE_FAMILY_CONTRACTS[key]),
                "payload_schemas": list(
                    SOURCE_FAMILY_CONTRACTS[key].payload_schemas
                ),
                "required_freshness_fields": list(
                    SOURCE_FAMILY_CONTRACTS[key].required_freshness_fields
                ),
                "optional_freshness_fields": list(
                    SOURCE_FAMILY_CONTRACTS[key].optional_freshness_fields
                ),
            }
            for key in sorted(SOURCE_FAMILY_CONTRACTS)
        ],
    }


def write_source_family_contract_manifest(
    destination: Path = SOURCE_FAMILY_CONTRACT_MANIFEST_PATH,
) -> dict[str, Any]:
    manifest = source_family_contract_manifest()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-family-contract-write-v1",
        "status": "ok",
        "destination": str(destination),
        "generated_knowledge_contract_count": len(GENERATED_KNOWLEDGE_CONTRACTS),
        "typed_record_contract_count": len(SOURCE_FAMILY_CONTRACTS),
    }
