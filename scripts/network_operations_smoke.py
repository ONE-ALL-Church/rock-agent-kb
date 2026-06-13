#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any, Callable


SCHEMA = "rock-kb-network-operations-smoke-v1"
EXPECTED_MCP_TOOLS = {"kb_search", "kb_get_claims", "kb_submit", "kb_review_dashboard"}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run public hosted-service smoke checks for the Rock KB network operations path.")
    parser.add_argument("--base-url", required=True, help="Hosted Rock KB service base URL.")
    parser.add_argument("--limit", type=int, default=5, help="Hosted eval result limit.")
    args = parser.parse_args(argv[1:])

    result = network_operations_smoke(args.base_url, limit=args.limit)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


def network_operations_smoke(
    base_url: str,
    *,
    limit: int = 5,
    evaluator: Callable[[str, int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    base = base_url.rstrip("/")
    checks = [
        get_json_check("health", f"{base}/health"),
        get_json_check("manifest", f"{base}/manifest.json"),
        get_json_check("operations_dashboard", f"{base}/operations/dashboard"),
        mcp_tools_check(base),
        unauthorized_submit_check(base),
        hosted_eval_check(base, limit, evaluator=evaluator),
    ]
    failures = [row for row in checks if row["status"] != "pass"]
    return {
        "schema": SCHEMA,
        "status": "fail" if failures else "ok",
        "base_url": base,
        "checks": checks,
    }


def get_json_check(name: str, url: str) -> dict[str, Any]:
    try:
        payload = fetch_json(url)
    except Exception as exc:
        return check(name, "fail", str(exc))
    return check(name, "pass", "ok", {"keys": sorted(payload)[:10] if isinstance(payload, dict) else []})


def mcp_tools_check(base_url: str) -> dict[str, Any]:
    try:
        payload = post_json(f"{base_url}/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    except Exception as exc:
        return check("mcp_tools", "fail", str(exc))
    tools = ((payload.get("result") or {}).get("tools") or []) if isinstance(payload, dict) else []
    tool_names = {tool.get("name") for tool in tools if isinstance(tool, dict)}
    missing = sorted(EXPECTED_MCP_TOOLS - tool_names)
    if missing:
        return check("mcp_tools", "fail", f"missing tools: {', '.join(missing)}", {"tool_names": sorted(tool_names)})
    return check("mcp_tools", "pass", "ok", {"tool_names": sorted(tool_names)})


def unauthorized_submit_check(base_url: str) -> dict[str, Any]:
    try:
        payload = post_json(f"{base_url}/submit", {"org_id": "network-ops-smoke", "bundle": []})
    except Exception as exc:
        return check("unauthorized_submit", "fail", str(exc))
    errors = payload.get("errors") or [] if isinstance(payload, dict) else []
    if isinstance(payload, dict) and payload.get("status") == "rejected" and "unauthorized org token" in errors:
        return check("unauthorized_submit", "pass", "ok")
    return check("unauthorized_submit", "fail", "unexpected submit response", {"response": payload})


def hosted_eval_check(base_url: str, limit: int, evaluator: Callable[[str, int], dict[str, Any]] | None = None) -> dict[str, Any]:
    try:
        result = (evaluator or evaluate_hosted_search)(base_url, limit)
    except Exception as exc:
        return check("hosted_eval", "fail", str(exc))
    if result.get("status") != "ok":
        return check(
            "hosted_eval",
            "fail",
            "hosted eval failed",
            {"pass_count": result.get("pass_count"), "fail_count": result.get("fail_count")},
        )
    return check("hosted_eval", "pass", "ok", {"pass_count": result.get("pass_count"), "fail_count": result.get("fail_count")})


def evaluate_hosted_search(base_url: str, limit: int) -> dict[str, Any]:
    from rock_kb.service_eval import evaluate_service

    return evaluate_service(base_url=base_url, limit=limit).as_dict()


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"user-agent": "rock-kb-network-operations/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, payload: dict[str, Any]) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json", "user-agent": "rock-kb-network-operations/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        raise RuntimeError(f"HTTP {exc.code}: {body[:500]}") from exc


def check(name: str, status: str, message: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"name": name, "status": status, "message": message, "evidence": evidence or {}}


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
