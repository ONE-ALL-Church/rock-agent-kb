from __future__ import annotations

import json

from rock_kb.canonical_retrieval_shadow import (
    apply_claim_collapse_maintainer_review,
    build_claim_collapse_review,
    build_endpoint_compatibility_cases,
    canonical_claim_search_title,
    canonical_search_body,
    canonical_search_row,
    evaluate_endpoint_compatibility,
    evaluate_retrieval_shadow,
    score_evaluation_hits,
)
from rock_kb.schemas import (
    EvidenceLink,
    KnowledgeUnit,
    SourceLocator,
    SourceSnapshot,
    SourceUnit,
)


def claim_unit() -> KnowledgeUnit:
    return KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="knowledge:claim:stable",
        knowledge_type="claim",
        title="Full claim statement",
        retrieval_text="Full claim statement",
        concept_facets=["system-admin-ops"],
        authority_tiers=["official"],
        claim_tier="source_backed",
        legacy_ids=["claim:claim:legacy"],
        payload={
            "claim_type": "operational_guidance",
            "approved_claims": [
                {
                    "claim_id": "claim:legacy",
                    "claim_type": "operational_guidance",
                }
            ],
        },
        content_hash="0" * 64,
    )


def test_canonical_claim_title_preserves_production_ranking_semantics():
    assert canonical_claim_search_title(claim_unit()) == "operational_guidance"


def test_source_native_search_body_includes_typed_reference_details():
    item = KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="source-native:structured_reference:test",
        knowledge_type="structured_reference",
        title="Kiosk Ad Fields",
        retrieval_text="Kiosk ad item configuration.",
        concept_facets=["check-in"],
        authority_tiers=["official"],
        payload_schema="rock-kb-source-native-artifact-payload-v1",
        payload={
            "artifact": {
                "independent_question": "Which fields control kiosk ad targeting?",
                "payload": {
                    "summary": "Reference for kiosk ad controls.",
                    "reference_items": [
                        {
                            "label": "Campuses",
                            "detail": "Limits the ad to selected campuses.",
                        }
                    ],
                    "steps": [],
                    "implementation_elements": [],
                    "cautions": ["Verify targeting before publishing."],
                    "completion_or_use": "Use this to target an ad.",
                }
            }
        },
        content_hash="0" * 64,
    )

    body = canonical_search_body(item)

    assert "Which fields control kiosk ad targeting?" in body
    assert "Campuses Limits the ad to selected campuses." in body
    assert "Verify targeting before publishing." in body


def test_canonical_search_row_exposes_observation_without_implying_version_scope():
    item = KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="source-native:claim:test",
        knowledge_type="claim",
        title="Observed documentation behavior",
        retrieval_text="The documentation describes this behavior.",
        concept_facets=["system-admin-ops"],
        authority_tiers=["official"],
        source_unit_ids=["source-unit:test"],
        version_scope_status="unprocessed",
        payload={},
        content_hash="0" * 64,
    )
    snapshot = SourceSnapshot(
        schema="rock-kb-source-snapshot-v2",
        source_snapshot_id="source-snapshot:test",
        source_id="rock_documentation",
        source_record_id="rock_documentation:article:100",
        canonical_url="https://community.rockrms.com/documentation/test",
        authority_tier="official",
        public_policy="cite_and_summarize_only",
        upstream_revision="v19.0",
        last_checked_at="2026-07-30T00:00:00+00:00",
        content_changed_at="2026-07-01T00:00:00+00:00",
    )
    unit = SourceUnit(
        schema="rock-kb-source-unit-v2",
        source_unit_id="source-unit:test",
        source_snapshot_id="source-snapshot:test",
        unit_kind="paragraph",
        locator=SourceLocator(
            kind="paragraph",
            value="Overview",
            url=snapshot.canonical_url,
        ),
        public_summary="The documentation describes the behavior.",
        required_public_handling="cite_and_summarize_only",
    )

    row = canonical_search_row(
        item,
        {snapshot.source_snapshot_id: snapshot},
        {unit.source_unit_id: unit},
    )

    assert row["payload"]["source_observation"]["upstream_revisions"] == ["v19.0"]
    assert row["payload"]["version_scope_note"].endswith(
        "verify this detail for the target version."
    )
    assert "Rock product-version applicability is unprocessed" in row["body"]


