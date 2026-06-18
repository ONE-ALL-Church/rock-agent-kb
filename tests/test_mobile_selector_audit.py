import json

from rock_kb import mobile_selector_audit as audit
from rock_kb.jsonl import write_jsonl


def test_mobile_selector_audit_dependencies_include_all_block_pages(tmp_path, monkeypatch):
    concept_dir = tmp_path / "knowledge" / "concepts" / "mobile"
    normalized_dir = tmp_path / "data" / "normalized"
    monkeypatch.setattr(audit, "MOBILE_CONCEPT_DIR", concept_dir)
    monkeypatch.setattr(audit, "MOBILE_RESOURCE_DIR", concept_dir / "resources")
    monkeypatch.setattr(audit, "SELECTOR_INVENTORY_PATH", concept_dir / "mobile-block-selector-xray.jsonl")
    monkeypatch.setattr(audit, "DEPENDENCY_PATH", concept_dir / "mobile-block-selector-xray-dependencies.json")
    monkeypatch.setattr(audit, "SELECTOR_AUDIT_PATH", concept_dir / "resources" / "block-selector-image-audit.md")
    monkeypatch.setattr(audit, "CSS_XRAY_RESOURCE_PATH", concept_dir / "resources" / "css-xray-design-resource.md")
    monkeypatch.setattr(audit, "NORMALIZED_DIR", normalized_dir)

    selector_url = "https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notes"
    no_selector_url = "https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/hero"
    write_jsonl(
        audit.SELECTOR_INVENTORY_PATH,
        [
            {
                "block": "Notes",
                "confidence": "high",
                "description": "note title",
                "element": "Label",
                "evidence": "official_text",
                "kind": "selector",
                "selector": "note-item-name",
                "url": selector_url,
            }
        ],
    )
    write_jsonl(
        normalized_dir / "rock_mobile_docs.jsonl",
        [
            normalized_row(selector_url, "hash-a"),
            normalized_row(no_selector_url, "hash-b"),
        ],
    )

    result = audit.build_mobile_selector_audit()
    dependency = json.loads(audit.DEPENDENCY_PATH.read_text())

    assert result["source_urls"] == 2
    assert dependency["source_url_count"] == 2
    assert dependency["selector_row_count"] == 1
    assert {row["url"] for row in dependency["dependencies"]} == {selector_url, no_selector_url}
    assert "note-item-name" in audit.SELECTOR_AUDIT_PATH.read_text()


def test_mobile_selector_audit_status_reports_fresh(tmp_path, monkeypatch):
    concept_dir = tmp_path / "knowledge" / "concepts" / "mobile"
    normalized_dir = tmp_path / "data" / "normalized"
    monkeypatch.setattr(audit, "MOBILE_CONCEPT_DIR", concept_dir)
    monkeypatch.setattr(audit, "MOBILE_RESOURCE_DIR", concept_dir / "resources")
    monkeypatch.setattr(audit, "SELECTOR_INVENTORY_PATH", concept_dir / "mobile-block-selector-xray.jsonl")
    monkeypatch.setattr(audit, "DEPENDENCY_PATH", concept_dir / "mobile-block-selector-xray-dependencies.json")
    monkeypatch.setattr(audit, "SELECTOR_AUDIT_PATH", concept_dir / "resources" / "block-selector-image-audit.md")
    monkeypatch.setattr(audit, "CSS_XRAY_RESOURCE_PATH", concept_dir / "resources" / "css-xray-design-resource.md")
    monkeypatch.setattr(audit, "NORMALIZED_DIR", normalized_dir)
    source_url = "https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notes"
    write_jsonl(
        audit.SELECTOR_INVENTORY_PATH,
        [
            {
                "block": "Notes",
                "confidence": "high",
                "description": "note title",
                "evidence": "official_text",
                "kind": "selector",
                "selector": "note-item-name",
                "url": source_url,
            }
        ],
    )
    write_jsonl(normalized_dir / "rock_mobile_docs.jsonl", [normalized_row(source_url, "hash-a")])
    audit.CSS_XRAY_RESOURCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    audit.CSS_XRAY_RESOURCE_PATH.write_text("# CSS X-Ray\n", encoding="utf-8")
    audit.build_mobile_selector_audit()

    assert audit.mobile_selector_audit_status()["status"] == "fresh"


def test_selector_audit_dependency_staleness_reports_changed_hash(tmp_path, monkeypatch):
    normalized_dir = tmp_path / "data" / "normalized"
    monkeypatch.setattr(audit, "NORMALIZED_DIR", normalized_dir)
    source_url = "https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notes"
    write_jsonl(normalized_dir / "rock_mobile_docs.jsonl", [normalized_row(source_url, "new-hash")])

    stale = audit.selector_audit_dependency_staleness(
        {
            "dependencies": [
                {
                    "url": source_url,
                    "content_hash": "old-hash",
                }
            ]
        }
    )

    assert stale == [
        {
            "url": source_url,
            "reason": "source_hash_changed",
            "old_content_hash": "old-hash",
            "new_content_hash": "new-hash",
        }
    ]


def normalized_row(url: str, content_hash: str) -> dict:
    return {
        "id": "rock_mobile_docs:" + content_hash,
        "source_id": "rock_mobile_docs",
        "source_url": url,
        "source_title": url.rsplit("/", 1)[-1],
        "content_hash": content_hash,
        "excerpt": "",
        "retrieved_at": "2026-06-04T00:00:00+00:00",
    }
