from __future__ import annotations

import json
import shutil
import tempfile
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .extract import now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT, REVIEW_DIR
from .schemas import (
    KnowledgeIdentity,
    ReviewedSourceNativeArtifact,
    ReviewedSourceNativeArtifactMigration,
    ReviewedSourceNativeLegacyMigration,
    SourceNativeArtifactCandidate,
    SourceNativeDistillationOutput,
    SourceNativeLegacyMigrationOutput,
    SourceSnapshot,
    SourceUnit,
)
from .schemas.source_native import SourceNativeDistillationArticle

SOURCE_NATIVE_LEGACY_MIGRATIONS_NAME = "legacy-migrations.jsonl"
SOURCE_NATIVE_ARTIFACT_MIGRATIONS_NAME = "artifact-migrations.jsonl"
SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID = "source-native-legacy-migration-v1"
SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION = "1.3.1"
SOURCE_NATIVE_LEGACY_MIGRATION_INPUT_HASH_VERSION = "2"
SOURCE_NATIVE_LEGACY_MIGRATION_REVIEW_DIR = (
    REVIEW_DIR / "source-native-legacy-migration"
)
SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH = (
    REPO_ROOT / "docs" / "prompts" / "source-native-legacy-migration-v1.md"
)
SOURCE_NATIVE_LEGACY_MIGRATION_SCHEMA_PATH = (
    REPO_ROOT / "docs" / "specs" / "source-native-legacy-migration-v1.schema.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def public_record_hash(value: Any) -> str:
    payload = value.public_dump() if hasattr(value, "public_dump") else value
    return sha256_text(canonical_json(payload))


def source_native_legacy_migration_input_hash(
    input_row: dict[str, Any],
    *,
    version: str | None = None,
) -> str:
    """Hash the exact source, legacy, and prior-artifact migration input."""

    resolved_version = str(
        version or input_row.get("migration_input_hash_version") or "1"
    )
    if resolved_version not in {"1", "2"}:
        raise ValueError(
            f"unsupported migration input hash version: {resolved_version}"
        )
    source_snapshot = SourceSnapshot.model_validate(input_row["source_snapshot"])
    source_input_hash = str(input_row.get("source_input_hash") or "")
    if resolved_version == "2":
        from .source_native import source_native_model_input_hash

        computed_source_input_hash = source_native_model_input_hash(
            snapshot=source_snapshot,
            source_units=[
                SourceUnit.model_validate(row)
                for row in input_row.get("source_units") or []
            ],
            concept_ids=input_row.get("concept_ids") or [],
            existing_claims=input_row.get("existing_claims") or [],
            documentation_path=input_row.get("documentation_path"),
            documentation_branches=(input_row.get("documentation_branches") or []),
            documentation_current_version=input_row.get(
                "documentation_current_version"
            ),
        )
        if source_input_hash != computed_source_input_hash:
            raise ValueError("source-native migration source input hash changed")
    payload = {
        "source_input_hash": source_input_hash,
        "source_snapshot_id": source_snapshot.source_snapshot_id,
        "source_snapshot_content_hash": source_snapshot.content_hash,
        "legacy_items": input_row.get("legacy_items") or [],
        "existing_source_native_artifacts": (
            input_row.get("existing_source_native_artifacts") or []
        ),
    }
    if resolved_version == "2":
        payload = {
            "migration_input_hash_version": resolved_version,
            "candidate_id": str(input_row.get("candidate_id") or ""),
            **payload,
        }
    return sha256_text(canonical_json(payload))


def write_source_native_legacy_migration_schema(
    destination: Path = SOURCE_NATIVE_LEGACY_MIGRATION_SCHEMA_PATH,
) -> dict[str, Any]:
    from .source_native import make_strict_response_schema, sha256_file

    schema = SourceNativeLegacyMigrationOutput.model_json_schema(by_alias=True)
    make_strict_response_schema(schema)
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-legacy-migration-schema-build-v1",
        "status": "ok",
        "destination": str(destination),
        "sha256": sha256_file(destination),
    }


