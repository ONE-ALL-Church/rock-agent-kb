import json
from pathlib import Path
from types import SimpleNamespace

import rock_kb.media as media_module
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.media import (
    build_media_public_rewrite_drafts,
    build_media_sidecars,
    build_media_priority_queue,
    build_media_understanding_benchmark,
    choose_transcription_tool,
    duration_seconds,
    discover_media,
    effective_transcription_model,
    extract_transcript_segments,
    format_timestamp,
    extract_media_urls,
    infer_media_kind,
    media_public_candidate_records,
    media_global_index_path,
    media_insight_records,
    media_insights_path,
    media_priority_queue_path,
    media_priority_report_path,
    media_priority_reasons,
    media_priority_score,
    media_public_candidates_path,
    media_public_promotions_path,
    media_public_rewrite_drafts_path,
    media_review_status_report,
    media_rows_from_normalized,
    media_sidecar_path,
    media_source_index_path,
    media_status_report,
    media_understanding_benchmark_path,
    media_tool_status,
    media_transcript_excerpt,
    normalize_mlx_model,
    ollama_media_payloads,
    pending_media_rows,
    prepare_media_understanding_benchmark_asset,
    prepare_media_for_transcription,
    prune_dry_run_transcript_rows,
    promote_media_public_candidates,
    priority_term_matches,
    read_transcription_output,
    read_transcription_output_detail,
    read_cloudflare_transcription_output,
    run_media_batch,
    summarize_transcript_insight,
    should_use_ytdlp,
    sync_media_manifest_transcript_status,
    transcribe_media,
    transcription_command,
    transcript_queue_row,
    ytdlp_command_prefix,
)
from rock_kb.normalize import parse_rss
from rock_kb.sources import get_source

FIXTURES = Path(__file__).parent / "fixtures"


def test_rss_media_rows_are_private_and_traceable():
    source = get_source("rock_podcast_rss")
    records = parse_rss(source, (FIXTURES / "rss.xml").read_text())
    rows = media_rows_from_normalized(source, records)
    assert len(rows) == 1
    row = rows[0]
    assert row["media_url"] == "https://example.com/audio/episode-214.mp3"
    assert row["media_kind"] == "audio"
    assert row["transcript_status"] == "pending"
    assert row["private_storage"] is True
    assert row["public_publish_mode"] == "private_only"
    assert row["source_record_id"].startswith("rock_podcast_rss:")
    assert row["citations"][0]["url"] == "https://shows.acast.com/rock-cast/episodes/episode-214"


def test_youtube_rss_media_discovery_uses_structured_feed(monkeypatch):
    source = get_source("rock_youtube")
    xml = (FIXTURES / "youtube_feed.xml").read_text()
    monkeypatch.setattr(
        media_module,
        "fetch_url",
        lambda _url: {"content": xml},
    )

    rows = discover_media(source)

    assert len(rows) == 1
    assert rows[0]["source_title"] == "AI Summit: The Community's First Look at Rock's AI Agents"
    assert rows[0]["media_url"] == "https://www.youtube.com/watch?v=UvW68dZBcJ8"
    assert rows[0]["media_kind"] == "video"


def test_extract_media_urls_from_html():
    html = """
    <main>
      <iframe src="/media/player/abc"></iframe>
      <audio><source src="https://cdn.example.org/talk.mp3" type="audio/mpeg"></audio>
      <a href="https://vimeo.com/123456">Watch</a>
      <script>window.asset = "https://media.example.org/video.mp4";</script>
    </main>
    """
    urls = extract_media_urls(html, "https://community.rockrms.com/community-hubs/abc")
    assert "https://cdn.example.org/talk.mp3" in urls
    assert "https://media.example.org/video.mp4" in urls
    assert "https://vimeo.com/123456" in urls
    assert "https://community.rockrms.com/media/player/abc" not in urls


def test_infer_media_kind():
    assert infer_media_kind("https://example.org/a.mp3") == "audio"
    assert infer_media_kind("https://example.org/v.mp4") == "video"
    assert infer_media_kind("https://player.vimeo.com/external/123.m3u8") == "video"
    assert infer_media_kind("https://vimeo.com/123") == "video"
    assert should_use_ytdlp("https://player.vimeo.com/external/123.m3u8")


def test_transcript_queue_row_is_private():
    row = {
        "id": "media:abc",
        "source_id": "rock_podcast_rss",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-214",
        "source_title": "Episode 214",
        "media_url": "https://example.com/audio/episode-214.mp3",
        "citations": [{"source_id": "rock_podcast_rss", "url": "https://shows.acast.com/rock-cast/episodes/episode-214"}],
    }
    queued = transcript_queue_row(row, selected_tool=None, dry_run=False)
    assert queued["transcript_status"] == "queued_missing_tool"
    assert queued["transcript"] == ""
    assert queued["private_storage"] is True
    assert queued["public_publish_mode"] == "private_only"


def test_transcribe_media_reuses_existing_transcript_index_row(monkeypatch, tmp_path):
    source = SimpleNamespace(id="rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr(media_module, "MEDIA_DIR", media_dir)
    manifest_path = media_dir / "rock_podcast_rss.media.jsonl"
    transcript_path = media_dir / "rock_podcast_rss.transcripts.jsonl"
    write_jsonl(
        manifest_path,
        [
            {
                "id": "media:abc",
                "source_id": "rock_podcast_rss",
                "source_record_id": "record:abc",
                "source_url": "https://example.org/episode",
                "source_title": "Episode",
                "media_url": "https://example.org/episode.mp3",
                "transcript_status": "pending",
            }
        ],
    )
    write_jsonl(
        transcript_path,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "transcript_status": "transcribed",
                "transcript": "Already transcribed.",
            }
        ],
    )
    monkeypatch.setattr(media_module, "transcribe_one", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("should not re-transcribe")))

    rows = transcribe_media(source, limit=1, tool="auto")

    assert rows[0]["transcription_reused"] is True
    assert rows[0]["transcript"] == "Already transcribed."


def test_openai_transcription_command_uses_bundled_skill(monkeypatch, tmp_path):
    script = tmp_path / "transcribe_diarize.py"
    script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    monkeypatch.setattr("rock_kb.media.transcribe_skill_script", lambda: script)
    command = transcription_command("openai-transcribe", tmp_path / "audio.mp3", tmp_path / "out", "auto")
    assert str(script) in command
    assert "gpt-4o-mini-transcribe" in command
    assert "--chunking-strategy" in command


def test_mlx_transcription_command_uses_large_v3_turbo_by_default(tmp_path):
    command = transcription_command("mlx_whisper", tmp_path / "audio.mp3", tmp_path / "out", "auto")
    assert "mlx-community/whisper-large-v3-turbo" in command
    assert "--output-format" in command
    assert "json" in command


