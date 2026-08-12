from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .canonical_knowledge import build_canonical_knowledge_bundle
from .concepts import (
    concept_has_path_constraints,
    concept_source_records,
    load_concepts,
    record_matches_path_constraints,
    record_text,
    score_text,
    topic_overlap_score,
)
from .extract import sha256_text
from .jsonl import read_jsonl
from .paths import REPO_ROOT, REVIEW_DIR
from .source_native import SOURCE_NATIVE_PROSE_SOURCE_IDS, load_source_native_pilot
from .source_workflows import load_source_freshness_policy
from .sources import Source, load_sources

SOURCE_NATIVE_MIGRATION_PRIORITY_DIR = REVIEW_DIR / "source-native-legacy-migration"
SOURCE_NATIVE_MIGRATION_PRIORITY_PATH = SOURCE_NATIVE_MIGRATION_PRIORITY_DIR / "priority-report.json"
SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA = "rock-kb-source-native-migration-priority-v1"
SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM = "3"
MIGRATION_PROMPT_ID = "source-native-legacy-migration-v1"

SCORE_WEIGHTS = {
    "legacy_claim": 100,
    "legacy_source_summary": 20,
    "verification_debt": 25,
    "exact_evaluation_case": 20,
    "source_native_coverage_gap": 25,
    "source_native_existing": 40,
    "external_signal": 20,
    "concept_routing": 5,
    "freshness_current": 10,
    "freshness_due_soon": 5,
    "freshness_overdue": -50,
    "freshness_missing": -100,
    "concept_routing_missing": -100,
}


def parse_utc(value: str | datetime | None) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif value:
        try:
            parsed = datetime.fromisoformat(str(value))
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def legacy_items_by_source_record(
    bundle: Any,
) -> tuple[dict[str, list[Any]], dict[str, set[str]], dict[str, set[str]]]:
    snapshots_by_id = {row.source_snapshot_id: row for row in bundle.source_snapshots}
    units_by_id = {row.source_unit_id: row for row in bundle.source_units}
    items_by_record: dict[str, list[Any]] = defaultdict(list)
    result_ids_by_record: dict[str, set[str]] = defaultdict(set)
    urls_by_record: dict[str, set[str]] = defaultdict(set)
    for item in bundle.knowledge_units:
        if item.ingestion_mode not in {
            "legacy_reviewed_claim_projection",
            "legacy_summary_projection",
        }:
            continue
        if item.knowledge_type not in {"claim", "source_summary"}:
            continue
        source_record_ids = {
            str(snapshot.source_record_id)
            for source_unit_id in item.source_unit_ids
            if (source_unit := units_by_id.get(source_unit_id))
            and (snapshot := snapshots_by_id.get(source_unit.source_snapshot_id))
            and snapshot.source_record_id
        }
        for source_record_id in source_record_ids:
            items_by_record[source_record_id].append(item)
            result_ids_by_record[source_record_id].update(
                {item.knowledge_unit_id, *item.legacy_ids}
            )
            urls_by_record[source_record_id].update(
                str(snapshot.canonical_url).rstrip("/")
                for source_unit_id in item.source_unit_ids
                if (source_unit := units_by_id.get(source_unit_id))
                and (snapshot := snapshots_by_id.get(source_unit.source_snapshot_id))
                and snapshot.source_record_id
                and str(snapshot.source_record_id) == source_record_id
                and snapshot.canonical_url
            )
    return dict(items_by_record), dict(result_ids_by_record), dict(urls_by_record)


def reconcile_legacy_source_record_ids(
    items_by_record: dict[str, list[Any]],
    result_ids_by_record: dict[str, set[str]],
    urls_by_record: dict[str, set[str]],
    records: dict[str, dict[str, Any]],
) -> tuple[dict[str, list[Any]], dict[str, set[str]], list[dict[str, str]]]:
    record_ids_by_url: dict[str, set[str]] = defaultdict(set)
    for source_record_id, record in records.items():
        for value in [record.get("source_url"), *(record.get("location_aliases") or [])]:
            source_url = str(value or "").rstrip("/")
            if source_url:
                record_ids_by_url[source_url].add(source_record_id)
    aliases: list[dict[str, str]] = []
    reconciled_items: dict[str, list[Any]] = defaultdict(list)
    reconciled_result_ids: dict[str, set[str]] = defaultdict(set)
    for source_record_id, items in items_by_record.items():
        resolved_id = source_record_id
        if source_record_id not in records:
            source_id = source_record_id.split(":", 1)[0]
            candidates = {
                candidate_id
                for source_url in urls_by_record.get(source_record_id) or set()
                for candidate_id in record_ids_by_url.get(source_url) or set()
                if candidate_id.startswith(f"{source_id}:")
            }
            if len(candidates) == 1:
                resolved_id = next(iter(candidates))
                aliases.append(
                    {
                        "legacy_source_record_id": source_record_id,
                        "canonical_source_record_id": resolved_id,
                        "canonical_url": next(iter(sorted(urls_by_record[source_record_id]))),
                    }
                )
        reconciled_items[resolved_id].extend(items)
        reconciled_result_ids[resolved_id].update(
            result_ids_by_record.get(source_record_id) or set()
        )
    aliases.sort(key=lambda row: row["legacy_source_record_id"])
    return dict(reconciled_items), dict(reconciled_result_ids), aliases


