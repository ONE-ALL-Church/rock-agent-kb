from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from rock_kb.canonical_knowledge import build_canonical_knowledge_bundle
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.normalize import canonical_record_id
from rock_kb.schemas import (
    GenerationActivity,
    ReviewedSourceNativeArtifact,
    ReviewedSourceNativeArtifactMigration,
    ReviewedSourceNativeLegacyMigration,
    SourceLocator,
    SourceNativeArtifactCandidate,
    SourceSnapshot,
    SourceUnit,
)
from rock_kb.source_native import (
    source_native_artifact_id,
    source_native_model_input_hash,
)
from rock_kb.source_native_migration import (
    _install_rebound_bundle_transactionally,
    build_source_native_legacy_migration_inputs,
    promote_rebound_source_native_legacy_migrations,
    public_record_hash,
    rebind_source_native_legacy_migration_output,
    source_native_legacy_migration_input_hash,
    validate_source_native_legacy_migration_output,
)


def rehash_migration_input(row: dict) -> dict:
    snapshot = SourceSnapshot.model_validate(row["source_snapshot"])
    row["source_input_hash"] = source_native_model_input_hash(
        snapshot=snapshot,
        source_units=[
            SourceUnit.model_validate(value) for value in row["source_units"]
        ],
        concept_ids=row["concept_ids"],
        existing_claims=row["existing_claims"],
        documentation_path=row.get("documentation_path"),
        documentation_branches=row.get("documentation_branches") or [],
        documentation_current_version=row.get("documentation_current_version"),
    )
    row["migration_input_hash_version"] = "2"
    row["migration_input_hash"] = source_native_legacy_migration_input_hash(row)
    return row


def migration_input() -> dict:
    return rehash_migration_input(
        {
            "schema": "rock-kb-source-native-distillation-input-v1",
            "candidate_id": "source-native-candidate:test",
            "source_input_hash": "a" * 64,
            "migration_input_hash": "b" * 64,
            "source_snapshot": {
                "schema": "rock-kb-source-snapshot-v2",
                "source_snapshot_id": "source-snapshot:test",
                "source_id": "rock_documentation",
                "source_record_id": "rock_documentation:article:100",
                "source_work_id": "documentation-article:100",
                "canonical_url": "https://community.rockrms.com/documentation/test",
                "title": "Test Article",
                "content_hash": "c" * 64,
                "normalized_content_hash": "c" * 64,
                "authority_tier": "official",
                "public_policy": "cite_and_summarize_only",
                "derivation": {"documentation_article_id": 100},
            },
            "source_units": [
                {
                    "schema": "rock-kb-source-unit-v2",
                    "source_unit_id": "source-unit:test",
                    "source_snapshot_id": "source-snapshot:test",
                    "unit_kind": "paragraph",
                    "locator": {
                        "kind": "paragraph",
                        "value": "Overview / paragraph-1",
                        "url": "https://community.rockrms.com/documentation/test",
                    },
                    "text": "The feature performs the documented behavior.",
                    "normalized_content_hash": "d" * 64,
                    "required_public_handling": "cite_and_summarize_only",
                }
            ],
            "concept_ids": ["workflows"],
            "existing_claims": [],
            "legacy_items": [
                {
                    "legacy_knowledge_unit_id": "knowledge:claim:legacy",
                    "legacy_result_ids": ["claim:legacy"],
                    "legacy_knowledge_type": "claim",
                    "legacy_ingestion_mode": "legacy_reviewed_claim_projection",
                    "legacy_content_hash": "e" * 64,
                    "title": "Legacy behavior",
                    "retrieval_text": "The feature performs the documented behavior.",
                    "concept_facets": ["workflows"],
                    "source_record_ids": ["rock_documentation:article:100"],
                }
            ],
            "existing_source_native_artifacts": [],
        }
    )


def migration_output() -> dict:
    input_row = migration_input()
    return {
        "schema": "rock-kb-source-native-legacy-migration-output-v1",
        "variant_id": "source_native_legacy_migration_v1",
        "articles": [
            {
                "candidate_id": "source-native-candidate:test",
                "source_input_hash": input_row["source_input_hash"],
                "migration_input_hash_version": "2",
                "migration_input_hash": input_row["migration_input_hash"],
                "unit_decisions": [
                    {
                        "source_unit_id": "source-unit:test",
                        "disposition": "claim",
                        "existing_relation": "novel",
                        "related_existing_claim_ids": [],
                        "evidence_summary": "The source states the behavior.",
                        "decision_reason": "The behavior is independently answerable.",
                        "mixed_material": False,
                    }
                ],
                "artifacts": [
                    {
                        "artifact_key": "feature-behavior",
                        "artifact_type": "claim",
                        "source_unit_ids": ["source-unit:test"],
                        "title": "The feature performs the documented behavior.",
                        "retrieval_text": "The feature performs the documented behavior.",
                        "independent_question": "What behavior does the feature perform?",
                        "rationale": "The source unit directly states this behavior.",
                        "concept_ids": ["workflows"],
                        "claim_type": "behavior",
                        "evidence_class": "current_behavior",
                        "confidence": "high",
                        "payload": {
                            "summary": "The feature performs the documented behavior."
                        },
                    }
                ],
                "verification_requests": [],
                "unmatched_routing_terms": [],
                "review_notes": [
                    "The source-native claim fully preserves the legacy behavior."
                ],
                "coverage_check": {
                    "material_unit_count": 1,
                    "captured_source_unit_ids": ["source-unit:test"],
                    "no_artifact_source_unit_ids": [],
                    "omitted_source_units": [],
                },
                "legacy_decisions": [
                    {
                        "legacy_knowledge_unit_id": "knowledge:claim:legacy",
                        "legacy_content_hash": "e" * 64,
                        "disposition": "replace",
                        "coverage": "full",
                        "replacement_artifact_key": "feature-behavior",
                        "supporting_replacement_artifact_keys": [],
                        "rationale": (
                            "The source-native claim preserves the complete supported "
                            "behavior in one independently retrievable artifact."
                        ),
                    }
                ],
                "existing_artifact_decisions": [],
            }
        ],
    }


