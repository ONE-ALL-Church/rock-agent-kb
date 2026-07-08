from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_new_contribution_script_writes_valid_bundle(tmp_path: Path) -> None:
    output = tmp_path / "community-contributions" / "test-org" / "bundle.jsonl"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/new_contribution.py",
            "--org-id",
            "test-org",
            "--org-name",
            "Test Org",
            "--concept",
            "workflows",
            "--type",
            "troubleshooting_pattern",
            "--title",
            "Workflow launch triage pattern",
            "--summary",
            "When a workflow does not launch, verify the trigger, active workflow type, entity context, action logs, and notification idempotency before changing configuration.",
            "--source-url",
            "https://community.rockrms.com/documentation",
            "--needs-live-verification",
            "--redaction-reviewed",
            "--license-attested",
            "--output",
            str(output),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert "Validate with:" in result.stdout
    row = json.loads(output.read_text(encoding="utf-8"))
    assert row["org_id"] == "test-org"
    assert row["review_status"] == "approved_for_public_distillation"
    assert row["redaction_attestation"] is True
    assert row["license_attestation"] is True

    validation = subprocess.run(
        [sys.executable, "scripts/validate_bundle.py", str(output)],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    assert '"status": "ok"' in validation.stdout
