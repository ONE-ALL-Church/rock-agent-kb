from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

SCHEMA = "rock-kb-org-contribution-v1"
CONTRIBUTION_TYPES = {
    "task_card",
    "troubleshooting_pattern",
    "release_caveat",
    "entity_note",
    "guide_section",
    "source_link",
    "open_question",
}
PUBLIC_REVIEW_STATUSES = {"redaction_reviewed", "approved_for_public_distillation"}
CONFIDENCE_VALUES = {"low", "medium", "high", "needs_review"}
REQUIRED_FIELDS = {
    "schema",
    "contribution_id",
    "org_id",
    "concept_ids",
    "contribution_type",
    "title",
    "distilled_summary",
    "source_urls",
    "source_record_ids",
    "redaction_attestation",
    "review_status",
    "license_attestation",
    "confidence",
    "needs_live_verification",
}
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
SENSITIVE_PATTERNS = (
    re.compile(r"(?i)(?:^|[^A-Za-z0-9_-])(password|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}(?![A-Za-z0-9_-])"),
    re.compile(r"(?i)connectionstring\s*[:=]"),
)


def validate_bundle(path: Path) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        label = f"{path}:{line_number}"
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label} invalid JSONL: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{label} row must be an object")
            continue
        errors.extend(validate_row(row, label))
    return errors


def validate_row(row: dict, label: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if field not in row or row.get(field) is None)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if row.get("schema") != SCHEMA:
        errors.append(f"{label} schema must be {SCHEMA}")
    if row.get("contribution_type") not in CONTRIBUTION_TYPES:
        errors.append(f"{label} invalid contribution_type")
    if row.get("review_status") not in PUBLIC_REVIEW_STATUSES:
        errors.append(f"{label} public contribution must be redaction_reviewed or approved_for_public_distillation")
    if row.get("confidence") not in CONFIDENCE_VALUES:
        errors.append(f"{label} invalid confidence")
    if not isinstance(row.get("needs_live_verification"), bool):
        errors.append(f"{label} needs_live_verification must be true or false")
    if not isinstance(row.get("concept_ids"), list) or not row.get("concept_ids"):
        errors.append(f"{label} concept_ids must be a non-empty list")
    if not isinstance(row.get("source_urls"), list):
        errors.append(f"{label} source_urls must be a list")
    if not isinstance(row.get("source_record_ids"), list):
        errors.append(f"{label} source_record_ids must be a list")
    if not row.get("source_urls") and not row.get("source_record_ids"):
        errors.append(f"{label} must include source_urls or source_record_ids")
    for url in row.get("source_urls") or []:
        if not isinstance(url, str):
            errors.append(f"{label} source_urls must contain strings")
        elif url and urlparse(url).scheme and urlparse(url).scheme not in {"http", "https"}:
            errors.append(f"{label} source_urls must use http or https URLs")
    if not truthy_attestation(row.get("redaction_attestation")):
        errors.append(f"{label} redaction_attestation must be true or an affirmative string")
    if not truthy_attestation(row.get("license_attestation")):
        errors.append(f"{label} license_attestation must be true or an affirmative string")
    errors.extend(f"{label} {message}" for message in find_leaks(row))
    return errors


def find_leaks(row: dict) -> list[str]:
    errors: list[str] = []
    for field_path in prohibited_public_field_paths(row):
        errors.append(f"contains prohibited public field: {field_path}")
    serialized = json.dumps(row, ensure_ascii=False)
    for line in serialized.splitlines():
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                errors.append(f"contains sensitive-looking value: {line.strip()[:120]}")
                break
    for path, value in string_values(row):
        lowered = value.lower()
        if any(hint in lowered for hint in DIRECT_MEDIA_URL_HINTS):
            errors.append(f"contains direct/tokenized media URL at {path}: {value[:120]}")
        normalized = value.replace("\\", "/")
        if any(prefix in normalized for prefix in PRIVATE_PATH_PREFIXES):
            errors.append(f"contains private path reference at {path}: {value[:120]}")
    return errors


def prohibited_public_field_paths(value, prefix: str = "$") -> list[str]:
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


def string_values(value, prefix: str = "$") -> list[tuple[str, str]]:
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


def truthy_attestation(value) -> bool:
    if value is True:
        return True
    return isinstance(value, str) and value.strip().lower() in {"true", "yes", "reviewed", "attested", "approved"}
