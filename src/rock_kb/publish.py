from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml

from .extract import generated_at_iso, grep_sensitive_values, sha256_text
from .contributions import EXAMPLE_BUNDLE_SUFFIX, validate_contribution_file
from .jsonl import read_jsonl
from .paths import PUBLIC_EXPORT_DIR, REPO_ROOT
from .sources import load_sources

PUBLIC_PATHS = [
    "claims/approved-claims.jsonl",
    "community-contributions",
    "docs/runbooks/contributor-reviewer-workflow.md",
    "docs/runbooks/rock-issue-intelligence.md",
    "docs/runbooks/rock-ideas-intelligence.md",
    "docs/specs/rock-issue-intelligence-v1.md",
    "docs/community-recipes.md",
    "docs/prompts/media-claim-distillation-v1.md",
    "docs/prompts/source-claim-distillation-v1.md",
    "docs/prompts/rock-issue-investigation-v1.md",
    "docs/decisions/public-export-policy.md",
    "docs/runbooks/public-publish-runbook.md",
    "docs/templates/rock-kb-agent/SKILL.md",
    "sources/registry.yaml",
    "concepts/registry.yaml",
    "knowledge/README.md",
    "source-suggestions/README.md",
    "knowledge/concepts",
    "knowledge/model-map",
    "knowledge/recipes",
    "knowledge/issues",
    "knowledge/ideas",
    "issues",
    "recipes",
    "agent/README.md",
    "agent/concept-index.jsonl",
    "agent/concept-release-caveats.jsonl",
    "agent/concept-task-cards.jsonl",
    "agent/entity-index.jsonl",
    "agent/llms.txt",
    "agent/release-index.jsonl",
    "agent/rock-kb-manifest.json",
    "agent/section-source-map.jsonl",
    "agent/section-status.jsonl",
    "agent/source-summary-report.json",
    "agent/source-summaries.jsonl",
    "agent/source-citations.jsonl",
    "agent/model-map-summary.json",
    "agent/model-map-entities.jsonl",
    "agent/model-map-properties.jsonl",
    "agent/model-map-methods.jsonl",
    "agent/model-map-version-diff.jsonl",
    "agent/model-map-digests.jsonl",
    "agent/lava-capabilities.jsonl",
    "agent/lava-capability-summary.json",
    "agent/lava-contexts.jsonl",
    "agent/lava-context-summary.json",
    "agent/recipes.jsonl",
    "agent/recipe-summary.json",
    "agent/rock-issues.jsonl",
    "agent/rock-issue-enrichments.jsonl",
    "agent/rock-issue-summary.json",
    "agent/rock-ideas.jsonl",
    "agent/rock-idea-relationships.jsonl",
    "agent/rock-idea-verification-queue.jsonl",
    "agent/rock-idea-summary.json",
    "agent/answer-pack.jsonl",
    "agent/live-inspection-checklists.jsonl",
    "agent/live-probe-recipes.jsonl",
    "agent/distilled-claims.jsonl",
    "agent/source-authority-rules.jsonl",
    "agent/claim-review-dashboard.md",
    "agent/claim-review-queue.jsonl",
    "agent/source-conflicts.jsonl",
    "agent/evaluation-report.json",
    "agent/evaluation-results.jsonl",
    "agent/evaluation-set.jsonl",
    "contributions",
]

PUBLIC_VIRTUAL_FILES = {
    "README.md": "docs/public-repo-readme.md",
}

PUBLIC_INTERNAL_AGENT_ENTRYPOINTS = {
    "private_media",
}

PRIVATE_PATH_PREFIXES = [
    "data/raw-manifests/",
    "data/normalized/",
    "data/review/",
    "data/media/",
    "data/index/",
    ".git/",
    ".venv/",
]

DISALLOWED_PUBLIC_JSON_FIELDS = {
    "private_corpus_pointer",
    "full_text",
    "raw_html",
    "html",
    "transcript",
    "derived_from_private_transcript",
    "markdown",
    "content",
}

FORBIDDEN_PUBLIC_TEXT_PATTERNS = {
    "/Users/": "absolute local user path",
    "local://": "local-only URI",
    "RockProduction": "private/local RockProduction reference",
    "RockDB": "connected database name",
    "mcp_readonly": "connected database login",
    "oneall-rockdb": "connected database evidence id",
    "ONE&ALL's Rock production": "connected production instance reference",
    "SiteId = 14": "instance-specific mobile site id",
    "brian.davis@": "personal account marker",
}

