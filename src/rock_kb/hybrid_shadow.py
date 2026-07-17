from __future__ import annotations

import json
import math
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import httpx

from .extract import sha256_text
from .jsonl import read_jsonl
from .paths import REPO_ROOT
from .service_eval import EVALUATION_SET_PATH, evaluation_metrics, hit_concepts
from .service_projection import SERVICE_DIR, SERVICE_RETRIEVAL_DOCUMENTS_PATH, build_service_projection
from .service_projection import AUTHORITY_TIER_RANK


DEFAULT_INSTANCE = "rock-kb-retrieval-shadow-stratified-dev"
DEFAULT_NAMESPACE = "default"
EMBEDDING_PRICE_PER_MILLION_TOKENS_USD = 0.012
EMBEDDING_PRICING_URL = "https://developers.cloudflare.com/workers-ai/platform/pricing/"
SHADOW_MANIFEST_PATH = SERVICE_RETRIEVAL_DOCUMENTS_PATH.parent / "hybrid-shadow-manifest.jsonl"
SHADOW_RESULTS_PATH = SERVICE_RETRIEVAL_DOCUMENTS_PATH.parent / "hybrid-shadow-results.json"
SHADOW_STUCK_AFTER_SECONDS = 30 * 60


@dataclass(frozen=True)
class CloudflareCredentials:
    account_id: str
    token: str


