from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .paths import REPO_ROOT
from .source_workflows import source_workflow_policy


SERVICE_DIR = REPO_ROOT / "service"
SOURCE_FIELDS = (
    "source_id",
    "name",
    "cadence",
    "maximum_age_hours",
    "last_checked_at",
    "content_changed_at",
    "result_count",
    "content_hash",
    "check_status",
    "status",
)


def source_freshness_snapshot(
    report: dict[str, Any],
    *,
    workflow_id: str,
    workflow_max_age_hours: float | None = None,
    run_id: str = "",
    run_url: str = "",
    source_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    if report.get("schema") != "rock-kb-source-freshness-report-v1":
        raise ValueError("Source freshness report has an unsupported schema")
    if not workflow_id or not all(character.isalnum() or character in "_-" for character in workflow_id):
        raise ValueError("workflow_id must be a short structured identifier")
    workflow_policy = source_workflow_policy(workflow_id)
    configured_maximum_age = float(workflow_policy["maximum_age_hours"])
    if workflow_max_age_hours is not None and float(workflow_max_age_hours) != configured_maximum_age:
        raise ValueError(
            f"{workflow_id} maximum age must match the configured value of {configured_maximum_age:g} hours"
        )
    workflow_max_age_hours = configured_maximum_age

    owned = {str(value) for value in workflow_policy["source_ids"]}
    requested = {str(value) for value in source_ids} if source_ids else owned
    foreign = requested - owned
    omitted = owned - requested
    if foreign:
        raise ValueError(
            f"{workflow_id} cannot publish sources owned by another workflow: {', '.join(sorted(foreign))}"
        )
    if omitted:
        raise ValueError(
            f"{workflow_id} snapshot omits owned sources: {', '.join(sorted(omitted))}"
        )
    raw_sources = report.get("sources")
    if not isinstance(raw_sources, list):
        raise ValueError("Source freshness report is missing source rows")
    selected: list[dict[str, Any]] = []
    for value in raw_sources:
        if not isinstance(value, dict):
            raise ValueError("Source freshness rows must be objects")
        source_id = str(value.get("source_id") or "")
        if requested and source_id not in requested:
            continue
        row = {field: value.get(field) for field in SOURCE_FIELDS}
        row["source_id"] = source_id
        row["name"] = str(row.get("name") or source_id)
        row["cadence"] = str(row.get("cadence") or "")
        row["last_checked_at"] = str(row.get("last_checked_at") or "")
        row["content_changed_at"] = str(row.get("content_changed_at") or "")
        row["content_hash"] = str(row.get("content_hash") or "")
        row["check_status"] = str(row.get("check_status") or "")
        row["status"] = str(row.get("status") or "")
        row["result_count"] = int(row.get("result_count") or 0)
        maximum_age = row.get("maximum_age_hours")
        row["maximum_age_hours"] = float(maximum_age) if maximum_age is not None else None
        if not source_id or row["status"] not in {"current", "due_soon", "overdue", "missing", "failed", "manual"}:
            raise ValueError("Source freshness row has an invalid identity or status")
        selected.append(row)

    missing = requested - {str(row["source_id"]) for row in selected}
    if missing:
        raise ValueError(f"Source freshness report is missing requested sources: {', '.join(sorted(missing))}")
    if not selected:
        raise ValueError("Source freshness snapshot must include at least one source")

    selected.sort(key=lambda row: str(row["source_id"]))
    observed_at = str(report.get("as_of") or report.get("generated_at") or "").strip()
    if not observed_at:
        raise ValueError("Source freshness report is missing its observation timestamp")
    blocking = sorted(
        str(row["source_id"])
        for row in selected
        if row["status"] in {"overdue", "missing", "failed"}
    )
    counts = Counter(str(row["status"]) for row in selected)
    content_projection = [
        {
            "source_id": row["source_id"],
            "result_count": row["result_count"],
            "content_hash": row["content_hash"],
            "check_status": row["check_status"],
            "status": row["status"],
        }
        for row in selected
    ]
    content_hash = hashlib.sha256(
        json.dumps(content_projection, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema": "rock-kb-source-operations-snapshot-v1",
        "workflow_id": workflow_id,
        "workflow_max_age_hours": float(workflow_max_age_hours),
        "run_id": str(run_id),
        "run_url": str(run_url),
        "observed_at": observed_at,
        "status": "fail" if blocking else "ok",
        "source_count": len(selected),
        "counts": dict(sorted(counts.items())),
        "blocking_source_ids": blocking,
        "content_hash": content_hash,
        "sources": selected,
    }


def source_freshness_sql(snapshot: dict[str, Any]) -> str:
    workflow_values = [
        snapshot["workflow_id"],
        snapshot["run_id"],
        snapshot["run_url"],
        snapshot["observed_at"],
        snapshot["status"],
        float(snapshot["workflow_max_age_hours"]),
        int(snapshot["source_count"]),
        snapshot["content_hash"],
        compact_json(snapshot["counts"]),
        compact_json(snapshot["blocking_source_ids"]),
    ]
    statements = [
        "CREATE TABLE IF NOT EXISTS source_workflow_runs_v1 (workflow_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, run_url TEXT NOT NULL, observed_at TEXT NOT NULL, status TEXT NOT NULL, maximum_age_hours REAL NOT NULL, source_count INTEGER NOT NULL, content_hash TEXT NOT NULL, counts_json TEXT NOT NULL, blocking_source_ids_json TEXT NOT NULL);",
        "CREATE TABLE IF NOT EXISTS source_freshness_state_v1 (source_id TEXT PRIMARY KEY, name TEXT NOT NULL, cadence TEXT NOT NULL, maximum_age_hours REAL, last_checked_at TEXT NOT NULL, content_changed_at TEXT NOT NULL, result_count INTEGER NOT NULL, content_hash TEXT NOT NULL, check_status TEXT NOT NULL, status TEXT NOT NULL, observed_at TEXT NOT NULL, workflow_id TEXT NOT NULL);",
        "INSERT INTO source_workflow_runs_v1 (workflow_id, run_id, run_url, observed_at, status, maximum_age_hours, source_count, content_hash, counts_json, blocking_source_ids_json)",
        f"VALUES ({', '.join(sql_value(value) for value in workflow_values)})",
        "ON CONFLICT(workflow_id) DO UPDATE SET run_id = excluded.run_id, run_url = excluded.run_url, observed_at = excluded.observed_at, status = excluded.status, maximum_age_hours = excluded.maximum_age_hours, source_count = excluded.source_count, content_hash = excluded.content_hash, counts_json = excluded.counts_json, blocking_source_ids_json = excluded.blocking_source_ids_json WHERE excluded.observed_at >= source_workflow_runs_v1.observed_at;",
    ]
    source_update_guard = (
        "(source_freshness_state_v1.observed_at = '' OR "
        "(excluded.observed_at <> '' AND julianday(excluded.observed_at) >= julianday(source_freshness_state_v1.observed_at))) "
        "AND (source_freshness_state_v1.last_checked_at = '' OR "
        "(excluded.last_checked_at <> '' AND julianday(excluded.last_checked_at) >= julianday(source_freshness_state_v1.last_checked_at))) "
        "AND (source_freshness_state_v1.content_changed_at = '' OR "
        "(excluded.content_changed_at <> '' AND julianday(excluded.content_changed_at) >= julianday(source_freshness_state_v1.content_changed_at))) "
        "AND (source_freshness_state_v1.workflow_id = excluded.workflow_id OR "
        "source_freshness_state_v1.last_checked_at = '' OR "
        "julianday(excluded.last_checked_at) > julianday(source_freshness_state_v1.last_checked_at))"
    )
    for row in snapshot["sources"]:
        source_values = [
            row["source_id"],
            row["name"],
            row["cadence"],
            row["maximum_age_hours"],
            row["last_checked_at"],
            row["content_changed_at"],
            int(row["result_count"]),
            row["content_hash"],
            row["check_status"],
            row["status"],
            snapshot["observed_at"],
            snapshot["workflow_id"],
        ]
        statements.extend(
            [
                "INSERT INTO source_freshness_state_v1 (source_id, name, cadence, maximum_age_hours, last_checked_at, content_changed_at, result_count, content_hash, check_status, status, observed_at, workflow_id)",
                f"VALUES ({', '.join(sql_value(value) for value in source_values)})",
                "ON CONFLICT(source_id) DO UPDATE SET name = excluded.name, cadence = excluded.cadence, maximum_age_hours = excluded.maximum_age_hours, last_checked_at = excluded.last_checked_at, content_changed_at = excluded.content_changed_at, result_count = excluded.result_count, content_hash = excluded.content_hash, check_status = excluded.check_status, status = excluded.status, observed_at = excluded.observed_at, workflow_id = excluded.workflow_id WHERE "
                + source_update_guard
                + ";",
            ]
        )
    return "\n".join(statements) + "\n"


def record_source_freshness(
    report_path: Path,
    *,
    workflow_id: str,
    workflow_max_age_hours: float | None = None,
    database: str,
    env: str | None = None,
    run_id: str = "",
    run_url: str = "",
    source_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("Source freshness report must contain a JSON object")
    snapshot = source_freshness_snapshot(
        report,
        workflow_id=workflow_id,
        workflow_max_age_hours=workflow_max_age_hours,
        run_id=run_id,
        run_url=run_url,
        source_ids=source_ids,
    )
    with tempfile.TemporaryDirectory(prefix="rock-kb-source-freshness-") as temp_dir:
        sql_path = Path(temp_dir) / "source-freshness.sql"
        sql_path.write_text(source_freshness_sql(snapshot), encoding="utf-8")
        command = ["npx", "wrangler", "d1", "execute", database, "--remote", "--file", str(sql_path), "--yes"]
        if env:
            command.extend(["--env", env])
        subprocess.run(command, cwd=SERVICE_DIR, check=True)
    return snapshot


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def sql_value(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"