PUBLIC_EXCLUDED_FILENAMES = {
    ".DS_Store",
    "guide-dependencies.json",
    "guide-quality.json",
}

PRIVATE_PROVENANCE_JSON_FIELDS = {
    "change_jsonl_path",
    "path",
    "source_path",
}


def public_export_manifest() -> dict[str, Any]:
    files_by_path = {}
    for public_path, source_path in iter_public_file_entries():
        text = public_export_text_for_path(source_path)
        files_by_path[public_path] = {
            "path": public_path,
            "bytes": len(text.encode("utf-8")),
            "sha256": sha256_text(text),
        }
    return {
        "schema": "rock-kb-public-export-v1",
        "generated_at": generated_at_iso(),
        "source_policy": source_policy_summary(),
        "files": sorted(files_by_path.values(), key=lambda row: row["path"]),
    }


def build_public_export(destination: Optional[Path] = None) -> dict[str, Any]:
    destination = destination or PUBLIC_EXPORT_DIR
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    manifest = public_export_manifest()
    errors = audit_public_export_manifest(manifest)
    if errors:
        return {"status": "failed", "errors": errors, "destination": str(destination)}

    for row in manifest["files"]:
        dst = destination / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(public_export_text_for_public_path(str(row["path"])), encoding="utf-8")
    manifest_path = destination / "public-export-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "ok",
        "destination": str(destination),
        "manifest_path": str(manifest_path),
        "files": len(manifest["files"]),
    }


def audit_public_export_manifest(manifest: Optional[dict[str, Any]] = None) -> list[str]:
    manifest = manifest or public_export_manifest()
    errors = []
    for row in manifest.get("files") or []:
        path = str(row.get("path") or "")
        if is_private_path(path):
            errors.append(f"{path} is private/raw working data and cannot be exported publicly")
            continue
        file_path = public_export_source_path(path)
        if not file_path.exists():
            errors.append(f"{path} is missing")
            continue
        text = public_export_text_for_path(file_path)
        for finding in grep_sensitive_values(text.splitlines()):
            errors.append(f"{path} contains sensitive-looking value: {finding[:120]}")
        errors.extend(audit_forbidden_public_text(path, text))
        if Path(path).suffix.lower() in {".json", ".jsonl"}:
            errors.extend(audit_json_public_fields(path, text))
            errors.extend(audit_json_public_traceability(path, text))
        if path.startswith("contributions/") and Path(path).suffix.lower() == ".jsonl" and not Path(path).name.endswith(EXAMPLE_BUNDLE_SUFFIX):
            errors.extend(validate_contribution_file(file_path))
        if path.startswith("claims/") and Path(path).name == "approved-claims.jsonl":
            from .claims import validate_claim_rows

            errors.extend(validate_claim_rows(read_jsonl_text(text), public=True, label=path))
    errors.extend(audit_agent_entrypoint_coverage())
    return errors