def test_source_native_search_row_distinguishes_not_required_from_unresolved():
    item = KnowledgeUnit(
        schema="rock-kb-knowledge-unit-v1",
        knowledge_unit_id="source-native:claim:test",
        knowledge_type="claim",
        title="Documented behavior",
        retrieval_text="The documentation describes this behavior.",
        concept_facets=["system-admin-ops"],
        authority_tiers=["official"],
        payload_schema="rock-kb-source-native-artifact-payload-v1",
        payload={"artifact": {"needs_live_verification": False}},
        content_hash="0" * 64,
    )

    not_required = canonical_search_row(item, {}, {})
    unresolved = canonical_search_row(
        item.model_copy(
            update={
                "payload": {
                    "artifact": {"needs_live_verification": True}
                }
            }
        ),
        {},
        {},
    )

    assert not_required["payload"]["verification_state"] == "not_required"
    assert unresolved["payload"]["verification_state"] == "unresolved"

    scoped = canonical_search_row(
        item.model_copy(
            update={
                "rock_versions": ["19.4"],
                "version_scope_status": "scoped",
            }
        ),
        {},
        {},
    )
    assert scoped["payload"]["rock_versions"] == ["19.4"]
    assert scoped["payload"]["version_scope_status"] == "scoped"


def test_canonical_claim_title_uses_statement_for_contribution_corroboration():
    item = claim_unit()
    payload = dict(item.payload)
    payload["approved_claims"] = [
        {
            "claim_id": "claim:legacy",
            "claim_type": "operational_guidance",
            "derived_from": {
                "related_contribution_ids": ["contribution:example"]
            },
        }
    ]

    assert (
        canonical_claim_search_title(item.model_copy(update={"payload": payload}))
        == "Full claim statement"
    )


def test_shadow_scoring_resolves_expected_legacy_id():
    result = score_evaluation_hits(
        {
            "id": "eval:exact",
            "question": "Exact lookup",
            "concept_id": "system-admin-ops",
            "expected_result_ids": ["claim:claim:legacy"],
            "max_rank": 1,
        },
        [
            {
                "id": "knowledge:claim:stable",
                "kind": "claim",
                "concepts": ["system-admin-ops"],
                "authority_tier": "official",
            }
        ],
        alias_map={
            "claim:claim:legacy": "knowledge:claim:stable",
            "knowledge:claim:stable": "knowledge:claim:stable",
        },
        latency_ms=1.5,
    )

    assert result["expected_result_id_rank"] == 1
    assert result["status"] == "pass"


def test_shadow_scoring_accepts_legacy_max_allowed_rank_alias():
    result = score_evaluation_hits(
        {
            "id": "eval:legacy-rank",
            "question": "Paraphrased lookup",
            "expected_result_ids": ["expected"],
            "max_allowed_rank": 3,
        },
        [
            {"id": "first", "kind": "claim"},
            {"id": "second", "kind": "claim"},
            {"id": "expected", "kind": "claim"},
        ],
        alias_map={},
        latency_ms=1,
    )

    assert result["max_allowed_rank"] == 3
    assert result["status"] == "pass"


def test_shadow_scoring_supports_no_answer_cases():
    passed = score_evaluation_hits(
        {
            "id": "eval:no-answer",
            "question": "unknown",
            "expect_no_results": True,
        },
        [],
        alias_map={},
        latency_ms=1,
    )
    failed = score_evaluation_hits(
        {
            "id": "eval:no-answer",
            "question": "unknown",
            "expect_no_results": True,
        },
        [{"id": "wrong", "kind": "claim"}],
        alias_map={"wrong": "wrong"},
        latency_ms=1,
    )

    assert passed["status"] == "pass"
    assert failed["status"] == "fail"


