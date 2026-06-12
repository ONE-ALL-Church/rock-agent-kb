from __future__ import annotations

from pathlib import Path
from typing import Any

from ..concepts import concept_source_records, report_guide_refresh_plan
from ..jsonl import read_jsonl
from ..media import media_review_status_report
from ..mobile_selector_audit import mobile_selector_audit_status
from ..paths import AGENT_DIR, REPO_ROOT
from .stages import STAGES, Stage, topological_stages
from .state import StageStatus, changed_input_paths, load_state, stage_status


def build_status_report(
    stages: list[Stage] | None = None,
    repo_root: Path = REPO_ROOT,
    state_path: Path | None = None,
    include_queues: bool = True,
) -> dict[str, Any]:
    state = load_state(state_path) if state_path else load_state()
    statuses: dict[str, StageStatus] = {}
    pipeline_rows = []
    for stage in topological_stages(stages or STAGES):
        status = stage_status(stage, state, repo_root=repo_root, upstream_statuses=statuses)
        statuses[stage.name] = status
        changed = changed_input_paths(stage, state, repo_root=repo_root)[:3] if status == "stale" else []
        pipeline_rows.append(
            {
                "name": stage.name,
                "description": stage.description,
                "status": status,
                "changed_inputs": changed,
                "manual": stage.manual,
                "private": stage.private,
                "depends_on": stage.depends_on,
            }
        )
    report = {
        "pipeline": pipeline_rows,
        "suggested_commands": suggested_commands(pipeline_rows),
    }
    if include_queues:
        report["queues"] = review_queue_summary()
    return report


def suggested_commands(pipeline_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    commands = []
    for row in pipeline_rows:
        status = row["status"]
        if row.get("manual"):
            commands.append(
                {
                    "stage": row["name"],
                    "reason": "manual gate",
                    "command": manual_stage_command(str(row["name"])),
                }
            )
        elif status in {"stale", "missing-outputs"}:
            commands.append(
                {
                    "stage": row["name"],
                    "reason": str(status),
                    "command": f"uv run kb build --stage {row['name']}",
                }
            )
    return commands


def manual_stage_command(stage_name: str) -> str:
    commands = {
        "model-map": "uv run kb modelmap build",
    }
    return commands.get(stage_name, f"Review manual gate for {stage_name}")


def review_queue_summary() -> dict[str, Any]:
    records = concept_source_records()
    guide_refresh = report_guide_refresh_plan(records)
    mobile_status = mobile_selector_audit_status()
    media_review = media_review_status_report()
    claim_review_path = AGENT_DIR / "claim-review-queue.jsonl"
    return {
        "media_review": {
            "source_count": len(media_review.get("sources") or []),
            "pending_candidate_count": sum(
                int(row.get("pending_candidate_count") or 0) for row in media_review.get("sources") or []
            ),
        },
        "claim_review_queue": {
            "path": str(claim_review_path),
            "rows": sum(1 for _ in read_jsonl(claim_review_path)) if claim_review_path.exists() else 0,
        },
        "guide_refresh": {
            "needs_generated_index_rebuild": guide_refresh.get("needs_generated_index_rebuild") or [],
            "needs_long_form_guide_refresh": guide_refresh.get("needs_long_form_guide_refresh") or [],
        },
        "concept_staleness": {
            "stale": sorted(
                set(guide_refresh.get("needs_generated_index_rebuild") or [])
                | set(guide_refresh.get("needs_long_form_guide_refresh") or [])
            ),
            "rows": int(guide_refresh.get("concept_count") or 0),
            "summary_scope": "guide-refresh-derived",
        },
        "mobile_selector_audit": mobile_status,
    }