def test_migration_output_requires_explicit_nullable_artifact_contract_fields():
    output = migration_output()
    del output["articles"][0]["artifacts"][0]["claim_type"]

    with pytest.raises(ValueError, match="claim_type"):
        validate_source_native_legacy_migration_output(
            output,
            inputs=[migration_input()],
        )


def test_migration_output_requires_explicit_nullable_replacement_key():
    output = migration_output()
    decision = output["articles"][0]["legacy_decisions"][0]
    decision["disposition"] = "retain"
    decision["coverage"] = "partial"
    del decision["replacement_artifact_key"]

    with pytest.raises(ValueError, match="replacement_artifact_key"):
        validate_source_native_legacy_migration_output(
            output,
            inputs=[migration_input()],
        )


def test_migration_input_rebuild_projects_legacy_rows_before_retirement(
    monkeypatch,
    tmp_path,
):
    candidate = migration_input()
    source_snapshot = SourceSnapshot.model_validate(candidate["source_snapshot"])
    source_unit = SourceUnit.model_validate(candidate["source_units"][0])
    legacy = SimpleNamespace(
        ingestion_mode="legacy_summary_projection",
        knowledge_type="source_summary",
        source_unit_ids=[source_unit.source_unit_id],
        knowledge_unit_id="source:rock_documentation:article:100",
        legacy_ids=["knowledge:source_summary:test"],
        content_hash="9" * 64,
        title="Test Article",
        retrieval_text="The article documents the feature behavior.",
        concept_facets=["workflows"],
    )

    def fake_build_canonical_knowledge_bundle(**kwargs):
        assert kwargs["identity_registry"] == []
        assert kwargs["include_source_native_pilot"] is False
        assert kwargs["include_legacy_migrations"] is False
        return (
            SimpleNamespace(
                source_snapshots=[source_snapshot],
                source_units=[source_unit],
                knowledge_units=[legacy],
            ),
            {},
        )

    monkeypatch.setattr(
        "rock_kb.canonical_knowledge.build_canonical_knowledge_bundle",
        fake_build_canonical_knowledge_bundle,
    )
    monkeypatch.setattr(
        "rock_kb.source_native.load_source_native_pilot",
        lambda _repo_root: {
            "source_snapshots": [source_snapshot],
            "source_units": [source_unit],
            "reviewed_artifacts": [],
        },
    )
    input_path = tmp_path / "source-native-input.jsonl"
    destination = tmp_path / "migration-input.jsonl"
    write_jsonl(input_path, [candidate])

    result = build_source_native_legacy_migration_inputs(
        source_native_input_path=input_path,
        destination=destination,
        repo_root=tmp_path,
    )

    output = list(read_jsonl(destination))
    assert result["legacy_item_count"] == 1
    assert output[0]["legacy_items"][0]["legacy_content_hash"] == "9" * 64


def test_migration_input_reconciles_same_family_redirect_alias(
    monkeypatch,
    tmp_path,
):
    candidate = migration_input()
    candidate["source_snapshot"].update(
        {
            "source_record_id": "rock_lava_docs:new",
            "source_id": "rock_lava_docs",
            "canonical_url": "https://community.rockrms.com/lava/commands/getting-started",
            "location_aliases": ["https://community.rockrms.com/lava/commands"],
        }
    )
    rehash_migration_input(candidate)
    legacy_snapshot = SourceSnapshot.model_validate(
        {
            **candidate["source_snapshot"],
            "source_snapshot_id": "source-snapshot:legacy",
            "source_record_id": "rock_lava_docs:old",
            "canonical_url": "https://community.rockrms.com/lava/commands",
            "location_aliases": [],
        }
    )
    legacy_unit = SourceUnit.model_validate(
        {
            **candidate["source_units"][0],
            "source_unit_id": "source-unit:legacy",
            "source_snapshot_id": legacy_snapshot.source_snapshot_id,
        }
    )
    legacy = SimpleNamespace(
        ingestion_mode="legacy_summary_projection",
        knowledge_type="source_summary",
        source_unit_ids=[legacy_unit.source_unit_id],
        knowledge_unit_id="source:rock_lava_docs:old",
        legacy_ids=["knowledge:source_summary:old"],
        content_hash="9" * 64,
        title="Getting Started",
        retrieval_text="Enable commands explicitly.",
        concept_facets=["lava"],
    )

    monkeypatch.setattr(
        "rock_kb.canonical_knowledge.build_canonical_knowledge_bundle",
        lambda **_kwargs: (
            SimpleNamespace(
                source_snapshots=[legacy_snapshot],
                source_units=[legacy_unit],
                knowledge_units=[legacy],
            ),
            {},
        ),
    )
    monkeypatch.setattr(
        "rock_kb.source_native.load_source_native_pilot",
        lambda _repo_root: {
            "source_snapshots": [],
            "source_units": [],
            "reviewed_artifacts": [],
        },
    )
    input_path = tmp_path / "source-native-input.jsonl"
    destination = tmp_path / "migration-input.jsonl"
    write_jsonl(input_path, [candidate])

    result = build_source_native_legacy_migration_inputs(
        source_native_input_path=input_path,
        destination=destination,
        repo_root=tmp_path,
    )

    assert result["legacy_item_count"] == 1
    assert result["reconciled_legacy_source_record_alias_count"] == 1
    assert next(iter(read_jsonl(destination)))["legacy_items"][0][
        "legacy_knowledge_unit_id"
    ] == "source:rock_lava_docs:old"


