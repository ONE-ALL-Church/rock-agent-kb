from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rock_kb import network_readiness as network_readiness_module
from rock_kb.network_readiness import (
    default_run_command,
    hosted_service_check,
    network_readiness_report,
    org_registry_depth_check,
    private_corpus_cloud_check,
    repo_side_implementation_check,
)


def completed(stdout: object = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=json.dumps(stdout) if isinstance(stdout, dict) else str(stdout),
        stderr="",
    )


def test_network_readiness_reports_current_missing_external_gates(tmp_path):
    def run(command: list[str]) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["gh", "pr", "view"]:
            return completed(
                {
                    "state": "OPEN",
                    "mergeable": "MERGEABLE",
                    "reviewDecision": "REVIEW_REQUIRED",
                    "url": "https://github.com/example/repo/pull/2",
                    "statusCheckRollup": [{"name": "public-surface", "status": "COMPLETED", "conclusion": "SUCCESS"}],
                }
            )
        if command[:3] == ["gh", "secret", "list"]:
            return completed("")
        if command[:3] == ["gh", "variable", "list"]:
            return completed("")
        if command[:2] == ["gh", "api"]:
            return completed({"allow_auto_merge": False})
        raise AssertionError(command)

    report = network_readiness_report(
        repo="ONE-ALL-Church/rock-agent-kb",
        pr=2,
        env={},
        run_command=run,
        private_corpus_path=tmp_path / "missing-corpus",
    )

    checks = {row["id"]: row for row in report["checks"]}
    assert report["status"] == "fail"
    assert checks["repo_side_implementation"]["status"] == "pass"
    assert checks["pr_review_gate"]["evidence"]["reviewDecision"] == "REVIEW_REQUIRED"
    assert checks["github_deploy_configuration"]["evidence"]["missing_secrets"] == [
        "CLOUDFLARE_ACCOUNT_ID",
        "CLOUDFLARE_API_TOKEN",
        "ORG_TOKEN_SHA256_JSON",
        "ROCK_KB_WORKER_GITHUB_TOKEN",
    ]
    assert checks["hosted_service"]["status"] == "fail"
    assert checks["github_auto_merge_policy"]["evidence"]["allow_auto_merge"] is False
    assert checks["private_corpus_cloud_restore"]["status"] == "fail"


def test_repo_side_implementation_requires_private_ingest_template():
    check = repo_side_implementation_check()

    assert check["status"] == "pass"
    assert "docs/templates/private-corpus-ingest.workflow.yml" in check["evidence"]["required"]


def test_org_registry_depth_requires_reviewed_orgs_with_public_contributions(tmp_path, monkeypatch):
    monkeypatch.setattr(network_readiness_module, "REPO_ROOT", tmp_path)
    orgs = tmp_path / "orgs"
    orgs.mkdir()
    (orgs / "first-org.yaml").write_text(
        "\n".join(
            [
                "schema: rock-kb-org-v1",
                "org_id: first-org",
                "display_name: First Org",
                "status: reviewed",
                "github_accounts: [first-agent]",
                "standing_attestations:",
                "  redaction: true",
                "  license: true",
            ]
        ),
        encoding="utf-8",
    )
    (orgs / "second-org.yaml").write_text(
        "\n".join(
            [
                "schema: rock-kb-org-v1",
                "org_id: second-org",
                "display_name: Second Org",
                "status: reviewed",
                "github_accounts: [second-agent]",
                "standing_attestations:",
                "  redaction: true",
                "  license: true",
            ]
        ),
        encoding="utf-8",
    )
    bundle = tmp_path / "community-contributions" / "first-org" / "bundle.jsonl"
    bundle.parent.mkdir(parents=True)
    bundle.write_text(json.dumps({"org_id": "first-org", "review_status": "redaction_reviewed"}) + "\n", encoding="utf-8")

    check = org_registry_depth_check()

    assert check["status"] == "fail"
    assert check["evidence"]["reviewed_org_count"] == 2
    assert check["evidence"]["reviewed_contributing_orgs"] == ["first-org"]
    assert check["evidence"]["required_reviewed_contributing_org_count"] == 2


