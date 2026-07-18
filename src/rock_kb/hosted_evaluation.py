from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .jsonl import read_jsonl
from .paths import REPO_ROOT
from .service_eval import EVALUATION_SET_PATH


SERVICE_DIR = REPO_ROOT / "service"
PERSISTED_METRICS = {
    "question_count",
    "relevance_question_count",
    "mean_reciprocal_rank",
    "recall_at_target_rank",
    "duplicate_result_count",
    "duplicate_result_rate",
    "authority_question_count",
    "authority_pass_rate",
    "mean_latency_ms",
    "p95_latency_ms",
}


def hosted_evaluation_record(report: dict[str, Any]) -> dict[str, Any]:
    if report.get("schema") != "rock-kb-service-evaluation-v1":
        raise ValueError("Hosted evaluation report has an unsupported schema")
    expected_ids = {str(row.get("id") or "") for row in read_jsonl(EVALUATION_SET_PATH)}
    results = report.get("results")
    if not isinstance(results, list):
        raise ValueError("Hosted evaluation report is missing results")
    result_ids = [str(row.get("id") or "") for row in results if isinstance(row, dict)]
    if len(result_ids) != len(expected_ids) or set(result_ids) != expected_ids:
        raise ValueError("Hosted evaluation report does not cover the complete current evaluation set")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("Hosted evaluation report contains duplicate case IDs")

    status = str(report.get("status") or "")
    pass_count = int(report.get("pass_count") or 0)
    fail_count = int(report.get("fail_count") or 0)
    if status not in {"ok", "fail"} or pass_count + fail_count != len(results):
        raise ValueError("Hosted evaluation counts are inconsistent")
    if status == "ok" and fail_count:
        raise ValueError("A passing hosted evaluation cannot contain failures")

    projection_version = str(report.get("projection_version") or "").strip()
    evaluated_at = str(report.get("evaluated_at") or "").strip()
    if not projection_version or not evaluated_at:
        raise ValueError("Hosted evaluation report is missing projection identity or timestamp")
    raw_metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    metrics = {key: raw_metrics[key] for key in sorted(PERSISTED_METRICS) if key in raw_metrics}
    if int(metrics.get("question_count") or 0) != len(results):
        raise ValueError("Hosted evaluation metric count does not match the evaluation set")
    return {
        "schema": "rock-kb-hosted-evaluation-record-v1",
        "projection_version": projection_version,
        "evaluated_at": evaluated_at,
        "status": status,
        "case_count": len(results),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "metrics": metrics,
        "client_version": "workflow-v1",
    }


def hosted_evaluation_sql(record: dict[str, Any]) -> str:
    metrics_json = json.dumps(record["metrics"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    values = [
        record["projection_version"],
        record["evaluated_at"],
        record["status"],
        int(record["case_count"]),
        int(record["pass_count"]),
        int(record["fail_count"]),
        metrics_json,
        record["client_version"],
    ]
    return "\n".join(
        [
            "CREATE TABLE IF NOT EXISTS hosted_evaluation_runs_v1 (projection_version TEXT PRIMARY KEY, evaluated_at TEXT NOT NULL, status TEXT NOT NULL, case_count INTEGER NOT NULL, pass_count INTEGER NOT NULL, fail_count INTEGER NOT NULL, metrics_json TEXT NOT NULL, client_version TEXT NOT NULL);",
            "INSERT INTO hosted_evaluation_runs_v1 (projection_version, evaluated_at, status, case_count, pass_count, fail_count, metrics_json, client_version)",
            f"VALUES ({', '.join(sql_value(value) for value in values)})",
            "ON CONFLICT(projection_version) DO UPDATE SET evaluated_at = excluded.evaluated_at, status = excluded.status, case_count = excluded.case_count, pass_count = excluded.pass_count, fail_count = excluded.fail_count, metrics_json = excluded.metrics_json, client_version = excluded.client_version WHERE excluded.evaluated_at >= hosted_evaluation_runs_v1.evaluated_at;",
        ]
    ) + "\n"


def record_hosted_evaluation(report_path: Path, *, database: str, env: str | None = None) -> dict[str, Any]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("Hosted evaluation report must contain a JSON object")
    record = hosted_evaluation_record(report)
    with tempfile.TemporaryDirectory(prefix="rock-kb-hosted-eval-") as temp_dir:
        sql_path = Path(temp_dir) / "hosted-evaluation.sql"
        sql_path.write_text(hosted_evaluation_sql(record), encoding="utf-8")
        command = ["npx", "wrangler", "d1", "execute", database, "--remote", "--file", str(sql_path), "--yes"]
        if env:
            command.extend(["--env", env])
        subprocess.run(command, cwd=SERVICE_DIR, check=True)
    return record


def sql_value(value: Any) -> str:
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"
