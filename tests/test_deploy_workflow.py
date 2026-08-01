from pathlib import Path


def deploy_workflow() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "deploy-service.yml"
    ).read_text(encoding="utf-8")


def test_hosted_smoke_test_retries_cloudflare_propagation_failures():
    workflow = deploy_workflow()
    smoke_step = workflow.split("- name: Smoke-test hosted service", 1)[1].split(
        "- name: Enforce bounded artifact retention", 1
    )[0]

    assert smoke_step.count("--retry 12") == 5
    assert smoke_step.count("--retry-all-errors") == 5
    assert smoke_step.count("--retry-delay 5") == 5
    assert '"${ROCK_KB_BASE_URL}/skill/manifest.json"' in smoke_step


def test_source_native_pipeline_changes_trigger_service_deploy():
    workflow = deploy_workflow()

    assert '- "src/rock_kb/source_native.py"' in workflow
    assert '- "src/rock_kb/schemas/source_native.py"' in workflow
    assert '- "src/rock_kb/source_family_contracts.py"' in workflow
