import json

import rock_kb.concepts as concepts_module
from rock_kb.concepts import (
    Concept,
    REQUIRED_AGENT_ENTRYPOINT_FILES,
    build_concept_guide,
    build_single_concept,
    concept_source_records,
    ensure_weighted_source_coverage,
    get_concept,
    load_concepts,
    rank_records_for_concept,
    refresh_long_form_approved_claims,
    replace_or_insert_generated_claim_section,
    replace_or_insert_generated_media_section,
    report_concept_staleness,
    report_guide_refresh_plan,
    render_concept_approved_claims_artifact,
    render_concept_approved_media_artifact,
    render_concept_guide,
    render_long_form_approved_claims_section,
    render_long_form_approved_media_section,
    render_approved_claims_section,
    record_table_rows,
    render_reviewed_media_insights,
)
from rock_kb.indexes import all_normalized_records
from rock_kb.jsonl import read_jsonl, write_jsonl


def test_load_concepts_registry():
    concepts = load_concepts()
    ids = {concept.id for concept in concepts}
    assert "check-in" in ids
    assert "api-integrations" in ids


def test_render_single_concept_guide():
    concept = get_concept("check-in")
    text, dependency = build_concept_guide(concept, all_normalized_records(), {})
    assert "# Check-In" in text
    assert "Rebuild Dependencies" in text
    assert dependency["concept_id"] == "check-in"


def test_weighted_source_coverage_keeps_release_records():
    concept = Concept(
        id="cms-websites",
        title="CMS And Websites",
        description="CMS",
        keywords=["cms"],
        source_weights={"rock_core_release_notes": 4, "rock_developer": 4},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=3,
        raw={},
    )
    ranked = [
        {"id": "dev1", "source_id": "rock_developer"},
        {"id": "dev2", "source_id": "rock_developer"},
        {"id": "dev3", "source_id": "rock_developer"},
        {"id": "rel1", "source_id": "rock_core_release_notes"},
        {"id": "rel2", "source_id": "rock_core_release_notes"},
    ]

    selected = ensure_weighted_source_coverage(concept, ranked, limit=4)

    assert {record["id"] for record in selected} >= {"rel1", "rel2"}


def test_path_constrained_concept_and_subguide_prefer_matching_developer_branch():
    concept = Concept(
        id="helix",
        title="Helix",
        description="Helix.",
        keywords=["helix"],
        source_weights={"rock_developer": 1},
        depends_on_topics=[],
        subguides=[
            {
                "title": "HTMX",
                "keywords": ["htmx"],
                "source_url_prefixes": ["https://community.rockrms.com/developer/helix/htmx"],
            }
        ],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={"source_url_prefixes": ["https://community.rockrms.com/developer/helix"]},
    )
    records = [
        {
            "id": "helix",
            "source_id": "rock_developer",
            "source_title": "Helix Overview",
            "source_url": "https://community.rockrms.com/developer/helix/overview",
            "summary": "Helix overview.",
        },
        {
            "id": "htmx",
            "source_id": "rock_developer",
            "source_title": "HTMX",
            "source_url": "https://community.rockrms.com/developer/helix/htmx",
            "summary": "HTMX details.",
        },
        {
            "id": "other",
            "source_id": "rock_developer",
            "source_title": "Other HTMX",
            "source_url": "https://community.rockrms.com/developer/obsidian/form-validation",
            "summary": "Mentions htmx but is not in the Helix HTMX branch.",
        },
    ]

    ranked = rank_records_for_concept(concept, records)
    text, dependency = build_concept_guide(concept, records, {})

    assert ranked[0]["id"] in {"helix", "htmx"}
    assert dependency["source_record_ids"][:2] == ["helix", "htmx"]
    assert "https://community.rockrms.com/developer/helix/htmx" in text
    assert "https://community.rockrms.com/developer/obsidian/form-validation" not in text


