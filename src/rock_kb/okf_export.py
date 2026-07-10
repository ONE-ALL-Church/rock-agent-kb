from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml

from .concepts import load_concepts
from .jsonl import read_jsonl
from .paths import CLAIMS_DIR, DATA_DIR, REPO_ROOT
from .sources import load_sources
from .timestamps import generated_at_iso


DEFAULT_OKF_EXPORT_DIR = DATA_DIR / "okf-export"
RESERVED_ROOT_FILES = {"index.md", "log.md"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def build_okf_export(destination: Path | None = None) -> dict[str, Any]:
    destination = (destination or DEFAULT_OKF_EXPORT_DIR).resolve()
    if destination in {Path("/").resolve(), Path.home().resolve(), REPO_ROOT.resolve()} or (destination / ".git").exists():
        raise ValueError(f"Refusing to replace unsafe OKF export destination: {destination}")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    generated_at = generated_at_iso()

    concepts = load_concepts()
    concept_ids = {concept.id for concept in concepts}
    claims = list(read_jsonl(CLAIMS_DIR / "approved-claims.jsonl"))
    source_registry = {source.id: source for source in load_sources()}
    claims_by_concept: dict[str, list[dict[str, Any]]] = defaultdict(list)
    claims_by_source: dict[str, list[str]] = defaultdict(list)
    source_meta: dict[str, dict[str, Any]] = {}
    relationships: list[dict[str, str]] = []

    for claim in claims:
        for concept_id in claim.get("concept_ids") or []:
            if concept_id in concept_ids:
                claims_by_concept[concept_id].append(claim)
        for ref in claim.get("source_refs") or []:
            source_id = str(ref.get("source_id") or "").strip()
            if source_id:
                claims_by_source[source_id].append(str(claim.get("claim_id") or ""))
                meta = source_meta.setdefault(
                    source_id,
                    {"title": str(ref.get("title") or source_id), "url": str(ref.get("url") or ""), "citations": []},
                )
                citation = {"title": str(ref.get("title") or source_id), "url": str(ref.get("url") or "")}
                if citation["url"] and citation not in meta["citations"]:
                    meta["citations"].append(citation)

    for source_id in sorted(source_meta):
        source = source_registry.get(source_id)
        meta = source_meta[source_id]
        title = source.name if source else meta["title"]
        url = source.root_url if source else meta["url"]
        description = source.description if source else "Public evidence source referenced by approved Rock KB claims."
        body = [description]
        if url:
            body.extend(["", f"- [Open source]({url})"])
        citations = sorted(meta["citations"], key=lambda row: (row["title"], row["url"]))
        if citations:
            body.extend(["", "## Cited Items", *[f"- [{markdown_label(row['title'])}]({row['url']})" for row in citations]])
        write_typed_markdown(
            destination / "references" / f"{safe_slug(source_id)}.md",
            {
                "type": "Reference",
                "id": source_id,
                "title": title,
                "source_url": url,
                "source_path": "sources/registry.yaml",
                "relationships": compact_relationships(
                    "supports",
                    [f"Claim:{claim_id}" for claim_id in sorted(set(claims_by_source[source_id])) if claim_id],
                ),
            },
            body,
        )

    for claim in claims:
        claim_id = str(claim.get("claim_id") or "")
        claim_text = str(claim.get("claim") or "").strip()
        concept_links = [
            f"- [{markdown_label(concept_id)}](../concepts/{safe_slug(concept_id)}.md)"
            for concept_id in claim.get("concept_ids") or []
            if concept_id in concept_ids
        ]
        source_links = []
        seen_sources: set[str] = set()
        claim_relationships: list[dict[str, str]] = []
        for concept_id in claim.get("concept_ids") or []:
            if concept_id in concept_ids:
                claim_relationships.append(relationship("about", f"Claim:{claim_id}", f"Concept:{concept_id}"))
        for ref in claim.get("source_refs") or []:
            source_id = str(ref.get("source_id") or "").strip()
            if not source_id or source_id in seen_sources:
                continue
            seen_sources.add(source_id)
            source_links.append(f"- [{markdown_label(source_id)}](../references/{safe_slug(source_id)}.md)")
            claim_relationships.append(relationship("supported_by", f"Claim:{claim_id}", f"Reference:{source_id}"))
        relationships.extend(claim_relationships)
        body = [claim_text, "", "## Concepts", *(concept_links or ["No concept route recorded."]), "", "## Evidence", *(source_links or ["No source reference recorded."])]
        write_typed_markdown(
            destination / "claims" / f"{claim_filename(claim_id)}.md",
            {
                "type": "Claim",
                "id": claim_id,
                "title": compact_title(claim_text),
                "authority_tier": str(claim.get("authority_tier") or ""),
                "claim_tier": str(claim.get("claim_tier") or ""),
                "concept_ids": list(claim.get("concept_ids") or []),
                "source_path": "claims/approved-claims.jsonl",
                "relationships": [{"type": row["type"], "target": row["target"]} for row in claim_relationships],
            },
            body,
        )

    for concept in concepts:
        claim_links = [
            f"- [{markdown_label(compact_title(str(claim.get('claim') or '')))}](../claims/{claim_filename(str(claim.get('claim_id') or ''))}.md)"
            for claim in sorted(claims_by_concept.get(concept.id, []), key=lambda row: str(row.get("claim_id") or ""))
        ]
        source_ids = sorted(
            {
                str(ref.get("source_id") or "")
                for claim in claims_by_concept.get(concept.id, [])
                for ref in claim.get("source_refs") or []
                if ref.get("source_id")
            }
        )
        source_links = [f"- [{markdown_label(source_id)}](../references/{safe_slug(source_id)}.md)" for source_id in source_ids]
        body = [
            concept.description,
            "",
            f"Canonical guide: `{concept.raw.get('guide_path') or f'knowledge/concepts/{concept.id}/index.md'}`",
            "",
            "## Approved Claims",
            *(claim_links or ["No approved claims recorded."]),
            "",
            "## Evidence Sources",
            *(source_links or ["No source references recorded."]),
        ]
        write_typed_markdown(
            destination / "concepts" / f"{safe_slug(concept.id)}.md",
            {
                "type": "Concept",
                "id": concept.id,
                "title": concept.title,
                "description": concept.description,
                "source_path": f"knowledge/concepts/{concept.id}/index.md",
                "relationships": compact_relationships(
                    "has_claim",
                    [f"Claim:{claim.get('claim_id')}" for claim in claims_by_concept.get(concept.id, []) if claim.get("claim_id")],
                ),
            },
            body,
        )

    index_lines = [
        "# Rock Agent Knowledge Base",
        "",
        "Generated Open Knowledge Format projection. The canonical Rock KB remains in its registries, approved claims, and generated agent artifacts.",
        "",
        "## Concepts",
        *[f"- [{markdown_label(concept.title)}](concepts/{safe_slug(concept.id)}.md)" for concept in concepts],
        "",
        "## Evidence Sources",
        *[f"- [{markdown_label(source_id)}](references/{safe_slug(source_id)}.md)" for source_id in sorted(source_meta)],
    ]
    (destination / "index.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    (destination / "log.md").write_text(f"# Log\n\n## {generated_at}\n\nGenerated from the public Rock KB projection.\n", encoding="utf-8")
    relationship_rows = sorted(relationships, key=lambda row: (row["source"], row["type"], row["target"]))
    (destination / "relationships.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in relationship_rows),
        encoding="utf-8",
    )

    errors = audit_okf_export(destination)
    report = {
        "schema": "rock-kb-okf-export-v1",
        "status": "ok" if not errors else "failed",
        "destination": str(destination),
        "generated_at": generated_at,
        "counts": {
            "concepts": len(concepts),
            "claims": len(claims),
            "references": len(source_meta),
            "markdown_files": len(list(destination.rglob("*.md"))),
            "relationships": len(relationship_rows),
        },
        "errors": errors,
    }
    (destination / "okf-export-manifest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def audit_okf_export(destination: Path) -> list[str]:
    errors: list[str] = []
    for reserved in sorted(RESERVED_ROOT_FILES):
        path = destination / reserved
        if not path.exists():
            errors.append(f"missing reserved root file: {reserved}")
        elif path.read_text(encoding="utf-8").startswith("---\n"):
            errors.append(f"reserved root file must not have frontmatter: {reserved}")

    for path in sorted(destination.rglob("*.md")):
        relative = path.relative_to(destination).as_posix()
        text = path.read_text(encoding="utf-8")
        if relative not in RESERVED_ROOT_FILES:
            frontmatter = read_frontmatter(text)
            if not frontmatter.get("type"):
                errors.append(f"{relative} missing non-empty type frontmatter")
        for target in markdown_targets(text):
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(destination.resolve()) or not resolved.exists():
                errors.append(f"{relative} has unresolved link: {target}")
        for marker in ("/Users/", "data/review/", "data/normalized/", "private_corpus_pointer"):
            if marker in text:
                errors.append(f"{relative} contains private marker: {marker}")
    return errors


def write_typed_markdown(path: Path, frontmatter: dict[str, Any], body: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_text = yaml.safe_dump(frontmatter, allow_unicode=False, sort_keys=False).strip()
    path.write_text(f"---\n{yaml_text}\n---\n\n" + "\n".join(body).rstrip() + "\n", encoding="utf-8")


def read_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    value = yaml.safe_load(text[4:end]) or {}
    return value if isinstance(value, dict) else {}


def markdown_targets(text: str) -> list[str]:
    targets = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            targets.append(target)
    return targets


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", value.lower()).strip("-") or "unknown"


def claim_filename(claim_id: str) -> str:
    return safe_slug(claim_id.removeprefix("claim:"))


def compact_title(value: str, limit: int = 96) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def markdown_label(value: str) -> str:
    return value.replace("[", "(").replace("]", ")")


def relationship(relation_type: str, source: str, target: str) -> dict[str, str]:
    return {
        "schema": "rock-kb-okf-relationship-v1",
        "type": relation_type,
        "source": source,
        "target": target,
    }


def compact_relationships(relation_type: str, targets: Iterable[str]) -> list[dict[str, str]]:
    return [{"type": relation_type, "target": target} for target in sorted(set(targets))]
