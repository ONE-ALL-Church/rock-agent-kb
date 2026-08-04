from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from rock_kb.canonical_knowledge import build_canonical_knowledge_bundle
from rock_kb.extract import sha256_text
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.schemas import SourceNativeDistillationOutput, SourceSnapshot, SourceUnit
from rock_kb.source_native import (
    apply_source_unit_split_rules,
    build_source_native_impact_report,
    build_source_native_document_candidates,
    load_source_unit_split_rules,
    merge_source_native_distillation_outputs,
    parse_markdown_source_units,
    promote_source_native_distillation,
    source_observation_metadata,
    source_native_model_input_hash,
    source_native_evaluation_rows,
    validate_source_native_bundle_consistency,
    validate_source_native_distillation,
    write_source_native_distillation_schema,
    write_source_native_generation_prompt,
    write_source_native_manifest,
)


def document_record() -> dict:
    return {
        "id": "rock_documentation:article:100",
        "source_id": "rock_documentation",
        "source_url": "https://community.rockrms.com/documentation/supporting-rock/caching/test",
        "source_title": "Test Cache Article",
        "summary": (
            "Configure and inspect a cache provider from the administration "
            "settings page, including the documented behavior and operational "
            "cautions for indexing."
        ),
        "excerpt": "Configure and inspect a cache provider.",
        "content_hash": "0" * 64,
        "documentation_path": "documentation/supporting-rock/caching/test",
        "documentation_branches": [
            "documentation/supporting-rock",
            "documentation/supporting-rock/caching",
        ],
        "documentation_article_id": 100,
        "documentation_current_version": "v19.0",
    }


def rockumentation_payload() -> dict:
    return {
        "initialContent": (
            '<article class="rockumentation-article" data-main-article="true">'
            "<p>The cache provider stores reusable values for later requests.</p>"
            "<h2>Configure</h2>"
            "<ol><li>Open the settings page.</li>"
            "<li>Enable the cache provider.</li></ol>"
            "</article>"
        ),
        "configurationValues": {
            "slug": "documentation/supporting-rock/caching/test",
            "title": "Test Cache Article",
        },
    }


def source_units() -> list[dict]:
    units = parse_markdown_source_units(
        markdown=(
            "Opening behavior for the feature.\n\n"
            "# Configure\n\n"
            "1. Open the settings page.\n"
            "2. Enable the provider.\n\n"
            "# Options\n\n"
            "| Setting | Meaning |\n"
            "| --- | --- |\n"
            "| Enabled | Allows indexing. |\n"
        ),
        source_snapshot_id="source-snapshot:test",
        source_record_id="rock_documentation:article:100",
        source_url="https://community.rockrms.com/documentation/test",
        source_title="Test Article",
        documentation_path="documentation/test",
    )
    return [row.model_dump(by_alias=True, exclude_none=True) for row in units]


def distillation_input() -> dict:
    units = source_units()
    return {
        "schema": "rock-kb-source-native-distillation-input-v1",
        "candidate_id": "source-native-candidate:test",
        "source_input_hash": "a" * 64,
        "source_snapshot": {
            "schema": "rock-kb-source-snapshot-v2",
            "source_snapshot_id": "source-snapshot:test",
            "source_id": "rock_documentation",
            "source_record_id": "rock_documentation:article:100",
            "source_work_id": "documentation-article:100",
            "canonical_url": "https://community.rockrms.com/documentation/test",
            "title": "Test Article",
            "content_hash": "b" * 64,
            "normalized_content_hash": "b" * 64,
            "authority_tier": "official",
            "public_policy": "cite_and_summarize_only",
            "derivation": {"documentation_article_id": 100},
        },
        "source_units": units,
        "concept_ids": ["system-admin-ops"],
        "existing_claims": [],
    }


def valid_output() -> dict:
    units = source_units()
    overview_id, procedure_id, procedure_id_2, reference_id = [
        row["source_unit_id"] for row in units
    ]
    return {
        "schema": "rock-kb-source-knowledge-distillation-v2.3",
        "variant_id": "source_knowledge_distillation_v2_3",
        "articles": [
            {
                "candidate_id": "source-native-candidate:test",
                "source_input_hash": "a" * 64,
                "unit_decisions": [
                    {
                        "source_unit_id": overview_id,
                        "disposition": "claim",
                        "existing_relation": "novel",
                        "related_existing_claim_ids": [],
                        "evidence_summary": "The feature has a documented behavior.",
                        "decision_reason": "The statement is independently answerable.",
                        "mixed_material": False,
                    },
                    {
                        "source_unit_id": procedure_id,
                        "disposition": "task_card",
                        "existing_relation": "novel",
                        "related_existing_claim_ids": [],
                        "evidence_summary": "The article gives an ordered setup procedure.",
                        "decision_reason": "Ordered actions belong in a task card.",
                        "mixed_material": False,
                    },
                    {
                        "source_unit_id": procedure_id_2,
                        "disposition": "task_card",
                        "existing_relation": "novel",
                        "related_existing_claim_ids": [],
                        "evidence_summary": "The article gives an ordered setup procedure.",
                        "decision_reason": "Ordered actions belong in a task card.",
                        "mixed_material": False,
                    },
                    {
                        "source_unit_id": reference_id,
                        "disposition": "structured_reference",
                        "existing_relation": "novel",
                        "related_existing_claim_ids": [],
                        "evidence_summary": "The article defines an exact setting.",
                        "decision_reason": "The table is an exact lookup reference.",
                        "mixed_material": False,
                    },
                ],
                "artifacts": [
                    {
                        "artifact_key": "feature-behavior",
                        "artifact_type": "claim",
                        "source_unit_ids": [overview_id],
                        "title": "Feature behavior",
                        "retrieval_text": "The feature provides the documented behavior when it is enabled.",
                        "independent_question": "What behavior does the feature provide?",
                        "rationale": "The opening paragraph directly supports this rule.",
                        "concept_ids": ["system-admin-ops"],
                        "claim_type": "behavior",
                        "evidence_class": "current_behavior",
                        "confidence": "high",
                        "payload": {
                            "summary": "The feature provides a durable documented behavior.",
                        },
                    },
                    {
                        "artifact_key": "configure-feature",
                        "artifact_type": "task_card",
                        "source_unit_ids": [procedure_id, procedure_id_2],
                        "title": "Configure the feature",
                        "retrieval_text": "Configure the feature from its settings page and enable its provider.",
                        "independent_question": "How do I configure the feature?",
                        "rationale": "The ordered list supplies the complete setup sequence.",
                        "concept_ids": ["system-admin-ops"],
                        "temporal_status": "release_sensitive",
                        "payload": {
                            "summary": "Configure the feature through its documented settings.",
                            "steps": [
                                {"order": 1, "instruction": "Open the settings page."},
                                {"order": 2, "instruction": "Enable the provider."},
                            ],
                        },
                    },
                    {
                        "artifact_key": "feature-settings",
                        "artifact_type": "structured_reference",
                        "source_unit_ids": [reference_id],
                        "title": "Feature settings",
                        "retrieval_text": "The Enabled setting controls whether indexing is allowed.",
                        "independent_question": "What does the Enabled setting control?",
                        "rationale": "The settings table defines the option semantics.",
                        "concept_ids": ["system-admin-ops"],
                        "temporal_status": "release_sensitive",
                        "payload": {
                            "summary": "Reference for the feature's documented setting.",
                            "reference_items": [
                                {
                                    "label": "Enabled",
                                    "detail": "Allows indexing.",
                                    "value_status": "documented_behavior",
                                    "needs_verification": False,
                                }
                            ],
                        },
                    },
                ],
                "verification_requests": [],
                "unmatched_routing_terms": [],
                "review_notes": ["Every structural unit received one primary representation."],
                "coverage_check": {
                    "material_unit_count": 4,
                    "captured_source_unit_ids": [
                        overview_id,
                        procedure_id,
                        procedure_id_2,
                        reference_id,
                    ],
                    "no_artifact_source_unit_ids": [],
                    "omitted_source_units": [],
                },
            }
        ],
    }


