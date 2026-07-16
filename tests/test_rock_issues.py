from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from rock_kb import rock_issues, service_projection
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.rock_issues import (
    assemble_investigation_packet,
    assess_catalog,
    assess_issue,
    attach_issue_enrichments,
    build_reviewed_enrichment_metrics,
    build_reviewed_issue_enrichments,
    find_issue_row,
    graphql_issue_to_raw,
    investigation_plan,
    normalize_issue,
    parse_issue_ref,
    parse_markdown_sections,
    route_issue,
    select_timeline_targets,
    validate_instance_profile,
    validate_rock_issue_rows,
    validate_worker_results,
)
from rock_kb.service_projection import build_d1_seed_sql, rock_issue_search_rows
from rock_kb.schemas.rock_issue import RockIssueReviewedEnrichment


def core_issue() -> tuple[dict, list[dict]]:
    issue = {
        "number": 6917,
        "title": "[Alpha 19.3.1] Classic Checkin Throws Illegal Characters Exception",
        "html_url": "https://github.com/SparkDevNetwork/Rock/issues/6917",
        "state": "closed",
        "state_reason": "completed",
        "created_at": "2026-07-14T14:00:00Z",
        "updated_at": "2026-07-14T22:33:30Z",
        "closed_at": "2026-07-14T22:33:09Z",
        "locked": False,
        "comments": 1,
        "labels": [
            {"name": "Topic: Check-in"},
            {"name": "Topic: CMS"},
            {"name": "Fixed in v19.3"},
        ],
        "milestone": None,
        "body": """### Description

Classic check-in throws an exception.

### Rock Version

19.3.1

### Client Culture Setting

en-US
""",
    }
    timeline = [
        {
            "event": "referenced",
            "commit_id": "aae87fcb73df28c84caa91d3a1e7e390dc6059a7",
            "created_at": "2026-07-14T22:31:47Z",
        },
        {
            "event": "closed",
            "commit_id": "aae87fcb73df28c84caa91d3a1e7e390dc6059a7",
            "created_at": "2026-07-14T22:33:09Z",
        },
    ]
    return issue, timeline


def test_normalize_core_issue_separates_report_fix_and_state():
    raw, timeline = core_issue()
    row = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)

    assert row["issue_id"] == "rock_issue:SparkDevNetwork/Rock#6917"
    assert row["validation_state"] == "confirmed"
    assert row["state"] == "closed"
    assert row["remediation_state"] == "fixed_release_recorded"
    assert row["authority_tier"] == "community-unreviewed"
    assert {item["concept_id"] for item in row["concept_routes"]} >= {"check-in", "cms-websites"}
    relationships = {(item["relationship"], item["normalized_version"]) for item in row["version_evidence"]}
    assert ("reported_affected", "19.3.1") in relationships
    assert ("fixed", "19.3") in relationships
    assert row["linked_commit_shas"] == ["aae87fcb73df28c84caa91d3a1e7e390dc6059a7"]
    assert row["timeline_updated_through"] == "2026-07-14T22:33:30Z"
    assert "body" not in row
    assert json.dumps(row).count("Classic check-in throws an exception") == 0
    validate_rock_issue_rows([row])


def test_normalize_mobile_issue_keeps_core_and_shell_versions_distinct():
    raw = {
        "number": 128,
        "title": "Chat text disappears",
        "html_url": "https://github.com/SparkDevNetwork/Rock.Mobile-Issues/issues/128",
        "state": "closed",
        "state_reason": "completed",
        "created_at": "2026-03-06T00:00:00Z",
        "updated_at": "2026-03-07T00:00:00Z",
        "closed_at": "2026-03-07T00:00:00Z",
        "comments": 0,
        "labels": [{"name": "status: verified"}],
        "milestone": {"title": "v19.3", "state": "open", "html_url": "https://github.com/example"},
        "body": """### Issue Type
Functional bug
### Frequency
Always reproducible
### Platform(s) Affected
Both iOS and Android
### Rock Mobile Shell Version
19.1
### Rock Core Version
19.2.0
""",
    }

    row = normalize_issue("SparkDevNetwork/Rock.Mobile-Issues", raw)

    evidence = {(item["component"], item["relationship"], item["normalized_version"]) for item in row["version_evidence"]}
    assert ("mobile_shell", "reported_affected", "19.1") in evidence
    assert ("rock_core", "reported_affected", "19.2.0") in evidence
    assert ("mobile_shell", "targeted", "19.3") in evidence
    assert row["platforms"] == ["ios", "android"]
    assert row["frequency"] == "always_reproducible"
    assert row["validation_state"] == "confirmed"


