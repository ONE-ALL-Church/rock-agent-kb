from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Review and refresh report commands.")

app.command("refresh")(legacy.report_refresh)
app.command("dashboard")(legacy.refresh_dashboard_command)
