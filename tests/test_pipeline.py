from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from rock_kb import cli as cli_module
from rock_kb.cli import _legacy as legacy_cli
from rock_kb.pipeline import Stage
from rock_kb.pipeline.build import run_build
from rock_kb.pipeline.status import build_status_report
from rock_kb.pipeline.state import (
    changed_input_paths,
    load_state,
    save_state,
    stage_status,
    update_stage_state,
)
from rock_kb.pipeline.stages import topological_stages


def touch(path: Path, text: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_stage_is_fresh_after_state_update(tmp_path):
    stage = Stage(
        name="one",
        description="one",
        inputs=["inputs/*.txt"],
        outputs=["outputs/result.txt"],
        run=lambda: None,
    )
    touch(tmp_path / "inputs/a.txt", "a")
    touch(tmp_path / "outputs/result.txt", "ok")

    state = update_stage_state(stage, {}, repo_root=tmp_path, completed_at="2026-06-11T00:00:00Z")

    assert stage_status(stage, state, repo_root=tmp_path) == "fresh"


def test_stage_is_stale_after_input_changes(tmp_path):
    stage = Stage(
        name="one",
        description="one",
        inputs=["inputs/*.txt"],
        outputs=["outputs/result.txt"],
        run=lambda: None,
    )
    input_path = touch(tmp_path / "inputs/a.txt", "a")
    touch(tmp_path / "outputs/result.txt", "ok")
    state = update_stage_state(stage, {}, repo_root=tmp_path)

    input_path.write_text("b", encoding="utf-8")

    assert stage_status(stage, state, repo_root=tmp_path) == "stale"
    assert changed_input_paths(stage, state, repo_root=tmp_path) == ["inputs/a.txt"]


def test_downstream_is_stale_when_upstream_is_stale(tmp_path):
    stage = Stage(
        name="two",
        description="two",
        inputs=["inputs/two.txt"],
        outputs=["outputs/two.txt"],
        run=lambda: None,
        depends_on=["one"],
    )
    touch(tmp_path / "inputs/two.txt")
    touch(tmp_path / "outputs/two.txt")
    state = update_stage_state(stage, {}, repo_root=tmp_path)

    assert stage_status(stage, state, repo_root=tmp_path, upstream_statuses={"one": "stale"}) == "stale"


def test_missing_outputs_are_detected(tmp_path):
    stage = Stage(
        name="one",
        description="one",
        inputs=["inputs/*.txt"],
        outputs=["outputs/result.txt"],
        run=lambda: None,
    )
    touch(tmp_path / "inputs/a.txt", "a")
    state = update_stage_state(stage, {}, repo_root=tmp_path)

    assert stage_status(stage, state, repo_root=tmp_path) == "missing-outputs"


def test_hash_is_stable_across_unchanged_runs(tmp_path):
    stage = Stage(
        name="one",
        description="one",
        inputs=["inputs/*.txt"],
        outputs=["outputs/result.txt"],
        run=lambda: None,
    )
    touch(tmp_path / "inputs/b.txt", "b")
    touch(tmp_path / "inputs/a.txt", "a")
    touch(tmp_path / "outputs/result.txt", "ok")

    first = update_stage_state(stage, {}, repo_root=tmp_path)
    second = update_stage_state(stage, {}, repo_root=tmp_path)

    assert first["one"]["input_hash"] == second["one"]["input_hash"]


def test_state_round_trips(tmp_path):
    state_path = tmp_path / "state.json"
    state = {"one": {"input_hash": "abc", "completed_at": "2026-06-11T00:00:00Z"}}

    save_state(state, state_path)

    assert load_state(state_path) == state


def test_manual_stage_status(tmp_path):
    stage = Stage(
        name="manual",
        description="manual",
        inputs=[],
        outputs=[],
        run=lambda: None,
        manual=True,
    )

    assert stage_status(stage, {}, repo_root=tmp_path) == "manual"


def test_topological_stages_orders_dependencies():
    one = Stage(name="one", description="one", inputs=[], outputs=[], run=lambda: None)
    two = Stage(name="two", description="two", inputs=[], outputs=[], run=lambda: None, depends_on=["one"])

    assert [stage.name for stage in topological_stages([two, one])] == ["one", "two"]


def test_status_report_suggests_stale_stage_command(tmp_path):
    stage = Stage(
        name="one",
        description="one",
        inputs=["inputs/*.txt"],
        outputs=["outputs/result.txt"],
        run=lambda: None,
    )
    touch(tmp_path / "inputs/a.txt", "a")
    touch(tmp_path / "outputs/result.txt", "ok")

    report = build_status_report(stages=[stage], repo_root=tmp_path, include_queues=False)

    assert report["pipeline"][0]["status"] == "stale"
    assert report["suggested_commands"] == [
        {"stage": "one", "reason": "stale", "command": "uv run kb build --stage one"}
    ]


def test_status_command_renders_pipeline_table(monkeypatch):
    monkeypatch.setattr(
        legacy_cli,
        "build_status_report",
        lambda: {
            "pipeline": [{"name": "one", "status": "stale", "changed_inputs": ["inputs/a.txt"]}],
            "queues": {
                "media_review": {"pending_candidate_count": 2},
                "claim_review_queue": {"rows": 3},
                "guide_refresh": {"needs_generated_index_rebuild": ["check-in"], "needs_long_form_guide_refresh": []},
                "concept_staleness": {"stale": []},
                "mobile_selector_audit": {"status": "fresh"},
            },
            "suggested_commands": [
                {"stage": "one", "reason": "stale", "command": "uv run kb build --stage one"}
            ],
        },
    )

    result = CliRunner().invoke(cli_module.app, ["status"])

    assert result.exit_code == 0
    assert "Pipeline Status" in result.output
    assert "uv run kb build --stage one" in result.output


def test_build_dry_run_orders_stale_stages(tmp_path):
    one = Stage(name="one", description="one", inputs=["inputs/one.txt"], outputs=["outputs/one.txt"], run=lambda: None)
    two = Stage(
        name="two",
        description="two",
        inputs=["inputs/two.txt"],
        outputs=["outputs/two.txt"],
        run=lambda: None,
        depends_on=["one"],
    )
    touch(tmp_path / "inputs/one.txt")
    touch(tmp_path / "inputs/two.txt")
    touch(tmp_path / "outputs/one.txt")
    touch(tmp_path / "outputs/two.txt")

    result = run_build(dry_run=True, stages=[two, one], repo_root=tmp_path, state_path=tmp_path / "state.json")

    assert [action["stage"] for action in result["actions"] if action["action"] == "run"] == ["one", "two"]
    assert result["ran"] == []


def test_build_updates_state_after_run(tmp_path):
    output = tmp_path / "outputs/one.txt"

    def run_one():
        touch(output, "ok")
        return {"ok": True}

    one = Stage(name="one", description="one", inputs=["inputs/one.txt"], outputs=["outputs/one.txt"], run=run_one)
    touch(tmp_path / "inputs/one.txt")
    state_path = tmp_path / "state.json"

    result = run_build(stages=[one], repo_root=tmp_path, state_path=state_path)

    assert result["ran"][0]["stage"] == "one"
    assert load_state(state_path)["one"]["input_hash"]


def test_build_reuses_public_artifacts_when_private_inputs_absent(tmp_path):
    runs = []

    def run_private():
        runs.append("private")

    private_stage = Stage(
        name="private-stage",
        description="private",
        inputs=["data/review/*.jsonl"],
        outputs=["claims/approved-claims.jsonl"],
        run=run_private,
        private=True,
    )
    public_stage = Stage(
        name="public-stage",
        description="public",
        inputs=["claims/approved-claims.jsonl"],
        outputs=["data/public-export/public-export-manifest.json"],
        run=lambda: touch(tmp_path / "data/public-export/public-export-manifest.json", "{}"),
        depends_on=["private-stage"],
    )
    touch(tmp_path / "claims/approved-claims.jsonl", "{}")
    state_path = tmp_path / "state.json"

    result = run_build(stages=[public_stage, private_stage], repo_root=tmp_path, state_path=state_path)

    assert runs == []
    assert result["actions"][0]["action"] == "reuse-public-artifacts"
    assert result["ran"][0]["stage"] == "public-stage"


def test_build_manual_gate_blocks_downstream(tmp_path):
    manual = Stage(name="manual", description="manual", inputs=[], outputs=[], run=lambda: None, manual=True)
    downstream = Stage(
        name="downstream",
        description="downstream",
        inputs=[],
        outputs=[],
        run=lambda: None,
        depends_on=["manual"],
    )

    result = run_build(stage_name="downstream", stages=[downstream, manual], repo_root=tmp_path, state_path=tmp_path / "state.json")

    assert result["blocked"]["stage"] == "manual"
    assert [action["stage"] for action in result["actions"]] == ["manual"]


def test_build_force_reruns_fresh_stage(tmp_path):
    runs = []

    def run_one():
        runs.append("one")

    one = Stage(name="one", description="one", inputs=["inputs/one.txt"], outputs=["outputs/one.txt"], run=run_one)
    touch(tmp_path / "inputs/one.txt")
    touch(tmp_path / "outputs/one.txt")
    state_path = tmp_path / "state.json"
    state = update_stage_state(one, {}, repo_root=tmp_path)
    save_state(state, state_path)

    result = run_build(stage_name="one", force=True, stages=[one], repo_root=tmp_path, state_path=state_path)

    assert runs == ["one"]
    assert result["actions"][0]["action"] == "run"
