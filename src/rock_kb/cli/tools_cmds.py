from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Developer utility commands.")

app.command("repo-pack")(legacy.repo_pack)