def test_parakeet_transcription_command_uses_json_stdout(tmp_path):
    command = transcription_command("parakeet", tmp_path / "audio.wav", tmp_path / "out", "auto")
    assert command == ["parakeet", "transcribe", str(tmp_path / "audio.wav"), "--format", "json"]


def test_prepare_media_for_transcription_leaves_wav_for_parakeet(tmp_path):
    media_path = tmp_path / "audio.wav"
    media_path.write_bytes(b"RIFF")
    assert prepare_media_for_transcription(media_path, "parakeet") == media_path


def test_read_transcription_output_can_parse_json_stdout(tmp_path):
    transcript, payload_path = read_transcription_output(
        tmp_path / "audio.wav",
        tmp_path,
        '{"text":"Rock security roles and permissions."}',
    )
    assert transcript == "Rock security roles and permissions."
    assert payload_path == tmp_path / "audio.transcript.json"


def test_read_transcription_output_detail_preserves_segments(tmp_path):
    payload = {
        "text": "Rock workflows matter.",
        "segments": [
            {"start": 62.4, "end": 66.1, "text": "Rock workflows matter."},
            {"start": "01:12", "end": "01:15", "text": "Permissions should be reviewed."},
        ],
    }
    (tmp_path / "audio.json").write_text(json.dumps(payload), encoding="utf-8")

    output = read_transcription_output_detail(tmp_path / "audio.wav", tmp_path, "")

    assert output["text"] == "Rock workflows matter."
    assert output["payload_path"] == tmp_path / "audio.json"
    assert output["segments"][0]["timestamp"] == "01:02"
    assert output["segments"][1]["start"] == 72.0


def test_extract_transcript_segments_supports_chunk_timestamps():
    segments = extract_transcript_segments(
        {
            "chunks": [
                {"timestamp": [3.2, 8.4], "text": "AI agents can help Rock admins."},
                {"timestamp": [10, 12], "text": ""},
            ]
        }
    )

    assert segments == [{"start": 3.2, "end": 8.4, "timestamp": "00:03", "text": "AI agents can help Rock admins."}]
    assert format_timestamp(3661) == "01:01:01"


def test_normalize_mlx_model_aliases():
    assert normalize_mlx_model("auto") == "mlx-community/whisper-large-v3-turbo"
    assert normalize_mlx_model("tiny") == "mlx-community/whisper-tiny"
    assert effective_transcription_model("mlx_whisper", "auto") == "mlx-community/whisper-large-v3-turbo"
    assert effective_transcription_model("parakeet", "auto") == "nvidia/parakeet-tdt-0.6b-v3"
    assert effective_transcription_model("cloudflare-workers-ai", "auto") == "@cf/openai/whisper-large-v3-turbo"


def test_choose_openai_transcription_tool_when_requested(monkeypatch, tmp_path):
    script = tmp_path / "transcribe_diarize.py"
    script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    monkeypatch.setattr("rock_kb.media.transcribe_skill_script", lambda: script)
    assert choose_transcription_tool("openai") == "openai-transcribe"


def test_choose_cloudflare_transcription_tool_when_requested(monkeypatch):
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "test-token")
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "test-account")
    assert choose_transcription_tool("cloudflare") == "cloudflare-workers-ai"
    assert choose_transcription_tool("cloudflare-workers-ai") == "cloudflare-workers-ai"


def test_ytdlp_can_fall_back_to_uvx(monkeypatch):
    monkeypatch.setattr("rock_kb.media.optional_command", lambda name: "/usr/bin/uvx" if name == "uvx" else None)
    assert ytdlp_command_prefix() == ["/usr/bin/uvx", "--from", "yt-dlp", "yt-dlp"]


def test_media_tool_status_reports_openai_readiness(monkeypatch, tmp_path):
    script = tmp_path / "transcribe_diarize.py"
    script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    monkeypatch.setattr("rock_kb.media.transcribe_skill_script", lambda: script)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("rock_kb.media.optional_command", lambda name: "/usr/bin/" + name if name in {"ffmpeg", "uvx"} else None)
    status = media_tool_status()
    assert status["openai_transcription_ready"] is True
    assert status["download_ready"] is True


def test_media_tool_status_reports_cloudflare_readiness(monkeypatch, tmp_path):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / ".codex"))
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "test-token")
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "test-account")
    status = media_tool_status()
    assert status["cloudflare_transcription_ready"] is True
    assert status["recommended_hosted_tool"] == "cloudflare-workers-ai"


def test_read_cloudflare_transcription_output_parses_nested_result(tmp_path):
    payload = {
        "success": True,
        "result": {
            "text": "Cloudflare Workers AI transcribed Rock media.",
            "segments": [{"start": 1.2, "end": 3.4, "text": "Cloudflare Workers AI"}],
        },
    }
    output = read_cloudflare_transcription_output(tmp_path / "audio.mp3", tmp_path, payload)

    assert output["text"] == "Cloudflare Workers AI transcribed Rock media."
    assert output["payload_path"] == tmp_path / "audio.cloudflare.transcript.json"
    assert output["segments"][0]["timestamp"] == "00:01"


def test_media_status_report_counts_private_rows(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    normalized_dir = tmp_path / "normalized"
    media_dir.mkdir()
    normalized_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.NORMALIZED_DIR", normalized_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        '{"transcript_status":"pending","media_kind":"audio","media_url":"https://example.com/a.mp3"}\n'
        '{"transcript_status":"no_media_url_found","media_kind":null,"media_url":null}\n',
        encoding="utf-8",
    )
    (media_dir / "rock_podcast_rss.transcripts.jsonl").write_text(
        '{"transcript_status":"transcribed","transcription_tool":"mlx_whisper"}\n',
        encoding="utf-8",
    )
    (normalized_dir / "rock_podcast_rss.media-insights.jsonl").write_text('{"id":"insight"}\n', encoding="utf-8")

    report = media_status_report(source)

    assert report["media_rows"] == 2
    assert report["pending_transcription"] == 1
    assert report["transcribed_rows"] == 1
    assert report["insight_rows"] == 1
    assert report["sidecar_rows"] == 0
    assert report["private_storage"] is True
    assert report["public_publish_mode"] == "private_only_for_raw_transcripts"


def test_pending_media_rows_skips_transcribed_items(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps({"id": "media:done", "media_url": "https://example.com/done.mp3", "transcript_status": "transcribed"}) + "\n"
        + json.dumps({"id": "media:next", "media_url": "https://example.com/next.mp3", "transcript_status": "pending"}) + "\n"
        + json.dumps({"id": "media:empty", "media_url": None, "transcript_status": "pending"}) + "\n",
        encoding="utf-8",
    )

    rows = pending_media_rows("rock_podcast_rss", limit=1)

    assert [row["id"] for row in rows] == ["media:next"]


