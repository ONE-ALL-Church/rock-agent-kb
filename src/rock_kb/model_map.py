from __future__ import annotations

import json
import os
import re
import shutil
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, REPO_ROOT, REVIEW_DIR
from .timestamps import generated_at_iso, now_iso

MODEL_MAP_DIR = KNOWLEDGE_DIR / "model-map"
MODEL_MAP_CONCEPT_DIR = MODEL_MAP_DIR / "concept-slices"
MODEL_MAP_MODELS_DIR = MODEL_MAP_DIR / "models"
MODEL_MAP_INDEX_PATH = MODEL_MAP_DIR / "index.md"
MODEL_MAP_PUBLIC_MODELS_PATH = MODEL_MAP_DIR / "public-models.jsonl"
MODEL_MAP_INSTANCE_SCHEMA_PATH = MODEL_MAP_DIR / "instance-schema.json"
MODEL_MAP_CROSSWALK_PATH = MODEL_MAP_DIR / "entity-crosswalk.jsonl"
MODEL_MAP_RELATIONSHIPS_PATH = MODEL_MAP_DIR / "relationships.jsonl"
MODEL_MAP_REFLECTION_PROPERTIES_PATH = MODEL_MAP_DIR / "reflection-properties.jsonl"
MODEL_MAP_STABLE_MODELS_PATH = MODEL_MAP_DIR / "stable-models.jsonl"
MODEL_MAP_LATEST_MODELS_PATH = MODEL_MAP_DIR / "latest-models.jsonl"
MODEL_MAP_STABLE_PROPERTIES_PATH = MODEL_MAP_DIR / "stable-properties.jsonl"
MODEL_MAP_LATEST_PROPERTIES_PATH = MODEL_MAP_DIR / "latest-properties.jsonl"
MODEL_MAP_STABLE_METHODS_PATH = MODEL_MAP_DIR / "stable-methods.jsonl"
MODEL_MAP_LATEST_METHODS_PATH = MODEL_MAP_DIR / "latest-methods.jsonl"
MODEL_MAP_PUBLIC_VERSION_DIFF_PATH = MODEL_MAP_DIR / "version-diff.json"
MODEL_MAP_PUBLIC_VERSION_DIFF_JSONL_PATH = MODEL_MAP_DIR / "version-diff.jsonl"

AGENT_MODEL_MAP_SUMMARY_PATH = AGENT_DIR / "model-map-summary.json"
AGENT_MODEL_MAP_ENTITIES_PATH = AGENT_DIR / "model-map-entities.jsonl"
AGENT_MODEL_MAP_RELATIONSHIPS_PATH = AGENT_DIR / "model-map-relationships.jsonl"
AGENT_MODEL_MAP_REFLECTION_PATH = AGENT_DIR / "model-map-reflection-properties.jsonl"
AGENT_MODEL_MAP_PROPERTIES_PATH = AGENT_DIR / "model-map-properties.jsonl"
AGENT_MODEL_MAP_METHODS_PATH = AGENT_DIR / "model-map-methods.jsonl"
AGENT_MODEL_MAP_VERSION_DIFF_PATH = AGENT_DIR / "model-map-version-diff.jsonl"
AGENT_MODEL_MAP_DIGESTS_PATH = AGENT_DIR / "model-map-digests.jsonl"

DEMO_ROCK_VERSION_ENDPOINT = "https://rocksolidchurchdemo.com/api/Utility/GetRockSemanticVersionNumber"
DEMO_MODEL_MAP_SCRAPE_PATH = REVIEW_DIR / "model-map-scrape" / "demo-model-map-full-scrape.json"
LATEST_ROCK_VERSION_ENDPOINT = "https://rockrmslatest.com/api/Utility/GetRockSemanticVersionNumber"
LATEST_MODEL_MAP_SCRAPE_PATH = REVIEW_DIR / "model-map-scrape" / "latest-model-map-full-scrape.json"
MODEL_MAP_VERSION_DIFF_PATH = REVIEW_DIR / "model-map-scrape" / "stable-vs-latest-model-map-diff.json"
MODEL_MAP_VERSION_DIFF_JSONL_PATH = REVIEW_DIR / "model-map-scrape" / "stable-vs-latest-model-map-diff.jsonl"

MODEL_MAP_VERSION_TRACKS = {
    "stable": {
        "label": "stable",
        "endpoint_url": DEMO_ROCK_VERSION_ENDPOINT,
        "source_url": "https://rocksolidchurchdemo.com/admin/power-tools/model-map",
    },
    "latest": {
        "label": "latest/pre-alpha",
        "endpoint_url": LATEST_ROCK_VERSION_ENDPOINT,
        "source_url": "https://rockrmslatest.com/admin/power-tools/model-map",
    },
}


def model_map_generated_at(*scrapes: dict[str, Any]) -> str:
    if os.environ.get("ROCK_KB_GENERATED_AT") or os.environ.get("SOURCE_DATE_EPOCH"):
        return generated_at_iso()
    candidates = [
        str(scrape.get(field))
        for scrape in scrapes
        for field in ("finished_at", "rock_version_probed_at", "started_at")
        if scrape.get(field)
    ]
    return max(candidates).replace("Z", "+00:00") if candidates else generated_at_iso()


def build_model_map(
    stable_scrape_path: Path = DEMO_MODEL_MAP_SCRAPE_PATH,
    latest_scrape_path: Path = LATEST_MODEL_MAP_SCRAPE_PATH,
) -> dict[str, Any]:
    """Build public model-map artifacts from scraped generic Rock Model Map pages."""
    MODEL_MAP_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_MAP_CONCEPT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_MAP_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_DIR.mkdir(parents=True, exist_ok=True)

    remove_legacy_model_map_outputs()
    stable = load_model_map_scrape(stable_scrape_path)
    latest = load_model_map_scrape(latest_scrape_path)
    stable_models = scraped_model_rows(stable, stable_scrape_path, track="stable")
    latest_models = scraped_model_rows(latest, latest_scrape_path, track="pre-alpha")
    stable_properties = scraped_property_rows(stable, stable_scrape_path, track="stable")
    latest_properties = scraped_property_rows(latest, latest_scrape_path, track="pre-alpha")
    stable_methods = scraped_method_rows(stable, stable_scrape_path, track="stable")
    latest_methods = scraped_method_rows(latest, latest_scrape_path, track="pre-alpha")
    diff_result = build_model_map_version_diff(
        stable_path=stable_scrape_path,
        latest_path=latest_scrape_path,
        output_path=MODEL_MAP_PUBLIC_VERSION_DIFF_PATH,
        output_jsonl_path=MODEL_MAP_PUBLIC_VERSION_DIFF_JSONL_PATH,
    )
    diff_rows = list(read_jsonl(MODEL_MAP_PUBLIC_VERSION_DIFF_JSONL_PATH))
    model_digests = build_model_map_digests(stable_models, stable_properties, stable_methods, diff_rows)
    model_detail_count = build_scraped_model_detail_pages(stable_models, stable_properties, diff_rows)
    concept_rows = build_scraped_concept_slice_pages(stable_models)

    write_jsonl(MODEL_MAP_STABLE_MODELS_PATH, stable_models)
    write_jsonl(MODEL_MAP_LATEST_MODELS_PATH, latest_models)
    write_jsonl(MODEL_MAP_STABLE_PROPERTIES_PATH, stable_properties)
    write_jsonl(MODEL_MAP_LATEST_PROPERTIES_PATH, latest_properties)
    write_jsonl(MODEL_MAP_STABLE_METHODS_PATH, stable_methods)
    write_jsonl(MODEL_MAP_LATEST_METHODS_PATH, latest_methods)
    write_jsonl(AGENT_MODEL_MAP_ENTITIES_PATH, agent_scraped_entity_rows(stable_models))
    write_jsonl(AGENT_MODEL_MAP_PROPERTIES_PATH, stable_properties)
    write_jsonl(AGENT_MODEL_MAP_METHODS_PATH, stable_methods)
    write_jsonl(AGENT_MODEL_MAP_VERSION_DIFF_PATH, diff_rows)
    write_jsonl(AGENT_MODEL_MAP_DIGESTS_PATH, model_digests)

    summary = build_scraped_summary(
        stable=stable,
        latest=latest,
        stable_models=stable_models,
        latest_models=latest_models,
        stable_properties=stable_properties,
        latest_properties=latest_properties,
        stable_methods=stable_methods,
        latest_methods=latest_methods,
        concept_rows=concept_rows,
        model_detail_count=model_detail_count,
        diff_result=diff_result,
        stable_scrape_path=stable_scrape_path,
        latest_scrape_path=latest_scrape_path,
    )
    AGENT_MODEL_MAP_SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    MODEL_MAP_INDEX_PATH.write_text(render_scraped_index_md(summary, stable_models), encoding="utf-8")

    return {
        "source": model_map_summary_source(stable, latest),
        "stable_version": summary["stable"].get("rock_version"),
        "pre_alpha_version": summary["latest"].get("rock_version"),
        "stable_models": len(stable_models),
        "pre_alpha_models": len(latest_models),
        "stable_properties": len(stable_properties),
        "pre_alpha_properties": len(latest_properties),
        "stable_methods": len(stable_methods),
        "pre_alpha_methods": len(latest_methods),
        "stable_lava_properties": sum(1 for row in stable_properties if row.get("is_lava")),
        "stable_non_database_lava_properties": sum(1 for row in stable_properties if row.get("is_lava_supported_non_database")),
        "concept_slices": len(concept_rows),
        "model_detail_pages": model_detail_count,
        "version_diff_changes": diff_result["change_count"],
        "model_digests": len(model_digests),
    }


