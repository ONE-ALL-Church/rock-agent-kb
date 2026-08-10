from __future__ import annotations

import json

import pytest
from bs4 import BeautifulSoup

from rock_kb.okf_export import rows_for_profile
from rock_kb.cli.ideas_cmds import relationships_for_record
from rock_kb.rock_ideas import (
    build_rock_idea_summary,
    canonical_idea_url,
    classify_idea_evidence_link,
    concept_ids_for_idea,
    concept_routes_for_idea,
    finalize_idea_row,
    idea_detail_refresh_urls,
    idea_next_page_target,
    normalize_planned_version_label,
    parse_ms_ajax_delta,
    parse_idea_detail_html,
    parse_idea_list_html,
    validate_rock_idea_rows,
)
from rock_kb.rock_idea_relationships import (
    build_rock_idea_verification_queue,
    model_aliases,
    release_evidence_hash,
    rock_idea_relationship_rows,
    validate_rock_idea_verification_reviews,
    validate_rock_idea_verification_queue,
    validate_rock_idea_relationship_rows,
    verification_candidate_set_hash,
    verification_evidence_set_hash,
)
from rock_kb import service_projection


LIST_HTML = """
<div class="row margin-b-lg">
  <div class="well"><h3>16</h3></div>
  <div class="feature-title">
    <h2><a href="/ideas/2137/workflow-action-search">Workflow Action Search</a></h2>
    <span class="label label-default">Workflow</span>
  </div>
  Private proposal wording that must not be retained.
  <span class="author">Example Person</span>, Example Organization
</div>
"""


def test_canonical_idea_url_stabilizes_encoded_and_unicode_paths() -> None:
    encoded = "https://community.rockrms.com/ideas/62/allow-%E2%80%9Ccombine%E2%80%9D-in-reports"
    unicode_path = "https://community.rockrms.com/ideas/62/allow-“combine”-in-reports"

    assert canonical_idea_url(encoded) == encoded
    assert canonical_idea_url(unicode_path) == encoded


DETAIL_HTML = """
<div class="feature-detail">
  <div class="well"><h3>7</h3></div>
  <div>
    <h2 class="h2">Add days to event duration</h2>
    <span class="label label-success">20.0</span>
    <span class="label label-default">Event</span>
    <span class="label label-success">Complete</span>
  </div>
  <div class="description">Private proposal body.</div>
  <span>Submitted by <strong>Example Person</strong>, Example Organization</span>
  <time datetime="2026-06-09T11:47:30-07:00"></time>
  <div class="response">
    <strong>Staff Person</strong>
    <time datetime="2026-06-10T00:00:00-07:00"></time>
    <div class="response-status">Private response wording.</div>
    <table>
      <tr><th>Planned Version</th><td>20.0</td></tr>
      <tr><th>Ministry Strength</th><td>1 / 5</td></tr>
      <tr><th>Feature Size</th><td>Small</td></tr>
    </table>
  </div>
</div>
"""


def test_list_parser_keeps_metadata_and_discards_proposal_identity() -> None:
    rows = parse_idea_list_html(LIST_HTML)

    assert rows == [
        {
            "number": 2137,
            "title": "Workflow Action Search",
            "url": "https://community.rockrms.com/ideas/2137/workflow-action-search",
            "category": "Workflow",
            "status": "open",
            "status_label": "Open",
            "status_is_inferred": True,
            "vote_count": 16,
            "planned_version": None,
            "submitted_at": None,
        }
    ]
    assert "Example Person" not in json.dumps(rows)
    assert "Private proposal" not in json.dumps(rows)


def test_detail_parser_keeps_bounded_lifecycle_shape_only() -> None:
    row = parse_idea_detail_html(
        DETAIL_HTML,
        "https://community.rockrms.com/ideas/2250/add-days-to-event-duration",
    )

    assert row is not None
    assert row["number"] == 2250
    assert row["status"] == "complete"
    assert row["planned_version"] == "20.0"
    assert row["ministry_strength"] == {"score": 1, "maximum": 5}
    assert row["feature_size"] == "Small"
    assert row["staff_response_present"] is True
    assert row["detail_shape_version"] == 2
    assert row["evidence_links"] == []
    serialized = json.dumps(row)
    assert "Private proposal" not in serialized
    assert "Private response" not in serialized
    assert "Example Person" not in serialized
    assert "Staff Person" not in serialized


