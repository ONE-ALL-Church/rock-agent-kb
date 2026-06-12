from types import SimpleNamespace

import pytest

from rock_kb import source_orchestration as so


def snapshot(records=None, media=None, claims=None):
    return {
        "source_records": records or {},
        "media_items": media or {},
        "claims": claims or {},
        "sources": {"rock_core_release_notes": {"status": "ok"}, "missing_source": {"status": "skipped"}},
    }


def test_source_scan_diff_reports_records_urls_release_model_map_and_media():
    previous = snapshot(
        records={
            "release:1": {"source_id": "rock_core_release_notes", "source_kind": "rock_release_notes", "source_url": "https://example.test/release-1", "content_hash": "old"},
            "model:1": {"source_id": "rock_model_map", "source_url": "https://example.test/model-1", "content_hash": "same"},
            "removed:1": {"source_id": "rock_documentation", "source_url": "https://example.test/removed", "content_hash": "gone"},
        },
        media={"media:old": {"transcribed": True}},
    )
    current = snapshot(
        records={
            "release:1": {"source_id": "rock_core_release_notes", "source_kind": "rock_release_notes", "source_url": "https://example.test/release-1", "content_hash": "new"},
            "model:1": {"source_id": "rock_model_map", "source_url": "https://example.test/model-1", "content_hash": "changed"},
            "new:1": {"source_id": "rock_documentation", "source_url": "https://example.test/new", "content_hash": "new"},
        },
        media={"media:old": {"transcribed": True}, "media:new": {"transcribed": False}},
    )

    diff = so.diff_source_snapshots(previous, current)

    assert diff["source_record_changes"]["changed_hash"] == ["model:1", "release:1"]
    assert diff["source_record_changes"]["new"] == ["new:1"]
    assert diff["source_record_changes"]["removed"] == ["removed:1"]
    assert diff["url_changes"]["new"] == ["https://example.test/new"]
    assert diff["url_changes"]["removed"] == ["https://example.test/removed"]
    assert diff["release_note_changes"] == ["release:1"]
    assert diff["model_map_changes"] == ["model:1"]
    assert diff["media_changes"]["new_media_items"] == ["media:new"]
    assert diff["media_changes"]["pending_transcription"] == ["media:new"]
    assert diff["source_family_status"]["skipped"] == ["missing_source"]


def test_source_scan_diff_merges_refresh_status_failures():
    current = snapshot(records={"record:1": {"source_id": "rock_documentation", "source_url": "https://example.test/1", "content_hash": "same"}})
    current["source_refresh_status"] = {"failed": ["rock_documentation"], "skipped": ["rock_qa"]}

    diff = so.diff_source_snapshots(snapshot(records=current["source_records"]), current)

    assert diff["source_family_status"]["failed"] == ["rock_documentation"]
    assert diff["source_family_status"]["skipped"] == ["missing_source", "rock_qa"]


def test_concept_impact_mapping_uses_direct_dependencies_and_inferred_keywords(monkeypatch):
    concepts = [
        SimpleNamespace(
            id="workflows",
            title="Workflows",
            keywords=["workflow"],
            depends_on_topics=["automation"],
        ),
        SimpleNamespace(
            id="mobile",
            title="Mobile",
            keywords=["mobile"],
            depends_on_topics=[],
        ),
    ]
    monkeypatch.setattr(so, "load_concepts", lambda: concepts)
    monkeypatch.setattr(
        so,
        "read_jsonl",
        lambda path: [{"concept_id": "workflows", "source_record_ids": ["direct:1"]}]
        if str(path).endswith("concept-dependencies.jsonl")
        else [],
    )
    records = {
        "direct:1": {"source_title": "Existing workflow record", "topics": []},
        "new:1": {"source_title": "Mobile block styling", "topics": ["mobile"]},
    }

    impacts = so.concept_impacts({"direct:1", "new:1"}, records)

    by_id = {row["concept_id"]: row for row in impacts}
    assert by_id["workflows"]["direct_source_record_ids"] == ["direct:1"]
    assert by_id["mobile"]["inferred_source_record_ids"] == ["new:1"]
    assert by_id["mobile"]["needs_authored_synthesis_review"] is True


