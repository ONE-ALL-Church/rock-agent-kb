from __future__ import annotations

import json
import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from typing import Any
from urllib.parse import urlencode

import httpx

from .jsonl import read_jsonl
from .paths import REPO_ROOT


EVALUATION_SET_PATH = REPO_ROOT / "agent" / "evaluation-set.jsonl"
PUBLIC_RESULT_ALIASES_PATH = (
    REPO_ROOT / "canonical" / "identity" / "v1" / "public-result-aliases.jsonl"
)


@dataclass(frozen=True)
class ServiceEvalResult:
    status: str
    pass_count: int
    fail_count: int
    results: list[dict[str, Any]]
    metrics: dict[str, Any]
    projection_version: str = ""
    retrieval_projection: str = ""
    evaluated_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "rock-kb-service-evaluation-v1",
            "status": self.status,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "metrics": self.metrics,
            "projection_version": self.projection_version,
            "retrieval_projection": self.retrieval_projection,
            "evaluated_at": self.evaluated_at,
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
    evaluated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    projection_version, retrieval_projection = hosted_projection_identity(
        base, timeout
    )
    result_aliases = (
        canonical_result_aliases()
        if retrieval_projection in {"canonical", "canonical-canary"}
        else {}
    )
    rows = list(read_jsonl(EVALUATION_SET_PATH))
    worker_count = max(1, min(concurrency, len(rows) or 1))
    max_allowed_rank = max(1, min(target_rank, limit))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(
            executor.map(
                lambda row: evaluate_row(
                    base,
                    row,
                    limit,
                    timeout,
                    max_allowed_rank,
                    result_aliases=result_aliases,
                ),
                rows,
            )
        )
    fail_count = sum(1 for row in results if row["status"] == "fail")
    return ServiceEvalResult(
        status="fail" if fail_count else "ok",
        pass_count=len(results) - fail_count,
        fail_count=fail_count,
        results=results,
        metrics=evaluation_metrics(results),
        projection_version=projection_version,
        retrieval_projection=retrieval_projection,
        evaluated_at=evaluated_at,
    )


