from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, NORMALIZED_DIR, REPO_ROOT

LAVA_SOURCE_ID = "rock_lava_docs"
LAVA_CONCEPT_ID = "lava"
LAVA_CAPABILITY_SCHEMA = "rock-kb-lava-capability-v1"
LAVA_DETAIL_MAX_CHARS = 360
LAVA_DEPENDENT_CONCEPTS = {
    "api-integrations",
    "apple-tv",
    "cms-websites",
    "communications",
    "data-views-reports",
    "helix",
    "lava",
    "mobile",
    "roku",
    "security-permissions",
    "tv-apps",
    "workflows",
}

CAPABILITY_JSONL = KNOWLEDGE_DIR / "concepts" / "lava" / "lava-capabilities.jsonl"
CAPABILITY_INDEX = KNOWLEDGE_DIR / "concepts" / "lava" / "lava-reference-index.md"
SAFETY_MATRIX = KNOWLEDGE_DIR / "concepts" / "lava" / "lava-safety-matrix.md"
USAGE_EXAMPLES = KNOWLEDGE_DIR / "concepts" / "lava" / "lava-agent-usage-examples.md"
DEPENDENCY_JSON = KNOWLEDGE_DIR / "concepts" / "lava" / "lava-capability-dependencies.json"
AGENT_CAPABILITY_JSONL = AGENT_DIR / "lava-capabilities.jsonl"
AGENT_SUMMARY_JSON = AGENT_DIR / "lava-capability-summary.json"

HIGH_RISK_NAMES = {
    "adaptive message",
    "cache",
    "calendar events",
    "entity",
    "event scheduled instance",
    "interaction write",
    "interaction intent write",
    "interaction content channel item write",
    "javascript",
    "personalize",
    "print zpl",
    "search",
    "sql",
    "stylesheet",
    "web request",
    "workflow activate",
    "remote lava",
    "creating apis using lava",
    "lava with obsidian",
    "create entity set",
    "delete user preference",
    "page redirect",
    "person impersonation token",
    "person token create",
    "person token read",
    "postback",
    "rock instance config",
    "run lava",
    "set user preference",
    "update persisted dataset",
    "upload binary file",
    "write cookie",
}
MEDIUM_RISK_TERMS = {
    "attribute",
    "personalize",
    "search",
    "javascript",
    "stylesheet",
    "include",
    "return",
    "shortcode",
    "cache",
    "encrypt",
    "decrypt",
    "person",
    "workflow",
}
OUTPUT_TERMS = {"javascript", "stylesheet", "css", "html", "page", "return", "redirect", "culture", "shortcode"}
DATA_TERMS = {
    "adaptive message",
    "attribute",
    "calendar",
    "entity",
    "event scheduled instance",
    "person",
    "personalize",
    "search",
    "sql",
    "tag list",
    "workflow",
}
MUTATION_TERMS = {"write", "activate", "print", "workflow", "interaction", "log", "launch"}
EXTERNAL_IO_TERMS = {"web request", "remote", "print zpl", "javascript"}
SQL_ENTITY_TERMS = {"sql", "entity"}
FLAG_NAMES = (
    "reads_data",
    "mutates_data",
    "performs_external_io",
    "affects_http_response_or_page_output",
    "launches_workflows",
    "uses_sql_or_entity_access",
)

COMMAND_FLAG_OVERRIDES: dict[str, dict[str, bool]] = {
    "adaptive message": {"reads_data": True, "affects_http_response_or_page_output": True},
    "cache": {"affects_http_response_or_page_output": True},
    "calendar events": {"reads_data": True, "uses_sql_or_entity_access": True},
    "entity": {"reads_data": True, "uses_sql_or_entity_access": True},
    "event scheduled instance": {"reads_data": True, "uses_sql_or_entity_access": True},
    "interaction content channel item write": {"mutates_data": True},
    "interaction intent write": {"reads_data": True, "mutates_data": True},
    "interaction write": {"mutates_data": True},
    "javascript": {"affects_http_response_or_page_output": True},
    "personalize": {"reads_data": True, "affects_http_response_or_page_output": True},
    "print zpl": {"performs_external_io": True},
    "search": {"reads_data": True},
    "set culture": {"affects_http_response_or_page_output": True},
    "sql": {"reads_data": True, "mutates_data": True, "uses_sql_or_entity_access": True},
    "stylesheet": {"affects_http_response_or_page_output": True},
    "tag list": {"reads_data": True},
    "web request": {"performs_external_io": True},
    "workflow activate": {"mutates_data": True, "launches_workflows": True},
}

