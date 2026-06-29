from __future__ import annotations

import json
import re
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .extract import generated_at_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, REPO_ROOT, REVIEW_DIR

LAVA_CONTEXT_SCHEMA = "rock-kb-lava-context-v1"
LAVA_CONTEXT_SUMMARY_SCHEMA = "rock-kb-lava-context-summary-v1"
LAVA_CONTEXT_DEPENDENCIES_SCHEMA = "rock-kb-lava-context-dependencies-v1"
SOURCE_REF = "develop"
SOURCE_ID = "sparkdevnetwork_rock"

LAVA_CONCEPT_DIR = KNOWLEDGE_DIR / "concepts" / "lava"
CONTEXT_JSONL = LAVA_CONCEPT_DIR / "lava-contexts.jsonl"
CONTEXT_INDEX = LAVA_CONCEPT_DIR / "lava-context-directory.md"
CONTEXT_DEPENDENCY_JSON = LAVA_CONCEPT_DIR / "lava-context-dependencies.json"
AGENT_CONTEXT_JSONL = AGENT_DIR / "lava-contexts.jsonl"
AGENT_CONTEXT_SUMMARY_JSON = AGENT_DIR / "lava-context-summary.json"
SOURCE_CACHE_DIR = REVIEW_DIR / "lava-context-source" / SOURCE_REF

DEFAULT_CONCEPT_IDS = ["lava"]
CHECK_IN_CONCEPT_IDS = ["lava", "check-in", "groups"]
COMMUNICATION_CONCEPT_IDS = ["lava", "communications", "people-families"]
WORKFLOW_CONCEPT_IDS = ["lava", "workflows"]
CMS_CONCEPT_IDS = ["lava", "cms-websites"]
MOBILE_CONCEPT_IDS = ["lava", "mobile"]


@dataclass(frozen=True)
class SourceFile:
    key: str
    source_file: str
    source_symbol: str

    @property
    def cache_path(self) -> Path:
        return SOURCE_CACHE_DIR / self.source_file.replace("/", "__")

    @property
    def raw_url(self) -> str:
        return f"https://raw.githubusercontent.com/SparkDevNetwork/Rock/{SOURCE_REF}/{self.source_file}"

    @property
    def blob_url(self) -> str:
        return f"https://github.com/SparkDevNetwork/Rock/blob/{SOURCE_REF}/{self.source_file}"


SOURCE_FILES: dict[str, SourceFile] = {
    "lava_helper": SourceFile("lava_helper", "Rock/Lava/LavaHelper.cs", "LavaHelper.GetCommonMergeFields"),
    "request_context": SourceFile("request_context", "Rock/Net/RockRequestContext.cs", "RockRequestContext.GetCommonMergeFields"),
    "person_label_data": SourceFile("person_label_data", "Rock/CheckIn/v2/Labels/PersonLabelData.cs", "PersonLabelData"),
    "field_source_helper": SourceFile("field_source_helper", "Rock/CheckIn/v2/Labels/FieldSourceHelper.cs", "FieldSourceHelper"),
    "label_field": SourceFile("label_field", "Rock/CheckIn/v2/Labels/LabelField.cs", "LabelField"),
    "communication_recipient": SourceFile(
        "communication_recipient",
        "Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs",
        "CommunicationRecipient.CommunicationMergeValues",
    ),
    "workflow_action": SourceFile("workflow_action", "Rock/Workflow/ActionComponent.cs", "ActionComponent.GetMergeFields"),
}

TYPE_MODEL_MAP = {
    "Person": ("Rock.Model.Person", "person", "object"),
    "PersonAlias": ("Rock.Model.PersonAlias", "person-alias", "object"),
    "Group": ("Rock.Model.Group", "group", "object"),
    "Location": ("Rock.Model.Location", "location", "object"),
    "Schedule": ("Rock.Model.Schedule", "schedule", "object"),
    "Communication": ("Rock.Model.Communication", "communication", "object"),
    "WorkflowAction": ("Rock.Model.WorkflowAction", "workflow-action", "object"),
    "WorkflowActivity": ("Rock.Model.WorkflowActivity", "workflow-activity", "object"),
    "Workflow": ("Rock.Model.Workflow", "workflow", "object"),
    "Campus": ("Rock.Model.Campus", "campus", "object"),
    "Device": ("Rock.Common.Mobile.DeviceData", None, "object"),
}

