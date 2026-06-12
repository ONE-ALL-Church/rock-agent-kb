from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import request

from .validator import validate_bundle

DEFAULT_BASE_URL = "https://rock-agent-kb.oneandall.church"


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

    subparsers.add_parser("manifest")
    subparsers.add_parser("dashboard")

    validate = subparsers.add_parser("validate")
    validate.add_argument("bundle", type=Path)

    submit = subparsers.add_parser("submit")
    submit.add_argument("bundle", type=Path)
    submit.add_argument("--org", required=True)

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
    if args.command == "submit":
        errors = validate_bundle(args.bundle)
        if errors:
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        token = os.environ.get("ROCK_KB_TOKEN")
        if not token:
            print("ERROR ROCK_KB_TOKEN is required for submit", file=sys.stderr)
            return 1
        rows = [json.loads(line) for line in args.bundle.read_text(encoding="utf-8").splitlines() if line.strip()]
        return print_json(post_json(f"{base_url}/submit", {"org_id": args.org, "bundle": rows}, token=token))
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


def get_json(url: str):
    return json.loads(get_text(url))


def get_text(url: str) -> str:
    with request.urlopen(url) as response:
        return response.read().decode("utf-8")


def post_json(url: str, payload: dict, token: str):
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={"content-type": "application/json", "authorization": f"Bearer {token}"},
    )
    with request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


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
