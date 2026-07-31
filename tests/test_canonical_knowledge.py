from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from rock_kb.canonical_knowledge import (
    build_canonical_knowledge_bundle,
    build_public_identity_baseline,
    merge_identity_registry_rows,
    write_canonical_knowledge_shadow,
)
from rock_kb.extract import sha256_text
from rock_kb.jsonl import read_jsonl
from rock_kb.schemas import (
    CanonicalKnowledgeBundle,
    EvidenceLink,
    KnowledgeIdentity,
    KnowledgeUnit,
    SourceLocator,
    SourceSnapshot,
    SourceUnit,
)
from rock_kb.service_projection import claim_search_rows


DIRECT_DATABASE_TEXT = (
    "AI integrations should not receive unrestricted direct database access. "
    "Route data operations through managed Rock code that enforces authorization and business rules, "
    "and treat model-generated SQL as unsafe for general-purpose operational access."
)


def test_direct_database_claim_collapses_concept_copies_and_media_mirrors():
    claim_rows = [row for row in claim_search_rows() if row.get("body") == DIRECT_DATABASE_TEXT]
    distilled_rows = [
        row
        for row in read_jsonl(Path("agent/distilled-claims.jsonl"))
        if row.get("distilled_claim") == DIRECT_DATABASE_TEXT
    ]

    bundle, summary = build_canonical_knowledge_bundle(
        search_rows=claim_rows,
        distilled_claims=distilled_rows,
    )

    assert len(bundle.knowledge_units) == 1
    item = bundle.knowledge_units[0]
    assert item.concept_facets == ["ai-agents-automation", "api-integrations", "security-permissions"]
    assert len([value for value in item.legacy_ids if value.startswith("distilled-claim:")]) == 3
    assert len(item.payload["approved_claims"]) == 2
    assert len(item.source_unit_ids) == 2
    assert item.source_work_ids == ["media-work:rockcast:episode:216"]
    assert len(bundle.relationships) == 1
    assert bundle.relationships[0].relation == "mirrors"
    assert summary["regressions"]["direct_database_access"]["independent_source_work_count"] == 1


def test_source_specific_payload_is_preserved_inside_common_envelope(tmp_path):
    commit_sha = "a" * 40
    recipe_payload = {
        "schema": "rock-kb-recipe-v1",
        "recipe_id": "example:test-recipe",
        "review_status": "community_reviewed",
        "implementation": {
            "commit_sha": commit_sha,
            "repository_url": "https://github.com/example/recipes",
            "source_path": "recipes/test",
        },
        "custom_recipe_field": {"kept": True},
    }
    search_row = {
        "id": "recipe:example:test-recipe",
        "kind": "recipe",
        "title": "Test Recipe",
        "body": "A bounded recipe body.",
        "url": f"https://github.com/example/recipes/tree/{commit_sha}/recipes/test",
        "concepts": ["workflows"],
        "topics": [],
        "authority_tier": "community-reviewed",
        "claim_tier": "answer_pack_approved",
        "source_id": "example",
        "payload": recipe_payload,
    }

    bundle, _summary = build_canonical_knowledge_bundle(search_rows=[search_row], distilled_claims=[])
    result = write_canonical_knowledge_shadow(
        tmp_path,
        search_rows=[search_row],
        distilled_claims=[],
    )

    assert bundle.knowledge_units[0].payload == recipe_payload
    assert bundle.knowledge_units[0].knowledge_type == "recipe"
    assert bundle.knowledge_units[0].knowledge_unit_id == "recipe:example:test-recipe"
    prior_hashed_id = (
        "knowledge:recipe:"
        + sha256_text("recipe:example:test-recipe")[:24]
    )
    assert prior_hashed_id in bundle.knowledge_units[0].legacy_ids
    assert bundle.identity_migrations[0].from_knowledge_unit_id == prior_hashed_id
    assert bundle.source_snapshots[0].immutable is True
    assert result["public_retrieval_changed"] is False
    written = json.loads((tmp_path / "knowledge-units.jsonl").read_text(encoding="utf-8"))
    assert written["payload"]["custom_recipe_field"] == {"kept": True}


def test_existing_knowledge_projection_cannot_be_primary_evidence():
    snapshot = SourceSnapshot(
        schema="rock-kb-source-snapshot-v1",
        source_snapshot_id="snapshot:test",
        source_id="test",
        source_record_id="record:test",
        authority_tier="community-reviewed",
        public_policy="existing_public_artifact",
    )
    source_unit = SourceUnit(
        schema="rock-kb-source-unit-v1",
        source_unit_id="unit:test",
        source_snapshot_id="snapshot:test",
        unit_kind="existing_knowledge_projection",
        locator=SourceLocator(kind="record", value="existing:test"),
        required_public_handling="existing_public_artifact",
    )
    knowledge = KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="knowledge:test",
        knowledge_type="claim",
        title="Test",
        retrieval_text="Test knowledge.",
        source_unit_ids=["unit:test"],
        payload={},
        content_hash="0" * 64,
    )
    evidence = EvidenceLink(
        schema="rock-kb-evidence-link-v1",
        evidence_link_id="evidence:test",
        knowledge_unit_id="knowledge:test",
        source_unit_id="unit:test",
        evidence_summary="Existing projection repeats this statement.",
        authority_tier="community-reviewed",
    )

    with pytest.raises(ValidationError, match="cannot be used as primary evidence"):
        CanonicalKnowledgeBundle(
            schema="rock-kb-canonical-knowledge-bundle-v1",
            source_snapshots=[snapshot],
            source_units=[source_unit],
            knowledge_units=[knowledge],
            evidence_links=[evidence],
        )


