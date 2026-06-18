from __future__ import annotations

import typer

from . import _legacy as legacy


def register(app: typer.Typer) -> None:
    app.command("status")(legacy.status_command)
    app.command("build")(legacy.build_command)
    app.command("deploy-service")(deploy_service_command)
    app.command("eval-service")(eval_service_command)
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
) -> None:
    """Project public artifacts into the hosted service deployment payload."""
    from rich import print_json

    from ..service_projection import deploy_service_projection

    result = deploy_service_projection(apply=apply, env=env, bucket=bucket, database=database)
    print_json(data=result)


def eval_service_command(
    base_url: str = typer.Option(..., "--base-url", help="Hosted Rock KB service base URL."),
    limit: int = typer.Option(5, "--limit", min=1, max=20, help="Search hits to inspect per evaluation question."),
    target_rank: int = typer.Option(2, "--target-rank", min=1, max=20, help="Expected concept must appear at or above this result rank."),
    concurrency: int = typer.Option(6, "--concurrency", min=1, max=25, help="Concurrent hosted search requests."),
) -> None:
    """Run the public evaluation set against the hosted service search API."""
    from rich import print_json

    from ..service_eval import evaluate_service

    result = evaluate_service(base_url=base_url, limit=limit, target_rank=target_rank, concurrency=concurrency).as_dict()
    print_json(data=result)
    if result["status"] != "ok":
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