def test_parser_preserves_stable_block_types_and_private_text():
    units = source_units()

    assert [row["unit_kind"] for row in units] == [
        "paragraph",
        "list_item",
        "list_item",
        "table",
    ]
    assert [row["ordinal"] for row in units] == [1, 2, 3, 4]
    assert units[1]["heading_path"] == ["Configure"]
    assert units[3]["locator"]["kind"] == "table"
    assert all(row["normalized_content_hash"] for row in units)
    assert all(row["text"] for row in units)


def test_parser_splits_mixed_paragraphs_into_addressable_sentences():
    units = parse_markdown_source_units(
        markdown=(
            "Enable auditing from Global Attributes. "
            "Enabling it materially affects performance. "
            "Use it only for brief periods."
        ),
        source_snapshot_id="source-snapshot:test",
        source_record_id="rock_documentation:article:101",
        source_url="https://community.rockrms.com/documentation/audit",
        source_title="Audit",
    )

    assert len(units) == 3
    assert [row.locator.value for row in units] == [
        "Overview / paragraph-1",
        "Overview / paragraph-2",
        "Overview / paragraph-3",
    ]
    assert len({row.source_unit_id for row in units}) == 3


def test_parser_splits_top_level_contrast_but_not_parenthetical_semicolon():
    units = parse_markdown_source_units(
        markdown=(
            "Businesses appear separately in results for filtering "
            "(sometimes you want them; sometimes you do not) but when "
            "configuring indexing, they share settings with people."
        ),
        source_snapshot_id="source-snapshot:test",
        source_record_id="rock_documentation:article:1017",
        source_url="https://community.rockrms.com/documentation/search",
        source_title="Search",
    )

    assert [row.text for row in units] == [
        (
            "Businesses appear separately in results for filtering "
            "(sometimes you want them; sometimes you do not)."
        ),
        "When configuring indexing, they share settings with people.",
    ]


def test_parser_splits_list_items_and_links_nested_catalog_to_parent():
    units = parse_markdown_source_units(
        markdown=(
            "* **Family:** One label prints per check-in session.\n"
            "  + `Family` (type Group)\n"
            "  + `CheckInDateTime` (type DateTime)\n"
            "* **Person Location:** One label prints for every person.\n"
        ),
        source_snapshot_id="source-snapshot:test",
        source_record_id="rock_documentation:article:102",
        source_url="https://community.rockrms.com/documentation/labels",
        source_title="Labels",
    )

    assert [row.unit_kind for row in units] == [
        "list_item",
        "list_item",
        "list_item",
    ]
    assert units[1].parent_source_unit_id == units[0].source_unit_id
    assert units[0].context == "Family"
    assert units[2].context == "Person Location"


def test_reviewed_split_rule_creates_addressable_child_units():
    source_record_id = "rock_documentation:article:split-test"
    markdown = (
        "1. **Inherited Permissions** - Items inherit from parents. "
        "Add item permissions only for a narrower override. "
        "Parent changes cascade to children."
    )
    unsplit = parse_markdown_source_units(
        markdown=markdown,
        source_snapshot_id="source-snapshot:split-test",
        source_record_id=source_record_id,
        source_url="https://community.rockrms.com/documentation/split-test",
        source_title="Split Test",
    )

    split = apply_source_unit_split_rules(
        [
            {
                "kind": "list_item",
                "heading_path": [],
                "context_label": "Inherited Permissions",
                "block_token": "list:0:1",
                "text": markdown,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": unsplit[0].normalized_content_hash,
                "strategy": "sentence",
            }
        ],
    )

    assert [row["kind"] for row in split] == [
        "list_item",
        "paragraph",
        "paragraph",
    ]
    assert split[1]["parent_block_token"] == split[0]["block_token"]
    assert split[0]["text"].startswith("1. **Inherited Permissions**")


def test_reviewed_split_rule_handles_joined_paragraph_sentences():
    source_record_id = "rock_documentation:article:paragraph-split-test"
    paragraph = (
        "It appears at the bottom by default."
        "Mailgun tracking must be disabled."
    )
    paragraph_hash = sha256_text(" ".join(paragraph.split()))
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Unsubscribe HTML",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": paragraph_hash,
                "strategy": "sentence",
            },
        ],
    )

    assert [row["text"] for row in split] == [
        "It appears at the bottom by default.",
        "Mailgun tracking must be disabled.",
    ]


