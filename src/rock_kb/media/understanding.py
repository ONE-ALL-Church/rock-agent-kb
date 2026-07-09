from ._shared import *  # noqa: F401,F403


def media_understanding_tool_status() -> dict[str, Any]:
    runtimes = {
        "litert_lm": bool(optional_command("litert-lm")),
        "ollama": bool(optional_command("ollama")),
        "mlx_lm_generate": bool(optional_command("mlx_lm.generate")),
        "llama_cli": bool(optional_command("llama-cli") or optional_command("llama.cpp")),
    }
    return {
        "candidate_tool": GEMMA4_BENCHMARK_TOOL,
        "role": "experimental_second_pass_media_understanding",
        "local_runtime_ready": any(runtimes.values()),
        "runtimes": runtimes,
        "baseline_transcription_tool": "mlx_whisper",
        "notes": [
            "Use for benchmarked enrichment only; do not replace the baseline transcript generator without evidence.",
            "Evaluate ASR quality, diarization, visual context, timestamp routing, speed, and memory before promoting it.",
            "Keep raw model outputs and direct media URLs in private review artifacts.",
        ],
    }

def build_media_understanding_benchmark(
    sources: Iterable[Source],
    tool: str = GEMMA4_BENCHMARK_TOOL,
    include_media_url: bool = False,
    write: bool = True,
) -> dict[str, Any]:
    source_by_id = {source.id: source for source in sources}
    selected: list[dict[str, Any]] = []
    selected.extend(
        benchmark_sample_rows(
            source_by_id.get("rock_youtube"),
            role="official_rock_video",
            media_kind="video",
            limit=1,
            pending_first=True,
            include_media_url=include_media_url,
        )
    )
    selected.extend(
        benchmark_sample_rows(
            source_by_id.get("rock_podcast_rss"),
            role="podcast_audio",
            media_kind="audio",
            limit=2,
            pending_first=False,
            include_media_url=include_media_url,
        )
    )
    selected.extend(
        benchmark_sample_rows(
            source_by_id.get("rock_community_hubs"),
            role="community_video",
            media_kind="video",
            limit=1,
            pending_first=True,
            include_media_url=include_media_url,
        )
    )
    selected.extend(
        benchmark_sample_rows(
            source_by_id.get("rock_rocku"),
            role="rock_training_video",
            media_kind="video",
            limit=1,
            pending_first=False,
            include_media_url=include_media_url,
        )
    )
    selected.extend(
        benchmark_sample_rows(
            source_by_id.get("triumph_resources"),
            role="triumph_technical_video",
            media_kind="video",
            limit=1,
            pending_first=False,
            include_media_url=include_media_url,
        )
    )
    selected = dedupe_benchmark_rows(selected)
    for index, row in enumerate(selected, start=1):
        row["sample_rank"] = index
    result = {
        "schema": "rock-kb-media-understanding-benchmark-v1",
        "generated_at": generated_at_iso(),
        "tool_candidate": tool,
        "tool_role": "experimental_second_pass_media_understanding",
        "baseline_transcription_tool": "mlx_whisper",
        "local_runtime_status": media_understanding_tool_status(),
        "selected_item_count": len(selected),
        "selected_items": selected,
        "evaluation_rubric": {
            "asr_accuracy": "Compare against the existing mlx_whisper transcript for omissions, hallucinated terms, Rock-specific names, and punctuation usefulness.",
            "timestamp_routing": "Check whether the output can point reviewers to useful source times without exposing direct media URLs publicly.",
            "speaker_or_host_context": "Note whether speaker or host labels are useful enough to improve public-safe candidate rewrites.",
            "visual_context": "For videos, check whether screenshots, UI actions, slides, or demos are summarized accurately beyond the audio transcript.",
            "chaptering": "Check whether generated chapters map to durable Rock topics and source sections.",
            "speed_memory": "Record wall time, peak memory, model/runtime, and whether the run is practical for small batches on this machine.",
            "public_safety": "Confirm outputs can be distilled into non-verbatim public claims with canonical source page URLs only.",
        },
        "pass_criteria": [
            "Do not replace mlx_whisper unless Gemma is at least comparable on transcript accuracy and clearly better on video understanding.",
            "Use Gemma output only as private enrichment until reviewer-authored public claims are approved.",
            "Do not publish direct media URLs, tokenized player URLs, raw transcripts, or unreviewed model summaries.",
        ],
        "recommended_next_commands": [
            "uv run kb media understand-benchmark --tool gemma4-12b",
            "uv run --extra media kb media batch --source rock_podcast_rss --limit 5 --tool mlx_whisper --model auto --dry-run",
        ],
    }
    if write:
        path = media_understanding_benchmark_path(tool)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["benchmark_path"] = str(path)
    return result