def prepare_shadow_documents(
    documents: Iterable[dict[str, Any]],
    destination: Path = SHADOW_MANIFEST_PATH,
    claim_limit: int = 100,
    lava_limit: int = 50,
) -> list[dict[str, Any]]:
    eligible = [document for document in documents if document.get("index_policy") == "hybrid_primary"]
    expected_ids = {
        str(value)
        for evaluation in read_jsonl(EVALUATION_SET_PATH)
        for value in evaluation.get("expected_result_ids") or []
    }
    claims = [document for document in eligible if document.get("kind") == "claim"]
    sampled_claim_ids = {
        str(document.get("id") or "")
        for document in sorted(claims, key=lambda row: sha256_text(str(row.get("id") or "")))[: max(0, claim_limit)]
    }
    lava_contexts = [document for document in eligible if document.get("kind") == "lava_context"]
    sampled_lava_ids = {
        str(document.get("id") or "")
        for document in sorted(lava_contexts, key=lambda row: sha256_text(str(row.get("id") or "")))[: max(0, lava_limit)]
    }
    targeted_lava_ids = {
        str(document.get("id") or "")
        for document in lava_contexts
        if any(term in str(document.get("text") or "").lower() for term in ["personattendance", "workflow merge"])
    }
    selected = [
        document
        for document in eligible
        if (
            document.get("kind") not in {"claim", "lava_context"}
            or (document.get("kind") == "claim" and (str(document.get("id") or "") in sampled_claim_ids or str(document.get("id") or "") in expected_ids))
            or (document.get("kind") == "lava_context" and (str(document.get("id") or "") in sampled_lava_ids or str(document.get("id") or "") in targeted_lava_ids))
        )
    ]
    rows = []
    for document in selected:
        canonical_id = str(document.get("id") or "")
        content_hash = str(document.get("content_hash") or sha256_text(str(document.get("text") or "")))
        key = f"rock-kb/{sha256_text(canonical_id)[:20]}-{content_hash[:12]}.md"
        metadata = {str(key): str(value) for key, value in (document.get("metadata") or {}).items()}
        rows.append(
            {
                "schema": "rock-kb-hybrid-shadow-item-v1",
                "id": canonical_id,
                "key": key,
                "content_hash": content_hash,
                "text": str(document.get("text") or ""),
                "metadata": metadata,
            }
        )
    rows.sort(key=lambda row: row["id"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return rows


def ensure_shadow_projection() -> list[dict[str, Any]]:
    if not SERVICE_RETRIEVAL_DOCUMENTS_PATH.exists():
        build_service_projection()
    return prepare_shadow_documents(read_jsonl(SERVICE_RETRIEVAL_DOCUMENTS_PATH))


def wrangler_credentials() -> CloudflareCredentials:
    whoami = json.loads(run_wrangler(["whoami", "--json"]))
    accounts = whoami.get("accounts") or []
    if not accounts:
        raise RuntimeError("Wrangler is authenticated but no Cloudflare account is available.")
    token_payload = json.loads(run_wrangler(["auth", "token", "--json"]))
    token = str(token_payload.get("token") or "").strip()
    if not token:
        raise RuntimeError("Wrangler did not return an authentication token.")
    return CloudflareCredentials(account_id=str(accounts[0]["id"]), token=token)


def ensure_shadow_instance(
    credentials: CloudflareCredentials, instance: str = DEFAULT_INSTANCE, namespace: str = DEFAULT_NAMESPACE
) -> dict[str, Any]:
    instances = json.loads(run_wrangler(["ai-search", "list", "--namespace", namespace, "--json"]))
    existing = next((row for row in instances if row.get("id") == instance), None)
    if existing:
        return existing
    response = httpx.post(
        f"https://api.cloudflare.com/client/v4/accounts/{credentials.account_id}/ai-search/instances",
        headers={"Authorization": f"Bearer {credentials.token}", "Content-Type": "application/json"},
        json={
            "id": instance,
            "embedding_model": "@cf/qwen/qwen3-embedding-0.6b",
            "chunk": True,
            "chunk_size": 512,
            "chunk_overlap": 30,
            "max_num_results": 10,
            "index_method": {"vector": True, "keyword": True},
            "fusion_method": "rrf",
            "indexing_options": {"keyword_tokenizer": "porter"},
            "retrieval_options": {"keyword_match_mode": "or", "boost_by": [{"field": "authority_rank", "direction": "desc"}]},
            "score_threshold": 0.2,
            "custom_metadata": [
                {"field_name": "kind", "data_type": "text"},
                {"field_name": "namespace", "data_type": "text"},
                {"field_name": "authority_rank", "data_type": "number"},
                {"field_name": "claim_tier_rank", "data_type": "number"},
                {"field_name": "concepts", "data_type": "text"},
            ],
        },
        timeout=60,
    )
    if response.is_error:
        raise RuntimeError(f"Cloudflare AI Search create failed ({response.status_code}): {response.text[:2000]}")
    payload = response.json()
    return payload.get("result") or payload


def upload_shadow_documents(
    rows: list[dict[str, Any]],
    credentials: CloudflareCredentials,
    *,
    instance: str = DEFAULT_INSTANCE,
    namespace: str = DEFAULT_NAMESPACE,
    concurrency: int = 8,
) -> dict[str, Any]:
    base_url = shadow_instance_url(credentials.account_id, instance, namespace)
    headers = {"Authorization": f"Bearer {credentials.token}"}
    existing = list_shadow_items(credentials, instance=instance, namespace=namespace)
    desired_keys = {str(row["key"]) for row in rows}
    reconciliation = shadow_reconciliation_plan(existing, desired_keys)
    deleted = delete_shadow_items(
        [row["item"] for row in reconciliation],
        credentials,
        instance=instance,
        namespace=namespace,
        concurrency=concurrency,
    )
    deleted_ids = {str(row.get("id") or "") for row in deleted}
    existing = [row for row in existing if str(row.get("id") or "") not in deleted_ids]
    accepted_statuses = {"queued", "running", "completed"}
    existing_keys = {str(row.get("key") or "") for row in existing if str(row.get("status") or "") in accepted_statuses}
    pending_rows = [row for row in rows if row["key"] not in existing_keys]

    def upload(row: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(6):
            try:
                response = httpx.post(
                    f"{base_url}/items",
                    headers=headers,
                    files={"file": (row["key"], row["text"].encode("utf-8"), "text/markdown")},
                    data={"metadata": json.dumps(row["metadata"], separators=(",", ":"))},
                    timeout=90,
                )
            except httpx.HTTPError as exc:
                if attempt == 5:
                    raise RuntimeError(f"Cloudflare AI Search upload failed for {row['id']}: {exc}") from exc
                time.sleep(min(2**attempt, 20))
                continue
            if not response.is_error:
                payload = response.json()
                return payload.get("result") or payload
            if response.status_code not in {429, 500, 502, 503, 504} or attempt == 5:
                raise RuntimeError(
                    f"Cloudflare AI Search upload failed for {row['id']} ({response.status_code}): {response.text[:1000]}"
                )
            time.sleep(min(2**attempt, 20))
        raise AssertionError("unreachable")

    worker_count = max(1, min(concurrency, len(pending_rows) or 1))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        uploaded = list(executor.map(upload, pending_rows))
    return {
        "uploaded": len(uploaded),
        "already_present": len(rows) - len(pending_rows),
        "deleted": len(deleted),
        "deleted_by_reason": count_values(str(row["reason"]) for row in reconciliation),
        "keys": [str(row.get("key") or "") for row in uploaded],
    }


def shadow_reconciliation_plan(
    items: list[dict[str, Any]],
    desired_keys: set[str],
    *,
    now: datetime | None = None,
    stuck_after_seconds: int = SHADOW_STUCK_AFTER_SECONDS,
) -> list[dict[str, Any]]:
    current_time = now or datetime.now(timezone.utc)
    plan: list[dict[str, Any]] = []
    for item in items:
        key = str(item.get("key") or "")
        status = str(item.get("status") or "")
        reason = ""
        if key not in desired_keys:
            reason = "obsolete"
        elif status in {"error", "skipped", "outdated"}:
            reason = "retryable_status"
        elif status in {"queued", "running"} and shadow_item_age_seconds(item, current_time) >= stuck_after_seconds:
            reason = "stuck_pending"
        if reason:
            plan.append({"reason": reason, "item": item})
    return plan


def shadow_item_age_seconds(item: dict[str, Any], now: datetime) -> float:
    value = str(item.get("last_seen_at") or item.get("created_at") or "").strip()
    if not value:
        return 0
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return 0
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return max(0, (now - timestamp.astimezone(timezone.utc)).total_seconds())


def delete_shadow_items(
    items: list[dict[str, Any]],
    credentials: CloudflareCredentials,
    *,
    instance: str = DEFAULT_INSTANCE,
    namespace: str = DEFAULT_NAMESPACE,
    concurrency: int = 8,
) -> list[dict[str, Any]]:
    base_url = f"{shadow_instance_url(credentials.account_id, instance, namespace)}/items"
    headers = {"Authorization": f"Bearer {credentials.token}"}

    def delete(item: dict[str, Any]) -> dict[str, Any]:
        item_id = str(item.get("id") or "")
        if not item_id:
            raise RuntimeError(f"Cloudflare AI Search item has no ID: {item.get('key')}")
        for attempt in range(5):
            try:
                response = httpx.delete(f"{base_url}/{item_id}", headers=headers, timeout=60)
            except httpx.HTTPError as exc:
                if attempt == 4:
                    raise RuntimeError(f"Cloudflare AI Search delete failed for {item.get('key')}: {exc}") from exc
                time.sleep(min(2**attempt, 10))
                continue
            if not response.is_error or response.status_code == 404:
                return item
            if response.status_code not in {429, 500, 502, 503, 504} or attempt == 4:
                raise RuntimeError(
                    f"Cloudflare AI Search delete failed for {item.get('key')} ({response.status_code}): {response.text[:1000]}"
                )
            time.sleep(min(2**attempt, 10))
        raise AssertionError("unreachable")

    worker_count = max(1, min(concurrency, 4, len(items) or 1))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        return list(executor.map(delete, items))


def list_shadow_items(
    credentials: CloudflareCredentials,
    *,
    instance: str = DEFAULT_INSTANCE,
    namespace: str = DEFAULT_NAMESPACE,
) -> list[dict[str, Any]]:
    base_url = f"{shadow_instance_url(credentials.account_id, instance, namespace)}/items"
    headers = {"Authorization": f"Bearer {credentials.token}"}
    page = 1
    rows: list[dict[str, Any]] = []
    while True:
        response = httpx.get(base_url, headers=headers, params={"page": page, "per_page": 50}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        result = payload.get("result") or []
        if isinstance(result, dict):
            result = result.get("result") or result.get("items") or []
        rows.extend(result)
        result_info = payload.get("result_info") or {}
        total = int(result_info.get("total_count") or len(rows))
        if not result or len(rows) >= total:
            return rows
        page += 1


def wait_for_shadow_index(
    credentials: CloudflareCredentials,
    *,
    expected_count: int,
    expected_keys: set[str] | None = None,
    instance: str = DEFAULT_INSTANCE,
    namespace: str = DEFAULT_NAMESPACE,
    timeout: float = 900,
    interval: float = 10,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_stats: dict[str, Any] = {}
    headers = {"Authorization": f"Bearer {credentials.token}"}
    url = f"{shadow_instance_url(credentials.account_id, instance, namespace)}/stats"
    while time.monotonic() < deadline:
        if expected_keys is not None:
            items = list_shadow_items(credentials, instance=instance, namespace=namespace)
            status_by_key = {str(item.get("key") or ""): str(item.get("status") or "") for item in items}
            statuses = [status_by_key.get(key, "missing") for key in expected_keys]
            counts = count_values(statuses)
            last_stats = {
                "item_status_counts": counts,
                "shadow_readiness": {
                    "expected": len(expected_keys),
                    "completed": int(counts.get("completed") or 0),
                    "ready": int(counts.get("completed") or 0) == len(expected_keys),
                },
            }
            if last_stats["shadow_readiness"]["ready"]:
                return last_stats
            if int(counts.get("error") or 0) or int(counts.get("skipped") or 0):
                raise RuntimeError(f"AI Search indexing failed for current shadow items: {counts}")
            time.sleep(interval)
            continue

        allowed_pending = max(1, math.floor(expected_count * 0.005))
        minimum_completed = expected_count - allowed_pending
        response = httpx.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        last_stats = payload.get("result") or payload
        counts = shadow_item_counts(last_stats)
        if counts["completed"] >= minimum_completed and counts["pending"] <= allowed_pending:
            last_stats["shadow_readiness"] = {
                "expected": expected_count,
                "completed": counts["completed"],
                "allowed_pending": allowed_pending,
                "ready": True,
            }
            return last_stats
        time.sleep(interval)
    raise TimeoutError(f"AI Search indexing did not complete within {timeout:.0f}s: {last_stats}")


def count_values(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def evaluate_shadow(
    rows: list[dict[str, Any]],
    credentials: CloudflareCredentials,
    *,
    instance: str = DEFAULT_INSTANCE,
    namespace: str = DEFAULT_NAMESPACE,
    limit: int = 10,
    concurrency: int = 6,
) -> dict[str, Any]:
    id_by_key = {row["key"]: row["id"] for row in rows}
    indexed_ids = set(id_by_key.values())
    evaluations = list(read_jsonl(EVALUATION_SET_PATH))
    base_url = f"{shadow_instance_url(credentials.account_id, instance, namespace)}/search"
    headers = {"Authorization": f"Bearer {credentials.token}", "Content-Type": "application/json"}

    def evaluate(row: dict[str, Any]) -> dict[str, Any]:
        expected_ids = [str(value) for value in row.get("expected_result_ids") or []]
        eligible_expected_ids = [value for value in expected_ids if value in indexed_ids]
        if expected_ids and not eligible_expected_ids:
            return {"id": row.get("id"), "question": row.get("question"), "source": row.get("source"), "evaluation_mode": row.get("evaluation_mode"), "status": "skip", "reason": "expected item excluded by index policy"}
        started = time.perf_counter()
        response = httpx.post(
            base_url,
            headers=headers,
            json={"messages": [{"role": "user", "content": str(row.get("question") or "")}], "max_num_results": limit},
            timeout=60,
        )
        response.raise_for_status()
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        payload = response.json()
        hits = shadow_hits(payload, id_by_key)
        result = score_shadow_row(row, hits, eligible_expected_ids, limit)
        result["latency_ms"] = latency_ms
        return result

    worker_count = max(1, min(concurrency, len(evaluations) or 1))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(executor.map(evaluate, evaluations))
    scored = [row for row in results if row["status"] != "skip"]
    retrieval_results = [
        row
        for row in scored
        if row.get("evaluation_mode") == "retrieval" or str(row.get("source") or "").startswith("curated_")
    ]
    generated_results = [row for row in scored if row.get("evaluation_mode") == "answer_structure"]
    failures = sum(1 for row in scored if row["status"] == "fail")
    latencies = sorted(float(row.get("latency_ms") or 0) for row in scored)
    report = {
        "schema": "rock-kb-hybrid-shadow-evaluation-v1",
        "instance": instance,
        "status": "fail" if failures else "ok",
        "pass_count": len(scored) - failures,
        "fail_count": failures,
        "skip_count": len(results) - len(scored),
        "metrics": evaluation_metrics(scored),
        "cohorts": {
            "curated_retrieval": cohort_report(retrieval_results),
            "generated_answer_structure": cohort_report(generated_results),
        },
        "latency_ms": {
            "mean": round(sum(latencies) / max(1, len(latencies)), 2),
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "max": round(max(latencies, default=0), 2),
        },
        "estimated_embedding_cost": shadow_cost_estimate(rows, len(scored)),
        "results": results,
    }
    SHADOW_RESULTS_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def score_shadow_row(
    row: dict[str, Any], hits: list[dict[str, Any]], expected_ids: list[str], limit: int
) -> dict[str, Any]:
    max_rank = max(1, min(int(row.get("max_rank") or 2), limit))
    expected_concept = str(row.get("concept_id") or "")
    expected_kinds = [str(value) for value in row.get("expected_result_kinds") or []]
    forbidden_ids = [str(value) for value in row.get("forbidden_result_ids") or []]
    ordered_ids = [str(hit.get("id") or "") for hit in hits]
    ordered_kinds = [str(hit.get("kind") or "") for hit in hits]
    ordered_authority_ranks = [int(hit.get("authority_rank") or 0) for hit in hits]
    expected_id_rank = first_rank(ordered_ids, expected_ids)
    expected_kind_rank = first_rank(ordered_kinds, expected_kinds)
    concept_rank = next((index + 1 for index, hit in enumerate(hits) if expected_concept in hit_concepts(hit)), None)
    forbidden_rank = first_rank(ordered_ids, forbidden_ids)
    relevant_rank = expected_id_rank if expected_ids else expected_kind_rank if expected_kinds else concept_rank
    relevant_indexes = [
        index
        for index, hit in enumerate(hits)
        if (expected_ids and str(hit.get("id") or "") in expected_ids)
        or (not expected_ids and expected_kinds and str(hit.get("kind") or "") in expected_kinds)
        or (not expected_ids and not expected_kinds and expected_concept in hit_concepts(hit))
    ]
    required_authorities = [str(value) for value in row.get("required_authority_tiers") or []]
    required_authority_ranks = {AUTHORITY_TIER_RANK.get(value, -1) for value in required_authorities}
    authority_passed = not required_authorities or any(
        ordered_authority_ranks[index] in required_authority_ranks for index in relevant_indexes if index < max_rank
    )
    required_terms = [str(term).lower() for term in row.get("required_terms") or []]
    serialized = json.dumps(hits, ensure_ascii=False).lower()
    missing_terms = [term for term in required_terms if term not in serialized]
    duplicate_count = len(ordered_ids) - len(set(ordered_ids))
    passed = bool(hits) and relevant_rank is not None and relevant_rank <= max_rank and authority_passed and not missing_terms and not duplicate_count
    if forbidden_rank is not None and forbidden_rank <= int(row.get("forbidden_max_rank") or max_rank):
        passed = False
    return {
        "id": row.get("id"),
        "question": row.get("question"),
        "expected_concept": expected_concept,
        "max_allowed_rank": max_rank,
        "hit_count": len(hits),
        "result_ids": ordered_ids,
        "result_kinds": ordered_kinds,
        "relevant_rank": relevant_rank,
        "reciprocal_rank": round(1 / relevant_rank, 6) if relevant_rank else 0.0,
        "has_relevance_expectation": True,
        "required_authority_tiers": required_authorities,
        "authority_passed": authority_passed,
        "duplicate_count": duplicate_count,
        "missing_terms": missing_terms,
        "source": row.get("source"),
        "evaluation_mode": row.get("evaluation_mode"),
        "status": "pass" if passed else "fail",
    }


def shadow_hits(payload: dict[str, Any], id_by_key: dict[str, str]) -> list[dict[str, Any]]:
    raw = payload.get("result") or payload
    data = (raw.get("data") or raw.get("chunks")) if isinstance(raw, dict) else []
    hits = []
    hit_by_key: dict[str, dict[str, Any]] = {}
    for hit in data or []:
        item = hit.get("item") or {}
        metadata = item.get("metadata") or hit.get("metadata") or {}
        concepts = [value for value in str(metadata.get("concepts") or "").split("|") if value]
        key = str(item.get("key") or hit.get("filename") or "")
        if key in hit_by_key:
            existing_text = str(hit_by_key[key].get("text") or "")
            next_text = str(hit.get("text") or "")
            if next_text and next_text not in existing_text:
                hit_by_key[key]["text"] = f"{existing_text}\n{next_text}".strip()
            continue
        result = {
                "id": id_by_key.get(key, key),
                "kind": str(metadata.get("kind") or ""),
                "concepts": concepts,
                "authority_rank": int(metadata.get("authority_rank") or 0),
                "text": str(hit.get("text") or ""),
                "score": hit.get("score"),
            }
        hit_by_key[key] = result
        hits.append(result)
    return hits


def shadow_item_counts(stats: dict[str, Any]) -> dict[str, int]:
    text = json.dumps(stats).lower()
    counts = stats.get("items") or stats.get("item_status_counts") or stats.get("status_counts") or {}
    if not counts and any(key in stats for key in ["completed", "queued", "running", "error"]):
        counts = stats
    if isinstance(counts, list):
        counts = {str(row.get("status") or ""): int(row.get("count") or 0) for row in counts}
    completed = int(counts.get("completed") or stats.get("items_completed") or 0)
    pending = sum(int(counts.get(key) or 0) for key in ["queued", "running", "outdated"])
    if not counts and "completed" not in text:
        return {"completed": 0, "pending": 1}
    return {"completed": completed, "pending": pending}


def shadow_instance_url(account_id: str, instance: str, namespace: str) -> str:
    return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai-search/namespaces/{namespace}/instances/{instance}"


def first_rank(values: list[str], expected: list[str]) -> int | None:
    return next((index + 1 for index, value in enumerate(values) if value in expected), None)


def shadow_cost_estimate(rows: list[dict[str, Any]], query_count: int = 0) -> dict[str, Any]:
    corpus_tokens = round(sum(len(str(row.get("text") or "")) for row in rows) / 4)
    query_tokens = query_count * 32
    estimated_tokens = corpus_tokens + query_tokens
    return {
        "model": "@cf/qwen/qwen3-embedding-0.6b",
        "estimated_tokens": estimated_tokens,
        "estimated_usd_before_free_allocation": round(
            estimated_tokens / 1_000_000 * EMBEDDING_PRICE_PER_MILLION_TOKENS_USD, 6
        ),
        "pricing_url": EMBEDDING_PRICING_URL,
        "note": "Token count uses a conservative four-characters-per-token estimate; Cloudflare bills actual model input.",
    }


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    index = min(len(values) - 1, max(0, round((len(values) - 1) * fraction)))
    return round(values[index], 2)


def cohort_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    failures = sum(1 for row in rows if row.get("status") == "fail")
    return {
        "question_count": len(rows),
        "pass_count": len(rows) - failures,
        "fail_count": failures,
        "metrics": evaluation_metrics(rows),
    }


def run_wrangler(arguments: list[str]) -> str:
    result = subprocess.run(
        ["npx", "wrangler", *arguments],
        cwd=SERVICE_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Wrangler command failed: {message}")
    return result.stdout
