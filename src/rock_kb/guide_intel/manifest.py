from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def build_rock_kb_manifest() -> dict[str, Any]:
    concept_rows = []
    for concept in load_concepts():
        concept_dir = KNOWLEDGE_DIR / "concepts" / concept.id
        quality_path = concept_dir / "guide-quality.json"
        quality = json.loads(quality_path.read_text(encoding="utf-8")) if quality_path.exists() else {}
        concept_rows.append(
            {
                "concept_id": concept.id,
                "title": concept.title,
                "description": concept.description,
                "artifact_level": "detailed" if quality else ("baseline" if (concept_dir / "quickstart.md").exists() else "missing"),
                "quickstart": str((concept_dir / "quickstart.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "quickstart.md").exists() else "",
                "guide": str(synthesis_output_path(concept.id).relative_to(KNOWLEDGE_DIR.parents[0])) if synthesis_output_path(concept.id).exists() else "",
                "approved_claims": str((concept_dir / "approved-claims.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "approved-claims.md").exists() else "",
                "approved_media": str((concept_dir / "approved-media.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "approved-media.md").exists() else "",
                "live_inspection_checklist": str((concept_dir / "live-inspection-checklist.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "live-inspection-checklist.md").exists() else "",
                "live_probe_recipes": str((concept_dir / "live-probe-recipes.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "live-probe-recipes.md").exists() else "",
                "answers": str((concept_dir / "answers").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "answers").exists() else "",
                "task_cards": str((concept_dir / "task-cards.jsonl").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "task-cards.jsonl").exists() else "",
                "entities": str((concept_dir / "entities.jsonl").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "entities.jsonl").exists() else "",
                "release_caveats": str((concept_dir / "release-caveats.jsonl").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "release-caveats.jsonl").exists() else "",
                "section_source_map": str((concept_dir / "section-source-map.jsonl").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "section-source-map.jsonl").exists() else "",
                "section_status": str((concept_dir / "section-status.jsonl").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "section-status.jsonl").exists() else "",
                "troubleshooting_tree": str((concept_dir / "troubleshooting-tree.json").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "troubleshooting-tree.json").exists() else "",
                "open_questions": str((concept_dir / "open-questions.md").relative_to(KNOWLEDGE_DIR.parents[0])) if (concept_dir / "open-questions.md").exists() else "",
                "quality_status": quality.get("status"),
                "quality_score": quality.get("score"),
                "section_count": quality.get("section_count") or count_jsonl(concept_dir / "section-source-map.jsonl"),
                "task_card_count": quality.get("task_card_count") or count_jsonl(concept_dir / "task-cards.jsonl"),
            }
        )
    return {
        "schema": "rock-kb-agent-manifest-v1",
        "generated_at": generated_at_iso(),
        "agent_entrypoints": {
            "concepts": "knowledge/concepts/*/quickstart.md",
            "tasks": "agent/concept-task-cards.jsonl",
            "entities": "agent/entity-index.jsonl",
            "sections": "agent/section-source-map.jsonl",
            "release_caveats": "agent/concept-release-caveats.jsonl",
            "section_status": "agent/section-status.jsonl",
            "source_summaries": "agent/source-summaries.jsonl",
            "source_summary_report": "agent/source-summary-report.json",
            "model_map": "knowledge/model-map/index.md",
            "model_map_summary": "agent/model-map-summary.json",
            "model_map_entities": "agent/model-map-entities.jsonl",
            "model_map_properties": "agent/model-map-properties.jsonl",
            "model_map_methods": "agent/model-map-methods.jsonl",
            "model_map_version_diff": "agent/model-map-version-diff.jsonl",
            "model_map_digests": "agent/model-map-digests.jsonl",
            "model_map_model_details": "knowledge/model-map/models/*.md",
            "lava_capabilities": "agent/lava-capabilities.jsonl",
            "lava_capability_summary": "agent/lava-capability-summary.json",
            "lava_reference_index": "knowledge/concepts/lava/lava-reference-index.md",
            "lava_safety_matrix": "knowledge/concepts/lava/lava-safety-matrix.md",
            "lava_agent_usage_examples": "knowledge/concepts/lava/lava-agent-usage-examples.md",
            "approved_claims": "claims/approved-claims.jsonl",
            "answer_pack": "agent/answer-pack.jsonl",
            "live_checklists": "agent/live-inspection-checklists.jsonl",
            "live_probe_recipes": "agent/live-probe-recipes.jsonl",
            "claim_review_queue": "agent/claim-review-queue.jsonl",
            "source_conflicts": "agent/source-conflicts.jsonl",
            "distilled_claims": "agent/distilled-claims.jsonl",
            "source_authority_rules": "agent/source-authority-rules.jsonl",
            "evaluation_set": "agent/evaluation-set.jsonl",
            "evaluation_results": "agent/evaluation-results.jsonl",
            "evaluation_report": "agent/evaluation-report.json",
            "claim_review_dashboard": "agent/claim-review-dashboard.md",
            "troubleshooting": "knowledge/concepts/*/troubleshooting-tree.json",
            "open_questions": "knowledge/concepts/*/open-questions.md",
            "private_media": "data/media/index/media-index.jsonl",
        },
        "approved_claims": approved_claims_manifest_entry(),
        "source_summaries": source_summaries_manifest_entry(),
        "private_media": private_media_manifest_entry(),
        "concepts": concept_rows,
        "task_count": count_jsonl(AGENT_DIR / "concept-task-cards.jsonl"),
        "entity_count": count_jsonl(AGENT_DIR / "entity-index.jsonl"),
        "release_caveat_count": count_jsonl(AGENT_DIR / "concept-release-caveats.jsonl"),
}

def approved_claims_manifest_entry() -> dict[str, Any]:
    path = CLAIMS_DIR / "approved-claims.jsonl"
    report_path = CLAIMS_DIR / "claim-export-report.json"
    report: dict[str, Any] = {}
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = {"error": "claim-export-report.json is invalid JSON"}
    return {
        "path": relative_path(path) if path.exists() else "",
        "record_count": count_jsonl(path),
        "report": relative_path(report_path) if report_path.exists() else "",
        "authority_tiers": report.get("authority_tiers") or {},
        "claim_types": report.get("claim_types") or {},
        "public_publish_mode": "public_cite_and_summarize_only",
        "publishability_status": "approved_public_claim_graph",
        "notes": "Approved claims are the durable public knowledge unit. Each row must trace to source refs or source record IDs and pass public/private leak checks.",
    }

def source_summaries_manifest_entry() -> dict[str, Any]:
    summary_path = AGENT_DIR / "source-summaries.jsonl"
    report_path = AGENT_DIR / "source-summary-report.json"
    report: dict[str, Any] = {}
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = {"error": "source-summary-report.json is invalid JSON"}
    return {
        "path": relative_path(summary_path) if summary_path.exists() else "",
        "record_count": count_jsonl(summary_path),
        "report": relative_path(report_path) if report_path.exists() else "",
        "eligible_record_count": report.get("eligible_record_count", 0),
        "skipped_sensitive_count": report.get("skipped_sensitive_count", 0),
        "public_publish_mode": "public_cite_and_summarize_only",
        "publishability_status": "public_distilled_source_routing_index",
        "notes": "Public source summaries are citation-first routing notes. They are not full source mirrors and exclude scanner-positive rows.",
    }

def private_media_manifest_entry() -> dict[str, Any]:
    index_dir = MEDIA_DIR / "index"
    global_index = index_dir / "media-index.jsonl"
    source_indexes = []
    for path in sorted(index_dir.glob("*.media-index.jsonl")):
        if path.name == "media-index.jsonl":
            continue
        source_indexes.append({"path": relative_path(path), "record_count": count_jsonl(path)})
    return {
        "path": relative_path(global_index) if global_index.exists() else "",
        "record_count": count_jsonl(global_index),
        "source_indexes": source_indexes,
        "priority_queue": relative_path(MEDIA_DIR / "index" / "transcription-priority-queue.jsonl")
        if (MEDIA_DIR / "index" / "transcription-priority-queue.jsonl").exists()
        else "",
        "priority_report": relative_path(MEDIA_DIR / "index" / "transcription-priority-report.json")
        if (MEDIA_DIR / "index" / "transcription-priority-report.json").exists()
        else "",
        "private_storage": True,
        "public_publish_mode": "private_only",
        "publishability_status": "private_media_routing_index_only",
        "notes": "Private media indexes route agents to local sidecars, transcripts, and prioritized transcription work. Public exports must not include raw transcript text or direct media queue rows.",
    }
