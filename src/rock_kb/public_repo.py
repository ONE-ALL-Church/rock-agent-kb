from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable, Optional

from .paths import PUBLIC_EXPORT_DIR

DEFAULT_PRESERVED_PUBLIC_PATHS = (
    ".git",
    ".github",
    "community-contributions",
    "source-suggestions",
)


def sync_public_export_to_repo(
    destination: Path,
    export_dir: Path = PUBLIC_EXPORT_DIR,
    delete: bool = True,
    preserve_paths: Iterable[str] = DEFAULT_PRESERVED_PUBLIC_PATHS,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Copy the audited public export into a public repo while preserving intake paths."""
    destination = destination.resolve()
    export_dir = export_dir.resolve()
    if not export_dir.exists():
        raise FileNotFoundError(f"{export_dir} does not exist; run kb publish export first")
    preserve = tuple(clean_preserve_path(path) for path in preserve_paths if clean_preserve_path(path))
    destination.mkdir(parents=True, exist_ok=True)

    deleted: list[str] = []
    copied: list[str] = []
    preserved_existing: list[str] = []

    if delete:
        for child in sorted(destination.iterdir(), key=lambda path: path.name):
            rel = child.relative_to(destination).as_posix()
            if is_preserved_public_path(rel, preserve):
                preserved_existing.append(rel)
                continue
            deleted.append(rel)
            if not dry_run:
                remove_path(child)

    for source in sorted(export_dir.rglob("*")):
        rel = source.relative_to(export_dir).as_posix()
        target = destination / rel
        if source.is_dir():
            if not dry_run:
                target.mkdir(parents=True, exist_ok=True)
            continue
        copied.append(rel)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    return {
        "schema": "rock-kb-public-repo-sync-v1",
        "status": "ok",
        "destination": str(destination),
        "export_dir": str(export_dir),
        "delete": delete,
        "dry_run": dry_run,
        "preserved_paths": list(preserve),
        "preserved_existing": preserved_existing,
        "deleted_count": len(deleted),
        "deleted": deleted,
        "copied_count": len(copied),
        "copied": copied,
    }


def commit_public_repo(
    destination: Path,
    message: str,
    push: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    status = git_status(destination)
    if not status:
        return {
            "schema": "rock-kb-public-repo-git-v1",
            "status": "clean",
            "destination": str(destination),
            "committed": False,
            "pushed": False,
        }
    if dry_run:
        return {
            "schema": "rock-kb-public-repo-git-v1",
            "status": "dry_run",
            "destination": str(destination),
            "committed": False,
            "pushed": False,
            "git_status": status,
        }
    run_git(destination, ["add", "-A"])
    run_git(destination, ["commit", "-m", message])
    pushed = False
    if push:
        run_git(destination, ["push"])
        pushed = True
    return {
        "schema": "rock-kb-public-repo-git-v1",
        "status": "committed",
        "destination": str(destination),
        "committed": True,
        "pushed": pushed,
    }


def clean_preserve_path(path: str) -> str:
    return path.strip().strip("/")


def is_preserved_public_path(rel_path: str, preserve_paths: Iterable[str]) -> bool:
    rel_path = clean_preserve_path(rel_path)
    for preserve in preserve_paths:
        if rel_path == preserve or rel_path.startswith(f"{preserve}/"):
            return True
    return False


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def git_status(destination: Path) -> str:
    result = run_git(destination, ["status", "--short"], capture=True)
    return result.stdout.strip()


def run_git(destination: Path, args: list[str], capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(destination), *args],
        check=True,
        text=True,
        capture_output=capture,
    )
