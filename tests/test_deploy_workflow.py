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


def release_workflow() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "release-client.yml"
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

    assert '- ".github/workflows/deploy-service.yml"' in workflow
    assert '- "src/rock_kb/source_native.py"' in workflow
    assert '- "src/rock_kb/schemas/source_native.py"' in workflow
    assert '- "src/rock_kb/source_family_contracts.py"' in workflow


def test_ci_quality_gates_use_bounded_local_worker_concurrency():
    repo_root = Path(__file__).resolve().parents[1]
    for name in (
        "deploy-service.yml",
        "public-surface.yml",
        "release-client.yml",
    ):
        workflow = (
            repo_root / ".github" / "workflows" / name
        ).read_text(encoding="utf-8")
        assert "uv run kb quality-gate --concurrency 3" in workflow


def test_release_uses_generic_conformance_for_immutable_previous_archives():
    workflow = release_workflow()
    build_step = workflow.split("- name: Build and validate OKF distribution", 1)[1].split(
        "- name: Attest OKF release archives", 1
    )[0]

    assert 'rock-kb okf conformance "${full_path}"' in build_step
    assert 'rock-kb okf conformance "${core_path}"' in build_step
    assert 'rock-kb okf verify "${full_path}"' not in build_step
    assert 'rock-kb okf verify "${core_path}"' not in build_step
    assert (
        'rock-kb okf verify "release-assets/rock-agent-kb-okf-v${version}.zip"'
        in build_step
    )
    assert (
        'rock-kb okf verify "release-assets/rock-agent-kb-okf-core-v${version}.zip"'
        in build_step
    )


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
    assert "Roll back failed canonical activation" in workflow
    assert "Verify automatic rollback" in workflow
    assert workflow.count("failure() && inputs.projection == 'canonical'") == 2
    assert "retrieval-projection legacy --apply" in workflow
