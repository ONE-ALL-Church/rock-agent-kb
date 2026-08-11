import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from rock_kb.concepts import Concept
import rock_kb.source_native_priority as source_native_priority_module
from rock_kb.source_native_priority import (
    add_source_native_location_aliases,
    bounded_dashboard_signals,
    infer_concept_ids,
    reconcile_legacy_source_record_ids,
    score_priority_row,
    source_record_freshness,
)
from rock_kb.sources import Source


def source(cadence: str = "weekly") -> Source:
    return Source(
        id="rock_documentation",
        name="Rock Manuals",
        kind="rock_documentation",
        root_url="https://community.rockrms.com/documentation",
        description="Official docs",
        owner="Spark",
        license_status="public_rights_reserved",
        allowed_extraction_mode="cite_and_summarize",
        private_storage=True,
        public_publish_mode="public_cite_and_summarize_only",
        allowed_excerpt_chars=800,
        requires_human_review=True,
        refresh_cadence=cadence,
        extraction_tier=1,
        preferred_tooling=["rockumentation_block_action"],
        topics=["admin"],
        raw={},
    )


def priority_row(**overrides):
    row = {
        "legacy_claim_count": 0,
        "legacy_source_summary_count": 1,
        "verification_debt_count": 0,
        "existing_source_native_artifact_count": 0,
        "exact_evaluation_case_count": 0,
        "external_signal_count": 0,
        "concept_ids": ["workflows"],
        "freshness": {"status": "current"},
    }
    row.update(overrides)
    return row


def test_claim_and_exact_evaluation_demand_outrank_summary_only_source():
    summary = score_priority_row(priority_row())
    claim = score_priority_row(
        priority_row(
            legacy_claim_count=2,
            verification_debt_count=1,
            exact_evaluation_case_count=1,
        )
    )

    assert claim["priority_score"] > summary["priority_score"]
    assert claim["priority"] == "high"
    assert claim["recommended_action"] == "generate_source_native_migration"


def test_reviewed_source_native_record_gets_completion_priority():
    legacy_only = score_priority_row(priority_row(legacy_claim_count=1))
    reviewed = score_priority_row(
        priority_row(
            legacy_claim_count=1,
            existing_source_native_artifact_count=3,
        )
    )

    assert reviewed["priority_score"] > legacy_only["priority_score"]
    assert reviewed["recommended_action"] == "run_legacy_migration_compiler"


def test_external_demand_is_bounded_and_changes_priority():
    no_external_demand = score_priority_row(priority_row(legacy_claim_count=1))
    one_external_signal = score_priority_row(
        priority_row(legacy_claim_count=1, external_signal_count=1)
    )
    many_external_signals = score_priority_row(
        priority_row(legacy_claim_count=1, external_signal_count=50)
    )

    assert (
        one_external_signal["priority_score"]
        - no_external_demand["priority_score"]
        == 20
    )
    assert (
        many_external_signals["priority_score"]
        - no_external_demand["priority_score"]
        == 60
    )


def test_stale_source_requires_refresh_before_migration():
    ranked = score_priority_row(
        priority_row(
            legacy_claim_count=2,
            freshness={"status": "overdue"},
        )
    )

    assert ranked["migration_ready"] is False
    assert ranked["recommended_action"] == "refresh_source_first"


def test_source_record_freshness_uses_registry_policy():
    policy = {
        "due_soon_fraction": 0.75,
        "cadences": {"weekly": {"maximum_age_hours": 216}},
    }
    as_of = datetime(2026, 8, 4, tzinfo=timezone.utc)

    current = source_record_freshness(
        {"retrieved_at": "2026-08-03T00:00:00Z"},
        source(),
        as_of=as_of,
        policy=policy,
    )
    overdue = source_record_freshness(
        {"retrieved_at": "2026-07-20T00:00:00Z"},
        source(),
        as_of=as_of,
        policy=policy,
    )

    assert current["status"] == "current"
    assert overdue["status"] == "overdue"


def test_legacy_hash_identity_reconciles_to_current_article_id_by_url():
    items, result_ids, aliases = reconcile_legacy_source_record_ids(
        {"rock_developer:legacy-hash": ["claim"]},
        {"rock_developer:legacy-hash": {"claim:legacy"}},
        {
            "rock_developer:legacy-hash": {
                "https://community.rockrms.com/developer/helix/overview/security"
            }
        },
        {
            "rock_developer:article:336": {
                "source_url": "https://community.rockrms.com/developer/helix/overview/security"
            }
        },
    )

    assert items == {"rock_developer:article:336": ["claim"]}
    assert result_ids == {"rock_developer:article:336": {"claim:legacy"}}
    assert aliases[0]["legacy_source_record_id"] == "rock_developer:legacy-hash"

    cross_source_items, _, cross_source_aliases = reconcile_legacy_source_record_ids(
        {"rock_podcast_rss:legacy-hash": ["episode"]},
        {"rock_podcast_rss:legacy-hash": set()},
        {"rock_podcast_rss:legacy-hash": {"https://example.test/shared"}},
        {"rock_community_blog:article": {"source_url": "https://example.test/shared"}},
    )
    assert cross_source_items == {"rock_podcast_rss:legacy-hash": ["episode"]}
    assert cross_source_aliases == []


