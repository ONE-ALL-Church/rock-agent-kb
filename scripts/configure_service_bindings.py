#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure service Cloudflare bindings for a deployment workspace.")
    parser.add_argument("--config", default="service/wrangler.jsonc", help="Path to wrangler JSON config.")
    parser.add_argument("--env", default="production", help="Wrangler environment to update.")
    parser.add_argument("--d1-database", default="rock-agent-kb", help="D1 database name.")
    parser.add_argument("--d1-database-id", required=True, help="D1 database id for the KB_DB binding.")
    parser.add_argument("--r2-bucket", default="rock-agent-kb-artifacts", help="R2 bucket name for the KB_ARTIFACTS binding.")
    args = parser.parse_args()

    path = Path(args.config)
    data = json.loads(path.read_text(encoding="utf-8"))
    update_bindings(data, args.d1_database, args.d1_database_id, args.r2_bucket)
    env_data = data.get("env", {}).get(args.env)
    if isinstance(env_data, dict):
        update_bindings(env_data, args.d1_database, args.d1_database_id, args.r2_bucket)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


def update_bindings(data: dict[str, Any], d1_database: str, d1_database_id: str, r2_bucket: str) -> None:
    for binding in data.get("d1_databases") or []:
        if isinstance(binding, dict) and binding.get("binding") == "KB_DB":
            binding["database_name"] = d1_database
            binding["database_id"] = d1_database_id
    for binding in data.get("r2_buckets") or []:
        if isinstance(binding, dict) and binding.get("binding") == "KB_ARTIFACTS":
            binding["bucket_name"] = r2_bucket


if __name__ == "__main__":
    raise SystemExit(main())
