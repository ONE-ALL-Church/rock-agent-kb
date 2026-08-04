from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import httpx
from bs4 import BeautifulSoup

from .community import fetch_rockumentation_payload
from .extract import USER_AGENT, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .schemas import (
    SourceNativeVerificationQueueItem,
    SourceNativeVerificationResolution,
    SourceSnapshot,
)


VERIFICATION_RESOLUTIONS_NAME = "verification-resolutions.jsonl"
VERIFICATION_REPORT_NAME = "verification-report.json"


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def source_native_verification_queue_hash(
    row: SourceNativeVerificationQueueItem | dict[str, Any],
) -> str:
    payload = (
        row.public_dump()
        if isinstance(row, SourceNativeVerificationQueueItem)
        else SourceNativeVerificationQueueItem.model_validate(row).public_dump()
    )
    return sha256_text(canonical_json(payload))


def index_source_native_verification_queue(
    rows: Iterable[dict[str, Any]],
    *,
    source: str,
) -> dict[str, SourceNativeVerificationQueueItem]:
    queue: dict[str, SourceNativeVerificationQueueItem] = {}
    for line_number, raw in enumerate(rows, start=1):
        item = SourceNativeVerificationQueueItem.model_validate(raw)
        if item.verification_id in queue:
            raise ValueError(
                f"{source}:{line_number} duplicates {item.verification_id}"
            )
        queue[item.verification_id] = item
    return queue


def build_source_native_verification_packet(
    *,
    queue_path: Path,
    destination: Path,
) -> dict[str, Any]:
    rows = []
    queue = index_source_native_verification_queue(
        read_jsonl(queue_path),
        source=str(queue_path),
    )
    for queue_item in queue.values():
        rows.append(
            {
                **queue_item.public_dump(),
                "queue_item_hash": source_native_verification_queue_hash(
                    queue_item
                ),
                "resolution_schema": (
                    "rock-kb-source-native-verification-resolution-v1"
                ),
            }
        )
    write_jsonl(destination, rows)
    return {
        "schema": "rock-kb-source-native-verification-packet-v1",
        "status": "ok",
        "queue_count": len(rows),
        "destination": str(destination),
    }


def promote_source_native_verification_resolutions(
    *,
    queue_path: Path,
    input_path: Path,
    destination: Path,
    reviewer: str,
    reviewed_at: str | None = None,
    source_snapshots_path: Path | None = None,
) -> dict[str, Any]:
    queue = index_source_native_verification_queue(
        read_jsonl(queue_path),
        source=str(queue_path),
    )
    if not queue:
        raise ValueError(f"no verification queue rows found at {queue_path}")
    resolved_at = reviewed_at or now_iso()
    incoming: list[SourceNativeVerificationResolution] = []
    incoming_ids: set[str] = set()
    for line_number, raw in enumerate(read_jsonl(input_path), start=1):
        payload = {
            **raw,
            "reviewer": reviewer,
            "reviewed_at": resolved_at,
        }
        resolution = SourceNativeVerificationResolution.model_validate(payload)
        if resolution.verification_id in incoming_ids:
            raise ValueError(
                f"{input_path}:{line_number} duplicates "
                f"{resolution.verification_id}"
            )
        queue_item = queue.get(resolution.verification_id)
        if queue_item is None:
            raise ValueError(
                f"{input_path}:{line_number} references an unknown verification"
            )
        expected_hash = source_native_verification_queue_hash(queue_item)
        if resolution.queue_item_hash != expected_hash:
            raise ValueError(
                f"{input_path}:{line_number} queue_item_hash is stale"
            )
        incoming.append(resolution)
        incoming_ids.add(resolution.verification_id)

    resolution_path = destination / VERIFICATION_RESOLUTIONS_NAME
    existing = [
        SourceNativeVerificationResolution.model_validate(row)
        for row in read_jsonl(resolution_path)
        if str(row.get("verification_id") or "") not in incoming_ids
        and str(row.get("verification_id") or "") in queue
    ]
    rows = sorted(
        [*existing, *incoming],
        key=lambda row: row.verification_id,
    )
    write_jsonl(resolution_path, [row.public_dump() for row in rows])
    report = audit_source_native_verifications(
        queue_path=queue_path,
        resolution_path=resolution_path,
        source_snapshots_path=source_snapshots_path,
    )
    report_path = destination / VERIFICATION_REPORT_NAME
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-verification-promotion-v1",
        "status": "ok",
        "resolution_count": len(rows),
        "incoming_count": len(incoming),
        "destination": str(resolution_path),
        "report": report,
    }


