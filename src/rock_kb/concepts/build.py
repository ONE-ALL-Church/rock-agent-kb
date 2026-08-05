from __future__ import annotations

from ._shared import *  # noqa: F401,F403
from .audit import write_concept_taxonomy_audit


def build_all_concepts() -> dict[str, int]:
    records = concept_source_records()
    previous = read_dependency_map()
    dependencies = []
    built = 0
    baseline_artifacts = 0
    for concept in load_concepts():
        guide, dependency = build_concept_guide(concept, records, previous)
        output = concept_path(concept)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(guide, encoding="utf-8")
        matched = rank_records_for_concept(concept, records)
        selected = ensure_weighted_source_coverage(concept, matched, concept.max_records)
        baseline_artifacts += ensure_baseline_agent_entrypoints(concept, selected, dependency)
        dependencies.append(dependency)
        built += 1
    write_jsonl(AGENT_DIR / "concept-dependencies.jsonl", dependencies)
    write_jsonl(AGENT_DIR / "concept-index.jsonl", concept_index_rows(dependencies))
    write_agent_manifest()
    taxonomy = write_concept_taxonomy_audit()
    return {
        "concept_guides": built,
        "concept_dependencies": len(dependencies),
        "baseline_agent_artifacts": baseline_artifacts,
        "concept_taxonomy_errors": len(taxonomy["errors"]),
        "concept_taxonomy_warnings": len(taxonomy["warnings"]),
    }

def build_single_concept(concept_id: str) -> dict[str, Any]:
    concept = get_concept(concept_id)
    records = concept_source_records()
    previous = read_dependency_map()
    guide, dependency = build_concept_guide(concept, records, previous)
    output = concept_path(concept)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(guide, encoding="utf-8")
    matched = rank_records_for_concept(concept, records)
    selected = ensure_weighted_source_coverage(concept, matched, concept.max_records)
    baseline_artifacts = ensure_baseline_agent_entrypoints(concept, selected, dependency)

    dependencies = list(previous.values())
    dependencies = [row for row in dependencies if row.get("concept_id") != concept.id]
    dependencies.append(dependency)
    dependencies.sort(key=lambda row: row.get("concept_id") or "")
    write_jsonl(AGENT_DIR / "concept-dependencies.jsonl", dependencies)
    write_jsonl(AGENT_DIR / "concept-index.jsonl", concept_index_rows(dependencies))
    write_agent_manifest()
    taxonomy = write_concept_taxonomy_audit()
    return {
        "concept_id": concept.id,
        "guide_path": repo_relative_path(output),
        "source_records": len(dependency["source_record_ids"]),
        "baseline_agent_artifacts": baseline_artifacts,
        "concept_taxonomy_status": taxonomy["status"],
    }

def build_concept_guide(
    concept: Concept,
    records: list[dict[str, Any]],
    previous_dependencies: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any]]:
    matched = rank_records_for_concept(concept, records)
    selected = ensure_weighted_source_coverage(concept, matched, concept.max_records)
    supplemental_model_records = supplemental_model_map_records(concept, matched, selected)
    supplemental_lava_records = supplemental_lava_capability_records(concept, records)
    dependency_records = merge_record_lists(selected, supplemental_model_records, supplemental_lava_records)
    previous = previous_dependencies.get(concept.id)
    source_hashes = {record["id"]: record.get("content_hash") for record in dependency_records if record.get("id")}
    model_map_hashes = {
        record["id"]: record.get("content_hash")
        for record in supplemental_model_records
        if record.get("id")
    }
    approved_claim_dependencies = approved_claim_dependencies_for_concept(concept.id)
    approved_claim_hashes = {
        str(row.get("claim_id")): row.get("claim_hash")
        for row in approved_claim_dependencies
        if row.get("claim_id")
    }
    stale_reason = stale_reason_for(previous, source_hashes)
    built_at = generated_at_iso()
    guide_path = relative_concept_path(concept)
    source_lifecycle = concept_source_lifecycle_metadata(
        concept,
        matched,
        selected_records=selected,
    )
    dependency = {
        "concept_id": concept.id,
        "title": concept.title,
        "guide_path": repo_relative_path(guide_path),
        "source_record_ids": list(source_hashes),
        "source_hashes": source_hashes,
        "source_count": len(source_hashes),
        "model_map_record_ids": list(model_map_hashes),
        "model_map_record_hashes": model_map_hashes,
        "model_map_record_count": len(model_map_hashes),
        "lava_capability_record_ids": [record["id"] for record in supplemental_lava_records if record.get("id")],
        "lava_capability_record_hashes": {
            record["id"]: record.get("content_hash") for record in supplemental_lava_records if record.get("id")
        },
        "lava_capability_record_count": len(supplemental_lava_records),
        "approved_claim_ids": list(approved_claim_hashes),
        "approved_claim_hashes": approved_claim_hashes,
        "approved_claim_count": len(approved_claim_hashes),
        "approved_claim_dependencies": approved_claim_dependencies,
        "last_built": built_at,
        "rebuild_policy": concept.rebuild_policy,
        "needs_rebuild": False,
        "stale_reason_before_build": stale_reason,
        "depends_on_topics": concept.depends_on_topics,
        "routing_role": concept.routing_role,
        "parent_concept_id": concept.parent_concept_id,
        "documentation_branches": record_constraint_values(concept.raw, "documentation_branches"),
        "source_freshness": source_lifecycle["source_freshness"],
        "source_native_migration": source_lifecycle["source_native_migration"],
        "guide_hash": "",
    }
    guide = render_concept_guide(concept, selected, matched, dependency)
    dependency["guide_hash"] = sha256_text(guide)
    return guide, dependency