def test_legacy_identity_reconciles_through_current_location_alias():
    item = object()
    items, result_ids, aliases = reconcile_legacy_source_record_ids(
        {"rock_lava_docs:old": [item]},
        {"rock_lava_docs:old": {"legacy:result"}},
        {"rock_lava_docs:old": {"https://community.rockrms.com/lava/commands"}},
        {
            "rock_lava_docs:new": {
                "source_url": "https://community.rockrms.com/lava/commands/getting-started",
                "location_aliases": ["https://community.rockrms.com/lava/commands"],
            }
        },
    )

    assert items == {"rock_lava_docs:new": [item]}
    assert result_ids == {"rock_lava_docs:new": {"legacy:result"}}
    assert aliases == [
        {
            "legacy_source_record_id": "rock_lava_docs:old",
            "canonical_source_record_id": "rock_lava_docs:new",
            "canonical_url": "https://community.rockrms.com/lava/commands",
        }
    ]


def test_reviewed_source_native_alias_reconciles_legacy_location():
    snapshot = type(
        "Snapshot",
        (),
        {
            "source_record_id": "rock_lava_docs:new",
            "canonical_url": "https://community.rockrms.com/lava/commands/getting-started",
            "location_aliases": ["https://community.rockrms.com/lava/commands"],
        },
    )()
    records = add_source_native_location_aliases(
        {
            "rock_lava_docs:new": {
                "source_url": "https://community.rockrms.com/lava/commands/getting-started",
                "location_aliases": [],
            }
        },
        [snapshot],
    )

    items, result_ids, aliases = reconcile_legacy_source_record_ids(
        {"rock_lava_docs:old": ["summary"]},
        {"rock_lava_docs:old": {"source:legacy"}},
        {"rock_lava_docs:old": {"https://community.rockrms.com/lava/commands"}},
        records,
    )

    assert items == {"rock_lava_docs:new": ["summary"]}
    assert result_ids == {"rock_lava_docs:new": {"source:legacy"}}
    assert aliases[0]["legacy_source_record_id"] == "rock_lava_docs:old"
    assert aliases[0]["canonical_source_record_id"] == "rock_lava_docs:new"


