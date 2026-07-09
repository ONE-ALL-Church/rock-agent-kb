from ._shared import *  # noqa: F401,F403


def discover_media(source: Source, limit: Optional[int] = None, include_empty: bool = False) -> list[dict[str, Any]]:
    if source.kind in {"podcast_rss", "rss"}:
        fetched = fetch_url(source.root_url)
        records = parse_rss(source, fetched["content"])
        return media_rows_from_normalized(source, records, include_empty=include_empty, limit=limit)

    normalized = list(read_jsonl(source_output_path(source.id, "normalized")))
    rows: list[dict[str, Any]] = []
    for record in normalized[: limit or None]:
        rows.extend(media_rows_for_page(source, record, include_empty=include_empty))
    return dedupe_media_rows(rows)

def media_rows_from_normalized(
    source: Source,
    records: Iterable[dict[str, Any]],
    include_empty: bool = False,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in list(records)[: limit or None]:
        media_url = record.get("media_url")
        if media_url:
            rows.append(
                build_media_row(
                    source=source,
                    source_record=record,
                    media_url=str(media_url),
                    media_kind=infer_media_kind(str(media_url), record.get("media_type")),
                    discovery_tool=str(record.get("extraction_tool") or "normalized_record"),
                    duration=record.get("duration"),
                )
            )
        elif include_empty:
            rows.append(build_empty_media_row(source, record, "no_media_url_in_record"))
    return dedupe_media_rows(rows)

def media_rows_for_page(source: Source, record: dict[str, Any], include_empty: bool = False) -> list[dict[str, Any]]:
    url = str(record.get("source_url") or "")
    if not url.startswith(("http://", "https://")):
        return []
    try:
        fetched = fetch_url(url)
    except Exception as exc:
        if include_empty:
            row = build_empty_media_row(source, record, "fetch_failed")
            row["error"] = str(exc)[:500]
            return [row]
        return []

    media_urls = extract_media_urls(fetched.get("content") or "", fetched.get("final_url") or url)
    if not media_urls and include_empty:
        return [build_empty_media_row(source, record, "no_media_url_found")]
    return [
        build_media_row(
            source=source,
            source_record=record,
            media_url=media_url,
            media_kind=infer_media_kind(media_url),
            discovery_tool="html_media_parser",
            duration=record.get("duration"),
        )
        for media_url in media_urls
    ]

def extract_media_urls(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    candidates: set[str] = set()
    for node in soup.find_all(["audio", "video", "source", "iframe", "embed"]):
        src = node.get("src")
        if src:
            absolute = canonicalize_url(urljoin(base_url, str(src)))
            if is_media_url(absolute):
                candidates.add(absolute)
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        absolute = canonicalize_url(urljoin(base_url, href))
        if is_media_url(absolute):
            candidates.add(absolute)
    for match in URL_RE.finditer(html):
        value = canonicalize_url(match.group(0).rstrip(".,;"))
        if is_media_url(value):
            candidates.add(value)
    return sorted(candidates)

def is_media_url(url: str) -> bool:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in AUDIO_EXTENSIONS | VIDEO_EXTENSIONS | STREAMING_EXTENSIONS:
        return True
    host = parsed.netloc.lower()
    return any(hint in host for hint in MEDIA_HOST_HINTS)

def infer_media_kind(url: str, media_type: Optional[str] = None) -> str:
    value = (media_type or "").lower()
    suffix = Path(urlparse(url).path).suffix.lower()
    if value.startswith("audio/") or suffix in AUDIO_EXTENSIONS:
        return "audio"
    if value.startswith("video/") or suffix in VIDEO_EXTENSIONS | STREAMING_EXTENSIONS:
        return "video"
    if "youtube" in url or "vimeo" in url or "wistia" in url:
        return "video"
    return "unknown"

def build_media_row(
    source: Source,
    source_record: dict[str, Any],
    media_url: str,
    media_kind: str,
    discovery_tool: str,
    duration: Any = None,
) -> dict[str, Any]:
    source_record_id = str(source_record.get("id") or "")
    row_id = "media:" + sha256_text(f"{source.id}:{source_record_id}:{media_url}")[:16]
    return {
        "id": row_id,
        "source_id": source.id,
        "source_record_id": source_record_id,
        "source_url": source_record.get("source_url") or source.root_url,
        "source_title": source_record.get("source_title") or source.name,
        "media_url": media_url,
        "media_kind": media_kind,
        "duration": duration,
        "discovered_at": now_iso(),
        "discovery_tool": discovery_tool,
        "transcript_status": "pending",
        "transcript_path": None,
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_transcript_only",
        "citations": source_record.get("citations") or [{"source_id": source.id, "url": source_record.get("source_url") or source.root_url}],
    }

def build_empty_media_row(source: Source, source_record: dict[str, Any], status: str) -> dict[str, Any]:
    source_record_id = str(source_record.get("id") or "")
    return {
        "id": "media-empty:" + sha256_text(f"{source.id}:{source_record_id}:{status}")[:16],
        "source_id": source.id,
        "source_record_id": source_record_id,
        "source_url": source_record.get("source_url") or source.root_url,
        "source_title": source_record.get("source_title") or source.name,
        "media_url": None,
        "media_kind": None,
        "duration": source_record.get("duration"),
        "discovered_at": now_iso(),
        "discovery_tool": "media_discovery",
        "transcript_status": status,
        "transcript_path": None,
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_transcript_only",
        "citations": source_record.get("citations") or [{"source_id": source.id, "url": source_record.get("source_url") or source.root_url}],
    }

def dedupe_media_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {}
    for row in rows:
        key = (row.get("source_record_id"), row.get("media_url"), row.get("transcript_status"))
        by_key[key] = row
    return list(by_key.values())
