from ._shared import *  # noqa: F401,F403


def media_review_status_report(sources: Optional[Iterable[Source]] = None) -> dict[str, Any]:
    if sources is None:
        from ..sources import load_sources

        sources = media_review_sources(load_sources())
    from ..concepts import load_concepts

    concepts = load_concepts()
    source_rows = []
    concept_rows = []
    for source in sources:
        transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
        candidate_rows = list(read_jsonl(media_public_candidates_path(source.id)))
        promotion_rows = list(read_jsonl(media_public_promotions_path(source.id)))
        transcribed_rows = [row for row in transcript_rows if row.get("transcript_status") == "transcribed"]
        approved_rows = [row for row in promotion_rows if row.get("review_status") in PUBLIC_MEDIA_REVIEW_STATUSES]
        approved_candidate_ids = {str(row.get("candidate_id") or "") for row in approved_rows if row.get("candidate_id")}
        candidate_ids = {str(row.get("id") or "") for row in candidate_rows if row.get("id")}
        rejected_rows = [
            row
            for row in promotion_rows
            if row.get("review_status") and row.get("review_status") not in PUBLIC_MEDIA_REVIEW_STATUSES
        ]
        pending_rows = [row for row in candidate_rows if str(row.get("id") or "") not in approved_candidate_ids]
        source_concepts = sorted(
            {
                concept_id
                for row in [*candidate_rows, *promotion_rows]
                for concept_id in media_review_record_concept_ids(row, concepts)
            }
        )
        source_rows.append(
            {
                "source_id": source.id,
                "source_kind": source.kind,
                "transcribed_count": len(transcribed_rows),
                "candidate_count": len(candidate_rows),
                "approved_promotion_count": len(approved_rows),
                "pending_candidate_count": len(pending_rows),
                "rejected_promotion_count": len(rejected_rows),
                "affected_concept_ids": source_concepts,
                "candidate_path": str(media_public_candidates_path(source.id)),
                "promotion_path": str(media_public_promotions_path(source.id)),
                "transcript_index_path": str(transcript_index_path(source.id)),
            }
        )
        for concept in concepts:
            candidates_for_concept = [row for row in candidate_rows if concept.id in media_review_record_concept_ids(row, concepts)]
            approvals_for_concept = [row for row in approved_rows if concept.id in media_review_record_concept_ids(row, concepts)]
            rejected_for_concept = [row for row in rejected_rows if concept.id in media_review_record_concept_ids(row, concepts)]
            if not candidates_for_concept and not approvals_for_concept and not rejected_for_concept:
                continue
            approved_for_concept_ids = {str(row.get("candidate_id") or "") for row in approvals_for_concept if row.get("candidate_id")}
            pending_for_concept = [
                row
                for row in candidates_for_concept
                if str(row.get("id") or "") not in approved_for_concept_ids
            ]
            concept_rows.append(
                {
                    "source_id": source.id,
                    "concept_id": concept.id,
                    "transcribed_count": len(candidates_for_concept),
                    "candidate_count": len(candidates_for_concept),
                    "approved_promotion_count": len(approvals_for_concept),
                    "pending_candidate_count": len(pending_for_concept),
                    "rejected_promotion_count": len(rejected_for_concept),
                    "candidate_id_sample": sorted(str(row.get("id") or "") for row in candidates_for_concept if row.get("id"))[:12],
                    "approved_candidate_ids": sorted(approved_for_concept_ids),
                }
            )
        unknown_approved = sorted(approved_candidate_ids - candidate_ids)
        if unknown_approved:
            source_rows[-1]["approved_without_current_candidate_ids"] = unknown_approved
    return {
        "schema": "rock-kb-media-review-status-v1",
        "source_count": len(source_rows),
        "sources": source_rows,
        "concepts": sorted(concept_rows, key=lambda row: (row["source_id"], row["concept_id"])),
        "summary": {
            "transcribed_count": sum(row["transcribed_count"] for row in source_rows),
            "candidate_count": sum(row["candidate_count"] for row in source_rows),
            "approved_promotion_count": sum(row["approved_promotion_count"] for row in source_rows),
            "pending_candidate_count": sum(row["pending_candidate_count"] for row in source_rows),
            "rejected_promotion_count": sum(row["rejected_promotion_count"] for row in source_rows),
        },
    }

