from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator, model_validator

from .base import KBRecord
from .source_native import SourceNativeDistillationArticle


class SourceNativeLegacyDecision(KBRecord):
    legacy_knowledge_unit_id: str = Field(min_length=3, max_length=240)
    legacy_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    disposition: Literal["replace", "retain"]
    coverage: Literal["full", "partial", "unsupported"]
    replacement_artifact_key: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        max_length=120,
    )
    supporting_replacement_artifact_keys: list[str] = Field(
        default_factory=list,
        max_length=30,
    )
    rationale: str = Field(min_length=20, max_length=1500)

    @model_validator(mode="after")
    def validate_disposition(self) -> SourceNativeLegacyDecision:
        if self.disposition == "replace":
            if self.coverage != "full" or not self.replacement_artifact_key:
                raise ValueError(
                    "replacement decisions require full coverage and an artifact key"
                )
        elif (
            self.replacement_artifact_key is not None
            or self.supporting_replacement_artifact_keys
        ):
            raise ValueError("retained legacy items cannot name replacement artifacts")
        if len(self.supporting_replacement_artifact_keys) != len(
            set(self.supporting_replacement_artifact_keys)
        ):
            raise ValueError("supporting replacement artifact keys must be unique")
        if self.replacement_artifact_key in self.supporting_replacement_artifact_keys:
            raise ValueError(
                "the primary replacement cannot also be a supporting replacement"
            )
        return self


class SourceNativeExistingArtifactDecision(KBRecord):
    existing_artifact_id: str = Field(min_length=3, max_length=240)
    existing_artifact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    disposition: Literal["retain_identity", "supersede"]
    replacement_artifact_key: str = Field(
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        max_length=120,
    )
    rationale: str = Field(min_length=20, max_length=1500)


class SourceNativeLegacyMigrationArticle(SourceNativeDistillationArticle):
    migration_input_hash_version: Literal["1", "2"] = "1"
    migration_input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    legacy_decisions: list[SourceNativeLegacyDecision] = Field(
        default_factory=list,
        max_length=100,
    )
    existing_artifact_decisions: list[SourceNativeExistingArtifactDecision] = Field(
        default_factory=list,
        max_length=100,
    )

    @field_validator("legacy_decisions")
    @classmethod
    def validate_unique_legacy_decisions(
        cls,
        values: list[SourceNativeLegacyDecision],
    ) -> list[SourceNativeLegacyDecision]:
        ids = [row.legacy_knowledge_unit_id for row in values]
        if len(ids) != len(set(ids)):
            raise ValueError(
                "legacy decisions must be unique by legacy_knowledge_unit_id"
            )
        return values

    @field_validator("existing_artifact_decisions")
    @classmethod
    def validate_unique_existing_artifact_decisions(
        cls,
        values: list[SourceNativeExistingArtifactDecision],
    ) -> list[SourceNativeExistingArtifactDecision]:
        ids = [row.existing_artifact_id for row in values]
        if len(ids) != len(set(ids)):
            raise ValueError(
                "existing artifact decisions must be unique by artifact ID"
            )
        return values


class SourceNativeLegacyMigrationOutput(KBRecord):
    schema_: Literal["rock-kb-source-native-legacy-migration-output-v1"] = Field(
        alias="schema"
    )
    variant_id: Literal["source_native_legacy_migration_v1"]
    articles: list[SourceNativeLegacyMigrationArticle] = Field(
        min_length=1,
        max_length=50,
    )