def test_reviewed_split_rule_handles_exact_contrast_clause():
    source_record_id = "rock_mobile_docs:article:contrast-test"
    paragraph = (
        "Hosting under your account gives you complete control, but you must "
        "grant the publisher access to release the app."
    )
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Developer Accounts",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": sha256_text(paragraph),
                "strategy": "contrast_clause",
            }
        ],
    )

    assert [row["text"] for row in split] == [
        "Hosting under your account gives you complete control.",
        "You must grant the publisher access to release the app.",
    ]


def test_reviewed_split_rule_handles_leading_while_contrast_clause():
    source_record_id = "rock_documentation:article:while-test"
    paragraph = (
        "While you can email these errors (see `Admin > Settings`), you can "
        "also view their history here."
    )
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Exceptions",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": sha256_text(paragraph),
                "strategy": "contrast_clause",
            }
        ],
    )

    assert [row["text"] for row in split] == [
        "You can email these errors (see `Admin > Settings`).",
        "You can view their history here.",
    ]


def test_reviewed_split_rule_handles_shared_subject_and_clause():
    source_record_id = "rock_documentation:article:shared-subject-test"
    paragraph = (
        "Once created, they are stored as a defined value of the Cache Tag "
        "Defined Type and can't be deleted."
    )
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Cache Tags",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": sha256_text(paragraph),
                "strategy": "shared_subject_and_clause",
            }
        ],
    )

    assert [row["text"] for row in split] == [
        "Once created, they are stored as a defined value of the Cache Tag Defined Type.",
        "They can't be deleted.",
    ]


def test_reviewed_split_rule_handles_causal_clause():
    source_record_id = "rock_documentation:article:causal-test"
    paragraph = (
        "Enabling statistics restarts Rock, so it is best to do this during "
        "low site activity."
    )
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Statistics",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": sha256_text(paragraph),
                "strategy": "causal_clause",
            }
        ],
    )

    assert [row["text"] for row in split] == [
        "Enabling statistics restarts Rock.",
        "It is best to do this during low site activity.",
    ]


def test_reviewed_split_rule_preserves_closing_markdown_before_joined_text():
    source_record_id = "rock_documentation:article:markdown-split-test"
    paragraph = "**Where Did It Go?**Each night, the cleanup job runs."
    split = apply_source_unit_split_rules(
        [
            {
                "kind": "paragraph",
                "heading_path": [],
                "context_label": "Cleanup",
                "block_token": "paragraph:0:1",
                "text": paragraph,
            }
        ],
        source_record_id=source_record_id,
        split_rules=[
            {
                "source_record_id": source_record_id,
                "source_unit_content_hash": sha256_text(paragraph),
                "strategy": "sentence",
            }
        ],
    )

    assert [row["text"] for row in split] == [
        "**Where Did It Go?**",
        "Each night, the cleanup job runs.",
    ]


def test_split_rule_file_requires_review_provenance(tmp_path: Path):
    split_rules_path = tmp_path / "split-rules.jsonl"
    write_jsonl(
        split_rules_path,
        [
            {
                "schema": "rock-kb-source-unit-split-rule-v1",
                "source_record_id": "rock_documentation:article:100",
                "source_unit_content_hash": "a" * 64,
                "strategy": "sentence",
                "review_reason": "The upstream block contains two independent facts.",
            }
        ],
    )

    with pytest.raises(ValueError, match="missing reviewed_by"):
        load_source_unit_split_rules(split_rules_path)


def test_parser_marks_repeated_text_without_dropping_source_locators():
    units = parse_markdown_source_units(
        markdown=(
            "# First Surface\n\n"
            "Content Channel Item permissions are not enforced.\n\n"
            "# Second Surface\n\n"
            "Content Channel Item permissions are not enforced.\n"
        ),
        source_snapshot_id="source-snapshot:test",
        source_record_id="rock_documentation:article:103",
        source_url="https://community.rockrms.com/documentation/kiosk",
        source_title="Kiosk Ads",
    )

    assert len(units) == 2
    assert units[0].duplicate_text_of_source_unit_id is None
    assert (
        units[1].duplicate_text_of_source_unit_id
        == units[0].source_unit_id
    )
    assert units[0].locator.value != units[1].locator.value


def test_source_observation_preserves_change_time_for_unchanged_content():
    unchanged = source_observation_metadata(
        previous={
            "normalized_content_hash": "a" * 64,
            "observed_at": "2026-07-01T00:00:00+00:00",
            "content_changed_at": "2026-07-01T00:00:00+00:00",
        },
        checked_at="2026-07-30T00:00:00+00:00",
        content_hash="a" * 64,
    )
    changed = source_observation_metadata(
        previous={"normalized_content_hash": "a" * 64},
        checked_at="2026-07-30T00:00:00+00:00",
        content_hash="b" * 64,
    )

    assert unchanged == {
        "observed_at": "2026-07-01T00:00:00+00:00",
        "content_changed_at": "2026-07-01T00:00:00+00:00",
        "observation_status": "unchanged",
    }
    assert changed["observation_status"] == "changed"
    assert changed["content_changed_at"] == "2026-07-30T00:00:00+00:00"


def test_candidate_build_can_target_one_prose_source_family(tmp_path: Path):
    developer_record = {
        **document_record(),
        "id": "rock_developer:article:200",
        "source_id": "rock_developer",
        "source_url": "https://community.rockrms.com/developer/obsidian/components",
        "source_title": "Obsidian Components",
        "documentation_path": "developer/obsidian/components",
        "documentation_branches": ["developer/obsidian"],
        "documentation_article_id": 200,
    }
    destination = tmp_path / "candidate"
    empty = tmp_path / "empty"
    empty.mkdir()

    result = build_source_native_document_candidates(
        concept_ids=["obsidian-development"],
        source_ids=["rock_developer"],
        limit_per_concept=1,
        destination=destination,
        previous_dir=empty,
        records=[document_record(), developer_record],
        markdown_loader=lambda _record: (
            "# Components\n\nObsidian components expose typed properties and "
            "events for Rock blocks."
        ),
    )

    assert result["source_ids"] == ["rock_developer"]
    snapshot = next(read_jsonl(destination / "source-snapshots.jsonl"))
    assert snapshot["source_id"] == "rock_developer"
    assert snapshot["parser_id"] == "rockumentation-markdown-blocks"