def media_review_sources(sources: Iterable[Source]) -> list[Source]:
    return [
        source
        for source in sources
        if source.kind == "podcast_rss"
        or "media_discovery" in source.preferred_tooling
        or "local_transcription" in source.preferred_tooling
        or transcript_index_path(source.id).exists()
    ]

def media_review_record_concept_ids(row: dict[str, Any], concepts: Iterable[Any]) -> list[str]:
    explicit = sorted({str(value) for value in row.get("concept_ids") or row.get("approved_concept_ids") or [] if value})
    if explicit:
        return explicit
    haystack_values = [
        row.get("source_title"),
        row.get("source_url"),
        " ".join(str(value) for value in row.get("topics") or []),
    ]
    for item in row.get("key_insights") or []:
        if isinstance(item, dict):
            haystack_values.append(item.get("topic"))
    haystack = " ".join(str(value or "").lower() for value in haystack_values)
    matched = []
    for concept in concepts:
        tokens = {concept.id, *getattr(concept, "keywords", []), *getattr(concept, "depends_on_topics", [])}
        if any(media_review_token_matches(str(token or "").lower(), haystack) for token in tokens if token):
            matched.append(concept.id)
    return sorted(set(matched))

def media_review_token_matches(token: str, haystack: str) -> bool:
    if not token:
        return False
    normalized = token.replace("-", " ").strip()
    if len(normalized) < 3:
        return False
    if " " in normalized:
        return normalized in haystack.replace("-", " ")
    return re.search(rf"(?<![a-z0-9]){re.escape(normalized)}(?![a-z0-9])", haystack) is not None

def build_media_insights(source: Source, min_transcript_chars: int = 80) -> list[dict[str, Any]]:
    transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
    records = media_insight_records(source, transcript_rows, min_transcript_chars=min_transcript_chars)
    write_jsonl(media_insights_path(source.id), records)
    if media_public_promotions_path(source.id).exists():
        apply_media_public_promotions(source)
        return list(read_jsonl(media_insights_path(source.id)))
    return records

def build_media_public_candidates(source: Source, min_transcript_chars: int = 80) -> list[dict[str, Any]]:
    transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
    records = media_public_candidate_records(source, transcript_rows, min_transcript_chars=min_transcript_chars)
    write_jsonl(media_public_candidates_path(source.id), records)
    return records

def build_media_public_rewrite_drafts(
    source: Source,
    candidate_ids: Optional[Iterable[str]] = None,
    pending_only: bool = True,
    max_insights: int = 3,
) -> dict[str, Any]:
    candidate_path = media_public_candidates_path(source.id)
    if not candidate_path.exists():
        raise FileNotFoundError(f"No media public candidates found at {candidate_path}")
    requested_ids = {str(value) for value in candidate_ids or [] if value}
    candidates = list(read_jsonl(candidate_path))
    if requested_ids:
        candidates = [row for row in candidates if str(row.get("id") or "") in requested_ids]
    found_ids = {str(row.get("id") or "") for row in candidates if row.get("id")}
    missing_ids = sorted(requested_ids - found_ids)
    if missing_ids:
        raise ValueError("Unknown candidate_id values: " + ", ".join(missing_ids))

    approved_candidate_ids = {
        str(row.get("candidate_id") or "")
        for row in read_jsonl(media_public_promotions_path(source.id))
        if row.get("review_status") in PUBLIC_MEDIA_REVIEW_STATUSES and row.get("candidate_id")
    }
    if pending_only:
        candidates = [row for row in candidates if str(row.get("id") or "") not in approved_candidate_ids]

    transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
    transcripts_by_key = {
        (str(row.get("media_id") or ""), sha256_text(str(row.get("transcript") or "").strip())): row
        for row in transcript_rows
        if row.get("transcript_status") == "transcribed" and row.get("transcript")
    }
    rewrites = []
    skipped = []
    for candidate in candidates:
        key = (str(candidate.get("media_id") or ""), str(candidate.get("transcript_hash") or ""))
        transcript_row = transcripts_by_key.get(key)
        if not transcript_row:
            skipped.append({"candidate_id": candidate.get("id"), "reason": "matching_transcript_not_found"})
            continue
        rewrite = media_public_rewrite_draft_from_transcript(source, candidate, transcript_row, max_insights=max_insights)
        validate_media_public_promotion_candidate(media_public_rewritten_candidate(candidate, rewrite))
        rewrites.append(rewrite)

    output_path = media_public_rewrite_drafts_path(source.id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_path, rewrites)
    return {
        "source_id": source.id,
        "candidate_path": str(candidate_path),
        "rewrite_path": str(output_path),
        "requested_candidates": len(requested_ids) if requested_ids else None,
        "pending_only": pending_only,
        "rewrite_rows": len(rewrites),
        "skipped_rows": len(skipped),
        "skipped": skipped[:50],
    }

