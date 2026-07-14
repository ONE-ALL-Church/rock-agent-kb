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
FILE_MANIFEST_NAME = "file-manifest.jsonl"
OKF_SPEC_COMMIT = "ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a"
RESERVED_FILENAMES = {"index.md", "log.md"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOG_DATE_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PRIVATE_MARKERS = (
    "/Users/",
    "data/review/",
    "data/normalized/",
    "private_corpus_pointer",
    "rockproduction_docs_private_candidates",
    "private_rock_repo_candidates",
    "outside_org_contribution_candidates",
)
REQUEST_TIMEOUT = 30
MAX_ARCHIVE_ENTRIES = 25_000
MAX_TOTAL_UNCOMPRESSED = 512 * 1024 * 1024
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200
MAX_DOWNLOAD_BYTES = 512 * 1024 * 1024


def download_okf(
    *,
    version: str,
    archive_format: str,
    destination: Path | None,
    force: bool,
    user_agent: str,
    profile: str = "full",
) -> dict:
    if profile not in {"full", "core"}:
        raise ValueError(f"Unknown OKF profile: {profile}")
    release = release_metadata(version, user_agent)
    resolved_version = str(release.get("tag_name") or version).removeprefix("rock-kb-v")
    suffix = ".zip" if archive_format == "zip" else ".tar.gz"
    base_name = (
        f"rock-agent-kb-okf-v{resolved_version}"
        if profile == "full"
        else f"rock-agent-kb-okf-{profile}-v{resolved_version}"
    )
    asset_name = f"{base_name}{suffix}"
    assets = release.get("assets") or []
    asset = next((item for item in assets if str(item.get("name") or "") == asset_name), None)
    if not asset:
        raise RuntimeError(
            f"Release {release.get('tag_name') or version} has no exact {profile} OKF {archive_format} asset: {asset_name}"
        )
    target = (destination or Path(asset_name)).expanduser().resolve()
    if target.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite existing file: {target}; pass --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    download_url(str(asset["browser_download_url"]), target, user_agent)

    actual = sha256_bytes(target.read_bytes())
    checksum_digest = expected_asset_checksum(assets, asset_name, user_agent)
    github_digest = str(asset.get("digest") or "")
    github_digest = github_digest.removeprefix("sha256:") if github_digest.startswith("sha256:") else ""
    expected_digests = [value for value in (checksum_digest, github_digest) if value]
    if not expected_digests:
        target.unlink(missing_ok=True)
        raise RuntimeError(f"Release asset {asset_name} has no published SHA-256 verification evidence")
    if any(not SHA256_RE.fullmatch(value) or value != actual for value in expected_digests):
        target.unlink(missing_ok=True)
        raise RuntimeError(f"Checksum mismatch for {asset_name}")
    return {
        "schema": "rock-kb-okf-download-v1",
        "status": "ok",
        "version": resolved_version,
        "profile": profile,
        "release_url": release.get("html_url") or "",
        "asset": asset_name,
        "destination": str(target),
        "bytes": target.stat().st_size,
        "sha256": actual,
        "checksum_verified": True,
        "checksum_sources": [
            source
            for source, value in (("checksum_asset", checksum_digest), ("github_asset_digest", github_digest))
            if value
        ],
    }


def inspect_okf(path: Path) -> dict:
    files = read_bundle(path)
    manifest = optional_manifest(files)
    root_meta = parse_frontmatter(files.get("index.md", b"").decode("utf-8", errors="replace"))
    markdown_files = sum(1 for name in files if name.endswith(".md"))
    return {
        "schema": "rock-kb-okf-inspection-v1",
        "status": "ok",
        "path": str(path.expanduser().resolve()),
        "okf_version": manifest.get("okf_version") or root_meta.get("okf_version"),
        "distribution_version": manifest.get("distribution_version") or root_meta.get("distribution_version"),
        "profile": manifest.get("profile") or root_meta.get("profile"),
        "generated_at": manifest.get("generated_at") or root_meta.get("timestamp"),
        "source_commit": manifest.get("source_commit") or root_meta.get("source_commit"),
        "read_only": manifest.get("read_only"),
        "counts": manifest.get("counts") or {},
        "markdown_files": manifest.get("markdown_files", markdown_files),
        "relationships": manifest.get("relationships"),
        "archive_entries": len(files),
        "rock_distribution": bool(manifest),
    }


def conform_okf(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        files = read_bundle(path)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        return conformance_report(path, [str(exc)], [])

    names = set(files)
    markdown_count = 0
    declared_versions: set[str] = set()
    for relative, content in sorted(files.items()):
        if not relative.endswith(".md"):
            continue
        markdown_count += 1
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{relative} is not valid UTF-8")
            continue
        name = PurePosixPath(relative).name
        metadata = parse_frontmatter(text)
        if name not in RESERVED_FILENAMES and not metadata.get("type"):
            errors.append(f"{relative} missing parseable non-empty type frontmatter")
        version = str(metadata.get("okf_version") or "").strip()
        if version:
            declared_versions.add(version)
        for target in markdown_targets(text):
            resolved = resolve_target(relative, target)
            if resolved and resolved not in names and not any(
                item.startswith(f"{resolved.rstrip('/')}/") for item in names
            ):
                warnings.append(f"{relative} has unresolved link: {target[:500]}")
    if markdown_count == 0:
        errors.append("bundle contains no Markdown knowledge files")
    for version in sorted(declared_versions - {"0.1"}):
        warnings.append(f"bundle declares unknown OKF version: {version}")
    return conformance_report(path, sorted(set(errors)), sorted(set(warnings)), markdown_count)


def verify_okf(path: Path) -> dict:
    conformance = conform_okf(path)
    errors = list(conformance["errors"])
    warnings = list(conformance["warnings"])
    unresolved = [warning for warning in warnings if " has unresolved link: " in warning]
    errors.extend(unresolved)
    warnings = [warning for warning in warnings if warning not in unresolved]
    try:
        files = read_bundle(path)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        return validation_report(path, sorted(set([*errors, str(exc)])), warnings)

    try:
        manifest = load_manifest(files)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        manifest = {}
        errors.append(str(exc))
    if manifest:
        if manifest.get("schema") != "rock-kb-okf-distribution-v1":
            errors.append(f"{MANIFEST_NAME} has unexpected schema")
        if str(manifest.get("okf_version") or "") != "0.1":
            errors.append(f"{MANIFEST_NAME} must declare okf_version 0.1")
        if manifest.get("okf_profile") != "rock-kb-okf-profile-v1":
            errors.append(f"{MANIFEST_NAME} has unexpected OKF extension profile")
        if manifest.get("okf_spec_commit") != OKF_SPEC_COMMIT:
            errors.append(f"{MANIFEST_NAME} has unexpected upstream OKF specification commit")
        if manifest.get("profile") not in {"full", "core"}:
            errors.append(f"{MANIFEST_NAME} must declare profile full or core")
        if manifest.get("read_only") is not True:
            errors.append(f"{MANIFEST_NAME} must declare read_only true")
        license_info = manifest.get("license") if isinstance(manifest.get("license"), dict) else {}
        if license_info.get("code") != "MIT" or license_info.get("original_content") != "CC-BY-4.0":
            errors.append(f"{MANIFEST_NAME} has incomplete distribution licensing")

    root_index = files.get("index.md")
    if root_index is None:
        errors.append("missing index.md")
    else:
        root_meta = parse_frontmatter(root_index.decode("utf-8", errors="replace"))
        if str(root_meta.get("okf_version") or "") != "0.1":
            errors.append("index.md must declare okf_version 0.1")
    for required in (
        "log.md",
        "profile.md",
        "LICENSE.txt",
        "NOTICE.txt",
        "relationships.jsonl",
        FILE_MANIFEST_NAME,
    ):
        if required not in files:
            errors.append(f"missing {required}")

    structured_paths: set[str] = set()
    for relative, content in sorted(files.items()):
        if relative.endswith(".md"):
            text = content.decode("utf-8", errors="replace")
            name = PurePosixPath(relative).name
            if name in RESERVED_FILENAMES:
                if relative != "index.md" and text.startswith("---\n"):
                    errors.append(f"reserved file must not have frontmatter: {relative}")
                if name == "log.md":
                    for line in text.splitlines():
                        if line.startswith("## ") and not LOG_DATE_RE.match(line):
                            errors.append(f"{relative} has non-ISO date heading: {line}")
            elif relative != "profile.md":
                metadata = parse_frontmatter(text)
                record_path = str(metadata.get("structured_record") or "").lstrip("/")
                if metadata.get("type") != "Reference" and not record_path:
                    errors.append(f"{relative} missing structured_record")
                elif record_path and record_path not in files:
                    errors.append(f"{relative} has missing structured record: {record_path}")
                elif record_path:
                    if record_path in structured_paths:
                        errors.append(f"duplicate structured record reference: {record_path}")
                    structured_paths.add(record_path)
                    try:
                        record = json.loads(files[record_path].decode("utf-8"))
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        errors.append(f"{record_path} is not valid structured-record JSON")
                    else:
                        if not isinstance(record, dict) or record.get("schema") != "rock-kb-okf-structured-record-v1":
                            errors.append(f"{record_path} has unexpected structured-record schema")
                        if str(record.get("canonical_id") or "") != str(
                            metadata.get("canonical_id") or metadata.get("id") or ""
                        ):
                            errors.append(f"{relative} canonical ID does not match {record_path}")
                for relationship in metadata.get("relationships") or []:
                    if isinstance(relationship, dict) and str(relationship.get("target") or "").lstrip("/") == relative:
                        errors.append(f"{relative} has self relationship")
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        lowered = text.lower()
        for marker in PRIVATE_MARKERS:
            if marker.lower() in lowered:
                errors.append(f"{relative} contains private marker: {marker}")

    record_files = {name for name in files if name.startswith("records/") and name.endswith(".json")}
    for relative in sorted(record_files - structured_paths):
        errors.append(f"unreferenced structured record: {relative}")

    if FILE_MANIFEST_NAME in files and manifest.get("file_manifest_sha256"):
        if sha256_bytes(files[FILE_MANIFEST_NAME]) != str(manifest["file_manifest_sha256"]):
            errors.append(f"{FILE_MANIFEST_NAME} does not match the manifest digest")
    if "relationships.jsonl" in files and manifest.get("relationships") is not None:
        relationship_count = sum(1 for line in files["relationships.jsonl"].splitlines() if line.strip())
        try:
            expected_relationships = int(manifest["relationships"])
        except (TypeError, ValueError):
            errors.append(f"{MANIFEST_NAME} relationships must be an integer")
        else:
            if relationship_count != expected_relationships:
                errors.append(
                    f"relationship count mismatch: expected {expected_relationships}, found {relationship_count}"
                )

    errors.extend(validate_checksums(files))
    if manifest.get("markdown_files") is not None:
        actual_markdown = sum(1 for name in files if name.endswith(".md"))
        try:
            expected_markdown = int(manifest["markdown_files"])
        except (TypeError, ValueError):
            errors.append(f"{MANIFEST_NAME} markdown_files must be an integer")
            expected_markdown = actual_markdown
        if expected_markdown != actual_markdown:
            errors.append(
                f"markdown file count mismatch: expected {manifest['markdown_files']}, found {actual_markdown}"
            )
    return validation_report(path, sorted(set(errors)), sorted(set(warnings)), manifest)


# Backward-compatible strict verifier name retained for existing agents.
validate_okf = verify_okf


def conformance_report(
    path: Path,
    errors: list[str],
    warnings: list[str],
    markdown_files: int = 0,
) -> dict:
    return {
        "schema": "rock-kb-okf-conformance-v1",
        "status": "ok" if not errors else "failed",
        "path": str(path.expanduser().resolve()),
        "markdown_files": markdown_files,
        "errors": errors,
        "warnings": warnings,
    }


def validation_report(
    path: Path,
    errors: list[str],
    warnings: list[str] | None = None,
    manifest: dict | None = None,
) -> dict:
    return {
        "schema": "rock-kb-okf-validation-v1",
        "status": "ok" if not errors else "failed",
        "path": str(path.expanduser().resolve()),
        "okf_version": (manifest or {}).get("okf_version"),
        "distribution_version": (manifest or {}).get("distribution_version"),
        "profile": (manifest or {}).get("profile"),
        "errors": errors,
        "warnings": warnings or [],
    }


def release_metadata(version: str, user_agent: str) -> dict:
    endpoint = (
        f"{GITHUB_RELEASES_API}/latest"
        if version == "latest"
        else f"{GITHUB_RELEASES_API}/tags/rock-kb-v{version.removeprefix('rock-kb-v')}"
    )
    req = request.Request(endpoint, headers={"user-agent": user_agent, "accept": "application/vnd.github+json"})
    with request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def download_url(url: str, destination: Path, user_agent: str) -> None:
    req = request.Request(url, headers={"user-agent": user_agent, "accept": "application/octet-stream"})
    written = 0
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as response, destination.open("wb") as handle:
            while chunk := response.read(1024 * 1024):
                written += len(chunk)
                if written > MAX_DOWNLOAD_BYTES:
                    raise ValueError(f"OKF download exceeds {MAX_DOWNLOAD_BYTES} bytes")
                handle.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise


def expected_asset_checksum(assets: list[dict], asset_name: str, user_agent: str) -> str:
    checksum_name = asset_name.removesuffix(".zip").removesuffix(".tar.gz") + ".sha256"
    checksum_asset = next(
        (item for item in assets if str(item.get("name") or "") == checksum_name),
        None,
    )
    if not checksum_asset:
        return ""
    req = request.Request(str(checksum_asset["browser_download_url"]), headers={"user-agent": user_agent})
    with request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
        text = response.read().decode("utf-8")
    for line in text.splitlines():
        if line.endswith(f"  {asset_name}"):
            return line.split("  ", 1)[0]
    return ""


def read_bundle(path: Path) -> dict[str, bytes]:
    resolved = path.expanduser().resolve()
    if resolved.is_dir():
        raw: dict[str, bytes] = {}
        total = 0
        for item in sorted(resolved.rglob("*")):
            if item.is_symlink():
                raise ValueError(f"Bundle contains unsupported symlink: {item.relative_to(resolved)}")
            if not item.is_file():
                continue
            relative = item.relative_to(resolved).as_posix()
            validate_archive_name(relative)
            size = item.stat().st_size
            total = checked_size(relative, size, total)
            raw[relative] = item.read_bytes()
            check_entry_count(len(raw))
        return raw
    if zipfile.is_zipfile(resolved):
        with zipfile.ZipFile(resolved) as archive:
            raw = {}
            total = 0
            infos = [info for info in archive.infolist() if not info.is_dir()]
            check_entry_count(len(infos))
            for info in infos:
                validate_archive_name(info.filename)
                if info.filename in raw:
                    raise ValueError(f"Archive contains duplicate path: {info.filename}")
                if info.flag_bits & 0x1:
                    raise ValueError(f"Archive contains encrypted entry: {info.filename}")
                total = checked_size(info.filename, info.file_size, total)
                if info.file_size > 1024 * 1024 and info.file_size / max(info.compress_size, 1) > MAX_COMPRESSION_RATIO:
                    raise ValueError(f"Archive entry exceeds compression ratio limit: {info.filename}")
                raw[info.filename] = archive.read(info)
            return normalize_archive_root(raw)
    if tarfile.is_tarfile(resolved):
        with tarfile.open(resolved, "r:*") as archive:
            raw = {}
            total = 0
            members = [member for member in archive.getmembers() if not member.isdir()]
            check_entry_count(len(members))
            declared_size = sum(member.size for member in members if member.isfile())
            if declared_size > 1024 * 1024 and declared_size / max(resolved.stat().st_size, 1) > MAX_COMPRESSION_RATIO:
                raise ValueError("Tar archive exceeds compression ratio limit")
            for member in members:
                validate_archive_name(member.name)
                if member.name in raw:
                    raise ValueError(f"Archive contains duplicate path: {member.name}")
                if not member.isfile():
                    raise ValueError(f"Archive contains unsupported non-file entry: {member.name}")
                total = checked_size(member.name, member.size, total)
                extracted = archive.extractfile(member)
                if extracted is None:
                    raise ValueError(f"Could not read archive entry: {member.name}")
                raw[member.name] = extracted.read(MAX_FILE_BYTES + 1)
                if len(raw[member.name]) != member.size:
                    raise ValueError(f"Archive entry size mismatch: {member.name}")
            return normalize_archive_root(raw)
    raise ValueError(f"Unsupported OKF bundle path: {resolved}")


def check_entry_count(count: int) -> None:
    if count > MAX_ARCHIVE_ENTRIES:
        raise ValueError(f"Bundle has {count} files; maximum is {MAX_ARCHIVE_ENTRIES}")


def checked_size(name: str, size: int, current_total: int) -> int:
    if size > MAX_FILE_BYTES:
        raise ValueError(f"Bundle file exceeds {MAX_FILE_BYTES} bytes: {name}")
    total = current_total + size
    if total > MAX_TOTAL_UNCOMPRESSED:
        raise ValueError(f"Bundle exceeds {MAX_TOTAL_UNCOMPRESSED} uncompressed bytes")
    return total


def validate_archive_name(name: str) -> None:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "" in path.parts:
        raise ValueError(f"Archive contains unsafe path: {name}")


def normalize_archive_root(files: dict[str, bytes]) -> dict[str, bytes]:
    if not files:
        return {}
    paths = [PurePosixPath(name) for name in files]
    first_parts = {path.parts[0] for path in paths if path.parts}
    stripped_names = {PurePosixPath(*path.parts[1:]).as_posix() for path in paths if len(path.parts) > 1}
    strip_root = (
        len(first_parts) == 1
        and all(len(path.parts) > 1 for path in paths)
        and bool({"index.md", MANIFEST_NAME} & stripped_names)
    )
    normalized: dict[str, bytes] = {}
    for name, content in files.items():
        path = PurePosixPath(name)
        relative = PurePosixPath(*path.parts[1:]).as_posix() if strip_root else path.as_posix()
        if relative in normalized:
            raise ValueError(f"Archive normalizes to duplicate path: {relative}")
        normalized[relative] = content
    return normalized


def optional_manifest(files: dict[str, bytes]) -> dict:
    try:
        return load_manifest(files)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


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
    errors: list[str] = []
    seen: set[str] = set()
    try:
        lines = files[CHECKSUMS_NAME].decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return [f"{CHECKSUMS_NAME} is not valid UTF-8"]
    for line in lines:
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid checksum row: {line}")
            continue
        if not SHA256_RE.fullmatch(expected):
            errors.append(f"invalid checksum digest: {line}")
            continue
        try:
            validate_archive_name(relative)
        except ValueError:
            errors.append(f"unsafe checksum target: {relative}")
            continue
        if relative in seen:
            errors.append(f"duplicate checksum target: {relative}")
            continue
        seen.add(relative)
        if relative not in files:
            errors.append(f"checksum target missing: {relative}")
        elif sha256_bytes(files[relative]) != expected:
            errors.append(f"checksum mismatch: {relative}")
    expected_paths = set(files) - {CHECKSUMS_NAME}
    for relative in sorted(expected_paths - seen):
        errors.append(f"file missing checksum: {relative}")
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