def test_static_prose_candidate_coalesces_concept_facets(tmp_path: Path):
    record = {
        **document_record(),
        "id": "rock_community_blog:ai-mobile",
        "source_id": "rock_community_blog",
        "source_url": "https://community.rockrms.com/connect/ai-mobile",
        "source_title": "AI Agents in Rock Mobile",
        "summary": (
            "Rock Mobile AI agents support automation and mobile ministry "
            "workflows in the current product preview."
        ),
        "documentation_path": None,
        "documentation_branches": [],
        "documentation_article_id": None,
    }
    destination = tmp_path / "candidate"
    empty = tmp_path / "empty"
    empty.mkdir()

    result = build_source_native_document_candidates(
        concept_ids=["ai-agents-automation", "mobile"],
        source_ids=["rock_community_blog"],
        source_record_ids=[record["id"]],
        limit_per_concept=1,
        destination=destination,
        previous_dir=empty,
        records=[document_record(), record],
        markdown_loader=lambda _record: (
            "# AI Agents in Rock Mobile\n\nThe preview combines mobile "
            "ministry workflows with configured AI agent automation."
        ),
    )

    assert result["article_count"] == 1
    assert result["source_record_ids"] == [record["id"]]
    candidate = next(read_jsonl(destination / "distillation-input.jsonl"))
    assert candidate["concept_ids"] == ["ai-agents-automation", "mobile"]


def test_unchanged_candidate_refresh_preserves_ids_and_change_time(
    tmp_path: Path,
):
    empty = tmp_path / "empty"
    first = tmp_path / "first"
    second = tmp_path / "second"
    empty.mkdir()
    first_checked = "2026-07-01T00:00:00+00:00"
    second_checked = "2026-07-30T00:00:00+00:00"

    build_source_native_document_candidates(
        concept_ids=["system-admin-ops"],
        limit_per_concept=1,
        destination=first,
        previous_dir=empty,
        checked_at=first_checked,
        records=[document_record()],
        payload_loader=lambda _record: rockumentation_payload(),
    )
    build_source_native_document_candidates(
        concept_ids=["system-admin-ops"],
        limit_per_concept=1,
        destination=second,
        previous_dir=first,
        checked_at=second_checked,
        records=[document_record()],
        payload_loader=lambda _record: rockumentation_payload(),
    )

    first_snapshot = list(read_jsonl(first / "source-snapshots.jsonl"))[0]
    second_snapshot = list(read_jsonl(second / "source-snapshots.jsonl"))[0]
    first_units = list(read_jsonl(first / "source-units.private.jsonl"))
    second_units = list(read_jsonl(second / "source-units.private.jsonl"))
    assert second_snapshot["source_snapshot_id"] == first_snapshot["source_snapshot_id"]
    assert [row["source_unit_id"] for row in second_units] == [
        row["source_unit_id"] for row in first_units
    ]
    assert second_snapshot["observed_at"] == first_checked
    assert second_snapshot["content_changed_at"] == first_checked
    assert second_snapshot["last_checked_at"] == second_checked
    assert second_snapshot["observation_status"] == "unchanged"

    artifact = {
        "artifact_id": "source-native:claim:test-cache",
        "artifact": {"source_unit_ids": [first_units[0]["source_unit_id"]]},
    }
    for destination, units in ((first, first_units), (second, second_units)):
        write_jsonl(destination / "source-units.jsonl", units)
        write_jsonl(destination / "reviewed-artifacts.jsonl", [artifact])
    report = build_source_native_impact_report(
        previous_dir=first,
        current_dir=second,
    )
    assert report["status"] == "unchanged"
    assert report["revalidation_queue"] == {
        "knowledge_unit_ids": [],
        "removed_or_prior_knowledge_unit_ids": [],
        "projection_targets": [],
    }


def test_model_input_hash_covers_stable_review_context_not_check_time():
    source_input = distillation_input()
    snapshot = SourceSnapshot.model_validate(source_input["source_snapshot"])
    units = [SourceUnit.model_validate(row) for row in source_input["source_units"]]

    def digest(
        selected_snapshot: SourceSnapshot,
        *,
        claims: list[dict] | None = None,
    ) -> str:
        return source_native_model_input_hash(
            snapshot=selected_snapshot,
            source_units=units,
            concept_ids=source_input["concept_ids"],
            existing_claims=claims or source_input["existing_claims"],
            documentation_path=source_input.get("documentation_path"),
            documentation_branches=source_input.get("documentation_branches") or [],
            documentation_current_version=source_input.get(
                "documentation_current_version"
            ),
        )

    baseline = digest(snapshot)
    assert digest(
        snapshot.model_copy(update={"last_checked_at": "2026-08-01T00:00:00Z"})
    ) == baseline
    assert digest(
        snapshot.model_copy(update={"parser_version": "next-parser-version"})
    ) != baseline
    assert digest(
        snapshot,
        claims=[
            {
                "claim_id": "claim:changed-context",
                "claim": "A materially changed existing claim.",
            }
        ],
    ) != baseline
def test_source_snapshot_rejects_private_or_parent_routing_paths():
    base = {
        "schema": "rock-kb-source-snapshot-v2",
        "source_snapshot_id": "source-snapshot:test",
        "source_id": "rock_documentation",
        "source_record_id": "rock_documentation:article:100",
        "authority_tier": "official",
        "public_policy": "cite_and_summarize_only",
    }

    with pytest.raises(ValidationError, match="source_path"):
        SourceSnapshot.model_validate(
            {**base, "source_path": "/Users/private/article"}
        )
    with pytest.raises(ValidationError, match="routing_paths"):
        SourceSnapshot.model_validate(
            {**base, "routing_paths": ["documentation/../private"]}
        )


