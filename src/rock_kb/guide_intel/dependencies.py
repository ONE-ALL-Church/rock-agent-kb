from __future__ import annotations

from ._shared import *  # noqa: F401,F403


def build_guide_intelligence(concept_id: str) -> dict[str, Any]:
    concept = get_concept(concept_id)
    guide_path = synthesis_output_path(concept_id)
    if not guide_path.exists():
        raise FileNotFoundError(f"No authored guide found at {guide_path}")
    guide_text = guide_path.read_text(encoding="utf-8")
    pack = read_latest_source_pack(concept_id)
    source_index = build_source_index(pack)
    sections = parse_markdown_sections(guide_text)
    section_rows = section_source_map(concept_id, sections, source_index)
    dependency = guide_dependency_record(concept_id, guide_path, guide_text, section_rows, source_index, pack)
    release_rows = release_caveat_rows(concept_id, guide_text, pack, section_rows)
    task_cards = build_task_cards(concept_id, guide_text, section_rows, source_index)
    entity_rows = build_entity_rows(concept_id, guide_text, section_rows, task_cards, source_index)
    section_status_rows = build_section_status_rows(concept_id, section_rows, source_index)
    troubleshooting_tree = build_troubleshooting_tree(concept_id, task_cards, section_rows)
    audit = audit_guide_quality(concept_id, guide_text, section_rows, dependency, task_cards, entity_rows, pack)

    concept_dir = KNOWLEDGE_DIR / "concepts" / concept_id
    tasks_dir = concept_dir / "tasks"
    agent_cards_dir = concept_dir / "agent-cards"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    agent_cards_dir.mkdir(parents=True, exist_ok=True)
    for card in task_cards:
        card_path = tasks_dir / f"{card['task_id']}.md"
        card["path"] = str(card_path.relative_to(KNOWLEDGE_DIR.parents[0]))
        card_path.write_text(render_task_card(card), encoding="utf-8")
        (agent_cards_dir / f"{card['task_id']}.md").write_text(render_task_card(card), encoding="utf-8")

    write_jsonl(concept_dir / "section-source-map.jsonl", section_rows)
    write_jsonl(concept_dir / "release-caveats.jsonl", release_rows)
    write_jsonl(concept_dir / "entities.jsonl", entity_rows)
    write_jsonl(concept_dir / "section-status.jsonl", section_status_rows)
    write_json(concept_dir / "guide-dependencies.json", dependency)
    write_json(concept_dir / "guide-quality.json", audit)
    write_json(concept_dir / "troubleshooting-tree.json", troubleshooting_tree)
    (concept_dir / "quickstart.md").write_text(render_quickstart(concept_id, guide_text, section_rows, task_cards, entity_rows, release_rows), encoding="utf-8")
    (concept_dir / "agent-cheatsheet.md").write_text(render_agent_cheatsheet(concept_id, section_rows, task_cards, entity_rows, release_rows), encoding="utf-8")
    (concept_dir / "open-questions.md").write_text(render_open_questions(concept_id, section_rows), encoding="utf-8")
    write_jsonl(concept_dir / "task-cards.jsonl", task_cards)
    write_jsonl(concept_dir / "agent-cards.jsonl", task_cards)
    upsert_jsonl(AGENT_DIR / "section-source-map.jsonl", section_rows, "concept_id", concept_id)
    upsert_jsonl(AGENT_DIR / "concept-task-cards.jsonl", task_cards, "concept_id", concept_id)
    upsert_jsonl(AGENT_DIR / "concept-release-caveats.jsonl", release_rows, "concept_id", concept_id)
    upsert_jsonl(AGENT_DIR / "entity-index.jsonl", entity_rows, "concept_id", concept_id)
    upsert_jsonl(AGENT_DIR / "section-status.jsonl", section_status_rows, "concept_id", concept_id)
    write_json(AGENT_DIR / "rock-kb-manifest.json", build_rock_kb_manifest())

    return {
        "concept_id": concept.id,
        "guide_path": repo_relative_path(guide_path),
        "sections": len(section_rows),
        "sources": len(dependency["sources"]),
        "task_cards": len(task_cards),
        "entities": len(entity_rows),
        "release_caveats": len(release_rows),
        "quality_status": audit["status"],
        "quality_score": audit["score"],
    }

