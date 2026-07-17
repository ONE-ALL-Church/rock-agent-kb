from pathlib import Path


def test_hosted_smoke_test_retries_cloudflare_propagation_failures():
    workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "deploy-service.yml").read_text(
        encoding="utf-8"
    )
    smoke_step = workflow.split("- name: Smoke-test hosted service", 1)[1].split(
        "- name: Enforce bounded artifact retention", 1
    )[0]

    assert smoke_step.count("--retry 12") == 3
    assert smoke_step.count("--retry-all-errors") == 3
    assert smoke_step.count("--retry-delay 5") == 3
