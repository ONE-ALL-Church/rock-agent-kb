from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from .base import KBRecord


class SourceNativeReviewAdjudication(KBRecord):
    recommendation_id: str = Field(min_length=3, max_length=240)
    disposition: Literal["accept", "modify", "reject"]
    rationale: str = Field(min_length=20, max_length=1500)
    evidence_refs: list[str] = Field(max_length=20)

    @field_validator("evidence_refs")
    @classmethod
    def validate_evidence_refs(cls, values: list[str]) -> list[str]:
        normalized = [str(value).strip() for value in values]
        if any(not value or len(value) > 500 for value in normalized):
            raise ValueError("evidence_refs must contain bounded non-empty values")
        if len(normalized) != len(set(normalized)):
            raise ValueError("evidence_refs must be unique")
        return normalized


class SourceNativeArticleReview(KBRecord):
    schema_: Literal["rock-kb-source-native-article-review-v1"] = Field(alias="schema")
    candidate_id: str = Field(min_length=3, max_length=240)
    source_record_id: str = Field(min_length=3, max_length=240)
    generated_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    reviewed_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    decision: Literal["approved", "approved_with_corrections"]
    reviewer: str = Field(min_length=2, max_length=160)
    reviewed_at: str = Field(min_length=10, max_length=80)
    notes: list[str] = Field(max_length=30)
    adjudications: list[SourceNativeReviewAdjudication] = Field(max_length=100)

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, values: list[str]) -> list[str]:
        normalized = [str(value).strip() for value in values]
        if any(not value or len(value) > 1500 for value in normalized):
            raise ValueError("notes must contain bounded non-empty values")
        return normalized

    @field_validator("adjudications")
    @classmethod
    def validate_unique_adjudications(
        cls,
        values: list[SourceNativeReviewAdjudication],
    ) -> list[SourceNativeReviewAdjudication]:
        ids = [value.recommendation_id for value in values]
        if len(ids) != len(set(ids)):
            raise ValueError("adjudication recommendation IDs must be unique")
        return values
