from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from .jsonl import read_jsonl
from .paths import REPO_ROOT


EVALUATION_SET_PATH = REPO_ROOT / "agent" / "evaluation-set.jsonl"


@dataclass(frozen=True)
class ServiceEvalResult:
    status: str
    pass_count: int
    fail_count: int
    results: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "rock-kb-service-evaluation-v1",
            "status": self.status,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "results": self.results,
        }


def evaluate_service(
    base_url: str,
    limit: int = 5,
    timeout: float = 20.0,
    concurrency: int = 6,
    target_rank: int = 2,
) -> ServiceEvalResult:
    base = base_url.rstrip("/")
    rows = list(read_jsonl(EVALUATION_SET_PATH))
    worker_count = max(1, min(concurrency, len(rows) or 1))
    max_allowed_rank = max(1, min(target_rank, limit))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(executor.map(lambda row: evaluate_row(base, row, limit, timeout, max_allowed_rank), rows))
    fail_count = sum(1 for row in results if row["status"] == "fail")
    return ServiceEvalResult(
        status="fail" if fail_count else "ok",
        pass_count=len(results) - fail_count,
        fail_count=fail_count,
        results=results,
    )


def evaluate_row(base_url: str, row: dict[str, Any], limit: int, timeout: float, max_allowed_rank: int = 2) -> dict[str, Any]:
    question = str(row.get("question") or "")
    expected_concept = str(row.get("concept_id") or "")
    row_max_rank = max(1, min(int(row.get("max_rank") or max_allowed_rank), limit))
    params = urlencode({"q": question, "limit": str(limit), "min_tier": "routing_context_only", "detail": "full"})
    try:
        response = httpx.get(f"{base_url}/search?{params}", headers={"user-agent": "rock-kb-eval/1.0"}, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        hits = payload.get("results") or []
    except Exception as exc:
        return {
            "id": row.get("id"),
            "question": question,
            "expected_concept": expected_concept,
            "expected_concept_rank": None,
            "max_allowed_rank": row_max_rank,
            "hit_count": 0,
            "concepts": [],
            "missing_terms": [],
            "status": "fail",
            "error": str(exc),
        }
    ordered_concepts = [str(hit.get("concept") or "") for hit in hits if isinstance(hit, dict)]
    concepts = set(ordered_concepts)
    expected_rank = next((index + 1 for index, concept in enumerate(ordered_concepts) if concept == expected_concept), None)
    ordered_ids = [str(hit.get("id") or "") for hit in hits if isinstance(hit, dict)]
    ordered_kinds = [str(hit.get("kind") or "") for hit in hits if isinstance(hit, dict)]
    expected_ids = [str(value) for value in row.get("expected_result_ids") or []]
    expected_kinds = [str(value) for value in row.get("expected_result_kinds") or []]
    expected_id_rank = next((index + 1 for index, result_id in enumerate(ordered_ids) if result_id in expected_ids), None)
    expected_kind_rank = next((index + 1 for index, kind in enumerate(ordered_kinds) if kind in expected_kinds), None)
    required_terms = [str(term).lower() for term in row.get("required_terms") or []]
    serialized = json.dumps(hits, ensure_ascii=False).lower()
    missing_terms = [term for term in required_terms if term.lower() not in serialized]
    rank_passed = not expected_concept or (expected_rank is not None and expected_rank <= row_max_rank)
    id_passed = not expected_ids or (expected_id_rank is not None and expected_id_rank <= row_max_rank)
    kind_passed = not expected_kinds or (expected_kind_rank is not None and expected_kind_rank <= row_max_rank)
    min_hits_passed = len(hits) >= int(row.get("min_hits") or 1)
    passed = bool(hits) and rank_passed and id_passed and kind_passed and min_hits_passed and not missing_terms
    return {
        "id": row.get("id"),
        "question": question,
        "expected_concept": expected_concept,
        "expected_concept_rank": expected_rank,
        "max_allowed_rank": row_max_rank,
        "hit_count": len(hits),
        "concepts": sorted(concepts),
        "result_ids": ordered_ids,
        "result_kinds": ordered_kinds,
        "expected_result_ids": expected_ids,
        "expected_result_kinds": expected_kinds,
        "expected_result_id_rank": expected_id_rank,
        "expected_result_kind_rank": expected_kind_rank,
        "missing_terms": missing_terms,
        "source": row.get("source"),
        "evaluation_mode": row.get("evaluation_mode"),
        "status": "pass" if passed else "fail",
    }
