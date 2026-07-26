from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import stat
import warnings
import zipfile
from pathlib import Path

import pytest

VALID_FIXTURE = Path("tests/fixtures/contributions/valid-bundle.jsonl")


@pytest.fixture(autouse=True)
def isolate_rock_kb_client_state(monkeypatch, tmp_path):
    monkeypatch.setenv("ROCK_KB_STATE_DIR", str(tmp_path / "rock-kb-state"))


def skill_source(version: str = "1.0.0") -> str:
    return (
        "---\n"
        "name: rock-kb-agent\n"
        "description: Test Rock KB skill.\n"
        "metadata:\n"
        f"  rock-kb-skill-version: \"{version}\"\n"
        "---\n\n"
        "# Rock KB Agent\n"
    )


def skill_manifest(source: str, version: str = "1.0.0") -> dict:
    return {
        "schema": "rock-kb-skill-manifest-v1",
        "name": "rock-kb-agent",
        "skill_version": version,
        "published_at": "2026-07-17T00:00:00Z",
        "source_repository": "https://github.com/ONE-ALL-Church/rock-agent-kb",
        "source_url": "https://example.test/artifacts/skills/rock-kb-agent/SKILL.md",
        "source_path": "skills/rock-kb-agent/SKILL.md",
        "legacy_source_path": "docs/templates/rock-kb-agent/SKILL.md",
        "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "minimum_client_version": "0.13.0",
        "restart_required": True,
        "update_check_interval_hours": 24,
        "default_update_policy": "notify",
        "supported_agents": ["codex", "claude", "cursor", "opencode"],
    }


def mock_skill_service(monkeypatch, cli, source: str | None = None) -> str:
    source = source or skill_source()
    manifest = skill_manifest(source)

    def get_json(url: str):
        if not url.endswith("/skill/manifest.json"):
            return {"status": "ok", "version": "test"}
        response = dict(manifest)
        service_url = url.removesuffix("/skill/manifest.json")
        response["source_url"] = f"{service_url}/artifacts/skills/rock-kb-agent/SKILL.md"
        return response

    monkeypatch.setattr(cli, "get_json", get_json)
    monkeypatch.setattr(cli, "get_text", lambda url: source)
    monkeypatch.setattr(cli, "package_version", lambda: "0.13.0")
    return source