def test_issue_assessment_is_conservative_about_release_lines():
    raw, timeline = core_issue()
    row = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)

    exact = assess_issue(row, {"core_version": "19.3.1"})
    line_only = assess_issue(row, {"core_version": "19.3.2"})
    unknown = assess_issue(row, {"core_version": "20.0"})

    assert exact["applicability"] == "likely"
    assert line_only["applicability"] == "possible"
    assert unknown["applicability"] == "insufficient_evidence"
    assert exact["remediation"] == "fix_release_recorded"
    assert exact["fixed_release_lines"] == ["19.3"]
    assert exact["fix_target_relations"] == ["same_release_line"]


def test_issue_catalog_assessment_pages_after_ranking_complete_result_set():
    raw, timeline = core_issue()
    first = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    raw = {**raw, "number": 6918, "html_url": "https://github.com/SparkDevNetwork/Rock/issues/6918"}
    second = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)

    first_page = assess_catalog([second, first], {"core_version": "19.3.1"}, limit=1)
    second_page = assess_catalog([second, first], {"core_version": "19.3.1"}, limit=1, offset=1)

    assert first_page["total_count"] == 2
    assert first_page["has_more"] is True
    assert first_page["next_offset"] == 1
    assert first_page["results"][0]["issue_id"].endswith("#6917")
    assert second_page["count"] == 1
    assert second_page["has_more"] is False
    assert second_page["next_offset"] is None
    assert second_page["results"][0]["issue_id"].endswith("#6918")


def test_issue_investigation_plan_separates_private_worker_and_disables_writes():
    raw, timeline = core_issue()
    row = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)

    plan = investigation_plan(row, include_private_instance=True)

    assert plan["coordination"] == "orchestrator_worker"
    assert plan["admission"]["github_write_enabled"] is False
    private = next(task for task in plan["tasks"] if task["role"] == "instance_investigator")
    assert private["visibility"] == "private_only"
    assert all(task["permission"] == "read_only" for task in plan["tasks"])


def test_timeline_selection_can_target_exact_core_and_mobile_issues():
    raw_rows = [
        (
            "SparkDevNetwork/Rock",
            {
                "node_id": "I_core",
                "number": 6917,
                "state": "closed",
                "created_at": "2026-07-14T14:00:00Z",
                "updated_at": "2026-07-14T22:33:30Z",
            },
        ),
        (
            "SparkDevNetwork/Rock.Mobile-Issues",
            {
                "node_id": "I_mobile",
                "number": 128,
                "state": "closed",
                "created_at": "2026-03-06T00:00:00Z",
                "updated_at": "2026-07-13T18:34:17Z",
            },
        ),
        (
            "SparkDevNetwork/Rock",
            {
                "node_id": "I_unrelated",
                "number": 6920,
                "state": "open",
                "created_at": "2026-07-15T00:00:00Z",
                "updated_at": "2026-07-15T01:00:00Z",
            },
        ),
    ]
    existing = {
        "I_core": {"timeline_status": "complete", "timeline_updated_through": "2026-07-14T22:33:30Z"},
        "I_mobile": {
            "timeline_status": "complete",
            "timeline_updated_through": "2026-07-13T18:34:17Z",
            "location_aliases": ["SparkDevNetwork/Chat-Issues#128"],
        },
    }

    targets = select_timeline_targets(
        raw_rows,
        existing,
        timeline_days=1,
        timeline_backfill_limit=0,
        timeline_issue_refs=["6917", "mobile:128"],
        now=datetime(2026, 7, 15, tzinfo=timezone.utc),
    )

    assert set(targets) == {"I_core", "I_mobile"}

    alias_target = select_timeline_targets(
        raw_rows,
        existing,
        timeline_issue_refs=["https://github.com/SparkDevNetwork/Chat-Issues/issues/128"],
        now=datetime(2026, 7, 15, tzinfo=timezone.utc),
    )
    assert set(alias_target) == {"I_mobile"}

    with pytest.raises(ValueError, match="not found"):
        select_timeline_targets(
            raw_rows,
            existing,
            timeline_backfill_limit=0,
            timeline_issue_refs=["999999"],
        )


