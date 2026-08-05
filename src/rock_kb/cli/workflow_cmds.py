from __future__ import annotations

import json
from pathlib import Path

import typer

from . import _legacy as legacy


def register(app: typer.Typer) -> None:
    app.command("status")(legacy.status_command)
    app.command("build")(legacy.build_command)
    app.command("deploy-service")(deploy_service_command)
    app.command("retrieval-projection")(retrieval_projection_command)
    app.command("service-retention")(service_retention_command)
    app.command("eval-service")(eval_service_command)
    app.command("record-hosted-eval", hidden=True)(record_hosted_eval_command)
    app.command("record-source-freshness", hidden=True)(record_source_freshness_command)
    app.command("quality-gate")(quality_gate_command)
    app.command("hybrid-shadow")(hybrid_shadow_command)
    app.command("shadow-lifecycle")(shadow_lifecycle_command)
    app.command("network-readiness")(network_readiness_command)
    app.command("serve")(serve_command)


def serve_command() -> None:
    """Run the read-only Rock KB MCP stdio server."""
    from ..serve.server import ServeDependencyError, run_stdio

    try:
        run_stdio()
    except ServeDependencyError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


def deploy_service_command(
    apply: bool = typer.Option(False, "--apply", help="Apply the projection to Cloudflare with Wrangler after building it."),
    env: str | None = typer.Option(None, "--env", help="Wrangler environment name."),
    bucket: str | None = typer.Option(None, "--bucket", help="R2 bucket name. Defaults to rock-agent-kb-artifacts."),
    database: str | None = typer.Option(None, "--database", help="D1 database name. Defaults to rock-agent-kb."),
    base_url: str | None = typer.Option(None, "--base-url", help="Current hosted service URL used to select the inactive R2 slot."),
) -> None:
    """Project public artifacts into the hosted service deployment payload."""
    from rich import print_json

    from ..service_projection import deploy_service_projection

    result = deploy_service_projection(apply=apply, env=env, bucket=bucket, database=database, base_url=base_url)
    print_json(data=result)


def retrieval_projection_command(
    projection: str = typer.Argument(
        ...,
        help="Active default reader: legacy or canonical.",
    ),
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Apply the guarded D1 switch and verify hosted health.",
    ),
    env: str | None = typer.Option(
        None,
        "--env",
        help="Wrangler environment name.",
    ),
    database: str | None = typer.Option(
        None,
        "--database",
        help="D1 database name. Defaults to rock-agent-kb.",
    ),
    base_url: str | None = typer.Option(
        None,
        "--base-url",
        help="Hosted service URL used for preflight and readback.",
    ),
) -> None:
    """Plan or apply a reversible active retrieval projection change."""
    from rich import print_json

    from ..service_projection import set_active_retrieval_projection

    print_json(
        data=set_active_retrieval_projection(
            projection,
            apply=apply,
            env=env,
            database=database,
            base_url=base_url,
        )
    )


def service_retention_command(
    base_url: str = typer.Option(..., "--base-url", help="Hosted Rock KB service URL."),
    bucket: str = typer.Option("rock-agent-kb-artifacts", "--bucket", help="R2 bucket name."),
    apply: bool = typer.Option(False, "--apply", help="Upsert the legacy artifact expiration rule through the Cloudflare API."),
) -> None:
    """Verify bounded artifact slots and configure safe legacy R2 cleanup."""
    from rich import print_json

    from ..service_projection import configure_bounded_artifact_retention

    print_json(data=configure_bounded_artifact_retention(base_url=base_url, bucket=bucket, apply=apply))


def eval_service_command(
    base_url: str = typer.Option(..., "--base-url", help="Hosted Rock KB service base URL."),
    limit: int = typer.Option(5, "--limit", min=1, max=20, help="Search hits to inspect per evaluation question."),
    target_rank: int = typer.Option(2, "--target-rank", min=1, max=20, help="Expected concept must appear at or above this result rank."),
    concurrency: int = typer.Option(6, "--concurrency", min=1, max=25, help="Concurrent hosted search requests."),
    output: Path | None = typer.Option(None, "--output", dir_okay=False, help="Write the complete ephemeral evaluation report for the deployment workflow."),
) -> None:
    """Run the public evaluation set against the hosted service search API."""
    from rich import print_json

    from ..service_eval import evaluate_service

    result = evaluate_service(base_url=base_url, limit=limit, target_rank=target_rank, concurrency=concurrency).as_dict()
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print_json(data=result)
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def record_hosted_eval_command(
    report: Path = typer.Argument(..., exists=True, dir_okay=False),
    database: str = typer.Option("rock-agent-kb", "--database"),
    env: str | None = typer.Option(None, "--env"),
) -> None:
    """Persist a trusted hosted-evaluation summary through Wrangler and D1."""
    from rich import print_json

    from ..hosted_evaluation import record_hosted_evaluation

    print_json(data=record_hosted_evaluation(report, database=database, env=env))


