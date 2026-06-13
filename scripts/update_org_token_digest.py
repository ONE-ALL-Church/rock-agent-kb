#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


ORG_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,62}[a-z0-9]$")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Add or update one org token SHA-256 digest in ORG_TOKEN_SHA256_JSON without printing the raw token."
    )
    parser.add_argument("--org-id", required=True, help="Reviewed org id from orgs/<org-id>.yaml.")
    parser.add_argument("--existing-json", default="", help="Existing ORG_TOKEN_SHA256_JSON value. Defaults to {}.")
    parser.add_argument("--existing-json-file", type=Path, help="File containing the existing ORG_TOKEN_SHA256_JSON value.")
    parser.add_argument("--token-env", default="", help="Read the raw token from this environment variable.")
    parser.add_argument("--output-file", type=Path, help="Write updated JSON to this file instead of stdout.")
    args = parser.parse_args(argv[1:])

    try:
        updated = update_digest_json(
            org_id=args.org_id,
            token=read_token(args.token_env),
            existing_json=read_existing_json(args.existing_json, args.existing_json_file),
        )
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    body = json.dumps(updated, sort_keys=True, separators=(",", ":"))
    if args.output_file:
        args.output_file.write_text(body + "\n", encoding="utf-8")
    else:
        print(body)
    return 0


def read_existing_json(existing_json: str, existing_json_file: Path | None) -> str:
    if existing_json_file:
        return existing_json_file.read_text(encoding="utf-8")
    return existing_json or "{}"


def read_token(token_env: str) -> str:
    if token_env:
        token = os.environ.get(token_env, "")
        if not token:
            raise ValueError(f"{token_env} is not set")
        return token
    token = sys.stdin.read()
    if not token:
        raise ValueError("raw token must be provided on stdin or with --token-env")
    return token.rstrip("\n")


def update_digest_json(*, org_id: str, token: str, existing_json: str) -> dict[str, str]:
    if not ORG_ID_PATTERN.match(org_id):
        raise ValueError("org id must be a lowercase slug")
    if not token:
        raise ValueError("raw token is empty")
    if token.strip() != token:
        raise ValueError("raw token has leading or trailing whitespace")
    if len(token) < 24:
        raise ValueError("raw token is too short for a production submit token")
    try:
        parsed: Any = json.loads(existing_json or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"existing JSON is invalid: {exc.msg}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("existing JSON must be an object mapping org ids to SHA-256 digests")
    updated: dict[str, str] = {}
    for key, value in parsed.items():
        if not isinstance(key, str) or not ORG_ID_PATTERN.match(key):
            raise ValueError(f"existing JSON has invalid org id: {key}")
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"existing JSON has invalid SHA-256 digest for {key}")
        updated[key] = value
    updated[org_id] = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return updated


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
