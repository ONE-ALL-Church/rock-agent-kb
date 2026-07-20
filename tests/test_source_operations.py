from __future__ import annotations

import json
import sqlite3
from copy import deepcopy

import pytest

from rock_kb.source_operations import source_freshness_snapshot, source_freshness_sql
from rock_kb.source_workflows import source_workflow_policies
from rock_kb.sources import load_sources


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


def test_source_freshness_snapshot_rejects_partial_and_foreign_ownership() -> None:
    with pytest.raises(ValueError, match="omits owned sources"):
        source_freshness_snapshot(
            report_fixture(),
            workflow_id="daily-issues",
            workflow_max_age_hours=36,
            source_ids=["rock_mobile_issues"],
        )

    with pytest.raises(ValueError, match="owned by another workflow"):
        source_freshness_snapshot(
            report_fixture(),
            workflow_id="daily-issues",
            workflow_max_age_hours=36,
            source_ids=["rock_core_issues", "rock_mobile_issues", "rock_documentation"],
        )


def test_source_workflow_policy_assigns_every_registered_source_once() -> None:
    workflows = source_workflow_policies()
    source_ids = [source_id for row in workflows.values() for source_id in row["source_ids"]]

    assert sorted(source_ids) == sorted(source.id for source in load_sources())
    assert len(source_ids) == len(set(source_ids))
    assert workflows["daily-issues"]["source_ids"] == ["rock_core_issues", "rock_mobile_issues"]
    assert workflows["daily-sources"]["maximum_age_hours"] == 52.0


def test_source_freshness_snapshot_rejects_workflow_maximum_age_drift() -> None:
    with pytest.raises(ValueError, match="configured value of 36 hours"):
        source_freshness_snapshot(
            report_fixture(),
            workflow_id="daily-issues",
            workflow_max_age_hours=48,
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
    assert "julianday(excluded.last_checked_at) >= julianday(source_freshness_state_v1.last_checked_at)" in sql
    assert "source_freshness_state_v1.workflow_id = excluded.workflow_id" in sql
    assert "rock_core_issues" in sql
    assert json.dumps(snapshot["counts"], sort_keys=True, separators=(",", ":")) in sql


def test_later_stale_workflow_cannot_overwrite_newer_source_observation() -> None:
    daily = source_freshness_snapshot(
        report_fixture(),
        workflow_id="daily-issues",
        run_id="daily",
    )
    stale_weekly = deepcopy(daily)
    stale_weekly.update(
        {
            "workflow_id": "weekly-comprehensive",
            "workflow_max_age_hours": 216.0,
            "run_id": "weekly",
            "observed_at": "2026-07-18T11:45:26+00:00",
        }
    )
    for row in stale_weekly["sources"]:
        row["last_checked_at"] = "2026-07-17T09:44:00+00:00"
        row["content_changed_at"] = "2026-07-17T09:44:00+00:00"
        row["content_hash"] = "c" * 64

    database = sqlite3.connect(":memory:")
    database.executescript(source_freshness_sql(daily))
    database.executescript(source_freshness_sql(stale_weekly))
    row = database.execute(
        "SELECT workflow_id, last_checked_at, content_changed_at, content_hash "
        "FROM source_freshness_state_v1 WHERE source_id = 'rock_core_issues'"
    ).fetchone()

    assert row == (
        "daily-issues",
        "2026-07-18T09:44:00+00:00",
        "2026-07-18T09:44:00+00:00",
        "a" * 64,
    )


def test_newer_owner_observation_can_repair_legacy_wrong_ownership() -> None:
    daily = source_freshness_snapshot(
        report_fixture(),
        workflow_id="daily-issues",
        run_id="daily",
    )
    daily["observed_at"] = "2026-07-18T12:45:26+00:00"
    stale_weekly = deepcopy(daily)
    stale_weekly.update(
        {
            "workflow_id": "weekly-comprehensive",
            "workflow_max_age_hours": 216.0,
            "run_id": "weekly",
            "observed_at": "2026-07-18T11:45:26+00:00",
        }
    )
    for row in stale_weekly["sources"]:
        row["last_checked_at"] = "2026-07-17T09:44:00+00:00"
        row["content_changed_at"] = "2026-07-17T09:44:00+00:00"

    database = sqlite3.connect(":memory:")
    database.executescript(source_freshness_sql(stale_weekly))
    database.executescript(source_freshness_sql(daily))
    row = database.execute(
        "SELECT workflow_id, last_checked_at FROM source_freshness_state_v1 "
        "WHERE source_id = 'rock_core_issues'"
    ).fetchone()

    assert row == ("daily-issues", "2026-07-18T09:44:00+00:00")