def record_source_freshness_command(
    report: Path = typer.Argument(..., exists=True, dir_okay=False),
    workflow_id: str = typer.Option(..., "--workflow-id"),
    workflow_max_age_hours: float | None = typer.Option(None, "--workflow-max-age-hours", min=1),
    source_ids: list[str] | None = typer.Option(None, "--source"),
    run_id: str = typer.Option("", "--run-id"),
    run_url: str = typer.Option("", "--run-url"),
    database: str = typer.Option("rock-agent-kb", "--database"),
    env: str | None = typer.Option(None, "--env"),
) -> None:
    """Persist a trusted public-safe source freshness snapshot through Wrangler and D1."""
    from rich import print_json

    from ..source_operations import record_source_freshness

    print_json(
        data=record_source_freshness(
            report,
            workflow_id=workflow_id,
            workflow_max_age_hours=workflow_max_age_hours,
            source_ids=source_ids,
            run_id=run_id,
            run_url=run_url,
            database=database,
            env=env,
        )
    )


def quality_gate_command(
    minimum_mrr: float = typer.Option(0.99, "--minimum-mrr", min=0, max=1),
    minimum_recall: float = typer.Option(1.0, "--minimum-recall", min=0, max=1),
    maximum_duplicate_rate: float = typer.Option(0.0, "--maximum-duplicate-rate", min=0, max=1),
    minimum_authority_pass_rate: float = typer.Option(1.0, "--minimum-authority-pass-rate", min=0, max=1),
    concurrency: int = typer.Option(6, "--concurrency", min=1, max=12),
    projection: str | None = typer.Option(
        None,
        "--projection",
        help="Reader to test. Defaults to the tracked cutover policy.",
    ),
) -> None:
    """Run the full lexical retrieval gate against an isolated local Worker and D1 database."""
    from rich import print_json

    from ..service_quality_gate import QualityThresholds, run_service_quality_gate

    result = run_service_quality_gate(
        thresholds=QualityThresholds(
            minimum_mrr=minimum_mrr,
            minimum_recall=minimum_recall,
            maximum_duplicate_rate=maximum_duplicate_rate,
            minimum_authority_pass_rate=minimum_authority_pass_rate,
        ),
        concurrency=concurrency,
        retrieval_projection=projection,
    )
    print_json(data=result)
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def hybrid_shadow_command(
    apply: bool = typer.Option(False, "--apply", help="Create the isolated AI Search instance, upload documents, and evaluate it."),
    instance: str = typer.Option("rock-kb-retrieval-shadow-stratified-dev", "--instance", help="Cloudflare AI Search instance name."),
    concurrency: int = typer.Option(8, "--concurrency", min=1, max=20, help="Concurrent upload requests."),
) -> None:
    """Build or run the isolated Cloudflare hybrid-search shadow pilot."""
    from rich import print_json

    from ..hybrid_shadow import (
        ensure_shadow_instance,
        ensure_shadow_projection,
        evaluate_shadow,
        shadow_cost_estimate,
        upload_shadow_documents,
        wait_for_shadow_index,
        wrangler_credentials,
    )

    rows = ensure_shadow_projection()
    result: dict[str, object] = {"schema": "rock-kb-hybrid-shadow-run-v1", "instance": instance, "document_count": len(rows), "estimated_embedding_cost": shadow_cost_estimate(rows), "applied": apply}
    if apply:
        credentials = wrangler_credentials()
        ensure_shadow_instance(credentials, instance=instance)
        result["upload"] = upload_shadow_documents(rows, credentials, instance=instance, concurrency=concurrency)
        result["stats"] = wait_for_shadow_index(
            credentials,
            expected_count=len(rows),
            expected_keys={str(row["key"]) for row in rows},
            instance=instance,
        )
        evaluation = evaluate_shadow(rows, credentials, instance=instance, concurrency=min(concurrency, 10))
        result["evaluation"] = {key: value for key, value in evaluation.items() if key != "results"}
        result["evaluation"]["results_path"] = "service/dist/hybrid-shadow-results.json"
    print_json(data=result)


def shadow_lifecycle_command(
    strict: bool = typer.Option(False, "--strict", help="Exit non-zero for expired instances or production routing."),
) -> None:
    """Audit the owner, review date, expiration, and routing boundary of shadow services."""
    from rich import print_json

    from ..shadow_lifecycle import shadow_lifecycle_report

    report = shadow_lifecycle_report()
    print_json(data=report)
    if strict and report["status"] != "ok":
        raise typer.Exit(code=1)


def network_readiness_command(
    repo: str = typer.Option("ONE-ALL-Church/rock-agent-kb", "--repo", help="GitHub repository to inspect."),
    pr: int | None = typer.Option(None, "--pr", help="Milestone pull request number to inspect."),
    private_corpus_path: str | None = typer.Option(None, "--private-corpus-path", help="Private corpus checkout path to verify."),
    skip_github: bool = typer.Option(False, "--skip-github", help="Skip live GitHub checks."),
    strict: bool = typer.Option(False, "--strict", help="Exit non-zero unless the network readiness status is pass."),
) -> None:
    """Audit the live gates for the Agent Knowledge Network milestones."""
    from pathlib import Path

    from rich import print_json

    from ..network_readiness import network_readiness_report

    result = network_readiness_report(
        repo=repo,
        pr=pr,
        private_corpus_path=Path(private_corpus_path).expanduser() if private_corpus_path else None,
        check_github=not skip_github,
    )
    print_json(data=result)
    if strict and result["status"] != "pass":
        raise typer.Exit(code=1)
