from __future__ import annotations

from rock_kb.service_quality_gate import QualityThresholds, quality_failures


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