def test_generated_response_schema_requires_every_declared_property(tmp_path: Path):
    destination = tmp_path / "schema.json"
    write_source_native_distillation_schema(destination)
    schema = json.loads(destination.read_text())

    def assert_strict(node):
        if isinstance(node, dict):
            if isinstance(node.get("properties"), dict):
                assert set(node["required"]) == set(node["properties"])
                assert node["additionalProperties"] is False
            for value in node.values():
                assert_strict(value)
        elif isinstance(node, list):
            for value in node:
                assert_strict(value)

    assert_strict(schema)


def test_v23_validator_requires_exact_coverage_and_one_primary_artifact():
    output = valid_output()
    validated = validate_source_native_distillation(
        output,
        inputs=[distillation_input()],
        require_promotable=True,
    )
    assert len(validated.articles[0].artifacts) == 3

    output["articles"][0]["artifacts"][1]["source_unit_ids"] = output[
        "articles"
    ][0]["artifacts"][0]["source_unit_ids"]
    with pytest.raises(ValueError, match="type does not match disposition"):
        validate_source_native_distillation(
            output,
            inputs=[distillation_input()],
        )


def test_v23_validator_requires_explicit_requests_for_verification_flags():
    output = valid_output()
    output["articles"][0]["artifacts"][0]["needs_live_verification"] = True

    with pytest.raises(ValueError, match="verification flag"):
        validate_source_native_distillation(
            output,
            inputs=[distillation_input()],
        )


def test_v23_schema_rejects_procedure_shadowed_as_claim():
    output = valid_output()
    claim = output["articles"][0]["artifacts"][0]
    claim["retrieval_text"] = (
        "Step 1 open settings. Step 2 enable the provider."
    )

    with pytest.raises(ValidationError, match="procedural text"):
        SourceNativeDistillationOutput.model_validate(output)


def test_promotion_strips_source_text_and_records_generation(tmp_path: Path):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "public"
    write_jsonl(input_path, [distillation_input()])
    output = valid_output()
    units = source_units()
    output["articles"][0]["artifacts"][1]["related_artifact_links"] = [
        {
            "target_artifact_key": "feature-behavior",
            "relation": "requires",
            "rationale": (
                "The configuration procedure requires the documented "
                "feature behavior."
            ),
            "evidence_source_unit_ids": [units[0]["source_unit_id"]],
        }
    ]
    output_path.write_text(json.dumps(output), encoding="utf-8")

    result = promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
        generation_prompt_version="2.3.0",
        generated_at="2026-07-29T12:00:00+00:00",
    )

    assert result["reviewed_artifact_count"] == 3
    activities = list(read_jsonl(destination / "generation-activities.jsonl"))
    assert len(activities) == 1
    assert activities[0]["prompt_version"] == "2.3.0"
    assert activities[0]["created_at"] == "2026-07-29T12:00:00+00:00"
    assert activities[0]["parameters"]["review_contract_version"] == "2.3.1"
    public_units = list(read_jsonl(destination / "source-units.jsonl"))
    assert all("text" not in row for row in public_units)
    assert all(row["public_summary"] for row in public_units)
    relationships = list(read_jsonl(destination / "relationships.jsonl"))
    assert len(relationships) == 1
    assert relationships[0]["relation"] == "requires"
    assert relationships[0]["from_id"].endswith(":configure-feature")
    assert relationships[0]["to_id"].endswith(":feature-behavior")
    evaluations = list(read_jsonl(destination / "evaluation-set.jsonl"))
    assert len(evaluations) == 3
    assert all(row["expected_result_ids"] for row in evaluations)
    manifest = json.loads((destination / "manifest.json").read_text())
    assert manifest["status"] == "canonical_input"
    assert manifest["public_retrieval_changed"] is False
    assert manifest["evaluation_case_count"] == 3


def test_promotion_appends_safely_and_records_review_corrections(tmp_path: Path):
    input_path = tmp_path / "input.jsonl"
    generated_path = tmp_path / "generated.json"
    reviewed_path = tmp_path / "reviewed.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    generated = valid_output()
    reviewed = valid_output()
    reviewed["articles"][0]["review_notes"].append(
        "Maintainer confirmed the artifact boundaries."
    )
    reviewed["articles"][0]["artifacts"][0]["needs_live_verification"] = True
    reviewed["articles"][0]["verification_requests"] = [
        {
            "source_unit_ids": [source_units()[0]["source_unit_id"]],
            "verification_surface": "public_source_code",
            "question": "Does current public source retain this behavior?",
            "why_material": (
                "The answer determines whether the release-sensitive artifact "
                "can be used without a verification caveat."
            ),
        }
    ]
    generated_path.write_text(json.dumps(generated), encoding="utf-8")
    reviewed_path.write_text(json.dumps(reviewed), encoding="utf-8")

    promote_source_native_distillation(
        input_path=input_path,
        output_path=reviewed_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
        generated_output_path=generated_path,
    )
    write_jsonl(
        destination / "evaluation-holdout.jsonl",
        [
            {
                "schema": "rock-kb-service-evaluation-case-v1",
                "id": "source-native-holdout:append",
                "question": "What behavior does the feature provide?",
                "concept_id": "system-admin-ops",
                "source": "source_native_pilot_manual_paraphrase",
                "evaluation_mode": "retrieval",
                "expected_result_ids": [
                    "source-native:claim:rock_documentation:"
                    "article-100:feature-behavior"
                ],
                "expected_result_kinds": ["claim"],
                "required_authority_tiers": ["official"],
                "max_rank": 5,
            }
        ],
    )
    write_source_native_manifest(destination)

    result = promote_source_native_distillation(
        input_path=input_path,
        output_path=reviewed_path,
        destination=destination,
        base_dir=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-31T12:00:00+00:00",
        generated_output_path=generated_path,
    )

    assert result["reviewed_artifact_count"] == 3
    assert len(list(read_jsonl(destination / "source-snapshots.jsonl"))) == 1
    assert len(list(read_jsonl(destination / "evaluation-holdout.jsonl"))) == 1
    verification_rows = list(read_jsonl(destination / "verification-queue.jsonl"))
    assert len(verification_rows) == 1
    assert verification_rows[0]["artifact_ids"] == [
        "source-native:claim:rock_documentation:article-100:feature-behavior"
    ]
    activity = next(read_jsonl(destination / "generation-activities.jsonl"))
    assert activity["prompt_version"] == "2.3.1"
    assert activity["parameters"]["review_changed"] is True
    assert activity["parameters"]["review_correction_count"] > 0
    manifest = json.loads((destination / "manifest.json").read_text())
    assert manifest["article_count"] == 1
    assert manifest["verification_request_count"] == 1
    assert manifest["review_changed_article_count"] == 1


