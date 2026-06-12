from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional

from .concepts import load_concepts
from .extract import grep_sensitive_values, now_iso, sha256_text

DEFAULT_EXTENSIONS = {".md", ".txt", ".sql", ".lava", ".liquid", ".cs", ".ts", ".js", ".json", ".yaml", ".yml"}
INSTANCE_MARKER_RE = {
    "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "rock_numeric_id": r"\b(?:Page|Block|Group|Workflow Type|DataView|AttributeValue|DefinedValue|PersonAlias|Campus)Id\s*[=:]\s*\d+\b",
    "rock_url_slug": r"\b(?:oneandall|one&all|lakesawyer|mywell|ministryplatform)\b",
    "production_host": r"\b(?:rock(?:rms)?|my)\.[A-Z0-9.-]+\.(?:church|org|com)\b",
}


def scan_private_repo(
    path: Path,
    allowlist: Optional[Path] = None,
    source_id: str = "private_rock_repo_candidates",
    org_id: str = "local",
) -> list[dict[str, Any]]:
    allowed_paths = load_allowlist(allowlist)
    records: list[dict[str, Any]] = []
    for file_path in sorted(path.rglob("*")):
        if not file_path.is_file() or should_skip_private_path(file_path, path):
            continue
        rel = file_path.relative_to(path).as_posix()
        if allowed_paths and rel not in allowed_paths:
            continue
        if file_path.suffix.lower() not in DEFAULT_EXTENSIONS:
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        findings = grep_sensitive_values(text.splitlines())
        risk_flags = private_risk_flags(text)
        classification = classify_private_document(text, findings, risk_flags)
        records.append(
            {
                "source_id": source_id,
                "source_kind": "private_docs_review",
                "org_id": org_id,
                "path": rel,
                "private_path_hash": sha256_text(rel),
                "scanned_at": now_iso(),
                "content_hash": sha256_text(text),
                "publishability_status": "blocked_sensitive_findings" if findings else "review_required",
                "review_classification": classification,
                "public_contribution_mode": contribution_mode(classification),
                "candidate_concepts": candidate_concepts(text),
                "risk_flags": risk_flags,
                "redaction_required": bool(findings or risk_flags),
                "sensitive_findings": findings[:10],
                "summary_candidate": "" if findings else " ".join(text.split())[:500],
            }
        )
    return records


def load_allowlist(path: Optional[Path]) -> set[str]:
    if not path:
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}


def should_skip_private_path(file_path: Path, root: Path) -> bool:
    rel_parts = file_path.relative_to(root).parts
    return any(part == ".git" or part.startswith(".") or part in {"node_modules", "bin", "obj", "__pycache__"} for part in rel_parts)


def private_risk_flags(text: str) -> list[str]:
    flags = []
    for label, pattern in INSTANCE_MARKER_RE.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            flags.append(label)
    return flags


def classify_private_document(text: str, sensitive_findings: list[str], risk_flags: list[str]) -> str:
    if sensitive_findings:
        return "instance_private"
    if risk_flags:
        return "needs_human_review"
    lowered = text.lower()
    if any(term in lowered for term in ["rock", "lava", "workflow", "group", "check-in", "dataview", "data view", "block", "page"]):
        return "generalizable_pattern"
    return "source_pointer_only"


def contribution_mode(classification: str) -> str:
    if classification == "generalizable_pattern":
        return "distill_then_review"
    if classification == "source_pointer_only":
        return "private_reference_only"
    return "private_only_until_reviewed"


def candidate_concepts(text: str) -> list[str]:
    lowered = text.lower()
    matches: list[tuple[int, str]] = []
    for concept in load_concepts():
        score = 0
        for keyword in concept.keywords:
            if str(keyword).lower() in lowered:
                score += 3
        for subguide in concept.subguides:
            for keyword in subguide.get("keywords", []):
                if str(keyword).lower() in lowered:
                    score += 1
        if score:
            matches.append((score, concept.id))
    matches.sort(key=lambda item: (-item[0], item[1]))
    return [concept_id for _, concept_id in matches[:5]]