def test_migration_rebind_accepts_only_hash_binding_changes(tmp_path):
    previous = migration_input()
    refreshed = copy.deepcopy(previous)
    refreshed["legacy_items"][0]["legacy_content_hash"] = "f" * 64
    refreshed["source_snapshot"]["last_checked_at"] = "2026-08-12T10:00:00Z"
    refreshed["source_snapshot"]["observation_status"] = "unchanged"
    artifact = SourceNativeArtifactCandidate.model_validate(
        migration_output()["articles"][0]["artifacts"][0]
    )
    snapshot = SourceSnapshot.model_validate(refreshed["source_snapshot"])
    artifact_id = source_native_artifact_id(snapshot, artifact)
    refreshed["existing_source_native_artifacts"] = [
        {
            "artifact_id": artifact_id,
            "artifact_hash": public_record_hash(artifact),
            "artifact": artifact.public_dump(),
        }
    ]
    rehash_migration_input(refreshed)
    previous_path = tmp_path / "previous.jsonl"
    refreshed_path = tmp_path / "refreshed.jsonl"
    output_path = tmp_path / "reviewed-output.json"
    destination = tmp_path / "rebound-output.json"
    write_jsonl(previous_path, [previous])
    write_jsonl(refreshed_path, [refreshed])
    output_path.write_text(
        json.dumps(migration_output(), indent=2) + "\n",
        encoding="utf-8",
    )

    result = rebind_source_native_legacy_migration_output(
        previous_input_path=previous_path,
        refreshed_input_path=refreshed_path,
        output_path=output_path,
        destination=destination,
    )
    rebound = json.loads(destination.read_text(encoding="utf-8"))
    assert result["changed_legacy_hash_count"] == 1
    assert result["materialized_artifact_count"] == 1
    assert rebound["articles"][0]["migration_input_hash"] == (
        refreshed["migration_input_hash"]
    )
    assert rebound["articles"][0]["legacy_decisions"][0][
        "legacy_content_hash"
    ] == "f" * 64
    assert rebound["articles"][0]["existing_artifact_decisions"][0][
        "disposition"
    ] == "retain_identity"

    changed_meaning = copy.deepcopy(refreshed)
    changed_meaning["legacy_items"][0]["retrieval_text"] += " Changed."
    rehash_migration_input(changed_meaning)
    write_jsonl(refreshed_path, [changed_meaning])
    with pytest.raises(ValueError, match="more than hash bindings"):
        rebind_source_native_legacy_migration_output(
            previous_input_path=previous_path,
            refreshed_input_path=refreshed_path,
            output_path=output_path,
            destination=destination,
        )


def test_migration_rebind_materializes_historical_nullable_fields(tmp_path):
    previous = migration_input()
    refreshed = copy.deepcopy(previous)
    refreshed["legacy_items"][0]["legacy_content_hash"] = "f" * 64

    reviewed = migration_output()
    reviewed_artifact = reviewed["articles"][0]["artifacts"][0]
    reviewed_artifact["artifact_type"] = "source_summary"
    reviewed["articles"][0]["unit_decisions"][0]["disposition"] = (
        "source_summary"
    )
    del reviewed_artifact["claim_type"]
    del reviewed_artifact["evidence_class"]

    materialized_artifact = copy.deepcopy(reviewed_artifact)
    materialized_artifact["claim_type"] = None
    materialized_artifact["evidence_class"] = None
    artifact = SourceNativeArtifactCandidate.model_validate(materialized_artifact)
    snapshot = SourceSnapshot.model_validate(refreshed["source_snapshot"])
    artifact_id = source_native_artifact_id(snapshot, artifact)
    refreshed["existing_source_native_artifacts"] = [
        {
            "artifact_id": artifact_id,
            "artifact_hash": public_record_hash(artifact),
            "artifact": artifact.public_dump(),
        }
    ]
    rehash_migration_input(refreshed)

    previous_path = tmp_path / "previous.jsonl"
    refreshed_path = tmp_path / "refreshed.jsonl"
    output_path = tmp_path / "reviewed-output.json"
    destination = tmp_path / "rebound-output.json"
    write_jsonl(previous_path, [previous])
    write_jsonl(refreshed_path, [refreshed])
    output_path.write_text(json.dumps(reviewed) + "\n", encoding="utf-8")

    result = rebind_source_native_legacy_migration_output(
        previous_input_path=previous_path,
        refreshed_input_path=refreshed_path,
        output_path=output_path,
        destination=destination,
    )

    rebound_artifact = json.loads(destination.read_text(encoding="utf-8"))[
        "articles"
    ][0]["artifacts"][0]
    assert result["materialized_nullable_field_count"] == 2
    assert rebound_artifact["claim_type"] is None
    assert rebound_artifact["evidence_class"] is None