@pytest.mark.parametrize("in_place", [False, True])
def test_promotion_drops_resolutions_for_replaced_verification_requests(
    tmp_path: Path,
    in_place: bool,
):
    input_path = tmp_path / "input.jsonl"
    reviewed_path = tmp_path / "reviewed.json"
    base = tmp_path / "base"
    write_jsonl(input_path, [distillation_input()])
    reviewed = valid_output()
    reviewed["articles"][0]["artifacts"][0]["needs_live_verification"] = True
    reviewed["articles"][0]["verification_requests"] = [
        {
            "source_unit_ids": [source_units()[0]["source_unit_id"]],
            "verification_surface": "public_source_code",
            "question": "Does current public source retain this behavior?",
            "why_material": (
                "The release-sensitive behavior changes the recommended "
                "implementation."
            ),
        }
    ]
    reviewed_path.write_text(json.dumps(reviewed), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=reviewed_path,
        destination=base,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )
    queue_row = next(read_jsonl(base / "verification-queue.jsonl"))
    write_jsonl(
        base / "verification-resolutions.jsonl",
        [
            {
                "schema": "rock-kb-source-native-verification-resolution-v1",
                "verification_id": queue_row["verification_id"],
                "queue_item_hash": "a" * 64,
                "resolution_state": "not_verified",
                "finding": "The prior verification request was not resolved.",
                "reviewer": "test-reviewer",
                "reviewed_at": "2026-07-30T12:00:00+00:00",
                "revalidation_policy": "source_hash_change",
            }
        ],
    )

    reviewed_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    destination = base if in_place else tmp_path / "refreshed"
    promote_source_native_distillation(
        input_path=input_path,
        output_path=reviewed_path,
        destination=destination,
        base_dir=base,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-31T12:00:00+00:00",
    )

    assert list(read_jsonl(destination / "verification-queue.jsonl")) == []
    assert list(read_jsonl(destination / "verification-resolutions.jsonl")) == []
    manifest = json.loads((destination / "manifest.json").read_text())
    assert manifest["verification_request_count"] == 0
    assert manifest["verification_resolution_count"] == 0


def test_manual_holdout_is_hashed_and_loaded_with_generated_evaluations(
    tmp_path: Path,
):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    output_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )
    write_jsonl(
        destination / "evaluation-holdout.jsonl",
        [
            {
                "schema": "rock-kb-service-evaluation-case-v1",
                "id": "source-native-holdout:test",
                "question": "How does the feature behave in other words?",
                "concept_id": "system-admin-ops",
                "source": "source_native_pilot_manual_paraphrase",
                "evaluation_mode": "retrieval",
                "expected_result_ids": [
                    "source-native:claim:rock_documentation:"
                    "article-100:feature-behavior"
                ],
                "expected_result_kinds": ["claim"],
                "required_authority_tiers": ["official"],
                "max_allowed_rank": 5,
            }
        ],
    )
    manifest = write_source_native_manifest(destination)

    assert manifest.evaluation_case_count == 4
    assert "evaluation-holdout.jsonl" in manifest.file_hashes
    assert len(source_native_evaluation_rows(tmp_path)) == 4


def test_manifest_rejects_holdouts_for_removed_artifacts(tmp_path: Path):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    output_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )
    write_jsonl(
        destination / "evaluation-holdout.jsonl",
        [
            {
                "schema": "rock-kb-service-evaluation-case-v1",
                "id": "source-native-holdout:stale",
                "question": "What happened to the removed artifact?",
                "concept_id": "system-admin-ops",
                "source": "source_native_manual_paraphrase",
                "evaluation_mode": "retrieval",
                "expected_result_ids": ["source-native:claim:removed"],
                "expected_result_kinds": ["claim"],
                "required_authority_tiers": ["official"],
                "max_rank": 5,
            }
        ],
    )

    with pytest.raises(ValueError, match="missing reviewed artifacts"):
        write_source_native_manifest(destination)


def test_final_bundle_rejects_verification_flags_missing_from_queue(
    tmp_path: Path,
):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    output_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )
    artifacts = list(read_jsonl(destination / "reviewed-artifacts.jsonl"))
    artifacts[0]["artifact"]["needs_live_verification"] = True

    with pytest.raises(ValueError, match="absent from the queue"):
        validate_source_native_bundle_consistency(
            {
                "reviewed-artifacts.jsonl": artifacts,
                "source-units.jsonl": list(
                    read_jsonl(destination / "source-units.jsonl")
                ),
                "verification-queue.jsonl": [],
            }
        )


def test_final_bundle_rejects_cross_candidate_verification_links():
    artifact = {
        "schema": "rock-kb-reviewed-source-native-artifact-v1",
        "artifact_id": "source-native:claim:test",
        "source_candidate_id": "source-native-candidate:first",
        "generation_activity_id": "generation:test",
        "artifact": valid_output()["articles"][0]["artifacts"][0],
        "review_state": "reviewer_approved",
        "reviewer": "test-reviewer",
        "reviewed_at": "2026-08-01T00:00:00Z",
        "review_notes": ["Reviewed for test coverage."],
        "source_input_hash": "a" * 64,
    }
    artifact["artifact"]["needs_live_verification"] = True
    source_unit_id = artifact["artifact"]["source_unit_ids"][0]
    queue = {
        "schema": "rock-kb-source-native-verification-request-v1",
        "verification_id": "source-native-verification:test",
        "source_candidate_id": "source-native-candidate:second",
        "artifact_ids": [artifact["artifact_id"]],
        "concept_ids": ["system-admin-ops"],
        "source_unit_ids": [source_unit_id],
        "verification_surface": "public_source_code",
        "question": "Does current public source retain this behavior?",
        "why_material": "The behavior changes the recommended implementation.",
    }
    unit = next(
        row for row in source_units() if row["source_unit_id"] == source_unit_id
    )

    with pytest.raises(ValueError, match="different source candidates"):
        validate_source_native_bundle_consistency(
            {
                "reviewed-artifacts.jsonl": [artifact],
                "source-units.jsonl": [unit],
                "verification-queue.jsonl": [queue],
            }
        )