def test_public_bundle_dump_excludes_private_source_text():
    snapshot = SourceSnapshot(
        schema="rock-kb-source-snapshot-v1",
        source_snapshot_id="snapshot:test",
        source_id="test",
        source_record_id="record:test",
        authority_tier="official",
        public_policy="cite_and_summarize_only",
    )
    source_unit = SourceUnit(
        schema="rock-kb-source-unit-v1",
        source_unit_id="unit:test",
        source_snapshot_id="snapshot:test",
        unit_kind="media_segment",
        locator=SourceLocator(kind="timestamp", value="01:00", timestamp_seconds=60),
        text="Private transcript text.",
        public_summary="Reviewed paraphrase.",
        required_public_handling="private_evidence_only",
    )

    public = CanonicalKnowledgeBundle(
        schema="rock-kb-canonical-knowledge-bundle-v1",
        source_snapshots=[snapshot],
        source_units=[source_unit],
    ).public_dump()

    assert "text" not in public["source_units"][0]


def test_registry_identity_survives_claim_wording_change():
    original = dict(claim_search_rows()[0])
    first, _summary = build_canonical_knowledge_bundle(
        search_rows=[original],
        distilled_claims=[],
    )
    changed = {
        **original,
        "title": "Updated wording",
        "body": f"{original['body']} This reviewed wording changed.",
        "payload": {
            **original["payload"],
            "claim": f"{original['payload']['claim']} This reviewed wording changed.",
        },
    }

    second, _summary = build_canonical_knowledge_bundle(
        search_rows=[changed],
        distilled_claims=[],
        identity_registry=[row.public_dump() for row in first.identities],
        identity_migrations=[
            row.public_dump() for row in first.identity_migrations
        ],
        previous_knowledge_units=[
            row.public_dump() for row in first.knowledge_units
        ],
    )

    assert (
        second.knowledge_units[0].knowledge_unit_id
        == first.knowledge_units[0].knowledge_unit_id
    )
    assert second.identities[0].identity_key == first.identities[0].identity_key
    assert second.identities[0].identity_basis == "legacy_anchor"
    assert len(second.identity_migrations) == 2


def test_distilled_claims_sharing_support_do_not_share_identity():
    distilled = [
        {
            "id": "distilled-claim:first",
            "distilled_claim": "First distinct reviewed conclusion.",
            "claim_type": "operational_guidance",
            "concept_id": "workflows",
            "supporting_claim_ids": ["claim:shared-source"],
            "distillation_status": "generated_needs_reviewer_approval",
        },
        {
            "id": "distilled-claim:second",
            "distilled_claim": "Second distinct reviewed conclusion.",
            "claim_type": "operational_guidance",
            "concept_id": "workflows",
            "supporting_claim_ids": ["claim:shared-source"],
            "distillation_status": "generated_needs_reviewer_approval",
        },
    ]

    bundle, _summary = build_canonical_knowledge_bundle(
        search_rows=[],
        distilled_claims=distilled,
    )

    assert len(bundle.knowledge_units) == 2
    assert len({row.knowledge_unit_id for row in bundle.knowledge_units}) == 2
    assert all(
        "claim:shared-source" not in row.aliases
        for row in bundle.identities
    )


def test_retired_shadow_identity_migration_is_not_carried_into_current_bundle():
    row = {
        "id": "recipe:example:current",
        "kind": "recipe",
        "title": "Current Recipe",
        "body": "Current recipe body.",
        "concepts": ["workflows"],
        "authority_tier": "community-reviewed",
        "claim_tier": "answer_pack_approved",
        "source_id": "example",
        "payload": {
            "schema": "rock-kb-recipe-v1",
            "recipe_id": "example:current",
            "review_status": "community_reviewed",
        },
    }
    stale_migration = {
        "schema": "rock-kb-knowledge-identity-migration-v1",
        "migration_id": "identity-migration:retired",
        "from_knowledge_unit_id": "knowledge:claim:old-content-addressed",
        "to_knowledge_unit_id": "knowledge:claim:retired-registry-identity",
        "migration_type": "content_addressed_to_registry",
        "reason": "This unpublished shadow-only target was retired.",
        "matched_aliases": [],
    }

    bundle, _summary = build_canonical_knowledge_bundle(
        search_rows=[row],
        distilled_claims=[],
        identity_migrations=[stale_migration],
    )

    assert bundle.identity_migrations
    assert all(
        migration.migration_id != "identity-migration:retired"
        for migration in bundle.identity_migrations
    )


