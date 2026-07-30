from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from .base import KBRecord


ArtifactType = Literal[
    "claim",
    "task_card",
    "recipe",
    "structured_reference",
    "source_summary",
]
Disposition = Literal[
    "claim",
    "task_card",
    "recipe",
    "structured_reference",
    "source_summary",
    "no_artifact",
    "split_required",
]
ExistingRelation = Literal[
    "novel",
    "duplicate",
    "corroborates",
    "adds_condition",
    "conflicts",
    "not_applicable",
]


class SourceNativeReferenceItem(KBRecord):
    label: str = Field(min_length=1, max_length=300)
    detail: str = Field(min_length=5, max_length=1500)
    value_status: Literal[
        "documented_behavior",
        "documented_value",
        "mutable_default",
        "example",
        "version_sensitive",
    ] = "documented_value"
    needs_verification: bool = False


class SourceNativeStep(KBRecord):
    order: int = Field(ge=1, le=50)
    instruction: str = Field(min_length=5, max_length=2000)


class SourceNativeArtifactPayload(KBRecord):
    summary: str = Field(min_length=20, max_length=5000)
    reference_items: list[SourceNativeReferenceItem] = Field(
        default_factory=list,
        max_length=50,
    )
    steps: list[SourceNativeStep] = Field(default_factory=list, max_length=50)
    implementation_elements: list[str] = Field(default_factory=list, max_length=50)
    cautions: list[str] = Field(default_factory=list, max_length=30)
    completion_or_use: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def validate_steps(self) -> "SourceNativeArtifactPayload":
        if self.steps:
            expected = list(range(1, len(self.steps) + 1))
            actual = [step.order for step in self.steps]
            if actual != expected:
                raise ValueError("steps must use contiguous one-based ordering")
        return self


class SourceNativeUnitDecision(KBRecord):
    source_unit_id: str = Field(min_length=3, max_length=240)
    disposition: Disposition
    existing_relation: ExistingRelation
    related_existing_claim_ids: list[str] = Field(
        default_factory=list,
        max_length=100,
    )
    evidence_summary: str = Field(default="", max_length=1500)
    decision_reason: str = Field(min_length=10, max_length=1500)
    mixed_material: bool = False

    @field_validator("related_existing_claim_ids")
    @classmethod
    def validate_claim_ids(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("related_existing_claim_ids values must be unique")
        for value in values:
            if not value.startswith("claim:"):
                raise ValueError("related existing claim IDs must start with claim:")
        return values

    @model_validator(mode="after")
    def validate_split_disposition(self) -> "SourceNativeUnitDecision":
        if self.mixed_material != (self.disposition == "split_required"):
            raise ValueError(
                "mixed_material must be true exactly when disposition is split_required"
            )
        return self


class SourceNativeArtifactCandidate(KBRecord):
    artifact_key: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=120)
    artifact_type: ArtifactType
    source_unit_ids: list[str] = Field(min_length=1, max_length=100)
    title: str = Field(min_length=5, max_length=500)
    retrieval_text: str = Field(min_length=20, max_length=20_000)
    independent_question: str = Field(min_length=8, max_length=500)
    rationale: str = Field(min_length=10, max_length=1500)
    concept_ids: list[str] = Field(min_length=1, max_length=20)
    priority: Literal["high", "medium", "low"] = "medium"
    claim_type: Literal[
        "behavior",
        "configuration",
        "implementation_pattern",
        "release_caveat",
        "risk",
        "operational_guidance",
    ] | None = None
    evidence_class: Literal[
        "current_behavior",
        "demonstration",
        "partner_or_custom",
        "historical",
        "operational_recommendation",
        "exploratory_roadmap",
    ] | None = None
    temporal_status: Literal[
        "current",
        "release_sensitive",
        "exploratory",
        "unknown",
    ] = "current"
    rock_versions: list[str] = Field(default_factory=list, max_length=100)
    version_scope_status: Literal[
        "scoped",
        "version_independent",
        "unprocessed",
    ] = "unprocessed"
    confidence: Literal["high", "medium", "low"] = "medium"
    needs_live_verification: bool = False
    relation_to_existing: Literal[
        "novel",
        "adds_condition",
        "conflicts",
        "not_applicable",
    ] = "novel"
    related_existing_claim_ids: list[str] = Field(default_factory=list, max_length=100)
    payload: SourceNativeArtifactPayload

    @model_validator(mode="after")
    def validate_artifact_shape(self) -> "SourceNativeArtifactCandidate":
        for field_name in (
            "source_unit_ids",
            "concept_ids",
            "rock_versions",
            "related_existing_claim_ids",
        ):
            values = getattr(self, field_name)
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} values must be unique")
        if not self.independent_question.rstrip().endswith("?"):
            raise ValueError("independent_question must end with a question mark")
        if self.retrieval_text.count("?") > 0:
            raise ValueError("retrieval_text must state knowledge, not ask questions")
        if re.search(r"\b(?:step\s+1|1[.)]\s+.+2[.)]\s+)", self.retrieval_text, re.I):
            if self.artifact_type == "claim":
                raise ValueError("procedural text cannot be represented as a claim")
        if self.artifact_type == "claim":
            if not self.claim_type or not self.evidence_class:
                raise ValueError("claims require claim_type and evidence_class")
            if self.payload.steps or self.payload.reference_items:
                raise ValueError(
                    "claim payloads cannot shadow procedures or structured references"
                )
        elif self.claim_type is not None:
            raise ValueError("claim_type is valid only for claim artifacts")
        if self.artifact_type == "task_card" and len(self.payload.steps) < 2:
            raise ValueError("task cards require at least two ordered steps")
        if (
            self.artifact_type == "structured_reference"
            and not self.payload.reference_items
        ):
            raise ValueError("structured references require reference_items")
        if self.artifact_type == "recipe" and (
            len(self.payload.steps) + len(self.payload.implementation_elements) < 2
        ):
            raise ValueError(
                "recipes require multiple steps or implementation elements"
            )
        if self.version_scope_status == "scoped" and not self.rock_versions:
            raise ValueError("scoped artifacts require rock_versions")
        if self.version_scope_status != "scoped" and self.rock_versions:
            raise ValueError("rock_versions require version_scope_status=scoped")
        return self


