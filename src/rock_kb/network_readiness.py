from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable

import yaml

from .paths import REPO_ROOT


NETWORK_READINESS_SCHEMA = "rock-kb-agent-network-readiness-v1"
RunCommand = Callable[[list[str]], subprocess.CompletedProcess[str]]


def network_readiness_report(
    *,
    repo: str = "ONE-ALL-Church/rock-agent-kb",
    pr: int | None = None,
    private_corpus_path: Path | None = None,
    env: dict[str, str] | None = None,
    run_command: RunCommand | None = None,
    check_github: bool = True,
) -> dict[str, Any]:
    env_values = env if env is not None else dict(os.environ)
    runner = run_command or default_run_command
    checks = [
        repo_side_implementation_check(),
        org_registry_depth_check(),
        private_corpus_cloud_check(private_corpus_path or env_private_corpus_path(env_values), env_values, runner, check_github=check_github),
        private_corpus_autonomous_ingest_check(env_values, runner, check_github=check_github),
        hosted_service_check(env_values, repo, runner, check_github=check_github),
    ]
    if check_github:
        checks.extend(
            [
                pr_review_gate_check(repo, pr, runner),
                github_deploy_configuration_check(repo, runner),
                github_auto_merge_check(repo, runner),
            ]
        )
    else:
        checks.append(check("github_live_state", "warn", "GitHub live-state checks were skipped.", {}))
    return {
        "schema": NETWORK_READINESS_SCHEMA,
        "status": readiness_status(checks),
        "summary": readiness_summary(checks),
        "checks": checks,
    }


def repo_side_implementation_check() -> dict[str, Any]:
    required = [
        "service/src/index.ts",
        "service/wrangler.jsonc",
        "src/rock_kb/service_projection.py",
        "src/rock_kb/service_eval.py",
        "clients/python/src/rock_kb_client/cli.py",
        "docs/runbooks/private-corpus-cloud-runbook.md",
        "docs/templates/private-corpus-ingest.workflow.yml",
        ".github/workflows/deploy-service.yml",
        ".github/workflows/network-operations.yml",
        "scripts/network_operations_smoke.py",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).exists()]
    feature_errors = repo_side_feature_errors()
    return check(
        "repo_side_implementation",
        "fail" if missing or feature_errors else "pass",
        "Repo-side hosted service, client, intake, and private-corpus foundations exist."
        if not missing and not feature_errors
        else "Repo-side Agent Knowledge Network implementation files or feature gates are missing.",
        {"missing": missing, "required": required, "feature_errors": feature_errors},
    )