FILTER_FLAG_OVERRIDES: dict[str, dict[str, bool]] = {
    "add css link": {"affects_http_response_or_page_output": True},
    "add link tag to head": {"affects_http_response_or_page_output": True},
    "add meta tag to head": {"affects_http_response_or_page_output": True},
    "add response header": {"affects_http_response_or_page_output": True},
    "add script link": {"affects_http_response_or_page_output": True},
    "add segment": {"reads_data": True},
    "append following": {"reads_data": True},
    "append segments": {"reads_data": True},
    "append watches": {"reads_data": True},
    "attributes": {"reads_data": True},
    "campus": {"reads_data": True},
    "children": {"reads_data": True},
    "client": {"reads_data": True},
    "create entity set": {"mutates_data": True, "uses_sql_or_entity_access": True},
    "create short link": {"mutates_data": True},
    "debug": {"reads_data": True},
    "delete user preference": {"mutates_data": True},
    "entity from cached object": {"reads_data": True, "uses_sql_or_entity_access": True},
    "family salutation": {"reads_data": True},
    "filter followed": {"reads_data": True},
    "filter unfollowed": {"reads_data": True},
    "from cache": {"reads_data": True},
    "from id hash": {"reads_data": True},
    "geofencing group members": {"reads_data": True},
    "geofencing groups": {"reads_data": True},
    "get person alternate id": {"reads_data": True},
    "get user preference": {"reads_data": True},
    "group": {"reads_data": True},
    "group by guid": {"reads_data": True},
    "group by id": {"reads_data": True},
    "groups": {"reads_data": True},
    "groups attended": {"reads_data": True},
    "guid to id": {"reads_data": True},
    "has rights to": {"reads_data": True},
    "has signed document": {"reads_data": True},
    "head of household": {"reads_data": True},
    "image url": {"reads_data": True, "affects_http_response_or_page_output": True},
    "is followed": {"reads_data": True},
    "is in data view": {"reads_data": True, "uses_sql_or_entity_access": True},
    "is in security role": {"reads_data": True},
    "last attended group of type": {"reads_data": True},
    "nearest campus": {"reads_data": True},
    "nearest group": {"reads_data": True},
    "nearest groups": {"reads_data": True},
    "notes": {"reads_data": True},
    "page": {"reads_data": True},
    "page parameter": {"reads_data": True},
    "page redirect": {"affects_http_response_or_page_output": True},
    "page route": {"reads_data": True},
    "parents": {"reads_data": True},
    "persisted dataset": {"reads_data": True},
    "person action identifier": {"reads_data": True},
    "personalization items": {"reads_data": True},
    "person by alias guid": {"reads_data": True},
    "person by alias id": {"reads_data": True},
    "person by guid": {"reads_data": True},
    "person by id": {"reads_data": True},
    "person by person action identifier": {"reads_data": True},
    "person by person alternate id": {"reads_data": True},
    "person impersonation token": {"reads_data": True, "affects_http_response_or_page_output": True},
    "person token create": {"reads_data": True, "affects_http_response_or_page_output": True},
    "person token read": {"reads_data": True},
    "phone number": {"reads_data": True},
    "postback": {"affects_http_response_or_page_output": True},
    "property": {"reads_data": True},
    "property to key value": {"reads_data": True},
    "read cookie": {"reads_data": True},
    "render structured content as html": {"affects_http_response_or_page_output": True},
    "resolve rock url": {"affects_http_response_or_page_output": True},
    "rock instance config": {"reads_data": True},
    "run lava": {"affects_http_response_or_page_output": True},
    "sanitize sql": {},
    "set page title": {"affects_http_response_or_page_output": True},
    "set url parameter": {"affects_http_response_or_page_output": True},
    "set user preference": {"mutates_data": True},
    "spouse": {"reads_data": True},
    "steps": {"reads_data": True},
    "to id hash": {"reads_data": True},
    "update persisted dataset": {"mutates_data": True},
    "upload binary file": {"mutates_data": True},
    "url": {"affects_http_response_or_page_output": True},
    "write cookie": {"mutates_data": True, "affects_http_response_or_page_output": True},
    "xaml wrap": {"affects_http_response_or_page_output": True},
    "zebra photo": {"reads_data": True},
}


