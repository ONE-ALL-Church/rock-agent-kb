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


@app.command("freshness")
def source_freshness_command(
    output_dir: Path = typer.Option(Path("data/review/source-freshness"), "--output-dir", file_okay=False),
    source_status: Path | None = typer.Option(None, "--source-status", exists=True, dir_okay=False),
    strict: bool = typer.Option(False, "--strict", help="Exit non-zero when required sources are failed, missing, or overdue."),
) -> None:
    """Classify every registered source against its expected refresh cadence."""
    from rich import print_json

    from ..source_freshness import build_source_freshness_report

    report = build_source_freshness_report(output_dir=output_dir, source_status_path=source_status)
    print_json(data=report)
    if strict and report["status"] != "ok":
        raise typer.Exit(code=1)