def concept_source_lifecycle_metadata(
    concept: Concept,
    matched_records: list[dict[str, Any]],
    selected_records: list[dict[str, Any]] | None = None,
    source_native_dir: Path | None = None,
) -> dict[str, Any]:
    """Separate upstream article freshness from reviewed typed migration coverage."""
    source_native_dir = source_native_dir or (
        REPO_ROOT / "canonical" / "source-native" / "v1"
    )

    def source_native_rows(filename: str) -> list[dict[str, Any]]:
        path = source_native_dir / filename
        return list(read_jsonl(path)) if path.exists() else []

    uses_explicit_routing = bool(concept_has_path_constraints(concept))
    lifecycle_records = (
        matched_records
        if uses_explicit_routing or selected_records is None
        else selected_records
    )
    article_records = {
        str(record.get("id")): record
        for record in lifecycle_records
        if record.get("id") and record.get("documentation_article_id")
    }
    eligible_ids = set(article_records)

    snapshots = source_native_rows("source-snapshots.jsonl")
    snapshots_by_id = {
        str(row.get("source_snapshot_id")): row
        for row in snapshots
        if row.get("source_snapshot_id")
    }
    snapshot_checks_by_record: dict[str, list[str]] = {}
    snapshot_changes_by_record: dict[str, list[str]] = {}
    for snapshot in snapshots:
        source_record_id = str(snapshot.get("source_record_id") or "")
        if source_record_id not in eligible_ids:
            continue
        checked_at = str(snapshot.get("last_checked_at") or "")
        changed_at = str(snapshot.get("content_changed_at") or "")
        if checked_at:
            snapshot_checks_by_record.setdefault(source_record_id, []).append(
                checked_at
            )
        if changed_at:
            snapshot_changes_by_record.setdefault(source_record_id, []).append(
                changed_at
            )

    checked_values: list[str] = []
    changed_values: list[str] = []
    unknown_checked_count = 0
    for source_record_id, record in article_records.items():
        record_checks = [
            str(value)
            for value in (
                record.get("last_checked_at"),
                record.get("retrieved_at"),
            )
            if value
        ]
        record_checks.extend(snapshot_checks_by_record.get(source_record_id, []))
        if record_checks:
            checked_values.append(max(record_checks))
        else:
            unknown_checked_count += 1
        record_changes = [
            str(value)
            for value in (record.get("content_changed_at"),)
            if value
        ]
        record_changes.extend(snapshot_changes_by_record.get(source_record_id, []))
        if record_changes:
            changed_values.append(max(record_changes))

    activities = {
        str(row.get("generation_activity_id")): row
        for row in source_native_rows("generation-activities.jsonl")
        if row.get("generation_activity_id")
    }
    typed_article_ids: set[str] = set()
    reviewed_artifacts = source_native_rows("reviewed-artifacts.jsonl")
    for reviewed in reviewed_artifacts:
        artifact = reviewed.get("artifact") or {}
        if concept.id not in {
            str(value) for value in artifact.get("concept_ids") or []
        }:
            continue
        activity = activities.get(str(reviewed.get("generation_activity_id") or ""))
        if not activity:
            continue
        for source_snapshot_id in activity.get("source_snapshot_ids") or []:
            snapshot = snapshots_by_id.get(str(source_snapshot_id))
            source_record_id = str((snapshot or {}).get("source_record_id") or "")
            if source_record_id in eligible_ids:
                typed_article_ids.add(source_record_id)

    retired_legacy_summary_ids = {
        str(row.get("source_record_id"))
        for row in source_native_rows("legacy-migrations.jsonl")
        if row.get("source_record_id") in eligible_ids
        and row.get("legacy_knowledge_type") == "source_summary"
        and row.get("coverage") == "full"
        and row.get("review_state") == "reviewer_approved"
    }

    eligible_count = len(eligible_ids)
    typed_count = len(typed_article_ids)
    retired_count = len(retired_legacy_summary_ids)
    if eligible_count == 0:
        migration_status = "not_applicable"
    elif typed_count == 0 and retired_count == 0:
        migration_status = "not_started"
    elif typed_count >= eligible_count and retired_count >= eligible_count:
        migration_status = "complete"
    else:
        migration_status = "partial"
    freshness_status = (
        "not_applicable"
        if eligible_count == 0
        else "complete"
        if unknown_checked_count == 0
        else "partial"
    )
    def coverage_ratio(value: int) -> float:
        return round(value / eligible_count, 4) if eligible_count else 0.0

    return {
        "source_freshness": {
            "status": freshness_status,
            "article_count": eligible_count,
            "oldest_last_checked_at": min(checked_values) if checked_values else None,
            "newest_last_checked_at": max(checked_values) if checked_values else None,
            "newest_content_changed_at": max(changed_values) if changed_values else None,
            "unknown_last_checked_count": unknown_checked_count,
            "basis": "official_article_last_checked_or_retrieved_at",
            "coverage_scope": (
                "explicit_concept_path_routing"
                if uses_explicit_routing
                else "bounded_concept_guide_selection"
            ),
        },
        "source_native_migration": {
            "status": migration_status,
            "eligible_article_count": eligible_count,
            "typed_article_count": typed_count,
            "typed_coverage_ratio": coverage_ratio(typed_count),
            "retired_legacy_summary_count": retired_count,
            "active_legacy_summary_count": max(eligible_count - retired_count, 0),
            "legacy_summary_retirement_ratio": coverage_ratio(retired_count),
        },
    }

