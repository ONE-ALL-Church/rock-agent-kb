import json

import rock_kb.indexes as indexes_module
from rock_kb.indexes import (
    build_public_source_summaries,
    build_public_source_summary_pack,
    dedupe_records_by_id,
    enrich_derived_documentation_metadata,
    is_public_agent_record,
    public_agent_records,
)


def test_public_agent_records_exclude_unreviewed_private_transcript_insights():
    private_row = {
        "id": "media-insight:1",
        "derived_from_private_transcript": True,
        "private_storage": True,
        "needs_review": True,
        "publishability_status": "distilled_summary_only",
    }
    public_row = {
        "id": "rock_documentation:1",
        "private_storage": False,
        "needs_review": False,
        "publishability_status": "public_summary",
    }

    assert public_agent_records([private_row, public_row]) == [public_row]


def test_public_agent_records_allow_reviewed_private_distillation():
    row = {
        "id": "media-insight:reviewed",
        "derived_from_private_transcript": True,
        "private_storage": True,
        "needs_review": False,
        "review_status": "redaction_reviewed",
        "publishability_status": "distilled_summary_only",
    }

    assert is_public_agent_record(row) is True


def test_dedupe_records_by_id_keeps_best_normalized_record():
    rows = dedupe_records_by_id(
        [
            {
                "id": "rock_lava_docs:home",
                "source_id": "rock_lava_docs",
                "summary": "Short summary.",
                "excerpt": "Short excerpt.",
                "retrieved_at": "2026-06-17T00:00:00+00:00",
            },
            {
                "id": "rock_lava_docs:home",
                "source_id": "rock_lava_docs",
                "summary": "Longer summary with more useful source context.",
                "excerpt": "Longer excerpt with more useful source context for the public agent pack.",
                "retrieved_at": "2026-06-18T00:00:00+00:00",
            },
            {
                "id": "rock_lava_docs:commands",
                "source_id": "rock_lava_docs",
                "summary": "Commands summary.",
            },
        ]
    )

    assert [row["id"] for row in rows] == ["rock_lava_docs:home", "rock_lava_docs:commands"]
    assert rows[0]["summary"].startswith("Longer summary")


def test_enrich_derived_documentation_metadata_backfills_branch_fields():
    row = enrich_derived_documentation_metadata(
        {
            "id": "rock_documentation:article:10",
            "documentation_family": "documentation",
            "documentation_slug": "engagement/prayer/request-settings",
            "documentation_path_parts": ["engagement", "prayer", "request-settings"],
        }
    )

    assert row["documentation_path"] == "documentation/engagement/prayer/request-settings"
    assert row["documentation_branch"] == "documentation/engagement/prayer"
    assert row["documentation_branches"] == [
        "documentation/engagement",
        "documentation/engagement/prayer",
        "documentation/engagement/prayer/request-settings",
    ]


def test_build_public_source_summaries_are_citation_first_without_raw_text():
    rows = build_public_source_summaries(
        [
            {
                "id": "rock_documentation:check-in",
                "source_id": "rock_documentation",
                "source_kind": "documentation",
                "source_url": "https://community.rockrms.com/documentation/bookcontent/9",
                "source_title": "Check-In",
                "summary": "Check-In uses areas, groups, schedules, locations, and labels. Verify release caveats before changing live kiosks.",
                "topics": ["check-in", "configuration"],
                "documentation_family": "documentation",
                "documentation_slug": "church-management/check-in",
                "documentation_path": "documentation/church-management/check-in",
                "documentation_branch": "documentation/church-management/check-in",
                "documentation_branches": ["documentation/church-management", "documentation/church-management/check-in"],
                "content_hash": "abc",
                "citations": [{"source_id": "rock_documentation", "url": "https://community.rockrms.com/documentation/bookcontent/9"}],
            }
        ]
    )

    assert rows[0]["schema"] == "rock-kb-public-source-summary-v1"
    assert rows[0]["source_record_id"] == "rock_documentation:check-in"
    assert rows[0]["key_insights"]
    assert rows[0]["citations"][0]["url"].startswith("https://community.rockrms.com")
    assert rows[0]["contains_raw_source_text"] is False
    assert rows[0]["documentation_branch"] == "documentation/church-management/check-in"


