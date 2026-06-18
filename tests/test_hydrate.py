from rock_kb.concepts import get_concept
import rock_kb.concepts as concepts_module
from rock_kb.contribution_sources import public_contribution_records
from rock_kb.hydrate import (
    concept_search_terms,
    language_for_path,
    relevant_code_excerpt,
    relevant_excerpt,
    score_github_tree,
    score_path,
)
from rock_kb.jsonl import write_jsonl


def test_relevant_excerpt_prefers_keyword_chunks():
    text = (
        "General introduction that does not matter much.\n\n"
        "Check-in uses families, attendance, kiosks, schedules, locations, and labels together.\n\n"
        "Another unrelated paragraph about a different feature."
    )

    excerpt = relevant_excerpt(text, ["check-in", "attendance", "labels"], max_chars=80)

    assert "Check-in uses families" in excerpt
    assert "unrelated" not in excerpt


def test_relevant_code_excerpt_returns_line_context():
    source = "\n".join(
        [
            "namespace Rock.CheckIn;",
            "public class Helper {",
            "  public void PrintLabel() {",
            "    var attendance = new AttendanceCode();",
            "  }",
            "}",
        ]
    )

    excerpt = relevant_code_excerpt(source, ["attendance", "label"], max_chars=500, context=1)

    assert "3:   public void PrintLabel()" in excerpt
    assert "4:     var attendance" in excerpt


def test_score_path_matches_compact_and_spaced_terms():
    score, matched = score_path("Rock/CheckIn/AttendanceLabel.cs", ["check-in", "mobile check-in", "attendance"])

    assert score > 0
    assert "check-in" in matched
    assert "attendance" in matched


def test_score_github_tree_filters_to_text_files():
    rows = score_github_tree(
        [
            {"type": "blob", "path": "Rock/CheckIn/AttendanceLabel.cs"},
            {"type": "blob", "path": "Rock/CheckIn/logo.png"},
            {"type": "tree", "path": "Rock/CheckIn"},
        ],
        ["check-in", "attendance"],
    )

    assert [row["path"] for row in rows] == ["Rock/CheckIn/AttendanceLabel.cs"]


def test_concept_search_terms_expands_hyphenated_terms():
    terms = concept_search_terms(get_concept("check-in"))

    assert "check-in" in terms
    assert "check in" in terms
    assert "checkin" in terms


def test_language_for_path():
    assert language_for_path("Rock/CheckIn/Thing.cs") == "C#"
    assert language_for_path("Themes/foo.lava") == "Lava"


def test_public_contribution_records_convert_reviewed_bundles(tmp_path):
    bundle = tmp_path / "org" / "bundle.jsonl"
    write_jsonl(
        bundle,
        [
            {
                "schema": "rock-kb-org-contribution-v1",
                "contribution_id": "org:workflow-pattern",
                "org_id": "org",
                "org_display_name": "Example Org",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Workflow Pattern",
                "distilled_summary": "Use a reviewed workflow pattern with official source support.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "redaction_attestation": True,
                "review_status": "redaction_reviewed",
                "license_attestation": True,
                "confidence": "medium",
                "needs_live_verification": True,
            },
            {
                "schema": "rock-kb-org-contribution-v1",
                "contribution_id": "org:draft",
                "org_id": "org",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft",
                "distilled_summary": "Draft.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "redaction_attestation": False,
                "review_status": "draft_private",
                "license_attestation": False,
                "confidence": "needs_review",
                "needs_live_verification": True,
            },
        ],
    )

    records = public_contribution_records("workflows", root=tmp_path)

    assert len(records) == 1
    assert records[0]["source_id"] == "org_contribution"
    assert records[0]["contribution_id"] == "org:workflow-pattern"
    assert records[0]["authority_tier"] == "community-reviewed"
    assert records[0]["claim_tier"] == "routing_context_only"
    assert records[0]["source_urls"] == ["https://community.rockrms.com/documentation"]


def test_public_contribution_records_prefer_promoted_bundle_over_intake_copy(tmp_path):
    intake = tmp_path / "community-contributions" / "org" / "bundle.jsonl"
    promoted = tmp_path / "contributions" / "org" / "bundle.jsonl"
    row = {
        "schema": "rock-kb-org-contribution-v1",
        "contribution_id": "org:checkin-capacity",
        "org_id": "org",
        "org_display_name": "Example Org",
        "concept_ids": ["check-in"],
        "contribution_type": "entity_note",
        "title": "Check-in Capacity",
        "distilled_summary": "Separate room capacity from schedule availability.",
        "source_urls": ["https://community.rockrms.com/ModelMap"],
        "source_record_ids": [],
        "redaction_attestation": True,
        "review_status": "redaction_reviewed",
        "license_attestation": True,
        "confidence": "medium",
        "needs_live_verification": True,
    }
    write_jsonl(intake, [row])
    write_jsonl(promoted, [{**row, "source_review_origin": "community_contribution"}])

    records = public_contribution_records("check-in", root=tmp_path)

    assert len(records) == 1
    assert records[0]["bundle_path"].endswith("contributions/org/bundle.jsonl")
    assert records[0]["authority_tier"] == "community-reviewed"
    assert records[0]["source_review_origin"] == "community_contribution"


def test_concept_synthesis_pack_includes_public_contributions(monkeypatch):
    monkeypatch.setattr(
        concepts_module,
        "public_contribution_records",
        lambda concept_id: [
            {
                "id": "org_contribution:org:workflow-pattern",
                "source_id": "org_contribution",
                "source_title": "Workflow Pattern",
                "summary": "Reviewed org contribution.",
                "topics": [concept_id],
                "content_hash": "hash",
                "contribution_id": "org:workflow-pattern",
                "source_urls": ["https://community.rockrms.com/documentation"],
            }
        ],
    )

    pack = concepts_module.concept_synthesis_pack("workflows", limit=1)

    assert pack["contribution_records"]
    assert pack["contribution_records"][0]["source_id"] == "org_contribution"
