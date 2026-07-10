from __future__ import annotations

import json

import pytest

from rock_kb import recipes


def test_canonical_recipes_validate_and_use_immutable_source_pins():
    rows = recipes.load_recipes()
    expected_ids = {
        "oneall:check-in-status-dashboard",
        "oneall:communication-history-active-search",
        "oneall:workflow-backed-sms-verification",
    }

    assert {row["recipe_id"] for row in rows} == expected_ids
    for row in rows:
        assert len(row["implementation"]["commit_sha"]) == 40
        assert row["implementation"]["commit_sha"] in row["implementation"]["manifest_url"]
        assert all(len(item["sha256"]) == 64 for item in row["implementation"]["files"])


def test_recipe_validation_rejects_unknown_concept(tmp_path):
    source = json.loads(recipes.recipe_paths()[0].read_text(encoding="utf-8"))
    source["org_id"] = "test-org"
    source["recipe_id"] = "test-org:example"
    source["concept_ids"] = ["does-not-exist"]
    source["implementation"]["owner"] = "ONE-ALL-Church"
    target = tmp_path / "test-org" / "example.json"
    target.parent.mkdir()
    target.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="unknown concept_ids"):
        recipes.load_recipes(tmp_path)


def test_build_recipes_writes_agent_and_human_artifacts(monkeypatch, tmp_path):
    monkeypatch.setattr(recipes, "RECIPE_DIR", recipes.RECIPE_DIR)
    monkeypatch.setattr(recipes, "RECIPE_OUTPUT", tmp_path / "agent" / "recipes.jsonl")
    monkeypatch.setattr(recipes, "RECIPE_SUMMARY", tmp_path / "agent" / "recipe-summary.json")
    monkeypatch.setattr(recipes, "RECIPE_KNOWLEDGE_DIR", tmp_path / "knowledge" / "recipes")

    report = recipes.build_recipes()

    assert report["recipe_count"] == 3
    assert (tmp_path / "agent" / "recipes.jsonl").exists()
    expected_artifacts = {
        "check-in-status-dashboard.md": "d8ea54fa67ef",
        "communication-history-active-search.md": "066de269c307",
        "workflow-backed-sms-verification.md": "066de269c307",
    }
    for filename, commit_prefix in expected_artifacts.items():
        rendered = (tmp_path / "knowledge" / "recipes" / "oneall" / filename).read_text(encoding="utf-8")
        assert "Reusable Learnings" in rendered
        assert commit_prefix in rendered


def test_promote_recipe_contribution_extracts_reviewed_canonical_record(monkeypatch, tmp_path):
    recipe = json.loads(recipes.recipe_paths()[0].read_text(encoding="utf-8"))
    recipe["review_status"] = "community_unreviewed"
    recipe["authority_tier"] = "community-unreviewed"
    contribution = {
        "schema": "rock-kb-org-contribution-v1",
        "contribution_id": recipe["recipe_id"],
        "org_id": recipe["org_id"],
        "org_display_name": "ONE&ALL Church",
        "contribution_type": "recipe",
        "concept_ids": recipe["concept_ids"],
        "title": recipe["title"],
        "distilled_summary": recipe["summary"],
        "source_urls": [recipe["implementation"]["repository_url"]],
        "source_record_ids": [],
        "confidence": "high",
        "review_status": "redaction_reviewed",
        "needs_live_verification": True,
        "license_attestation": True,
        "redaction_attestation": True,
        "recipe": recipe,
    }
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(contribution) + "\n", encoding="utf-8")
    output = tmp_path / "recipes"
    monkeypatch.setattr(recipes, "RECIPE_DIR", output)

    report = recipes.promote_recipe_contribution(bundle, recipe["recipe_id"])

    promoted = json.loads((output / "oneall" / "check-in-status-dashboard.json").read_text(encoding="utf-8"))
    assert report["status"] == "ok"
    assert promoted["review_status"] == "community_reviewed"
    assert promoted["authority_tier"] == "community-reviewed"
