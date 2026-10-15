"""Bounded anonymous ingestion of official Forge release notes."""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from datetime import date
from typing import Annotated, Any, Literal
from urllib.parse import parse_qs, urlencode, urlsplit
from uuid import UUID

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .extract import USER_AGENT, now_iso, sha256_text
from .normalize import canonical_record_id, infer_audience, infer_severity, parse_release_notes, summarize_locally
from .sources import Source

ORIGIN = "https://www.rockrms.com"
API_PREFIX = "/api/v2/lava-app/1/"  # 1 is the route version, not a SiteId.
SOURCE_ROUTES = {
    "rock_core_release_notes": ("rock_release_notes", "/releasenotes", "release-notes-forge-test"),
    "rock_mobile_release_notes": ("rock_mobile_release_notes", "/mobilereleasenotes", "mobile-release-notes"),
}
MAX_VERSIONS = 256
MAX_NOTES = 5000
MAX_RECORDS = 50000
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_FETCH_SECONDS = 600
VERSION_PATTERN = r"[0-9]+(?:\.[0-9]+){1,3}"
Version = Annotated[str, Field(pattern=rf"^{VERSION_PATTERN}$", max_length=32)]
Count = Annotated[int, Field(ge=0, le=MAX_NOTES)]
CHANGE_TYPES = {"added": "new_feature", "improved": "improvement", "fixed": "bug_fix", "security": "security"}
# v2 introduced semantic hashes; v3 separates API versions from product display.
PARSER_VERSION = "release-lava-app-v3"


class ReleaseNotesError(ValueError):
    """A complete public release-note snapshot could not be validated."""


class _Model(BaseModel):
    model_config = ConfigDict(strict=True)


class _Note(_Model):
    noteGuid: str
    type: Literal["added", "improved", "fixed", "security"]
    category: Annotated[str, Field(min_length=1, max_length=200)]
    categoryOrder: int
    html: Annotated[str, Field(min_length=1, max_length=200000)]
    issues: list[Annotated[str, Field(pattern=r"^[1-9][0-9]*$", max_length=12)]]

    @field_validator("noteGuid")
    @classmethod
    def valid_guid(cls, value: str) -> str:
        if str(UUID(value)) != value.lower():
            raise ValueError("Invalid note GUID")
        return value


class _Release(_Model):
    version: Version
    releaseDate: str

    @field_validator("releaseDate")
    @classmethod
    def valid_date(cls, value: str) -> str:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError("Invalid release date")
        return value


class _Summary(_Release):
    status: str
    isAlpha: bool
    isBeta: bool
    isEarlyAccess: bool
    isProduction: bool
    isLatestSecured: bool
    total: Count
    added: Count
    improved: Count
    fixed: Count
    security: Count


class _CoreOverview(_Model):
    versionCount: Annotated[int, Field(ge=1, le=MAX_VERSIONS)]
    versions: Annotated[list[_Summary], Field(min_length=1, max_length=MAX_VERSIONS)]


class _CoreRelease(_Release):
    isFound: bool
    status: str
    notes: Annotated[list[_Note], Field(min_length=1, max_length=MAX_NOTES)]
    headsUpHtml: str
    introHtml: str


class _MobileRelease(_Release):
    display: Version
    minimumOs: Annotated[str, Field(min_length=1, max_length=1000)]
    minimumRock: Version
    introHtml: str
    notes: Annotated[list[_Note], Field(min_length=1, max_length=MAX_NOTES)]


class _MobileReleases(_Model):
    versionCount: Annotated[int, Field(ge=1, le=MAX_VERSIONS)]
    versions: Annotated[list[_MobileRelease], Field(min_length=1, max_length=MAX_VERSIONS)]


def _source_route(source: Source) -> tuple[str, str, str]:
    route = SOURCE_ROUTES.get(source.id)
    if route is None or source.kind != route[0] or source.root_url != ORIGIN + route[1]:
        raise ReleaseNotesError("Release source is outside the public allowlist")
    return route