def test_migration_rebind_promotion_updates_only_hash_bindings(
    monkeypatch,
    tmp_path,
):
    previous = migration_input()
    refreshed = copy.deepcopy(previous)
    refreshed["legacy_items"][0]["legacy_content_hash"] = "f" * 64
    artifact = SourceNativeArtifactCandidate.model_validate(
        migration_output()["articles"][0]["artifacts"][0]
    )
    snapshot = SourceSnapshot.model_validate(refreshed["source_snapshot"])
    artifact_id = source_native_artifact_id(snapshot, artifact)
    refreshed["existing_source_native_artifacts"] = [
        {
            "artifact_id": artifact_id,
            "artifact_hash": public_record_hash(artifact),
            "artifact": artifact.public_dump(),
        }
    ]
    rehash_migration_input(refreshed)

    reviewed = migration_output()
    reviewed["articles"][0]["migration_input_hash"] = refreshed[
        "migration_input_hash"
    ]
    reviewed["articles"][0]["legacy_decisions"][0][
        "legacy_content_hash"
    ] = "f" * 64
    reviewed["articles"][0]["existing_artifact_decisions"] = [
        {
            "existing_artifact_id": artifact_id,
            "existing_artifact_hash": public_record_hash(artifact),
            "disposition": "retain_identity",
            "replacement_artifact_key": artifact.artifact_key,
            "rationale": (
                "The current artifact exactly matches the reviewed output, so "
                "its stable identity is retained."
            ),
        }
    ]
    reviewed_record = ReviewedSourceNativeArtifact(
        schema="rock-kb-reviewed-source-native-artifact-v1",
        artifact_id=artifact_id,
        source_candidate_id=refreshed["candidate_id"],
        generation_activity_id="generation:test",
        artifact=artifact,
        review_state="reviewer_approved",
        reviewer="test-reviewer",
        reviewed_at="2026-08-04T00:00:00Z",
        source_input_hash=refreshed["source_input_hash"],
    )
    decision = reviewed["articles"][0]["legacy_decisions"][0]
    existing_migration = ReviewedSourceNativeLegacyMigration(
        schema="rock-kb-reviewed-source-native-legacy-migration-v1",
        migration_id="source-native-legacy-migration:test",
        source_record_id=str(snapshot.source_record_id),
        source_snapshot_id=snapshot.source_snapshot_id,
        source_snapshot_content_hash=snapshot.content_hash,
        legacy_knowledge_unit_id=decision["legacy_knowledge_unit_id"],
        legacy_result_ids=refreshed["legacy_items"][0]["legacy_result_ids"],
        legacy_knowledge_type="claim",
        legacy_ingestion_mode="legacy_reviewed_claim_projection",
        legacy_content_hash="e" * 64,
        migration_input_hash=previous["migration_input_hash"],
        migration_input_hash_version="2",
        replacement_artifact_id=artifact_id,
        replacement_artifact_hash=public_record_hash(artifact),
        rationale=decision["rationale"],
        generation_model="test-model",
        generation_prompt_id="source-native-legacy-migration-v1",
        generation_prompt_version="1.3.1",
        generated_article_hash="1" * 64,
        reviewed_article_hash="2" * 64,
        review_correction_count=1,
        reviewer="original-reviewer",
        reviewed_at="2026-08-04T00:00:00Z",
    )
    base_bundle = {
        "source_snapshots": [snapshot],
        "source_units": [],
        "generation_activities": [],
        "reviewed_artifacts": [reviewed_record],
        "relationships": [],
        "evaluation_set": [],
        "verification_queue": [],
        "verification_resolutions": [],
        "legacy_migrations": [existing_migration],
        "artifact_migrations": [],
    }
    monkeypatch.setattr(
        "rock_kb.source_native.load_source_native_pilot_directory",
        lambda _path: base_bundle,
    )
    monkeypatch.setattr(
        "rock_kb.source_native.write_source_native_manifest",
        lambda path: (path / "manifest.json").write_text(
            "{}\n", encoding="utf-8"
        ),
    )
    monkeypatch.setattr(
        "rock_kb.source_native_migration._active_legacy_projection",
        lambda _repo_root: (
            {
                str(snapshot.source_record_id): [
                    copy.deepcopy(refreshed["legacy_items"][0])
                ]
            },
            {},
        ),
    )

    input_path = tmp_path / "refreshed.jsonl"
    output_path = tmp_path / "rebound.json"
    base_dir = tmp_path / "base"
    destination = tmp_path / "destination"
    base_dir.mkdir()
    destination.mkdir()
    write_jsonl(destination / "artifact-migrations.jsonl", [{"stale": True}])
    write_jsonl(input_path, [refreshed])
    output_path.write_text(json.dumps(reviewed) + "\n", encoding="utf-8")
    write_jsonl(
        base_dir / "legacy-migrations.jsonl",
        [existing_migration.public_dump()],
    )

    fabricated = copy.deepcopy(refreshed)
    fabricated["legacy_items"][0]["legacy_content_hash"] = "a" * 64
    rehash_migration_input(fabricated)
    fabricated_output = copy.deepcopy(reviewed)
    fabricated_output["articles"][0]["migration_input_hash"] = fabricated[
        "migration_input_hash"
    ]
    fabricated_output["articles"][0]["legacy_decisions"][0][
        "legacy_content_hash"
    ] = "a" * 64
    fabricated_input_path = tmp_path / "fabricated.jsonl"
    fabricated_output_path = tmp_path / "fabricated-output.json"
    write_jsonl(fabricated_input_path, [fabricated])
    fabricated_output_path.write_text(
        json.dumps(fabricated_output) + "\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="current legacy projection"):
        promote_rebound_source_native_legacy_migrations(
            input_path=fabricated_input_path,
            output_path=fabricated_output_path,
            destination=destination,
            base_dir=base_dir,
        )

    result = promote_rebound_source_native_legacy_migrations(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        base_dir=base_dir,
    )

    promoted = next(iter(read_jsonl(destination / "legacy-migrations.jsonl")))
    assert result["migration_count"] == 1
    assert promoted["legacy_content_hash"] == "f" * 64
    assert promoted["migration_input_hash"] == refreshed["migration_input_hash"]
    assert promoted["generation_prompt_version"] == "1.3.1"
    assert promoted["reviewer"] == "original-reviewer"
    assert not (destination / "artifact-migrations.jsonl").exists()


def test_migration_rebind_transaction_restores_previous_bundle_on_install_failure(
    monkeypatch,
    tmp_path,
):
    destination = tmp_path / "canonical"
    staging = tmp_path / ".canonical.rebind-promotion-staging-test"
    destination.mkdir()
    staging.mkdir()
    (destination / "marker.txt").write_text("previous\n", encoding="utf-8")
    (staging / "marker.txt").write_text("replacement\n", encoding="utf-8")

    original_replace = Path.replace

    def fail_staging_install(path: Path, target: Path) -> Path:
        if path == staging:
            raise OSError("simulated install failure")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_staging_install)

    with pytest.raises(OSError, match="simulated install failure"):
        _install_rebound_bundle_transactionally(
            staging=staging,
            destination=destination,
        )

    assert (destination / "marker.txt").read_text(encoding="utf-8") == (
        "previous\n"
    )
    assert not staging.exists()
    assert not (
        tmp_path / ".canonical.rebind-promotion-journal.json"
    ).exists()
    assert not list(
        tmp_path.glob(".canonical.rebind-promotion-backup-*")
    )