def test_reviewed_media_source_summaries_preserve_timestamps_without_media_urls():
    rows = build_public_source_summaries(
        [
            {
                "id": "media-insight:reviewed",
                "source_id": "rock_rocku",
                "source_kind": "media_insight",
                "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration",
                "source_title": "Mobile Check-in Configuration Transcript Insight",
                "media_url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret",
                "summary": "Mobile check-in configuration depends on virtual kiosk devices.",
                "topics": ["check-in", "mobile"],
                "content_hash": "abc",
                "derived_from_private_transcript": True,
                "private_storage": True,
                "needs_review": False,
                "review_status": "approved_for_public_distillation",
                "publishability_status": "approved_public_distillation",
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
            }
        ]
    )

    insight = rows[0]["key_insights"][0]
    serialized = json.dumps(rows)
    assert insight["confidence"] == "reviewed-media-insight"
    assert insight["timestamp"] == "00:44"
    assert insight["timestamp_seconds"] == 44
    assert insight["source_timestamp_url"] == "https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration"
    assert "media_url" not in serialized
    assert "player.vimeo.com" not in serialized
    assert "oauth2_token_id" not in serialized


def test_build_public_source_summaries_skip_sensitive_looking_rows():
    rows, report = build_public_source_summary_pack(
        [
            {
                "id": "rock_developer:setup",
                "source_id": "rock_developer",
                "source_url": "https://community.rockrms.com/developer/setup",
                "source_title": "Setup",
                "summary": "Replace password = local and connectionString=\"Data Source=local\" for your local system.",
                "topics": ["developer"],
            }
        ]
    )

    assert rows == []
    assert report["eligible_record_count"] == 1
    assert report["public_summary_count"] == 0
    assert report["skipped_sensitive_count"] == 1
    assert report["skipped_sensitive_by_source"] == {"rock_developer": 1}


def test_build_or_reuse_model_map_reuses_generated_artifacts_without_raw_scrapes(monkeypatch, tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    agent_dir = tmp_path / "agent"
    model_map_dir = knowledge_dir / "model-map"
    model_map_dir.mkdir(parents=True)
    agent_dir.mkdir(parents=True)
    monkeypatch.setattr(indexes_module, "KNOWLEDGE_DIR", knowledge_dir)
    monkeypatch.setattr(indexes_module, "AGENT_DIR", agent_dir)

    (model_map_dir / "index.md").write_text("# Model Map\n", encoding="utf-8")
    (model_map_dir / "stable-models.jsonl").write_text('{"model":"Person"}\n', encoding="utf-8")
    (model_map_dir / "stable-properties.jsonl").write_text('{"property":"Name"}\n', encoding="utf-8")
    (model_map_dir / "latest-models.jsonl").write_text('{"model":"Person"}\n{"model":"AI"}\n', encoding="utf-8")
    (model_map_dir / "latest-properties.jsonl").write_text('{"property":"Name"}\n{"property":"Prompt"}\n', encoding="utf-8")
    (model_map_dir / "version-diff.jsonl").write_text('{"change":"added"}\n', encoding="utf-8")
    (agent_dir / "model-map-summary.json").write_text(
        json.dumps({"stable": {"rock_version": "18.2.4"}, "pre_alpha": {"rock_version": "20.0.3"}}),
        encoding="utf-8",
    )
    (agent_dir / "model-map-entities.jsonl").write_text('{"entity":"Person"}\n', encoding="utf-8")
    (agent_dir / "model-map-properties.jsonl").write_text('{"property":"Name"}\n', encoding="utf-8")
    (agent_dir / "model-map-version-diff.jsonl").write_text('{"change":"added"}\n', encoding="utf-8")

    result = indexes_module.build_or_reuse_model_map()

    assert result["source"] == "reused_generated_model_map"
    assert result["reused_existing_artifacts"] == 1
    assert result["stable_version"] == "18.2.4"
    assert result["pre_alpha_version"] == "20.0.3"
    assert result["stable_models"] == 1
    assert result["pre_alpha_models"] == 2
