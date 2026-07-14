from __future__ import annotations

import hashlib
import json
import posixpath
import re
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib import request

import yaml


GITHUB_RELEASES_API = "https://api.github.com/repos/ONE-ALL-Church/rock-agent-kb/releases"
MANIFEST_NAME = "okf-manifest.json"
CHECKSUMS_NAME = "checksums.sha256"
RESERVED_FILENAMES = {"index.md", "log.md"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOG_DATE_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}$")
PRIVATE_MARKERS = (
    "/Users/",
    "data/review/",
    "data/normalized/",
    "private_corpus_pointer",
    "rockproduction_docs_private_candidates",
    "private_rock_repo_candidates",
    "outside_org_contribution_candidates",
)


def download_okf(
    *,
    version: str,
    archive_format: str,
    destination: Path | None,
    force: bool,
    user_agent: str,
) -> dict:
    release = release_metadata(version, user_agent)
    suffix = ".zip" if archive_format == "zip" else ".tar.gz"
    assets = release.get("assets") or []
    asset = next(
        (
            item
            for item in assets
            if str(item.get("name") or "").startswith("rock-agent-kb-okf-v")
            and str(item.get("name") or "").endswith(suffix)
        ),
        None,
    )
    if not asset:
        raise RuntimeError(f"Release {release.get('tag_name') or version} has no OKF {archive_format} asset")
    target = (destination or Path(str(asset["name"]))).expanduser().resolve()
    if target.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite existing file: {target}; pass --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    download_url(str(asset["browser_download_url"]), target, user_agent)

    expected = expected_asset_checksum(assets, str(asset["name"]), user_agent)
    actual = sha256_bytes(target.read_bytes())
    if expected and expected != actual:
        target.unlink(missing_ok=True)
        raise RuntimeError(f"Checksum mismatch for {asset['name']}")
    return {
        "schema": "rock-kb-okf-download-v1",
        "status": "ok",
        "version": str(release.get("tag_name") or version).removeprefix("rock-kb-v"),
        "release_url": release.get("html_url") or "",
        "asset": str(asset["name"]),
        "destination": str(target),
        "bytes": target.stat().st_size,
        "sha256": actual,
        "checksum_verified": bool(expected),
    }


def inspect_okf(path: Path) -> dict:
    files = read_bundle(path)
    manifest = load_manifest(files)
    return {
        "schema": "rock-kb-okf-inspection-v1",
        "status": "ok",
        "path": str(path.expanduser().resolve()),
        "okf_version": manifest.get("okf_version"),
        "distribution_version": manifest.get("distribution_version"),
        "generated_at": manifest.get("generated_at"),
        "source_commit": manifest.get("source_commit"),
        "read_only": manifest.get("read_only"),
        "counts": manifest.get("counts") or {},
        "markdown_files": manifest.get("markdown_files"),
        "relationships": manifest.get("relationships"),
        "archive_entries": len(files),
    }


def validate_okf(path: Path) -> dict:
    errors: list[str] = []
    try:
        files = read_bundle(path)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        return validation_report(path, [str(exc)])

    try:
        manifest = load_manifest(files)
    except (ValueError, json.JSONDecodeError) as exc:
        manifest = {}
        errors.append(str(exc))
    if manifest:
        if manifest.get("schema") != "rock-kb-okf-distribution-v1":
            errors.append(f"{MANIFEST_NAME} has unexpected schema")
        if str(manifest.get("okf_version") or "") != "0.1":
            errors.append(f"{MANIFEST_NAME} must declare okf_version 0.1")
        if manifest.get("read_only") is not True:
            errors.append(f"{MANIFEST_NAME} must declare read_only true")

    root_index = files.get("index.md")
    if root_index is None:
        errors.append("missing index.md")
    else:
        root_meta = parse_frontmatter(root_index.decode("utf-8"))
        if str(root_meta.get("okf_version") or "") != "0.1":
            errors.append("index.md must declare okf_version 0.1")
    if "log.md" not in files:
        errors.append("missing log.md")

    names = set(files)
    for relative, content in sorted(files.items()):
        if not relative.endswith(".md"):
            continue
        text = content.decode("utf-8")
        name = PurePosixPath(relative).name
        if name in RESERVED_FILENAMES:
            if relative != "index.md" and text.startswith("---\n"):
                errors.append(f"reserved file must not have frontmatter: {relative}")
            if name == "log.md":
                for line in text.splitlines():
                    if line.startswith("## ") and not LOG_DATE_RE.match(line):
                        errors.append(f"{relative} has non-ISO date heading: {line}")
        else:
            metadata = parse_frontmatter(text)
            if not metadata.get("type"):
                errors.append(f"{relative} missing parseable non-empty type frontmatter")
        for target in markdown_targets(text):
            resolved = resolve_target(relative, target)
            if resolved and resolved not in names and not any(name.startswith(f"{resolved.rstrip('/')}/") for name in names):
                errors.append(f"{relative} has unresolved link: {target}")
        lowered = text.lower()
        for marker in PRIVATE_MARKERS:
            if marker.lower() in lowered:
                errors.append(f"{relative} contains private marker: {marker}")

    errors.extend(validate_checksums(files))
    if manifest.get("markdown_files") is not None:
        actual_markdown = sum(1 for name in files if name.endswith(".md"))
        if int(manifest["markdown_files"]) != actual_markdown:
            errors.append(f"markdown file count mismatch: expected {manifest['markdown_files']}, found {actual_markdown}")
    return validation_report(path, sorted(set(errors)), manifest)


