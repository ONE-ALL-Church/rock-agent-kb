from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"


def workflow_text(name: str) -> str:
    return (WORKFLOW_DIR / name).read_text(encoding="utf-8")


def test_required_pull_request_checks_run_when_draft_becomes_ready() -> None:
    for name in ("public-surface.yml", "validate-contributions.yml"):
        text = workflow_text(name)
        event_section = text.split("on:", 1)[1].split("permissions:", 1)[0]

        assert "workflow_dispatch:" in event_section
        assert "pull_request:" in event_section
        assert "ready_for_review" in event_section
        assert "github.event.pull_request.draft == false" in text


def test_automated_refreshes_use_draft_ready_review_gate() -> None:
    for name in ("refresh-rock-issues.yml", "refresh.yml"):
        text = workflow_text(name)
        permissions = text.split("permissions:", 1)[1].split("concurrency:", 1)[0]

        assert "actions: write" not in permissions
        assert "draft: always-true" in text
        assert "automated-refresh-pr-review.md" in text
        assert "Dispatch required pull request checks" not in text
        assert "gh workflow run public-surface.yml" not in text
        assert "gh workflow run validate-contributions.yml" not in text