def render_concept_guide(
    concept: Concept,
    selected: list[dict[str, Any]],
    all_matches: list[dict[str, Any]],
    dependency: dict[str, Any],
) -> str:
    model_records = supplemental_model_map_records(concept, all_matches, selected)
    display_records = merge_record_lists(selected, model_records)
    source_counts = count_by(display_records, "source_id")
    source_lines = [f"- `{source_id}`: {count}" for source_id, count in sorted(source_counts.items())]
    primary_sources = display_records[:12] if concept_has_path_constraints(concept) else top_records(display_records, limit=12)
    release_records = [record for record in selected if record.get("release_family")][:12]
    model_crosswalk = model_map_crosswalk_for_records(model_records)
    model_change_counts = model_map_pre_alpha_change_counts(model_crosswalk)
    repo_records = [record for record in selected if record.get("repo_url")][:12]
    subguide_sections = render_subguides(concept, all_matches, selected)
    reviewed_media_section = render_reviewed_media_insights(selected)
    approved_claim_section = render_approved_claims_section(dependency.get("approved_claim_dependencies") or [])
    source_freshness = dependency.get("source_freshness") or {
        "status": "not_applicable",
        "newest_last_checked_at": None,
    }
    source_native_migration = dependency.get("source_native_migration") or {
        "status": "not_applicable",
        "typed_article_count": 0,
        "retired_legacy_summary_count": 0,
        "eligible_article_count": 0,
    }

    lines = [
        "---",
        f"id: concept-{concept.id}",
        f"title: {concept.title}",
        "generated: true",
        f"last_built: {dependency['last_built']}",
        f"guide_status: {concept.guide_status}",
        f"rebuild_policy: {concept.rebuild_policy}",
        f"source_count: {len(selected)}",
        f"source_freshness_status: {source_freshness['status']}",
        f"source_last_checked_at: {source_freshness.get('newest_last_checked_at') or ''}",
        f"source_native_migration_status: {source_native_migration['status']}",
        f"source_native_article_coverage: {source_native_migration['typed_article_count']}/{source_native_migration['eligible_article_count']}",
        f"legacy_summary_retirement_coverage: {source_native_migration['retired_legacy_summary_count']}/{source_native_migration['eligible_article_count']}",
        "depends_on_topics:",
    ]
    lines.extend([f"  - {topic}" for topic in concept.depends_on_topics])
    lines.extend(
        [
            "---",
            "",
            f"# {concept.title}",
            "",
            concept.description,
            "",
            "> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.",
            "",
            "## Agent Starting Points",
            "",
        ]
    )
    lines.extend(agent_starting_points(concept, selected))
    lines.extend(
        [
            "",
            "## How To Think About This Area",
            "",
        ]
    )
    lines.extend(render_synthesis_bullets(concept, selected))
    lines.extend(reviewed_media_section)
    lines.extend(approved_claim_section)
    lines.extend(
        [
            "",
            "## Source Coverage",
            "",
        ]
    )
    lines.extend(source_lines or ["- No source records matched."])
    lines.extend(
        [
            "",
            "## Highest Signal Sources",
            "",
            "| Title | Source | Why It Matters | Citation |",
            "| --- | --- | --- | --- |",
        ]
    )
    lines.extend(record_table_rows(primary_sources))
    if model_records:
        lines.extend(
            [
                "",
                "## Data Model Landmarks",
                "",
                "| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for record in model_records:
            crosswalk = model_crosswalk.get(str(record.get("model_name") or record.get("source_title") or ""))
            model_label = escape_table_cell(record.get("model_name") or record.get("source_title") or "")
            model_cell = linked_model_cell(model_label, crosswalk)
            lines.append(
                f"| {model_cell} "
                f"| {escape_table_cell(record.get('model_category') or '')} "
                f"| {escape_table_cell((crosswalk or {}).get('rock_version') or '')} "
                f"| {escape_table_cell((crosswalk or {}).get('property_count') or '')} "
                f"| {escape_table_cell((crosswalk or {}).get('database_property_count') or '')} "
                f"| {escape_table_cell((crosswalk or {}).get('lava_property_count') or '')} "
                f"| {escape_table_cell((crosswalk or {}).get('lava_non_database_property_count') or '')} "
                f"| {escape_table_cell(model_change_counts.get(model_label, 0))} "
                f"| [source]({record.get('source_url')}) |"
            )
        lava_non_db_notes = model_map_lava_non_database_notes(model_crosswalk, limit=8)
        if lava_non_db_notes:
            lines.extend(
                [
                    "",
                    "Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:",
                    "",
                ]
            )
            lines.extend(lava_non_db_notes)
    if release_records:
        lines.extend(
            [
                "",
                "## Version And Release Watch",
                "",
                "| Version | Module | Change | Citation |",
                "| --- | --- | --- | --- |",
            ]
        )
        for record in release_records:
            lines.append(
                f"| {escape_table_cell(record.get('version') or '')} "
                f"| {escape_table_cell(record.get('module') or '')} "
                f"| {escape_table_cell(record.get('summary') or '')} "
                f"| [source]({record.get('source_url')}) |"
            )
    if repo_records:
        lines.extend(
            [
                "",
                "## Repository Landmarks",
                "",
                "| Repository | Language | Inclusion Reason | Citation |",
                "| --- | --- | --- | --- |",
            ]
        )
        for record in repo_records:
            lines.append(
                f"| {escape_table_cell(record.get('repo') or record.get('source_title') or '')} "
                f"| {escape_table_cell(record.get('language') or '')} "
                f"| {escape_table_cell(record.get('inclusion_reason') or '')} "
                f"| [source]({record.get('source_url')}) |"
            )
    lines.extend(subguide_sections)
    lines.extend(render_lava_capability_reference_section(concept, dependency))
    lines.extend(render_source_lifecycle_section(dependency))
    lines.extend(["", "## Rebuild Dependencies", "", f"- Source records: `{len(dependency['source_record_ids'])}`"])
    if dependency.get("lava_capability_record_count"):
        lines.append(f"- Lava capability source records: `{dependency.get('lava_capability_record_count', 0)}`")
    lines.extend(
        [
            f"- Approved claims: `{dependency.get('approved_claim_count', 0)}`",
            "- Dependency file: `agent/concept-dependencies.jsonl`",
            "",
            "When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.",
            "",
        ]
    )
    return "\n".join(lines)


def render_source_lifecycle_section(dependency: dict[str, Any]) -> list[str]:
    freshness = dependency.get("source_freshness") or {}
    migration = dependency.get("source_native_migration") or {}
    if not freshness.get("article_count"):
        return []
    oldest = freshness.get("oldest_last_checked_at") or "unknown"
    newest = freshness.get("newest_last_checked_at") or "unknown"
    article_scope = (
        "routed here"
        if freshness.get("coverage_scope") == "explicit_concept_path_routing"
        else "in the bounded guide selection"
    )
    return [
        "",
        "## Source Lifecycle",
        "",
        f"- Official article records {article_scope}: `{freshness.get('article_count', 0)}`",
        f"- Upstream check range: `{oldest}` through `{newest}`",
        f"- Source-native typed articles: `{migration.get('typed_article_count', 0)}` of `{migration.get('eligible_article_count', 0)}`",
        f"- Legacy source summaries retired: `{migration.get('retired_legacy_summary_count', 0)}`; still active: `{migration.get('active_legacy_summary_count', 0)}`",
        f"- Migration status: `{migration.get('status') or 'not_applicable'}`",
        "",
        "A recent source check or concept rebuild does not imply that every legacy summary has been replaced by reviewed source-native artifacts.",
    ]

def render_lava_capability_reference_section(concept: Concept, dependency: dict[str, Any]) -> list[str]:
    if not dependency.get("lava_capability_record_count"):
        return []
    prefix = "" if concept.id == "lava" else "../lava/"
    return [
        "",
        "## Lava Capability References",
        "",
        "This concept depends on the generated Lava capability layer. Agents should use the stable guidance first, then verify syntax and behavior against the official source and the live Rock instance.",
        "",
        f"- Reference index: [{prefix}lava-reference-index.md]({prefix}lava-reference-index.md)",
        f"- Safety matrix: [{prefix}lava-safety-matrix.md]({prefix}lava-safety-matrix.md)",
        f"- Agent usage examples: [{prefix}lava-agent-usage-examples.md]({prefix}lava-agent-usage-examples.md)",
        "- Machine-readable rows: [agent/lava-capabilities.jsonl](../../../agent/lava-capabilities.jsonl)",
    ]

def render_approved_claims_section(claims: list[dict[str, Any]], limit: int = 18) -> list[str]:
    if not claims:
        return []
    selected = sort_approved_claim_dependencies(claims)[:limit]
    lines = [
        "",
        "## Approved Claims",
        "",
        "These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.",
        "",
        "| Authority | Type | Claim | Source |",
        "| --- | --- | --- | --- |",
    ]
    for row in selected:
        lines.append(render_approved_claim_row(row, include_claim_id=False))
    if len(claims) > limit:
        lines.append(f"| More |  | {len(claims) - limit} additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |")
    return lines

def linked_model_cell(label: str, crosswalk: Optional[dict[str, Any]]) -> str:
    slug = (crosswalk or {}).get("model_slug")
    if not slug:
        return label
    return f"[{label}](../../model-map/models/{slug}.md)"

def supplemental_model_map_records(
    concept: Concept,
    ranked: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    limit: int = 12,
) -> list[dict[str, Any]]:
    selected_models = [record for record in selected if record.get("source_id") == "rock_model_map"]
    ranked_models = [record for record in ranked if record.get("source_id") == "rock_model_map"]
    return merge_record_lists(selected_models, ranked_models)[:limit]

def supplemental_lava_capability_records(concept: Concept, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not should_attach_lava_dependency(concept.id):
        return []
    return merge_record_lists(
        sorted(
            [record for record in records if record.get("source_id") == LAVA_SOURCE_ID],
            key=lambda row: (str(row.get("source_url") or ""), str(row.get("id") or "")),
        )
    )

def merge_record_lists(*record_lists: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = []
    seen: set[str] = set()
    for records in record_lists:
        for record in records:
            record_id = str(record.get("id") or "")
            if not record_id or record_id in seen:
                continue
            seen.add(record_id)
            merged.append(record)
    return merged

def model_map_crosswalk_for_records(model_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not model_records:
        return {}
    model_names = {str(record.get("model_name") or record.get("source_title") or "") for record in model_records}
    path = KNOWLEDGE_DIR / "model-map" / "stable-models.jsonl"
    if not path.exists():
        return {}
    rows = {}
    for row in read_jsonl(path):
        model_name = str(row.get("model_name") or "")
        if model_name in model_names:
            rows[model_name] = row
    return rows

def model_map_lava_non_database_notes(model_crosswalk: dict[str, dict[str, Any]], limit: int = 8) -> list[str]:
    if not model_crosswalk:
        return []
    model_names = set(model_crosswalk)
    model_name_keys = {normalize_model_map_name(model_name) for model_name in model_names}
    models_by_normalized_name = {normalize_model_map_name(name): row for name, row in model_crosswalk.items()}
    path = KNOWLEDGE_DIR / "model-map" / "stable-properties.jsonl"
    if not path.exists():
        return []
    notes = []
    for row in read_jsonl(path):
        if len(notes) >= limit:
            break
        if row.get("model_name") not in model_names and normalize_model_map_name(row.get("model_name")) not in model_name_keys:
            continue
        if not row.get("is_lava_supported_non_database"):
            continue
        model = model_crosswalk.get(str(row.get("model_name") or "")) or models_by_normalized_name.get(
            normalize_model_map_name(row.get("model_name"))
        ) or {}
        notes.append(
            "- `{model}.{property}` is Lava-marked but not database-marked in the generated Model Map"
            " (Rock {rock_version}; source {source_url}).".format(
                model=row.get("model_name"),
                property=row.get("property_name"),
                rock_version=model.get("rock_version") or "unknown",
                source_url=row.get("source_url") or "Model Map",
            )
        )
    return notes

def model_map_pre_alpha_change_counts(model_crosswalk: dict[str, dict[str, Any]]) -> dict[str, int]:
    if not model_crosswalk:
        return {}
    model_names = set(model_crosswalk)
    path = KNOWLEDGE_DIR / "model-map" / "version-diff.jsonl"
    if not path.exists():
        return {}
    counts = {model_name: 0 for model_name in model_names}
    for row in read_jsonl(path):
        model_name = str(row.get("model_name") or "")
        if model_name in counts:
            counts[model_name] += 1
    return counts

def normalize_model_map_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())

def sort_approved_claim_dependencies(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority = {
        "official": 0,
        "source-code-confirmed": 1,
        "release-note-confirmed": 2,
        "rocku-confirmed": 3,
        "community-reviewed": 4,
        "community-unreviewed": 5,
        "agent-inference": 6,
        "needs-live-verification": 7,
        "private-draft": 8,
    }
    return sorted(
        claims,
        key=lambda row: (
            priority.get(str(row.get("authority_tier") or ""), 99),
            bool(row.get("needs_live_verification")),
            str(row.get("claim_type") or ""),
            str(row.get("claim_id") or ""),
            str(row.get("claim") or ""),
        ),
    )

def render_approved_claim_row(row: dict[str, Any], include_claim_id: bool) -> str:
    refs = [ref for ref in row.get("source_refs") or [] if isinstance(ref, dict)]
    source_url = str((refs[0] if refs else {}).get("url") or "")
    source_cell = f"[source]({source_url})" if source_url.startswith("http") else ""
    claim = str(row.get("claim") or "")
    if row.get("needs_live_verification"):
        claim = f"{claim} _(live verification recommended)_"
    cells = []
    if include_claim_id:
        cells.append(f"`{escape_table_cell(row.get('claim_id') or '')}`")
    cells.extend(
        [
            escape_table_cell(row.get("authority_tier") or ""),
            escape_table_cell(row.get("claim_type") or ""),
            escape_table_cell(claim),
            source_cell,
        ]
    )
    return "| " + " | ".join(cells) + " |"

def render_long_form_approved_claims_section(claims: list[dict[str, Any]], limit: int = 12) -> str:
    lines = [
        "",
        APPROVED_CLAIMS_SECTION_START,
        "## Approved Claim Coverage",
        "",
        "This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.",
        "",
    ]
    if not claims:
        lines.extend(["No approved claims are currently routed to this concept.", APPROVED_CLAIMS_SECTION_END, ""])
        return "\n".join(lines)
    selected = sort_approved_claim_dependencies(claims)[:limit]
    lines.extend(
        [
            f"- Approved claims routed to this concept: `{len(claims)}`",
            "- Full generated claim table: `approved-claims.md`",
            "",
            "| Authority | Type | Claim | Source |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in selected:
        lines.append(render_approved_claim_row(row, include_claim_id=False))
    if len(claims) > limit:
        lines.append(f"| More |  | {len(claims) - limit} additional approved claims are tracked in `approved-claims.md`. |  |")
    lines.extend(["", APPROVED_CLAIMS_SECTION_END, ""])
    return "\n".join(lines)

def render_concept_approved_claims_artifact(concept: Concept, claims: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        "generated: true",
        "artifact_level: claim_graph",
        f"approved_claim_count: {len(claims)}",
        "---",
        "",
        f"# {concept.title} Approved Claims",
        "",
        "This generated artifact contains the full approved public claim coverage for the concept. Use the long-form `guide.md` for synthesis and this file for traceability, review, and agent retrieval.",
        "",
    ]
    if not claims:
        lines.extend(["No approved claims are currently routed to this concept.", ""])
        return "\n".join(lines)
    lines.extend(["| Claim ID | Authority | Type | Claim | Source |", "| --- | --- | --- | --- | --- |"])
    lines.extend(render_approved_claim_row(row, include_claim_id=True) for row in sort_approved_claim_dependencies(claims))
    lines.append("")
    return "\n".join(lines)

def render_long_form_approved_media_section(media: list[dict[str, Any]], limit: int = 8) -> str:
    lines = [
        "",
        "<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->",
        "## Approved Media Coverage",
        "",
        "This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.",
        "",
    ]
    if not media:
        lines.extend(["No approved media distillations are currently routed to this concept.", "<!-- END GENERATED APPROVED MEDIA COVERAGE -->", ""])
        return "\n".join(lines)
    selected = sorted(media, key=lambda row: (str(row.get("source_title") or ""), str(row.get("source_record_id") or "")))[:limit]
    lines.extend(
        [
            f"- Approved media records routed to this concept: `{len(media)}`",
            "- Full generated media table: `approved-media.md`",
            "",
            "| Source | Review Status | Insights | Citation |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in selected:
        url = str(row.get("source_url") or "")
        source_cell = f"[{escape_table_cell(row.get('source_title') or row.get('source_record_id') or '')}]({url})" if url.startswith("http") else escape_table_cell(row.get("source_title") or "")
        lines.append(
            f"| {source_cell} "
            f"| {escape_table_cell(row.get('review_status') or '')} "
            f"| {escape_table_cell(row.get('key_insight_count') or 0)} "
            f"| {escape_table_cell(row.get('source_record_id') or '')} |"
        )
    if len(media) > limit:
        lines.append(f"| More |  | {len(media) - limit} additional reviewed media records are tracked in `approved-media.md`. |  |")
    lines.extend(["", "<!-- END GENERATED APPROVED MEDIA COVERAGE -->", ""])
    return "\n".join(lines)

def render_concept_approved_media_artifact(concept: Concept, media: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        "generated: true",
        "artifact_level: media_distillation",
        f"approved_media_count: {len(media)}",
        "---",
        "",
        f"# {concept.title} Approved Media",
        "",
        "This generated artifact contains reviewed public media distillations routed to the concept. It stores public-safe routing metadata only; raw transcripts, media files, and tokenized media URLs stay private.",
        "",
    ]
    if not media:
        lines.extend(["No approved media distillations are currently routed to this concept.", ""])
        return "\n".join(lines)
    lines.extend(["| Source Record | Title | Review Status | Insights | Citation |", "| --- | --- | --- | --- | --- |"])
    for row in sorted(media, key=lambda item: (str(item.get("source_title") or ""), str(item.get("source_record_id") or ""))):
        url = str(row.get("source_url") or "")
        citation = f"[source]({url})" if url.startswith("http") else ""
        lines.append(
            f"| `{escape_table_cell(row.get('source_record_id') or '')}` "
            f"| {escape_table_cell(row.get('source_title') or '')} "
            f"| {escape_table_cell(row.get('review_status') or '')} "
            f"| {escape_table_cell(row.get('key_insight_count') or 0)} "
            f"| {citation} |"
        )
    lines.append("")
    return "\n".join(lines)

def refresh_long_form_approved_claims(
    concept_id: Optional[str] = None,
) -> dict[str, Any]:
    concepts = [get_concept(concept_id)] if concept_id else load_concepts()
    rows = []
    for concept in concepts:
        guide_path = synthesis_output_path(concept.id)
        if not guide_path.exists():
            rows.append(
                {
                    "concept_id": concept.id,
                    "guide_path": relative_path(guide_path),
                    "status": "missing_guide",
                    "approved_claim_count": 0,
                    "approved_media_count": 0,
                    "changed": False,
                }
            )
            continue
        claims = approved_claim_dependencies_for_concept(concept.id)
        media = approved_media_dependencies_for_concept(concept.id)
        artifact_path = guide_path.parent / "approved-claims.md"
        artifact_text = render_concept_approved_claims_artifact(concept, claims)
        previous_artifact = artifact_path.read_text(encoding="utf-8") if artifact_path.exists() else ""
        artifact_changed = previous_artifact != artifact_text
        if artifact_changed:
            artifact_path.write_text(artifact_text, encoding="utf-8")
        media_path = guide_path.parent / "approved-media.md"
        media_text = render_concept_approved_media_artifact(concept, media)
        previous_media = media_path.read_text(encoding="utf-8") if media_path.exists() else ""
        media_changed = previous_media != media_text
        if media_changed:
            media_path.write_text(media_text, encoding="utf-8")
        original = guide_path.read_text(encoding="utf-8")
        rendered_section = render_long_form_approved_claims_section(claims)
        refreshed = replace_or_insert_generated_claim_section(original, rendered_section)
        refreshed = replace_or_insert_generated_media_section(refreshed, render_long_form_approved_media_section(media))
        guide_changed = refreshed != original
        if guide_changed:
            guide_path.write_text(refreshed, encoding="utf-8")
        rows.append(
            {
                "concept_id": concept.id,
                "guide_path": relative_path(guide_path),
                "approved_claims_path": relative_path(artifact_path),
                "approved_media_path": relative_path(media_path),
                "status": "updated" if guide_changed or artifact_changed or media_changed else "current",
                "approved_claim_count": len(claims),
                "approved_media_count": len(media),
                "changed": guide_changed or artifact_changed or media_changed,
                "guide_changed": guide_changed,
                "approved_claims_changed": artifact_changed,
                "approved_media_changed": media_changed,
            }
        )
    return {
        "schema": "rock-kb-long-form-approved-claim-refresh-v1",
        "concept_count": len(rows),
        "updated_count": sum(1 for row in rows if row["changed"]),
        "total_approved_claims": sum(int(row["approved_claim_count"]) for row in rows),
        "total_approved_media": sum(int(row["approved_media_count"]) for row in rows),
        "concepts": rows,
    }

def refresh_long_form_model_map_pointers(concept_id: Optional[str] = None) -> dict[str, Any]:
    concepts = [get_concept(concept_id)] if concept_id else load_concepts()
    rows = []
    for concept in concepts:
        guide_path = synthesis_output_path(concept.id)
        if not guide_path.exists():
            rows.append(
                {
                    "concept_id": concept.id,
                    "guide_path": relative_path(guide_path),
                    "status": "missing_guide",
                    "changed": False,
                }
            )
            continue
        original = guide_path.read_text(encoding="utf-8")
        section = render_long_form_model_map_pointer_section(concept)
        refreshed = replace_or_insert_generated_model_map_pointer_section(original, section)
        changed = refreshed != original
        if changed:
            guide_path.write_text(refreshed, encoding="utf-8")
        rows.append(
            {
                "concept_id": concept.id,
                "guide_path": relative_path(guide_path),
                "status": "updated" if changed else "current",
                "changed": changed,
            }
        )
    return {
        "schema": "rock-kb-long-form-model-map-pointer-refresh-v1",
        "concept_count": len(rows),
        "updated_count": sum(1 for row in rows if row["changed"]),
        "concepts": rows,
    }

def render_long_form_model_map_pointer_section(concept: Concept) -> str:
    concept_index_path = f"index.md#data-model-landmarks"
    return "\n".join(
        [
            MODEL_MAP_POINTER_SECTION_START,
            "## Generated Model Map Pointers",
            "",
            "Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:",
            "",
            f"- Concept data-model landmarks: [{concept.title} index]({concept_index_path})",
            "- Global model-map index: [Rock Model Map](../../model-map/index.md)",
            "- Stable model rows: `../../model-map/stable-models.jsonl`",
            "- Stable property rows: `../../model-map/stable-properties.jsonl`",
            "- Stable method rows: `../../model-map/stable-methods.jsonl`",
            "- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`",
            "- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`",
            "- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`",
            "",
            MODEL_MAP_POINTER_SECTION_END,
            "",
        ]
    )

def replace_or_insert_generated_model_map_pointer_section(guide_text: str, section: str) -> str:
    section = section.strip()
    pattern = re.compile(
        rf"\n*{re.escape(MODEL_MAP_POINTER_SECTION_START)}.*?{re.escape(MODEL_MAP_POINTER_SECTION_END)}\n*",
        re.DOTALL,
    )
    if pattern.search(guide_text):
        return pattern.sub("\n\n" + section + "\n\n", guide_text).rstrip() + "\n"

    first_heading = re.search(r"\n##\s+", guide_text)
    if first_heading:
        return (guide_text[: first_heading.start()].rstrip() + "\n\n" + section + "\n\n" + guide_text[first_heading.start() :].lstrip()).rstrip() + "\n"
    return guide_text.rstrip() + "\n\n" + section + "\n"

def replace_or_insert_generated_claim_section(guide_text: str, section: str) -> str:
    section = section.strip() + "\n"
    pattern = re.compile(
        rf"\n*{re.escape(APPROVED_CLAIMS_SECTION_START)}.*?{re.escape(APPROVED_CLAIMS_SECTION_END)}\n*",
        re.DOTALL,
    )
    if pattern.search(guide_text):
        return pattern.sub("\n\n" + section + "\n", guide_text).rstrip() + "\n"

    source_map_heading = re.search(r"\n## \d*\.?\s*Source Map And Dependency Notes\b", guide_text)
    if source_map_heading:
        return (guide_text[: source_map_heading.start()] + "\n" + section + guide_text[source_map_heading.start() :]).rstrip() + "\n"
    return guide_text.rstrip() + "\n\n" + section

def replace_or_insert_generated_media_section(guide_text: str, section: str) -> str:
    section = section.strip() + "\n"
    start = "<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->"
    end = "<!-- END GENERATED APPROVED MEDIA COVERAGE -->"
    pattern = re.compile(rf"\n*{re.escape(start)}.*?{re.escape(end)}\n*", re.DOTALL)
    if pattern.search(guide_text):
        return pattern.sub("\n\n" + section + "\n", guide_text).rstrip() + "\n"

    claim_section = re.search(rf"{re.escape(APPROVED_CLAIMS_SECTION_END)}\n?", guide_text)
    if claim_section:
        return (guide_text[: claim_section.end()] + "\n" + section + guide_text[claim_section.end() :]).rstrip() + "\n"

    source_map_heading = re.search(r"\n## \d*\.?\s*Source Map And Dependency Notes\b", guide_text)
    if source_map_heading:
        return (guide_text[: source_map_heading.start()] + "\n" + section + guide_text[source_map_heading.start() :]).rstrip() + "\n"
    return guide_text.rstrip() + "\n\n" + section

def agent_starting_points(concept: Concept, selected: list[dict[str, Any]]) -> list[str]:
    points = [
        f"- Start with this concept's official or highest-weight records before using community answers.",
        f"- Check release records when the task could be version-sensitive.",
        f"- Follow citations for operational steps, screenshots, or code before making a change.",
    ]
    if "security" in concept.depends_on_topics:
        points.append("- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.")
    if any(record.get("source_id") == "rock_model_map" for record in selected):
        points.append("- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.")
    if any(record.get("source_id") in {"rock_recipes", "rock_qa"} for record in selected):
        points.append("- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.")
    return points

def render_synthesis_bullets(concept: Concept, selected: list[dict[str, Any]]) -> list[str]:
    bullets = [
        f"- `{concept.title}` spans {', '.join(concept.depends_on_topics[:6]) or 'multiple Rock areas'}. Agents should expect cross-cutting dependencies rather than a single page or table.",
        f"- The strongest source families in this build are: {', '.join(list(count_by(selected, 'source_id'))[:6]) or 'none'}.",
    ]
    topic_counts: dict[str, int] = {}
    for record in selected:
        for topic in record.get("topics") or []:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    top_topics = sorted(topic_counts, key=lambda topic: (-topic_counts[topic], topic))[:8]
    if top_topics:
        bullets.append(f"- Related tags found in source records: {', '.join(top_topics)}.")
    detail_types = sorted({record.get("detail_type") for record in selected if record.get("detail_type")})
    if detail_types:
        bullets.append(f"- Source detail types include: {', '.join(detail_types[:8])}.")
    return bullets

def render_subguides(
    concept: Concept,
    records: list[dict[str, Any]],
    selected_records: Optional[list[dict[str, Any]]] = None,
) -> list[str]:
    if not concept.subguides:
        return []
    lines = ["", "## Subguides", ""]
    for subguide in concept.subguides:
        keywords = [str(value) for value in subguide.get("keywords") or []]
        matched = records_matching_subguide(records, subguide, keywords)[:10]
        media_matches = [
            record
            for record in selected_records or []
            if is_reviewed_media_insight(record) and score_media_insight_for_keywords(record, keywords) > 0
        ][:6]
        lines.extend(
            [
                f"### {subguide.get('title')}",
                "",
                f"Keywords: `{', '.join(keywords)}`",
                "",
            ]
        )
        lines.extend(render_reviewed_media_insights(media_matches, heading="Reviewed distilled media insights", heading_level=4))
        lines.extend(
            [
                "| Title | Source | Summary | Citation |",
                "| --- | --- | --- | --- |",
            ]
        )
        lines.extend(record_table_rows(matched) or ["| No matched records |  |  |  |"])
        lines.append("")
    return lines

def render_reviewed_media_insights(
    records: list[dict[str, Any]],
    heading: str = "Reviewed Media Insights",
    heading_level: int = 2,
) -> list[str]:
    media_records = [record for record in records if is_reviewed_media_insight(record)]
    rows: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for record in media_records:
        insight_items = record.get("key_insights") or []
        if not insight_items:
            insight_items = [{"topic": "", "insight": record.get("summary") or ""}]
        for item in insight_items:
            if isinstance(item, dict):
                topic = str(item.get("topic") or "").strip()
                insight = str(item.get("insight") or "").strip()
                source_url = str(item.get("source_url") or record.get("source_url") or "")
            else:
                topic = ""
                insight = str(item or "").strip()
                source_url = str(record.get("source_url") or "")
            if not insight:
                continue
            key = (str(record.get("id") or ""), topic, insight)
            if key in seen:
                continue
            seen.add(key)
            timestamp = str(item.get("timestamp") or "") if isinstance(item, dict) else ""
            timestamp_url = str(item.get("source_timestamp_url") or "") if isinstance(item, dict) else ""
            citation_url = timestamp_url or source_url
            citation_cell = f"[source]({citation_url})" if citation_url.startswith("http") else escape_table_cell(citation_url)
            rows.append(
                f"| {escape_table_cell(record.get('source_title') or record.get('id') or '')} "
                f"| {escape_table_cell(topic)} "
                f"| {escape_table_cell(timestamp)} "
                f"| {escape_table_cell(insight)} "
                f"| {citation_cell} |"
            )
    if not rows:
        return []
    prefix = "#" * heading_level
    return [
        "",
        f"{prefix} {heading}",
        "",
        "| Source | Topic | Timestamp | Distilled Claim | Citation |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
    ]

def record_table_rows(records: list[dict[str, Any]]) -> list[str]:
    rows = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        key = (record.get("source_title") or "", record.get("source_url") or "")
        if key in seen:
            continue
        seen.add(key)
        title = escape_table_cell(record.get("source_title") or record.get("id") or "")
        source_id = escape_table_cell(record.get("source_id") or "")
        summary = escape_table_cell(record.get("summary") or record.get("excerpt") or "")
        citation = record.get("source_url") or ""
        citation_cell = f"[source]({citation})" if citation.startswith("http") else escape_table_cell(citation)
        row = f"| {title} | {source_id} | {summary} | {citation_cell} |"
        if grep_sensitive_values([row]):
            continue
        rows.append(row)
    return rows

def concept_path(concept: Concept) -> Path:
    return KNOWLEDGE_DIR / "concepts" / concept.id / "index.md"

def relative_concept_path(concept: Concept) -> str:
    return f"knowledge/concepts/{concept.id}/index.md"

def read_dependency_map() -> dict[str, dict[str, Any]]:
    return {
        row.get("concept_id"): row
        for row in read_jsonl(AGENT_DIR / "concept-dependencies.jsonl")
        if row.get("concept_id")
    }

def concept_index_rows(dependencies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in sorted(dependencies, key=lambda item: item.get("concept_id") or ""):
        rows.append(
            {
                "concept_id": row.get("concept_id"),
                "title": row.get("title"),
                "guide_path": row.get("guide_path"),
                "source_count": row.get("source_count"),
                "last_built": row.get("last_built"),
                "needs_rebuild": row.get("needs_rebuild"),
                "depends_on_topics": row.get("depends_on_topics"),
                "routing_role": row.get("routing_role") or "primary",
                "parent_concept_id": row.get("parent_concept_id") or "",
                "documentation_branches": row.get("documentation_branches") or [],
                "source_freshness": row.get("source_freshness") or {},
                "source_native_migration": row.get("source_native_migration") or {},
            }
        )
    return rows

def ensure_baseline_agent_entrypoints(concept: Concept, selected: list[dict[str, Any]], dependency: dict[str, Any]) -> int:
    concept_dir = KNOWLEDGE_DIR / "concepts" / concept.id
    if (concept_dir / "guide-quality.json").exists():
        return 0
    concept_dir.mkdir(parents=True, exist_ok=True)
    (concept_dir / "tasks").mkdir(parents=True, exist_ok=True)
    (concept_dir / "agent-cards").mkdir(parents=True, exist_ok=True)

    sources = baseline_sources(selected)
    section_rows = baseline_section_rows(concept, sources)
    task_rows = baseline_task_cards(concept, sources)
    entity_rows = baseline_entity_rows(concept, selected, sources)
    release_rows = baseline_release_caveats(concept, selected, sources)
    status_rows = baseline_section_status_rows(concept, section_rows, sources)
    tree = baseline_troubleshooting_tree(concept, task_rows)

    artifacts: dict[Path, str] = {
        concept_dir / "quickstart.md": render_baseline_quickstart(concept, task_rows, entity_rows, release_rows, section_rows),
        concept_dir / "approved-claims.md": render_concept_approved_claims_artifact(
            concept,
            approved_claim_dependencies_for_concept(concept.id),
        ),
        concept_dir / "approved-media.md": render_concept_approved_media_artifact(
            concept,
            approved_media_dependencies_for_concept(concept.id),
        ),
        concept_dir / "open-questions.md": render_baseline_open_questions(concept, section_rows, sources),
        concept_dir / "agent-cheatsheet.md": render_baseline_agent_cheatsheet(concept, task_rows, entity_rows, release_rows),
    }
    for path, text in artifacts.items():
        path.write_text(text, encoding="utf-8")
    write_jsonl(concept_dir / "section-source-map.jsonl", section_rows)
    write_jsonl(concept_dir / "section-status.jsonl", status_rows)
    write_jsonl(concept_dir / "task-cards.jsonl", task_rows)
    write_jsonl(concept_dir / "agent-cards.jsonl", task_rows)
    write_jsonl(concept_dir / "entities.jsonl", entity_rows)
    write_jsonl(concept_dir / "release-caveats.jsonl", release_rows)
    write_json(concept_dir / "troubleshooting-tree.json", tree)
    for card in task_rows:
        card_text = render_baseline_task_card(card)
        (concept_dir / "tasks" / f"{card['task_id']}.md").write_text(card_text, encoding="utf-8")
        (concept_dir / "agent-cards" / f"{card['task_id']}.md").write_text(card_text, encoding="utf-8")

    upsert_agent_jsonl(AGENT_DIR / "section-source-map.jsonl", section_rows, concept.id)
    upsert_agent_jsonl(AGENT_DIR / "section-status.jsonl", status_rows, concept.id)
    upsert_agent_jsonl(AGENT_DIR / "concept-task-cards.jsonl", task_rows, concept.id)
    upsert_agent_jsonl(AGENT_DIR / "entity-index.jsonl", entity_rows, concept.id)
    upsert_agent_jsonl(AGENT_DIR / "concept-release-caveats.jsonl", release_rows, concept.id)
    return len(REQUIRED_AGENT_ENTRYPOINT_FILES)

def baseline_sources(selected: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    sources = []
    seen: set[str] = set()
    for record in selected:
        identifier = str(record.get("id") or record.get("source_url") or record.get("source_title") or "")
        if not identifier or identifier in seen:
            continue
        seen.add(identifier)
        sources.append(
            {
                "source_key": baseline_source_key(record),
                "source_record_id": record.get("id"),
                "source_id": record.get("source_id"),
                "source_url": record.get("source_url") or "",
                "title": record.get("source_title") or record.get("title") or record.get("id"),
                "summary": record.get("summary") or record.get("excerpt") or "",
                "content_hash": record.get("content_hash"),
                "release_family": record.get("release_family"),
                "version": record.get("version"),
                "release_date": record.get("release_date"),
                "module": record.get("module"),
                "change_type": record.get("change_type"),
                "severity": record.get("severity"),
            }
        )
        if len(sources) >= limit:
            break
    return sources

def baseline_source_key(record: dict[str, Any]) -> str:
    value = "|".join(
        str(record.get(field) or "")
        for field in ["source_id", "id", "source_url", "source_title"]
    )
    return "baseline:" + sha256_text(value)[:16]

def source_refs(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_key": source.get("source_key"),
            "source_id": source.get("source_id"),
            "source_record_id": source.get("source_record_id"),
            "url": source.get("source_url"),
            "content_hash": source.get("content_hash"),
        }
        for source in sources
    ]

def baseline_section_rows(concept: Concept, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    source_keys = [source["source_key"] for source in sources]
    source_ids = compact_unique(source.get("source_id") for source in sources)
    source_record_ids = compact_unique(source.get("source_record_id") for source in sources)
    citations = [{"label": source.get("title") or source.get("source_id") or "source", "url": source.get("source_url")} for source in sources if source.get("source_url")]
    rows.append(
        {
            "concept_id": concept.id,
            "section_id": "baseline-overview",
            "heading": "Baseline Overview",
            "parent": "",
            "level": 2,
            "start_line": 1,
            "end_line": 1,
            "word_count": count_words(concept.description),
            "citation_count": len(citations),
            "citations": citations,
            "direct_source_keys": source_keys,
            "source_keys": source_keys,
            "source_record_ids": source_record_ids,
            "source_ids": source_ids,
            "authorities": [],
            "trace_mode": "baseline_ranked_sources",
            "confidence": "baseline",
            "needs_live_verification": True,
        }
    )
    for subguide in concept.subguides[:8]:
        rows.append(
            {
                "concept_id": concept.id,
                "section_id": slugify(str(subguide.get("title") or "subguide")),
                "heading": str(subguide.get("title") or "Subguide"),
                "parent": "Baseline Overview",
                "level": 3,
                "start_line": 1,
                "end_line": 1,
                "word_count": count_words(str(subguide.get("focus") or "")),
                "citation_count": len(citations),
                "citations": citations,
                "direct_source_keys": source_keys,
                "source_keys": source_keys,
                "source_record_ids": source_record_ids,
                "source_ids": source_ids,
                "authorities": [],
                "trace_mode": "baseline_ranked_sources",
                "confidence": "baseline",
                "needs_live_verification": True,
            }
        )
    return rows

def baseline_task_cards(concept: Concept, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_urls = compact_unique(source.get("source_url") for source in sources)
    source_keys = compact_unique(source.get("source_key") for source in sources)
    source_record_ids = compact_unique(source.get("source_record_id") for source in sources)
    sections = [str(subguide.get("title") or "") for subguide in concept.subguides if subguide.get("title")]
    templates = concept.subguides[:4] or [{"title": concept.title, "focus": concept.description}]
    rows = []
    for subguide in templates:
        title = f"Inspect {subguide.get('title') or concept.title}"
        task_id = slugify(title)
        rows.append(
            {
                "concept_id": concept.id,
                "task_id": task_id,
                "title": title,
                "goal": str(subguide.get("focus") or f"Gather authoritative context for {concept.title}."),
                "guide_sections": sections[:6] or ["Baseline Overview"],
                "live_records": ["Relevant Rock records", "Configured pages/blocks", "Security roles", "Recent logs"],
                "entities": baseline_entity_names(concept, []),
                "source_keywords": list(subguide.get("keywords") or concept.keywords[:8]),
                "source_urls": source_urls,
                "source_keys": source_keys,
                "source_record_ids": source_record_ids,
                "confidence": "baseline",
                "needs_live_verification": True,
                "steps": [
                    "Start with official or source-code records listed in the source map.",
                    "Use community or org examples only as examples, not as official Rock behavior.",
                    "Inspect live Rock records before changing configuration or code.",
                    "Check release caveats before deciding whether behavior is version-specific.",
                ],
                "do_not_assume": [
                    "Do not treat this baseline task card as a replacement for a detailed authored guide.",
                    "Do not skip source links and live-instance verification.",
                ],
            }
        )
    return rows

def baseline_entity_rows(concept: Concept, selected: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    names = baseline_entity_names(concept, selected)
    source_urls = compact_unique(source.get("source_url") for source in sources)
    source_keys = compact_unique(source.get("source_key") for source in sources)
    source_record_ids = compact_unique(source.get("source_record_id") for source in sources)
    return [
        {
            "concept_id": concept.id,
            "entity": name,
            "purpose": f"Likely relevant Rock entity or configuration surface for {concept.title}. Verify exact usage against source links and live records.",
            "source_urls": source_urls,
            "source_keys": source_keys,
            "source_record_ids": source_record_ids,
            "confidence": "baseline",
            "needs_live_verification": True,
            "agent_notes": ["Generated from concept keywords and ranked source records.", "Confirm joins, filters, and security in the live Rock instance."],
        }
        for name in names
    ]

def baseline_entity_names(concept: Concept, selected: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for record in selected:
        for field in ["model_name", "source_title", "title"]:
            value = str(record.get(field) or "")
            if re.fullmatch(r"[A-Z][A-Za-z0-9]{2,}", value):
                names.append(value)
    for keyword in concept.keywords:
        normalized = " ".join(part.capitalize() for part in re.split(r"[-_\s]+", keyword) if part)
        if normalized and len(normalized) > 2:
            names.append(normalized)
    return compact_unique(names)[:10] or [concept.title]

def baseline_release_caveats(concept: Concept, selected: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    source_by_key = {source["source_key"]: source for source in sources}
    for record in selected:
        if not record.get("release_family"):
            continue
        key = baseline_source_key(record)
        source = source_by_key.get(key) or {
            "source_key": key,
            "source_record_id": record.get("id"),
            "source_id": record.get("source_id"),
            "source_url": record.get("source_url") or "",
            "content_hash": record.get("content_hash"),
        }
        rows.append(
            {
                "concept_id": concept.id,
                "version": record.get("version"),
                "release_date": record.get("release_date"),
                "module": record.get("module"),
                "change_type": record.get("change_type"),
                "severity": record.get("severity") or "unknown",
                "summary": record.get("summary") or record.get("source_title") or "Release note may affect this concept.",
                "source_url": record.get("source_url") or "",
                "source_record_id": record.get("id"),
                "source_key": source.get("source_key"),
                "content_hash": source.get("content_hash"),
                "confidence": "baseline",
            }
        )
        if len(rows) >= 12:
            break
    return rows

def baseline_section_status_rows(
    concept: Concept,
    section_rows: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    refs = source_refs(sources)
    return [
        {
            "concept_id": concept.id,
            "section_id": row["section_id"],
            "heading": row["heading"],
            "status": "baseline_needs_authored_guide",
            "confidence": "baseline",
            "needs_live_verification": True,
            "depends_on_sources": refs,
            "rebuild_reasons": ["source_hash_changed", "authored_guide_missing"],
        }
        for row in section_rows
    ]

def baseline_troubleshooting_tree(concept: Concept, task_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "concept_id": concept.id,
        "generated_at": generated_at_iso(),
        "artifact_level": "baseline",
        "entrypoint": "Choose the task branch closest to the user's request, then inspect source links and live Rock records before acting.",
        "branches": [
            {
                "id": row["task_id"],
                "title": row["title"],
                "when": row["goal"],
                "start_with": row.get("steps", [])[:2],
                "inspect": row.get("live_records") or [],
                "entities": row.get("entities") or [],
                "do_not_assume": row.get("do_not_assume") or [],
                "source_urls": row.get("source_urls") or [],
            }
            for row in task_rows
        ],
    }

def render_baseline_quickstart(
    concept: Concept,
    task_rows: list[dict[str, Any]],
    entity_rows: list[dict[str, Any]],
    release_rows: list[dict[str, Any]],
    section_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        f"title: {concept.title} Quickstart",
        "generated: true",
        "artifact_level: baseline",
        "---",
        "",
        f"# {concept.title} Quickstart",
        "",
        concept.description,
        "",
        "This is a baseline agent entrypoint generated from the concept registry and ranked source records. Prefer a detailed authored guide when one exists.",
        "",
        "## Agent Entry Points",
        "",
        "- Start with `task-cards.jsonl` when the user has an operational task or symptom.",
        "- Use `entities.jsonl` to identify likely records, models, tables, blocks, or configuration surfaces.",
        "- Use `release-caveats.jsonl` before deciding behavior is configuration, customization, or a bug.",
        "- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.",
        "- Use `section-source-map.jsonl` and `section-status.jsonl` to decide which source records need refresh.",
        "",
        "## Primary Tasks",
        "",
    ]
    lines.extend(f"- [{row['title']}](tasks/{row['task_id']}.md): {row['goal']}" for row in task_rows)
    lines.extend(["", "## Likely Entities", ""])
    lines.extend(f"- `{row['entity']}`: {row['purpose']}" for row in entity_rows[:8])
    lines.extend(["", "## Release Caveats", ""])
    if release_rows:
        lines.extend(f"- {row.get('version') or 'unknown version'}: {row.get('summary')}" for row in release_rows[:8])
    else:
        lines.append("- No concept-specific release caveat rows were selected yet. Check global release notes before acting.")
    lines.extend(["", "## Source Map Sections", ""])
    lines.extend(f"- `{row['section_id']}`: {row['heading']} ({row['confidence']})" for row in section_rows)
    lines.append("")
    return "\n".join(lines)

def render_baseline_task_card(card: dict[str, Any]) -> str:
    lines = [
        "---",
        f"concept_id: {card['concept_id']}",
        f"task_id: {card['task_id']}",
        f"title: {card['title']}",
        "generated: true",
        "artifact_level: baseline",
        "---",
        "",
        f"# {card['title']}",
        "",
        card["goal"],
        "",
        "## Steps",
        "",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(card.get("steps") or [], start=1))
    lines.extend(["", "## Live Records To Inspect", ""])
    lines.extend(f"- `{value}`" for value in card.get("live_records") or [])
    lines.extend(["", "## Do Not Assume", ""])
    lines.extend(f"- {value}" for value in card.get("do_not_assume") or [])
    lines.extend(["", "## Source Links", ""])
    lines.extend(f"- {value}" for value in card.get("source_urls") or [])
    lines.append("")
    return "\n".join(lines)

def render_baseline_open_questions(concept: Concept, section_rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        "generated: true",
        "artifact_level: baseline",
        "---",
        "",
        f"# {concept.title} Open Questions",
        "",
        "- Which official docs or source files should become required citations for this concept's authored guide?",
        "- Which live Rock records should agents inspect before changing configuration or code?",
        "- Which release-note ranges materially affect this concept?",
        "- Which community examples are useful patterns, and which are too instance-specific?",
        "",
        "## Current Baseline Sections",
        "",
    ]
    lines.extend(f"- `{row['section_id']}`: {row['heading']}" for row in section_rows)
    lines.extend(["", "## Highest-Ranked Sources", ""])
    lines.extend(f"- [{source.get('title') or source.get('source_id')}]({source.get('source_url')})" for source in sources if source.get("source_url"))
    lines.append("")
    return "\n".join(lines)

def render_baseline_agent_cheatsheet(
    concept: Concept,
    task_rows: list[dict[str, Any]],
    entity_rows: list[dict[str, Any]],
    release_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        "generated: true",
        "artifact_level: baseline",
        "---",
        "",
        f"# {concept.title} Agent Cheatsheet",
        "",
        "## Tasks",
        "",
    ]
    lines.extend(f"- `{row['task_id']}`: {row['title']}" for row in task_rows)
    lines.extend(["", "## Entities", ""])
    lines.extend(f"- `{row['entity']}`" for row in entity_rows[:10])
    lines.extend(["", "## Release Caveat Count", "", f"- {len(release_rows)} baseline caveats selected.", ""])
    return "\n".join(lines)

def write_agent_manifest() -> None:
    write_json(AGENT_DIR / "rock-kb-manifest.json", build_agent_manifest())

def build_agent_manifest() -> dict[str, Any]:
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
                "routing_role": concept.routing_role,
                "parent_concept_id": concept.parent_concept_id,
                "documentation_branches": record_constraint_values(concept.raw, "documentation_branches"),
                "artifact_level": "detailed" if quality else ("baseline" if (concept_dir / "quickstart.md").exists() else "missing"),
                "quickstart": relative_if_exists(concept_dir / "quickstart.md"),
                "guide": relative_if_exists(synthesis_output_path(concept.id)),
                "approved_claims": relative_if_exists(concept_dir / "approved-claims.md"),
                "approved_media": relative_if_exists(concept_dir / "approved-media.md"),
                "live_inspection_checklist": relative_if_exists(concept_dir / "live-inspection-checklist.md"),
                "live_probe_recipes": relative_if_exists(concept_dir / "live-probe-recipes.md"),
                "answers": relative_if_exists(concept_dir / "answers"),
                "task_cards": relative_if_exists(concept_dir / "task-cards.jsonl"),
                "entities": relative_if_exists(concept_dir / "entities.jsonl"),
                "release_caveats": relative_if_exists(concept_dir / "release-caveats.jsonl"),
                "section_source_map": relative_if_exists(concept_dir / "section-source-map.jsonl"),
                "section_status": relative_if_exists(concept_dir / "section-status.jsonl"),
                "troubleshooting_tree": relative_if_exists(concept_dir / "troubleshooting-tree.json"),
                "open_questions": relative_if_exists(concept_dir / "open-questions.md"),
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
            "skill_manifest": "skills/rock-kb-agent/manifest.json",
            "skill_lifecycle": "docs/agent-skill-lifecycle.md",
            "concepts": "knowledge/concepts/*/quickstart.md",
            "tasks": "agent/concept-task-cards.jsonl",
            "entities": "agent/entity-index.jsonl",
            "sections": "agent/section-source-map.jsonl",
            "release_caveats": "agent/concept-release-caveats.jsonl",
            "section_status": "agent/section-status.jsonl",
            "source_summaries": "agent/source-summaries.jsonl",
            "source_summary_report": "agent/source-summary-report.json",
            "concept_taxonomy_report": "agent/concept-taxonomy-report.json",
            "model_map": "knowledge/model-map/index.md",
            "model_map_summary": "agent/model-map-summary.json",
            "model_map_entities": "agent/model-map-entities.jsonl",
            "model_map_properties": "agent/model-map-properties.jsonl",
            "model_map_methods": "agent/model-map-methods.jsonl",
            "model_map_version_diff": "agent/model-map-version-diff.jsonl",
            "model_map_model_details": "knowledge/model-map/models/*.md",
            "lava_capabilities": "agent/lava-capabilities.jsonl",
            "lava_capability_summary": "agent/lava-capability-summary.json",
            "lava_contexts": "agent/lava-contexts.jsonl",
            "lava_context_version_diff": "agent/lava-context-version-diff.jsonl",
            "lava_context_summary": "agent/lava-context-summary.json",
            "lava_context_directory": "knowledge/concepts/lava/lava-context-directory.md",
            "lava_reference_index": "knowledge/concepts/lava/lava-reference-index.md",
            "lava_safety_matrix": "knowledge/concepts/lava/lava-safety-matrix.md",
            "lava_agent_usage_examples": "knowledge/concepts/lava/lava-agent-usage-examples.md",
            "rock_issues": "agent/rock-issues.jsonl",
            "rock_issue_enrichments": "agent/rock-issue-enrichments.jsonl",
            "rock_issue_summary": "agent/rock-issue-summary.json",
            "rock_issue_directory": "knowledge/issues/index.md",
            "rock_issue_investigation_prompt": "docs/prompts/rock-issue-investigation-v1.md",
            "rock_ideas": "agent/rock-ideas.jsonl",
            "rock_idea_relationships": "agent/rock-idea-relationships.jsonl",
            "rock_idea_verification_queue": "agent/rock-idea-verification-queue.jsonl",
            "rock_idea_summary": "agent/rock-idea-summary.json",
            "rock_idea_directory": "knowledge/ideas/index.md",
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
        "rock_issue_count": count_jsonl(AGENT_DIR / "rock-issues.jsonl"),
        "rock_issue_enrichment_count": count_jsonl(AGENT_DIR / "rock-issue-enrichments.jsonl"),
        "rock_idea_count": count_jsonl(AGENT_DIR / "rock-ideas.jsonl"),
        "rock_idea_relationship_count": count_jsonl(AGENT_DIR / "rock-idea-relationships.jsonl"),
        "rock_idea_verification_queue_count": count_jsonl(AGENT_DIR / "rock-idea-verification-queue.jsonl"),
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
