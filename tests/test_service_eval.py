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