def add_source_native_location_aliases(
    records: dict[str, dict[str, Any]],
    snapshots: Iterable[Any],
) -> dict[str, dict[str, Any]]:
    enriched = {source_record_id: {**record} for source_record_id, record in records.items()}
    for snapshot in snapshots:
        source_record_id = str(snapshot.source_record_id or "")
        record = enriched.get(source_record_id)
        if record is None:
            continue
        source_url = str(record.get("source_url") or "").rstrip("/")
        locations = {
            str(value).rstrip("/")
            for value in [
                *(record.get("location_aliases") or []),
                snapshot.canonical_url,
                *snapshot.location_aliases,
            ]
            if value and str(value).rstrip("/") != source_url
        }
        record["location_aliases"] = sorted(locations)
    return enriched


def source_native_indexes(source_native: dict[str, Any]) -> dict[str, Any]:
    snapshots_by_id = {
        row.source_snapshot_id: row for row in source_native["source_snapshots"]
    }
    units_by_id = {row.source_unit_id: row for row in source_native["source_units"]}
    artifact_ids_by_record: dict[str, set[str]] = defaultdict(set)
    artifact_concepts_by_record: dict[str, set[str]] = defaultdict(set)
    artifact_record_by_id: dict[str, str] = {}
    for reviewed in source_native["reviewed_artifacts"]:
        source_record_ids = {
            str(snapshot.source_record_id)
            for source_unit_id in reviewed.artifact.source_unit_ids
            if (unit := units_by_id.get(source_unit_id))
            and (snapshot := snapshots_by_id.get(unit.source_snapshot_id))
            and snapshot.source_record_id
        }
        for source_record_id in source_record_ids:
            artifact_ids_by_record[source_record_id].add(reviewed.artifact_id)
            artifact_concepts_by_record[source_record_id].update(
                reviewed.artifact.concept_ids
            )
            artifact_record_by_id[reviewed.artifact_id] = source_record_id

    migrated_source_records: set[str] = set()
    for activity in source_native["generation_activities"]:
        if activity.prompt_id != MIGRATION_PROMPT_ID:
            continue
        for snapshot_id in activity.source_snapshot_ids:
            snapshot = snapshots_by_id.get(snapshot_id)
            if snapshot and snapshot.source_record_id:
                migrated_source_records.add(str(snapshot.source_record_id))
    return {
        "artifact_ids_by_record": dict(artifact_ids_by_record),
        "artifact_concepts_by_record": dict(artifact_concepts_by_record),
        "artifact_record_by_id": artifact_record_by_id,
        "migrated_source_records": migrated_source_records,
    }