def _validate_url(url: str, source: Source) -> None:
    _, page, app = _source_route(source)
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "www.rockrms.com" or parsed.fragment:
        raise ReleaseNotesError("Release URL is outside the public allowlist")
    if parsed.path == page and not parsed.query:
        return
    base = API_PREFIX + app
    if app == "mobile-release-notes" and parsed.path == base + "/releases" and not parsed.query:
        return
    if app == "release-notes-forge-test":
        if parsed.path == base + "/overview" and not parsed.query:
            return
        query = parse_qs(parsed.query, keep_blank_values=True)
        if parsed.path == base + "/version" and set(query) == {"version"}:
            versions = query["version"]
            if len(versions) == 1 and re.fullmatch(VERSION_PATTERN, versions[0]):
                return
    raise ReleaseNotesError("Release URL is outside the public allowlist")


def discover_release_app(source: Source, html: str) -> str | None:
    """Read JSON block configuration and literal calls, never execute JavaScript."""
    _, _, default = _source_route(source)
    apps: set[str] = set()
    decoder = json.JSONDecoder()
    for script in BeautifulSoup(html, "html.parser").find_all("script"):
        text = script.get_text()
        for match in re.finditer(r"\binitializeBlock\s*\(\s*", text):
            try:
                block, _ = decoder.raw_decode(text[match.end():])
            except ValueError:
                if "forgeContentDetail.obs" in text:
                    raise ReleaseNotesError("Malformed Forge block configuration") from None
                continue
            if not isinstance(block, dict) or block.get("blockFileUrl") != "/Obsidian/Blocks/Cms/forgeContentDetail.obs":
                continue
            config = block.get("configurationValues")
            compiled = config.get("compiledContent") if isinstance(config, dict) else None
            if not isinstance(compiled, str) or not compiled.strip():
                raise ReleaseNotesError("Missing Forge compiled content")
            calls = re.findall(r"\buseLavaApp\s*\(([^)]*)\)", compiled)
            if not calls:
                apps.add(default)
            for call in calls:
                literal = re.fullmatch(r"\s*(['\"])([a-z0-9-]+)\1\s*", call)
                if literal is None or literal.group(2) != default:
                    raise ReleaseNotesError("Unrecognized release LavaApp")
                apps.add(literal.group(2))
    return next(iter(apps)) if apps else None


class _PublicFetcher:
    def __init__(self, client: httpx.Client, source: Source):
        self.client = client
        self.source = source
        self.deadline = time.monotonic() + MAX_FETCH_SECONDS
        self.total_bytes = 0
        self.requests = 0

    def get(self, url: str, *, json_response: bool = True) -> str:
        _validate_url(url, self.source)
        remaining = self.deadline - time.monotonic()
        self.requests += 1
        if remaining <= 0 or self.requests > MAX_VERSIONS + 2:
            raise ReleaseNotesError("Release fetch exceeded its request or time bound")
        self.client.cookies.clear()
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json" if json_response else "text/html",
            "X-Helix-CSRF-Protection": "true",
        }
        try:
            with self.client.stream("GET", url, headers=headers, timeout=min(30.0, remaining)) as response:
                if response.status_code != 200:
                    raise ReleaseNotesError(f"Release fetch failed with HTTP {response.status_code}")
                expected = "application/json" if json_response else "text/html"
                if response.headers.get("content-type", "").split(";", 1)[0].strip().lower() != expected:
                    raise ReleaseNotesError("Unexpected release response content type")
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    self.total_bytes += len(chunk)
                    if len(body) > MAX_RESPONSE_BYTES or self.total_bytes > MAX_TOTAL_BYTES:
                        raise ReleaseNotesError("Release response exceeded its byte bound")
                    if time.monotonic() > self.deadline:
                        raise ReleaseNotesError("Release fetch exceeded its time bound")
                return body.decode("utf-8")
        except (httpx.HTTPError, UnicodeError):
            raise ReleaseNotesError("Public release fetch failed") from None

    def model(self, url: str, model: type[_Model]) -> tuple[Any, str]:
        text = self.get(url)
        try:
            return model.model_validate(json.loads(text)), sha256_text(text)
        except (ValueError, ValidationError):
            raise ReleaseNotesError(f"Malformed {model.__name__.lstrip('_')} response") from None


def _validate_versions(payload: _CoreOverview | _MobileReleases) -> None:
    versions = [row.version for row in payload.versions]
    if payload.versionCount != len(versions) or len(set(versions)) != len(versions):
        raise ReleaseNotesError("Incomplete or duplicate release version list")