def prepare_media_understanding_benchmark_assets(
    sources: Iterable[Source],
    tool: str = GEMMA4_BENCHMARK_TOOL,
    seconds: int = 30,
    manifest_path: Path = MEDIA_UNDERSTANDING_CLIP_MANIFEST,
) -> dict[str, Any]:
    benchmark = build_media_understanding_benchmark(sources, tool=tool, include_media_url=True, write=False)
    clip_dir = manifest_path.parent / "clips"
    frame_dir = manifest_path.parent / "frames"
    clip_dir.mkdir(parents=True, exist_ok=True)
    frame_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        prepare_media_understanding_benchmark_asset(row, clip_dir=clip_dir, frame_dir=frame_dir, seconds=seconds)
        for row in benchmark["selected_items"]
    ]
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema": "rock-kb-media-understanding-assets-v1",
        "generated_at": generated_at_iso(),
        "tool_candidate": tool,
        "seconds": seconds,
        "manifest_path": str(manifest_path),
        "selected_item_count": len(rows),
        "clip_count": sum(1 for row in rows if row.get("clip_status") == "ok"),
        "frame_count": sum(1 for row in rows if row.get("frame_status") == "ok"),
        "items": rows,
    }

def prepare_media_understanding_benchmark_asset(
    item: dict[str, Any],
    clip_dir: Path,
    frame_dir: Path,
    seconds: int,
) -> dict[str, Any]:
    media_id = str(item.get("media_id") or "")
    source_id = str(item.get("source_id") or "")
    safe_name = safe_media_filename(f"{source_id}-{media_id}")
    media_row = {
        "id": media_id,
        "media_url": item.get("media_url"),
        "source_id": source_id,
        "source_title": item.get("source_title"),
        "media_kind": item.get("media_kind"),
    }
    output = {
        "source_id": source_id,
        "media_id": media_id,
        "source_title": item.get("source_title"),
        "media_kind": item.get("media_kind"),
        "transcript_status": item.get("transcript_status"),
        "clip_path": str(clip_dir / f"{safe_name}.wav"),
        "clip_status": "pending",
        "clip_error": "",
        "frame_path": str(frame_dir / f"{safe_name}.jpg") if item.get("media_kind") == "video" else None,
        "frame_status": "pending" if item.get("media_kind") == "video" else "not_video",
    }
    try:
        media_path = download_media(media_row)
        output["download_path"] = str(media_path)
        Path(output["clip_path"]).parent.mkdir(parents=True, exist_ok=True)
        extract_audio_clip(media_path, Path(output["clip_path"]), seconds=seconds)
        output["clip_status"] = "ok"
    except Exception as exc:
        output["clip_status"] = "error"
        output["clip_error"] = str(exc)[:1000]
    if item.get("media_kind") == "video" and output.get("frame_path"):
        try:
            Path(output["frame_path"]).parent.mkdir(parents=True, exist_ok=True)
            extract_video_frame(str(item.get("media_url") or output.get("download_path")), Path(output["frame_path"]))
            output["frame_status"] = "ok"
        except Exception as exc:
            output["frame_status"] = "error"
            output["frame_error"] = str(exc)[:1000]
    return output

def extract_audio_clip(media_path: Path, output_path: Path, seconds: int) -> None:
    ffmpeg = optional_command("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to prepare Gemma audio benchmark clips")
    if output_path.exists() and output_path.stat().st_size > 0:
        return
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(media_path),
        "-t",
        str(seconds),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_path),
    ]
    result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:1000] or result.stdout[:1000] or "ffmpeg audio extraction failed")

def extract_video_frame(input_value: str, output_path: Path) -> None:
    ffmpeg = optional_command("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to prepare Gemma video frames")
    if output_path.exists() and output_path.stat().st_size > 0:
        return
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        "5",
        "-i",
        input_value,
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]
    result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:1000] or result.stdout[:1000] or "ffmpeg frame extraction failed")