def infer_concept_routing(
    record: dict[str, Any],
    *,
    seeded_concept_ids: Iterable[str],
    legacy_concept_ids: Iterable[str] = (),
    max_inferred: int = 3,
    concepts: Iterable[Any] | None = None,
) -> dict[str, Any]:
    concept_rows = list(concepts) if concepts is not None else load_concepts()
    concepts_by_id = {concept.id: concept for concept in concept_rows}
    known = set(concepts_by_id)
    seeded = {str(value) for value in seeded_concept_ids if str(value) in known}
    if seeded:
        concept_ids = sorted(seeded)
        return {
            "concept_ids": concept_ids,
            "routes": [
                {
                    "concept_id": concept_id,
                    "method": "reviewed_artifact_seeded",
                }
                for concept_id in concept_ids
            ],
            "confidence": "high",
        }
    legacy = {str(value) for value in legacy_concept_ids if str(value) in known}
    record_topics = {str(value) for value in record.get("topics") or []}
    scored: list[tuple[int, int, int, str, str]] = []
    text = record_text(record)
    for concept in concept_rows:
        path_match = concept_has_path_constraints(concept) and record_matches_path_constraints(
            record, concept.raw
        )
        lexical_score = score_text(text, concept.keywords)
        topic_score = topic_overlap_score(record, concept)
        if path_match:
            routing_class = 0
            route_method = "documentation_path"
        elif concept.id in record_topics:
            routing_class = 1
            route_method = "exact_source_topic"
        elif concept.id in legacy and (lexical_score > 0 or topic_score > 0):
            routing_class = 2
            route_method = "supported_legacy"
        elif lexical_score > 0:
            routing_class = 3
            route_method = "lexical_only"
        else:
            continue
        role_order = 0 if concept.routing_role == "primary" else 1
        scored.append(
            (routing_class, -lexical_score, role_order, concept.id, route_method)
        )
    scored.sort(key=lambda row: row[:4])
    if any(row[0] <= 1 for row in scored):
        scored = [row for row in scored if row[0] <= 1]
    elif any(row[0] == 2 for row in scored):
        scored = [row for row in scored if row[0] == 2]
    selected_routes = {
        concept_id: route_method
        for *_scores, concept_id, route_method in scored[:max_inferred]
    }
    concept_ids = sorted(selected_routes)
    methods = set(selected_routes.values())
    if not methods or "lexical_only" in methods:
        confidence = "low"
    elif "supported_legacy" in methods:
        confidence = "medium"
    else:
        confidence = "high"
    return {
        "concept_ids": concept_ids,
        "routes": [
            {
                "concept_id": concept_id,
                "method": selected_routes[concept_id],
            }
            for concept_id in concept_ids
        ],
        "confidence": confidence,
    }


def infer_concept_ids(
    record: dict[str, Any],
    *,
    seeded_concept_ids: Iterable[str],
    legacy_concept_ids: Iterable[str] = (),
    max_inferred: int = 3,
    concepts: Iterable[Any] | None = None,
) -> list[str]:
    return infer_concept_routing(
        record,
        seeded_concept_ids=seeded_concept_ids,
        legacy_concept_ids=legacy_concept_ids,
        max_inferred=max_inferred,
        concepts=concepts,
    )["concept_ids"]


def source_record_freshness(
    record: dict[str, Any],
    source: Source,
    *,
    as_of: datetime,
    policy: dict[str, Any],
) -> dict[str, Any]:
    checked_at = parse_utc(record.get("retrieved_at"))
    maximum_age = (policy.get("cadences") or {}).get(source.refresh_cadence, {}).get(
        "maximum_age_hours"
    )
    if source.refresh_cadence == "manual" or maximum_age is None:
        status = "manual"
        age_hours = None if checked_at is None else max(0.0, (as_of - checked_at).total_seconds() / 3600)
    elif checked_at is None:
        status = "missing"
        age_hours = None
    else:
        age_hours = max(0.0, (as_of - checked_at).total_seconds() / 3600)
        due_soon_fraction = float(policy.get("due_soon_fraction") or 0.75)
        if age_hours > float(maximum_age):
            status = "overdue"
        elif age_hours >= float(maximum_age) * due_soon_fraction:
            status = "due_soon"
        else:
            status = "current"
    return {
        "status": status,
        "cadence": source.refresh_cadence,
        "last_checked_at": checked_at.isoformat() if checked_at else None,
        "age_hours": round(age_hours, 2) if age_hours is not None else None,
        "maximum_age_hours": maximum_age,
    }


def item_needs_live_verification(item: Any) -> bool:
    payload = item.payload if isinstance(item.payload, dict) else {}
    return any(
        bool(claim.get("needs_live_verification"))
        for claim in payload.get("approved_claims") or []
        if isinstance(claim, dict)
    )