def test_org_registry_depth_passes_with_two_reviewed_contributing_orgs(tmp_path, monkeypatch):
    monkeypatch.setattr(network_readiness_module, "REPO_ROOT", tmp_path)
    orgs = tmp_path / "orgs"
    orgs.mkdir()
    for org_id in ["first-org", "second-org"]:
        (orgs / f"{org_id}.yaml").write_text(
            "\n".join(
                [
                    "schema: rock-kb-org-v1",
                    f"org_id: {org_id}",
                    f"display_name: {org_id}",
                    "status: reviewed",
                    f"github_accounts: [{org_id}-agent]",
                    "standing_attestations:",
                    "  redaction: true",
                    "  license: true",
                ]
            ),
            encoding="utf-8",
        )
        bundle = tmp_path / "community-contributions" / org_id / "bundle.jsonl"
        bundle.parent.mkdir(parents=True)
        bundle.write_text(json.dumps({"org_id": org_id, "review_status": "redaction_reviewed"}) + "\n", encoding="utf-8")

    check = org_registry_depth_check()

    assert check["status"] == "pass"
    assert check["evidence"]["reviewed_contributing_org_count"] == 2


def test_private_corpus_cloud_check_redacts_local_path(tmp_path):
    corpus = tmp_path / "private-corpus"
    for rel in [
        "data/media",
        "data/review",
        "data/normalized",
        "data/raw-manifests",
    ]:
        (corpus / rel).mkdir(parents=True)
    (corpus / "private-corpus-manifest.json").write_text("{}\n", encoding="utf-8")
    (corpus / "large-media-restore-manifest.json").write_text("{}\n", encoding="utf-8")

    check = private_corpus_cloud_check(corpus)

    assert check["status"] == "pass"
    assert check["evidence"]["mount_path"] == "<redacted-private-corpus-path>"
    assert check["evidence"]["path_provided"] is True
    assert check["evidence"]["path_exists"] is True
    assert str(corpus) not in json.dumps(check)


def test_hosted_service_failure_evidence_includes_stdout_and_returncode():
    def run(command: list[str]) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["curl", "--fail", "--silent"]:
            return completed("{}")
        if command[:4] == ["uv", "run", "kb", "eval-service"]:
            return subprocess.CompletedProcess(args=command, returncode=2, stdout='{"status":"fail"}\n', stderr="")
        raise AssertionError(command)

    check = hosted_service_check(
        {"ROCK_KB_BASE_URL": "https://example.test"},
        repo="example/repo",
        run_command=run,
        check_github=False,
    )

    assert check["status"] == "fail"
    failure = check["evidence"]["failures"][0]
    assert failure["returncode"] == 2
    assert failure["stdout_tail"] == '{"status":"fail"}\n'
    assert failure["stderr_tail"] == ""