def read_latest_source_pack(concept_id: str) -> dict[str, Any]:
    review_dir = REVIEW_DIR / "concept-synthesis"
    hydrated = review_dir / f"{concept_id}.hydrated-source-pack.json"
    compact = review_dir / f"{concept_id}.source-pack.json"
    for path in [hydrated, compact]:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}

def guide_dependency_record(
    concept_id: str,
    guide_path: Path,
    guide_text: str,
    section_rows: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
    pack: dict[str, Any],
) -> dict[str, Any]:
    used_keys = compact_unique(key for row in section_rows for key in row.get("source_keys") or [])
    used_sources = [source_index[key] for key in used_keys if key in source_index]
    approved_media_artifact_path = guide_path.parent / "approved-media.md"
    approved_media_artifact_text = (
        approved_media_artifact_path.read_text(encoding="utf-8")
        if approved_media_artifact_path.exists()
        else ""
    )
    approved_media_dependencies = approved_media_dependencies_for_concept(
        concept_id,
        guide_text=guide_text,
        coverage_text=approved_media_artifact_text,
    )
    approved_media_dependency_hashes = {
        str(row.get("source_record_id")): row.get("content_hash")
        for row in approved_media_dependencies
        if row.get("source_record_id")
    }
    approved_claim_artifact_path = guide_path.parent / "approved-claims.md"
    approved_claim_artifact_text = (
        approved_claim_artifact_path.read_text(encoding="utf-8")
        if approved_claim_artifact_path.exists()
        else ""
    )
    approved_claim_dependencies = approved_claim_dependencies_for_concept(
        concept_id,
        guide_text=guide_text,
        coverage_text=approved_claim_artifact_text,
    )
    approved_claim_hashes = {
        str(row.get("claim_id")): row.get("claim_hash")
        for row in approved_claim_dependencies
        if row.get("claim_id")
    }
    return {
        "concept_id": concept_id,
        "guide_path": repo_relative_path(guide_path),
        "guide_hash": sha256_text(guide_text),
        "guide_word_count": count_words(guide_text),
        "guide_line_count": len(guide_text.splitlines()),
        "built_at": now_iso(),
        "source_pack_hydrated_at": pack.get("hydrated_at"),
        "synthesis_profile": pack.get("synthesis_profile"),
        "sections": [
            {
                "section_id": row["section_id"],
                "heading": row["heading"],
                "start_line": row["start_line"],
                "end_line": row["end_line"],
                "source_keys": row["source_keys"],
                "confidence": row["confidence"],
                "needs_live_verification": row["needs_live_verification"],
            }
            for row in section_rows
        ],
        "sources": used_sources,
        "approved_media_dependencies": approved_media_dependencies,
        "approved_media_path": repo_relative_path(approved_media_artifact_path) if approved_media_artifact_path.exists() else "",
        "approved_media_hash": sha256_text(approved_media_artifact_text) if approved_media_artifact_text else "",
        "approved_media_dependency_hashes": approved_media_dependency_hashes,
        "approved_claims_path": repo_relative_path(approved_claim_artifact_path) if approved_claim_artifact_path.exists() else "",
        "approved_claims_hash": sha256_text(approved_claim_artifact_text) if approved_claim_artifact_text else "",
        "approved_claim_dependencies": approved_claim_dependencies,
        "approved_claim_hashes": approved_claim_hashes,
        "rebuild_triggers": [
            {
                "source_key": source["source_key"],
                "source_id": source.get("source_id"),
                "source_record_id": source.get("source_record_id"),
                "url": source.get("url"),
                "content_hash": source.get("content_hash"),
                "excerpt_hash": source.get("excerpt_hash"),
                "authority": source.get("authority"),
            }
            for source in used_sources
        ],
    }