def test_retrieval_report_distinguishes_equivalence_from_shared_failure():
    evaluation = {
        "id": "eval:shared",
        "question": "Unknown issue",
        "expect_no_results": True,
    }
    raw = {
        "variants": {
            "baseline": {
                "setup_ms": 10,
                "query_ms": 5,
                "results": [
                    {
                        "id": "eval:shared",
                        "latency_ms": 1,
                        "hits": [{"id": "rock_issue:1", "kind": "rock_issue"}],
                    }
                ],
            },
            "candidate": {
                "setup_ms": 10,
                "query_ms": 5,
                "results": [
                    {
                        "id": "eval:shared",
                        "latency_ms": 1,
                        "hits": [{"id": "rock_issue:1", "kind": "rock_issue"}],
                    }
                ],
            },
        }
    }
    row = {
        "id": "rock_issue:1",
        "kind": "rock_issue",
        "title": "Issue",
        "body": "Issue",
        "path": "issues",
        "concepts": [],
        "topics": [],
        "legacy_ids": [],
        "payload": {},
    }

    report = evaluate_retrieval_shadow(
        raw,
        evaluations=[evaluation],
        baseline_rows=[row],
        candidate_rows=[row],
        projection_summary={
            "output": {
                "identity_migrations": 1,
                "content_fallback_identities": 0,
            }
        },
    )

    assert report["summary"]["status"] == "pass"
    assert report["summary"]["shared_failure_count"] == 1
    assert report["promotion_gate"]["retrieval_equivalence_passed"] is True
    assert report["promotion_gate"]["ready_for_production_promotion"] is False


def test_endpoint_compatibility_allows_canonical_id_change_behind_public_alias():
    case = {
        "id": "endpoint:public-result-id",
        "surface": "result",
        "transport": "rest",
        "expected": {
            "http_status": 200,
            "payload_status": "ok",
            "requested_result_id": "claim:claim:legacy",
            "result_kind": "claim",
        },
    }
    raw = {
        "variants": {
            "baseline": {
                "endpoint_results": [
                    {
                        "id": case["id"],
                        "http_status": 200,
                        "latency_ms": 1,
                        "payload": {
                            "status": "ok",
                            "requested_result_id": "claim:claim:legacy",
                            "canonical_result_id": "claim:claim:legacy",
                            "result": {"kind": "claim"},
                        },
                    }
                ]
            },
            "candidate": {
                "endpoint_results": [
                    {
                        "id": case["id"],
                        "http_status": 200,
                        "latency_ms": 1,
                        "payload": {
                            "status": "ok",
                            "requested_result_id": "claim:claim:legacy",
                            "canonical_result_id": "knowledge:claim:stable",
                            "result": {"kind": "claim"},
                        },
                    }
                ]
            },
        }
    }

    report = evaluate_endpoint_compatibility(raw, endpoint_cases=[case])

    assert report["status"] == "pass"
    assert report["contract_mismatch_count"] == 0
    assert (
        report["cases"][0]["candidate"]["resolved_canonical_id"]
        == "knowledge:claim:stable"
    )


