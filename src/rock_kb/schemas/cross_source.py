from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from .base import KBRecord
from .knowledge import SourceSnapshot, SourceUnit


class ReviewedCrossSourceEvidence(KBRecord):
    schema_: Literal["reviewed-cross-source-evidence"] = Field(alias="schema")
    source_snapshot: SourceSnapshot
    source_unit: SourceUnit
    relation: Literal[
        "supports",
        "qualifies",
        "contradicts",
        "supersedes",
        "derived_from",
        "reports",
        "demonstrates",
    ]
    evidence_summary: str = Field(min_length=10, max_length=1500)
    authority_tier: str = Field(min_length=1, max_length=80)
    confidence: Literal["low", "medium", "high", "needs_review"] = "medium"
    independence_group: str = Field(min_length=3, max_length=240)
    needs_review: bool = False

    @model_validator(mode="after")
    def validate_source_alignment(self) -> "ReviewedCrossSourceEvidence":
        if (
            self.source_unit.source_snapshot_id
            != self.source_snapshot.source_snapshot_id
        ):
            raise ValueError(
                "source_unit must reference its embedded source_snapshot"
            )
        if self.source_unit.text is not None:
            raise ValueError(
                "reviewed cross-source evidence cannot contain private source text"
            )
        if not self.source_unit.public_summary:
            raise ValueError(
                "reviewed cross-source evidence requires a public summary"
            )
        if self.authority_tier != self.source_snapshot.authority_tier:
            raise ValueError(
                "evidence authority_tier must match its source snapshot"
            )
        if self.source_snapshot.public_policy in {
            "private_evidence_only",
            "manual_review_required",
        }:
            raise ValueError(
                "reviewed cross-source evidence must be public-exportable"
            )
        return self