def test_rebuild_plan_separates_deterministic_and_reviewer_ai_work():
    scan_report = {
        "summary": {
            "changed_source_records": 2,
            "new_source_records": 1,
            "removed_source_records": 0,
            "affected_concepts": 1,
            "affected_claims": 1,
            "affected_source_summaries": 1,
            "changed_model_map_rows": 1,
            "new_media_items": 1,
            "pending_media_items": 1,
        },
        "diff": {"media_changes": {"new_media_items": ["media:1"], "pending_transcription": ["media:1"]}},
        "impacts": {
            "affected_concepts": [{"concept_id": "mobile", "needs_authored_synthesis_review": True}],
            "affected_claims": [{"claim_id": "claim:1", "needs_live_verification": True}],
        },
    }
    guide_plan = {"needs_generated_index_rebuild": ["mobile"], "needs_long_form_guide_refresh": ["mobile"]}

    plan = so.build_rebuild_plan_from_scan(scan_report, guide_plan)

    commands = plan["commands"]
    assert "uv run kb build --stage claims" in commands
    assert "uv run kb modelmap build" in commands
    assert "uv run kb build --stage concepts" in commands
    assert "uv run kb build --stage refresh-claims" in commands
    assert "uv run kb build --stage agent-pack" in commands
    assert "uv run kb publish export" in commands
    reviewer_ids = {row["id"] for row in plan["reviewer_ai_work"]}
    assert {"media_review", "live_verification", "source_conflict_review", "authored_guide_synthesis"} <= reviewer_ids
    authored = [row for row in plan["reviewer_ai_work"] if row["id"] == "authored_guide_synthesis"][0]
    assert "uv run kb concepts synthesize --concept mobile" in authored["description"]
    assert "uv run kb build --stage guide-intel" in authored["description"]
    assert plan["safety"]["unreviewed_claim_promotion"] == "not_allowed"


def test_claim_add_change_remove_impacts_concepts_public_export_and_rebuild_steps(monkeypatch):
    monkeypatch.setattr(
        so,
        "load_concepts",
        lambda: [SimpleNamespace(id="mobile", title="Mobile", keywords=["mobile"], depends_on_topics=[])],
    )
    monkeypatch.setattr(so, "read_jsonl", lambda path: [])
    diff = {
        "source_record_changes": {"new": [], "removed": [], "changed_hash": []},
        "claim_changes": {"new": ["claim:new"], "changed_hash": ["claim:changed"], "removed": ["claim:removed"]},
    }
    current = snapshot(
        claims={
            "claim:new": {"claim_id": "claim:new", "claim_hash": "new", "concept_ids": ["mobile"], "source_record_ids": []},
            "claim:changed": {"claim_id": "claim:changed", "claim_hash": "changed", "concept_ids": ["mobile"], "source_record_ids": []},
        }
    )
    previous = snapshot(
        claims={
            "claim:changed": {"claim_id": "claim:changed", "claim_hash": "old", "concept_ids": ["mobile"], "source_record_ids": []},
            "claim:removed": {"claim_id": "claim:removed", "claim_hash": "removed", "concept_ids": ["mobile"], "source_record_ids": []},
        }
    )

    impacts = so.map_source_scan_impacts(diff, current, previous)
    summary = so.scan_summary(current, diff, impacts)
    plan = so.build_rebuild_plan_from_scan({"summary": summary, "diff": diff, "impacts": impacts}, {})

    assert {row["claim_id"]: row["change_type"] for row in impacts["affected_claims"]} == {
        "claim:changed": "changed_hash",
        "claim:new": "new",
        "claim:removed": "removed",
    }
    assert impacts["affected_concepts"][0]["concept_id"] == "mobile"
    assert "claims/approved-claims.jsonl" in impacts["affected_public_export_files"]
    assert "uv run kb build --stage claims" in plan["commands"]
    assert "uv run kb build --stage agent-pack" in plan["commands"]
    assert summary["claims_added"] == 1
    assert summary["claims_changed"] == 1
    assert summary["claims_removed"] == 1


