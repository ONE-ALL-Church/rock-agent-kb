from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable, Optional

from .extract import generated_at_iso, grep_sensitive_values, now_iso, sha256_text
from .paths import DATA_DIR, MEDIA_DIR, NORMALIZED_DIR, RAW_MANIFEST_DIR, REPO_ROOT, REVIEW_DIR
from .publish import audit_public_export_manifest, build_public_export, iter_public_files

PRIVATE_CORPUS_SCHEMA = "rock-kb-private-corpus-v1"
PRIVATE_CORPUS_MANIFEST = "private-corpus-manifest.json"
PRIVATE_CORPUS_RESTORE_MANIFEST = "large-media-restore-manifest.json"

SYNCABLE_PRIVATE_ROOTS = [RAW_MANIFEST_DIR, NORMALIZED_DIR, REVIEW_DIR, MEDIA_DIR, DATA_DIR / "index"]
TEXT_ARTIFACT_SUFFIXES = {".json", ".jsonl", ".md", ".txt", ".yaml", ".yml", ".csv"}
LARGE_MEDIA_SUFFIXES = {".mp3", ".mp4", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".mov", ".m4v", ".webm", ".jpg", ".jpeg", ".png"}
PRIVATE_LEAK_MARKERS = {
    "transcript": "raw transcript field",
    "media_url": "direct media URL field",
    "download_path": "download path field",
    "clip_path": "private clip path field",
    "frame_path": "private frame path field",
}


def initialize_private_corpus(path: Path) -> dict[str, Any]:
    path.mkdir(parents=True, exist_ok=True)
    for rel in ["data/raw-manifests", "data/normalized", "data/review", "data/media", "data/index", "objects"]:
        (path / rel).mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": PRIVATE_CORPUS_SCHEMA,
        "created_at": now_iso(),
        "public_repo": REPO_ROOT.name,
        "text_artifact_roots": [relative_path(root) for root in SYNCABLE_PRIVATE_ROOTS],
        "large_media_restore_manifest": PRIVATE_CORPUS_RESTORE_MANIFEST,
        "notes": [
            "This private corpus may contain raw transcripts, review artifacts, private normalized records, manifests, and benchmark outputs.",
            "Do not publish this repo or copy its contents into the public export.",
            "Large media binaries should be restored through object storage or Git LFS/DVC rather than normal git.",
        ],
    }
    manifest_path = path / PRIVATE_CORPUS_MANIFEST
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    gitignore = path / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("objects/\n*.mp3\n*.mp4\n*.wav\n*.m4a\n*.mov\n*.webm\n*.m3u8\n", encoding="utf-8")
    return validate_private_corpus(path)


