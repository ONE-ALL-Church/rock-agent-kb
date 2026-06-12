from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Public contribution bundle commands.")

app.command("new")(legacy.contribution_new)
app.command("check")(legacy.contribution_check)
app.command("validate")(legacy.contribution_validate)
app.command("promote")(legacy.contribution_promote)