def remove_legacy_model_map_outputs() -> None:
    """Remove the prior SQL/source-derived model-map outputs from the public layer."""
    for path in [
        MODEL_MAP_PUBLIC_MODELS_PATH,
        MODEL_MAP_INSTANCE_SCHEMA_PATH,
        MODEL_MAP_CROSSWALK_PATH,
        MODEL_MAP_RELATIONSHIPS_PATH,
        MODEL_MAP_REFLECTION_PROPERTIES_PATH,
        AGENT_MODEL_MAP_RELATIONSHIPS_PATH,
        AGENT_MODEL_MAP_REFLECTION_PATH,
    ]:
        if path.exists():
            path.unlink()
    for path in [MODEL_MAP_CONCEPT_DIR, MODEL_MAP_MODELS_DIR]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def scraped_model_rows(scrape: dict[str, Any], scrape_path: Path, track: str) -> list[dict[str, Any]]:
    rows = []
    source_path = public_source_path(scrape_path)
    for model in scrape.get("models") or []:
        model_name = model_display_name(model)
        if not model_name:
            continue
        properties = [prop for prop in model.get("properties") or [] if is_model_property_row(prop)]
        slug = slugify(model_name)
        rows.append(
            {
                "schema": "rock-kb-scraped-model-map-model-v1",
                "track": track,
                "rock_version": model.get("rock_version") or scrape.get("rock_version"),
                "source_url": scrape.get("source_url"),
                "source_path": source_path,
                "model_name": model_name,
                "model_title": model.get("model_title"),
                "collection_method": scrape.get("collection_method") or "page_script_scrape",
                "initialization_endpoint": model.get("initialization_endpoint")
                or (scrape.get("obsidian_block_action") or {}).get("initialization_endpoint"),
                "detail_endpoint": model.get("detail_endpoint")
                or (scrape.get("obsidian_block_action") or {}).get("detail_endpoint"),
                "block_guid": model.get("block_guid") or (scrape.get("obsidian_block_action") or {}).get("block_guid"),
                "block_type_guid": model.get("block_type_guid")
                or (scrape.get("obsidian_block_action") or {}).get("block_type_guid"),
                "block_file_url": model.get("block_file_url")
                or (scrape.get("obsidian_block_action") or {}).get("block_file_url"),
                "model_slug": slug,
                "model_category": model.get("category_name") or "Other",
                "model_guid": model.get("model_guid"),
                "entity_type_id": model.get("selected_entity_type_id") or None,
                "entity_type_guid": model.get("selected_entity_type_guid") or model.get("model_guid"),
                "table_name": model.get("table_name"),
                "is_obsolete": bool(model.get("is_obsolete")),
                "obsolete_message": model.get("obsolete_message"),
                "description": normalize_description(model.get("description") or ""),
                "example": normalize_description(model.get("example") or ""),
                "property_count": int(model.get("property_count") or len(properties)),
                "database_property_count": int(model.get("database_property_count") or 0),
                "lava_property_count": int(model.get("lava_property_count") or 0),
                "lava_non_database_property_count": sum(
                    1 for prop in properties if bool(prop.get("is_lava")) and not bool(prop.get("is_database"))
                ),
                "not_mapped_property_count": int(model.get("not_mapped_property_count") or 0),
                "required_property_count": int(model.get("required_property_count") or 0),
                "qualifier_property_count": int(model.get("qualifier_property_count") or 0),
                "obsolete_property_count": int(model.get("obsolete_property_count") or 0),
                "enum_value_property_count": int(model.get("enum_value_property_count") or 0),
                "related_entity_property_count": int(model.get("related_entity_property_count") or 0),
                "method_count": int(model.get("method_count") or len(model.get("methods") or [])),
                "obsolete_method_count": int(model.get("obsolete_method_count") or 0),
                "model_detail_path": f"knowledge/model-map/models/{slug}.md",
                "contains_row_data": False,
                "source_keys": [f"rock_model_map_scrape_{track}"],
                "source_urls": [scrape.get("source_url")] if scrape.get("source_url") else [],
            }
        )
    return sorted(rows, key=lambda row: (row["model_category"], row["model_name"]))


def scraped_property_rows(scrape: dict[str, Any], scrape_path: Path, track: str) -> list[dict[str, Any]]:
    rows = []
    source_path = public_source_path(scrape_path)
    for model in scrape.get("models") or []:
        model_name = model_display_name(model)
        model_slug = slugify(model_name)
        for prop in model.get("properties") or []:
            if not is_model_property_row(prop):
                continue
            property_name = str(prop.get("name") or prop.get("property_name") or "").strip()
            rows.append(
                {
                    "schema": "rock-kb-scraped-model-map-property-v1",
                    "track": track,
                    "source_url": scrape.get("source_url"),
                    "source_path": source_path,
                    "model_name": model_name,
                    "model_title": model.get("model_title"),
                    "model_slug": model_slug,
                    "model_category": model.get("category_name") or "Other",
                    "property_name": property_name,
                    "property_slug": slugify(property_name),
                    "property_key": f"{model_slug}:{slugify(property_name)}",
                    "collection_method": scrape.get("collection_method") or "page_script_scrape",
                    "inherited": bool(prop.get("inherited")),
                    "is_database": bool(prop.get("is_database")),
                    "is_not_mapped": bool(prop.get("is_not_mapped")),
                    "is_lava": bool(prop.get("is_lava")),
                    "is_lava_supported_non_database": bool(prop.get("is_lava")) and not bool(prop.get("is_database")),
                    "is_qualifier": bool(prop.get("is_qualifier")),
                    "is_required": bool(prop.get("is_required")),
                    "is_obsolete": bool(prop.get("is_obsolete")),
                    "is_virtual": bool(prop.get("is_virtual")),
                    "is_enum": bool(prop.get("is_enum")),
                    "is_defined_value": bool(prop.get("is_defined_value")),
                    "obsolete_message": prop.get("obsolete_message"),
                    "description": normalize_description(prop.get("description") or ""),
                    "related_entity_links": scraped_related_links(prop.get("related_entity_links") or []),
                    "related_defined_type_links": scraped_related_links(prop.get("related_defined_type_links") or []),
                    "enum_values": normalize_enum_values(prop.get("enum_values") or []),
                    "contains_row_data": False,
                    "source_keys": [f"rock_model_map_scrape_{track}"],
                    "source_urls": [scrape.get("source_url")] if scrape.get("source_url") else [],
                }
            )
    return sorted(rows, key=lambda row: (row["model_category"], row["model_name"], row["property_name"]))


