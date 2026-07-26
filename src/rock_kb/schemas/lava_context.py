from __future__ import annotations

import re
from typing import Literal

from pydantic import Field, field_validator, model_validator

from .base import KBRecord


SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
SAFE_RELATIVE_PATH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/ -]{0,255}$")


class LavaContextExtensionRoot(KBRecord):
    root_key: str = Field(min_length=1, max_length=128)
    root_type: str = Field(min_length=1, max_length=256)
    value_kind: Literal["object", "collection", "scalar", "scalar_collection", "dictionary", "dynamic", "unknown"]
    model_slug: str | None = Field(default=None, max_length=128)
    nested_path: str = Field(default="", max_length=256)
    availability_condition: str = Field(min_length=3, max_length=500)
    may_be_null: bool = False
    required_setting: str = Field(default="", max_length=256)
    execution_phase: str = Field(default="render", min_length=1, max_length=64)
    notes: str = Field(default="", max_length=1000)
    source_path: str
    source_symbol: str = Field(min_length=1, max_length=256)
    source_line_start: int = Field(ge=1)
    source_line_end: int = Field(ge=1)
    needs_live_verification: bool = True

    @field_validator("source_path")
    @classmethod
    def validate_source_path(cls, value: str) -> str:
        normalized = value.replace("\\", "/").strip()
        if (
            not SAFE_RELATIVE_PATH.fullmatch(normalized)
            or normalized.startswith("/")
            or ".." in normalized.split("/")
            or normalized.startswith(("data/", "private/", ".git/"))
        ):
            raise ValueError("source_path must be a public-safe relative repository path")
        return normalized

    @model_validator(mode="after")
    def validate_lines(self) -> "LavaContextExtensionRoot":
        if self.source_line_end < self.source_line_start:
            raise ValueError("source_line_end must be greater than or equal to source_line_start")
        return self


class LavaContextExtensionContext(KBRecord):
    context_id: str
    context_family: str = Field(min_length=1, max_length=64)
    surface_name: str = Field(min_length=1, max_length=200)
    surface_type: str = Field(min_length=1, max_length=128)
    concept_ids: list[str] = Field(min_length=1, max_length=20)
    includes_context_ids: list[str] = Field(default_factory=list, max_length=20)
    availability_condition: str = Field(min_length=3, max_length=500)
    coverage_status: Literal["complete_for_source_snapshot", "reviewed_curated", "partial_curated", "dynamic"]
    roots: list[LavaContextExtensionRoot] = Field(min_length=1, max_length=500)

    @field_validator("context_id")
    @classmethod
    def validate_context_id(cls, value: str) -> str:
        if not SAFE_ID.fullmatch(value):
            raise ValueError("context_id must be a stable lowercase public identifier")
        return value


class LavaContextExtensionManifest(KBRecord):
    schema_: Literal["rock-kb-lava-context-extension-v1"] = Field(alias="schema")
    extension_id: str
    org_id: str
    title: str = Field(min_length=3, max_length=200)
    repository_url: str
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    source_version: str = Field(default="", max_length=64)
    license: str = Field(min_length=1, max_length=100)
    license_url: str
    license_attestation: Literal[True]
    redaction_attestation: Literal[True]
    review_status: Literal["community_reviewed"]
    contexts: list[LavaContextExtensionContext] = Field(min_length=1, max_length=200)

    @field_validator("extension_id", "org_id")
    @classmethod
    def validate_ids(cls, value: str) -> str:
        if not SAFE_ID.fullmatch(value):
            raise ValueError("extension and organization identifiers must be stable lowercase public identifiers")
        return value

    @field_validator("repository_url", "license_url")
    @classmethod
    def validate_public_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("public extension URLs must use https")
        return value

    @field_validator("repository_url")
    @classmethod
    def validate_github_repository_url(cls, value: str) -> str:
        normalized = value.rstrip("/").removesuffix(".git")
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", normalized):
            raise ValueError("repository_url must identify a public GitHub repository root")
        return normalized

    @model_validator(mode="after")
    def validate_context_namespace(self) -> "LavaContextExtensionManifest":
        prefix = f"{self.org_id}:"
        if any(not context.context_id.startswith(prefix) for context in self.contexts):
            raise ValueError(f"extension context_id values must start with {prefix}")
        return self
