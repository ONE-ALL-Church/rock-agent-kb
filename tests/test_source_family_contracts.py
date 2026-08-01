from __future__ import annotations

import json

import pytest

from rock_kb.source_family_contracts import (
    GENERATED_KNOWLEDGE_CONTRACTS,
    SOURCE_FAMILY_CONTRACTS,
    SOURCE_FAMILY_CONTRACT_MANIFEST_PATH,
    source_family_contract,
    source_family_contract_manifest,
    source_family_contract_summary,
    write_source_family_contract_manifest,
)


def test_every_non_claim_canonical_family_has_an_explicit_contract():
    assert set(SOURCE_FAMILY_CONTRACTS) == {
        "community_contribution",
        "recipe",
        "source_summary",
        "model_map",
        "lava_context",
        "rock_issue",
        "rock_idea",
    }
    assert source_family_contract(
        "rock_issue",
        {
            "schema": "rock-kb-rock-issue-v1",
            "updated_at": "2026-07-31T00:00:00Z",
            "source_content_hash": "a" * 64,
        },
    ).ingestion_mode == "official_api_derived_record"
    assert source_family_contract(
        "lava_context",
        {
            "schema": "rock-kb-lava-context-v3",
            "source_commit": "a" * 40,
            "last_seen_version": "v19",
        },
    ).ingestion_mode == "source_code_derived_record"


def test_source_family_contract_rejects_schema_drift():
    with pytest.raises(ValueError, match="is not allowed"):
        source_family_contract(
            "rock_issue",
            {
                "schema": "rock-kb-rock-issue-v2-unreviewed",
                "updated_at": "2026-07-31T00:00:00Z",
                "source_content_hash": "a" * 64,
            },
        )


def test_source_family_contract_rejects_missing_required_freshness():
    with pytest.raises(ValueError, match="identity.rock_version"):
        source_family_contract(
            "model_map",
            {
                "schema": "rock-kb-model-map-search-payload-v1",
                "identity": {"track": "stable"},
            },
        )


def test_source_family_contract_summary_reports_coverage_and_errors():
    summary = source_family_contract_summary(
        [
            {
                "id": "rock_issue:1",
                "kind": "rock_issue",
                "payload": {
                    "schema": "rock-kb-rock-issue-v1",
                    "updated_at": "2026-07-31T00:00:00Z",
                    "source_content_hash": "a" * 64,
                },
            },
            {
                "id": "lava_context:test",
                "kind": "lava_context",
                "payload": {
                    "schema": "rock-kb-lava-context-v3",
                    "source_commit": "a" * 40,
                    "last_seen_version": "v19",
                },
            },
        ]
    )

    assert summary["status"] == "ok"
    assert summary["row_count"] == 2
    assert summary["errors"] == []


def test_manifest_distinguishes_generated_and_deterministic_typed_sources():
    manifest = source_family_contract_manifest()

    assert manifest["default_retrieval_projection"] == "legacy"
    assert manifest["canonical_projection_state"] == "shadow_and_opt_in_canary"
    assert set(GENERATED_KNOWLEDGE_CONTRACTS) == {
        "approved_claim",
        "official_documentation",
        "reviewed_cross_source",
    }
    generated = {
        row["source_family"]: row
        for row in manifest["generated_knowledge_contracts"]
    }
    assert (
        generated["official_documentation"]["ingestion_mode"]
        == "source_native_distillation"
    )
    typed = {
        row["knowledge_type"]: row
        for row in manifest["typed_record_contracts"]
    }
    assert typed["rock_issue"]["ingestion_mode"] == "official_api_derived_record"
    assert typed["source_summary"]["ingestion_mode"] == "legacy_summary_projection"


def test_contract_manifest_writer_is_deterministic(tmp_path):
    destination = tmp_path / "source-family-contracts.json"

    first = write_source_family_contract_manifest(destination)
    first_text = destination.read_text(encoding="utf-8")
    second = write_source_family_contract_manifest(destination)

    assert first["status"] == "ok"
    assert second["status"] == "ok"
    assert destination.read_text(encoding="utf-8") == first_text


def test_tracked_contract_manifest_matches_the_reviewed_registry():
    assert json.loads(
        SOURCE_FAMILY_CONTRACT_MANIFEST_PATH.read_text(encoding="utf-8")
    ) == source_family_contract_manifest()