class SourceNativeVerificationRequest(KBRecord):
    source_unit_ids: list[str] = Field(min_length=1, max_length=50)
    verification_surface: Literal[
        "public_source_code",
        "official_api",
        "read_only_instance",
        "maintainer_review",
    ]
    question: str = Field(min_length=10, max_length=1000)
    why_material: str = Field(min_length=10, max_length=1500)


class SourceNativeCoverageCheck(KBRecord):
    material_unit_count: int = Field(ge=0, le=200)
    captured_source_unit_ids: list[str] = Field(default_factory=list, max_length=200)
    no_artifact_source_unit_ids: list[str] = Field(default_factory=list, max_length=200)
    omitted_source_units: list["SourceNativeOmittedUnit"] = Field(
        default_factory=list,
        max_length=200,
    )


class SourceNativeOmittedUnit(KBRecord):
    source_unit_id: str = Field(min_length=3, max_length=240)
    reason: str = Field(min_length=10, max_length=1500)


class SourceNativeDistillationArticle(KBRecord):
    candidate_id: str = Field(min_length=3, max_length=240)
    source_input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    unit_decisions: list[SourceNativeUnitDecision] = Field(
        min_length=1,
        max_length=200,
    )
    artifacts: list[SourceNativeArtifactCandidate] = Field(
        default_factory=list,
        max_length=50,
    )
    verification_requests: list[SourceNativeVerificationRequest] = Field(
        default_factory=list,
        max_length=20,
    )
    unmatched_routing_terms: list[str] = Field(default_factory=list, max_length=3)
    review_notes: list[str] = Field(min_length=1, max_length=30)
    coverage_check: SourceNativeCoverageCheck

    @model_validator(mode="after")
    def validate_local_uniqueness(self) -> "SourceNativeDistillationArticle":
        unit_ids = [row.source_unit_id for row in self.unit_decisions]
        if len(unit_ids) != len(set(unit_ids)):
            raise ValueError("unit decisions must be unique by source_unit_id")
        artifact_keys = [row.artifact_key for row in self.artifacts]
        if len(artifact_keys) != len(set(artifact_keys)):
            raise ValueError("artifact_key values must be unique per article")
        questions = [
            " ".join(row.independent_question.lower().split())
            for row in self.artifacts
        ]
        if len(questions) != len(set(questions)):
            raise ValueError(
                "each artifact must answer a distinct independent question"
            )
        return self


class SourceNativeDistillationOutput(KBRecord):
    schema_: Literal["rock-kb-source-knowledge-distillation-v2.3"] = Field(
        alias="schema"
    )
    variant_id: Literal["source_knowledge_distillation_v2_3"]
    articles: list[SourceNativeDistillationArticle] = Field(
        min_length=1,
        max_length=50,
    )


class ReviewedSourceNativeArtifact(KBRecord):
    schema_: Literal["rock-kb-reviewed-source-native-artifact-v1"] = Field(
        alias="schema"
    )
    artifact_id: str = Field(min_length=3, max_length=240)
    source_candidate_id: str = Field(min_length=3, max_length=240)
    generation_activity_id: str = Field(min_length=3, max_length=240)
    artifact: SourceNativeArtifactCandidate
    review_state: Literal["reviewer_approved"]
    reviewer: str = Field(min_length=2, max_length=160)
    reviewed_at: str = Field(min_length=10, max_length=80)
    review_notes: list[str] = Field(default_factory=list, max_length=30)
    source_input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class SourceNativePilotManifest(KBRecord):
    schema_: Literal["rock-kb-source-native-pilot-manifest-v1"] = Field(
        alias="schema"
    )
    status: Literal["shadow_only"] = "shadow_only"
    public_retrieval_changed: Literal[False] = False
    prompt_id: Literal["source-knowledge-distillation-v2.3"]
    prompt_version: str = Field(min_length=1, max_length=80)
    concept_ids: list[str] = Field(min_length=1, max_length=20)
    source_snapshot_count: int = Field(ge=0)
    source_unit_count: int = Field(ge=0)
    generation_activity_count: int = Field(ge=0)
    reviewed_artifact_count: int = Field(ge=0)
    relationship_count: int = Field(ge=0)
    evaluation_case_count: int = Field(ge=0)
    file_hashes: dict[str, str] = Field(default_factory=dict)
    source_refresh_required_for_rebuild: bool = True
    notes: list[str] = Field(default_factory=list, max_length=30)


def public_payload(value: SourceNativeArtifactCandidate) -> dict[str, Any]:
    return value.public_dump()
