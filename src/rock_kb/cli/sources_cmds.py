from __future__ import annotations

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
