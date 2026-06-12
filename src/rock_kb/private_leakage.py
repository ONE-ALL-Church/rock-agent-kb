from __future__ import annotations

import json
from typing import Any

from .extract import grep_sensitive_values

PRIVATE_FIELD_NAMES = {
    "raw_text",
    "full_text",
    "content",
    "html",
    "markdown",
    "transcript",
    "media_url",
    "private_path",
    "private_source_paths",
    "private_corpus_pointer",
}
PRIVATE_PATH_PREFIXES = (
    "data/review/",
    "data/media/",
    "data/normalized/",
    "data/raw-manifests/",
    "data/index/",
)
DIRECT_MEDIA_URL_HINTS = (
    ".mp3",
    ".mp4",
    ".m3u8",
    ".mpd",
    "player.vimeo.com",
    "oauth2_token_id=",
    "access_token=",
    "signature=",
)


def find_leaks(row: dict[str, Any]) -> list[str]:
    """Return public-boundary violations for a JSON-like row."""
    errors: list[str] = []
    for field_path in prohibited_public_field_paths(row):
        errors.append(f"contains prohibited public field: {field_path}")
    serialized = json.dumps(row, ensure_ascii=False)
    for finding in grep_sensitive_values(serialized.splitlines()):
        errors.append(f"contains sensitive-looking value: {finding[:120]}")
    for path, value in string_values(row):
        if direct_or_tokenized_media_url(value):
            errors.append(f"contains direct/tokenized media URL at {path}: {value[:120]}")
        if private_path_reference(value):
            errors.append(f"contains private path reference at {path}: {value[:120]}")
    if raw_transcript_marker(str(row.get("claim") or "")):
        errors.append("claim looks like raw transcript text")
    return errors


def direct_or_tokenized_media_url(url: str) -> bool:
    lowered = str(url).lower()
    return any(hint in lowered for hint in DIRECT_MEDIA_URL_HINTS)


def private_path_reference(value: str) -> bool:
    normalized = str(value).replace("\\", "/")
    return any(prefix in normalized for prefix in PRIVATE_PATH_PREFIXES)


def prohibited_public_field_paths(value: Any, prefix: str = "$") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}"
            if key in PRIVATE_FIELD_NAMES:
                paths.append(path)
            paths.extend(prohibited_public_field_paths(nested, path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            paths.extend(prohibited_public_field_paths(nested, f"{prefix}[{index}]"))
    return paths


def raw_transcript_marker(text: str) -> bool:
    lowered = " ".join(text.lower().split())
    return lowered.startswith("speaker ") or " transcript " in lowered[:120]


def string_values(value: Any, prefix: str = "$") -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            values.extend(string_values(nested, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            values.extend(string_values(nested, f"{prefix}[{index}]"))
    elif isinstance(value, str):
        values.append((prefix, value))
    return values
