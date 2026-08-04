from __future__ import annotations

from rock_kb import service_eval
import httpx


class FakeResponse:
    def __init__(self, results: list[dict], **payload):
        self._results = results
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"results": self._results, **self._payload}


def test_canonical_result_aliases_reject_conflicts(tmp_path, monkeypatch):
    aliases = tmp_path / "aliases.jsonl"
    aliases.write_text(
        '\n'.join(
            [
                '{"alias_id":"claim:legacy","canonical_knowledge_unit_id":"knowledge:claim:one"}',
                '{"alias_id":"claim:legacy","canonical_knowledge_unit_id":"knowledge:claim:two"}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(service_eval, "PUBLIC_RESULT_ALIASES_PATH", aliases)

    try:
        service_eval.canonical_result_aliases()
    except ValueError as exc:
        assert "maps to multiple results" in str(exc)
    else:
        raise AssertionError("conflicting aliases must fail closed")


def test_evaluate_row_resolves_canonical_identity_aliases(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {
                    "id": "knowledge:claim:stable",
                    "kind": "claim",
                    "concept": "security-permissions",
                    "authority_tier": "official",
                    "body": "Direct database access requires authorization.",
                }
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:canonical-alias",
            "question": "Should an agent have direct database access?",
            "concept_id": "security-permissions",
            "expected_result_ids": ["claim:claim:legacy"],
            "expected_result_kinds": ["claim"],
            "required_authority_tiers": ["official"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=1,
        result_aliases={
            "claim:claim:legacy": "knowledge:claim:stable"
        },
    )

    assert result["original_expected_result_ids"] == ["claim:claim:legacy"]
    assert result["expected_result_ids"] == ["knowledge:claim:stable"]
    assert result["expected_result_id_rank"] == 1
    assert result["authority_passed"] is True
    assert result["status"] == "pass"


def test_evaluate_service_uses_aliases_only_for_canonical_projection(
    monkeypatch,
):
    rows = [
        {
            "id": "eval:projection-aware",
            "question": "Direct access",
            "expected_result_ids": ["claim:legacy"],
        }
    ]
    monkeypatch.setattr(service_eval, "read_jsonl", lambda path: iter(rows))
    monkeypatch.setattr(
        service_eval,
        "hosted_projection_identity",
        lambda *args: ("projection-v1", "canonical"),
    )
    monkeypatch.setattr(
        service_eval,
        "canonical_result_aliases",
        lambda: {"claim:legacy": "knowledge:claim:stable"},
    )
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [{"id": "knowledge:claim:stable", "kind": "claim"}]
        ),
    )

    result = service_eval.evaluate_service(
        "https://example.test", limit=1, concurrency=1, target_rank=1
    )

    assert result.retrieval_projection == "canonical"
    assert result.status == "ok"
    assert result.results[0]["expected_result_id_rank"] == 1


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


def test_evaluate_row_accepts_legacy_max_allowed_rank_alias(monkeypatch):
    monkeypatch.setattr(
        service_eval.httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(
            [
                {"id": "first", "kind": "claim"},
                {"id": "second", "kind": "claim"},
                {"id": "expected", "kind": "claim"},
            ]
        ),
    )

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:legacy-rank",
            "question": "Paraphrased lookup",
            "expected_result_ids": ["expected"],
            "max_allowed_rank": 3,
        },
        limit=5,
        timeout=1,
        max_allowed_rank=2,
    )

    assert result["max_allowed_rank"] == 3
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
    assert result["request_attempt_count"] == 1
    assert result["failure_category"] == "retrieval_quality"


