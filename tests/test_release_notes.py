from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from uuid import UUID

import httpx
import pytest
from typer.testing import CliRunner

from rock_kb import release_notes as releases
from rock_kb.cli import app
from rock_kb.cli import _legacy
from rock_kb.jsonl import read_jsonl
from rock_kb.normalize import canonical_record_id, parse_release_notes
from rock_kb.rock_issues import load_release_note_index, normalize_release_note_refs
from rock_kb.sources import get_source


def note(number=1, kind="fixed", **overrides):
    return {
        "noteGuid": str(UUID(int=number)), "type": kind, "category": "CMS", "categoryOrder": 3,
        "html": f"Synthetic change {number} without an issue number.", "issues": ["123"], **overrides,
    }


def core_release(version="20.0", notes=None, **overrides):
    return {
        "isFound": True, "version": version, "releaseDate": "2026-09-02", "status": "Alpha Testing",
        "notes": notes if notes is not None else [note()], "headsUpHtml": "", "introHtml": "", **overrides,
    }


def overview(details):
    versions = []
    for row in details:
        counts = {kind: sum(note["type"] == kind for note in row["notes"]) for kind in releases.CHANGE_TYPES}
        versions.append({
            **{key: row[key] for key in ("version", "releaseDate", "status")},
            "isAlpha": True, "isBeta": False, "isEarlyAccess": True,
            "isProduction": False, "isLatestSecured": False, "total": len(row["notes"]), **counts,
        })
    return {"versionCount": len(versions), "versions": versions}


def mobile_release(version="19.5", **overrides):
    return {
        "version": version, "display": version, "releaseDate": "2026-10-02",
        "minimumOs": "iOS version 15.0, Android version 7.0 (API level 24)",
        "minimumRock": "1.12.6", "introHtml": "", "notes": [note()], **overrides,
    }


def shell(slug, compiled=None):
    block = {
        "blockFileUrl": "/Obsidian/Blocks/Cms/forgeContentDetail.obs",
        "configurationValues": {"compiledContent": compiled or f'const app = useLavaApp("{slug}");'},
    }
    return f"<html><main></main><script>module.initializeBlock({json.dumps(block)});</script></html>"


def fake_transport(source, *, details=None, index=None, html=None, override=None):
    mobile = source.kind == "rock_mobile_release_notes"
    slug = releases.SOURCE_ROUTES[source.id][2]
    details = details if details is not None else [core_release()]
    payload = index if index is not None else (
        {"versionCount": 1, "versions": [mobile_release()]} if mobile else overview(details)
    )
    requests = []

    def handler(request):
        requests.append(request)
        assert request.method == "GET"
        assert request.url.host == "www.rockrms.com"
        assert request.headers["X-Helix-CSRF-Protection"] == "true"
        assert "authorization" not in request.headers
        assert "cookie" not in request.headers
        if override:
            response = override(request)
            if response is not None:
                return response
        if str(request.url) == source.root_url:
            return httpx.Response(200, text=html if html is not None else shell(slug), headers={
                "content-type": "text/html", "set-cookie": "session=not-forwarded; Path=/",
            })
        if request.url.path.endswith(("/overview", "/releases")):
            return httpx.Response(200, json=payload)
        if request.url.path.endswith("/version"):
            version = request.url.params["version"]
            return httpx.Response(200, json=next(row for row in details if row["version"] == version))
        pytest.fail(f"Unexpected request: {request.url}")

    return httpx.MockTransport(handler), requests


def fetch_core(**kwargs):
    source = get_source("rock_core_release_notes")
    transport, requests = fake_transport(source, **kwargs)
    return releases.fetch_release_note_records(source, transport=transport), requests


def test_core_anonymous_headers_complete_snapshot_and_provenance():
    details = [core_release(notes=[note(1, "added"), note(2, "improved"), note(3), note(4, "security")]),
               core_release("19.1", notes=[note(5)])]
    rows, requests = fetch_core(details=details)
    assert len(rows) == 5
    assert len(requests) == 4
    assert requests[1].url.path == "/api/v2/lava-app/1/release-notes-forge-test/overview"
    assert {row["version"] for row in rows} == {"20.0", "19.1"}
    assert [row["change_type"] for row in rows[:4]] == ["new_feature", "improvement", "bug_fix", "security"]
    assert [row["upstream_change_type"] for row in rows[:4]] == ["added", "improved", "fixed", "security"]
    assert rows[0]["release_status"] == "Alpha Testing"
    assert rows[0]["module"] == "CMS"
    assert rows[0]["issue_refs"] == ["123"]
    assert "123" not in rows[0]["excerpt"]
    assert rows[0]["note_guid"] == str(UUID(int=1))
    assert rows[0]["id"] == canonical_record_id("rock_core_release_notes", "20.0:CMS:" + rows[0]["excerpt"])
    assert rows[0]["api_provenance"]["url"].endswith("/version?version=20.0")
    assert len(rows[0]["api_provenance"]["payload_sha256"]) == 64
    assert rows[0]["api_provenance"]["route_version"] == 1
    assert rows[0]["api_provenance"]["parser_version"] == "release-lava-app-v3"
    assert rows[3]["severity"] == "high"