def repo_side_feature_errors() -> list[str]:
    errors = []
    deploy_workflow = read_repo_text(".github/workflows/deploy-service.yml")
    network_workflow = read_repo_text(".github/workflows/network-operations.yml")
    public_surface_workflow = read_repo_text(".github/workflows/public-surface.yml")
    validate_contributions_workflow = read_repo_text(".github/workflows/validate-contributions.yml")
    service_projection = read_repo_text("src/rock_kb/service_projection.py")
    worker = read_repo_text("service/src/index.ts")
    client = read_repo_text("clients/python/src/rock_kb_client/cli.py")
    private_ingest_template = read_repo_text("docs/templates/private-corpus-ingest.workflow.yml")
    for path in ["community-contributions/**", "source-suggestions/**", "orgs/**"]:
        if path not in deploy_workflow:
            errors.append(f"deploy-service workflow does not trigger on {path}")
    for label, workflow in [
        ("public-surface", public_surface_workflow),
        ("validate-contributions", validate_contributions_workflow),
    ]:
        if "pull_request:" not in workflow or "permissions:" not in workflow or "contents: read" not in workflow:
            errors.append(f"{label} workflow does not declare read-only permissions for untrusted PR validation")
    if "uv run python scripts/validate_orgs.py" not in deploy_workflow or "uv run python scripts/validate_bundle.py" not in deploy_workflow:
        errors.append("deploy-service workflow does not validate orgs and bundles in the project environment")
    if "/operations/dashboard" not in deploy_workflow:
        errors.append("deploy-service workflow does not smoke-test the hosted operations dashboard")
    if "schedule:" not in network_workflow or "workflow_dispatch:" not in network_workflow:
        errors.append("network operations workflow is not scheduled and manually runnable")
    smoke_script = read_repo_text("scripts/network_operations_smoke.py")
    if "scripts/network_operations_smoke.py" not in network_workflow:
        errors.append("network operations workflow does not use the checked-in smoke test script")
    if "hosted_eval_check" not in smoke_script or "/operations/dashboard" not in smoke_script:
        errors.append("network operations smoke script does not run hosted eval and dashboard probes")
    if "/submit" not in smoke_script or "/mcp" not in smoke_script:
        errors.append("network operations workflow does not smoke-test hosted MCP and intake boundary")
    if "schedule:" not in private_ingest_template or "workflow_dispatch:" not in private_ingest_template:
        errors.append("private corpus ingest template is not scheduled and manually runnable")
    if "kb corpus restore" not in private_ingest_template or "kb corpus autosync --path ../private-corpus --commit" not in private_ingest_template:
        errors.append("private corpus ingest template does not restore and autosync the corpus")
    if "git config user.name" not in private_ingest_template or "git config user.email" not in private_ingest_template:
        errors.append("private corpus ingest template does not configure a git identity before commit")
    if "PRIVATE_CORPUS_REPO" not in private_ingest_template or "PRIVATE_CORPUS_TOKEN" not in private_ingest_template:
        errors.append("private corpus ingest template does not parameterize the private repo and write token")
    if "contribution_search_rows" not in service_projection or "community_contribution" not in service_projection:
        errors.append("service projection does not emit community contribution rows")
    if "kind IN ('claim', 'community_contribution')" not in worker:
        errors.append("Worker claims endpoint does not include community contribution rows")
    if "/operations/dashboard" not in worker or "kb_review_dashboard" not in worker:
        errors.append("Worker does not expose the public operations dashboard endpoint and MCP tool")
    worker_validation_markers = [
        "unknown fields:",
        "needs_live_verification must be true or false",
        "source_urls must use http or https URLs",
        "distilled_summary looks like raw transcript text",
    ]
    if any(marker not in worker for marker in worker_validation_markers):
        errors.append("Worker submit validator is missing CI-parity contribution validation gates")
    if "autoMergeEligibility" not in worker or "expectedPath" not in worker or "auto_merge_allowed" not in worker:
        errors.append("Worker auto-merge path does not enforce org approval and exact per-org intake path eligibility")
    if "/operations/dashboard" not in client or 'subparsers.add_parser("dashboard")' not in client:
        errors.append("Python client does not expose the hosted operations dashboard")
    return errors


def read_repo_text(path: str) -> str:
    target = REPO_ROOT / path
    return target.read_text(encoding="utf-8") if target.exists() else ""


