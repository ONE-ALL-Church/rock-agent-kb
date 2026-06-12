from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from ..jsonl import read_jsonl
from ..paths import REPO_ROOT

PUBLIC_SEARCH_PREFIXES = ("knowledge/", "agent/", "claims/")
PRIVATE_PATH_PREFIXES = ("data/review/", "data/media/", "data/normalized/", "data/raw-manifests/", "data/index/")


def search(query: str, limit: int = 10, root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    db_path = root / "data" / "index" / "kb.sqlite"
    if not db_path.exists():
        return []
    fts_query = build_fts_query(query)
    if not fts_query:
        return []
    rows: list[dict[str, Any]] = []
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        for row in connection.execute(
            """
            SELECT
              r.id,
              r.source_id,
              r.source_url,
              r.source_title,
              r.topics,
              r.summary,
              r.excerpt,
              r.canonical_path,
              snippet(records_fts, 3, '', '', '...', 16) AS snippet
            FROM records_fts
            JOIN records r ON r.id = records_fts.id
            WHERE records_fts MATCH ?
            LIMIT ?
            """,
            (fts_query, max(limit * 4, limit)),
        ):
            item = dict(row)
            if not is_public_artifact_path(str(item.get("canonical_path") or "")):
                continue
            rows.append(
                {
                    "id": item.get("id"),
                    "title": item.get("source_title"),
                    "path": item.get("canonical_path"),
                    "url": item.get("source_url"),
                    "concept": first_topic(item.get("topics")),
                    "topics": split_topics(item.get("topics")),
                    "snippet": item.get("snippet") or item.get("summary") or item.get("excerpt"),
                    "source_id": item.get("source_id"),
                }
            )
            if len(rows) >= limit:
                break
    return rows


def get_manifest(root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    path = root / "agent" / "rock-kb-manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def list_concepts(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    return list(read_jsonl(root / "agent" / "concept-index.jsonl"))


def get_concept(concept_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    concept_dir = root / "knowledge" / "concepts" / concept_id
    index_row = next((row for row in list_concepts(root) if row.get("concept_id") == concept_id), None)
    return {
        "concept_id": concept_id,
        "title": (index_row or {}).get("title"),
        "index": index_row,
        "quickstart": read_text_if_public(concept_dir / "quickstart.md", root),
        "guide_path": public_relpath(concept_dir / "index.md", root),
        "answers": [row for row in read_jsonl(root / "agent" / "answer-pack.jsonl") if row.get("concept_id") == concept_id],
        "task_cards": [row for row in read_jsonl(root / "agent" / "concept-task-cards.jsonl") if row.get("concept_id") == concept_id],
        "release_caveats": [row for row in read_jsonl(root / "agent" / "concept-release-caveats.jsonl") if row.get("concept_id") == concept_id],
    }


def get_claims(concept_id: str, tier: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    root = root or REPO_ROOT
    rows = []
    for row in read_jsonl(root / "claims" / "approved-claims.jsonl"):
        if concept_id not in (row.get("concept_ids") or []):
            continue
        if tier and row.get("claim_tier") != tier:
            continue
        rows.append(row)
    return rows


def build_fts_query(query: str) -> str:
    terms = re.findall(r"[A-Za-z0-9_]+", query)
    return " ".join(terms)


def is_public_artifact_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("/")
    if any(normalized.startswith(prefix) for prefix in PRIVATE_PATH_PREFIXES):
        return False
    return any(normalized.startswith(prefix) for prefix in PUBLIC_SEARCH_PREFIXES)


def split_topics(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [part for part in str(value or "").split(",") if part]


def first_topic(value: Any) -> str | None:
    topics = split_topics(value)
    return topics[0] if topics else None


def read_text_if_public(path: Path, root: Path) -> str | None:
    if not path.exists():
        return None
    rel = public_relpath(path, root)
    if not is_public_artifact_path(rel):
        return None
    return path.read_text(encoding="utf-8")


def public_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)
