import json
from pathlib import Path

import pytest
import yaml

from rock_kb import source_orchestration as so
from rock_kb.source_hashing import source_content_hash


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"


def workflow_text(name: str) -> str:
    return (WORKFLOW_DIR / name).read_text(encoding="utf-8")


def workflow_steps(name: str) -> list[dict]:
    return yaml.load(workflow_text(name), Loader=yaml.BaseLoader)["jobs"]["refresh"]["steps"]


def embedded_python(name: str, step_name: str) -> str:
    step = next(step for step in workflow_steps(name) if step.get("name") == step_name)
    lines = step["run"].splitlines()
    start = next(index for index, line in enumerate(lines) if "<<'PY'" in line) + 1
    end = next(index for index in range(start, len(lines)) if lines[index] == "PY")
    return "\n".join(lines[start:end]) + "\n"


def execute_embedded(name: str, step_name: str) -> None:
    exec(compile(embedded_python(name, step_name), f"{name}:{step_name}", "exec"), {"__name__": "__main__"})


def scan_report(state: str) -> dict:
    def snapshot(content_hash):
        return {
            "schema": so.SOURCE_SNAPSHOT_SCHEMA,
            "generated_at": "2026-10-14T00:00:00Z",
            "sources": {"rock_documentation": {"status": "ok"}},
            "source_records": {
                "record:1": {"id": "record:1", "source_id": "rock_documentation",
                             "content_hash": content_hash, "source_url": "https://example.test/record-1"},
            },
            "claims": {},
            "media_items": {},
        }

    current = snapshot("new" if state == "changed" else "same")
    previous = None if state == "unavailable" else snapshot("same")
    diff = so.diff_source_snapshots(previous, current)
    return {"comparison": diff["comparison"], "summary": so.scan_summary(current, diff, {})}


@pytest.fixture
def workflow_workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    output = tmp_path / "github-output.txt"
    summary = tmp_path / "github-summary.md"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    (tmp_path / "data/review/source-scan").mkdir(parents=True)
    return tmp_path, output, summary


def write_scan(root: Path, report: dict) -> None:
    (root / "data/review/source-scan/source-scan-report.json").write_text(json.dumps(report), encoding="utf-8")


def read_outputs(path: Path) -> dict[str, str]:
    return dict(line.split("=", 1) for line in path.read_text(encoding="utf-8").splitlines())


@pytest.mark.parametrize("state", ["identical", "changed", "unavailable"])
def test_actual_weekly_classifier_requires_available_comparison(workflow_workspace, capsys, state):
    root, output, summary = workflow_workspace
    write_scan(root, scan_report(state))

    if state == "unavailable":
        with pytest.raises(SystemExit, match="review blocked: comparison unavailable"):
            execute_embedded("refresh.yml", "Classify refresh scope")
        values = read_outputs(output)
        assert values["comparison_status"] == "comparison_unavailable"
        assert values["comparison_reason"] == "baseline_missing"
        assert values["review_blocked"] == "true"
        assert values["source_change_count"] == "unavailable"
        assert values["has_source_changes"] == "unavailable"
        assert "Source Refresh Review Blocked" in summary.read_text(encoding="utf-8")
        assert "source_change_count=0" not in capsys.readouterr().out
    else:
        execute_embedded("refresh.yml", "Classify refresh scope")
        values = read_outputs(output)
        assert values["comparison_status"] == "available"
        assert values["review_blocked"] == "false"
        assert values["source_change_count"] == ("1" if state == "changed" else "0")
        assert values["has_source_changes"] == ("true" if state == "changed" else "false")
        assert values["has_private_media"] == "false"