def org_registry_depth_check() -> dict[str, Any]:
    reviewed_orgs = []
    pending_orgs = []
    for path in sorted((REPO_ROOT / "orgs").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            continue
        org_id = str(data.get("org_id") or path.stem)
        if data.get("status") == "reviewed":
            reviewed_orgs.append(org_id)
        elif data.get("status") == "pending":
            pending_orgs.append(org_id)
    contribution_orgs = public_contribution_orgs()
    reviewed_contributing_orgs = sorted(set(reviewed_orgs) & contribution_orgs)
    status = "pass" if len(reviewed_contributing_orgs) >= 2 else "fail"
    return check(
        "second_org_proof",
        status,
        "At least two reviewed orgs have public contribution evidence."
        if status == "pass"
        else "Milestone 3 still needs two real reviewed orgs with contribution evidence.",
        {
            "reviewed_orgs": reviewed_orgs,
            "pending_orgs": pending_orgs,
            "contribution_orgs": sorted(contribution_orgs),
            "reviewed_contributing_orgs": reviewed_contributing_orgs,
            "reviewed_org_count": len(reviewed_orgs),
            "reviewed_contributing_org_count": len(reviewed_contributing_orgs),
            "required_reviewed_contributing_org_count": 2,
        },
    )


def public_contribution_orgs() -> set[str]:
    orgs: set[str] = set()
    public_statuses = {"redaction_reviewed", "approved_for_public_distillation"}
    for base in [REPO_ROOT / "community-contributions", REPO_ROOT / "contributions"]:
        if not base.exists():
            continue
        for path in sorted(base.glob("*/bundle*.jsonl")):
            if path.name.endswith(".example.jsonl"):
                continue
            expected_org = path.parent.name
            for row in read_jsonl_safely(path):
                org_id = str(row.get("org_id") or "")
                if org_id == expected_org and row.get("review_status") in public_statuses:
                    orgs.add(org_id)
                    break
    return orgs


def read_jsonl_safely(path: Path) -> list[dict[str, Any]]:
    rows = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def private_corpus_cloud_check(path: Path | None, env: dict[str, str] | None = None, run_command: RunCommand | None = None, *, check_github: bool = False) -> dict[str, Any]:
    env_values = env or {}
    runner = run_command or default_run_command
    if path is None:
        return check(
            "private_corpus_cloud_restore",
            "fail",
            "No private corpus path was provided, so laptop-free restore cannot be verified.",
            {"expected_env": "ROCK_KB_PRIVATE_CORPUS_PATH"},
        )
    required = [
        "private-corpus-manifest.json",
        "large-media-restore-manifest.json",
        "data/media",
        "data/review",
        "data/normalized",
        "data/raw-manifests",
    ]
    missing = [item for item in required if not (path / item).exists()]
    workflow_evidence = private_corpus_workflow_evidence(env_values, runner, check_github=check_github)
    failures = []
    if missing:
        failures.append("private corpus restore artifacts are missing")
    if workflow_evidence["status"] != "pass":
        failures.append(workflow_evidence["message"])
    return check(
        "private_corpus_cloud_restore",
        "fail" if failures else "pass",
        "Private corpus restore artifacts and cloud restore workflow are verified."
        if not failures
        else "Private corpus cloud restore is incomplete.",
        {
            "mount_path": "<redacted-private-corpus-path>",
            "path_provided": True,
            "path_exists": path.exists(),
            "missing": missing,
            "required": required,
            "workflow": workflow_evidence,
        },
    )


def private_corpus_autonomous_ingest_check(env: dict[str, str], run_command: RunCommand, *, check_github: bool) -> dict[str, Any]:
    if not check_github:
        return check("private_corpus_autonomous_ingest", "warn", "GitHub live-state checks were skipped.", {})
    repo = private_corpus_repo(env)
    if not repo:
        return check(
            "private_corpus_autonomous_ingest",
            "fail",
            "No private corpus repo was provided, so autonomous ingest configuration cannot be verified.",
            {"expected_env": "ROCK_KB_PRIVATE_CORPUS_REPO"},
        )
    secrets = set(list_names(["gh", "secret", "list", "--repo", repo], run_command))
    variables = set(list_names(["gh", "variable", "list", "--repo", repo], run_command))
    has_transcription_secret = bool({"OPENAI_API_KEY", "CLOUDFLARE_API_TOKEN"} & secrets)
    r2_ready = "PRIVATE_R2_BUCKET" in variables and "CLOUDFLARE_ACCOUNT_ID" in variables and "CLOUDFLARE_API_TOKEN" in secrets
    missing = []
    if not has_transcription_secret:
        missing.append("OPENAI_API_KEY or CLOUDFLARE_API_TOKEN")
    if not r2_ready:
        missing.extend(sorted({"PRIVATE_R2_BUCKET", "CLOUDFLARE_ACCOUNT_ID"} - variables))
        missing.extend(sorted({"CLOUDFLARE_API_TOKEN"} - secrets))
    return check(
        "private_corpus_autonomous_ingest",
        "pass" if not missing else "fail",
        "Private corpus autonomous transcription and R2 prerequisites are configured."
        if not missing
        else "Private corpus autonomous transcription or R2 prerequisites are missing.",
        {
            "private_repo": "<redacted-private-corpus-repo>",
            "has_transcription_secret": has_transcription_secret,
            "r2_ready": r2_ready,
            "missing": sorted(set(missing)),
        },
    )


def private_corpus_workflow_evidence(env: dict[str, str], run_command: RunCommand, *, check_github: bool) -> dict[str, Any]:
    if not check_github:
        return {"status": "warn", "message": "GitHub live-state checks were skipped.", "private_repo": "<redacted-private-corpus-repo>"}
    repo = private_corpus_repo(env)
    if not repo:
        return {"status": "fail", "message": "ROCK_KB_PRIVATE_CORPUS_REPO is not configured.", "private_repo": "<redacted-private-corpus-repo>"}
    workflows = run_json(["gh", "api", f"repos/{repo}/actions/workflows"], run_command)
    if workflows["status"] != "ok":
        return {"status": "fail", "message": "Private corpus workflow lookup failed.", "private_repo": "<redacted-private-corpus-repo>"}
    workflow_rows = workflows["data"].get("workflows") or []
    workflow = next((row for row in workflow_rows if row.get("path") == ".github/workflows/private-corpus-ingest.yml"), None)
    if not workflow or workflow.get("state") != "active":
        return {"status": "fail", "message": "Private Corpus Ingest workflow is not active.", "private_repo": "<redacted-private-corpus-repo>"}
    runs = run_json(
        [
            "gh",
            "run",
            "list",
            "--repo",
            repo,
            "--workflow",
            "Private Corpus Ingest",
            "--limit",
            "5",
            "--json",
            "databaseId,status,conclusion,event,createdAt,headSha",
        ],
        run_command,
    )
    if runs["status"] != "ok":
        return {"status": "fail", "message": "Private corpus workflow run lookup failed.", "private_repo": "<redacted-private-corpus-repo>"}
    run_rows = runs["data"] if isinstance(runs["data"], list) else []
    successful = [row for row in run_rows if row.get("status") == "completed" and row.get("conclusion") == "success"]
    if not successful:
        return {
            "status": "fail",
            "message": "Private Corpus Ingest workflow has no recent successful run.",
            "private_repo": "<redacted-private-corpus-repo>",
            "workflow_state": workflow.get("state"),
            "recent_run_count": len(run_rows),
        }
    latest = successful[0]
    return {
        "status": "pass",
        "message": "Private Corpus Ingest workflow is active and has a recent successful run.",
        "private_repo": "<redacted-private-corpus-repo>",
        "workflow_state": workflow.get("state"),
        "latest_success": {
            "databaseId": latest.get("databaseId"),
            "event": latest.get("event"),
            "createdAt": latest.get("createdAt"),
            "headSha": latest.get("headSha"),
        },
    }


def hosted_service_check(env: dict[str, str], repo: str, run_command: RunCommand, *, check_github: bool) -> dict[str, Any]:
    base_url = hosted_service_base_url(env, repo, run_command, check_github=check_github)
    if not base_url:
        return check(
            "hosted_service",
            "fail",
            "No hosted service base URL is configured, so the live read service cannot be verified.",
            {"expected_env_or_variable": "ROCK_KB_BASE_URL"},
        )
    probes = [
        ["curl", "--fail", "--silent", f"{base_url.rstrip('/')}/health"],
        ["curl", "--fail", "--silent", f"{base_url.rstrip('/')}/operations/dashboard"],
        ["uv", "run", "kb", "eval-service", "--base-url", base_url.rstrip("/"), "--limit", "5"],
    ]
    failures = []
    for command in probes:
        result = run_command(command)
        if result.returncode != 0:
            failures.append(
                {
                    "command": command,
                    "returncode": result.returncode,
                    "stdout_tail": result.stdout[-500:],
                    "stderr_tail": result.stderr[-500:],
                }
            )
    return check(
        "hosted_service",
        "pass" if not failures else "fail",
        "Hosted read service health, operations dashboard, and evaluation gate pass."
        if not failures
        else "Hosted read service health, operations dashboard, or evaluation gate failed.",
        {"base_url": base_url, "failures": failures},
    )


def hosted_service_base_url(env: dict[str, str], repo: str, run_command: RunCommand, *, check_github: bool) -> str:
    value = (env.get("ROCK_KB_BASE_URL") or "").strip()
    if value or not check_github:
        return value
    variables = github_variable_values(repo, run_command)
    return variables.get("ROCK_KB_BASE_URL", "").strip()


def pr_review_gate_check(repo: str, pr: int | None, run_command: RunCommand) -> dict[str, Any]:
    if pr is None:
        return check("pr_review_gate", "fail", "No PR number was provided for merge-readiness verification.", {})
    result = run_json(["gh", "pr", "view", str(pr), "--repo", repo, "--json", "state,mergeable,reviewDecision,statusCheckRollup,url,mergedAt"], run_command)
    if result["status"] != "ok":
        return result
    data = result["data"]
    checks = data.get("statusCheckRollup") or []
    failing = [row.get("name") for row in checks if row.get("conclusion") not in {"SUCCESS", "SKIPPED"} or row.get("status") != "COMPLETED"]
    review_decision = data.get("reviewDecision")
    mergeable = data.get("mergeable")
    state = data.get("state")
    merged = state == "MERGED"
    open_ready = state == "OPEN" and mergeable == "MERGEABLE" and review_decision == "APPROVED" and not failing
    passed = merged or open_ready
    return check(
        "pr_review_gate",
        "pass" if passed else "fail",
        "Milestone PR is merged."
        if merged
        else "Milestone PR is approved, mergeable, and checks are green."
        if open_ready
        else "Milestone PR is not yet approved/merge-complete.",
        {
            "url": data.get("url"),
            "state": state,
            "mergeable": mergeable,
            "reviewDecision": review_decision,
            "mergedAt": data.get("mergedAt"),
            "non_green_checks": failing,
            "required_action": pr_required_action(state, review_decision, failing),
        },
    )


def pr_required_action(state: str | None, review_decision: str | None, failing: list[str]) -> str:
    if state == "MERGED":
        return ""
    if state == "CLOSED":
        return "Reopen or replace the milestone PR, then approve and merge it."
    if failing:
        return "Make the milestone PR checks green."
    if review_decision == "REVIEW_REQUIRED":
        return "Have a non-author reviewer approve and merge the PR."
    if review_decision != "APPROVED":
        return "Approve and merge the milestone PR."
    return "Merge the approved milestone PR."


def github_deploy_configuration_check(repo: str, run_command: RunCommand) -> dict[str, Any]:
    secrets = set(list_names(["gh", "secret", "list", "--repo", repo, "--env", "production"], run_command))
    variables = set(list_names(["gh", "variable", "list", "--repo", repo, "--env", "production"], run_command))
    variables.update(list_names(["gh", "variable", "list", "--repo", repo], run_command))
    required_secrets = {"CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID", "ROCK_KB_WORKER_GITHUB_TOKEN", "ORG_TOKEN_SHA256_JSON"}
    required_variables = {"ROCK_KB_D1_DATABASE_ID", "ROCK_KB_BASE_URL"}
    missing_secrets = sorted(required_secrets - secrets)
    missing_variables = sorted(required_variables - variables)
    status = "pass" if not missing_secrets and not missing_variables else "fail"
    return check(
        "github_deploy_configuration",
        status,
        "Production deploy secrets and variables are configured."
        if status == "pass"
        else "Production deploy secrets or variables are missing.",
        {
            "missing_secrets": missing_secrets,
            "missing_variables": missing_variables,
            "optional_variables": ["ROCK_KB_D1_DATABASE", "ROCK_KB_R2_BUCKET"],
        },
    )


def github_variable_values(repo: str, run_command: RunCommand) -> dict[str, str]:
    values: dict[str, str] = {}
    for command in [
        ["gh", "variable", "list", "--repo", repo, "--env", "production"],
        ["gh", "variable", "list", "--repo", repo],
    ]:
        result = run_command(command)
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0]:
                values.setdefault(parts[0], parts[1])
    return values


