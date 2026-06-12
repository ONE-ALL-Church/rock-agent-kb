from __future__ import annotations

import importlib.util
from pathlib import Path


def load_audit_module():
    path = Path("scripts/audit_tracked_tree.py")
    spec = importlib.util.spec_from_file_location("audit_tracked_tree", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tracked_tree_blocks_ignored_data_and_public_output_prefixes():
    audit = load_audit_module()

    errors = audit.audit_tracked_path("data/review/live-verification-evidence/example.md")

    assert errors
    assert "must remain ignored" in errors[0]


def test_tracked_tree_scans_public_paths_only():
    audit = load_audit_module()

    assert audit.should_scan_text("knowledge/concepts/check-in/guide.md")
    assert audit.should_scan_text("docs/runbooks/public-publish-runbook.md")
    assert not audit.should_scan_text("src/rock_kb/publish.py")
    assert not audit.should_scan_text("tests/test_audit_private.py")


def test_tracked_tree_detects_private_markers_in_public_text(tmp_path):
    audit = load_audit_module()
    path = tmp_path / "public.md"
    path.write_text("private path: /Users/example/private.md\n", encoding="utf-8")

    errors = audit.audit_text_file(path)

    assert any("absolute local user path" in error for error in errors)
