from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Private-source scan, distillation, review, and impact commands.")

app.command("scan")(legacy.private_scan)
app.command("ingest")(legacy.private_ingest)
app.command("review-report")(legacy.private_review_report_command)
app.command("distill")(legacy.distill_private)
app.command("stale")(legacy.private_stale)
app.command("impact")(legacy.private_impact)