@pytest.mark.parametrize("url", [
    "http://www.rockrms.com/releasenotes", "https://evil.example/releasenotes",
    "https://www.rockrms.com.evil.example/releasenotes", "https://user@www.rockrms.com/releasenotes",
    "https://www.rockrms.com:443/releasenotes", "https://www.rockrms.com/releasenotes?SiteId=1",
    "https://www.rockrms.com/api/v2/lava-app/2/release-notes-forge-test/overview",
    "https://www.rockrms.com/api/v2/lava-app/1/unknown/overview",
    "https://www.rockrms.com/api/v2/lava-app/1/release-notes-forge-test/version?version=20.0&version=19.0",
    "https://www.rockrms.com/api/v2/lava-app/1/release-notes-forge-test/version?version=../../private",
    "https://www.rockrms.com/api/v2/lava-app/1/release-notes-forge-test/version?version=20.0&SiteId=1",
])
def test_allowlist_rejects_unproven_routes(url):
    with pytest.raises(releases.ReleaseNotesError, match="allowlist"):
        releases._validate_url(url, get_source("rock_core_release_notes"))


def test_source_allowlist_runs_before_any_request():
    source = replace(get_source("rock_core_release_notes"), root_url="https://evil.example/releasenotes")
    with pytest.raises(releases.ReleaseNotesError, match="allowlist"):
        releases.fetch_release_note_records(source, transport=httpx.MockTransport(lambda request: pytest.fail("Network")))


@pytest.mark.parametrize("compiled", [
    'useLavaApp("unapproved-app")', 'useLavaApp("mobile-release-notes")', "useLavaApp(dynamicSlug)",
])
def test_unrecognized_forge_apps_fail_closed(compiled):
    with pytest.raises(releases.ReleaseNotesError, match="Unrecognized"):
        fetch_core(html=shell("unused", compiled=compiled))


def test_source_specific_default_does_not_execute_compiled_content():
    rows, _ = fetch_core(html=shell("unused", compiled="throw new Error('must never execute');"))
    assert rows[0]["api_provenance"]["app_slug"] == "release-notes-forge-test"


@pytest.mark.parametrize("mutation", [
    lambda payload: payload.update(versionCount=138),
    lambda payload: payload.update(versionCount=0, versions=[]),
    lambda payload: payload.update(versionCount=True),
    lambda payload: payload.update(versionCount=2, versions=payload["versions"] * 2),
    lambda payload: payload["versions"][0].update(total=2),
    lambda payload: payload["versions"][0].update(added=1),
    lambda payload: payload["versions"][0].pop("fixed"),
    lambda payload: payload["versions"][0].update(version="unknown"),
    lambda payload: payload["versions"][0].update(isAlpha="true"),
])
def test_overview_completeness_and_strict_schema(mutation):
    payload = overview([core_release()])
    mutation(payload)
    with pytest.raises(releases.ReleaseNotesError):
        fetch_core(index=payload)


@pytest.mark.parametrize("mutation", [
    lambda row: row.update(isFound=False), lambda row: row.update(version="99.0"),
    lambda row: row.update(status="Production"), lambda row: row.update(releaseDate="2026-09-03"),
    lambda row: row.update(notes=[]), lambda row: row["notes"].append(note(2)),
    lambda row: row["notes"][0].update(type="added"), lambda row: row["notes"][0].update(html="<p> </p>"),
    lambda row: row["notes"][0].update(noteGuid="not-a-guid"),
    lambda row: row["notes"][0].update(issues=[123]), lambda row: row["notes"][0].pop("issues"),
])
def test_missing_partial_or_mismatched_detail_fails(mutation):
    detail = core_release()
    index = overview([detail])
    mutation(detail)

    def override(request):
        return httpx.Response(200, json=detail) if request.url.path.endswith("/version") else None

    with pytest.raises(releases.ReleaseNotesError):
        fetch_core(index=index, override=override)


