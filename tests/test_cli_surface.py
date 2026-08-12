from __future__ import annotations

import pytest
from typer.testing import CliRunner

from rock_kb.cli import app
from rock_kb.cli import audit_cmds
from rock_kb.cli import tools_cmds
from rock_kb.source_native import SOURCE_NATIVE_PILOT_DIR
from rock_kb.source_native import SOURCE_NATIVE_PILOT_CONCEPTS
from rock_kb.source_native_verification import VERIFICATION_REPORT_NAME


FINAL_COMMANDS = [
    ["status"],
    ["build"],
    ["serve"],
    ["deploy-service"],
    ["eval-service"],
    ["network-readiness"],
    ["sources", "list"],
    ["sources", "validate"],
    ["sources", "discover"],
    ["sources", "discover-community"],
    ["sources", "fetch"],
    ["sources", "normalize"],
    ["sources", "summarize"],
    ["sources", "refresh"],
    ["sources", "probe-endpoints"],
    ["sources", "scan"],
    ["extract", "markdown"],
    ["extract", "doctor"],
    ["issues", "sync"],
    ["issues", "validate"],
    ["issues", "list"],
    ["issues", "get"],
    ["issues", "plan"],
    ["issues", "assess"],
    ["lava", "contexts-build"],
    ["lava", "contexts-refresh-source"],
    ["media", "discover"],
    ["media", "transcribe"],
    ["media", "batch"],
    ["media", "doctor"],
    ["media", "report"],
    ["media", "queue"],
    ["media", "normalize"],
    ["media", "sidecars"],
    ["media", "prune-dry-runs"],
    ["media", "candidates"],
    ["media", "review-status"],
    ["media", "draft-rewrites"],
    ["media", "promote"],
    ["media", "understand-benchmark"],
    ["media", "understand-prepare"],
    ["media", "understand-run"],
    ["claims", "validate"],
    ["claims", "live-plan"],
    ["corpus", "init"],
    ["corpus", "validate"],
    ["corpus", "report"],
    ["corpus", "sync"],
    ["corpus", "media-manifest"],
    ["corpus", "audit"],
    ["corpus", "verify-rebuild"],
    ["private", "scan"],
    ["private", "ingest"],
    ["private", "review-report"],
    ["private", "distill"],
    ["private", "stale"],
    ["private", "impact"],
    ["contributions", "new"],
    ["contributions", "check"],
    ["contributions", "validate"],
    ["contributions", "promote"],
    ["concepts", "list"],
    ["concepts", "synthesize"],
    ["concepts", "hydrate"],
    ["modelmap", "build"],
    ["modelmap", "stamp"],
    ["modelmap", "diff"],
    ["recipes", "validate"],
    ["recipes", "build"],
    ["recipes", "list"],
    ["recipes", "get"],
    ["recipes", "check-upstream"],
    ["recipes", "promote"],
    ["audit", "guide"],
    ["audit", "licenses"],
    ["audit", "rockumentation-api-coverage"],
    ["audit", "source-policy"],
    ["audit", "public-export"],
    ["audit", "readiness"],
    ["audit", "all"],
    ["publish", "export"],
    ["report", "refresh"],
    ["report", "dashboard"],
    ["tools", "repo-pack"],
]

DEAD_COMMANDS = [
    ["build-claims"],
    ["media-public-promote"],
    ["guide-refresh-plan"],
    ["private-corpus-sync"],
    ["rebuild-plan"],
    ["contributions", "import-public"],
    ["publish", "push"],
]


@pytest.mark.parametrize("command", FINAL_COMMANDS)
def test_final_cli_surface_resolves_help(command):
    result = CliRunner().invoke(app, [*command, "--help"])

    assert result.exit_code == 0, result.output


@pytest.mark.parametrize("command", DEAD_COMMANDS)
def test_dead_flat_cli_names_fail(command):
    result = CliRunner().invoke(app, [*command, "--help"])

    assert result.exit_code != 0


def test_audit_all_passes_concrete_rockumentation_options(monkeypatch):
    calls = []
    monkeypatch.setattr(audit_cmds.legacy, "audit_licenses", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_source_url_duplicates_command", lambda: None)
    monkeypatch.setattr(
        audit_cmds.legacy,
        "audit_rockumentation_api_coverage_command",
        lambda **options: calls.append(options),
    )
    monkeypatch.setattr(audit_cmds.legacy, "audit_source_policy_command", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_public_export_command", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_readiness", lambda **options: calls.append(options))

    audit_cmds.audit_all(public_only=True)

    assert calls == [
        {"probe_static": False, "max_static_probes": None},
        {"public_only": True},
    ]


def test_live_verification_audit_rejects_manifest_bound_report_destination():
    result = CliRunner().invoke(
        app,
        [
            "tools",
            "source-native-verification-audit",
            "--check-live",
            "--destination",
            str(SOURCE_NATIVE_PILOT_DIR / VERIFICATION_REPORT_NAME),
        ],
    )

    assert result.exit_code != 0
    assert "ephemeral readiness evidence" in result.output


def test_exact_source_native_candidates_require_explicit_concept():
    result = CliRunner().invoke(
        app,
        [
            "tools",
            "source-native-candidates",
            "--source-record-id",
            "rock_developer:article:139",
        ],
    )

    assert result.exit_code != 0
    assert "exact --source-record-id selection requires" in result.output
    assert "explicit --concept routing facet" in result.output


def test_balanced_source_native_candidates_keep_pilot_concepts(monkeypatch):
    calls = []
    monkeypatch.setattr(
        tools_cmds,
        "build_source_native_document_candidates",
        lambda **options: calls.append(options) or {"status": "ok"},
    )

    result = CliRunner().invoke(
        app,
        ["tools", "source-native-candidates", "--limit-per-concept", "1"],
    )

    assert result.exit_code == 0, result.output
    assert calls[0]["concept_ids"] == list(SOURCE_NATIVE_PILOT_CONCEPTS)


def test_exact_source_native_candidates_forward_explicit_concept(monkeypatch):
    calls = []
    monkeypatch.setattr(
        tools_cmds,
        "build_source_native_document_candidates",
        lambda **options: calls.append(options) or {"status": "ok"},
    )

    result = CliRunner().invoke(
        app,
        [
            "tools",
            "source-native-candidates",
            "--concept",
            "apple-tv",
            "--source-id",
            "rock_developer",
            "--source-record-id",
            "rock_developer:article:139",
        ],
    )

    assert result.exit_code == 0, result.output
    assert calls[0]["concept_ids"] == ["apple-tv"]
    assert calls[0]["source_record_ids"] == ["rock_developer:article:139"]
