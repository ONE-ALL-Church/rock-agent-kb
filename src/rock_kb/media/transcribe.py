from ._shared import *  # noqa: F401,F403


def transcribe_skill_script() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    return codex_home / "skills" / "transcribe" / "scripts" / "transcribe_diarize.py"

def media_tool_status() -> dict[str, Any]:
    script = transcribe_skill_script()
    has_openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    understanding_status = media_understanding_tool_status()
    return {
        "ffmpeg": bool(optional_command("ffmpeg")),
        "uvx": bool(optional_command("uvx")),
        "yt_dlp": bool(optional_command("yt-dlp")),
        "yt_dlp_via_uvx": bool(optional_command("uvx")),
        "whisper": bool(optional_command("whisper")),
        "mlx_whisper": bool(optional_command("mlx_whisper")),
        "whisper_cli": bool(optional_command("whisper-cli")),
        "parakeet": bool(optional_command("parakeet")),
        "openai_transcribe_script": script.exists(),
        "openai_api_key": has_openai_key,
        "download_ready": bool(optional_command("yt-dlp") or optional_command("uvx")),
        "local_transcription_ready": any(optional_command(name) for name in ["mlx_whisper", "parakeet", "whisper", "whisper-cli"]),
        "openai_transcription_ready": script.exists() and has_openai_key,
        "recommended_local_tool": "mlx_whisper",
        "recommended_local_model": MLX_WHISPER_MODEL,
        "experimental_high_throughput_tool": "parakeet",
        "experimental_high_throughput_model": PARAKEET_MODEL,
        "experimental_media_understanding": understanding_status,
        "smoke_test_model": MLX_WHISPER_SMOKE_MODEL,
        "notes": [
            "OpenAI transcription uses OPENAI_API_KEY and the bundled transcribe skill script.",
            "On Apple Silicon, mlx-whisper with Whisper Large v3 Turbo is the recommended local default.",
            "Parakeet CLI is tracked as the newer high-throughput local candidate; it may require ffmpeg conversion to WAV.",
            "Gemma 4 12B is tracked only as an experimental second-pass audio/video understanding candidate.",
            "Video/HLS downloads use yt-dlp directly or via uvx.",
            "Raw media downloads and transcripts stay under data/media/ and are private.",
        ],
    }