def test_documentation_branch_constraints_match_structured_metadata():
    concept = Concept(
        id="prayer-care",
        title="Prayer And Care",
        description="Prayer.",
        keywords=["prayer"],
        source_weights={"rock_documentation": 1},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={"documentation_branches": ["documentation/engagement/prayer"]},
    )
    records = [
        {
            "id": "prayer",
            "source_id": "rock_documentation",
            "source_title": "Request Settings",
            "source_url": "https://community.rockrms.com/documentation/engagement/prayer/request-settings",
            "documentation_branch": "documentation/engagement/prayer",
            "documentation_branches": [
                "documentation/engagement",
                "documentation/engagement/prayer",
                "documentation/engagement/prayer/request-settings",
            ],
            "documentation_path": "documentation/engagement/prayer/request-settings",
            "summary": "Configuration for request settings.",
        },
        {
            "id": "groups",
            "source_id": "rock_documentation",
            "source_title": "Prayer Group Mention",
            "source_url": "https://community.rockrms.com/documentation/engagement/groups/prayer-group-mention",
            "documentation_branch": "documentation/engagement/groups",
            "documentation_branches": [
                "documentation/engagement",
                "documentation/engagement/groups",
                "documentation/engagement/groups/prayer-group-mention",
            ],
            "documentation_path": "documentation/engagement/groups/prayer-group-mention",
            "summary": "Mentions prayer while documenting groups.",
        },
    ]

    ranked = rank_records_for_concept(concept, records)

    assert [record["id"] for record in ranked] == ["prayer"]


def test_record_table_rows_skip_sensitive_looking_summaries():
    rows = record_table_rows(
        [
                {
                    "source_title": "Setup",
                    "source_id": "rock_developer",
                "summary": "Replace [server_name] and [password] with your local values. Example: Password=local-value",
                    "source_url": "https://community.rockrms.com/developer/quickstart-tutorials/appendix/appendix---setup",
                },
            {
                "source_title": "Overview",
                "source_id": "rock_developer",
                "summary": "Developer overview.",
                "source_url": "https://community.rockrms.com/developer",
            },
        ]
    )

    text = "\n".join(rows)
    assert "password" not in text
    assert "Developer overview" in text


def test_concept_source_records_require_promoted_transcript_insights(monkeypatch):
    monkeypatch.setattr(
        concepts_module,
        "all_normalized_records",
        lambda: [
            {
                "id": "media-insight:unreviewed",
                "derived_from_private_transcript": True,
                "private_storage": True,
                "needs_review": True,
                "publishability_status": "distilled_summary_only",
            },
            {
                "id": "media-insight:reviewed",
                "derived_from_private_transcript": True,
                "private_storage": True,
                "needs_review": False,
                "review_status": "approved_for_public_distillation",
                "publishability_status": "approved_public_distillation",
            },
            {
                "id": "rock_documentation:public",
                "source_id": "rock_documentation",
                "needs_review": False,
                "publishability_status": "public_summary",
            },
        ],
    )

    ids = {record["id"] for record in concept_source_records()}

    assert "media-insight:unreviewed" not in ids
    assert "media-insight:reviewed" in ids
    assert "rock_documentation:public" in ids


def test_reviewed_media_insights_render_key_insights_without_placeholders():
    rows = render_reviewed_media_insights(
        [
            {
                "id": "media-insight:reviewed",
                "source_title": "Mobile Check-in Configuration Transcript Insight",
                "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration",
                "media_url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret",
                "needs_review": False,
                "summary": "Mobile check-in configuration depends on virtual kiosks.",
                "key_insights": [
                    {
                        "topic": "virtual kiosk devices",
                        "insight": "Treat each mobile check-in device record like a virtual kiosk.",
                        "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration",
                        "source_timestamp_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration",
                        "timestamp": "00:44",
                        "timestamp_seconds": 44,
                    }
                ],
            },
            {
                "id": "media-insight:unreviewed",
                "source_title": "Unreviewed",
                "needs_review": True,
                "key_insights": [{"insight": "Review this timestamp for a public-safe distilled insight."}],
            },
        ]
    )
    text = "\n".join(rows)

    assert "Reviewed Media Insights" in text
    assert "| Source | Topic | Timestamp | Distilled Claim | Citation |" in text
    assert "virtual kiosk devices" in text
    assert "00:44" in text
    assert "Treat each mobile check-in device record like a virtual kiosk." in text
    assert "Review this timestamp" not in text
    assert "player.vimeo.com" not in text
    assert "oauth2_token_id" not in text


