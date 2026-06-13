from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def load_bootstrap_module():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_service_infra.py"
    spec = importlib.util.spec_from_file_location("bootstrap_service_infra", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def completed(stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


def test_bootstrap_service_infra_dry_run_lists_required_commands(tmp_path):
    bootstrap = load_bootstrap_module()

    result = bootstrap.bootstrap_service_infra(
        repo="ONE-ALL-Church/rock-agent-kb",
        environment="production",
        database="rock-agent-kb",
        bucket="rock-agent-kb-artifacts",
        base_url="https://rock-agent-kb.oneandall.church",
        location="wnam",
        service_dir=tmp_path,
        apply=False,
        env={},
    )

    assert result["status"] == "dry_run"
    assert any("wrangler d1 create rock-agent-kb" in command for command in result["planned_commands"])
    assert any("ROCK_KB_D1_DATABASE_ID" in command for command in result["planned_commands"])
    assert any("CLOUDFLARE_API_TOKEN" in command for command in result["planned_commands"])
    assert any("ROCK_KB_WORKER_GITHUB_TOKEN" in command for command in result["planned_commands"])
    assert any("ORG_TOKEN_SHA256_JSON" in command for command in result["planned_commands"])


def test_bootstrap_service_infra_apply_sets_variables_and_secrets(tmp_path):
    bootstrap = load_bootstrap_module()
    commands: list[list[str]] = []

    def run(command: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        if command[:4] == ["npx", "wrangler", "d1", "list"]:
            return completed("[]")
        if command[:4] == ["npx", "wrangler", "d1", "create"]:
            return completed("database_id = \"11111111-1111-1111-1111-111111111111\"")
        if command[:5] == ["npx", "wrangler", "r2", "bucket", "list"]:
            return completed("")
        if command[:5] == ["npx", "wrangler", "r2", "bucket", "create"]:
            return completed("created")
        if tuple(command[:3]) in {("gh", "variable", "set"), ("gh", "secret", "set")}:
            return completed("")
        raise AssertionError(command)

    result = bootstrap.bootstrap_service_infra(
        repo="ONE-ALL-Church/rock-agent-kb",
        environment="production",
        database="rock-agent-kb",
        bucket="rock-agent-kb-artifacts",
        base_url="https://rock-agent-kb.oneandall.church",
        location="wnam",
        service_dir=tmp_path,
        apply=True,
        env={
            "CLOUDFLARE_API_TOKEN": "token",
            "CLOUDFLARE_ACCOUNT_ID": "account",
            "ROCK_KB_WORKER_GITHUB_TOKEN": "github-token",
            "ORG_TOKEN_SHA256_JSON": '{"example":"digest"}',
        },
        run=run,
    )

    assert result["status"] == "ok"
    assert result["d1_database_id"] == "11111111-1111-1111-1111-111111111111"
    assert ["gh", "variable", "set", "ROCK_KB_D1_DATABASE_ID", "--repo", "ONE-ALL-Church/rock-agent-kb", "--env", "production", "--body", result["d1_database_id"]] in commands
    assert any(command[:3] == ["gh", "secret", "set"] and command[3] == "CLOUDFLARE_API_TOKEN" for command in commands)
    assert any(command[:3] == ["gh", "secret", "set"] and command[3] == "ROCK_KB_WORKER_GITHUB_TOKEN" for command in commands)
    assert any(command[:3] == ["gh", "secret", "set"] and command[3] == "ORG_TOKEN_SHA256_JSON" for command in commands)