def test_duplicate_guid_fails():
    with pytest.raises(releases.ReleaseNotesError, match="Duplicate"):
        fetch_core(details=[core_release(notes=[note(), note(html="Different synthetic text")])])


def test_repeated_identical_content_keeps_legacy_id_and_all_upstream_metadata():
    rows, _ = fetch_core(details=[core_release(notes=[note(), note(2, html=note()["html"], issues=["456"])])])
    assert len(rows) == 1
    assert rows[0]["upstream_note_guids"] == [str(UUID(int=1)), str(UUID(int=2))]
    assert rows[0]["issue_refs"] == ["123", "456"]
    assert rows[0]["api_provenance"]["release_note_count"] == 2
    assert rows[0]["id"] == canonical_record_id("rock_core_release_notes", "20.0:CMS:" + note()["html"])


def test_colliding_content_with_different_type_fails():
    with pytest.raises(releases.ReleaseNotesError, match="Conflicting release identity"):
        fetch_core(details=[core_release(notes=[note(), note(2, "added", html=note()["html"])])])


@pytest.mark.parametrize("upstream,product", [
    ("1.16.0", "16.0"), ("1.16.12", "16.12"), ("1.15.4", "1.15.4"), ("20.0", "20.0"),
])
def test_core_display_mapping_is_exact_and_ids_keep_raw_version(upstream, product):
    rows, _ = fetch_core(details=[core_release(upstream)])
    row = rows[0]
    assert row["version"] == row["upstream_version"] == upstream
    assert row["release_display"] == row["product_version"] == product
    assert row["id"] == canonical_record_id(row["source_id"], f"{upstream}:CMS:{row['excerpt']}")
    assert row["api_provenance"]["version_mapping_url"] == "https://www.rockrms.com/releasenotes"
    assert releases.upgrade_cached_release_record(row) == row


def test_mobile_display_mapping_uses_api_field_and_never_strips_prefix_by_guess():
    source = get_source("rock_mobile_release_notes")
    transport, _ = fake_transport(source, index={"versionCount": 1, "versions": [mobile_release("1.7.0", display="7.0")]})
    row = releases.fetch_release_note_records(source, transport=transport)[0]
    assert row["version"] == row["upstream_version"] == "1.7.0"
    assert row["product_version"] == row["release_display"] == "7.0"
    assert row["api_provenance"]["version_mapping_url"] == "https://www.rockrms.com/mobilereleasenotes"
    assert releases.release_version_metadata({"release_family": "mobile", "version": "1.7.0"})["product_version"] == "1.7.0"


@pytest.mark.parametrize("changes", [
    {"status": "Released"}, {"releaseDate": "2026-09-03"},
])
def test_core_release_metadata_changes_hash_without_changing_record_id(changes):
    before, _ = fetch_core()
    after, _ = fetch_core(details=[core_release(**changes)])
    assert before[0]["id"] == after[0]["id"]
    assert before[0]["content_hash"] != after[0]["content_hash"]


@pytest.mark.parametrize("flag", ["isAlpha", "isBeta", "isEarlyAccess", "isProduction", "isLatestSecured"])
def test_release_flag_only_changes_hash(flag):
    before, _ = fetch_core()
    index = overview([core_release()])
    index["versions"][0][flag] = not index["versions"][0][flag]
    after, _ = fetch_core(index=index)
    assert before[0]["id"] == after[0]["id"]
    assert before[0]["content_hash"] != after[0]["content_hash"]


@pytest.mark.parametrize("changes", [
    {"issues": ["456"]}, {"issues": []}, {"type": "added"}, {"type": "improved"}, {"type": "security"},
])
def test_issue_refs_or_type_only_changes_hash_without_changing_record_id(changes):
    before, _ = fetch_core()
    after, _ = fetch_core(details=[core_release(notes=[note(**changes)])])
    assert before[0]["id"] == after[0]["id"]
    assert before[0]["content_hash"] != after[0]["content_hash"]


@pytest.mark.parametrize("changes", [
    {"minimumOs": "iOS version 16.0, Android version 7.0 (API level 24)"},
    {"minimumOs": "iOS version 15.0, Android version 8.0 (API level 26)"},
    {"minimumRock": "1.12.8"},
])
def test_mobile_minimum_only_changes_hash_without_changing_record_id(changes):
    source = get_source("rock_mobile_release_notes")
    before_transport, _ = fake_transport(source)
    after_transport, _ = fake_transport(source, index={"versionCount": 1, "versions": [mobile_release(**changes)]})
    before = releases.fetch_release_note_records(source, transport=before_transport)
    after = releases.fetch_release_note_records(source, transport=after_transport)
    assert before[0]["id"] == after[0]["id"]
    assert before[0]["content_hash"] != after[0]["content_hash"]


