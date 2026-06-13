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


def evaluate_service(base_url: str, limit: int = 5, timeout: float = 20.0, concurrency: int = 6) -> ServiceEvalResult:
    base = base_url.rstrip("/")
    rows = list(read_jsonl(EVALUATION_SET_PATH))
    worker_count = max(1, min(concurrency, len(rows) or 1))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(executor.map(lambda row: evaluate_row(base, row, limit, timeout), rows))
    fail_count = sum(1 for row in results if row["status"] == "fail")
    return ServiceEvalResult(
        status="fail" if fail_count else "ok",
        pass_count=len(results) - fail_count,
        fail_count=fail_count,
        results=results,
    )


def evaluate_row(base_url: str, row: dict[str, Any], limit: int, timeout: float) -> dict[str, Any]:
    question = str(row.get("question") or "")
    expected_concept = str(row.get("concept_id") or "")
    params = urlencode({"q": question, "limit": str(limit), "min_tier": "routing_context_only"})
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
            "hit_count": 0,
            "concepts": [],
            "missing_terms": [],
            "status": "fail",
            "error": str(exc),
        }
    concepts = {str(hit.get("concept") or "") for hit in hits if isinstance(hit, dict)}
    required_terms = [str(term).lower() for term in row.get("required_terms") or []]
    serialized = json.dumps(hits, ensure_ascii=False).lower()
    missing_terms = [term for term in required_terms if term.lower() not in serialized]
    passed = bool(hits) and (not expected_concept or expected_concept in concepts) and not missing_terms
    return {
        "id": row.get("id"),
        "question": question,
        "expected_concept": expected_concept,
        "hit_count": len(hits),
        "concepts": sorted(concepts),
        "missing_terms": missing_terms,
        "status": "pass" if passed else "fail",
    }