def test_worker_results_are_typed_revision_bound_and_assembled_for_review():
    raw, timeline = core_issue()
    issue = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    result = {
        "schema": "rock-kb-rock-issue-worker-result-v1",
        "run_id": "run-1",
        "issue_id": issue["issue_id"],
        "issue_updated_at": issue["updated_at"],
        "task_id": "intake",
        "status": "complete",
        "findings": [
            {
                "statement": "The report names Rock 19.3.1.",
                "classification": "reporter_observation",
                "evidence_refs": [issue["url"]],
                "confidence": "medium",
            }
        ],
        "tests": [],
        "proposed_applicability": [],
        "proposed_workarounds": [],
        "open_questions": [],
        "confidence": "medium",
        "private_output_refs": [],
    }

    packet = assemble_investigation_packet(issue, [result])

    assert packet["completed_tasks"] == ["intake"]
    assert packet["ready_for_skeptic"] is False
    assert packet["ready_for_public_review"] is False
    assert packet["packet_hash"]

    with pytest.raises(ValueError, match="stale"):
        validate_worker_results(issue, [{**result, "issue_updated_at": "2026-01-01T00:00:00Z"}])


def test_public_worker_cannot_return_private_output_refs():
    raw, timeline = core_issue()
    issue = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    result = {
        "schema": "rock-kb-rock-issue-worker-result-v1",
        "run_id": "run-1",
        "issue_id": issue["issue_id"],
        "issue_updated_at": issue["updated_at"],
        "task_id": "kb_router",
        "status": "complete",
        "findings": [],
        "tests": [],
        "proposed_applicability": [],
        "proposed_workarounds": [],
        "open_questions": [],
        "confidence": "low",
        "private_output_refs": ["private-evidence:fixture"],
    }

    with pytest.raises(ValueError, match="private instance investigator"):
        validate_worker_results(issue, [result])


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("6917", ("SparkDevNetwork/Rock", 6917)),
        ("mobile:128", ("SparkDevNetwork/Rock.Mobile-Issues", 128)),
        ("https://github.com/SparkDevNetwork/Rock/issues/6917", ("SparkDevNetwork/Rock", 6917)),
        ("rock_issue:SparkDevNetwork/Rock.Mobile-Issues#128", ("SparkDevNetwork/Rock.Mobile-Issues", 128)),
    ],
)
def test_parse_issue_refs(value, expected):
    assert parse_issue_ref(value) == expected


def test_profile_rejects_free_form_or_unbounded_fields():
    with pytest.raises(ValueError, match="Unsupported instance profile fields"):
        validate_instance_profile({"core_version": "19.2", "logs": "raw private logs"})
    with pytest.raises(ValueError, match="requires core_version"):
        validate_instance_profile({"concepts": ["check-in"]})


def test_markdown_section_parser_handles_mobile_heading_punctuation():
    sections = parse_markdown_sections("### Platform(s) Affected\nBoth iOS and Android\n### Rock Core Version\n19.1")
    assert sections["platform s affected"] == "Both iOS and Android"
    assert sections["rock core version"] == "19.1"