@pytest.mark.parametrize("bad_count", [None, -1, "0", False])
def test_actual_weekly_classifier_rejects_invalid_available_counts(workflow_workspace, bad_count):
    root, output, summary = workflow_workspace
    report = scan_report("identical")
    report["summary"]["new_source_records"] = bad_count
    write_scan(root, report)

    with pytest.raises(SystemExit, match="invalid_comparison_counts"):
        execute_embedded("refresh.yml", "Classify refresh scope")

    values = read_outputs(output)
    assert values["review_blocked"] == "true"
    assert values["source_change_count"] == "unavailable"
    assert values["has_source_changes"] != "false"


def test_actual_weekly_classifier_rejects_legacy_report_without_comparison_status(workflow_workspace):
    root, output, summary = workflow_workspace
    report = scan_report("identical")
    report["summary"].pop("comparison_status")
    write_scan(root, report)

    with pytest.raises(SystemExit, match="comparison unavailable"):
        execute_embedded("refresh.yml", "Classify refresh scope")

    assert read_outputs(output)["review_blocked"] == "true"


def test_weekly_rebuild_and_pr_paths_require_available_comparison():
    steps = {step.get("name"): step for step in workflow_steps("refresh.yml")}
    for name in (
        "Run deterministic rebuild path",
        "Skip deterministic rebuild without private media",
        "Create refresh pull request",
        "Skip refresh pull request without source changes",
    ):
        assert "steps.refresh_scope.outputs.comparison_status == 'available'" in steps[name]["if"]
    assert "steps.refresh_scope.outputs.has_source_changes == 'false'" in steps["Skip refresh pull request without source changes"]["if"]


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
def test_pre_refresh_bootstrap_scan_remains_baseline_free(name):
    step = next(step for step in workflow_steps(name) if step.get("name") == "Capture pre-refresh source snapshot")
    assert "kb sources scan" in step["run"]
    assert "--snapshot-output data/review/source-scan-pre/source-snapshot.json" in step["run"]
    assert "--baseline-snapshot" not in step["run"]
    assert "if" not in step


@pytest.mark.parametrize("state", ["identical", "changed", "unavailable"])
def test_actual_daily_summary_displays_comparison_availability(workflow_workspace, capsys, state):
    root, output, summary = workflow_workspace
    write_scan(root, scan_report(state))
    path = root / "data/review/source-freshness/source-freshness-report.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"status": "ok", "blocking_source_ids": []}), encoding="utf-8")

    execute_embedded("refresh-daily.yml", "Summarize daily refresh")

    text = capsys.readouterr().out
    assert "`None`" not in text
    if state == "unavailable":
        assert "Comparison: `comparison_unavailable` (baseline_missing)" in text
        assert "Review: `blocked`" in text
        assert "Changed records: `unavailable`" in text
        assert "New records: `unavailable`" in text
        assert "Removed records: `unavailable`" in text
    else:
        assert "Comparison: `available` (ok)" in text
        assert f"Changed records: `{'1' if state == 'changed' else '0'}`" in text


def test_actual_weekly_pr_body_displays_unavailable_counts(workflow_workspace):
    root, output, summary = workflow_workspace
    write_scan(root, scan_report("unavailable"))
    (root / "data/review/rebuild-plan").mkdir()

    execute_embedded("refresh.yml", "Build status and dry-run plan")

    body = (root / "data/review/rebuild-plan/pull-request-body.md").read_text(encoding="utf-8")
    assert "Comparison: `comparison_unavailable` (baseline_missing)" in body
    assert "Changed source records: `unavailable`" in body
    assert "New source records: `unavailable`" in body
    assert "Removed source records: `unavailable`" in body
    assert len(body.splitlines()) > 5


def test_required_pull_request_checks_run_when_draft_becomes_ready() -> None:
    for name in ("public-surface.yml", "validate-contributions.yml"):
        text = workflow_text(name)
        event_section = text.split("on:", 1)[1].split("permissions:", 1)[0]

        assert "workflow_dispatch:" in event_section
        assert "pull_request:" in event_section
        assert "ready_for_review" in event_section
        assert "github.event.pull_request.draft == false" in text


