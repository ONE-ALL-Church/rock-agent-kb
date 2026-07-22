from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "rock-kb-agent" / "SKILL.md"
CONTRIBUTOR_INSTRUCTIONS = REPO_ROOT / "docs" / "templates" / "agent-contributor-instructions.md"
ONBOARDING = REPO_ROOT / "docs" / "community-onboarding.md"


def test_agent_skill_requires_versioned_feedback_consent() -> None:
    text = SKILL.read_text(encoding="utf-8")
    normalized = " ".join(text.replace("\n> ", "\n").split())

    assert "## Feedback Consent" in text
    assert "Allow automatically, Ask each time, or Do not send" in normalized
    assert "May I remember that choice in private user-level memory?" in normalized
    assert "notice_version: 2" in text
    assert "quality_feedback: automatic" in text
    assert "usefulness_outcomes: automatic" in text
    assert "anonymous_installation: enabled" in text
    assert "cohort: community" in text
    assert "malfunction_reports: ask" in text
    assert "test_rounds: ask" in text
    assert "contributions: explicit_review" in text


def test_agent_skill_limits_standing_permission_to_exact_result_feedback() -> None:
    text = SKILL.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "Standing permission is not permission to report every search" in text
    assert "Submit at most one quality rating and one usefulness outcome per exact result" in text
    assert "`kb_report_issue` still requires confirmation for each report" in text
    assert "Contributions and public PRs always require explicit human review" in normalized
    assert "Never put this preference or the private installation marker" in text
    assert "uvx rock-kb telemetry disable" in text


def test_public_agent_guidance_repeats_consent_and_revocation_boundaries() -> None:
    contributor_text = CONTRIBUTOR_INSTRUCTIONS.read_text(encoding="utf-8")
    onboarding_text = ONBOARDING.read_text(encoding="utf-8")

    for text in (contributor_text, onboarding_text):
        assert "Allow automatically" in text
        assert "Ask each time" in text
        assert "Do not send" in text
        assert "private user-level memory" in text
        assert "revoke" in text

    assert "Standing permission applies only to exact-result `kb_feedback` and completed-task" in contributor_text
    assert "uvx rock-kb telemetry enable --cohort community --consent-attested" in contributor_text
    assert "Agents must still ask before each redaction-attested malfunction report" in onboarding_text