def _plain_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup.find_all(["script", "style", "noscript"]):
        node.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


def _minimum_os(value: str) -> dict[str, str]:
    match = re.fullmatch(r"iOS version:?\s*([^,]+),\s*Android version:?\s*(.+)", value)
    if match is None:
        raise ReleaseNotesError("Unrecognized per-release mobile OS requirements")
    return {"ios": match.group(1).strip(), "android": match.group(2).strip()}


def release_version_metadata(row: dict[str, Any]) -> dict[str, str]:
    upstream = str(row.get("upstream_version") or row.get("version") or "")
    display = upstream
    if row.get("release_family") == "core":
        # Exact displayVersion() mapping in the official Forge frontend.
        match = re.fullmatch(r"1\.(16\.\d+)", upstream)
        if match:
            display = match.group(1)
    elif row.get("release_family") == "mobile":
        # The mobile frontend renders the API display field, not a prefix rule.
        display = str(row.get("release_display") or row.get("product_version") or upstream)
    return {"upstream_version": upstream, "product_version": display, "release_display": display}


def upgrade_cached_release_record(row: dict[str, Any]) -> dict[str, Any]:
    """Update derived version metadata without fetching or changing record IDs."""
    upgraded = {**row, **release_version_metadata(row)}
    if row.get("extraction_tool") == "release_lava_app_api":
        mobile = row["release_family"] == "mobile"
        upgraded["api_provenance"] = {
            **row["api_provenance"], "parser_version": PARSER_VERSION,
            "version_mapping": "mobile-api-display" if mobile else "core-frontend-displayVersion-rock16",
            "version_mapping_url": ORIGIN + ("/mobilereleasenotes" if mobile else "/releasenotes"),
        }
        upgraded["content_hash"] = _semantic_content_hash(upgraded)
    return upgraded


def _semantic_content_hash(row: dict[str, Any]) -> str:
    """Hash meaning, not retrieval time, GUID aliases, or transport payloads."""
    fields = (
        "excerpt", "release_family", "version", "release_display", "release_date",
        "release_status", "release_flags", "module", "category_order",
        "change_type", "upstream_change_type", "severity", "minimum_os", "minimum_rock_version",
    )
    payload = {key: row[key] for key in fields}
    payload["hash_contract"] = "release-note-content-v2"
    for key in ("issue_refs", "bulletin_refs"):
        payload[key] = sorted(set(row[key]))
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _release_records(
    source: Source,
    release: _CoreRelease | _MobileRelease,
    provenance: dict[str, Any],
    summary: _Summary | None = None,
) -> list[dict[str, Any]]:
    mobile = isinstance(release, _MobileRelease)
    family = "mobile" if mobile else "core"
    minimum_os = _minimum_os(release.minimumOs) if mobile else None
    seen_guids: set[str] = set()
    rows = []
    for note in release.notes:
        guid = note.noteGuid.lower()
        if guid in seen_guids:
            raise ReleaseNotesError("Duplicate release note GUID")
        seen_guids.add(guid)
        change = _plain_text(note.html)
        if not change or not note.category.strip():
            raise ReleaseNotesError("Empty release note or category")
        rows.append({
            "id": canonical_record_id(source.id, f"{release.version}:{note.category}:{change}"),
            "source_id": source.id,
            "source_url": source.root_url,
            "source_title": source.name,
            "source_kind": source.kind,
            "retrieved_at": now_iso(),
            "updated_at": None,
            "license_status": source.license_status,
            "allowed_extraction_mode": source.allowed_extraction_mode,
            "extraction_tool": "release_lava_app_api",
            "extraction_mode": source.allowed_extraction_mode,
            "summary_model": None,
            "topics": source.topics,
            "rock_version_min": None,
            "rock_version_max": None,
            "rock_versions": [release.version],
            "audience": infer_audience(source),
            "summary": summarize_locally(change),
            "excerpt": change,
            "canonical_path": f"knowledge/releases/{family}-v{release.version}.md",
            "citations": [{"source_id": source.id, "url": source.root_url}],
            "release_family": family,
            "version": release.version,
            "release_date": release.releaseDate,
            "release_status": release.status if not mobile else None,
            "module": note.category,
            "change_type": CHANGE_TYPES[note.type],
            "upstream_change_type": note.type,
            "severity": "high" if note.type == "security" else infer_severity(change),
            "minimum_os": minimum_os,
            "minimum_rock_version": release.minimumRock if mobile else None,
            "issue_refs": list(dict.fromkeys(note.issues)),
            "bulletin_refs": [],
            "needs_review": False,
            "note_guid": note.noteGuid,
            "upstream_note_guids": [note.noteGuid],
            "category_order": note.categoryOrder,
            "release_display": release.display if mobile else release.version,
            "release_flags": {
                key: getattr(summary, key)
                for key in ("isAlpha", "isBeta", "isEarlyAccess", "isProduction", "isLatestSecured")
            } if summary else {},
            "api_provenance": provenance,
        })
        rows[-1] = upgrade_cached_release_record(rows[-1])
    return rows


