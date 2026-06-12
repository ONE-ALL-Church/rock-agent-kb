#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ORG_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,62}[a-z0-9]$")
STATUSES = {"pending", "reviewed", "suspended"}
PROHIBITED_TEXT = [
    "/Users/",
    "data/review/",
    "data/media/",
    "data/normalized/",
    "password",
    "secret",
    "api_key",
    "token",
    "connectionString",
]


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("orgs")
    errors: list[str] = []
    files = sorted(root.glob("*.yaml"))
    for path in files:
        errors.extend(validate_org_file(path))
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "ok", "files": len(files)}))
    return 0


def validate_org_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"{path} invalid YAML: {exc}"]
    if not isinstance(data, dict):
        return [f"{path} must contain a YAML object"]
    org_id = str(data.get("org_id") or "")
    if data.get("schema") != "rock-kb-org-v1":
        errors.append(f"{path} schema must be rock-kb-org-v1")
    if not ORG_ID_PATTERN.match(org_id):
        errors.append(f"{path} org_id must be a lowercase slug")
    if path.stem != org_id:
        errors.append(f"{path} filename must match org_id")
    if not data.get("display_name"):
        errors.append(f"{path} display_name is required")
    if data.get("status") not in STATUSES:
        errors.append(f"{path} status must be one of: {', '.join(sorted(STATUSES))}")
    if not list_of_strings(data.get("github_accounts")):
        errors.append(f"{path} github_accounts must be a non-empty list of strings")
    attestations = data.get("standing_attestations")
    if not isinstance(attestations, dict):
        errors.append(f"{path} standing_attestations is required")
    else:
        if attestations.get("redaction") is not True:
            errors.append(f"{path} standing_attestations.redaction must be true")
        if attestations.get("license") is not True:
            errors.append(f"{path} standing_attestations.license must be true")
    serialized = yaml.safe_dump(data, sort_keys=True)
    for marker in PROHIBITED_TEXT:
        if marker.lower() in serialized.lower():
            errors.append(f"{path} contains prohibited private/secret marker: {marker}")
    return errors


def list_of_strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