class SourceNativeLegacyReplacementRef(KBRecord):
    artifact_id: str = Field(min_length=3, max_length=240)
    artifact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class ReviewedSourceNativeLegacyMigration(KBRecord):
    schema_: Literal["rock-kb-reviewed-source-native-legacy-migration-v1"] = Field(
        alias="schema"
    )
    migration_id: str = Field(min_length=3, max_length=240)
    source_record_id: str = Field(min_length=3, max_length=240)
    source_snapshot_id: str = Field(min_length=3, max_length=240)
    source_snapshot_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    legacy_knowledge_unit_id: str = Field(min_length=3, max_length=240)
    legacy_result_ids: list[str] = Field(min_length=1, max_length=1000)
    legacy_knowledge_type: Literal["claim", "source_summary"]
    legacy_ingestion_mode: Literal[
        "legacy_reviewed_claim_projection",
        "legacy_summary_projection",
    ]
    legacy_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    migration_input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    migration_input_hash_version: Literal["1", "2"] = "1"
    replacement_artifact_id: str = Field(min_length=3, max_length=240)
    replacement_artifact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    supporting_replacement_artifacts: list[SourceNativeLegacyReplacementRef] = Field(
        default_factory=list, max_length=30
    )
    coverage: Literal["full"] = "full"
    rationale: str = Field(min_length=20, max_length=1500)
    generation_model: str = Field(min_length=1, max_length=160)
    generation_prompt_id: Literal["source-native-legacy-migration-v1"]
    generation_prompt_version: str = Field(min_length=1, max_length=80)
    generated_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    reviewed_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_correction_count: int = Field(ge=0)
    review_state: Literal["reviewer_approved"] = "reviewer_approved"
    reviewer: str = Field(min_length=2, max_length=160)
    reviewed_at: str = Field(min_length=10, max_length=80)

    @field_validator("legacy_result_ids")
    @classmethod
    def validate_legacy_result_ids(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("legacy_result_ids values must be unique")
        if any(not value.strip() for value in values):
            raise ValueError("legacy_result_ids cannot contain empty values")
        return values

    @model_validator(mode="after")
    def validate_legacy_shape(self) -> ReviewedSourceNativeLegacyMigration:
        expected_mode = {
            "claim": "legacy_reviewed_claim_projection",
            "source_summary": "legacy_summary_projection",
        }[self.legacy_knowledge_type]
        if self.legacy_ingestion_mode != expected_mode:
            raise ValueError(
                "legacy knowledge type and ingestion mode must describe the same row"
            )
        if self.legacy_knowledge_unit_id == self.replacement_artifact_id:
            raise ValueError("legacy migration must change the knowledge unit identity")
        supporting_ids = [
            row.artifact_id for row in self.supporting_replacement_artifacts
        ]
        if len(supporting_ids) != len(set(supporting_ids)):
            raise ValueError("supporting replacement artifact IDs must be unique")
        if self.replacement_artifact_id in supporting_ids:
            raise ValueError(
                "the primary replacement cannot also be a supporting replacement"
            )
        if self.legacy_knowledge_type == "claim" and supporting_ids:
            raise ValueError(
                "legacy claims require one independently complete replacement"
            )
        return self


class ReviewedSourceNativeArtifactMigration(KBRecord):
    schema_: Literal["rock-kb-reviewed-source-native-artifact-migration-v1"] = Field(
        alias="schema"
    )
    migration_id: str = Field(min_length=3, max_length=240)
    source_record_id: str = Field(min_length=3, max_length=240)
    source_snapshot_id: str = Field(min_length=3, max_length=240)
    source_snapshot_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    prior_artifact_id: str = Field(min_length=3, max_length=240)
    prior_artifact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    replacement_artifact_id: str = Field(min_length=3, max_length=240)
    replacement_artifact_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    migration_input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    migration_input_hash_version: Literal["1", "2"] = "1"
    rationale: str = Field(min_length=20, max_length=1500)
    generation_model: str = Field(min_length=1, max_length=160)
    generation_prompt_id: Literal["source-native-legacy-migration-v1"]
    generation_prompt_version: str = Field(min_length=1, max_length=80)
    generated_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    reviewed_article_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_correction_count: int = Field(ge=0)
    review_state: Literal["reviewer_approved"] = "reviewer_approved"
    reviewer: str = Field(min_length=2, max_length=160)
    reviewed_at: str = Field(min_length=10, max_length=80)

    @model_validator(mode="after")
    def validate_artifact_migration(self) -> ReviewedSourceNativeArtifactMigration:
        if self.prior_artifact_id == self.replacement_artifact_id:
            raise ValueError("artifact migrations must change the public artifact ID")
        return self