def test_migration_output_requires_exact_legacy_coverage():
    validated = validate_source_native_legacy_migration_output(
        migration_output(),
        inputs=[migration_input()],
    )
    assert validated.articles[0].legacy_decisions[0].disposition == "replace"

    missing = migration_output()
    missing["articles"][0]["legacy_decisions"] = []
    with pytest.raises(ValueError, match="exact input"):
        validate_source_native_legacy_migration_output(
            missing,
            inputs=[migration_input()],
        )


def test_migration_input_hash_rejects_source_and_legacy_tampering():
    source_tampered = migration_input()
    source_tampered["source_units"][0]["text"] += " Tampered."
    with pytest.raises(ValueError, match="source input hash changed"):
        validate_source_native_legacy_migration_output(
            migration_output(),
            inputs=[source_tampered],
        )

    legacy_tampered = migration_input()
    legacy_tampered["legacy_items"][0]["retrieval_text"] += " Tampered."
    with pytest.raises(ValueError, match="migration input contents changed"):
        validate_source_native_legacy_migration_output(
            migration_output(),
            inputs=[legacy_tampered],
        )


def test_existing_artifact_decisions_require_exact_hash_bound_coverage():
    input_row = migration_input()
    existing_id = "source-native:claim:rock_documentation:article-100:feature-behavior"
    input_row["existing_source_native_artifacts"] = [
        {
            "artifact_id": existing_id,
            "artifact_hash": "1" * 64,
            "artifact": migration_output()["articles"][0]["artifacts"][0],
        }
    ]
    rehash_migration_input(input_row)
    output = migration_output()
    article = output["articles"][0]
    article["source_input_hash"] = input_row["source_input_hash"]
    article["migration_input_hash"] = input_row["migration_input_hash"]

    with pytest.raises(ValueError, match="existing artifact decisions"):
        validate_source_native_legacy_migration_output(
            output,
            inputs=[input_row],
        )

    article["existing_artifact_decisions"] = [
        {
            "existing_artifact_id": existing_id,
            "existing_artifact_hash": "1" * 64,
            "disposition": "retain_identity",
            "replacement_artifact_key": "feature-behavior",
            "rationale": (
                "The emitted claim retains the same durable source-native "
                "identity and complete supported meaning."
            ),
        }
    ]
    assert (
        validate_source_native_legacy_migration_output(
            output,
            inputs=[input_row],
        )
        .articles[0]
        .existing_artifact_decisions[0]
        .disposition
        == "retain_identity"
    )

    article["existing_artifact_decisions"][0]["existing_artifact_hash"] = "2" * 64
    with pytest.raises(ValueError, match="artifact hash changed"):
        validate_source_native_legacy_migration_output(
            output,
            inputs=[input_row],
        )