def test_pending_media_rows_can_target_stable_media_id(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    write_jsonl(
        media_dir / "rock_youtube.media.jsonl",
        [
            {"id": "media:first", "media_url": "https://youtube.com/watch?v=first", "transcript_status": "pending"},
            {"id": "media:summit", "media_url": "https://youtube.com/watch?v=summit", "transcript_status": "pending"},
        ],
    )

    rows = pending_media_rows("rock_youtube", media_ids=["media:summit"])

    assert [row["id"] for row in rows] == ["media:summit"]


def test_pending_media_rows_prioritizes_high_signal_items(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:general",
                "source_id": "rock_podcast_rss",
                "source_title": "General Community Story | Ep 100",
                "media_url": "https://example.com/general.mp3",
                "media_kind": "audio",
                "duration": "58:00",
                "transcript_status": "pending",
            }
        )
        + "\n"
        + json.dumps(
            {
                "id": "media:ai",
                "source_id": "rock_podcast_rss",
                "source_title": "AI Agents and Release Risk | Ep 214",
                "media_url": "https://example.com/ai.mp3",
                "media_kind": "audio",
                "duration": "20:00",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    rows = pending_media_rows("rock_podcast_rss", source=source)

    assert [row["id"] for row in rows] == ["media:ai", "media:general"]
    assert media_priority_score(rows[0], source) > media_priority_score(rows[1], source)


def test_build_media_priority_queue_writes_ranked_private_queue(monkeypatch, tmp_path):
    source = get_source("rock_rocku")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_rocku.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:slow",
                "source_id": "rock_rocku",
                "source_title": "General Admin Training",
                "source_url": "https://community.rockrms.com/rocku/general",
                "media_url": "https://player.vimeo.com/external/1.m3u8",
                "media_kind": "video",
                "duration": "40:00",
                "transcript_status": "pending",
            }
        )
        + "\n"
        + json.dumps(
            {
                "id": "media:fast",
                "source_id": "rock_rocku",
                "source_title": "Check-In Manager",
                "source_url": "https://community.rockrms.com/rocku/check-in-manager",
                "media_url": "https://player.vimeo.com/external/2.m3u8",
                "media_kind": "video",
                "duration": "8:40",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = build_media_priority_queue([source])
    rows = list(read_jsonl(media_priority_queue_path()))
    report = json.loads(media_priority_report_path().read_text(encoding="utf-8"))

    assert result["queued_rows"] == 2
    assert rows[0]["rank"] == 1
    assert rows[0]["media_id"] == "media:fast"
    assert rows[0]["private_storage"] is True
    assert rows[0]["publishability_status"] == "private_media_queue_only"
    assert report["queued_by_source"] == {"rock_rocku": 2}
    assert duration_seconds("8:40") == 520


def test_build_media_understanding_benchmark_selects_private_eval_set(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    review_dir = tmp_path / "review"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.REVIEW_DIR", review_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "media:podcast-1",
                        "source_id": "rock_podcast_rss",
                        "source_title": "Rock's Future Anchored in Vision | Ep 202",
                        "source_url": "https://shows.acast.com/rock-cast/episodes/202",
                        "media_url": "https://cdn.example.org/202.mp3",
                        "media_kind": "audio",
                        "duration": "21:00",
                        "transcript_status": "pending",
                    }
                ),
                json.dumps(
                    {
                        "id": "media:podcast-2",
                        "source_id": "rock_podcast_rss",
                        "source_title": "Episode 33: Rock 7.3 and New RX2018 Tracks",
                        "source_url": "https://shows.acast.com/rock-cast/episodes/33",
                        "media_url": "https://cdn.example.org/33.mp3",
                        "media_kind": "audio",
                        "duration": "12:00",
                        "transcript_status": "pending",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (media_dir / "rock_community_hubs.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:hub-1",
                "source_id": "rock_community_hubs",
                "source_title": "Community Hub Walkthrough",
                "source_url": "https://community.rockrms.com/hubs/example",
                "media_url": "https://video.example.org/hub.m3u8",
                "media_kind": "video",
                "duration": "9:00",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (media_dir / "rock_rocku.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:rocku-1",
                "source_id": "rock_rocku",
                "source_title": "LMS - Create a Program",
                "source_url": "https://community.rockrms.com/rocku/lms/lms-create-a-program",
                "media_url": "https://player.vimeo.com/external/rocku.m3u8",
                "media_kind": "video",
                "duration": "8:00",
                "transcript_status": "transcribed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (media_dir / "triumph_resources.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:triumph-1",
                "source_id": "triumph_resources",
                "source_title": "GitHub Spotlight: 11/14/2025",
                "source_url": "https://www.triumph.tech/resources/github-spotlight-11142025",
                "media_url": "https://video.example.org/triumph.mp4",
                "media_kind": "video",
                "duration": "15:00",
                "transcript_status": "transcribed",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = build_media_understanding_benchmark(
        [get_source("rock_podcast_rss"), get_source("rock_community_hubs"), get_source("rock_rocku"), get_source("triumph_resources")]
    )

    assert result["selected_item_count"] == 5
    assert [row["role"] for row in result["selected_items"]] == [
        "podcast_audio",
        "podcast_audio",
        "community_video",
        "rock_training_video",
        "triumph_technical_video",
    ]
    assert all("media_url" not in row for row in result["selected_items"])
    assert media_understanding_benchmark_path().exists()


def test_media_understanding_benchmark_can_include_private_media_urls(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    review_dir = tmp_path / "review"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.REVIEW_DIR", review_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:podcast-1",
                "source_id": "rock_podcast_rss",
                "source_title": "Episode 1",
                "source_url": "https://shows.acast.com/rock-cast/episodes/1",
                "media_url": "https://cdn.example.org/1.mp3",
                "media_kind": "audio",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = build_media_understanding_benchmark([get_source("rock_podcast_rss")], include_media_url=True, write=False)

    assert result["selected_item_count"] == 1
    assert result["selected_items"][0]["media_url"] == "https://cdn.example.org/1.mp3"
    assert result["selected_items"][0]["public_publish_mode"] == "private_review_only"


def test_ollama_media_payloads_includes_raw_audio_and_frame(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    clip = tmp_path / "clip.wav"
    frame = tmp_path / "frame.jpg"
    clip.write_bytes(b"RIFF----WAVEfmt ")
    frame.write_bytes(b"\xff\xd8\xff")

    result = ollama_media_payloads(
        {
            "clip_status": "ok",
            "clip_path": "clip.wav",
            "frame_status": "ok",
            "frame_path": "frame.jpg",
        }
    )

    assert result["raw_audio_input"] is True
    assert result["frame_input"] is True
    assert result["audio_payload_path"] is not None
    assert result["audio_payload_bytes"] > 0
    assert result["source_clip_bytes"] > 0
    assert len(result["base64"]) == 2
    assert result["base64"][0] != result["base64"][1]


def test_prepare_media_understanding_benchmark_asset_writes_clip_and_frame(monkeypatch, tmp_path):
    media_file = tmp_path / "download.mp3"
    media_file.write_bytes(b"audio")

    def fake_download(row):
        assert row["media_url"] == "https://video.example.org/item.m3u8"
        return media_file

    def fake_audio_clip(media_path, output_path, seconds):
        assert media_path == media_file
        assert seconds == 30
        output_path.write_bytes(b"wav")

    def fake_video_frame(input_value, output_path):
        assert input_value == "https://video.example.org/item.m3u8"
        output_path.write_bytes(b"jpg")

    monkeypatch.setattr("rock_kb.media.download_media", fake_download)
    monkeypatch.setattr("rock_kb.media.extract_audio_clip", fake_audio_clip)
    monkeypatch.setattr("rock_kb.media.extract_video_frame", fake_video_frame)

    result = prepare_media_understanding_benchmark_asset(
        {
            "source_id": "rock_rocku",
            "media_id": "media:abc",
            "source_title": "Training Video",
            "media_kind": "video",
            "media_url": "https://video.example.org/item.m3u8",
            "transcript_status": "transcribed",
        },
        clip_dir=tmp_path / "clips",
        frame_dir=tmp_path / "frames",
        seconds=30,
    )

    assert result["clip_status"] == "ok"
    assert result["frame_status"] == "ok"
    assert result["download_path"] == str(media_file)
    assert Path(result["clip_path"]).exists()
    assert Path(result["frame_path"]).exists()


def test_media_transcript_excerpt_prefers_row_json(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    transcript_dir = media_dir / "transcripts" / "rock_rocku"
    transcript_dir.mkdir(parents=True)
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (transcript_dir / "media:abc.json").write_text(json.dumps({"transcript": "raw payload text"}), encoding="utf-8")
    (transcript_dir / "media:abc.row.json").write_text(
        json.dumps(
            {
                "transcript": "review row text",
                "transcript_segments": [{"start": 0, "end": 1, "text": "review row text"}],
            }
        ),
        encoding="utf-8",
    )

    text, path, segments = media_transcript_excerpt({"source_id": "rock_rocku", "media_id": "media:abc"})

    assert text == "review row text"
    assert path is not None and path.endswith("media:abc.row.json")
    assert len(segments) == 1


def test_priority_term_matching_avoids_substrings_and_media_url_tokens():
    source = get_source("rock_rocku")
    row = {
        "id": "media:training",
        "source_id": "rock_rocku",
        "source_title": "Staff Training",
        "source_url": "https://community.rockrms.com/rocku/staff-training",
        "media_url": "https://player.vimeo.com/external/1.m3u8?oauth2_token_id=123",
        "media_kind": "video",
        "duration": "8:00",
        "transcript_status": "pending",
    }

    assert priority_term_matches("ai agents", "ai") is True
    assert priority_term_matches("staff training", "ai") is False
    reasons = set(media_priority_reasons(row, source))
    assert "topic:ai-agent-readiness" not in reasons
    assert "topic:governance-risk" not in reasons


def test_transcribe_media_dry_run_does_not_write_index(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.choose_transcription_tool", lambda tool: "mlx_whisper")
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:next",
                "source_id": "rock_podcast_rss",
                "source_record_id": "rock_podcast_rss:next",
                "source_url": "https://shows.acast.com/rock-cast/episodes/next",
                "source_title": "Next",
                "media_url": "https://example.com/next.mp3",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    rows = transcribe_media(source, limit=1, tool="mlx_whisper", model="tiny", dry_run=True)

    assert rows[0]["media_id"] == "media:next"
    assert rows[0]["transcript_status"] == "dry_run"
    assert not (media_dir / "rock_podcast_rss.transcripts.jsonl").exists()


def test_transcribe_media_prunes_stale_dry_run_rows_on_real_write(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.choose_transcription_tool", lambda tool: "mlx_whisper")
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:next",
                "source_id": "rock_podcast_rss",
                "source_record_id": "rock_podcast_rss:next",
                "source_url": "https://shows.acast.com/rock-cast/episodes/next",
                "source_title": "Next",
                "media_url": "https://example.com/next.mp3",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (media_dir / "rock_podcast_rss.transcripts.jsonl").write_text(
        json.dumps({"id": "media:old:transcript", "media_id": "media:old", "transcript_status": "dry_run"})
        + "\n",
        encoding="utf-8",
    )

    def fake_transcribe_one(media_row, tool, model):
        return {
            "id": media_row["id"] + ":transcript",
            "media_id": media_row["id"],
            "source_id": media_row["source_id"],
            "source_record_id": media_row["source_record_id"],
            "source_url": media_row["source_url"],
            "source_title": media_row["source_title"],
            "media_url": media_row["media_url"],
            "transcript_status": "transcribed",
            "transcription_tool": tool,
            "transcription_model": model,
            "transcribed_at": "2026-06-02T00:00:00+00:00",
            "transcript_path": "data/media/transcripts/next.json",
            "transcript": "Rock operations transcript.",
        }

    monkeypatch.setattr("rock_kb.media.transcribe_one", fake_transcribe_one)

    transcribe_media(source, limit=1, tool="mlx_whisper", model="tiny")

    rows = list(read_jsonl(media_dir / "rock_podcast_rss.transcripts.jsonl"))
    assert [row["transcript_status"] for row in rows] == ["transcribed"]


def test_transcribe_media_persists_each_completed_row(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.choose_transcription_tool", lambda tool: "mlx_whisper")
    media_rows = [
        {
            "id": "media:first",
            "source_id": "rock_podcast_rss",
            "source_record_id": "rock_podcast_rss:first",
            "source_url": "https://shows.acast.com/rock-cast/episodes/first",
            "source_title": "First",
            "media_url": "https://example.com/first.mp3",
            "transcript_status": "pending",
        },
        {
            "id": "media:second",
            "source_id": "rock_podcast_rss",
            "source_record_id": "rock_podcast_rss:second",
            "source_url": "https://shows.acast.com/rock-cast/episodes/second",
            "source_title": "Second",
            "media_url": "https://example.com/second.mp3",
            "transcript_status": "pending",
        },
    ]
    write_jsonl(media_dir / "rock_podcast_rss.media.jsonl", media_rows)

    def fake_transcribe_one(media_row, tool, model):
        if media_row["id"] == "media:second":
            raise KeyboardInterrupt()
        return {
            "id": media_row["id"] + ":transcript",
            "media_id": media_row["id"],
            "source_id": media_row["source_id"],
            "source_record_id": media_row["source_record_id"],
            "source_url": media_row["source_url"],
            "source_title": media_row["source_title"],
            "media_url": media_row["media_url"],
            "transcript_status": "transcribed",
            "transcription_tool": tool,
            "transcription_model": model,
            "transcribed_at": "2026-06-02T00:00:00+00:00",
            "transcript_path": "data/media/transcripts/first.json",
            "transcript": "Rock operations transcript.",
        }

    monkeypatch.setattr("rock_kb.media.transcribe_one", fake_transcribe_one)

    interrupted = False
    try:
        transcribe_media(source, limit=2, tool="mlx_whisper", model="tiny")
    except KeyboardInterrupt:
        interrupted = True

    transcript_rows = list(read_jsonl(media_dir / "rock_podcast_rss.transcripts.jsonl"))
    manifest_rows = list(read_jsonl(media_dir / "rock_podcast_rss.media.jsonl"))
    assert interrupted is True
    assert [row["media_id"] for row in transcript_rows] == ["media:first"]
    assert manifest_rows[0]["transcript_status"] == "transcribed"
    assert manifest_rows[1]["transcript_status"] == "pending"


def test_prune_dry_run_transcript_rows_removes_stale_rows(monkeypatch, tmp_path):
    source = get_source("rock_community_hubs")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_community_hubs.transcripts.jsonl").write_text(
        json.dumps({"id": "dry", "transcript_status": "dry_run"})
        + "\n"
        + json.dumps({"id": "real", "transcript_status": "transcribed"})
        + "\n",
        encoding="utf-8",
    )

    result = prune_dry_run_transcript_rows(source)

    rows = list(read_jsonl(media_dir / "rock_community_hubs.transcripts.jsonl"))
    assert result["removed_dry_run_rows"] == 1
    assert [row["id"] for row in rows] == ["real"]


def test_run_media_batch_dry_run_previews_without_writes(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.choose_transcription_tool", lambda tool: "mlx_whisper")
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:next",
                "source_id": "rock_podcast_rss",
                "source_record_id": "rock_podcast_rss:next",
                "source_url": "https://shows.acast.com/rock-cast/episodes/next",
                "source_title": "Next Pending Episode",
                "media_url": "https://example.com/next.mp3",
                "media_kind": "audio",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = run_media_batch(source, limit=1, tool="mlx_whisper", model="tiny", dry_run=True)

    assert result["dry_run"] is True
    assert result["selected"][0]["source_title"] == "Next Pending Episode"
    assert result["transcript_statuses"] == {"dry_run": 1}
    assert result["report"] is None
    assert not (media_dir / "rock_podcast_rss.transcripts.jsonl").exists()


def test_run_media_batch_refreshes_private_artifacts(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    normalized_dir = tmp_path / "normalized"
    media_dir.mkdir()
    normalized_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    monkeypatch.setattr("rock_kb.media.NORMALIZED_DIR", normalized_dir)
    monkeypatch.setattr("rock_kb.media.choose_transcription_tool", lambda tool: "mlx_whisper")
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:next",
                "source_id": "rock_podcast_rss",
                "source_record_id": "rock_podcast_rss:next",
                "source_url": "https://shows.acast.com/rock-cast/episodes/next",
                "source_title": "Next Pending Episode",
                "media_url": "https://example.com/next.mp3",
                "media_kind": "audio",
                "transcript_status": "pending",
                "citations": [{"source_id": "rock_podcast_rss", "url": "https://shows.acast.com/rock-cast/episodes/next"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    def fake_transcribe_one(media_row, tool, model):
        return {
            "id": media_row["id"] + ":transcript",
            "media_id": media_row["id"],
            "source_id": media_row["source_id"],
            "source_record_id": media_row["source_record_id"],
            "source_url": media_row["source_url"],
            "source_title": media_row["source_title"],
            "media_url": media_row["media_url"],
            "transcript_status": "transcribed",
            "transcription_tool": tool,
            "transcription_model": model,
            "transcribed_at": "2026-06-02T00:00:00+00:00",
            "transcript_path": "data/media/transcripts/next.json",
            "transcript": "Rock staff training and workflow operations need repeatable documentation. " * 4,
            "private_storage": True,
            "public_publish_mode": "private_only",
            "publishability_status": "private_transcript_only",
            "citations": media_row.get("citations") or [],
        }

    monkeypatch.setattr("rock_kb.media.transcribe_one", fake_transcribe_one)

    result = run_media_batch(source, limit=1, tool="mlx_whisper", model="tiny")

    assert result["dry_run"] is False
    assert result["transcript_statuses"] == {"transcribed": 1}
    assert result["insight_rows"] == 1
    assert result["sidecar_result"]["sidecars"] == 1
    manifest_rows = list(read_jsonl(media_dir / "rock_podcast_rss.media.jsonl"))
    assert manifest_rows[0]["transcript_status"] == "transcribed"
    assert list(read_jsonl(normalized_dir / "rock_podcast_rss.media-insights.jsonl"))
    assert list(read_jsonl(media_source_index_path("rock_podcast_rss")))


def test_sync_media_manifest_transcript_status_updates_queue_row(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:abc",
                "source_id": "rock_podcast_rss",
                "media_url": "https://example.com/a.mp3",
                "transcript_status": "pending",
                "transcript_path": None,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    updated = sync_media_manifest_transcript_status(
        "rock_podcast_rss",
        [
            {
                "media_id": "media:abc",
                "transcript_status": "transcribed",
                "transcript_path": "data/media/transcripts/a.json",
                "transcription_tool": "mlx_whisper",
                "transcription_model": "tiny",
                "transcribed_at": "2026-06-02T00:00:00+00:00",
            }
        ],
    )

    rows = list(read_jsonl(media_dir / "rock_podcast_rss.media.jsonl"))
    assert updated == 1
    assert rows[0]["transcript_status"] == "transcribed"
    assert rows[0]["transcription_tool"] == "mlx_whisper"


def test_sync_media_manifest_transcript_status_ignores_dry_run(monkeypatch, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps({"id": "media:abc", "media_url": "https://example.com/a.mp3", "transcript_status": "pending"}) + "\n",
        encoding="utf-8",
    )

    updated = sync_media_manifest_transcript_status(
        "rock_podcast_rss",
        [{"media_id": "media:abc", "transcript_status": "dry_run", "transcription_tool": "mlx_whisper"}],
    )

    rows = list(read_jsonl(media_dir / "rock_podcast_rss.media.jsonl"))
    assert updated == 0
    assert rows[0]["transcript_status"] == "pending"


def test_build_media_sidecars_writes_private_sidecar_and_textless_index(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    transcript = "Rock check-in training should connect room setup, schedules, and release-note changes."
    media_row = {
        "id": "media:abc",
        "source_id": "rock_podcast_rss",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-214",
        "source_title": "Episode 214",
        "media_url": "https://example.com/audio/episode-214.mp3",
        "media_kind": "audio",
        "duration": "42:00",
        "transcript_status": "pending",
        "citations": [{"source_id": "rock_podcast_rss", "url": "https://shows.acast.com/rock-cast/episodes/episode-214"}],
    }
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_id": "rock_podcast_rss",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-214",
        "source_title": "Episode 214",
        "media_url": "https://example.com/audio/episode-214.mp3",
        "transcript_status": "transcribed",
        "transcription_tool": "mlx_whisper",
        "transcription_model": "tiny",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript_path": "data/media/transcripts/rock_podcast_rss/audio.json",
        "transcript": transcript,
    }
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(json.dumps(media_row) + "\n", encoding="utf-8")
    (media_dir / "rock_podcast_rss.transcripts.jsonl").write_text(json.dumps(transcript_row) + "\n", encoding="utf-8")

    result = build_media_sidecars(source)

    sidecar = media_sidecar_path("rock_podcast_rss", "media:abc")
    source_index = media_source_index_path("rock_podcast_rss")
    global_index = media_global_index_path()
    sidecar_text = sidecar.read_text(encoding="utf-8")
    index_text = source_index.read_text(encoding="utf-8")
    assert result["sidecars"] == 1
    assert transcript in sidecar_text
    assert "private media sidecar" in sidecar_text
    assert transcript not in index_text
    assert '"has_private_transcript": true' in index_text
    assert global_index.exists()


def test_build_media_sidecars_ignores_dry_run_transcript_rows(monkeypatch, tmp_path):
    source = get_source("rock_podcast_rss")
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    monkeypatch.setattr("rock_kb.media.MEDIA_DIR", media_dir)
    (media_dir / "rock_podcast_rss.media.jsonl").write_text(
        json.dumps(
            {
                "id": "media:abc",
                "source_id": "rock_podcast_rss",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-214",
                "source_title": "Episode 214",
                "media_url": "https://example.com/audio/episode-214.mp3",
                "media_kind": "audio",
                "transcript_status": "pending",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (media_dir / "rock_podcast_rss.transcripts.jsonl").write_text(
        json.dumps(
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "transcript_status": "dry_run",
                "transcription_tool": "mlx_whisper",
                "transcript": "",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    build_media_sidecars(source)

    rows = list(read_jsonl(media_source_index_path("rock_podcast_rss")))
    assert rows[0]["transcript_status"] == "pending"
    assert rows[0]["has_private_transcript"] is False


def test_media_insight_records_strip_raw_transcript():
    source = get_source("rock_podcast_rss")
    transcript = (
        "Rock admins should document their fragile workflows before vacation. "
        "The episode explains agentic AI and training gaps in Rock operations. "
        "Teams should connect release notes, staff training, and live process owners."
    )
    records = media_insight_records(
        source,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_title": "Episode 213",
                "media_url": "https://example.com/audio.mp3",
                "transcript_status": "transcribed",
                "transcription_tool": "openai-transcribe",
                "transcription_model": "gpt-4o-mini-transcribe",
                "transcribed_at": "2026-06-02T00:00:00+00:00",
                "transcript": transcript,
                "citations": [{"source_id": "rock_podcast_rss", "url": "https://shows.acast.com/rock-cast/episodes/episode-213"}],
            }
        ],
    )
    assert len(records) == 1
    record = records[0]
    assert "transcript" not in record
    assert record["derived_from_private_transcript"] is True
    assert record["transcript_hash"]
    assert record["source_record_id"] == "rock_podcast_rss:abc"
    assert record["citations"][0]["url"] == "https://shows.acast.com/rock-cast/episodes/episode-213"
    assert record["summary"]
    assert transcript not in record["summary"]
    assert not record["summary"].startswith("Rock admins should document")
    assert "Private transcript-derived insight" in record["summary"]


def test_media_insight_records_skip_failed_or_short_transcripts():
    source = get_source("rock_podcast_rss")
    records = media_insight_records(
        source,
        [
            {"transcript_status": "failed", "transcript": "This is long enough but failed." * 10},
            {"transcript_status": "transcribed", "transcript": "too short"},
        ],
    )
    assert records == []


def test_media_public_candidate_records_are_timestamped_without_raw_transcript():
    source = get_source("rock_podcast_rss")
    transcript = (
        "Rock admins discuss AI agents and automation. "
        "Later they explain staff training and permissions governance."
    )
    records = media_public_candidate_records(
        source,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_title": "Episode 213",
                "media_url": "https://example.com/audio.mp3",
                "transcript_status": "transcribed",
                "transcription_tool": "mlx_whisper",
                "transcription_model": "tiny",
                "transcribed_at": "2026-06-02T00:00:00+00:00",
                "transcript": transcript,
                "transcript_segments": [
                    {"start": 12.5, "end": 16.0, "text": "Rock admins discuss AI agents and automation."},
                    {"start": 98.0, "end": 104.0, "text": "Staff training should include permissions governance."},
                ],
                "citations": [{"source_id": "rock_podcast_rss", "url": "https://shows.acast.com/rock-cast/episodes/episode-213"}],
            }
        ],
    )

    assert len(records) == 1
    record = records[0]
    serialized = json.dumps(record)
    assert record["timestamped_transcript_available"] is True
    assert record["key_insights"][0]["timestamp"] == "00:12"
    assert record["contains_raw_transcript"] is False
    assert record["needs_review"] is True
    assert transcript not in serialized
    assert "Rock admins discuss AI agents" not in serialized


def test_media_public_promote_updates_matching_insight_without_raw_transcript(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript = "Rock admins discuss AI agents and automation. Staff training matters for governance." * 4
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "source_title": "Episode 213",
        "media_url": "https://example.com/audio.mp3",
        "transcript_status": "transcribed",
        "transcription_tool": "mlx_whisper",
        "transcription_model": "tiny",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript": transcript,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    insight = media_insight_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), [insight])
    rewrite = {
        "summary": "Rock administrators can use this episode as a public-safe reminder to pair AI automation with staff training and governance.",
        "key_insights": [
            {
                "topic": "governance",
                "insight": "Public automation guidance should connect AI use with staff training and permission review.",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_timestamp_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "timestamp": "00:12",
                "timestamp_seconds": 12,
                "contains_verbatim_transcript": False,
                "evidence_class": "operational_recommendation",
                "temporal_status": "current",
            }
        ],
        "generation_provenance": {
            "model": "test-model",
            "prompt_id": "rock-kb-media-claim-distillation",
            "prompt_version": "1.0.0",
            "method": "agent_reviewed_whole_source",
            "source_input_hash": candidate["transcript_hash"],
        },
    }

    result = promote_media_public_candidates(
        source,
        candidate_ids=[candidate["id"]],
        review_status="approved_for_public_distillation",
        reviewer="test-reviewer",
        concept_ids=["check-in"],
        rewrites_by_candidate_id={candidate["id"]: rewrite},
    )

    assert result["selected_candidates"] == 1
    assert result["updated_insight_rows"] == 1
    promotion = list(read_jsonl(media_public_promotions_path(source.id)))[0]
    updated = list(read_jsonl(media_insights_path(source.id)))[0]
    assert promotion["media_insight_id"] == insight["id"]
    assert promotion["contains_raw_transcript"] is False
    assert promotion["contains_verbatim_transcript"] is False
    assert promotion["review_rewrite_applied"] is True
    assert promotion["summary"] == rewrite["summary"]
    assert promotion["key_insights"][0]["timestamp"] == "00:12"
    assert promotion["key_insights"][0]["timestamp_seconds"] == 12
    assert promotion["generation_provenance"]["model"] == "test-model"
    assert updated["needs_review"] is False
    assert updated["review_status"] == "approved_for_public_distillation"
    assert updated["review_origin"] == "media_public_promotion"
    assert updated["approved_concept_ids"] == ["check-in"]
    assert updated["summary"] == rewrite["summary"]
    assert updated["key_insights"] == rewrite["key_insights"]
    assert updated["generation_provenance"] == rewrite["generation_provenance"]
    serialized = json.dumps(promotion)
    assert transcript not in serialized


def test_media_promotion_rejects_generation_provenance_for_different_source(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript = "Rock admins discuss a concrete workflow pattern and its permission boundaries. " * 4
    transcript_row = {
        "media_id": "media:hash-check",
        "source_record_id": "rock_podcast_rss:hash-check",
        "source_url": "https://shows.acast.com/rock-cast/episodes/hash-check",
        "source_title": "Hash Check",
        "transcript_status": "transcribed",
        "transcribed_at": "2026-07-09T00:00:00+00:00",
        "transcript": transcript,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), media_insight_records(source, [transcript_row]))
    rewrite = {
        "summary": "This source describes a workflow pattern with explicit permission boundaries.",
        "key_insights": [
            {
                "insight": "Workflow tools should expose only the permissions needed for the current task.",
                "source_url": transcript_row["source_url"],
            }
        ],
        "generation_provenance": {
            "model": "test-model",
            "prompt_id": "rock-kb-media-claim-distillation",
            "prompt_version": "1.0.0",
            "method": "agent_reviewed_whole_source",
            "source_input_hash": "0" * 64,
        },
    }

    try:
        promote_media_public_candidates(
            source,
            candidate_ids=[candidate["id"]],
            rewrites_by_candidate_id={candidate["id"]: rewrite},
        )
    except ValueError as exc:
        assert "does not match transcript_hash" in str(exc)
    else:
        raise AssertionError("expected mismatched generation provenance to be rejected")


def test_media_promotion_preserves_reviewed_at_when_only_provenance_is_added(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript = "Rock admins discuss a reusable workflow pattern and permission boundary. " * 4
    transcript_row = {
        "media_id": "media:idempotent",
        "source_record_id": "rock_podcast_rss:idempotent",
        "source_url": "https://shows.acast.com/rock-cast/episodes/idempotent",
        "source_title": "Idempotent Review",
        "transcript_status": "transcribed",
        "transcribed_at": "2026-07-09T00:00:00+00:00",
        "transcript": transcript,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    rewrite = {
        "summary": "This source describes a reusable workflow pattern with permission boundaries.",
        "key_insights": [
            {
                "insight": "Workflow tools should expose only the permissions needed for the current task.",
                "source_url": transcript_row["source_url"],
            }
        ],
    }
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), media_insight_records(source, [transcript_row]))
    promote_media_public_candidates(
        source,
        candidate_ids=[candidate["id"]],
        rewrites_by_candidate_id={candidate["id"]: rewrite},
    )
    promotion = next(read_jsonl(media_public_promotions_path(source.id)))
    promotion["reviewed_at"] = "2026-07-01T00:00:00+00:00"
    write_jsonl(media_public_promotions_path(source.id), [promotion])

    promote_media_public_candidates(
        source,
        candidate_ids=[candidate["id"]],
        rewrites_by_candidate_id={candidate["id"]: rewrite},
        review_provenance={
            "model": "test-model",
            "prompt_id": "legacy-review",
            "prompt_version": "legacy-unversioned",
            "method": "agent_reviewed_whole_source",
        },
    )
    updated = next(read_jsonl(media_public_promotions_path(source.id)))

    assert updated["reviewed_at"] == "2026-07-01T00:00:00+00:00"
    assert updated["generation_provenance"]["model"] == "test-model"


def test_build_media_insights_reapplies_existing_public_promotions(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript = "Rock admins discuss AI agents and automation. Staff training matters for governance. " * 4
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "source_title": "Episode 213",
        "media_url": "https://example.com/audio.mp3",
        "transcript_status": "transcribed",
        "transcription_tool": "mlx_whisper",
        "transcription_model": "tiny",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript": transcript,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    promotion = {
        "id": "media-public-promotion:test",
        "candidate_id": candidate["id"],
        "media_insight_id": candidate["media_insight_id"],
        "media_id": candidate["media_id"],
        "transcript_hash": candidate["transcript_hash"],
        "review_status": "approved_for_public_distillation",
        "reviewed_at": "2026-06-02T00:00:00+00:00",
        "reviewer": "test-reviewer",
        "summary": "Approved public-safe summary.",
        "key_insights": [{"topic": "governance", "insight": "Approved public-safe insight."}],
        "content_hash": "approved-content-hash",
        "topics": ["risk and governance"],
        "citations": candidate["citations"],
        "concept_ids": ["security-permissions"],
    }
    write_jsonl(media_module.transcript_index_path(source.id), [transcript_row])
    write_jsonl(media_public_promotions_path(source.id), [promotion])

    rows = media_module.build_media_insights(source)

    assert len(rows) == 1
    assert rows[0]["id"] == candidate["media_insight_id"]
    assert rows[0]["needs_review"] is False
    assert rows[0]["review_status"] == "approved_for_public_distillation"
    assert rows[0]["review_origin"] == "media_public_promotion"
    assert rows[0]["public_promotion_id"] == "media-public-promotion:test"
    assert rows[0]["summary"] == "Approved public-safe summary."
    assert rows[0]["approved_concept_ids"] == ["security-permissions"]


def test_media_public_promote_rejects_placeholder_without_rewrite(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "source_title": "Episode 213",
        "media_url": "https://example.com/audio.mp3",
        "transcript_status": "transcribed",
        "transcription_tool": "mlx_whisper",
        "transcription_model": "tiny",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript": "Rock admins discuss AI agents and automation. Staff training matters for governance." * 4,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    insight = media_insight_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), [insight])

    try:
        promote_media_public_candidates(
            source,
            candidate_ids=[candidate["id"]],
            review_status="approved_for_public_distillation",
            reviewer="test-reviewer",
            concept_ids=["check-in"],
        )
    except ValueError as exc:
        assert "placeholder review candidate" in str(exc)
    else:
        raise AssertionError("placeholder candidate promotion should require a rewrite")


def test_media_public_promote_rejects_tokenized_media_urls(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "source_title": "Episode 213",
        "media_url": "https://example.com/audio.mp3",
        "transcript_status": "transcribed",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript": "Rock admins discuss check-in operations and staff training. " * 8,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    insight = media_insight_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), [insight])

    try:
        promote_media_public_candidates(
            source,
            candidate_ids=[candidate["id"]],
            review_status="approved_for_public_distillation",
            reviewer="test-reviewer",
            rewrites_by_candidate_id={
                candidate["id"]: {
                    "summary": "Public-safe operations guidance should be reviewed before release.",
                    "key_insights": [
                        {
                            "topic": "governance",
                            "insight": "Use canonical public source pages for reviewed media citations.",
                            "source_url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret",
                            "contains_verbatim_transcript": False,
                        }
                    ],
                }
            },
        )
    except ValueError as exc:
        assert "direct, streaming, player, or tokenized media URL" in str(exc)
    else:
        raise AssertionError("tokenized direct media URL should be rejected")


def test_media_public_promote_rejects_raw_transcript_like_rewrites(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    source = get_source("rock_podcast_rss")
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_podcast_rss:abc",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "source_title": "Episode 213",
        "media_url": "https://example.com/audio.mp3",
        "transcript_status": "transcribed",
        "transcribed_at": "2026-06-02T00:00:00+00:00",
        "transcript": "Rock admins discuss check-in operations and staff training. " * 8,
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    insight = media_insight_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_insights_path(source.id), [insight])

    try:
        promote_media_public_candidates(
            source,
            candidate_ids=[candidate["id"]],
            review_status="approved_for_public_distillation",
            reviewer="test-reviewer",
            rewrites_by_candidate_id={
                candidate["id"]: {
                    "summary": "Speaker 1: This is copied transcript-shaped text.",
                    "key_insights": [
                        {
                            "topic": "governance",
                            "insight": "Public-safe guidance should be reviewed before release.",
                            "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                            "contains_verbatim_transcript": False,
                        }
                    ],
                }
            },
        )
    except ValueError as exc:
        assert "raw transcript text" in str(exc)
    else:
        raise AssertionError("raw transcript-like rewrite should be rejected")


def test_media_review_status_report_counts_source_and_concepts(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    monkeypatch.setattr(media_module, "NORMALIZED_DIR", tmp_path / "normalized")
    monkeypatch.setattr(
        "rock_kb.concepts.load_concepts",
        lambda: [
            SimpleNamespace(id="check-in", keywords=["check-in"], depends_on_topics=["mobile"]),
            SimpleNamespace(id="workflows", keywords=["workflow"], depends_on_topics=[]),
        ],
    )
    source = get_source("rock_podcast_rss")
    transcript_index_path = media_module.transcript_index_path(source.id)
    transcript_index_path.parent.mkdir(parents=True)
    write_jsonl(
        transcript_index_path,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_title": "Check-in training",
                "transcript_status": "transcribed",
                "transcript": "Rock check-in mobile training. " * 5,
            }
        ],
    )
    candidate = {
        "id": "media-public-candidate:abc",
        "source_title": "Check-in training",
        "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
        "topics": ["check-in", "mobile"],
        "concept_ids": ["check-in"],
    }
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(
        media_public_promotions_path(source.id),
        [
            {
                "candidate_id": "media-public-candidate:abc",
                "review_status": "approved_for_public_distillation",
                "concept_ids": ["check-in"],
            }
        ],
    )

    report = media_review_status_report([source])

    assert report["summary"]["transcribed_count"] == 1
    assert report["summary"]["candidate_count"] == 1
    assert report["summary"]["approved_promotion_count"] == 1
    check_in = next(row for row in report["concepts"] if row["concept_id"] == "check-in")
    assert check_in["candidate_count"] == 1
    assert check_in["approved_promotion_count"] == 1


def test_media_public_draft_rewrites_use_transcripts_without_media_urls(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    source = get_source("rock_podcast_rss")
    transcript = "Rock administrators need staff training for AI automation and governance. " * 8
    transcript_path = media_module.transcript_index_path(source.id)
    transcript_path.parent.mkdir(parents=True)
    write_jsonl(
        transcript_path,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_title": "AI Staff Training",
                "media_url": "https://sphinx.acast.com/p/open/media.mp3",
                "transcript_status": "transcribed",
                "transcribed_at": "2026-06-02T00:00:00+00:00",
                "transcript": transcript,
            }
        ],
    )
    candidate = media_public_candidate_records(
        source,
        [
            {
                "id": "media:abc:transcript",
                "media_id": "media:abc",
                "source_record_id": "rock_podcast_rss:abc",
                "source_url": "https://shows.acast.com/rock-cast/episodes/episode-213",
                "source_title": "AI Staff Training",
                "media_url": "https://sphinx.acast.com/p/open/media.mp3",
                "transcript_status": "transcribed",
                "transcribed_at": "2026-06-02T00:00:00+00:00",
                "transcript": transcript,
            }
        ],
    )[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])

    result = build_media_public_rewrite_drafts(source)
    rewrites = list(read_jsonl(media_public_rewrite_drafts_path(source.id)))
    serialized = json.dumps(rewrites)

    assert result["rewrite_rows"] == 1
    assert rewrites[0]["candidate_id"] == candidate["id"]
    assert not rewrites[0]["summary"].startswith("Private transcript-derived")
    assert "Review this" not in serialized
    assert "staff training" in serialized
    assert "https://shows.acast.com/rock-cast/episodes/episode-213" in serialized
    assert "media.mp3" not in serialized


def test_media_public_draft_rewrites_include_top_level_source_url(monkeypatch, tmp_path):
    monkeypatch.setattr(media_module, "REVIEW_DIR", tmp_path / "review")
    monkeypatch.setattr(media_module, "MEDIA_DIR", tmp_path / "media")
    source = get_source("rock_rocku")
    transcript_row = {
        "id": "media:abc:transcript",
        "media_id": "media:abc",
        "source_record_id": "rock_rocku:abc",
        "source_url": "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview",
        "source_title": "Mobile Check-In Overview",
        "media_url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret",
        "transcript_status": "transcribed",
        "transcript": "Rock check-in mobile operations and staff training guidance. " * 8,
        "transcript_segments": [{"start": 0, "text": "Rock check-in mobile operations."}],
    }
    candidate = media_public_candidate_records(source, [transcript_row])[0]
    write_jsonl(media_public_candidates_path(source.id), [candidate])
    write_jsonl(media_module.transcript_index_path(source.id), [transcript_row])

    build_media_public_rewrite_drafts(source)

    rewrite = list(read_jsonl(media_public_rewrite_drafts_path(source.id)))[0]
    assert rewrite["source_url"] == "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview"
    assert rewrite["citations"][0]["url"] == "https://community.rockrms.com/rocku/check-in/mobile-check-in-overview"


def test_summarize_transcript_insight_caps_text():
    text = " ".join(["This sentence explains Rock operations."] * 80)
    summary = summarize_transcript_insight(text, max_chars=180)
    assert len(summary) <= 180
    assert summary
    assert not summary.startswith("This sentence explains")