def test_evaluate_row_passes_expected_no_answer_and_fails_false_positive(monkeypatch):
    responses = iter([FakeResponse([]), FakeResponse([{"id": "rock_issue:unrelated", "kind": "rock_issue"}])])
    monkeypatch.setattr(service_eval.httpx, "get", lambda *args, **kwargs: next(responses))
    row = {
        "id": "eval:curated:unknown-rock-issue-no-answer",
        "question": "Rock issue #999999999",
        "concept_id": "",
        "expect_no_results": True,
    }

    passed = service_eval.evaluate_row(
        "https://example.test",
        row,
        limit=5,
        timeout=1,
        max_allowed_rank=1,
    )
    failed = service_eval.evaluate_row(
        "https://example.test",
        row,
        limit=5,
        timeout=1,
        max_allowed_rank=1,
    )

    assert passed["status"] == "pass"
    assert passed["expect_no_results"] is True
    assert passed["has_relevance_expectation"] is False
    assert failed["status"] == "fail"
    assert failed["failure_category"] == "retrieval_quality"


def test_evaluate_row_retries_one_transport_timeout_and_keeps_ranking_strict(monkeypatch):
    calls = 0

    def get(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("first request timed out")
        return FakeResponse([{"id": "wrong:result", "kind": "claim", "concept": "groups", "body": "unrelated"}])

    monkeypatch.setattr(service_eval.httpx, "get", get)

    result = service_eval.evaluate_row(
        "https://example.test",
        {
            "id": "eval:strict-after-retry",
            "question": "Show the Group model",
            "concept_id": "model-map",
            "expected_result_ids": ["model_map:stable:group"],
        },
        limit=5,
        timeout=1,
        max_allowed_rank=1,
    )

    assert calls == 2
    assert result["status"] == "fail"
    assert result["availability_status"] == "recovered_after_timeout"
    assert result["failure_category"] == "retrieval_quality"
    assert result["retry_count"] == 1


def test_evaluate_row_does_not_retry_non_timeout_failures(monkeypatch):
    calls = 0

    def get(*args, **kwargs):
        nonlocal calls
        calls += 1
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(service_eval.httpx, "get", get)

    result = service_eval.evaluate_row(
        "https://example.test",
        {"id": "eval:no-retry", "question": "test", "concept_id": "groups"},
        limit=5,
        timeout=1,
    )

    assert calls == 1
    assert result["status"] == "fail"
    assert result["availability_status"] == "unavailable"
    assert result["error_type"] == "transport_error"
    assert result["retry_count"] == 0


def test_evaluate_row_stops_after_second_transport_timeout(monkeypatch):
    calls = 0

    def get(*args, **kwargs):
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("still timed out")

    monkeypatch.setattr(service_eval.httpx, "get", get)

    result = service_eval.evaluate_row(
        "https://example.test",
        {"id": "eval:bounded-retry", "question": "test", "concept_id": "groups"},
        limit=5,
        timeout=1,
    )

    assert calls == 2
    assert result["availability_status"] == "unavailable"
    assert result["error_type"] == "transport_timeout"
    assert result["retry_count"] == 1
    assert result["transport_timeout_count"] == 2


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


def test_evaluation_metrics_separates_availability_from_retrieval_quality():
    metrics = service_eval.evaluation_metrics(
        [
            {
                "availability_status": "available",
                "status": "pass",
                "has_relevance_expectation": True,
                "relevant_rank": 1,
                "max_allowed_rank": 1,
                "reciprocal_rank": 1.0,
                "hit_count": 1,
                "duplicate_count": 0,
            },
            {
                "availability_status": "unavailable",
                "status": "fail",
                "has_relevance_expectation": True,
                "relevant_rank": None,
                "reciprocal_rank": 0.0,
                "hit_count": 0,
                "transport_timeout_count": 2,
                "retry_count": 1,
            },
        ]
    )

    assert metrics["availability_rate"] == 0.5
    assert metrics["unavailable_question_count"] == 1
    assert metrics["transport_timeout_count"] == 2
    assert metrics["recall_at_target_rank"] == 1.0
    assert metrics["mean_reciprocal_rank"] == 1.0
    assert metrics["availability_passed"] is False
    assert metrics["retrieval_quality_passed"] is True
