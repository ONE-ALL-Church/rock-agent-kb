#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


Runner = Callable[[list[str], Path | None], subprocess.CompletedProcess[str]]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Cloudflare and GitHub settings for the hosted Rock KB service.")
    parser.add_argument("--repo", default="ONE-ALL-Church/rock-agent-kb", help="GitHub repo owner/name.")
    parser.add_argument("--environment", default="production", help="GitHub environment and Wrangler environment.")
    parser.add_argument("--database", default="rock-agent-kb", help="D1 database name.")
    parser.add_argument("--bucket", default="rock-agent-kb-artifacts", help="R2 bucket name.")
    parser.add_argument("--base-url", default="https://rock-agent-kb.oneandall.church", help="Hosted service base URL.")
    parser.add_argument("--location", default="wnam", help="Cloudflare location hint for new D1/R2 resources.")
    parser.add_argument("--service-dir", default="service", help="Path to the Worker project.")
    parser.add_argument("--apply", action="store_true", help="Create resources and set GitHub settings. Defaults to dry-run.")
    args = parser.parse_args(argv[1:])

    result = bootstrap_service_infra(
        repo=args.repo,
        environment=args.environment,
        database=args.database,
        bucket=args.bucket,
        base_url=args.base_url,
        location=args.location,
        service_dir=Path(args.service_dir),
        apply=args.apply,
        env=dict(os.environ),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"ok", "dry_run"} else 1


def bootstrap_service_infra(
    *,
    repo: str,
    environment: str,
    database: str,
    bucket: str,
    base_url: str,
    location: str,
    service_dir: Path,
    apply: bool,
    env: dict[str, str],
    run: Runner | None = None,
) -> dict[str, Any]:
    runner = run or run_command
    planned = planned_commands(repo, environment, database, bucket, base_url, location)
    if not apply:
        return {"schema": "rock-kb-service-bootstrap-v1", "status": "dry_run", "planned_commands": planned}

    errors: list[str] = []
    d1_id = ensure_d1_database(database, location, service_dir, runner, errors)
    ensure_r2_bucket(bucket, location, service_dir, runner, errors)
    if d1_id:
        set_github_variable(repo, environment, "ROCK_KB_D1_DATABASE_ID", d1_id, runner, errors)
    set_github_variable(repo, environment, "ROCK_KB_D1_DATABASE", database, runner, errors)
    set_github_variable(repo, environment, "ROCK_KB_R2_BUCKET", bucket, runner, errors)
    set_github_variable(repo, environment, "ROCK_KB_BASE_URL", base_url, runner, errors)
    maybe_set_github_secret(repo, environment, "CLOUDFLARE_API_TOKEN", env, runner, errors)
    maybe_set_github_secret(repo, environment, "CLOUDFLARE_ACCOUNT_ID", env, runner, errors)
    maybe_set_github_secret(repo, environment, "ROCK_KB_WORKER_GITHUB_TOKEN", env, runner, errors)
    maybe_set_github_secret(repo, environment, "ORG_TOKEN_SHA256_JSON", env, runner, errors)
    return {
        "schema": "rock-kb-service-bootstrap-v1",
        "status": "fail" if errors else "ok",
        "d1_database_id": d1_id,
        "errors": errors,
    }


def planned_commands(repo: str, environment: str, database: str, bucket: str, base_url: str, location: str) -> list[str]:
    return [
        f"cd service && npx wrangler d1 create {database} --location {location}",
        f"cd service && npx wrangler r2 bucket create {bucket} --location {location}",
        f"gh variable set ROCK_KB_D1_DATABASE_ID --repo {repo} --env {environment} --body <d1-database-id>",
        f"gh variable set ROCK_KB_D1_DATABASE --repo {repo} --env {environment} --body {database}",
        f"gh variable set ROCK_KB_R2_BUCKET --repo {repo} --env {environment} --body {bucket}",
        f"gh variable set ROCK_KB_BASE_URL --repo {repo} --env {environment} --body {base_url}",
        f"gh secret set CLOUDFLARE_API_TOKEN --repo {repo} --env {environment} --body \"$CLOUDFLARE_API_TOKEN\"",
        f"gh secret set CLOUDFLARE_ACCOUNT_ID --repo {repo} --env {environment} --body \"$CLOUDFLARE_ACCOUNT_ID\"",
        f"gh secret set ROCK_KB_WORKER_GITHUB_TOKEN --repo {repo} --env {environment} --body \"$ROCK_KB_WORKER_GITHUB_TOKEN\"",
        f"gh secret set ORG_TOKEN_SHA256_JSON --repo {repo} --env {environment} --body \"$ORG_TOKEN_SHA256_JSON\"",
    ]


def ensure_d1_database(database: str, location: str, service_dir: Path, run: Runner, errors: list[str]) -> str:
    listing = run(["npx", "wrangler", "d1", "list", "--json"], service_dir)
    if listing.returncode == 0:
        for row in parse_json_list(listing.stdout):
            if str(row.get("name") or "") == database:
                database_id = str(row.get("uuid") or row.get("id") or "")
                if database_id:
                    return database_id
    created = run(["npx", "wrangler", "d1", "create", database, "--location", location], service_dir)
    if created.returncode != 0:
        errors.append(f"wrangler d1 create failed: {created.stderr.strip()}")
        return ""
    database_id = parse_uuid(created.stdout)
    if not database_id:
        errors.append("Could not parse D1 database id from wrangler output.")
    return database_id


def ensure_r2_bucket(bucket: str, location: str, service_dir: Path, run: Runner, errors: list[str]) -> None:
    listing = run(["npx", "wrangler", "r2", "bucket", "list"], service_dir)
    if listing.returncode == 0 and bucket in listing.stdout:
        return
    created = run(["npx", "wrangler", "r2", "bucket", "create", bucket, "--location", location], service_dir)
    if created.returncode != 0:
        errors.append(f"wrangler r2 bucket create failed: {created.stderr.strip()}")


def set_github_variable(repo: str, environment: str, name: str, value: str, run: Runner, errors: list[str]) -> None:
    result = run(["gh", "variable", "set", name, "--repo", repo, "--env", environment, "--body", value], None)
    if result.returncode != 0:
        errors.append(f"gh variable set {name} failed: {result.stderr.strip()}")


def maybe_set_github_secret(repo: str, environment: str, name: str, env: dict[str, str], run: Runner, errors: list[str]) -> None:
    value = env.get(name)
    if not value:
        errors.append(f"{name} not set in environment; GitHub secret was not written.")
        return
    result = run(["gh", "secret", "set", name, "--repo", repo, "--env", environment, "--body", value], None)
    if result.returncode != 0:
        errors.append(f"gh secret set {name} failed: {result.stderr.strip()}")


def parse_json_list(value: str) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, list):
        return [row for row in parsed if isinstance(row, dict)]
    if isinstance(parsed, dict) and isinstance(parsed.get("result"), list):
        return [row for row in parsed["result"] if isinstance(row, dict)]
    return []


def parse_uuid(value: str) -> str:
    match = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", value)
    return match.group(0) if match else ""


def run_command(command: list[str], cwd: Path | None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
