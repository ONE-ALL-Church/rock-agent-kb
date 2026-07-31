from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from rock_kb.canonical_knowledge import build_canonical_knowledge_bundle
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.schemas import SourceNativeDistillationOutput, SourceSnapshot
from rock_kb.source_native import (
    build_source_native_impact_report,
    build_source_native_document_candidates,
    merge_source_native_distillation_outputs,
    parse_markdown_source_units,
    promote_source_native_distillation,
    source_observation_metadata,
    source_native_evaluation_rows,
    validate_source_native_distillation,
    write_source_native_distillation_schema,
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
    assert manifest["public_retrieval_changed"] is False
    assert manifest["evaluation_case_count"] == 3


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


def test_promoted_pilot_compiles_into_canonical_shadow_only(tmp_path: Path):
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
