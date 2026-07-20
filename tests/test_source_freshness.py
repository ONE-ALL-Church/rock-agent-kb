from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import yaml

from rock_kb.source_freshness import blocking_source_ids, build_source_observations, source_freshness_rows
from rock_kb.source_workflows import source_workflow_policy
from rock_kb.sources import load_sources


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


def test_source_observations_separate_check_time_from_unchanged_content_time():
    as_of = datetime(2026, 7, 16, 12, tzinfo=timezone.utc)
    snapshot = {
        "sources": {
            "rock_youtube": {
                "retrieved_at_max": "2026-07-16T11:59:00+00:00",
                "record_count": 2,
            }
        },
        "source_records": {
            "video:1": {"source_id": "rock_youtube", "content_hash": "a" * 64},
            "video:2": {"source_id": "rock_youtube", "content_hash": "b" * 64},
        },
    }
    first = build_source_observations(
        [source("rock_youtube", "daily")],
        snapshot,
        as_of,
        refresh_status={"checked": ["rock_youtube"], "checked_at": "2026-07-16T12:00:00Z"},
    )
    first_row = first["sources"]["rock_youtube"]
    first_row["content_changed_at"] = "2026-07-14T08:00:00+00:00"

    second = build_source_observations(
        [source("rock_youtube", "daily")],
        snapshot,
        as_of,
        refresh_status={"checked": ["rock_youtube"], "checked_at": "2026-07-16T12:00:00Z"},
        previous_observations=first,
    )
    row = second["sources"]["rock_youtube"]

    assert row["last_checked_at"] == "2026-07-16T12:00:00+00:00"
    assert row["content_changed_at"] == "2026-07-14T08:00:00+00:00"
    assert row["result_count"] == 2
    assert len(row["content_hash"]) == 64
    assert row["status"] == "success"


def test_source_observations_advance_content_time_when_hash_changes():
    as_of = datetime(2026, 7, 16, 12, tzinfo=timezone.utc)
    snapshot = {
        "sources": {"rock_youtube": {"retrieved_at_max": as_of.isoformat(), "record_count": 1}},
        "source_records": {"video:1": {"source_id": "rock_youtube", "content_hash": "new"}},
    }
    previous = {
        "sources": {
            "rock_youtube": {
                "content_hash": "old",
                "content_changed_at": "2026-07-14T08:00:00+00:00",
            }
        }
    }

    observations = build_source_observations(
        [source("rock_youtube", "daily")],
        snapshot,
        as_of,
        refresh_status={"checked": ["rock_youtube"], "checked_at": as_of.isoformat()},
        previous_observations=previous,
    )

    assert observations["sources"]["rock_youtube"]["content_changed_at"] == as_of.isoformat()


def test_source_observations_ignore_raw_page_chrome_when_normalized_summary_is_unchanged():
    first_checked = datetime(2026, 7, 16, 11, tzinfo=timezone.utc)
    second_checked = datetime(2026, 7, 16, 12, tzinfo=timezone.utc)
    first_snapshot = {
        "sources": {"rock_community_blog": {"retrieved_at_max": first_checked.isoformat(), "record_count": 1}},
        "source_records": {
            "article:1": {
                "source_id": "rock_community_blog",
                "source_title": "Stable article",
                "source_url": "https://example.org/stable-article",
                "content_hash": "raw-html-first",
                "summary_hash": "stable-normalized-summary",
                "topics": ["community"],
            }
        },
    }
    first = build_source_observations(
        [source("rock_community_blog", "daily")],
        first_snapshot,
        first_checked,
        refresh_status={"checked": ["rock_community_blog"], "checked_at": first_checked.isoformat()},
    )
    first["sources"]["rock_community_blog"]["content_changed_at"] = "2026-07-14T08:00:00+00:00"
    second_snapshot = json.loads(json.dumps(first_snapshot))
    second_snapshot["sources"]["rock_community_blog"]["retrieved_at_max"] = second_checked.isoformat()
    second_snapshot["source_records"]["article:1"]["content_hash"] = "raw-html-second"

    second = build_source_observations(
        [source("rock_community_blog", "daily")],
        second_snapshot,
        second_checked,
        refresh_status={"checked": ["rock_community_blog"], "checked_at": second_checked.isoformat()},
        previous_observations=first,
    )
    row = second["sources"]["rock_community_blog"]

    assert row["last_checked_at"] == second_checked.isoformat()
    assert row["content_changed_at"] == "2026-07-14T08:00:00+00:00"
    assert row["content_hash"] == first["sources"]["rock_community_blog"]["content_hash"]


