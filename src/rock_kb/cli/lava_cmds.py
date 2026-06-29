from __future__ import annotations

import json
from pathlib import Path

import typer

from ..lava_contexts import build_lava_context_reference, refresh_lava_context_source_cache

app = typer.Typer(help="Lava capability and context directory utilities.")


@app.command("contexts-build")
def contexts_build(
    source_dir: Path | None = typer.Option(None, "--source-dir", file_okay=False, dir_okay=True),
    skip_fetch: bool = typer.Option(False, "--skip-fetch", help="Do not fetch missing public source files."),
) -> None:
    """Build generated Lava data-context directory artifacts."""
    typer.echo(json.dumps(build_lava_context_reference(fetch_missing=not skip_fetch, source_dir=source_dir), indent=2, sort_keys=True))


@app.command("contexts-refresh-source")
def contexts_refresh_source(
    source_dir: Path | None = typer.Option(None, "--source-dir", file_okay=False, dir_okay=True),
) -> None:
    """Refresh ignored public Rock source cache used by the Lava context builder."""
    typer.echo(json.dumps(refresh_lava_context_source_cache(source_dir=source_dir), indent=2, sort_keys=True))
