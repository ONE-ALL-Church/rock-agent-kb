from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from rock_kb.serve.server import build_server
from rock_kb.serve import get_claim, get_claims, get_concept, get_manifest, get_result, list_concepts, search


def seed_root(root: Path) -> None:
    (root / "data" / "index").mkdir(parents=True)
    (root / "agent").mkdir()
    (root / "claims").mkdir()
    (root / "knowledge" / "concepts" / "workflows").mkdir(parents=True)
    (root / "data" / "review").mkdir(parents=True)

    with sqlite3.connect(root / "data" / "index" / "kb.sqlite") as connection:
        connection.execute(
            """
            CREATE TABLE records (
                id TEXT PRIMARY KEY,
                source_id TEXT,
                source_url TEXT,
                source_title TEXT,
                source_kind TEXT,
                license_status TEXT,
                topics TEXT,
                summary TEXT,
                excerpt TEXT,
                canonical_path TEXT,
                json TEXT
            )
            """
        )
        connection.execute("CREATE VIRTUAL TABLE records_fts USING fts5(id, source_title, topics, summary, excerpt)")
        rows = [
            (
                "public:workflow",
                "rock_docs",
                "https://example.org/workflows",
                "Workflow Docs",
                "docs",
                "public",
                "workflows,automation",
                "Workflow launch troubleshooting and automation guidance.",
                "Workflow launch troubleshooting.",
                "knowledge/concepts/workflows/index.md",
            ),
            (
                "private:workflow",
                "private_docs",
                "",
                "Private Workflow Notes",
                "private",
                "private",
                "workflows",
                "Workflow secret private notes.",
                "Workflow secret private notes.",
                "data/review/private-workflows.md",
            ),
        ]
        for row in rows:
            connection.execute(
                """
                INSERT INTO records
                (id, source_id, source_url, source_title, source_kind, license_status, topics, summary, excerpt, canonical_path, json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (*row, json.dumps({"id": row[0]})),
            )
            connection.execute(
                "INSERT INTO records_fts (id, source_title, topics, summary, excerpt) VALUES (?, ?, ?, ?, ?)",
                (row[0], row[3], row[6], row[7], row[8]),
            )

    (root / "agent" / "rock-kb-manifest.json").write_text(json.dumps({"schema": "manifest", "concept_count": 1}), encoding="utf-8")
    write_jsonl(
        root / "agent" / "concept-index.jsonl",
        [{"concept_id": "workflows", "title": "Workflows", "guide_path": "knowledge/concepts/workflows/index.md"}],
    )
    write_jsonl(root / "agent" / "answer-pack.jsonl", [{"id": "answer:workflows", "concept_id": "workflows", "answer": "Check triggers."}])
    write_jsonl(root / "agent" / "concept-task-cards.jsonl", [{"task_id": "task:workflow", "concept_id": "workflows", "title": "Inspect trigger"}])
    write_jsonl(root / "agent" / "concept-release-caveats.jsonl", [{"concept_id": "workflows", "summary": "Version-specific workflow caveat."}])
    write_jsonl(
        root / "claims" / "approved-claims.jsonl",
        [
            {"claim_id": "claim:workflow-source", "concept_ids": ["workflows"], "claim_tier": "source_backed", "claim": "Workflow claim."},
            {"claim_id": "claim:workflow-live", "concept_ids": ["workflows"], "claim_tier": "live_verified", "claim": "Live workflow claim."},
            {"claim_id": "claim:groups", "concept_ids": ["groups"], "claim_tier": "source_backed", "claim": "Group claim."},
        ],
    )
    (root / "knowledge" / "concepts" / "workflows" / "quickstart.md").write_text("# Workflow Quickstart\n", encoding="utf-8")
    (root / "knowledge" / "concepts" / "workflows" / "index.md").write_text("# Workflows\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def test_search_uses_existing_fts_and_filters_private_paths(tmp_path):
    seed_root(tmp_path)

    results = search("workflow", root=tmp_path)

    assert [row["id"] for row in results] == ["public:workflow"]
    assert results[0]["path"] == "knowledge/concepts/workflows/index.md"
    assert results[0]["concept"] == "workflows"


def test_manifest_and_concepts_load_from_public_agent_artifacts(tmp_path):
    seed_root(tmp_path)

    assert get_manifest(root=tmp_path)["concept_count"] == 1
    assert list_concepts(root=tmp_path)[0]["concept_id"] == "workflows"


def test_get_concept_assembles_public_concept_payload(tmp_path):
    seed_root(tmp_path)

    concept = get_concept("workflows", root=tmp_path)

    assert concept["title"] == "Workflows"
    assert "Workflow Quickstart" in concept["quickstart"]
    assert concept["answers"][0]["id"] == "answer:workflows"
    assert concept["task_cards"][0]["task_id"] == "task:workflow"
    assert concept["release_caveats"][0]["summary"] == "Version-specific workflow caveat."


def test_get_claims_filters_by_concept_and_tier(tmp_path):
    seed_root(tmp_path)

    assert {row["claim_id"] for row in get_claims("workflows", root=tmp_path)} == {"claim:workflow-source", "claim:workflow-live"}
    assert [row["claim_id"] for row in get_claims("workflows", tier="live_verified", root=tmp_path)] == ["claim:workflow-live"]


def test_exact_result_and_claim_lookup(tmp_path):
    seed_root(tmp_path)

    result = get_result("public:workflow", root=tmp_path)
    claim = get_claim("workflow-source", root=tmp_path)

    assert result["status"] == "ok"
    assert result["result"]["payload"]["id"] == "public:workflow"
    assert claim["status"] == "ok"
    assert claim["claim"]["claim_id"] == "claim:workflow-source"


class FakeFastMCP:
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, dict] = {}

    def tool(self, name: str, description: str):
        def decorator(func):
            self.tools[name] = {"description": description, "func": func}
            return func

        return decorator


def test_build_server_registers_expected_tools():
    server = build_server(fastmcp_cls=FakeFastMCP)

    assert server.name == "Rock KB"
    assert set(server.tools) == {
        "kb_search",
        "kb_get_result",
        "kb_get_claim",
        "kb_list_models",
        "kb_get_model",
        "kb_manifest",
        "kb_list_concepts",
        "kb_get_concept",
        "kb_get_claims",
    }
    assert "Start here for any Rock question" in server.tools["kb_search"]["description"]