def media_public_rewrite_draft_from_transcript(
    source: Source,
    candidate: dict[str, Any],
    transcript_row: dict[str, Any],
    max_insights: int = 3,
) -> dict[str, Any]:
    transcript = str(transcript_row.get("transcript") or "").strip()
    title = clean_media_title(str(candidate.get("source_title") or transcript_row.get("source_title") or source.name))
    source_url = str(candidate.get("source_url") or transcript_row.get("source_url") or source.root_url)
    signals = transcript_signal_counts(transcript)
    selected_signals = signals[:max_insights] or [("source context", 1)]
    topics = [label for label, _ in selected_signals]
    concepts = media_rewrite_concept_ids(candidate, transcript_row, topics)
    summary = media_public_rewrite_summary(source, title, topics)
    key_insights = []
    candidate_insights = [item for item in candidate.get("key_insights") or [] if isinstance(item, dict)]
    candidate_by_topic = {str(item.get("topic") or ""): item for item in candidate_insights}
    for index, (topic, count) in enumerate(selected_signals):
        seed = candidate_by_topic.get(topic) or {}
        timestamp_seconds = seed.get("timestamp_seconds")
        if timestamp_seconds in (None, ""):
            timestamp_seconds = first_signal_timestamp(transcript_row.get("transcript_segments") or [], TRANSCRIPT_SIGNAL_PATTERNS.get(topic, []))
        insight = {
            "topic": topic,
            "insight": media_public_rewrite_claim(source, title, topic, count, index),
            "source_url": source_url,
            "source_timestamp_url": seed.get("source_timestamp_url") or timestamp_source_url(source_url, timestamp_seconds),
            "contains_verbatim_transcript": False,
        }
        if timestamp_seconds not in (None, ""):
            insight["timestamp_seconds"] = timestamp_seconds
            insight["timestamp"] = seed.get("timestamp") or format_timestamp(float(timestamp_seconds))
        elif seed.get("timestamp"):
            insight["timestamp"] = seed.get("timestamp")
        key_insights.append(insight)
    return {
        "candidate_id": candidate.get("id"),
        "source_url": source_url,
        "source_title": title,
        "summary": summary,
        "key_insights": key_insights,
        "concept_ids": concepts,
        "citations": candidate.get("citations")
        or transcript_row.get("citations")
        or [{"source_id": source.id, "url": source_url}],
        "review_notes": [
            "Transcript-backed reviewer rewrite generated from private transcript signals.",
            "No transcript excerpts, direct media URLs, HLS manifests, or tokenized player URLs are included.",
            "Treat implementation details as source-routed guidance that still needs official docs, release notes, source code, or live-instance verification before action.",
        ],
    }