def evaluate_row(
    base_url: str,
    row: dict[str, Any],
    limit: int,
    timeout: float,
    max_allowed_rank: int = 2,
    *,
    result_aliases: dict[str, str] | None = None,
) -> dict[str, Any]:
    question = str(row.get("question") or "")
    expected_concept = str(row.get("concept_id") or "")
    row_max_rank = max(
        1,
        min(
            int(
                row.get("max_rank")
                or row.get("max_allowed_rank")
                or max_allowed_rank
            ),
            limit,
        ),
    )
    params = urlencode({"q": question, "limit": str(limit), "min_tier": "routing_context_only", "detail": "full"})
    started_at = perf_counter()
    request_attempt_count = 0
    transport_timeout_count = 0
    try:
        for request_attempt_count in range(1, 3):
            try:
                response = httpx.get(
                    f"{base_url}/search?{params}",
                    headers={"user-agent": "rock-kb-eval/1.0", "x-rock-kb-client": "eval"},
                    timeout=timeout,
                )
                break
            except httpx.TimeoutException:
                transport_timeout_count += 1
                if request_attempt_count == 2:
                    raise
        response.raise_for_status()
        payload = response.json()
        hits = payload.get("results") or []
    except Exception as exc:
        has_relevance_expectation = bool(expected_concept or row.get("expected_result_ids") or row.get("expected_result_kinds"))
        return {
            "id": row.get("id"),
            "question": question,
            "expected_concept": expected_concept,
            "expected_concept_rank": None,
            "max_allowed_rank": row_max_rank,
            "hit_count": 0,
            "concepts": [],
            "missing_terms": [],
            "duplicate_count": 0,
            "has_relevance_expectation": has_relevance_expectation,
            "relevant_rank": None,
            "reciprocal_rank": 0.0,
            "required_authority_tiers": row.get("required_authority_tiers") or [],
            "authority_passed": False,
            "latency_ms": round((perf_counter() - started_at) * 1000, 3),
            "availability_status": "unavailable",
            "failure_category": "availability",
            "request_attempt_count": request_attempt_count,
            "retry_count": max(0, request_attempt_count - 1),
            "transport_timeout_count": transport_timeout_count,
            "error_type": evaluation_error_type(exc),
            "status": "fail",
            "error": str(exc),
        }
    ordered_concept_sets = [hit_concepts(hit) for hit in hits if isinstance(hit, dict)]
    concepts = {concept for values in ordered_concept_sets for concept in values}
    expected_rank = next((index + 1 for index, values in enumerate(ordered_concept_sets) if expected_concept in values), None)
    ordered_ids = [str(hit.get("id") or "") for hit in hits if isinstance(hit, dict)]
    ordered_kinds = [str(hit.get("kind") or "") for hit in hits if isinstance(hit, dict)]
    ordered_authorities = [str(hit.get("authority_tier") or "") for hit in hits if isinstance(hit, dict)]
    expect_no_results = bool(row.get("expect_no_results"))
    aliases = result_aliases or {}
    original_expected_ids = [
        str(value) for value in row.get("expected_result_ids") or []
    ]
    expected_ids = [aliases.get(value, value) for value in original_expected_ids]
    expected_kinds = [str(value) for value in row.get("expected_result_kinds") or []]
    original_forbidden_ids = [
        str(value) for value in row.get("forbidden_result_ids") or []
    ]
    forbidden_ids = [
        aliases.get(value, value) for value in original_forbidden_ids
    ]
    required_authorities = [str(value) for value in row.get("required_authority_tiers") or []]
    expected_id_rank = next((index + 1 for index, result_id in enumerate(ordered_ids) if result_id in expected_ids), None)
    expected_kind_rank = next((index + 1 for index, kind in enumerate(ordered_kinds) if kind in expected_kinds), None)
    forbidden_id_rank = next((index + 1 for index, result_id in enumerate(ordered_ids) if result_id in forbidden_ids), None)
    duplicate_ids = sorted({result_id for result_id in ordered_ids if result_id and ordered_ids.count(result_id) > 1})
    required_terms = [str(term).lower() for term in row.get("required_terms") or []]
    serialized = json.dumps(hits, ensure_ascii=False).lower()
    missing_terms = [term for term in required_terms if term.lower() not in serialized]
    rank_passed = not expected_concept or (expected_rank is not None and expected_rank <= row_max_rank)
    id_passed = not expected_ids or (expected_id_rank is not None and expected_id_rank <= row_max_rank)
    kind_passed = not expected_kinds or (expected_kind_rank is not None and expected_kind_rank <= row_max_rank)
    forbidden_max_rank = max(1, min(int(row.get("forbidden_max_rank") or row_max_rank), limit))
    forbidden_passed = not forbidden_ids or forbidden_id_rank is None or forbidden_id_rank > forbidden_max_rank
    relevant_indexes = [
        index
        for index, hit in enumerate(hits)
        if isinstance(hit, dict)
        and (
            (expected_ids and str(hit.get("id") or "") in expected_ids)
            or (not expected_ids and expected_kinds and str(hit.get("kind") or "") in expected_kinds)
            or (not expected_ids and not expected_kinds and expected_concept in hit_concepts(hit))
        )
    ]
    authority_passed = not required_authorities or any(ordered_authorities[index] in required_authorities for index in relevant_indexes if index < row_max_rank)
    min_hits_passed = expect_no_results or len(hits) >= int(row.get("min_hits") or 1)
    relevant_rank = expected_id_rank if expected_ids else expected_kind_rank if expected_kinds else expected_rank
    has_relevance_expectation = not expect_no_results and bool(expected_ids or expected_kinds or expected_concept)
    reciprocal_rank = round(1 / relevant_rank, 6) if relevant_rank else 0.0
    passed = (
        not hits
        if expect_no_results
        else bool(hits)
        and rank_passed
        and id_passed
        and kind_passed
        and forbidden_passed
        and authority_passed
        and min_hits_passed
        and not missing_terms
        and not duplicate_ids
    )
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
        "authority_tiers": ordered_authorities,
        "duplicate_result_ids": duplicate_ids,
        "duplicate_count": len(ordered_ids) - len(set(ordered_ids)),
        "expected_result_ids": expected_ids,
        "original_expected_result_ids": original_expected_ids,
        "expected_result_kinds": expected_kinds,
        "expected_result_id_rank": expected_id_rank,
        "expected_result_kind_rank": expected_kind_rank,
        "forbidden_result_ids": forbidden_ids,
        "original_forbidden_result_ids": original_forbidden_ids,
        "forbidden_result_id_rank": forbidden_id_rank,
        "forbidden_max_rank": forbidden_max_rank,
        "required_authority_tiers": required_authorities,
        "authority_passed": authority_passed,
        "expect_no_results": expect_no_results,
        "has_relevance_expectation": has_relevance_expectation,
        "relevant_rank": relevant_rank,
        "reciprocal_rank": reciprocal_rank,
        "missing_terms": missing_terms,
        "source": row.get("source"),
        "evaluation_mode": row.get("evaluation_mode"),
        "latency_ms": round((perf_counter() - started_at) * 1000, 3),
        "availability_status": "recovered_after_timeout" if transport_timeout_count else "available",
        "failure_category": "" if passed else "retrieval_quality",
        "request_attempt_count": request_attempt_count,
        "retry_count": max(0, request_attempt_count - 1),
        "transport_timeout_count": transport_timeout_count,
        "status": "pass" if passed else "fail",
    }


