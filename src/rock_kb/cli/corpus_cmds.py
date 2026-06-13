from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Private corpus portability commands.")

app.command("init")(legacy.private_corpus_init)
app.command("validate")(legacy.private_corpus_validate)
app.command("report")(legacy.private_corpus_report)
app.command("sync")(legacy.private_corpus_sync)
app.command("autosync")(legacy.private_corpus_autosync)
app.command("restore")(legacy.private_corpus_restore)
app.command("media-manifest")(legacy.private_corpus_media_manifest)
app.command("audit")(legacy.private_corpus_audit)
app.command("verify-rebuild")(legacy.private_corpus_verify_rebuild)