def build_lava_capability_reference(records: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    lava_records = [record for record in (records if records is not None else load_lava_records()) if record.get("source_id") == LAVA_SOURCE_ID]
    capabilities = lava_capability_rows(lava_records)
    source_dependencies = lava_source_dependencies(lava_records)
    write_lava_capability_artifacts(capabilities, source_dependencies)
    return {
        "lava_capabilities": len(capabilities),
        "lava_capability_source_records": len(source_dependencies),
        "lava_capability_high_risk": sum(1 for row in capabilities if row.get("risk_tier") == "high"),
    }


def load_lava_records() -> list[dict[str, Any]]:
    path = NORMALIZED_DIR / f"{LAVA_SOURCE_ID}.jsonl"
    if not path.exists():
        return []
    return [row for row in read_jsonl(path) if row.get("source_id") == LAVA_SOURCE_ID]


def lava_capability_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    seen: set[tuple[str, str, str]] = set()
    for record in records:
        elements = record.get("lava_elements") or fallback_elements_for_record(record)
        for element in elements:
            name = clean_name(element.get("name") or record.get("source_title") or "")
            category = canonical_category(str(element.get("category") or record.get("lava_doc_category") or "reference"))
            if not name:
                continue
            key = (category, normalize_key(name), str(record.get("source_url") or ""))
            if key in seen:
                continue
            seen.add(key)
            rows.append(lava_capability_row(record, element, name, category))
    return sorted(rows, key=lambda row: (category_sort_key(row["category"]), row["name"].lower(), row["official_url"]))


def fallback_elements_for_record(record: dict[str, Any]) -> list[dict[str, Any]]:
    category = str(record.get("lava_doc_category") or infer_category_from_url(str(record.get("source_url") or "")))
    if category in {"overview", "command_overview", "filter_overview"}:
        return []
    return [
        {
            "category": category,
            "name": record.get("source_title"),
            "official_url": record.get("source_url"),
            "server_versions": record.get("rock_versions") or [],
            "mobile_versions": [],
            "summary_hint": record.get("summary") or "",
            "source_fragment_hash": record.get("content_hash"),
        }
    ]


def lava_capability_row(record: dict[str, Any], element: dict[str, Any], name: str, category: str) -> dict[str, Any]:
    combined = " ".join(
        [
            name,
            category,
            str(element.get("summary_hint") or ""),
            str(record.get("summary") or ""),
            str(record.get("source_url") or ""),
        ]
    )
    flags = infer_safety_flags(name, category, combined)
    risk_tier = infer_risk_tier(name, category, flags)
    related = related_concepts_for(name, category, flags, record)
    raw_server_versions = element.get("server_versions")
    if raw_server_versions is None:
        raw_server_versions = record.get("rock_versions") or []
    server_versions = sorted(set(str(value) for value in raw_server_versions if value))
    mobile_versions = sorted(set(str(value) for value in (element.get("mobile_versions") or []) if value))
    official_url = str(element.get("official_url") or record.get("source_url") or "")
    capability_id = f"lava-capability:{category}:{normalize_key(name)}:{sha256_text(official_url)[:8]}"
    description = lava_description_for(record, element, name, category)
    return {
        "schema": LAVA_CAPABILITY_SCHEMA,
        "id": capability_id,
        "category": category,
        "name": name,
        "aliases": element.get("aliases") or [],
        "description": description,
        "usage_summary": lava_usage_summary_for(name, category, description),
        "parameter_summary": lava_parameter_summary_for(record, category, name),
        "example_summary": lava_example_summary_for(record),
        "gotchas": lava_gotchas_for(record, name, category, flags, risk_tier),
        "official_url": official_url,
        "source_id": record.get("source_id"),
        "source_record_id": record.get("id"),
        "source_content_hash": record.get("content_hash"),
        "source_fragment_hash": element.get("source_fragment_hash") or record.get("content_hash"),
        "rock_versions": server_versions,
        "rock_version_notes": version_notes(server_versions),
        "fluid_dotliquid_caveats": fluid_caveats_for(name, category, record),
        "obsidian_caveats": obsidian_caveats_for(name, category, record),
        "mobile_client_support": mobile_support_for(mobile_versions, record),
        "command_enablement_required": command_enablement_required(category, name),
        "command_enablement_scope": command_enablement_scope(category, name),
        "risk_tier": risk_tier,
        **flags,
        "requires_security_review": requires_security_review(risk_tier, flags),
        "requires_live_instance_verification": requires_live_verification(risk_tier, flags),
        "related_kb_concepts": related,
        "maintainer_summary": maintainer_summary(name, category, flags),
        "agent_use_guidance": agent_guidance(name, category, risk_tier, flags),
        "operational_example": operational_example(name, category, flags),
        "official_docs_note": "Link to the official Rock Lava page for syntax, parameters, and examples; this row is only structured metadata and KB guidance.",
        "citations": [{"source_id": record.get("source_id"), "url": official_url}],
    }


def lava_description_for(record: dict[str, Any], element: dict[str, Any], name: str, category: str) -> str:
    candidates = [
        element.get("summary_hint"),
        record.get("summary"),
        record.get("excerpt"),
    ]
    for candidate in candidates:
        cleaned = clean_lava_detail_text(name, str(candidate or ""))
        if cleaned:
            return compact_lava_detail(cleaned)
    return f"{name} is a Lava {category.replace('_', ' ')} documented by the official Rock Lava reference."


def clean_lava_detail_text(name: str, value: str) -> str:
    text = " ".join(str(value or "").split())
    if not text or "Toggle navigation" in text:
        return ""
    escaped = re.escape(name)
    text = re.sub(rf"^{escaped}\s+Show Details\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(rf"^{escaped}\s+Command Basics\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(rf"^{escaped}\s+Command\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(rf"^{escaped}\s+v[0-9.]+\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^Show Details\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^Server:\s*v[0-9.]+(?:\s+Mobile:\s*v[0-9.]+)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bServer:\s*v[0-9.]+(?:\s+Mobile:\s*v[0-9.]+)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r'^So you may be wondering,\s*"What\'s an entity\?"\s*', "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compact_lava_detail(value: str, max_chars: int = LAVA_DETAIL_MAX_CHARS) -> str:
    text = " ".join(value.split()).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    compact = " ".join(sentence for sentence in sentences[:2] if sentence).strip()
    if not compact:
        compact = text
    if len(compact) <= max_chars:
        return compact
    return compact[:max_chars].rsplit(" ", 1)[0] + "..."


def lava_usage_summary_for(name: str, category: str, description: str) -> str:
    label = category.replace("_", " ")
    if category == "filter":
        return f"Use {name} as a Lava filter in a supported rendering surface; the official page defines accepted input, arguments, and examples."
    if category == "command":
        return f"Use {name} as an enabled Lava command where the rendering surface permits it; verify command enablement and security before implementation."
    if category == "tag":
        return f"Use {name} as a Lava tag to control template behavior; verify parser support in the target rendering surface."
    if category == "shortcode":
        return f"Use {name} as a Lava shortcode only where that shortcode is installed, enabled, and permission-safe."
    if category == "lava_api":
        return f"Use {name} for Lava-backed API/webhook patterns only after reviewing route exposure, authentication, inputs, and output data."
    if category == "remote_lava":
        return f"Use {name} only after verifying remote endpoint trust, timeout behavior, and data exposure."
    if category == "obsidian":
        return f"Use {name} only after checking the Obsidian or client surface supports the relevant Lava behavior."
    if category == "workflow":
        return f"Use {name} in workflow-related Lava only after verifying workflow type, activity, requester, and permissions."
    return f"Use {name} as a Lava {label} reference; {description}"


def lava_parameter_summary_for(record: dict[str, Any], category: str, name: str) -> str:
    headings = record.get("headings") or {}
    section_names = [
        str(value)
        for group in [headings.get("h2") or [], headings.get("h3") or []]
        for value in group
        if value
    ]
    parameter_sections = [section for section in section_names if is_lava_parameter_section(section)]
    if parameter_sections:
        return "Official page sections cover: " + ", ".join(parameter_sections[:10]) + "."
    if category == "filter":
        return "No separate parameter section was extracted; use the official filter page for accepted input and optional arguments."
    if category == "command":
        return "No separate parameter section was extracted; use the official command page for required attributes, blocks, and return variables."
    return f"No separate parameter section was extracted for {name}; use the official page for exact syntax."


def is_lava_parameter_section(value: str) -> bool:
    lowered = value.lower()
    skipped = {"usage", "example", "examples", "note", "notes", "tip", "getting started", "security"}
    if lowered in skipped:
        return False
    return True


def lava_example_summary_for(record: dict[str, Any]) -> str:
    text = " ".join([str(record.get("summary") or ""), str(record.get("excerpt") or "")])
    if "{{" in text or "{%" in text:
        return "Official page includes Lava examples; use the linked page for exact syntax and complete snippets."
    headings = record.get("headings") or {}
    all_headings = " ".join(str(value) for values in headings.values() for value in (values or []))
    if "example" in all_headings.lower():
        return "Official page includes an example section; use the linked page for exact syntax."
    return "No explicit example was extracted into this generated row; use the linked official page for examples."


def lava_gotchas_for(record: dict[str, Any], name: str, category: str, flags: dict[str, bool], risk_tier: str) -> list[str]:
    text = " ".join([name, category, str(record.get("summary") or ""), str(record.get("excerpt") or "")]).lower()
    gotchas = []
    if command_enablement_required(category, name):
        gotchas.append("Lava command must be enabled in the page, block, communication, workflow, or rendering context before it will run.")
    if risk_tier == "high":
        gotchas.append("Requires live-instance review before recommending operational use.")
    if "sql injection" in text:
        gotchas.append("Do not concatenate untrusted input into SQL; verify parameterization or sanitization before use.")
    if "no security" in text or "security by default" in text:
        gotchas.append("Do not expose sensitive data without explicit authentication, authorization, and route review.")
    if flags.get("performs_external_io"):
        gotchas.append("Verify destination, credentials, timeout, retry behavior, and data exposure.")
    if flags.get("launches_workflows"):
        gotchas.append("Verify workflow type, activity, requester, permissions, and duplicate-launch behavior.")
    if flags.get("uses_sql_or_entity_access"):
        gotchas.append("Prefer a safer Data View, block setting, API endpoint, or model-map-backed service when direct data access is not required.")
    if category == "obsidian":
        gotchas.append("Client or Obsidian surfaces may not support the same Lava behavior as server-rendered pages.")
    return sorted(set(gotchas))


def infer_safety_flags(name: str, category: str, text: str) -> dict[str, bool]:
    normalized_name = normalize_phrase(name)
    flags = empty_flags()
    overrides = flag_overrides_for(normalized_name, category)
    if overrides is not None:
        flags.update(overrides)
        return flags

    lowered_name = normalized_name
    flags["reads_data"] = category in {"lava_api", "remote_lava", "workflow", "obsidian"} or any(
        term in lowered_name for term in DATA_TERMS
    )
    flags["mutates_data"] = (
        category in {"lava_api", "remote_lava", "workflow", "obsidian"}
        or any(term in lowered_name for term in MUTATION_TERMS)
    ) and not normalize_key(name).startswith("write_to_page")
    flags["performs_external_io"] = category in {"lava_api", "remote_lava"} or any(term in lowered_name for term in EXTERNAL_IO_TERMS)
    flags["affects_http_response_or_page_output"] = category in {"lava_api", "remote_lava", "obsidian"} or any(
        term in lowered_name for term in OUTPUT_TERMS
    )
    flags["launches_workflows"] = "workflow" in lowered_name and ("activate" in lowered_name or "launch" in lowered_name or category == "workflow")
    flags["uses_sql_or_entity_access"] = "sql" in lowered_name or normalized_name == "entity"
    return flags


def empty_flags() -> dict[str, bool]:
    return {name: False for name in FLAG_NAMES}


def flag_overrides_for(normalized_name: str, category: str) -> Optional[dict[str, bool]]:
    if category == "command":
        return lookup_name_rule(COMMAND_FLAG_OVERRIDES, normalized_name)
    if category == "filter":
        return lookup_name_rule(FILTER_FLAG_OVERRIDES, normalized_name)
    if category == "lava_api":
        return {
            "reads_data": True,
            "mutates_data": True,
            "performs_external_io": True,
            "affects_http_response_or_page_output": True,
            "launches_workflows": False,
            "uses_sql_or_entity_access": False,
        }
    if category == "remote_lava":
        return {
            "reads_data": True,
            "mutates_data": True,
            "performs_external_io": True,
            "affects_http_response_or_page_output": True,
            "launches_workflows": False,
            "uses_sql_or_entity_access": False,
        }
    if category == "workflow":
        return {
            "reads_data": True,
            "mutates_data": True,
            "performs_external_io": False,
            "affects_http_response_or_page_output": False,
            "launches_workflows": True,
            "uses_sql_or_entity_access": False,
        }
    if category == "obsidian":
        return {
            "reads_data": True,
            "mutates_data": False,
            "performs_external_io": False,
            "affects_http_response_or_page_output": True,
            "launches_workflows": False,
            "uses_sql_or_entity_access": False,
        }
    return None


def lookup_name_rule(rules: dict[str, dict[str, bool]], normalized_name: str) -> Optional[dict[str, bool]]:
    direct = rules.get(normalized_name)
    if direct is not None:
        return direct
    compact_name = normalized_name.replace(" ", "")
    for key, value in rules.items():
        if key.replace(" ", "") == compact_name:
            return value
    return None


def name_in_set(normalized_name: str, names: set[str]) -> bool:
    if normalized_name in names:
        return True
    compact_name = normalized_name.replace(" ", "")
    return any(name.replace(" ", "") == compact_name for name in names)


def infer_risk_tier(name: str, category: str, flags: dict[str, bool]) -> str:
    normalized_name = normalize_phrase(name)
    if name_in_set(normalized_name, HIGH_RISK_NAMES):
        return "high"
    if flags["mutates_data"] or flags["performs_external_io"] or flags["launches_workflows"] or flags["uses_sql_or_entity_access"]:
        return "high"
    if category in {"lava_api", "remote_lava", "obsidian"}:
        return "high"
    if category == "command":
        return "medium"
    lowered = normalized_name
    if any(term in lowered for term in MEDIUM_RISK_TERMS):
        return "medium"
    if flags["reads_data"] or flags["affects_http_response_or_page_output"]:
        return "medium"
    return "low"


def related_concepts_for(name: str, category: str, flags: dict[str, bool], record: dict[str, Any]) -> list[str]:
    lowered = " ".join([name, category, " ".join(record.get("topics") or [])]).lower()
    concepts = {LAVA_CONCEPT_ID}
    if "security" in lowered or flags["uses_sql_or_entity_access"] or flags["performs_external_io"] or flags["mutates_data"]:
        concepts.add("security-permissions")
    if "workflow" in lowered or flags["launches_workflows"]:
        concepts.add("workflows")
    if "api" in lowered or "web request" in lowered or category in {"lava_api", "remote_lava"}:
        concepts.add("api-integrations")
    if "obsidian" in lowered or "helix" in lowered:
        concepts.add("helix")
    if "mobile" in lowered or record.get("lava_elements"):
        if any((element.get("mobile_versions") or []) for element in record.get("lava_elements") or []):
            concepts.add("mobile")
    if "communication" in lowered or "message" in lowered:
        concepts.add("communications")
    if "report" in lowered or "sql" in lowered or "entity" in lowered:
        concepts.add("data-views-reports")
    if "roku" in lowered:
        concepts.add("roku")
    if "apple tv" in lowered or "tvml" in lowered:
        concepts.add("apple-tv")
    if "tv" in lowered:
        concepts.add("tv-apps")
    if category in {"command", "tag", "shortcode", "lava_api", "remote_lava"}:
        concepts.add("cms-websites")
    return sorted(concepts)


def version_notes(versions: list[str]) -> str:
    if not versions:
        return "No Rock version marker was extracted from the official Lava source page; verify against the linked page and the live instance version."
    return "Official Lava page includes extracted server version marker(s): " + ", ".join(f"v{version}" for version in versions) + "."


def fluid_caveats_for(name: str, category: str, record: dict[str, Any]) -> list[str]:
    text = " ".join([name, category, str(record.get("summary") or ""), str(record.get("source_url") or "")]).lower()
    caveats = []
    if "fluid" in text or "dotliquid" in text:
        caveats.append("Fluid/DotLiquid migration behavior is source-specific; consult the linked official Fluid page before changing legacy Lava.")
    if category in {"tag", "shortcode"}:
        caveats.append("Parser behavior can differ between engines; verify syntax under the instance's Lava engine when changing reusable tags or shortcodes.")
    return caveats


def obsidian_caveats_for(name: str, category: str, record: dict[str, Any]) -> list[str]:
    text = " ".join([name, category, str(record.get("summary") or ""), str(record.get("source_url") or "")]).lower()
    if "obsidian" in text:
        return ["Obsidian Lava support is constrained by the Obsidian/client surface; do not assume server-page Lava behavior without verification."]
    if category in {"command", "tag", "shortcode"}:
        return ["If this is used inside Obsidian, verify the block/client surface supports it before recommending a change."]
    return []


def mobile_support_for(mobile_versions: list[str], record: dict[str, Any]) -> dict[str, Any]:
    return {
        "supported": bool(mobile_versions),
        "versions": mobile_versions,
        "notes": "Official page includes mobile version marker(s)." if mobile_versions else "No mobile support marker was extracted; verify before recommending this for Rock Mobile.",
    }


def command_enablement_required(category: str, name: str) -> bool:
    if category != "command":
        return False
    return normalize_phrase(name) != "tag list"


def command_enablement_scope(category: str, name: str) -> str:
    if category != "command":
        return "not_a_lava_command"
    if normalize_phrase(name) == "tag list":
        return "diagnostic_command"
    return "requires the relevant Lava command to be enabled where the Lava is rendered"


def requires_security_review(risk_tier: str, flags: dict[str, bool]) -> bool:
    return risk_tier in {"high", "medium"} or any(
        flags[key]
        for key in [
            "reads_data",
            "mutates_data",
            "performs_external_io",
            "launches_workflows",
            "uses_sql_or_entity_access",
        ]
    )


def requires_live_verification(risk_tier: str, flags: dict[str, bool]) -> bool:
    return risk_tier == "high" or flags["mutates_data"] or flags["performs_external_io"] or flags["launches_workflows"] or flags["uses_sql_or_entity_access"]


def maintainer_summary(name: str, category: str, flags: dict[str, bool]) -> str:
    label = category.replace("_", " ")
    if flags["mutates_data"]:
        return f"{name} is a {label} surface that can change operational state; treat it as implementation metadata, not copied syntax."
    if flags["performs_external_io"]:
        return f"{name} is a {label} surface that can communicate outside the page/render path."
    if flags["reads_data"]:
        return f"{name} is a {label} surface that can read Rock or request-context data."
    if flags["affects_http_response_or_page_output"]:
        return f"{name} is a {label} surface that affects rendered output or response behavior."
    return f"{name} is a {label} surface documented by the official Rock Lava reference."


def agent_guidance(name: str, category: str, risk_tier: str, flags: dict[str, bool]) -> str:
    if requires_live_verification(risk_tier, flags):
        return f"Before recommending {name} operationally, verify the exact page/block/shortcode, enabled commands, security context, and Rock version in the live instance."
    if risk_tier == "medium":
        return f"Use {name} only after checking the rendering surface and linked official page; confirm no sensitive data or unsupported client surface is involved."
    return f"Use {name} as a low-risk Lava reference pointer, then link to the official page for exact syntax."


def operational_example(name: str, category: str, flags: dict[str, bool]) -> str:
    if category == "lava_api":
        return f"Example review question: What route exposure, authentication model, request inputs, output shape, page/block security, and data exposure are involved before enabling {name}?"
    if flags["uses_sql_or_entity_access"]:
        return f"Example review question: Should this page use {name}, or should the data be provided by a Data View, block setting, API endpoint, or model-map-backed service instead?"
    if flags["launches_workflows"]:
        return f"Example review question: Which workflow type, activity, requester, and duplicate-launch behavior will {name} touch?"
    if flags["performs_external_io"]:
        return f"Example review question: What destination, credentials, timeout, retry behavior, and data exposure are involved before enabling {name}?"
    if category == "shortcode":
        return f"Example review question: Is this shortcode reusable, permission-safe, and documented for every page or block that calls {name}?"
    return f"Example review question: Which rendering surface uses {name}, and does that surface support this Lava element?"


def write_lava_capability_artifacts(capabilities: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> None:
    CAPABILITY_JSONL.parent.mkdir(parents=True, exist_ok=True)
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(CAPABILITY_JSONL, capabilities)
    write_jsonl(AGENT_CAPABILITY_JSONL, capabilities)
    CAPABILITY_INDEX.write_text(render_reference_index(capabilities, source_dependencies), encoding="utf-8")
    SAFETY_MATRIX.write_text(render_safety_matrix(capabilities), encoding="utf-8")
    USAGE_EXAMPLES.write_text(render_agent_usage_examples(capabilities), encoding="utf-8")
    summary = lava_capability_summary(capabilities, source_dependencies)
    AGENT_SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DEPENDENCY_JSON.write_text(
        json.dumps(
            {
                "schema": "rock-kb-lava-capability-dependencies-v1",
                "generated_at": generated_at_iso(),
                "source_id": LAVA_SOURCE_ID,
                "source_dependencies": source_dependencies,
                "capability_count": len(capabilities),
                "dependent_concepts": sorted(LAVA_DEPENDENT_CONCEPTS),
                "resource_paths": {
                    "capabilities": relative_path(CAPABILITY_JSONL),
                    "reference_index": relative_path(CAPABILITY_INDEX),
                    "safety_matrix": relative_path(SAFETY_MATRIX),
                    "agent_usage_examples": relative_path(USAGE_EXAMPLES),
                    "agent_capabilities": relative_path(AGENT_CAPABILITY_JSONL),
                    "agent_summary": relative_path(AGENT_SUMMARY_JSON),
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def render_reference_index(capabilities: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> str:
    counts = Counter(row["category"] for row in capabilities)
    lines = [
        "# Lava Capability Reference Index",
        "",
        "Generated from the official `rock_lava_docs` source family. This file is a structured navigation layer and does not replace the official Rock Lava documentation.",
        "",
        "Use the linked official page for syntax, parameters, and examples. Use this index to decide what kind of verification or security review an agent should do first.",
        "",
        "## Coverage",
        "",
        f"- Lava capability rows: `{len(capabilities)}`",
        f"- Official Lava source records: `{len(source_dependencies)}`",
        "- Machine-readable rows: `lava-capabilities.jsonl` and `../../../agent/lava-capabilities.jsonl`",
        "- Safety matrix: `lava-safety-matrix.md`",
        "",
    ]
    for category, count in sorted(counts.items()):
        lines.append(f"- `{category}`: {count}")
    lines.extend(["", "## Capability Rows", "", "| Category | Name | Description | Risk | Version | Mobile | Security Review | Official Page |", "| --- | --- | --- | --- | --- | --- | --- | --- |"])
    for row in capabilities:
        versions = ", ".join(f"v{version}" for version in row.get("rock_versions") or []) or "verify"
        mobile = "yes" if (row.get("mobile_client_support") or {}).get("supported") else "verify"
        lines.append(
            f"| `{row['category']}` | {escape_cell(row['name'])} | {escape_cell(row.get('description'))} | `{row['risk_tier']}` | {escape_cell(versions)} | {mobile} | {yes_no(row['requires_security_review'])} | [official]({row['official_url']}) |"
        )
    lines.extend(
        [
            "",
            "## Usage Detail Rows",
            "",
            "These rows expose the structured guidance from the machine-readable Lava capability layer. They are not copied syntax docs; use the official page when exact attributes, filter arguments, or examples are needed.",
            "",
            "| Category | Name | How To Use | Parameters | Examples | Gotchas | Official Docs Boundary | Official Page |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in capabilities:
        gotchas = "; ".join(row.get("gotchas") or []) or "No generated gotchas beyond normal official-doc verification."
        lines.append(
            f"| `{row['category']}` "
            f"| {escape_cell(row['name'])} "
            f"| {escape_cell(row.get('usage_summary'))} "
            f"| {escape_cell(row.get('parameter_summary'))} "
            f"| {escape_cell(row.get('example_summary'))} "
            f"| {escape_cell(gotchas)} "
            f"| {escape_cell(row.get('official_docs_note'))} "
            f"| [official]({row['official_url']}) |"
        )
    lines.append("")
    return "\n".join(lines)


def render_safety_matrix(capabilities: list[dict[str, Any]]) -> str:
    high = [row for row in capabilities if row.get("risk_tier") == "high"]
    medium = [row for row in capabilities if row.get("risk_tier") == "medium"]
    lines = [
        "# Lava Safety Matrix",
        "",
        "Generated from structured metadata derived from official Rock Lava pages plus maintainer-authored operational guidance.",
        "",
        "## Agent Rules",
        "",
        "- Do not treat this matrix as syntax documentation; link to the official Rock page for syntax.",
        "- High-risk rows require live-instance verification before recommending operational changes.",
        "- Any row that reads data, mutates data, performs external I/O, uses SQL/entity access, launches workflows, or affects page/HTTP output should trigger security review in public or staff-facing surfaces.",
        "- Lava command rows usually require explicit command enablement in the rendering context.",
        "",
        "## High-Risk Rows",
        "",
        "| Name | Category | Why It Is Sensitive | Live Verification Prompt | Official Page |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in high:
        lines.append(
            f"| {escape_cell(row['name'])} | `{row['category']}` | {escape_cell(risk_reason(row))} | {escape_cell(row['agent_use_guidance'])} | [official]({row['official_url']}) |"
        )
    lines.extend(["", "## Medium-Risk Rows", "", "| Name | Category | Safety Notes | Official Page |", "| --- | --- | --- | --- |"])
    for row in medium:
        lines.append(f"| {escape_cell(row['name'])} | `{row['category']}` | {escape_cell(risk_reason(row))} | [official]({row['official_url']}) |")
    lines.extend(["", "## Flag Matrix", "", "| Name | Reads | Mutates | External I/O | HTTP/Page Output | Workflow | SQL/Entity | Enablement | Official Page |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for row in capabilities:
        lines.append(
            f"| {escape_cell(row['name'])} | {yes_no(row['reads_data'])} | {yes_no(row['mutates_data'])} | {yes_no(row['performs_external_io'])} | {yes_no(row['affects_http_response_or_page_output'])} | {yes_no(row['launches_workflows'])} | {yes_no(row['uses_sql_or_entity_access'])} | {yes_no(row['command_enablement_required'])} | [official]({row['official_url']}) |"
        )
    lines.append("")
    return "\n".join(lines)


def render_agent_usage_examples(capabilities: list[dict[str, Any]]) -> str:
    selected_names = {
        "Creating APIs Using Lava",
        "Entity",
        "Lava With Obsidian",
        "SQL",
        "Web Request",
        "Workflow Activate",
    }
    selected_by_name = {row["name"]: row for row in capabilities if row.get("name") in selected_names}
    lines = [
        "# Lava Agent Usage Examples",
        "",
        "Generated from structured metadata derived from official `rock_lava_docs` records. This page is a retrieval aid for agents; use the official Lava documentation for syntax, parameters, and examples.",
        "",
        "Related generated resources:",
        "",
        "- Reference index: [lava-reference-index.md](lava-reference-index.md)",
        "- Safety matrix: [lava-safety-matrix.md](lava-safety-matrix.md)",
        "- Machine-readable rows: `lava-capabilities.jsonl` and `../../../agent/lava-capabilities.jsonl`",
        "",
        "## Before Recommending Lava",
        "",
        "- Identify the rendering surface: page, block, shortcode, workflow, webhook, Obsidian/Helix surface, or mobile client.",
        "- Verify the live Rock version, enabled Lava commands, security context, current record inputs, query-string inputs, and output destination.",
        "- Treat Lava that reads data, mutates data, launches workflows, performs external I/O, uses SQL/entity access, or affects HTTP/page output as requiring security review.",
        "- Link to the official source page for syntax; do not copy snippets from this generated layer as implementation-ready Lava.",
        "",
        "## Risk Triage Examples",
        "",
        "- API or webhook answer: start from `Creating APIs Using Lava`, then verify authentication, route exposure, request inputs, output shape, and whether the endpoint exposes sensitive data.",
        "- SQL or Entity command answer: prefer a Data View, report, block setting, API endpoint, or model-map-backed service when possible; require live review before suggesting direct Lava data access.",
        "- Web Request command answer: verify destination, credentials, timeout behavior, retry behavior, and the exact data sent outside the page render path.",
        "- Workflow Activate command answer: verify WorkflowType, launch path, requester, duplicate-launch behavior, and permissions before recommending the Lava command.",
        "- Obsidian/Helix answer: check the client surface before assuming server-page Lava behavior works the same way.",
        "- Mobile answer: verify official mobile support markers, the mobile shell/client version, and the page or block that renders the Lava output.",
        "",
        "## Safe Answer Shape",
        "",
        "Use this pattern for high-risk Lava guidance:",
        "",
        "1. Name the Lava surface and link the official page.",
        "2. State the generated risk tier from the safety matrix.",
        "3. List the live checks needed before implementation.",
        "4. Recommend a safer data or integration path when SQL, Entity, Web Request, webhook, or workflow launch behavior is not required.",
        "",
        "## Selected Capability Rows",
        "",
        "| Name | Risk | Security Review | Live Verification | Operational Prompt | Official Page |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name in sorted(selected_names):
        row = selected_by_name.get(name)
        if not row:
            lines.append(f"| {escape_cell(name)} | missing | verify | verify | Rebuild the Lava capability layer and check the official Lava source. |  |")
            continue
        lines.append(
            f"| {escape_cell(row['name'])} "
            f"| `{row['risk_tier']}` "
            f"| {yes_no(row['requires_security_review'])} "
            f"| {yes_no(row['requires_live_instance_verification'])} "
            f"| {escape_cell(row['operational_example'])} "
            f"| [official]({row['official_url']}) |"
        )
    lines.append("")
    return "\n".join(lines)


def lava_capability_summary(capabilities: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "rock-kb-lava-capability-summary-v1",
        "generated_at": generated_at_iso(),
        "source_id": LAVA_SOURCE_ID,
        "source_record_count": len(source_dependencies),
        "capability_count": len(capabilities),
        "categories": dict(sorted(Counter(row["category"] for row in capabilities).items())),
        "risk_tiers": dict(sorted(Counter(row["risk_tier"] for row in capabilities).items())),
        "high_risk_count": sum(1 for row in capabilities if row.get("risk_tier") == "high"),
        "command_enablement_required_count": sum(1 for row in capabilities if row.get("command_enablement_required")),
        "live_verification_required_count": sum(1 for row in capabilities if row.get("requires_live_instance_verification")),
        "paths": {
            "capabilities": relative_path(CAPABILITY_JSONL),
            "reference_index": relative_path(CAPABILITY_INDEX),
            "safety_matrix": relative_path(SAFETY_MATRIX),
            "agent_usage_examples": relative_path(USAGE_EXAMPLES),
            "dependencies": relative_path(DEPENDENCY_JSON),
        },
    }


def lava_source_dependencies(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    seen = set()
    for record in sorted(records, key=lambda row: (str(row.get("source_url") or ""), str(row.get("id") or ""))):
        record_id = str(record.get("id") or "")
        if not record_id or record_id in seen:
            continue
        seen.add(record_id)
        rows.append(
            {
                "source_record_id": record_id,
                "source_id": record.get("source_id"),
                "source_title": record.get("source_title"),
                "source_url": record.get("source_url"),
                "content_hash": record.get("content_hash"),
                "lava_doc_category": record.get("lava_doc_category") or infer_category_from_url(str(record.get("source_url") or "")),
                "lava_element_count": int(record.get("lava_element_count") or len(record.get("lava_elements") or [])),
            }
        )
    return rows


def lava_source_dependency_hashes(records: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    lava_records = records if records is not None else load_lava_records()
    return {row["source_record_id"]: row.get("content_hash") for row in lava_source_dependencies(lava_records)}


def should_attach_lava_dependency(concept_id: str) -> bool:
    return concept_id in LAVA_DEPENDENT_CONCEPTS


def infer_category_from_url(url: str) -> str:
    path = re.sub(r"^/+", "", re.sub(r"https?://[^/]+/?", "", url)).lower()
    if path.startswith("lava/commands/"):
        return "command"
    if path.startswith("lava/filters/"):
        return "filter"
    if path.startswith("lava/tags/"):
        return "tag"
    if path.startswith("lava/shortcodes/"):
        return "shortcode"
    if path.startswith("lava/fluid"):
        return "fluid_migration"
    if path == "lava/lava-api":
        return "lava_api"
    if path == "lava/obsidian":
        return "obsidian"
    if path == "lava/remote-lava":
        return "remote_lava"
    if path == "lava/workflows":
        return "workflow"
    return "reference"


def canonical_category(category: str) -> str:
    if category == "command_overview":
        return "command"
    if category == "filter_overview":
        return "filter"
    return category


def category_sort_key(category: str) -> int:
    order = {
        "command": 0,
        "filter": 1,
        "tag": 2,
        "shortcode": 3,
        "lava_api": 4,
        "remote_lava": 5,
        "obsidian": 6,
        "fluid_migration": 7,
        "workflow": 8,
        "reference": 9,
    }
    return order.get(category, 99)


def clean_name(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def has_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def risk_reason(row: dict[str, Any]) -> str:
    reasons = []
    if row.get("reads_data"):
        reasons.append("reads data")
    if row.get("mutates_data"):
        reasons.append("mutates data")
    if row.get("performs_external_io"):
        reasons.append("external I/O")
    if row.get("affects_http_response_or_page_output"):
        reasons.append("page/HTTP output")
    if row.get("launches_workflows"):
        reasons.append("workflow launch")
    if row.get("uses_sql_or_entity_access"):
        reasons.append("SQL/entity access")
    if row.get("command_enablement_required"):
        reasons.append("requires command enablement")
    return ", ".join(reasons) or "rendering/context dependent"


def escape_cell(value: Any) -> str:
    return " ".join(str(value or "").split()).replace("|", "\\|")


def yes_no(value: Any) -> str:
    return "yes" if bool(value) else "no"


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)