def test_endpoint_case_builder_covers_all_exact_surfaces():
    rows = [
        {
            "id": "claim:claim:legacy",
            "kind": "claim",
            "legacy_ids": ["claim:claim:legacy:groups"],
            "payload": {"claim_id": "claim:legacy"},
        },
        {
            "id": "rock_issue:SparkDevNetwork/Rock#1",
            "kind": "rock_issue",
            "payload": {
                "issue_id": "rock_issue:SparkDevNetwork/Rock#1"
            },
        },
        {
            "id": "rock_idea:1",
            "kind": "rock_idea",
            "payload": {"idea_id": "rock_idea:1"},
        },
        {
            "id": "model_map:stable:group",
            "kind": "model_map",
            "payload": {"identity": {"model_slug": "group"}},
        },
        {
            "id": "recipe:example:one",
            "kind": "recipe",
            "payload": {"recipe_id": "example:one"},
        },
        {
            "id": "lava_context:surface:personattendance:hash",
            "kind": "lava_context",
            "payload": {
                "context_id": "surface",
                "root_key": "PersonAttendance",
            },
        },
    ]

    cases = build_endpoint_compatibility_cases(rows)

    assert {row["surface"] for row in cases} == {
        "result",
        "claim",
        "rock_issue",
        "rock_issue_missing",
        "rock_idea",
        "model_map",
        "lava_context",
        "recipe",
        "mcp_result",
    }
    mcp_case = next(row for row in cases if row["surface"] == "mcp_result")
    assert mcp_case["arguments"] == {"id": "claim:claim:legacy"}


def test_claim_collapse_review_preserves_aliases_authority_and_mirror_evidence(
    tmp_path,
):
    unit = claim_unit().model_copy(
        update={
            "legacy_ids": ["claim:claim:first", "claim:claim:second"],
            "source_unit_ids": ["unit:first", "unit:second"],
            "source_work_ids": ["media-work:episode:1"],
            "authority_tiers": ["official", "community-reviewed"],
        }
    )
    snapshots = [
        SourceSnapshot(
            schema="rock-kb-source-snapshot-v1",
            source_snapshot_id=f"snapshot:{suffix}",
            source_id=f"source:{suffix}",
            source_record_id=f"record:{suffix}",
            source_work_id="media-work:episode:1",
            authority_tier=authority,
            public_policy="cite_and_summarize_only",
        )
        for suffix, authority in [
            ("first", "official"),
            ("second", "community-reviewed"),
        ]
    ]
    source_units = [
        SourceUnit(
            schema="rock-kb-source-unit-v1",
            source_unit_id=f"unit:{suffix}",
            source_snapshot_id=f"snapshot:{suffix}",
            unit_kind="media_segment",
            locator=SourceLocator(kind="timestamp", value="01:00"),
            required_public_handling="cite_and_summarize_only",
        )
        for suffix in ["first", "second"]
    ]
    links = [
        EvidenceLink(
            schema="rock-kb-evidence-link-v1",
            evidence_link_id=f"evidence:{suffix}",
            knowledge_unit_id=unit.knowledge_unit_id,
            source_unit_id=f"unit:{suffix}",
            evidence_summary="Exact reviewed statement.",
            authority_tier="official",
        )
        for suffix in ["first", "second"]
    ]
    baseline = [
        {
            "id": f"claim:claim:{suffix}",
            "kind": "claim",
            "body": "Full claim statement",
            "payload": {
                "claim": "Full claim statement",
                "claim_type": "operational_guidance",
            },
        }
        for suffix in ["first", "second"]
    ]

    report = build_claim_collapse_review(
        baseline_rows=baseline,
        knowledge_units=[unit],
        source_snapshots=snapshots,
        source_units=source_units,
        evidence_links=links,
    )
    group = report["groups"][0]

    assert report["collapsed_group_count"] == 1
    assert report["redundant_public_row_count"] == 1
    assert group["reviewable"] is True
    assert group["independent_source_work_count"] == 1
    assert group["mirrored_evidence_count"] == 1
    review_path = tmp_path / "review.json"
    review_path.write_text(
        json.dumps(
            {
                "review_input_sha256": report["review_input_sha256"],
                "reviewed_at": "2026-07-30",
                "reviewer": "test",
                "decisions": [
                    {
                        "knowledge_unit_id": unit.knowledge_unit_id,
                        "decision": "approve",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    reviewed = apply_claim_collapse_maintainer_review(report, review_path)

    assert reviewed["status"] == "reviewer_approved"
    assert reviewed["maintainer_review"]["status"] == "approved"