def validate_private_corpus(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = path / PRIVATE_CORPUS_MANIFEST
    manifest: dict[str, Any] = {}
    if not path.exists():
        errors.append(f"{path} does not exist")
    if not manifest_path.exists():
        errors.append(f"{PRIVATE_CORPUS_MANIFEST} is missing")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append(f"{PRIVATE_CORPUS_MANIFEST} is invalid JSON")
    if manifest and manifest.get("schema") != PRIVATE_CORPUS_SCHEMA:
        errors.append(f"{PRIVATE_CORPUS_MANIFEST} schema must be {PRIVATE_CORPUS_SCHEMA}")
    missing_dirs = [rel for rel in ["data/raw-manifests", "data/normalized", "data/review", "data/media", "data/index"] if not (path / rel).exists()]
    errors.extend(f"{rel} is missing" for rel in missing_dirs)
    return {
        "schema": "rock-kb-private-corpus-validation-v1",
        "status": "fail" if errors else "ok",
        "path": str(path),
        "manifest_path": str(manifest_path),
        "errors": errors,
        "missing_dirs": missing_dirs,
    }


def ignored_private_artifact_report(include_artifacts: bool = False, sample_limit: int = 25) -> dict[str, Any]:
    artifacts = private_artifacts()
    report = {
        "schema": "rock-kb-private-artifact-report-v1",
        "generated_at": generated_at_iso(),
        "artifact_count": len(artifacts),
        "text_json_artifact_count": sum(1 for row in artifacts if row["sync_class"] == "text_json"),
        "large_media_artifact_count": sum(1 for row in artifacts if row["sync_class"] == "large_media"),
        "other_private_artifact_count": sum(1 for row in artifacts if row["sync_class"] == "other_private"),
        "sample": artifacts[:sample_limit],
    }
    if include_artifacts:
        report["artifacts"] = artifacts
    return report


def sync_private_text_artifacts(corpus_path: Path, dry_run: bool = False) -> dict[str, Any]:
    validation = validate_private_corpus(corpus_path)
    if validation["status"] != "ok":
        return {"schema": "rock-kb-private-corpus-sync-v1", "status": "fail", "errors": validation["errors"], "copied": 0}
    artifacts = [row for row in private_artifacts() if row["sync_class"] == "text_json"]
    copied = 0
    for artifact in artifacts:
        rel = artifact["path"]
        src = REPO_ROOT / rel
        dst = corpus_path / rel
        if dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    return {
        "schema": "rock-kb-private-corpus-sync-v1",
        "status": "ok",
        "dry_run": dry_run,
        "corpus_path": str(corpus_path),
        "selected_artifacts": len(artifacts),
        "copied": copied,
        "sample": artifacts[:25],
    }


def restore_private_text_artifacts(corpus_path: Path, dry_run: bool = False, overwrite: bool = False) -> dict[str, Any]:
    validation = validate_private_corpus(corpus_path)
    if validation["status"] != "ok":
        return {"schema": "rock-kb-private-corpus-restore-v1", "status": "fail", "errors": validation["errors"], "restored": 0}
    restored = 0
    skipped = 0
    candidates: list[dict[str, Any]] = []
    for root_rel in ["data/raw-manifests", "data/normalized", "data/review", "data/media", "data/index"]:
        root = corpus_path / root_rel
        if not root.exists():
            continue
        for source in sorted(root.rglob("*")):
            if not source.is_file() or source.suffix.lower() not in TEXT_ARTIFACT_SUFFIXES:
                continue
            rel = source.relative_to(corpus_path).as_posix()
            target = REPO_ROOT / rel
            candidates.append({"source": str(source), "destination": rel})
            if target.exists() and not overwrite:
                skipped += 1
                continue
            if dry_run:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            restored += 1
    return {
        "schema": "rock-kb-private-corpus-restore-v1",
        "status": "ok",
        "dry_run": dry_run,
        "overwrite": overwrite,
        "corpus_path": str(corpus_path),
        "candidate_count": len(candidates),
        "restored": restored,
        "skipped_existing": skipped,
        "sample": candidates[:25],
    }


def autosync_private_corpus(corpus_path: Path, dry_run: bool = False, commit: bool = False) -> dict[str, Any]:
    sync_result = sync_private_text_artifacts(corpus_path, dry_run=dry_run)
    if sync_result["status"] != "ok":
        return {"schema": "rock-kb-private-corpus-autosync-v1", "status": "fail", "sync": sync_result}
    media_result = write_large_media_restore_manifest(corpus_path) if not dry_run else {"status": "dry_run"}
    commit_result: dict[str, Any] | None = None
    if commit and not dry_run:
        commit_result = commit_private_corpus_changes(corpus_path)
    return {
        "schema": "rock-kb-private-corpus-autosync-v1",
        "status": "ok" if media_result.get("status") in {"ok", "dry_run"} else "fail",
        "dry_run": dry_run,
        "sync": sync_result,
        "media_manifest": media_result,
        "commit": commit_result,
    }


def commit_private_corpus_changes(corpus_path: Path) -> dict[str, Any]:
    if not (corpus_path / ".git").exists():
        return {"status": "skipped", "reason": "private corpus path is not a git repository"}
    subprocess.run(["git", "add", "data", PRIVATE_CORPUS_RESTORE_MANIFEST, PRIVATE_CORPUS_MANIFEST], cwd=corpus_path, check=False)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=corpus_path, check=False)
    if diff.returncode == 0:
        return {"status": "skipped", "reason": "no private corpus changes"}
    message = "Sync Rock KB private corpus artifacts"
    result = subprocess.run(["git", "commit", "-m", message], cwd=corpus_path, check=False, text=True, capture_output=True)
    return {
        "status": "ok" if result.returncode == 0 else "fail",
        "message": message,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
    }


def write_large_media_restore_manifest(corpus_path: Path) -> dict[str, Any]:
    validation = validate_private_corpus(corpus_path)
    if validation["status"] != "ok":
        return {"schema": "rock-kb-large-media-restore-v1", "status": "fail", "errors": validation["errors"]}
    rows = [large_media_restore_row(row) for row in private_artifacts() if row["sync_class"] == "large_media"]
    manifest = {
        "schema": "rock-kb-large-media-restore-v1",
        "generated_at": generated_at_iso(),
        "public_repo": REPO_ROOT.name,
        "object_store_required": bool(rows),
        "media_objects": rows,
    }
    output = corpus_path / PRIVATE_CORPUS_RESTORE_MANIFEST
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"schema": "rock-kb-large-media-restore-result-v1", "status": "ok", "output": str(output), "media_object_count": len(rows)}


def verify_private_corpus_rebuild(
    corpus_path: Path,
    public_export_destination: Optional[Path] = None,
) -> dict[str, Any]:
    validation = validate_private_corpus(corpus_path)
    errors = list(validation.get("errors") or [])
    summary = private_corpus_artifact_summary(corpus_path)
    required_counts = {
        "raw_manifest_files": summary["raw_manifest_files"],
        "normalized_files": summary["normalized_files"],
        "review_files": summary["review_files"],
        "media_text_files": summary["media_text_files"],
    }
    for key, count in required_counts.items():
        if count == 0:
            errors.append(f"private corpus has no {key}")
    if summary["large_media_restore_manifest_exists"] is False:
        errors.append(f"{PRIVATE_CORPUS_RESTORE_MANIFEST} is missing; run kb corpus media-manifest")
    leak_audit = audit_private_corpus_leaks(corpus_path)
    if leak_audit["status"] != "ok":
        errors.extend(leak_audit.get("errors") or [])
    export_result: Optional[dict[str, Any]] = None
    if public_export_destination:
        export_result = build_public_export(public_export_destination)
        if export_result.get("status") != "ok":
            errors.extend(export_result.get("errors") or ["public export rebuild failed"])
    return {
        "schema": "rock-kb-private-corpus-rebuild-verification-v1",
        "status": "fail" if errors else "ok",
        "corpus_path": str(corpus_path),
        "artifact_summary": summary,
        "public_export_destination": str(public_export_destination) if public_export_destination else None,
        "public_export_result": export_result,
        "leak_audit_status": leak_audit["status"],
        "errors": errors[:100],
        "error_count": len(errors),
    }


