from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

from .extract import now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import KNOWLEDGE_DIR, NORMALIZED_DIR

MOBILE_CONCEPT_DIR = KNOWLEDGE_DIR / "concepts" / "mobile"
MOBILE_RESOURCE_DIR = MOBILE_CONCEPT_DIR / "resources"
SELECTOR_INVENTORY_PATH = MOBILE_CONCEPT_DIR / "mobile-block-selector-xray.jsonl"
DEPENDENCY_PATH = MOBILE_CONCEPT_DIR / "mobile-block-selector-xray-dependencies.json"
SELECTOR_AUDIT_PATH = MOBILE_RESOURCE_DIR / "block-selector-image-audit.md"
CSS_XRAY_RESOURCE_PATH = MOBILE_RESOURCE_DIR / "css-xray-design-resource.md"

OFFICIAL_BLOCK_PATH = "/developer/mobile-docs/essentials/blocks"
SOURCE_PRIORITY = {
    "rock_mobile_docs": 0,
    "rock_developer": 1,
    "rock_community_site": 2,
}


def build_mobile_selector_audit() -> dict[str, Any]:
    """Regenerate the mobile selector audit markdown and dependency metadata."""
    inventory_rows = read_selector_inventory()
    write_jsonl(SELECTOR_INVENTORY_PATH, inventory_rows)

    dependency = build_selector_dependency_metadata(inventory_rows)
    write_json(DEPENDENCY_PATH, dependency)

    SELECTOR_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SELECTOR_AUDIT_PATH.write_text(render_selector_audit_markdown(inventory_rows, dependency), encoding="utf-8")

    return {
        "status": "ok",
        "selector_rows": len(inventory_rows),
        "selector_path": str(SELECTOR_INVENTORY_PATH),
        "dependency_path": str(DEPENDENCY_PATH),
        "audit_path": str(SELECTOR_AUDIT_PATH),
        "source_urls": dependency["source_url_count"],
        "missing_source_urls": dependency["missing_source_url_count"],
        "stale_dependency_count": len(selector_audit_dependency_staleness(dependency)),
    }


def read_selector_inventory(path: Optional[Path] = None) -> list[dict[str, Any]]:
    path = path or SELECTOR_INVENTORY_PATH
    rows = list(read_jsonl(path))
    return [normalize_selector_row(row) for row in rows]


def normalize_selector_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(row)
    for key in ["block", "confidence", "description", "evidence", "kind", "url"]:
        normalized[key] = str(normalized.get(key) or "").strip()
    selector = normalized.get("selector")
    normalized["selector"] = str(selector).strip() if selector not in {None, ""} else None
    element = normalized.get("element")
    normalized["element"] = str(element).strip() if element not in {None, ""} else None
    return normalized


