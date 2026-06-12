from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import KBRecord


ContributionType = Literal[
    "task_card",
    "troubleshooting_pattern",
    "release_caveat",
    "entity_note",
    "guide_section",
    "source_link",
    "open_question",
]
ReviewStatus = Literal[
    "draft_private",
    "redaction_reviewed",
    "approved_for_public_distillation",
    "rejected_private",
    "needs_followup",
]
Confidence = Literal["low", "medium", "high", "needs_review"]

# Allowed review_status transitions. Promotion to a public bundle is only
# legal from a status marked promotable, and only with reviewed +
# redaction_attestation + license_attestation all true.
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "draft_private": {"needs_followup", "redaction_reviewed", "approved_for_public_distillation", "rejected_private"},
    "needs_followup": {"redaction_reviewed", "approved_for_public_distillation", "rejected_private"},
    "redaction_reviewed": {"approved_for_public_distillation", "needs_followup", "rejected_private"},
    "approved_for_public_distillation": {"redaction_reviewed", "needs_followup", "rejected_private"},
    "rejected_private": set(),
}
PROMOTABLE_STATUSES: frozenset[str] = frozenset({"redaction_reviewed", "approved_for_public_distillation"})


class ContributionRow(KBRecord):
    schema_: Literal["rock-kb-org-contribution-v1"] = Field(alias="schema")
    contribution_id: str
    org_id: str
    org_display_name: str | None = None
    contribution_type: ContributionType
    concept_ids: list[str] = Field(min_length=1)
    title: str | None = None
    distilled_summary: str
    source_urls: list[str] = Field(default_factory=list)
    source_record_ids: list[str] = Field(default_factory=list)
    confidence: Confidence
    review_status: ReviewStatus
    needs_live_verification: bool
    license_attestation: bool | str
    redaction_attestation: bool | str
    created_at: str | None = None
    publishability_status: str | None = None
    source_review_origin: str | None = None
    source_id: str | None = None
    source_private_contribution_id: str | None = None
    reviewer_notes: str | list[str] | None = None
