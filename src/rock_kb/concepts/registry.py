from __future__ import annotations

from ._shared import *  # noqa: F401,F403


@dataclass(frozen=True)
class Concept:
    id: str
    title: str
    description: str
    keywords: list[str]
    source_weights: dict[str, int]
    depends_on_topics: list[str]
    subguides: list[dict[str, Any]]
    rebuild_policy: str
    guide_status: str
    max_records: int
    raw: dict[str, Any]
    routing_role: str = "primary"
    parent_concept_id: str = ""

def concept_registry_path() -> Path:
    return CONCEPTS_DIR / "registry.yaml"

def load_concepts(path: Optional[Path] = None) -> list[Concept]:
    registry_path = path or concept_registry_path()
    with registry_path.open("r", encoding="utf-8") as handle:
        registry = yaml.safe_load(handle) or {}
    defaults = registry.get("defaults") or {}
    concepts = []
    for item in registry.get("concepts") or []:
        merged = {**defaults, **item}
        concepts.append(
            Concept(
                id=str(merged["id"]),
                title=str(merged["title"]),
                description=str(merged["description"]),
                keywords=list(merged.get("keywords") or []),
                source_weights=dict(merged.get("source_weights") or {}),
                depends_on_topics=list(merged.get("depends_on_topics") or []),
                subguides=list(merged.get("subguides") or []),
                rebuild_policy=str(merged.get("rebuild_policy", "source_hash_changed_or_weekly")),
                guide_status=str(merged.get("guide_status", "generated_needs_review")),
                max_records=int(merged.get("max_records", 80)),
                raw=merged,
                routing_role=str(merged.get("routing_role") or "primary"),
                parent_concept_id=str(merged.get("parent_concept_id") or ""),
            )
        )
    return concepts

def load_concept_registry_metadata(path: Optional[Path] = None) -> dict[str, Any]:
    registry_path = path or concept_registry_path()
    with registry_path.open("r", encoding="utf-8") as handle:
        registry = yaml.safe_load(handle) or {}
    return {
        "version": int(registry.get("version") or 1),
        "taxonomy": dict(registry.get("taxonomy") or {}),
    }

def get_concept(concept_id: str) -> Concept:
    for concept in load_concepts():
        if concept.id == concept_id:
            return concept
    raise KeyError(f"Unknown concept id: {concept_id}")

def report_concept_staleness() -> list[dict[str, Any]]:
    records = concept_source_records()
    private_impacts = private_impacts_by_concept()
    guide_refresh_rows = {row["concept_id"]: row for row in report_guide_refresh_plan(records).get("concepts", [])}
    rows = []
    for concept in load_concepts():
        dependency = read_dependency_map().get(concept.id)
        matched = rank_records_for_concept(concept, records)
        current_selected = ensure_weighted_source_coverage(concept, matched, concept.max_records)
        supplemental_model_records = supplemental_model_map_records(concept, matched, current_selected)
        supplemental_lava_records = supplemental_lava_capability_records(concept, records)
        dependency_records = merge_record_lists(current_selected, supplemental_model_records, supplemental_lava_records)
        current_hashes = {record["id"]: record.get("content_hash") for record in dependency_records if record.get("id")}
        concept_private_impacts = private_impacts.get(concept.id, [])
        guide_refresh = guide_refresh_rows.get(concept.id, {})
        needs_guide_refresh = bool(guide_refresh.get("needs_long_form_guide_refresh"))
        if not dependency:
            rows.append(
                {
                    "concept_id": concept.id,
                    "title": concept.title,
                    "guide_path": relative_concept_path(concept),
                    "needs_rebuild": True,
                    "reason": "never_built",
                    "changed_source_records": list(current_hashes),
                    "private_dependency_impacts": concept_private_impacts,
                    "private_dependency_impact_count": len(concept_private_impacts),
                    "needs_guide_refresh": needs_guide_refresh,
                    "guide_refresh_reason": guide_refresh.get("long_form_guide_reason"),
                    "approved_media_dependency_count": guide_refresh.get("approved_media_dependency_count", 0),
                    "changed_approved_media_records": guide_refresh.get("changed_approved_media_records", []),
                }
            )
            continue
        previous_hashes = dependency.get("source_hashes") or {}
        added = sorted(set(current_hashes) - set(previous_hashes))
        removed = sorted(set(previous_hashes) - set(current_hashes))
        changed = sorted(
            record_id
            for record_id, current_hash in current_hashes.items()
            if record_id in previous_hashes and previous_hashes[record_id] != current_hash
        )
        needs_rebuild = bool(added or removed or changed or concept_private_impacts or needs_guide_refresh)
        if changed:
            reason = "source_hash_changed"
        elif added:
            reason = "source_record_added"
        elif removed:
            reason = "source_record_removed"
        elif concept_private_impacts:
            reason = "private_source_hash_changed"
        elif needs_guide_refresh:
            reason = "approved_media_guide_refresh_needed"
        else:
            reason = "current"
        rows.append(
            {
                "concept_id": concept.id,
                "title": concept.title,
                "guide_path": dependency.get("guide_path"),
                "needs_rebuild": needs_rebuild,
                "reason": reason,
                "changed_source_records": changed,
                "added_source_records": added,
                "removed_source_records": removed,
                "private_dependency_impacts": concept_private_impacts,
                "private_dependency_impact_count": len(concept_private_impacts),
                "needs_guide_refresh": needs_guide_refresh,
                "guide_refresh_reason": guide_refresh.get("long_form_guide_reason"),
                "approved_media_dependency_count": guide_refresh.get("approved_media_dependency_count", 0),
                "changed_approved_media_records": guide_refresh.get("changed_approved_media_records", []),
                "unmentioned_approved_media_records": guide_refresh.get("unmentioned_approved_media_records", []),
                "last_built": dependency.get("last_built"),
                "source_count": dependency.get("source_count"),
            }
        )
    return rows

