from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from pydantic import ValidationError

from .concepts import load_concepts
from .extract import generated_at_iso
from .jsonl import write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, REPO_ROOT
from .schemas.recipe import RecipeRow


RECIPE_DIR = REPO_ROOT / "recipes"
RECIPE_OUTPUT = AGENT_DIR / "recipes.jsonl"
RECIPE_SUMMARY = AGENT_DIR / "recipe-summary.json"
RECIPE_KNOWLEDGE_DIR = KNOWLEDGE_DIR / "recipes"
SAFE_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def recipe_paths(root: Path | None = None) -> list[Path]:
    return sorted((root or RECIPE_DIR).glob("*/*.json"))


def load_recipes(root: Path | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in recipe_paths(root):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            row = RecipeRow.model_validate(raw).public_dump()
        except (json.JSONDecodeError, ValidationError) as exc:
            errors.append(f"{relative(path)}: {exc}")
            continue
        errors.extend(validate_recipe(row, path))
        rows.append(row)
    ids = [str(row["recipe_id"]) for row in rows]
    duplicate_ids = sorted({recipe_id for recipe_id in ids if ids.count(recipe_id) > 1})
    if duplicate_ids:
        errors.append(f"duplicate recipe_id values: {', '.join(duplicate_ids)}")
    if errors:
        raise ValueError("\n".join(errors))
    return sorted(rows, key=lambda row: str(row["recipe_id"]))


def validate_recipe(row: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    recipe_id = str(row.get("recipe_id") or "")
    org_id = str(row.get("org_id") or "")
    if not SAFE_SEGMENT.fullmatch(org_id):
        errors.append(f"{relative(path)}: invalid org_id {org_id!r}")
    if not recipe_id.startswith(f"{org_id}:") or not SAFE_SEGMENT.fullmatch(recipe_id.partition(":")[2]):
        errors.append(f"{relative(path)}: recipe_id must be <org-id>:<slug>")
    if path.parent.name != org_id:
        errors.append(f"{relative(path)}: org_id must match recipes/{path.parent.name}/")
    known_concepts = {concept.id for concept in load_concepts()}
    unknown = sorted(set(row.get("concept_ids") or []) - known_concepts)
    if unknown:
        errors.append(f"{relative(path)}: unknown concept_ids: {', '.join(unknown)}")
    implementation = row.get("implementation") or {}
    repository_url = str(implementation.get("repository_url") or "")
    parsed = urlparse(repository_url)
    owner = str(implementation.get("owner") or "")
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        errors.append(f"{relative(path)}: repository_url must be an HTTPS GitHub repository")
    repo_parts = [part for part in parsed.path.split("/") if part]
    if len(repo_parts) != 2 or repo_parts[0].lower() != owner.lower():
        errors.append(f"{relative(path)}: implementation owner must match the GitHub repository owner")
    commit = str(implementation.get("commit_sha") or "")
    immutable_fragment = f"/{commit}/"
    for field in ["manifest_url", "license_url"]:
        value = str(implementation.get(field) or "")
        if "raw.githubusercontent.com" not in value or immutable_fragment not in value:
            errors.append(f"{relative(path)}: {field} must be pinned to commit_sha")
    seen_files: set[str] = set()
    for item in implementation.get("files") or []:
        file_path = str(item.get("path") or "")
        if not file_path or file_path.startswith("/") or ".." in Path(file_path).parts:
            errors.append(f"{relative(path)}: unsafe implementation file path {file_path!r}")
        if file_path in seen_files:
            errors.append(f"{relative(path)}: duplicate implementation file {file_path}")
        seen_files.add(file_path)
    security = row.get("security") or {}
    if security.get("data_access") == "read_only" and security.get("csrf_required"):
        errors.append(f"{relative(path)}: read-only recipes should not claim CSRF is required")
    expected_tier = "community-reviewed" if row.get("review_status") == "community_reviewed" else "community-unreviewed"
    if row.get("authority_tier") != expected_tier:
        errors.append(f"{relative(path)}: authority_tier does not match review_status")
    return errors


def build_recipes() -> dict[str, Any]:
    rows = load_recipes()
    RECIPE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(RECIPE_OUTPUT, rows)
    if RECIPE_KNOWLEDGE_DIR.exists():
        for path in RECIPE_KNOWLEDGE_DIR.glob("*/*.md"):
            path.unlink()
    for row in rows:
        org_id, slug = str(row["recipe_id"]).split(":", 1)
        target = RECIPE_KNOWLEDGE_DIR / org_id / f"{slug}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_recipe(row), encoding="utf-8")
    summary = {
        "schema": "rock-kb-recipe-summary-v1",
        "generated_at": generated_at_iso(),
        "recipe_count": len(rows),
        "review_statuses": counts(rows, "review_status"),
        "recipe_kinds": counts(rows, "recipe_kind"),
        "org_ids": counts(rows, "org_id"),
        "artifact": "agent/recipes.jsonl",
    }
    RECIPE_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_recipe(row: dict[str, Any]) -> str:
    implementation = row["implementation"]
    security = row["security"]
    compatibility = row["compatibility"]
    lines = [
        f"# {row['title']}", "", row["summary"], "",
        f"- Recipe ID: `{row['recipe_id']}`",
        f"- Community status: `{row['authority_tier']}`",
        f"- Version: `{row['version']}`",
        f"- Source commit: [`{implementation['commit_sha'][:12]}`]({implementation['repository_url']}/tree/{implementation['commit_sha']}/{implementation['source_path']})",
        f"- License: [{implementation['license']}]({implementation['license_url']})", "",
        "## Use Cases", "", *[f"- {value}" for value in row["use_cases"]], "",
        "## Adaptation Points", "", *[f"- `{item['key']}`: {item['description']}" for item in row["adaptation_points"]], "",
        "## Implementation", "", *[f"{index}. {value}" for index, value in enumerate(row["instructions"], 1)], "",
        "## Validate", "", *[f"{index}. {value}" for index, value in enumerate(row["validation_steps"], 1)], "",
        "## Security", "",
        f"- Data access: `{security['data_access']}`",
        f"- Authentication: {security['authentication']}",
        f"- Authorization: {security['authorization']}",
        f"- Handles sensitive data: `{str(security['handles_sensitive_data']).lower()}`",
        *[f"- {value}" for value in security["notes"]], "",
        "## Compatibility", "",
        f"- Tested Rock versions: {', '.join(compatibility['tested_rock_versions']) or 'Not declared'}",
        f"- Last verified: {compatibility.get('last_verified_at') or 'Not declared'}",
        *[f"- Rock `{item['rock_version']}`: `{item['status']}`" + (f" - {' '.join(item['notes'])}" if item['notes'] else "") for item in compatibility.get("version_matrix") or []],
        *[f"- {value}" for value in compatibility["notes"]], "",
        "## Community Verification", "",
        *render_attestations(row.get("verification_attestations") or []),
        *( [f"- Feedback and issues: {row['feedback_url']}"] if row.get("feedback_url") else []), "",
        "## Reusable Learnings", "", *[f"- {value}" for value in row["learnings"]], "",
        "## Limitations", "", *[f"- {value}" for value in row["known_limitations"]], "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_attestations(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["- No consumer verification attestations have been submitted yet."]
    return [
        f"- `{row['org_id']}` on Rock `{row['rock_version']}`: `{row['outcome']}` ({row['scope']}, {row['verified_at']})"
        for row in rows
    ]


def check_recipe_upstreams() -> dict[str, Any]:
    results = []
    for row in load_recipes():
        implementation = row["implementation"]
        process = subprocess.run(
            ["git", "ls-remote", "--symref", implementation["repository_url"], "HEAD"],
            capture_output=True, text=True, check=False, timeout=30,
        )
        default_branch = ""
        default_commit = ""
        for line in process.stdout.splitlines():
            match = re.match(r"ref: refs/heads/(\S+)\s+HEAD$", line)
            if match:
                default_branch = match.group(1)
                continue
            match = re.match(r"([0-9a-f]{40})\s+HEAD$", line)
            if match:
                default_commit = match.group(1)
        owner, repository = repository_parts(implementation["repository_url"])
        changed_files: list[str] = []
        unavailable_files: list[str] = []
        if default_branch and owner and repository:
            for item in implementation["files"]:
                source_path = f"{implementation['source_path'].rstrip('/')}/{item['path']}"
                source_ref = default_commit or f"refs/heads/{default_branch}"
                url = f"https://raw.githubusercontent.com/{owner}/{repository}/{source_ref}/{source_path}"
                try:
                    request = Request(url, headers={"User-Agent": "rock-agent-kb-recipe-check/1.0"})
                    with urlopen(request, timeout=30) as response:
                        digest = hashlib.sha256(response.read()).hexdigest()
                    if digest != item["sha256"]:
                        changed_files.append(item["path"])
                except (HTTPError, URLError, TimeoutError):
                    unavailable_files.append(item["path"])
        if not default_branch or not owner or not repository:
            status = "unavailable"
        elif unavailable_files and len(unavailable_files) == len(implementation["files"]):
            status = "not_on_default_branch"
        elif unavailable_files:
            status = "unavailable"
        elif changed_files:
            status = "upstream_changed"
        else:
            status = "current"
        results.append({
            "recipe_id": row["recipe_id"],
            "pinned_commit": implementation["commit_sha"],
            "default_branch": default_branch,
            "status": status,
            "changed_files": changed_files,
            "unavailable_files": unavailable_files,
        })
    return {"schema": "rock-kb-recipe-upstream-check-v1", "results": results}


def verify_recipe(recipe_id: str, rock_version: str | None = None) -> dict[str, Any]:
    row = next((item for item in load_recipes() if item["recipe_id"] == recipe_id), None)
    if row is None:
        raise ValueError(f"unknown recipe_id: {recipe_id}")
    implementation = row["implementation"]
    owner, repository = repository_parts(implementation["repository_url"])
    file_checks = []
    for item in implementation["files"]:
        source_path = f"{implementation['source_path'].rstrip('/')}/{item['path']}"
        url = f"https://raw.githubusercontent.com/{owner}/{repository}/{implementation['commit_sha']}/{source_path}"
        try:
            actual = fetch_url_digest(url)
            status = "pass" if actual == item["sha256"] else "fail"
        except (HTTPError, URLError, TimeoutError):
            actual = None
            status = "unavailable"
        file_checks.append(
            {
                "path": item["path"],
                "status": status,
                "expected_sha256": item["sha256"],
                "actual_sha256": actual,
            }
        )
    compatibility = recipe_compatibility_check(row, rock_version)
    failed = any(item["status"] == "fail" for item in file_checks) or compatibility["status"] == "fail"
    unavailable = any(item["status"] == "unavailable" for item in file_checks)
    status = "fail" if failed else "unavailable" if unavailable else "pass"
    verifier_files = [
        item["path"]
        for item in implementation["files"]
        if item["path"].startswith("tests/") or item["path"].endswith(".sql")
    ]
    return {
        "schema": "rock-kb-recipe-verification-v1",
        "status": status,
        "recipe_id": recipe_id,
        "recipe_version": row["version"],
        "pinned_commit": implementation["commit_sha"],
        "compatibility": compatibility,
        "file_checks": file_checks,
        "verifier_files": verifier_files,
        "prerequisite_count": len(row.get("prerequisites") or []),
        "validation_step_count": len(row.get("validation_steps") or []),
        "attestation_count": len(row.get("verification_attestations") or []),
        "safety": "Verification is read-only and does not execute community recipe code or modify a Rock instance.",
    }


def fetch_url_digest(url: str) -> str:
    request = Request(url, headers={"User-Agent": "rock-agent-kb-recipe-verify/1.0"})
    with urlopen(request, timeout=30) as response:
        return hashlib.sha256(response.read()).hexdigest()


def recipe_compatibility_check(row: dict[str, Any], rock_version: str | None) -> dict[str, Any]:
    if not rock_version:
        return {"status": "not_checked", "rock_version": None, "declared": row["compatibility"]}
    compatibility = row["compatibility"]
    matrix = {str(item["rock_version"]): item for item in compatibility.get("version_matrix") or []}
    matrix_row = matrix.get(str(rock_version))
    if matrix_row:
        status = "fail" if matrix_row["status"] == "unsupported" else "pass" if matrix_row["status"] == "verified" else "warn"
        return {"status": status, "rock_version": rock_version, "declaration": matrix_row}
    if str(rock_version) in {str(value) for value in compatibility.get("tested_rock_versions") or []}:
        return {"status": "pass", "rock_version": rock_version, "declaration": {"status": "verified"}}
    minimum = compatibility.get("minimum_rock_version")
    maximum = compatibility.get("maximum_rock_version")
    if minimum and version_key(rock_version) < version_key(str(minimum)):
        return {"status": "fail", "rock_version": rock_version, "reason": f"below minimum Rock version {minimum}"}
    if maximum and version_key(rock_version) > version_key(str(maximum)):
        return {"status": "fail", "rock_version": rock_version, "reason": f"above maximum Rock version {maximum}"}
    return {"status": "warn", "rock_version": rock_version, "reason": "version is in the declared range but lacks a verification attestation"}


def version_key(value: str) -> tuple[int, ...]:
    parts = [int(part) for part in re.findall(r"\d+", value)]
    return tuple(parts or [0])


def promote_recipe_contribution(bundle_path: Path, recipe_id: str, overwrite: bool = False) -> dict[str, Any]:
    from .contributions import validate_contribution_file

    errors = validate_contribution_file(bundle_path)
    if errors:
        raise ValueError("\n".join(errors))
    contribution = None
    for line in bundle_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            candidate = json.loads(line)
            if candidate.get("contribution_id") == recipe_id:
                contribution = candidate
                break
    if contribution is None or contribution.get("contribution_type") != "recipe":
        raise ValueError(f"recipe contribution not found: {recipe_id}")
    row = dict(contribution["recipe"])
    row["review_status"] = "community_reviewed"
    row["authority_tier"] = "community-reviewed"
    org_id, slug = recipe_id.split(":", 1)
    target = RECIPE_DIR / org_id / f"{slug}.json"
    if target.exists() and not overwrite:
        raise ValueError(f"{relative(target)} already exists; pass --overwrite to replace it")
    RecipeRow.model_validate(row)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    load_recipes()
    return {"status": "ok", "recipe_id": recipe_id, "path": relative(target)}


def counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "")
        result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items()))


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def repository_parts(repository_url: str) -> tuple[str, str]:
    parts = [part for part in urlparse(repository_url).path.split("/") if part]
    if len(parts) != 2:
        return "", ""
    return parts[0], parts[1].removesuffix(".git")
