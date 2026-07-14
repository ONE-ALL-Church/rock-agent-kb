from __future__ import annotations

import json
from pathlib import Path

import typer

from . import _legacy as legacy
from ..okf_export import audit_okf_export, build_okf_export

app = typer.Typer(help="Public export and publish commands.")

app.command("export")(legacy.public_export)


@app.command("okf")
def okf_export(
    destination: Path | None = typer.Option(None, "--destination", "-d", file_okay=False, dir_okay=True),
    archive_dir: Path | None = typer.Option(None, "--archive-dir", file_okay=False, dir_okay=True),
    distribution_version: str | None = typer.Option(None, "--version"),
    source_commit: str | None = typer.Option(None, "--source-commit"),
    profile: str = typer.Option("full", "--profile", help="Distribution profile: full or core."),
    previous_bundle: Path | None = typer.Option(None, "--previous-bundle", exists=True),
) -> None:
    """Build a read-only Open Knowledge Format distribution."""
    result = build_okf_export(
        destination,
        distribution_version=distribution_version,
        source_commit=source_commit,
        archive_dir=archive_dir,
        profile=profile,
        previous_bundle=previous_bundle,
    )
    legacy.console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


@app.command("okf-validate")
def okf_validate(bundle: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True)) -> None:
    """Validate a generated OKF directory for conformance, integrity, and public safety."""
    errors = audit_okf_export(bundle.resolve())
    result = {
        "schema": "rock-kb-okf-validation-v1",
        "status": "ok" if not errors else "failed",
        "bundle": str(bundle.resolve()),
        "errors": errors,
    }
    legacy.console.print_json(json.dumps(result))
    if errors:
        raise typer.Exit(code=1)