def report_guide_refresh_plan(records: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    source_records = records if records is not None else concept_source_records()
    index_dependencies = read_dependency_map()
    rows = []
    for concept in load_concepts():
        claim_dependencies = approved_claim_dependencies_for_concept(concept.id)
        current_claim_hashes = {
            str(row.get("claim_id")): row.get("claim_hash")
            for row in claim_dependencies
            if row.get("claim_id")
        }
        media_dependencies = approved_media_dependencies_for_concept(concept.id, records=source_records)
        current_hashes = {
            str(row.get("source_record_id")): row.get("content_hash")
            for row in media_dependencies
            if row.get("source_record_id")
        }
        index_hashes = (index_dependencies.get(concept.id) or {}).get("source_hashes") or {}
        index_claim_hashes = (index_dependencies.get(concept.id) or {}).get("approved_claim_hashes") or {}
        generated_missing_or_changed = sorted(
            record_id
            for record_id, content_hash in current_hashes.items()
            if index_hashes.get(record_id) != content_hash
        )
        generated_claims_missing_or_changed = sorted(
            claim_id
            for claim_id, claim_hash in current_claim_hashes.items()
            if index_claim_hashes.get(claim_id) != claim_hash
        )
        guide_dependency = read_long_form_guide_dependency(concept.id)
        guide_media_rows = guide_dependency.get("approved_media_dependencies") or []
        guide_hashes = {
            str(row.get("source_record_id")): row.get("content_hash")
            for row in guide_media_rows
            if row.get("source_record_id")
        }
        guide_claim_rows = guide_dependency.get("approved_claim_dependencies") or []
        guide_claim_hashes = {
            str(row.get("claim_id")): row.get("claim_hash")
            for row in guide_claim_rows
            if row.get("claim_id")
        }
        guide_claim_mentioned = {
            str(row.get("claim_id")): bool(row.get("mentioned_in_guide"))
            for row in guide_claim_rows
            if row.get("claim_id")
        }
        guide_mentioned = {
            str(row.get("source_record_id")): bool(row.get("mentioned_in_guide"))
            for row in guide_media_rows
            if row.get("source_record_id")
        }
        changed_approved_media = sorted(
            record_id
            for record_id, content_hash in current_hashes.items()
            if guide_hashes.get(record_id) != content_hash
        )
        removed_approved_media = sorted(set(guide_hashes) - set(current_hashes))
        unmentioned = sorted(
            record_id
            for record_id in current_hashes
            if guide_hashes.get(record_id) == current_hashes.get(record_id) and not guide_mentioned.get(record_id)
        )
        changed_approved_claims = sorted(
            claim_id
            for claim_id, claim_hash in current_claim_hashes.items()
            if guide_claim_hashes.get(claim_id) != claim_hash
        )
        removed_approved_claims = sorted(set(guide_claim_hashes) - set(current_claim_hashes))
        unmentioned_claims = sorted(
            claim_id
            for claim_id in current_claim_hashes
            if guide_claim_hashes.get(claim_id) == current_claim_hashes.get(claim_id) and not guide_claim_mentioned.get(claim_id)
        )
        missing_metadata = bool(current_hashes and not guide_dependency.get("approved_media_dependency_hashes"))
        missing_claim_metadata = bool(current_claim_hashes and not guide_dependency.get("approved_claim_hashes"))
        needs_guide_refresh = bool(
            changed_approved_media
            or removed_approved_media
            or unmentioned
            or missing_metadata
            or changed_approved_claims
            or removed_approved_claims
            or unmentioned_claims
            or missing_claim_metadata
        )
        if changed_approved_media:
            long_form_reason = "approved_media_hash_changed_or_missing"
        elif removed_approved_media:
            long_form_reason = "approved_media_removed"
        elif unmentioned:
            long_form_reason = "approved_media_not_mentioned_in_guide"
        elif missing_metadata:
            long_form_reason = "approved_media_dependency_metadata_missing"
        elif changed_approved_claims:
            long_form_reason = "approved_claim_hash_changed_or_missing"
        elif removed_approved_claims:
            long_form_reason = "approved_claim_removed"
        elif unmentioned_claims:
            long_form_reason = "approved_claim_not_mentioned_in_guide"
        elif missing_claim_metadata:
            long_form_reason = "approved_claim_dependency_metadata_missing"
        else:
            long_form_reason = "current"
        generated_index_changed = sorted(set(generated_missing_or_changed) | set(generated_claims_missing_or_changed))
        rows.append(
            {
                "concept_id": concept.id,
                "title": concept.title,
                "generated_index_path": relative_concept_path(concept),
                "long_form_guide_path": relative_path(synthesis_output_path(concept.id)),
                "needs_generated_index_rebuild": bool(generated_index_changed),
                "needs_long_form_guide_refresh": needs_guide_refresh,
                "generated_index_reason": "approved_claim_or_media_hash_changed_or_missing" if generated_index_changed else "current",
                "long_form_guide_reason": long_form_reason,
                "approved_media_dependency_count": len(current_hashes),
                "approved_claim_dependency_count": len(current_claim_hashes),
                "changed_approved_media_records": changed_approved_media,
                "removed_approved_media_records": removed_approved_media,
                "unmentioned_approved_media_records": unmentioned,
                "changed_approved_claims": changed_approved_claims,
                "removed_approved_claims": removed_approved_claims,
                "unmentioned_approved_claims": unmentioned_claims,
                "generated_index_changed_approved_media_records": generated_missing_or_changed,
                "generated_index_changed_approved_claims": generated_claims_missing_or_changed,
                "guide_dependency_path": relative_path(guide_dependency_path(concept.id)) if guide_dependency_path(concept.id).exists() else "",
                "actions": guide_refresh_actions(bool(generated_index_changed), needs_guide_refresh, concept.id),
            }
        )
    return {
        "schema": "rock-kb-guide-refresh-plan-v1",
        "concept_count": len(rows),
        "needs_generated_index_rebuild": [row["concept_id"] for row in rows if row["needs_generated_index_rebuild"]],
        "needs_long_form_guide_refresh": [row["concept_id"] for row in rows if row["needs_long_form_guide_refresh"]],
        "concepts": rows,
    }

def guide_refresh_actions(needs_index: bool, needs_guide: bool, concept_id: str) -> list[str]:
    actions = []
    if needs_index:
        actions.append("uv run kb build --stage concepts")
    if needs_guide:
        actions.extend(
            [
                f"refresh knowledge/concepts/{concept_id}/guide.md from approved public distillations",
                f"uv run kb build --stage guide-intel --concept {concept_id}",
            ]
        )
    if needs_index or needs_guide:
        actions.extend(["uv run kb build --stage agent-pack", "uv run kb publish export"])
    return actions

def guide_dependency_path(concept_id: str) -> Path:
    return KNOWLEDGE_DIR / "concepts" / concept_id / "guide-dependencies.json"

def read_long_form_guide_dependency(concept_id: str) -> dict[str, Any]:
    path = guide_dependency_path(concept_id)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

def stale_reason_for(previous: Optional[dict[str, Any]], source_hashes: dict[str, Any]) -> str:
    if not previous:
        return "never_built"
    previous_hashes = previous.get("source_hashes") or {}
    if previous_hashes != source_hashes:
        return "source_set_or_hash_changed"
    return "current"
