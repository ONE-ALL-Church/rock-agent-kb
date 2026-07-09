from __future__ import annotations

import json
from pathlib import Path

import typer

from . import _legacy as legacy
from ..okf_export import build_okf_export

app = typer.Typer(help="Public export and publish commands.")

app.command("export")(legacy.public_export)


@app.command("okf")
def okf_export(destination: Path | None = typer.Option(None, "--destination", "-d", file_okay=False, dir_okay=True)) -> None:
    """Build an optional typed-Markdown projection for Open Knowledge Format consumers."""
    result = build_okf_export(destination)
    legacy.console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)
