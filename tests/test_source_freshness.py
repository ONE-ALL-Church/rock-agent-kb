from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from rock_kb.source_freshness import source_freshness_rows


def source(source_id: str, cadence: str):
    return SimpleNamespace(id=source_id, name=source_id.title(), refresh_cadence=cadence)


def test_source_freshness_classifies_current_due_overdue_missing_and_manual():
    as_of = datetime(2026, 7, 10, 12, tzinfo=timezone.utc)
    snapshot = {
        "sources": {
            "current": {"retrieved_at_max": "2026-07-10T00:00:00+00:00", "record_count": 2},
            "due": {"retrieved_at_max": "2026-07-08T22:00:00+00:00", "record_count": 2},
            "overdue": {"retrieved_at_max": "2026-07-07T00:00:00+00:00", "record_count": 2},
        }
    }
    policy = {"due_soon_fraction": 0.75, "cadences": {"daily": {"maximum_age_hours": 48}, "manual": {"maximum_age_hours": None}}}

    rows = source_freshness_rows(
        [source("current", "daily"), source("due", "daily"), source("overdue", "daily"), source("missing", "daily"), source("manual", "manual")],
        snapshot,
        policy,
        as_of,
    )

    assert {row["source_id"]: row["status"] for row in rows} == {
        "current": "current",
        "due": "due_soon",
        "manual": "manual",
        "missing": "missing",
        "overdue": "overdue",
    }


def test_source_refresh_failure_overrides_age():
    rows = source_freshness_rows(
        [source("rock_documentation", "weekly")],
        {"sources": {"rock_documentation": {"retrieved_at_max": "2026-07-10T00:00:00+00:00", "record_count": 2}}},
        {"due_soon_fraction": 0.75, "cadences": {"weekly": {"maximum_age_hours": 216}}},
        datetime(2026, 7, 10, 12, tzinfo=timezone.utc),
        {"failed": ["rock_documentation"]},
    )

    assert rows[0]["status"] == "failed"
