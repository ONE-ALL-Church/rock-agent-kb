#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from urllib import request


DEFAULT_EXPECTED_COMMIT = "3fcbb9f828c2f23d109c855ee403c3a4c81f3a96"
COMMITS_URL = (
    "https://api.github.com/repos/GoogleCloudPlatform/knowledge-catalog/commits"
    "?path=okf/SPEC.md&per_page=1"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect upstream OKF specification changes.")
    parser.add_argument("--expected", default=DEFAULT_EXPECTED_COMMIT)
    args = parser.parse_args()

    req = request.Request(
        COMMITS_URL,
        headers={
            "accept": "application/vnd.github+json",
            "user-agent": "rock-agent-kb-okf-monitor/1",
        },
    )
    with request.urlopen(req, timeout=30) as response:
        rows = json.loads(response.read().decode("utf-8"))
    current = str(rows[0].get("sha") or "") if rows else ""
    status = "current" if current == args.expected else "review_required"
    print(
        json.dumps(
            {
                "schema": "rock-kb-okf-upstream-check-v1",
                "status": status,
                "expected_commit": args.expected,
                "current_commit": current,
                "spec_url": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if status == "current" else 1


if __name__ == "__main__":
    raise SystemExit(main())
