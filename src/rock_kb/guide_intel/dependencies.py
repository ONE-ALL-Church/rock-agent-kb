from __future__ import annotations

import yaml

from ._shared import *  # noqa: F401,F403


TASK_CARD_OVERRIDES = {
    (
        "scheduling-locations",
        "recipe-prove-why-a-check-in-room-is-not-available",
    ): {
        "goal": "Identify the first configuration, schedule, device, capacity, eligibility, or workflow filter that removes a specific room for a specific person and check-in attempt.",
        "live_records": [
            "Check-in Configuration",
            "Person",
            "Device",
            "Group",
            "GroupLocation",
            "GroupLocationSchedule",
            "Location",
            "Schedule",
            "Workflow",
        ],
        "entities": [
            "Person",
            "Device",
            "Group",
            "GroupLocation",
            "Location",
            "Schedule",
            "Workflow",
        ],
        "decision_order": [
            "Reproduce the exact person, device, check-in configuration, campus, and Rock time.",
            "Prove the room, group, and group-location-schedule chain is active and complete.",
            "Prove the current schedule and device scope include that chain.",
            "Evaluate person eligibility and room capacity against the same attempt.",
            "Trace location-selection and workflow filters in execution order; stop at the first removal.",
            "Check version-specific behavior only after current data and filter state are known.",
        ],
        "read_only_checks": [
            "Read the Location record and parent path; record IsActive and any Check-In Manager open or closed state.",
            "Read the GroupLocation joining the expected Group and Location; confirm the link is not inferred from matching names.",
            "Read the schedule configuration on that GroupLocation and compare it with the current date and time.",
            "Read the Device location scope and check-in configuration used by the failing kiosk or workflow.",
            "Evaluate age, grade, ability, requirements, group membership, capacity threshold, and overflow rules for the exact person without changing them.",
            "Inspect the workflow action log or equivalent diagnostic state and record which filter first excluded the location.",
        ],
        "steps": [
            "Record the exact check-in configuration, person, device, campus, occurrence, and current Rock time for one reproducible attempt.",
            "Confirm the expected Location is active, open, and under the intended campus and building hierarchy.",
            "Confirm the expected Group is active and included by the selected check-in configuration.",
            "Confirm a GroupLocation record joins that exact Group and Location.",
            "Confirm the GroupLocation schedule configuration includes the intended Schedule and occurrence.",
            "Confirm the Schedule is active at the recorded Rock time, including start date, end date, weekly time, and exclusions.",
            "Confirm the Device and kiosk configuration are allowed to display the expected location path.",
            "Evaluate the person's age, grade, ability, requirements, group membership, and other eligibility rules for that occurrence.",
            "Evaluate hard or soft capacity, room-closed state, overflow behavior, and location-selection strategy.",
            "Trace Check-In workflow filters in configured execution order and capture the first filter whose input contains the room but whose output does not.",
            "Compare the observed filter behavior with the cited Rock source and release caveats for the installed version.",
            "Report the first proven exclusion, the supporting record IDs or public model references, and the smallest safe configuration correction; do not change production during diagnosis.",
        ],
        "do_not_assume": [
            "A room with the right name is linked to the intended group or schedule.",
            "An active Location is open for Check-In or visible to the current device.",
            "A schedule is active now merely because it exists on the group.",
            "A full room, eligibility failure, or workflow filter is the cause until the same attempt proves it.",
            "The last configured filter caused the removal; identify the first input-to-output transition.",
        ],
        "related_result_ids": [
            "concept:check-in",
            "model_map:stable:device",
            "model_map:stable:group",
            "model_map:stable:group-location",
            "model_map:stable:location",
            "model_map:stable:schedule",
        ],
        "source_keywords": [
            "check-in room availability",
            "GroupLocation",
            "Schedule",
            "Device",
            "FilterLocations",
        ],
    }
}


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
    troubleshooting_tree = build_troubleshooting_tree(concept_id, guide_text, task_cards, section_rows)
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
    answer_bearing_claim_count = sum(
        1
        for row in approved_claim_dependencies
        if str(row.get("claim_tier") or "") in {"source_backed", "answer_pack_approved", "live_verified"}
    )
    routing_context_claim_count = sum(
        1
        for row in approved_claim_dependencies
        if str(row.get("claim_tier") or "") == "routing_context_only"
    )
    return {
        "concept_id": concept_id,
        "guide_path": repo_relative_path(guide_path),
        "guide_hash": sha256_text(guide_text),
        "guide_word_count": count_words(guide_text),
        "guide_line_count": len(guide_text.splitlines()),
        "built_at": generated_at_iso(),
        "source_pack_hydrated_at": pack.get("hydrated_at"),
        "synthesis_profile": pack.get("synthesis_profile"),
        "synthesis_provenance": guide_synthesis_provenance(guide_text, pack),
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
        "approved_claim_count": len(approved_claim_dependencies),
        "answer_bearing_claim_count": answer_bearing_claim_count,
        "routing_context_claim_count": routing_context_claim_count,
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

def guide_synthesis_provenance(guide_text: str, pack: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    if guide_text.startswith("---\n") and "\n---\n" in guide_text[4:]:
        frontmatter_text = guide_text.split("\n---\n", 1)[0].removeprefix("---\n")
        parsed = yaml.safe_load(frontmatter_text) or {}
        if isinstance(parsed, dict):
            metadata = parsed
    request = pack.get("synthesis_request") or {}
    values = {
        "model": metadata.get("synthesis_model") or request.get("model"),
        "reasoning_effort": metadata.get("synthesis_reasoning_effort")
        or request.get("reasoning_effort"),
        "prompt_id": metadata.get("synthesis_prompt_id") or request.get("prompt_id"),
        "prompt_version": metadata.get("synthesis_prompt_version")
        or request.get("prompt_version"),
        "source_pack_hash": metadata.get("synthesis_source_pack_hash"),
    }
    return {key: value for key, value in values.items() if value not in (None, "")}

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
        base_template = template
        override = TASK_CARD_OVERRIDES.get(
            (concept_id, str(template.get("id") or "")),
            {},
        )
        template = {
            **base_template,
            **override,
        }
        if override:
            template["source_keywords"] = compact_unique(
                [
                    *(base_template.get("source_keywords") or []),
                    *(override.get("source_keywords") or []),
                ]
            )
        source_keys = source_keys_for_keywords(
            template.get("source_keywords") or [],
            section_rows,
            source_index,
        )
        related_headings = set(template.get("related_source_headings") or [])
        related_source_keys = compact_unique(
            key
            for row in section_rows
            if row.get("heading") in related_headings
            for key in row.get("source_keys") or []
        )
        source_keys = compact_unique([*source_keys, *related_source_keys])[:16]
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
                "decision_order": template.get("decision_order") or [],
                "read_only_checks": template.get("read_only_checks") or [],
                "related_result_ids": template.get("related_result_ids") or [],
                "do_not_assume": template.get("do_not_assume") or [],
                "source_keys": source_keys,
                "source_urls": compact_unique(source_index[key].get("url") for key in source_keys if key in source_index),
                "created_at": generated_at_iso(),
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
