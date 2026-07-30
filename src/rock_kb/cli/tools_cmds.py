from __future__ import annotations

import json
from pathlib import Path

import typer

from ..canonical_knowledge import (
    CANONICAL_IDENTITY_BASELINE_RELATIVE_DIR,
    SHADOW_DIR,
    write_canonical_identity_baseline,
    write_canonical_knowledge_shadow,
)
from ..paths import REPO_ROOT
from ..canonical_retrieval_shadow import run_canonical_retrieval_shadow
from . import _legacy as legacy

app = typer.Typer(help="Developer utility commands.")

app.command("repo-pack")(legacy.repo_pack)


@app.command("canonical-shadow")
def canonical_shadow(
    destination: Path = typer.Option(
        SHADOW_DIR,
        "--destination",
        help="Ignored review directory for the canonical knowledge shadow projection.",
    ),
) -> None:
    """Build the canonical architecture projection without changing public retrieval."""

    typer.echo(json.dumps(write_canonical_knowledge_shadow(destination), ensure_ascii=False, indent=2))


@app.command("canonical-retrieval-shadow")
def canonical_retrieval_shadow(
    destination: Path = typer.Option(
        SHADOW_DIR,
        "--destination",
        help="Ignored review directory for canonical projection and retrieval comparison artifacts.",
    ),
    limit: int = typer.Option(
        5,
        "--limit",
        min=1,
        max=20,
        help="Results to score per evaluation query.",
    ),
    skip_worker_build: bool = typer.Option(
        False,
        "--skip-worker-build",
        help="Reuse an existing dry-run Worker bundle.",
    ),
) -> None:
    """Run current and canonical rows through the production ranking Worker."""

    typer.echo(
        json.dumps(
            run_canonical_retrieval_shadow(
                destination,
                limit=limit,
                build_worker=not skip_worker_build,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("canonical-identity-baseline")
def canonical_identity_baseline(
    destination: Path = typer.Option(
        REPO_ROOT / CANONICAL_IDENTITY_BASELINE_RELATIVE_DIR,
        "--destination",
        help="Tracked directory for the versioned public-safe identity baseline.",
    ),
    shadow_destination: Path = typer.Option(
        SHADOW_DIR,
        "--shadow-destination",
        help="Ignored review directory retaining unpublished pilot migrations.",
    ),
) -> None:
    """Write stable identities and existing-public-ID aliases without a retrieval cutover."""

    typer.echo(
        json.dumps(
            write_canonical_identity_baseline(
                destination,
                shadow_destination=shadow_destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
