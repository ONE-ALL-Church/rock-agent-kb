from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml

from .jsonl import read_jsonl
from .paths import NORMALIZED_DIR

FULL_TEXT_ALLOWED = {
    "source_allowed_by_license",
    "structured_metadata",
}


def audit_license_records(paths: Optional[list[Path]] = None) -> list[str]:
    paths = paths or sorted(NORMALIZED_DIR.glob("*.jsonl"))
    errors: list[str] = []
    for path in paths:
        for record in read_jsonl(path):
            mode = record.get("allowed_extraction_mode") or record.get("extraction_mode")
            if not record.get("license_status"):
                errors.append(f"{path.name}:{record.get('id')} missing license_status")
            if record.get("full_text") and mode not in FULL_TEXT_ALLOWED:
                errors.append(f"{path.name}:{record.get('id')} stores full_text without full-text permission")
            if not record.get("citations"):
                errors.append(f"{path.name}:{record.get('id')} missing citations")
    return errors


def validate_markdown_frontmatter(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [f"{path} missing YAML frontmatter"]
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return [f"{path} has malformed YAML frontmatter"]
    data: dict[str, Any] = yaml.safe_load(frontmatter) or {}
    required = {"id", "source_ids", "license_status", "last_verified", "topics", "rock_versions", "agent_notes"}
    missing = sorted(required - set(data))
    return [f"{path} missing frontmatter fields: {', '.join(missing)}"] if missing else []
