from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from .claims import APPROVED_CLAIMS_PATH, claim_export_report
from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .media import transcript_index_path
from .paths import NORMALIZED_DIR, REVIEW_DIR


CLAIM_MODEL_EVALUATION_DIR = REVIEW_DIR / "claim-model-evaluations"
DEFAULT_CONTEXT_CHARS = 8_000
STOP_WORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "before",
    "but",
    "can",
    "for",
    "from",
    "has",
    "have",
    "into",
    "its",
    "not",
    "rock",
    "should",
    "that",
    "the",
    "their",
    "this",
    "through",
    "use",
    "using",
    "when",
    "with",
}


def claim_provenance_report(path: Path = APPROVED_CLAIMS_PATH) -> dict[str, Any]:
    rows = list(read_jsonl(path))
    report = claim_export_report(rows, path)["generation_provenance"]
    return {
        "schema": "rock-kb-claim-provenance-report-v1",
        "generated_at": generated_at_iso(),
        "claim_count": len(rows),
        **report,
    }


def build_claim_model_evaluation_sample(
    model: str,
    sample_size: int = 48,
    claims_path: Path = APPROVED_CLAIMS_PATH,
    output_path: Path | None = None,
    legacy_only: bool = True,
    max_context_chars: int = DEFAULT_CONTEXT_CHARS,
) -> dict[str, Any]:
    model = model.strip()
    if not model:
        raise ValueError("model must not be empty")
    if sample_size < 1:
        raise ValueError("sample_size must be at least 1")
    claims = list(read_jsonl(claims_path))
    eligible = [row for row in claims if not legacy_only or not row.get("generation_provenance")]
    selected = stratified_claim_sample(eligible, min(sample_size, len(eligible)), model)
    promotions = promotion_index()
    normalized = normalized_record_index()
    transcript_cache: dict[str, dict[tuple[str, str], dict[str, Any]]] = {}
    records = [
        claim_evaluation_record(
            row,
            model=model,
            promotions=promotions,
            normalized=normalized,
            transcript_cache=transcript_cache,
            max_context_chars=max_context_chars,
        )
        for row in selected
    ]
    output = output_path or default_evaluation_sample_path(model)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output, records)
    return {
        "schema": "rock-kb-claim-model-evaluation-sample-result-v1",
        "generated_at": generated_at_iso(),
        "model": model,
        "legacy_only": legacy_only,
        "eligible_claims": len(eligible),
        "sample_size": len(records),
        "source_context_available": sum(row["source_context_kind"] != "unavailable" for row in records),
        "output": str(output),
        "strata": count_values(row["stratum"] for row in records),
    }


def stratified_claim_sample(rows: Iterable[dict[str, Any]], sample_size: int, seed: str) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        source_id = primary_source_id(row)
        claim_type = str(row.get("claim_type") or "unknown")
        buckets[f"{source_id}|{claim_type}"].append(row)
    for key, bucket in buckets.items():
        bucket.sort(key=lambda row: sha256_text(f"{seed}:{key}:{row.get('claim_id')}"))
    ordered_keys = sorted(buckets, key=lambda key: sha256_text(f"{seed}:{key}"))
    selected: list[dict[str, Any]] = []
    while ordered_keys and len(selected) < sample_size:
        remaining = []
        for key in ordered_keys:
            bucket = buckets[key]
            if bucket and len(selected) < sample_size:
                selected.append(bucket.pop(0))
            if bucket:
                remaining.append(key)
        ordered_keys = remaining
    return selected


def claim_evaluation_record(
    claim: dict[str, Any],
    model: str,
    promotions: dict[str, dict[str, Any]],
    normalized: dict[str, dict[str, Any]],
    transcript_cache: dict[str, dict[tuple[str, str], dict[str, Any]]],
    max_context_chars: int,
) -> dict[str, Any]:
    source_id = primary_source_id(claim)
    context, context_kind, context_hash = source_context_for_claim(
        claim,
        source_id=source_id,
        promotions=promotions,
        normalized=normalized,
        transcript_cache=transcript_cache,
        max_chars=max_context_chars,
    )
    return {
        "schema": "rock-kb-claim-model-evaluation-item-v1",
        "evaluation_model": model,
        "claim_id": claim.get("claim_id"),
        "claim": claim.get("claim"),
        "claim_type": claim.get("claim_type"),
        "claim_tier": claim.get("claim_tier"),
        "authority_tier": claim.get("authority_tier"),
        "concept_ids": claim.get("concept_ids") or [],
        "source_refs": claim.get("source_refs") or [],
        "source_record_ids": claim.get("source_record_ids") or [],
        "stratum": f"{source_id}|{claim.get('claim_type') or 'unknown'}",
        "prior_generation_provenance": claim.get("generation_provenance"),
        "source_context_kind": context_kind,
        "source_context_hash": context_hash,
        "source_context": context,
        "rubric": {
            "source_fidelity": None,
            "specificity": None,
            "agent_actionability": None,
            "concept_routing": None,
            "temporal_precision": None,
            "duplication_risk": None,
            "recommended_action": None,
            "notes": None,
        },
    }