def audit_source_native_verifications(
    *,
    queue_path: Path,
    resolution_path: Path,
    source_snapshots_path: Path | None = None,
    check_live: bool = False,
    checked_at: str | None = None,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    queue = index_source_native_verification_queue(
        read_jsonl(queue_path),
        source=str(queue_path),
    )
    resolutions: dict[str, SourceNativeVerificationResolution] = {}
    for raw in read_jsonl(resolution_path):
        resolution = SourceNativeVerificationResolution.model_validate(raw)
        if resolution.verification_id in resolutions:
            raise ValueError(
                "verification resolutions must be unique by verification_id"
            )
        if resolution.verification_id not in queue:
            raise ValueError(
                "verification resolution references an unknown queue item: "
                f"{resolution.verification_id}"
            )
        resolutions[resolution.verification_id] = resolution

    snapshots = {
        snapshot.source_snapshot_id: snapshot
        for snapshot in (
            SourceSnapshot.model_validate(row)
            for row in read_jsonl(source_snapshots_path)
        )
    } if source_snapshots_path else {}
    effective_checked_at = checked_at or now_iso()
    now = parse_iso(effective_checked_at)
    live_cache: dict[tuple[str, str], tuple[str | None, str | None]] = {}
    statuses: list[dict[str, Any]] = []
    owns_client = check_live and client is None
    resolved_client = client
    if owns_client:
        resolved_client = httpx.Client(
            follow_redirects=True,
            timeout=30,
            headers={"User-Agent": USER_AGENT},
        )
    try:
        for verification_id, queue_item in sorted(queue.items()):
            resolution = resolutions.get(verification_id)
            status = "unresolved"
            stale_reasons: list[str] = []
            if resolution is not None:
                expected_hash = source_native_verification_queue_hash(queue_item)
                if resolution.queue_item_hash != expected_hash:
                    stale_reasons.append("queue_item_changed")
                if (
                    resolution.revalidate_after
                    and parse_iso(resolution.revalidate_after) <= now
                ):
                    stale_reasons.append("revalidation_due")
                for evidence in resolution.evidence:
                    if evidence.evidence_type == "source_snapshot":
                        snapshot = snapshots.get(evidence.source_ref)
                        if snapshot is None:
                            stale_reasons.append("source_snapshot_missing")
                        elif evidence.content_hash not in {
                            snapshot.content_hash,
                            snapshot.normalized_content_hash,
                        }:
                            stale_reasons.append("source_snapshot_changed")
                    if check_live and evidence.revalidation_url:
                        cache_key = (
                            evidence.revalidation_url,
                            evidence.hash_mode,
                        )
                        if cache_key not in live_cache:
                            try:
                                live_hash = hash_live_evidence_with_timeout_retry(
                                    resolved_client,
                                    evidence.revalidation_url,
                                    evidence.hash_mode,
                                )
                                live_cache[cache_key] = (live_hash, None)
                            except Exception as exc:  # pragma: no cover - network diagnostic
                                live_cache[cache_key] = (None, str(exc))
                        live_hash, live_error = live_cache[cache_key]
                        if live_error:
                            stale_reasons.append("live_check_failed")
                        elif live_hash != evidence.content_hash:
                            stale_reasons.append("evidence_content_changed")
                status = (
                    "stale"
                    if stale_reasons
                    else resolution.resolution_state
                )
            statuses.append(
                {
                    "verification_id": verification_id,
                    "verification_surface": queue_item.verification_surface,
                    "artifact_ids": queue_item.artifact_ids,
                    "status": status,
                    "stale_reasons": sorted(set(stale_reasons)),
                    "reviewed_at": (
                        resolution.reviewed_at if resolution else None
                    ),
                }
            )
    finally:
        if owns_client and resolved_client is not None:
            resolved_client.close()

    state_counts = dict(
        sorted(Counter(row["status"] for row in statuses).items())
    )
    disposition_counts = dict(
        sorted(
            Counter(
                resolution.artifact_disposition
                for resolution in resolutions.values()
            ).items()
        )
    )
    unresolved_states = {"unresolved", "stale"}
    blocker_states = {
        "unresolved",
        "stale",
        "partially_verified",
        "not_verified",
        "superseded",
    }
    return {
        "schema": "rock-kb-source-native-verification-report-v1",
        "status": "ok",
        "checked_at": effective_checked_at,
        "live_check_performed": check_live,
        "queue_count": len(queue),
        "resolution_count": len(resolutions),
        "verified_count": state_counts.get("verified", 0),
        "unresolved_count": sum(
            count
            for state, count in state_counts.items()
            if state in unresolved_states
        ),
        "default_cutover_blocker_count": sum(
            count
            for state, count in state_counts.items()
            if state in blocker_states
        ),
        "by_state": state_counts,
        "by_disposition": disposition_counts,
        "by_surface": dict(
            sorted(
                Counter(
                    queue[verification_id].verification_surface
                    for verification_id in queue
                ).items()
            )
        ),
        "items": statuses,
    }


def verification_resolutions_by_artifact(
    *,
    queue_rows: Iterable[dict[str, Any]],
    resolution_rows: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    queue = index_source_native_verification_queue(
        queue_rows,
        source="verification queue rows",
    )
    result: dict[str, list[dict[str, Any]]] = {}
    for raw in resolution_rows:
        resolution = SourceNativeVerificationResolution.model_validate(raw)
        queue_item = queue.get(resolution.verification_id)
        if queue_item is None:
            continue
        common_summary = {
            "verification_id": resolution.verification_id,
            "resolution_state": resolution.resolution_state,
            "finding": resolution.finding,
            "reviewed_at": resolution.reviewed_at,
            "revalidation_policy": resolution.revalidation_policy,
            "revalidate_after": resolution.revalidate_after,
            "rock_versions": resolution.rock_versions,
            "version_scope_status": resolution.version_scope_status,
            "evidence": [
                {
                    "evidence_type": evidence.evidence_type,
                    "source_url": evidence.source_url,
                    "source_ref": evidence.source_ref,
                    "finding": evidence.finding,
                    "locator": (
                        evidence.locator.public_dump()
                        if evidence.locator
                        else None
                    ),
                }
                for evidence in resolution.evidence
            ],
        }
        overrides = {
            row.artifact_id: row
            for row in resolution.artifact_overrides
        }
        if overrides and set(overrides) != set(queue_item.artifact_ids):
            raise ValueError(
                "artifact overrides must cover the verification queue artifact IDs "
                f"exactly: {resolution.verification_id}"
            )
        for artifact_id in queue_item.artifact_ids:
            override = overrides.get(artifact_id)
            result.setdefault(artifact_id, []).append(
                {
                    **common_summary,
                    "artifact_disposition": (
                        override.artifact_disposition
                        if override
                        else resolution.artifact_disposition
                    ),
                    "effective_title": (
                        override.effective_title
                        if override
                        else resolution.effective_title
                    ),
                    "effective_retrieval_text": (
                        override.effective_retrieval_text
                        if override
                        else resolution.effective_retrieval_text
                    ),
                }
            )
    for values in result.values():
        values.sort(key=lambda row: str(row["verification_id"]))
    return result


def hash_live_evidence(
    client: httpx.Client | None,
    url: str,
    hash_mode: str,
) -> str:
    if client is None:
        raise ValueError("live verification requires an HTTP client")
    if hash_mode == "rockumentation_markdown":
        from .source_native import rockumentation_markdown

        payload = fetch_rockumentation_payload(client, url)
        markdown = rockumentation_markdown(payload)
        if not markdown:
            raise ValueError("Rockumentation article content was unavailable")
        return sha256_text(markdown)
    response = client.get(url)
    response.raise_for_status()
    if hash_mode == "raw_content":
        return hashlib.sha256(response.content).hexdigest()
    if hash_mode in {"normalized_text", "normalized_article_text"}:
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup
        if hash_mode == "normalized_article_text":
            content = soup.find("article")
            if content is None:
                raise ValueError("verification page does not expose an article element")
        text = " ".join(content.get_text(" ", strip=True).split())
        return sha256_text(text)
    raise ValueError(f"unsupported live evidence hash mode: {hash_mode}")


def hash_live_evidence_with_timeout_retry(
    client: httpx.Client | None,
    url: str,
    hash_mode: str,
) -> str:
    try:
        return hash_live_evidence(client, url, hash_mode)
    except httpx.TimeoutException:
        return hash_live_evidence(client, url, hash_mode)


def parse_iso(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
