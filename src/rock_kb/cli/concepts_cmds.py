from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Concept listing, hydration, and synthesis commands.")

app.command("list")(legacy.list_concepts)
app.command("synthesize")(legacy.synthesize_concept_command)
app.command("hydrate")(legacy.hydrate_concept_command)
