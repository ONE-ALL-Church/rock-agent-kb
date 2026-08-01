from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from rock_kb.canonical_knowledge import build_canonical_knowledge_bundle
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.paths import REPO_ROOT
from rock_kb.reviewed_cross_source import (
    REVIEWED_CROSS_SOURCE_RELATIVE_DIR,
    load_reviewed_cross_source,
    promote_reviewed_cross_source,
    reviewed_cross_source_evaluation_rows,
)
from rock_kb.schemas import ReviewedCrossSourceArtifact


ISSUE_ID = "rock_issue:SparkDevNetwork/Rock#6914"
ARTIFACT_ID = (
    "cross-source:claim:content-channel-item-list-authorization-6914"
)


def review_decision() -> dict:
    return next(
        read_jsonl(
            REPO_ROOT
            / REVIEWED_CROSS_SOURCE_RELATIVE_DIR
            / "review-decisions.jsonl"
        )
    )


def issue_search_row() -> dict:
    return {
        "id": ISSUE_ID,
        "kind": "rock_issue",
        "title": "Content Channel Item entity permission issue",
        "body": "Issue #6914 reports the affected behavior.",
        "url": "https://github.com/SparkDevNetwork/Rock/issues/6914",
        "concepts": ["content-personalization"],
        "topics": ["issue"],
        "authority_tier": "community-unreviewed",
        "source_id": "rock_core_issues",
        "payload": {
            "schema": "rock-kb-rock-issue-v1",
            "issue_id": ISSUE_ID,
            "number": 6914,
            "repository": "SparkDevNetwork/Rock",
            "source_id": "rock_core_issues",
            "github_node_id": "I_kwDOABihOc8AAAABIN1ZQA",
            "url": "https://github.com/SparkDevNetwork/Rock/issues/6914",
            "updated_at": "2026-07-26T20:26:36Z",
            "source_content_hash": "a" * 64,
            "authority_tier": "community-unreviewed",
            "claim_tier": "routing_context_only",
        },
    }


def test_promoted_cross_source_bundle_separates_report_release_and_code():
    records = load_reviewed_cross_source(REPO_ROOT)

    assert len(records["knowledge_units"]) == 1
    assert len(records["source_snapshots"]) == 3
    assert len(records["evidence_links"]) == 3
    by_source = {
        row.source_id: row
        for row in records["source_snapshots"]
    }
    assert by_source["rock_core_issues"].immutable is False
    assert by_source["rock_core_issues"].authority_tier == "community-unreviewed"
    assert by_source["rock_core_release_notes"].upstream_revision == "19.3"
    assert by_source["sparkdevnetwork_rock"].immutable is True
    assert (
        by_source["sparkdevnetwork_rock"].upstream_revision
        == "4d2eb5b7b236e5e76023c6a9c46685175b6c1811"
    )
    assert {row.relation for row in records["evidence_links"]} == {
        "supports",
        "reports",
        "demonstrates",
    }
    code_unit = next(
        row
        for row in records["source_units"]
        if row.unit_kind == "source_code_span"
    )
    assert code_unit.locator.line_start == 281
    assert code_unit.locator.line_end == 300
    assert code_unit.locator.symbol == (
        "ContentChannelItemList.GetIsAddDeleteEnabled"
    )
    assert all(row.text is None for row in records["source_units"])


def test_cross_source_promotion_is_reproducible(tmp_path: Path):
    input_path = tmp_path / "decision.jsonl"
    destination = tmp_path / "canonical" / "cross-source" / "v1"
    write_jsonl(input_path, [review_decision()])

    first = promote_reviewed_cross_source(
        input_path=input_path,
        destination=destination,
    )
    second = promote_reviewed_cross_source(
        input_path=input_path,
        destination=destination,
    )

    assert first["file_hashes"] == second["file_hashes"]
    assert first["artifact_count"] == 1
    assert first["source_snapshot_count"] == 3
    assert first["evaluation_case_count"] == 2


def test_cross_source_schema_requires_distinct_source_families():
    decision = review_decision()
    issue_source_id = decision["source_evidence"][0]["source_snapshot"][
        "source_id"
    ]
    for evidence in decision["source_evidence"]:
        evidence["source_snapshot"]["source_id"] = issue_source_id

    with pytest.raises(
        ValidationError,
        match="at least two distinct sources",
    ):
        ReviewedCrossSourceArtifact.model_validate(decision)


def test_cross_source_records_resolve_existing_issue_and_version_relationship():
    bundle, summary = build_canonical_knowledge_bundle(
        search_rows=[issue_search_row()],
        distilled_claims=[],
        include_source_native_pilot=False,
        include_reviewed_cross_source=True,
        repo_root=REPO_ROOT,
    )

    item = next(
        row
        for row in bundle.knowledge_units
        if row.knowledge_unit_id == ARTIFACT_ID
    )
    assert item.rock_versions == ["19.1", "19.1.8", "19.3"]
    assert item.version_scope_status == "scoped"
    assert item.authority_tiers == [
        "community-unreviewed",
        "release-note-confirmed",
        "source-code-confirmed",
    ]
    relationships = [
        row
        for row in bundle.relationships
        if row.from_id == ARTIFACT_ID
    ]
    assert {row.relation for row in relationships} == {
        "affects_version",
        "corroborates",
    }
    assert ISSUE_ID in {row.to_id for row in relationships}
    assert (
        "source-snapshot:rock-release-note:6914"
        in {row.to_id for row in relationships}
    )
    assert summary["input"]["reviewed_cross_source_artifacts"] == 1


def test_cross_source_evaluations_cover_exact_and_paraphrase():
    rows = reviewed_cross_source_evaluation_rows(REPO_ROOT)

    assert len(rows) == 2
    assert {row["query_type"] for row in rows} == {"exact", "paraphrase"}
    assert all(row["expected_result_ids"] == [ARTIFACT_ID] for row in rows)
    assert {row["max_allowed_rank"] for row in rows} == {2, 3}
    assert all(
        row["required_authority_tiers"] == ["source-code-confirmed"]
        for row in rows
    )


def test_cross_source_evaluations_require_exact_and_paraphrase():
    decision = review_decision()
    for evaluation in decision["evaluations"]:
        evaluation["query_type"] = "exact"

    with pytest.raises(
        ValidationError,
        match="must cover exact and paraphrase",
    ):
        ReviewedCrossSourceArtifact.model_validate(decision)
