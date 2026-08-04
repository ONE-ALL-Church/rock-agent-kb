from datetime import datetime, timezone

from rock_kb.source_native_priority import (
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