def test_automated_refreshes_use_draft_ready_review_gate() -> None:
    for name in ("refresh-rock-issues.yml", "refresh.yml"):
        text = workflow_text(name)
        permissions = text.split("permissions:", 1)[1].split("concurrency:", 1)[0]

        assert "actions: write" not in permissions
        assert "draft: always-true" in text
        assert "automated-refresh-pr-review.md" in text
        assert "Dispatch required pull request checks" not in text
        assert "gh workflow run public-surface.yml" not in text
        assert "gh workflow run validate-contributions.yml" not in text


def baseline_path(name: str) -> Path:
    workflow = yaml.load(workflow_text(name), Loader=yaml.BaseLoader)
    return Path(workflow["jobs"]["refresh"]["env"]["SOURCE_BASELINE_PATH"])


def checked_snapshot(content_hash="same"):
    return {
        "schema": so.SOURCE_SNAPSHOT_SCHEMA,
        "generated_at": "2026-10-15T00:00:00Z",
        "sources": {"rock_documentation": {"source_id": "rock_documentation", "status": "ok", "record_count": 1}},
        "source_records": {"record:1": {"id": "record:1", "source_id": "rock_documentation",
                                       "content_hash": content_hash, "source_url": "https://example.test/record-1"}},
        "claims": {}, "media_items": {},
    }


