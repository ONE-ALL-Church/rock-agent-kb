from pathlib import Path


def deploy_workflow() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "deploy-service.yml"
    ).read_text(encoding="utf-8")


def projection_workflow() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "set-retrieval-projection.yml"
    ).read_text(encoding="utf-8")


def test_hosted_smoke_test_retries_cloudflare_propagation_failures():
    workflow = deploy_workflow()
    smoke_step = workflow.split("- name: Smoke-test hosted service", 1)[1].split(
        "- name: Enforce bounded artifact retention", 1
    )[0]

    assert smoke_step.count("--retry 12") == 6
    assert smoke_step.count("--retry-all-errors") == 6
    assert smoke_step.count("--retry-delay 5") == 6
    assert '"${ROCK_KB_BASE_URL}/skill/manifest.json"' in smoke_step


def test_source_native_pipeline_changes_trigger_service_deploy():
    workflow = deploy_workflow()

    assert '- "src/rock_kb/source_native.py"' in workflow
    assert '- "src/rock_kb/schemas/source_native.py"' in workflow
    assert '- "src/rock_kb/source_family_contracts.py"' in workflow


def test_projection_workflow_is_guarded_reversible_and_serialized_with_deploys():
    workflow = projection_workflow()

    assert "environment: production" in workflow
    assert "group: rock-kb-production-deploy" in workflow
    assert "cancel-in-progress: false" in workflow
    assert "- canonical" in workflow
    assert "- legacy" in workflow
    assert 'retrieval-projection "${EXPECTED_PROJECTION}" --apply' in workflow
    assert "projection=legacy" in workflow
    assert "Run hosted retrieval evaluation" in workflow
