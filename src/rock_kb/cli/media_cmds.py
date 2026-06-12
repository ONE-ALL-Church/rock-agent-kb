from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Private media discovery, transcription, review, and promotion commands.")

app.command("discover")(legacy.media_discover)
app.command("transcribe")(legacy.media_transcribe)
app.command("batch")(legacy.media_batch)
app.command("doctor")(legacy.media_doctor)
app.command("report")(legacy.media_report)
app.command("queue")(legacy.media_queue)
app.command("normalize")(legacy.media_normalize)
app.command("sidecars")(legacy.media_sidecars)
app.command("prune-dry-runs")(legacy.media_prune_dry_runs)
app.command("candidates")(legacy.media_public_candidates)
app.command("review-status")(legacy.media_review_status)
app.command("draft-rewrites")(legacy.media_public_draft_rewrites)
app.command("promote")(legacy.media_public_promote)
app.command("understand-benchmark")(legacy.media_understanding_benchmark)
app.command("understand-prepare")(legacy.media_understanding_prepare)
app.command("understand-run")(legacy.media_understanding_run_ollama)