def test_detail_parser_retains_only_allowlisted_link_targets_without_link_text() -> None:
    html = DETAIL_HTML.replace(
        "Private proposal body.",
        'Private proposal body. <a href="https://github.com/SparkDevNetwork/Rock/issues/6919">secret issue wording</a> '
        '<a href="/documentation/BookContent/1">documentation wording</a> '
        '<a href="https://untrusted.example/private?token=secret">do not keep</a>',
    ).replace(
        "Private response wording.",
        'Private response wording. <a href="https://www.rockrms.com/releasenotes/?Version=20.0">release wording</a> '
        '<a href="/ideas/2137/workflow-action-search">related idea wording</a>',
    )

    row = parse_idea_detail_html(html, "https://community.rockrms.com/ideas/2250/add-days-to-event-duration")

    assert row is not None
    assert row["evidence_links"] == [
        {
            "link_kind": "github_issue",
            "target_kind": "rock_issue",
            "target_id": "rock_issue:SparkDevNetwork/Rock#6919",
            "url": "https://github.com/SparkDevNetwork/Rock/issues/6919",
            "origin": "proposal",
            "authority_tier": "community-unreviewed",
        },
        {
            "link_kind": "official_documentation",
            "target_kind": "official_documentation",
            "url": "https://community.rockrms.com/documentation/BookContent/1",
            "origin": "proposal",
            "authority_tier": "official",
        },
        {
            "link_kind": "release_notes",
            "target_kind": "release_notes",
            "url": "https://www.rockrms.com/releasenotes/",
            "origin": "staff_response",
            "authority_tier": "official",
        },
        {
            "link_kind": "rock_idea",
            "target_kind": "rock_idea",
            "target_id": "rock_idea:2137",
            "url": "https://community.rockrms.com/ideas/2137/workflow-action-search",
            "origin": "staff_response",
            "authority_tier": "community-unreviewed",
        },
    ]
    serialized = json.dumps(row)
    assert "secret issue wording" not in serialized
    assert "token=secret" not in serialized
    assert "related idea wording" not in serialized


def test_legacy_planned_version_badge_is_normalized_to_the_detail_table_shape() -> None:
    assert normalize_planned_version_label("1.16.10") == "16.10"
    assert normalize_planned_version_label("1.4.1") == "4.1"
    assert normalize_planned_version_label("20.0") == "20.0"


def test_webforms_delta_parser_uses_length_prefixes_and_handles_emoji() -> None:
    panel = '<div><a href="javascript:__doPostBack(\'pager$next\',\'\')">Next</a> Idea \U0001f4a1</div>'
    hidden = "state-value"

    def record(record_type: str, record_id: str, value: str) -> str:
        length = len(value.encode("utf-16-le")) // 2
        return f"{length}|{record_type}|{record_id}|{value}|"

    payload = "1|#||4|" + record("updatePanel", "ideas", panel) + record("hiddenField", "__CVIEWSTATE", hidden)

    records = parse_ms_ajax_delta(payload)

    assert records == [("updatePanel", "ideas", panel), ("hiddenField", "__CVIEWSTATE", hidden)]
    assert idea_next_page_target(BeautifulSoup(panel, "html.parser")) == "pager$next"


def test_finalized_row_is_routing_only_and_concept_linked() -> None:
    row = finalize_idea_row(
        {
            "number": 2250,
            "title": "Add days to event duration",
            "url": "https://community.rockrms.com/ideas/2250/add-days-to-event-duration",
            "category": "Event",
            "status": "complete",
            "status_label": "Complete",
            "planned_version": "20.0",
        },
        checked_at="2026-07-17T00:00:00Z",
        previous=None,
    )

    validate_rock_idea_rows([row])
    assert row["claim_tier"] == "routing_context_only"
    assert row["authority_tier"] == "community-unreviewed"
    assert row["needs_live_verification"] is True
    assert "event-registration" in row["concept_ids"]


def test_detail_fields_are_preserved_until_the_next_bounded_detail_check() -> None:
    previous = finalize_idea_row(
        {
            "number": 2250,
            "title": "Add days to event duration",
            "category": "Event",
            "status": "complete",
            "planned_version": "20.0",
            "feature_size": "Small",
            "staff_response_present": True,
            "detail_last_checked_at": "2026-07-16T00:00:00Z",
        },
        checked_at="2026-07-16T00:00:00Z",
        previous=None,
    )

    current = finalize_idea_row(
        {
            "number": 2250,
            "title": "Add days to event duration",
            "category": "Event",
            "status": "complete",
        },
        checked_at="2026-07-17T00:00:00Z",
        previous=previous,
    )

    assert current["feature_size"] == "Small"
    assert current["planned_version"] == "20.0"
    assert current["staff_response_present"] is True
    assert current["detail_last_checked_at"] == "2026-07-16T00:00:00Z"

    detail_rechecked = finalize_idea_row(
        {
            "number": 2250,
            "title": "Add days to event duration",
            "category": "Event",
            "status": "open",
            "planned_version": None,
            "_detail_observed": True,
            "detail_last_checked_at": "2026-07-17T00:00:00Z",
        },
        checked_at="2026-07-17T00:00:00Z",
        previous=previous,
    )
    assert detail_rechecked["planned_version"] is None
    assert detail_rechecked["feature_size"] is None