def build_selector_dependency_metadata(inventory_rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_index = normalized_source_index()
    urls = sorted({str(row.get("url")) for row in inventory_rows if row.get("url")} | set(normalized_block_page_urls(source_index)))
    dependencies = []
    missing = []
    for url in urls:
        source = source_index.get(url)
        if not source:
            missing.append(url)
            dependencies.append({"url": url, "status": "missing_normalized_source"})
            continue
        dependencies.append(
            {
                "url": url,
                "status": "current",
                "source_id": source.get("source_id"),
                "source_title": source.get("source_title"),
                "source_record_id": source.get("id") or source.get("source_record_id"),
                "source_key": source_key(source),
                "content_hash": source.get("content_hash"),
                "excerpt_hash": sha256_text(str(source.get("excerpt") or "")),
                "retrieved_at": source.get("retrieved_at"),
            }
        )

    selector_rows = [row for row in inventory_rows if row.get("kind") == "selector"]
    source_hash = sha256_text(json.dumps(dependencies, sort_keys=True))
    inventory_hash = sha256_text(json.dumps(inventory_rows, sort_keys=True))
    return {
        "schema": "rock-kb-mobile-selector-audit-dependencies-v1",
        "built_at": now_iso(),
        "concept_id": "mobile",
        "resource_paths": {
            "css_xray_resource": str(CSS_XRAY_RESOURCE_PATH.relative_to(MOBILE_CONCEPT_DIR.parent.parent.parent)),
            "selector_audit": str(SELECTOR_AUDIT_PATH.relative_to(MOBILE_CONCEPT_DIR.parent.parent.parent)),
            "selector_inventory": str(SELECTOR_INVENTORY_PATH.relative_to(MOBILE_CONCEPT_DIR.parent.parent.parent)),
            "selector_dependencies": str(DEPENDENCY_PATH.relative_to(MOBILE_CONCEPT_DIR.parent.parent.parent)),
        },
        "selector_row_count": len(selector_rows),
        "inventory_row_count": len(inventory_rows),
        "source_url_count": len(urls),
        "missing_source_url_count": len(missing),
        "missing_source_urls": missing,
        "source_hash": source_hash,
        "inventory_hash": inventory_hash,
        "dependencies": dependencies,
    }


def normalized_source_index() -> dict[str, dict[str, Any]]:
    by_url: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in sorted(NORMALIZED_DIR.glob("*.jsonl")):
        for row in read_jsonl(path):
            url = row.get("source_url")
            if url:
                by_url[str(url)].append(row)
    return {url: preferred_source_record(rows) for url, rows in by_url.items()}


def normalized_block_page_urls(source_index: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(url for url in source_index if OFFICIAL_BLOCK_PATH in url)


def preferred_source_record(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return sorted(rows, key=lambda row: (SOURCE_PRIORITY.get(str(row.get("source_id")), 99), str(row.get("source_id") or "")))[0]


def source_key(row: dict[str, Any]) -> Optional[str]:
    record_id = str(row.get("id") or row.get("source_record_id") or "")
    if ":" in record_id:
        return record_id.split(":", 1)[1]
    return record_id or None


def render_selector_audit_markdown(inventory_rows: list[dict[str, Any]], dependency: dict[str, Any]) -> str:
    lines = [
        "# Rock Mobile Block Selector Image Audit",
        "",
        f"Generated: {dependency['built_at']}",
        "",
        "This concept resource digs through official Rock Mobile block documentation pages and their screenshots to recover selector and x-ray clues useful for styling Rock RMS mobile app blocks. It complements the broader [Rock Mobile CSS X-Ray Design Resource](css-xray-design-resource.md).",
        "",
        "## Method",
        "",
        f"- Uses {dependency['source_url_count']} official block-page source URLs under `developer/mobile-docs/essentials/blocks`.",
        "- Uses the reviewed selector inventory in [mobile-block-selector-xray.jsonl](../mobile-block-selector-xray.jsonl).",
        "- Selector rows preserve evidence type and confidence so OCR-derived callouts do not outrank explicit official text tables.",
        "- Source dependency hashes are recorded in [mobile-block-selector-xray-dependencies.json](../mobile-block-selector-xray-dependencies.json).",
        "- Private crawl/OCR scratch files may exist under `data/review/mobile-block-image-audit/`; those are review inputs, not public source artifacts.",
        "",
        "## Findings",
        "",
        "- Many block pages still have no styling x-ray or explicitly say no styling x-ray is available because the block renders a XAML template.",
        "- The most useful selector data appears in x-ray screenshots for finance, reminders, communication, check-in, profile, notes, and group blocks.",
        "- Content-style blocks usually need semantic `StyleClass` hooks in the authored XAML rather than relying on generated block internals.",
        "- Apple Vision OCR was more reliable than Gemma for exact label/class extraction from documentation screenshots.",
        "",
        "## Machine-Readable Inventory",
        "",
        "The selector inventory is available as JSONL at [knowledge/concepts/mobile/mobile-block-selector-xray.jsonl](../mobile-block-selector-xray.jsonl).",
        "",
        "## Selector Inventory",
        "",
    ]

    for block, rows in grouped_inventory_rows(inventory_rows):
        source_url = next((row.get("url") for row in rows if row.get("url")), "")
        lines.extend([f"### {block}", ""])
        if source_url:
            lines.extend([f"Source: [{source_url}]({source_url})", ""])

        selector_rows = [row for row in rows if row.get("kind") == "selector"]
        note_rows = [row for row in rows if row.get("kind") != "selector"]
        if selector_rows:
            lines.extend(
                [
                    "| Selector | Element | Use | Evidence | Confidence |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
            for row in selector_rows:
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            f"`{escape_table_cell(str(row.get('selector') or ''))}`",
                            escape_table_cell(str(row.get("element") or "")),
                            escape_table_cell(str(row.get("description") or "")),
                            escape_table_cell(str(row.get("evidence") or "")),
                            escape_table_cell(str(row.get("confidence") or "")),
                        ]
                    )
                    + " |"
                )
            lines.append("")
        if note_rows:
            lines.extend(["| Context | Note | Evidence | Confidence |", "| --- | --- | --- | --- |"])
            for row in note_rows:
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            escape_table_cell(str(row.get("kind") or "")),
                            escape_table_cell(str(row.get("description") or "")),
                            escape_table_cell(str(row.get("evidence") or "")),
                            escape_table_cell(str(row.get("confidence") or "")),
                        ]
                    )
                    + " |"
                )
            lines.append("")

    lines.extend(
        [
            "## Use Rules",
            "",
            "- Treat `official_text` rows as strongest because they come from page text or style-class tables.",
            "- Treat `image_xray_ocr` and `manual_image_review` rows as strong design clues, but verify against the current live docs and app shell before making production changes.",
            "- If a block exposes a template setting, prefer adding your own semantic `StyleClass` hooks inside the template.",
            "- If a block has no x-ray and no template, style only with documented block/page/device selectors and verify in the rendered app.",
            "",
        ]
    )
    return "\n".join(lines)