def private_corpus_artifact_summary(corpus_path: Path) -> dict[str, Any]:
    media_dir = corpus_path / "data" / "media"
    return {
        "raw_manifest_files": count_files(corpus_path / "data" / "raw-manifests", TEXT_ARTIFACT_SUFFIXES),
        "normalized_files": count_files(corpus_path / "data" / "normalized", TEXT_ARTIFACT_SUFFIXES),
        "review_files": count_files(corpus_path / "data" / "review", TEXT_ARTIFACT_SUFFIXES),
        "media_text_files": count_files(media_dir, TEXT_ARTIFACT_SUFFIXES),
        "media_index_files": count_files(media_dir / "index", TEXT_ARTIFACT_SUFFIXES),
        "transcript_files": len(list(media_dir.glob("*.transcripts.jsonl"))) + len(list((media_dir / "transcripts").rglob("*.json"))) if media_dir.exists() else 0,
        "large_media_restore_manifest_exists": (corpus_path / PRIVATE_CORPUS_RESTORE_MANIFEST).exists(),
    }


def count_files(root: Path, suffixes: set[str]) -> int:
    if not root.exists():
        return 0
    return sum(1 for path in root.rglob("*") if path.is_file() and path.suffix.lower() in suffixes)


def audit_private_corpus_leaks(corpus_path: Optional[Path] = None) -> dict[str, Any]:
    errors = audit_public_export_manifest()
    markers: list[str] = []
    corpus_path_text = str(corpus_path) if corpus_path else ""
    for path in iter_public_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if corpus_path_text and corpus_path_text in text:
            markers.append(f"{rel}: contains private corpus absolute path")
        for finding in grep_sensitive_values(text.splitlines()):
            markers.append(f"{rel}: sensitive-looking value {finding[:120]}")
        if path.suffix.lower() in {".json", ".jsonl"}:
            markers.extend(public_json_private_markers(rel, text))
    errors.extend(markers)
    return {
        "schema": "rock-kb-private-corpus-leak-audit-v1",
        "status": "fail" if errors else "ok",
        "corpus_path": str(corpus_path) if corpus_path else None,
        "errors": errors[:100],
        "error_count": len(errors),
    }


def private_artifacts() -> list[dict[str, Any]]:
    rows = []
    for root in SYNCABLE_PRIVATE_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or not is_git_ignored(path):
                continue
            rows.append(private_artifact_row(path))
    return rows


def private_artifact_row(path: Path) -> dict[str, Any]:
    rel = relative_path(path)
    stat = path.stat()
    return {
        "path": rel,
        "bytes": stat.st_size,
        "sha256": sha256_file(path),
        "sync_class": sync_class(path),
        "private_corpus_path": rel,
        "large_media_restore_required": path.suffix.lower() in LARGE_MEDIA_SUFFIXES,
    }


def large_media_restore_row(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": artifact["path"],
        "bytes": artifact["bytes"],
        "sha256": artifact["sha256"],
        "object_key": f"rock-kb/{artifact['sha256'][:2]}/{artifact['sha256']}",
        "restore_status": "external_private_object_required",
    }


def sync_class(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in LARGE_MEDIA_SUFFIXES:
        return "large_media"
    if suffix in TEXT_ARTIFACT_SUFFIXES:
        return "text_json"
    return "other_private"


def is_git_ignored(path: Path) -> bool:
    rel = relative_path(path)
    result = subprocess.run(["git", "check-ignore", "-q", rel], cwd=REPO_ROOT, check=False)
    return result.returncode == 0


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def public_json_private_markers(path: str, text: str) -> list[str]:
    findings: list[str] = []
    rows = parse_public_json_rows(text, path.endswith(".jsonl"))
    for index, row in enumerate(rows):
        for field_path, reason in private_field_paths(row):
            findings.append(f"{path}:{index} contains {reason}: {field_path}")
    return findings


def parse_public_json_rows(text: str, jsonl: bool) -> list[Any]:
    if jsonl:
        rows = []
        for line in text.splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows
    payload = json.loads(text)
    return payload if isinstance(payload, list) else [payload]


def private_field_paths(value: Any, prefix: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}"
            if key in PRIVATE_LEAK_MARKERS:
                yield path, PRIVATE_LEAK_MARKERS[key]
            yield from private_field_paths(nested, path)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from private_field_paths(nested, f"{prefix}[{index}]")