def test_prompt_can_target_a_stable_source_record_after_candidate_id_changes(
    tmp_path: Path,
):
    first = distillation_input()
    second = json.loads(json.dumps(first))
    second["candidate_id"] = "source-native-candidate:second"
    second["source_snapshot"]["source_record_id"] = (
        "rock_documentation:article:second"
    )
    input_path = tmp_path / "input.jsonl"
    destination = tmp_path / "prompt.txt"
    write_jsonl(input_path, [first, second])

    result = write_source_native_generation_prompt(
        input_path=input_path,
        destination=destination,
        source_record_id="rock_documentation:article:second",
    )

    prompt = destination.read_text(encoding="utf-8")
    assert result["candidate_count"] == 1
    assert "source-native-candidate:second" in prompt
    assert "source-native-candidate:test" not in prompt
    with pytest.raises(ValueError, match="mutually exclusive"):
        write_source_native_generation_prompt(
            input_path=input_path,
            destination=destination,
            candidate_id="source-native-candidate:second",
            source_record_id="rock_documentation:article:second",
        )


def test_prompt_fails_closed_when_article_exceeds_response_contract(
    tmp_path: Path,
):
    candidate = distillation_input()
    template = candidate["source_units"][0]
    candidate["source_units"] = [
        {
            **template,
            "source_unit_id": f"source-unit:oversized:{index}",
        }
        for index in range(201)
    ]
    input_path = tmp_path / "input.jsonl"
    destination = tmp_path / "prompt.txt"
    write_jsonl(input_path, [candidate])

    with pytest.raises(ValueError, match="deterministic partitioning"):
        write_source_native_generation_prompt(
            input_path=input_path,
            destination=destination,
        )


def test_merge_orders_batches_by_canonical_input_and_runs_semantic_gate(
    tmp_path: Path,
):
    input_path = tmp_path / "input.jsonl"
    batch_path = tmp_path / "batch.json"
    destination = tmp_path / "merged.json"
    write_jsonl(input_path, [distillation_input()])
    batch_path.write_text(json.dumps(valid_output()), encoding="utf-8")

    result = merge_source_native_distillation_outputs(
        input_path=input_path,
        batch_paths=[batch_path],
        destination=destination,
    )

    assert result["article_count"] == 1
    assert result["artifact_count"] == 3
    assert json.loads(destination.read_text())["articles"][0][
        "candidate_id"
    ] == "source-native-candidate:test"


def test_merge_can_preserve_split_feedback_for_private_review(tmp_path: Path):
    input_path = tmp_path / "input.jsonl"
    batch_path = tmp_path / "batch.json"
    destination = tmp_path / "merged.json"
    write_jsonl(input_path, [distillation_input()])
    blocked = valid_output()
    article = blocked["articles"][0]
    blocked_unit_id = article["unit_decisions"][0]["source_unit_id"]
    article["unit_decisions"][0].update(
        {
            "disposition": "split_required",
            "mixed_material": True,
            "decision_reason": (
                "The source unit combines facts that require maintainer review."
            ),
        }
    )
    article["artifacts"] = article["artifacts"][1:]
    article["coverage_check"]["material_unit_count"] = 3
    article["coverage_check"]["captured_source_unit_ids"] = article[
        "coverage_check"
    ]["captured_source_unit_ids"][1:]
    article["coverage_check"]["omitted_source_units"] = [
        {
            "source_unit_id": blocked_unit_id,
            "reason": "The source unit requires an exact maintainer disposition.",
        }
    ]
    article["verification_requests"] = [
        {
            "source_unit_ids": [blocked_unit_id],
            "verification_surface": "maintainer_review",
            "question": "Does this unit require a deterministic source split?",
            "why_material": (
                "The answer determines whether the unit can receive one "
                "reviewed primary representation."
            ),
        }
    ]
    batch_path.write_text(json.dumps(blocked), encoding="utf-8")

    with pytest.raises(ValueError, match="requires deterministic source-unit splits"):
        merge_source_native_distillation_outputs(
            input_path=input_path,
            batch_paths=[batch_path],
            destination=destination,
        )

    result = merge_source_native_distillation_outputs(
        input_path=input_path,
        batch_paths=[batch_path],
        destination=destination,
        allow_review_blockers=True,
    )

    assert result["status"] == "review_required"
    assert result["split_required_count"] == 1
    assert json.loads(destination.read_text())["articles"][0][
        "coverage_check"
    ]["omitted_source_units"] == [
        {
            "reason": "The source unit requires an exact maintainer disposition.",
            "source_unit_id": blocked_unit_id,
        }
    ]


def test_promoted_bundle_compiles_into_canonical_projection_input(tmp_path: Path):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    output_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )

    bundle, summary = build_canonical_knowledge_bundle(
        search_rows=[],
        distilled_claims=[],
        include_source_native_pilot=True,
        repo_root=tmp_path,
    )

    assert len(bundle.knowledge_units) == 3
    assert len(bundle.generation_activities) == 1
    assert len(bundle.evidence_links) == 4
    assert {row.knowledge_type for row in bundle.knowledge_units} == {
        "claim",
        "task_card",
        "structured_reference",
    }
    assert summary["public_retrieval_changed"] is False
    assert summary["input"]["source_native_reviewed_artifacts"] == 3


