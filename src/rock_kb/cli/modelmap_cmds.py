from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Model-map build and scrape utilities.")

app.command("build")(legacy.build_model_map_command)
app.command("stamp")(legacy.stamp_model_map_scrape_version_command)
app.command("diff")(legacy.diff_model_map_scrapes_command)
