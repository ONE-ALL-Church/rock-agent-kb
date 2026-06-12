from __future__ import annotations

from pathlib import Path


def test_untrusted_pr_validation_workflows_are_read_only():
    for path in [
        Path(".github/workflows/public-surface.yml"),
        Path(".github/workflows/validate-contributions.yml"),
    ]:
        text = path.read_text(encoding="utf-8")
        assert "pull_request:" in text
        assert "permissions:" in text
        assert "contents: read" in text
