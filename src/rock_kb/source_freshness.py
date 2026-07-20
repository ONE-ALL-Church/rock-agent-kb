from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .extract import generated_at_iso, sha256_text
from .paths import AGENT_DIR, DATA_DIR, REPO_ROOT
from .source_orchestration import build_source_snapshot
from .source_workflows import load_source_freshness_policy
from .sources import Source, load_sources


POLICY_PATH = REPO_ROOT / "sources" / "freshness-policy.yaml"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "review" / "source-freshness"
OBSERVATION_SCHEMA = "rock-kb-source-observations-v1"
ROCK_ISSUE_SUMMARY_PATH = AGENT_DIR / "rock-issue-summary.json"
ROCK_ISSUE_CHECKPOINT_PATH = DATA_DIR / "review" / "rock-issues" / "checkpoint.json"
ISSUE_SOURCE_REPOSITORIES = {
    "rock_core_issues": "SparkDevNetwork/Rock",
    "rock_mobile_issues": "SparkDevNetwork/Rock.Mobile-Issues",
}


def build_source_freshness_report(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    as_of: datetime | None = None,
    source_status_path: Path | None = None,
    baseline_snapshot_path: Path | None = None,
    previous_observations_path: Path | None = None,
    issue_summary_path: Path = ROCK_ISSUE_SUMMARY_PATH,
    issue_checkpoint_path: Path = ROCK_ISSUE_CHECKPOINT_PATH,
    required_cadences: Iterable[str] | None = None,
    required_source_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
    policy = load_freshness_policy()
    snapshot = build_source_snapshot()
    refresh_status = read_json(source_status_path) if source_status_path and source_status_path.exists() else {}
    output_dir.mkdir(parents=True, exist_ok=True)
    observation_path = output_dir / "source-observations.json"
    previous_path = previous_observations_path or observation_path
    previous_observations = read_json(previous_path) if previous_path.exists() else {}
    baseline_snapshot = read_json(baseline_snapshot_path) if baseline_snapshot_path and baseline_snapshot_path.exists() else {}
    issue_summary = read_json(issue_summary_path) if issue_summary_path.exists() else {}
    issue_checkpoint = read_json(issue_checkpoint_path) if issue_checkpoint_path.exists() else {}
    sources = load_sources()
    observations = build_source_observations(
        sources,
        snapshot,
        as_of,
        refresh_status=refresh_status,
        previous_observations=previous_observations,
        baseline_snapshot=baseline_snapshot,
        issue_summary=issue_summary,
        issue_checkpoint=issue_checkpoint,
    )
    rows = source_freshness_rows(sources, snapshot, policy, as_of, refresh_status, observations)
    counts = Counter(str(row["status"]) for row in rows)
    required_cadence_set = {str(value) for value in required_cadences or []}
    required_source_id_set = {str(value) for value in required_source_ids or []}
    known_cadences = {source.refresh_cadence for source in sources}
    known_source_ids = {source.id for source in sources}
    unknown_cadences = required_cadence_set - known_cadences
    if unknown_cadences:
        raise ValueError(f"Unknown required cadence(s): {', '.join(sorted(unknown_cadences))}")
    unknown_source_ids = required_source_id_set - known_source_ids
    if unknown_source_ids:
        raise ValueError(f"Unknown required source(s): {', '.join(sorted(unknown_source_ids))}")
    blocking = blocking_source_ids(
        rows,
        required_cadence_set or None,
        required_source_id_set or None,
    )
    report = {
        "schema": "rock-kb-source-freshness-report-v1",
        "generated_at": generated_at_iso(),
        "as_of": as_of.isoformat(),
        "policy_path": "sources/freshness-policy.yaml",
        "status": "fail" if blocking else "ok",
        "counts": dict(sorted(counts.items())),
        "required_cadences": sorted(required_cadence_set),
        "required_source_ids": sorted(required_source_id_set),
        "blocking_source_ids": sorted(blocking),
        "sources": rows,
    }
    observation_path.write_text(
        json.dumps(observations, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "source-freshness-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "source-freshness-summary.md").write_text(render_freshness_markdown(report), encoding="utf-8")
    return report


def blocking_source_ids(
    rows: Iterable[dict[str, Any]],
    required_cadences: set[str] | None = None,
    required_source_ids: set[str] | None = None,
) -> list[str]:
    return sorted(
        str(row["source_id"])
        for row in rows
        if row.get("status") in {"overdue", "missing", "failed"}
        and (not required_cadences or row.get("cadence") in required_cadences)
        and (not required_source_ids or row.get("source_id") in required_source_ids)
    )


def build_source_observations(
    sources: Iterable[Source],
    snapshot: dict[str, Any],
    as_of: datetime,
    *,
    refresh_status: dict[str, Any] | None = None,
    previous_observations: dict[str, Any] | None = None,
    baseline_snapshot: dict[str, Any] | None = None,
    issue_summary: dict[str, Any] | None = None,
    issue_checkpoint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    refresh_status = refresh_status or {}
    previous_sources = (previous_observations or {}).get("sources") or {}
    baseline_snapshot = baseline_snapshot or {}
    issue_summary = issue_summary or {}
    issue_checkpoint = issue_checkpoint or {}
    snapshot_sources = snapshot.get("sources") or {}
    checked = {str(value) for value in refresh_status.get("checked") or []}
    failed = {str(value) for value in refresh_status.get("failed") or []}
    skipped = {str(value) for value in refresh_status.get("skipped") or []}
    explicit_checked = "checked" in refresh_status
    checked_at = parse_datetime(refresh_status.get("checked_at"))
    issue_checked_at = parse_datetime(issue_checkpoint.get("checked_at")) or parse_datetime(
        issue_summary.get("source_updated_through")
    )
    rows: dict[str, dict[str, Any]] = {}

    for source in sorted(sources, key=lambda item: item.id):
        current = snapshot_sources.get(source.id) or {}
        previous = previous_sources.get(source.id) or {}
        result_count = int(current.get("record_count") or 0)
        content_hash = source_content_hash(snapshot, source.id)
        source_checked_at = parse_datetime(current.get("retrieved_at_max"))

        repository = ISSUE_SOURCE_REPOSITORIES.get(source.id)
        if repository and issue_summary:
            result_count = int((issue_summary.get("repositories") or {}).get(repository) or 0)
            catalog_hash = str(issue_summary.get("catalog_content_hash") or "")
            content_hash = sha256_text(f"{source.id}:{catalog_hash}:{result_count}") if catalog_hash else ""
            source_checked_at = issue_checked_at

        if source.refresh_cadence == "manual":
            check_status = "manual"
        elif source.id in failed or "refresh_pipeline" in failed:
            check_status = "failed"
        elif source.id in skipped:
            check_status = "skipped"
        elif repository and source_checked_at and result_count:
            check_status = "success"
        elif source.id in checked:
            check_status = "success" if result_count else "missing"
            source_checked_at = checked_at or source_checked_at
        elif explicit_checked:
            check_status = "not_checked"
        elif source_checked_at and result_count:
            check_status = "success"
        else:
            check_status = "missing"

        last_checked_at = source_checked_at
        if check_status == "not_checked" and previous.get("last_checked_at"):
            last_checked_at = parse_datetime(previous.get("last_checked_at"))
        if source.id in checked and checked_at:
            last_checked_at = checked_at

        content_changed_at = resolve_content_changed_at(
            source.id,
            content_hash,
            previous,
            baseline_snapshot,
            last_checked_at or as_of,
        )
        rows[source.id] = {
            "source_id": source.id,
            "last_checked_at": isoformat(last_checked_at),
            "content_changed_at": isoformat(content_changed_at),
            "result_count": result_count,
            "content_hash": content_hash,
            "status": check_status,
        }

    return {
        "schema": OBSERVATION_SCHEMA,
        "generated_at": generated_at_iso(),
        "sources": rows,
    }


def resolve_content_changed_at(
    source_id: str,
    content_hash: str,
    previous: dict[str, Any],
    baseline_snapshot: dict[str, Any],
    fallback: datetime,
) -> datetime | None:
    if not content_hash:
        return None
    if previous.get("content_hash") == content_hash and previous.get("content_changed_at"):
        return parse_datetime(previous.get("content_changed_at"))
    baseline_hash = source_content_hash(baseline_snapshot, source_id)
    if baseline_hash == content_hash:
        baseline_source = ((baseline_snapshot.get("sources") or {}).get(source_id) or {})
        return (
            parse_datetime(baseline_source.get("retrieved_at_max"))
            or parse_datetime(baseline_snapshot.get("generated_at"))
            or fallback
        )
    return fallback


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


def source_freshness_rows(
    sources: Iterable[Source],
    snapshot: dict[str, Any],
    policy: dict[str, Any],
    as_of: datetime,
    refresh_status: dict[str, Any] | None = None,
    observations: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    refresh_status = refresh_status or {}
    failed = {str(value) for value in refresh_status.get("failed") or []}
    skipped = {str(value) for value in refresh_status.get("skipped") or []}
    snapshot_sources = snapshot.get("sources") or {}
    observation_sources = (observations or {}).get("sources") or {}
    due_soon_fraction = float(policy.get("due_soon_fraction") or 0.75)
    cadence_policy = policy.get("cadences") or {}
    rows = []
    for source in sorted(sources, key=lambda item: item.id):
        current = snapshot_sources.get(source.id) or {}
        observation = observation_sources.get(source.id) or {}
        maximum_age = (cadence_policy.get(source.refresh_cadence) or {}).get("maximum_age_hours")
        last_checked_at = parse_datetime(observation.get("last_checked_at") or current.get("retrieved_at_max"))
        content_changed_at = parse_datetime(observation.get("content_changed_at"))
        result_count = int(observation.get("result_count") if "result_count" in observation else current.get("record_count") or 0)
        check_status = str(observation.get("status") or "")
        age_hours = round((as_of - last_checked_at).total_seconds() / 3600, 2) if last_checked_at else None
        if source.id in failed or "refresh_pipeline" in failed or check_status == "failed":
            status = "failed"
        elif source.refresh_cadence == "manual":
            status = "manual"
        elif not last_checked_at or not result_count:
            status = "missing"
        elif maximum_age is not None and age_hours is not None and age_hours > float(maximum_age):
            status = "overdue"
        elif maximum_age is not None and age_hours is not None and age_hours >= float(maximum_age) * due_soon_fraction:
            status = "due_soon"
        else:
            status = "current"
        rows.append(
            {
                "source_id": source.id,
                "name": source.name,
                "cadence": source.refresh_cadence,
                "maximum_age_hours": maximum_age,
                "last_checked_at": isoformat(last_checked_at),
                "content_changed_at": isoformat(content_changed_at),
                "result_count": result_count,
                "content_hash": str(observation.get("content_hash") or ""),
                "check_status": check_status or ("success" if last_checked_at and result_count else "missing"),
                "retrieved_at": isoformat(last_checked_at),
                "age_hours": age_hours,
                "record_count": result_count,
                "status": status,
                "refresh_skipped": source.id in skipped or check_status == "skipped",
            }
        )
    return rows


def load_freshness_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    return load_source_freshness_policy(path)


def parse_datetime(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def isoformat(value: datetime | None) -> str:
    return value.isoformat() if value else ""


def render_freshness_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Source Freshness",
        "",
        f"Status: **{report['status']}**",
        "",
        "| Source | Cadence | Last checked | Content changed | Age (hours) | Results | Check | Freshness |",
        "|---|---:|---|---|---:|---:|---|---|",
    ]
    for row in report["sources"]:
        age = "n/a" if row["age_hours"] is None else f"{row['age_hours']:.1f}"
        lines.append(
            f"| `{row['source_id']}` | {row['cadence']} | {row['last_checked_at'] or 'n/a'} | "
            f"{row['content_changed_at'] or 'n/a'} | {age} | {row['result_count']} | "
            f"{row['check_status']} | {row['status']} |"
        )
    return "\n".join(lines) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}