def test_detail_refresh_prioritizes_new_and_changed_rows() -> None:
    discovered = {
        3: {"number": 3, "title": "New", "status": "open", "url": "https://community.rockrms.com/ideas/3"},
        2: {"number": 2, "title": "Changed", "status": "complete", "url": "https://community.rockrms.com/ideas/2"},
        1: {"number": 1, "title": "Same", "status": "open", "url": "https://community.rockrms.com/ideas/1"},
    }
    existing = {
        2: {"number": 2, "title": "Changed", "status": "open", "detail_last_checked_at": "2026-07-17T00:00:00Z"},
        1: {"number": 1, "title": "Same", "status": "open", "detail_last_checked_at": "2026-01-01T00:00:00Z"},
    }

    assert idea_detail_refresh_urls(discovered, existing, limit=2) == [
        "https://community.rockrms.com/ideas/2",
        "https://community.rockrms.com/ideas/3",
    ]


def test_summary_separates_check_change_result_and_detail_failure_metadata() -> None:
    row = finalize_idea_row(
        {"number": 1, "title": "Example", "category": "Other", "status": "open"},
        checked_at="2026-07-16T00:00:00Z",
        previous=None,
    )
    first = build_rock_idea_summary(
        [row],
        checked_at="2026-07-16T00:00:00Z",
        page_count=1,
        catalog_complete=True,
        detail_selected=2,
        detail_refreshed=1,
    )
    second = build_rock_idea_summary(
        [row],
        checked_at="2026-07-17T00:00:00Z",
        page_count=1,
        catalog_complete=True,
        detail_selected=2,
        detail_refreshed=1,
        normalized_rows=[
            {
                "id": "rock_ideas:1",
                "source_id": "rock_ideas",
                "source_title": "Example",
                "source_url": "https://community.rockrms.com/ideas/1",
                "content_hash": row["content_hash"],
            }
        ],
        previous=first,
    )

    assert second["status"] == "ok"
    assert second["result_count"] == 1
    assert second["last_checked_at"] == "2026-07-17T00:00:00Z"
    assert second["content_changed_at"] == "2026-07-16T00:00:00Z"
    assert second["detail_rows_failed"] == 1
    assert len(second["source_content_hash"]) == 64


def test_validation_rejects_raw_idea_content() -> None:
    row = finalize_idea_row(
        {"number": 1, "title": "Example", "category": "Other", "status": "open"},
        checked_at="2026-07-17T00:00:00Z",
        previous=None,
    )
    row["description"] = "Raw proposal text"

    with pytest.raises(ValueError, match="disallowed"):
        validate_rock_idea_rows([row])