COMMON_KEY_TYPE_MAP = {
    "Context": ("Dictionary<string, object>", None, "dictionary"),
    "PageParameter": ("IDictionary<string, string>", None, "dictionary"),
    "OSFamily": ("string", None, "scalar"),
    "DeviceFamily": ("string", None, "scalar"),
    "CurrentPerson": TYPE_MODEL_MAP["Person"],
    "CurrentVisitor": TYPE_MODEL_MAP["PersonAlias"],
    "Campuses": ("IEnumerable<CampusCache>", "campus", "collection"),
    "Geolocation": ("Rock.Net.Geolocation", None, "object"),
    "ExperienceMode": ("string", None, "scalar"),
    "Device": TYPE_MODEL_MAP["Device"],
}

LABEL_NESTED_MODEL_MAP = {
    "Area": ("Rock.Model.GroupType", None, "object"),
    "Campus": TYPE_MODEL_MAP["Campus"],
    "CheckedInByPerson": TYPE_MODEL_MAP["Person"],
    "Device": TYPE_MODEL_MAP["Device"],
    "Group": TYPE_MODEL_MAP["Group"],
    "Location": TYPE_MODEL_MAP["Location"],
    "Schedule": TYPE_MODEL_MAP["Schedule"],
}


def build_lava_context_reference(fetch_missing: bool = True, source_dir: Path | None = None) -> dict[str, Any]:
    """Build generated Lava data-context artifacts from public Rock source files."""
    source_texts = load_source_texts(fetch_missing=fetch_missing, source_dir=source_dir)
    rows = lava_context_rows(source_texts)
    source_dependencies = lava_context_source_dependencies(source_texts)
    write_lava_context_artifacts(rows, source_dependencies)
    return {
        "lava_contexts": len(rows),
        "lava_context_source_files": len(source_dependencies),
        "lava_context_families": len({row.get("context_family") for row in rows}),
    }


def refresh_lava_context_source_cache(source_dir: Path | None = None) -> dict[str, Any]:
    destination = source_dir or SOURCE_CACHE_DIR
    destination.mkdir(parents=True, exist_ok=True)
    fetched = []
    for source in SOURCE_FILES.values():
        target = destination / source.source_file.replace("/", "__")
        text = fetch_public_source(source.raw_url)
        target.write_text(text, encoding="utf-8")
        fetched.append({"source_file": source.source_file, "path": str(target), "bytes": len(text.encode("utf-8"))})
    return {"schema": "rock-kb-lava-context-source-refresh-v1", "source_ref": SOURCE_REF, "source_files": fetched}


def load_source_texts(fetch_missing: bool = True, source_dir: Path | None = None) -> dict[str, str]:
    base = source_dir or SOURCE_CACHE_DIR
    texts: dict[str, str] = {}
    for key, source in SOURCE_FILES.items():
        path = base / source.source_file.replace("/", "__")
        if path.exists():
            texts[key] = path.read_text(encoding="utf-8", errors="ignore")
            continue
        if not fetch_missing:
            continue
        text = fetch_public_source(source.raw_url)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        texts[key] = text
    return texts


