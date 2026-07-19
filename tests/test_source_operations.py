from __future__ import annotations

import json

import pytest

from rock_kb.source_operations import source_freshness_snapshot, source_freshness_sql


def report_fixture() -> dict[str, object]:
    return {
        "schema": "rock-kb-source-freshness-report-v1",
        "as_of": "2026-07-18T10:45:26+00:00",
        "status": "ok",
        "sources": [
            {
                "source_id": "rock_core_issues",
                "name": "Rock Core GitHub Issues",
                "cadence": "daily",
                "maximum_age_hours": 48,
                "last_checked_at": "2026-07-18T09:44:00+00:00",
                "content_changed_at": "2026-07-18T09:44:00+00:00",
                "result_count": 123,
                "content_hash": "a" * 64,
                "check_status": "success",
                "status": "current",
            },
            {
                "source_id": "rock_mobile_issues",
                "name": "Rock Mobile GitHub Issues",
                "cadence": "daily",
                "maximum_age_hours": 48,
                "last_checked_at": "2026-07-18T09:44:00+00:00",
                "content_changed_at": "2026-07-17T09:44:00+00:00",
                "result_count": 45,
                "content_hash": "b" * 64,
                "check_status": "success",
                "status": "current",
            },
        ],
    }


def test_source_freshness_snapshot_keeps_separate_public_operational_fields() -> None:
    snapshot = source_freshness_snapshot(
        report_fixture(),
        workflow_id="daily-issues",
        workflow_max_age_hours=36,
        run_id="12345",
        run_url="https://github.com/ONE-ALL-Church/rock-agent-kb/actions/runs/12345",
        source_ids=["rock_core_issues", "rock_mobile_issues"],
    )

    assert snapshot["schema"] == "rock-kb-source-operations-snapshot-v1"
    assert snapshot["status"] == "ok"
    assert snapshot["source_count"] == 2
    assert len(snapshot["content_hash"]) == 64
    assert snapshot["sources"][0] == {
        "source_id": "rock_core_issues",
        "name": "Rock Core GitHub Issues",
        "cadence": "daily",
        "maximum_age_hours": 48.0,
        "last_checked_at": "2026-07-18T09:44:00+00:00",
        "content_changed_at": "2026-07-18T09:44:00+00:00",
        "result_count": 123,
        "content_hash": "a" * 64,
        "check_status": "success",
        "status": "current",
    }


def test_source_freshness_snapshot_filters_and_rejects_missing_requested_sources() -> None:
    snapshot = source_freshness_snapshot(
        report_fixture(),
        workflow_id="daily-issues",
        workflow_max_age_hours=36,
        source_ids=["rock_mobile_issues"],
    )
    assert [row["source_id"] for row in snapshot["sources"]] == ["rock_mobile_issues"]

    with pytest.raises(ValueError, match="missing requested sources"):
        source_freshness_snapshot(
            report_fixture(),
            workflow_id="daily-issues",
            workflow_max_age_hours=36,
            source_ids=["not_registered"],
        )


def test_source_freshness_sql_upserts_workflow_and_source_state() -> None:
    snapshot = source_freshness_snapshot(
        report_fixture(),
        workflow_id="daily-issues",
        workflow_max_age_hours=36,
        run_id="12345",
    )
    sql = source_freshness_sql(snapshot)

    assert "CREATE TABLE IF NOT EXISTS source_workflow_runs_v1" in sql
    assert "CREATE TABLE IF NOT EXISTS source_freshness_state_v1" in sql
    assert "WHERE excluded.observed_at >= source_workflow_runs_v1.observed_at" in sql
    assert "WHERE excluded.observed_at >= source_freshness_state_v1.observed_at" in sql
    assert "rock_core_issues" in sql
    assert json.dumps(snapshot["counts"], sort_keys=True, separators=(",", ":")) in sql
