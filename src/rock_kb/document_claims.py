from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable, Iterable

import httpx

from .claims import (
    CLAIM_TYPES,
    SOURCE_CLAIM_REVIEW_SCHEMA,
    approved_claim_rows,
    source_claim_review_to_claim,
    validate_claim_rows,
)
from .community import fetch_rockumentation_payload, rockumentation_readable_text
from .concepts import (
    concept_has_path_constraints,
    concept_source_records,
    get_concept,
    load_concepts,
    rank_records_for_concept,
    record_matches_path_constraints,
    score_text,
)
from .extract import USER_AGENT, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REVIEW_DIR


DOCUMENT_CLAIM_CANDIDATE_SCHEMA = "rock-kb-document-claim-candidate-v1"
DOCUMENT_CLAIM_REWRITE_SCHEMA = "rock-kb-document-claim-rewrite-v1"
DEFAULT_DOCUMENT_CLAIM_CONCEPTS = [
    "workflows",
    "data-views-reports",
    "security-permissions",
    "groups",
    "cms-websites",
    "check-in",
    "communications",
    "event-registration",
    "giving-finance",
    "mobile",
    "api-integrations",
    "people-families",
    "connections",
    "scheduling-locations",
    "system-admin-ops",
    "serving-volunteer-ops",
    "learning-lms-engagement",
    "documents-signatures",
    "hosting-infrastructure",
    "prayer-care",
    "engagement-tracking",
    "content-personalization",
    "obsidian-development",
]
DEFAULT_DOCUMENT_SOURCE_IDS = {
    "rock_documentation",
    "rock_developer",
    "rock_mobile_docs",
}
DEFAULT_CANDIDATE_PATH = REVIEW_DIR / "source-claim-candidates" / "official-docs.jsonl"
DEFAULT_REVIEW_PATH = REVIEW_DIR / "source-claim-reviews" / "official-docs-sol-v1.jsonl"
MAX_SOURCE_CONTEXT_CHARS = 60_000