def scraped_method_rows(scrape: dict[str, Any], scrape_path: Path, track: str) -> list[dict[str, Any]]:
    rows = []
    source_path = public_source_path(scrape_path)
    for model in scrape.get("models") or []:
        model_name = model_display_name(model)
        model_slug = slugify(model_name)
        for method in model.get("methods") or []:
            signature = str(method.get("signature") or "").strip()
            if not signature:
                continue
            rows.append(
                {
                    "schema": "rock-kb-scraped-model-map-method-v1",
                    "track": track,
                    "source_url": scrape.get("source_url"),
                    "source_path": source_path,
                    "collection_method": scrape.get("collection_method") or "page_script_scrape",
                    "model_name": model_name,
                    "model_title": model.get("model_title"),
                    "model_slug": model_slug,
                    "model_category": model.get("category_name") or "Other",
                    "method_key": f"{model_slug}:{signature}",
                    "signature": signature,
                    "inherited": bool(method.get("inherited")),
                    "is_obsolete": bool(method.get("is_obsolete")),
                    "obsolete_message": method.get("obsolete_message"),
                    "description": normalize_description(method.get("description") or ""),
                    "contains_row_data": False,
                    "source_keys": [f"rock_model_map_scrape_{track}"],
                    "source_urls": [scrape.get("source_url")] if scrape.get("source_url") else [],
                }
            )
    return sorted(rows, key=lambda row: (row["model_category"], row["model_name"], row["signature"]))


def public_source_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_scraped_model_detail_pages(
    model_rows: list[dict[str, Any]],
    property_rows: list[dict[str, Any]],
    diff_rows: list[dict[str, Any]],
) -> int:
    properties_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in property_rows:
        properties_by_model[str(row.get("model_name") or "")].append(row)
    changes_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in diff_rows:
        changes_by_model[str(row.get("model_name") or "")].append(row)
    models_by_key = {normalize_name(row.get("model_name")): row for row in model_rows}
    count = 0
    for model in model_rows:
        path = MODEL_MAP_MODELS_DIR / f"{model.get('model_slug')}.md"
        path.write_text(
            render_scraped_model_detail_md(
                model,
                properties_by_model.get(str(model.get("model_name") or ""), []),
                changes_by_model.get(str(model.get("model_name") or ""), []),
                models_by_key,
            ),
            encoding="utf-8",
        )
        count += 1
    return count