def source_context_for_claim(
    claim: dict[str, Any],
    source_id: str,
    promotions: dict[str, dict[str, Any]],
    normalized: dict[str, dict[str, Any]],
    transcript_cache: dict[str, dict[tuple[str, str], dict[str, Any]]],
    max_chars: int,
) -> tuple[str | None, str, str | None]:
    promotion_id = str((claim.get("derived_from") or {}).get("id") or "")
    promotion = promotions.get(promotion_id)
    if promotion:
        source_rows = transcript_cache.setdefault(source_id, load_transcripts(source_id))
        key = (str(promotion.get("media_id") or ""), str(promotion.get("transcript_hash") or ""))
        transcript_row = source_rows.get(key)
        if transcript_row and transcript_row.get("transcript"):
            context = relevant_text_window(
                str(transcript_row["transcript"]),
                str(claim.get("claim") or ""),
                max_chars=max_chars,
            )
            return context, "private_transcript_window", sha256_text(context)
    for record_id in claim.get("source_record_ids") or []:
        row = normalized.get(str(record_id))
        if not row:
            continue
        values = [row.get("title"), row.get("summary"), row.get("excerpt"), row.get("content"), row.get("full_text")]
        text = "\n\n".join(str(value).strip() for value in values if value)
        if text:
            context = relevant_text_window(text, str(claim.get("claim") or ""), max_chars=max_chars)
            return context, "normalized_source_window", sha256_text(context)
    for ref in claim.get("source_refs") or []:
        if not isinstance(ref, dict) or not ref.get("url"):
            continue
        row = normalized.get("url:" + str(ref["url"]).rstrip("/"))
        if not row:
            continue
        values = [row.get("source_title"), row.get("summary"), row.get("excerpt")]
        text = "\n\n".join(str(value).strip() for value in values if value)
        if text:
            context = relevant_text_window(text, str(claim.get("claim") or ""), max_chars=max_chars)
            return context, "normalized_source_url_window", sha256_text(context)
    return None, "unavailable", None


def promotion_index() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted((REVIEW_DIR / "public-media-promotions").glob("*.jsonl")):
        for row in read_jsonl(path):
            if row.get("id"):
                rows[str(row["id"])] = row
    return rows


def normalized_record_index() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted(NORMALIZED_DIR.glob("*.jsonl")):
        for row in read_jsonl(path):
            if row.get("id"):
                rows[str(row["id"])] = row
            urls = [row.get("source_url")]
            urls.extend(
                citation.get("url")
                for citation in row.get("citations") or []
                if isinstance(citation, dict)
            )
            for url in urls:
                if url:
                    rows.setdefault("url:" + str(url).rstrip("/"), row)
    return rows


def load_transcripts(source_id: str) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for row in read_jsonl(transcript_index_path(source_id)):
        transcript = str(row.get("transcript") or "")
        if not transcript:
            continue
        key = (str(row.get("media_id") or ""), sha256_text(transcript.strip()))
        rows[key] = row
    return rows


def relevant_text_window(text: str, claim: str, max_chars: int) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    terms = {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_-]+", claim.lower())
        if len(token) >= 4 and token not in STOP_WORDS
    }
    sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", cleaned) if item.strip()]
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: (
            -sum(1 for term in terms if term in item[1].lower()),
            item[0],
        ),
    )
    selected_indexes: set[int] = set()
    size = 0
    for index, sentence in ranked:
        if size >= max_chars:
            break
        for nearby in range(max(0, index - 1), min(len(sentences), index + 2)):
            if nearby in selected_indexes:
                continue
            selected_indexes.add(nearby)
            size += len(sentences[nearby]) + 1
            if size >= max_chars:
                break
    context = " ".join(sentences[index] for index in sorted(selected_indexes))
    return context[:max_chars].rstrip()


def primary_source_id(row: dict[str, Any]) -> str:
    refs = [ref for ref in row.get("source_refs") or [] if isinstance(ref, dict)]
    if refs and refs[0].get("source_id"):
        return str(refs[0]["source_id"])
    return str((row.get("derived_from") or {}).get("source_id") or "unknown")


def default_evaluation_sample_path(model: str) -> Path:
    safe_model = re.sub(r"[^a-z0-9_.-]+", "-", model.lower()).strip("-") or "model"
    return CLAIM_MODEL_EVALUATION_DIR / f"{safe_model}.legacy-claim-sample.jsonl"


def count_values(values: Iterable[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))
