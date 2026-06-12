from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from .base import KBRecord, Private


ClaimType = Literal[
    "behavior",
    "configuration",
    "implementation_pattern",
    "release_caveat",
    "risk",
    "recipe",
    "source_summary",
    "operational_guidance",
]
AuthorityTier = Literal[
    "official",
    "rocku-confirmed",
    "release-note-confirmed",
    "source-code-confirmed",
    "community-reviewed",
    "community-unreviewed",
    "agent-inference",
    "private-draft",
    "needs-live-verification",
]
ClaimTier = Literal[
    "source_backed",
    "answer_pack_approved",
    "live_verified",
    "routing_context_only",
]
ReviewStatus = Literal[
    "approved_for_public_distillation",
    "redaction_reviewed",
    "public_reviewed",
]
Confidence = Literal["low", "medium", "high", "needs_review"]
LicenseStatus = Literal["public", "cite_and_summarize_only", "manual_review_required", "private_only", "unknown"]
PublicPublishMode = Literal["public", "public_cite_and_summarize_only", "manual_review_required"]


class SourceRef(KBRecord):
    source_id: str | None = None
    url: str
    title: str | None = None
    timestamp: str | None = None
    timestamp_seconds: float | None = None
    source_timestamp_url: str | None = None


class PrivateCorpusPointer(KBRecord):
    kind: str
    media_id: str | None = None
    source_id: str | None = None


class LiveEvidenceRef(KBRecord):
    evidence_id: str | None = None
    probe_id: str | None = None
    path: str | None = Private(default=None)
    probe_type: str | None = None
    tables: list[str] = Field(default_factory=list)


class LiveVerification(KBRecord):
    instance: str | None = None
    verification_scope: str | None = None
    verified_at: str
    verified_by: str
    verification_method: str
    evidence_refs: list[LiveEvidenceRef] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_instance_or_scope(self) -> LiveVerification:
        if not self.instance and not self.verification_scope:
            raise ValueError("live_verification must include instance or verification_scope")
        return self


class Claim(KBRecord):
    schema_: Literal["rock-kb-claim-v1"] = Field(alias="schema")
    claim_id: str
    claim: str
    claim_type: ClaimType
    concept_ids: list[str]
    source_refs: list[SourceRef] = Field(default_factory=list)
    source_record_ids: list[str] = Field(default_factory=list)
    authority_tier: AuthorityTier
    confidence: Confidence
    review_status: ReviewStatus
    license_status: LicenseStatus
    public_publish_mode: PublicPublishMode
    rock_versions: list[str] = Field(default_factory=list)
    safe_evidence_hash: str
    needs_live_verification: bool
    created_at: str
    updated_at: str
    derived_from: dict[str, Any]
    community_derived: bool
    primary_concept_id: str
    secondary_concept_ids: list[str] = Field(default_factory=list)
    concept_assignment_reason: str
    answer_candidate: bool
    operational_priority: int
    requires_live_instance: bool
    common_failure_mode: list[str] = Field(default_factory=list)
    claim_tier: ClaimTier
    private_corpus_pointer: PrivateCorpusPointer | None = Private(default=None)
    timestamp: str | None = None
    timestamp_seconds: float | None = None
    source_timestamp_url: str | None = None
    live_verification: LiveVerification | None = None
    verification_notes: list[str] | None = None

    @model_validator(mode="after")
    def require_live_verification_for_live_verified(self) -> Claim:
        if self.claim_tier == "live_verified" and self.live_verification is None:
            raise ValueError("live_verified claim must include live_verification evidence")
        return self
