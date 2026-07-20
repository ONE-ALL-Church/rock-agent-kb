from __future__ import annotations

from pathlib import Path

import typer

from . import _legacy as legacy

app = typer.Typer(help="Source registry and ingestion commands.")

app.command("list")(legacy.list_sources)
app.command("validate")(legacy.validate_sources)
app.command("discover")(legacy.discover)
app.command("discover-community")(legacy.discover_community)
app.command("fetch")(legacy.fetch)
app.command("normalize")(legacy.normalize)
app.command("summarize")(legacy.summarize)
app.command("refresh")(legacy.refresh)
app.command("probe-endpoints")(legacy.probe_endpoint_command)
app.command("scan")(legacy.source_scan_command)


@app.command("workflow-sources", hidden=True)
def source_workflow_sources_command(
    workflow_id: str = typer.Argument(...),
) -> None:
    """Print the registered source ids owned by one refresh workflow."""
    from ..source_workflows import source_workflow_policy

    for source_id in source_workflow_policy(workflow_id)["source_ids"]:
        typer.echo(source_id)


@app.command("freshness")
def source_freshness_command(
    output_dir: Path = typer.Option(Path("data/review/source-freshness"), "--output-dir", file_okay=False),
    source_status: Path | None = typer.Option(None, "--source-status", exists=True, dir_okay=False),
    baseline_snapshot: Path | None = typer.Option(None, "--baseline-snapshot", exists=True, dir_okay=False),
    previous_observations: Path | None = typer.Option(None, "--previous-observations", exists=True, dir_okay=False),
    required_cadence: list[str] = typer.Option(
        [],
        "--required-cadence",
        help="Restrict the strict freshness gate to one or more cadences while retaining all rows in the report.",
    ),
    required_workflow: str | None = typer.Option(
        None,
        "--required-workflow",
        help="Restrict the strict freshness gate to sources owned by one configured workflow.",
    ),
    strict: bool = typer.Option(False, "--strict", help="Exit non-zero when required sources are failed, missing, or overdue."),
) -> None:
    """Classify every registered source against its expected refresh cadence."""
    from rich import print_json

    from ..source_freshness import build_source_freshness_report
    from ..source_workflows import source_workflow_policy

    if required_cadence and required_workflow:
        raise typer.BadParameter("Use either --required-cadence or --required-workflow, not both.")
    required_source_ids = (
        source_workflow_policy(required_workflow)["source_ids"] if required_workflow else []
    )

    report = build_source_freshness_report(
        output_dir=output_dir,
        source_status_path=source_status,
        baseline_snapshot_path=baseline_snapshot,
        previous_observations_path=previous_observations,
        required_cadences=required_cadence,
        required_source_ids=required_source_ids,
    )
    print_json(data=report)
    if strict and report["status"] != "ok":
        raise typer.Exit(code=1)
