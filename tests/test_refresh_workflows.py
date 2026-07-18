from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"


def workflow_text(name: str) -> str:
    return (WORKFLOW_DIR / name).read_text(encoding="utf-8")


def test_required_pull_request_checks_support_explicit_dispatch() -> None:
    for name in ("public-surface.yml", "validate-contributions.yml"):
        event_section = workflow_text(name).split("on:", 1)[1].split("permissions:", 1)[0]

        assert "workflow_dispatch:" in event_section
        assert "pull_request:" in event_section


def test_automated_refreshes_dispatch_both_required_checks() -> None:
    for name in ("refresh-rock-issues.yml", "refresh.yml"):
        text = workflow_text(name)
        dispatch_step = text.split("- name: Dispatch required pull request checks", 1)[1]

        assert "actions: write" in text
        assert "id: refresh_pr" in text
        assert "steps.refresh_pr.outputs.pull-request-number != ''" in dispatch_step
        assert "steps.refresh_pr.outputs.pull-request-branch" in dispatch_step
        assert 'gh workflow run public-surface.yml --ref "$PR_BRANCH"' in dispatch_step
        assert 'gh workflow run validate-contributions.yml --ref "$PR_BRANCH"' in dispatch_step
