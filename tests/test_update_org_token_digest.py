from __future__ import annotations

import hashlib
import json
import subprocess


SCRIPT = "scripts/update_org_token_digest.py"


def run_digest(*args: str, token: str = "abcdefghijklmnopqrstuvwxyz123456") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", SCRIPT, *args],
        input=token,
        text=True,
        capture_output=True,
        check=False,
    )


def test_updates_existing_org_token_digest():
    existing = {"oneall": hashlib.sha256(b"existing-token-with-enough-length").hexdigest()}

    result = run_digest("--org-id", "second-org", "--existing-json", json.dumps(existing))

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["oneall"] == existing["oneall"]
    assert payload["second-org"] == hashlib.sha256(b"abcdefghijklmnopqrstuvwxyz123456").hexdigest()


def test_rejects_short_tokens():
    result = run_digest("--org-id", "second-org", token="short")

    assert result.returncode == 1
    assert "too short" in result.stderr


def test_rejects_invalid_existing_digest():
    result = run_digest("--org-id", "second-org", "--existing-json", '{"oneall":"not-a-digest"}')

    assert result.returncode == 1
    assert "invalid SHA-256 digest" in result.stderr
