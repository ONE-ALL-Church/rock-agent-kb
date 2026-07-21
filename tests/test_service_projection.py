from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from rock_kb import service_projection
from rock_kb.service_projection import build_d1_seed_sql, build_retrieval_documents, build_search_rows, build_service_projection, retrieval_projection_diff


def load_update_bindings():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "configure_service_bindings.py"
    spec = importlib.util.spec_from_file_location("configure_service_bindings", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.update_bindings


def test_build_search_rows_includes_tiered_claims_and_concepts():
    rows = build_search_rows()

    assert any(row["kind"] == "concept" and row["concept"] == "check-in" for row in rows)
    assert any(row["kind"] == "claim" and row["claim_tier"] for row in rows)
    assert all("authority_tier" in row and "claim_tier" in row for row in rows)
    corroborating_claims = [
        row
        for row in rows
        if row["kind"] == "claim"
        and (row.get("payload", {}).get("derived_from", {}).get("related_contribution_ids") or [])
    ]
    assert corroborating_claims
    assert all(row["title"] == row["body"] for row in corroborating_claims)


def test_build_search_rows_includes_public_community_contributions(monkeypatch):
    monkeypatch.setattr(
        service_projection,
        "public_contribution_records",
        lambda: [
            {
                "contribution_id": "test-org:workflow-pattern",
                "org_id": "test-org",
                "source_id": "org_contribution",
                "source_title": "Workflow launch pattern",
                "source_url": "https://community.rockrms.com/documentation",
                "summary": "Check workflow trigger, activation, context, and action logs before changing configuration.",
                "topics": ["workflows"],
                "authority_tier": "community-unreviewed",
                "claim_tier": "routing_context_only",
                "bundle_path": "community-contributions/test-org/bundle.jsonl",
            }
        ],
    )

    rows = build_search_rows()
    row = next(row for row in rows if row["id"] == "community_contribution:test-org:workflow-pattern")

    assert row["kind"] == "community_contribution"
    assert row["authority_tier"] == "community-unreviewed"
    assert row["claim_tier"] == "routing_context_only"
    assert row["payload"]["claim"] == row["body"]
    assert row["payload"]["concept_ids"] == ["workflows"]
    assert row["concepts"] == ["workflows"]
    assert row["legacy_ids"] == ["community_contribution:test-org:workflow-pattern:workflows"]


def test_reviewed_contribution_wins_over_unreviewed_copy(monkeypatch):
    shared = {
        "contribution_id": "test-org:reviewed-pattern",
        "org_id": "test-org",
        "source_id": "org_contribution",
        "source_title": "Reviewed pattern",
        "source_url": "https://community.rockrms.com/documentation",
        "summary": "Use the reviewed canonical pattern.",
        "topics": ["workflows"],
        "claim_tier": "routing_context_only",
    }
    monkeypatch.setattr(
        service_projection,
        "public_contribution_records",
        lambda: [
            {
                **shared,
                "authority_tier": "community-reviewed",
                "bundle_path": "contributions/test-org/bundle.jsonl",
            },
            {
                **shared,
                "authority_tier": "community-unreviewed",
                "bundle_path": "community-contributions/test-org/bundle.jsonl",
            },
        ],
    )

    rows = build_search_rows()
    matches = [row for row in rows if row["id"] == "community_contribution:test-org:reviewed-pattern"]

    assert len(matches) == 1
    assert matches[0]["authority_tier"] == "community-reviewed"
    assert matches[0]["path"] == "contributions/test-org/bundle.jsonl"


def test_promoted_recipe_contribution_is_not_indexed_as_duplicate_guidance(monkeypatch):
    monkeypatch.setattr(
        service_projection,
        "public_contribution_records",
        lambda: [
            {
                "contribution_id": "test-org:workflow-recipe",
                "contribution_type": "recipe",
                "org_id": "test-org",
                "source_title": "Old workflow recipe",
                "summary": "Obsolete recipe guidance.",
                "topics": ["workflows"],
                "authority_tier": "community-unreviewed",
                "claim_tier": "routing_context_only",
                "bundle_path": "community-contributions/test-org/bundle.jsonl",
            }
        ],
    )

    original_read_jsonl = service_projection.read_jsonl

    def fake_read_jsonl(path):
        if path.name == "recipes.jsonl":
            return [{"recipe_id": "test-org:workflow-recipe"}]
        return original_read_jsonl(path)

    monkeypatch.setattr(service_projection, "read_jsonl", fake_read_jsonl)

    rows = service_projection.contribution_search_rows()

    assert rows == []


def test_recipe_explicitly_supersedes_only_named_contribution_patterns(monkeypatch):
    monkeypatch.setattr(
        service_projection,
        "public_contribution_records",
        lambda: [
            {
                "contribution_id": "test-org:older-dashboard-pattern",
                "contribution_type": "guide_section",
                "org_id": "test-org",
                "source_title": "Older dashboard pattern",
                "summary": "Guidance now incorporated into the canonical recipe.",
                "topics": ["check-in"],
            },
            {
                "contribution_id": "test-org:distinct-check-in-pattern",
                "contribution_type": "guide_section",
                "org_id": "test-org",
                "source_title": "Distinct check-in pattern",
                "summary": "Separate guidance that remains useful.",
                "topics": ["check-in"],
            },
        ],
    )

    original_read_jsonl = service_projection.read_jsonl

    def fake_read_jsonl(path):
        if path.name == "recipes.jsonl":
            return iter(
                [
                    {
                        "recipe_id": "test-org:canonical-dashboard",
                        "supersedes_contribution_ids": ["test-org:older-dashboard-pattern"],
                    }
                ]
            )
        return original_read_jsonl(path)

    monkeypatch.setattr(service_projection, "read_jsonl", fake_read_jsonl)

    rows = service_projection.contribution_search_rows()

    assert [row["id"] for row in rows] == [
        "community_contribution:test-org:distinct-check-in-pattern"
    ]


def test_recipe_search_rows_include_reusable_learnings():
    rows = service_projection.recipe_search_rows()
    row = next(row for row in rows if row["id"] == "recipe:oneall:check-in-status-dashboard")

    assert row["kind"] == "recipe"
    assert row["authority_tier"] == "community-reviewed"
    assert row["claim_tier"] == "answer_pack_approved"
    assert "AttendanceOccurrence" in row["body"]
    assert row["payload"]["implementation"]["commit_sha"] == "d8ea54fa67efe40692689fb009561ff96e88bf42"
    assert row["payload"]["supersedes_contribution_ids"] == [
        "oneall:read-only-check-in-status-dashboard-data-pattern"
    ]
    assert set(row["concepts"]) >= {"check-in", "event-registration", "lava"}
    assert "recipe:oneall:check-in-status-dashboard:check-in" in row["legacy_ids"]


def test_answer_search_rows_include_live_inspection_checklist(monkeypatch):
    def fake_read_jsonl(path):
        if path.name == "answer-pack.jsonl":
            return [
                {
                    "id": "answer:workflows:live-inspection",
                    "concept_id": "workflows",
                    "question": "What live Rock records should I inspect for Workflows?",
                    "answer": "Inspect WorkflowType and Workflow records.",
                    "live_checklist_id": "live-checklist:workflows",
                    "citations": [{"title": "Workflow docs", "url": "https://example.test/workflow"}],
                }
            ]
        if path.name == "live-inspection-checklists.jsonl":
            return [
                {
                    "id": "live-checklist:workflows",
                    "inspection_targets": ["WorkflowType and Workflow records"],
                    "steps": ["Inspect launch surfaces."],
                    "probes": [{"label": "Workflow actions", "sql": "SELECT * FROM WorkflowActionType;"}],
                }
            ]
        return []

    monkeypatch.setattr(service_projection, "read_jsonl", fake_read_jsonl)

    rows = service_projection.answer_search_rows()

    assert len(rows) == 1
    assert "WorkflowActionType" in rows[0]["body"]
    assert "Workflow docs" in rows[0]["body"]


def test_model_map_search_rows_include_model_detail_properties():
    rows = service_projection.model_map_search_rows()
    row = next(row for row in rows if row["id"] == "model_map:stable:group-member")

    assert row["kind"] == "model_map"
    assert row["concept"] == "model-map"
    assert row["path"] == "knowledge/model-map/models/group-member.md"
    assert row["payload"]["schema"] == "rock-kb-model-map-search-payload-v1"
    assert row["payload"]["identity"]["model_slug"] == "group-member"
    assert "GroupMember" in row["body"]
    assert "exact slug group-member" in row["body"]
    assert "PersonId" in row["body"]
    assert "GroupRoleId" in row["body"]


def test_lava_context_search_rows_include_source_backed_roots(monkeypatch):
    def fake_read_jsonl(path):
        if path.name == "lava-contexts.jsonl":
            return [
                {
                    "schema": "rock-kb-lava-context-v1",
                    "id": "lava_context:check-in-label-person-dynamic-text:personattendance:abc12345",
                    "context_id": "check-in-label-person-dynamic-text",
                    "context_family": "check-in-label",
                    "surface_name": "Check-In Label Designer Person Dynamic Text",
                    "surface_type": "label_dynamic_text",
                    "concept_ids": ["lava", "check-in"],
                    "root_key": "PersonAttendance",
                    "root_type": "List<LabelAttendanceDetail>",
                    "model_slug": None,
                    "value_kind": "collection",
                    "nested_path": "",
                    "availability": "source-code-confirmed",
                    "source_id": "sparkdevnetwork_rock",
                    "source_url": "https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L52",
                    "source_file": "Rock/CheckIn/v2/Labels/PersonLabelData.cs",
                    "source_symbol": "PersonLabelData",
                    "source_line_start": 52,
                    "source_ref": "develop",
                    "model_map_links": [],
                    "needs_live_verification": False,
                    "notes": "Person label data property exposed to Dynamic Text Lava.",
                }
            ]
        return []

    monkeypatch.setattr(service_projection, "read_jsonl", fake_read_jsonl)

    rows = service_projection.lava_context_search_rows()

    assert len(rows) == 1
    assert rows[0]["concept"] == "lava"
    assert set(rows[0]["concepts"]) == {"lava", "check-in"}
    assert set(rows[0]["legacy_ids"]) == {
        "lava_context:check-in-label-person-dynamic-text:personattendance:abc12345:lava",
        "lava_context:check-in-label-person-dynamic-text:personattendance:abc12345:check-in",
    }
    assert all(row["kind"] == "lava_context" for row in rows)
    assert all(row["authority_tier"] == "source-code-confirmed" for row in rows)
    assert all(row["claim_tier"] == "source_backed" for row in rows)
    assert "PersonAttendance" in rows[0]["body"]
    assert "Person Attendance" in rows[0]["body"]
    assert rows[0]["payload"]["source_line_start"] == 52


def test_lava_context_search_body_adds_natural_language_aliases():
    body = service_projection.lava_context_search_body(
        {
            "context_id": "event-registrant-waitlist-transition-template",
            "context_family": "event-registration",
            "surface_name": "Registrant wait-list transition email Lava",
            "surface_type": "event_registration_waitlist_transition_template",
            "root_key": "TransitionedRegistrants",
            "root_type": "List<RegistrationRegistrant>",
            "value_kind": "collection",
            "availability": "source-code-confirmed",
            "source_symbol": "RegistrantWaitListMove.BuildMergeFields",
            "source_file": "Rock.Blocks/Event/RegistrantWaitListMove.cs",
            "notes": "Registrant wait-list transition emails use this root.",
            "model_map_links": [{"model_slug": "registration-registrant", "model_title": "RegistrationRegistrant"}],
        }
    )

    assert "Transitioned Registrants" in body
    assert "event registrant waitlist transition template" in body
    assert "registration registrant" in body
    assert "Registration Registrant" in body


def test_source_summary_search_rows_preserve_records_and_reviewed_insights(monkeypatch):
    def fake_read_jsonl(path):
        if path.name != "source-summaries.jsonl":
            return []
        return [
            {
                "id": "rock_youtube:video-one:public-summary",
                "source_record_id": "rock_youtube:video-one",
                "source_id": "rock_youtube",
                "source_title": "First Rock Video",
                "source_url": "https://www.youtube.com/watch?v=video-one",
                "summary": "A product overview.",
                "topics": ["ai"],
                "key_insights": [
                    {
                        "topic": "runtime safety",
                        "insight": "Do not expose arbitrary AI-generated SQL as a runtime tool.",
                        "timestamp": "01:11:20",
                    }
                ],
            },
            {
                "id": "rock_youtube:video-two:public-summary",
                "source_record_id": "rock_youtube:video-two",
                "source_id": "rock_youtube",
                "source_title": "Second Rock Video",
                "source_url": "https://www.youtube.com/watch?v=video-two",
                "summary": "A separate product overview.",
                "topics": ["ai"],
            },
        ]

    monkeypatch.setattr(service_projection, "read_jsonl", fake_read_jsonl)

    rows = service_projection.source_summary_search_rows()

    assert [row["id"] for row in rows] == [
        "source:rock_youtube:video-one",
        "source:rock_youtube:video-two",
    ]
    assert rows[0]["title"] == "First Rock Video"
    assert rows[0]["url"] == "https://www.youtube.com/watch?v=video-one"
    assert "AI-generated SQL" in rows[0]["body"]
    assert "01:11:20" in rows[0]["body"]
    assert rows[0]["source_id"] == "rock_youtube"


def test_build_search_rows_uses_one_row_per_canonical_multi_concept_artifact():
    rows = build_search_rows()
    claim_count = sum(1 for row in read_jsonl_for_test("claims/approved-claims.jsonl") if row.get("claim_id"))
    recipe_count = sum(1 for row in read_jsonl_for_test("agent/recipes.jsonl") if row.get("recipe_id"))
    lava_count = sum(1 for row in read_jsonl_for_test("agent/lava-contexts.jsonl") if row.get("id") or row.get("context_id"))

    assert len([row for row in rows if row["kind"] == "claim"]) == claim_count
    assert len([row for row in rows if row["kind"] == "recipe"]) == recipe_count
    assert len([row for row in rows if row["kind"] == "lava_context"]) == lava_count
    assert len({row["id"] for row in rows}) == len(rows)
    assert all(isinstance(row["concepts"], list) for row in rows)


def test_retrieval_documents_are_contextual_stable_and_policy_scoped():
    documents = build_retrieval_documents(
        [
            {
                "id": "claim:claim:abc",
                "kind": "claim",
                "title": "operational guidance",
                "body": "Use managed Rock authorization for data access.",
                "path": "claims/approved-claims.jsonl",
                "url": "https://example.test/source",
                "concept": "security-permissions",
                "concepts": ["security-permissions", "api-integrations"],
                "topics": ["authorization"],
                "authority_tier": "official",
                "claim_tier": "answer_pack_approved",
                "source_id": "rock_official",
                "payload": {"rock_versions": ["19.1"], "content_hash": "source-hash"},
            },
            {
                "id": "model_map:stable:group",
                "kind": "model_map",
                "title": "Group Model Map",
                "body": "Group properties and relationships.",
                "path": "knowledge/model-map/models/group.md",
                "concept": "model-map",
                "concepts": ["model-map"],
                "authority_tier": "source-code-confirmed",
                "claim_tier": "source_backed",
                "source_id": "rock_model_map",
                "payload": {},
            },
        ]
    )

    claim = next(row for row in documents if row["kind"] == "claim")
    model = next(row for row in documents if row["kind"] == "model_map")
    assert claim["schema"] == "rock-kb-retrieval-document-v1"
    assert "Concepts: security-permissions, api-integrations" in claim["text"]
    assert claim["rock_versions"] == ["19.1"]
    assert claim["source_content_hash"] == "source-hash"
    assert len(claim["content_hash"]) == 64
    assert claim["index_policy"] == "hybrid_primary"
    assert set(claim["metadata"]) == {"kind", "namespace", "authority_rank", "claim_tier_rank", "concepts"}
    assert model["index_policy"] == "exact_lexical_only"


def test_retrieval_projection_diff_queues_source_and_policy_changes():
    previous = [
        {"id": "claim:a", "content_hash": "old", "source_content_hash": "source-old", "index_policy": "hybrid_primary"},
        {"id": "claim:removed", "content_hash": "same", "source_content_hash": "same", "index_policy": "hybrid_primary"},
    ]
    current = [
        {"id": "claim:a", "content_hash": "new", "source_content_hash": "source-new", "index_policy": "semantic_secondary"},
        {"id": "claim:new", "content_hash": "new", "source_content_hash": "new", "index_policy": "hybrid_primary", "needs_review": True},
    ]

    report = retrieval_projection_diff(previous, current)

    assert report["counts"]["new"] == 1
    assert report["counts"]["removed"] == 1
    assert report["changed_source_ids"] == ["claim:a"]
    assert report["changed_policy_ids"] == ["claim:a"]
    assert report["review_required_ids"] == ["claim:a", "claim:new"]


def test_build_service_projection_writes_d1_seed_and_artifacts(tmp_path):
    projection = build_service_projection(destination=tmp_path / "dist")

    sql = projection.sql_path.read_text(encoding="utf-8")
    assert projection.artifact_count > 100
    assert projection.search_row_count > 100
    assert "CREATE VIRTUAL TABLE search_rows_fts" in sql
    assert "CREATE TABLE search_row_concepts" in sql
    assert "CREATE TABLE search_row_aliases" in sql
    assert "'artifact_prefix'" in sql
    assert "'rock_issue_catalog_content_hash'" in sql
    assert "'rock_issue_record_count'" in sql
    assert "'rock_issue_source_content_hashes'" in sql
    assert f"'versions/{projection.version}'" in sql
    assert projection.retrieval_document_count == projection.search_row_count
    assert (projection.dist / "retrieval-documents.jsonl").exists()
    assert (projection.dist / "retrieval-change-report.json").exists()
    assert (projection.dist / "artifacts" / "agent" / "rock-kb-manifest.json").exists()
    canonical_skill = projection.dist / "artifacts" / "skills" / "rock-kb-agent" / "SKILL.md"
    legacy_skill = projection.dist / "artifacts" / "docs" / "templates" / "rock-kb-agent" / "SKILL.md"
    skill_manifest = json.loads((projection.dist / "artifacts" / "skills" / "rock-kb-agent" / "manifest.json").read_text(encoding="utf-8"))
    assert canonical_skill.read_text(encoding="utf-8") == legacy_skill.read_text(encoding="utf-8")
    assert skill_manifest["source_path"] == "skills/rock-kb-agent/SKILL.md"
    assert skill_manifest["skill_version"] == "1.2.1"
    shard_files = sorted((projection.dist / "artifact-shards").glob("*.json"))
    assert len(shard_files) == 16**service_projection.ARTIFACT_SHARD_PREFIX_LENGTH
    shard_payload = json.loads(shard_files[0].read_text(encoding="utf-8"))
    assert shard_payload["schema"] == "rock-kb-artifact-shard-v1"
    assert isinstance(shard_payload["artifacts"], dict)
    assert (projection.dist / "org-registry.json").exists()
    payload = json.loads((projection.dist / "projection.json").read_text(encoding="utf-8"))
    assert payload["version"] == projection.version


def test_build_service_projection_version_ignores_generated_timestamp(monkeypatch, tmp_path):
    generated_values = iter(["2026-06-12T00:00:00Z", "2026-06-12T01:00:00Z"])
    monkeypatch.setattr(
        service_projection,
        "public_export_manifest",
        lambda: {"schema": "test-manifest", "generated_at": next(generated_values), "files": [{"path": "agent/test.json"}]},
    )
    monkeypatch.setattr(service_projection, "public_export_text_for_public_path", lambda path: "{}\n")
    monkeypatch.setattr(service_projection, "build_search_rows", lambda: [])
    monkeypatch.setattr(service_projection, "load_org_registry", lambda: [])

    first = build_service_projection(destination=tmp_path / "first")
    second = build_service_projection(destination=tmp_path / "second")

    assert first.version == second.version


def test_build_d1_seed_sql_bounds_large_search_bodies():
    sql = build_d1_seed_sql(
        version="abc123",
        generated_at="2026-06-12T00:00:00Z",
        search_rows=[
            {
                "id": "concept:large",
                "kind": "concept",
                "title": "Large Concept",
                "body": "a" * 120_000,
                "path": "knowledge/concepts/large/index.md",
                "url": "",
                "concept": "large",
                "authority_tier": "official",
                "claim_tier": "source_backed",
                "source_id": "",
                "payload": {},
            }
        ],
        org_rows=[],
    )

    assert max_sql_statement_length(sql) < 100_000
    assert "Search body truncated" in sql


def test_build_d1_seed_sql_switches_artifact_prefix_after_projection_rows():
    sql = build_d1_seed_sql(
        version="abc123",
        generated_at="2026-06-12T00:00:00Z",
        search_rows=[],
        org_rows=[],
        artifact_prefix="slots/b",
    )

    assert "DROP TABLE IF EXISTS kb_meta" not in sql
    assert "('artifact_prefix', 'slots/b') ON CONFLICT(key)" in sql
    assert sql.rfind("'artifact_prefix'") > sql.rfind("CREATE TABLE rock_issue_enrichments")


def test_build_d1_seed_sql_records_issue_projection_content_hashes():
    catalog_hash = "a" * 64
    core_hash = service_projection.sha256_text(f"rock_core_issues:{catalog_hash}:7")
    mobile_hash = service_projection.sha256_text(f"rock_mobile_issues:{catalog_hash}:3")
    sql = build_d1_seed_sql(
        version="abc123",
        generated_at="2026-07-21T00:00:00Z",
        search_rows=[],
        org_rows=[],
        rock_issue_summary={
            "record_count": 10,
            "catalog_content_hash": catalog_hash,
            "repositories": {
                "SparkDevNetwork/Rock": 7,
                "SparkDevNetwork/Rock.Mobile-Issues": 3,
            },
        },
    )

    assert f"'rock_issue_catalog_content_hash', '{catalog_hash}'" in sql
    assert "'rock_issue_record_count', '10'" in sql
    assert core_hash in sql
    assert mobile_hash in sql


def test_build_d1_seed_sql_projects_canonical_related_content_edges(monkeypatch, tmp_path):
    agent_dir = tmp_path / "agent"
    agent_dir.mkdir()
    relationship = {
        "relationship_id": "rock_idea_relationship:fixture",
        "source_id": "rock_idea:2250",
        "target_id": "rock_issue:SparkDevNetwork/Rock#6919",
        "target_url": "https://github.com/SparkDevNetwork/Rock/issues/6919",
        "target_kind": "rock_issue",
        "relationship_type": "references_issue",
        "authority_tier": "community-unreviewed",
        "confidence": "high",
        "review_state": "source_observed",
    }
    (agent_dir / "rock-idea-relationships.jsonl").write_text(json.dumps(relationship) + "\n", encoding="utf-8")
    monkeypatch.setattr(service_projection, "REPO_ROOT", tmp_path)

    sql = build_d1_seed_sql("v1", "2026-07-17T00:00:00Z", [], [])

    assert "CREATE TABLE related_content_edges" in sql
    assert "rock_idea_relationship:fixture" in sql
    assert "rock_issue:SparkDevNetwork/Rock#6919" in sql


def test_rock_idea_search_rows_attach_verification_context(monkeypatch, tmp_path):
    agent_dir = tmp_path / "agent"
    agent_dir.mkdir()
    idea = {
        "idea_id": "rock_idea:2250",
        "number": 2250,
        "title": "Add days to event duration",
        "url": "https://community.rockrms.com/ideas/2250/add-days-to-event-duration",
        "category": "Event",
        "status": "complete",
        "status_label": "Complete",
        "concept_ids": ["event-registration"],
    }
    verification = {
        "schema": "rock-kb-rock-idea-verification-queue-v1",
        "idea_id": idea["idea_id"],
        "verification_state": "candidate_review_pending",
        "recommended_action": "corroborate_completed_state",
        "review_input_hash": "review-input-hash",
        "content_hash": "verification-content-hash",
        "claim_tier": "routing_context_only",
        "needs_live_verification": True,
    }
    (agent_dir / "rock-ideas.jsonl").write_text(json.dumps(idea) + "\n", encoding="utf-8")
    (agent_dir / "rock-idea-relationships.jsonl").write_text("", encoding="utf-8")
    (agent_dir / "rock-idea-verification-queue.jsonl").write_text(
        json.dumps(verification) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(service_projection, "REPO_ROOT", tmp_path)

    rows = service_projection.rock_idea_search_rows()

    assert len(rows) == 1
    assert rows[0]["payload"]["verification"] == verification
    assert "candidate_review_pending" in rows[0]["body"]
    assert "corroborate_completed_state" in rows[0]["body"]


def read_jsonl_for_test(relative_path: str):
    path = Path(__file__).resolve().parents[1] / relative_path
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_apply_projection_uploads_artifacts_before_remote_d1_seed(monkeypatch, tmp_path):
    dist = tmp_path / "dist"
    shards = dist / "artifact-shards"
    shard = shards / "ab.json"
    shard.parent.mkdir(parents=True)
    shard.write_text('{"schema":"rock-kb-artifact-shard-v1","shard":"ab","artifacts":{}}\n', encoding="utf-8")
    projection = service_projection.ServiceProjection(
        version="abc123",
        generated_at="2026-06-12T00:00:00Z",
        artifact_count=1,
        search_row_count=1,
        retrieval_document_count=1,
        org_count=1,
        dist=dist,
        sql_path=dist / "d1-seed.sql",
        artifact_prefix="slots/a",
    )
    projection.sql_path.write_text("SELECT 1;\n", encoding="utf-8")
    commands: list[list[str]] = []
    monkeypatch.setattr(service_projection, "run", lambda command, cwd: commands.append(command))
    monkeypatch.setattr(service_projection, "run_with_retries", lambda command, cwd: commands.append(command))

    service_projection.apply_projection_to_cloudflare(projection, env="production", bucket="bucket", database="database")

    assert commands[0][:5] == ["npx", "wrangler", "r2", "object", "put"]
    assert commands[0][5] == "bucket/slots/a/artifact-shards/ab.json"
    assert "--remote" in commands[0]
    assert commands[1] == ["npx", "wrangler", "deploy", "--env", "production"]
    assert commands[2][:5] == ["npx", "wrangler", "d1", "execute", "database"]
    assert "--remote" in commands[2]
    assert "--yes" in commands[2]


def test_select_deploy_artifact_prefix_uses_inactive_slot_and_legacy_migration(monkeypatch):
    monkeypatch.setattr(service_projection, "request_json", lambda url: {"status": "ok", "version": "old"})
    assert service_projection.select_deploy_artifact_prefix(base_url="https://kb.test") == "slots/a"

    monkeypatch.setattr(
        service_projection,
        "request_json",
        lambda url: {"status": "ok", "version": "current", "artifact_prefix": "slots/a"},
    )
    assert service_projection.select_deploy_artifact_prefix(base_url="https://kb.test") == "slots/b"
    assert service_projection.select_deploy_artifact_prefix(base_url="", override="slots/a") == "slots/a"


def test_select_deploy_artifact_prefix_fails_closed_for_unknown_or_missing_state(monkeypatch):
    monkeypatch.setattr(
        service_projection,
        "request_json",
        lambda url: {"status": "ok", "artifact_prefix": "unexpected/current"},
    )
    with pytest.raises(RuntimeError, match="Unsupported active artifact prefix"):
        service_projection.select_deploy_artifact_prefix(base_url="https://kb.test")
    with pytest.raises(RuntimeError, match="ROCK_KB_BASE_URL"):
        service_projection.select_deploy_artifact_prefix(base_url="")


def test_configure_bounded_artifact_retention_preserves_other_rules(monkeypatch):
    calls = []
    multipart_rule = {
        "id": "abort-multipart",
        "enabled": True,
        "conditions": {},
        "abortMultipartUploadsTransition": {"condition": {"type": "Age", "maxAge": 604800}},
    }

    def fake_request(url, *, method="GET", headers=None, payload=None):
        calls.append((url, method, payload))
        if url.endswith("/health"):
            return {"status": "ok", "artifact_prefix": "slots/b"}
        if method == "GET":
            return {"result": {"rules": [multipart_rule]}}
        return {"success": True, "result": None}

    monkeypatch.setattr(service_projection, "request_json", fake_request)
    report = service_projection.configure_bounded_artifact_retention(
        base_url="https://kb.test",
        bucket="bucket",
        apply=True,
        account_id="account",
        api_token="token",
    )

    assert report["status"] == "updated"
    put_payload = calls[-1][2]
    assert put_payload["rules"][0] == multipart_rule
    assert put_payload["rules"][1] == service_projection.legacy_artifact_retention_rule()
    assert put_payload["rules"][1]["conditions"] == {"prefix": "versions/"}


def test_configure_bounded_artifact_retention_is_idempotent(monkeypatch):
    target = service_projection.legacy_artifact_retention_rule()
    calls = []

    def fake_request(url, *, method="GET", headers=None, payload=None):
        calls.append((url, method, payload))
        if url.endswith("/health"):
            return {"status": "ok", "artifact_prefix": "slots/a"}
        return {"result": {"rules": [target]}}

    monkeypatch.setattr(service_projection, "request_json", fake_request)
    report = service_projection.configure_bounded_artifact_retention(
        base_url="https://kb.test",
        apply=True,
        account_id="account",
        api_token="token",
    )

    assert report["status"] == "unchanged"
    assert all(method == "GET" for _, method, _ in calls)


def test_request_json_uses_named_json_client_headers(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def read(self):
            return b'{"status":"ok"}'

    def fake_urlopen(request, timeout):
        captured["headers"] = {key.lower(): value for key, value in request.header_items()}
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(service_projection.urllib_request, "urlopen", fake_urlopen)

    result = service_projection.request_json("https://kb.test/health")

    assert result == {"status": "ok"}
    assert captured["headers"]["accept"] == "application/json"
    assert captured["headers"]["user-agent"] == "rock-kb-deployer/1.0"
    assert captured["timeout"] == 30


def max_sql_statement_length(sql: str) -> int:
    statements: list[str] = []
    in_string = False
    start = 0
    index = 0
    while index < len(sql):
        char = sql[index]
        if char == "'":
            if in_string and index + 1 < len(sql) and sql[index + 1] == "'":
                index += 2
                continue
            in_string = not in_string
        elif char == ";" and not in_string:
            statements.append(sql[start : index + 1])
            start = index + 1
        index += 1
    return max(len(statement) for statement in statements)


def test_configure_service_bindings_updates_top_level_and_environment():
    update_bindings = load_update_bindings()
    data = {
        "d1_databases": [{"binding": "KB_DB", "database_name": "old", "database_id": "old-id"}],
        "r2_buckets": [{"binding": "KB_ARTIFACTS", "bucket_name": "old-bucket"}],
        "env": {
            "production": {
                "d1_databases": [{"binding": "KB_DB", "database_name": "old", "database_id": "old-id"}],
                "r2_buckets": [{"binding": "KB_ARTIFACTS", "bucket_name": "old-bucket"}],
            }
        },
    }

    update_bindings(data, "rock-agent-kb", "real-id", "real-bucket")
    update_bindings(data["env"]["production"], "rock-agent-kb", "real-id", "real-bucket")

    assert data["d1_databases"][0]["database_id"] == "real-id"
    assert data["env"]["production"]["d1_databases"][0]["database_id"] == "real-id"
    assert data["r2_buckets"][0]["bucket_name"] == "real-bucket"