def test_idea_projection_is_secondary_and_core_okf_excludes_it(tmp_path, monkeypatch) -> None:
    agent = tmp_path / "agent"
    agent.mkdir()
    row = finalize_idea_row(
        {
            "number": 2250,
            "title": "Add days to event duration",
            "url": "https://community.rockrms.com/ideas/2250/add-days-to-event-duration",
            "category": "Event",
            "status": "complete",
            "status_label": "Complete",
            "planned_version": "20.0",
        },
        checked_at="2026-07-17T00:00:00Z",
        previous=None,
    )
    (agent / "rock-ideas.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    (agent / "rock-idea-relationships.jsonl").write_text(
        json.dumps(
            {
                "source_id": "rock_idea:2250",
                "target_id": "rock_issue:SparkDevNetwork/Rock#6919",
                "target_kind": "rock_issue",
                "relationship_type": "references_issue",
                "signal": "#6919",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(service_projection, "REPO_ROOT", tmp_path)

    projected = service_projection.rock_idea_search_rows()

    assert projected[0]["id"] == "rock_idea:2250"
    assert projected[0]["kind"] == "rock_idea"
    assert projected[0]["claim_tier"] == "routing_context_only"
    assert "rock_issue:SparkDevNetwork/Rock#6919" in projected[0]["body"]
    assert service_projection.retrieval_index_policy(projected[0]) == "semantic_secondary"
    assert rows_for_profile(projected, "core") == []
    assert rows_for_profile(projected, "full") == projected


def test_concept_routing_uses_category_and_specific_title_signals() -> None:
    assert concept_ids_for_idea("Workflow", "Workflow e-sign document action") == [
        "workflows",
        "documents-signatures",
    ]
    assert concept_routes_for_idea("Workflow", "Workflow e-sign document action") == [
        {"concept_id": "workflows", "basis": "official_category", "signal": "Workflow"},
        {"concept_id": "documents-signatures", "basis": "title_keyword", "signal": "document"},
    ]


def test_relationship_projection_uses_exact_model_and_official_release_evidence() -> None:
    idea = finalize_idea_row(
        {
            "number": 2500,
            "title": "Registration Instance Fee Search",
            "category": "Event",
            "status": "complete",
            "status_label": "Complete",
            "planned_version": "20.0",
            "evidence_links": [
                classify_idea_evidence_link(
                    "https://github.com/SparkDevNetwork/Rock/issues/6919",
                    origin="staff_response",
                ),
                classify_idea_evidence_link(
                    "https://community.rockrms.com/documentation/bookcontent/10/288#achievementlabels",
                    origin="staff_response",
                ),
            ],
            "detail_shape_version": 2,
        },
        checked_at="2026-07-17T00:00:00Z",
        previous=None,
    )
    model_rows = [
        {
            "identity": {
                "model_slug": "registration-instance",
                "model_name": "Registration Instance",
                "model_title": "RegistrationInstance",
            }
        },
        {"identity": {"model_slug": "group", "model_name": "Group", "model_title": "Group"}},
    ]
    release_rows = [
        {
            "id": "rock_core_release_notes:fixture",
            "version": "20.0",
            "module": "Event",
            "release_family": "core",
            "summary": "Registration Instance Fee Search",
            "issue_refs": ["6919"],
        }
    ]
    issue_rows = [
        {
            "issue_id": "rock_issue:SparkDevNetwork/Rock#6919",
            "repository": "SparkDevNetwork/Rock",
            "number": 6919,
        }
    ]

    relationships, candidates = rock_idea_relationship_rows(
        [idea],
        model_rows=model_rows,
        release_rows=release_rows,
        issue_rows=issue_rows,
        source_rows=[
            {
                "source_record_id": "rock_documentation:fixture",
                "source_url": "https://community.rockrms.com/documentation/bookcontent/10/288",
            }
        ],
        checked_at="2026-07-17T00:00:00Z",
    )

    validate_rock_idea_relationship_rows(relationships, idea_rows=[idea])
    assert candidates == []
    assert {row["relationship_type"] for row in relationships} == {
        "about",
        "about_model",
        "references_issue",
        "references_official_documentation",
        "corroborated_by_release_note",
        "implemented_by_issue",
    }
    assert any(row.get("target_id") == "model_map:stable:registration-instance" for row in relationships)
    assert any(row.get("target_id") == "source:rock_documentation:fixture" for row in relationships)
    assert not any(row.get("target_id") == "model_map:stable:group" for row in relationships)
    assert "Private" not in json.dumps(relationships)


def test_verification_queue_prioritizes_lifecycle_claims_without_leaking_candidates() -> None:
    ideas = [
        finalize_idea_row(
            {
                "number": 1,
                "title": "Completed feature",
                "category": "Core",
                "status": "complete",
                "status_label": "Complete",
                "planned_version": "20.0",
                "vote_count": 30,
            },
            checked_at="2026-07-17T00:00:00Z",
            previous=None,
        ),
        finalize_idea_row(
            {
                "number": 2,
                "title": "Planned feature",
                "category": "Workflow",
                "status": "planned",
                "status_label": "Planned",
                "planned_version": "21.0",
                "vote_count": 45,
            },
            checked_at="2026-07-17T00:00:00Z",
            previous=None,
        ),
        finalize_idea_row(
            {
                "number": 3,
                "title": "Open feature",
                "category": "Other",
                "status": "open",
                "status_label": "Open",
                "vote_count": 100,
            },
            checked_at="2026-07-17T00:00:00Z",
            previous=None,
        ),
    ]
    relationship = {
        "relationship_id": "rock_idea_relationship:official",
        "source_id": "rock_idea:1",
        "relationship_type": "corroborated_by_release_note",
        "authority_tier": "official",
        "confidence": "high",
        "content_hash": "relationship-hash",
    }
    candidate = {
        "candidate_id": "rock_idea_relationship_candidate:private",
        "source_id": "rock_idea:2",
        "release_record_id": "private-release-candidate",
        "title_token_coverage": 0.8,
    }

    queue, summary = build_rock_idea_verification_queue(
        ideas,
        relationships=[relationship],
        candidates=[candidate],
        checked_at="2026-07-17T00:00:00Z",
    )

    validate_rock_idea_verification_queue(queue, idea_rows=ideas)
    by_id = {row["idea_id"]: row for row in queue}
    assert set(by_id) == {"rock_idea:1", "rock_idea:2"}
    assert by_id["rock_idea:1"]["verification_state"] == "officially_corroborated"
    assert by_id["rock_idea:2"]["verification_state"] == "candidate_review_pending"
    assert by_id["rock_idea:2"]["priority_score"] > by_id["rock_idea:1"]["priority_score"]
    assert summary["queue_count"] == 2
    assert summary["candidate_review_count"] == 1
    assert summary["officially_corroborated_count"] == 1
    public_text = json.dumps(queue)
    assert "private-release-candidate" not in public_text
    assert "rock_idea_relationship_candidate:private" not in public_text

    updated_candidates = [{**candidate, "title_token_coverage": 0.9}]
    updated_queue, _ = build_rock_idea_verification_queue(
        ideas,
        relationships=[relationship],
        candidates=updated_candidates,
        checked_at="2026-07-17T00:00:00Z",
    )
    updated_by_id = {row["idea_id"]: row for row in updated_queue}
    assert updated_by_id["rock_idea:2"]["review_input_hash"] != by_id["rock_idea:2"]["review_input_hash"]


def test_maintainer_review_promotes_a_current_release_candidate() -> None:
    idea = finalize_idea_row(
        {
            "number": 1399,
            "title": "Add the ability to input family address from Check-In",
            "category": "Check-in",
            "status": "complete",
            "status_label": "Complete",
            "planned_version": "17.0",
            "vote_count": 50,
        },
        checked_at="2026-07-18T00:00:00Z",
        previous=None,
    )
    release = {
        "id": "rock_core_release_notes:family-address",
        "version": "17.0",
        "module": "Check-in",
        "release_family": "core",
        "change_type": "bug_fix",
        "summary": "Fixed Next Gen Check-In not saving a family address.",
        "issue_refs": ["6224"],
    }
    base_relationships, candidates = rock_idea_relationship_rows(
        [idea],
        model_rows=[],
        release_rows=[release],
        issue_rows=[],
        checked_at="2026-07-18T00:00:00Z",
    )
    assert len(candidates) == 1
    review = {
        "schema": "rock-kb-rock-idea-verification-review-v1",
        "review_id": "rock_idea_verification_review:1399",
        "idea_id": "rock_idea:1399",
        "source_content_hash": idea["content_hash"],
        "evidence_relationship_set_hash": verification_evidence_set_hash(base_relationships),
        "candidate_set_hash": verification_candidate_set_hash(candidates),
        "outcome": "corroborated_by_release_note",
        "reason_code": "official_release_note_describes_same_shipped_behavior",
        "candidate_id": candidates[0]["candidate_id"],
        "release_record_id": release["id"],
        "release_evidence_hash": release_evidence_hash(release),
        "reviewer": "delegated-reviewer",
        "reviewed_at": "2026-07-18T01:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
    }
    validate_rock_idea_verification_reviews([review], idea_rows=[idea])

    relationships, _ = rock_idea_relationship_rows(
        [idea],
        model_rows=[],
        release_rows=[release],
        issue_rows=[],
        verification_reviews=[review],
        checked_at="2026-07-18T00:00:00Z",
    )
    reviewed = [row for row in relationships if row.get("review_state") == "maintainer_reviewed"]
    assert len(reviewed) == 1
    assert reviewed[0]["relationship_type"] == "corroborated_by_release_note"
    assert reviewed[0]["basis"] == "maintainer_reviewed_official_release_match"
    assert reviewed[0]["metadata"]["review_id"] == review["review_id"]

    queue, summary = build_rock_idea_verification_queue(
        [idea],
        relationships=relationships,
        candidates=candidates,
        verification_reviews=[review],
        checked_at="2026-07-18T00:00:00Z",
    )
    assert queue[0]["verification_state"] == "officially_corroborated"
    assert queue[0]["verification_review_id"] == review["review_id"]
    assert queue[0]["priority_band"] == "low"
    assert summary["maintainer_reviewed_count"] == 1


def test_negative_review_closes_current_inputs_and_requeues_when_candidates_change() -> None:
    idea = finalize_idea_row(
        {
            "number": 62,
            "title": "Combine family members in reports",
            "category": "Reporting",
            "status": "complete",
            "status_label": "Complete",
            "planned_version": "13.4",
            "vote_count": 136,
        },
        checked_at="2026-07-18T00:00:00Z",
        previous=None,
    )
    review = {
        "schema": "rock-kb-rock-idea-verification-review-v1",
        "review_id": "rock_idea_verification_review:62",
        "idea_id": "rock_idea:62",
        "source_content_hash": idea["content_hash"],
        "evidence_relationship_set_hash": verification_evidence_set_hash([]),
        "candidate_set_hash": verification_candidate_set_hash([]),
        "outcome": "no_official_match",
        "reason_code": "no_matching_official_evidence_in_current_inputs",
        "reviewer": "delegated-reviewer",
        "reviewed_at": "2026-07-18T01:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
    }
    queue, _ = build_rock_idea_verification_queue(
        [idea],
        relationships=[],
        candidates=[],
        verification_reviews=[review],
    )
    assert queue[0]["verification_state"] == "maintainer_reviewed_no_official_match"
    assert queue[0]["recommended_action"] == "revalidate_when_review_inputs_change"
    assert queue[0]["priority_band"] == "low"

    candidate = {
        "candidate_id": "rock_idea_relationship_candidate:new",
        "source_id": "rock_idea:62",
        "release_record_id": "rock_core_release_notes:new",
        "title_token_coverage": 0.8,
    }
    updated_queue, _ = build_rock_idea_verification_queue(
        [idea],
        relationships=[],
        candidates=[candidate],
        verification_reviews=[review],
    )
    assert updated_queue[0]["verification_state"] == "candidate_review_pending"
    assert updated_queue[0]["verification_review_id"] is None


def test_verification_review_rejects_free_form_content() -> None:
    idea = finalize_idea_row(
        {
            "number": 1,
            "title": "Reviewed idea",
            "category": "Core",
            "status": "complete",
            "status_label": "Complete",
        },
        checked_at="2026-07-18T00:00:00Z",
        previous=None,
    )
    review = {
        "schema": "rock-kb-rock-idea-verification-review-v1",
        "review_id": "rock_idea_verification_review:1",
        "idea_id": "rock_idea:1",
        "source_content_hash": idea["content_hash"],
        "evidence_relationship_set_hash": verification_evidence_set_hash([]),
        "candidate_set_hash": verification_candidate_set_hash([]),
        "outcome": "no_official_match",
        "reason_code": "no_matching_official_evidence_in_current_inputs",
        "reviewer": "delegated-reviewer",
        "reviewed_at": "2026-07-18T01:00:00Z",
        "redaction_attestation": True,
        "license_attestation": True,
        "notes": "Free-form reviewer text must not be published.",
    }
    with pytest.raises(ValueError, match="unsupported fields"):
        validate_rock_idea_verification_reviews([review], idea_rows=[idea])


def test_model_aliases_keep_human_and_code_names_but_exclude_generic_single_tokens() -> None:
    aliases = model_aliases(
        [
            {
                "identity": {
                    "model_slug": "registration-instance",
                    "model_name": "Registration Instance",
                    "model_title": "RegistrationInstance",
                }
            },
            {"identity": {"model_slug": "person", "model_name": "Person", "model_title": "Person"}},
            {
                "identity": {
                    "model_slug": "registration",
                    "model_name": "Registration",
                    "model_title": "Registration",
                }
            },
        ]
    )

    assert {row["phrase"] for row in aliases} == {"registration instance", "registrationinstance"}


def test_local_idea_relationships_report_outbound_and_inbound_directions() -> None:
    rows = [
        {"source_id": "rock_idea:1", "target_id": "rock_issue:SparkDevNetwork/Rock#2"},
        {"source_id": "rock_idea:3", "target_id": "rock_idea:1"},
        {"source_id": "rock_idea:4", "target_id": "concept:groups"},
    ]

    relationships = relationships_for_record(rows, "rock_idea:1")

    assert [(row["direction"], row["related_record_id"]) for row in relationships] == [
        ("outbound", "rock_issue:SparkDevNetwork/Rock#2"),
        ("inbound", "rock_idea:3"),
    ]
