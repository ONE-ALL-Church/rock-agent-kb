from __future__ import annotations

from pathlib import Path
from typing import Any

from ..paths import DATA_DIR, NORMALIZED_DIR, REPO_ROOT
from .stages import STAGES, Stage, stage_by_name, topological_stages
from .state import StageStatus, load_state, save_state, stage_status, update_stage_state


def run_build(
    stage_name: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    stages: list[Stage] | None = None,
    repo_root: Path = REPO_ROOT,
    state_path: Path | None = None,
) -> dict[str, Any]:
    stage_list = stages or STAGES
    selected = selected_stages(stage_list, stage_name=stage_name, force=force)
    state = load_state(state_path) if state_path else load_state()
    statuses: dict[str, StageStatus] = {}
    actions = []
    ran = []
    blocked = None
    for stage in selected:
        status = stage_status(stage, state, repo_root=repo_root, upstream_statuses=statuses)
        statuses[stage.name] = status
        if stage.manual:
            action = {
                "stage": stage.name,
                "status": status,
                "action": "manual-gate",
                "command": manual_stage_command(stage.name),
            }
            actions.append(action)
            if stage_blocks_remaining(stage, selected):
                blocked = action
                break
            continue
        if stage.private and not force and not private_processing_artifacts_available(repo_root):
            action = {
                "stage": stage.name,
                "status": status,
                "action": "reuse-public-artifacts",
                "command": f"Mount the private corpus, then run uv run kb build --stage {stage.name}",
            }
            actions.append(action)
            statuses[stage.name] = "fresh"
            continue
        should_run = force or status in {"stale", "missing-outputs"}
        action_name = "run" if should_run else "skip"
        if status == "private-stale" and not force:
            action_name = "private-inputs-changed"
        action = {
            "stage": stage.name,
            "status": status,
            "action": action_name,
            "command": f"uv run kb build --stage {stage.name}",
        }
        actions.append(action)
        if not should_run or dry_run:
            continue
        result = stage.run()
        state = update_stage_state(stage, state, repo_root=repo_root)
        if state_path:
            save_state(state, state_path)
        else:
            save_state(state)
        statuses[stage.name] = "fresh"
        ran.append({"stage": stage.name, "result": serializable_result(result)})
    return {
        "schema": "rock-kb-build-result-v1",
        "dry_run": dry_run,
        "force": force,
        "stage": stage_name,
        "actions": actions,
        "ran": ran,
        "blocked": blocked,
    }


def selected_stages(stages: list[Stage], stage_name: str | None = None, force: bool = False) -> list[Stage]:
    ordered = topological_stages(stages)
    if stage_name is None:
        return ordered
    by_name = stage_by_name(stages)
    if stage_name not in by_name:
        raise KeyError(f"Unknown pipeline stage: {stage_name}")
    if force:
        return [by_name[stage_name]]
    needed = dependency_closure(stage_name, by_name)
    return [stage for stage in ordered if stage.name in needed]


def dependency_closure(stage_name: str, by_name: dict[str, Stage]) -> set[str]:
    needed = {stage_name}
    for dependency in by_name[stage_name].depends_on:
        needed.update(dependency_closure(dependency, by_name))
    return needed


def stage_blocks_remaining(stage: Stage, selected: list[Stage]) -> bool:
    downstream = {later.name for later in selected[selected.index(stage) + 1 :]}
    return any(stage.name in later.depends_on and later.name in downstream for later in selected)


def manual_stage_command(stage_name: str) -> str:
    commands = {
        "model-map": "uv run kb modelmap build",
    }
    return commands.get(stage_name, f"Review manual gate for {stage_name}")


def private_processing_artifacts_available(repo_root: Path = REPO_ROOT) -> bool:
    data_dir = repo_root / DATA_DIR.relative_to(REPO_ROOT)
    normalized_dir = repo_root / NORMALIZED_DIR.relative_to(REPO_ROOT)
    media_index = data_dir / "media" / "index" / "media-index.jsonl"
    review_dir = data_dir / "review"
    return any(normalized_dir.glob("*.jsonl")) or media_index.exists() or any(review_dir.glob("**/*"))


def serializable_result(result: Any) -> Any:
    if isinstance(result, Path):
        return str(result)
    if isinstance(result, dict):
        return {str(key): serializable_result(value) for key, value in result.items()}
    if isinstance(result, list):
        return [serializable_result(value) for value in result]
    if isinstance(result, tuple):
        return [serializable_result(value) for value in result]
    if result is None or isinstance(result, (str, int, float, bool)):
        return result
    return repr(result)
