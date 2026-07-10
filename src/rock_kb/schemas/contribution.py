from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .base import KBRecord
from .recipe import RecipeRow


ContributionType = Literal[
    "task_card",
    "troubleshooting_pattern",
    "release_caveat",
    "entity_note",
    "guide_section",
    "source_link",
    "open_question",
    "recipe",
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
    recipe: RecipeRow | None = None

    @model_validator(mode="after")
    def validate_recipe_payload(self) -> "ContributionRow":
        if self.contribution_type == "recipe" and self.recipe is None:
            raise ValueError("recipe contribution requires a recipe payload")
        if self.contribution_type != "recipe" and self.recipe is not None:
            raise ValueError("recipe payload is only valid for recipe contributions")
        if self.recipe and (self.recipe.org_id != self.org_id or self.recipe.recipe_id != self.contribution_id):
            raise ValueError("recipe org_id and recipe_id must match the contribution")
        return self
