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
from ..reviewed_cross_source import (
    REVIEWED_CROSS_SOURCE_RELATIVE_DIR,
    REVIEW_DECISIONS_NAME,
    promote_reviewed_cross_source,
)
from ..source_native import (
    SOURCE_NATIVE_PILOT_CONCEPTS,
    SOURCE_NATIVE_PILOT_DIR,
    SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT,
    SOURCE_NATIVE_REVIEW_DIR,
    SOURCE_NATIVE_SCHEMA_PATH,
    build_source_native_document_candidates,
    build_source_native_impact_report,
    merge_source_native_distillation_outputs,
    promote_source_native_distillation,
    write_source_native_distillation_schema,
    write_source_native_generation_prompt,
)
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


@app.command("reviewed-cross-source-promote")
def reviewed_cross_source_promote(
    input_path: Path = typer.Option(
        ...,
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Public-safe reviewed cross-source decision JSONL.",
    ),
    destination: Path = typer.Option(
        REPO_ROOT / REVIEWED_CROSS_SOURCE_RELATIVE_DIR,
        "--destination",
        file_okay=False,
        dir_okay=True,
        help="Tracked canonical reviewed cross-source bundle directory.",
    ),
) -> None:
    """Promote reviewed multi-source evidence into the canonical shadow."""

    if input_path.name != REVIEW_DECISIONS_NAME:
        typer.echo(
            "The promoted bundle will retain a normalized "
            f"{REVIEW_DECISIONS_NAME} copy.",
            err=True,
        )
    typer.echo(
        json.dumps(
            promote_reviewed_cross_source(
                input_path=input_path,
                destination=destination,
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


@app.command("source-native-candidates")
def source_native_candidates(
    concept: list[str] = typer.Option(
        list(SOURCE_NATIVE_PILOT_CONCEPTS),
        "--concept",
        "-c",
        help="Concept to include in the source-native documentation pilot.",
    ),
    limit_per_concept: int = typer.Option(
        SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT,
        "--limit-per-concept",
        min=1,
        max=20,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR,
        "--destination",
        help="Ignored directory for source text and model-review inputs.",
    ),
) -> None:
    """Build deterministic Rockumentation source units and private review inputs."""

    typer.echo(
        json.dumps(
            build_source_native_document_candidates(
                concept_ids=concept,
                limit_per_concept=limit_per_concept,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-schema")
def source_native_schema(
    destination: Path = typer.Option(
        SOURCE_NATIVE_SCHEMA_PATH,
        "--destination",
        help="Generated JSON Schema for v2.3 structured model output.",
    ),
) -> None:
    """Write the model-output schema from the validated Pydantic contract."""

    typer.echo(
        json.dumps(
            write_source_native_distillation_schema(destination),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-prompt")
def source_native_prompt(
    input_path: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "distillation-input.jsonl",
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "generation-prompt.txt",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
    concept: str | None = typer.Option(
        None,
        "--concept",
        help="Optionally render only candidates for one concept.",
    ),
    offset: int = typer.Option(0, "--offset", min=0),
    limit: int | None = typer.Option(
        None,
        "--limit",
        min=1,
        help="Optionally bound the number of candidates after filtering.",
    ),
) -> None:
    """Render a bounded no-tools v2.3 prompt from private candidate inputs."""

    typer.echo(
        json.dumps(
            write_source_native_generation_prompt(
                input_path=input_path,
                destination=destination,
                concept_id=concept,
                offset=offset,
                limit=limit,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-promote")
def source_native_promote(
    input_path: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "distillation-input.jsonl",
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_path: Path = typer.Option(
        ...,
        "--output",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Reviewed v2.3 model output JSON.",
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--destination",
        help="Tracked public-safe source-native pilot directory.",
    ),
    reviewer: str = typer.Option(..., "--reviewer"),
    model: str = typer.Option(..., "--model"),
    reviewed_at: str | None = typer.Option(
        None,
        "--reviewed-at",
        help="Optional fixed ISO-8601 review timestamp for reproducible rebuilds.",
    ),
    generation_prompt_version: str | None = typer.Option(
        None,
        "--generation-prompt-version",
        help=(
            "Exact prompt version used for the model generation when the "
            "review contract has since advanced."
        ),
    ),
    generated_at: str | None = typer.Option(
        None,
        "--generated-at",
        help=(
            "Original model-generation timestamp when maintainer review "
            "occurs later."
        ),
    ),
) -> None:
    """Validate reviewed typed artifacts and write the public-safe shadow bundle."""

    typer.echo(
        json.dumps(
            promote_source_native_distillation(
                input_path=input_path,
                output_path=output_path,
                destination=destination,
                reviewer=reviewer,
                model=model,
                reviewed_at=reviewed_at,
                generation_prompt_version=generation_prompt_version,
                generated_at=generated_at,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-merge")
def source_native_merge(
    batch: list[Path] = typer.Option(
        ...,
        "--batch",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Repeat for every schema-constrained model output batch.",
    ),
    input_path: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "distillation-input.jsonl",
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "reviewed-output.json",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Merge model batches in source order and enforce the semantic gate."""

    typer.echo(
        json.dumps(
            merge_source_native_distillation_outputs(
                input_path=input_path,
                batch_paths=batch,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-impact")
def source_native_impact(
    previous: Path = typer.Option(
        ...,
        "--previous",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    current: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--current",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    """Report source-unit changes and the bounded dependent revalidation queue."""

    typer.echo(
        json.dumps(
            build_source_native_impact_report(
                previous_dir=previous,
                current_dir=current,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
