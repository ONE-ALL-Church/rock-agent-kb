from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Extraction helper commands.")

app.command("markdown")(legacy.extract_markdown)
app.command("doctor")(legacy.extractor_doctor)