def transcribe_media(
    source: Source,
    limit: Optional[int] = None,
    tool: str = "auto",
    model: str = "base",
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    rows = pending_media_rows(source.id, limit=limit, source=source)
    selected_tool = choose_transcription_tool(tool)
    results: list[dict[str, Any]] = []
    existing_by_id: dict[Any, dict[str, Any]] = {}
    if not dry_run:
        existing = [row for row in read_jsonl(transcript_index_path(source.id)) if row.get("transcript_status") != "dry_run"]
        existing_by_id = {row.get("id"): row for row in existing}
    for row in rows:
        if dry_run or not selected_tool:
            result = transcript_queue_row(row, selected_tool, dry_run=dry_run)
        else:
            try:
                result = transcribe_one(row, selected_tool, model)
            except Exception as exc:
                result = transcript_error_row(row, selected_tool, model, exc)
        results.append(result)
        if not dry_run:
            existing_by_id[result["id"]] = result
            write_jsonl(transcript_index_path(source.id), existing_by_id.values())
            sync_media_manifest_transcript_status(source.id, [result])
    if dry_run:
        return results
    if not results:
        write_jsonl(transcript_index_path(source.id), existing_by_id.values())
    return results

def run_media_batch(
    source: Source,
    limit: int = 1,
    tool: str = "auto",
    model: str = "auto",
    dry_run: bool = False,
    normalize: bool = True,
    sidecars: bool = True,
    min_transcript_chars: int = 80,
) -> dict[str, Any]:
    pending_before = pending_media_rows(source.id, limit=limit, source=source)
    transcript_rows = transcribe_media(source, limit=limit, tool=tool, model=model, dry_run=dry_run)
    insight_rows: list[dict[str, Any]] = []
    sidecar_result: dict[str, Any] | None = None
    if not dry_run:
        if normalize:
            insight_rows = build_media_insights(source, min_transcript_chars=min_transcript_chars)
        if sidecars:
            sidecar_result = build_media_sidecars(source)
    statuses = count_values(row.get("transcript_status") for row in transcript_rows)
    return {
        "source_id": source.id,
        "dry_run": dry_run,
        "limit": limit,
        "selected_count": len(pending_before),
        "selected": [
            {
                "media_id": row.get("id"),
                "source_title": row.get("source_title"),
                "media_kind": row.get("media_kind"),
                "duration": row.get("duration"),
                "status": row.get("transcript_status"),
                "priority_score": media_priority_score(row, source),
                "priority_reasons": media_priority_reasons(row, source),
            }
            for row in pending_before
        ],
        "transcript_rows": len(transcript_rows),
        "transcript_statuses": statuses,
        "insight_rows": len(insight_rows),
        "sidecar_result": sidecar_result,
        "report": media_status_report(source) if not dry_run else None,
    }

def choose_transcription_tool(tool: str) -> Optional[str]:
    normalized = tool.strip().lower()
    if normalized in {"openai", "openai-transcribe", "gpt-4o-mini-transcribe", "gpt-4o-transcribe"}:
        return "openai-transcribe" if transcribe_skill_script().exists() else None
    candidates = [normalized] if normalized != "auto" else auto_transcription_candidates()
    for candidate in candidates:
        if candidate == "openai-transcribe" and transcribe_skill_script().exists():
            return candidate
        if optional_command(candidate):
            return candidate
    return None

def auto_transcription_candidates() -> list[str]:
    if os.environ.get("OPENAI_API_KEY") and transcribe_skill_script().exists():
        return ["openai-transcribe", "mlx_whisper", "parakeet", "whisper-cli", "whisper"]
    return ["mlx_whisper", "parakeet", "whisper-cli", "whisper"]

def transcript_queue_row(media_row: dict[str, Any], selected_tool: Optional[str], dry_run: bool) -> dict[str, Any]:
    status = "dry_run" if dry_run else "queued_missing_tool"
    return {
        "id": media_row["id"] + ":transcript",
        "media_id": media_row["id"],
        "source_id": media_row["source_id"],
        "source_record_id": media_row["source_record_id"],
        "source_url": media_row["source_url"],
        "source_title": media_row["source_title"],
        "media_url": media_row["media_url"],
        "transcript_status": status,
        "transcription_tool": selected_tool,
        "transcription_model": None,
        "transcribed_at": now_iso(),
        "transcript_path": None,
        "transcript": "",
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_transcript_only",
        "citations": media_row.get("citations") or [],
    }

def transcript_error_row(media_row: dict[str, Any], selected_tool: Optional[str], model: str, exc: Exception) -> dict[str, Any]:
    return {
        "id": media_row["id"] + ":transcript",
        "media_id": media_row["id"],
        "source_id": media_row["source_id"],
        "source_record_id": media_row["source_record_id"],
        "source_url": media_row["source_url"],
        "source_title": media_row["source_title"],
        "media_url": media_row["media_url"],
        "transcript_status": "failed",
        "transcription_tool": selected_tool,
        "transcription_model": model,
        "transcribed_at": now_iso(),
        "transcript_path": None,
        "transcript": "",
        "error": str(exc)[:1000],
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_transcript_only",
        "citations": media_row.get("citations") or [],
    }

def transcribe_one(media_row: dict[str, Any], tool: str, model: str) -> dict[str, Any]:
    media_path = download_media(media_row)
    transcription_input_path = prepare_media_for_transcription(media_path, tool)
    transcript_dir = MEDIA_DIR / "transcripts" / media_row["source_id"]
    transcript_dir.mkdir(parents=True, exist_ok=True)
    command = transcription_command(tool, transcription_input_path, transcript_dir, model)
    effective_model = effective_transcription_model(tool, model)
    result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=3600)
    output = read_transcription_output_detail(transcription_input_path, transcript_dir, result.stdout)
    transcript_text = str(output.get("text") or "")
    raw_transcript_payload_path = output.get("payload_path")
    if output.get("raw_payload") is not None and raw_transcript_payload_path and not Path(raw_transcript_payload_path).exists():
        Path(raw_transcript_payload_path).write_text(
            json.dumps(output["raw_payload"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    status = "transcribed" if result.returncode == 0 and transcript_text.strip() else "failed"
    transcript_row_path = transcript_dir / f"{transcription_input_path.stem}.row.json"
    row = {
        "id": media_row["id"] + ":transcript",
        "media_id": media_row["id"],
        "source_id": media_row["source_id"],
        "source_record_id": media_row["source_record_id"],
        "source_url": media_row["source_url"],
        "source_title": media_row["source_title"],
        "media_url": media_row["media_url"],
        "transcript_status": status,
        "transcription_tool": tool,
        "transcription_model": effective_model,
        "transcribed_at": now_iso(),
        "transcript_path": str(transcript_row_path),
        "raw_transcript_payload_path": str(raw_transcript_payload_path) if raw_transcript_payload_path else None,
        "transcript": transcript_text,
        "transcript_segments": output.get("segments") or [],
        "transcript_segment_count": len(output.get("segments") or []),
        "timestamped_transcript_available": bool(output.get("segments")),
        "stdout_preview": result.stdout[:1000],
        "stderr_preview": result.stderr[:1000],
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_transcript_only",
        "citations": media_row.get("citations") or [],
    }
    transcript_row_path.write_text(json.dumps(row, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return row

def download_media(media_row: dict[str, Any]) -> Path:
    parsed = urlparse(str(media_row["media_url"]))
    suffix = Path(parsed.path).suffix or ".media"
    if should_use_ytdlp(str(media_row["media_url"])):
        return download_with_ytdlp(str(media_row["media_url"]), str(media_row["id"]))
    destination = MEDIA_DIR / "downloads" / f"{media_row['id']}{suffix}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        return destination
    with httpx.stream("GET", str(media_row["media_url"]), follow_redirects=True, timeout=120, headers={"User-Agent": USER_AGENT}) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_bytes():
                handle.write(chunk)
    return destination

def should_use_ytdlp(url: str) -> bool:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in STREAMING_EXTENSIONS:
        return True
    host = parsed.netloc.lower()
    return any(hint in host for hint in {"youtube.com", "youtu.be", "vimeo.com", "wistia.com", "wistia.net"})

def download_with_ytdlp(url: str, media_id: str) -> Path:
    command_prefix = ytdlp_command_prefix()
    if not command_prefix:
        raise RuntimeError("yt-dlp is required to download streaming/video media before transcription")
    destination_dir = MEDIA_DIR / "downloads"
    destination_dir.mkdir(parents=True, exist_ok=True)
    output_template = destination_dir / f"{media_id}.%(ext)s"
    command = [
        *command_prefix,
        "--no-playlist",
        "-x",
        "--audio-format",
        "mp3",
        "-o",
        str(output_template),
        url,
    ]
    result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:1000] or result.stdout[:1000] or "yt-dlp failed")
    candidates = sorted(destination_dir.glob(f"{media_id}.*"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        raise RuntimeError("yt-dlp finished without producing a media file")
    return candidates[0]

def prepare_media_for_transcription(media_path: Path, tool: str) -> Path:
    if tool != "parakeet":
        return media_path
    if media_path.suffix.lower() == ".wav":
        return media_path
    ffmpeg = optional_command("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to convert non-WAV media before Parakeet transcription")
    destination = media_path.with_suffix(".parakeet.wav")
    if destination.exists() and destination.stat().st_size > 0:
        return destination
    command = [ffmpeg, "-y", "-i", str(media_path), "-ac", "1", "-ar", "16000", str(destination)]
    result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:1000] or result.stdout[:1000] or "ffmpeg conversion failed")
    return destination

def ytdlp_command_prefix() -> list[str]:
    ytdlp = optional_command("yt-dlp")
    if ytdlp:
        return [ytdlp]
    uvx = optional_command("uvx")
    if uvx:
        return [uvx, "--from", "yt-dlp", "yt-dlp"]
    return []

def transcription_command(tool: str, media_path: Path, transcript_dir: Path, model: str) -> list[str]:
    if tool == "openai-transcribe":
        selected_model = OPENAI_TRANSCRIBE_MODEL if model in {"auto", "base"} else model
        return [
            sys.executable,
            str(transcribe_skill_script()),
            str(media_path),
            "--model",
            selected_model,
            "--response-format",
            "text",
            "--chunking-strategy",
            "auto",
            "--out-dir",
            str(transcript_dir),
        ]
    if tool == "whisper":
        selected_model = "base" if model == "auto" else model
        return [tool, str(media_path), "--model", selected_model, "--output_dir", str(transcript_dir), "--output_format", "json"]
    if tool == "mlx_whisper":
        selected_model = normalize_mlx_model(model)
        return [tool, str(media_path), "--model", selected_model, "--output-dir", str(transcript_dir), "--output-format", "json"]
    if tool == "parakeet":
        return [tool, "transcribe", str(media_path), "--format", "json"]
    return [tool, str(media_path)]

def normalize_mlx_model(model: str) -> str:
    value = (model or "auto").strip()
    aliases = {
        "auto": MLX_WHISPER_MODEL,
        "large-v3-turbo": MLX_WHISPER_MODEL,
        "turbo": MLX_WHISPER_MODEL,
        "tiny": MLX_WHISPER_SMOKE_MODEL,
        "smoke": MLX_WHISPER_SMOKE_MODEL,
    }
    return aliases.get(value, value)

def effective_transcription_model(tool: str, model: str) -> str:
    if tool == "mlx_whisper":
        return normalize_mlx_model(model)
    if tool == "openai-transcribe":
        return OPENAI_TRANSCRIBE_MODEL if model in {"auto", "base"} else model
    if tool == "whisper":
        return "base" if model == "auto" else model
    if tool == "parakeet":
        return PARAKEET_MODEL if model == "auto" else model
    return model

def read_transcription_output(media_path: Path, transcript_dir: Path, stdout: str) -> tuple[str, Optional[Path]]:
    output = read_transcription_output_detail(media_path, transcript_dir, stdout)
    payload_path = output.get("payload_path")
    return str(output.get("text") or ""), Path(payload_path) if payload_path else None

def read_transcription_output_detail(media_path: Path, transcript_dir: Path, stdout: str) -> dict[str, Any]:
    json_path = transcript_dir / f"{media_path.stem}.json"
    txt_path = transcript_dir / f"{media_path.stem}.txt"
    skill_txt_path = transcript_dir / f"{media_path.stem}.transcript.txt"
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        text = transcript_text_from_payload(payload)
        return {"text": text, "payload_path": json_path, "raw_payload": payload, "segments": extract_transcript_segments(payload)}
    if txt_path.exists():
        return {"text": txt_path.read_text(encoding="utf-8"), "payload_path": txt_path, "raw_payload": None, "segments": []}
    if skill_txt_path.exists():
        return {"text": skill_txt_path.read_text(encoding="utf-8"), "payload_path": skill_txt_path, "raw_payload": None, "segments": []}
    stdout_value = stdout.strip()
    if stdout_value.startswith("{"):
        try:
            payload = json.loads(stdout_value)
            text = transcript_text_from_payload(payload)
            if isinstance(text, str):
                return {
                    "text": text,
                    "payload_path": transcript_dir / f"{media_path.stem}.transcript.json",
                    "raw_payload": payload,
                    "segments": extract_transcript_segments(payload),
                }
        except json.JSONDecodeError:
            pass
    return {"text": stdout, "payload_path": transcript_dir / f"{media_path.stem}.transcript.json", "raw_payload": None, "segments": []}

def transcript_text_from_payload(payload: dict[str, Any]) -> str:
    text = payload.get("text") or payload.get("transcript") or payload.get("transcription")
    if isinstance(text, str):
        return text
    segments = extract_transcript_segments(payload)
    return " ".join(str(segment.get("text") or "").strip() for segment in segments if segment.get("text")).strip()

def extract_transcript_segments(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    raw_segments = payload.get("segments")
    if not isinstance(raw_segments, list):
        raw_segments = payload.get("chunks")
    if not isinstance(raw_segments, list):
        return []
    segments = []
    for raw_segment in raw_segments:
        segment = normalize_transcript_segment(raw_segment)
        if segment:
            segments.append(segment)
    return segments

def normalize_transcript_segment(raw_segment: Any) -> Optional[dict[str, Any]]:
    if not isinstance(raw_segment, dict):
        return None
    text = str(raw_segment.get("text") or "").strip()
    start = raw_segment.get("start")
    end = raw_segment.get("end")
    timestamp = raw_segment.get("timestamp")
    if isinstance(timestamp, (list, tuple)) and timestamp:
        start = timestamp[0]
        if len(timestamp) > 1:
            end = timestamp[1]
    start_seconds = numeric_seconds(start)
    end_seconds = numeric_seconds(end)
    if not text or start_seconds is None:
        return None
    return {
        "start": start_seconds,
        "end": end_seconds,
        "timestamp": format_timestamp(start_seconds),
        "text": text,
    }
