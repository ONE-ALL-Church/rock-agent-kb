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
from ..canonical_retrieval_shadow import run_canonical_retrieval_shadow
from ..paths import REPO_ROOT
from ..reviewed_cross_source import (
    REVIEW_DECISIONS_NAME,
    REVIEWED_CROSS_SOURCE_RELATIVE_DIR,
    promote_reviewed_cross_source,
)
from ..source_family_contracts import (
    SOURCE_FAMILY_CONTRACT_MANIFEST_PATH,
    write_source_family_contract_manifest,
)
from ..source_native import (
    SOURCE_NATIVE_PILOT_CONCEPTS,
    SOURCE_NATIVE_PILOT_DIR,
    SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT,
    SOURCE_NATIVE_PROSE_SOURCE_IDS,
    SOURCE_NATIVE_REVIEW_DIR,
    SOURCE_NATIVE_ROCKUMENTATION_SOURCE_IDS,
    SOURCE_NATIVE_SCHEMA_PATH,
    build_source_native_document_candidates,
    build_source_native_impact_report,
    merge_source_native_distillation_outputs,
    promote_source_native_distillation,
    rebind_source_native_presentation_metadata,
    write_source_native_distillation_schema,
    write_source_native_generation_prompt,
    write_source_native_manifest,
)
from ..source_native_migration import (
    SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR,
    SOURCE_NATIVE_LEGACY_MIGRATION_SCHEMA_PATH,
    build_source_native_legacy_migration_inputs,
    merge_source_native_legacy_migration_outputs,
    promote_source_native_legacy_migration,
    rebind_source_native_legacy_migration_output,
    write_source_native_legacy_migration_prompt,
    write_source_native_legacy_migration_schema,
)
from ..source_native_priority import (
    SOURCE_NATIVE_MIGRATION_PRIORITY_PATH,
    build_source_native_migration_priority_report,
    parse_utc,
)
from ..source_native_readiness import (
    SOURCE_NATIVE_PROMOTION_POLICY_PATH,
    evaluate_source_native_promotion_readiness,
    fetch_operations_dashboard,
    load_json,
)
from ..source_native_verification import (
    VERIFICATION_REPORT_NAME,
    VERIFICATION_RESOLUTIONS_NAME,
    audit_source_native_verifications,
    build_source_native_verification_packet,
    promote_source_native_verification_resolutions,
)
from . import _legacy as legacy

app = typer.Typer(help="Developer utility commands.")

app.command("repo-pack")(legacy.repo_pack)


