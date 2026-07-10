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
    assert failures[0] == "2 evaluation questions failed"
