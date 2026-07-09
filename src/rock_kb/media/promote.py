from ._shared import *  # noqa: F401,F403


def promote_media_public_candidates(
    source: Source,
    candidate_ids: Optional[Iterable[str]] = None,
    review_status: str = "approved_for_public_distillation",
    reviewer: str = "local-review",
    concept_ids: Optional[Iterable[str]] = None,
    promote_all: bool = False,
    rewrites_by_candidate_id: Optional[dict[str, dict[str, Any]]] = None,
    review_provenance: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    if review_status not in PUBLIC_MEDIA_REVIEW_STATUSES:
        raise ValueError(
            "review_status must be one of: " + ", ".join(sorted(PUBLIC_MEDIA_REVIEW_STATUSES))
        )
    candidate_path = media_public_candidates_path(source.id)
    if not candidate_path.exists():
        raise FileNotFoundError(f"No media public candidates found at {candidate_path}")
    requested_ids = {str(value) for value in candidate_ids or [] if value}
    if not requested_ids and not promote_all:
        raise ValueError("Provide at least one candidate_id or set promote_all=True")

    candidates = list(read_jsonl(candidate_path))
    selected = [
        candidate
        for candidate in candidates
        if promote_all or str(candidate.get("id") or "") in requested_ids
    ]
    found_ids = {str(candidate.get("id") or "") for candidate in selected}
    missing_ids = sorted(requested_ids - found_ids)
    if missing_ids:
        raise ValueError("Unknown candidate_id values: " + ", ".join(missing_ids))

    existing_promotions = list(read_jsonl(media_public_promotions_path(source.id)))
    by_candidate_id = {
        str(row.get("candidate_id") or row.get("id") or ""): row
        for row in existing_promotions
        if row.get("candidate_id") or row.get("id")
    }
    reviewed_at = now_iso()
    for candidate in selected:
        candidate_id = str(candidate.get("id") or "")
        rewrite = (rewrites_by_candidate_id or {}).get(candidate_id)
        if rewrite is not None and review_provenance:
            rewrite = {
                **rewrite,
                "generation_provenance": normalize_generation_provenance(
                    {
                        **review_provenance,
                        "source_input_hash": candidate.get("transcript_hash"),
                    }
                ),
            }
        if is_placeholder_media_candidate(candidate) and rewrite is None:
            raise ValueError(
                f"{candidate_id} is a placeholder review candidate; provide --rewrite-file with a public-safe summary and key_insights"
            )
        promotion_candidate = media_public_rewritten_candidate(candidate, rewrite) if rewrite else candidate
        if is_placeholder_media_candidate(promotion_candidate):
            raise ValueError(f"{candidate_id} rewrite still contains placeholder summary or insight text")
        validate_media_public_promotion_candidate(promotion_candidate)
        promotion_concept_ids = sorted(
            {
                str(value)
                for value in list(concept_ids or []) + list(promotion_candidate.get("concept_ids") or [])
                if value
            }
        )
        candidate_reviewed_at = reviewed_at
        existing = by_candidate_id.get(candidate_id)
        if existing and media_promotion_content_unchanged(
            existing,
            promotion_candidate,
            review_status=review_status,
            concept_ids=promotion_concept_ids,
        ):
            candidate_reviewed_at = str(existing.get("reviewed_at") or reviewed_at)
        by_candidate_id[candidate_id] = media_public_promotion_record(
            source=source,
            candidate=promotion_candidate,
            review_status=review_status,
            reviewer=reviewer,
            reviewed_at=candidate_reviewed_at,
            concept_ids=promotion_concept_ids,
        )

    promotion_rows = sorted(by_candidate_id.values(), key=lambda row: str(row.get("candidate_id") or row.get("id") or ""))
    write_jsonl(media_public_promotions_path(source.id), promotion_rows)
    apply_result = apply_media_public_promotions(source)
    return {
        "source_id": source.id,
        "candidate_path": str(candidate_path),
        "promotion_path": str(media_public_promotions_path(source.id)),
        "selected_candidates": len(selected),
        "promotion_rows": len(promotion_rows),
        **apply_result,
    }


def media_promotion_content_unchanged(
    existing: dict[str, Any],
    candidate: dict[str, Any],
    review_status: str,
    concept_ids: Iterable[str],
) -> bool:
    return all(
        [
            existing.get("summary") == candidate.get("summary"),
            (existing.get("key_insights") or []) == (candidate.get("key_insights") or []),
            existing.get("review_status") == review_status,
            sorted(existing.get("concept_ids") or []) == sorted(concept_ids),
        ]
    )


def media_public_promotion_record(
    source: Source,
    candidate: dict[str, Any],
    review_status: str,
    reviewer: str,
    reviewed_at: str,
    concept_ids: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    safe_payload = {
        "candidate_id": candidate.get("id"),
        "media_id": candidate.get("media_id"),
        "source_record_id": candidate.get("source_record_id"),
        "source_url": candidate.get("source_url"),
        "source_title": candidate.get("source_title"),
        "summary": candidate.get("summary"),
        "key_insights": candidate.get("key_insights") or [],
        "topics": candidate.get("topics") or [],
        "transcript_hash": candidate.get("transcript_hash"),
        "review_status": review_status,
        "concept_ids": sorted({str(value) for value in concept_ids or [] if value}),
    }
    return {
        "schema": "rock-kb-media-public-promotion-v1",
        "id": "media-public-promotion:" + sha256_text(json.dumps(safe_payload, sort_keys=True))[:16],
        "candidate_id": candidate.get("id"),
        "media_insight_id": candidate.get("media_insight_id")
        or media_insight_id(source.id, str(candidate.get("media_id") or ""), str(candidate.get("transcript_hash") or "")),
        "source_id": source.id,
        "source_kind": source.kind,
        "source_record_id": candidate.get("source_record_id"),
        "source_url": candidate.get("source_url") or source.root_url,
        "source_title": candidate.get("source_title") or source.name,
        "media_id": candidate.get("media_id"),
        "media_url": candidate.get("media_url"),
        "transcript_hash": candidate.get("transcript_hash"),
        "transcribed_at": candidate.get("transcribed_at"),
        "review_status": review_status,
        "reviewed_at": reviewed_at,
        "reviewer": reviewer,
        "concept_ids": safe_payload["concept_ids"],
        "summary": candidate.get("summary"),
        "key_insights": candidate.get("key_insights") or [],
        "topics": candidate.get("topics") or [],
        "citations": candidate.get("citations") or [{"source_id": source.id, "url": candidate.get("source_url") or source.root_url}],
        "contains_raw_transcript": False,
        "contains_verbatim_transcript": False,
        "derived_from_private_transcript": True,
        "review_rewrite_applied": bool(candidate.get("review_rewrite_applied")),
        "generation_provenance": candidate.get("generation_provenance"),
        "public_publish_mode": "public_cite_and_summarize_only",
        "publishability_status": "approved_public_distillation",
        "content_hash": sha256_text(json.dumps(safe_payload, sort_keys=True)),
    }

def load_media_public_rewrites(path: Path) -> dict[str, dict[str, Any]]:
    rewrites: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(path):
        candidate_id = str(row.get("candidate_id") or row.get("id") or "")
        if not candidate_id:
            raise ValueError(f"Rewrite row in {path} is missing candidate_id")
        rewrites[candidate_id] = normalize_media_public_rewrite(row)
    return rewrites

def normalize_media_public_rewrite(row: dict[str, Any]) -> dict[str, Any]:
    summary = str(row.get("summary") or "").strip()
    if not summary:
        raise ValueError("Media public rewrite rows must include a non-empty summary")
    if summary.startswith(PUBLIC_MEDIA_PLACEHOLDER_SUMMARY_PREFIX):
        raise ValueError("Media public rewrite summary is still a placeholder")
    key_insights = normalize_media_public_key_insights(row.get("key_insights"))
    if not key_insights:
        raise ValueError("Media public rewrite rows must include at least one key_insights item")
    if row.get("contains_raw_transcript") is True or row.get("contains_verbatim_transcript") is True:
        raise ValueError("Media public rewrite rows cannot be marked as containing raw or verbatim transcript text")
    concept_ids = sorted({str(value) for value in row.get("concept_ids") or row.get("approved_concept_ids") or [] if value})
    normalized = {
        "summary": summary,
        "key_insights": key_insights,
        "concept_ids": concept_ids,
    }
    if row.get("generation_provenance"):
        normalized["generation_provenance"] = normalize_generation_provenance(row["generation_provenance"])
    for key in ["source_url", "source_timestamp_url", "source_title", "topics", "citations", "review_notes"]:
        if row.get(key):
            normalized[key] = row.get(key)
    return normalized


def normalize_generation_provenance(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("generation_provenance must be an object")
    required = ["model", "prompt_id", "prompt_version", "method", "source_input_hash"]
    normalized = {key: str(value.get(key) or "").strip() for key in required}
    missing = [key for key, item in normalized.items() if not item]
    if missing:
        raise ValueError("generation_provenance is missing: " + ", ".join(missing))
    if not re.fullmatch(r"[0-9a-f]{64}", normalized["source_input_hash"]):
        raise ValueError("generation_provenance.source_input_hash must be a lowercase SHA-256 hash")
    return normalized


def normalize_media_public_key_insights(value: Any) -> list[dict[str, Any]]:
    insights: list[dict[str, Any]] = []
    for item in value or []:
        if isinstance(item, str):
            insight_text = item.strip()
            normalized = {"insight": insight_text}
        elif isinstance(item, dict):
            normalized = dict(item)
            insight_text = str(normalized.get("insight") or "").strip()
            normalized["insight"] = insight_text
        else:
            continue
        if not insight_text:
            continue
        if insight_text.startswith(PUBLIC_MEDIA_PLACEHOLDER_INSIGHT_PREFIX):
            raise ValueError("Media public rewrite key_insights still contain placeholder review text")
        normalized["contains_verbatim_transcript"] = bool(normalized.get("contains_verbatim_transcript", False))
        insights.append(normalized)
    return insights

def media_public_rewritten_candidate(candidate: dict[str, Any], rewrite: Optional[dict[str, Any]]) -> dict[str, Any]:
    if rewrite is None:
        return candidate
    rewritten = dict(candidate)
    rewritten.update(
        {
            "summary": rewrite["summary"],
            "key_insights": rewrite["key_insights"],
            "review_rewrite_applied": True,
        }
    )
    for key in [
        "source_url",
        "source_timestamp_url",
        "source_title",
        "topics",
        "citations",
        "concept_ids",
        "review_notes",
        "generation_provenance",
    ]:
        if rewrite.get(key):
            rewritten[key] = rewrite[key]
    rewritten["contains_raw_transcript"] = False
    rewritten["contains_verbatim_transcript"] = False
    return rewritten

def validate_media_public_promotion_candidate(candidate: dict[str, Any]) -> None:
    source_url = str(candidate.get("source_url") or "").strip()
    if not source_url.startswith("http"):
        raise ValueError(f"{candidate.get('id') or 'media candidate'} lacks canonical source_url traceability")
    if is_disallowed_public_media_url(source_url):
        raise ValueError(f"{candidate.get('id') or 'media candidate'} source_url is a direct, streaming, player, or tokenized media URL")
    provenance = candidate.get("generation_provenance")
    if provenance:
        normalized_provenance = normalize_generation_provenance(provenance)
        transcript_hash = str(candidate.get("transcript_hash") or "").strip()
        if transcript_hash and normalized_provenance["source_input_hash"] != transcript_hash:
            raise ValueError(
                f"{candidate.get('id') or 'media candidate'} generation_provenance.source_input_hash does not match transcript_hash"
            )
    if looks_like_raw_transcript_text(str(candidate.get("summary") or "")):
        raise ValueError(f"{candidate.get('id') or 'media candidate'} summary looks like raw transcript text")
    for url in urls_in_value(candidate.get("summary")):
        if is_disallowed_public_media_url(url):
            raise ValueError(f"{candidate.get('id') or 'media candidate'} summary includes a direct, streaming, player, or tokenized media URL")
    for citation in candidate.get("citations") or []:
        if not isinstance(citation, dict):
            continue
        url = str(citation.get("url") or "").strip()
        if url and is_disallowed_public_media_url(url):
            raise ValueError(f"{candidate.get('id') or 'media candidate'} citation includes a direct, streaming, player, or tokenized media URL")
    for item in candidate.get("key_insights") or []:
        if not isinstance(item, dict):
            text = str(item or "")
            if looks_like_raw_transcript_text(text):
                raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights look like raw transcript text")
            continue
        insight = str(item.get("insight") or "")
        if looks_like_raw_transcript_text(insight):
            raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights look like raw transcript text")
        if item.get("contains_raw_transcript") is True or item.get("contains_verbatim_transcript") is True:
            raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights cannot contain raw or verbatim transcript text")
        insight_source = str(item.get("source_url") or source_url or "").strip()
        if not insight_source.startswith("http"):
            raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights lack source_url traceability")
        for key in ["source_url", "source_timestamp_url"]:
            url = str(item.get(key) or "").strip()
            if url and is_disallowed_public_media_url(url):
                raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights include a direct, streaming, player, or tokenized media URL")
        for url in urls_in_value(insight):
            if is_disallowed_public_media_url(url):
                raise ValueError(f"{candidate.get('id') or 'media candidate'} key_insights include a direct, streaming, player, or tokenized media URL")

def urls_in_value(value: Any) -> list[str]:
    if value in (None, "", [], {}):
        return []
    if isinstance(value, str):
        return URL_RE.findall(value)
    if isinstance(value, dict):
        return [url for item in value.values() for url in urls_in_value(item)]
    if isinstance(value, list):
        return [url for item in value for url in urls_in_value(item)]
    return []

def is_disallowed_public_media_url(url: str) -> bool:
    parsed = urlparse(str(url or ""))
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()
    if not parsed.scheme.startswith("http"):
        return False
    if host in DISALLOWED_PUBLIC_MEDIA_HOSTS or host.endswith(".wistia.net"):
        return True
    if "/external/" in path or any(path.endswith(ext) for ext in sorted(AUDIO_EXTENSIONS | VIDEO_EXTENSIONS | STREAMING_EXTENSIONS)):
        return True
    if any(ext in query for ext in STREAMING_EXTENSIONS):
        return True
    query_pairs = [(key.lower(), value.lower()) for key, value in parse_qsl(parsed.query, keep_blank_values=True)]
    if any(
        key in TOKENIZED_QUERY_HINTS
        or key.endswith("_token")
        or key.endswith("_signature")
        or any(hint in value for hint in ["oauth", "token", "signature", ".m3u8", ".mpd"])
        for key, value in query_pairs
    ):
        return True
    return False

def looks_like_raw_transcript_text(text: str) -> bool:
    value = str(text or "")
    if re.search(r"(?im)^\s*(speaker|host|interviewer|participant|guest)\s*\d*\s*:", value):
        return True
    if re.search(r"\[\s?\d{1,2}:\d{2}(?::\d{2})?\s?\]", value):
        return True
    if re.search(r"\b\d{1,2}:\d{2}(?::\d{2})?\s*[-–]\s*\d{1,2}:\d{2}(?::\d{2})?\b", value):
        return True
    if value.lower().startswith("transcript:"):
        return True
    return False

def is_placeholder_media_candidate(candidate: dict[str, Any]) -> bool:
    summary = str(candidate.get("summary") or "")
    if summary.startswith(PUBLIC_MEDIA_PLACEHOLDER_SUMMARY_PREFIX):
        return True
    for item in candidate.get("key_insights") or []:
        if isinstance(item, dict):
            insight = str(item.get("insight") or "")
        else:
            insight = str(item or "")
        if insight.startswith(PUBLIC_MEDIA_PLACEHOLDER_INSIGHT_PREFIX):
            return True
    return False

def apply_media_public_promotions(source: Source) -> dict[str, Any]:
    promotions = [
        row
        for row in read_jsonl(media_public_promotions_path(source.id))
        if row.get("review_status") in PUBLIC_MEDIA_REVIEW_STATUSES
    ]
    promotion_by_insight_id = {
        str(row.get("media_insight_id") or ""): row
        for row in promotions
        if row.get("media_insight_id")
    }
    promotion_by_media_hash = {
        (str(row.get("media_id") or ""), str(row.get("transcript_hash") or "")): row
        for row in promotions
        if row.get("media_id") and row.get("transcript_hash")
    }
    path = media_insights_path(source.id)
    rows = list(read_jsonl(path))
    updated_rows = []
    updated = 0
    for row in rows:
        insight_id = str(row.get("id") or "")
        media_hash = (str(row.get("media_id") or ""), str(row.get("transcript_hash") or ""))
        promotion = promotion_by_insight_id.get(insight_id) or promotion_by_media_hash.get(media_hash)
        if promotion:
            row = dict(row)
            row["needs_review"] = False
            row["review_status"] = promotion.get("review_status")
            row["reviewed_at"] = promotion.get("reviewed_at")
            row["reviewer"] = promotion.get("reviewer")
            if promotion.get("generation_provenance"):
                row["generation_provenance"] = promotion.get("generation_provenance")
            row["review_origin"] = "media_public_promotion"
            row["public_promotion_id"] = promotion.get("id")
            row["public_promotion_candidate_id"] = promotion.get("candidate_id")
            row["summary"] = promotion.get("summary") or row.get("summary")
            row["excerpt"] = str(row.get("summary") or "")[:600]
            row["key_insights"] = promotion.get("key_insights") or []
            row["content_hash"] = promotion.get("content_hash") or row.get("content_hash")
            row["public_publish_mode"] = "public_cite_and_summarize_only"
            row["publishability_status"] = "approved_public_distillation"
            if promotion.get("topics"):
                row["topics"] = promotion.get("topics")
            if promotion.get("citations"):
                row["citations"] = promotion.get("citations")
            if promotion.get("concept_ids"):
                row["approved_concept_ids"] = promotion.get("concept_ids")
            updated += 1
        updated_rows.append(row)
    if updated:
        write_jsonl(path, updated_rows)
    return {
        "insight_path": str(path),
        "approved_promotion_rows": len(promotions),
        "updated_insight_rows": updated,
    }