def write_checked_candidate(root, snapshot, freshness_status="ok"):
    (root / "data/review/source-scan/source-snapshot.json").write_text(json.dumps(snapshot))
    path = root / "data/review/source-freshness/source-freshness-report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": "rock-kb-source-freshness-report-v1", "status": freshness_status}))


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
@pytest.mark.parametrize("second_hash,changed", [("same", 0), ("changed", 1)])
def test_actual_baseline_bootstrap_then_restored_comparison(workflow_workspace, monkeypatch, capsys, name, second_hash, changed):
    root, output, summary = workflow_workspace
    path = baseline_path(name)
    monkeypatch.setenv("SOURCE_BASELINE_PATH", str(path))
    monkeypatch.setenv("SOURCE_FETCH_OUTCOME", "success")
    monkeypatch.setenv("STRICT_FRESHNESS_OUTCOME", "success")
    execute_embedded(name, "Validate restored source baseline")
    assert read_outputs(output)["available"] == "false"
    assert read_outputs(output)["initial_review_required"] == "true"
    current = checked_snapshot()
    diff = so.diff_source_snapshots(None, current)
    first = {"comparison": diff["comparison"], "summary": so.scan_summary(current, diff, {})}
    write_scan(root, first)
    assert first["summary"]["changed_source_records"] is None
    write_checked_candidate(root, current)
    execute_embedded(name, "Prepare validated source baseline")
    cached = json.loads(path.read_text())
    assert cached["initial_review_required"] is True
    if name == "refresh.yml":
        with pytest.raises(SystemExit, match="comparison unavailable"):
            execute_embedded(name, "Classify refresh scope")
        assert path.exists(), "Bootstrap must cache before classification blocks"
    # The next clean checkout restores only the compact cache, not normalized data.
    output.write_text("")
    (root / "data/review/source-scan/source-snapshot.json").unlink()
    execute_embedded(name, "Validate restored source baseline")
    assert read_outputs(output)["available"] == "true"
    assert read_outputs(output)["initial_review_required"] == "true"
    previous, comparison = so.load_source_snapshot_baseline(path)
    current = checked_snapshot(second_hash)
    diff = so.diff_source_snapshots(previous, current, comparison=comparison)
    second = {"comparison": diff["comparison"], "summary": so.scan_summary(current, diff, {})}
    assert second["summary"]["comparison_status"] == "available"
    assert second["summary"]["changed_source_records"] == changed
    write_scan(root, second)
    write_checked_candidate(root, current)
    execute_embedded(name, "Prepare validated source baseline")
    assert json.loads(path.read_text())["initial_review_required"] is True
    monkeypatch.setenv("INITIAL_REVIEW_REQUIRED", "true")
    if name == "refresh.yml":
        execute_embedded(name, "Classify refresh scope")
        assert read_outputs(output)["initial_review_required"] == "true"
        assert "Initial Public Projection Review Required" in summary.read_text()
    else:
        execute_embedded(name, "Summarize daily refresh")
        assert "Initial review: `required`" in capsys.readouterr().out


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
def test_actual_malformed_cache_recovers_without_approving_initial_review(workflow_workspace, monkeypatch, name):
    root, output, summary = workflow_workspace
    path = baseline_path(name)
    path.parent.mkdir(parents=True)
    path.write_text("{malformed")
    monkeypatch.setenv("SOURCE_BASELINE_PATH", str(path))
    monkeypatch.setenv("SOURCE_FETCH_OUTCOME", "success")
    monkeypatch.setenv("STRICT_FRESHNESS_OUTCOME", "success")
    execute_embedded(name, "Validate restored source baseline")
    assert read_outputs(output)["available"] == "false"
    write_checked_candidate(root, checked_snapshot())
    execute_embedded(name, "Prepare validated source baseline")
    payload, comparison = so.load_source_snapshot_baseline(path)
    assert comparison["status"] == "available"
    assert payload["initial_review_required"] is True


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
@pytest.mark.parametrize("fetch,freshness,status", [
    ("failure", "success", "ok"), ("success", "failure", "ok"),
    ("cancelled", "success", "ok"), ("success", "skipped", "ok"),
    ("success", "success", "fail"),
])
def test_actual_failed_checks_cannot_advance_baseline(workflow_workspace, monkeypatch, name, fetch, freshness, status):
    root, output, summary = workflow_workspace
    path = baseline_path(name)
    path.parent.mkdir(parents=True)
    old = json.dumps({**checked_snapshot("old"), "initial_review_required": True})
    path.write_text(old)
    monkeypatch.setenv("SOURCE_BASELINE_PATH", str(path))
    monkeypatch.setenv("SOURCE_FETCH_OUTCOME", fetch)
    monkeypatch.setenv("STRICT_FRESHNESS_OUTCOME", freshness)
    write_checked_candidate(root, checked_snapshot("new"), status)
    with pytest.raises(SystemExit, match="Cannot advance baseline"):
        execute_embedded(name, "Prepare validated source baseline")
    assert path.read_text() == old


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
def test_actual_baseline_cache_is_compact_public_metadata_and_nonempty(workflow_workspace, monkeypatch, name):
    root, output, summary = workflow_workspace
    path = baseline_path(name)
    monkeypatch.setenv("SOURCE_BASELINE_PATH", str(path))
    monkeypatch.setenv("SOURCE_FETCH_OUTCOME", "success")
    monkeypatch.setenv("STRICT_FRESHNESS_OUTCOME", "success")
    candidate = checked_snapshot()
    candidate["raw_source"] = "DO_NOT_CACHE"
    candidate["source_records"]["record:1"]["text"] = "DO_NOT_CACHE"
    candidate["media_items"] = {"private:1": {"transcript": "DO_NOT_CACHE"}}
    candidate["sources"]["private"] = {"private_storage": True}
    candidate["source_records"]["private:1"] = {"id": "private:1", "source_id": "private", "content_hash": "private"}
    write_checked_candidate(root, candidate)
    execute_embedded(name, "Prepare validated source baseline")
    cached = json.loads(path.read_text())
    assert "DO_NOT_CACHE" not in path.read_text()
    assert "private:1" not in cached["source_records"]
    assert cached["media_items"] == {}
    old = path.read_text()
    candidate["source_records"] = {}
    write_checked_candidate(root, candidate)
    with pytest.raises(SystemExit, match="invalid or empty baseline"):
        execute_embedded(name, "Prepare validated source baseline")
    assert path.read_text() == old


