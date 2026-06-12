from __future__ import annotations

import typer

from . import _legacy as legacy


def register(app: typer.Typer) -> None:
    app.command("status")(legacy.status_command)
    app.command("build")(legacy.build_command)
    app.command("serve")(serve_command)


def serve_command() -> None:
    """Run the read-only Rock KB MCP stdio server."""
    from ..serve.server import ServeDependencyError, run_stdio

    try:
        run_stdio()
    except ServeDependencyError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
