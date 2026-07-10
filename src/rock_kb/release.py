from __future__ import annotations

import re
import tomllib
from pathlib import Path


def validate_release(tag: str, client_project: Path, changelog: Path) -> list[str]:
    errors: list[str] = []
    match = re.fullmatch(r"rock-kb-v(?P<version>\d+\.\d+\.\d+)", tag)
    if not match:
        return [f"release tag must match rock-kb-vMAJOR.MINOR.PATCH: {tag}"]
    expected = match.group("version")
    project = tomllib.loads(client_project.read_text(encoding="utf-8"))
    actual = str(project.get("project", {}).get("version") or "")
    if actual != expected:
        errors.append(f"client version {actual or '<missing>'} does not match tag version {expected}")
    changelog_text = changelog.read_text(encoding="utf-8")
    if f"## [{expected}]" not in changelog_text:
        errors.append(f"CHANGELOG.md does not contain a {expected} release section")
    return errors