class ReviewedCrossSourceRelationship(KBRecord):
    schema_: Literal["reviewed-cross-source-relationship"] = Field(
        alias="schema"
    )
    target_id: str = Field(min_length=3, max_length=240)
    relation: Literal[
        "related_to",
        "corroborates",
        "contradicts",
        "qualifies",
        "supersedes",
        "implements",
        "affects",
        "affects_model",
        "affects_version",
        "applies_to",
        "requires",
        "workaround_for",
        "references",
    ]
    rationale: str = Field(min_length=10, max_length=1500)
    evidence_source_unit_ids: list[str] = Field(
        default_factory=list,
        max_length=100,
    )
    confidence: Literal["low", "medium", "high", "needs_review"] = "medium"

    @field_validator("evidence_source_unit_ids")
    @classmethod
    def validate_unique_evidence(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("evidence_source_unit_ids values must be unique")
        return values


class ReviewedCrossSourceEvaluation(KBRecord):
    schema_: Literal["reviewed-cross-source-evaluation"] = Field(
        alias="schema"
    )
    evaluation_id: str = Field(
        pattern=r"^[a-z0-9]+(?:[-:][a-z0-9]+)*$",
        max_length=200,
    )
    question: str = Field(min_length=8, max_length=500)
    query_type: Literal["exact", "paraphrase"]
    concept_id: str = Field(min_length=1, max_length=160)
    max_rank: int = Field(default=3, ge=1, le=20)
    required_terms: list[str] = Field(default_factory=list, max_length=20)
    required_authority_tiers: list[str] = Field(
        default_factory=list,
        max_length=10,
    )

    @field_validator("required_terms", "required_authority_tiers")
    @classmethod
    def validate_unique_values(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("evaluation list values must be unique")
        return values


class ReviewedCrossSourceArtifact(KBRecord):
    schema_: Literal["rock-kb-reviewed-cross-source-artifact-v1"] = Field(
        alias="schema"
    )
    knowledge_unit_id: str = Field(
        pattern=r"^cross-source:[a-z0-9]+(?:[-:][a-z0-9]+)*$",
        max_length=240,
    )
    knowledge_type: Literal[
        "claim",
        "task_card",
        "structured_reference",
        "troubleshooting_node",
        "source_summary",
    ]
    title: str = Field(min_length=5, max_length=500)
    retrieval_text: str = Field(min_length=20, max_length=20_000)
    concept_ids: list[str] = Field(min_length=1, max_length=20)
    topic_ids: list[str] = Field(default_factory=list, max_length=30)
    claim_tier: Literal[
        "source_backed",
        "answer_pack_approved",
        "live_verified",
    ] = "source_backed"
    review_state: Literal["reviewer_approved"] = "reviewer_approved"
    rock_versions: list[str] = Field(default_factory=list, max_length=100)
    version_scope_status: Literal[
        "scoped",
        "version_independent",
        "unprocessed",
    ]
    temporal_status: Literal[
        "current",
        "release_sensitive",
        "historical",
        "unknown",
    ]
    source_evidence: list[ReviewedCrossSourceEvidence] = Field(
        min_length=2,
        max_length=20,
    )
    relationships: list[ReviewedCrossSourceRelationship] = Field(
        default_factory=list,
        max_length=30,
    )
    evaluations: list[ReviewedCrossSourceEvaluation] = Field(
        min_length=2,
        max_length=20,
    )
    payload: dict[str, Any]
    generation_model: str = Field(min_length=2, max_length=160)
    generation_prompt_id: str = Field(min_length=2, max_length=160)
    generation_prompt_version: str = Field(min_length=1, max_length=80)
    reviewer: str = Field(min_length=2, max_length=160)
    reviewed_at: str = Field(min_length=10, max_length=80)
    review_rationale: str = Field(min_length=20, max_length=2000)

    @model_validator(mode="after")
    def validate_reviewed_artifact(self) -> "ReviewedCrossSourceArtifact":
        for field_name in ("concept_ids", "topic_ids", "rock_versions"):
            values = getattr(self, field_name)
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} values must be unique")
        if not self.retrieval_text.rstrip().endswith((".", "!")):
            raise ValueError(
                "retrieval_text must be a complete declarative sentence"
            )
        if self.version_scope_status == "scoped" and not self.rock_versions:
            raise ValueError("scoped artifacts require rock_versions")
        if self.version_scope_status != "scoped" and self.rock_versions:
            raise ValueError(
                "rock_versions require version_scope_status=scoped"
            )
        source_unit_ids = [
            row.source_unit.source_unit_id
            for row in self.source_evidence
        ]
        if len(source_unit_ids) != len(set(source_unit_ids)):
            raise ValueError("cross-source evidence units must be unique")
        source_ids = {
            row.source_snapshot.source_id
            for row in self.source_evidence
        }
        if len(source_ids) < 2:
            raise ValueError(
                "cross-source artifacts require at least two distinct sources"
            )
        evidence_id_set = set(source_unit_ids)
        relationship_keys: set[tuple[str, str]] = set()
        for relationship in self.relationships:
            missing = (
                set(relationship.evidence_source_unit_ids)
                - evidence_id_set
            )
            if missing:
                raise ValueError(
                    "relationships reference unknown evidence source units"
                )
            key = (relationship.relation, relationship.target_id)
            if key in relationship_keys:
                raise ValueError(
                    "cross-source relationships must be unique"
                )
            relationship_keys.add(key)
        evaluation_ids = [row.evaluation_id for row in self.evaluations]
        questions = [
            " ".join(row.question.lower().split())
            for row in self.evaluations
        ]
        if len(evaluation_ids) != len(set(evaluation_ids)):
            raise ValueError("evaluation IDs must be unique")
        if len(questions) != len(set(questions)):
            raise ValueError("evaluation questions must be distinct")
        query_types = {row.query_type for row in self.evaluations}
        if query_types != {"exact", "paraphrase"}:
            raise ValueError(
                "cross-source evaluations must cover exact and paraphrase"
            )
        return self


class ReviewedCrossSourceManifest(KBRecord):
    schema_: Literal["rock-kb-reviewed-cross-source-manifest-v1"] = Field(
        alias="schema"
    )
    status: Literal["shadow_only"] = "shadow_only"
    public_retrieval_changed: Literal[False] = False
    artifact_count: int = Field(ge=0)
    source_snapshot_count: int = Field(ge=0)
    source_unit_count: int = Field(ge=0)
    generation_activity_count: int = Field(ge=0)
    evidence_link_count: int = Field(ge=0)
    relationship_count: int = Field(ge=0)
    evaluation_case_count: int = Field(ge=0)
    file_hashes: dict[str, str]
    notes: list[str] = Field(default_factory=list, max_length=30)