def test_transport_only_and_retrieval_time_changes_do_not_change_hash(monkeypatch):
    monkeypatch.setattr(releases, "now_iso", lambda: "2026-10-14T10:00:00+00:00")
    before, _ = fetch_core()
    monkeypatch.setattr(releases, "now_iso", lambda: "2026-10-14T11:00:00+00:00")

    def override(request):
        if request.url.path.endswith("/overview"):
            payload = overview([core_release()])
        elif request.url.path.endswith("/version"):
            payload = core_release()
        else:
            return None
        payload["transportOnly"] = "does not affect release meaning"
        return httpx.Response(200, text=json.dumps(payload, indent=4, sort_keys=True),
                              headers={"content-type": "application/json"})

    after, _ = fetch_core(override=override)
    assert before[0]["retrieved_at"] != after[0]["retrieved_at"]
    assert before[0]["api_provenance"]["payload_sha256"] != after[0]["api_provenance"]["payload_sha256"]
    assert before[0]["api_provenance"]["overview_sha256"] != after[0]["api_provenance"]["overview_sha256"]
    assert before[0]["id"] == after[0]["id"]
    assert before[0]["content_hash"] == after[0]["content_hash"]


def test_issue_reference_order_does_not_change_semantic_hash():
    before, _ = fetch_core(details=[core_release(notes=[note(issues=["123", "456"])])])
    after, _ = fetch_core(details=[core_release(notes=[note(issues=["456", "123", "123"])])])
    assert before[0]["content_hash"] == after[0]["content_hash"]


def test_duplicate_merge_hash_binds_all_issue_references():
    single, _ = fetch_core()
    merged, _ = fetch_core(details=[core_release(notes=[note(), note(2, html=note()["html"], issues=["456"])])])
    union, _ = fetch_core(details=[core_release(notes=[note(issues=["123", "456"])])])
    assert merged[0]["content_hash"] != single[0]["content_hash"]
    assert merged[0]["content_hash"] == union[0]["content_hash"]


def test_mobile_requirements_are_per_release_and_versions_are_exact():
    source = get_source("rock_mobile_release_notes")
    payload = {"versionCount": 2, "versions": [mobile_release(), mobile_release(
        "1.2.0", display="2.0", minimumOs="iOS version: 12.0, Android version: 6.0 (API level 23)",
        minimumRock="1.12.4", notes=[note(2, "added")],
    )]}
    transport, requests = fake_transport(source, index=payload)
    rows = releases.fetch_release_note_records(source, transport=transport)
    assert len(requests) == 2
    assert requests[1].url.path == "/api/v2/lava-app/1/mobile-release-notes/releases"
    assert rows[0]["minimum_os"] == {"ios": "15.0", "android": "7.0 (API level 24)"}
    assert rows[1]["minimum_os"] == {"ios": "12.0", "android": "6.0 (API level 23)"}
    assert rows[0]["minimum_rock_version"] == "1.12.6"
    assert rows[1]["minimum_rock_version"] == "1.12.4"
    assert rows[1]["version"] == "1.2.0"
    assert rows[1]["release_display"] == "2.0"
    assert rows[1]["release_family"] == "mobile"
    assert rows[1]["release_status"] is None


@pytest.mark.parametrize("mutation", [
    lambda payload: payload.update(versionCount=13),
    lambda payload: payload["versions"][0].update(notes=[]),
    lambda payload: payload["versions"][0].pop("minimumRock"),
    lambda payload: payload["versions"][0].update(minimumOs="Unknown OS"),
    lambda payload: payload["versions"][0].update(version="unknown"),
])
def test_mobile_partial_responses_fail(mutation):
    source = get_source("rock_mobile_release_notes")
    payload = {"versionCount": 1, "versions": [mobile_release()]}
    mutation(payload)
    transport, _ = fake_transport(source, index=payload)
    with pytest.raises(releases.ReleaseNotesError):
        releases.fetch_release_note_records(source, transport=transport)


@pytest.mark.parametrize("response", [
    httpx.Response(302, headers={"location": "https://evil.example/private"}),
    httpx.Response(401), httpx.Response(500),
    httpx.Response(200, text="{}", headers={"content-type": "text/html"}),
    httpx.Response(200, text="not JSON", headers={"content-type": "application/json"}),
    httpx.Response(200, json={}),
])
def test_http_and_malformed_responses_fail_without_redirect(response):
    calls = []

    def override(request):
        calls.append(request)
        return response if request.url.path.endswith("/overview") else None

    with pytest.raises(releases.ReleaseNotesError):
        fetch_core(override=override)
    assert len(calls) == 2