def clean_media_title(title: str) -> str:
    value = re.sub(r"\s*\|\s*Ep\s*\d+\s*$", "", title or "", flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip()
    return value or "this media item"

def media_public_rewrite_summary(source: Source, title: str, topics: list[str]) -> str:
    topic_text = ", ".join(public_topic_phrase(topic) for topic in topics[:3]) or "Rock operations"
    if source.kind == "podcast_rss":
        return (
            f"{title} is approved as a public-safe Rock Cast episode distillation for {topic_text}. "
            "Use it as operational perspective and route implementation work back through official documentation, release notes, source code, or live-instance verification."
        )
    summary = (
        f"{title} is approved as a public-safe RockU training distillation for {topic_text}. "
        "Use it as cited training context, while verifying implementation details against the current Rock version and local configuration."
    )
    if "legacy" in title.lower():
        summary += " Because this training is labeled legacy, confirm whether a newer Rock surface has replaced it before recommending implementation steps."
    return summary

def media_public_rewrite_claim(source: Source, title: str, topic: str, signal_count: int, index: int) -> str:
    phrase = public_topic_phrase(topic)
    if source.kind == "podcast_rss":
        episode_label = title if title.lower().startswith(("the ", "what", "how", "why", "when", "where", "who")) else f"the {title}"
        if index == 0:
            return (
                f"{episode_label} episode gives public operational perspective on {phrase}; use it to frame questions for staff process review rather than as authoritative configuration guidance."
            )
        return (
            f"When applying {phrase} ideas from {title}, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting."
        )
    if index == 0:
        claim = (
            f"The {title} RockU lesson provides training context for {phrase}; use the canonical lesson page as the citation and verify local configuration before implementation."
        )
    else:
        claim = (
            f"For {phrase}, {title} should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks."
        )
    if "legacy" in title.lower():
        claim += " Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally."
    return claim

def public_topic_phrase(topic: str) -> str:
    mapping = {
        "AI and automation": "AI, automation, and responsible tool use",
        "Rock operations": "Rock operations and administration",
        "data and reporting": "reporting, analytics, and measurement",
        "ministry process": "ministry process design",
        "release and roadmap awareness": "version, roadmap, and release-caveat awareness",
        "risk and governance": "risk, governance, permissions, and policy review",
        "staff training": "staff training and operational readiness",
    }
    return mapping.get(str(topic or ""), str(topic or "source context"))

def media_rewrite_concept_ids(candidate: dict[str, Any], transcript_row: dict[str, Any], topics: list[str]) -> list[str]:
    explicit = sorted({str(value) for value in candidate.get("concept_ids") or candidate.get("approved_concept_ids") or [] if value})
    if explicit:
        return explicit
    text = " ".join(
        str(value or "")
        for value in [
            candidate.get("source_title"),
            transcript_row.get("source_title"),
            candidate.get("source_url"),
            " ".join(candidate.get("topics") or []),
            " ".join(topics or []),
        ]
    ).lower()
    rules = [
        ("check-in", ["check-in", "check in", "attendance", "kiosk", "label"]),
        ("mobile", ["mobile", "app", "phone", "proximity"]),
        ("groups", ["group", "scheduling", "rsvp"]),
        ("workflows", ["workflow", "automation"]),
        ("communications", ["communication", "email", "sms", "saturation"]),
        ("data-views-reports", ["analytics", "report", "data view", "dashboard"]),
        ("giving-finance", ["giving", "finance", "financial", "transaction", "payment", "pledge"]),
        ("event-registration", ["event", "registration"]),
        ("cms-websites", ["cms", "website", "content", "page"]),
        ("lava", ["lava", "template"]),
        ("security-permissions", ["security", "permission", "governance", "risk"]),
        ("api-integrations", ["api", "integration"]),
        ("people-families", ["person", "people", "family"]),
        ("scheduling-locations", ["schedule", "location", "campus", "room"]),
    ]
    ids = [concept_id for concept_id, needles in rules if any(needle in text for needle in needles)]
    if not ids and candidate.get("source_id") == "rock_podcast_rss":
        ids = ["workflows"]
    if not ids:
        ids = ["cms-websites"]
    return sorted(set(ids))

def media_insight_records(
    source: Source,
    transcript_rows: Iterable[dict[str, Any]],
    min_transcript_chars: int = 80,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in transcript_rows:
        transcript = str(row.get("transcript") or "").strip()
        if row.get("transcript_status") != "transcribed" or len(transcript) < min_transcript_chars:
            continue
        source_record_id = str(row.get("source_record_id") or "")
        media_id = str(row.get("media_id") or row.get("id") or "")
        transcript_hash = sha256_text(transcript)
        insight_id = media_insight_id(source.id, media_id, transcript_hash)
        summary = summarize_transcript_insight(transcript)
        records.append(
            {
                "id": insight_id,
                "source_id": source.id,
                "source_url": row.get("source_url") or source.root_url,
                "source_title": f"{row.get('source_title') or source.name} Transcript Insight",
                "source_kind": f"{source.kind}_media_transcript",
                "retrieved_at": row.get("transcribed_at") or now_iso(),
                "updated_at": row.get("transcribed_at"),
                "license_status": source.license_status,
                "allowed_extraction_mode": source.allowed_extraction_mode,
                "content_hash": sha256_text(summary + source_record_id + media_id),
                "extraction_tool": row.get("transcription_tool") or "media_transcript",
                "extraction_mode": "private_transcript_distilled_summary",
                "summary_model": row.get("transcription_model") or "local-extractive-transcript-v1",
                "topics": sorted(set((source.topics or []) + ["media", "transcript"])),
                "rock_version_min": None,
                "rock_version_max": None,
                "rock_versions": [],
                "audience": ["agent", "rock-admin"],
                "summary": summary,
                "excerpt": summary[:600],
                "canonical_path": f"knowledge/media/{source.id}-{media_id.replace(':', '-')}.md",
                "citations": row.get("citations") or [{"source_id": source.id, "url": row.get("source_url") or source.root_url}],
                "source_record_id": source_record_id,
                "media_id": media_id,
                "media_url": row.get("media_url"),
                "transcript_hash": transcript_hash,
                "transcript_status": row.get("transcript_status"),
                "derived_from_private_transcript": True,
                "private_storage": True,
                "public_publish_mode": "public_cite_and_summarize_only",
                "publishability_status": "distilled_summary_only",
                "needs_review": True,
            }
        )
    return records

def media_public_candidate_records(
    source: Source,
    transcript_rows: Iterable[dict[str, Any]],
    min_transcript_chars: int = 80,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in transcript_rows:
        transcript = str(row.get("transcript") or "").strip()
        if row.get("transcript_status") != "transcribed" or len(transcript) < min_transcript_chars:
            continue
        media_id = str(row.get("media_id") or row.get("id") or "")
        transcript_hash = sha256_text(transcript)
        insight_id = media_insight_id(source.id, media_id, transcript_hash)
        records.append(
            {
                "schema": "rock-kb-media-public-summary-candidate-v1",
                "id": "media-public-candidate:" + sha256_text(f"{source.id}:{media_id}:{transcript_hash}")[:16],
                "media_insight_id": insight_id,
                "source_id": source.id,
                "source_kind": source.kind,
                "source_record_id": row.get("source_record_id"),
                "source_url": row.get("source_url") or source.root_url,
                "source_title": row.get("source_title") or source.name,
                "media_id": media_id,
                "media_url": row.get("media_url"),
                "transcript_hash": transcript_hash,
                "transcribed_at": row.get("transcribed_at"),
                "transcription_tool": row.get("transcription_tool"),
                "transcription_model": row.get("transcription_model"),
                "timestamped_transcript_available": bool(row.get("transcript_segments")),
                "transcript_segment_count": len(row.get("transcript_segments") or []),
                "topics": sorted(set((source.topics or []) + ["media", "podcast", "timestamped-insights"])),
                "summary": summarize_transcript_insight(transcript),
                "key_insights": transcript_key_insight_candidates(row),
                "citations": row.get("citations") or [{"source_id": source.id, "url": row.get("source_url") or source.root_url}],
                "private_input": True,
                "contains_raw_transcript": False,
                "contains_verbatim_transcript": False,
                "public_publish_mode": "public_cite_and_summarize_only_after_review",
                "publishability_status": "review_candidate_public_distillation",
                "needs_review": True,
                "review_notes": [
                    "Candidate was generated from a private transcript.",
                    "Before public release, verify timestamps against the source player and rewrite/approve each insight.",
                    "Do not add transcript excerpts to public artifacts unless source license explicitly allows it.",
                ],
            }
        )
    return records

def media_insight_id(source_id: str, media_id: str, transcript_hash: str) -> str:
    return "media-insight:" + sha256_text(f"{source_id}:{media_id}:{transcript_hash}")[:16]

def transcript_key_insight_candidates(row: dict[str, Any], max_items: int = 6) -> list[dict[str, Any]]:
    transcript = str(row.get("transcript") or "")
    signals = transcript_signal_counts(transcript)
    segments = row.get("transcript_segments") or []
    insights = []
    for label, count in signals[:max_items]:
        timestamp_seconds = first_signal_timestamp(segments, TRANSCRIPT_SIGNAL_PATTERNS.get(label, []))
        insights.append(
            {
                "topic": label,
                "signal_count": count,
                "timestamp_seconds": timestamp_seconds,
                "timestamp": format_timestamp(timestamp_seconds) if timestamp_seconds is not None else None,
                "source_url": row.get("source_url"),
                "source_timestamp_url": timestamp_source_url(row.get("source_url"), timestamp_seconds),
                "insight": f"Review this timestamp for a public-safe distilled insight about {label}.",
                "contains_verbatim_transcript": False,
            }
        )
    if insights:
        return insights
    return [
        {
            "topic": "general Rock context",
            "signal_count": 0,
            "timestamp_seconds": None,
            "timestamp": None,
            "source_url": row.get("source_url"),
            "source_timestamp_url": row.get("source_url"),
            "insight": "Review this media item for public-safe distilled Rock context.",
            "contains_verbatim_transcript": False,
        }
    ]

def first_signal_timestamp(segments: Iterable[dict[str, Any]], patterns: Iterable[str]) -> Optional[float]:
    lowered_patterns = [pattern.lower() for pattern in patterns]
    for segment in segments:
        text = str(segment.get("text") or "").lower()
        if any(re.search(rf"\b{re.escape(pattern)}\b", text) for pattern in lowered_patterns):
            return numeric_seconds(segment.get("start"))
    return None

def timestamp_source_url(source_url: Any, seconds: Optional[float]) -> Optional[str]:
    if not source_url:
        return None
    url = str(source_url)
    if seconds is None:
        return url
    parsed = urlparse(url)
    whole_seconds = int(seconds)
    if "youtube.com" in parsed.netloc:
        separator = "&" if parsed.query else "?"
        return f"{url}{separator}t={whole_seconds}s"
    if "youtu.be" in parsed.netloc:
        separator = "&" if parsed.query else "?"
        return f"{url}{separator}t={whole_seconds}"
    return url

def summarize_transcript_insight(text: str, max_chars: int = 900) -> str:
    cleaned = " ".join(text.split())
    signals = transcript_signal_counts(cleaned)
    signal_text = ", ".join(f"{label} ({count})" for label, count in signals[:5]) or "general Rock operations context"
    word_count = count_words(cleaned)
    sentence_count = len(re.findall(r"[.!?](?:\s|$)", cleaned))
    summary = (
        "Private transcript-derived insight: this media item has been transcribed locally and should be used as "
        f"a private synthesis source. Detected themes: {signal_text}. Transcript scale: about {word_count} words"
        f" across {sentence_count or 'unknown'} sentence-like segments. Public guidance may cite the source URL and "
        "use reviewed distilled claims, but should not copy transcript text."
    )
    if len(summary) <= max_chars:
        return summary
    return summary[: max_chars - 3].rsplit(" ", 1)[0] + "..."

def transcript_signal_counts(text: str) -> list[tuple[str, int]]:
    lowered = text.lower()
    counts: Counter[str] = Counter()
    for label, patterns in TRANSCRIPT_SIGNAL_PATTERNS.items():
        for pattern in patterns:
            counts[label] += len(re.findall(rf"\b{re.escape(pattern.lower())}\b", lowered))
    return [(label, count) for label, count in counts.most_common() if count > 0]

def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))
