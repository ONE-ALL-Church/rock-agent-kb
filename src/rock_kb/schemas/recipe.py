from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import KBRecord


class RecipeFile(KBRecord):
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    purpose: str


class RecipeImplementation(KBRecord):
    repository_url: str
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    source_path: str
    manifest_url: str
    license: str
    license_url: str
    owner: str
    ingestion_mode: Literal["link_only", "index_documentation", "snapshot_source"]
    files: list[RecipeFile] = Field(min_length=1)


class RecipeCompatibility(KBRecord):
    tested_rock_versions: list[str] = Field(default_factory=list)
    minimum_rock_version: str | None = None
    maximum_rock_version: str | None = None
    last_verified_at: str | None = None
    notes: list[str] = Field(default_factory=list)
    version_matrix: list["RecipeVersionCompatibility"] = Field(default_factory=list)


class RecipeVersionCompatibility(KBRecord):
    rock_version: str
    status: Literal["verified", "expected", "unsupported"]
    notes: list[str] = Field(default_factory=list)


class RecipeVerificationAttestation(KBRecord):
    org_id: str
    rock_version: str
    verified_at: str
    outcome: Literal["pass", "partial", "fail"]
    scope: Literal["source_pattern_review", "package_static_validation", "nonproduction_test", "production_adaptation"]
    evidence_url: str | None = None
    notes: list[str] = Field(default_factory=list)


class RecipeRelease(KBRecord):
    version: str
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    released_at: str
    notes: list[str] = Field(default_factory=list)


class RecipeSecurity(KBRecord):
    data_access: Literal["read_only", "writes"]
    authentication: str
    authorization: str
    csrf_required: bool
    handles_sensitive_data: bool
    notes: list[str] = Field(default_factory=list)


class RecipeAdaptationPoint(KBRecord):
    key: str
    description: str
    required: bool = True
    example: str | None = None
    sensitive: bool = False


class RecipeRow(KBRecord):
    schema_: Literal["rock-kb-recipe-v1"] = Field(alias="schema")
    recipe_id: str
    org_id: str
    title: str
    summary: str
    version: str
    status: Literal["active", "deprecated", "experimental"] = "active"
    recipe_kind: Literal[
        "lava_application",
        "workflow",
        "sql_report",
        "integration",
        "block_configuration",
        "automation",
        "other",
    ]
    difficulty: Literal["beginner", "intermediate", "advanced"]
    audience: list[str] = Field(min_length=1)
    concept_ids: list[str] = Field(min_length=1)
    supersedes_contribution_ids: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(min_length=1)
    outcomes: list[str] = Field(min_length=1)
    prerequisites: list[str] = Field(default_factory=list)
    adaptation_points: list[RecipeAdaptationPoint] = Field(default_factory=list)
    security: RecipeSecurity
    compatibility: RecipeCompatibility
    implementation: RecipeImplementation
    instructions: list[str] = Field(min_length=1)
    validation_steps: list[str] = Field(min_length=1)
    rollback_steps: list[str] = Field(default_factory=list)
    known_limitations: list[str] = Field(default_factory=list)
    learnings: list[str] = Field(min_length=1)
    evidence_urls: list[str] = Field(default_factory=list)
    feedback_url: str | None = None
    release_history: list[RecipeRelease] = Field(default_factory=list)
    verification_attestations: list[RecipeVerificationAttestation] = Field(default_factory=list)
    needs_live_verification: bool = True
    review_status: Literal["community_unreviewed", "community_reviewed"]
    authority_tier: Literal["community-unreviewed", "community-reviewed"]
    created_at: str
    updated_at: str