def test_priority_report_uses_the_supplied_repo_root_for_inputs_and_default_output(
    monkeypatch,
    tmp_path: Path,
):
    identity_path = tmp_path / "canonical" / "identity" / "v1" / "identity-registry.jsonl"
    identity_path.parent.mkdir(parents=True)
    identity_path.write_text('{"identity_id":"identity:alternate"}\n', encoding="utf-8")
    search_rows_path = tmp_path / "service" / "dist" / "search-rows.jsonl"
    search_rows_path.parent.mkdir(parents=True)
    search_rows_path.write_text('{"id":"search:alternate"}\n', encoding="utf-8")
    source_snapshot = SimpleNamespace(
        source_snapshot_id="source-snapshot:alternate",
        source_record_id="rock_documentation:alternate",
        canonical_url="https://example.test/alternate",
    )
    source_unit = SimpleNamespace(
        source_unit_id="source-unit:alternate",
        source_snapshot_id=source_snapshot.source_snapshot_id,
    )
    legacy_item = SimpleNamespace(
        ingestion_mode="legacy_reviewed_claim_projection",
        knowledge_type="claim",
        source_unit_ids=[source_unit.source_unit_id],
        knowledge_unit_id="knowledge:alternate",
        legacy_ids=[],
        concept_facets=["alternate-concept"],
        authority_tiers=["official"],
        payload={"approved_claims": []},
    )
    bundle = SimpleNamespace(
        source_snapshots=[source_snapshot],
        source_units=[source_unit],
        knowledge_units=[legacy_item],
    )
    alternate_concept = Concept(
        id="alternate-concept",
        title="Alternate Concept",
        description="Alternate-root report fixture.",
        keywords=["alternate"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    received: dict[str, Path] = {}

    def fake_build_canonical_knowledge_bundle(**kwargs):
        assert kwargs["repo_root"] == tmp_path
        assert kwargs["identity_registry"] == [{"identity_id": "identity:alternate"}]
        assert kwargs["search_rows"] == [{"id": "search:alternate"}]
        return bundle, {}

    def fake_concept_source_records(*, repo_root: Path):
        received["normalized_records"] = repo_root
        return [
            {
                "id": "rock_documentation:alternate",
                "source_id": "rock_documentation",
                "source_title": "Alternate record",
                "source_url": "https://example.test/alternate",
                "retrieved_at": "2026-08-10T00:00:00+00:00",
            }
        ]

    def fake_load_sources(path: Path):
        received["sources"] = path
        return [source()]

    def fake_load_source_freshness_policy(path: Path):
        received["freshness_policy"] = path
        return {"due_soon_fraction": 0.75, "cadences": {"weekly": {"maximum_age_hours": 168}}}

    def fake_load_concepts(path: Path):
        received["concepts"] = path
        return [alternate_concept]

    def fake_load_source_native_pilot(repo_root: Path):
        received["source_native"] = repo_root
        return {
            "source_snapshots": [],
            "source_units": [],
            "reviewed_artifacts": [],
            "generation_activities": [],
        }

    monkeypatch.setattr(
        source_native_priority_module,
        "build_canonical_knowledge_bundle",
        fake_build_canonical_knowledge_bundle,
    )
    monkeypatch.setattr(
        source_native_priority_module,
        "concept_source_records",
        fake_concept_source_records,
    )
    monkeypatch.setattr(
        source_native_priority_module,
        "load_source_native_pilot",
        fake_load_source_native_pilot,
    )
    monkeypatch.setattr(source_native_priority_module, "load_sources", fake_load_sources)
    monkeypatch.setattr(
        source_native_priority_module,
        "load_source_freshness_policy",
        fake_load_source_freshness_policy,
    )
    monkeypatch.setattr(source_native_priority_module, "load_concepts", fake_load_concepts)

    result = source_native_priority_module.build_source_native_migration_priority_report(
        repo_root=tmp_path,
        as_of=datetime(2026, 8, 11, tzinfo=timezone.utc),
    )

    destination = (
        tmp_path
        / "data"
        / "review"
        / "source-native-legacy-migration"
        / "priority-report.json"
    )
    assert result["destination"] == str(destination)
    assert received == {
        "normalized_records": tmp_path,
        "source_native": tmp_path,
        "sources": tmp_path / "sources" / "registry.yaml",
        "freshness_policy": tmp_path / "sources" / "freshness-policy.yaml",
        "concepts": tmp_path / "concepts" / "registry.yaml",
    }
    report = json.loads(destination.read_text(encoding="utf-8"))
    assert report["rows"][0]["source_record_id"] == "rock_documentation:alternate"
    assert report["rows"][0]["concept_ids"] == ["alternate-concept"]


def test_dashboard_signals_are_bounded_to_public_result_identity():
    dashboard = {
        "field_validation": {
            "review_queue": {
                "items": [
                    {
                        "result_id": "concept:security-permissions",
                        "result_kind": "concept",
                        "signal": "negative_outcome",
                        "occurrence_count": 2,
                        "query": "private query must not survive",
                        "description": "raw free form must not survive",
                    }
                ]
            }
        }
    }

    by_record, by_concept, rows = bounded_dashboard_signals(
        dashboard,
        result_records={},
    )

    assert not by_record
    assert by_concept["security-permissions"] == 2
    assert rows == [
        {
            "result_id": "concept:security-permissions",
            "result_kind": "concept",
            "signal": "negative_outcome",
            "occurrence_count": 2,
        }
    ]


def test_concept_inference_prefers_path_and_supported_legacy_routing():
    concepts = infer_concept_ids(
        {
            "source_id": "rock_documentation",
            "source_title": "Configure Sign-Up Permissions",
            "summary": "Configure security permissions and role access for Sign-Ups.",
            "topics": ["security"],
            "documentation_branches": [
                "documentation/engagement/additional-engagement-tools/sign-ups"
            ],
        },
        seeded_concept_ids=[],
        legacy_concept_ids=["engagement-tracking", "security-permissions"],
    )

    assert "engagement-tracking" in concepts
    assert "security-permissions" in concepts
    assert "platform-configuration" not in concepts

    assert infer_concept_ids(
        {"source_title": "Debugging Obsidian in VS Code"},
        seeded_concept_ids=["obsidian-development"],
        legacy_concept_ids=["security-permissions"],
    ) == ["obsidian-development"]

    media_concepts = infer_concept_ids(
        {
            "source_id": "rock_documentation",
            "source_title": "Media Player Lava Shortcode",
            "summary": "Use the Lava shortcode to display a video on a page.",
            "topics": ["lava"],
            "documentation_branches": [
                "documentation/digital-publishing/content-management/digital-media"
            ],
        },
        seeded_concept_ids=[],
        legacy_concept_ids=["cms-websites", "content-personalization"],
    )
    assert "lava" in media_concepts