def audit_agent_entrypoint_coverage() -> list[str]:
    from .concepts import REQUIRED_AGENT_ENTRYPOINT_FILES, load_concepts

    errors = []
    for concept in load_concepts():
        concept_dir = REPO_ROOT / "knowledge" / "concepts" / concept.id
        for filename in REQUIRED_AGENT_ENTRYPOINT_FILES:
            path = concept_dir / filename
            if not path.exists():
                errors.append(f"knowledge/concepts/{concept.id}/{filename} is missing required agent entrypoint")
    manifest_path = REPO_ROOT / "agent" / "rock-kb-manifest.json"
    if not manifest_path.exists():
        errors.append("agent/rock-kb-manifest.json is missing")
        return errors
    try:
        manifest = json.loads(public_export_text_for_path(manifest_path))
    except json.JSONDecodeError:
        return errors + ["agent/rock-kb-manifest.json is invalid JSON"]
    manifest_rows = {row.get("concept_id"): row for row in manifest.get("concepts") or []}
    entrypoints = manifest.get("agent_entrypoints") or {}
    if not entrypoints.get("source_summaries"):
        errors.append("agent/rock-kb-manifest.json missing source_summaries entrypoint")
    if not entrypoints.get("source_summary_report"):
        errors.append("agent/rock-kb-manifest.json missing source_summary_report entrypoint")
    if not entrypoints.get("approved_claims"):
        errors.append("agent/rock-kb-manifest.json missing approved_claims entrypoint")
    for field in [
        "answer_pack",
        "live_checklists",
        "live_probe_recipes",
        "distilled_claims",
        "source_authority_rules",
        "rock_issues",
        "rock_issue_summary",
        "rock_issue_directory",
        "rock_issue_investigation_prompt",
        "rock_ideas",
        "rock_idea_relationships",
        "rock_idea_verification_queue",
        "rock_idea_summary",
        "rock_idea_directory",
    ]:
        if not entrypoints.get(field):
            errors.append(f"agent/rock-kb-manifest.json missing {field} entrypoint")
    if not (manifest.get("source_summaries") or {}).get("path"):
        errors.append("agent/rock-kb-manifest.json missing source_summaries path")
    if not (manifest.get("source_summaries") or {}).get("report"):
        errors.append("agent/rock-kb-manifest.json missing source_summaries report")
    for field in [
        "model_map",
        "model_map_summary",
        "model_map_entities",
        "model_map_properties",
        "model_map_version_diff",
        "model_map_model_details",
        "lava_capabilities",
        "lava_capability_summary",
        "lava_contexts",
        "lava_context_summary",
        "lava_context_directory",
        "lava_reference_index",
        "lava_safety_matrix",
        "lava_agent_usage_examples",
    ]:
        if not entrypoints.get(field):
            errors.append(f"agent/rock-kb-manifest.json missing {field} entrypoint")
    if not (manifest.get("approved_claims") or {}).get("path"):
        errors.append("agent/rock-kb-manifest.json missing approved_claims path")
    for concept in load_concepts():
        row = manifest_rows.get(concept.id)
        if not row:
            errors.append(f"agent/rock-kb-manifest.json missing concept {concept.id}")
            continue
        for field in ["quickstart", "task_cards", "entities", "release_caveats", "section_source_map", "section_status", "troubleshooting_tree", "open_questions"]:
            if not row.get(field):
                errors.append(f"agent/rock-kb-manifest.json concept {concept.id} missing {field}")
        for field in ["approved_claims", "approved_media", "live_inspection_checklist", "live_probe_recipes", "answers"]:
            if not row.get(field):
                errors.append(f"agent/rock-kb-manifest.json concept {concept.id} missing {field}")
    return errors


def audit_source_policy() -> list[str]:
    errors = []
    for source in load_sources():
        if source.public_publish_mode == "public_full_text_allowed" and not source.permits_full_text:
            errors.append(f"{source.id} allows public full text but extraction mode does not permit full text")
        if source.public_publish_mode == "private_only" and not source.requires_human_review:
            errors.append(f"{source.id} is private_only but does not require human review")
        if source.public_publish_mode in {"private_only", "manual_review_required"} and source.allowed_excerpt_chars != 0:
            errors.append(f"{source.id} should use allowed_excerpt_chars: 0 for {source.public_publish_mode}")
        if source.public_publish_mode == "public_cite_and_summarize_only" and source.allowed_excerpt_chars > 1000:
            errors.append(f"{source.id} cite-and-summarize excerpt limit is too high")
    return errors


def iter_public_files() -> Iterable[Path]:
    for _, source_path in iter_public_file_entries():
        yield source_path


def iter_public_file_entries() -> Iterable[tuple[str, Path]]:
    for public_path, source_rel in PUBLIC_VIRTUAL_FILES.items():
        yield public_path, REPO_ROOT / source_rel
    for rel in PUBLIC_PATHS:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        if path.is_file():
            if is_public_export_file(path):
                yield path.relative_to(REPO_ROOT).as_posix(), path
            continue
        for child in sorted(path.rglob("*")):
            if child.is_file() and is_public_export_file(child):
                yield child.relative_to(REPO_ROOT).as_posix(), child


def source_policy_summary() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source.id,
            "license_status": source.license_status,
            "allowed_extraction_mode": source.allowed_extraction_mode,
            "private_storage": source.private_storage,
            "public_publish_mode": source.public_publish_mode,
            "allowed_excerpt_chars": source.allowed_excerpt_chars,
            "requires_human_review": source.requires_human_review,
        }
        for source in load_sources()
        if is_public_source(source.raw)
    ]


