from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

from .agent_answer_pack import build_agent_answer_pack
from .extract import grep_sensitive_values
from .jsonl import read_jsonl, write_jsonl
from .lava_capabilities import build_lava_capability_reference
from .lava_contexts import build_lava_context_reference
from .paths import AGENT_DIR, INDEX_DIR, KNOWLEDGE_DIR, NORMALIZED_DIR, SOURCES_DIR
from .sources import load_sources


def all_normalized_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(NORMALIZED_DIR.glob("*.jsonl")):
        records.extend(enrich_derived_documentation_metadata(record) for record in read_jsonl(path))
    return dedupe_records_by_id(records)


def enrich_derived_documentation_metadata(record: dict[str, Any]) -> dict[str, Any]:
    """Backfill compact Rockumentation branch fields for older normalized rows."""

    family = str(record.get("documentation_family") or "").strip()
    if family not in {"documentation", "developer"}:
        return record
    if record.get("documentation_path") and record.get("documentation_branch") and record.get("documentation_branches"):
        return record

    path_parts = [str(part).strip("/") for part in record.get("documentation_path_parts") or [] if str(part or "").strip("/")]
    if not path_parts:
        slug = str(record.get("documentation_slug") or "").strip("/")
        path_parts = [part for part in slug.split("/") if part]
    if not path_parts:
        return record

    enriched = dict(record)
    documentation_path = "/".join([family, *path_parts])
    branch_depth = 2 if family == "documentation" else 1
    documentation_branch = (
        "/".join([family, *path_parts[:branch_depth]])
        if len(path_parts) >= branch_depth
        else documentation_path
    )
    enriched.setdefault("documentation_path", documentation_path)
    enriched.setdefault("documentation_branch", documentation_branch)
    enriched.setdefault(
        "documentation_branches",
        ["/".join([family, *path_parts[:index]]) for index in range(1, len(path_parts) + 1)],
    )
    return enriched


def dedupe_records_by_id(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse duplicate normalized records before building public artifacts."""

    records_by_id: dict[str, dict[str, Any]] = {}
    ordered_ids: list[str] = []
    passthrough: list[dict[str, Any]] = []
    for record in records:
        record_id = str(record.get("id") or "").strip()
        if not record_id:
            passthrough.append(record)
            continue
        if record_id not in records_by_id:
            records_by_id[record_id] = record
            ordered_ids.append(record_id)
            continue
        if normalized_record_quality_key(record) > normalized_record_quality_key(records_by_id[record_id]):
            records_by_id[record_id] = record
    return [records_by_id[record_id] for record_id in ordered_ids] + passthrough


def normalized_record_quality_key(record: dict[str, Any]) -> tuple[int, int, int, str]:
    return (
        len(str(record.get("excerpt") or "")),
        len(str(record.get("summary") or "")),
        int(bool(record.get("documentation_article_id"))),
        str(record.get("retrieved_at") or ""),
    )


def build_sqlite_index(path: Optional[Path] = None) -> Path:
    path = path or INDEX_DIR / "kb.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    records = all_normalized_records()
    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE IF EXISTS records")
        connection.execute(
            """
            CREATE TABLE records (
                id TEXT PRIMARY KEY,
                source_id TEXT,
                source_url TEXT,
                source_title TEXT,
                source_kind TEXT,
                license_status TEXT,
                topics TEXT,
                summary TEXT,
                excerpt TEXT,
                canonical_path TEXT,
                json TEXT
            )
            """
        )
        connection.execute("DROP TABLE IF EXISTS records_fts")
        connection.execute(
            "CREATE VIRTUAL TABLE records_fts USING fts5(id, source_title, topics, summary, excerpt)"
        )
        for record in records:
            topics = ",".join(record.get("topics") or [])
            connection.execute(
                """
                INSERT OR REPLACE INTO records
                (id, source_id, source_url, source_title, source_kind, license_status, topics, summary, excerpt, canonical_path, json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("id"),
                    record.get("source_id"),
                    record.get("source_url"),
                    record.get("source_title"),
                    record.get("source_kind"),
                    record.get("license_status"),
                    topics,
                    record.get("summary"),
                    record.get("excerpt"),
                    record.get("canonical_path"),
                    json.dumps(record, ensure_ascii=False, sort_keys=True),
                ),
            )
            connection.execute(
                "INSERT INTO records_fts (id, source_title, topics, summary, excerpt) VALUES (?, ?, ?, ?, ?)",
                (
                    record.get("id"),
                    record.get("source_title") or "",
                    topics,
                    record.get("summary") or "",
                    record.get("excerpt") or "",
                ),
            )
    return path


