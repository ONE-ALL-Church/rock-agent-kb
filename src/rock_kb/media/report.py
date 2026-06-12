from ._shared import *  # noqa: F401,F403


def media_status_report(source: Source) -> dict[str, Any]:
    media_rows = list(read_jsonl(media_manifest_path(source.id)))
    transcript_rows = list(read_jsonl(transcript_index_path(source.id)))
    insight_rows = list(read_jsonl(media_insights_path(source.id)))
    source_index_rows = list(read_jsonl(media_source_index_path(source.id)))
    pending = [row for row in media_rows if row.get("transcript_status") == "pending" and row.get("media_url")]
    transcribed = [row for row in transcript_rows if row.get("transcript_status") == "transcribed"]
    return {
        "source_id": source.id,
        "media_manifest_path": str(media_manifest_path(source.id)),
        "transcript_index_path": str(transcript_index_path(source.id)),
        "media_insights_path": str(media_insights_path(source.id)),
        "media_source_index_path": str(media_source_index_path(source.id)),
        "media_sidecar_dir": str(media_sidecar_dir(source.id)),
        "media_rows": len(media_rows),
        "media_statuses": count_values(row.get("transcript_status") for row in media_rows),
        "media_kinds": count_values(row.get("media_kind") for row in media_rows),
        "pending_transcription": len(pending),
        "transcript_rows": len(transcript_rows),
        "transcript_statuses": count_values(row.get("transcript_status") for row in transcript_rows),
        "transcription_tools": count_values(row.get("transcription_tool") for row in transcript_rows),
        "transcribed_rows": len(transcribed),
        "insight_rows": len(insight_rows),
        "sidecar_rows": len(source_index_rows),
        "sidecar_statuses": count_values(row.get("transcript_status") for row in source_index_rows),
        "private_storage": True,
        "public_publish_mode": "private_only_for_raw_transcripts",
        "ready_for_private_normalize": bool(transcribed),
    }

def prune_dry_run_transcript_rows(source: Source) -> dict[str, Any]:
    path = transcript_index_path(source.id)
    rows = list(read_jsonl(path))
    kept = [row for row in rows if row.get("transcript_status") != "dry_run"]
    removed = len(rows) - len(kept)
    if removed:
        write_jsonl(path, kept)
    return {
        "source_id": source.id,
        "path": str(path),
        "before": len(rows),
        "after": len(kept),
        "removed_dry_run_rows": removed,
    }