def audit_json_public_fields(path: str, text: str) -> list[str]:
    errors = []
    rows = []
    if path.endswith(".jsonl"):
        rows = list(read_jsonl_text(text))
    else:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return [f"{path} is invalid JSON"]
        rows = payload if isinstance(payload, list) else [payload]
    for index, row in enumerate(rows):
        for field_path in disallowed_json_field_paths(row):
            errors.append(f"{path}:{index} contains disallowed public field: {field_path}")
    return errors


def audit_forbidden_public_text(path: str, text: str) -> list[str]:
    errors = []
    lower_text = text.lower()
    for pattern, reason in FORBIDDEN_PUBLIC_TEXT_PATTERNS.items():
        if pattern.lower() in lower_text:
            errors.append(f"{path} contains forbidden public marker ({reason}): {pattern}")
    return errors


def audit_json_public_traceability(path: str, text: str) -> list[str]:
    if not path.endswith(
        (
            "release-caveats.jsonl",
            "entity-index.jsonl",
            "entities.jsonl",
            "concept-task-cards.jsonl",
            "task-cards.jsonl",
            "agent-cards.jsonl",
            "section-source-map.jsonl",
            "section-status.jsonl",
            "lava-capabilities.jsonl",
            "lava-contexts.jsonl",
            "rock-issues.jsonl",
            "rock-ideas.jsonl",
            "rock-idea-relationships.jsonl",
            "rock-idea-verification-queue.jsonl",
        )
    ):
        return []
    errors = []
    for index, line in enumerate(text.splitlines()):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{path}:{index} is invalid JSONL")
            continue
        if not isinstance(row, dict):
            continue
        if path.endswith("release-caveats.jsonl") and not (row.get("source_url") or row.get("source_record_id")):
            errors.append(f"{path}:{index} release caveat has no source_url or source_record_id")
        if path.endswith(("entity-index.jsonl", "entities.jsonl")) and not (row.get("source_urls") or row.get("source_keys")):
            errors.append(f"{path}:{index} entity row has no source_urls or source_keys")
        if path.endswith(("concept-task-cards.jsonl", "task-cards.jsonl", "agent-cards.jsonl")) and not (row.get("source_urls") or row.get("source_keys")):
            errors.append(f"{path}:{index} task card has no source_urls or source_keys")
        structural_section_without_sources = row.get("section_id") in {
            "approved-claim-coverage",
            "approved-media-coverage",
        } and row.get("confidence") == "structural"
        if path.endswith("section-source-map.jsonl") and not (row.get("source_keys") or row.get("citations") or structural_section_without_sources):
            errors.append(f"{path}:{index} section source row has no source_keys or citations")
        if path.endswith("section-status.jsonl") and not (row.get("depends_on_sources") or row.get("section_id") in {"approved-claim-coverage", "approved-media-coverage"}):
            errors.append(f"{path}:{index} section status row has no depends_on_sources")
        if path.endswith("lava-capabilities.jsonl") and not (row.get("official_url") and row.get("source_record_id")):
            errors.append(f"{path}:{index} Lava capability row has no official_url or source_record_id")
        if path.endswith("lava-contexts.jsonl") and not (row.get("source_url") and row.get("source_file") and row.get("source_line_start")):
            errors.append(f"{path}:{index} Lava context row has no source_url, source_file, or source_line_start")
        if path.endswith("rock-issues.jsonl"):
            forbidden = sorted({"body", "comments", "users", "assignees", "timeline", "attachments"}.intersection(row))
            if forbidden:
                errors.append(f"{path}:{index} Rock issue row republishes forbidden raw fields: {', '.join(forbidden)}")
            required = ["issue_id", "source_id", "url", "body_sha256", "source_content_hash", "concept_ids"]
            missing = [field for field in required if not row.get(field)]
            if missing:
                errors.append(f"{path}:{index} Rock issue row has incomplete traceability: {', '.join(missing)}")
            if row.get("raw_content_policy") != "untrusted_not_republished":
                errors.append(f"{path}:{index} Rock issue row does not declare the raw-content boundary")
            if row.get("claim_tier") != "routing_context_only":
                errors.append(f"{path}:{index} Rock issue row must remain routing_context_only")
        if path.endswith("rock-ideas.jsonl"):
            forbidden = sorted({"author", "submitter", "organization", "description", "body", "response", "response_text", "comments"}.intersection(row))
            if forbidden:
                errors.append(f"{path}:{index} Rock idea row republishes forbidden raw fields: {', '.join(forbidden)}")
            required = ["idea_id", "source_id", "url", "content_hash", "concept_ids"]
            missing = [field for field in required if not row.get(field)]
            if missing:
                errors.append(f"{path}:{index} Rock idea row has incomplete traceability: {', '.join(missing)}")
            if row.get("claim_tier") != "routing_context_only":
                errors.append(f"{path}:{index} Rock idea row must remain routing_context_only")
        if path.endswith("rock-idea-relationships.jsonl"):
            forbidden = sorted(
                {"description", "body", "response", "response_text", "comments", "author", "submitter", "organization"}.intersection(row)
            )
            if forbidden:
                errors.append(
                    f"{path}:{index} Rock idea relationship republishes forbidden raw fields: {', '.join(forbidden)}"
                )
            required = [
                "relationship_id",
                "source_id",
                "relationship_type",
                "basis",
                "evidence_url",
                "authority_tier",
                "confidence",
                "content_hash",
            ]
            missing = [field for field in required if not row.get(field)]
            if missing:
                errors.append(
                    f"{path}:{index} Rock idea relationship has incomplete traceability: {', '.join(missing)}"
                )
            if not row.get("target_id") and not row.get("target_url"):
                errors.append(f"{path}:{index} Rock idea relationship has no target")
            if row.get("needs_live_verification") is not True:
                errors.append(f"{path}:{index} Rock idea relationship must require live verification")
        if path.endswith("rock-idea-verification-queue.jsonl"):
            forbidden = sorted(
                {"description", "body", "response", "response_text", "comments", "author", "submitter", "organization"}.intersection(row)
            )
            if forbidden:
                errors.append(
                    f"{path}:{index} Rock idea verification row republishes forbidden raw fields: {', '.join(forbidden)}"
                )
            required = [
                "queue_id",
                "idea_id",
                "url",
                "verification_state",
                "recommended_action",
                "source_content_hash",
                "review_input_hash",
                "content_hash",
            ]
            missing = [field for field in required if not row.get(field)]
            if missing:
                errors.append(
                    f"{path}:{index} Rock idea verification row has incomplete traceability: {', '.join(missing)}"
                )
            if row.get("needs_live_verification") is not True or row.get("claim_tier") != "routing_context_only":
                errors.append(f"{path}:{index} Rock idea verification row overstates verification authority")
    return errors