def test_source_summary_can_use_companions_but_claims_cannot():
    source_summary_input = migration_input()
    reference_unit = copy.deepcopy(source_summary_input["source_units"][0])
    reference_unit["source_unit_id"] = "source-unit:reference"
    reference_unit["normalized_content_hash"] = "9" * 64
    source_summary_input["source_units"].append(reference_unit)
    source_summary_input["legacy_items"] = [
        {
            "legacy_knowledge_unit_id": "source:rock_documentation:article:100",
            "legacy_result_ids": ["source:rock_documentation:article:100"],
            "legacy_knowledge_type": "source_summary",
            "legacy_ingestion_mode": "legacy_summary_projection",
            "legacy_content_hash": "f" * 64,
            "title": "Legacy article summary",
            "retrieval_text": "The article documents the feature behavior.",
            "concept_facets": ["workflows"],
            "source_record_ids": ["rock_documentation:article:100"],
        }
    ]
    output = migration_output()
    article = output["articles"][0]
    article["unit_decisions"][0]["disposition"] = "source_summary"
    article["unit_decisions"][0]["existing_relation"] = "not_applicable"
    article["unit_decisions"].append(
        {
            "source_unit_id": "source-unit:reference",
            "disposition": "structured_reference",
            "existing_relation": "not_applicable",
            "related_existing_claim_ids": [],
            "evidence_summary": "The source supplies the compact reference.",
            "decision_reason": "The detail is best represented as a reference item.",
            "mixed_material": False,
        }
    )
    article["coverage_check"] = {
        "material_unit_count": 2,
        "captured_source_unit_ids": ["source-unit:test", "source-unit:reference"],
        "no_artifact_source_unit_ids": [],
        "omitted_source_units": [],
    }
    article["artifacts"] = [
        {
            "artifact_key": "feature-summary",
            "artifact_type": "source_summary",
            "source_unit_ids": ["source-unit:test"],
            "title": "The article documents the feature behavior.",
            "retrieval_text": "The article documents the feature behavior.",
            "independent_question": "What does the feature article cover?",
            "rationale": "The source unit establishes the article's documented scope.",
            "concept_ids": ["workflows"],
            "claim_type": None,
            "evidence_class": None,
            "confidence": "high",
            "payload": {"summary": "The article documents the feature behavior."},
        },
        {
            "artifact_key": "feature-reference",
            "artifact_type": "structured_reference",
            "source_unit_ids": ["source-unit:reference"],
            "title": "The feature has a documented behavior reference.",
            "retrieval_text": "Feature behavior reference.",
            "independent_question": "Where is the feature behavior summarized?",
            "rationale": "The source unit directly supports this compact reference.",
            "concept_ids": ["workflows"],
            "claim_type": None,
            "evidence_class": None,
            "confidence": "high",
            "temporal_status": "release_sensitive",
            "payload": {
                "summary": "The feature performs the documented behavior.",
                "reference_items": [
                    {
                        "label": "Behavior",
                        "detail": "The feature performs the documented behavior.",
                        "value_status": "documented_behavior",
                        "needs_verification": False,
                    }
                ],
            },
        },
    ]
    article["legacy_decisions"] = [
        {
            "legacy_knowledge_unit_id": "source:rock_documentation:article:100",
            "legacy_content_hash": "f" * 64,
            "disposition": "replace",
            "coverage": "full",
            "replacement_artifact_key": "feature-summary",
            "supporting_replacement_artifact_keys": ["feature-reference"],
            "rationale": (
                "The source summary preserves article scope and the companion "
                "preserves its independently retrievable operational detail."
            ),
        }
    ]
    rehash_migration_input(source_summary_input)
    article["source_input_hash"] = source_summary_input["source_input_hash"]
    article["migration_input_hash"] = source_summary_input["migration_input_hash"]
    validated = validate_source_native_legacy_migration_output(
        output,
        inputs=[source_summary_input],
    )
    assert validated.articles[0].legacy_decisions[
        0
    ].supporting_replacement_artifact_keys == ["feature-reference"]

    claim_input = migration_input()
    claim_reference_unit = copy.deepcopy(claim_input["source_units"][0])
    claim_reference_unit["source_unit_id"] = "source-unit:reference"
    claim_reference_unit["normalized_content_hash"] = "9" * 64
    claim_input["source_units"].append(claim_reference_unit)
    rehash_migration_input(claim_input)
    claim_with_companion = migration_output()
    claim_article = claim_with_companion["articles"][0]
    claim_article["source_input_hash"] = claim_input["source_input_hash"]
    claim_article["migration_input_hash"] = claim_input["migration_input_hash"]
    claim_article["unit_decisions"].append(
        {
            "source_unit_id": "source-unit:reference",
            "disposition": "claim",
            "existing_relation": "novel",
            "related_existing_claim_ids": [],
            "evidence_summary": "The source states another supported behavior.",
            "decision_reason": "The behavior is independently answerable.",
            "mixed_material": False,
        }
    )
    companion_claim = copy.deepcopy(claim_article["artifacts"][0])
    companion_claim["artifact_key"] = "feature-companion"
    companion_claim["source_unit_ids"] = ["source-unit:reference"]
    companion_claim["title"] = "The feature also performs a second behavior."
    companion_claim["retrieval_text"] = (
        "The feature also performs a second documented behavior."
    )
    companion_claim["independent_question"] = (
        "What second behavior does the feature perform?"
    )
    companion_claim["payload"] = {
        "summary": "The feature also performs a second documented behavior."
    }
    claim_article["artifacts"].append(companion_claim)
    claim_article["coverage_check"] = {
        "material_unit_count": 2,
        "captured_source_unit_ids": ["source-unit:test", "source-unit:reference"],
        "no_artifact_source_unit_ids": [],
        "omitted_source_units": [],
    }
    claim_with_companion["articles"][0]["legacy_decisions"][0][
        "supporting_replacement_artifact_keys"
    ] = ["feature-companion"]
    with pytest.raises(ValueError, match="legacy claims cannot use"):
        validate_source_native_legacy_migration_output(
            claim_with_companion,
            inputs=[claim_input],
        )


def test_source_summary_can_use_typed_primary_without_synthetic_summary():
    input_row = migration_input()
    input_row["legacy_items"] = [
        {
            "legacy_knowledge_unit_id": "source:rock_documentation:article:100",
            "legacy_result_ids": ["source:rock_documentation:article:100"],
            "legacy_knowledge_type": "source_summary",
            "legacy_ingestion_mode": "legacy_summary_projection",
            "legacy_content_hash": "f" * 64,
            "title": "Legacy article summary",
            "retrieval_text": "The article documents the feature behavior.",
            "concept_facets": ["workflows"],
            "source_record_ids": ["rock_documentation:article:100"],
        }
    ]
    rehash_migration_input(input_row)
    output = migration_output()
    article = output["articles"][0]
    article["source_input_hash"] = input_row["source_input_hash"]
    article["migration_input_hash"] = input_row["migration_input_hash"]
    article["unit_decisions"][0].update(
        {
            "disposition": "structured_reference",
            "existing_relation": "not_applicable",
        }
    )
    article["artifacts"] = [
        {
            "artifact_key": "feature-behavior-reference",
            "artifact_type": "structured_reference",
            "source_unit_ids": ["source-unit:test"],
            "title": "The feature has a documented behavior reference.",
            "retrieval_text": (
                "The feature behavior reference states that the feature performs "
                "the documented behavior."
            ),
            "independent_question": (
                "What behavior does the feature reference document?"
            ),
            "rationale": (
                "The source unit is a bounded behavior reference and completely "
                "preserves the useful legacy landing value."
            ),
            "concept_ids": ["workflows"],
            "claim_type": None,
            "evidence_class": None,
            "confidence": "high",
            "temporal_status": "release_sensitive",
            "payload": {
                "summary": "The feature performs the documented behavior.",
                "reference_items": [
                    {
                        "label": "Behavior",
                        "detail": "The feature performs the documented behavior.",
                        "value_status": "documented_behavior",
                        "needs_verification": False,
                    }
                ],
            },
        }
    ]
    article["legacy_decisions"] = [
        {
            "legacy_knowledge_unit_id": "source:rock_documentation:article:100",
            "legacy_content_hash": "f" * 64,
            "disposition": "replace",
            "coverage": "full",
            "replacement_artifact_key": "feature-behavior-reference",
            "supporting_replacement_artifact_keys": [],
            "rationale": (
                "The structured reference independently preserves the useful "
                "scope and answer value of the legacy source summary."
            ),
        }
    ]

    validated = validate_source_native_legacy_migration_output(
        output,
        inputs=[input_row],
    )

    decision = validated.articles[0].legacy_decisions[0]
    assert decision.disposition == "replace"
    assert decision.replacement_artifact_key == "feature-behavior-reference"
    assert validated.articles[0].artifacts[0].artifact_type == "structured_reference"


