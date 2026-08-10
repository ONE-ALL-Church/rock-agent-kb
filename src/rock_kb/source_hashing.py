from __future__ import annotations

import json
from typing import Any

from .extract import sha256_text


def source_content_hash(snapshot: dict[str, Any], source_id: str) -> str:
    records = snapshot.get("source_records") or {}
    pairs = sorted(
        (str(record_id), source_record_freshness_hash(row))
        for record_id, row in records.items()
        if row.get("source_id") == source_id
    )
    if not pairs:
        return ""
    return sha256_text(json.dumps(pairs, ensure_ascii=False, separators=(",", ":")))


def source_record_freshness_hash(row: dict[str, Any]) -> str:
    payload = {
        "normalized_content_hash": row.get("summary_hash") or row.get("content_hash") or "",
        "source_title": row.get("source_title") or "",
        "source_url": row.get("source_url") or "",
        "topics": sorted(str(value) for value in row.get("topics") or []),
        "rock_versions": sorted(str(value) for value in row.get("rock_versions") or []),
        "version": row.get("version") or "",
        "release_family": row.get("release_family") or "",
        "model_name": row.get("model_name") or "",
        "model_category": row.get("model_category") or "",
    }
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
