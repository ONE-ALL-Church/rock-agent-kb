from __future__ import annotations

from pathlib import Path

from rock_kb.release import validate_release


def write_release_files(tmp_path: Path, version: str = "0.5.0") -> tuple[Path, Path]:
    project = tmp_path / "pyproject.toml"
    project.write_text(f'[project]\nname = "rock-kb"\nversion = "{version}"\n', encoding="utf-8")
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(f"# Changelog\n\n## [{version}] - 2026-07-10\n", encoding="utf-8")
    return project, changelog


def test_release_version_accepts_matching_tag_package_and_changelog(tmp_path):
    project, changelog = write_release_files(tmp_path)

    assert validate_release("rock-kb-v0.5.0", project, changelog) == []


def test_release_version_rejects_mismatches(tmp_path):
    project, changelog = write_release_files(tmp_path, version="0.4.0")

    errors = validate_release("rock-kb-v0.5.0", project, changelog)

    assert len(errors) == 2