@pytest.mark.parametrize(
    ("legacy_kind", "replacement_type", "legacy_ingestion_mode"),
    [
        ("claim", "claim", "legacy_reviewed_claim_projection"),
        ("source_summary", "structured_reference", "legacy_summary_projection"),
    ],
)
def test_canonical_migration_replaces_legacy_row_and_preserves_aliases(
    monkeypatch,
    legacy_kind,
    replacement_type,
    legacy_ingestion_mode,
):
    legacy_source_url = "https://community.rockrms.com/documentation/test"
    legacy_source_record_id = canonical_record_id(
        "rock_documentation",
        legacy_source_url,
    )
    if legacy_kind == "claim":
        search_row = {
            "id": "claim:claim:legacy",
            "kind": "claim",
            "title": "Legacy behavior",
            "body": "The feature performs the documented behavior.",
            "concepts": ["workflows"],
            "authority_tier": "official",
            "claim_tier": "answer_pack_approved",
            "source_id": "rock_documentation",
            "payload": {
                "schema": "rock-kb-claim-v1",
                "claim_id": "claim:legacy",
                "claim": "The feature performs the documented behavior.",
                "claim_type": "behavior",
                "concept_ids": ["workflows"],
                "source_record_ids": [legacy_source_record_id],
                "source_refs": [
                    {
                        "source_id": "rock_documentation",
                        "title": "Test Article",
                        "url": legacy_source_url,
                    }
                ],
                "authority_tier": "official",
                "confidence": "high",
                "review_status": "approved_for_public_distillation",
                "license_status": "cite_and_summarize_only",
                "public_publish_mode": "public_cite_and_summarize_only",
                "safe_evidence_hash": "1" * 64,
                "needs_live_verification": False,
                "created_at": "2026-08-04T00:00:00+00:00",
                "updated_at": "2026-08-04T00:00:00+00:00",
                "derived_from": {"type": "test"},
                "community_derived": False,
                "primary_concept_id": "workflows",
                "concept_assignment_reason": "test_fixture",
                "answer_candidate": True,
                "operational_priority": 100,
                "requires_live_instance": False,
                "claim_tier": "answer_pack_approved",
            },
        }
    else:
        search_row = {
            "id": "source:rock_documentation:article:100",
            "kind": "source_summary",
            "title": "Test Article",
            "body": "The article documents the feature behavior.",
            "url": legacy_source_url,
            "concepts": ["workflows"],
            "topics": [],
            "authority_tier": "official",
            "source_id": "rock_documentation",
            "payload": {
                "schema": "rock-kb-public-source-summary-v1",
                "source_id": "rock_documentation",
                "source_record_id": "rock_documentation:article:100",
                "source_title": "Test Article",
                "source_url": legacy_source_url,
                "summary": "The article documents the feature behavior.",
                "content_hash": "1" * 64,
                "retrieved_at": "2026-08-04T00:00:00+00:00",
            },
        }
    legacy_bundle, _summary = build_canonical_knowledge_bundle(
        search_rows=[search_row],
        distilled_claims=[],
        include_source_native_pilot=False,
    )
    legacy = legacy_bundle.knowledge_units[0]
    snapshot = SourceSnapshot(
        schema="rock-kb-source-snapshot-v2",
        source_snapshot_id="source-snapshot:test",
        source_id="rock_documentation",
        source_record_id="rock_documentation:article:100",
        source_work_id="documentation-article:100",
        canonical_url="https://community.rockrms.com/documentation/test",
        title="Test Article",
        content_hash="c" * 64,
        normalized_content_hash="c" * 64,
        authority_tier="official",
        public_policy="cite_and_summarize_only",
        derivation={"documentation_article_id": 100},
    )
    unit = SourceUnit(
        schema="rock-kb-source-unit-v2",
        source_unit_id="source-unit:test",
        source_snapshot_id=snapshot.source_snapshot_id,
        unit_kind="paragraph",
        locator=SourceLocator(
            kind="paragraph",
            value="Overview / paragraph-1",
            url=snapshot.canonical_url,
        ),
        public_summary="The source states the documented behavior.",
        normalized_content_hash="d" * 64,
        required_public_handling="cite_and_summarize_only",
    )
    artifact_payload = (
        {"summary": "The feature performs the documented behavior."}
        if replacement_type == "claim"
        else {
            "summary": "The feature performs the documented behavior.",
            "reference_items": [
                {
                    "label": "Behavior",
                    "detail": "The feature performs the documented behavior.",
                    "value_status": "documented_behavior",
                    "needs_verification": False,
                }
            ],
        }
    )
    artifact = SourceNativeArtifactCandidate(
        artifact_key="feature-behavior",
        artifact_type=replacement_type,
        source_unit_ids=[unit.source_unit_id],
        title="The feature performs the documented behavior.",
        retrieval_text="The feature performs the documented behavior.",
        independent_question="What behavior does the feature perform?",
        rationale="The source unit directly states this behavior.",
        concept_ids=["workflows"],
        claim_type="behavior" if replacement_type == "claim" else None,
        evidence_class="current_behavior" if replacement_type == "claim" else None,
        temporal_status=(
            "release_sensitive" if replacement_type == "structured_reference" else "current"
        ),
        confidence="high",
        payload=artifact_payload,
    )
    reviewed = ReviewedSourceNativeArtifact(
        schema="rock-kb-reviewed-source-native-artifact-v1",
        artifact_id=(
            f"source-native:{replacement_type}:rock_documentation:article-100:"
            "feature-behavior"
        ),
        source_candidate_id="source-native-candidate:test",
        generation_activity_id="generation:test",
        artifact=artifact,
        review_state="reviewer_approved",
        reviewer="test-reviewer",
        reviewed_at="2026-08-04T00:00:00+00:00",
        source_input_hash="a" * 64,
    )
    migration = ReviewedSourceNativeLegacyMigration(
        schema="rock-kb-reviewed-source-native-legacy-migration-v1",
        migration_id="source-native-legacy-migration:test",
        source_record_id="rock_documentation:article:100",
        source_snapshot_id=snapshot.source_snapshot_id,
        source_snapshot_content_hash=snapshot.content_hash,
        legacy_knowledge_unit_id=legacy.knowledge_unit_id,
        legacy_result_ids=sorted({legacy.knowledge_unit_id, *legacy.legacy_ids}),
        legacy_knowledge_type=legacy_kind,
        legacy_ingestion_mode=legacy_ingestion_mode,
        legacy_content_hash=legacy.content_hash,
        migration_input_hash="b" * 64,
        replacement_artifact_id=reviewed.artifact_id,
        replacement_artifact_hash=public_record_hash(reviewed.artifact),
        rationale=(
            "The replacement preserves the complete supported behavior in one "
            "source-native artifact."
        ),
        generation_model="test-model",
        generation_prompt_id="source-native-legacy-migration-v1",
        generation_prompt_version="1.2.0",
        generated_article_hash="2" * 64,
        reviewed_article_hash="3" * 64,
        review_correction_count=0,
        reviewer="test-reviewer",
        reviewed_at="2026-08-04T00:00:00+00:00",
    )
    artifact_migration = ReviewedSourceNativeArtifactMigration(
        schema="rock-kb-reviewed-source-native-artifact-migration-v1",
        migration_id="source-native-artifact-migration:test",
        source_record_id="rock_documentation:article:100",
        source_snapshot_id=snapshot.source_snapshot_id,
        source_snapshot_content_hash=snapshot.content_hash,
        prior_artifact_id=(
            f"source-native:{replacement_type}:rock_documentation:article-100:old-key"
        ),
        prior_artifact_hash="4" * 64,
        replacement_artifact_id=reviewed.artifact_id,
        replacement_artifact_hash=public_record_hash(reviewed.artifact),
        migration_input_hash="b" * 64,
        rationale=(
            "The reviewed replacement fully supersedes the earlier source-native "
            "artifact while preserving its exact public lookup ID."
        ),
        generation_model="test-model",
        generation_prompt_id="source-native-legacy-migration-v1",
        generation_prompt_version="1.2.0",
        generated_article_hash="2" * 64,
        reviewed_article_hash="3" * 64,
        review_correction_count=0,
        reviewer="test-reviewer",
        reviewed_at="2026-08-04T00:00:00+00:00",
    )
    source_native = {
        "source_snapshots": [snapshot],
        "source_units": [unit],
        "generation_activities": [
            GenerationActivity(
                schema="rock-kb-generation-activity-v1",
                generation_activity_id="generation:test",
                activity_type="source_distillation",
                model="test-model",
                prompt_id="source-native-legacy-migration-v1",
                prompt_version="1.0.0",
                source_snapshot_ids=[snapshot.source_snapshot_id],
                source_unit_ids=[unit.source_unit_id],
            )
        ],
        "reviewed_artifacts": [reviewed],
        "relationships": [],
        "verification_queue": [],
        "verification_resolutions": [],
        "legacy_migrations": [migration],
        "artifact_migrations": [artifact_migration],
    }
    monkeypatch.setattr(
        "rock_kb.canonical_knowledge.load_source_native_pilot",
        lambda _repo_root: source_native,
    )

    bundle, summary = build_canonical_knowledge_bundle(
        search_rows=[search_row],
        distilled_claims=[],
        identity_registry=[row.public_dump() for row in legacy_bundle.identities],
        include_source_native_pilot=True,
    )

    assert len(bundle.knowledge_units) == 1
    replacement = bundle.knowledge_units[0]
    assert replacement.knowledge_unit_id == reviewed.artifact_id
    assert replacement.ingestion_mode == "source_native_distillation"
    assert set(migration.legacy_result_ids) <= set(replacement.legacy_ids)
    assert artifact_migration.prior_artifact_id in replacement.legacy_ids
    assert summary["input"]["reviewed_legacy_migrations"] == 1
    assert summary["input"]["reviewed_source_native_artifact_migrations"] == 1
    assert summary["output"]["ingestion_modes"].get(legacy_ingestion_mode, 0) == 0
    identity_migration = next(
        row
        for row in bundle.identity_migrations
        if row.from_knowledge_unit_id == legacy.knowledge_unit_id
    )
    assert identity_migration.to_knowledge_unit_id == reviewed.artifact_id
    assert identity_migration.review_state == "reviewer_approved"

    stale_source_native = copy.deepcopy(source_native)
    stale_source_native["legacy_migrations"][0] = migration.model_copy(
        update={"legacy_content_hash": "f" * 64}
    )
    monkeypatch.setattr(
        "rock_kb.canonical_knowledge.load_source_native_pilot",
        lambda _repo_root: stale_source_native,
    )
    with pytest.raises(ValueError, match="content hash changed"):
        build_canonical_knowledge_bundle(
            search_rows=[search_row],
            distilled_claims=[],
            identity_registry=[row.public_dump() for row in legacy_bundle.identities],
            include_source_native_pilot=True,
        )

    if legacy_kind == "claim":
        unrelated_source_native = copy.deepcopy(source_native)
        unrelated_source_native["source_snapshots"][0] = snapshot.model_copy(
            update={
                "canonical_url": (
                    "https://community.rockrms.com/documentation/different-article"
                )
            }
        )
        monkeypatch.setattr(
            "rock_kb.canonical_knowledge.load_source_native_pilot",
            lambda _repo_root: unrelated_source_native,
        )
        with pytest.raises(ValueError, match="source record changed"):
            build_canonical_knowledge_bundle(
                search_rows=[search_row],
                distilled_claims=[],
                identity_registry=[
                    row.public_dump() for row in legacy_bundle.identities
                ],
                include_source_native_pilot=True,
            )