def load_client_validator():
    path = Path("clients/python/src/rock_kb_client/validator.py")
    spec = importlib.util.spec_from_file_location("client_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_client_cli():
    source_root = str(Path("clients/python/src").resolve())
    if source_root not in sys.path:
        sys.path.insert(0, source_root)
    import rock_kb_client.cli as cli

    return cli


def test_client_validator_accepts_valid_fixture():
    validator = load_client_validator()

    assert validator.validate_bundle(VALID_FIXTURE) == []


def test_client_validator_rejects_private_path(tmp_path):
    validator = load_client_validator()
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    row["source_urls"] = ["data/review/private-source.md"]
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")

    errors = validator.validate_bundle(bundle)

    assert any("private path reference" in error for error in errors)


def test_client_validator_rejects_duplicate_contribution_ids(tmp_path):
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")

    errors = load_client_validator().validate_bundle(bundle)

    assert any("duplicate contribution_id fixture-org:workflow-troubleshooting" in error for error in errors)


def test_client_dashboard_command_hits_operations_dashboard(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-operations-dashboard-v2"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main(["--url", "https://example.test", "dashboard"])

    assert exit_code == 0
    assert urls == ["https://example.test/operations/dashboard"]
    assert "rock-kb-operations-dashboard-v2" in capsys.readouterr().out


def test_client_freshness_command_hits_hosted_source_operations(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-source-operations-v1", "status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "freshness"]) == 0
    assert urls == ["https://example.test/operations/freshness"]
    assert "rock-kb-source-operations-v1" in capsys.readouterr().out


def test_client_test_round_exercises_search_recipes_and_imported_issues(monkeypatch, capsys):
    cli = load_client_cli()

    def fake_get_json(url: str):
        if url.endswith("/health"):
            return {"status": "ok", "version": "projection-v1", "artifact_prefix": "slots/a"}
        if "/model-map/models/group" in url:
            return {
                "status": "ok",
                "model": {
                    "identity": {"model_slug": "group", "rock_version": "19.2.0"},
                    "relationships": [{"property_name": "Members"}],
                },
            }
        if "Check-In%20Label%20Designer" in url:
            return {"results": [{"id": "lava_context:check-in-label:personattendance:1", "kind": "lava_context", "authority_tier": "source-code-confirmed"}]}
        if "/recipes/" in url:
            return {"status": "ok", "recipe": {"authority_tier": "community-reviewed", "needs_live_verification": True, "implementation": {"commit_sha": "a" * 40}}}
        if "child%20eligible" in url:
            return {"results": [{"id": "answer:check-in:first-checks", "concepts": ["check-in"], "authority_tier": "official"}]}
        if url.endswith("/rock-ideas/1307"):
            return {
                "status": "ok",
                "idea": {
                    "idea_id": "rock_idea:1307",
                    "authority_tier": "community-unreviewed",
                    "needs_live_verification": True,
                    "verification": {"verification_state": "references_available"},
                },
                "relationships": [
                    {"relationship_type": "about", "target_id": "concept:communications"},
                    {"relationship_type": "about_model", "target_id": "model_map:stable:phone-number"},
                    {"relationship_type": "references_issue", "target_id": "rock_issue:SparkDevNetwork/Rock#2935"},
                ],
            }
        if url.endswith("/rock-issues/6920"):
            return {
                "status": "ok",
                "issue_id": "rock_issue:SparkDevNetwork/Rock#6920",
                "issue": {"authority_tier": "community-unreviewed", "reviewed_enrichments": [{"claim_tier": "source_backed"}]},
            }
        if url.endswith("/rock-issues/mobile%3A116"):
            return {
                "status": "ok",
                "issue_id": "rock_issue:SparkDevNetwork/Rock.Mobile-Issues#116",
                "issue": {
                    "state": "closed",
                    "evidence_state": "fixed_release_recorded",
                    "needs_live_verification": True,
                    "version_evidence": [{"relationship": "fixed", "authority_tier": "official", "normalized_version": "19.2"}],
                },
            }
        if "qzvwx9417" in url:
            return {"results": []}
        raise AssertionError(url)

    def fake_post_json(url: str, payload: dict, token: str = ""):
        assert url.endswith("/rock-issues/assess")
        assert payload["profile"]["core_version"] == "19.1.8"
        return {
            "caveat": "Verify locally.",
            "results": [{"issue_id": "rock_issue:SparkDevNetwork/Rock#6920", "applicability": "possible", "needs_live_verification": True}],
        }

    monkeypatch.setattr(cli, "get_json", fake_get_json)
    monkeypatch.setattr(cli, "post_json", fake_post_json)

    exit_code = cli.main(["--url", "https://example.test", "test-round"])
    report = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert report["status"] == "ok"
    assert report["case_count"] == 10
    assert report["rock_idea_case_count"] == 1
    assert report["imported_issue_case_count"] == 3
    assert report["manual_review_required"] is True
    assert report["projection_version"] == "projection-v1"
    assert all(row["status"] == "pass" for row in report["cases"])


def test_client_test_round_submits_complete_bounded_review(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    from rock_kb_client.cohort_test import CASE_DEFINITIONS

    cases = [
        {
            "case_id": case_id,
            "category": category,
            "status": "pass",
            "manual_review_prompt": "Review this bounded case.",
            "result_ids": [] if category in {"service", "no_answer"} else ["claim:claim:abc123"],
        }
        for case_id, category in CASE_DEFINITIONS
    ]
    report = {
        "schema": "rock-kb-community-test-round-v1",
        "projection_version": "projection-v1",
        "status": "ok",
        "cases": cases,
    }
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps({"outcomes": {case_id: "useful" for case_id, _ in CASE_DEFINITIONS}}), encoding="utf-8")
    calls = []

    monkeypatch.setattr(cli, "run_cohort_test", lambda **_kwargs: report)
    monkeypatch.setattr(
        cli,
        "post_json",
        lambda url, payload, token="": calls.append((url, payload)) or {"status": "recorded", "case_count": 10},
    )

    exit_code = cli.main(
        [
            "--url",
            "https://example.test",
            "--cohort",
            "external-test",
            "test-round",
            "--review-file",
            str(review_path),
            "--submit",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert calls[0][0] == "https://example.test/test-rounds/review"
    assert calls[0][1]["schema"] == "rock-kb-community-test-round-review-v1"
    assert len(calls[0][1]["cases"]) == 10
    assert all(set(row) == {"case_id", "category", "automatic_status", "outcome", "result_id"} for row in calls[0][1]["cases"])
    assert payload["submission"]["status"] == "recorded"


def test_client_test_round_returns_failure_when_submission_is_rejected(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    from rock_kb_client.cohort_test import CASE_DEFINITIONS

    report = {
        "schema": "rock-kb-community-test-round-v1",
        "projection_version": "projection-v1",
        "status": "ok",
        "cases": [
            {
                "case_id": case_id,
                "category": category,
                "status": "pass",
                "manual_review_prompt": "Review this bounded case.",
                "result_ids": [] if category in {"service", "no_answer"} else ["claim:claim:abc123"],
            }
            for case_id, category in CASE_DEFINITIONS
        ],
    }
    review_path = tmp_path / "review.json"
    review_path.write_text(
        json.dumps({"outcomes": {case_id: "useful" for case_id, _ in CASE_DEFINITIONS}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "run_cohort_test", lambda **_kwargs: report)
    monkeypatch.setattr(
        cli,
        "post_json",
        lambda *_args, **_kwargs: {"status": "rejected", "error_code": "invalid_result_id"},
    )

    exit_code = cli.main(
        [
            "--url",
            "https://example.test",
            "--cohort",
            "external-test",
            "test-round",
            "--review-file",
            str(review_path),
            "--submit",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert payload["submission"]["status"] == "rejected"
    assert payload["submission"]["error_code"] == "invalid_result_id"


def test_client_test_round_rejects_ordinary_community_cohort(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(cli, "passive_skill_checks", lambda **_kwargs: [])
    review_path = tmp_path / "review.json"
    review_path.write_text('{"outcomes":{}}\n', encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        cli.main([
            "--cohort", "community",
            "test-round",
            "--review-file", str(review_path),
            "--submit",
        ])

    assert exc.value.code == 2
    assert "requires --cohort external-test or --cohort maintainer" in capsys.readouterr().err


def test_client_feedback_posts_structured_result_feedback(monkeypatch, capsys):
    cli = load_client_cli()
    calls = []

    def fake_post(url, payload, token=""):
        calls.append((url, payload, token))
        return {"schema": "rock-kb-feedback-result-v1", "status": "recorded"}

    monkeypatch.setattr(cli, "post_json", fake_post)

    exit_code = cli.main(
        [
            "--url",
            "https://example.test",
            "feedback",
            "claim:example",
            "--rating",
            "-1",
            "--reason",
            "outdated",
        ]
    )

    assert exit_code == 0
    assert calls == [
        (
            "https://example.test/feedback",
            {"result_id": "claim:example", "rating": -1, "reason": "outdated"},
            "",
        )
    ]
    assert "recorded" in capsys.readouterr().out


def test_client_report_issue_posts_only_structured_attested_fields(monkeypatch, capsys):
    cli = load_client_cli()
    calls = []

    def fake_post(url, payload, token=""):
        calls.append((url, payload, token))
        return {"schema": "rock-kb-issue-report-result-v1", "status": "pending_review", "report_id": "kbir_example"}

    monkeypatch.setattr(cli, "post_json", fake_post)

    exit_code = cli.main(
        [
            "--url",
            "https://example.test",
            "report-issue",
            "--failure-type",
            "retrieval",
            "--operation",
            "search",
            "--error-code",
            "search_unavailable",
            "--description",
            "Search returned a temporary service failure.",
            "--result-id",
            "claim:example",
            "--http-status",
            "503",
            "--redaction-attested",
        ]
    )

    assert exit_code == 0
    assert calls == [
        (
            "https://example.test/issues/report",
            {
                "failure_type": "retrieval",
                "operation": "search",
                "error_code": "search_unavailable",
                "description": "Search returned a temporary service failure.",
                "redaction_attested": True,
                "result_id": "claim:example",
                "http_status": 503,
            },
            "",
        )
    ]
    assert "kbir_example" in capsys.readouterr().out


def test_client_search_uses_compact_results_by_default(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-search-result-v2", "results": []}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "search", "check in labels"]) == 0
    assert urls == ["https://example.test/search?q=check%20in%20labels&limit=10&min_tier=routing_context_only&detail=compact"]
    assert "rock-kb-search-result-v2" in capsys.readouterr().out


def test_client_exact_result_and_claim_commands(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "result", "claim:claim:abc:check-in"]) == 0
    assert cli.main(["--url", "https://example.test", "claim", "claim:abc"]) == 0
    assert urls == [
        "https://example.test/results/claim%3Aclaim%3Aabc%3Acheck-in",
        "https://example.test/claims/id/claim%3Aabc",
    ]
    capsys.readouterr()


def test_client_model_command_hits_exact_model_endpoint(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-model-map-model-result-v1", "status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main([
        "--url",
        "https://example.test",
        "model",
        "Group",
        "--fields",
        "identity,required,diffs",
        "--property",
        "Members",
    ])

    assert exit_code == 0
    assert urls == ["https://example.test/model-map/models/Group?fields=identity%2Crequired%2Cdiffs&property=Members&format=json"]
    assert "rock-kb-model-map-model-result-v1" in capsys.readouterr().out


def test_client_model_map_list_command_hits_model_list_endpoint(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-model-map-model-list-v1", "count": 0, "models": []}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main(["--url", "https://example.test", "model-map", "list"])

    assert exit_code == 0
    assert urls == ["https://example.test/model-map/models"]
    assert "rock-kb-model-map-model-list-v1" in capsys.readouterr().out


def test_client_lava_context_commands_hit_exact_endpoints(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-lava-context-surface-result-v1", "status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(
        [
            "--url",
            "https://example.test",
            "lava-context",
            "list",
            "--family",
            "check-in-label",
            "--surface-type",
            "label_dynamic_text",
        ]
    ) == 0
    assert cli.main(
        [
            "--url",
            "https://example.test",
            "lava-context",
            "get",
            "check-in-label-checkout-dynamic-text",
            "--root",
            "CheckoutDateTime",
        ]
    ) == 0
    assert urls == [
        "https://example.test/lava-contexts?family=check-in-label&surface_type=label_dynamic_text",
        "https://example.test/lava-contexts/check-in-label-checkout-dynamic-text?root=CheckoutDateTime",
    ]
    assert "rock-kb-lava-context-surface-result-v1" in capsys.readouterr().out


def test_client_okf_commands_are_read_only(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    archive = tmp_path / "bundle.zip"
    archive.write_bytes(b"fixture")
    calls = []

    monkeypatch.setattr(
        cli,
        "download_okf",
        lambda **kwargs: calls.append(("download", kwargs)) or {"schema": "rock-kb-okf-download-v1", "status": "ok"},
    )
    monkeypatch.setattr(
        cli,
        "inspect_okf",
        lambda path: calls.append(("inspect", path)) or {"schema": "rock-kb-okf-inspection-v1", "status": "ok"},
    )
    monkeypatch.setattr(
        cli,
        "verify_okf",
        lambda path: calls.append(("verify", path)) or {"schema": "rock-kb-okf-validation-v1", "status": "ok"},
    )
    monkeypatch.setattr(
        cli,
        "conform_okf",
        lambda path: calls.append(("conformance", path)) or {"schema": "rock-kb-okf-conformance-v1", "status": "ok"},
    )

    assert cli.main(["okf", "download", "--version", "0.7.0", "--profile", "core", "--format", "tar.gz", "--destination", str(archive), "--force"]) == 0
    assert cli.main(["okf", "inspect", str(archive)]) == 0
    assert cli.main(["okf", "conformance", str(archive)]) == 0
    assert cli.main(["okf", "verify", str(archive)]) == 0
    assert cli.main(["okf", "validate", str(archive)]) == 0
    assert calls[0][0] == "download"
    assert calls[0][1]["version"] == "0.7.0"
    assert calls[0][1]["profile"] == "core"
    assert calls[0][1]["archive_format"] == "tar.gz"
    assert calls[1:] == [
        ("inspect", archive),
        ("conformance", archive),
        ("verify", archive),
        ("verify", archive),
    ]
    assert "rock-kb-okf-validation-v1" in capsys.readouterr().out


def test_client_okf_verifier_accepts_directory_and_archive(tmp_path):
    load_client_cli()
    from rock_kb_client.okf import verify_okf

    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "index.md").write_text("---\nokf_version: '0.1'\n---\n\n# Fixture\n\n[Claim](claims/example.md)\n", encoding="utf-8")
    (bundle / "log.md").write_text("# Log\n\n## 2026-07-13\n\n* **Creation**: Fixture.\n", encoding="utf-8")
    (bundle / "claims").mkdir()
    (bundle / "claims" / "example.md").write_text("---\ntype: Claim\nid: claim:example\ncanonical_id: claim:example\ntitle: Example\nstructured_record: /records/claim/example.json\n---\n\n# Example\n", encoding="utf-8")
    (bundle / "records" / "claim").mkdir(parents=True)
    (bundle / "records" / "claim" / "example.json").write_text(
        '{"schema":"rock-kb-okf-structured-record-v1","kind":"claim","canonical_id":"claim:example"}\n',
        encoding="utf-8",
    )
    (bundle / "profile.md").write_text("---\ntype: Reference\ntitle: Profile\n---\n\n# Profile\n", encoding="utf-8")
    (bundle / "LICENSE.txt").write_text("MIT\n", encoding="utf-8")
    (bundle / "NOTICE.txt").write_text("Notice\n", encoding="utf-8")
    (bundle / "relationships.jsonl").write_text("", encoding="utf-8")
    (bundle / "file-manifest.jsonl").write_text("", encoding="utf-8")
    manifest = {
        "schema": "rock-kb-okf-distribution-v1",
        "okf_version": "0.1",
        "okf_spec_commit": "ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a",
        "okf_profile": "rock-kb-okf-profile-v1",
        "profile": "core",
        "distribution_version": "test",
        "read_only": True,
        "license": {"code": "MIT", "original_content": "CC-BY-4.0", "notice": "NOTICE.txt"},
        "relationships": 0,
        "file_manifest_sha256": hashlib.sha256(b"").hexdigest(),
        "markdown_files": 4,
    }
    (bundle / "okf-manifest.json").write_text(json.dumps(manifest) + "\n", encoding="utf-8")
    checksum_targets = sorted(
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file() and path.name != "checksums.sha256"
    )
    (bundle / "checksums.sha256").write_text(
        "".join(
            f"{hashlib.sha256((bundle / relative).read_bytes()).hexdigest()}  {relative}\n"
            for relative in checksum_targets
        ),
        encoding="utf-8",
    )

    assert verify_okf(bundle)["status"] == "ok"

    archive_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for path in bundle.rglob("*"):
            if path.is_file():
                archive.write(path, f"rock-agent-kb-okf-vtest/{path.relative_to(bundle).as_posix()}")
    assert verify_okf(archive_path)["status"] == "ok"


def test_client_okf_generic_conformance_is_not_rock_distribution_verification(tmp_path):
    load_client_cli()
    from rock_kb_client.okf import conform_okf, verify_okf

    bundle = tmp_path / "generic"
    bundle.mkdir()
    (bundle / "knowledge.md").write_text(
        "---\ntype: Knowledge\ntitle: Generic\nokf_version: '9.9'\n---\n\n[Optional missing link](missing.md)\n",
        encoding="utf-8",
    )

    conformance = conform_okf(bundle)
    strict = verify_okf(bundle)

    assert conformance["status"] == "ok"
    assert any("unresolved link" in warning for warning in conformance["warnings"])
    assert any("unknown OKF version" in warning for warning in conformance["warnings"])
    assert strict["status"] == "failed"
    assert any("okf-manifest.json" in error for error in strict["errors"])


def test_client_okf_verifier_requires_complete_checksum_coverage(tmp_path):
    load_client_cli()
    from rock_kb_client.okf import validate_checksums

    files = {
        "index.md": b"# Index\n",
        "uncovered.txt": b"not covered\n",
    }
    files["checksums.sha256"] = (
        f"{hashlib.sha256(files['index.md']).hexdigest()}  index.md\n".encode()
    )

    assert "file missing checksum: uncovered.txt" in validate_checksums(files)


def test_client_okf_archive_limits_and_duplicate_paths(monkeypatch, tmp_path):
    load_client_cli()
    from rock_kb_client import okf

    duplicate = tmp_path / "duplicate.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(duplicate, "w") as archive:
            archive.writestr("root/index.md", "first")
            archive.writestr("root/index.md", "second")
    try:
        okf.read_bundle(duplicate)
    except ValueError as exc:
        assert "duplicate path" in str(exc)
    else:
        raise AssertionError("duplicate archive path was accepted")

    monkeypatch.setattr(okf, "MAX_FILE_BYTES", 8)
    oversized = tmp_path / "oversized.zip"
    with zipfile.ZipFile(oversized, "w") as archive:
        archive.writestr("root/index.md", "too many bytes")
    try:
        okf.read_bundle(oversized)
    except ValueError as exc:
        assert "exceeds" in str(exc)
    else:
        raise AssertionError("oversized archive entry was accepted")

    monkeypatch.setattr(okf, "MAX_ARCHIVE_ENTRIES", 1)
    too_many_entries = tmp_path / "too-many-entries.zip"
    with zipfile.ZipFile(too_many_entries, "w") as archive:
        archive.writestr("root/index.md", "index")
        archive.writestr("root/knowledge.md", "knowledge")
    try:
        okf.read_bundle(too_many_entries)
    except ValueError as exc:
        assert "maximum is 1" in str(exc)
    else:
        raise AssertionError("archive entry-count limit was not enforced")


def test_client_okf_download_selects_release_asset_and_verifies_checksum(monkeypatch, tmp_path):
    load_client_cli()
    from rock_kb_client import okf

    content = b"okf archive"
    expected = hashlib.sha256(content).hexdigest()
    monkeypatch.setattr(
        okf,
        "release_metadata",
        lambda version, user_agent: {
            "tag_name": "rock-kb-v0.7.0",
            "html_url": "https://example.test/release",
            "assets": [
                {
                    "name": "rock-agent-kb-okf-v0.7.0.zip",
                    "browser_download_url": "https://example.test/bundle.zip",
                },
                {
                    "name": "rock-agent-kb-okf-v0.7.0.sha256",
                    "browser_download_url": "https://example.test/bundle.sha256",
                },
            ],
        },
    )
    monkeypatch.setattr(okf, "download_url", lambda url, destination, user_agent: destination.write_bytes(content))
    monkeypatch.setattr(okf, "expected_asset_checksum", lambda assets, asset_name, user_agent: expected)
    destination = tmp_path / "download.zip"

    report = okf.download_okf(
        version="latest",
        archive_format="zip",
        destination=destination,
        force=False,
        user_agent="test",
    )

    assert destination.read_bytes() == content
    assert report["status"] == "ok"
    assert report["version"] == "0.7.0"
    assert report["checksum_verified"] is True
    assert report["sha256"] == expected


def test_client_okf_download_selects_exact_core_asset_and_github_digest(monkeypatch, tmp_path):
    load_client_cli()
    from rock_kb_client import okf

    content = b"core okf archive"
    expected = hashlib.sha256(content).hexdigest()
    selected_urls: list[str] = []
    monkeypatch.setattr(
        okf,
        "release_metadata",
        lambda version, user_agent: {
            "tag_name": "rock-kb-v0.7.0",
            "assets": [
                {
                    "name": "rock-agent-kb-okf-v0.7.0.zip",
                    "browser_download_url": "https://example.test/full.zip",
                    "digest": f"sha256:{hashlib.sha256(b'full').hexdigest()}",
                },
                {
                    "name": "rock-agent-kb-okf-core-v0.7.0.zip",
                    "browser_download_url": "https://example.test/core.zip",
                    "digest": f"sha256:{expected}",
                },
            ],
        },
    )

    def fake_download(url, destination, user_agent):
        selected_urls.append(url)
        destination.write_bytes(content)

    monkeypatch.setattr(okf, "download_url", fake_download)
    monkeypatch.setattr(okf, "expected_asset_checksum", lambda assets, asset_name, user_agent: "")

    report = okf.download_okf(
        version="latest",
        archive_format="zip",
        destination=tmp_path / "core.zip",
        force=False,
        user_agent="test",
        profile="core",
    )

    assert selected_urls == ["https://example.test/core.zip"]
    assert report["asset"] == "rock-agent-kb-okf-core-v0.7.0.zip"
    assert report["checksum_sources"] == ["github_asset_digest"]


def test_client_recipe_commands_hit_recipe_endpoints(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "recipe", "oneall:check-in-status-dashboard"]) == 0
    assert cli.main(["--url", "https://example.test", "recipes", "list", "--concept", "check-in"]) == 0
    assert cli.main(["--url", "https://example.test", "recipes", "search", "attendance roster"]) == 0
    assert urls == [
        "https://example.test/recipes/oneall%3Acheck-in-status-dashboard",
        "https://example.test/recipes?concept=check-in",
        "https://example.test/search?q=attendance%20roster&limit=10&min_tier=routing_context_only&kind=recipe&detail=compact",
    ]


def test_client_recipe_verify_uses_hosted_read_only_verifier(monkeypatch, capsys):
    cli = load_client_cli()
    urls = []

    def fake_get(url):
        urls.append(url)
        return {"schema": "rock-kb-recipe-verification-v1", "status": "pass"}

    monkeypatch.setattr(cli, "get_json", fake_get)

    assert cli.main(
        [
            "--url",
            "https://example.test",
            "recipe",
            "verify",
            "oneall:check-in-status-dashboard",
            "--rock-version",
            "18",
        ]
    ) == 0
    assert urls == [
        "https://example.test/recipes/oneall%3Acheck-in-status-dashboard/verify?rock_version=18"
    ]
    assert "rock-kb-recipe-verification-v1" in capsys.readouterr().out
    capsys.readouterr()


def test_client_rock_issue_commands_use_dedicated_read_only_endpoints(monkeypatch, tmp_path):
    cli = load_client_cli()
    gets: list[str] = []
    posts: list[tuple[str, dict]] = []
    profile = tmp_path / "profile.json"
    profile.write_text('{"core_version":"19.2.0","concepts":["hosting-infrastructure"]}\n')

    monkeypatch.setattr(cli, "get_json", lambda url: gets.append(url) or {"status": "ok"})
    monkeypatch.setattr(cli, "post_json", lambda url, payload, token="": posts.append((url, payload)) or {"status": "ok"})

    assert cli.main(["--url", "https://example.test", "issue", "mobile:128"]) == 0
    assert cli.main(["--url", "https://example.test", "issues", "search", "chat text issue", "--limit", "4"]) == 0
    assert cli.main(["--url", "https://example.test", "issues", "list", "--repository", "core", "--state", "open", "--version", "19.2"]) == 0
    assert cli.main(["--url", "https://example.test", "issues", "plan", "6919", "--include-private-instance"]) == 0
    assert cli.main(["--url", "https://example.test", "issues", "assess", str(profile), "--limit", "25"]) == 0

    assert gets == [
        "https://example.test/rock-issues/mobile%3A128",
        "https://example.test/rock-issues/search?q=chat%20text%20issue&limit=4",
        "https://example.test/rock-issues?limit=50&offset=0&repository=core&state=open&version=19.2",
        "https://example.test/rock-issues/6919/plan?include_private_instance=true",
    ]
    assert posts == [
        (
            "https://example.test/rock-issues/assess",
            {
                "profile": {"core_version": "19.2.0", "concepts": ["hosting-infrastructure"]},
                "scope": "open",
                "limit": 25,
            },
        )
    ]


def test_client_rock_idea_commands_use_dedicated_metadata_endpoints(monkeypatch):
    cli = load_client_cli()
    gets: list[str] = []
    monkeypatch.setattr(cli, "get_json", lambda url: gets.append(url) or {"status": "ok"})

    assert cli.main(["--url", "https://example.test", "idea", "2250"]) == 0
    assert cli.main(["--url", "https://example.test", "ideas", "search", "event duration feature request", "--limit", "4"]) == 0
    assert cli.main(
        [
            "--url",
            "https://example.test",
            "ideas",
            "list",
            "--status",
            "complete",
            "--category",
            "Event",
            "--concept",
            "event-registration",
            "--planned-version",
            "20.0",
        ]
    ) == 0

    assert gets == [
        "https://example.test/rock-ideas/2250",
        "https://example.test/rock-ideas/search?q=event%20duration%20feature%20request&limit=4",
        "https://example.test/rock-ideas?limit=50&offset=0&status=complete&category=Event&concept=event-registration&planned_version=20.0",
    ]


def test_client_issue_watch_collects_all_pages_and_detects_changes(tmp_path):
    from rock_kb_client.issue_watch import run_issue_watch

    state_path = tmp_path / "private" / "watch.json"
    profile = {"core_version": "19.2.0", "concepts": ["hosting-infrastructure"]}
    rows = [
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#1", "possible", "none_recorded"),
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#2", "likely", "candidate_fix"),
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#3", "confirmed", "official_fix_recorded"),
    ]

    first = run_issue_watch(
        profile=profile,
        service="https://example.test",
        fetch_page=assessment_page_fetcher(rows),
        state_path=state_path,
        page_size=2,
    )

    assert first["status"] == "initialized"
    assert first["total_count"] == 3
    assert [row["issue_id"] for row in first["results"]] == [row["issue_id"] for row in rows]
    assert stat.S_IMODE(state_path.stat().st_mode) == 0o600
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["schema"] == "rock-kb-issue-watch-state-v2"
    assert state["scope"] == "open"
    assert state["catalog"]["status"] == "current"
    assert "profile" not in state
    assert state["profile_sha256"] == first["profile_sha256"]

    changed = [
        issue_assessment_row(
            "rock_issue:SparkDevNetwork/Rock#1",
            "confirmed",
            "candidate_fix",
            revalidation=["enrichment:1"],
            risk_level="high",
        ),
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#3", "confirmed", "official_fix_recorded"),
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#4", "possible", "none_recorded"),
    ]
    second = run_issue_watch(
        profile=profile,
        service="https://example.test",
        fetch_page=assessment_page_fetcher(changed),
        state_path=state_path,
        page_size=2,
    )

    assert second["status"] == "updated"
    assert [row["issue_id"] for row in second["changes"]["newly_relevant"]] == ["rock_issue:SparkDevNetwork/Rock#4"]
    assert [row["issue_id"] for row in second["changes"]["no_longer_relevant"]] == ["rock_issue:SparkDevNetwork/Rock#2"]
    assert second["changes"]["applicability_changed"][0]["issue_id"].endswith("#1")
    assert second["changes"]["remediation_changed"][0]["issue_id"].endswith("#1")
    assert second["changes"]["risk_changed"][0]["issue_id"].endswith("#1")
    assert second["changes"]["revalidation_due"][0]["issue_id"].endswith("#1")
    assert second["changes"]["population_changed"] is None
    assert second["changes"]["catalog_changed"] is None


def test_client_issue_watch_does_not_replace_state_after_incomplete_page(tmp_path):
    from rock_kb_client.issue_watch import run_issue_watch

    state_path = tmp_path / "watch.json"
    profile = {"core_version": "19.2.0"}
    baseline = [issue_assessment_row("rock_issue:SparkDevNetwork/Rock#1", "possible", "none_recorded")]
    run_issue_watch(
        profile=profile,
        service="https://example.test",
        fetch_page=assessment_page_fetcher(baseline),
        state_path=state_path,
    )
    before = state_path.read_bytes()

    def incomplete(_payload):
        return {
            "schema": "rock-kb-rock-issue-assessment-v2",
            "projection_version": "test-v1",
            "scope": "open",
            "catalog": {"status": "current"},
            "count": 1,
            "total_count": 2,
            "evaluated_count": 2,
            "population_by_state": {"open": 2},
            "offset": 0,
            "limit": 500,
            "next_offset": None,
            "has_more": False,
            "counts": {"possible": 2},
            "exclusion_summary": {"count": 0, "by_basis": {}, "examples": [], "truncated": False},
            "results": baseline,
        }

    import pytest

    with pytest.raises(RuntimeError, match="complete result set"):
        run_issue_watch(
            profile=profile,
            service="https://example.test",
            fetch_page=incomplete,
            state_path=state_path,
        )
    assert state_path.read_bytes() == before


def test_client_issue_watch_state_isolated_by_assessment_scope(monkeypatch, tmp_path):
    from rock_kb_client.issue_watch import default_state_path

    monkeypatch.setenv("ROCK_KB_STATE_DIR", str(tmp_path))
    profile = {"core_version": "19.2.0"}

    assert default_state_path(profile, "https://example.test", "open") != default_state_path(
        profile,
        "https://example.test",
        "historical-unresolved",
    )


def test_client_issue_watch_reports_catalog_population_and_exclusion_changes(tmp_path):
    from rock_kb_client.issue_watch import run_issue_watch

    state_path = tmp_path / "watch.json"
    profile = {"core_version": "19.2.0"}
    rows = [issue_assessment_row("rock_issue:SparkDevNetwork/Rock#1", "possible", "none_recorded")]
    run_issue_watch(
        profile=profile,
        service="https://example.test",
        fetch_page=assessment_page_fetcher(rows),
        state_path=state_path,
    )

    changed = run_issue_watch(
        profile=profile,
        service="https://example.test",
        fetch_page=assessment_page_fetcher(
            rows,
            catalog_status="source_stale",
            exclusion_count=1,
            evaluated_count=2,
        ),
        state_path=state_path,
    )

    assert changed["status"] == "updated"
    assert changed["changes"]["catalog_changed"]["after"]["status"] == "source_stale"
    assert changed["changes"]["exclusion_summary_changed"]["after"]["count"] == 1
    assert changed["changes"]["population_changed"]["after"]["evaluated_count"] == 2


def issue_assessment_row(issue_id, applicability, remediation, *, revalidation=None, risk_level="unrated"):
    return {
        "issue_id": issue_id,
        "title": issue_id,
        "url": f"https://github.com/{issue_id.split(':', 1)[1].replace('#', '/issues/')}",
        "state": "open",
        "assessment_scope": "open",
        "applicability": applicability,
        "reason": "Fixture evidence.",
        "remediation": remediation,
        "target_version": "19.2.0",
        "fixed_release_lines": [],
        "fix_target_relations": [],
        "reviewed_assertion_ids": [],
        "revalidation_due_enrichment_ids": revalidation or [],
        "decision": {"matched_on": [], "excluded_by": [], "unknowns": []},
        "requirement_evaluation": [],
        "risk": {
            "level": risk_level,
            "source": "reviewed_enrichment" if risk_level != "unrated" else "none",
            "rationale": "Fixture risk evidence." if risk_level != "unrated" else "No reviewed risk evidence.",
            "evidence_refs": ["https://example.test/evidence"] if risk_level != "unrated" else [],
        },
        "live_verification": {"required": True, "playbook_available": False, "playbook_step_count": 0, "methods": []},
        "needs_live_verification": True,
    }


def assessment_page_fetcher(rows, *, catalog_status="current", exclusion_count=0, evaluated_count=None):
    def fetch(payload):
        offset = payload["offset"]
        limit = payload["limit"]
        page = rows[offset : offset + limit]
        next_offset = offset + len(page)
        has_more = next_offset < len(rows)
        return {
            "schema": "rock-kb-rock-issue-assessment-v2",
            "projection_version": "test-v1",
            "scope": payload["scope"],
            "catalog": {
                "schema": "rock-kb-rock-issue-catalog-freshness-v1",
                "status": catalog_status,
                "projection_matches_source": True,
            },
            "count": len(page),
            "total_count": len(rows),
            "evaluated_count": evaluated_count if evaluated_count is not None else len(rows),
            "population_by_state": {"open": evaluated_count if evaluated_count is not None else len(rows)},
            "offset": offset,
            "limit": limit,
            "next_offset": next_offset if has_more else None,
            "has_more": has_more,
            "counts": {"possible": len(rows)},
            "exclusion_summary": {
                "count": exclusion_count,
                "by_basis": {"concept:no_profile_concept_match": exclusion_count} if exclusion_count else {},
                "examples": [],
                "truncated": False,
            },
            "results": page,
        }

    return fetch


def test_client_get_text_sends_user_agent(monkeypatch):
    cli = load_client_cli()
    cli.REQUEST_COHORT = "external-test"
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return b"ok"

    def fake_urlopen(req):
        captured["user_agent"] = req.headers.get("User-agent")
        captured["client_version"] = req.headers.get("X-rock-kb-client-version")
        captured["cohort"] = req.headers.get("X-rock-kb-cohort")
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.get_text("https://example.test/manifest.json") == "ok"
    assert captured["user_agent"] == cli.USER_AGENT
    assert captured["client_version"] == cli.package_version()
    assert captured["cohort"] == "external-test"


def test_client_post_json_sends_user_agent_and_accept(monkeypatch):
    cli = load_client_cli()
    cli.REQUEST_COHORT = "maintainer"
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return b'{"status":"ok"}'

    def fake_urlopen(req):
        captured["user_agent"] = req.headers.get("User-agent")
        captured["accept"] = req.headers.get("Accept")
        captured["client_version"] = req.headers.get("X-rock-kb-client-version")
        captured["cohort"] = req.headers.get("X-rock-kb-cohort")
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.post_json("https://example.test/submit", {"ok": True}, token="secret") == {"status": "ok"}
    assert captured["user_agent"] == cli.USER_AGENT
    assert captured["accept"] == "application/json"
    assert captured["client_version"] == cli.package_version()
    assert captured["cohort"] == "maintainer"


def test_client_mcp_config_includes_only_bounded_opt_in_cohort(capsys):
    cli = load_client_cli()

    assert cli.main(["--url", "https://example.test", "--cohort", "external-test", "mcp-config"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["mcpServers"]["rock-kb"]["headers"] == {"x-rock-kb-cohort": "external-test"}


def test_client_telemetry_opt_in_is_private_and_mcp_config_uses_anonymous_marker(capsys):
    cli = load_client_cli()

    assert cli.main(["telemetry", "enable", "--cohort", "community", "--consent-attested"]) == 0
    enabled = json.loads(capsys.readouterr().out)
    state_path = Path(enabled["state_path"])
    state = json.loads(state_path.read_text(encoding="utf-8"))

    assert enabled["enabled"] is True
    assert enabled["anonymous_installation_id_present"] is True
    assert "installation_id" not in enabled
    assert stat.S_IMODE(state_path.stat().st_mode) == 0o600
    assert state["installation_id"].startswith("rkbi_")

    assert cli.main(["mcp-config"]) == 0
    config = json.loads(capsys.readouterr().out)
    assert config["mcpServers"]["rock-kb"]["headers"] == {
        "x-rock-kb-cohort": "community",
        "x-rock-kb-installation-id": state["installation_id"],
    }

    assert cli.main(["telemetry", "disable"]) == 0
    disabled = json.loads(capsys.readouterr().out)
    assert disabled["enabled"] is False
    assert not state_path.exists()


def test_client_telemetry_status_detects_current_managed_mcp_configuration(monkeypatch, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(
        cli,
        "skill_status",
        lambda **_kwargs: {
            "agents": [
                {
                    "agent": "codex",
                    "config_status": "current",
                }
            ]
        },
    )

    assert cli.main(["telemetry", "enable", "--cohort", "maintainer", "--consent-attested"]) == 0
    capsys.readouterr()
    assert cli.main(["telemetry", "status"]) == 0
    status = json.loads(capsys.readouterr().out)

    assert status["enabled"] is True
    assert status["mcp_configuration_status"] == "current"
    assert status["mcp_configuration_update_required"] is False
    assert status["managed_agent_configurations"] == [
        {
            "agent": "codex",
            "config_status": "current",
        }
    ]


def test_client_telemetry_status_detects_stale_managed_mcp_configuration(monkeypatch, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(
        cli,
        "skill_status",
        lambda **_kwargs: {
            "agents": [
                {
                    "agent": "codex",
                    "config_status": "update_available",
                }
            ]
        },
    )

    assert cli.main(["telemetry", "status"]) == 0
    status = json.loads(capsys.readouterr().out)

    assert status["mcp_configuration_status"] == "update_required"
    assert status["mcp_configuration_update_required"] is True


def test_client_outcome_posts_only_fixed_structured_fields(monkeypatch, capsys):
    cli = load_client_cli()
    captured = {}

    def fake_post_json(url: str, payload: dict, token: str = ""):
        captured["url"] = url
        captured["payload"] = payload
        return {"status": "recorded"}

    monkeypatch.setattr(cli, "post_json", fake_post_json)

    assert cli.main([
        "--url", "https://example.test",
        "outcome", "claim:claim:abc123",
        "--outcome", "partially_useful",
        "--reason", "incomplete",
        "--reason", "version_gap",
        "--consent-attested",
    ]) == 0

    assert captured == {
        "url": "https://example.test/outcomes",
        "payload": {
            "result_id": "claim:claim:abc123",
            "outcome": "partially_useful",
            "reason_codes": ["incomplete", "version_gap"],
            "consent_attested": True,
        },
    }
    assert "recorded" in capsys.readouterr().out


def test_client_outcome_rejects_incompatible_reason_before_posting(monkeypatch, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(cli, "post_json", lambda *_args, **_kwargs: pytest.fail("outcome should not be posted"))

    with pytest.raises(SystemExit) as exc:
        cli.main([
            "outcome", "claim:claim:abc123",
            "--outcome", "useful",
            "--reason", "incorrect",
            "--consent-attested",
        ])

    assert exc.value.code == 2
    assert "incompatible with useful" in capsys.readouterr().err


def test_client_mcp_config_supports_opt_in_codemode(capsys):
    cli = load_client_cli()

    assert cli.main(["--url", "https://example.test", "mcp-config", "--mode", "code"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["mcpServers"]["rock-kb"]["url"] == "https://example.test/mcp/code"


def test_client_submit_infers_org_and_reads_token_file(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")
    token_file = tmp_path / "token.txt"
    token_file.write_text("secret-token\n", encoding="utf-8")
    captured = {}

    def fake_post_json(url: str, payload: dict, token: str):
        captured["url"] = url
        captured["payload"] = payload
        captured["token"] = token
        return {"status": "validated"}

    monkeypatch.setattr(cli, "post_json", fake_post_json)

    exit_code = cli.main(["--url", "https://example.test", "submit", str(bundle), "--token-file", str(token_file), "--dry-run"])

    assert exit_code == 0
    assert captured["url"] == "https://example.test/submit"
    assert captured["payload"]["org_id"] == row["org_id"]
    assert captured["payload"]["dry_run"] is True
    assert captured["token"] == "secret-token"
    assert "validated" in capsys.readouterr().out


def test_client_auth_check_uses_token_file(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    token_file = tmp_path / "token.txt"
    token_file.write_text("secret-token\n", encoding="utf-8")
    captured = {}

    def fake_post_json(url: str, payload: dict, token: str):
        captured["url"] = url
        captured["payload"] = payload
        captured["token"] = token
        return {"status": "ok"}

    monkeypatch.setattr(cli, "post_json", fake_post_json)

    exit_code = cli.main(["--url", "https://example.test", "auth-check", "--org", "fixture-org", "--token-file", str(token_file)])

    assert exit_code == 0
    assert captured == {
        "url": "https://example.test/auth/check",
        "payload": {"org_id": "fixture-org"},
        "token": "secret-token",
    }
    assert "ok" in capsys.readouterr().out


def test_agent_installer_preserves_config_and_creates_backups(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    config = tmp_path / ".codex" / "config.toml"
    config.parent.mkdir(parents=True)
    config.write_text('# keep this comment\nmodel = "gpt-5"\n\n[mcp_servers.other]\nurl = "https://other.test/mcp"\n', encoding="utf-8")

    mock_skill_service(monkeypatch, cli)

    exit_code = cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)])

    assert exit_code == 0
    updated = config.read_text(encoding="utf-8")
    assert "# keep this comment" in updated
    assert '[mcp_servers.rock-kb]\nurl = "https://example.test/mcp"' in updated
    assert '[mcp_servers.other]\nurl = "https://other.test/mcp"' in updated
    assert list(config.parent.glob("config.toml.rock-kb-backup-*"))
    installed_skill = tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md"
    assert installed_skill.exists()
    assert "rock-kb-managed-by: rock-kb" in installed_skill.read_text(encoding="utf-8")
    output = json.loads(capsys.readouterr().out)
    state_path = Path(output["state_path"])
    assert state_path.exists()
    assert state_path.stat().st_mode & 0o777 == 0o600
    assert output["status"] == "ok"
    assert output["restart_required"] is True


def test_agent_installer_applies_and_removes_private_telemetry_headers(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    mock_skill_service(monkeypatch, cli)

    assert cli.main(["telemetry", "enable", "--cohort", "community", "--consent-attested"]) == 0
    enabled = json.loads(capsys.readouterr().out)
    state = json.loads(Path(enabled["state_path"]).read_text(encoding="utf-8"))
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    config = tmp_path / ".codex" / "config.toml"
    installed = config.read_text(encoding="utf-8")
    assert '"x-rock-kb-cohort" = "community"' in installed
    assert state["installation_id"] in installed

    assert cli.main(["telemetry", "disable"]) == 0
    capsys.readouterr()
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    updated = config.read_text(encoding="utf-8")
    assert "x-rock-kb-cohort" not in updated
    assert "x-rock-kb-installation-id" not in updated


def test_agent_installer_dry_run_is_non_mutating(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    mock_skill_service(monkeypatch, cli)

    exit_code = cli.main(["install-agent", "--agent", "cursor", "--home", str(tmp_path), "--dry-run"])

    assert exit_code == 0
    assert not (tmp_path / ".cursor" / "mcp.json").exists()
    output = capsys.readouterr().out
    assert '"status": "dry_run"' in output
    assert '"config_action": "would_update"' in output


def test_agent_installer_rejects_manifest_hash_mismatch_before_writing(monkeypatch, tmp_path):
    cli = load_client_cli()
    source = skill_source()
    manifest = skill_manifest(source)
    manifest["sha256"] = "0" * 64
    monkeypatch.setattr(cli, "get_json", lambda url: manifest if url.endswith("/skill/manifest.json") else {"status": "ok"})
    monkeypatch.setattr(cli, "get_text", lambda url: source)
    monkeypatch.setattr(cli, "package_version", lambda: "0.13.0")

    try:
        cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)])
    except RuntimeError as exc:
        assert "published manifest hash" in str(exc)
    else:
        raise AssertionError("mismatched skill bytes should fail closed")

    assert not (tmp_path / ".codex" / "config.toml").exists()
    assert not (tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md").exists()


def test_agent_installer_surgically_updates_json_config():
    load_client_cli()
    from rock_kb_client.installer import update_json_config

    original = '{\n    "theme": {"font": "large"},\n    "mcpServers": {\n      "other": {"url": "https://other.test/mcp"}\n    }\n}\n'

    updated = update_json_config(original, "mcpServers", "rock-kb", {"type": "http", "url": "https://kb.test/mcp"})

    parsed = json.loads(updated)
    assert parsed["theme"] == {"font": "large"}
    assert parsed["mcpServers"]["other"] == {"url": "https://other.test/mcp"}
    assert parsed["mcpServers"]["rock-kb"] == {"type": "http", "url": "https://kb.test/mcp"}
    assert '    "theme": {"font": "large"}' in updated


def test_agent_installer_preflights_all_hosts_before_writing(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    cursor_config = tmp_path / ".cursor" / "mcp.json"
    cursor_config.parent.mkdir(parents=True)
    cursor_config.write_text('{"mcpServers": {}}\n', encoding="utf-8")
    (tmp_path / ".claude.json").write_text('{"mcpServers": ', encoding="utf-8")
    mock_skill_service(monkeypatch, cli)

    try:
        cli.main(["install-agent", "--agent", "cursor", "--agent", "claude", "--home", str(tmp_path)])
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("malformed second config should abort installation")

    assert json.loads(cursor_config.read_text(encoding="utf-8")) == {"mcpServers": {}}
    assert not list(cursor_config.parent.glob("mcp.json.rock-kb-backup-*"))
    capsys.readouterr()


def test_skill_check_is_non_mutating_and_update_is_backup_protected(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    first_source = mock_skill_service(monkeypatch, cli)
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    skill_path = tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md"
    installed_before = skill_path.read_text(encoding="utf-8")

    second_source = skill_source("1.0.1")
    second_manifest = skill_manifest(second_source, "1.0.1")
    monkeypatch.setattr(cli, "get_json", lambda url: second_manifest if url.endswith("/skill/manifest.json") else {"status": "ok", "version": "test"})
    monkeypatch.setattr(cli, "get_text", lambda url: second_source)

    assert cli.main(["--url", "https://example.test", "skill", "check", "--agent", "codex", "--home", str(tmp_path)]) == 0
    check = json.loads(capsys.readouterr().out)
    assert check["status"] == "update_available"
    assert check["recommended_action"] == "notify_human_before_update"
    assert skill_path.read_text(encoding="utf-8") == installed_before
    assert second_source != first_source

    assert cli.main(["--url", "https://example.test", "skill", "update", "--agent", "codex", "--home", str(tmp_path)]) == 0
    update = json.loads(capsys.readouterr().out)
    installed_after = skill_path.read_text(encoding="utf-8")
    assert update["status"] == "ok"
    assert update["restart_required"] is True
    assert "rock-kb-skill-version: 1.0.1" in installed_after
    assert second_manifest["sha256"] in installed_after
    assert list(skill_path.parent.glob("SKILL.md.rock-kb-backup-*"))


def test_skill_status_and_policy_are_stable_and_project_auto_is_rejected(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    mock_skill_service(monkeypatch, cli)
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "cursor", "--home", str(tmp_path)]) == 0
    capsys.readouterr()

    assert cli.main(["--url", "https://example.test", "skill", "policy", "auto", "--agent", "cursor", "--home", str(tmp_path)]) == 0
    policy = json.loads(capsys.readouterr().out)
    assert policy["schema"] == "rock-kb-skill-policy-v1"
    assert policy["policy"] == "auto"

    assert cli.main(["--url", "https://example.test", "skill", "status", "--agent", "cursor", "--home", str(tmp_path), "--format", "json"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["schema"] == "rock-kb-skill-status-v1"
    assert status["status"] == "current"
    assert status["policy"] == "auto"
    assert status["agents"][0]["source_sha256"] == skill_manifest(skill_source())["sha256"]

    project = tmp_path / "project"
    project.mkdir()
    assert cli.main([
        "--url", "https://example.test", "skill", "policy", "auto", "--agent", "cursor", "--home", str(tmp_path),
        "--scope", "project", "--project-dir", str(project),
    ]) == 1
    rejected = json.loads(capsys.readouterr().out)
    assert rejected["status"] == "error"
    assert "cannot use auto policy" in rejected["error"]


def test_pinned_skill_requires_explicit_unpin_before_update(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    mock_skill_service(monkeypatch, cli)
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    assert cli.main(["--url", "https://example.test", "skill", "policy", "pinned", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    skill_path = tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md"
    pinned_text = skill_path.read_text(encoding="utf-8")

    new_source = skill_source("1.0.1")
    new_manifest = skill_manifest(new_source, "1.0.1")
    monkeypatch.setattr(cli, "get_json", lambda url: new_manifest if url.endswith("/skill/manifest.json") else {"status": "ok", "version": "test"})
    monkeypatch.setattr(cli, "get_text", lambda url: new_source)

    assert cli.main(["--url", "https://example.test", "skill", "update", "--agent", "codex", "--home", str(tmp_path)]) == 1
    pinned = json.loads(capsys.readouterr().out)
    assert pinned["status"] == "pinned"
    assert skill_path.read_text(encoding="utf-8") == pinned_text

    assert cli.main(["--url", "https://example.test", "skill", "update", "--unpin", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    assert "rock-kb-skill-version: 1.0.1" in skill_path.read_text(encoding="utf-8")


def test_if_due_check_skips_network_and_passive_auto_update_uses_persisted_consent(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    mock_skill_service(monkeypatch, cli)
    assert cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)]) == 0
    install = json.loads(capsys.readouterr().out)
    assert cli.main(["--url", "https://example.test", "skill", "policy", "auto", "--agent", "codex", "--home", str(tmp_path)]) == 0
    capsys.readouterr()

    calls: list[str] = []
    monkeypatch.setattr(cli, "get_json", lambda url: calls.append(url) or {"status": "ok"})
    assert cli.main(["--url", "https://example.test", "skill", "check", "--if-due", "--agent", "codex", "--home", str(tmp_path)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "not_due"
    assert calls == []

    state_path = Path(install["state_path"])
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["last_checked_at"] = "2026-07-15T00:00:00Z"
    state["last_attempted_at"] = "2026-07-15T00:00:00Z"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    new_source = skill_source("1.0.1")
    new_manifest = skill_manifest(new_source, "1.0.1")

    def service_json(url: str):
        if url.endswith("/skill/manifest.json"):
            return new_manifest
        if url.endswith("/health"):
            return {"status": "ok", "version": "test"}
        if "/search?" in url:
            return {"schema": "rock-kb-search-result-v2", "results": []}
        raise AssertionError(url)

    monkeypatch.setattr(cli, "get_json", service_json)
    monkeypatch.setattr(cli, "get_text", lambda url: new_source)
    monkeypatch.setattr(cli.Path, "home", lambda: tmp_path)
    assert cli.main(["--url", "https://example.test", "search", "labels"]) == 0
    captured = capsys.readouterr()
    assert "updated automatically" in captured.err
    assert "rock-kb-skill-version: 1.0.1" in (tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md").read_text(encoding="utf-8")