def test_issue_routing_does_not_use_generic_body_words_when_topic_labels_exist():
    routes = route_issue(
        "SparkDevNetwork/Rock",
        title="Classic Checkin exception",
        body="The person reported this on a server and included an error report.",
        labels=["Topic: Check-in"],
    )

    assert routes == [{"concept_id": "check-in", "basis": "github_topic_label", "signal": "Topic: Check-in"}]


def test_issue_routing_uses_only_precise_body_fallbacks():
    routes = route_issue(
        "SparkDevNetwork/Rock",
        title="Unexpected behavior",
        body="A person sees a report. The workflow action then updates a connection request.",
        labels=[],
    )

    assert {route["concept_id"] for route in routes} == {"workflows", "connections"}


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Copying a Learning Class shares the LearningActivity", "learning-lms-engagement"),
        ("LMS navigation is hidden on mobile", "learning-lms-engagement"),
        ("Creating a New Website sets an interaction value", "cms-websites"),
        ("Stuck consumer causes message loss on in-memory bus", "hosting-infrastructure"),
    ],
)
def test_issue_routing_covers_precise_open_issue_domains(title, expected):
    routes = route_issue("SparkDevNetwork/Rock", title=title, body="", labels=[])

    assert expected in {route["concept_id"] for route in routes}


def test_release_note_join_adds_official_fix_evidence():
    raw, _ = core_issue()
    raw["labels"] = [{"name": "Topic: Check-in"}]
    row = normalize_issue(
        "SparkDevNetwork/Rock",
        raw,
        release_notes=[
            {
                "id": "rock_core_release_notes:fixture",
                "source_id": "rock_core_release_notes",
                "source_url": "https://www.rockrms.com/releasenotes",
                "version": "19.3",
                "module": "Check-in",
                "summary": "Fixed the classic check-in issue. Fixes: #6917",
                "content_hash": "a" * 64,
            }
        ],
    )

    assert row["validation_state"] == "confirmed"
    assert row["release_note_refs"][0]["record_id"] == "rock_core_release_notes:fixture"
    assert any(
        evidence["source_kind"] == "release_note"
        and evidence["relationship"] == "fixed"
        and evidence["normalized_version"] == "19.3"
        for evidence in row["version_evidence"]
    )


def test_graphql_mapper_preserves_immutable_ids_and_current_label_ids():
    raw = graphql_issue_to_raw(
        {
            "id": "I_issue",
            "number": 42,
            "title": "Fixture",
            "url": "https://github.com/SparkDevNetwork/Rock/issues/42",
            "state": "OPEN",
            "labels": {"totalCount": 2, "nodes": [{"id": "L_topic", "name": "Topic: CMS"}]},
            "comments": {"totalCount": 3},
        }
    )

    assert raw["node_id"] == "I_issue"
    assert raw["labels"] == [{"node_id": "L_topic", "name": "Topic: CMS"}]
    assert raw["labels_truncated"] is True
    assert raw["comments"] == 3


def test_validator_rejects_duplicate_github_node_ids():
    raw, timeline = core_issue()
    raw["node_id"] = "I_same"
    first = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    raw = {**raw, "number": 6918, "html_url": "https://github.com/SparkDevNetwork/Rock/issues/6918"}
    second = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)

    with pytest.raises(ValueError, match="Duplicate GitHub node ID"):
        validate_rock_issue_rows([first, second])


def test_old_issue_location_alias_resolves_to_current_node():
    raw, timeline = core_issue()
    row = normalize_issue(
        "SparkDevNetwork/Rock",
        raw,
        timeline=timeline,
        previous={"location_id": "SparkDevNetwork/Rock#6000"},
    )

    assert row["location_aliases"] == ["SparkDevNetwork/Rock#6000"]
    assert find_issue_row([row], "SparkDevNetwork/Rock", 6000) == row


