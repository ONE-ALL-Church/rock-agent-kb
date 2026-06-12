from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pydantic import ValidationError

from rock_kb.private_leakage import find_leaks
from rock_kb.schemas import ContributionRow

SCRIPT = Path("scripts/validate_bundle.py")
VALID_FIXTURE = Path("tests/fixtures/contributions/valid-bundle.jsonl")
INVALID_FIXTURE = Path("tests/fixtures/contributions/invalid-bundle.jsonl")


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )


def model_plus_leaks_accepts(path: Path) -> bool:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        try:
            ContributionRow.model_validate(row)
        except ValidationError:
            return False
        if find_leaks(row):
            return False
    return True


def test_validate_bundle_script_accepts_valid_fixture():
    result = run_validator(VALID_FIXTURE)

    assert result.returncode == 0, result.stderr
    assert model_plus_leaks_accepts(VALID_FIXTURE) is True


def test_validate_bundle_script_rejects_invalid_fixture_like_schema():
    result = run_validator(INVALID_FIXTURE)

    assert result.returncode == 1
    assert "invalid contribution_type" in result.stderr
    assert "unknown fields: unexpected" in result.stderr
    assert model_plus_leaks_accepts(INVALID_FIXTURE) is False


def test_validate_bundle_script_rejects_private_path_like_leak_checker(tmp_path):
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    row["source_urls"] = ["data/review/private-source.md"]
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = run_validator(bundle)

    assert result.returncode == 1
    assert "private path reference" in result.stderr
    assert model_plus_leaks_accepts(bundle) is False
