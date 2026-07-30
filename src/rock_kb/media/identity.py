from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Iterable
from urllib.parse import parse_qs, urlparse

from ..extract import sha256_text


ROCKCAST_SOURCE_IDS = {"rock_podcast_rss", "rock_youtube"}
EPISODE_PATTERN = re.compile(r"\bep(?:isode)?\.?\s*#?\s*(\d{1,6})\b", re.IGNORECASE)


def infer_source_work_id(
    *,
    source_id: str,
    source_title: str = "",
    source_record_id: str = "",
    source_url: str = "",
    media_url: str = "",
    episode_number: Any = None,
    existing: str | None = None,
) -> str:
    """Return a conservative identity for the underlying work, not its locator."""

    if existing and str(existing).strip():
        return str(existing).strip()

    episode = normalized_episode_number(episode_number) or episode_number_from_title(source_title)
    if source_id in ROCKCAST_SOURCE_IDS and episode is not None:
        return f"media-work:rockcast:episode:{episode}"

    youtube_id = youtube_video_id(source_url) or youtube_video_id(media_url)
    if youtube_id:
        return f"media-work:youtube:{youtube_id}"

    identity_seed = source_record_id or source_url or media_url or source_title
    digest = sha256_text(f"{source_id}:{identity_seed}")[:20]
    return f"media-work:{safe_identity_part(source_id)}:{digest}"


def episode_number_from_title(title: str) -> str | None:
    match = EPISODE_PATTERN.search(str(title or ""))
    return normalized_episode_number(match.group(1)) if match else None


def normalized_episode_number(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text or not text.isdigit():
        return None
    return str(int(text))


def youtube_video_id(url: str) -> str | None:
    if not url:
        return None
    parsed = urlparse(str(url))
    host = parsed.netloc.lower()
    if host in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.strip("/").split("/", 1)[0]
        return safe_external_id(candidate)
    if "youtube.com" not in host:
        return None
    if parsed.path.startswith("/watch"):
        candidate = (parse_qs(parsed.query).get("v") or [""])[0]
        return safe_external_id(candidate)
    if parsed.path.startswith(("/shorts/", "/embed/")):
        candidate = parsed.path.strip("/").split("/", 1)[1]
        return safe_external_id(candidate)
    return None


def annotate_media_mirrors(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    annotated = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in rows:
        row = dict(raw)
        row["source_work_id"] = infer_source_work_id(
            source_id=str(row.get("source_id") or "unknown"),
            source_title=str(row.get("source_title") or ""),
            source_record_id=str(row.get("source_record_id") or ""),
            source_url=str(row.get("source_url") or ""),
            media_url=str(row.get("media_url") or ""),
            episode_number=row.get("episode_number"),
            existing=str(row.get("source_work_id") or "") or None,
        )
        annotated.append(row)
        groups[row["source_work_id"]].append(row)

    for row in annotated:
        peers = [
            peer
            for peer in groups[row["source_work_id"]]
            if str(peer.get("media_id") or peer.get("id") or "") != str(row.get("media_id") or row.get("id") or "")
        ]
        row["mirror_media_ids"] = sorted(
            {
                str(peer.get("media_id") or peer.get("id") or "")
                for peer in peers
                if peer.get("media_id") or peer.get("id")
            }
        )
        row["mirror_source_ids"] = sorted({str(peer.get("source_id") or "") for peer in peers if peer.get("source_id")})
        row["mirror_count"] = len(row["mirror_media_ids"])
        row["is_source_mirror"] = bool(row["mirror_media_ids"])
    return annotated


def safe_external_id(value: str) -> str | None:
    candidate = str(value or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,80}", candidate):
        return None
    return candidate


def safe_identity_part(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", str(value or "").lower()).strip("-") or "unknown"