def test_network_failure_is_sanitized():
    def override(request):
        raise httpx.ReadTimeout("untrusted response text", request=request)

    with pytest.raises(releases.ReleaseNotesError, match="^Public release fetch failed$"):
        fetch_core(override=override)


@pytest.mark.parametrize("bound,value", [
    ("MAX_RESPONSE_BYTES", 10), ("MAX_TOTAL_BYTES", 10), ("MAX_FETCH_SECONDS", 0), ("MAX_RECORDS", 0),
])
def test_resource_bounds(monkeypatch, bound, value):
    monkeypatch.setattr(releases, bound, value)
    with pytest.raises(releases.ReleaseNotesError, match="bound"):
        fetch_core()


@pytest.mark.parametrize("source_id,fixture", [
    ("rock_core_release_notes", "release_notes.html"),
    ("rock_mobile_release_notes", "mobile_release_notes.html"),
])
def test_genuine_static_html_keeps_legacy_envelope_and_ids(source_id, fixture):
    source = get_source(source_id)
    html = (Path(__file__).parent / "fixtures" / "html" / fixture).read_text()
    transport, requests = fake_transport(source, html=html)
    rows = releases.fetch_release_note_records(source, transport=transport)
    expected = parse_release_notes(source, html)
    assert [{k: v for k, v in row.items() if k != "retrieved_at"} for row in rows] == [
        {k: v for k, v in row.items() if k != "retrieved_at"} for row in expected
    ]
    assert len(requests) == 1


def test_issue_refs_join_independently_of_prose(tmp_path, monkeypatch):
    rows, _ = fetch_core()
    index_path = tmp_path / "releases.jsonl"
    index_path.write_text("\n".join(json.dumps(row) for row in rows))
    monkeypatch.setattr("rock_kb.rock_issues.RELEASE_INDEX_PATH", index_path)
    joined = load_release_note_index()[("SparkDevNetwork/Rock", 123)]
    refs = normalize_release_note_refs("SparkDevNetwork/Rock", joined)
    assert refs[0]["record_id"] == rows[0]["id"]
    assert refs[0]["version"] == "20.0"


def test_canonical_cli_preserves_last_good_data_on_late_failure(tmp_path, monkeypatch):
    source = get_source("rock_core_release_notes")
    path = tmp_path / "normalized.jsonl"
    previous = b'{"id":"last-good"}\n'
    path.write_bytes(previous)
    details = [core_release(), core_release("19.1", notes=[note(2)])]

    def override(request):
        if request.url.params.get("version") == "19.1":
            return httpx.Response(200, json={"isFound": False})
        return None

    transport, requests = fake_transport(source, details=details, override=override)
    fetch = releases.fetch_release_note_records
    monkeypatch.setattr(_legacy, "fetch_release_note_records", lambda src: fetch(src, transport=transport))
    monkeypatch.setattr(_legacy, "source_output_path", lambda *args: path)
    monkeypatch.setattr(_legacy, "ensure_generated_dirs", lambda: None)
    result = CliRunner().invoke(app, ["sources", "normalize", "--source", source.id])
    assert result.exit_code != 0
    assert isinstance(result.exception, releases.ReleaseNotesError)
    assert len(requests) == 4
    assert path.read_bytes() == previous


def test_canonical_cli_writes_only_validated_release_records(tmp_path, monkeypatch):
    source = get_source("rock_mobile_release_notes")
    path = tmp_path / "normalized.jsonl"
    transport, _ = fake_transport(source)
    fetch = releases.fetch_release_note_records
    monkeypatch.setattr(_legacy, "fetch_release_note_records", lambda src: fetch(src, transport=transport))
    monkeypatch.setattr(_legacy, "source_output_path", lambda *args: path)
    monkeypatch.setattr(_legacy, "ensure_generated_dirs", lambda: None)
    result = CliRunner().invoke(app, ["sources", "normalize", "--source", source.id])
    assert result.exit_code == 0, result.output
    assert list(read_jsonl(path))[0]["version"] == "19.5"


def test_empty_html_cannot_replace_normalized_snapshot():
    with pytest.raises(releases.ReleaseNotesError, match="No static release notes"):
        fetch_core(html="<html><main>Sign in</main></html>")