def load_evaluation_signals(
    *,
    repo_root: Path,
    result_records: dict[str, set[str]],
    artifact_record_by_id: dict[str, str],
) -> tuple[Counter[str], Counter[str]]:
    exact_counts: Counter[str] = Counter()
    concept_counts: Counter[str] = Counter()
    seen_cases: set[str] = set()
    paths = [
        repo_root / "evaluations" / "real-world.jsonl",
        repo_root / "agent" / "evaluation-set.jsonl",
        repo_root / "canonical" / "source-native" / "v1" / "evaluation-set.jsonl",
        repo_root / "canonical" / "cross-source" / "v1" / "evaluation-set.jsonl",
    ]
    for path in paths:
        for row in read_jsonl(path):
            case_id = str(row.get("id") or "")
            if not case_id or case_id in seen_cases:
                continue
            seen_cases.add(case_id)
            concept_id = str(row.get("concept_id") or "")
            if concept_id:
                concept_counts[concept_id] += 1
            matched_records: set[str] = set()
            for result_id in row.get("expected_result_ids") or []:
                result_id = str(result_id)
                matched_records.update(result_records.get(result_id) or set())
                if result_id in artifact_record_by_id:
                    matched_records.add(artifact_record_by_id[result_id])
            for source_record_id in matched_records:
                exact_counts[source_record_id] += 1
    return exact_counts, concept_counts


def bounded_dashboard_signals(
    dashboard: dict[str, Any] | None,
    *,
    result_records: dict[str, set[str]],
) -> tuple[Counter[str], Counter[str], list[dict[str, Any]]]:
    by_record: Counter[str] = Counter()
    by_concept: Counter[str] = Counter()
    bounded_rows: list[dict[str, Any]] = []
    if not dashboard:
        return by_record, by_concept, bounded_rows
    queues = [
        ((dashboard.get("field_validation") or {}).get("review_queue") or {}).get("items") or [],
        (dashboard.get("retrieval_comparisons") or {}).get("review_queue") or [],
    ]
    for item in [row for queue in queues for row in queue if isinstance(row, dict)]:
        result_id = str(item.get("result_id") or "")
        if not result_id:
            continue
        occurrence_count = max(1, int(item.get("occurrence_count") or 1))
        signal = {
            "result_id": result_id,
            "result_kind": str(item.get("result_kind") or ""),
            "signal": str(item.get("signal") or "negative_outcome"),
            "occurrence_count": occurrence_count,
        }
        bounded_rows.append(signal)
        if result_id.startswith("concept:"):
            by_concept[result_id.removeprefix("concept:")] += occurrence_count
        for source_record_id in result_records.get(result_id) or set():
            by_record[source_record_id] += occurrence_count
    bounded_rows.sort(key=lambda row: (row["result_id"], row["signal"]))
    return by_record, by_concept, bounded_rows


def score_priority_row(row: dict[str, Any]) -> dict[str, Any]:
    freshness = str((row.get("freshness") or {}).get("status") or "missing")
    components = {
        "legacy_claims": min(int(row["legacy_claim_count"]), 5) * SCORE_WEIGHTS["legacy_claim"],
        "legacy_source_summary": min(int(row["legacy_source_summary_count"]), 1)
        * SCORE_WEIGHTS["legacy_source_summary"],
        "verification_debt": min(int(row["verification_debt_count"]), 5)
        * SCORE_WEIGHTS["verification_debt"],
        "exact_evaluation_cases": min(int(row["exact_evaluation_case_count"]), 5)
        * SCORE_WEIGHTS["exact_evaluation_case"],
        "source_native_coverage": (
            SCORE_WEIGHTS["source_native_existing"]
            if row["existing_source_native_artifact_count"]
            else SCORE_WEIGHTS["source_native_coverage_gap"]
        ),
        "external_signals": min(int(row["external_signal_count"]), 3)
        * SCORE_WEIGHTS["external_signal"],
        "concept_routing": (
            SCORE_WEIGHTS["concept_routing"]
            if row["concept_ids"]
            else SCORE_WEIGHTS["concept_routing_missing"]
        ),
        "freshness": SCORE_WEIGHTS.get(f"freshness_{freshness}", 0),
    }
    score = sum(components.values())
    if not row["concept_ids"]:
        recommended_action = "review_concept_routing"
    elif freshness in {"overdue", "missing"}:
        recommended_action = "refresh_source_first"
    elif row["existing_source_native_artifact_count"]:
        recommended_action = "run_legacy_migration_compiler"
    else:
        recommended_action = "generate_source_native_migration"
    priority = "high" if score >= 220 else "medium" if score >= 100 else "low"
    return {
        **row,
        "priority_score": score,
        "priority": priority,
        "score_components": components,
        "recommended_action": recommended_action,
        "migration_ready": recommended_action
        in {"run_legacy_migration_compiler", "generate_source_native_migration"},
    }


