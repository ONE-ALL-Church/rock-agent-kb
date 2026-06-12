from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Claim validation and live-verification planning commands.")

app.command("validate")(legacy.validate_claims_command)
app.command("live-plan")(legacy.live_verification_plan)
