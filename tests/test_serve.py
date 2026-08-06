from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from rock_kb.serve.server import build_server
from rock_kb.serve import (
    assess_rock_issues,
    get_claim,
    get_claims,
    get_concept,
    get_lava_context,
    get_manifest,
    get_recipe,
    get_result,
    get_rock_issue,
    list_concepts,
    list_lava_contexts,
    list_rock_issues,
    plan_rock_issue_investigation,
    search,
    search_rock_issues,
)


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
        root / "agent" / "recipes.jsonl",
        [
            {
                "recipe_id": "test-org:check-in-dashboard",
                "org_id": "test-org",
                "title": "Check-In Dashboard",
                "summary": "Combine a registration roster with latest attendance.",
                "concept_ids": ["check-in"],
                "authority_tier": "community-reviewed",
                "implementation": {
                    "repository_url": "https://github.com/test-org/recipes",
                    "commit_sha": "a" * 40,
                    "source_path": "check-in-dashboard",
                },
            }
        ],
    )
    write_jsonl(
        root / "agent" / "lava-contexts.jsonl",
        [
            {
                "schema": "rock-kb-lava-context-v2",
                "id": "lava_context:check-in-label-checkout-dynamic-text:checkoutdatetime:fixture",
                "context_id": "check-in-label-checkout-dynamic-text",
                "context_family": "check-in-label",
                "surface_name": "Check-In Label Designer Checkout Dynamic Text",
                "surface_type": "label_dynamic_text",
                "concept_ids": ["lava", "check-in"],
                "root_key": "CheckoutDateTime",
                "root_type": "DateTime",
                "model_slug": None,
                "value_kind": "scalar",
                "nested_path": "",
                "availability": "source-code-confirmed",
                "availability_condition": "The Checkout data type is selected.",
                "may_be_null": False,
                "required_setting": "",
                "execution_phase": "label_render",
                "coverage_status": "complete_for_source_snapshot",
                "includes_context_ids": [],
                "source_id": "sparkdevnetwork_rock",
                "source_url": "https://github.com/SparkDevNetwork/Rock/blob/abc/Rock/CheckIn/CheckoutLabelData.cs#L68",
                "source_file": "Rock/CheckIn/CheckoutLabelData.cs",
                "source_symbol": "CheckoutLabelData",
                "source_line_start": 68,
                "source_line_end": 68,
                "source_ref": "develop",
                "source_commit": "a" * 40,
                "source_version": "20.0.5",
                "model_map_links": [],
                "notes": "",
                "needs_live_verification": False,
            }
        ],
    )
    write_jsonl(
        root / "claims" / "approved-claims.jsonl",
        [
            {"claim_id": "claim:workflow-source", "concept_ids": ["workflows"], "claim_tier": "source_backed", "claim": "Workflow claim."},
            {"claim_id": "claim:workflow-live", "concept_ids": ["workflows"], "claim_tier": "live_verified", "claim": "Live workflow claim."},
            {"claim_id": "claim:groups", "concept_ids": ["groups"], "claim_tier": "source_backed", "claim": "Group claim."},
        ],
    )
    write_jsonl(
        root / "agent" / "rock-issues.jsonl",
        [
            {
                "issue_id": "rock_issue:SparkDevNetwork/Rock#6919",
                "repository": "SparkDevNetwork/Rock",
                "component": "rock_core",
                "number": 6919,
                "title": "Azure Blob Storage race causes CPU saturation",
                "url": "https://github.com/SparkDevNetwork/Rock/issues/6919",
                "state": "open",
                "validation_state": "reported",
                "updated_at": "2026-07-15T00:00:00Z",
                "concept_ids": ["hosting-infrastructure"],
                "labels": [],
                "version_evidence": [
                    {
                        "component": "rock_core",
                        "relationship": "reported_affected",
                        "normalized_version": "19.2.0",
                        "version_line": "19.2",
                    }
                ],
                "linked_commit_shas": [],
                "remediation_state": "none_recorded",
                "evidence_state": "report_only",
            }
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


def test_search_and_concept_package_include_recipes(tmp_path):
    seed_root(tmp_path)

    results = search("registration attendance dashboard", root=tmp_path)
    concept = get_concept("check-in", root=tmp_path)

    assert results[0]["id"] == "recipe:test-org:check-in-dashboard"
    assert results[0]["authority_tier"] == "community-reviewed"
    assert concept["recipes"][0]["recipe_id"] == "test-org:check-in-dashboard"


def test_get_recipe_accepts_exact_result_ids_and_unique_slugs(tmp_path):
    seed_root(tmp_path)

    for recipe_id in [
        "test-org:check-in-dashboard",
        "recipe:test-org:check-in-dashboard",
        "check-in-dashboard",
    ]:
        result = get_recipe(recipe_id, root=tmp_path)
        assert result["status"] == "ok"
        assert result["recipe"]["recipe_id"] == "test-org:check-in-dashboard"


def test_get_recipe_rejects_ambiguous_bare_slug(tmp_path):
    seed_root(tmp_path)
    recipes_path = tmp_path / "agent" / "recipes.jsonl"
    recipes = [json.loads(line) for line in recipes_path.read_text(encoding="utf-8").splitlines()]
    recipes.append({**recipes[0], "recipe_id": "another-org:check-in-dashboard", "org_id": "another-org"})
    write_jsonl(recipes_path, recipes)

    result = get_recipe("check-in-dashboard", root=tmp_path)

    assert result["status"] == "ambiguous"
    assert result["candidate_recipe_ids"] == [
        "another-org:check-in-dashboard",
        "test-org:check-in-dashboard",
    ]


def test_manifest_and_concepts_load_from_public_agent_artifacts(tmp_path):
    seed_root(tmp_path)

    assert get_manifest(root=tmp_path)["concept_count"] == 1
    assert list_concepts(root=tmp_path)[0]["concept_id"] == "workflows"


def test_lava_context_list_and_exact_get_do_not_cross_surfaces(tmp_path):
    seed_root(tmp_path)

    listed = list_lava_contexts(context_family="check-in-label", root=tmp_path)
    exact = get_lava_context("check-in-label-checkout-dynamic-text", root_key="CheckoutDateTime", root=tmp_path)
    wrong = get_lava_context("check-in-label-person-dynamic-text", root=tmp_path)

    assert listed["count"] == 1
    assert exact["status"] == "ok"
    assert exact["roots"][0]["root_key"] == "CheckoutDateTime"
    assert wrong["status"] == "not_found"


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


def test_local_issue_tools_search_filter_assess_and_plan(tmp_path):
    seed_root(tmp_path)

    search_result = search_rock_issues("Azure CPU issue", root=tmp_path)
    listed = list_rock_issues(repository="core", state="open", version="19.2", root=tmp_path)
    exact = get_rock_issue("6919", root=tmp_path)
    assessed = assess_rock_issues({"core_version": "19.2.0"}, limit=1, offset=0, root=tmp_path)
    plan = plan_rock_issue_investigation("6919", include_private_instance=True, root=tmp_path)

    assert search_result["results"][0]["issue_id"] == "rock_issue:SparkDevNetwork/Rock#6919"
    assert listed["count"] == 1
    assert exact["status"] == "ok"
    assert assessed["results"][0]["applicability"] == "possible"
    assert assessed["total_count"] == 1
    assert assessed["has_more"] is False
    assert plan["admission"]["github_write_enabled"] is False
    assert next(row for row in plan["tasks"] if row["role"] == "instance_investigator")["visibility"] == "private_only"


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
        "kb_list_lava_contexts",
        "kb_get_lava_context",
        "kb_diff_lava_context",
        "kb_manifest",
        "kb_list_concepts",
        "kb_get_concept",
        "kb_get_claims",
        "kb_list_recipes",
        "kb_get_recipe",
        "kb_search_rock_issues",
        "kb_list_rock_issues",
        "kb_get_rock_issue",
        "kb_assess_rock_issues",
        "kb_plan_rock_issue_investigation",
    }
    assert "Start here for any Rock question" in server.tools["kb_search"]["description"]
