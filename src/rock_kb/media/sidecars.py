from ._shared import *  # noqa: F401,F403
from .identity import annotate_media_mirrors, infer_source_work_id


def sync_media_manifest_transcript_status(source_id: str, transcript_rows: Iterable[dict[str, Any]]) -> int:
    path = media_manifest_path(source_id)
    rows = list(read_jsonl(path))
    if not rows:
        return 0
    by_media_id = {
        str(row.get("media_id") or ""): row
        for row in transcript_rows
        if row.get("media_id") and row.get("transcript_status") in SYNCABLE_TRANSCRIPT_STATUSES
    }
    updated = 0
    output = []
    for row in rows:
        media_id = str(row.get("id") or "")
        transcript = by_media_id.get(media_id)
        if transcript:
            row = dict(row)
            row["transcript_status"] = transcript.get("transcript_status")
            row["transcript_path"] = transcript.get("transcript_path")
            row["transcription_tool"] = transcript.get("transcription_tool")
            row["transcription_model"] = transcript.get("transcription_model")
            row["transcribed_at"] = transcript.get("transcribed_at")
            updated += 1
        output.append(row)
    if updated:
        write_jsonl(path, output)
    return updated

def build_media_sidecars(source: Source) -> dict[str, Any]:
    transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
    sync_media_manifest_transcript_status(source.id, transcript_rows)
    media_rows = list(read_jsonl(media_manifest_path(source.id)))
    transcripts_by_media_id = {
        str(row.get("media_id") or ""): row
        for row in transcript_rows
        if row.get("media_id") and row.get("transcript_status") in SYNCABLE_TRANSCRIPT_STATUSES
    }
    index_rows: list[dict[str, Any]] = []
    for media_row in media_rows:
        media_id = str(media_row.get("id") or "")
        if not media_id or not media_row.get("media_url"):
            continue
        transcript_row = transcripts_by_media_id.get(media_id)
        sidecar = media_sidecar_path(source.id, media_id)
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        transcript = str(transcript_row.get("transcript") or "") if transcript_row else ""
        index_row = media_sidecar_index_row(source, media_row, transcript_row, sidecar, transcript)
        sidecar.write_text(media_sidecar_markdown(source, media_row, transcript_row, index_row, transcript), encoding="utf-8")
        index_rows.append(index_row)
    write_jsonl(media_source_index_path(source.id), index_rows)
    refresh_global_media_index()
    return {
        "source_id": source.id,
        "sidecars": len(index_rows),
        "source_index_path": str(media_source_index_path(source.id)),
        "global_index_path": str(media_global_index_path()),
        "sidecar_dir": str(media_sidecar_dir(source.id)),
    }

def media_sidecar_index_row(
    source: Source,
    media_row: dict[str, Any],
    transcript_row: Optional[dict[str, Any]],
    sidecar: Path,
    transcript: str,
) -> dict[str, Any]:
    media_id = str(media_row.get("id") or "")
    status = str((transcript_row or {}).get("transcript_status") or media_row.get("transcript_status") or "pending")
    transcript_hash = sha256_text(transcript) if transcript else None
    source_work_id = infer_source_work_id(
        source_id=source.id,
        source_title=str(media_row.get("source_title") or source.name),
        source_record_id=str(media_row.get("source_record_id") or ""),
        source_url=str(media_row.get("source_url") or source.root_url),
        media_url=str(media_row.get("media_url") or ""),
        episode_number=media_row.get("episode_number"),
        existing=str(media_row.get("source_work_id") or "") or None,
    )
    return {
        "schema": "rock-kb-media-index-v1",
        "id": f"{media_id}:sidecar",
        "media_id": media_id,
        "source_work_id": source_work_id,
        "source_id": source.id,
        "source_kind": source.kind,
        "source_record_id": media_row.get("source_record_id"),
        "source_url": media_row.get("source_url") or source.root_url,
        "source_title": media_row.get("source_title") or source.name,
        "media_url": media_row.get("media_url"),
        "media_kind": media_row.get("media_kind"),
        "duration": media_row.get("duration"),
        "sidecar_path": str(sidecar),
        "transcript_status": status,
        "transcription_tool": (transcript_row or {}).get("transcription_tool"),
        "transcription_model": (transcript_row or {}).get("transcription_model"),
        "transcribed_at": (transcript_row or {}).get("transcribed_at"),
        "transcript_hash": transcript_hash,
        "transcript_chars": len(transcript),
        "transcript_segment_count": len((transcript_row or {}).get("transcript_segments") or []),
        "timestamped_transcript_available": bool((transcript_row or {}).get("transcript_segments")),
        "has_private_transcript": bool(transcript),
        "topics": sorted(set((source.topics or []) + ["media", "transcript"])),
        "citations": media_row.get("citations") or [{"source_id": source.id, "url": media_row.get("source_url") or source.root_url}],
        "content_hash": sha256_text(json.dumps(public_media_index_hash_payload(media_row, transcript_hash), sort_keys=True)),
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_media_sidecar_only",
    }