def disallowed_json_field_paths(value: Any, prefix: str = "$") -> list[str]:
    paths = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{prefix}.{key}"
            if key in DISALLOWED_PUBLIC_JSON_FIELDS:
                paths.append(key_path)
            paths.extend(disallowed_json_field_paths(nested, key_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            paths.extend(disallowed_json_field_paths(nested, f"{prefix}[{index}]"))
    return paths


def is_private_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in PRIVATE_PATH_PREFIXES)


def is_public_export_file(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if is_private_path(rel):
        return False
    if rel.startswith("contributions/") and path.name.endswith(EXAMPLE_BUNDLE_SUFFIX):
        return False
    if path.name in PUBLIC_EXCLUDED_FILENAMES:
        return False
    return True


def public_export_source_path(public_path: str) -> Path:
    return REPO_ROOT / PUBLIC_VIRTUAL_FILES.get(public_path, public_path)


def public_export_text_for_public_path(public_path: str) -> str:
    return public_export_text_for_path(public_export_source_path(public_path))


def public_export_text_for_path(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel == "claims/approved-claims.jsonl":
        return public_approved_claims_text(path)
    if rel == "concepts/registry.yaml":
        return public_concept_registry_text(path)
    if rel == "sources/registry.yaml":
        return public_source_registry_text(path)
    if rel == "agent/llms.txt":
        return public_llms_text(path)
    if rel == "agent/rock-kb-manifest.json":
        return public_agent_manifest_text(path)
    if rel == "agent/model-map-summary.json":
        return public_model_map_summary_text(path)
    if rel.startswith("knowledge/model-map/") or rel.startswith("agent/model-map-"):
        return public_model_map_text(path)
    if path.suffix.lower() in {".json", ".jsonl"}:
        return public_json_text(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def read_jsonl_text(text: str) -> Iterable[dict[str, Any]]:
    for line in text.splitlines():
        line = line.strip()
        if line:
            yield json.loads(line)


def public_approved_claims_text(path: Path) -> str:
    rows = [sanitize_public_claim(row) for row in read_jsonl(path)]
    return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + ("\n" if rows else "")


def sanitize_public_claim(row: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(row)
    sanitized.pop("private_corpus_pointer", None)
    if isinstance(sanitized.get("derived_from"), dict):
        derived = sanitized["derived_from"]
        sanitized["derived_from"] = {
            key: derived.get(key)
            for key in ["type", "source_id", "schema"]
            if derived.get(key)
        }
    if sanitized.get("live_verification"):
        sanitized["live_verification"] = sanitize_public_live_verification(sanitized["live_verification"])
    return sanitized


def sanitize_public_live_verification(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    refs = []
    for ref in value.get("evidence_refs") or []:
        if not isinstance(ref, dict):
            continue
        refs.append({key: ref.get(key) for key in ["probe_type", "tables"] if ref.get(key)})
    return {
        "verification_scope": "connected_read_only_rock_instance",
        "verification_method": value.get("verification_method") or "read_only_live_probe",
        "verified_at": value.get("verified_at"),
        "verified_by": "read_only_verification",
        "evidence_refs": refs,
        "notes": [sanitize_public_note(str(note)) for note in value.get("notes") or [] if note],
    }


def sanitize_public_note(value: str) -> str:
    replacements = {
        "ONE&ALL RockDB": "a connected Rock instance",
        "ONE&ALL's Rock production SQL surface": "a connected Rock instance",
        "RockDB": "a connected Rock database",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def public_source_registry_text(path: Path) -> str:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    public_payload = dict(payload)
    public_payload["sources"] = [
        source
        for source in payload.get("sources") or []
        if isinstance(source, dict) and is_public_source(source)
    ]
    return yaml.safe_dump(public_payload, sort_keys=False, allow_unicode=True)


def public_concept_registry_text(path: Path) -> str:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def is_public_source(source: dict[str, Any]) -> bool:
    if str(source.get("public_publish_mode") or "") == "private_only":
        return False
    if str(source.get("root_url") or "").startswith("local://"):
        return False
    return True


def public_llms_text(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    lines = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if audit_forbidden_public_text(rel, line):
            continue
        if "Private Rock Repo Candidates" in line or "RockProduction Docs Private Candidates" in line:
            continue
        lines.append(line)
    return "\n".join(lines) + "\n"


def public_agent_manifest_text(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop("private_media", None)
    entrypoints = payload.get("agent_entrypoints") or {}
    for key in PUBLIC_INTERNAL_AGENT_ENTRYPOINTS:
        entrypoints.pop(key, None)
    payload["agent_entrypoints"] = entrypoints
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def public_model_map_summary_text(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in ["stable", "latest", "pre_alpha"]:
        if isinstance(payload.get(key), dict):
            payload[key].pop("path", None)
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def public_model_map_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".jsonl":
        rows = [strip_private_provenance(row) for row in read_jsonl_text(text)]
        return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + ("\n" if rows else "")
    if path.suffix.lower() == ".json":
        payload = strip_private_provenance(json.loads(text))
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return text


def public_json_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".jsonl":
        rows = list(read_jsonl_text(text))
        return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + ("\n" if rows else "")
    payload = json.loads(text)
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def strip_private_provenance(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized = {}
        for key, nested in value.items():
            if key in PRIVATE_PROVENANCE_JSON_FIELDS and contains_private_marker(nested):
                continue
            sanitized[key] = strip_private_provenance(nested)
        return sanitized
    if isinstance(value, list):
        return [strip_private_provenance(item) for item in value]
    return value


def contains_private_marker(value: Any) -> bool:
    if isinstance(value, str):
        lower_value = value.lower()
        return any(pattern.lower() in lower_value for pattern in FORBIDDEN_PUBLIC_TEXT_PATTERNS)
    if isinstance(value, dict):
        return any(contains_private_marker(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_private_marker(item) for item in value)
    return False
