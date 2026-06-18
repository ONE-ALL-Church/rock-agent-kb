import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_artifact(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8").lower()


def test_workflows_best_answer_mentions_workflow_form_actions_and_live_launch_context():
    text = read_artifact("knowledge/concepts/workflows/answers/first-checks.md")

    for term in ["workflowtype", "launch path", "workflow records", "actions", "form fields"]:
        assert term in text


def test_mobile_best_answer_mentions_selector_theme_and_dark_mode_constraints():
    text = read_artifact("knowledge/concepts/mobile/answers/first-checks.md")

    for term in ["css selector", "block settings", "theme variables", "dark mode", "official mobile block docs"]:
        assert term in text


def test_security_best_answer_mentions_inherited_page_block_and_record_permissions():
    text = read_artifact("knowledge/concepts/security-permissions/answers/first-checks.md")

    for term in ["inherited page security", "block security", "auth rows", "view and edit", "record-level permission"]:
        assert term in text


def test_evaluation_report_has_no_failures():
    report = json.loads((REPO_ROOT / "agent/evaluation-report.json").read_text(encoding="utf-8"))

    assert report["question_count"] == report["result_count"]
    assert report["question_count"] >= 100
    assert report["fail_count"] == 0


def test_lava_risky_answer_mentions_webhook_security_and_live_review():
    text = read_artifact("knowledge/concepts/lava/answers/risks-caveats.md")

    for term in ["lava webhooks", "security by default", "page/block security", "enabled lava commands"]:
        assert term in text


def test_api_integration_risky_answer_mentions_lava_webhook_security():
    text = read_artifact("knowledge/concepts/api-integrations/answers/risks-caveats.md")

    for term in ["lava api", "lava webhooks", "security by default"]:
        assert term in text


def test_high_risk_lava_rows_require_review_and_live_verification():
    rows = {}
    path = REPO_ROOT / "agent/lava-capabilities.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rows[row["name"].lower()] = row

    for name in ["sql", "entity", "web request", "workflow activate"]:
        row = rows[name]
        assert row["risk_tier"] == "high"
        assert row["requires_security_review"] is True
        assert row["requires_live_instance_verification"] is True
        assert row["command_enablement_required"] is True


def test_lava_usage_examples_cover_agent_triage_cases():
    text = read_artifact("knowledge/concepts/lava/lava-agent-usage-examples.md")

    for term in [
        "lava-safety-matrix.md",
        "creating apis using lava",
        "sql",
        "entity",
        "web request",
        "workflow activate",
        "obsidian/helix",
        "mobile",
    ]:
        assert term in text


def test_lava_dependent_guides_link_capability_references():
    for concept in ["security-permissions", "workflows", "cms-websites", "api-integrations"]:
        text = read_artifact(f"knowledge/concepts/{concept}/index.md")
        for term in [
            "## lava capability references",
            "../lava/lava-reference-index.md",
            "../lava/lava-safety-matrix.md",
            "../lava/lava-agent-usage-examples.md",
            "../../../agent/lava-capabilities.jsonl",
        ]:
            assert term in text