def release_caveat_rows(
    concept_id: str,
    guide_text: str,
    pack: dict[str, Any],
    section_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    seen: set[tuple[str, str, str]] = set()
    for record in pack.get("source_records") or []:
        if record.get("source_id") not in {"rock_core_release_notes", "rock_mobile_release_notes"}:
            continue
        row = {
            "concept_id": concept_id,
            "version": record.get("version"),
            "release_date": record.get("release_date"),
            "channel": "mobile" if record.get("source_id") == "rock_mobile_release_notes" else "core",
            "module": record.get("module"),
            "change_type": record.get("change_type"),
            "severity": record.get("severity"),
            "summary": record.get("summary") or record.get("excerpt") or record.get("source_title"),
            "source_url": record.get("source_url"),
            "source_record_id": record.get("id"),
            "mentioned_in_sections": sections_mentioning(guide_text, section_rows, [str(record.get("version") or ""), str(record.get("module") or "")]),
        }
        key = (str(row["version"]), str(row["summary"]), str(row["source_url"]))
        if key not in seen:
            seen.add(key)
            rows.append(row)
    return rows

def build_task_cards(
    concept_id: str,
    guide_text: str,
    section_rows: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if concept_id == "check-in":
        templates = CHECK_IN_TASK_CARDS
    elif concept_id == "learning-lms-engagement":
        templates = LEARNING_LMS_TASK_CARDS
    else:
        templates = inferred_task_templates(guide_text)
    cards = []
    for template in templates:
        source_keys = source_keys_for_keywords(template.get("source_keywords") or [], section_rows, source_index)
        cards.append(
            {
                "concept_id": concept_id,
                "task_id": template["id"],
                "title": template["title"],
                "goal": template["goal"],
                "guide_sections": template.get("guide_sections") or [],
                "live_records": template.get("live_records") or [],
                "entities": template.get("entities") or [],
                "steps": template.get("steps") or [],
                "do_not_assume": template.get("do_not_assume") or [],
                "source_keys": source_keys,
                "source_urls": compact_unique(source_index[key].get("url") for key in source_keys if key in source_index),
                "created_at": now_iso(),
            }
        )
    return cards

def build_entity_rows(
    concept_id: str,
    guide_text: str,
    section_rows: list[dict[str, Any]],
    task_cards: list[dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    all_entities = set()
    for entity in KNOWN_ENTITY_TERMS:
        if re.search(rf"\b{re.escape(entity)}\b", guide_text, re.IGNORECASE):
            all_entities.add(entity)
    for card in task_cards:
        all_entities.update(card.get("entities") or [])
        all_entities.update(card.get("live_records") or [])
    for entity in sorted(all_entities):
        search_terms = entity_search_terms(entity)
        section_ids = sections_mentioning(guide_text, section_rows, search_terms)
        task_ids = [card["task_id"] for card in task_cards if entity in (card.get("entities") or []) or entity in (card.get("live_records") or [])]
        source_keys = source_keys_for_keywords(search_terms, section_rows, source_index, limit=12)
        if not source_keys:
            source_keys = compact_unique(
                key
                for section in section_rows
                if section.get("section_id") in section_ids
                for key in section.get("source_keys") or []
            )[:12]
        if not source_keys:
            source_keys = compact_unique(
                key
                for card in task_cards
                if entity in (card.get("entities") or []) or entity in (card.get("live_records") or [])
                for key in card.get("source_keys") or []
            )[:12]
        note = ENTITY_NOTES.get(entity, {})
        rows.append(
            {
                "concept_id": concept_id,
                "entity": entity,
                "purpose": note.get("purpose") or f"Rock concept/entity referenced by the {concept_id} guide.",
                "used_by_sections": section_ids,
                "task_ids": task_ids,
                "source_keys": source_keys,
                "source_urls": compact_unique(source_index[key].get("url") for key in source_keys if key in source_index),
                "common_joins": note.get("common_joins") or [],
                "agent_notes": note.get("agent_notes") or ["Verify the exact record/entity shape in the live Rock version before making changes."],
                "confidence": "guide-derived",
            }
        )
    return rows

def entity_search_terms(entity: str) -> list[str]:
    return compact_unique([entity, *(ENTITY_ALIASES.get(entity) or [])])

def model_map_pointer_source() -> dict[str, Any]:
    url = "https://rocksolidchurchdemo.com/admin/power-tools/model-map"
    return {
        "source_key": stable_source_key(url, "rock_model_map_stable"),
        "source_record_id": "rock_model_map:stable-demo-scrape",
        "source_id": "rock_model_map",
        "kind": "generated_model_map_pointer",
        "title": "Stable Rock Model Map scrape",
        "url": url,
        "authority": "official-model-map",
        "authority_score": SOURCE_PRIORITY.get("official-model-map", 0),
    }
