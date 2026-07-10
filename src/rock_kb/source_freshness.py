from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from .extract import generated_at_iso
from .paths import REPO_ROOT
from .source_orchestration import build_source_snapshot
from .sources import Source, load_sources


POLICY_PATH = REPO_ROOT / "sources" / "freshness-policy.yaml"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "review" / "source-freshness"


def build_source_freshness_report(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    as_of: datetime | None = None,
    source_status_path: Path | None = None,
) -> dict[str, Any]:
    as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
    policy = load_freshness_policy()
    snapshot = build_source_snapshot()
    refresh_status = read_json(source_status_path) if source_status_path and source_status_path.exists() else {}
    rows = source_freshness_rows(load_sources(), snapshot, policy, as_of, refresh_status)
    counts = Counter(str(row["status"]) for row in rows)
    blocking = [row["source_id"] for row in rows if row["status"] in {"overdue", "missing", "failed"}]
    report = {
        "schema": "rock-kb-source-freshness-report-v1",
        "generated_at": generated_at_iso(),
        "as_of": as_of.isoformat(),
        "policy_path": "sources/freshness-policy.yaml",
        "status": "fail" if blocking else "ok",
        "counts": dict(sorted(counts.items())),
        "blocking_source_ids": sorted(blocking),
        "sources": rows,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source-freshness-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "source-freshness-summary.md").write_text(render_freshness_markdown(report), encoding="utf-8")
    return report


def source_freshness_rows(
    sources: Iterable[Source],
    snapshot: dict[str, Any],
    policy: dict[str, Any],
    as_of: datetime,
    refresh_status: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    refresh_status = refresh_status or {}
    failed = {str(value) for value in refresh_status.get("failed") or []}
    skipped = {str(value) for value in refresh_status.get("skipped") or []}
    snapshot_sources = snapshot.get("sources") or {}
    due_soon_fraction = float(policy.get("due_soon_fraction") or 0.75)
    cadence_policy = policy.get("cadences") or {}
    rows = []
    for source in sorted(sources, key=lambda item: item.id):
        current = snapshot_sources.get(source.id) or {}
        maximum_age = (cadence_policy.get(source.refresh_cadence) or {}).get("maximum_age_hours")
        retrieved_at = parse_datetime(current.get("retrieved_at_max"))
        age_hours = round((as_of - retrieved_at).total_seconds() / 3600, 2) if retrieved_at else None
        if source.id in failed or "refresh_pipeline" in failed:
            status = "failed"
        elif source.refresh_cadence == "manual":
            status = "manual"
        elif not retrieved_at or not int(current.get("record_count") or 0):
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
                "retrieved_at": retrieved_at.isoformat() if retrieved_at else "",
                "age_hours": age_hours,
                "record_count": int(current.get("record_count") or 0),
                "status": status,
                "refresh_skipped": source.id in skipped,
            }
        )
    return rows


def load_freshness_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if value.get("schema") != "rock-kb-source-freshness-policy-v1":
        raise ValueError("Unsupported source freshness policy schema.")
    return value


def parse_datetime(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def render_freshness_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Source Freshness",
        "",
        f"Status: **{report['status']}**",
        "",
        "| Source | Cadence | Age (hours) | Records | Status |",
        "|---|---:|---:|---:|---|",
    ]
    for row in report["sources"]:
        age = "n/a" if row["age_hours"] is None else f"{row['age_hours']:.1f}"
        lines.append(f"| `{row['source_id']}` | {row['cadence']} | {age} | {row['record_count']} | {row['status']} |")
    return "\n".join(lines) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}