def github_auto_merge_check(repo: str, run_command: RunCommand) -> dict[str, Any]:
    result = run_json(["gh", "api", f"repos/{repo}"], run_command)
    if result["status"] != "ok":
        return result
    allow_auto_merge = bool(result["data"].get("allow_auto_merge"))
    return check(
        "github_auto_merge_policy",
        "pass" if allow_auto_merge else "fail",
        "Repository auto-merge is enabled." if allow_auto_merge else "Repository auto-merge is not enabled.",
        {
            "allow_auto_merge": allow_auto_merge,
            "required_action": "Enable auto-merge only after a GitHub App or equivalent server-side path gate enforces per-org intake boundaries."
            if not allow_auto_merge
            else "",
        },
    )


def run_json(command: list[str], run_command: RunCommand) -> dict[str, Any]:
    result = run_command(command)
    if result.returncode != 0:
        return check(command[-1] if command else "command", "fail", "Live command failed.", {"command": command, "stderr": result.stderr})
    try:
        return {"status": "ok", "data": json.loads(result.stdout or "{}")}
    except json.JSONDecodeError as exc:
        return check("json_command", "fail", "Live command returned invalid JSON.", {"command": command, "error": str(exc)})


def list_names(command: list[str], run_command: RunCommand) -> list[str]:
    result = run_command(command)
    if result.returncode != 0:
        return []
    names = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if parts:
            names.append(parts[0])
    return names


