from __future__ import annotations

import json

import pytest

from rock_kb.service_quality_gate import (
    QualityThresholds,
    normalize_quality_gate_projection,
    quality_failures,
)


def test_quality_failures_accepts_corrected_lexical_baseline():
    failures = quality_failures(
        {
            "fail_count": 0,
            "metrics": {
                "mean_reciprocal_rank": 0.993056,
                "recall_at_target_rank": 1.0,
                "duplicate_result_rate": 0.0,
                "authority_pass_rate": 1.0,
            },
        },
        QualityThresholds(),
    )

    assert failures == []


def test_quality_failures_reports_every_regression():
    failures = quality_failures(
        {
            "fail_count": 2,
            "metrics": {
                "mean_reciprocal_rank": 0.8,
                "recall_at_target_rank": 0.9,
                "duplicate_result_rate": 0.01,
                "authority_pass_rate": 0.5,
            },
        },
        QualityThresholds(),
    )

    assert len(failures) == 5
    assert failures[0] == "2 retrieval-quality questions failed"


def test_quality_failures_reports_availability_separately():
    failures = quality_failures(
        {
            "fail_count": 1,
            "metrics": {
                "unavailable_question_count": 1,
                "retrieval_quality_failure_count": 0,
                "mean_reciprocal_rank": 1.0,
                "recall_at_target_rank": 1.0,
                "duplicate_result_rate": 0.0,
                "authority_pass_rate": 1.0,
            },
        },
        QualityThresholds(),
    )

    assert failures == ["1 evaluation requests unavailable"]


def test_quality_failures_does_not_invent_ranking_failures_when_every_request_is_unavailable():
    failures = quality_failures(
        {
            "fail_count": 2,
            "metrics": {
                "available_question_count": 0,
                "unavailable_question_count": 2,
                "retrieval_quality_failure_count": 0,
                "relevance_question_count": 0,
                "authority_question_count": 0,
                "mean_reciprocal_rank": 0.0,
                "recall_at_target_rank": 0.0,
                "duplicate_result_rate": 0.0,
                "authority_pass_rate": 0.0,
            },
        },
        QualityThresholds(),
    )

    assert failures == ["2 evaluation requests unavailable"]


def test_quality_gate_projection_follows_approved_cutover_policy(tmp_path):
    policy_path = tmp_path / "promotion-policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "cutover_authorization": {
                    "status": "approved",
                    "mode": "maintainer_approved_reversible_technical_cutover",
                    "requires_legacy_rollback": True,
                }
            }
        ),
        encoding="utf-8",
    )

    assert normalize_quality_gate_projection(None, policy_path=policy_path) == "canonical"


@pytest.mark.parametrize(
    "authorization",
    [
        {},
        {"status": "pending"},
        {
            "status": "approved",
            "mode": "maintainer_approved_reversible_technical_cutover",
            "requires_legacy_rollback": False,
        },
    ],
)
def test_quality_gate_projection_fails_closed_to_legacy(tmp_path, authorization):
    policy_path = tmp_path / "promotion-policy.json"
    policy_path.write_text(
        json.dumps({"cutover_authorization": authorization}),
        encoding="utf-8",
    )

    assert normalize_quality_gate_projection(None, policy_path=policy_path) == "legacy"


def test_quality_gate_projection_accepts_explicit_diagnostics_override(tmp_path):
    missing_policy = tmp_path / "missing.json"

    assert normalize_quality_gate_projection("canonical", policy_path=missing_policy) == "canonical"
    assert normalize_quality_gate_projection("legacy", policy_path=missing_policy) == "legacy"
    with pytest.raises(ValueError, match="legacy or canonical"):
        normalize_quality_gate_projection("canary", policy_path=missing_policy)
