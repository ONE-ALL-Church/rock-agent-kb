#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

DISALLOWED_TRACKED_PREFIXES = (
    "data/",
    "data/public-export/",
    "docs/log/",
    "templates/public-repo/",
)

PUBLIC_SCAN_PREFIXES = (
    "AGENTS.md",
    "README.md",
    ".github/",
    "agent/",
    "claims/",
    "community-contributions/",
    "concepts/",
    "contributions/",
    "docs/",
    "knowledge/",
    "source-suggestions/",
    "sources/",
)

FORBIDDEN_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("absolute local user path", re.compile(r"/Users/")),
    ("local-only user URI", re.compile(r"local:///Users")),
    ("private RockProduction marker", re.compile(r"RockProduction")),
    ("private RockDB marker", re.compile(r"\bRockDB\b")),
    ("connected database login", re.compile(r"mcp_readonly")),
    ("private live-verification evidence path", re.compile(r"data/review/live-verification-evidence/")),
    ("private evidence URI", re.compile(r"private-evidence://")),
    ("connected database evidence id", re.compile(r"connected-rockdb|oneall-rockdb")),
    ("demo login credential", re.compile(r"\badmin/admin\b")),
    ("private key material", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("openai token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
)


def main() -> int:
    tracked = tracked_files()
    errors: list[str] = []
    for rel_path in tracked:
        errors.extend(audit_tracked_path(rel_path))
        if should_scan_text(rel_path):
            errors.extend(audit_text_file(Path(rel_path)))
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "ok", "files": len(tracked)}))
    return 0


def tracked_files() -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True)
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def audit_tracked_path(rel_path: str) -> list[str]:
    return [
        f"{rel_path} is tracked but must remain ignored scratch/private output"
        for prefix in DISALLOWED_TRACKED_PREFIXES
        if rel_path.startswith(prefix)
    ]


def should_scan_text(rel_path: str) -> bool:
    return any(rel_path == prefix or rel_path.startswith(prefix) for prefix in PUBLIC_SCAN_PREFIXES)


def audit_text_file(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    errors: list[str] = []
    for label, pattern in FORBIDDEN_TEXT_PATTERNS:
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                errors.append(f"{path}:{line_number} contains {label}")
                break
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