def test_baseline_cache_paths_prefixes_guards_and_command_wiring():
    caches = []
    for name in ("refresh.yml", "refresh-daily.yml"):
        steps = workflow_steps(name)
        by_name = {step.get("name"): step for step in steps}
        restore = by_name["Restore compact source baseline"]
        save = by_name["Save compact source baseline"]
        assert restore["uses"] == "actions/cache/restore@v6"
        assert save["uses"] == "actions/cache/save@v6"
        assert restore["with"]["path"] == save["with"]["path"] == str(baseline_path(name))
        assert restore["with"]["key"] == save["with"]["key"]
        assert "github.run_attempt" in save["with"]["key"]
        for step_name in ("Prepare validated source baseline", "Save compact source baseline"):
            condition = by_name[step_name]["if"]
            assert "steps.refresh_sources.outcome == 'success'" in condition
            assert "steps.source_freshness.outcome == 'success'" in condition
        assert "steps.prepare_source_baseline.outcome == 'success'" in save["if"]
        if name == "refresh.yml":
            assert steps.index(save) < steps.index(by_name["Classify refresh scope"])
        for step in steps:
            run = step.get("run", "")
            if any(command in run for command in ("kb sources refresh", "kb sources freshness", "kb sources scan")) and step.get("name") != "Capture pre-refresh source snapshot":
                assert '"${baseline_args[@]}"' in run
                assert 'baseline_args=(--baseline-snapshot "$SOURCE_BASELINE_PATH")' in run
                assert "source-scan-pre/source-snapshot.json" not in run
        caches.append(restore["with"])
    assert caches[0]["path"] != caches[1]["path"]
    assert caches[0]["restore-keys"] != caches[1]["restore-keys"]


@pytest.mark.parametrize("name", ["refresh.yml", "refresh-daily.yml"])
def test_actual_cache_preserves_source_freshness_hashes(workflow_workspace, monkeypatch, name):
    root, output, summary = workflow_workspace
    path = baseline_path(name)
    monkeypatch.setenv("SOURCE_BASELINE_PATH", str(path))
    monkeypatch.setenv("SOURCE_FETCH_OUTCOME", "success")
    monkeypatch.setenv("STRICT_FRESHNESS_OUTCOME", "success")
    candidate = checked_snapshot()
    candidate["sources"]["rock_core_release_notes"] = {"source_id": "rock_core_release_notes", "status": "ok", "record_count": 1}
    candidate["source_records"] = {
        "release:19.0": so.compact_source_record({
            "id": "release:19.0", "source_id": "rock_core_release_notes",
            "source_kind": "rock_release_notes", "source_title": "Rock 19.0 Release Notes",
            "source_url": "https://example.test/releases/19.0", "content_hash": "a" * 64,
            "retrieved_at": "2026-10-15T00:00:00Z", "topics": ["releases"],
            "rock_versions": ["19.0"], "release_family": "core", "version": "19.0",
        }),
        "documentation:check-in": so.compact_source_record({
            "id": "documentation:check-in", "source_id": "rock_documentation",
            "source_kind": "documentation", "source_title": "Check-In Configuration",
            "source_url": "https://example.test/documentation/check-in", "content_hash": "b" * 64,
            "retrieved_at": "2026-10-15T00:00:00Z", "topics": ["check-in"],
            "rock_versions": ["19.0"], "summary": "Public documentation summary.",
        }),
    }
    write_checked_candidate(root, candidate)
    execute_embedded(name, "Prepare validated source baseline")
    cached = json.loads(path.read_text())
    for source_id in ("rock_core_release_notes", "rock_documentation"):
        assert source_content_hash(cached, source_id) == source_content_hash(candidate, source_id)
    for record_id, record in candidate["source_records"].items():
        assert cached["source_records"][record_id]["source_title"] == record["source_title"]
        assert cached["source_records"][record_id]["retrieved_at"] == record["retrieved_at"]
    assert cached["initial_review_required"] is True