def build_model_map_digests(
    model_rows: list[dict[str, Any]],
    property_rows: list[dict[str, Any]],
    method_rows: list[dict[str, Any]],
    diff_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    properties_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in property_rows:
        properties_by_model[str(row.get("model_slug") or "")].append(row)
    methods_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in method_rows:
        methods_by_model[str(row.get("model_slug") or "")].append(row)
    changes_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in diff_rows:
        changes_by_model[str(row.get("model_name") or "")].append(row)
    models_by_key = {normalize_name(row.get("model_name")): row for row in model_rows}
    return [
        build_model_map_digest(
            model,
            properties_by_model.get(str(model.get("model_slug") or ""), []),
            methods_by_model.get(str(model.get("model_slug") or ""), []),
            changes_by_model.get(str(model.get("model_name") or ""), []),
            models_by_key,
        )
        for model in model_rows
    ]


def build_model_map_digest(
    model: dict[str, Any],
    properties: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    changes: list[dict[str, Any]],
    models_by_key: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    property_groups = {
        "database": [compact_property(row) for row in properties if row.get("is_database")],
        "lava": [compact_property(row) for row in properties if row.get("is_lava")],
        "lava_non_database": [compact_property(row) for row in properties if row.get("is_lava_supported_non_database")],
        "not_mapped": [compact_property(row) for row in properties if row.get("is_not_mapped")],
        "required": [compact_property(row) for row in properties if row.get("is_required")],
        "enum": [compact_property(row) for row in properties if row.get("is_enum")],
        "defined_value": [compact_property(row) for row in properties if row.get("is_defined_value")],
        "obsolete": [compact_property(row) for row in properties if row.get("is_obsolete")],
    }
    relationships = [
        {
            "property_name": row.get("property_name"),
            "related_model": row.get("related_model"),
            "entity_type_guid": row.get("entity_type_guid"),
            "target_model_slug": (row.get("target_model") or {}).get("model_slug") if row.get("target_model") else None,
        }
        for row in related_model_links_for_properties(properties, models_by_key)
    ]
    return {
        "schema": "rock-kb-agent-model-map-digest-v1",
        "identity": {
            "track": model.get("track"),
            "rock_version": model.get("rock_version"),
            "model_slug": model.get("model_slug"),
            "model_name": model.get("model_name"),
            "model_title": model.get("model_title"),
            "model_category": model.get("model_category"),
            "table_name": model.get("table_name"),
            "entity_type_id": model.get("entity_type_id"),
            "entity_type_guid": model.get("entity_type_guid"),
            "model_guid": model.get("model_guid"),
            "is_obsolete": bool(model.get("is_obsolete")),
            "obsolete_message": model.get("obsolete_message"),
            "source_url": model.get("source_url"),
            "model_detail_path": model.get("model_detail_path"),
            "collection_method": model.get("collection_method"),
            "initialization_endpoint": model.get("initialization_endpoint"),
            "detail_endpoint": model.get("detail_endpoint"),
        },
        "counts": {
            "properties": model.get("property_count") or len(properties),
            "database_properties": model.get("database_property_count") or len(property_groups["database"]),
            "lava_properties": model.get("lava_property_count") or len(property_groups["lava"]),
            "lava_non_database_properties": model.get("lava_non_database_property_count") or len(property_groups["lava_non_database"]),
            "not_mapped_properties": model.get("not_mapped_property_count") or len(property_groups["not_mapped"]),
            "required_properties": model.get("required_property_count") or len(property_groups["required"]),
            "enum_properties": model.get("enum_value_property_count") or len(property_groups["enum"]),
            "defined_value_properties": sum(1 for row in properties if row.get("is_defined_value")),
            "obsolete_properties": model.get("obsolete_property_count") or len(property_groups["obsolete"]),
            "relationships": len(relationships),
            "methods": model.get("method_count") or len(methods),
            "obsolete_methods": model.get("obsolete_method_count") or sum(1 for row in methods if row.get("is_obsolete")),
            "version_diffs": len(changes),
        },
        "required_fields": property_groups["required"],
        "operational_notes": model_map_operational_notes(model, property_groups, changes),
        "relationships": relationships,
        "version_diffs": [compact_version_diff(row) for row in changes],
        "property_groups": property_groups,
        "methods": [compact_method(row) for row in methods],
        "paths": {
            "model_detail": model.get("model_detail_path"),
            "stable_models": "knowledge/model-map/stable-models.jsonl",
            "stable_properties": "knowledge/model-map/stable-properties.jsonl",
            "stable_methods": "knowledge/model-map/stable-methods.jsonl",
            "version_diff": "knowledge/model-map/version-diff.jsonl",
        },
    }


def compact_property(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": row.get("property_name"),
        "slug": row.get("property_slug"),
        "description": row.get("description"),
        "flags": {
            "database": bool(row.get("is_database")),
            "lava": bool(row.get("is_lava")),
            "lava_non_database": bool(row.get("is_lava_supported_non_database")),
            "not_mapped": bool(row.get("is_not_mapped")),
            "required": bool(row.get("is_required")),
            "obsolete": bool(row.get("is_obsolete")),
            "enum": bool(row.get("is_enum")),
            "defined_value": bool(row.get("is_defined_value")),
            "virtual": bool(row.get("is_virtual")),
            "qualifier": bool(row.get("is_qualifier")),
            "inherited": bool(row.get("inherited")),
        },
        "related_entities": [
            {
                "text": link.get("text"),
                "entity_type_guid": link.get("entity_type_guid"),
            }
            for link in row.get("related_entity_links") or []
        ],
        "related_defined_types": [
            {
                "text": link.get("text"),
                "entity_type_guid": link.get("entity_type_guid"),
            }
            for link in row.get("related_defined_type_links") or []
        ],
        "enum_values": row.get("enum_values") or [],
        "obsolete_message": row.get("obsolete_message"),
    }


def compact_method(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature": row.get("signature"),
        "description": row.get("description"),
        "inherited": bool(row.get("inherited")),
        "is_obsolete": bool(row.get("is_obsolete")),
        "obsolete_message": row.get("obsolete_message"),
    }


def compact_version_diff(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "change_type": row.get("change_type"),
        "property_name": row.get("property_name"),
        "changed_fields": row.get("changed_fields") or [],
        "stable_value": row.get("stable_value"),
        "latest_value": row.get("latest_value"),
    }


def model_map_operational_notes(
    model: dict[str, Any],
    property_groups: dict[str, list[dict[str, Any]]],
    changes: list[dict[str, Any]],
) -> list[str]:
    notes = [
        "Use the stable track as the default public model reference.",
        "Verify a specific Rock instance schema separately before SQL or production data changes.",
    ]
    if not model.get("table_name"):
        notes.append("The Model Map did not provide an API table name for this model.")
    if property_groups.get("lava_non_database"):
        notes.append("Some Lava-supported properties are not database-backed; do not assume every Lava field is a SQL column.")
    if property_groups.get("not_mapped"):
        notes.append("NotMapped properties may be computed or framework-backed rather than persisted columns.")
    if changes:
        notes.append("Stable-to-pre-alpha differences exist; use them only as upcoming-version callouts.")
    if model.get("is_obsolete"):
        notes.append("This model is marked obsolete in the stable Model Map.")
    return notes


def build_scraped_concept_slice_pages(model_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in model_rows:
        rows_by_category[str(row.get("model_category") or "Other")].append(row)
    concept_rows = []
    for category, rows in sorted(rows_by_category.items()):
        slug = slugify(category)
        path = MODEL_MAP_CONCEPT_DIR / f"{slug}.md"
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        path.write_text(render_scraped_category_md(category, rows), encoding="utf-8")
        concept_rows.append(
            {
                "category": category,
                "path": rel_path,
                "model_count": len(rows),
                "property_count": sum(int(row.get("property_count") or 0) for row in rows),
            }
        )
    return concept_rows


def agent_scraped_entity_rows(model_rows: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for row in model_rows:
        yield {
            "schema": "rock-kb-agent-model-map-entity-v2",
            "name": row.get("model_name"),
            "category": row.get("model_category"),
            "rock_version": row.get("rock_version"),
            "model_title": row.get("model_title"),
            "model_detail_path": row.get("model_detail_path"),
            "entity_type_guid": row.get("entity_type_guid"),
            "entity_type_id": row.get("entity_type_id"),
            "property_count": row.get("property_count"),
            "database_property_count": row.get("database_property_count"),
            "lava_property_count": row.get("lava_property_count"),
            "lava_non_database_property_count": row.get("lava_non_database_property_count"),
            "not_mapped_property_count": row.get("not_mapped_property_count"),
            "required_property_count": row.get("required_property_count"),
            "obsolete_property_count": row.get("obsolete_property_count"),
            "source_url": row.get("source_url"),
            "source_urls": row.get("source_urls") or [],
            "source_keys": row.get("source_keys") or ["rock_model_map_scrape_latest"],
        }


def build_scraped_summary(
    stable: dict[str, Any],
    latest: dict[str, Any],
    stable_models: list[dict[str, Any]],
    latest_models: list[dict[str, Any]],
    stable_properties: list[dict[str, Any]],
    latest_properties: list[dict[str, Any]],
    stable_methods: list[dict[str, Any]],
    latest_methods: list[dict[str, Any]],
    concept_rows: list[dict[str, Any]],
    model_detail_count: int,
    diff_result: dict[str, Any],
    stable_scrape_path: Path,
    latest_scrape_path: Path,
) -> dict[str, Any]:
    category_counts = Counter(row["model_category"] for row in stable_models)
    return {
        "schema": "rock-kb-model-map-summary-v2",
        "generated_at": model_map_generated_at(stable, latest),
        "source": model_map_summary_source(stable, latest),
        "generation_method": [
            "Stable and pre-alpha model/property data come from authenticated Obsidian block-action calls against generic Rock demo Model Map pages.",
            "The collector uses RefreshObsidianBlockInitialization for the category/model list and GetModelDetails for each model detail payload.",
            "Stable model/property data is the preferred reference layer for concept guide landmarks, agent entity rows, and model detail pages.",
            "Stable method rows are stored separately so agents can inspect API/Lava surface hints without bloating model or property records.",
            "The public KB no longer publishes the prior read-only SQL instance schema crosswalk.",
            "The public KB no longer publishes source-parsed reflection properties as the model-map authority.",
            "Use the version diff to see changes between the stable and upcoming generic Rock versions.",
        ],
        "contains_row_data": False,
        "stable": scrape_summary(stable, stable_scrape_path),
        "pre_alpha": scrape_summary(latest, latest_scrape_path),
        "latest": scrape_summary(latest, latest_scrape_path),
        "stable_model_count": len(stable_models),
        "latest_model_count": len(latest_models),
        "stable_property_count": len(stable_properties),
        "latest_property_count": len(latest_properties),
        "stable_method_count": len(stable_methods),
        "latest_method_count": len(latest_methods),
        "stable_database_property_count": sum(1 for row in stable_properties if row.get("is_database")),
        "stable_lava_property_count": sum(1 for row in stable_properties if row.get("is_lava")),
        "stable_non_database_lava_property_count": sum(1 for row in stable_properties if row.get("is_lava_supported_non_database")),
        "stable_not_mapped_property_count": sum(1 for row in stable_properties if row.get("is_not_mapped")),
        "stable_enum_property_count": sum(1 for row in stable_properties if row.get("is_enum")),
        "stable_defined_value_property_count": sum(1 for row in stable_properties if row.get("is_defined_value")),
        "stable_table_name_model_count": sum(1 for row in stable_models if row.get("table_name")),
        "stable_missing_table_name_count": sum(1 for row in stable_models if not row.get("table_name")),
        "stable_obsolete_model_count": sum(1 for row in stable_models if row.get("is_obsolete")),
        "stable_obsolete_method_count": sum(1 for row in stable_methods if row.get("is_obsolete")),
        "pre_alpha_model_count": len(latest_models),
        "pre_alpha_property_count": len(latest_properties),
        "pre_alpha_method_count": len(latest_methods),
        "concept_slice_count": len(concept_rows),
        "model_detail_count": model_detail_count,
        "category_counts": dict(sorted(category_counts.items())),
        "version_diff": {
            "change_count": diff_result.get("change_count"),
            "model_added_count": diff_result.get("model_added_count"),
            "model_removed_count": diff_result.get("model_removed_count"),
            "property_added_count": diff_result.get("property_added_count"),
            "property_removed_count": diff_result.get("property_removed_count"),
            "property_changed_count": diff_result.get("property_changed_count"),
        },
        "paths": {
            "index": "knowledge/model-map/index.md",
            "stable_models": "knowledge/model-map/stable-models.jsonl",
            "latest_models": "knowledge/model-map/latest-models.jsonl",
            "stable_properties": "knowledge/model-map/stable-properties.jsonl",
            "latest_properties": "knowledge/model-map/latest-properties.jsonl",
            "stable_methods": "knowledge/model-map/stable-methods.jsonl",
            "latest_methods": "knowledge/model-map/latest-methods.jsonl",
            "version_diff": "knowledge/model-map/version-diff.json",
            "version_diff_rows": "knowledge/model-map/version-diff.jsonl",
            "model_details": "knowledge/model-map/models/*.md",
            "concept_slices": "knowledge/model-map/concept-slices/*.md",
            "agent_summary": "agent/model-map-summary.json",
            "agent_entities": "agent/model-map-entities.jsonl",
            "agent_properties": "agent/model-map-properties.jsonl",
            "agent_methods": "agent/model-map-methods.jsonl",
            "agent_version_diff": "agent/model-map-version-diff.jsonl",
            "agent_digests": "agent/model-map-digests.jsonl",
        },
    }


def model_map_summary_source(stable: dict[str, Any], latest: dict[str, Any]) -> str:
    methods = {stable.get("collection_method"), latest.get("collection_method")}
    if methods == {"obsidian_block_action"}:
        return "obsidian_block_action_model_maps"
    if "obsidian_block_action" in methods:
        return "mixed_model_map_collection"
    return "scraped_generic_rock_model_maps"


def render_scraped_index_md(summary: dict[str, Any], stable_models: list[dict[str, Any]]) -> str:
    top_models = sorted(stable_models, key=lambda row: int(row.get("property_count") or 0), reverse=True)[:25]
    stable = summary.get("stable") or {}
    pre_alpha = summary.get("pre_alpha") or summary.get("latest") or {}
    version_diff = summary.get("version_diff") or {}
    lines = [
        "# Rock Model Map",
        "",
        "This generated resource is built from authenticated Obsidian block-action responses from generic Rock Model Map pages, not from a local SQL schema snapshot.",
        "",
        "## How To Use This",
        "",
        "- Use `stable-models.jsonl` for the preferred stable generic Rock model landmarks.",
        "- Use `stable-properties.jsonl` for stable per-model property flags, descriptions, enum values, and related entity link text from the scraped Model Map.",
        "- Use `stable-methods.jsonl` for stable method signatures, inheritance, and obsolete-method callouts from the model detail payload.",
        "- Use `models/*.md` for direct human-readable stable model detail pages.",
        "- Use `version-diff.jsonl`, `latest-models.jsonl`, and `latest-properties.jsonl` only to call out pre-alpha/upcoming differences.",
        "- For database columns in a specific Rock instance, verify against that instance's schema separately; this public layer intentionally avoids organization-specific SQL metadata.",
        "",
        "## Tracks",
        "",
        "| Track | Rock Version | Source | Models | Properties |",
        "| --- | --- | --- | ---: | ---: |",
        "| Stable | `{stable_version}` | [Model Map]({stable_url}) | {stable_models} | {stable_properties} |".format(
            stable_version=stable.get("rock_version") or "unknown",
            stable_url=stable.get("source_url") or "",
            stable_models=summary.get("stable_model_count") or 0,
            stable_properties=summary.get("stable_property_count") or 0,
        ),
        "| Pre-alpha / upcoming | `{latest_version}` | [Model Map]({latest_url}) | {latest_models} | {latest_properties} |".format(
            latest_version=pre_alpha.get("rock_version") or "unknown",
            latest_url=pre_alpha.get("source_url") or "",
            latest_models=summary.get("pre_alpha_model_count") or summary.get("latest_model_count") or 0,
            latest_properties=summary.get("pre_alpha_property_count") or summary.get("latest_property_count") or 0,
        ),
        "",
        "## Stable Coverage",
        "",
        f"- Models: {summary.get('stable_model_count') or 0}",
        f"- Properties: {summary.get('stable_property_count') or 0}",
        f"- Database-marked properties: {summary.get('stable_database_property_count') or 0}",
        f"- Lava-marked properties: {summary.get('stable_lava_property_count') or 0}",
        f"- Lava-marked non-database properties: {summary.get('stable_non_database_lava_property_count') or 0}",
        f"- NotMapped properties: {summary.get('stable_not_mapped_property_count') or 0}",
        f"- Enum properties: {summary.get('stable_enum_property_count') or 0}",
        f"- DefinedValue properties: {summary.get('stable_defined_value_property_count') or 0}",
        f"- Method signatures: {summary.get('stable_method_count') or 0}",
        f"- Models with API table name: {summary.get('stable_table_name_model_count') or 0}",
        f"- Models missing API table name: {summary.get('stable_missing_table_name_count') or 0}",
        f"- Obsolete models: {summary.get('stable_obsolete_model_count') or 0}",
        "",
        "## Pre-Alpha Difference Callouts",
        "",
        f"- Total changes: {version_diff.get('change_count') or 0}",
        f"- Models added: {version_diff.get('model_added_count') or 0}",
        f"- Models removed: {version_diff.get('model_removed_count') or 0}",
        f"- Properties added: {version_diff.get('property_added_count') or 0}",
        f"- Properties removed: {version_diff.get('property_removed_count') or 0}",
        f"- Properties changed: {version_diff.get('property_changed_count') or 0}",
        "",
        "## Largest Stable Models",
        "",
        "| Model | Category | Properties | DB | Lava | NotMapped | Obsolete |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in top_models:
        lines.append(
            "| {model} | {category} | {properties} | {database} | {lava} | {not_mapped} | {obsolete} |".format(
                model=f"[{escape_pipe(row.get('model_name'))}](models/{row.get('model_slug')}.md)",
                category=escape_pipe(row.get("model_category")),
                properties=row.get("property_count") or 0,
                database=row.get("database_property_count") or 0,
                lava=row.get("lava_property_count") or 0,
                not_mapped=row.get("not_mapped_property_count") or 0,
                obsolete=row.get("obsolete_property_count") or 0,
            )
        )
    lines.extend(["", "## Category Slices", ""])
    for category, count in sorted((summary.get("category_counts") or {}).items()):
        lines.append(f"- [{category}](concept-slices/{slugify(category)}.md) - {count} models")
    lines.extend(
        [
            "",
            "## Regeneration",
            "",
            "```bash",
            "uv run kb modelmap build",
            "uv run kb build --stage agent-pack",
            "uv run kb publish export",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_scraped_category_md(category: str, rows: list[dict[str, Any]]) -> str:
    rows = sorted(rows, key=lambda row: row.get("model_name") or "")
    lines = [
        f"# {category} Model Map",
        "",
        f"Generated stable-track slice for Rock models in the `{category}` category.",
        "",
        "| Model | Title | Properties | DB | Lava | NotMapped | Obsolete |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {model} | {title} | {properties} | {database} | {lava} | {not_mapped} | {obsolete} |".format(
                model=f"[{escape_pipe(row.get('model_name'))}](../models/{row.get('model_slug')}.md)",
                title=escape_pipe(row.get("model_title") or ""),
                properties=row.get("property_count") or 0,
                database=row.get("database_property_count") or 0,
                lava=row.get("lava_property_count") or 0,
                not_mapped=row.get("not_mapped_property_count") or 0,
                obsolete=row.get("obsolete_property_count") or 0,
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_scraped_model_detail_md(
    model: dict[str, Any],
    properties: list[dict[str, Any]],
    changes: list[dict[str, Any]],
    models_by_key: dict[str, dict[str, Any]],
) -> str:
    database_rows = [row for row in properties if row.get("is_database")]
    lava_rows = [row for row in properties if row.get("is_lava")]
    lava_non_db_rows = [row for row in properties if row.get("is_lava_supported_non_database")]
    related_model_rows = related_model_links_for_properties(properties, models_by_key)
    lines = [
        f"# {model.get('model_name')} Model Detail",
        "",
        f"- Track: `{model.get('track')}`",
        f"- Rock version: `{model.get('rock_version') or 'unknown'}`",
        f"- Category: `{model.get('model_category') or ''}`",
        f"- Model title: `{model.get('model_title') or ''}`",
        f"- Table name: `{model.get('table_name') or 'not provided'}`",
        f"- Obsolete: `{'yes' if model.get('is_obsolete') else 'no'}`",
        f"- Method signatures: `{model.get('method_count') or 0}`",
        f"- Obsolete methods: `{model.get('obsolete_method_count') or 0}`",
        f"- EntityType GUID: `{model.get('entity_type_guid') or 'not provided'}`",
        f"- Source: [Model Map]({model.get('source_url')})",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Properties | {len(properties)} |",
        f"| Database-marked properties | {len(database_rows)} |",
        f"| Lava-marked properties | {len(lava_rows)} |",
        f"| Lava-marked non-database properties | {len(lava_non_db_rows)} |",
        f"| Related model links | {len(related_model_rows)} |",
        f"| Method signatures | {model.get('method_count') or 0} |",
        f"| Obsolete methods | {model.get('obsolete_method_count') or 0} |",
        f"| Pre-alpha changes touching this model | {len(changes)} |",
        "",
        "## Properties",
        "",
    ]
    if properties:
        lines.extend(["| Property | DB | Lava | NotMapped | Required | Obsolete | Description |", "| --- | --- | --- | --- | --- | --- | --- |"])
        for row in sorted(properties, key=lambda item: item.get("property_name") or ""):
            lines.append(
                "| {prop} | {db} | {lava} | {not_mapped} | {required} | {obsolete} | {description} |".format(
                    prop=escape_pipe(row.get("property_name")),
                    db="yes" if row.get("is_database") else "",
                    lava="yes" if row.get("is_lava") else "",
                    not_mapped="yes" if row.get("is_not_mapped") else "",
                    required="yes" if row.get("is_required") else "",
                    obsolete="yes" if row.get("is_obsolete") else "",
                    description=escape_pipe(row.get("description") or ""),
                )
            )
    else:
        lines.append("No properties were present in the scraped Model Map detail response.")
    lines.extend(["", "## Lava-Marked Non-Database Properties", ""])
    if lava_non_db_rows:
        lines.extend(["| Property | Description |", "| --- | --- |"])
        for row in sorted(lava_non_db_rows, key=lambda item: item.get("property_name") or ""):
            lines.append(f"| {escape_pipe(row.get('property_name'))} | {escape_pipe(row.get('description') or '')} |")
    else:
        lines.append("No Lava-marked non-database properties were found in the scraped Model Map for this model.")
    lines.extend(["", "## Related Model Map Links", ""])
    if related_model_rows:
        lines.extend(["| Property | Related Model | EntityType GUID |", "| --- | --- | --- |"])
        for row in related_model_rows:
            target = row.get("target_model")
            related = str(row.get("related_model") or "")
            related_cell = (
                f"[{escape_pipe(related)}]({target.get('model_slug')}.md)"
                if target and target.get("model_slug")
                else escape_pipe(related)
            )
            lines.append(
                "| {prop} | {related} | {guid} |".format(
                    prop=escape_pipe(row.get("property_name")),
                    related=related_cell,
                    guid=escape_pipe(row.get("entity_type_guid") or ""),
                )
            )
    else:
        lines.append("No related entity links were present in the scraped Model Map for this model.")
    lines.extend(["", "## Stable To Pre-Alpha Changes", ""])
    if changes:
        lines.extend(["| Change | Property | Fields |", "| --- | --- | --- |"])
        for row in changes[:50]:
            lines.append(
                "| {change} | {prop} | {fields} |".format(
                    change=escape_pipe(row.get("change_type")),
                    prop=escape_pipe(row.get("property_name") or ""),
                    fields=escape_pipe(", ".join(row.get("changed_fields") or [])),
                )
            )
        if len(changes) > 50:
            lines.append(f"\nShowing 50 of {len(changes)} changes. Use `../version-diff.jsonl` for the full set.")
    else:
        lines.append("No stable-to-pre-alpha changes were detected for this model.")
    lines.append("")
    return "\n".join(lines)


def related_model_links_for_properties(
    properties: list[dict[str, Any]],
    models_by_key: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    seen = set()
    for prop in sorted(properties, key=lambda item: item.get("property_name") or ""):
        for link in prop.get("related_entity_links") or []:
            related_model = str(link.get("text") or "").strip()
            if not related_model:
                continue
            key = (prop.get("property_name"), normalize_name(related_model), link.get("entity_type_guid"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "property_name": prop.get("property_name"),
                    "related_model": related_model,
                    "entity_type_guid": link.get("entity_type_guid"),
                    "target_model": related_model_target(related_model, models_by_key),
                }
            )
    return rows


def related_model_target(related_model: str, models_by_key: dict[str, dict[str, Any]]) -> Optional[dict[str, Any]]:
    key = normalize_name(related_model)
    if key in models_by_key:
        return models_by_key[key]
    if key.endswith("id"):
        without_id = key[:-2]
        if without_id in models_by_key:
            return models_by_key[without_id]
    return None


def probe_demo_rock_version(endpoint_url: str = DEMO_ROCK_VERSION_ENDPOINT, timeout_seconds: int = 20) -> dict[str, Any]:
    """Probe the demo Rock utility endpoint for the installed semantic version."""
    result: dict[str, Any] = {
        "schema": "rock-kb-demo-rock-version-probe-v1",
        "endpoint_url": endpoint_url,
        "probed_at": now_iso(),
        "version": None,
        "status": "not_detected",
    }
    request = urllib.request.Request(endpoint_url, headers={"User-Agent": "rock-kb-model-map-version-probe"})
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read(500).decode("utf-8", errors="replace").strip()
            result["http_status"] = getattr(response, "status", None)
            result["content_type"] = response.headers.get("content-type")
            result["raw_response_preview"] = body[:120]
    except urllib.error.HTTPError as exc:
        result.update(
            {
                "http_status": exc.code,
                "status": "http_error",
                "error": str(exc),
            }
        )
        return result
    except urllib.error.URLError as exc:
        result.update(
            {
                "status": "network_error",
                "error": str(exc.reason),
            }
        )
        return result
    except TimeoutError as exc:
        result.update({"status": "timeout", "error": str(exc)})
        return result

    version = parse_demo_rock_version_response(str(result.get("raw_response_preview") or ""))
    if version:
        result["version"] = version
        result["status"] = "detected"
    return result


def parse_demo_rock_version_response(body: str) -> Optional[str]:
    """Extract a semantic Rock version from a utility endpoint body."""
    value = body.strip()
    if not value:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value
    if isinstance(parsed, dict):
        for key in ("version", "Version", "semanticVersion", "SemanticVersion"):
            if parsed.get(key):
                parsed = parsed[key]
                break
    if not isinstance(parsed, str):
        parsed = str(parsed)
    match = re.search(r"\b\d+\.\d+\.\d+(?:\.\d+)?\b", parsed)
    return match.group(0) if match else None


def rock_version_key(version: object) -> tuple[int, ...] | None:
    """Return a comparable numeric key for a Rock semantic version."""
    value = str(version or "").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:\.\d+)?", value):
        return None
    return tuple(int(part) for part in value.split("."))


def model_map_artifact_freshness(
    summary_path: Path = AGENT_MODEL_MAP_SUMMARY_PATH,
    timeout_seconds: int = 5,
) -> dict[str, Any]:
    """Compare committed public model-map artifact versions with the live generic Rock sites."""
    if not summary_path.exists():
        return {
            "schema": "rock-kb-model-map-version-freshness-v1",
            "status": "missing",
            "summary_path": str(summary_path),
            "tracks": [],
            "stale_tracks": [],
            "message": "Model-map summary artifact is missing.",
        }
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    stable = summary.get("stable") or {}
    latest = summary.get("latest") or summary.get("pre_alpha") or {}
    return model_map_version_freshness(
        [
            {
                "track": "stable",
                "recorded_version": stable.get("rock_version"),
                "source_url": stable.get("source_url"),
                "version_source_url": stable.get("rock_version_source_url"),
                "collection_method": stable.get("collection_method"),
                "initialization_endpoint": stable.get("initialization_endpoint"),
                "detail_endpoint": stable.get("detail_endpoint"),
                "model_count": stable.get("model_count"),
                "listed_model_count": stable.get("listed_model_count"),
                "failure_count": stable.get("failure_count"),
                "path": stable.get("path"),
            },
            {
                "track": "latest",
                "recorded_version": latest.get("rock_version"),
                "source_url": latest.get("source_url"),
                "version_source_url": latest.get("rock_version_source_url"),
                "collection_method": latest.get("collection_method"),
                "initialization_endpoint": latest.get("initialization_endpoint"),
                "detail_endpoint": latest.get("detail_endpoint"),
                "model_count": latest.get("model_count"),
                "listed_model_count": latest.get("listed_model_count"),
                "failure_count": latest.get("failure_count"),
                "path": latest.get("path"),
            },
        ],
        timeout_seconds=timeout_seconds,
        source="summary",
        source_path=str(summary_path),
    )


def model_map_scrape_freshness(
    stable_scrape_path: Path = DEMO_MODEL_MAP_SCRAPE_PATH,
    latest_scrape_path: Path = LATEST_MODEL_MAP_SCRAPE_PATH,
    timeout_seconds: int = 5,
) -> dict[str, Any]:
    """Compare local raw scrape versions with the live generic Rock sites before rebuilding."""
    records = []
    for track, path in [("stable", stable_scrape_path), ("latest", latest_scrape_path)]:
        if not path.exists():
            records.append({"track": track, "path": str(path), "recorded_version": None, "missing": True})
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(
            {
                "track": track,
                "recorded_version": payload.get("rock_version"),
                "source_url": payload.get("source_url"),
                "version_source_url": payload.get("rock_version_source_url"),
                "collection_method": payload.get("collection_method"),
                "initialization_endpoint": (payload.get("obsidian_block_action") or {}).get("initialization_endpoint"),
                "detail_endpoint": (payload.get("obsidian_block_action") or {}).get("detail_endpoint"),
                "model_count": payload.get("model_count"),
                "listed_model_count": payload.get("listed_model_count"),
                "failure_count": payload.get("failure_count"),
                "path": str(path),
            }
        )
    return model_map_version_freshness(records, timeout_seconds=timeout_seconds, source="scrape")


def model_map_version_freshness(
    records: list[dict[str, Any]],
    timeout_seconds: int = 5,
    source: str = "unknown",
    source_path: str | None = None,
) -> dict[str, Any]:
    """Compare recorded model-map Rock versions with live version endpoints."""
    rows = []
    for record in records:
        track = str(record.get("track") or "")
        track_config = MODEL_MAP_VERSION_TRACKS.get(track, {})
        endpoint_url = str(record.get("version_source_url") or track_config.get("endpoint_url") or "")
        recorded_version = record.get("recorded_version")
        row = {
            "track": track,
            "label": track_config.get("label") or track,
            "path": record.get("path"),
            "source_url": record.get("source_url") or track_config.get("source_url"),
            "version_source_url": endpoint_url,
            "collection_method": record.get("collection_method"),
            "initialization_endpoint": record.get("initialization_endpoint"),
            "detail_endpoint": record.get("detail_endpoint"),
            "model_count": record.get("model_count"),
            "listed_model_count": record.get("listed_model_count"),
            "failure_count": record.get("failure_count"),
            "recorded_version": recorded_version,
            "live_version": None,
            "probe_status": "not_run",
            "status": "unknown",
        }
        if record.get("missing"):
            row["status"] = "missing"
            row["probe_status"] = "missing_local_artifact"
            rows.append(row)
            continue
        if not recorded_version:
            row["status"] = "missing-version"
            row["probe_status"] = "missing_recorded_version"
            rows.append(row)
            continue
        if not endpoint_url:
            row["status"] = "unknown"
            row["probe_status"] = "missing_version_endpoint"
            rows.append(row)
            continue
        probe = probe_demo_rock_version(endpoint_url=endpoint_url, timeout_seconds=timeout_seconds)
        row["probe_status"] = probe.get("status")
        row["http_status"] = probe.get("http_status")
        row["live_version"] = probe.get("version")
        if probe.get("status") != "detected" or not probe.get("version"):
            row["status"] = "unknown"
        elif probe.get("version") == recorded_version:
            row["status"] = "current"
        else:
            recorded_key = rock_version_key(recorded_version)
            live_key = rock_version_key(probe.get("version"))
            if recorded_key is not None and live_key is not None and live_key < recorded_key:
                row["status"] = "live-behind"
            else:
                row["status"] = "stale"
        rows.append(row)

    stale_tracks = [row for row in rows if row.get("status") == "stale"]
    ahead_tracks = [row for row in rows if row.get("status") == "live-behind"]
    blocking_tracks = [row for row in rows if row.get("status") in {"missing", "missing-version"}]
    unknown_tracks = [row for row in rows if row.get("status") == "unknown"]
    if stale_tracks:
        status = "stale"
    elif blocking_tracks:
        status = "missing"
    elif unknown_tracks:
        status = "unknown"
    else:
        status = "current"
    return {
        "schema": "rock-kb-model-map-version-freshness-v1",
        "status": status,
        "source": source,
        "source_path": source_path,
        "checked_at": now_iso(),
        "tracks": rows,
        "stale_tracks": stale_tracks,
        "ahead_tracks": ahead_tracks,
        "unknown_tracks": unknown_tracks,
        "missing_tracks": blocking_tracks,
    }


def stamp_model_map_scrape_version(
    scrape_path: Path = DEMO_MODEL_MAP_SCRAPE_PATH,
    endpoint_url: str = DEMO_ROCK_VERSION_ENDPOINT,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    """Add demo Rock version metadata to an existing full model-map scrape artifact."""
    if not scrape_path.exists():
        raise FileNotFoundError(f"Model-map scrape artifact not found: {scrape_path}")
    payload = json.loads(scrape_path.read_text(encoding="utf-8"))
    version_context = probe_demo_rock_version(endpoint_url=endpoint_url, timeout_seconds=timeout_seconds)
    payload["rock_version"] = version_context.get("version")
    payload["rock_version_source_url"] = endpoint_url
    payload["rock_version_probed_at"] = version_context.get("probed_at")
    payload["demo_rock_version_context"] = version_context
    scrape_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    models_jsonl_path = scrape_path.with_name(f"{scrape_path.stem}.models.jsonl")
    models_jsonl_updated = 0
    if models_jsonl_path.exists():
        model_rows = []
        for row in read_jsonl(models_jsonl_path):
            updated = dict(row)
            updated["rock_version"] = payload.get("rock_version")
            updated["rock_version_source_url"] = payload.get("rock_version_source_url")
            updated["rock_version_probed_at"] = payload.get("rock_version_probed_at")
            model_rows.append(updated)
        write_jsonl(models_jsonl_path, model_rows)
        models_jsonl_updated = len(model_rows)
    return {
        "scrape_path": str(scrape_path),
        "rock_version": payload.get("rock_version"),
        "rock_version_source_url": payload.get("rock_version_source_url"),
        "probe_status": version_context.get("status"),
        "http_status": version_context.get("http_status"),
        "models_jsonl_path": str(models_jsonl_path) if models_jsonl_path.exists() else None,
        "models_jsonl_updated": models_jsonl_updated,
    }


def build_model_map_version_diff(
    stable_path: Path = DEMO_MODEL_MAP_SCRAPE_PATH,
    latest_path: Path = LATEST_MODEL_MAP_SCRAPE_PATH,
    output_path: Path = MODEL_MAP_VERSION_DIFF_PATH,
    output_jsonl_path: Path = MODEL_MAP_VERSION_DIFF_JSONL_PATH,
) -> dict[str, Any]:
    """Compare stable and latest generic model-map scrapes."""
    stable = load_model_map_scrape(stable_path)
    latest = load_model_map_scrape(latest_path)
    stable_models = {model_identity(row): row for row in stable.get("models") or []}
    latest_models = {model_identity(row): row for row in latest.get("models") or []}

    stable_keys = set(stable_models)
    latest_keys = set(latest_models)
    change_rows: list[dict[str, Any]] = []

    for key in sorted(latest_keys - stable_keys):
        model = latest_models[key]
        change_rows.append(model_change_row("model_added", model, stable, latest))

    for key in sorted(stable_keys - latest_keys):
        model = stable_models[key]
        change_rows.append(model_change_row("model_removed", model, stable, latest))

    for key in sorted(stable_keys & latest_keys):
        stable_model = stable_models[key]
        latest_model = latest_models[key]
        stable_props = {
            property_identity(prop): prop
            for prop in stable_model.get("properties") or []
            if is_model_property_row(prop)
        }
        latest_props = {
            property_identity(prop): prop
            for prop in latest_model.get("properties") or []
            if is_model_property_row(prop)
        }
        for prop_key in sorted(set(latest_props) - set(stable_props)):
            change_rows.append(property_change_row("property_added", stable_model, latest_model, None, latest_props[prop_key], stable, latest))
        for prop_key in sorted(set(stable_props) - set(latest_props)):
            change_rows.append(property_change_row("property_removed", stable_model, latest_model, stable_props[prop_key], None, stable, latest))
        for prop_key in sorted(set(stable_props) & set(latest_props)):
            old = stable_props[prop_key]
            new = latest_props[prop_key]
            changed_fields = changed_property_fields(old, new)
            if changed_fields:
                change_rows.append(
                    property_change_row(
                        "property_changed",
                        stable_model,
                        latest_model,
                        old,
                        new,
                        stable,
                        latest,
                        changed_fields=changed_fields,
                    )
                )

    summary = {
        "schema": "rock-kb-model-map-version-diff-v1",
        "generated_at": model_map_generated_at(stable, latest),
        "stable": scrape_summary(stable, stable_path),
        "latest": scrape_summary(latest, latest_path),
        "change_count": len(change_rows),
        "model_added_count": sum(1 for row in change_rows if row["change_type"] == "model_added"),
        "model_removed_count": sum(1 for row in change_rows if row["change_type"] == "model_removed"),
        "property_added_count": sum(1 for row in change_rows if row["change_type"] == "property_added"),
        "property_removed_count": sum(1 for row in change_rows if row["change_type"] == "property_removed"),
        "property_changed_count": sum(1 for row in change_rows if row["change_type"] == "property_changed"),
        "changed_field_counts": dict(Counter(field for row in change_rows for field in row.get("changed_fields") or [])),
        "changes": change_rows[:500],
        "truncated_changes": len(change_rows) > 500,
        "change_jsonl_path": public_source_path(output_jsonl_path),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_jsonl(output_jsonl_path, change_rows)
    return {
        "stable_version": summary["stable"].get("rock_version"),
        "latest_version": summary["latest"].get("rock_version"),
        "change_count": summary["change_count"],
        "model_added_count": summary["model_added_count"],
        "model_removed_count": summary["model_removed_count"],
        "property_added_count": summary["property_added_count"],
        "property_removed_count": summary["property_removed_count"],
        "property_changed_count": summary["property_changed_count"],
        "output_path": public_source_path(output_path),
        "output_jsonl_path": public_source_path(output_jsonl_path),
    }


def load_model_map_scrape(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Model-map scrape artifact not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def scrape_summary(scrape: dict[str, Any], path: Path) -> dict[str, Any]:
    block_action = scrape.get("obsidian_block_action") or {}
    return {
        "path": public_source_path(path),
        "source_url": scrape.get("source_url"),
        "collection_method": scrape.get("collection_method") or "page_script_scrape",
        "block_file_url": block_action.get("block_file_url"),
        "block_guid": block_action.get("block_guid"),
        "block_type_guid": block_action.get("block_type_guid"),
        "initialization_endpoint": block_action.get("initialization_endpoint"),
        "detail_endpoint": block_action.get("detail_endpoint"),
        "rock_version": scrape.get("rock_version"),
        "rock_version_source_url": scrape.get("rock_version_source_url"),
        "listed_model_count": scrape.get("listed_model_count"),
        "category_count": scrape.get("category_count"),
        "failure_count": scrape.get("failure_count"),
        "model_count": scrape.get("model_count") or len(scrape.get("models") or []),
        "property_count": scrape.get("property_count")
        or sum(int(model.get("property_count") or len(model.get("properties") or [])) for model in scrape.get("models") or []),
        "method_count": scrape.get("method_count")
        or sum(int(model.get("method_count") or len(model.get("methods") or [])) for model in scrape.get("models") or []),
        "table_name_model_count": scrape.get("table_name_model_count")
        or scrape.get("table_backed_model_count")
        or sum(1 for model in scrape.get("models") or [] if model.get("table_name")),
        "missing_table_name_count": sum(1 for model in scrape.get("models") or [] if not model.get("table_name")),
        "obsolete_model_count": scrape.get("obsolete_model_count")
        or sum(1 for model in scrape.get("models") or [] if model.get("is_obsolete")),
    }


def model_identity(model: dict[str, Any]) -> str:
    return normalize_name(model_display_name(model))


def model_display_name(model: dict[str, Any]) -> str:
    return str(model.get("model_link_name") or model.get("model_title") or model.get("name") or "").strip()


def property_identity(prop: dict[str, Any]) -> str:
    return normalize_name(prop.get("name") or prop.get("property_name"))


def is_model_property_row(prop: dict[str, Any]) -> bool:
    name = str(prop.get("name") or prop.get("property_name") or "").strip()
    if not name:
        return False
    if re.match(r"^-?\d+$", name):
        return False
    if re.match(r"^\d+\s*=", name):
        return False
    return True


def model_change_row(change_type: str, model: dict[str, Any], stable: dict[str, Any], latest: dict[str, Any]) -> dict[str, Any]:
    version = latest.get("rock_version") if change_type == "model_added" else stable.get("rock_version")
    return {
        "schema": "rock-kb-model-map-version-change-v1",
        "change_type": change_type,
        "model_name": model_display_name(model),
        "model_title": model.get("model_title"),
        "model_category": model.get("category_name"),
        "entity_type_guid": model.get("selected_entity_type_guid") or model.get("model_guid"),
        "entity_type_id": model.get("selected_entity_type_id"),
        "property_count": model.get("property_count"),
        "rock_version": version,
        "stable_version": stable.get("rock_version"),
        "latest_version": latest.get("rock_version"),
    }


def property_change_row(
    change_type: str,
    stable_model: dict[str, Any],
    latest_model: dict[str, Any],
    stable_property: Optional[dict[str, Any]],
    latest_property: Optional[dict[str, Any]],
    stable: dict[str, Any],
    latest: dict[str, Any],
    changed_fields: Optional[list[str]] = None,
) -> dict[str, Any]:
    prop = latest_property or stable_property or {}
    latest_values = comparable_property_values(latest_property or {})
    stable_values = comparable_property_values(stable_property or {})
    return {
        "schema": "rock-kb-model-map-version-change-v1",
        "change_type": change_type,
        "model_name": model_display_name(latest_model or stable_model),
        "stable_model_title": stable_model.get("model_title"),
        "latest_model_title": latest_model.get("model_title"),
        "model_category": latest_model.get("category_name") or stable_model.get("category_name"),
        "property_name": prop.get("name") or prop.get("property_name"),
        "stable_version": stable.get("rock_version"),
        "latest_version": latest.get("rock_version"),
        "changed_fields": changed_fields or [],
        "stable": stable_values if stable_property else None,
        "latest": latest_values if latest_property else None,
    }


def changed_property_fields(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    old_values = comparable_property_values(old)
    new_values = comparable_property_values(new)
    return [field for field in old_values if old_values.get(field) != new_values.get(field)]


def comparable_property_values(prop: dict[str, Any]) -> dict[str, Any]:
    return {
        "description": normalize_description_for_compare(prop.get("description") or prop.get("comments") or ""),
        "is_database": bool(prop.get("is_database")),
        "is_lava": bool(prop.get("is_lava") if "is_lava" in prop else prop.get("is_lava_include")),
        "is_not_mapped": bool(prop.get("is_not_mapped") if "is_not_mapped" in prop else prop.get("notMapped")),
        "is_required": bool(prop.get("is_required") if "is_required" in prop else prop.get("required")),
        "is_qualifier": bool(prop.get("is_qualifier") if "is_qualifier" in prop else prop.get("isAttributeQualifier")),
        "is_obsolete": bool(prop.get("is_obsolete") if "is_obsolete" in prop else prop.get("isObsolete")),
        "is_enum": bool(prop.get("is_enum") if "is_enum" in prop else prop.get("isEnum")),
        "is_defined_value": bool(prop.get("is_defined_value") if "is_defined_value" in prop else prop.get("isDefinedValue")),
        "enum_values": normalize_enum_values(prop.get("enum_values") or prop.get("keyValues") or []),
        "related_entity_links": normalize_related_links(prop.get("related_entity_links") or []),
    }


def normalize_description(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", str(value or ""))
    return " ".join(value.split())


def normalize_description_for_compare(value: str) -> str:
    return normalize_name(normalize_description(value))


def normalize_enum_values(values: Any) -> list[dict[str, str]]:
    if isinstance(values, dict):
        items = values.items()
    else:
        items = []
        for row in values or []:
            if isinstance(row, dict):
                items.append((row.get("value"), row.get("label")))
    return sorted(
        [{"value": str(key), "label": str(value)} for key, value in items if key is not None],
        key=lambda row: (row["value"], row["label"]),
    )


def scraped_related_links(values: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = []
    for row in values or []:
        text = str(row.get("text") or "").strip()
        if not text:
            continue
        rows.append(
            {
                "text": text,
                "model_key": normalize_name(text),
                "entity_type_guid": str(row.get("entity_type_guid") or ""),
                "href": str(row.get("href") or ""),
            }
        )
    return sorted(rows, key=lambda row: (row["model_key"], row["entity_type_guid"]))


def normalize_related_links(values: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = []
    for row in values or []:
        text = str(row.get("text") or "").strip()
        if text:
            rows.append({"text": normalize_name(text)})
    return sorted(rows, key=lambda row: row["text"])


def normalize_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def slugify(value: Any) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return slug or "item"


def escape_pipe(value: Any) -> str:
    return str(value or "").replace("|", "\\|")