def build_source_native_legacy_migration_inputs(
    *,
    source_native_input_path: Path,
    destination: Path,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Join private source inputs to active legacy rows and reviewed replacements."""

    from .canonical_knowledge import build_canonical_knowledge_bundle
    from .source_native import load_source_native_pilot

    candidates = list(read_jsonl(source_native_input_path))
    if not candidates:
        raise ValueError("source-native migration input requires source candidates")

    # Reconstruct the pre-retirement surface. The persisted identity baseline may
    # already transfer legacy aliases to source-native survivors, so it cannot be
    # used to refresh the hash-bound migration that authorized that transfer.
    bundle, _summary = build_canonical_knowledge_bundle(
        identity_registry=[],
        include_source_native_pilot=False,
        include_legacy_migrations=False,
        include_reviewed_cross_source=True,
        repo_root=repo_root,
    )
    snapshots_by_id = {row.source_snapshot_id: row for row in bundle.source_snapshots}
    units_by_id = {row.source_unit_id: row for row in bundle.source_units}

    active_legacy_by_record: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in bundle.knowledge_units:
        if item.ingestion_mode not in {
            "legacy_reviewed_claim_projection",
            "legacy_summary_projection",
        }:
            continue
        if item.knowledge_type not in {"claim", "source_summary"}:
            continue
        source_record_ids = sorted(
            {
                str(snapshot.source_record_id)
                for source_unit_id in item.source_unit_ids
                if (source_unit := units_by_id.get(source_unit_id))
                and (snapshot := snapshots_by_id.get(source_unit.source_snapshot_id))
                and snapshot.source_record_id
            }
        )
        public_item = {
            "legacy_knowledge_unit_id": item.knowledge_unit_id,
            "legacy_result_ids": sorted({item.knowledge_unit_id, *item.legacy_ids}),
            "legacy_knowledge_type": item.knowledge_type,
            "legacy_ingestion_mode": item.ingestion_mode,
            "legacy_content_hash": item.content_hash,
            "title": item.title,
            "retrieval_text": item.retrieval_text,
            "concept_facets": item.concept_facets,
            "source_record_ids": source_record_ids,
        }
        for source_record_id in source_record_ids:
            active_legacy_by_record[source_record_id].append(public_item)

    source_native = load_source_native_pilot(repo_root)
    native_snapshots = {
        row.source_snapshot_id: row for row in source_native["source_snapshots"]
    }
    native_units = {row.source_unit_id: row for row in source_native["source_units"]}
    native_artifacts_by_record: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for reviewed in source_native["reviewed_artifacts"]:
        source_record_ids = {
            str(snapshot.source_record_id)
            for source_unit_id in reviewed.artifact.source_unit_ids
            if (unit := native_units.get(source_unit_id))
            and (snapshot := native_snapshots.get(unit.source_snapshot_id))
            and snapshot.source_record_id
        }
        artifact_row = reviewed.public_dump()
        public_item = {
            "artifact_id": reviewed.artifact_id,
            "artifact_hash": public_record_hash(reviewed.artifact),
            "artifact": artifact_row["artifact"],
        }
        for source_record_id in source_record_ids:
            native_artifacts_by_record[source_record_id].append(public_item)

    output_rows: list[dict[str, Any]] = []
    missing_legacy: list[str] = []
    for candidate in candidates:
        source_snapshot = SourceSnapshot.model_validate(candidate["source_snapshot"])
        source_record_id = str(source_snapshot.source_record_id or "")
        legacy_items = sorted(
            active_legacy_by_record.get(source_record_id) or [],
            key=lambda row: str(row["legacy_knowledge_unit_id"]),
        )
        if not legacy_items:
            missing_legacy.append(source_record_id)
            continue
        existing_artifacts = sorted(
            native_artifacts_by_record.get(source_record_id) or [],
            key=lambda row: str(row["artifact_id"]),
        )
        migration_row = {
            **candidate,
            "migration_input_hash_version": (
                SOURCE_NATIVE_LEGACY_MIGRATION_INPUT_HASH_VERSION
            ),
            "legacy_items": legacy_items,
            "existing_source_native_artifacts": existing_artifacts,
        }
        migration_row["migration_input_hash"] = (
            source_native_legacy_migration_input_hash(migration_row)
        )
        output_rows.append(migration_row)
    if missing_legacy:
        raise ValueError(
            "selected migration sources contain no active legacy rows: "
            + ", ".join(sorted(missing_legacy))
        )
    write_jsonl(destination, output_rows)
    return {
        "schema": "rock-kb-source-native-legacy-migration-input-build-v1",
        "status": "ok",
        "article_count": len(output_rows),
        "legacy_item_count": sum(len(row["legacy_items"]) for row in output_rows),
        "existing_artifact_count": sum(
            len(row["existing_source_native_artifacts"]) for row in output_rows
        ),
        "destination": str(destination),
    }


def write_source_native_legacy_migration_prompt(
    *,
    input_path: Path,
    destination: Path,
    source_record_id: str | None = None,
) -> dict[str, Any]:
    from .source_native import SOURCE_NATIVE_PROMPT_PATH, sha256_file

    inputs = list(read_jsonl(input_path))
    if source_record_id:
        inputs = [
            row
            for row in inputs
            if str((row.get("source_snapshot") or {}).get("source_record_id") or "")
            == source_record_id
        ]
    if not inputs:
        raise ValueError("No legacy migration candidates matched the prompt filter")
    source_native_contract = SOURCE_NATIVE_PROMPT_PATH.read_text(
        encoding="utf-8"
    ).rstrip()
    source_native_contract = source_native_contract.split(
        "\n## Output\n",
        1,
    )[0]
    migration_contract = SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH.read_text(
        encoding="utf-8"
    ).rstrip()
    prompt = source_native_contract + "\n\n---\n\n" + migration_contract
    prompt += (
        "\n\n## Batch Requirement\n\n"
        f"Return exactly {len(inputs)} articles in the supplied order. "
        "Copy each migration hash version and hash exactly, review every "
        "source unit, and decide every legacy item and existing artifact.\n\n"
        "INPUT CANDIDATES\n"
        + json.dumps(inputs, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(prompt, encoding="utf-8")
    return {
        "schema": "rock-kb-source-native-legacy-migration-prompt-build-v1",
        "status": "ok",
        "source_record_id": source_record_id,
        "candidate_count": len(inputs),
        "destination": str(destination),
        "sha256": sha256_file(destination),
    }


def migration_output_as_source_native(
    output: SourceNativeLegacyMigrationOutput,
) -> SourceNativeDistillationOutput:
    return SourceNativeDistillationOutput(
        schema="rock-kb-source-knowledge-distillation-v2.3",
        variant_id="source_knowledge_distillation_v2_3",
        articles=[
            SourceNativeDistillationArticle.model_validate(
                article.model_dump(
                        by_alias=True,
                        exclude={
                            "migration_input_hash",
                            "migration_input_hash_version",
                            "legacy_decisions",
                            "existing_artifact_decisions",
                        },
                )
            )
            for article in output.articles
        ],
    )


def validate_source_native_legacy_migration_output(
    raw_output: dict[str, Any] | SourceNativeLegacyMigrationOutput,
    *,
    inputs: Iterable[dict[str, Any]],
) -> SourceNativeLegacyMigrationOutput:
    from .source_native import (
        source_native_artifact_id,
        validate_source_native_distillation,
    )

    input_rows = list(inputs)
    output = (
        raw_output
        if isinstance(raw_output, SourceNativeLegacyMigrationOutput)
        else SourceNativeLegacyMigrationOutput.model_validate(raw_output)
    )
    inputs_by_id = {str(row["candidate_id"]): row for row in input_rows}
    article_ids = [row.candidate_id for row in output.articles]
    if len(article_ids) != len(set(article_ids)):
        raise ValueError("migration output candidate IDs must be unique")
    if article_ids != list(inputs_by_id):
        raise ValueError(
            "migration output must cover candidates exactly and in input order"
        )
    validate_source_native_distillation(
        migration_output_as_source_native(output),
        inputs=input_rows,
        require_promotable=True,
    )
    for article in output.articles:
        input_row = inputs_by_id[article.candidate_id]
        input_hash_version = str(input_row.get("migration_input_hash_version") or "1")
        expected_migration_input_hash = source_native_legacy_migration_input_hash(
            input_row,
            version=input_hash_version,
        )
        if input_row.get("migration_input_hash") != expected_migration_input_hash:
            raise ValueError(
                f"migration input contents changed for {article.candidate_id}"
            )
        if article.migration_input_hash_version != input_hash_version:
            raise ValueError(
                f"migration input hash version changed for {article.candidate_id}"
            )
        if article.migration_input_hash != input_row.get("migration_input_hash"):
            raise ValueError(f"migration input hash changed for {article.candidate_id}")
        legacy_by_id = {
            str(row["legacy_knowledge_unit_id"]): row
            for row in input_row.get("legacy_items") or []
        }
        decisions_by_id = {
            row.legacy_knowledge_unit_id: row for row in article.legacy_decisions
        }
        if set(decisions_by_id) != set(legacy_by_id):
            raise ValueError(
                f"legacy decisions must cover the exact input for {article.candidate_id}"
            )
        existing_artifacts_by_id = {
            str(row["artifact_id"]): row
            for row in input_row.get("existing_source_native_artifacts") or []
        }
        existing_decisions_by_id = {
            row.existing_artifact_id: row for row in article.existing_artifact_decisions
        }
        if set(existing_decisions_by_id) != set(existing_artifacts_by_id):
            raise ValueError(
                "existing artifact decisions must cover the exact input for "
                f"{article.candidate_id}"
            )
        artifacts_by_key = {row.artifact_key: row for row in article.artifacts}
        artifact_keys = set(artifacts_by_key)
        snapshot = SourceSnapshot.model_validate(input_row["source_snapshot"])
        for existing_id, decision in existing_decisions_by_id.items():
            existing = existing_artifacts_by_id[existing_id]
            if decision.existing_artifact_hash != existing.get("artifact_hash"):
                raise ValueError(
                    f"existing source-native artifact hash changed for {existing_id}"
                )
            replacement = artifacts_by_key.get(decision.replacement_artifact_key)
            if replacement is None:
                raise ValueError(
                    f"existing artifact replacement is missing for {existing_id}"
                )
            replacement_id = source_native_artifact_id(snapshot, replacement)
            if decision.disposition == "retain_identity":
                if replacement_id != existing_id:
                    raise ValueError(
                        "retain_identity decisions must preserve the exact artifact ID: "
                        f"{existing_id}"
                    )
            elif replacement_id == existing_id:
                raise ValueError(
                    "supersede decisions must select a different artifact identity: "
                    f"{existing_id}"
                )
        for legacy_id, decision in decisions_by_id.items():
            if decision.legacy_content_hash != legacy_by_id[legacy_id].get(
                "legacy_content_hash"
            ):
                raise ValueError(f"legacy content hash changed for {legacy_id}")
            if (
                decision.disposition == "replace"
                and decision.replacement_artifact_key not in artifact_keys
            ):
                raise ValueError(f"replacement artifact key is missing for {legacy_id}")
            missing_supporting = sorted(
                set(decision.supporting_replacement_artifact_keys) - artifact_keys
            )
            if missing_supporting:
                raise ValueError(
                    f"supporting replacement artifacts are missing for {legacy_id}"
                )
            legacy_type = str(
                legacy_by_id[legacy_id].get("legacy_knowledge_type") or ""
            )
            if (
                decision.disposition == "replace"
                and legacy_type == "source_summary"
                and artifacts_by_key[
                    str(decision.replacement_artifact_key)
                ].artifact_type
                != "source_summary"
            ):
                raise ValueError(
                    "legacy source summaries require a source-summary primary "
                    f"replacement: {legacy_id}"
                )
            if legacy_type == "claim" and decision.supporting_replacement_artifact_keys:
                raise ValueError(
                    f"legacy claims cannot use supporting replacements: {legacy_id}"
                )
    return output


def merge_source_native_legacy_migration_outputs(
    *,
    input_path: Path,
    batch_paths: Iterable[Path],
    destination: Path,
) -> dict[str, Any]:
    inputs = list(read_jsonl(input_path))
    expected_ids = [str(row["candidate_id"]) for row in inputs]
    articles_by_id: dict[str, dict[str, Any]] = {}
    paths = list(batch_paths)
    for path in paths:
        batch = SourceNativeLegacyMigrationOutput.model_validate(
            json.loads(path.read_text(encoding="utf-8"))
        )
        for article in batch.articles:
            if article.candidate_id in articles_by_id:
                raise ValueError(
                    f"duplicate generated candidate_id: {article.candidate_id}"
                )
            articles_by_id[article.candidate_id] = article.public_dump()
    if set(articles_by_id) != set(expected_ids):
        raise ValueError("migration batches must cover the exact migration input")
    merged = {
        "schema": "rock-kb-source-native-legacy-migration-output-v1",
        "variant_id": "source_native_legacy_migration_v1",
        "articles": [articles_by_id[value] for value in expected_ids],
    }
    validated = validate_source_native_legacy_migration_output(
        merged,
        inputs=inputs,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(
            validated.public_dump(), ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-legacy-migration-output-merge-v1",
        "status": "ok",
        "batch_count": len(paths),
        "article_count": len(validated.articles),
        "replacement_count": sum(
            row.disposition == "replace"
            for article in validated.articles
            for row in article.legacy_decisions
        ),
        "retained_count": sum(
            row.disposition == "retain"
            for article in validated.articles
            for row in article.legacy_decisions
        ),
        "destination": str(destination),
    }


def rebind_source_native_legacy_migration_output(
    *,
    previous_input_path: Path,
    refreshed_input_path: Path,
    output_path: Path,
    destination: Path,
) -> dict[str, Any]:
    """Rebind a reviewed decision when only legacy content hashes changed."""

    from .source_native import source_native_artifact_id

    previous_inputs = list(read_jsonl(previous_input_path))
    refreshed_inputs = list(read_jsonl(refreshed_input_path))
    reviewed_output = validate_source_native_legacy_migration_output(
        json.loads(output_path.read_text(encoding="utf-8")),
        inputs=previous_inputs,
    )
    previous_by_id = {str(row["candidate_id"]): row for row in previous_inputs}
    refreshed_by_id = {str(row["candidate_id"]): row for row in refreshed_inputs}
    if list(previous_by_id) != list(refreshed_by_id):
        raise ValueError(
            "refreshed migration input must preserve candidate IDs and order"
        )

    rebound = reviewed_output.public_dump()
    changed_legacy_hash_count = 0
    materialized_artifact_count = 0
    for article in rebound["articles"]:
        candidate_id = str(article["candidate_id"])
        previous = previous_by_id[candidate_id]
        refreshed = refreshed_by_id[candidate_id]
        if _migration_rebind_stable_payload(previous) != (
            _migration_rebind_stable_payload(refreshed)
        ):
            raise ValueError(
                "refreshed migration input changed more than hash bindings for "
                f"{candidate_id}"
            )

        refreshed_legacy = {
            str(row["legacy_knowledge_unit_id"]): row
            for row in refreshed.get("legacy_items") or []
        }
        article["migration_input_hash_version"] = str(
            refreshed.get("migration_input_hash_version") or "1"
        )
        article["migration_input_hash"] = str(
            refreshed.get("migration_input_hash") or ""
        )
        for decision in article.get("legacy_decisions") or []:
            legacy_id = str(decision["legacy_knowledge_unit_id"])
            refreshed_hash = str(
                refreshed_legacy[legacy_id].get("legacy_content_hash") or ""
            )
            if decision.get("legacy_content_hash") != refreshed_hash:
                changed_legacy_hash_count += 1
            decision["legacy_content_hash"] = refreshed_hash

        previous_existing = previous.get("existing_source_native_artifacts") or []
        refreshed_existing = refreshed.get("existing_source_native_artifacts") or []
        if previous_existing != refreshed_existing:
            snapshot = SourceSnapshot.model_validate(refreshed["source_snapshot"])
            reviewed_artifacts = {
                source_native_artifact_id(
                    snapshot,
                    SourceNativeArtifactCandidate.model_validate(artifact),
                ): artifact
                for artifact in article.get("artifacts") or []
            }
            refreshed_existing_by_id = {
                str(row["artifact_id"]): row for row in refreshed_existing
            }
            if set(refreshed_existing_by_id) != set(reviewed_artifacts):
                raise ValueError(
                    "refreshed migration input contains artifacts outside the "
                    f"reviewed output for {candidate_id}"
                )
            decisions = []
            for artifact_id, artifact in sorted(reviewed_artifacts.items()):
                expected_hash = public_record_hash(artifact)
                existing = refreshed_existing_by_id[artifact_id]
                if existing.get("artifact_hash") != expected_hash:
                    raise ValueError(
                        "materialized source-native artifact hash changed for "
                        f"{artifact_id}"
                    )
                materialized_artifact_count += 1
                decisions.append(
                    {
                        "existing_artifact_id": artifact_id,
                        "existing_artifact_hash": expected_hash,
                        "disposition": "retain_identity",
                        "replacement_artifact_key": artifact["artifact_key"],
                        "rationale": (
                            "The current source-native artifact exactly matches the "
                            "reviewed output, so its stable identity is retained."
                        ),
                    }
                )
            article["existing_artifact_decisions"] = decisions

    validated = validate_source_native_legacy_migration_output(
        rebound,
        inputs=refreshed_inputs,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(
            validated.public_dump(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-legacy-migration-rebind-v1",
        "status": "ok",
        "article_count": len(validated.articles),
        "changed_legacy_hash_count": changed_legacy_hash_count,
        "materialized_artifact_count": materialized_artifact_count,
        "destination": str(destination),
    }


def _migration_rebind_stable_payload(row: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in row.items()
        if key
        not in {
            "existing_source_native_artifacts",
            "migration_input_hash",
            "migration_input_hash_version",
        }
    }
    payload["legacy_items"] = [
        {
            key: value
            for key, value in legacy.items()
            if key != "legacy_content_hash"
        }
        for legacy in row.get("legacy_items") or []
    ]
    return canonical_json(payload)


def load_reviewed_source_native_legacy_migrations(
    destination: Path,
    *,
    reviewed_artifacts: Iterable[ReviewedSourceNativeArtifact],
    source_snapshots: Iterable[SourceSnapshot],
    source_units: Iterable[SourceUnit],
) -> list[ReviewedSourceNativeLegacyMigration]:
    rows = [
        ReviewedSourceNativeLegacyMigration.model_validate(row)
        for row in read_jsonl(destination / SOURCE_NATIVE_LEGACY_MIGRATIONS_NAME)
    ]
    artifacts_by_id = {row.artifact_id: row for row in reviewed_artifacts}
    snapshots_by_id = {row.source_snapshot_id: row for row in source_snapshots}
    units_by_id = {row.source_unit_id: row for row in source_units}
    legacy_owners: dict[str, str] = {}
    result_owners: dict[str, str] = {}
    for migration in rows:
        existing = legacy_owners.get(migration.legacy_knowledge_unit_id)
        if existing and existing != migration.migration_id:
            raise ValueError(
                "legacy knowledge unit has multiple migration decisions: "
                f"{migration.legacy_knowledge_unit_id}"
            )
        legacy_owners[migration.legacy_knowledge_unit_id] = migration.migration_id
        for result_id in migration.legacy_result_ids:
            owner = result_owners.get(result_id)
            if owner and owner != migration.migration_id:
                raise ValueError(
                    f"legacy result ID has multiple migration decisions: {result_id}"
                )
            result_owners[result_id] = migration.migration_id
        artifact = artifacts_by_id.get(migration.replacement_artifact_id)
        if artifact is None:
            raise ValueError(
                "legacy migration replacement artifact is missing: "
                f"{migration.replacement_artifact_id}"
            )
        if public_record_hash(artifact.artifact) != migration.replacement_artifact_hash:
            raise ValueError(
                "legacy migration replacement artifact hash changed: "
                f"{migration.migration_id}"
            )
        snapshot = snapshots_by_id.get(migration.source_snapshot_id)
        if (
            snapshot is None
            or snapshot.content_hash != migration.source_snapshot_content_hash
        ):
            raise ValueError(
                f"legacy migration source snapshot changed: {migration.migration_id}"
            )
        if snapshot.source_record_id != migration.source_record_id:
            raise ValueError(
                f"legacy migration source record changed: {migration.migration_id}"
            )
        artifact_snapshot_ids = {
            units_by_id[source_unit_id].source_snapshot_id
            for source_unit_id in artifact.artifact.source_unit_ids
            if source_unit_id in units_by_id
        }
        if artifact_snapshot_ids != {migration.source_snapshot_id}:
            raise ValueError(
                "legacy migration replacement must be supported by the exact source "
                f"snapshot: {migration.migration_id}"
            )
        for supporting in migration.supporting_replacement_artifacts:
            supporting_artifact = artifacts_by_id.get(supporting.artifact_id)
            if supporting_artifact is None:
                raise ValueError(
                    "legacy migration supporting artifact is missing: "
                    f"{supporting.artifact_id}"
                )
            if (
                public_record_hash(supporting_artifact.artifact)
                != supporting.artifact_hash
            ):
                raise ValueError(
                    "legacy migration supporting artifact hash changed: "
                    f"{migration.migration_id}"
                )
            supporting_snapshot_ids = {
                units_by_id[source_unit_id].source_snapshot_id
                for source_unit_id in supporting_artifact.artifact.source_unit_ids
                if source_unit_id in units_by_id
            }
            if supporting_snapshot_ids != {migration.source_snapshot_id}:
                raise ValueError(
                    "legacy migration supporting artifacts must use the exact "
                    f"source snapshot: {migration.migration_id}"
                )
    return sorted(rows, key=lambda row: row.migration_id)


def load_reviewed_source_native_artifact_migrations(
    destination: Path,
    *,
    reviewed_artifacts: Iterable[ReviewedSourceNativeArtifact],
    source_snapshots: Iterable[SourceSnapshot],
    source_units: Iterable[SourceUnit],
) -> list[ReviewedSourceNativeArtifactMigration]:
    rows = [
        ReviewedSourceNativeArtifactMigration.model_validate(row)
        for row in read_jsonl(destination / SOURCE_NATIVE_ARTIFACT_MIGRATIONS_NAME)
    ]
    artifacts_by_id = {row.artifact_id: row for row in reviewed_artifacts}
    snapshots_by_id = {row.source_snapshot_id: row for row in source_snapshots}
    units_by_id = {row.source_unit_id: row for row in source_units}
    prior_owners: dict[str, str] = {}
    for migration in rows:
        owner = prior_owners.get(migration.prior_artifact_id)
        if owner and owner != migration.migration_id:
            raise ValueError(
                "source-native artifact has multiple migration decisions: "
                f"{migration.prior_artifact_id}"
            )
        prior_owners[migration.prior_artifact_id] = migration.migration_id
        replacement = artifacts_by_id.get(migration.replacement_artifact_id)
        if replacement is None:
            raise ValueError(
                "source-native artifact migration replacement is missing: "
                f"{migration.replacement_artifact_id}"
            )
        if (
            public_record_hash(replacement.artifact)
            != migration.replacement_artifact_hash
        ):
            raise ValueError(
                "source-native artifact migration replacement hash changed: "
                f"{migration.migration_id}"
            )
        snapshot = snapshots_by_id.get(migration.source_snapshot_id)
        if (
            snapshot is None
            or snapshot.content_hash != migration.source_snapshot_content_hash
        ):
            raise ValueError(
                "source-native artifact migration source snapshot changed: "
                f"{migration.migration_id}"
            )
        if snapshot.source_record_id != migration.source_record_id:
            raise ValueError(
                "source-native artifact migration source record changed: "
                f"{migration.migration_id}"
            )
        replacement_snapshot_ids = {
            units_by_id[source_unit_id].source_snapshot_id
            for source_unit_id in replacement.artifact.source_unit_ids
            if source_unit_id in units_by_id
        }
        if replacement_snapshot_ids != {migration.source_snapshot_id}:
            raise ValueError(
                "source-native artifact migration replacement must use the exact "
                f"source snapshot: {migration.migration_id}"
            )
    return sorted(rows, key=lambda row: row.migration_id)


def promote_source_native_legacy_migration(
    *,
    input_path: Path,
    output_path: Path,
    destination: Path,
    base_dir: Path,
    reviewer: str,
    model: str,
    reviewed_at: str | None = None,
    generated_output_path: Path | None = None,
) -> dict[str, Any]:
    from .source_native import (
        PILOT_FILE_NAMES,
        json_change_count,
        load_source_native_pilot_directory,
        promote_source_native_distillation,
        write_source_native_manifest,
    )

    inputs = list(read_jsonl(input_path))
    reviewed_output = validate_source_native_legacy_migration_output(
        json.loads(output_path.read_text(encoding="utf-8")),
        inputs=inputs,
    )
    generated_articles_by_id: dict[str, dict[str, Any]] = {}
    if generated_output_path is not None:
        raw_generated = json.loads(generated_output_path.read_text(encoding="utf-8"))
        if not isinstance(raw_generated, dict) or raw_generated.get("schema") != (
            "rock-kb-source-native-legacy-migration-output-v1"
        ):
            raise ValueError("generated migration output has an unknown schema")
        if raw_generated.get("variant_id") != ("source_native_legacy_migration_v1"):
            raise ValueError("generated migration output has an unknown variant")
        raw_articles = raw_generated.get("articles")
        if not isinstance(raw_articles, list) or not all(
            isinstance(row, dict) for row in raw_articles
        ):
            raise ValueError("generated migration output requires article objects")
        for row in raw_articles:
            candidate_id = str(row.get("candidate_id") or "")
            if not candidate_id or candidate_id in generated_articles_by_id:
                raise ValueError(
                    "generated migration candidate IDs must be non-empty and unique"
                )
            generated_articles_by_id[candidate_id] = row
        if set(generated_articles_by_id) != {
            article.candidate_id for article in reviewed_output.articles
        }:
            raise ValueError(
                "generated migration output must cover the same candidates as the "
                "reviewed output"
            )
    reviewed_at = reviewed_at or now_iso()
    inputs_by_id = {str(row["candidate_id"]): row for row in inputs}

    with tempfile.TemporaryDirectory(
        prefix="rock-kb-source-native-migration-"
    ) as temporary:
        temporary_dir = Path(temporary)
        standard_output_path = temporary_dir / "reviewed-source-native-output.json"
        standard_output_path.write_text(
            json.dumps(
                migration_output_as_source_native(reviewed_output).public_dump(),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        generated_standard_articles = {
            candidate_id: {
                key: value
                for key, value in row.items()
                if key
                not in {
                    "migration_input_hash",
                    "migration_input_hash_version",
                    "legacy_decisions",
                    "existing_artifact_decisions",
                }
            }
            for candidate_id, row in generated_articles_by_id.items()
        }
        promoted_dir = temporary_dir / "bundle"
        promote_source_native_distillation(
            input_path=input_path,
            output_path=standard_output_path,
            destination=promoted_dir,
            reviewer=reviewer,
            model=model,
            reviewed_at=reviewed_at,
            generation_prompt_id=SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID,
            generation_prompt_version=SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION,
            generation_prompt_path=SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_PATH,
            base_dir=base_dir,
            generated_article_payloads=(generated_standard_articles or None),
        )

        promoted = load_source_native_pilot_directory(promoted_dir)
        artifacts_by_candidate_and_key = {
            (row.source_candidate_id, row.artifact.artifact_key): row
            for row in promoted["reviewed_artifacts"]
        }
        snapshots_by_id = {
            row.source_snapshot_id: row for row in promoted["source_snapshots"]
        }
        base_migrations = [
            ReviewedSourceNativeLegacyMigration.model_validate(row)
            for row in read_jsonl(base_dir / SOURCE_NATIVE_LEGACY_MIGRATIONS_NAME)
        ]
        migrations_by_legacy_id = {
            row.legacy_knowledge_unit_id: row for row in base_migrations
        }
        base_artifact_migrations = [
            ReviewedSourceNativeArtifactMigration.model_validate(row)
            for row in read_jsonl(base_dir / SOURCE_NATIVE_ARTIFACT_MIGRATIONS_NAME)
        ]
        artifact_migrations_by_prior_id = {
            row.prior_artifact_id: row for row in base_artifact_migrations
        }
        for article in reviewed_output.articles:
            input_row = inputs_by_id[article.candidate_id]
            reviewed_article_payload = article.public_dump()
            generated_article_payload = generated_articles_by_id.get(
                article.candidate_id,
                reviewed_article_payload,
            )
            generated_article_hash = sha256_text(
                canonical_json(generated_article_payload)
            )
            reviewed_article_hash = sha256_text(
                canonical_json(reviewed_article_payload)
            )
            review_correction_count = json_change_count(
                generated_article_payload,
                reviewed_article_payload,
            )
            legacy_by_id = {
                str(row["legacy_knowledge_unit_id"]): row
                for row in input_row["legacy_items"]
            }
            snapshot = SourceSnapshot.model_validate(input_row["source_snapshot"])
            promoted_snapshot = snapshots_by_id.get(snapshot.source_snapshot_id)
            if promoted_snapshot is None or not promoted_snapshot.content_hash:
                raise ValueError(
                    f"promoted source snapshot is missing for {article.candidate_id}"
                )
            existing_artifacts_by_id = {
                str(row["artifact_id"]): row
                for row in input_row.get("existing_source_native_artifacts") or []
            }
            for decision in article.existing_artifact_decisions:
                existing = existing_artifacts_by_id[decision.existing_artifact_id]
                replacement = artifacts_by_candidate_and_key.get(
                    (article.candidate_id, decision.replacement_artifact_key)
                )
                if replacement is None:
                    raise ValueError(
                        "promoted source-native artifact replacement is missing for "
                        f"{decision.existing_artifact_id}"
                    )
                if decision.disposition == "retain_identity":
                    if replacement.artifact_id != decision.existing_artifact_id:
                        raise ValueError(
                            "retained source-native artifact identity changed during "
                            f"promotion: {decision.existing_artifact_id}"
                        )
                    continue
                dependent_migrations = [
                    row
                    for row in base_artifact_migrations
                    if row.replacement_artifact_id == decision.existing_artifact_id
                ]
                if dependent_migrations:
                    raise ValueError(
                        "chained source-native artifact migrations require explicit "
                        "flattening before supersession: "
                        f"{decision.existing_artifact_id}"
                    )
                migration_id = (
                    "source-native-artifact-migration:"
                    + sha256_text(
                        f"{decision.existing_artifact_id}:{replacement.artifact_id}"
                    )[:24]
                )
                artifact_migrations_by_prior_id[decision.existing_artifact_id] = (
                    ReviewedSourceNativeArtifactMigration(
                        schema=("rock-kb-reviewed-source-native-artifact-migration-v1"),
                        migration_id=migration_id,
                        source_record_id=str(snapshot.source_record_id),
                        source_snapshot_id=snapshot.source_snapshot_id,
                        source_snapshot_content_hash=promoted_snapshot.content_hash,
                        prior_artifact_id=decision.existing_artifact_id,
                        prior_artifact_hash=str(existing["artifact_hash"]),
                        replacement_artifact_id=replacement.artifact_id,
                        replacement_artifact_hash=public_record_hash(
                            replacement.artifact
                        ),
                        migration_input_hash=article.migration_input_hash,
                        migration_input_hash_version=(
                            article.migration_input_hash_version
                        ),
                        rationale=decision.rationale,
                        generation_model=model,
                        generation_prompt_id=(SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID),
                        generation_prompt_version=(
                            SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION
                        ),
                        generated_article_hash=generated_article_hash,
                        reviewed_article_hash=reviewed_article_hash,
                        review_correction_count=review_correction_count,
                        reviewer=reviewer,
                        reviewed_at=reviewed_at,
                    )
                )
            for decision in article.legacy_decisions:
                legacy = legacy_by_id[decision.legacy_knowledge_unit_id]
                if decision.disposition == "retain":
                    migrations_by_legacy_id.pop(
                        decision.legacy_knowledge_unit_id,
                        None,
                    )
                    continue
                reviewed_artifact = artifacts_by_candidate_and_key.get(
                    (article.candidate_id, str(decision.replacement_artifact_key))
                )
                if reviewed_artifact is None:
                    raise ValueError(
                        "promoted replacement artifact is missing for "
                        f"{decision.legacy_knowledge_unit_id}"
                    )
                supporting_artifacts = [
                    artifacts_by_candidate_and_key[(article.candidate_id, artifact_key)]
                    for artifact_key in decision.supporting_replacement_artifact_keys
                ]
                migration_id = (
                    "source-native-legacy-migration:"
                    + sha256_text(
                        f"{decision.legacy_knowledge_unit_id}:"
                        f"{reviewed_artifact.artifact_id}"
                    )[:24]
                )
                migrations_by_legacy_id[decision.legacy_knowledge_unit_id] = (
                    ReviewedSourceNativeLegacyMigration(
                        schema="rock-kb-reviewed-source-native-legacy-migration-v1",
                        migration_id=migration_id,
                        source_record_id=str(snapshot.source_record_id),
                        source_snapshot_id=snapshot.source_snapshot_id,
                        source_snapshot_content_hash=promoted_snapshot.content_hash,
                        legacy_knowledge_unit_id=decision.legacy_knowledge_unit_id,
                        legacy_result_ids=sorted(set(legacy["legacy_result_ids"])),
                        legacy_knowledge_type=legacy["legacy_knowledge_type"],
                        legacy_ingestion_mode=legacy["legacy_ingestion_mode"],
                        legacy_content_hash=decision.legacy_content_hash,
                        migration_input_hash=article.migration_input_hash,
                        migration_input_hash_version=(
                            article.migration_input_hash_version
                        ),
                        replacement_artifact_id=reviewed_artifact.artifact_id,
                        replacement_artifact_hash=public_record_hash(
                            reviewed_artifact.artifact
                        ),
                        supporting_replacement_artifacts=[
                            {
                                "artifact_id": row.artifact_id,
                                "artifact_hash": public_record_hash(row.artifact),
                            }
                            for row in supporting_artifacts
                        ],
                        rationale=decision.rationale,
                        generation_model=model,
                        generation_prompt_id=(SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_ID),
                        generation_prompt_version=(
                            SOURCE_NATIVE_LEGACY_MIGRATION_PROMPT_VERSION
                        ),
                        generated_article_hash=generated_article_hash,
                        reviewed_article_hash=reviewed_article_hash,
                        review_correction_count=review_correction_count,
                        reviewer=reviewer,
                        reviewed_at=reviewed_at,
                    )
                )
        write_jsonl(
            promoted_dir / SOURCE_NATIVE_LEGACY_MIGRATIONS_NAME,
            [
                row.public_dump()
                for row in sorted(
                    migrations_by_legacy_id.values(),
                    key=lambda value: value.migration_id,
                )
            ],
        )
        write_jsonl(
            promoted_dir / SOURCE_NATIVE_ARTIFACT_MIGRATIONS_NAME,
            [
                row.public_dump()
                for row in sorted(
                    artifact_migrations_by_prior_id.values(),
                    key=lambda value: value.migration_id,
                )
            ],
        )
        write_source_native_manifest(promoted_dir)
        validated_bundle = load_source_native_pilot_directory(promoted_dir)
        migration_count = len(validated_bundle["legacy_migrations"])
        artifact_migration_count = len(validated_bundle["artifact_migrations"])

        destination.mkdir(parents=True, exist_ok=True)
        for name in (*PILOT_FILE_NAMES, "manifest.json"):
            source = promoted_dir / name
            target = destination / name
            if source.exists():
                shutil.copy2(source, target)
            elif target.exists():
                target.unlink()

    return {
        "schema": "rock-kb-source-native-legacy-migration-promotion-v1",
        "status": "ok",
        "destination": str(destination),
        "article_count": len(reviewed_output.articles),
        "replacement_count": sum(
            row.disposition == "replace"
            for article in reviewed_output.articles
            for row in article.legacy_decisions
        ),
        "retained_count": sum(
            row.disposition == "retain"
            for article in reviewed_output.articles
            for row in article.legacy_decisions
        ),
        "migration_count": migration_count,
        "artifact_migration_count": artifact_migration_count,
    }


class LegacyMigrationIndex:
    def __init__(
        self,
        migrations: Iterable[ReviewedSourceNativeLegacyMigration],
    ) -> None:
        self.migrations = list(migrations)
        self.matched_migration_ids: set[str] = set()
        self.by_result_id: dict[str, ReviewedSourceNativeLegacyMigration] = {}
        for migration in self.migrations:
            for result_id in migration.legacy_result_ids:
                existing = self.by_result_id.get(result_id)
                if existing and existing.migration_id != migration.migration_id:
                    raise ValueError(
                        f"legacy result ID has multiple migrations: {result_id}"
                    )
                self.by_result_id[result_id] = migration

    def match(
        self,
        *,
        result_ids: Iterable[str],
        knowledge_type: str,
        ingestion_mode: str,
        content_hash: str,
        source_record_ids: Iterable[str],
    ) -> ReviewedSourceNativeLegacyMigration | None:
        matches = {
            row.migration_id: row
            for result_id in result_ids
            if (row := self.by_result_id.get(str(result_id)))
        }
        if not matches:
            return None
        if len(matches) != 1:
            raise ValueError("one legacy row matched multiple migration decisions")
        migration = next(iter(matches.values()))
        if migration.legacy_knowledge_type != knowledge_type:
            raise ValueError(
                f"legacy migration knowledge type changed: {migration.migration_id}"
            )
        if migration.legacy_ingestion_mode != ingestion_mode:
            raise ValueError(
                f"legacy migration ingestion mode changed: {migration.migration_id}"
            )
        if migration.legacy_content_hash != content_hash:
            raise ValueError(
                f"legacy migration content hash changed: {migration.migration_id}"
            )
        if migration.source_record_id not in set(source_record_ids):
            raise ValueError(
                f"legacy migration source record changed: {migration.migration_id}"
            )
        if migration.migration_id in self.matched_migration_ids:
            raise ValueError(
                "legacy migration matched more than one active projection row: "
                f"{migration.migration_id}"
            )
        self.matched_migration_ids.add(migration.migration_id)
        return migration

    def assert_all_applied(self) -> None:
        missing = sorted(
            {row.migration_id for row in self.migrations} - self.matched_migration_ids
        )
        if missing:
            raise ValueError(
                "reviewed legacy migrations did not match active legacy rows: "
                + ", ".join(missing[:3])
            )

    def aliases_by_replacement(self) -> dict[str, list[str]]:
        aliases: dict[str, set[str]] = defaultdict(set)
        for migration in self.migrations:
            aliases[migration.replacement_artifact_id].update(
                {
                    migration.legacy_knowledge_unit_id,
                    *migration.legacy_result_ids,
                }
            )
        return {artifact_id: sorted(values) for artifact_id, values in aliases.items()}

    def migrations_by_replacement(
        self,
    ) -> dict[str, list[ReviewedSourceNativeLegacyMigration]]:
        rows: dict[str, list[ReviewedSourceNativeLegacyMigration]] = defaultdict(list)
        for migration in self.migrations:
            rows[migration.replacement_artifact_id].append(migration)
        return {
            artifact_id: sorted(values, key=lambda row: row.migration_id)
            for artifact_id, values in rows.items()
        }


class SourceNativeArtifactMigrationIndex:
    def __init__(
        self,
        migrations: Iterable[ReviewedSourceNativeArtifactMigration],
    ) -> None:
        self.migrations = list(migrations)
        prior_ids = [row.prior_artifact_id for row in self.migrations]
        if len(prior_ids) != len(set(prior_ids)):
            raise ValueError(
                "source-native prior artifact IDs must have one migration owner"
            )

    def aliases_by_replacement(self) -> dict[str, list[str]]:
        aliases: dict[str, set[str]] = defaultdict(set)
        for migration in self.migrations:
            aliases[migration.replacement_artifact_id].add(migration.prior_artifact_id)
        return {artifact_id: sorted(values) for artifact_id, values in aliases.items()}

    def migrations_by_replacement(
        self,
    ) -> dict[str, list[ReviewedSourceNativeArtifactMigration]]:
        rows: dict[str, list[ReviewedSourceNativeArtifactMigration]] = defaultdict(list)
        for migration in self.migrations:
            rows[migration.replacement_artifact_id].append(migration)
        return {
            artifact_id: sorted(values, key=lambda row: row.migration_id)
            for artifact_id, values in rows.items()
        }


def load_identity_registry(repo_root: Path = REPO_ROOT) -> list[KnowledgeIdentity]:
    return [
        KnowledgeIdentity.model_validate(row)
        for row in read_jsonl(
            repo_root / "canonical" / "identity" / "v1" / "identity-registry.jsonl"
        )
    ]
