import rock_kb.readiness as readiness_module
from rock_kb.readiness import concept_artifacts_check, goal_readiness_report, readiness_status, readiness_summary


def test_readiness_status_fails_on_failed_check():
    checks = [{"status": "pass"}, {"status": "warn"}, {"status": "fail"}]

    assert readiness_status(checks) == "fail"


def test_readiness_status_is_incomplete_on_warning_only():
    checks = [{"status": "pass"}, {"status": "warn"}]

    assert readiness_status(checks) == "incomplete"


def test_readiness_summary_counts_statuses():
    checks = [{"status": "pass"}, {"status": "warn"}, {"status": "warn"}, {"status": "fail"}]

    assert readiness_summary(checks) == {"pass": 1, "warn": 2, "fail": 1}


def test_concept_artifacts_reports_quality_debt_as_warning(tmp_path, monkeypatch):
    concept_dir = tmp_path / "concepts" / "test-concept"
    concept_dir.mkdir(parents=True)
    for filename in readiness_module.REQUIRED_AGENT_ENTRYPOINT_FILES:
        (concept_dir / filename).write_text("", encoding="utf-8")
    (concept_dir / "guide-quality.json").write_text(
        '{"score": 90, "status": "fail"}',
        encoding="utf-8",
    )
    concept = type("Concept", (), {"id": "test-concept"})()
    monkeypatch.setattr(readiness_module, "KNOWLEDGE_DIR", tmp_path)
    monkeypatch.setattr(readiness_module, "load_concepts", lambda: [concept])

    result = concept_artifacts_check()

    assert result["status"] == "warn"
    assert result["evidence"]["artifact_error_count"] == 0
    assert result["evidence"]["quality_debt_count"] == 1


def test_concept_artifacts_still_fails_when_entrypoint_is_missing(tmp_path, monkeypatch):
    concept_dir = tmp_path / "concepts" / "test-concept"
    concept_dir.mkdir(parents=True)
    (concept_dir / "guide-quality.json").write_text(
        '{"score": 100, "status": "pass"}',
        encoding="utf-8",
    )
    concept = type("Concept", (), {"id": "test-concept"})()
    monkeypatch.setattr(readiness_module, "KNOWLEDGE_DIR", tmp_path)
    monkeypatch.setattr(readiness_module, "load_concepts", lambda: [concept])

    result = concept_artifacts_check()

    assert result["status"] == "fail"
    assert result["evidence"]["artifact_error_count"] > 0


def test_public_readiness_scope_skips_private_media_check(monkeypatch):
    def passing_check(check_id):
        return {"id": check_id, "status": "pass", "message": "ok", "evidence": {}}

    monkeypatch.setattr(readiness_module, "source_registry_check", lambda: passing_check("source_registry"))
    monkeypatch.setattr(readiness_module, "claim_graph_check", lambda: passing_check("claim_graph"))
    monkeypatch.setattr(readiness_module, "normalized_corpus_check", lambda: passing_check("normalized_corpus"))
    monkeypatch.setattr(readiness_module, "public_policy_check", lambda: passing_check("public_policy"))
    monkeypatch.setattr(readiness_module, "public_export_check", lambda: passing_check("public_export"))
    monkeypatch.setattr(readiness_module, "agent_manifest_check", lambda: passing_check("agent_manifest"))
    monkeypatch.setattr(readiness_module, "concept_artifacts_check", lambda: passing_check("concept_artifacts"))
    monkeypatch.setattr(readiness_module, "concept_staleness_check", lambda: passing_check("concept_staleness"))
    monkeypatch.setattr(readiness_module, "guide_refresh_plan_check", lambda: passing_check("guide_refresh_plan"))
    monkeypatch.setattr(readiness_module, "lava_capability_reference_check", lambda: passing_check("lava_capability_reference"))
    monkeypatch.setattr(readiness_module, "mobile_selector_audit_check", lambda: passing_check("mobile_selector_audit"))
    monkeypatch.setattr(readiness_module, "rebuild_metadata_check", lambda: passing_check("rebuild_metadata"))
    monkeypatch.setattr(readiness_module, "private_media_check", lambda: {"id": "private_media", "status": "fail", "message": "missing", "evidence": {}})
    monkeypatch.setattr(readiness_module, "private_public_boundary_check", lambda: passing_check("private_public_boundary"))
    monkeypatch.setattr(readiness_module, "private_processing_artifacts_available", lambda: True)

    report = goal_readiness_report(include_private=False)

    assert report["scope"] == "public"
    assert report["status"] == "pass"
    assert "private_media" not in {check["id"] for check in report["checks"]}


def test_full_readiness_uses_public_scope_when_private_corpus_absent(monkeypatch):
    def passing_check(check_id):
        return {"id": check_id, "status": "pass", "message": "ok", "evidence": {}}

    monkeypatch.setattr(readiness_module, "source_registry_check", lambda: passing_check("source_registry"))
    monkeypatch.setattr(readiness_module, "claim_graph_check", lambda: passing_check("claim_graph"))
    monkeypatch.setattr(readiness_module, "public_policy_check", lambda: passing_check("public_policy"))
    monkeypatch.setattr(readiness_module, "public_export_check", lambda: passing_check("public_export"))
    monkeypatch.setattr(readiness_module, "agent_manifest_check", lambda: passing_check("agent_manifest"))
    monkeypatch.setattr(readiness_module, "concept_artifacts_check", lambda: passing_check("concept_artifacts"))
    monkeypatch.setattr(readiness_module, "lava_capability_reference_check", lambda: passing_check("lava_capability_reference"))
    monkeypatch.setattr(readiness_module, "rebuild_metadata_check", lambda: passing_check("rebuild_metadata"))
    monkeypatch.setattr(readiness_module, "private_public_boundary_check", lambda: passing_check("private_public_boundary"))
    monkeypatch.setattr(readiness_module, "private_processing_artifacts_available", lambda: False)

    report = goal_readiness_report(include_private=True)

    assert report["scope"] == "public"
    assert report["status"] == "pass"
    assert "private_corpus" in {check["id"] for check in report["checks"]}
    assert "private_media" not in {check["id"] for check in report["checks"]}
