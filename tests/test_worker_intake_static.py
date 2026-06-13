from __future__ import annotations

from pathlib import Path


WORKER = Path("service/src/index.ts")


def test_worker_submit_validator_has_ci_parity_privacy_gates():
    source = WORKER.read_text(encoding="utf-8")

    expected_snippets = [
        "ALLOWED_CONTRIBUTION_FIELDS",
        "unknown fields:",
        "needs_live_verification must be true or false",
        "source_urls must contain strings",
        "source_urls must use http or https URLs",
        "sk-[A-Za-z0-9_-]{20,}",
        "connectionstring",
        "distilled_summary looks like raw transcript text",
    ]

    for snippet in expected_snippets:
        assert snippet in source


def test_worker_auto_merge_keeps_server_side_path_gate():
    source = WORKER.read_text(encoding="utf-8")

    expected_snippets = [
        "AUTO_MERGE_INTAKE",
        "auto_merge_allowed",
        "Auto-merge requires exactly one changed file",
        "Changed file ${filename || \"<missing>\"} did not match expected path ${expectedPath}.",
        "enablePullRequestAutoMerge",
    ]

    for snippet in expected_snippets:
        assert snippet in source
