from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from ..paths import INDEX_DIR, REPO_ROOT
from .stages import Stage

StageStatus = Literal["fresh", "stale", "missing-outputs", "manual"]

DEFAULT_STATE_PATH = INDEX_DIR / "build-state.json"


def load_state(path: Path = DEFAULT_STATE_PATH) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict[str, dict[str, Any]], path: Path = DEFAULT_STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_stage_state(
    stage: Stage,
    state: dict[str, dict[str, Any]],
    repo_root: Path = REPO_ROOT,
    completed_at: str | None = None,
) -> dict[str, dict[str, Any]]:
    updated = dict(state)
    updated[stage.name] = {
        "input_hash": combined_input_hash(stage, repo_root=repo_root),
        "completed_at": completed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    return updated


def stage_status(
    stage: Stage,
    state: dict[str, dict[str, Any]],
    repo_root: Path = REPO_ROOT,
    upstream_statuses: dict[str, StageStatus] | None = None,
) -> StageStatus:
    if stage.manual:
        return "manual"
    if any((upstream_statuses or {}).get(dep) != "fresh" for dep in stage.depends_on):
        return "stale"
    if missing_output_patterns(stage, repo_root=repo_root):
        return "missing-outputs"
    previous = state.get(stage.name) or {}
    if previous.get("input_hash") != combined_input_hash(stage, repo_root=repo_root):
        return "stale"
    return "fresh"


def changed_input_paths(stage: Stage, state: dict[str, dict[str, Any]], repo_root: Path = REPO_ROOT) -> list[str]:
    previous = state.get(stage.name) or {}
    if previous.get("input_hash") == combined_input_hash(stage, repo_root=repo_root):
        return []
    return [path.relative_to(repo_root).as_posix() for path in input_files(stage, repo_root=repo_root)]


def combined_input_hash(stage: Stage, repo_root: Path = REPO_ROOT) -> str:
    digest = hashlib.sha256()
    for path in input_files(stage, repo_root=repo_root):
        relative = path.relative_to(repo_root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def input_files(stage: Stage, repo_root: Path = REPO_ROOT) -> list[Path]:
    return matching_files(stage.inputs, repo_root=repo_root)


def missing_output_patterns(stage: Stage, repo_root: Path = REPO_ROOT) -> list[str]:
    missing = []
    for pattern in stage.outputs:
        matches = matching_files([pattern], repo_root=repo_root)
        if not matches:
            missing.append(pattern)
    return missing


def matching_files(patterns: list[str], repo_root: Path = REPO_ROOT) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        paths.update(path for path in repo_root.glob(pattern) if path.is_file())
    return sorted(paths)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