@app.command("source-family-contracts")
def source_family_contracts(
    destination: Path = typer.Option(
        SOURCE_FAMILY_CONTRACT_MANIFEST_PATH,
        "--destination",
        help="Tracked machine-readable canonical ingestion contracts.",
    ),
) -> None:
    """Write reviewed ingestion contracts for each canonical source family."""

    typer.echo(
        json.dumps(
            write_source_family_contract_manifest(destination),
            ensure_ascii=False,
            indent=2,
        )
    )


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
        help="Concept to include in the source-native documentation batch.",
    ),
    limit_per_concept: int = typer.Option(
        SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT,
        "--limit-per-concept",
        min=1,
        max=20,
    ),
    source_id: list[str] = typer.Option(
        list(SOURCE_NATIVE_ROCKUMENTATION_SOURCE_IDS),
        "--source-id",
        help=(
            "Official prose source family to include. Repeat to build a "
            "balanced family-specific batch. Supported values: "
            + ", ".join(SOURCE_NATIVE_PROSE_SOURCE_IDS)
        ),
    ),
    source_record_id: list[str] = typer.Option(
        [],
        "--source-record-id",
        help=(
            "Optionally select exact normalized source records. Repeat for a "
            "bounded, reviewable source-native batch."
        ),
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
                source_ids=source_id,
                source_record_ids=source_record_id,
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
    candidate_id: str | None = typer.Option(
        None,
        "--candidate-id",
        help="Render the one exact content-derived candidate ID.",
    ),
    source_record_id: str | None = typer.Option(
        None,
        "--source-record-id",
        help="Render the one exact stable source record, including after a split.",
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
                candidate_id=candidate_id,
                source_record_id=source_record_id,
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
        help="Tracked public-safe source-native bundle directory.",
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
    base_dir: Path | None = typer.Option(
        None,
        "--base",
        exists=True,
        file_okay=False,
        dir_okay=True,
        help=(
            "Append to this reviewed source-native bundle, replacing only "
            "records for refreshed source works."
        ),
    ),
    generated_output_path: Path | None = typer.Option(
        None,
        "--generated-output",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help=(
            "Unedited merged model output used to record bounded reviewer "
            "correction metrics without publishing the raw review file."
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
                base_dir=base_dir,
                generated_output_path=generated_output_path,
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
    allow_review_blockers: bool = typer.Option(
        False,
        "--allow-review-blockers",
        help=(
            "Write a private review packet containing exact split_required "
            "feedback; final promotion remains strict."
        ),
    ),
) -> None:
    """Merge model batches in source order and enforce the semantic gate."""

    typer.echo(
        json.dumps(
            merge_source_native_distillation_outputs(
                input_path=input_path,
                batch_paths=batch,
                destination=destination,
                allow_review_blockers=allow_review_blockers,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-input")
def source_native_migration_input(
    source_native_input: Path = typer.Option(
        ...,
        "--source-native-input",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Private v2.3 source-native distillation input JSONL.",
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR / "migration-input.jsonl",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Bind selected source-native candidates to active legacy projections."""

    typer.echo(
        json.dumps(
            build_source_native_legacy_migration_inputs(
                source_native_input_path=source_native_input,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-schema")
def source_native_migration_schema(
    destination: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_SCHEMA_PATH,
        "--destination",
    ),
) -> None:
    """Write the strict legacy-migration model response schema."""

    typer.echo(
        json.dumps(
            write_source_native_legacy_migration_schema(destination),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-prompt")
def source_native_migration_prompt(
    input_path: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR / "migration-input.jsonl",
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR / "generation-prompt.txt",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
    source_record_id: str | None = typer.Option(
        None,
        "--source-record-id",
        help="Optionally render one exact source record.",
    ),
) -> None:
    """Render the no-tools, exact-coverage migration prompt."""

    typer.echo(
        json.dumps(
            write_source_native_legacy_migration_prompt(
                input_path=input_path,
                destination=destination,
                source_record_id=source_record_id,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-merge")
def source_native_migration_merge(
    batch: list[Path] = typer.Option(
        ...,
        "--batch",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    input_path: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR / "migration-input.jsonl",
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR / "reviewed-output.json",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Merge schema-constrained migration batches and enforce full coverage."""

    typer.echo(
        json.dumps(
            merge_source_native_legacy_migration_outputs(
                input_path=input_path,
                batch_paths=batch,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-promote")
def source_native_migration_promote(
    input_path: Path = typer.Option(
        ...,
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
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--destination",
        file_okay=False,
        dir_okay=True,
    ),
    base_dir: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--base",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    reviewer: str = typer.Option(..., "--reviewer"),
    model: str = typer.Option(..., "--model"),
    reviewed_at: str | None = typer.Option(None, "--reviewed-at"),
    generated_output_path: Path | None = typer.Option(
        None,
        "--generated-output",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Promote reviewed typed replacements and hash-bound retirement decisions."""

    typer.echo(
        json.dumps(
            promote_source_native_legacy_migration(
                input_path=input_path,
                output_path=output_path,
                destination=destination,
                base_dir=base_dir,
                reviewer=reviewer,
                model=model,
                reviewed_at=reviewed_at,
                generated_output_path=generated_output_path,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-rebind")
def source_native_migration_rebind(
    previous_input: Path = typer.Option(
        ...,
        "--previous-input",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    refreshed_input: Path = typer.Option(
        ...,
        "--refreshed-input",
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
        help="Previously reviewed migration output.",
    ),
    destination: Path = typer.Option(
        ...,
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Rebind reviewed decisions after a metadata-only legacy hash refresh."""

    typer.echo(
        json.dumps(
            rebind_source_native_legacy_migration_output(
                previous_input_path=previous_input,
                refreshed_input_path=refreshed_input,
                output_path=output_path,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-presentation-rebind")
def source_native_presentation_rebind(
    input_path: Path = typer.Option(
        ...,
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Fresh hash-verified source-native distillation input JSONL.",
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--destination",
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    """Rebind reviewed title metadata when source semantics are unchanged."""

    typer.echo(
        json.dumps(
            rebind_source_native_presentation_metadata(
                input_path=input_path,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-migration-priority")
def source_native_migration_priority(
    destination: Path = typer.Option(
        SOURCE_NATIVE_MIGRATION_PRIORITY_PATH,
        "--destination",
        file_okay=True,
        dir_okay=False,
        help="Ignored deterministic migration queue report.",
    ),
    as_of: str | None = typer.Option(
        None,
        "--as-of",
        help="UTC ISO-8601 ranking time; defaults to now.",
    ),
    limit: int = typer.Option(200, "--limit", min=1, max=2000),
    dashboard_path: Path | None = typer.Option(
        None,
        "--dashboard",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Captured operations dashboard; overrides hosted readback.",
    ),
    dashboard_url: str = typer.Option(
        "https://rock-agent-kb.oneandall.church/operations/dashboard",
        "--dashboard-url",
        help="Hosted operations dashboard used for privacy-bounded demand signals.",
    ),
    hosted_dashboard: bool = typer.Option(
        True,
        "--hosted-dashboard/--no-hosted-dashboard",
        help="Read bounded demand signals from the hosted dashboard when no capture is supplied.",
    ),
) -> None:
    """Rank active, unreviewed legacy prose records for bounded migration."""

    as_of_value = parse_utc(as_of)
    if as_of and as_of_value is None:
        raise typer.BadParameter("--as-of must be a valid ISO-8601 timestamp")
    dashboard = (
        load_json(dashboard_path)
        if dashboard_path is not None
        else fetch_operations_dashboard(dashboard_url)
        if hosted_dashboard
        else None
    )
    typer.echo(
        json.dumps(
            build_source_native_migration_priority_report(
                destination=destination,
                as_of=as_of_value,
                limit=limit,
                dashboard=dashboard,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-verification-packet")
def source_native_verification_packet(
    queue_path: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR / "verification-queue.jsonl",
        "--queue",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_REVIEW_DIR / "verification-packet.jsonl",
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Write hash-bound private review inputs for unresolved verification rows."""

    typer.echo(
        json.dumps(
            build_source_native_verification_packet(
                queue_path=queue_path,
                destination=destination,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("source-native-verification-promote")
def source_native_verification_promote(
    input_path: Path = typer.Option(
        ...,
        "--input",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Reviewed public-safe verification resolutions JSONL.",
    ),
    queue_path: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR / "verification-queue.jsonl",
        "--queue",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR,
        "--destination",
        file_okay=False,
        dir_okay=True,
    ),
    reviewer: str = typer.Option(..., "--reviewer"),
    reviewed_at: str | None = typer.Option(None, "--reviewed-at"),
) -> None:
    """Promote reviewed evidence without rewriting source-native artifacts."""

    result = promote_source_native_verification_resolutions(
        queue_path=queue_path,
        input_path=input_path,
        destination=destination,
        reviewer=reviewer,
        reviewed_at=reviewed_at,
        source_snapshots_path=destination / "source-snapshots.jsonl",
    )
    result["manifest"] = write_source_native_manifest(destination).public_dump()
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("source-native-verification-audit")
def source_native_verification_audit(
    queue_path: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR / "verification-queue.jsonl",
        "--queue",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    resolution_path: Path = typer.Option(
        SOURCE_NATIVE_PILOT_DIR / VERIFICATION_RESOLUTIONS_NAME,
        "--resolutions",
        file_okay=True,
        dir_okay=False,
    ),
    check_live: bool = typer.Option(
        False,
        "--check-live",
        help="Re-fetch mutable public evidence and compare content hashes.",
    ),
    destination: Path | None = typer.Option(
        None,
        "--destination",
        file_okay=True,
        dir_okay=False,
        help="Optional captured report for the readiness gate.",
    ),
) -> None:
    """Report unresolved, stale, and default-cutover-blocking verification rows."""

    tracked_report = SOURCE_NATIVE_PILOT_DIR / VERIFICATION_REPORT_NAME
    if (
        check_live
        and destination is not None
        and destination.resolve() == tracked_report.resolve()
    ):
        raise typer.BadParameter(
            "live verification reports are ephemeral readiness evidence; "
            "write them under ignored data/review instead of the manifest-bound "
            "canonical bundle"
        )
    report = audit_source_native_verifications(
        queue_path=queue_path,
        resolution_path=resolution_path,
        source_snapshots_path=(
            SOURCE_NATIVE_PILOT_DIR / "source-snapshots.jsonl"
        ),
        check_live=check_live,
    )
    if destination is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
    typer.echo(json.dumps(report, ensure_ascii=False, indent=2))


@app.command("source-native-readiness")
def source_native_readiness(
    retrieval_report_path: Path = typer.Option(
        ...,
        "--retrieval-report",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    dashboard_path: Path | None = typer.Option(
        None,
        "--dashboard",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Optional captured operations dashboard; hosted readback is the default.",
    ),
    dashboard_url: str = typer.Option(
        "https://rock-agent-kb.oneandall.church/operations/dashboard",
        "--dashboard-url",
    ),
    verification_report_path: Path | None = typer.Option(
        None,
        "--verification-report",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help=(
            "Optional captured live verification report. Without it, the "
            "command re-fetches mutable public evidence."
        ),
    ),
    policy_path: Path = typer.Option(
        SOURCE_NATIVE_PROMOTION_POLICY_PATH,
        "--policy",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    destination: Path | None = typer.Option(
        None,
        "--destination",
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Evaluate technical and independent external evidence separately."""

    dashboard = (
        load_json(dashboard_path)
        if dashboard_path is not None
        else fetch_operations_dashboard(dashboard_url)
    )
    verification_report = (
        load_json(verification_report_path)
        if verification_report_path is not None
        else audit_source_native_verifications(
            queue_path=(
                SOURCE_NATIVE_PILOT_DIR / "verification-queue.jsonl"
            ),
            resolution_path=(
                SOURCE_NATIVE_PILOT_DIR / VERIFICATION_RESOLUTIONS_NAME
            ),
            source_snapshots_path=(
                SOURCE_NATIVE_PILOT_DIR / "source-snapshots.jsonl"
            ),
            check_live=True,
        )
    )
    report = evaluate_source_native_promotion_readiness(
        manifest=load_json(SOURCE_NATIVE_PILOT_DIR / "manifest.json"),
        verification_report=verification_report,
        retrieval_report=load_json(retrieval_report_path),
        dashboard=dashboard,
        policy=load_json(policy_path),
    )
    if destination is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
    typer.echo(json.dumps(report, ensure_ascii=False, indent=2))


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