def hosted_projection_identity(
    base_url: str, timeout: float
) -> tuple[str, str]:
    try:
        response = httpx.get(
            f"{base_url.rstrip('/')}/health",
            headers={"user-agent": "rock-kb-eval/1.0", "x-rock-kb-client": "eval"},
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return (
            str(
                payload.get("retrieval_projection_version")
                or payload.get("version")
                or ""
            ),
            str(payload.get("retrieval_projection") or ""),
        )
    except Exception:
        return "", ""


def hosted_projection_version(base_url: str, timeout: float) -> str:
    return hosted_projection_identity(base_url, timeout)[0]


def canonical_result_aliases() -> dict[str, str]:
    aliases: dict[str, str] = {}
    for row in read_jsonl(PUBLIC_RESULT_ALIASES_PATH):
        alias_id = str(row.get("alias_id") or "").strip()
        canonical_id = str(
            row.get("canonical_knowledge_unit_id") or ""
        ).strip()
        if not alias_id or not canonical_id:
            raise ValueError("Canonical result alias is missing an identity")
        existing = aliases.get(alias_id)
        if existing and existing != canonical_id:
            raise ValueError(
                f"Canonical result alias maps to multiple results: {alias_id}"
            )
        aliases[alias_id] = canonical_id
    return aliases


def hit_concepts(hit: dict[str, Any]) -> list[str]:
    values = hit.get("concepts")
    if isinstance(values, list):
        concepts = [str(value or "").strip() for value in values]
        concepts = [value for value in concepts if value]
        if concepts:
            return list(dict.fromkeys(concepts))
    concept = str(hit.get("concept") or "").strip()
    return [concept] if concept else []


def evaluation_error_type(exc: Exception) -> str:
    if isinstance(exc, httpx.TimeoutException):
        return "transport_timeout"
    if isinstance(exc, httpx.TransportError):
        return "transport_error"
    if isinstance(exc, httpx.HTTPStatusError):
        return "http_status_error"
    if isinstance(exc, (json.JSONDecodeError, AttributeError, TypeError, ValueError)):
        return "invalid_response"
    return "request_error"


def evaluation_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    available_rows = [row for row in results if row.get("availability_status", "available") != "unavailable"]
    unavailable_rows = [row for row in results if row.get("availability_status") == "unavailable"]
    relevance_rows = [row for row in available_rows if row.get("has_relevance_expectation")]
    authority_rows = [row for row in available_rows if row.get("required_authority_tiers")]
    duplicate_count = sum(int(row.get("duplicate_count") or 0) for row in available_rows)
    retrieved_count = sum(int(row.get("hit_count") or 0) for row in available_rows)
    recall_count = sum(
        1
        for row in relevance_rows
        if row.get("relevant_rank") is not None and int(row["relevant_rank"]) <= int(row.get("max_allowed_rank") or 1)
    )
    latencies = sorted(float(row.get("latency_ms") or 0) for row in available_rows if row.get("latency_ms") is not None)
    p95_index = max(0, min(len(latencies) - 1, math.ceil(len(latencies) * 0.95) - 1)) if latencies else 0
    return {
        "question_count": len(results),
        "available_question_count": len(available_rows),
        "unavailable_question_count": len(unavailable_rows),
        "availability_rate": round(len(available_rows) / max(1, len(results)), 6),
        "transport_timeout_count": sum(int(row.get("transport_timeout_count") or 0) for row in results),
        "retry_count": sum(int(row.get("retry_count") or 0) for row in results),
        "recovered_after_timeout_count": sum(1 for row in results if row.get("availability_status") == "recovered_after_timeout"),
        "retrieval_quality_failure_count": sum(1 for row in available_rows if row.get("status") == "fail"),
        "availability_passed": len(unavailable_rows) == 0,
        "retrieval_quality_passed": all(row.get("status") != "fail" for row in available_rows) if available_rows else None,
        "relevance_question_count": len(relevance_rows),
        "mean_reciprocal_rank": round(sum(float(row.get("reciprocal_rank") or 0) for row in relevance_rows) / max(1, len(relevance_rows)), 6),
        "recall_at_target_rank": round(recall_count / max(1, len(relevance_rows)), 6),
        "duplicate_result_count": duplicate_count,
        "duplicate_result_rate": round(duplicate_count / max(1, retrieved_count), 6),
        "authority_question_count": len(authority_rows),
        "authority_pass_rate": round(sum(1 for row in authority_rows if row.get("authority_passed")) / max(1, len(authority_rows)), 6),
        "mean_latency_ms": round(sum(latencies) / max(1, len(latencies)), 3),
        "p95_latency_ms": round(latencies[p95_index], 3) if latencies else 0.0,
    }
