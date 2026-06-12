from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Public export and publish commands.")

app.command("export")(legacy.public_export)