def test_rock_issue_summary_supplies_issue_source_freshness_metadata():
    as_of = datetime(2026, 7, 16, 12, tzinfo=timezone.utc)
    sources = [source("rock_core_issues", "daily"), source("rock_mobile_issues", "daily")]
    issue_summary = {
        "source_updated_through": "2026-07-16T11:30:00Z",
        "catalog_content_hash": "c" * 64,
        "repositories": {
            "SparkDevNetwork/Rock": 5671,
            "SparkDevNetwork/Rock.Mobile-Issues": 127,
        },
    }

    observations = build_source_observations(
        sources,
        {"sources": {}, "source_records": {}},
        as_of,
        issue_summary=issue_summary,
    )
    rows = source_freshness_rows(
        sources,
        {"sources": {}},
        {"due_soon_fraction": 0.75, "cadences": {"daily": {"maximum_age_hours": 48}}},
        as_of,
        observations=observations,
    )
    by_id = {row["source_id"]: row for row in rows}

    assert by_id["rock_core_issues"]["status"] == "current"
    assert by_id["rock_core_issues"]["result_count"] == 5671
    assert by_id["rock_mobile_issues"]["result_count"] == 127
    assert by_id["rock_core_issues"]["last_checked_at"] == "2026-07-16T11:30:00+00:00"
    assert by_id["rock_core_issues"]["content_hash"] != by_id["rock_mobile_issues"]["content_hash"]


def test_rock_issue_checkpoint_advances_check_time_without_changing_content_time():
    as_of = datetime(2026, 7, 18, 12, tzinfo=timezone.utc)
    sources = [source("rock_core_issues", "daily"), source("rock_mobile_issues", "daily")]
    issue_summary = {
        "source_updated_through": "2026-07-16T11:30:00Z",
        "catalog_content_hash": "c" * 64,
        "repositories": {
            "SparkDevNetwork/Rock": 5671,
            "SparkDevNetwork/Rock.Mobile-Issues": 127,
        },
    }
    previous = build_source_observations(
        sources,
        {"sources": {}, "source_records": {}},
        as_of,
        issue_summary=issue_summary,
        issue_checkpoint={"checked_at": "2026-07-17T09:43:00Z"},
    )
    for row in previous["sources"].values():
        row["content_changed_at"] = "2026-07-16T11:30:00+00:00"

    observations = build_source_observations(
        sources,
        {"sources": {}, "source_records": {}},
        as_of,
        previous_observations=previous,
        issue_summary=issue_summary,
        issue_checkpoint={"checked_at": "2026-07-18T09:43:00Z"},
    )

    for row in observations["sources"].values():
        assert row["last_checked_at"] == "2026-07-18T09:43:00+00:00"
        assert row["content_changed_at"] == "2026-07-16T11:30:00+00:00"
        assert row["status"] == "success"


def test_issue_refresh_workflow_restores_dedicated_observation_cache():
    workflow = Path(".github/workflows/refresh-rock-issues.yml").read_text(encoding="utf-8")

    assert "data/review/rock-issue-freshness/source-observations.json" in workflow
    assert "rock-kb-issue-source-observations-" in workflow


def test_blocking_sources_can_be_scoped_to_daily_cadence():
    rows = [
        {"source_id": "daily-current", "cadence": "daily", "status": "current"},
        {"source_id": "daily-missing", "cadence": "daily", "status": "missing"},
        {"source_id": "weekly-missing", "cadence": "weekly", "status": "missing"},
    ]

    assert blocking_source_ids(rows) == ["daily-missing", "weekly-missing"]
    assert blocking_source_ids(rows, {"daily"}) == ["daily-missing"]
    assert blocking_source_ids(rows, required_source_ids={"weekly-missing"}) == ["weekly-missing"]


def test_daily_workflow_covers_refreshable_daily_sources_and_leaves_weekly_refresh():
    daily_workflow = yaml.safe_load(Path(".github/workflows/refresh-daily.yml").read_text(encoding="utf-8"))
    configured = set(source_workflow_policy("daily-sources")["source_ids"])
    expected = {
        item.id
        for item in load_sources()
        if item.refresh_cadence == "daily" and item.kind != "github_issues"
    }

    assert configured == expected
    assert 'cron: "17 10 * * 0,2-6"' in Path(".github/workflows/refresh-daily.yml").read_text(encoding="utf-8")
    assert "workflow-sources daily-sources" in Path(".github/workflows/refresh-daily.yml").read_text(encoding="utf-8")
    assert "--required-workflow daily-sources" in Path(".github/workflows/refresh-daily.yml").read_text(encoding="utf-8")
    weekly_workflow = Path(".github/workflows/refresh.yml").read_text(encoding="utf-8")
    assert 'cron: "17 10 * * 1"' in weekly_workflow
    assert "--required-workflow weekly-comprehensive" in weekly_workflow
    issue_workflow = Path(".github/workflows/refresh-rock-issues.yml").read_text(encoding="utf-8")
    assert "--required-workflow daily-issues" in issue_workflow
    assert daily_workflow["concurrency"]["group"] == "source-refresh"
