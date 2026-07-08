from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import error, request

from .validator import validate_bundle

DEFAULT_BASE_URL = "https://rock-agent-kb.oneandall.church"
USER_AGENT = "rock-kb-client/0.1.2 (+https://github.com/ONE-ALL-Church/rock-agent-kb)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rock-kb")
    parser.add_argument("--url", default=os.environ.get("ROCK_KB_URL", DEFAULT_BASE_URL), help="Rock KB service base URL")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--min-tier", default="routing_context_only")

    subparsers.add_parser("concepts")
    get = subparsers.add_parser("get")
    get.add_argument("concept_id")

    claims = subparsers.add_parser("claims")
    claims.add_argument("concept_id")
    claims.add_argument("--tier")
    claims.add_argument("--min-tier", default="routing_context_only")

    model = subparsers.add_parser("model")
    model.add_argument("model")
    model.add_argument("--fields")
    model.add_argument("--property")
    model.add_argument("--format", choices=["json", "markdown"], default="json")

    model_map = subparsers.add_parser("model-map")
    model_map_subparsers = model_map.add_subparsers(dest="model_map_command", required=True)
    model_map_subparsers.add_parser("list")
    model_map_get = model_map_subparsers.add_parser("get")
    model_map_get.add_argument("model")
    model_map_get.add_argument("--fields")
    model_map_get.add_argument("--property")
    model_map_get.add_argument("--format", choices=["json", "markdown"], default="json")

    subparsers.add_parser("manifest")
    subparsers.add_parser("dashboard")

    validate = subparsers.add_parser("validate")
    validate.add_argument("bundle", type=Path)

    auth_check = subparsers.add_parser("auth-check")
    auth_check.add_argument("--org", required=True)
    add_token_options(auth_check)

    submit = subparsers.add_parser("submit")
    submit.add_argument("bundle", type=Path)
    submit.add_argument("--org", help="Defaults to the org_id in the bundle when every row has the same org_id.")
    submit.add_argument("--dry-run", action="store_true", help="Validate hosted auth and bundle without opening a PR.")
    add_token_options(submit)

    subparsers.add_parser("mcp-config")

    args = parser.parse_args(argv)
    base_url = str(args.url).rstrip("/")

    if args.command == "search":
        return print_json(get_json(f"{base_url}/search?q={quote(args.query)}&limit={args.limit}&min_tier={quote(args.min_tier)}"))
    if args.command == "concepts":
        return print_json(get_json(f"{base_url}/concepts"))
    if args.command == "get":
        return print_text(get_text(f"{base_url}/concepts/{quote(args.concept_id)}.md"))
    if args.command == "claims":
        suffix = f"?min_tier={quote(args.min_tier)}"
        if args.tier:
            suffix += f"&tier={quote(args.tier)}"
        return print_json(get_json(f"{base_url}/claims/{quote(args.concept_id)}{suffix}"))
    if args.command == "model":
        return print_model(base_url, args.model, args.fields, args.property, args.format)
    if args.command == "model-map":
        if args.model_map_command == "list":
            return print_json(get_json(f"{base_url}/model-map/models"))
        if args.model_map_command == "get":
            return print_model(base_url, args.model, args.fields, args.property, args.format)
    if args.command == "manifest":
        return print_json(get_json(f"{base_url}/manifest.json"))
    if args.command == "dashboard":
        return print_json(get_json(f"{base_url}/operations/dashboard"))
    if args.command == "validate":
        errors = validate_bundle(args.bundle)
        if errors:
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        return print_json({"status": "ok", "file": str(args.bundle)})
    if args.command == "auth-check":
        token = resolve_token(args)
        if not token:
            print(missing_token_message(args.org), file=sys.stderr)
            return 1
        return print_json(post_json(f"{base_url}/auth/check", {"org_id": args.org}, token=token))
    if args.command == "submit":
        errors = validate_bundle(args.bundle)
        if errors:
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        rows = [json.loads(line) for line in args.bundle.read_text(encoding="utf-8").splitlines() if line.strip()]
        org_id = args.org or infer_org_id(rows)
        if not org_id:
            print("ERROR --org is required when bundle rows do not all use the same org_id", file=sys.stderr)
            return 1
        token = resolve_token(args)
        if not token:
            print(missing_token_message(org_id), file=sys.stderr)
            return 1
        return print_json(post_json(f"{base_url}/submit", {"org_id": org_id, "bundle": rows, "dry_run": bool(args.dry_run)}, token=token))
    if args.command == "mcp-config":
        return print_json(
            {
                "mcpServers": {
                    "rock-kb": {
                        "type": "http",
                        "url": f"{base_url}/mcp"
                    }
                }
            }
        )
    return 1


def add_token_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--token-file", type=Path, help="Read the submit token from a secret-mounted file.")
    parser.add_argument("--token-stdin", action="store_true", help="Read the submit token from stdin.")


def resolve_token(args) -> str:
    if getattr(args, "token_stdin", False):
        return sys.stdin.read().strip()
    token_file = getattr(args, "token_file", None) or (Path(os.environ["ROCK_KB_TOKEN_FILE"]) if os.environ.get("ROCK_KB_TOKEN_FILE") else None)
    if token_file:
        return token_file.read_text(encoding="utf-8").strip()
    return os.environ.get("ROCK_KB_TOKEN", "").strip()


def infer_org_id(rows: list[dict]) -> str:
    org_ids = {str(row.get("org_id") or "") for row in rows}
    org_ids.discard("")
    return next(iter(org_ids)) if len(org_ids) == 1 else ""


def missing_token_message(org_id: str) -> str:
    return (
        "ERROR hosted submission requires a per-organization submit token.\n"
        f"Org: {org_id}\n"
        "Ask a Rock KB maintainer to review orgs/<org-id>.yaml and issue or rotate a token outside git.\n"
        "Provide it to this command with ROCK_KB_TOKEN, ROCK_KB_TOKEN_FILE, --token-file, or --token-stdin."
    )


def print_model(base_url: str, model: str, fields: str | None, property_name: str | None, format_name: str) -> int:
    params = []
    if fields:
        params.append(f"fields={quote(fields)}")
    if property_name:
        params.append(f"property={quote(property_name)}")
    if format_name:
        params.append(f"format={quote(format_name)}")
    suffix = f"?{'&'.join(params)}" if params else ""
    url = f"{base_url}/model-map/models/{quote(model)}{suffix}"
    if format_name == "markdown":
        return print_text(get_text(url))
    return print_json(get_json(url))


def get_json(url: str):
    return json.loads(get_text(url))


def get_text(url: str) -> str:
    req = request.Request(url, headers={"user-agent": USER_AGENT})
    with request.urlopen(req) as response:
        return response.read().decode("utf-8")


def post_json(url: str, payload: dict, token: str):
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "user-agent": USER_AGENT,
            "accept": "application/json",
        },
    )
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def quote(value: str) -> str:
    from urllib.parse import quote as url_quote

    return url_quote(value, safe="")


def print_json(value) -> int:
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


def print_text(value: str) -> int:
    print(value, end="" if value.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
