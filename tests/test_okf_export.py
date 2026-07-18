from __future__ import annotations

import json
import hashlib
import zipfile
from pathlib import Path, PurePosixPath

from rock_kb.contribution_sources import public_contribution_records
from rock_kb.jsonl import read_jsonl
from rock_kb.okf_export import (
    MAX_INDEX_BYTES,
    MAX_INDEX_ENTRIES,
    audit_okf_export,
    build_okf_export,
    create_okf_archives,
    read_frontmatter,
    related_paths_for_row,
    write_update_log,
)


def test_okf_export_is_complete_typed_linked_and_conformant(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ROCK_KB_GENERATED_AT", "2026-07-09T12:00:00+00:00")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1783598400")
    destination = tmp_path / "okf"

    report = build_okf_export(
        destination,
        distribution_version="9.8.7",
        source_commit="0123456789abcdef",
    )

    assert report["status"] == "ok"
    assert report["okf_version"] == "0.1"
    assert report["distribution_version"] == "9.8.7"
    assert report["source_commit"] == "0123456789abcdef"
    assert report["read_only"] is True
    assert report["counts"]["claims"] == len(list(read_jsonl(Path("claims/approved-claims.jsonl"))))
    assert report["counts"]["recipes"] == len(list(read_jsonl(Path("agent/recipes.jsonl"))))
    assert report["counts"]["lava_contexts"] == len(list(read_jsonl(Path("agent/lava-contexts.jsonl"))))
    assert report["counts"]["models"] == len(list(read_jsonl(Path("agent/model-map-digests.jsonl"))))
    assert report["counts"]["source_summaries"] == len(list(read_jsonl(Path("agent/source-summaries.jsonl"))))
    assert report["counts"]["task_cards"] == len(list(read_jsonl(Path("agent/concept-task-cards.jsonl"))))
    assert report["counts"]["rock_issues"] == len(list(read_jsonl(Path("agent/rock-issues.jsonl"))))
    assert report["counts"]["rock_ideas"] == len(list(read_jsonl(Path("agent/rock-ideas.jsonl"))))
    assert report["counts"]["contributions"] == len(
        {str(row["contribution_id"]) for row in public_contribution_records()}
    )
    assert report["relationships"] > report["counts"]["claims"]
    assert audit_okf_export(destination) == []
    assert (destination / "LICENSE.txt").exists()
    assert (destination / "NOTICE.txt").exists()
    assert (destination / "profile.md").exists()

    root_index = (destination / "index.md").read_text(encoding="utf-8")
    assert read_frontmatter(root_index)["okf_version"] == "0.1"
    assert "complete read-only Open Knowledge Format distribution" in root_index
    assert "## 2026-07-09" in (destination / "log.md").read_text(encoding="utf-8")
    assert "2026-07-09T12:00:00" not in (destination / "log.md").read_text(encoding="utf-8")

    expected_types = {
        "Concept",
        "Agent Answer",
        "Claim",
        "Contribution Provenance",
        "Community Recipe",
        "Lava Context",
        "Rock Model",
        "Source Summary",
        "Agent Task Card",
        "Rock Issue",
        "Rock Idea",
        "Reference",
    }
    seen_ids: set[str] = set()
    seen_types: set[str] = set()
    for path in destination.rglob("*.md"):
        if path.name in {"index.md", "log.md"}:
            continue
        metadata = read_frontmatter(path.read_text(encoding="utf-8"))
        seen_types.add(str(metadata["type"]))
        if metadata.get("id"):
            assert metadata["id"] not in seen_ids
            seen_ids.add(str(metadata["id"]))
    assert expected_types <= seen_types

    for path in destination.rglob("index.md"):
        text = path.read_text(encoding="utf-8")
        assert len(text.encode("utf-8")) <= MAX_INDEX_BYTES
        assert sum(1 for line in text.splitlines() if line.startswith("- [")) <= MAX_INDEX_ENTRIES

    recipe = find_document(destination, "recipe:oneall:check-in-status-dashboard")
    recipe_metadata = read_frontmatter(recipe.read_text(encoding="utf-8"))
    assert recipe_metadata["type"] == "Community Recipe"
    assert recipe_metadata["canonical_id"] == "recipe:oneall:check-in-status-dashboard"
    assert recipe_metadata["source_path"]
    assert (destination / str(recipe_metadata["structured_record"]).lstrip("/")).exists()
    assert {row["type"] for row in recipe_metadata["relationships"]} >= {"about", "supersedes"}

    lava = find_document(destination, "lava_context:conflict-profile-template:person:989c0c46")
    assert "uses_model" in {row["type"] for row in read_frontmatter(lava.read_text(encoding="utf-8"))["relationships"]}
    group = find_document(destination, "model_map:stable:group")
    group_metadata = read_frontmatter(group.read_text(encoding="utf-8"))
    group_record = json.loads((destination / str(group_metadata["structured_record"]).lstrip("/")).read_text())
    assert "property_groups" in group_record["payload"]

    relationship_rows = [json.loads(line) for line in (destination / "relationships.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {row["type"] for row in relationship_rows} >= {"about", "supported_by", "uses_model", "related_model", "supersedes"}
    assert all(row["schema"] == "rock-kb-okf-relationship-v1" for row in relationship_rows)
    assert all(not row["source"].startswith("Claim:claim:") for row in relationship_rows)
    assert all(row["source"] != row["target"] for row in relationship_rows)

    claim_paths = list((destination / "claims").glob("*/*/*.md"))
    assert claim_paths, "claims must be sharded below concept and hash-prefix directories"


def test_okf_idea_relationships_resolve_to_canonical_issue_and_model_paths():
    idea_path = PurePosixPath("rock-ideas/open/a/idea.md")
    issue_path = PurePosixPath("rock-issues/core/b/issue.md")
    model_path = PurePosixPath("models/event/registration-instance.md")
    concept_path = PurePosixPath("concepts/event-registration.md")
    row = {
        "id": "rock_idea:2250",
        "kind": "rock_idea",
        "concepts": ["event-registration"],
        "payload": {"idea_id": "rock_idea:2250", "concept_ids": ["event-registration"]},
    }

    related = related_paths_for_row(
        row,
        concept_ids={"event-registration"},
        concept_paths={"event-registration": concept_path},
        reference_paths={},
        model_path_by_slug={"registration-instance": model_path},
        path_by_id={
            "rock_idea:2250": idea_path,
            "rock_issue:SparkDevNetwork/Rock#6919": issue_path,
            "model_map:stable:registration-instance": model_path,
        },
        idea_relationships=[
            {
                "relationship_type": "references_issue",
                "target_id": "rock_issue:SparkDevNetwork/Rock#6919",
            },
            {
                "relationship_type": "about_model",
                "target_id": "model_map:stable:registration-instance",
            },
        ],
    )

    assert set(related) == {
        ("about", concept_path),
        ("about_model", model_path),
        ("references_issue", issue_path),
    }


def test_okf_core_profile_is_smaller_and_keeps_canonical_agent_knowledge(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ROCK_KB_GENERATED_AT", "2026-07-14T12:00:00+00:00")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1784030400")
    destination = tmp_path / "core"

    report = build_okf_export(destination, distribution_version="9.8.7", source_commit="abc", profile="core")

    assert report["status"] == "ok"
    assert report["profile"] == "core"
    assert report["counts"].get("source_summaries", 0) == 0
    assert report["counts"].get("contributions", 0) == 0
    assert report["counts"].get("rock_issues", 0) == 0
    assert report["counts"]["claims"] < len(list(read_jsonl(Path("claims/approved-claims.jsonl"))))
    assert report["counts"]["recipes"] == len(list(read_jsonl(Path("agent/recipes.jsonl"))))
    assert find_document(destination, "model_map:stable:group")
    assert audit_okf_export(destination) == []



def test_okf_archive_packaging_is_versioned_and_rooted(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1783598400")
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "okf-manifest.json").write_text('{"status":"ok"}\n', encoding="utf-8")
    (bundle / "index.md").write_text("# Fixture\n", encoding="utf-8")

    rows = create_okf_archives(bundle, tmp_path / "archives", "9.8.7")

    archive_paths = {Path(row["path"]) for row in rows}
    zip_path = tmp_path / "archives" / "rock-agent-kb-okf-v9.8.7.zip"
    assert zip_path in archive_paths
    assert tmp_path / "archives" / "rock-agent-kb-okf-v9.8.7.tar.gz" in archive_paths
    assert tmp_path / "archives" / "rock-agent-kb-okf-v9.8.7.sha256" in archive_paths
    with zipfile.ZipFile(zip_path) as archive:
        assert "rock-agent-kb-okf-v9.8.7/okf-manifest.json" in archive.namelist()

    first_hashes = {row["name"]: row["sha256"] for row in rows}
    repeated = create_okf_archives(bundle, tmp_path / "archives-repeated", "9.8.7")
    assert first_hashes == {row["name"]: row["sha256"] for row in repeated}

    core_rows = create_okf_archives(bundle, tmp_path / "core-archives", "9.8.7", profile="core")
    assert {row["name"] for row in core_rows} == {
        "rock-agent-kb-okf-core-v9.8.7.zip",
        "rock-agent-kb-okf-core-v9.8.7.tar.gz",
        "rock-agent-kb-okf-core-v9.8.7.sha256",
    }


def test_okf_update_log_reports_real_snapshot_delta(tmp_path: Path):
    previous = tmp_path / "previous"
    current = tmp_path / "current"
    previous.mkdir()
    current.mkdir()
    (previous / "okf-manifest.json").write_text('{"distribution_version":"1.0.0"}\n', encoding="utf-8")
    old_hash = hashlib.sha256(b"old\n").hexdigest()
    (previous / "file-manifest.jsonl").write_text(
        json.dumps({"path": "same.md", "sha256": old_hash, "bytes": 4}) + "\n"
        + json.dumps({"path": "removed.md", "sha256": old_hash, "bytes": 4}) + "\n",
        encoding="utf-8",
    )
    (current / "same.md").write_text("new\n", encoding="utf-8")
    (current / "added.md").write_text("added\n", encoding="utf-8")

    changes = write_update_log(
        current,
        generated_at="2026-07-14T12:00:00+00:00",
        version="1.1.0",
        previous_bundle=previous,
    )

    assert changes == {"previous_version": "1.0.0", "added": 1, "changed": 1, "removed": 1}
    log = (current / "log.md").read_text(encoding="utf-8")
    assert "## 2026-07-14" in log
    assert "### Added" in log and "### Changed" in log and "### Removed" in log


def test_okf_audit_rejects_untyped_broken_private_and_bad_log_nodes(tmp_path: Path):
    (tmp_path / "index.md").write_text("---\nokf_version: '0.1'\n---\n\n# Index\n", encoding="utf-8")
    (tmp_path / "log.md").write_text("# Log\n\n## 2026-07-09T12:00:00Z\n", encoding="utf-8")
    (tmp_path / "bad.md").write_text("[Missing](missing.md)\n/Users/private/path\n", encoding="utf-8")

    errors = audit_okf_export(tmp_path)

    assert "bad.md missing non-empty type frontmatter" in errors
    assert "bad.md has unresolved link: missing.md" in errors
    assert "bad.md contains private marker: /Users/" in errors
    assert "log.md has non-ISO date heading: ## 2026-07-09T12:00:00Z" in errors


def find_document(destination: Path, document_id: str) -> Path:
    for path in destination.rglob("*.md"):
        if path.name in {"index.md", "log.md"}:
            continue
        if read_frontmatter(path.read_text(encoding="utf-8")).get("id") == document_id:
            return path
    raise AssertionError(f"Missing OKF document {document_id}")
