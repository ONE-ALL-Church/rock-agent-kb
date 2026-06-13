from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import parse_qsl, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from ..extract import USER_AGENT, canonicalize_url, fetch_url, generated_at_iso, now_iso, optional_command, sha256_text
from ..jsonl import read_jsonl, write_jsonl
from ..normalize import parse_rss
from ..paths import MEDIA_DIR, NORMALIZED_DIR, REVIEW_DIR, source_output_path
from ..sources import Source

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}
STREAMING_EXTENSIONS = {".m3u8", ".mpd"}
MEDIA_HOST_HINTS = {
    "acast.com",
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "wistia.com",
    "wistia.net",
}
URL_RE = re.compile(r"https?://[^'\"\s<>\\)]+")
OPENAI_TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"
CLOUDFLARE_TRANSCRIBE_MODEL = "@cf/openai/whisper-large-v3-turbo"
MLX_WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
MLX_WHISPER_SMOKE_MODEL = "mlx-community/whisper-tiny"
PARAKEET_MODEL = "nvidia/parakeet-tdt-0.6b-v3"
SYNCABLE_TRANSCRIPT_STATUSES = {"transcribed", "failed"}
TRANSCRIPT_SIGNAL_PATTERNS = {
    "AI and automation": ["ai", "agent", "automation", "model", "prompt"],
    "staff training": ["training", "trained", "onboarding", "staff", "team"],
    "Rock operations": ["rock", "admin", "workflow", "check-in", "communication", "giving"],
    "release and roadmap awareness": ["release", "version", "roadmap", "update", "upgrade"],
    "data and reporting": ["data", "report", "dashboard", "analytics", "sql"],
    "risk and governance": ["security", "permission", "risk", "policy", "privacy", "access"],
    "ministry process": ["ministry", "church", "congregation", "connection", "volunteer"],
}
MEDIA_PRIORITY_TERMS = {
    "ai-agent-readiness": ["ai", "agent", "automation", "prompt", "model"],
    "release-risk": ["release", "upgrade", "version", "v16", "v17", "v18", "breaking"],
    "core-operations": ["workflow", "check-in", "communication", "group", "giving", "registration"],
    "developer-implementation": ["api", "lava", "sql", "integration", "mobile", "plugin"],
    "governance-risk": ["security", "permission", "privacy", "access", "token"],
    "reporting-data": ["report", "analytics", "dashboard", "business intelligence", "bi"],
}
MEDIA_SOURCE_PRIORITY = {
    "rock_rocku": 96,
    "rock_podcast_rss": 88,
    "rock_community_hubs": 84,
}
MEDIA_KIND_PRIORITY = {
    "audio": 8,
    "video": 4,
}
PUBLIC_MEDIA_REVIEW_STATUSES = {"redaction_reviewed", "approved_for_public_distillation", "public_reviewed"}
PUBLIC_MEDIA_PLACEHOLDER_SUMMARY_PREFIX = "Private transcript-derived insight:"
PUBLIC_MEDIA_PLACEHOLDER_INSIGHT_PREFIX = "Review this"
TOKENIZED_QUERY_HINTS = {"access_token", "expires", "key", "oauth", "oauth2_token_id", "policy", "signature", "sig", "token"}
DISALLOWED_PUBLIC_MEDIA_HOSTS = {"player.vimeo.com"}
GEMMA4_BENCHMARK_TOOL = "gemma4-12b"
GEMMA4_OLLAMA_MODEL = "gemma4:12b"
MEDIA_UNDERSTANDING_WORK_DIR = Path("data/tmp/gemma-benchmark")
MEDIA_UNDERSTANDING_CLIP_MANIFEST = MEDIA_UNDERSTANDING_WORK_DIR / "clip-manifest.json"
MEDIA_UNDERSTANDING_OLLAMA_RESULT = REVIEW_DIR / "media-understanding-benchmarks" / "gemma4-12b-ollama-run.json"
MEDIA_UNDERSTANDING_AUDIO_BITRATE = "64k"
MEDIA_UNDERSTANDING_BENCHMARK_ROLES = {
    "podcast_audio": ["asr_accuracy", "topic_extraction", "speaker_or_host_context", "timestamp_routing"],
    "rock_training_video": ["asr_accuracy", "visual_context", "chaptering", "ui_or_screen_summary", "timestamp_routing"],
    "community_video": ["asr_accuracy", "visual_context", "operational_topic_extraction", "timestamp_routing"],
    "triumph_technical_video": ["asr_accuracy", "visual_context", "technical_change_summary", "risk_or_upgrade_signals"],
}

def media_manifest_path(source_id: str) -> Path:
    return MEDIA_DIR / f"{source_id}.media.jsonl"

def transcript_index_path(source_id: str) -> Path:
    return MEDIA_DIR / f"{source_id}.transcripts.jsonl"

def media_insights_path(source_id: str) -> Path:
    return NORMALIZED_DIR / f"{source_id}.media-insights.jsonl"

def media_public_candidates_path(source_id: str) -> Path:
    return REVIEW_DIR / "public-summary-candidates" / f"{source_id}.media-public-candidates.jsonl"

def media_public_promotions_path(source_id: str) -> Path:
    return REVIEW_DIR / "public-media-promotions" / f"{source_id}.media-public-promotions.jsonl"

def media_public_rewrite_drafts_path(source_id: str) -> Path:
    return REVIEW_DIR / "media-rewrites" / f"{source_id}.transcript-reviewed-rewrites.jsonl"

def media_sidecar_dir(source_id: str) -> Path:
    return MEDIA_DIR / "sidecars" / source_id

def media_sidecar_path(source_id: str, media_id: str) -> Path:
    return media_sidecar_dir(source_id) / f"{safe_media_filename(media_id)}.media.md"

def media_source_index_path(source_id: str) -> Path:
    return MEDIA_DIR / "index" / f"{source_id}.media-index.jsonl"

def media_global_index_path() -> Path:
    return MEDIA_DIR / "index" / "media-index.jsonl"

def media_priority_queue_path() -> Path:
    return MEDIA_DIR / "index" / "transcription-priority-queue.jsonl"

def media_priority_report_path() -> Path:
    return MEDIA_DIR / "index" / "transcription-priority-report.json"

def media_understanding_benchmark_path(tool: str = GEMMA4_BENCHMARK_TOOL) -> Path:
    safe_tool = re.sub(r"[^a-z0-9_.-]+", "-", tool.strip().lower()).strip("-") or "media-understanding"
    return REVIEW_DIR / "media-understanding-benchmarks" / f"{safe_tool}.json"

def media_understanding_ollama_result_path() -> Path:
    return MEDIA_UNDERSTANDING_OLLAMA_RESULT

def count_values(values: Iterable[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value if value is not None else "none")
        counts[key] = counts.get(key, 0) + 1
    return counts

def safe_media_filename(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return safe[:140] or "media"

def numeric_seconds(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            parts = stripped.split(":")
            if not all(part.replace(".", "", 1).isdigit() for part in parts):
                return None
            total = 0.0
            for part in parts:
                total = total * 60 + float(part)
            return total
    return None

def format_timestamp(seconds: Any) -> str:
    value = numeric_seconds(seconds)
    if value is None:
        return "00:00"
    whole_seconds = max(0, int(value))
    hours = whole_seconds // 3600
    minutes = (whole_seconds % 3600) // 60
    secs = whole_seconds % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"
