from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .paths import REPO_ROOT


POLICY_PATH = REPO_ROOT / "service" / "shadow-lifecycle.yaml"
REPORT_PATH = REPO_ROOT / "service" / "dist" / "shadow-lifecycle-report.json"


def shadow_lifecycle_report(*, as_of: date | None = None, policy_path: Path = POLICY_PATH) -> dict[str, Any]:
    as_of = as_of or date.today()
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    if policy.get("schema") != "rock-kb-shadow-lifecycle-v1":
        raise ValueError("Unsupported shadow lifecycle policy schema.")
    rows = [instance_lifecycle(row, as_of) for row in policy.get("instances") or []]
    blocking = [row["id"] for row in rows if row["status"] in {"expired", "invalid_production_route"}]
    report = {
        "schema": "rock-kb-shadow-lifecycle-report-v1",
        "as_of": as_of.isoformat(),
        "status": "fail" if blocking else "ok",
        "blocking_instance_ids": blocking,
        "instances": rows,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def instance_lifecycle(row: dict[str, Any], as_of: date) -> dict[str, Any]:
    review_by = parse_date(row.get("review_by"))
    expires_at = parse_date(row.get("expires_at"))
    production_routing = bool(row.get("production_routing"))
    if production_routing:
        status = "invalid_production_route"
    elif as_of >= expires_at:
        status = "expired"
    elif as_of >= review_by:
        status = "review_due"
    else:
        status = "active"
    return {
        **row,
        "created_at": str(row.get("created_at") or ""),
        "review_by": review_by.isoformat(),
        "expires_at": expires_at.isoformat(),
        "days_until_review": (review_by - as_of).days,
        "days_until_expiration": (expires_at - as_of).days,
        "status": status,
    }


def parse_date(value: Any) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"Invalid lifecycle date: {value}") from exc
