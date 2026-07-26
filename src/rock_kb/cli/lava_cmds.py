from __future__ import annotations

import json
from pathlib import Path

import typer

from ..jsonl import read_jsonl
from ..lava_contexts import (
    AGENT_CONTEXT_JSONL,
    build_lava_context_reference,
    discover_lava_context_candidates,
    get_lava_context_surface,
    get_lava_context_version_diff,
    list_lava_context_surfaces,
    refresh_lava_context_source_cache,
    validate_lava_context_extension,
    validate_private_lava_context_overlay,
)

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


@app.command("contexts-list")
def contexts_list(
    context_family: str | None = typer.Option(None, "--family"),
    surface_type: str | None = typer.Option(None, "--surface-type"),
    rock_version: str | None = typer.Option(None, "--rock-version"),
) -> None:
    """List generated Lava rendering surfaces."""
    rows = list(read_jsonl(AGENT_CONTEXT_JSONL))
    typer.echo(
        json.dumps(
            list_lava_context_surfaces(rows, context_family=context_family, surface_type=surface_type, rock_version=rock_version),
            indent=2,
            sort_keys=True,
        )
    )


@app.command("contexts-get")
def contexts_get(
    context_id: str = typer.Argument(...),
    root_key: str | None = typer.Option(None, "--root"),
    rock_version: str | None = typer.Option(None, "--rock-version"),
) -> None:
    """Get one exact Lava surface with direct and inherited roots."""
    rows = list(read_jsonl(AGENT_CONTEXT_JSONL))
    result = get_lava_context_surface(rows, context_id, root_key=root_key, rock_version=rock_version)
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "ok":
        raise typer.Exit(1)


@app.command("contexts-diff")
def contexts_diff(
    from_version: str = typer.Option(..., "--from"),
    to_version: str = typer.Option(..., "--to"),
    context_id: str | None = typer.Option(None, "--context"),
) -> None:
    """Compare exact Lava roots and contracts between observed Rock versions."""
    rows = list(read_jsonl(AGENT_CONTEXT_JSONL))
    typer.echo(json.dumps(get_lava_context_version_diff(rows, from_version, to_version, context_id=context_id), indent=2, sort_keys=True))


@app.command("contexts-discover")
def contexts_discover(
    source_tree: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    output: Path | None = typer.Option(None, "--output", file_okay=True, dir_okay=False),
    source_commit: str = typer.Option("", "--source-commit"),
    source_version: str = typer.Option("", "--source-version"),
) -> None:
    """Scan a public Rock source checkout into the private maintainer review queue."""
    kwargs = {
        "source_commit": source_commit,
        "source_version": source_version,
    }
    if output is not None:
        kwargs["output_path"] = output
    typer.echo(json.dumps(discover_lava_context_candidates(source_tree, **kwargs), indent=2, sort_keys=True))


@app.command("contexts-validate-extension")
def contexts_validate_extension(
    path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Validate one reviewed public Lava context extension manifest."""
    result = validate_lava_context_extension(path)
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "valid":
        raise typer.Exit(1)


@app.command("contexts-validate-overlay")
def contexts_validate_overlay(
    path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Validate a private, non-exportable Lava context overlay."""
    result = validate_private_lava_context_overlay(path)
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "valid":
        raise typer.Exit(1)
