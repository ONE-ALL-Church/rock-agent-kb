from __future__ import annotations

from rock_kb import service_eval


class FakeResponse:
    def __init__(self, results: list[dict]):
        self._results = results

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"results": self._results}


def test_evaluate_row_requires_expected_concept_in_top_two(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {"concept": "groups", "body": "workflow launch trigger"},
                {"concept": "lava", "body": "workflow launch trigger"},
                {"concept": "workflows", "body": "workflow launch trigger"},
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:workflows:test",
            "question": "How do I troubleshoot workflow launch triggers?",
            "concept_id": "workflows",
            "required_terms": ["workflow", "launch"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_concept_rank"] == 3
    assert result["max_allowed_rank"] == 2
    assert result["status"] == "fail"


def test_evaluate_row_passes_expected_concept_in_top_two(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {"concept": "groups", "body": "workflow launch trigger"},
                {"concept": "workflows", "body": "workflow launch trigger"},
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:workflows:test",
            "question": "How do I troubleshoot workflow launch triggers?",
            "concept_id": "workflows",
            "required_terms": ["workflow", "launch"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_concept_rank"] == 2
    assert result["status"] == "pass"


def test_evaluate_row_matches_secondary_concept_and_reports_reciprocal_rank(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {"id": "claim:one", "concept": "lava", "concepts": ["lava", "check-in"], "body": "PersonAttendance"},
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:check-in:secondary",
            "question": "Which PersonAttendance roots exist?",
            "concept_id": "check-in",
            "required_terms": ["PersonAttendance"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_concept_rank"] == 1
    assert result["reciprocal_rank"] == 1.0
    assert result["status"] == "pass"


def test_evaluate_row_requires_expected_result_kind_and_exact_id(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {
                    "id": "model_map:stable:group",
                    "kind": "model_map",
                    "concept": "model-map",
                    "body": "Group Members relationship",
                }
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:curated:model-map-group-exact",
            "question": "Show me the Group Model Map",
            "concept_id": "model-map",
            "expected_result_ids": ["model_map:stable:group"],
            "expected_result_kinds": ["model_map"],
            "required_terms": ["Members"],
            "max_rank": 1,
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_result_id_rank"] == 1
    assert result["expected_result_kind_rank"] == 1
    assert result["status"] == "pass"


def test_evaluate_row_fails_when_expected_result_id_is_missing(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [{"id": "model_map:stable:group-member", "kind": "model_map", "concept": "model-map", "body": "Group"}]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:curated:model-map-group-exact",
            "question": "Show me the Group Model Map",
            "concept_id": "model-map",
            "expected_result_ids": ["model_map:stable:group"],
            "expected_result_kinds": ["model_map"],
            "required_terms": ["Group"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_result_id_rank"] is None
    assert result["status"] == "fail"


def test_evaluate_row_rejects_forbidden_result_and_wrong_authority(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {
                    "id": "recipe:oneall:registration-transfer",
                    "kind": "recipe",
                    "concept": "security-permissions",
                    "authority_tier": "community-reviewed",
                    "body": "authorization",
                },
                {
                    "id": "claim:claim:direct-access",
                    "kind": "claim",
                    "concept": "security-permissions",
                    "authority_tier": "official",
                    "body": "direct database access authorization",
                },
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:curated:direct-access",
            "question": "Should AI receive direct database access?",
            "concept_id": "security-permissions",
            "expected_result_ids": ["claim:claim:direct-access"],
            "forbidden_result_ids": ["recipe:oneall:registration-transfer"],
            "forbidden_max_rank": 1,
            "required_authority_tiers": ["official"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["expected_result_id_rank"] == 2
    assert result["forbidden_result_id_rank"] == 1
    assert result["authority_passed"] is True
    assert result["status"] == "fail"


def test_evaluation_metrics_reports_mrr_recall_duplicates_and_authority():
    metrics = service_eval.evaluation_metrics(
        [
            {
                "has_relevance_expectation": True,
                "relevant_rank": 1,
                "max_allowed_rank": 2,
                "reciprocal_rank": 1.0,
                "hit_count": 3,
                "duplicate_count": 1,
                "required_authority_tiers": ["official"],
                "authority_passed": True,
            },
            {
                "has_relevance_expectation": True,
                "relevant_rank": None,
                "max_allowed_rank": 2,
                "reciprocal_rank": 0.0,
                "hit_count": 2,
                "duplicate_count": 0,
                "required_authority_tiers": ["official"],
                "authority_passed": False,
            },
        ]
    )

    assert metrics["mean_reciprocal_rank"] == 0.5
    assert metrics["recall_at_target_rank"] == 0.5
    assert metrics["duplicate_result_count"] == 1
    assert metrics["duplicate_result_rate"] == 0.2
    assert metrics["authority_pass_rate"] == 0.5
