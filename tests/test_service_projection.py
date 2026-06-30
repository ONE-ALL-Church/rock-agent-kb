from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from rock_kb import service_projection
from rock_kb.service_projection import build_d1_seed_sql, build_search_rows, build_service_projection


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
    row = next(row for row in rows if row["id"] == "community_contribution:test-org:workflow-pattern:workflows")

    assert row["kind"] == "community_contribution"
    assert row["authority_tier"] == "community-unreviewed"
    assert row["claim_tier"] == "routing_context_only"
    assert row["payload"]["claim"] == row["body"]
    assert row["payload"]["concept_ids"] == ["workflows"]


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

    assert {row["concept"] for row in rows} == {"lava", "check-in"}
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


def test_build_service_projection_writes_d1_seed_and_artifacts(tmp_path):
    projection = build_service_projection(destination=tmp_path / "dist")

    sql = projection.sql_path.read_text(encoding="utf-8")
    assert projection.artifact_count > 100
    assert projection.search_row_count > 100
    assert "CREATE VIRTUAL TABLE search_rows_fts" in sql
    assert (projection.dist / "artifacts" / "agent" / "rock-kb-manifest.json").exists()
    shard_files = sorted((projection.dist / "artifact-shards").glob("*.json"))
    assert shard_files
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
        org_count=1,
        dist=dist,
        sql_path=dist / "d1-seed.sql",
    )
    projection.sql_path.write_text("SELECT 1;\n", encoding="utf-8")
    commands: list[list[str]] = []
    monkeypatch.setattr(service_projection, "run", lambda command, cwd: commands.append(command))
    monkeypatch.setattr(service_projection, "run_with_retries", lambda command, cwd: commands.append(command))

    service_projection.apply_projection_to_cloudflare(projection, env="production", bucket="bucket", database="database")

    assert commands[0][:5] == ["npx", "wrangler", "r2", "object", "put"]
    assert commands[0][5] == "bucket/versions/abc123/artifact-shards/ab.json"
    assert "--remote" in commands[0]
    assert commands[1][:5] == ["npx", "wrangler", "d1", "execute", "database"]
    assert "--remote" in commands[1]
    assert "--yes" in commands[1]
    assert commands[2] == ["npx", "wrangler", "deploy", "--env", "production"]


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
