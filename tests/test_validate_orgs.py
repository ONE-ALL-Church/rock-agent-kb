from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/validate_orgs.py")


def test_validate_orgs_accepts_example_registry():
    result = subprocess.run([sys.executable, str(SCRIPT)], text=True, capture_output=True, check=False)

    assert result.returncode == 0, result.stderr
    assert '"status": "ok"' in result.stdout


def test_validate_orgs_rejects_filename_mismatch(tmp_path):
    orgs = tmp_path / "orgs"
    orgs.mkdir()
    (orgs / "wrong.yaml").write_text(
        """
schema: rock-kb-org-v1
org_id: right
display_name: Right Church
status: reviewed
github_accounts:
  - right-agent
standing_attestations:
  redaction: true
  license: true
""",
        encoding="utf-8",
    )

    result = subprocess.run([sys.executable, str(SCRIPT), str(orgs)], text=True, capture_output=True, check=False)

    assert result.returncode == 1
    assert "filename must match org_id" in result.stderr
