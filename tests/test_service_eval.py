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