def grouped_inventory_rows(rows: Iterable[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    order: list[str] = []
    for row in rows:
        block = str(row.get("block") or "Unknown")
        if block not in groups:
            order.append(block)
        groups[block].append(row)
    return [(block, groups[block]) for block in order]


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def selector_audit_dependency_staleness(dependency: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    dependency = dependency or load_selector_dependency_metadata()
    current_index = normalized_source_index()
    stale = []
    for row in dependency.get("dependencies") or []:
        url = row.get("url")
        current = current_index.get(str(url))
        if not current:
            stale.append({"url": url, "reason": "missing_normalized_source"})
            continue
        if row.get("content_hash") != current.get("content_hash"):
            stale.append(
                {
                    "url": url,
                    "reason": "source_hash_changed",
                    "old_content_hash": row.get("content_hash"),
                    "new_content_hash": current.get("content_hash"),
                }
            )
    return stale


def mobile_selector_audit_status() -> dict[str, Any]:
    missing_paths = [
        str(path)
        for path in [CSS_XRAY_RESOURCE_PATH, SELECTOR_AUDIT_PATH, SELECTOR_INVENTORY_PATH, DEPENDENCY_PATH]
        if not path.exists()
    ]
    dependency = load_selector_dependency_metadata()
    stale = selector_audit_dependency_staleness(dependency) if dependency else []
    inventory_errors = validate_selector_inventory(read_selector_inventory() if SELECTOR_INVENTORY_PATH.exists() else [])
    return {
        "missing_paths": missing_paths,
        "stale_dependencies": stale,
        "stale_dependency_count": len(stale),
        "inventory_errors": inventory_errors,
        "inventory_error_count": len(inventory_errors),
        "dependency": dependency,
    }


def validate_selector_inventory(rows: list[dict[str, Any]]) -> list[str]:
    errors = []
    for index, row in enumerate(rows, start=1):
        label = f"row {index}"
        for key in ["block", "evidence", "confidence", "kind", "url"]:
            if not row.get(key):
                errors.append(f"{label} missing {key}")
        if row.get("kind") == "selector" and not row.get("selector"):
            errors.append(f"{label} selector row missing selector")
        if row.get("kind") != "selector" and not row.get("description"):
            errors.append(f"{label} non-selector row missing description")
    return errors


def load_selector_dependency_metadata(path: Optional[Path] = None) -> dict[str, Any]:
    path = path or DEPENDENCY_PATH
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