def test_concept_guide_surfaces_reviewed_media_key_insights():
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in", "mobile"],
        source_weights={},
        depends_on_topics=["mobile"],
        subguides=[{"title": "Mobile Check-In", "keywords": ["mobile check-in", "kiosk"]}],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    records = [
        {
            "id": "media-insight:reviewed",
            "source_id": "rock_rocku",
            "source_title": "Mobile Check-in Overview Transcript Insight",
            "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
            "content_hash": "hash",
            "needs_review": False,
            "summary": "Mobile check-in is a contactless check-in flow.",
            "topics": ["mobile", "check-in"],
            "key_insights": [
                    {
                        "topic": "mobile check-in flow",
                        "insight": "The mobile flow still follows the familiar check-in pattern.",
                        "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
                        "source_timestamp_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
                        "timestamp": "01:22",
                        "timestamp_seconds": 82,
                    }
                ],
            }
    ]

    text, dependency = build_concept_guide(concept, records, {})

    assert "## Reviewed Media Insights" in text
    assert "#### Reviewed distilled media insights" in text
    assert "01:22" in text
    assert "The mobile flow still follows the familiar check-in pattern." in text
    assert dependency["source_record_ids"] == ["media-insight:reviewed"]


def test_concept_guide_references_generated_model_map_crosswalk(monkeypatch, tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", knowledge_dir)
    model_map_dir = knowledge_dir / "model-map"
    write_jsonl(
        model_map_dir / "stable-models.jsonl",
        [
            {
                "model_name": "Person",
                "model_slug": "person",
                "rock_version": "18.2.4",
                "property_count": 72,
                "database_property_count": 33,
                "lava_property_count": 101,
                "lava_non_database_property_count": 39,
            }
        ],
    )
    write_jsonl(
        model_map_dir / "stable-properties.jsonl",
        [
            {
                "model_name": "Person",
                "property_name": "FullName",
                "source_url": "https://stable.example/admin/power-tools/model-map",
                "is_lava_supported_non_database": True,
            }
        ],
    )
    write_jsonl(
        model_map_dir / "version-diff.jsonl",
        [
            {
                "model_name": "Person",
                "change_type": "property_changed",
                "property_name": "FullName",
                "changed_fields": ["description"],
            }
        ],
    )
    concept = Concept(
        id="people-families",
        title="People And Families",
        description="People.",
        keywords=["person"],
        source_weights={"rock_model_map": 3},
        depends_on_topics=["people"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    selected = [
        {
            "id": "rock_model_map:person",
            "source_id": "rock_model_map",
            "source_title": "Person",
            "source_url": "https://community.rockrms.com/ModelMap",
            "model_name": "Person",
            "model_category": "CRM",
            "summary": "Person is a Rock model.",
            "topics": ["people", "model-map"],
        }
    ]
    dependency = {
        "last_built": "2026-06-07T00:00:00+00:00",
        "source_record_ids": ["rock_model_map:person"],
        "approved_claim_count": 0,
        "approved_claim_dependencies": [],
    }

    text = render_concept_guide(concept, selected, selected, dependency)

    assert "| [Person](../../model-map/models/person.md) | CRM | 18.2.4 | 72 | 33 | 101 | 39 | 1 |" in text
    assert "`Person.FullName` is Lava-marked but not database-marked in the generated Model Map (Rock 18.2.4" in text


def test_refresh_long_form_model_map_pointers_updates_existing_guides(monkeypatch, tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", knowledge_dir)
    concept_dir = knowledge_dir / "concepts" / "groups"
    concept_dir.mkdir(parents=True)
    guide_path = concept_dir / "guide.md"
    guide_path.write_text("# Groups\n\n## Existing Section\n\nBody.\n", encoding="utf-8")

    concept = Concept(
        id="groups",
        title="Groups",
        description="Groups.",
        keywords=["group"],
        source_weights={},
        depends_on_topics=["groups"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    monkeypatch.setattr(concepts_module, "load_concepts", lambda: [concept])

    result = concepts_module.refresh_long_form_model_map_pointers()

    assert result["updated_count"] == 1
    text = guide_path.read_text(encoding="utf-8")
    assert "<!-- BEGIN GENERATED MODEL MAP POINTERS -->" in text
    assert "[Groups index](index.md#data-model-landmarks)" in text
    assert "## Existing Section" in text

    second_result = concepts_module.refresh_long_form_model_map_pointers()
    assert second_result["updated_count"] == 0
    assert guide_path.read_text(encoding="utf-8") == text


def test_concept_guide_tracks_and_renders_approved_claims(monkeypatch):
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    monkeypatch.setattr(
        concepts_module,
        "approved_claim_dependencies_for_concept",
        lambda concept_id: [
            {
                "claim_id": "claim:abc",
                "claim_hash": "claim-hash",
                "claim": "Reviewed RockU check-in training should be verified against local configuration.",
                "claim_type": "operational_guidance",
                "authority_tier": "rocku-confirmed",
                "source_refs": [{"url": "https://community.rockrms.com/rocku/check-in/example"}],
                "needs_live_verification": True,
            }
        ],
    )
    monkeypatch.setattr(concepts_module, "approved_media_dependencies_for_concept", lambda concept_id: [])

    text, dependency = build_concept_guide(concept, [], {})

    assert "## Approved Claims" in text
    assert "rocku-confirmed" in text
    assert "Reviewed RockU check-in training" in text
    assert dependency["approved_claim_ids"] == ["claim:abc"]
    assert dependency["approved_claim_hashes"] == {"claim:abc": "claim-hash"}


def test_render_approved_claims_labels_community_derived_material():
    lines = render_approved_claims_section(
        [
            {
                "claim_id": "claim:community",
                "claim": "A reviewed community pattern can inform workflow design after live verification.",
                "claim_type": "implementation_pattern",
                "authority_tier": "community-reviewed",
                "source_refs": [{"url": "https://community.rockrms.com/community-hubs/example"}],
                "needs_live_verification": True,
            }
        ]
    )
    text = "\n".join(lines)

    assert "Community-derived claims are labeled" in text
    assert "community-reviewed" in text
    assert "live verification recommended" in text
    assert "https://community.rockrms.com/community-hubs/example" in text


def test_rank_records_prioritizes_approved_media_concept_mapping():
    concept = Concept(
        id="communications",
        title="Communications",
        description="Communications.",
        keywords=["communication", "email"],
        source_weights={"rock_documentation": 10},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    records = [
        {
            "id": "rock_documentation:email",
            "source_id": "rock_documentation",
            "source_title": "Email Communication Documentation",
            "summary": "Email communication template recipient communication.",
        },
        {
            "id": "media-insight:approved",
            "source_id": "rock_community_hubs",
            "source_title": "Media Watch Transcript Insight",
            "summary": "Reviewed sender trust guidance.",
            "approved_concept_ids": ["communications"],
            "needs_review": False,
            "review_status": "approved_for_public_distillation",
            "key_insights": [{"insight": "Verify sender authentication before sending."}],
        },
    ]

    ranked = rank_records_for_concept(concept, records)

    assert ranked[0]["id"] == "media-insight:approved"


def test_subguide_media_matching_does_not_match_only_insight_body_words():
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=["mobile"],
        subguides=[{"title": "Mobile Check-In", "keywords": ["mobile check-in", "mobile", "family"]}],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=10,
        raw={},
    )
    records = [
        {
            "id": "media-insight:rapid-attendance",
            "source_id": "rock_rocku",
            "source_title": "Rapid Attendance Entry Transcript Insight",
            "source_url": "https://community.rockrms.com/rocku/check-in/rapid-attendance-entry",
            "content_hash": "hash",
            "needs_review": False,
            "summary": "Rapid Attendance Entry can collect attendance, family updates, and related ministry information.",
            "topics": ["check-in", "attendance"],
            "key_insights": [
                {
                    "topic": "attendance and care capture",
                    "insight": "The block can combine attendance marking with family editing.",
                    "source_url": "https://community.rockrms.com/rocku/check-in/rapid-attendance-entry",
                }
            ],
        }
    ]

    text, _ = build_concept_guide(concept, records, {})
    mobile_section = text.split("### Mobile Check-In", 1)[1]

    assert "#### Reviewed distilled media insights" not in mobile_section


def test_concept_staleness_report():
    rows = report_concept_staleness()
    assert rows
    assert any(row["concept_id"] == "check-in" for row in rows)


def test_concept_staleness_includes_private_dependency_impacts(monkeypatch):
    monkeypatch.setattr(
        concepts_module,
        "private_impacts_by_concept",
        lambda: {
            "check-in": [
                {
                    "public_contribution_id": "oneall:check-in-pattern",
                    "concept_ids": ["check-in"],
                    "needs_rebuild": True,
                    "public_artifact_path": "contributions/oneall/bundle.jsonl",
                }
            ]
        },
    )
    rows = report_concept_staleness()
    check_in = next(row for row in rows if row["concept_id"] == "check-in")
    assert check_in["needs_rebuild"] is True
    assert check_in["private_dependency_impact_count"] == 1
    if check_in["reason"] == "current":
        raise AssertionError("private dependency impacts must change stale reason")


def test_guide_refresh_plan_flags_missing_approved_media_metadata(monkeypatch, tmp_path):
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", tmp_path / "knowledge")
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=["mobile"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(concepts_module, "load_concepts", lambda: [concept])
    monkeypatch.setattr(concepts_module, "approved_claim_dependencies_for_concept", lambda concept_id: [])
    monkeypatch.setattr(
        concepts_module,
        "read_dependency_map",
        lambda: {"check-in": {"source_hashes": {"media-insight:approved": "hash-1"}}},
    )
    records = [
        {
            "id": "media-insight:approved",
            "source_id": "rock_rocku",
            "source_title": "Mobile Check-in Overview Transcript Insight",
            "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
            "content_hash": "hash-1",
            "needs_review": False,
            "review_status": "approved_for_public_distillation",
            "summary": "Mobile check-in needs review.",
            "topics": ["check-in", "mobile"],
            "key_insights": [{"topic": "mobile", "insight": "Use reviewed claims."}],
        }
    ]

    plan = report_guide_refresh_plan(records)
    check_in = plan["concepts"][0]

    assert plan["needs_generated_index_rebuild"] == []
    assert plan["needs_long_form_guide_refresh"] == ["check-in"]
    assert check_in["long_form_guide_reason"] == "approved_media_hash_changed_or_missing"
    assert check_in["changed_approved_media_records"] == ["media-insight:approved"]


def test_guide_refresh_plan_accepts_current_mentioned_approved_media(monkeypatch, tmp_path):
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", tmp_path / "knowledge")
    concept_dir = tmp_path / "knowledge" / "concepts" / "check-in"
    concept_dir.mkdir(parents=True)
    (concept_dir / "guide-dependencies.json").write_text(
        json.dumps(
            {
                "approved_media_dependency_hashes": {"media-insight:approved": "hash-1"},
                "approved_media_dependencies": [
                    {
                        "source_record_id": "media-insight:approved",
                        "content_hash": "hash-1",
                        "mentioned_in_guide": True,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=["mobile"],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(concepts_module, "load_concepts", lambda: [concept])
    monkeypatch.setattr(concepts_module, "approved_claim_dependencies_for_concept", lambda concept_id: [])
    monkeypatch.setattr(
        concepts_module,
        "read_dependency_map",
        lambda: {"check-in": {"source_hashes": {"media-insight:approved": "hash-1"}}},
    )
    records = [
        {
            "id": "media-insight:approved",
            "source_id": "rock_rocku",
            "source_title": "Mobile Check-in Overview Transcript Insight",
            "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
            "content_hash": "hash-1",
            "needs_review": False,
            "review_status": "approved_for_public_distillation",
            "summary": "Mobile check-in needs review.",
            "topics": ["check-in", "mobile"],
            "key_insights": [{"topic": "mobile", "insight": "Use reviewed claims."}],
        }
    ]

    plan = report_guide_refresh_plan(records)
    check_in = plan["concepts"][0]

    assert plan["needs_generated_index_rebuild"] == []
    assert plan["needs_long_form_guide_refresh"] == []
    assert check_in["long_form_guide_reason"] == "current"


def test_guide_refresh_plan_flags_changed_approved_claims(monkeypatch, tmp_path):
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", tmp_path / "knowledge")
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(concepts_module, "load_concepts", lambda: [concept])
    monkeypatch.setattr(
        concepts_module,
        "read_dependency_map",
        lambda: {"check-in": {"source_hashes": {}, "approved_claim_hashes": {"claim:abc": "old-hash"}}},
    )
    monkeypatch.setattr(
        concepts_module,
        "approved_claim_dependencies_for_concept",
        lambda concept_id: [
            {
                "claim_id": "claim:abc",
                "claim_hash": "new-hash",
                "claim": "A reviewed claim changed.",
                "mentioned_in_guide": False,
            }
        ],
    )

    plan = report_guide_refresh_plan([])
    check_in = plan["concepts"][0]

    assert plan["needs_generated_index_rebuild"] == ["check-in"]
    assert plan["needs_long_form_guide_refresh"] == ["check-in"]
    assert check_in["generated_index_changed_approved_claims"] == ["claim:abc"]
    assert check_in["changed_approved_claims"] == ["claim:abc"]
    assert check_in["long_form_guide_reason"] == "approved_claim_hash_changed_or_missing"


def test_refresh_long_form_approved_claims_inserts_summary_and_full_artifact(monkeypatch, tmp_path):
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", tmp_path / "knowledge")
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    monkeypatch.setattr(concepts_module, "load_concepts", lambda: [concept])
    monkeypatch.setattr(concepts_module, "get_concept", lambda concept_id: concept)
    monkeypatch.setattr(
        concepts_module,
        "approved_claim_dependencies_for_concept",
        lambda concept_id: [
            {
                "claim_id": "claim:abc",
                "claim_hash": "claim-hash",
                "claim": "A reviewed claim belongs in the guide.",
                "claim_type": "operational_guidance",
                "authority_tier": "rocku-confirmed",
                "source_refs": [{"url": "https://example.com/source"}],
            }
        ],
    )
    monkeypatch.setattr(concepts_module, "approved_media_dependencies_for_concept", lambda concept_id: [])
    guide_dir = tmp_path / "knowledge" / "concepts" / "check-in"
    guide_dir.mkdir(parents=True)
    (guide_dir / "guide.md").write_text("# Check-In\n\nBody.\n\n## 20. Source Map And Dependency Notes\n\nSources.\n", encoding="utf-8")

    result = refresh_long_form_approved_claims("check-in")
    text = (guide_dir / "guide.md").read_text(encoding="utf-8")
    artifact_text = (guide_dir / "approved-claims.md").read_text(encoding="utf-8")
    media_text = (guide_dir / "approved-media.md").read_text(encoding="utf-8")

    assert result["updated_count"] == 1
    assert "## Approved Claim Coverage" in text
    assert "Full generated claim table: `approved-claims.md`" in text
    assert "A reviewed claim belongs in the guide." in text
    assert "`claim:abc`" in artifact_text
    assert "A reviewed claim belongs in the guide." in artifact_text
    assert "No approved media distillations are currently routed to this concept." in media_text
    assert text.index("## Approved Claim Coverage") < text.index("## 20. Source Map And Dependency Notes")


def test_long_form_claim_coverage_is_bounded():
    claims = [
        {
            "claim_id": f"claim:{index}",
            "claim": f"Claim {index}.",
            "claim_type": "operational_guidance",
            "authority_tier": "rocku-confirmed",
            "source_refs": [],
        }
        for index in range(20)
    ]
    section = render_long_form_approved_claims_section(claims, limit=3)

    assert section.count("| rocku-confirmed |") == 3
    assert "17 additional approved claims are tracked in `approved-claims.md`" in section


def test_full_claim_artifact_includes_all_claim_ids():
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    artifact = render_concept_approved_claims_artifact(
        concept,
        [
            {
                "claim_id": "claim:abc",
                "claim": "A reviewed claim belongs in the artifact.",
                "claim_type": "operational_guidance",
                "authority_tier": "rocku-confirmed",
                "source_refs": [],
            }
        ],
    )

    assert "# Check-In Approved Claims" in artifact
    assert "`claim:abc`" in artifact
    assert "A reviewed claim belongs in the artifact." in artifact


def test_long_form_media_coverage_is_bounded():
    media = [
        {
            "source_record_id": f"media-insight:{index}",
            "source_title": f"Media {index}",
            "source_url": f"https://example.com/media/{index}",
            "review_status": "approved_for_public_distillation",
            "key_insight_count": index,
        }
        for index in range(12)
    ]
    section = render_long_form_approved_media_section(media, limit=4)

    assert section.count("approved_for_public_distillation") == 4
    assert "8 additional reviewed media records are tracked in `approved-media.md`" in section


def test_full_media_artifact_includes_all_media_ids():
    concept = Concept(
        id="check-in",
        title="Check-In",
        description="Check-in.",
        keywords=["check-in"],
        source_weights={},
        depends_on_topics=[],
        subguides=[],
        rebuild_policy="source_hash_changed_or_weekly",
        guide_status="generated_needs_review",
        max_records=5,
        raw={},
    )
    artifact = render_concept_approved_media_artifact(
        concept,
        [
            {
                "source_record_id": "media-insight:abc",
                "source_title": "Reviewed media",
                "source_url": "https://example.com/media",
                "review_status": "approved_for_public_distillation",
                "key_insight_count": 2,
            }
        ],
    )

    assert "# Check-In Approved Media" in artifact
    assert "`media-insight:abc`" in artifact
    assert "Reviewed media" in artifact


def test_replace_or_insert_generated_claim_section_replaces_existing_section():
    first = render_long_form_approved_claims_section(
        [
            {
                "claim_id": "claim:old",
                "claim": "Old claim.",
                "claim_type": "risk",
                "authority_tier": "community-reviewed",
                "source_refs": [],
            }
        ]
    )
    second = render_long_form_approved_claims_section(
        [
            {
                "claim_id": "claim:new",
                "claim": "New claim.",
                "claim_type": "risk",
                "authority_tier": "community-reviewed",
                "source_refs": [],
            }
        ]
    )
    text = replace_or_insert_generated_claim_section("# Guide\n\nBody.\n", first)
    text = replace_or_insert_generated_claim_section(text, second)

    assert "New claim." in text
    assert "Old claim." not in text
    assert text.count("BEGIN GENERATED APPROVED CLAIM COVERAGE") == 1


def test_replace_or_insert_generated_media_section_replaces_existing_section():
    first = render_long_form_approved_media_section(
        [
            {
                "source_record_id": "media-insight:old",
                "source_title": "Old media",
                "source_url": "https://example.com/old",
                "review_status": "approved_for_public_distillation",
                "key_insight_count": 1,
            }
        ]
    )
    second = render_long_form_approved_media_section(
        [
            {
                "source_record_id": "media-insight:new",
                "source_title": "New media",
                "source_url": "https://example.com/new",
                "review_status": "approved_for_public_distillation",
                "key_insight_count": 1,
            }
        ]
    )
    text = replace_or_insert_generated_media_section("# Guide\n\nBody.\n", first)
    text = replace_or_insert_generated_media_section(text, second)

    assert "New media" in text
    assert "Old media" not in text
    assert text.count("BEGIN GENERATED APPROVED MEDIA COVERAGE") == 1


def test_generated_claim_and_media_sections_are_idempotent():
    claim_section = render_long_form_approved_claims_section(
        [
            {
                "claim_id": "claim:one",
                "claim": "One claim.",
                "claim_type": "configuration",
                "authority_tier": "community-reviewed",
                "source_refs": [],
            }
        ]
    )
    media_section = render_long_form_approved_media_section(
        [
            {
                "source_record_id": "media-insight:one",
                "source_title": "One media",
                "source_url": "https://example.com/media",
                "review_status": "approved_for_public_distillation",
                "key_insight_count": 1,
            }
        ]
    )
    text = "# Guide\n\nBody.\n\n## Source Map And Dependency Notes\n"
    first = replace_or_insert_generated_media_section(
        replace_or_insert_generated_claim_section(text, claim_section),
        media_section,
    )
    second = replace_or_insert_generated_media_section(
        replace_or_insert_generated_claim_section(first, claim_section),
        media_section,
    )

    assert second == first


def test_build_single_concept_creates_baseline_agent_entrypoints(monkeypatch, tmp_path):
    monkeypatch.setattr(concepts_module, "KNOWLEDGE_DIR", tmp_path / "knowledge")
    monkeypatch.setattr(concepts_module, "AGENT_DIR", tmp_path / "agent")
    monkeypatch.setattr(concepts_module, "MEDIA_DIR", tmp_path / "data" / "media")
    agent_dir = tmp_path / "agent"
    agent_dir.mkdir(parents=True)
    (agent_dir / "source-summaries.jsonl").write_text('{"id":"summary"}\n', encoding="utf-8")
    (agent_dir / "source-summary-report.json").write_text(
        json.dumps({"eligible_record_count": 1, "skipped_sensitive_count": 0}),
        encoding="utf-8",
    )
    media_index_dir = tmp_path / "data" / "media" / "index"
    media_index_dir.mkdir(parents=True)
    (media_index_dir / "media-index.jsonl").write_text('{"id":"media:abc:sidecar"}\n', encoding="utf-8")
    monkeypatch.setattr(
        concepts_module,
        "all_normalized_records",
        lambda: [
            {
                "id": "rock_developer:test-api",
                "source_id": "rock_developer",
                "source_url": "https://community.rockrms.com/developer/test-api",
                "source_title": "The Rock REST API",
                "summary": "REST API authentication, endpoints, webhooks, and integrations.",
                "excerpt": "REST API authentication and endpoint guidance.",
                "topics": ["api"],
                "content_hash": "hash-api",
            }
        ],
    )
    result = build_single_concept("api-integrations")
    concept_dir = tmp_path / "knowledge" / "concepts" / "api-integrations"
    assert result["baseline_agent_artifacts"] == len(REQUIRED_AGENT_ENTRYPOINT_FILES)
    for filename in REQUIRED_AGENT_ENTRYPOINT_FILES:
        assert (concept_dir / filename).exists()
    assert list(read_jsonl(concept_dir / "task-cards.jsonl"))
    assert list(read_jsonl(tmp_path / "agent" / "concept-task-cards.jsonl"))
    manifest = json.loads((tmp_path / "agent" / "rock-kb-manifest.json").read_text(encoding="utf-8"))
    row = next(item for item in manifest["concepts"] if item["concept_id"] == "api-integrations")
    assert row["artifact_level"] == "baseline"
    assert row["quickstart"] == "knowledge/concepts/api-integrations/quickstart.md"
    assert manifest["agent_entrypoints"]["source_summaries"] == "agent/source-summaries.jsonl"
    assert manifest["agent_entrypoints"]["source_summary_report"] == "agent/source-summary-report.json"
    assert manifest["source_summaries"]["record_count"] == 1
    assert manifest["source_summaries"]["skipped_sensitive_count"] == 0
    assert manifest["agent_entrypoints"]["private_media"] == "data/media/index/media-index.jsonl"
    assert manifest["private_media"]["record_count"] == 1
    assert manifest["private_media"]["public_publish_mode"] == "private_only"
