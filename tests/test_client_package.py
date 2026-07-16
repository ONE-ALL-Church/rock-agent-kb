from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import stat
import warnings
import zipfile
from pathlib import Path

VALID_FIXTURE = Path("tests/fixtures/contributions/valid-bundle.jsonl")


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
            {"profile": {"core_version": "19.2.0", "concepts": ["hosting-infrastructure"]}, "limit": 25},
        )
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
    assert "profile" not in state
    assert state["profile_sha256"] == first["profile_sha256"]

    changed = [
        issue_assessment_row("rock_issue:SparkDevNetwork/Rock#1", "confirmed", "candidate_fix", revalidation=["enrichment:1"]),
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
    assert second["changes"]["revalidation_due"][0]["issue_id"].endswith("#1")


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
            "schema": "rock-kb-rock-issue-assessment-v1",
            "projection_version": "test-v1",
            "count": 1,
            "total_count": 2,
            "offset": 0,
            "limit": 500,
            "next_offset": None,
            "has_more": False,
            "counts": {"possible": 2},
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


def issue_assessment_row(issue_id, applicability, remediation, *, revalidation=None):
    return {
        "issue_id": issue_id,
        "title": issue_id,
        "url": f"https://github.com/{issue_id.split(':', 1)[1].replace('#', '/issues/')}",
        "state": "open",
        "applicability": applicability,
        "reason": "Fixture evidence.",
        "remediation": remediation,
        "target_version": "19.2.0",
        "fixed_release_lines": [],
        "fix_target_relations": [],
        "reviewed_assertion_ids": [],
        "revalidation_due_enrichment_ids": revalidation or [],
        "needs_live_verification": True,
    }


def assessment_page_fetcher(rows):
    def fetch(payload):
        offset = payload["offset"]
        limit = payload["limit"]
        page = rows[offset : offset + limit]
        next_offset = offset + len(page)
        has_more = next_offset < len(rows)
        return {
            "schema": "rock-kb-rock-issue-assessment-v1",
            "projection_version": "test-v1",
            "count": len(page),
            "total_count": len(rows),
            "offset": offset,
            "limit": limit,
            "next_offset": next_offset if has_more else None,
            "has_more": has_more,
            "counts": {"possible": len(rows)},
            "results": page,
        }

    return fetch


def test_client_get_text_sends_user_agent(monkeypatch):
    cli = load_client_cli()
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
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.get_text("https://example.test/manifest.json") == "ok"
    assert captured["user_agent"] == cli.USER_AGENT
    assert captured["client_version"] == cli.package_version()


def test_client_post_json_sends_user_agent_and_accept(monkeypatch):
    cli = load_client_cli()
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
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.post_json("https://example.test/submit", {"ok": True}, token="secret") == {"status": "ok"}
    assert captured["user_agent"] == cli.USER_AGENT
    assert captured["accept"] == "application/json"
    assert captured["client_version"] == cli.package_version()


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

    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok", "version": "test"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n\n# Rock KB Agent\n")

    exit_code = cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)])

    assert exit_code == 0
    updated = config.read_text(encoding="utf-8")
    assert "# keep this comment" in updated
    assert '[mcp_servers.rock-kb]\nurl = "https://example.test/mcp"' in updated
    assert '[mcp_servers.other]\nurl = "https://other.test/mcp"' in updated
    assert list(config.parent.glob("config.toml.rock-kb-backup-*"))
    assert (tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md").exists()
    assert '"status": "ok"' in capsys.readouterr().out


def test_agent_installer_dry_run_is_non_mutating(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n")

    exit_code = cli.main(["install-agent", "--agent", "cursor", "--home", str(tmp_path), "--dry-run"])

    assert exit_code == 0
    assert not (tmp_path / ".cursor" / "mcp.json").exists()
    output = capsys.readouterr().out
    assert '"status": "dry_run"' in output
    assert '"config_action": "would_update"' in output


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
    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n")

    try:
        cli.main(["install-agent", "--agent", "cursor", "--agent", "claude", "--home", str(tmp_path)])
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("malformed second config should abort installation")

    assert json.loads(cursor_config.read_text(encoding="utf-8")) == {"mcpServers": {}}
    assert not list(cursor_config.parent.glob("mcp.json.rock-kb-backup-*"))
    capsys.readouterr()
