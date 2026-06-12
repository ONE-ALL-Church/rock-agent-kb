from ._shared import *  # noqa: F401,F403


def pending_media_rows(source_id: str, limit: Optional[int] = None, source: Optional[Source] = None, prioritized: bool = True) -> list[dict[str, Any]]:
    rows = [
        row
        for row in read_jsonl(media_manifest_path(source_id))
        if row.get("media_url") and row.get("transcript_status") in {None, "", "pending", "queued_missing_tool"}
    ]
    if prioritized:
        rows = sorted(rows, key=lambda row: (-media_priority_score(row, source), duration_seconds(row.get("duration")) or 999999, str(row.get("source_title") or "")))
    return rows[: limit or None]

def build_media_priority_queue(sources: Iterable[Source], limit: Optional[int] = None) -> dict[str, Any]:
    queue_rows: list[dict[str, Any]] = []
    for source in sources:
        path = media_manifest_path(source.id)
        if not path.exists():
            continue
        for row in pending_media_rows(source.id, source=source, prioritized=True):
            queue_rows.append(media_priority_queue_row(row, source))
    queue_rows = sorted(queue_rows, key=lambda row: (-int(row["priority_score"]), row.get("duration_seconds") or 999999, row.get("source_title") or ""))
    if limit:
        queue_rows = queue_rows[:limit]
    for index, row in enumerate(queue_rows, start=1):
        row["rank"] = index
    queue_path = media_priority_queue_path()
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(queue_path, queue_rows)
    report = media_priority_report(queue_rows)
    media_priority_report_path().write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "queue_path": str(queue_path),
        "report_path": str(media_priority_report_path()),
        "queued_rows": len(queue_rows),
        "top_sources": report["queued_by_source"],
        "top_reasons": report["reason_counts"],
    }

def media_priority_queue_row(row: dict[str, Any], source: Optional[Source] = None) -> dict[str, Any]:
    duration = duration_seconds(row.get("duration"))
    return {
        "schema": "rock-kb-media-transcription-priority-v1",
        "id": f"{row.get('id')}:priority",
        "media_id": row.get("id"),
        "source_id": row.get("source_id"),
        "source_kind": source.kind if source else None,
        "source_title": row.get("source_title"),
        "source_url": row.get("source_url"),
        "media_url": row.get("media_url"),
        "media_kind": row.get("media_kind"),
        "duration": row.get("duration"),
        "duration_seconds": duration,
        "transcript_status": row.get("transcript_status"),
        "priority_score": media_priority_score(row, source),
        "priority_reasons": media_priority_reasons(row, source),
        "recommended_action": recommended_transcription_action(row, duration),
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_media_queue_only",
        "citations": row.get("citations") or [{"source_id": row.get("source_id"), "url": row.get("source_url")}],
    }

def media_priority_report(queue_rows: list[dict[str, Any]]) -> dict[str, Any]:
    queued_by_source = count_values(row.get("source_id") for row in queue_rows)
    queued_by_kind = count_values(row.get("media_kind") for row in queue_rows)
    reason_counts: Counter[str] = Counter()
    for row in queue_rows:
        for reason in row.get("priority_reasons") or []:
            reason_counts[str(reason)] += 1
    return {
        "schema": "rock-kb-media-transcription-priority-report-v1",
        "generated_at": generated_at_iso(),
        "queue_path": str(media_priority_queue_path()),
        "queued_rows": len(queue_rows),
        "queued_by_source": queued_by_source,
        "queued_by_kind": queued_by_kind,
        "reason_counts": dict(reason_counts.most_common()),
        "top_items": [
            {
                "rank": row.get("rank"),
                "media_id": row.get("media_id"),
                "source_id": row.get("source_id"),
                "source_title": row.get("source_title"),
                "priority_score": row.get("priority_score"),
                "priority_reasons": row.get("priority_reasons"),
                "recommended_action": row.get("recommended_action"),
            }
            for row in queue_rows[:20]
        ],
        "notes": [
            "Queue rows are private routing metadata and may include direct media URLs.",
            "Scores favor authority, operational usefulness, topic relevance, and shorter media for faster coverage.",
            "Run kb media batch --source <source_id> --limit N to process prioritized rows within a source.",
        ],
    }

def media_priority_score(row: dict[str, Any], source: Optional[Source] = None) -> int:
    source_id = str(row.get("source_id") or (source.id if source else ""))
    score = MEDIA_SOURCE_PRIORITY.get(source_id, 50)
    score += MEDIA_KIND_PRIORITY.get(str(row.get("media_kind") or ""), 0)
    reasons = media_priority_reasons(row, source)
    score += 8 * len([reason for reason in reasons if reason.startswith("topic:")])
    duration = duration_seconds(row.get("duration"))
    if duration is not None:
        if duration <= 10 * 60:
            score += 12
        elif duration <= 30 * 60:
            score += 8
        elif duration <= 60 * 60:
            score += 4
    episode = episode_number(row)
    if episode is not None:
        score += min(18, max(0, episode - 196))
    return score

def media_priority_reasons(row: dict[str, Any], source: Optional[Source] = None) -> list[str]:
    reasons = []
    source_id = str(row.get("source_id") or (source.id if source else ""))
    if source_id in MEDIA_SOURCE_PRIORITY:
        reasons.append(f"source:{source_id}")
    media_kind = str(row.get("media_kind") or "")
    if media_kind:
        reasons.append(f"kind:{media_kind}")
    text = " ".join(str(row.get(key) or "") for key in ["source_title", "source_url"]).lower()
    for label, terms in MEDIA_PRIORITY_TERMS.items():
        if any(priority_term_matches(text, term) for term in terms):
            reasons.append(f"topic:{label}")
    duration = duration_seconds(row.get("duration"))
    if duration is not None and duration <= 10 * 60:
        reasons.append("duration:short")
    elif duration is not None and duration <= 30 * 60:
        reasons.append("duration:medium")
    episode = episode_number(row)
    if episode is not None:
        reasons.append("episode:recent" if episode >= 197 else "episode:catalog")
    return sorted(set(reasons))

def recommended_transcription_action(row: dict[str, Any], duration: Optional[int]) -> str:
    if row.get("media_kind") == "video":
        return "download_with_yt_dlp_then_transcribe_locally"
    if duration is not None and duration > 60 * 60:
        return "transcribe_in_small_batch_or_hosted_fallback_if_local_runtime_is_slow"
    return "transcribe_locally_with_mlx_whisper"

def duration_seconds(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        return int(text)
    parts = text.split(":")
    if not all(part.isdigit() for part in parts):
        return None
    total = 0
    for part in parts:
        total = total * 60 + int(part)
    return total

def episode_number(row: dict[str, Any]) -> Optional[int]:
    text = " ".join(str(row.get(key) or "") for key in ["source_title", "source_url"])
    match = re.search(r"(?:episode|ep)[^\d]{0,8}(\d{1,4})\b", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = int(match.group(1))
    if value > 300:
        return None
    return value

def priority_term_matches(text: str, term: str) -> bool:
    escaped = re.escape(term.lower())
    if re.search(r"\s", term):
        return re.search(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", text) is not None
    return re.search(rf"\b{escaped}\b", text) is not None
