from __future__ import annotations

import pytest
from typer.testing import CliRunner

from rock_kb.cli import app


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