def public_media_index_hash_payload(media_row: dict[str, Any], transcript_hash: Optional[str]) -> dict[str, Any]:
    return {
        "source_work_id": infer_source_work_id(
            source_id=str(media_row.get("source_id") or "unknown"),
            source_title=str(media_row.get("source_title") or ""),
            source_record_id=str(media_row.get("source_record_id") or ""),
            source_url=str(media_row.get("source_url") or ""),
            media_url=str(media_row.get("media_url") or ""),
            episode_number=media_row.get("episode_number"),
            existing=str(media_row.get("source_work_id") or "") or None,
        ),
        "source_record_id": media_row.get("source_record_id"),
        "source_url": media_row.get("source_url"),
        "media_url": media_row.get("media_url"),
        "transcript_hash": transcript_hash,
    }

def media_sidecar_markdown(
    source: Source,
    media_row: dict[str, Any],
    transcript_row: Optional[dict[str, Any]],
    index_row: dict[str, Any],
    transcript: str,
) -> str:
    title = str(media_row.get("source_title") or source.name)
    frontmatter = {
        "schema": "rock-kb-media-sidecar-v1",
        "media_id": index_row["media_id"],
        "source_work_id": index_row["source_work_id"],
        "source_id": source.id,
        "source_record_id": media_row.get("source_record_id"),
        "source_url": media_row.get("source_url") or source.root_url,
        "media_url": media_row.get("media_url"),
        "media_kind": media_row.get("media_kind"),
        "transcript_status": index_row["transcript_status"],
        "transcription_tool": index_row.get("transcription_tool"),
        "transcription_model": index_row.get("transcription_model"),
        "transcript_hash": index_row.get("transcript_hash"),
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_media_sidecar_only",
    }
    lines = ["---", *frontmatter_lines(frontmatter), "---", "", f"# {title}", ""]
    lines.extend(
        [
            "## Agent Use",
            "",
            "This is a private media sidecar for local synthesis. Do not publish raw transcripts, downloaded media paths, or generated visual notes from this file. Public artifacts may use distilled claims, source URLs, timestamps, and hashes after review.",
            "",
            "## Source",
            "",
            f"- Source: {media_row.get('source_url') or source.root_url}",
            f"- Media: {media_row.get('media_url')}",
            f"- Kind: {media_row.get('media_kind') or 'unknown'}",
            f"- Source record: {media_row.get('source_record_id') or ''}",
            "",
            "## Transcription",
            "",
            f"- Status: {index_row['transcript_status']}",
            f"- Tool: {index_row.get('transcription_tool') or ''}",
            f"- Model: {index_row.get('transcription_model') or ''}",
            f"- Transcript hash: {index_row.get('transcript_hash') or ''}",
            f"- Transcript payload: {(transcript_row or {}).get('transcript_path') or ''}",
            f"- Raw timestamp payload: {(transcript_row or {}).get('raw_transcript_payload_path') or ''}",
            f"- Timed segments: {index_row.get('transcript_segment_count') or 0}",
            "",
            "## Timed Transcript Segments (Private)",
            "",
        ]
    )
    segments = (transcript_row or {}).get("transcript_segments") or []
    if segments:
        for segment in segments:
            label = format_timestamp(segment.get("start"))
            text = str(segment.get("text") or "").strip()
            if text:
                lines.append(f"- [{label}] {text}")
    else:
        lines.append("No timed transcript segments have been captured yet.")
    lines.extend(
        [
            "",
            "## Transcript (Private)",
            "",
        ]
    )
    lines.append(transcript if transcript else "No transcript has been captured yet.")
    lines.append("")
    return "\n".join(lines)

def frontmatter_lines(values: dict[str, Any]) -> list[str]:
    lines = []
    for key, value in values.items():
        if value is None:
            rendered = "null"
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = json.dumps(value, ensure_ascii=False)
        lines.append(f"{key}: {rendered}")
    return lines

def refresh_global_media_index() -> int:
    index_dir = MEDIA_DIR / "index"
    rows: list[dict[str, Any]] = []
    for path in sorted(index_dir.glob("*.media-index.jsonl")):
        if path.name == "media-index.jsonl":
            continue
        rows.extend(read_jsonl(path))
    return write_jsonl(media_global_index_path(), annotate_media_mirrors(rows))
