import json

import rock_kb.contributions as contributions
from rock_kb.contributions import import_public_contribution_bundles
from rock_kb.public_repo import sync_public_export_to_repo


def public_contribution_row(org_id="test-org"):
    return {
        "schema": "rock-kb-org-contribution-v1",
        "contribution_id": f"{org_id}:workflow-check",
        "org_id": org_id,
        "org_display_name": "Test Org",
        "concept_ids": ["workflows"],
        "contribution_type": "troubleshooting_pattern",
        "title": "Workflow launch check",
        "distilled_summary": "When troubleshooting workflow launch behavior, identify the launch surface, security context, Workflow Type, and active workflow records before changing actions.",
        "source_urls": ["https://community.rockrms.com/documentation/BookContent/12"],
        "source_record_ids": [],
        "redaction_attestation": True,
        "review_status": "redaction_reviewed",
        "license_attestation": True,
        "confidence": "medium",
        "needs_live_verification": True,
    }


def test_sync_public_export_preserves_public_intake_paths(tmp_path):
    export = tmp_path / "export"
    destination = tmp_path / "public-repo"
    (export / "agent").mkdir(parents=True)
    (export / "agent" / "rock-kb-manifest.json").write_text("{}\n", encoding="utf-8")
    (export / "community-contributions").mkdir()
    (export / "community-contributions" / "README.md").write_text("generated readme\n", encoding="utf-8")
    (destination / "agent").mkdir(parents=True)
    (destination / "agent" / "stale.json").write_text("{}\n", encoding="utf-8")
    (destination / "community-contributions" / "outside-org").mkdir(parents=True)
    (destination / "community-contributions" / "outside-org" / "bundle.jsonl").write_text('{"keep":true}\n', encoding="utf-8")

    result = sync_public_export_to_repo(destination=destination, export_dir=export)

    assert result["status"] == "ok"
    assert not (destination / "agent" / "stale.json").exists()
    assert (destination / "agent" / "rock-kb-manifest.json").exists()
    assert (destination / "community-contributions" / "README.md").read_text(encoding="utf-8") == "generated readme\n"
    assert (destination / "community-contributions" / "outside-org" / "bundle.jsonl").exists()


def test_import_public_contribution_bundles_validates_and_copies(monkeypatch, tmp_path):
    repo_root = tmp_path / "build"
    public_repo = tmp_path / "public"
    bundle = public_repo / "community-contributions" / "test-org" / "bundle.jsonl"
    bundle.parent.mkdir(parents=True)
    bundle.write_text(json.dumps(public_contribution_row()) + "\n", encoding="utf-8")
    output_root = repo_root / "contributions"
    monkeypatch.setattr(contributions, "REPO_ROOT", repo_root)

    result = import_public_contribution_bundles(public_repo=public_repo, output_root=output_root)

    assert result["status"] == "ok"
    assert result["imported_count"] == 1
    imported = output_root / "test-org" / "bundle.jsonl"
    assert imported.exists()
    assert json.loads(imported.read_text(encoding="utf-8"))["contribution_id"] == "test-org:workflow-check"


def test_import_public_contribution_bundles_rejects_org_mismatch(monkeypatch, tmp_path):
    repo_root = tmp_path / "build"
    public_repo = tmp_path / "public"
    bundle = public_repo / "community-contributions" / "test-org" / "bundle.jsonl"
    bundle.parent.mkdir(parents=True)
    row = public_contribution_row(org_id="other-org")
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")
    monkeypatch.setattr(contributions, "REPO_ROOT", repo_root)

    result = import_public_contribution_bundles(public_repo=public_repo, output_root=repo_root / "contributions")

    assert result["status"] == "fail"
    assert any("org_id does not match directory test-org" in error for error in result["errors"])
