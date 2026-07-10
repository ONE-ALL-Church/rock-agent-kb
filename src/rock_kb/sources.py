from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml

from .paths import SOURCES_DIR

REQUIRED_SOURCE_FIELDS = {
    "id",
    "name",
    "kind",
    "root_url",
    "description",
    "owner",
    "license_status",
    "allowed_extraction_mode",
    "private_storage",
    "public_publish_mode",
    "allowed_excerpt_chars",
    "requires_human_review",
    "refresh_cadence",
    "extraction_tier",
    "preferred_tooling",
    "topics",
}

ALLOWED_EXTRACTION_MODES = {
    "cite_and_summarize",
    "structured_metadata",
    "source_allowed_by_license",
    "metadata_then_license_gate",
    "reviewed_summaries_only",
}

ALLOWED_PUBLIC_PUBLISH_MODES = {
    "public_full_text_allowed",
    "public_excerpt_only",
    "public_cite_and_summarize_only",
    "private_only",
    "manual_review_required",
}

ALLOWED_REFRESH_CADENCES = {"daily", "weekly", "monthly", "manual"}


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    kind: str
    root_url: str
    description: str
    owner: str
    license_status: str
    allowed_extraction_mode: str
    private_storage: bool
    public_publish_mode: str
    allowed_excerpt_chars: int
    requires_human_review: bool
    refresh_cadence: str
    extraction_tier: int
    preferred_tooling: list[str]
    topics: list[str]
    raw: dict[str, Any]

    @property
    def permits_full_text(self) -> bool:
        return self.allowed_extraction_mode in {
            "source_allowed_by_license",
            "structured_metadata",
        }

    @property
    def permits_public_full_text(self) -> bool:
        return self.public_publish_mode == "public_full_text_allowed"


def registry_path() -> Path:
    return SOURCES_DIR / "registry.yaml"


def load_registry(path: Optional[Path] = None) -> dict[str, Any]:
    path = path or registry_path()
    with path.open("r", encoding="utf-8") as handle:
        registry = yaml.safe_load(handle) or {}
    if not isinstance(registry, dict):
        raise ValueError("Registry root must be a mapping.")
    return registry


def load_sources(path: Optional[Path] = None) -> list[Source]:
    registry = load_registry(path)
    defaults = registry.get("defaults", {})
    sources = []
    for item in registry.get("sources", []):
        merged = {**defaults, **item}
        sources.append(
            Source(
                id=str(merged["id"]),
                name=str(merged["name"]),
                kind=str(merged["kind"]),
                root_url=str(merged["root_url"]),
                description=str(merged["description"]),
                owner=str(merged["owner"]),
                license_status=str(merged["license_status"]),
                allowed_extraction_mode=str(merged["allowed_extraction_mode"]),
                private_storage=bool(merged["private_storage"]),
                public_publish_mode=str(merged["public_publish_mode"]),
                allowed_excerpt_chars=int(merged["allowed_excerpt_chars"]),
                requires_human_review=bool(merged["requires_human_review"]),
                refresh_cadence=str(merged["refresh_cadence"]),
                extraction_tier=int(merged["extraction_tier"]),
                preferred_tooling=list(merged["preferred_tooling"]),
                topics=list(merged["topics"]),
                raw=merged,
            )
        )
    return sources


def get_source(source_id: str) -> Source:
    for source in load_sources():
        if source.id == source_id:
            return source
    raise KeyError(f"Unknown source id: {source_id}")


def validate_registry(path: Optional[Path] = None) -> list[str]:
    registry = load_registry(path)
    errors: list[str] = []
    ids: set[str] = set()
    sources = registry.get("sources", [])
    if not isinstance(sources, list) or not sources:
        errors.append("Registry must contain at least one source.")
        return errors
    defaults = registry.get("defaults", {})
    for index, item in enumerate(sources):
        if not isinstance(item, dict):
            errors.append(f"sources[{index}] must be a mapping.")
            continue
        merged = {**defaults, **item}
        missing = sorted(REQUIRED_SOURCE_FIELDS - set(merged))
        if missing:
            errors.append(f"{item.get('id', f'sources[{index}]')} missing fields: {', '.join(missing)}")
            continue
        source_id = str(merged["id"])
        if source_id in ids:
            errors.append(f"Duplicate source id: {source_id}")
        ids.add(source_id)
        if merged["allowed_extraction_mode"] not in ALLOWED_EXTRACTION_MODES:
            errors.append(f"{source_id} has invalid allowed_extraction_mode.")
        if merged["public_publish_mode"] not in ALLOWED_PUBLIC_PUBLISH_MODES:
            errors.append(f"{source_id} has invalid public_publish_mode.")
        if merged["refresh_cadence"] not in ALLOWED_REFRESH_CADENCES:
            errors.append(f"{source_id} has invalid refresh_cadence.")
        try:
            excerpt_chars = int(merged["allowed_excerpt_chars"])
        except (TypeError, ValueError):
            errors.append(f"{source_id} allowed_excerpt_chars must be an integer.")
            excerpt_chars = -1
        if excerpt_chars < 0:
            errors.append(f"{source_id} allowed_excerpt_chars must be non-negative.")
        if not isinstance(merged["private_storage"], bool):
            errors.append(f"{source_id} private_storage must be true or false.")
        if not isinstance(merged["requires_human_review"], bool):
            errors.append(f"{source_id} requires_human_review must be true or false.")
        try:
            tier = int(merged["extraction_tier"])
        except (TypeError, ValueError):
            errors.append(f"{source_id} extraction_tier must be an integer.")
            continue
        if tier not in (1, 2, 3, 4):
            errors.append(f"{source_id} extraction_tier must be 1, 2, 3, or 4.")
        if not isinstance(merged["preferred_tooling"], list) or not merged["preferred_tooling"]:
            errors.append(f"{source_id} preferred_tooling must be a non-empty list.")
        if not isinstance(merged["topics"], list) or not merged["topics"]:
            errors.append(f"{source_id} topics must be a non-empty list.")
    return errors