def fetch_public_source(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "rock-kb-lava-context-builder"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def lava_context_rows(source_texts: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    model_links = model_map_links_by_slug()
    rows.extend(parse_common_merge_fields("lava_helper", source_texts.get("lava_helper", ""), "global-lava-helper-common"))
    rows.extend(parse_common_merge_fields("request_context", source_texts.get("request_context", ""), "global-request-context-common"))
    rows.extend(parse_person_label_data(source_texts.get("person_label_data", "")))
    rows.extend(parse_field_source_helper_person_label_paths(source_texts.get("field_source_helper", "")))
    rows.extend(parse_communication_merge_values(source_texts.get("communication_recipient", "")))
    rows.extend(parse_workflow_merge_fields(source_texts.get("workflow_action", "")))
    rows.extend(static_surface_boundary_rows(source_texts))

    normalized = []
    seen: set[tuple[str, str, str, str]] = set()
    for row in rows:
        key = (
            str(row.get("context_id") or ""),
            str(row.get("root_key") or ""),
            str(row.get("nested_path") or ""),
            str(row.get("source_symbol") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        model_slug = row.get("model_slug")
        row["model_map_links"] = model_links.get(str(model_slug), []) if model_slug else []
        row["id"] = lava_context_id(row)
        normalized.append(row)
    return sorted(
        normalized,
        key=lambda row: (
            str(row.get("context_family") or ""),
            str(row.get("context_id") or ""),
            str(row.get("root_key") or ""),
            str(row.get("nested_path") or ""),
            str(row.get("source_symbol") or ""),
        ),
    )


def parse_common_merge_fields(source_key: str, text: str, context_id: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES[source_key]
    if source_key == "lava_helper":
        surface_name = "Global common Lava merge fields"
        notes = "Common fields returned by LavaHelper.GetCommonMergeFields for Web Forms/page Lava surfaces."
    else:
        surface_name = "Rock request-context common Lava merge fields"
        notes = "Common fields returned by RockRequestContext.GetCommonMergeFields for request-context and Obsidian/block-action surfaces."
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.search(r'mergeFields\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if not match:
            continue
        root_key = match.group(1)
        root_type, model_slug, value_kind = COMMON_KEY_TYPE_MAP.get(root_key, ("object", None, "unknown"))
        rows.append(
            context_row(
                context_id=context_id,
                context_family="global",
                surface_name=surface_name,
                surface_type="common_merge_fields",
                concept_ids=DEFAULT_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes=notes,
                needs_live_verification=root_key in {"Context", "PageParameter", "CurrentPerson", "CurrentVisitor", "Device", "Geolocation"},
            )
        )
    return rows


def parse_person_label_data(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["person_label_data"]
    rows = []
    property_pattern = re.compile(r"public\s+([^;{}=]+?)\s+([A-Za-z][A-Za-z0-9_]*)\s*\{\s*get;\s*\}")
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = property_pattern.search(line)
        if not match:
            continue
        raw_type = normalize_cs_type(match.group(1))
        root_key = match.group(2)
        root_type, model_slug, value_kind = classify_cs_type(raw_type)
        rows.append(
            context_row(
                context_id="check-in-label-person-dynamic-text",
                context_family="check-in-label",
                surface_name="Check-In Label Designer Person Dynamic Text",
                surface_type="label_dynamic_text",
                concept_ids=CHECK_IN_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes="Person label data property exposed to Check-In label Dynamic Text Lava through the selected label data object.",
                needs_live_verification=False,
            )
        )
    rows.extend(parse_person_attendance_assignment_paths(text, source))
    return rows


def parse_person_attendance_assignment_paths(text: str, source: SourceFile) -> list[dict[str, Any]]:
    rows = []
    patterns = [
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Select\( a => a\.(?P<nested>\w+)\.Name \)"),
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Select\( a => a\.(?P<nested>SecurityCode) \)"),
        re.compile(r"(?P<label>\w+)\s*=\s*PersonAttendance\.Any\( a => a\.(?P<nested>IsFirstTime) \)"),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            nested = match.group("nested")
            root_type, model_slug, value_kind = LABEL_NESTED_MODEL_MAP.get(nested, ("LabelAttendanceDetail", None, "scalar"))
            rows.append(
                context_row(
                    context_id="check-in-label-person-dynamic-text",
                    context_family="check-in-label",
                    surface_name="Check-In Label Designer Person Dynamic Text",
                    surface_type="label_dynamic_text_nested_path",
                    concept_ids=CHECK_IN_CONCEPT_IDS,
                    root_key="PersonAttendance",
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    nested_path=f"PersonAttendance.{nested}",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes=f"Nested path used while deriving the `{match.group('label')}` label data property.",
                    needs_live_verification=False,
                )
            )
    return rows


def parse_field_source_helper_person_label_paths(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["field_source_helper"]
    rows = []
    patterns = [
        re.compile(r"source\.PersonAttendance\.FirstOrDefault\(\)\?\.(?P<nested>\w+)"),
        re.compile(r"source\.PersonAttendance\.Select\( a => a\.(?P<nested>\w+)"),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            match = pattern.search(line)
            if not match:
                continue
            nested = match.group("nested")
            if nested not in LABEL_NESTED_MODEL_MAP:
                continue
            root_type, model_slug, value_kind = LABEL_NESTED_MODEL_MAP[nested]
            rows.append(
                context_row(
                    context_id="check-in-label-person-field-sources",
                    context_family="check-in-label",
                    surface_name="Check-In Label Designer Person field sources",
                    surface_type="label_field_source",
                    concept_ids=CHECK_IN_CONCEPT_IDS,
                    root_key="PersonAttendance",
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    nested_path=f"PersonAttendance.{nested}",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="FieldSourceHelper references this nested person-attendance path while building Check-In label data sources.",
                    needs_live_verification=False,
                )
            )
    return rows


def parse_communication_merge_values(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["communication_recipient"]
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.search(r'mergeValues\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if match:
            root_key = match.group(1)
            root_type, model_slug, value_kind = {
                "Communication": TYPE_MODEL_MAP["Communication"],
                "Person": TYPE_MODEL_MAP["Person"],
            }.get(root_key, ("object", None, "unknown"))
            rows.append(
                context_row(
                    context_id="communication-recipient-merge-values",
                    context_family="communication",
                    surface_name="Communication recipient merge values",
                    surface_type="communication_template_merge_values",
                    concept_ids=COMMUNICATION_CONCEPT_IDS,
                    root_key=root_key,
                    root_type=root_type,
                    model_slug=model_slug,
                    value_kind=value_kind,
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="CommunicationRecipient.CommunicationMergeValues adds this root when preparing recipient Lava merge values.",
                    needs_live_verification=False,
                )
            )
        if "mergeValues.Add( entityTypeType.Name, mergeEntity )" in line:
            rows.append(
                context_row(
                    context_id="communication-recipient-merge-values",
                    context_family="communication",
                    surface_name="Communication recipient additional merge values",
                    surface_type="communication_template_dynamic_merge_values",
                    concept_ids=COMMUNICATION_CONCEPT_IDS,
                    root_key="AdditionalMergeValues",
                    root_type="dynamic entity or scalar",
                    model_slug=None,
                    value_kind="dynamic",
                    source=source,
                    source_line_start=line_number,
                    source_line_end=line_number,
                    availability="source-code-confirmed",
                    notes="Additional merge values may add an entity by entity type name or a scalar by merge field key; inspect the communication/report setup before relying on a specific root.",
                    needs_live_verification=True,
                )
            )
    return rows


def parse_workflow_merge_fields(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    source = SOURCE_FILES["workflow_action"]
    rows = []
    current_symbol = ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "protected Dictionary<string, object> GetMergeFields( WorkflowAction action )" in line:
            current_symbol = "ActionComponent.GetMergeFields(WorkflowAction)"
        elif "protected Dictionary<string, object> GetMergeFields( WorkflowAction action, RockRequestContext requestContext )" in line:
            current_symbol = "ActionComponent.GetMergeFields(WorkflowAction,RockRequestContext)"
        match = re.search(r'mergeFields\.Add\(\s*"([^"]+)"\s*,\s*(.*?)\s*\);', line)
        if not match or not current_symbol:
            continue
        root_key = match.group(1)
        root_type, model_slug, value_kind = {
            "Action": TYPE_MODEL_MAP["WorkflowAction"],
            "Activity": TYPE_MODEL_MAP["WorkflowActivity"],
            "Workflow": TYPE_MODEL_MAP["Workflow"],
        }.get(root_key, ("object", None, "unknown"))
        rows.append(
            context_row(
                context_id="workflow-action-component-merge-fields",
                context_family="workflow",
                surface_name="Workflow action component Lava merge fields",
                surface_type="workflow_action_merge_fields",
                concept_ids=WORKFLOW_CONCEPT_IDS,
                root_key=root_key,
                root_type=root_type,
                model_slug=model_slug,
                value_kind=value_kind,
                source=source,
                source_symbol=current_symbol,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes="Workflow ActionComponent.GetMergeFields adds this root when resolving Lava in workflow action components.",
                needs_live_verification=False,
            )
        )
    return rows


def static_surface_boundary_rows(source_texts: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for source_key, context_id, family, surface_name, concept_ids, notes in [
        (
            "label_field",
            "check-in-label-field-definition",
            "check-in-label",
            "Check-In Label Designer field definition",
            CHECK_IN_CONCEPT_IDS,
            "LabelField exposes field configuration, but not arbitrary Lava roots; use label data rows for Dynamic Text context roots.",
        ),
        (
            "field_source_helper",
            "check-in-label-field-source-directory",
            "check-in-label",
            "Check-In Label Designer field-source directory",
            CHECK_IN_CONCEPT_IDS,
            "FieldSourceHelper defines available formatted label fields and filters; do not treat every field source as a raw Lava root.",
        ),
    ]:
        text = source_texts.get(source_key, "")
        if not text:
            continue
        source = SOURCE_FILES[source_key]
        line_number = first_interesting_line(text, source.source_symbol)
        rows.append(
            context_row(
                context_id=context_id,
                context_family=family,
                surface_name=surface_name,
                surface_type="surface_boundary",
                concept_ids=concept_ids,
                root_key="source-boundary",
                root_type="source-code boundary",
                model_slug=None,
                value_kind="boundary",
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="source-code-confirmed",
                notes=notes,
                needs_live_verification=True,
            )
        )
    for context_id, family, surface_name, concept_ids, notes, source_key in [
        (
            "cms-block-template-context",
            "cms-block",
            "CMS/web block Lava template context",
            CMS_CONCEPT_IDS,
            "V1 only records this as a source-code boundary. Add explicit block roots when public source declares them.",
            "lava_helper",
        ),
        (
            "mobile-block-template-context",
            "mobile-block",
            "Mobile block Lava template context",
            MOBILE_CONCEPT_IDS,
            "V1 only records this as a source-code boundary. Add explicit mobile roots when public source declares them.",
            "lava_helper",
        ),
    ]:
        source = SOURCE_FILES[source_key]
        text = source_texts.get(source_key, "")
        line_number = first_interesting_line(text, "GetCommonMergeFields") if text else 1
        rows.append(
            context_row(
                context_id=context_id,
                context_family=family,
                surface_name=surface_name,
                surface_type="surface_boundary",
                concept_ids=concept_ids,
                root_key="source-boundary",
                root_type="source-code boundary",
                model_slug=None,
                value_kind="boundary",
                source=source,
                source_line_start=line_number,
                source_line_end=line_number,
                availability="documented-boundary",
                notes=notes,
                needs_live_verification=True,
            )
        )
    return rows


def context_row(
    *,
    context_id: str,
    context_family: str,
    surface_name: str,
    surface_type: str,
    concept_ids: list[str],
    root_key: str,
    root_type: str,
    model_slug: str | None,
    value_kind: str,
    source: SourceFile,
    source_line_start: int,
    source_line_end: int,
    availability: str,
    notes: str,
    needs_live_verification: bool,
    nested_path: str = "",
    source_symbol: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": LAVA_CONTEXT_SCHEMA,
        "context_id": context_id,
        "context_family": context_family,
        "surface_name": surface_name,
        "surface_type": surface_type,
        "concept_ids": concept_ids,
        "root_key": root_key,
        "root_type": root_type,
        "model_slug": model_slug,
        "value_kind": value_kind,
        "nested_path": nested_path,
        "availability": availability,
        "source_id": SOURCE_ID,
        "source_url": source_url(source, source_line_start, source_line_end),
        "source_file": source.source_file,
        "source_symbol": source_symbol or source.source_symbol,
        "source_line_start": source_line_start,
        "source_line_end": source_line_end,
        "source_ref": SOURCE_REF,
        "model_map_links": [],
        "notes": notes,
        "needs_live_verification": needs_live_verification,
    }


def source_url(source: SourceFile, start: int, end: int) -> str:
    if start == end:
        return f"{source.blob_url}#L{start}"
    return f"{source.blob_url}#L{start}-L{end}"


def lava_context_id(row: dict[str, Any]) -> str:
    stable = "|".join(
        str(row.get(key) or "")
        for key in ["context_id", "root_key", "nested_path", "source_symbol", "source_file", "source_line_start"]
    )
    return f"lava_context:{row.get('context_id')}:{normalize_key(str(row.get('root_key') or 'root'))}:{sha256_text(stable)[:8]}"


def normalize_cs_type(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("?", "")).strip()


def classify_cs_type(raw_type: str) -> tuple[str, str | None, str]:
    type_name = raw_type
    list_match = re.match(r"(?:List|IEnumerable|ICollection)<(.+)>", raw_type)
    if list_match:
        inner = normalize_cs_type(list_match.group(1))
        root_type, model_slug, _ = TYPE_MODEL_MAP.get(inner, (inner, None, "object"))
        if inner in {"string", "int", "bool", "DateTime", "Guid", "decimal"}:
            return raw_type, None, "scalar_collection"
        return f"List<{root_type}>", model_slug, "collection"
    if type_name in TYPE_MODEL_MAP:
        return TYPE_MODEL_MAP[type_name]
    if type_name in {"string", "int", "bool", "DateTime", "Guid", "decimal"}:
        return type_name, None, "scalar"
    return type_name, None, "object"


def first_interesting_line(text: str, needle: str) -> int:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return line_number
    return 1


def model_map_links_by_slug() -> dict[str, list[dict[str, Any]]]:
    links: dict[str, list[dict[str, Any]]] = {}
    for digest in read_jsonl(AGENT_DIR / "model-map-digests.jsonl"):
        identity = digest.get("identity") or {}
        slug = str(identity.get("model_slug") or "")
        if not slug:
            continue
        links[slug] = [
            {
                "model_slug": slug,
                "model_name": identity.get("model_name"),
                "model_title": identity.get("model_title"),
                "model_detail_path": identity.get("model_detail_path"),
                "rock_version": identity.get("rock_version"),
            }
        ]
    return links


def lava_context_source_dependencies(source_texts: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for key, text in sorted(source_texts.items()):
        source = SOURCE_FILES.get(key)
        if not source:
            continue
        rows.append(
            {
                "source_id": SOURCE_ID,
                "source_ref": SOURCE_REF,
                "source_file": source.source_file,
                "source_url": source.blob_url,
                "content_hash": sha256_text(text),
            }
        )
    return rows


def write_lava_context_artifacts(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> None:
    LAVA_CONCEPT_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(CONTEXT_JSONL, rows)
    write_jsonl(AGENT_CONTEXT_JSONL, rows)
    CONTEXT_INDEX.write_text(render_lava_context_directory(rows, source_dependencies), encoding="utf-8")
    summary = lava_context_summary(rows, source_dependencies)
    AGENT_CONTEXT_SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CONTEXT_DEPENDENCY_JSON.write_text(
        json.dumps(
            {
                "schema": LAVA_CONTEXT_DEPENDENCIES_SCHEMA,
                "generated_at": generated_at_iso(),
                "source_id": SOURCE_ID,
                "source_ref": SOURCE_REF,
                "source_dependencies": source_dependencies,
                "context_count": len(rows),
                "context_families": dict(sorted(Counter(row["context_family"] for row in rows).items())),
                "resource_paths": {
                    "contexts": relative_path(CONTEXT_JSONL),
                    "directory": relative_path(CONTEXT_INDEX),
                    "agent_contexts": relative_path(AGENT_CONTEXT_JSONL),
                    "agent_summary": relative_path(AGENT_CONTEXT_SUMMARY_JSON),
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def lava_context_summary(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": LAVA_CONTEXT_SUMMARY_SCHEMA,
        "generated_at": generated_at_iso(),
        "source_id": SOURCE_ID,
        "source_ref": SOURCE_REF,
        "source_file_count": len(source_dependencies),
        "context_count": len(rows),
        "context_families": dict(sorted(Counter(row["context_family"] for row in rows).items())),
        "surface_types": dict(sorted(Counter(row["surface_type"] for row in rows).items())),
        "availability": dict(sorted(Counter(row["availability"] for row in rows).items())),
        "needs_live_verification_count": sum(1 for row in rows if row.get("needs_live_verification")),
        "model_link_count": sum(1 for row in rows if row.get("model_map_links")),
        "paths": {
            "contexts": relative_path(CONTEXT_JSONL),
            "directory": relative_path(CONTEXT_INDEX),
            "dependencies": relative_path(CONTEXT_DEPENDENCY_JSON),
            "agent_contexts": relative_path(AGENT_CONTEXT_JSONL),
        },
    }


def render_lava_context_directory(rows: list[dict[str, Any]], source_dependencies: list[dict[str, Any]]) -> str:
    family_counts = Counter(row["context_family"] for row in rows)
    lines = [
        "# Lava Data Context Directory",
        "",
        "Generated from public SparkDevNetwork/Rock source files. This directory answers which root objects are available in selected Lava rendering surfaces; use the Model Map after identifying a root object.",
        "",
        "## Agent Use",
        "",
        "1. Identify the rendering surface and context family.",
        "2. Use this directory to find available root keys and nested paths.",
        "3. Use `agent/model-map-digests.jsonl`, `uvx rock-kb model <slug>`, or `uvx rock-kb model-map get <slug>` to inspect properties for linked model roots.",
        "4. Use `agent/lava-capabilities.jsonl` for filters, commands, and Lava behavior.",
        "5. Treat rows marked for live verification as source-code leads that still depend on the page, block, communication, workflow, or label configuration.",
        "",
        "## Coverage",
        "",
        f"- Lava context rows: `{len(rows)}`",
        f"- Public source files: `{len(source_dependencies)}`",
        "- Machine-readable rows: `lava-contexts.jsonl` and `../../../agent/lava-contexts.jsonl`",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"- `{family}`: {count}")
    lines.extend(["", "## Context Rows", "", "| Family | Surface | Root Key | Nested Path | Type | Model Map | Verification | Source |", "| --- | --- | --- | --- | --- | --- | --- | --- |"])
    for row in rows:
        model_links = row.get("model_map_links") or []
        if model_links:
            first = model_links[0]
            model_text = f"`{first.get('model_slug')}`"
        else:
            model_text = ""
        verification = "live check" if row.get("needs_live_verification") else "source code"
        lines.append(
            f"| `{row['context_family']}` "
            f"| {escape_cell(row.get('surface_name'))} "
            f"| `{escape_cell(row.get('root_key'))}` "
            f"| {escape_cell(row.get('nested_path') or '')} "
            f"| {escape_cell(row.get('root_type'))} "
            f"| {model_text} "
            f"| {verification} "
            f"| [source]({row['source_url']}) |"
        )
    lines.extend(["", "## Public Source Files", ""])
    for dependency in source_dependencies:
        lines.append(f"- [{dependency['source_file']}]({dependency['source_url']})")
    lines.append("")
    return "\n".join(lines)


def relative_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "root"