def build_source_native_migration_priority_report(
    *,
    destination: Path | None = None,
    repo_root: Path = REPO_ROOT,
    as_of: datetime | None = None,
    limit: int = 200,
    dashboard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if limit < 1:
        raise ValueError("priority report limit must be at least 1")
    destination = destination or (
        repo_root / "data" / "review" / "source-native-legacy-migration" / "priority-report.json"
    )
    as_of = (as_of or datetime.now(UTC)).astimezone(UTC)
    identity_registry = list(
        read_jsonl(repo_root / "canonical" / "identity" / "v1" / "identity-registry.jsonl")
    )
    canonical_bundle_inputs: dict[str, Any] = {
        "identity_registry": identity_registry,
        "include_source_native_pilot": True,
        "include_reviewed_cross_source": True,
        "repo_root": repo_root,
    }
    if repo_root != REPO_ROOT:
        canonical_bundle_inputs["search_rows"] = list(
            read_jsonl(repo_root / "service" / "dist" / "search-rows.jsonl")
        )
    bundle, _summary = build_canonical_knowledge_bundle(
        **canonical_bundle_inputs,
    )
    (
        raw_legacy_by_record,
        raw_result_ids_by_record,
        legacy_urls_by_record,
    ) = legacy_items_by_source_record(bundle)
    source_native = load_source_native_pilot(repo_root)
    records = {
        str(record.get("id") or ""): record
        for record in concept_source_records(repo_root=repo_root)
        if str(record.get("source_id") or "") in SOURCE_NATIVE_PROSE_SOURCE_IDS
        and record.get("id")
    }
    records = add_source_native_location_aliases(
        records,
        source_native["source_snapshots"],
    )
    (
        all_legacy_by_record,
        all_result_ids_by_record,
        source_record_aliases,
    ) = reconcile_legacy_source_record_ids(
        raw_legacy_by_record,
        raw_result_ids_by_record,
        legacy_urls_by_record,
        records,
    )
    supported_prefixes = tuple(f"{source_id}:" for source_id in SOURCE_NATIVE_PROSE_SOURCE_IDS)
    legacy_by_record = {
        source_record_id: items
        for source_record_id, items in all_legacy_by_record.items()
        if source_record_id.startswith(supported_prefixes)
    }
    result_ids_by_record = {
        source_record_id: result_ids
        for source_record_id, result_ids in all_result_ids_by_record.items()
        if source_record_id in legacy_by_record
    }
    result_records: dict[str, set[str]] = defaultdict(set)
    for source_record_id, result_ids in result_ids_by_record.items():
        for result_id in result_ids:
            result_records[result_id].add(source_record_id)

    native = source_native_indexes(source_native)
    for artifact_id, source_record_id in native["artifact_record_by_id"].items():
        result_records[artifact_id].add(source_record_id)

    exact_eval, concept_eval = load_evaluation_signals(
        repo_root=repo_root,
        result_records=result_records,
        artifact_record_by_id=native["artifact_record_by_id"],
    )
    external_by_record, external_by_concept, bounded_external_rows = bounded_dashboard_signals(
        dashboard,
        result_records=result_records,
    )
    sources = {
        source.id: source
        for source in load_sources(repo_root / "sources" / "registry.yaml")
    }
    freshness_policy = load_source_freshness_policy(
        repo_root / "sources" / "freshness-policy.yaml"
    )
    concepts = load_concepts(repo_root / "concepts" / "registry.yaml")
    reviewed_retained = sorted(
        set(legacy_by_record) & set(native["migrated_source_records"])
    )
    unresolved_records = sorted(set(legacy_by_record) - set(records))
    rows: list[dict[str, Any]] = []
    for source_record_id in sorted(set(legacy_by_record) - set(reviewed_retained)):
        record = records.get(source_record_id)
        if record is None:
            continue
        source_id = str(record.get("source_id") or "")
        source = sources.get(source_id)
        if source is None:
            continue
        legacy_items = legacy_by_record[source_record_id]
        legacy_concept_ids = {
            concept_id
            for item in legacy_items
            for concept_id in item.concept_facets
        }
        reviewed_concept_ids = native["artifact_concepts_by_record"].get(source_record_id) or set()
        concept_routing = infer_concept_routing(
            record,
            seeded_concept_ids=reviewed_concept_ids,
            legacy_concept_ids=legacy_concept_ids,
            concepts=concepts,
        )
        concept_ids = concept_routing["concept_ids"]
        external_signal_count = external_by_record[source_record_id] + sum(
            external_by_concept[concept_id] for concept_id in concept_ids
        )
        row = score_priority_row(
            {
                "source_record_id": source_record_id,
                "source_id": source_id,
                "source_title": str(record.get("source_title") or ""),
                "source_url": str(record.get("source_url") or ""),
                "source_content_hash": str(record.get("content_hash") or ""),
                "documentation_path": record.get("documentation_path"),
                "documentation_branches": record.get("documentation_branches") or [],
                "authority_tiers": sorted(
                    {
                        authority
                        for item in legacy_items
                        for authority in item.authority_tiers
                    }
                ),
                "concept_ids": concept_ids,
                "concept_routing": concept_routing,
                "legacy_concept_ids": sorted(legacy_concept_ids),
                "legacy_claim_count": sum(item.knowledge_type == "claim" for item in legacy_items),
                "legacy_source_summary_count": sum(
                    item.knowledge_type == "source_summary" for item in legacy_items
                ),
                "verification_debt_count": sum(
                    item_needs_live_verification(item) for item in legacy_items
                ),
                "existing_source_native_artifact_count": len(
                    native["artifact_ids_by_record"].get(source_record_id) or set()
                ),
                "exact_evaluation_case_count": exact_eval[source_record_id],
                "concept_evaluation_case_count": sum(
                    concept_eval[concept_id] for concept_id in concept_ids
                ),
                "external_signal_count": external_signal_count,
                "freshness": source_record_freshness(
                    record,
                    source,
                    as_of=as_of,
                    policy=freshness_policy,
                ),
            }
        )
        rows.append(row)
    rows.sort(
        key=lambda row: (
            -int(row["priority_score"]),
            -int(row["legacy_claim_count"]),
            str(row["source_record_id"]),
        )
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank

    top_by_concept: dict[str, list[str]] = defaultdict(list)
    top_by_source: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        for concept_id in row["concept_ids"]:
            if len(top_by_concept[concept_id]) < 10:
                top_by_concept[concept_id].append(row["source_record_id"])
        if len(top_by_source[row["source_id"]]) < 10:
            top_by_source[row["source_id"]].append(row["source_record_id"])

    hash_payload = {
        "algorithm_version": SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM,
        "as_of": as_of.isoformat(),
        "score_weights": SCORE_WEIGHTS,
        "rows": rows,
        "reviewed_retained": reviewed_retained,
        "unresolved_records": unresolved_records,
        "source_record_aliases": source_record_aliases,
        "external_signals": bounded_external_rows,
    }
    counts = Counter(str(row["recommended_action"]) for row in rows)
    report = {
        "schema": SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA,
        "algorithm_version": SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM,
        "status": "ok",
        "as_of": as_of.isoformat(),
        "input_hash": sha256_text(canonical_json(hash_payload)),
        "score_weights": SCORE_WEIGHTS,
        "privacy": {
            "raw_queries_included": False,
            "organization_identifiers_included": False,
            "private_rock_data_included": False,
            "external_signals_are_advisory": True,
        },
        "counts": {
            "active_legacy_source_count": len(legacy_by_record),
            "unsupported_source_family_legacy_count": (
                len(all_legacy_by_record) - len(legacy_by_record)
            ),
            "actionable_source_count": len(rows),
            "migration_ready_count": sum(bool(row["migration_ready"]) for row in rows),
            "reviewed_retained_source_count": len(reviewed_retained),
            "unresolved_source_identity_count": len(unresolved_records),
            "reconciled_source_record_alias_count": len(source_record_aliases),
            "by_recommended_action": dict(sorted(counts.items())),
        },
        "reviewed_retained_source_record_ids": reviewed_retained,
        "source_record_aliases": source_record_aliases,
        "unresolved_source_records": [
            {
                "source_record_id": source_record_id,
                "canonical_urls": sorted(legacy_urls_by_record.get(source_record_id) or set()),
            }
            for source_record_id in unresolved_records
        ],
        "bounded_external_signals": bounded_external_rows,
        "top_source_record_ids_by_concept": dict(sorted(top_by_concept.items())),
        "top_source_record_ids_by_source": dict(sorted(top_by_source.items())),
        "rows": rows[:limit],
        "row_limit": limit,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema": SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA,
        "status": "ok",
        "destination": str(destination),
        "input_hash": report["input_hash"],
        **report["counts"],
        "top_rows": [
            {
                "rank": row["rank"],
                "source_record_id": row["source_record_id"],
                "source_title": row["source_title"],
                "priority_score": row["priority_score"],
                "recommended_action": row["recommended_action"],
                "concept_ids": row["concept_ids"],
            }
            for row in rows[:10]
        ],
    }
