from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def load_bootstrap_module():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_private_corpus_infra.py"
    spec = importlib.util.spec_from_file_location("bootstrap_private_corpus_infra", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def completed(stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


def test_bootstrap_private_corpus_infra_dry_run_lists_required_commands(tmp_path):
    bootstrap = load_bootstrap_module()

    result = bootstrap.bootstrap_private_corpus_infra(
        repo="example/private-corpus",
        bucket="private-media",
        account_id="account",
        location="wnam",
        service_dir=tmp_path,
        workflow="private-corpus-ingest.yml",
        dispatch=True,
        run_media_batch=True,
        media_source="rock_podcast_rss",
        media_limit="1",
        apply=False,
        env={},
    )

    assert result["status"] == "dry_run"
    assert any("wrangler r2 bucket create private-media" in command for command in result["planned_commands"])
    assert any("gh variable set CLOUDFLARE_ACCOUNT_ID" in command for command in result["planned_commands"])
    assert any("gh secret set CLOUDFLARE_API_TOKEN" in command for command in result["planned_commands"])
    assert any("gh workflow run private-corpus-ingest.yml" in command for command in result["planned_commands"])
    assert not any("token" in command.lower() and "CLOUDFLARE_API_TOKEN\"" not in command for command in result["planned_commands"])


def test_bootstrap_private_corpus_infra_apply_sets_private_repo_values(tmp_path):
    bootstrap = load_bootstrap_module()
    commands: list[list[str]] = []

    def run(command: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        if command[:5] == ["npx", "wrangler", "r2", "bucket", "list"]:
            return completed("")
        if command[:5] == ["npx", "wrangler", "r2", "bucket", "create"]:
            return completed("created")
        if tuple(command[:3]) in {("gh", "variable", "set"), ("gh", "secret", "set")}:
            return completed("")
        if command[:3] == ["gh", "workflow", "run"]:
            return completed("")
        raise AssertionError(command)

    result = bootstrap.bootstrap_private_corpus_infra(
        repo="example/private-corpus",
        bucket="private-media",
        account_id="account",
        location="wnam",
        service_dir=tmp_path,
        workflow="private-corpus-ingest.yml",
        dispatch=True,
        run_media_batch=False,
        media_source="rock_podcast_rss",
        media_limit="1",
        apply=True,
        env={"CLOUDFLARE_API_TOKEN": "secret-token"},
        run=run,
    )

    assert result["status"] == "ok"
    assert result["repo"] == "<redacted-private-corpus-repo>"
    assert ["gh", "variable", "set", "CLOUDFLARE_ACCOUNT_ID", "--repo", "example/private-corpus", "--body", "account"] in commands
    assert ["gh", "variable", "set", "PRIVATE_R2_BUCKET", "--repo", "example/private-corpus", "--body", "private-media"] in commands
    assert ["gh", "secret", "set", "CLOUDFLARE_API_TOKEN", "--repo", "example/private-corpus", "--body", "secret-token"] in commands
    assert any(command[:3] == ["gh", "workflow", "run"] and "run_media_batch=false" in command for command in commands)


def test_bootstrap_private_corpus_infra_apply_requires_token(tmp_path):
    bootstrap = load_bootstrap_module()

    result = bootstrap.bootstrap_private_corpus_infra(
        repo="example/private-corpus",
        bucket="private-media",
        account_id="account",
        location="wnam",
        service_dir=tmp_path,
        workflow="private-corpus-ingest.yml",
        dispatch=False,
        run_media_batch=False,
        media_source="rock_podcast_rss",
        media_limit="1",
        apply=True,
        env={},
    )

    assert result["status"] == "fail"
    assert result["errors"] == ["CLOUDFLARE_API_TOKEN is required in the environment; GitHub secret was not written."]