def test_d1_projection_has_first_class_issue_tables(monkeypatch):
    raw, timeline = core_issue()
    issue = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    row = {
        "id": issue["issue_id"],
        "kind": "rock_issue",
        "title": issue["title"],
        "body": issue["title"],
        "path": "agent/rock-issues.jsonl",
        "url": issue["url"],
        "concept": "check-in",
        "concepts": issue["concept_ids"],
        "topics": [],
        "authority_tier": issue["authority_tier"],
        "claim_tier": "routing_context_only",
        "source_id": issue["source_id"],
        "payload": issue,
    }

    sql = build_d1_seed_sql("v1", "2026-07-15T00:00:00Z", [row], [])

    assert "CREATE TABLE rock_issues" in sql
    assert "github_node_id TEXT NOT NULL UNIQUE" in sql
    assert "CREATE TABLE rock_issue_versions" in sql
    assert "CREATE TABLE rock_issue_locations" in sql
    assert "CREATE TABLE rock_issue_concepts" in sql
    assert "CREATE TABLE rock_issue_enrichments" in sql
    assert "rock_issue:SparkDevNetwork/Rock#6917" in sql


def test_reviewed_enrichment_is_projected_into_one_canonical_issue(monkeypatch, tmp_path):
    raw, timeline = core_issue()
    issue = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    reviewed_dir = tmp_path / "issues" / "check-in"
    reviewed_dir.mkdir(parents=True)
    enrichment_path = tmp_path / "agent" / "rock-issue-enrichments.jsonl"
    enrichment_path.parent.mkdir(parents=True)
    payload = {
        "schema": "rock-kb-rock-issue-enrichment-v1",
        "enrichment_id": "rock_issue_enrichment:core-6917-v1",
        "issue_id": issue["issue_id"],
        "diagnosis_status": "source_supported",
        "diagnosis_summary": "The public source identifies the parsing path that produced the exception.",
        "workaround_summaries": ["Use the corrected build and verify one representative check-in label before rollout."],
        "applicability": [
            {
                "assertion_id": "core-6917-affected-19.3.1",
                "component": "rock_core",
                "version_scheme": "rock_release",
                "versions": ["19.3.1"],
                "ranges": [],
                "status": "affected",
                "evidence_refs": [issue["url"]],
                "authority_tier": "source-code-confirmed",
                "claim_tier": "source_backed",
                "confidence": "high",
                "assessed_at": "2026-07-15T00:00:00Z",
            }
        ],
        "source_refs": [issue["url"]],
        "agent_run_ids": [],
        "authority_tier": "community-reviewed",
        "claim_tier": "source_backed",
        "confidence": "high",
        "review_status": "approved_for_public_distillation",
        "reviewer": "fixture-reviewer",
        "issue_updated_at": issue["updated_at"],
        "reviewed_at": "2026-07-15T00:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
    }
    (reviewed_dir / "core-6917.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(rock_issues, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(rock_issues, "ROCK_ISSUE_REVIEWED_DIR", tmp_path / "issues")
    monkeypatch.setattr(rock_issues, "ROCK_ISSUE_ENRICHMENT_PATH", enrichment_path)

    enrichments = build_reviewed_issue_enrichments([issue])
    joined = attach_issue_enrichments(issue, {issue["issue_id"]: enrichments})
    assessment = assess_issue(joined, {"core_version": "19.3.1"})

    assert len(enrichments) == 1
    assert list(read_jsonl(enrichment_path)) == enrichments
    assert assessment["applicability"] == "confirmed"
    assert assessment["reviewed_assertion_ids"] == ["core-6917-affected-19.3.1"]

    write_jsonl(tmp_path / "agent" / "rock-issues.jsonl", [issue])
    monkeypatch.setattr(service_projection, "REPO_ROOT", tmp_path)
    search_rows = service_projection.rock_issue_search_rows()
    assert len(search_rows) == 1
    assert search_rows[0]["payload"]["reviewed_enrichments"][0]["enrichment_id"] == payload["enrichment_id"]
    assert payload["diagnosis_summary"] in search_rows[0]["body"]

    current_metrics = build_reviewed_enrichment_metrics([issue], enrichments)
    assert current_metrics["reviewed_enrichment_count"] == 1
    assert current_metrics["reviewed_enrichment_metrics"] == {
        "issue_count": 1,
        "diagnosis_statuses": {"source_supported": 1},
        "confidences": {"high": 1},
        "revalidation_due_count": 0,
        "revalidation_due_enrichment_ids": [],
    }

    stale_issue = {**issue, "updated_at": "2026-07-16T00:00:00Z"}
    stale_metrics = build_reviewed_enrichment_metrics([stale_issue], enrichments)
    assert stale_metrics["reviewed_enrichment_metrics"]["revalidation_due_count"] == 1
    assert stale_metrics["reviewed_enrichment_metrics"]["revalidation_due_enrichment_ids"] == [
        "rock_issue_enrichment:core-6917-v1"
    ]
    stale_assessment = assess_issue(
        attach_issue_enrichments(stale_issue, {issue["issue_id"]: enrichments}),
        {"core_version": "19.3.1"},
    )
    assert stale_assessment["applicability"] == "likely"
    assert stale_assessment["reviewed_assertion_ids"] == []
    assert stale_assessment["revalidation_due_enrichment_ids"] == ["rock_issue_enrichment:core-6917-v1"]


def test_hypothesis_enrichment_cannot_be_promoted_as_source_backed(monkeypatch, tmp_path):
    raw, timeline = core_issue()
    issue = normalize_issue("SparkDevNetwork/Rock", raw, timeline=timeline)
    reviewed_dir = tmp_path / "issues"
    reviewed_dir.mkdir()
    payload = {
        "schema": "rock-kb-rock-issue-enrichment-v1",
        "enrichment_id": "rock_issue_enrichment:core-6917-hypothesis-v1",
        "issue_id": issue["issue_id"],
        "diagnosis_status": "hypothesis",
        "diagnosis_summary": "A bounded hypothesis.",
        "source_refs": [issue["url"]],
        "authority_tier": "community-reviewed",
        "claim_tier": "source_backed",
        "confidence": "low",
        "review_status": "approved_for_public_distillation",
        "reviewer": "fixture-reviewer",
        "issue_updated_at": issue["updated_at"],
        "reviewed_at": "2026-07-15T00:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
    }
    (reviewed_dir / "invalid.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(rock_issues, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(rock_issues, "ROCK_ISSUE_REVIEWED_DIR", reviewed_dir)

    with pytest.raises(ValueError, match="routing_context_only"):
        rock_issues.load_reviewed_issue_enrichments({issue["issue_id"]})


def test_reviewed_enrichment_requires_revision_bound_rfc3339_timestamps():
    payload = {
        "schema": "rock-kb-rock-issue-enrichment-v1",
        "enrichment_id": "rock_issue_enrichment:fixture-timestamps-v1",
        "issue_id": "rock_issue:SparkDevNetwork/Rock#6917",
        "diagnosis_status": "source_supported",
        "diagnosis_summary": "A bounded fixture diagnosis.",
        "source_refs": ["https://github.com/SparkDevNetwork/Rock/issues/6917"],
        "claim_tier": "source_backed",
        "confidence": "medium",
        "review_status": "approved_for_public_distillation",
        "reviewer": "fixture-reviewer",
        "issue_updated_at": "2026-07-14T22:33:30Z",
        "reviewed_at": "2026-07-15T00:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
    }

    assert RockIssueReviewedEnrichment.model_validate(payload).issue_updated_at == "2026-07-14T22:33:30Z"
    with pytest.raises(ValueError, match="RFC 3339"):
        RockIssueReviewedEnrichment.model_validate({**payload, "reviewed_at": "not-a-date"})
    with pytest.raises(ValueError, match="cannot be in the future"):
        RockIssueReviewedEnrichment.model_validate({**payload, "reviewed_at": "2099-01-01T00:00:00Z"})
