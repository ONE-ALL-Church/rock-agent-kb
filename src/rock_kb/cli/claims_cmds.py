from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Claim validation and live-verification planning commands.")

app.command("validate")(legacy.validate_claims_command)
app.command("live-plan")(legacy.live_verification_plan)
app.command("provenance")(legacy.claim_provenance_command)
app.command("evaluation-sample")(legacy.claim_evaluation_sample_command)
app.command("document-candidates")(legacy.document_claim_candidates_command)
app.command("document-promote")(legacy.document_claim_promote_command)