def run_ollama_media_understanding_benchmark(
    model: str = GEMMA4_OLLAMA_MODEL,
    manifest_path: Path = MEDIA_UNDERSTANDING_CLIP_MANIFEST,
    endpoint: str = "http://127.0.0.1:11434/api/chat",
    output_path: Path = MEDIA_UNDERSTANDING_OLLAMA_RESULT,
    include_transcript_excerpt: bool = True,
    timeout: float = 300.0,
) -> dict[str, Any]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Benchmark clip manifest not found: {manifest_path}")
    items = json.loads(manifest_path.read_text(encoding="utf-8"))
    result = {
        "schema": "rock-kb-media-understanding-benchmark-run-v2",
        "started_at": now_iso(),
        "model": model,
        "runtime": "ollama",
        "endpoint": endpoint,
        "input_strategy": {
            "raw_audio": "Prefer compressed MP3 clips as base64 multimodal payloads in the Ollama message images field; fall back to 16 kHz mono WAV if compression fails.",
            "frames": "Send extracted video frames as base64 multimodal payloads in the same field after audio.",
            "transcripts": "Include private transcript excerpts as grounding when available; do not write raw media bytes or base64 to the result.",
        },
        "items": [],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for item in items:
        try:
            row = run_ollama_media_understanding_item(
                item,
                model=model,
                endpoint=endpoint,
                include_transcript_excerpt=include_transcript_excerpt,
                timeout=timeout,
            )
        except Exception as exc:
            row = {
                "source_id": item.get("source_id"),
                "media_id": item.get("media_id"),
                "source_title": item.get("source_title"),
                "status": "error",
                "error": repr(exc),
            }
        result["items"].append(row)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["finished_at"] = now_iso()
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output_path"] = str(output_path)
    return result

def run_ollama_media_understanding_item(
    item: dict[str, Any],
    model: str,
    endpoint: str,
    include_transcript_excerpt: bool,
    timeout: float,
) -> dict[str, Any]:
    payloads = ollama_media_payloads(item)
    transcript, transcript_path, segments = media_transcript_excerpt(item) if include_transcript_excerpt else ("", None, [])
    prompt = ollama_media_understanding_prompt(item, transcript, transcript_path)
    request = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": payloads["base64"],
            }
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0,
            "num_ctx": 8192,
            "num_predict": 700,
        },
    }
    start = time.monotonic()
    response = httpx.post(endpoint, json=request, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    elapsed = time.monotonic() - start
    message = data.get("message") or {}
    return {
        "source_id": item.get("source_id"),
        "media_id": item.get("media_id"),
        "source_title": item.get("source_title"),
        "media_kind": item.get("media_kind"),
        "transcript_status": item.get("transcript_status"),
        "raw_audio_input": payloads["raw_audio_input"],
        "audio_payload_path": payloads["audio_payload_path"],
        "audio_payload_format": payloads["audio_payload_format"],
        "audio_payload_bytes": payloads["audio_payload_bytes"],
        "source_clip_bytes": payloads["source_clip_bytes"],
        "frame_input": payloads["frame_input"],
        "multimodal_payload_count": len(payloads["base64"]),
        "clip_path": item.get("clip_path") if payloads["raw_audio_input"] else None,
        "frame_path": item.get("frame_path") if payloads["frame_input"] else None,
        "transcript_excerpt_path": transcript_path,
        "transcript_excerpt_chars": len(transcript),
        "timestamped_segment_count": len(segments),
        "seconds": round(elapsed, 3),
        "done_reason": data.get("done_reason"),
        "prompt_eval_count": data.get("prompt_eval_count"),
        "eval_count": data.get("eval_count"),
        "total_duration_ns": data.get("total_duration"),
        "response": message.get("content", ""),
    }

def ollama_media_payloads(item: dict[str, Any]) -> dict[str, Any]:
    encoded: list[str] = []
    raw_audio_input = False
    audio_payload_path = None
    audio_payload_format = None
    audio_payload_bytes = 0
    source_clip_bytes = 0
    frame_input = False
    clip_path = item.get("clip_path")
    if item.get("clip_status") == "ok" and clip_path:
        clip = Path(str(clip_path))
        if clip.exists():
            source_clip_bytes = clip.stat().st_size
            payload_path = compressed_ollama_audio_path(clip)
            audio_payload_path = str(payload_path)
            audio_payload_format = payload_path.suffix.lstrip(".").lower()
            audio_payload_bytes = payload_path.stat().st_size
            encoded.append(base64.b64encode(payload_path.read_bytes()).decode("ascii"))
            raw_audio_input = True
    frame_path = item.get("frame_path")
    if item.get("frame_status") == "ok" and frame_path:
        frame = Path(str(frame_path))
        if frame.exists():
            encoded.append(base64.b64encode(frame.read_bytes()).decode("ascii"))
            frame_input = True
    return {
        "base64": encoded,
        "raw_audio_input": raw_audio_input,
        "audio_payload_path": audio_payload_path,
        "audio_payload_format": audio_payload_format,
        "audio_payload_bytes": audio_payload_bytes,
        "source_clip_bytes": source_clip_bytes,
        "frame_input": frame_input,
    }

def compressed_ollama_audio_path(clip: Path) -> Path:
    if clip.suffix.lower() == ".mp3":
        return clip
    ffmpeg = optional_command("ffmpeg")
    if clip.suffix.lower() != ".wav" or not ffmpeg:
        return clip
    output_dir = clip.parent.parent / "compressed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{clip.stem}.mp3"
    if output.exists() and output.stat().st_mtime >= clip.stat().st_mtime and output.stat().st_size > 0:
        return output
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(clip),
        "-codec:a",
        "libmp3lame",
        "-b:a",
        MEDIA_UNDERSTANDING_AUDIO_BITRATE,
        str(output),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return clip
    return output if output.exists() and output.stat().st_size > 0 else clip

def media_transcript_excerpt(item: dict[str, Any], max_chars: int = 2400) -> tuple[str, Optional[str], list[dict[str, Any]]]:
    source_id = str(item.get("source_id") or "")
    media_id = str(item.get("media_id") or "")
    if not source_id or not media_id:
        return "", None, []
    candidates = [
        MEDIA_DIR / "transcripts" / source_id / f"{media_id}.row.json",
        MEDIA_DIR / "transcripts" / source_id / f"{media_id}.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        transcript = data.get("transcript")
        if isinstance(transcript, str) and transcript.strip():
            segments = data.get("transcript_segments")
            return transcript.strip()[:max_chars], str(path), segments if isinstance(segments, list) else []
    return "", None, []

def ollama_media_understanding_prompt(item: dict[str, Any], transcript: str, transcript_path: Optional[str]) -> str:
    return (
        "You are evaluating private Rock RMS media for knowledge-base enrichment. "
        "The request includes raw audio when a prepared clip is available; video items may also include one frame image. "
        "Use the raw audio as primary evidence for what was spoken, and use the transcript excerpt only as a comparison aid. "
        "If the audio conflicts with the transcript, say so.\n\n"
        f"Title: {item.get('source_title')}\n"
        f"Source: {item.get('source_id')}\n"
        f"Media id: {item.get('media_id')}\n"
        f"Media kind: {item.get('media_kind')}\n"
        f"Transcript status: {item.get('transcript_status')}\n"
        f"Transcript excerpt path: {transcript_path or 'none'}\n"
        f"Transcript excerpt:\n{transcript or '[no transcript excerpt available]'}\n\n"
        "Return compact JSON with keys: audio_summary, topics, durable_claims, visual_context, "
        "audio_vs_transcript, recommendation, confidence, caveats. Do not quote long transcript passages."
    )

def benchmark_sample_rows(
    source: Optional[Source],
    role: str,
    media_kind: str,
    limit: int,
    pending_first: bool,
    include_media_url: bool,
) -> list[dict[str, Any]]:
    if source is None or not media_manifest_path(source.id).exists():
        return []
    rows = [
        row
        for row in read_jsonl(media_manifest_path(source.id))
        if row.get("media_url") and row.get("media_kind") == media_kind
    ]
    if pending_first:
        pending = [row for row in rows if row.get("transcript_status") in {None, "", "pending", "queued_missing_tool"}]
        others = [row for row in rows if row not in pending]
        rows = [*pending, *others]
    rows = sorted(rows, key=lambda row: (-media_priority_score(row, source), duration_seconds(row.get("duration")) or 999999, str(row.get("source_title") or "")))
    return [benchmark_sample_row(source, row, role, include_media_url) for row in rows[:limit]]

def benchmark_sample_row(source: Source, row: dict[str, Any], role: str, include_media_url: bool) -> dict[str, Any]:
    output = {
        "sample_id": f"{source.id}:{row.get('id')}",
        "role": role,
        "source_id": source.id,
        "source_kind": source.kind,
        "media_id": row.get("id"),
        "source_title": row.get("source_title"),
        "source_url": row.get("source_url"),
        "media_kind": row.get("media_kind"),
        "duration": row.get("duration"),
        "duration_seconds": duration_seconds(row.get("duration")),
        "transcript_status": row.get("transcript_status"),
        "media_url_available": bool(row.get("media_url")),
        "benchmark_tasks": MEDIA_UNDERSTANDING_BENCHMARK_ROLES.get(role, []),
        "prompt": media_understanding_prompt(role),
        "private_storage": True,
        "public_publish_mode": "private_review_only",
    }
    if include_media_url:
        output["media_url"] = row.get("media_url")
    return output

def media_understanding_prompt(role: str) -> str:
    shared = (
        "Analyze this Rock RMS media item as private benchmark evidence. "
        "Return non-verbatim notes with concise topic labels, timestamp references when available, "
        "and a clear distinction between audio transcript facts and visual observations."
    )
    if role in {"official_rock_video", "rock_training_video", "community_video", "triumph_technical_video"}:
        return shared + " Include any screen, slide, UI, or demo context that would not appear in an audio-only transcript."
    return shared + " Focus on transcript accuracy, speaker or host context, and durable topics for later reviewer-written summaries."

def dedupe_benchmark_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    seen: set[str] = set()
    for row in rows:
        key = str(row.get("sample_id") or "")
        if key and key not in seen:
            seen.add(key)
            output.append(row)
    return output