def test_source_native_relationship_resolves_existing_public_alias(
    tmp_path: Path,
):
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.json"
    destination = tmp_path / "canonical" / "source-native" / "v1"
    write_jsonl(input_path, [distillation_input()])
    output_path.write_text(json.dumps(valid_output()), encoding="utf-8")
    promote_source_native_distillation(
        input_path=input_path,
        output_path=output_path,
        destination=destination,
        reviewer="test-reviewer",
        model="test-model",
        reviewed_at="2026-07-30T12:00:00+00:00",
    )
    write_jsonl(
        destination / "relationships.jsonl",
        [
            {
                "schema": "rock-kb-knowledge-relationship-v1",
                "relationship_id": "relationship:test",
                "from_id": (
                    "source-native:claim:rock_documentation:"
                    "article-100:feature-behavior"
                ),
                "to_id": "recipe:test-legacy",
                "relation": "applies_to",
                "decision": "accept",
                "confidence": "high",
                "rationale": "The reviewed behavior applies to this recipe.",
                "evidence_source_unit_ids": [
                    source_units()[0]["source_unit_id"]
                ],
            }
        ],
    )
    write_source_native_manifest(destination)
    recipe_row = {
        "id": "recipe:test",
        "legacy_ids": ["recipe:test-legacy"],
        "kind": "recipe",
        "title": "Test Recipe",
        "body": "A reviewed recipe.",
        "concepts": ["system-admin-ops"],
        "topics": [],
        "authority_tier": "community-reviewed",
        "source_id": "test",
        "payload": {
            "schema": "rock-kb-recipe-v1",
            "recipe_id": "test",
            "review_status": "community_reviewed",
            "implementation": {"commit_sha": "a" * 40},
            "updated_at": "2026-07-31",
        },
    }

    bundle, _summary = build_canonical_knowledge_bundle(
        search_rows=[recipe_row],
        distilled_claims=[],
        include_source_native_pilot=True,
        repo_root=tmp_path,
    )

    relationship = next(
        row
        for row in bundle.relationships
        if row.relation == "applies_to"
    )
    assert relationship.to_id == "recipe:test"


def test_impact_report_requeues_only_dependent_artifact(tmp_path: Path):
    previous = tmp_path / "previous"
    current = tmp_path / "current"
    previous.mkdir()
    current.mkdir()
    snapshot = distillation_input()["source_snapshot"]
    units = source_units()
    write_jsonl(previous / "source-snapshots.jsonl", [snapshot])
    write_jsonl(current / "source-snapshots.jsonl", [snapshot])
    write_jsonl(previous / "source-units.jsonl", units)
    changed_units = [dict(row) for row in units]
    changed_units[0] = {
        **changed_units[0],
        "normalized_content_hash": "c" * 64,
    }
    write_jsonl(current / "source-units.jsonl", changed_units)
    artifacts = [
        {
            "artifact_id": "source-native:claim:test",
            "artifact": {"source_unit_ids": [units[0]["source_unit_id"]]},
        },
        {
            "artifact_id": "source-native:task-card:unrelated",
            "artifact": {"source_unit_ids": [units[2]["source_unit_id"]]},
        },
    ]
    write_jsonl(previous / "reviewed-artifacts.jsonl", artifacts)
    write_jsonl(current / "reviewed-artifacts.jsonl", artifacts)

    report = build_source_native_impact_report(
        previous_dir=previous,
        current_dir=current,
    )

    assert report["status"] == "changed"
    assert report["revalidation_queue"]["knowledge_unit_ids"] == [
        "source-native:claim:test"
    ]
    assert "source-native:task-card:unrelated" not in json.dumps(report)


def test_impact_report_requeues_removed_unit_dependency(tmp_path: Path):
    previous = tmp_path / "previous"
    current = tmp_path / "current"
    previous.mkdir()
    current.mkdir()
    snapshot = distillation_input()["source_snapshot"]
    units = source_units()
    write_jsonl(previous / "source-snapshots.jsonl", [snapshot])
    write_jsonl(current / "source-snapshots.jsonl", [snapshot])
    write_jsonl(previous / "source-units.jsonl", units)
    write_jsonl(current / "source-units.jsonl", units[1:])
    write_jsonl(
        previous / "reviewed-artifacts.jsonl",
        [
            {
                "artifact_id": "source-native:claim:removed",
                "artifact": {"source_unit_ids": [units[0]["source_unit_id"]]},
            }
        ],
    )
    write_jsonl(current / "reviewed-artifacts.jsonl", [])

    report = build_source_native_impact_report(
        previous_dir=previous,
        current_dir=current,
    )

    assert report["status"] == "changed"
    assert len(report["source_units"]["removed"]) == 1
    assert report["revalidation_queue"]["knowledge_unit_ids"] == []
    assert report["revalidation_queue"][
        "removed_or_prior_knowledge_unit_ids"
    ] == ["source-native:claim:removed"]


def test_impact_report_requeues_route_metadata_move(tmp_path: Path):
    previous = tmp_path / "previous"
    current = tmp_path / "current"
    previous.mkdir()
    current.mkdir()
    prior_snapshot = distillation_input()["source_snapshot"]
    current_snapshot = {
        **prior_snapshot,
        "canonical_url": "https://community.rockrms.com/documentation/new-route/test",
        "source_path": "documentation/new-route/test",
        "routing_paths": [
            "documentation/new-route",
            "documentation/new-route/test",
        ],
    }
    units = source_units()
    artifact = {
        "artifact_id": "source-native:claim:routed",
        "artifact": {"source_unit_ids": [units[0]["source_unit_id"]]},
    }
    write_jsonl(previous / "source-snapshots.jsonl", [prior_snapshot])
    write_jsonl(current / "source-snapshots.jsonl", [current_snapshot])
    write_jsonl(previous / "source-units.jsonl", units)
    write_jsonl(current / "source-units.jsonl", units)
    write_jsonl(previous / "reviewed-artifacts.jsonl", [artifact])
    write_jsonl(current / "reviewed-artifacts.jsonl", [artifact])

    report = build_source_native_impact_report(
        previous_dir=previous,
        current_dir=current,
    )

    assert report["status"] == "changed"
    assert report["source_records"]["routing_changed"] == [
        "rock_documentation|documentation-article:100"
    ]
    assert report["source_units"]["changed"] == []
    assert report["revalidation_queue"]["knowledge_unit_ids"] == [
        "source-native:claim:routed"
    ]
