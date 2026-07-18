from __future__ import annotations

from rock_kb.hosted_evaluation import hosted_evaluation_record, hosted_evaluation_sql
from rock_kb.jsonl import read_jsonl
from rock_kb.service_eval import EVALUATION_SET_PATH


def complete_report() -> dict:
    ids = [str(row["id"]) for row in read_jsonl(EVALUATION_SET_PATH)]
    return {
        "schema": "rock-kb-service-evaluation-v1",
        "status": "ok",
        "pass_count": len(ids),
        "fail_count": 0,
        "projection_version": "projection-v1",
        "evaluated_at": "2026-07-17T20:00:00Z",
        "metrics": {
            "question_count": len(ids),
            "mean_reciprocal_rank": 0.99,
            "recall_at_target_rank": 1.0,
            "duplicate_result_rate": 0.0,
            "authority_pass_rate": 1.0,
            "mean_latency_ms": 12.5,
            "p95_latency_ms": 20.0,
        },
        "results": [{"id": case_id, "question": "not persisted", "status": "pass"} for case_id in ids],
    }


def test_hosted_evaluation_record_keeps_only_bounded_summary():
    record = hosted_evaluation_record(complete_report())

    assert record["status"] == "ok"
    assert record["case_count"] == len(list(read_jsonl(EVALUATION_SET_PATH)))
    assert "results" not in record
    assert "question" not in record
    assert "questions" not in record
    assert set(record["metrics"]) <= {
        "question_count",
        "mean_reciprocal_rank",
        "recall_at_target_rank",
        "duplicate_result_rate",
        "authority_pass_rate",
        "mean_latency_ms",
        "p95_latency_ms",
    }


def test_hosted_evaluation_sql_contains_no_queries_or_case_text():
    sql = hosted_evaluation_sql(hosted_evaluation_record(complete_report()))

    assert "hosted_evaluation_runs_v1" in sql
    assert "not persisted" not in sql
    assert "ON CONFLICT(projection_version)" in sql


def test_hosted_evaluation_rejects_incomplete_case_set():
    report = complete_report()
    report["results"] = report["results"][:-1]
    report["pass_count"] -= 1
    report["metrics"]["question_count"] -= 1

    try:
        hosted_evaluation_record(report)
    except ValueError as exc:
        assert "complete current evaluation set" in str(exc)
    else:
        raise AssertionError("incomplete hosted evaluation was accepted")