def test_retired_shadow_identity_migration_is_archived(tmp_path):
    stale_migration = {
        "schema": "rock-kb-knowledge-identity-migration-v1",
        "migration_id": "identity-migration:retired",
        "from_knowledge_unit_id": "knowledge:claim:old-content-addressed",
        "to_knowledge_unit_id": "knowledge:claim:retired-registry-identity",
        "migration_type": "content_addressed_to_registry",
        "reason": "This unpublished shadow-only target was retired.",
        "matched_aliases": [],
    }
    (tmp_path / "identity-migrations.jsonl").write_text(
        json.dumps(stale_migration) + "\n",
        encoding="utf-8",
    )
    row = {
        "id": "recipe:example:current",
        "kind": "recipe",
        "title": "Current Recipe",
        "body": "Current recipe body.",
        "concepts": ["workflows"],
        "authority_tier": "community-reviewed",
        "claim_tier": "answer_pack_approved",
        "source_id": "example",
        "payload": {
            "schema": "rock-kb-recipe-v1",
            "recipe_id": "example:current",
            "review_status": "community_reviewed",
        },
    }

    result = write_canonical_knowledge_shadow(
        tmp_path,
        search_rows=[row],
        distilled_claims=[],
    )

    active = list(read_jsonl(tmp_path / "identity-migrations.jsonl"))
    retired = list(read_jsonl(tmp_path / "retired-identity-migrations.jsonl"))
    assert all(
        migration["migration_id"] != "identity-migration:retired"
        for migration in active
    )
    assert [migration["migration_id"] for migration in retired] == [
        "identity-migration:retired"
    ]
    assert result["output"]["retired_identity_migrations"] == 1


def test_identity_registry_and_migrations_are_byte_stable_on_rerun(tmp_path):
    row = {
        "id": "recipe:example:stable",
        "kind": "recipe",
        "title": "Stable Recipe",
        "body": "Stable recipe body.",
        "concepts": ["workflows"],
        "authority_tier": "community-reviewed",
        "claim_tier": "answer_pack_approved",
        "source_id": "example",
        "payload": {
            "schema": "rock-kb-recipe-v1",
            "recipe_id": "example:stable",
            "review_status": "community_reviewed",
        },
    }
    write_canonical_knowledge_shadow(
        tmp_path,
        search_rows=[row],
        distilled_claims=[],
    )
    first_registry = (tmp_path / "identity-registry.jsonl").read_bytes()
    first_migrations = (tmp_path / "identity-migrations.jsonl").read_bytes()

    write_canonical_knowledge_shadow(
        tmp_path,
        search_rows=[row],
        distilled_claims=[],
    )

    assert (tmp_path / "identity-registry.jsonl").read_bytes() == first_registry
    assert (
        tmp_path / "identity-migrations.jsonl"
    ).read_bytes() == first_migrations


def test_public_identity_baseline_excludes_unpublished_pilot_aliases():
    unit = KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="knowledge:claim:stable",
        knowledge_type="claim",
        title="Stable claim",
        retrieval_text="Stable claim.",
        legacy_ids=[
            "claim:claim:public",
            "claim:claim:public:workflows",
            "knowledge:claim:unpublished-pilot",
        ],
        payload={},
        content_hash="0" * 64,
    )
    identity = KnowledgeIdentity(
        schema="rock-kb-knowledge-identity-v1",
        knowledge_unit_id=unit.knowledge_unit_id,
        knowledge_type="claim",
        identity_key="claim_alias:claim:claim:public",
        identity_basis="legacy_anchor",
        aliases=unit.legacy_ids,
        content_fingerprint="1" * 64,
    )

    registry, aliases, metadata = build_public_identity_baseline(
        identities=[identity],
        knowledge_units=[unit],
        public_search_rows=[
            {
                "id": "claim:claim:public",
                "kind": "claim",
                "legacy_ids": ["claim:claim:public:workflows"],
            }
        ],
    )

    assert registry[0].aliases == [
        "claim:claim:public",
        "claim:claim:public:workflows",
    ]
    assert {
        row.alias_id for row in aliases
    } == {
        "claim:claim:public",
        "claim:claim:public:workflows",
    }
    assert metadata["existing_result_id_alias_count"] == 1
    assert metadata["existing_legacy_id_alias_count"] == 1


def test_persistent_and_private_identity_registries_merge_alias_history():
    base = {
        "schema": "rock-kb-knowledge-identity-v1",
        "knowledge_unit_id": "knowledge:claim:stable",
        "knowledge_type": "claim",
        "identity_key": "claim_alias:public",
        "identity_basis": "legacy_anchor",
        "aliases": ["claim:claim:public"],
        "content_fingerprint": "0" * 64,
    }
    private = {
        **base,
        "aliases": [
            "claim:claim:public",
            "knowledge:claim:unpublished-pilot",
        ],
        "content_fingerprint": "1" * 64,
    }

    merged = merge_identity_registry_rows([base], [private])

    assert merged[0]["aliases"] == [
        "claim:claim:public",
        "knowledge:claim:unpublished-pilot",
    ]
    assert merged[0]["content_fingerprint"] == "1" * 64