def test_rebuild_pr_body_has_required_summary_and_safety_text():
    scan_report = {
        "summary": {
            "changed_source_records": 1,
            "new_source_records": 2,
            "removed_source_records": 0,
            "new_urls": 2,
            "removed_urls": 0,
            "changed_release_notes": 1,
            "changed_model_map_rows": 1,
            "new_media_items": 1,
            "affected_concepts": 2,
            "affected_claims": 3,
            "affected_source_summaries": 4,
            "claims_added": 1,
            "claims_changed": 2,
            "claims_removed": 0,
            "failed_source_families": 0,
            "skipped_source_families": 1,
            "manual_review_source_families": 2,
        }
    }
    plan = {
        "summary": {
            "deterministic_step_count": 2,
            "reviewer_step_count": 1,
            "guides_automatically_refreshed": ["mobile"],
            "guides_flagged_for_authored_synthesis": ["workflows"],
            "media_queued_for_transcription_or_review": 1,
            "live_verification_needs": 3,
        },
        "commands": ["uv run kb build --stage agent-pack", "uv run kb publish export"],
        "audit_commands": ["uv run kb audit public-export"],
        "verification": {"pytest": "202 passed"},
    }

    body = so.render_rebuild_pr_body(scan_report, plan)

    assert "Changed source records" in body
    assert "Affected source summaries: `4`" in body
    assert "Claims added / changed / removed: `1` / `2` / `0`" in body
    assert "Failed / skipped / manual-review source families: `0` / `1` / `2`" in body
    assert "Guides flagged for authored synthesis" in body
    assert "uv run kb build --stage agent-pack" in body
    assert "Unreviewed claims were not promoted automatically." in body
    assert "202 passed" in body


def test_public_payload_safety_gate_blocks_private_or_tokenized_terms():
    errors = so.public_payload_safety_errors("This body contains a raw transcript and access_token=secret")

    assert errors
    assert so.public_payload_safety_errors("See http://localhost/admin and /Users/briand/private.md")
    with pytest.raises(ValueError):
        so.render_rebuild_pr_body({"summary": {"changed_source_records": 0}}, {"summary": {}, "commands": [], "audit_commands": [], "verification": {"note": "access_token=secret"}})


def test_refresh_dashboard_summarizes_source_plan_and_evaluation_misses(tmp_path):
    scan_report = {
        "summary": {
            "changed_source_records": 2,
            "new_source_records": 1,
            "removed_source_records": 0,
            "new_urls": 1,
            "removed_urls": 0,
            "changed_release_notes": 1,
            "changed_model_map_rows": 0,
            "new_media_items": 1,
            "affected_concepts": 1,
            "affected_claims": 2,
            "failed_source_families": 0,
            "skipped_source_families": 1,
            "manual_review_source_families": 3,
        },
        "impacts": {"affected_concepts": [{"concept_id": "mobile"}]},
    }
    rebuild_plan = {
        "summary": {"deterministic_step_count": 2, "reviewer_step_count": 1},
        "deterministic_work": [{"id": "build_agent_pack", "command": "uv run kb build --stage agent-pack"}],
        "reviewer_ai_work": [{"id": "authored_guide_synthesis", "concept_id": "mobile", "description": "Refresh mobile guide."}],
    }
    evaluation_report = {
        "fail_count": 0,
        "term_miss_count": 1,
        "near_misses": [{"id": "eval:mobile:4", "concept_id": "mobile", "score": 0.833, "missing_terms": ["official mobile docs"]}],
    }
    output_dir = tmp_path / "dashboard"

    dashboard = so.build_refresh_dashboard_payload(scan_report, rebuild_plan, evaluation_report)
    markdown = so.render_refresh_dashboard_markdown(dashboard)
    rows = so.refresh_dashboard_jsonl_rows(dashboard)

    assert dashboard["schema"] == so.REFRESH_DASHBOARD_SCHEMA
    assert dashboard["summary"]["source_change_count"] == 6
    assert dashboard["summary"]["evaluation_term_miss_count"] == 1
    assert "Review answer evaluation term misses" in " ".join(dashboard["next_actions"])
    assert "eval:mobile:4" in markdown
    assert any(row["row_type"] == "evaluation_near_miss" for row in rows)

    scan_path = tmp_path / "scan.json"
    plan_path = tmp_path / "plan.json"
    eval_path = tmp_path / "eval.json"
    scan_path.write_text(__import__("json").dumps(scan_report), encoding="utf-8")
    plan_path.write_text(__import__("json").dumps(rebuild_plan), encoding="utf-8")
    eval_path.write_text(__import__("json").dumps(evaluation_report), encoding="utf-8")
    written = so.build_refresh_dashboard(scan_path, plan_path, eval_path, output_dir)

    assert written["summary"]["affected_concepts"] == 1
    assert (output_dir / "refresh-dashboard-report.json").exists()
    assert (output_dir / "refresh-dashboard-summary.md").exists()
    assert (output_dir / "refresh-dashboard-rows.jsonl").exists()