def validation_report(path: Path, errors: list[str], manifest: dict | None = None) -> dict:
    return {
        "schema": "rock-kb-okf-validation-v1",
        "status": "ok" if not errors else "failed",
        "path": str(path.expanduser().resolve()),
        "okf_version": (manifest or {}).get("okf_version"),
        "distribution_version": (manifest or {}).get("distribution_version"),
        "errors": errors,
    }


def release_metadata(version: str, user_agent: str) -> dict:
    endpoint = f"{GITHUB_RELEASES_API}/latest" if version == "latest" else f"{GITHUB_RELEASES_API}/tags/rock-kb-v{version.removeprefix('rock-kb-v')}"
    req = request.Request(endpoint, headers={"user-agent": user_agent, "accept": "application/vnd.github+json"})
    with request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def download_url(url: str, destination: Path, user_agent: str) -> None:
    req = request.Request(url, headers={"user-agent": user_agent, "accept": "application/octet-stream"})
    with request.urlopen(req) as response, destination.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)


def expected_asset_checksum(assets: list[dict], asset_name: str, user_agent: str) -> str:
    checksum_asset = next(
        (
            item
            for item in assets
            if str(item.get("name") or "").startswith("rock-agent-kb-okf-v")
            and str(item.get("name") or "").endswith(".sha256")
        ),
        None,
    )
    if not checksum_asset:
        return ""
    req = request.Request(str(checksum_asset["browser_download_url"]), headers={"user-agent": user_agent})
    with request.urlopen(req) as response:
        text = response.read().decode("utf-8")
    for line in text.splitlines():
        if line.endswith(f"  {asset_name}"):
            return line.split("  ", 1)[0]
    return ""


def read_bundle(path: Path) -> dict[str, bytes]:
    resolved = path.expanduser().resolve()
    if resolved.is_dir():
        return {
            item.relative_to(resolved).as_posix(): item.read_bytes()
            for item in resolved.rglob("*")
            if item.is_file()
        }
    if zipfile.is_zipfile(resolved):
        with zipfile.ZipFile(resolved) as archive:
            raw = {}
            for info in archive.infolist():
                if info.is_dir():
                    continue
                validate_archive_name(info.filename)
                raw[info.filename] = archive.read(info)
            return normalize_archive_root(raw)
    if tarfile.is_tarfile(resolved):
        with tarfile.open(resolved, "r:*") as archive:
            raw = {}
            for member in archive.getmembers():
                if member.isdir():
                    continue
                validate_archive_name(member.name)
                if not member.isfile():
                    raise ValueError(f"Archive contains unsupported non-file entry: {member.name}")
                extracted = archive.extractfile(member)
                if extracted is None:
                    raise ValueError(f"Could not read archive entry: {member.name}")
                raw[member.name] = extracted.read()
            return normalize_archive_root(raw)
    raise ValueError(f"Unsupported OKF bundle path: {resolved}")


def validate_archive_name(name: str) -> None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Archive contains unsafe path: {name}")


def normalize_archive_root(files: dict[str, bytes]) -> dict[str, bytes]:
    manifest_paths = [name for name in files if PurePosixPath(name).name == MANIFEST_NAME]
    if len(manifest_paths) != 1:
        raise ValueError(f"Archive must contain exactly one {MANIFEST_NAME}")
    root = PurePosixPath(manifest_paths[0]).parent
    normalized = {}
    for name, content in files.items():
        path = PurePosixPath(name)
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            raise ValueError(f"Archive entry is outside the bundle root: {name}") from None
        normalized[relative] = content
    return normalized


def load_manifest(files: dict[str, bytes]) -> dict:
    if MANIFEST_NAME not in files:
        raise ValueError(f"Bundle is missing {MANIFEST_NAME}")
    value = json.loads(files[MANIFEST_NAME].decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{MANIFEST_NAME} must contain a JSON object")
    return value


def validate_checksums(files: dict[str, bytes]) -> list[str]:
    if CHECKSUMS_NAME not in files:
        return [f"missing {CHECKSUMS_NAME}"]
    errors = []
    for line in files[CHECKSUMS_NAME].decode("utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid checksum row: {line}")
            continue
        if relative not in files:
            errors.append(f"checksum target missing: {relative}")
        elif sha256_bytes(files[relative]) != expected:
            errors.append(f"checksum mismatch: {relative}")
    return errors


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    try:
        value = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def markdown_targets(text: str) -> list[str]:
    targets = []
    for match in MARKDOWN_LINK_RE.finditer(strip_fenced_blocks(text)):
        target = match.group(1).strip().strip("<>").split("#", 1)[0].strip()
        if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            targets.append(target)
    return targets


def strip_fenced_blocks(text: str) -> str:
    kept: list[str] = []
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if not fence and marker:
            fence = marker.group(1)[0]
            continue
        if fence and re.match(rf"^{re.escape(fence)}{{3,}}\s*$", stripped):
            fence = ""
            continue
        if not fence:
            kept.append(line)
    return "\n".join(kept)


def resolve_target(source: str, target: str) -> str:
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), target))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