def test_network_readiness_can_pass_when_live_gates_are_satisfied(tmp_path, monkeypatch):
    monkeypatch.setattr(
        network_readiness_module,
        "org_registry_depth_check",
        lambda: {"id": "second_org_proof", "status": "pass", "message": "ok", "evidence": {}},
    )
    corpus = tmp_path / "corpus"
    for rel in [
        "data/media",
        "data/review",
        "data/normalized",
        "data/raw-manifests",
    ]:
        (corpus / rel).mkdir(parents=True)
    (corpus / "private-corpus-manifest.json").write_text("{}\n", encoding="utf-8")
    (corpus / "large-media-restore-manifest.json").write_text("{}\n", encoding="utf-8")

    def run(command: list[str]) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["gh", "pr", "view"]:
            return completed(
                {
                    "state": "OPEN",
                    "mergeable": "MERGEABLE",
                    "reviewDecision": "APPROVED",
                    "url": "https://github.com/example/repo/pull/2",
                    "statusCheckRollup": [{"name": "public-surface", "status": "COMPLETED", "conclusion": "SUCCESS"}],
                }
            )
        if command[:3] == ["gh", "secret", "list"]:
            return completed(
                "CLOUDFLARE_API_TOKEN\t2026-06-12\n"
                "CLOUDFLARE_ACCOUNT_ID\t2026-06-12\n"
                "ROCK_KB_WORKER_GITHUB_TOKEN\t2026-06-12\n"
                "ORG_TOKEN_SHA256_JSON\t2026-06-12\n"
            )
        if command[:3] == ["gh", "variable", "list"]:
            return completed("ROCK_KB_D1_DATABASE_ID\tset\nROCK_KB_BASE_URL\tset\n")
        if command[:2] == ["gh", "api"]:
            return completed({"allow_auto_merge": True})
        if command[:3] == ["curl", "--fail", "--silent"]:
            return completed("{}")
        if command[:4] == ["uv", "run", "kb", "eval-service"]:
            return completed({"status": "ok", "pass_count": 100, "fail_count": 0})
        raise AssertionError(command)

    report = network_readiness_report(repo="ONE-ALL-Church/rock-agent-kb", pr=2, private_corpus_path=corpus, run_command=run)

    assert report["status"] == "pass"


def test_network_readiness_pr_gate_passes_after_merge(tmp_path, monkeypatch):
    monkeypatch.setattr(
        network_readiness_module,
        "org_registry_depth_check",
        lambda: {"id": "second_org_proof", "status": "pass", "message": "ok", "evidence": {}},
    )
    corpus = tmp_path / "corpus"
    for rel in [
        "data/media",
        "data/review",
        "data/normalized",
        "data/raw-manifests",
    ]:
        (corpus / rel).mkdir(parents=True)
    (corpus / "private-corpus-manifest.json").write_text("{}\n", encoding="utf-8")
    (corpus / "large-media-restore-manifest.json").write_text("{}\n", encoding="utf-8")

    def run(command: list[str]) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["gh", "pr", "view"]:
            return completed(
                {
                    "state": "MERGED",
                    "mergeable": "UNKNOWN",
                    "reviewDecision": "",
                    "mergedAt": "2026-06-12T20:00:00Z",
                    "url": "https://github.com/example/repo/pull/2",
                    "statusCheckRollup": [{"name": "public-surface", "status": "COMPLETED", "conclusion": "SUCCESS"}],
                }
            )
        if command[:3] == ["gh", "secret", "list"]:
            return completed(
                "CLOUDFLARE_API_TOKEN\t2026-06-12\n"
                "CLOUDFLARE_ACCOUNT_ID\t2026-06-12\n"
                "ROCK_KB_WORKER_GITHUB_TOKEN\t2026-06-12\n"
                "ORG_TOKEN_SHA256_JSON\t2026-06-12\n"
            )
        if command[:3] == ["gh", "variable", "list"]:
            return completed("ROCK_KB_D1_DATABASE_ID\tset\nROCK_KB_BASE_URL\tset\n")
        if command[:2] == ["gh", "api"]:
            return completed({"allow_auto_merge": True})
        if command[:3] == ["curl", "--fail", "--silent"]:
            return completed("{}")
        if command[:4] == ["uv", "run", "kb", "eval-service"]:
            return completed({"status": "ok", "pass_count": 100, "fail_count": 0})
        raise AssertionError(command)

    report = network_readiness_report(repo="ONE-ALL-Church/rock-agent-kb", pr=2, private_corpus_path=corpus, run_command=run)

    assert report["status"] == "pass"
    checks = {row["id"]: row for row in report["checks"]}
    assert checks["pr_review_gate"]["message"] == "Milestone PR is merged."
    assert checks["pr_review_gate"]["evidence"]["required_action"] == ""


def test_default_run_command_times_out(monkeypatch):
    monkeypatch.setenv("ROCK_KB_NETWORK_READINESS_TIMEOUT", "1")

    result = default_run_command(["python3", "-c", "import time; time.sleep(3)"])

    assert result.returncode == 124
    assert "Command timed out after 1s" in result.stderr
