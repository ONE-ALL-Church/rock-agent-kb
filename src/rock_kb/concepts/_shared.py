from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml

from ..claims import approved_claim_dependencies_for_concept
from ..contribution_sources import public_contribution_records
from ..extract import generated_at_iso, grep_sensitive_values, now_iso, sha256_text
from ..indexes import all_normalized_records, escape_table_cell, public_agent_records
from ..jsonl import read_jsonl, write_jsonl
from ..lava_capabilities import LAVA_SOURCE_ID, should_attach_lava_dependency
from ..paths import AGENT_DIR, CLAIMS_DIR, CONCEPTS_DIR, KNOWLEDGE_DIR, MEDIA_DIR, REPO_ROOT
from ..private_dependencies import private_impacts_by_concept

PUBLIC_MEDIA_REVIEW_STATUSES = {"redaction_reviewed", "approved_for_public_distillation", "public_reviewed"}
APPROVED_CLAIMS_SECTION_START = "<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->"
APPROVED_CLAIMS_SECTION_END = "<!-- END GENERATED APPROVED CLAIM COVERAGE -->"
MODEL_MAP_POINTER_SECTION_START = "<!-- BEGIN GENERATED MODEL MAP POINTERS -->"
MODEL_MAP_POINTER_SECTION_END = "<!-- END GENERATED MODEL MAP POINTERS -->"


def repo_relative_path(path: Path | str) -> str:
    path = Path(path)
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()

REQUIRED_AGENT_ENTRYPOINT_FILES = [
    "quickstart.md",
    "approved-claims.md",
    "approved-media.md",
    "task-cards.jsonl",
    "entities.jsonl",
    "release-caveats.jsonl",
    "section-source-map.jsonl",
    "section-status.jsonl",
    "troubleshooting-tree.json",
    "open-questions.md",
]

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def upsert_agent_jsonl(path: Path, rows: list[dict[str, Any]], concept_id: str) -> None:
    existing = [row for row in read_jsonl(path) if row.get("concept_id") != concept_id] if path.exists() else []
    write_jsonl(path, existing + rows)

def relative_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return relative_path(path)

def relative_path(path: Path) -> str:
    try:
        return path.relative_to(KNOWLEDGE_DIR.parents[0]).as_posix()
    except ValueError:
        return str(path)

def count_jsonl(path: Path) -> int:
    return sum(1 for _ in read_jsonl(path)) if path.exists() else 0

def compact_unique(values: Iterable[Any]) -> list[Any]:
    output = []
    seen = set()
    for value in values:
        if value in (None, "", [], {}):
            continue
        key = json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
        if key in seen:
            continue
        seen.add(key)
        output.append(value)
    return output

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"

def count_words(value: str) -> int:
    return len(re.findall(r"\b\w+\b", value))