def default_run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    timeout_seconds = int(os.environ.get("ROCK_KB_NETWORK_READINESS_TIMEOUT", "45"))
    try:
        return subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
            stderr=f"Command timed out after {timeout_seconds}s: {' '.join(command)}",
        )


def env_private_corpus_path(env: dict[str, str]) -> Path | None:
    value = env.get("ROCK_KB_PRIVATE_CORPUS_PATH") or env.get("PRIVATE_CORPUS_PATH")
    return Path(value).expanduser() if value else None


def private_corpus_repo(env: dict[str, str]) -> str:
    return env.get("ROCK_KB_PRIVATE_CORPUS_REPO") or env.get("PRIVATE_CORPUS_REPO") or ""


def readiness_status(checks: list[dict[str, Any]]) -> str:
    if any(row["status"] == "fail" for row in checks):
        return "fail"
    if any(row["status"] == "warn" for row in checks):
        return "incomplete"
    return "pass"


def readiness_summary(checks: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "pass": sum(1 for row in checks if row["status"] == "pass"),
        "warn": sum(1 for row in checks if row["status"] == "warn"),
        "fail": sum(1 for row in checks if row["status"] == "fail"),
    }


def check(check_id: str, status: str, message: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"id": check_id, "status": status, "message": message, "evidence": evidence or {}}
