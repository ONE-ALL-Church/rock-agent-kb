#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


Runner = Callable[[list[str], Path | None], subprocess.CompletedProcess[str]]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap private corpus GitHub and Cloudflare automation settings.")
    parser.add_argument("--repo", default=os.environ.get("PRIVATE_CORPUS_REPO", ""), help="Private corpus GitHub repo owner/name.")
    parser.add_argument("--bucket", default=os.environ.get("PRIVATE_R2_BUCKET", ""), help="Private R2 bucket for media binaries.")
    parser.add_argument("--account-id", default=os.environ.get("CLOUDFLARE_ACCOUNT_ID", ""), help="Cloudflare account id.")
    parser.add_argument("--location", default="wnam", help="Cloudflare location hint for a newly-created R2 bucket.")
    parser.add_argument("--service-dir", default="service", help="Path to the Worker project for Wrangler commands.")
    parser.add_argument("--workflow", default="private-corpus-ingest.yml", help="Private corpus ingest workflow filename.")
    parser.add_argument("--dispatch", action="store_true", help="Trigger the private ingest workflow after settings are written.")
    parser.add_argument("--run-media-batch", action="store_true", help="When dispatching, run one hosted media transcription item.")
    parser.add_argument("--media-source", default="rock_podcast_rss", help="Media source for optional workflow dispatch.")
    parser.add_argument("--media-limit", default="1", help="Media limit for optional workflow dispatch.")
    parser.add_argument("--apply", action="store_true", help="Create/update settings. Defaults to dry-run.")
    args = parser.parse_args(argv[1:])

    result = bootstrap_private_corpus_infra(
        repo=args.repo,
        bucket=args.bucket,
        account_id=args.account_id,
        location=args.location,
        service_dir=Path(args.service_dir),
        workflow=args.workflow,
        dispatch=args.dispatch,
        run_media_batch=args.run_media_batch,
        media_source=args.media_source,
        media_limit=args.media_limit,
        apply=args.apply,
        env=dict(os.environ),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"ok", "dry_run"} else 1


def bootstrap_private_corpus_infra(
    *,
    repo: str,
    bucket: str,
    account_id: str,
    location: str,
    service_dir: Path,
    workflow: str,
    dispatch: bool,
    run_media_batch: bool,
    media_source: str,
    media_limit: str,
    apply: bool,
    env: dict[str, str],
    run: Runner | None = None,
) -> dict[str, Any]:
    runner = run or run_command
    planned = planned_commands(repo, bucket, account_id, location, workflow, dispatch, run_media_batch, media_source, media_limit)
    if not apply:
        return {"schema": "rock-kb-private-corpus-bootstrap-v1", "status": "dry_run", "planned_commands": planned}

    errors: list[str] = []
    if not repo:
        errors.append("--repo or PRIVATE_CORPUS_REPO is required.")
    if not bucket:
        errors.append("--bucket or PRIVATE_R2_BUCKET is required.")
    if not account_id:
        errors.append("--account-id or CLOUDFLARE_ACCOUNT_ID is required.")
    if not env.get("CLOUDFLARE_API_TOKEN"):
        errors.append("CLOUDFLARE_API_TOKEN is required in the environment; GitHub secret was not written.")
    if errors:
        return {"schema": "rock-kb-private-corpus-bootstrap-v1", "status": "fail", "errors": errors}

    ensure_r2_bucket(bucket, location, service_dir, runner, errors)
    set_github_variable(repo, "CLOUDFLARE_ACCOUNT_ID", account_id, runner, errors)
    set_github_variable(repo, "PRIVATE_R2_BUCKET", bucket, runner, errors)
    set_github_secret(repo, "CLOUDFLARE_API_TOKEN", env["CLOUDFLARE_API_TOKEN"], runner, errors)
    if dispatch:
        dispatch_private_ingest(repo, workflow, run_media_batch, media_source, media_limit, runner, errors)
    return {
        "schema": "rock-kb-private-corpus-bootstrap-v1",
        "status": "fail" if errors else "ok",
        "repo": "<redacted-private-corpus-repo>",
        "bucket": bucket,
        "workflow_dispatched": dispatch and not errors,
        "errors": errors,
    }


def planned_commands(
    repo: str,
    bucket: str,
    account_id: str,
    location: str,
    workflow: str,
    dispatch: bool,
    run_media_batch: bool,
    media_source: str,
    media_limit: str,
) -> list[str]:
    repo_label = repo or "<private-corpus-repo>"
    bucket_label = bucket or "<private-r2-bucket>"
    account_label = account_id or "<cloudflare-account-id>"
    commands = [
        f"cd service && npx wrangler r2 bucket create {bucket_label} --location {location} # skipped if it already exists",
        f"gh variable set CLOUDFLARE_ACCOUNT_ID --repo {repo_label} --body {account_label}",
        f"gh variable set PRIVATE_R2_BUCKET --repo {repo_label} --body {bucket_label}",
        f"gh secret set CLOUDFLARE_API_TOKEN --repo {repo_label} --body \"$CLOUDFLARE_API_TOKEN\"",
    ]
    if dispatch:
        commands.append(
            "gh workflow run "
            f"{workflow} --repo {repo_label} "
            f"-f run_media_batch={'true' if run_media_batch else 'false'} "
            f"-f media_source={media_source} -f media_limit={media_limit} "
            "-f transcribe_tool=cloudflare -f transcribe_model=auto"
        )
    return commands


def ensure_r2_bucket(bucket: str, location: str, service_dir: Path, run: Runner, errors: list[str]) -> None:
    listing = run(["npx", "wrangler", "r2", "bucket", "list"], service_dir)
    if listing.returncode == 0 and bucket in listing.stdout:
        return
    created = run(["npx", "wrangler", "r2", "bucket", "create", bucket, "--location", location], service_dir)
    if created.returncode != 0:
        errors.append(f"wrangler r2 bucket create failed: {created.stderr.strip()}")


def set_github_variable(repo: str, name: str, value: str, run: Runner, errors: list[str]) -> None:
    result = run(["gh", "variable", "set", name, "--repo", repo, "--body", value], None)
    if result.returncode != 0:
        errors.append(f"gh variable set {name} failed: {result.stderr.strip()}")


def set_github_secret(repo: str, name: str, value: str, run: Runner, errors: list[str]) -> None:
    result = run(["gh", "secret", "set", name, "--repo", repo, "--body", value], None)
    if result.returncode != 0:
        errors.append(f"gh secret set {name} failed: {result.stderr.strip()}")


def dispatch_private_ingest(
    repo: str,
    workflow: str,
    run_media_batch: bool,
    media_source: str,
    media_limit: str,
    run: Runner,
    errors: list[str],
) -> None:
    result = run(
        [
            "gh",
            "workflow",
            "run",
            workflow,
            "--repo",
            repo,
            "-f",
            f"run_media_batch={'true' if run_media_batch else 'false'}",
            "-f",
            f"media_source={media_source}",
            "-f",
            f"media_limit={media_limit}",
            "-f",
            "transcribe_tool=cloudflare",
            "-f",
            "transcribe_model=auto",
        ],
        None,
    )
    if result.returncode != 0:
        errors.append(f"gh workflow run {workflow} failed: {result.stderr.strip()}")


def run_command(command: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