def build_document_claim_candidates(
    concept_ids: Iterable[str] | None = None,
    limit_per_concept: int = 8,
    output_path: Path = DEFAULT_CANDIDATE_PATH,
    records: list[dict[str, Any]] | None = None,
    context_loader: Callable[[dict[str, Any]], str] | None = None,
    require_full_text: bool = True,
    source_ids: Iterable[str] | None = None,
    source_record_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    if limit_per_concept < 1:
        raise ValueError("limit_per_concept must be at least 1")
    requested = list(concept_ids or DEFAULT_DOCUMENT_CLAIM_CONCEPTS)
    requested_source_ids = sorted(
        {
            str(source_id).strip()
            for source_id in (source_ids or DEFAULT_DOCUMENT_SOURCE_IDS)
            if str(source_id).strip()
        }
    )
    if not requested_source_ids:
        raise ValueError("source_ids must contain at least one source ID")
    allowed_source_ids = set(requested_source_ids)
    requested_record_ids = {
        str(source_record_id).strip()
        for source_record_id in (source_record_ids or [])
        if str(source_record_id).strip()
    }
    concepts = {concept.id: concept for concept in load_concepts()}
    unknown = sorted(set(requested) - set(concepts))
    if unknown:
        raise ValueError("Unknown concept IDs: " + ", ".join(unknown))
    source_records = records if records is not None else concept_source_records()
    existing_by_concept = existing_claims_by_concept()
    selected: list[tuple[Any, dict[str, Any], int]] = []
    skipped: list[dict[str, Any]] = []
    for concept_id in requested:
        concept = concepts[concept_id]
        ranked = rank_records_for_concept(concept, source_records)
        ranked_ids = {str(record.get("id") or "") for record in ranked}
        ranked.extend(
            sorted(
                (
                    record
                    for record in source_records
                    if str(record.get("id") or "") in requested_record_ids
                    and str(record.get("id") or "") not in ranked_ids
                ),
                key=lambda record: str(record.get("id") or ""),
            )
        )
        eligible = []
        for rank, record in enumerate(ranked):
            if str(record.get("source_id") or "") not in allowed_source_ids:
                continue
            if (
                concept_has_path_constraints(concept)
                and str(record.get("source_id") or "")
                in DEFAULT_DOCUMENT_SOURCE_IDS
                and not record_matches_path_constraints(record, concept.raw)
            ):
                continue
            if not record.get("id") or not str(record.get("source_url") or "").startswith("http"):
                continue
            context = normalized_document_context(record)
            if len(context) < 100:
                skipped.append({"concept_id": concept_id, "source_record_id": record.get("id"), "reason": "insufficient_normalized_context"})
                continue
            quality = document_candidate_quality_score(record, concept.keywords, rank)
            eligible.append((quality, str(record.get("documentation_path") or record.get("source_url") or ""), record))
        eligible.sort(key=lambda item: (-item[0], item[1]))
        concept_selection = reserve_subguide_coverage(concept, eligible, limit_per_concept)
        selected.extend((concept, record, quality) for quality, _path, record in concept_selection)

    rows: list[dict[str, Any]] = []
    if context_loader is not None:
        rows, hydration_skips = hydrate_document_candidates(
            selected,
            context_loader=context_loader,
            existing_by_concept=existing_by_concept,
            require_full_text=require_full_text,
        )
        skipped.extend(hydration_skips)
    else:
        with httpx.Client(follow_redirects=True, timeout=30, headers={"User-Agent": USER_AGENT}) as client:
            rows, hydration_skips = hydrate_document_candidates(
                selected,
                context_loader=lambda record: rockumentation_source_context(client, record),
                existing_by_concept=existing_by_concept,
                require_full_text=require_full_text,
            )
            skipped.extend(hydration_skips)

    rows.sort(
        key=lambda row: (
            tuple(str(value) for value in row.get("concept_ids") or []),
            str(row.get("source_url") or ""),
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_path, rows)
    return {
        "schema": "rock-kb-document-claim-candidate-build-v1",
        "status": "ok",
        "concept_ids": requested,
        "source_ids": requested_source_ids,
        "source_record_ids": sorted(requested_record_ids),
        "limit_per_concept": limit_per_concept,
        "candidate_count": len(rows),
        "full_text_candidates": sum(
            str(row.get("source_context_mode") or "").endswith("_full_text")
            for row in rows
        ),
        "skipped_count": len(skipped),
        "skipped": skipped[:50],
        "output": str(output_path),
    }


def hydrate_document_candidates(
    selected: list[tuple[Any, dict[str, Any], int]],
    context_loader: Callable[[dict[str, Any]], str],
    existing_by_concept: dict[str, list[dict[str, Any]]],
    require_full_text: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    skipped = []
    grouped: dict[str, dict[str, Any]] = {}
    for concept, record, quality in selected:
        record_id = str(record.get("id") or "")
        if not record_id:
            continue
        entry = grouped.setdefault(
            record_id,
            {
                "record": record,
                "concepts": {},
                "quality": quality,
            },
        )
        entry["concepts"][concept.id] = concept
        entry["quality"] = max(int(entry["quality"]), quality)

    ordered = sorted(
        grouped.values(),
        key=lambda entry: (
            tuple(sorted(entry["concepts"])),
            str(entry["record"].get("source_url") or ""),
        ),
    )
    for entry in ordered:
        record = entry["record"]
        concepts = [
            entry["concepts"][concept_id]
            for concept_id in sorted(entry["concepts"])
        ]
        concept_ids = [concept.id for concept in concepts]
        quality = int(entry["quality"])
        full_text = " ".join(str(context_loader(record) or "").split())
        source_id = str(record.get("source_id") or "")
        context_mode = (
            "rockumentation_full_text"
            if full_text and source_id in DEFAULT_DOCUMENT_SOURCE_IDS
            else "official_source_full_text"
            if full_text
            else "normalized_summary"
        )
        source_context = full_text or normalized_document_context(record)
        if require_full_text and not context_mode.endswith("_full_text"):
            skipped.append(
                {
                    "concept_ids": concept_ids,
                    "source_record_id": record.get("id"),
                    "reason": "official_full_text_unavailable",
                }
            )
            continue
        truncated = len(source_context) > MAX_SOURCE_CONTEXT_CHARS
        if truncated and require_full_text:
            skipped.append(
                {
                    "concept_ids": concept_ids,
                    "source_record_id": record.get("id"),
                    "reason": "rockumentation_full_text_exceeds_review_limit",
                }
            )
            continue
        if truncated:
            context_mode += "_truncated"
        source_context = source_context[:MAX_SOURCE_CONTEXT_CHARS]
        source_input_hash = sha256_text(source_context)
        candidate_id = "document-claim-candidate:" + sha256_text(
            f"{','.join(concept_ids)}:{record.get('id')}:{source_input_hash}"
        )[:20]
        existing_claims: dict[str, dict[str, Any]] = {}
        for concept in concepts:
            for claim in relevant_existing_claims(
                source_context,
                existing_by_concept.get(concept.id, []),
            ):
                existing_claims[str(claim.get("claim_id") or "")] = claim
        rows.append(
            {
                "schema": DOCUMENT_CLAIM_CANDIDATE_SCHEMA,
                "id": candidate_id,
                "source_record_id": record.get("id"),
                "source_id": record.get("source_id"),
                "source_url": record.get("source_url"),
                "source_title": record.get("source_title"),
                "concept_ids": concept_ids,
                "documentation_path": record.get("documentation_path"),
                "documentation_branches": record.get("documentation_branches") or [],
                "documentation_article_id": record.get("documentation_article_id"),
                "documentation_current_version": record.get("documentation_current_version"),
                "normalized_content_hash": record.get("content_hash"),
                "source_input_hash": source_input_hash,
                "source_context_hash": source_input_hash,
                "source_context_mode": context_mode,
                "source_context_truncated": truncated,
                "source_context": source_context,
                "existing_claims": [
                    existing_claims[claim_id]
                    for claim_id in sorted(existing_claims)
                    if claim_id
                ],
                "selection_score": quality,
                "review_status": "needs_agent_distillation",
                "recommended_prompt_id": "rock-kb-source-claim-distillation",
                "recommended_prompt_version": "1.1.0",
            }
        )
    return rows, skipped


def rockumentation_source_context(client: httpx.Client, record: dict[str, Any]) -> str:
    payload = fetch_rockumentation_payload(client, str(record.get("source_url") or ""))
    return rockumentation_readable_text(payload)


def normalized_document_context(record: dict[str, Any]) -> str:
    values = [record.get("source_title"), record.get("summary"), record.get("excerpt")]
    return "\n\n".join(str(value).strip() for value in values if value)


def document_candidate_quality_score(record: dict[str, Any], keywords: list[str], rank: int) -> int:
    text = normalized_document_context(record).lower()
    path = str(record.get("documentation_path") or "")
    toc_links = int(record.get("documentation_table_of_contents_link_count") or 0)
    score = max(0, 1_000 - rank)
    score += min(80, score_text(text, keywords) * 4)
    score += min(30, path.count("/") * 3)
    if toc_links <= 1:
        score += 80
    if text.startswith("sections ") or text.count("](") >= 4:
        score -= 160
    if record.get("documentation_article_id"):
        score += 10
    return score


def reserve_subguide_coverage(
    concept: Any,
    eligible: list[tuple[int, str, dict[str, Any]]],
    limit: int,
) -> list[tuple[int, str, dict[str, Any]]]:
    selected: list[tuple[int, str, dict[str, Any]]] = []
    selected_ids: set[str] = set()
    for subguide in concept.subguides:
        matches = [item for item in eligible if record_matches_subguide(item[2], subguide)]
        if not matches:
            continue
        best = matches[0]
        record_id = str(best[2].get("id") or "")
        if record_id and record_id not in selected_ids:
            selected.append(best)
            selected_ids.add(record_id)
        if len(selected) >= limit:
            return selected
    for item in eligible:
        record_id = str(item[2].get("id") or "")
        if not record_id or record_id in selected_ids:
            continue
        selected.append(item)
        selected_ids.add(record_id)
        if len(selected) >= limit:
            break
    return selected


def record_matches_subguide(record: dict[str, Any], subguide: dict[str, Any]) -> bool:
    if any(
        subguide.get(key)
        for key in ["source_url_prefixes", "developer_doc_prefixes", "documentation_branches", "documentation_path_prefixes"]
    ):
        return record_matches_path_constraints(record, subguide)
    keywords = [str(value) for value in subguide.get("keywords") or [] if value]
    return bool(keywords and score_text(normalized_document_context(record).lower(), keywords) > 0)


def existing_claims_by_concept() -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in approved_claim_rows():
        for concept_id in row.get("concept_ids") or []:
            grouped.setdefault(str(concept_id), []).append(row)
    return grouped


def relevant_existing_claims(source_context: str, claims: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    context_tokens = significant_tokens(source_context)
    scored = []
    for claim in claims:
        claim_tokens = significant_tokens(str(claim.get("claim") or ""))
        overlap = len(context_tokens & claim_tokens)
        scored.append((overlap, str(claim.get("claim_id") or ""), claim))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [
        {
            "claim_id": claim.get("claim_id"),
            "claim": claim.get("claim"),
            "authority_tier": claim.get("authority_tier"),
            "source_refs": claim.get("source_refs") or [],
        }
        for overlap, _claim_id, claim in scored[:limit]
        if overlap > 0
    ]


def significant_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_-]+", value.lower())
        if len(token) >= 4 and token not in {"rock", "that", "this", "with", "from", "have", "your", "will"}
    }


def promote_document_claim_rewrites(
    candidate_path: Path,
    rewrite_path: Path,
    output_path: Path = DEFAULT_REVIEW_PATH,
    reviewer: str = "local-review",
    model: str = "gpt-5.6-sol",
    prompt_id: str = "rock-kb-source-claim-distillation",
    prompt_version: str = "1.1.0",
    method: str = "agent_reviewed_full_article",
) -> dict[str, Any]:
    candidates = {str(row.get("id") or ""): row for row in read_jsonl(candidate_path) if row.get("id")}
    if not candidates:
        raise ValueError(f"No document claim candidates found at {candidate_path}")
    known_concepts = {concept.id for concept in load_concepts()}
    existing_claims_by_text: dict[str, list[dict[str, Any]]] = {}
    for row in approved_claim_rows():
        existing_claims_by_text.setdefault(normalize_claim_text(str(row.get("claim") or "")), []).append(row)
    promoted_claim_texts: set[str] = set()
    reviewed_at = now_iso()
    promoted: list[dict[str, Any]] = []
    promoted_candidates: set[str] = set()
    claimful_candidates: set[str] = set()
    for line_number, rewrite in enumerate(read_jsonl(rewrite_path), start=1):
        candidate_id = str(rewrite.get("candidate_id") or "")
        candidate = candidates.get(candidate_id)
        if not candidate:
            raise ValueError(f"{rewrite_path}:{line_number} has unknown candidate_id {candidate_id!r}")
        if rewrite.get("schema") not in {None, DOCUMENT_CLAIM_REWRITE_SCHEMA}:
            raise ValueError(f"{rewrite_path}:{line_number} has unsupported schema {rewrite.get('schema')}")
        if str(rewrite.get("source_input_hash") or "") != str(candidate.get("source_input_hash") or ""):
            raise ValueError(f"{rewrite_path}:{line_number} source_input_hash does not match the candidate")
        if candidate.get("source_context_truncated") and method == "agent_reviewed_full_article":
            raise ValueError(
                f"{rewrite_path}:{line_number} cannot use agent_reviewed_full_article with truncated source context"
            )
        claim_items = rewrite.get("claims") or []
        if not isinstance(claim_items, list):
            raise ValueError(f"{rewrite_path}:{line_number} claims must be an array")
        for item_index, item in enumerate(claim_items, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} must be an object")
            claim_text = " ".join(str(item.get("claim") or "").split())
            if len(claim_text) < 40:
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} is too short")
            if claim_text in str(candidate.get("source_context") or ""):
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} appears to copy source text verbatim")
            normalized_claim = normalize_claim_text(claim_text)
            if normalized_claim in promoted_claim_texts:
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} duplicates another promoted claim")
            existing_matches = existing_claims_by_text.get(normalized_claim) or []
            if existing_matches and not any(
                str((row.get("derived_from") or {}).get("candidate_id") or "") == candidate_id
                for row in existing_matches
            ):
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} duplicates an approved claim")
            claim_type = str(item.get("claim_type") or "operational_guidance")
            if claim_type not in CLAIM_TYPES:
                raise ValueError(f"{rewrite_path}:{line_number} claim {item_index} has invalid claim_type {claim_type}")
            concept_ids = sorted(
                {
                    str(value)
                    for value in [*(candidate.get("concept_ids") or []), *(item.get("concept_ids") or [])]
                    if value
                }
            )
            unknown_concepts = sorted(set(concept_ids) - known_concepts)
            if unknown_concepts:
                raise ValueError(
                    f"{rewrite_path}:{line_number} claim {item_index} has unknown concept IDs: {', '.join(unknown_concepts)}"
                )
            source_input_hash = str(candidate["source_input_hash"])
            rock_versions = normalized_rock_versions(candidate, item)
            version_scope_status = normalized_version_scope_status(item, rock_versions)
            review_id = "source-claim:" + sha256_text(f"{candidate_id}:{claim_text}")[:20]
            review = {
                "schema": SOURCE_CLAIM_REVIEW_SCHEMA,
                "id": review_id,
                "candidate_id": candidate_id,
                "claim": claim_text,
                "claim_type": claim_type,
                "concept_ids": concept_ids,
                "source_id": candidate.get("source_id"),
                "source_url": candidate.get("source_url"),
                "source_title": candidate.get("source_title"),
                "source_refs": [
                    {
                        "source_id": candidate.get("source_id"),
                        "url": candidate.get("source_url"),
                        "title": candidate.get("source_title"),
                    }
                ],
                "source_record_ids": [candidate.get("source_record_id")],
                "authority_tier": "official",
                "confidence": str(item.get("confidence") or "high"),
                "review_status": "approved_for_public_distillation",
                "reviewed_at": reviewed_at,
                "reviewer": reviewer,
                "license_status": "cite_and_summarize_only",
                "public_publish_mode": "public_cite_and_summarize_only",
                "rock_versions": rock_versions,
                "version_scope_status": version_scope_status,
                "safe_evidence_hash": source_input_hash,
                "source_input_hash": source_input_hash,
                "normalized_content_hash": candidate.get("normalized_content_hash"),
                "documentation_path": candidate.get("documentation_path"),
                "documentation_article_id": candidate.get("documentation_article_id"),
                "needs_live_verification": bool(item.get("needs_live_verification", False)),
                "generation_provenance": {
                    "model": model,
                    "prompt_id": prompt_id,
                    "prompt_version": prompt_version,
                    "method": method,
                    "source_input_hash": source_input_hash,
                },
                "review_notes": rewrite.get("review_notes") or [],
            }
            for key in ["evidence_class", "temporal_status"]:
                if item.get(key):
                    review[key] = item[key]
            promoted.append(review)
            promoted_claim_texts.add(normalized_claim)
            claimful_candidates.add(candidate_id)
        promoted_candidates.add(candidate_id)

    existing = [
        row
        for row in read_jsonl(output_path)
        if str(row.get("candidate_id") or "") not in promoted_candidates
    ]
    rows = sorted([*existing, *promoted], key=lambda row: str(row.get("id") or ""))
    public_claims = [source_claim_review_to_claim(row) for row in rows]
    errors = validate_claim_rows(public_claims, public=True, label=str(output_path))
    if errors:
        raise ValueError("\n".join(errors))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_path, rows)
    return {
        "schema": "rock-kb-document-claim-promotion-result-v1",
        "status": "ok",
        "candidate_count": len(candidates),
        "reviewed_candidate_count": len(promoted_candidates),
        "promoted_candidate_count": len(claimful_candidates),
        "promoted_claim_count": len(promoted),
        "review_row_count": len(rows),
        "output": str(output_path),
        "next_command": "uv run kb build --stage claims --force",
    }


def normalize_claim_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def normalized_rock_versions(candidate: dict[str, Any], item: dict[str, Any]) -> list[str]:
    explicit = [str(value).lstrip("v") for value in item.get("rock_versions") or [] if value]
    return sorted(set(explicit))


def normalized_version_scope_status(item: dict[str, Any], rock_versions: list[str]) -> str:
    if rock_versions:
        return "scoped"
    status = str(item.get("version_scope_status") or "unprocessed")
    if status not in {"version_independent", "unprocessed"}:
        raise ValueError(
            "version_scope_status must be version_independent or unprocessed when rock_versions is empty"
        )
    return status
