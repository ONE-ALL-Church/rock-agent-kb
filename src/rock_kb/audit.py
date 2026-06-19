from __future__ import annotations

from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlsplit, urlunsplit

import yaml

from .jsonl import read_jsonl
from .paths import NORMALIZED_DIR

FULL_TEXT_ALLOWED = {
    "source_allowed_by_license",
    "structured_metadata",
}

ALLOWED_DUPLICATE_SOURCE_URL_PAIRS = {
    ("public_rock_repos", "sparkdevnetwork_rock"),
    ("public_rock_repos", "sparkdevnetwork_slingshot"),
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


def audit_duplicate_source_urls(
    paths: Optional[list[Path]] = None,
    allowed_pairs: Optional[set[tuple[str, str]]] = None,
) -> list[str]:
    paths = paths or sorted(NORMALIZED_DIR.glob("*.jsonl"))
    allowed_pairs = allowed_pairs or ALLOWED_DUPLICATE_SOURCE_URL_PAIRS
    by_url: dict[str, set[str]] = {}
    for path in paths:
        for record in read_jsonl(path):
            source_id = str(record.get("source_id") or path.stem.removesuffix(".media-insights"))
            url = canonical_audit_url(str(record.get("source_url") or record.get("url") or ""))
            if not url:
                continue
            by_url.setdefault(url, set()).add(source_id)

    duplicate_counts: dict[tuple[str, str], int] = {}
    for source_ids in by_url.values():
        if len(source_ids) < 2:
            continue
        ordered = sorted(source_ids)
        for index, first in enumerate(ordered):
            for second in ordered[index + 1 :]:
                pair = tuple(sorted((first, second)))
                duplicate_counts[pair] = duplicate_counts.get(pair, 0) + 1

    errors: list[str] = []
    for pair, count in sorted(duplicate_counts.items()):
        if pair not in allowed_pairs:
            errors.append(f"duplicate source_url pair {pair[0]} vs {pair[1]}: {count}")
    return errors


def canonical_audit_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlsplit(url.strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


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