def _merge_identical_notes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    # Old releases can repeat identical notes under separate upstream GUIDs.
    merged_fields = {"note_guid", "upstream_note_guids", "issue_refs", "retrieved_at", "content_hash"}
    for row in records:
        existing = by_id.get(row["id"])
        if existing is None:
            by_id[row["id"]] = row
            continue
        if any(existing[key] != value for key, value in row.items() if key not in merged_fields):
            raise ReleaseNotesError(f"Conflicting release identity in version {row['version']}")
        existing["upstream_note_guids"].extend(row["upstream_note_guids"])
        existing["issue_refs"] = list(dict.fromkeys([*existing["issue_refs"], *row["issue_refs"]]))
        existing["content_hash"] = _semantic_content_hash(existing)
    return list(by_id.values())


def fetch_release_note_records(
    source: Source, *, transport: httpx.BaseTransport | None = None,
) -> list[dict[str, Any]]:
    """Return a fully validated snapshot; callers must not write on failure."""
    _source_route(source)
    with httpx.Client(transport=transport, follow_redirects=False, trust_env=False, auth=None) as client:
        fetcher = _PublicFetcher(client, source)
        html = fetcher.get(source.root_url, json_response=False)
        app = discover_release_app(source, html)
        if app is None:
            records = parse_release_notes(source, html)
            if not records:
                raise ReleaseNotesError("No static release notes or recognized Forge app")
            return records
        base = ORIGIN + API_PREFIX + app
        overview_url = base + ("/releases" if source.kind == "rock_mobile_release_notes" else "/overview")
        model = _MobileReleases if source.kind == "rock_mobile_release_notes" else _CoreOverview
        overview, overview_hash = fetcher.model(overview_url, model)
        _validate_versions(overview)
        records = []
        for version in overview.versions:
            detail_url = overview_url
            detail_hash = overview_hash
            summary = None
            if isinstance(version, _Summary):
                summary = version
                expected = {key: getattr(version, key) for key in CHANGE_TYPES}
                if version.total < 1 or version.total != sum(expected.values()):
                    raise ReleaseNotesError("Invalid core release overview note counts")
                detail_url = base + "/version?" + urlencode({"version": version.version})
                release, detail_hash = fetcher.model(detail_url, _CoreRelease)
                if not release.isFound or any(
                    getattr(release, key) != getattr(version, key) for key in ("version", "releaseDate", "status")
                ):
                    raise ReleaseNotesError("Core release detail does not match the overview")
                counts = Counter(note.type for note in release.notes)
                if len(release.notes) != version.total or any(counts[key] != count for key, count in expected.items()):
                    raise ReleaseNotesError("Incomplete core release detail note counts")
            else:
                release = version
            records.extend(_release_records(source, release, {
                "app_slug": app,
                "route_version": 1,
                "url": detail_url,
                "overview_url": overview_url,
                "payload_sha256": detail_hash,
                "overview_sha256": overview_hash,
                "version_count": overview.versionCount,
                "release_note_count": len(release.notes),
                "parser_version": PARSER_VERSION,
            }, summary))
            if len(records) > MAX_RECORDS:
                raise ReleaseNotesError("Release snapshot exceeded its record bound")
        if not records:
            raise ReleaseNotesError("Empty release snapshot")
        return _merge_identical_notes(records)