def build_agent_pack() -> dict[str, int]:
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    records = public_agent_records(all_normalized_records())
    sources = load_sources()

    llms_lines = [
        "# Rock RMS General Knowledge Base",
        "",
        "This file is generated for AI agents. It points to source registries, curated knowledge, and machine-readable indexes.",
        "",
        "## Core Files",
        "",
        "- [Source registry](../sources/registry.yaml)",
        "- [Project goal](../docs/decisions/project-goal.md)",
        "- [Data organization decision](../docs/decisions/data-organization-decision.md)",
        "- [Pipeline overview](../docs/runbooks/pipeline-overview.md)",
        "- [Concept registry](../concepts/registry.yaml)",
        "- [Concept dependency map](concept-dependencies.jsonl)",
        "- [Concept index](concept-index.jsonl)",
        "- [Public source summaries](source-summaries.jsonl)",
        "- [Source summary coverage report](source-summary-report.json)",
        "",
        "## Sources",
        "",
    ]
    for source in sources:
        if source.public_publish_mode == "private_only" or source.root_url.startswith(("local://", "private-corpus://")):
            continue
        llms_lines.append(f"- [{source.name}]({source.root_url}) - {source.description}")
    (AGENT_DIR / "llms.txt").write_text("\n".join(llms_lines) + "\n", encoding="utf-8")

    topics: dict[str, list[dict[str, Any]]] = defaultdict(list)
    release_rows: list[dict[str, Any]] = []
    citation_rows: list[dict[str, Any]] = []
    for record in records:
        for topic in record.get("topics") or ["untagged"]:
            topics[topic].append(
                {
                    "id": record.get("id"),
                    "source_id": record.get("source_id"),
                    "title": record.get("source_title"),
                    "summary": record.get("summary"),
                    "canonical_path": record.get("canonical_path"),
                }
            )
        if record.get("release_family"):
            release_rows.append(
                {
                    "id": record.get("id"),
                    "release_family": record.get("release_family"),
                    "version": record.get("version"),
                    "release_date": record.get("release_date"),
                    "module": record.get("module"),
                    "change_type": record.get("change_type"),
                    "severity": record.get("severity"),
                    "summary": record.get("summary"),
                    "issue_refs": record.get("issue_refs"),
                }
            )
        citation_rows.append(
            {
                "id": record.get("id"),
                "source_id": record.get("source_id"),
                "citations": record.get("citations") or [],
            }
        )

    topic_rows = [{"topic": topic, "records": rows} for topic, rows in sorted(topics.items())]
    source_summary_rows, source_summary_report = build_public_source_summary_pack(records)
    (AGENT_DIR / "source-summary-report.json").write_text(
        json.dumps(source_summary_report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    counts = {
        "topic_index": write_jsonl(AGENT_DIR / "topic-index.jsonl", topic_rows),
        "release_index": write_jsonl(AGENT_DIR / "release-index.jsonl", release_rows),
        "source_citations": write_jsonl(AGENT_DIR / "source-citations.jsonl", citation_rows),
        "source_summaries": write_jsonl(AGENT_DIR / "source-summaries.jsonl", source_summary_rows),
        "source_summary_skipped_sensitive": int(source_summary_report["skipped_sensitive_count"]),
    }
    counts["knowledge_source_pages"] = build_knowledge_source_pages(records)
    counts["knowledge_topic_pages"] = build_curated_topic_pages(records)
    counts.update({f"model_map_{key}": value for key, value in build_or_reuse_model_map().items()})
    counts.update(build_lava_capability_reference(records))
    counts.update(build_lava_context_reference())
    from .concepts import refresh_long_form_model_map_pointers

    model_map_pointer_result = refresh_long_form_model_map_pointers()
    counts["long_form_model_map_pointer_guides"] = int(model_map_pointer_result["concept_count"])
    counts["long_form_model_map_pointer_updated"] = int(model_map_pointer_result["updated_count"])
    counts.update(build_agent_answer_pack())
    refresh_agent_manifest()
    return counts


def build_or_reuse_model_map() -> dict[str, Any]:
    """Reuse committed generated model-map artifacts.

    Raw model-map fetch artifacts are ignored review inputs and may be stale.
    Only the explicit `kb modelmap fetch` plus `kb modelmap build` workflow
    should regenerate public model-map files from those artifacts.
    """

    required_paths = [
        KNOWLEDGE_DIR / "model-map" / "index.md",
        KNOWLEDGE_DIR / "model-map" / "stable-models.jsonl",
        KNOWLEDGE_DIR / "model-map" / "stable-properties.jsonl",
        KNOWLEDGE_DIR / "model-map" / "stable-methods.jsonl",
        KNOWLEDGE_DIR / "model-map" / "latest-models.jsonl",
        KNOWLEDGE_DIR / "model-map" / "latest-properties.jsonl",
        KNOWLEDGE_DIR / "model-map" / "latest-methods.jsonl",
        KNOWLEDGE_DIR / "model-map" / "version-diff.jsonl",
        AGENT_DIR / "model-map-summary.json",
        AGENT_DIR / "model-map-entities.jsonl",
        AGENT_DIR / "model-map-properties.jsonl",
        AGENT_DIR / "model-map-methods.jsonl",
        AGENT_DIR / "model-map-version-diff.jsonl",
        AGENT_DIR / "model-map-digests.jsonl",
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Generated model-map artifacts are incomplete. "
            "Run `uv run kb modelmap fetch --track both` and then `uv run kb modelmap build`. "
            f"Missing generated artifacts: {', '.join(missing[:5])}"
        )

    summary = json.loads((AGENT_DIR / "model-map-summary.json").read_text(encoding="utf-8"))
    stable_models = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "stable-models.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    latest_models = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "latest-models.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    stable_properties = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "stable-properties.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    latest_properties = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "latest-properties.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    stable_methods = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "stable-methods.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    latest_methods = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "latest-methods.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    version_diff_changes = sum(1 for line in (KNOWLEDGE_DIR / "model-map" / "version-diff.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    model_digests = sum(1 for line in (AGENT_DIR / "model-map-digests.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    return {
        "source": "reused_generated_model_map",
        "reused_existing_artifacts": 1,
        "stable_version": (summary.get("stable") or {}).get("rock_version"),
        "pre_alpha_version": (summary.get("pre_alpha") or summary.get("latest") or {}).get("rock_version"),
        "stable_models": stable_models,
        "pre_alpha_models": latest_models,
        "stable_properties": stable_properties,
        "pre_alpha_properties": latest_properties,
        "stable_methods": stable_methods,
        "pre_alpha_methods": latest_methods,
        "version_diff_changes": version_diff_changes,
        "model_digests": model_digests,
    }


def refresh_agent_manifest() -> None:
    from .guide_intel import build_rock_kb_manifest

    (AGENT_DIR / "rock-kb-manifest.json").write_text(
        json.dumps(build_rock_kb_manifest(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def public_agent_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if is_public_agent_record(record)]


def is_public_agent_record(record: dict[str, Any]) -> bool:
    if record.get("derived_from_private_transcript") and not is_reviewed_for_public_agent_pack(record):
        return False
    if record.get("private_storage") and record.get("needs_review"):
        return False
    publishability = str(record.get("publishability_status") or "")
    if publishability.startswith("private_") or publishability in {"private_transcript_only", "private_media_sidecar_only"}:
        return False
    return True


def is_reviewed_for_public_agent_pack(record: dict[str, Any]) -> bool:
    review_status = str(record.get("review_status") or "")
    return review_status in {"redaction_reviewed", "approved_for_public_distillation", "public_reviewed"}


def build_public_source_summaries(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return build_public_source_summary_pack(records)[0]


def build_public_source_summary_pack(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    skipped_by_source: dict[str, int] = defaultdict(int)
    eligible_by_source: dict[str, int] = defaultdict(int)
    for record in records:
        source_id = str(record.get("source_id") or "unknown")
        eligible_by_source[source_id] += 1
        row = {
            "schema": "rock-kb-public-source-summary-v1",
            "id": f"{record.get('id')}:public-summary",
            "source_record_id": record.get("id"),
            "source_id": record.get("source_id"),
            "source_kind": record.get("source_kind"),
            "source_url": record.get("source_url"),
            "source_title": record.get("source_title"),
            "canonical_path": record.get("canonical_path"),
            "topics": record.get("topics") or [],
            "rock_versions": record.get("rock_versions") or [],
            "retrieved_at": record.get("retrieved_at"),
            "updated_at": record.get("updated_at"),
            "content_hash": record.get("content_hash"),
            "license_status": record.get("license_status"),
            "allowed_extraction_mode": record.get("allowed_extraction_mode"),
            "summary": public_summary_text(record),
            "key_insights": public_key_insights(record),
            "agent_use": agent_use_for_record(record),
            "citations": record.get("citations") or [{"source_id": record.get("source_id"), "url": record.get("source_url")}],
            "public_publish_mode": record.get("public_publish_mode") or "public_cite_and_summarize_only",
            "contains_raw_source_text": False,
            "needs_review": bool(record.get("needs_review")),
        }
        for key in [
            "documentation_family",
            "documentation_slug",
            "documentation_path",
            "documentation_branch",
            "documentation_branches",
        ]:
            if record.get(key) not in (None, "", [], {}):
                row[key] = record.get(key)
        serialized = json.dumps(row, ensure_ascii=False, sort_keys=True)
        if grep_sensitive_values([serialized]):
            skipped_by_source[source_id] += 1
            continue
        rows.append(row)
    report = {
        "schema": "rock-kb-source-summary-report-v1",
        "public_summary_path": "agent/source-summaries.jsonl",
        "eligible_record_count": len(records),
        "public_summary_count": len(rows),
        "skipped_sensitive_count": sum(skipped_by_source.values()),
        "skipped_sensitive_by_source": dict(sorted(skipped_by_source.items())),
        "eligible_by_source": dict(sorted(eligible_by_source.items())),
        "public_publish_mode": "public_cite_and_summarize_only",
        "notes": [
            "Rows are generated only from records already eligible for the public agent pack.",
            "Rows that trigger the public secret scanner are excluded from source-summaries.jsonl.",
            "Skipped rows remain available in private/generated normalized data and by following their source URLs.",
        ],
    }
    return rows, report


def public_summary_text(record: dict[str, Any]) -> str:
    summary = " ".join(str(record.get("summary") or "").split())
    if summary:
        return summary[:1200]
    title = record.get("source_title") or record.get("id") or "Untitled source"
    return f"Public source note for {title}. Review the linked source for authoritative details."


def public_key_insights(record: dict[str, Any], max_items: int = 4) -> list[dict[str, Any]]:
    if str(record.get("id") or "").startswith("media-insight:") and record.get("key_insights"):
        insights = []
        for item in record.get("key_insights") or []:
            if not isinstance(item, dict):
                insight_text = str(item or "").strip()
                if not insight_text:
                    continue
                item = {"insight": insight_text}
            insight_text = str(item.get("insight") or "").strip()
            if not insight_text:
                continue
            insight = {
                "insight": insight_text,
                "source_url": item.get("source_url") or record.get("source_url"),
                "source_timestamp_url": item.get("source_timestamp_url") or item.get("source_url") or record.get("source_url"),
                "source_record_id": record.get("id"),
                "confidence": "reviewed-media-insight",
            }
            for key in ["topic", "timestamp", "timestamp_seconds"]:
                if item.get(key) not in (None, ""):
                    insight[key] = item.get(key)
            insights.append(insight)
        return insights[:max_items]

    insights = []
    summary = public_summary_text(record)
    for sentence in split_public_sentences(summary)[:max_items]:
        insights.append(
            {
                "insight": sentence,
                "source_url": record.get("source_url"),
                "source_record_id": record.get("id"),
                "confidence": "source-summary",
            }
        )
    if record.get("release_family") or record.get("version"):
        insights.append(
            {
                "insight": "Treat this as release-aware context and check version applicability before acting.",
                "source_url": record.get("source_url"),
                "source_record_id": record.get("id"),
                "confidence": "release-metadata",
            }
        )
    return insights[:max_items]


def split_public_sentences(text: str) -> list[str]:
    pieces = re_split_sentences(text)
    return [piece for piece in pieces if len(piece) >= 24]


def re_split_sentences(text: str) -> list[str]:
    import re

    return [piece.strip() for piece in re.split(r"(?<=[.!?])\s+", text) if piece.strip()]


def agent_use_for_record(record: dict[str, Any]) -> str:
    topics = set(record.get("topics") or [])
    source_kind = str(record.get("source_kind") or "")
    if record.get("release_family") or "release" in topics:
        return "Use for version checks, upgrade planning, regression risk, and release caveats."
    if "developer" in topics or "api" in topics or "github" in source_kind:
        return "Use for implementation details, API behavior, code references, and developer workflows."
    if "recipe" in topics:
        return "Use as practical implementation context; verify against current Rock version and local configuration."
    return "Use as a cited retrieval clue for concept guides, task cards, and follow-up source inspection."


def build_knowledge_source_pages(records: list[dict[str, Any]]) -> int:
    output_dir = KNOWLEDGE_DIR / "sources"
    output_dir.mkdir(parents=True, exist_ok=True)
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_source[record.get("source_id") or "unknown"].append(record)

    for source_id, source_records in sorted(by_source.items()):
        lines = [
            "---",
            f"id: {source_id}",
            "generated: true",
            "---",
            "",
            f"# {source_id}",
            "",
            f"Records: {len(source_records)}",
            "",
            "| Title | Summary | Citation |",
            "| --- | --- | --- |",
        ]
        for record in sorted(source_records, key=lambda row: (row.get("source_title") or "", row.get("source_url") or "")):
            title = escape_table_cell(record.get("source_title") or record.get("id") or "")
            summary = escape_table_cell(record.get("summary") or "")
            citation = record.get("source_url") or ""
            citation_cell = f"[source]({citation})" if citation.startswith("http") else escape_table_cell(citation)
            lines.append(f"| {title} | {summary} | {citation_cell} |")
        (output_dir / f"{source_id}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(by_source)


def escape_table_cell(value: str) -> str:
    return " ".join(str(value).replace("|", "\\|").split())


CURATED_TOPICS = {
    "api": {
        "title": "Rock API",
        "keywords": ["api", "rest", "webhook", "odata", "integration"],
        "description": "REST, API v1/v2, integrations, auth, and endpoint-related records.",
    },
    "lava": {
        "title": "Lava",
        "keywords": ["lava", "shortcode", "filter", "command"],
        "description": "Lava syntax, filters, commands, shortcodes, and CMS/developer usage.",
    },
    "mobile": {
        "title": "Rock Mobile",
        "keywords": ["mobile", "maui", "xaml", "ios", "android", "shell"],
        "description": "Rock Mobile shell, mobile docs, controls, commands, and mobile release notes.",
    },
    "release-upgrade-notes": {
        "title": "Release And Upgrade Notes",
        "keywords": ["release", "upgrade", "breaking", "deprecated", "security"],
        "description": "Core and mobile release notes grouped for upgrade planning.",
    },
    "sql": {
        "title": "SQL And Reporting",
        "keywords": ["sql", "database", "report", "query", "model map"],
        "description": "SQL, reporting, Model Map, BI, and data-oriented records.",
    },
    "workflows": {
        "title": "Workflows",
        "keywords": ["workflow", "automation", "job", "trigger"],
        "description": "Workflow, automation, jobs, and operational recipes.",
    },
    "plugins": {
        "title": "Plugins And Rock Shop",
        "keywords": ["plugin", "rock shop", "package", "assembly"],
        "description": "Plugin metadata, Rock Shop records, uninstall notes, and extension resources.",
    },
}


def build_curated_topic_pages(records: list[dict[str, Any]]) -> int:
    output_dir = KNOWLEDGE_DIR / "topics"
    output_dir.mkdir(parents=True, exist_ok=True)
    for slug, config in CURATED_TOPICS.items():
        matched = rank_topic_records(records, config["keywords"])
        lines = [
            "---",
            f"id: topic-{slug}",
            "generated: true",
            f"topic: {slug}",
            "---",
            "",
            f"# {config['title']}",
            "",
            config["description"],
            "",
            "This page is generated from normalized records. Follow source links before applying operational or code changes.",
            "",
            f"Matched records: {len(matched)}",
            "",
            "## Highest Signal Records",
            "",
            "| Title | Source | Summary | Citation |",
            "| --- | --- | --- | --- |",
        ]
        for record in matched[:80]:
            title = escape_table_cell(record.get("source_title") or record.get("id") or "")
            source_id = escape_table_cell(record.get("source_id") or "")
            summary = escape_table_cell(record.get("summary") or "")
            citation = record.get("source_url") or ""
            citation_cell = f"[source]({citation})" if citation.startswith("http") else escape_table_cell(citation)
            lines.append(f"| {title} | {source_id} | {summary} | {citation_cell} |")
        (output_dir / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(CURATED_TOPICS)


def rank_topic_records(records: list[dict[str, Any]], keywords: list[str]) -> list[dict[str, Any]]:
    scored = []
    for record in records:
        haystack = " ".join(
            [
                str(record.get("source_title") or ""),
                str(record.get("summary") or ""),
                str(record.get("excerpt") or ""),
                " ".join(record.get("topics") or []),
                str(record.get("detail_type") or ""),
                str(record.get("module") or ""),
            ]
        ).lower()
        score = sum(haystack.count(keyword.lower()) for keyword in keywords)
        if record.get("source_id") in {"rock_core_release_notes", "rock_mobile_release_notes"}:
            score += 1 if "release" in keywords or "upgrade" in keywords else 0
        if score > 0:
            scored.append((score, record.get("updated_at") or record.get("retrieved_at") or "", record))
    scored.sort(key=lambda item: (-item[0], item[1], item[2].get("source_title") or ""))
    return [record for _, _, record in scored]
