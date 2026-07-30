from rock_kb.concepts import Concept, get_concept
import rock_kb.concepts as concepts_module
from rock_kb.contribution_sources import public_contribution_records
from rock_kb.hydrate import (
    concept_search_terms,
    discover_repo_source_files,
    hydrate_source_record,
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


def test_hydrate_source_record_prefers_rockumentation_api(monkeypatch):
    payload = {
        "configurationValues": {
            "title": "Workflow Actions",
            "slug": "core-concepts/workflows/workflow-actions",
            "currentVersion": "v19.0",
        },
        "initialContent": (
            '<article class="rockumentation-article" data-main-article="true" '
            'data-article-id="2647"><h1>Workflow Actions</h1>'
            "<p>Workflow actions execute configured behavior.</p></article>"
        ),
    }
    monkeypatch.setattr(
        "rock_kb.hydrate.fetch_rockumentation_payload",
        lambda client, url: payload,
    )

    row = hydrate_source_record(
        object(),
        {
            "id": "rock_documentation:article:2647",
            "source_id": "rock_documentation",
            "source_url": "https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions",
            "source_title": "Workflow Actions",
        },
        ["workflow", "action"],
        max_chars=1000,
    )

    assert row["status"] == "ok"
    assert row["hydration_tool"] == "rockumentation_block_action"
    assert row["documentation_article_id"] == 2647
    assert row["documentation_current_version"] == "v19.0"
    assert "execute configured behavior" in row["excerpt"]


def test_github_source_hydration_pins_immutable_commit_ref():
    class Response:
        def __init__(self, *, payload=None, text="", status_code=200):
            self._payload = payload
            self.text = text
            self.status_code = status_code

        def json(self):
            return self._payload

    class Client:
        def get(self, url):
            if url == "https://api.github.com/repos/SparkDevNetwork/Rock":
                return Response(payload={"default_branch": "develop"})
            if "/git/trees/develop" in url:
                return Response(
                    payload={
                        "sha": "0123456789abcdef",
                        "tree": [{"type": "blob", "path": "Rock/Workflows/WorkflowAction.cs"}],
                    }
                )
            assert "0123456789abcdef" in url
            return Response(text="public class WorkflowAction { public void Execute() {} }")

    concept = Concept(
        id="workflows",
        title="Workflows",
        description="Workflow behavior.",
        keywords=["workflow", "action"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )

    rows = discover_repo_source_files(
        Client(),
        "SparkDevNetwork/Rock",
        concept_search_terms(concept),
        limit=1,
        max_chars=1000,
    )

    assert rows[0]["source_ref"] == "0123456789abcdef"
    assert "/blob/0123456789abcdef/" in rows[0]["url"]
    assert "/0123456789abcdef/" in rows[0]["raw_url"]


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
