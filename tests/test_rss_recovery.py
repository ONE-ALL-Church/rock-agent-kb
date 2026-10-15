import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from rock_kb.cli import app, _legacy
from rock_kb.normalize import parse_rss
from rock_kb.sources import get_source

FIXTURES = Path(__file__).parent / "fixtures"
RSS = '<rss version="2.0"><channel><title>Synthetic feed</title><item><guid>one</guid><title>Synthetic item</title><link>https://example.test/one</link></item></channel></rss>'
EMPTY_RSS = '<rss version="2.0"><channel><title>Synthetic feed</title></channel></rss>'
EMPTY_ATOM = '<feed xmlns="http://www.w3.org/2005/Atom"><title>Synthetic feed</title></feed>'


@pytest.mark.parametrize("content", [
    "", "   ", "<html><title>Error 404</title><body>Not Found</body></html>",
    '{"error":"temporarily unavailable"}', "<document><title>Not a feed</title></document>",
    EMPTY_RSS, EMPTY_ATOM, RSS.removesuffix("</channel></rss>"),
])
def test_parser_rejects_invalid_empty_and_partial_feeds(content):
    with pytest.raises(ValueError, match="RSS/Atom"):
        parse_rss(get_source("rock_youtube"), content)


@pytest.mark.parametrize("source_id,fixture", [
    ("rock_youtube", "youtube_feed.xml"), ("rock_podcast_rss", "rss.xml"),
])
def test_valid_registered_feed_schemas_still_normalize(source_id, fixture):
    records = parse_rss(get_source(source_id), (FIXTURES / fixture).read_text())
    assert len(records) == 1
    assert records[0]["source_id"] == source_id
    assert records[0]["source_url"].startswith("https://")


def invoke_normalize(monkeypatch, tmp_path, response, source_id="rock_youtube", command="normalize"):
    path = tmp_path / "normalized.jsonl"
    previous = b'{"id":"last-good","retrieved_at":"2026-10-14T00:00:00+00:00"}\n'
    path.write_bytes(previous)
    monkeypatch.setattr(_legacy, "source_output_path", lambda *args: path)
    monkeypatch.setattr(_legacy, "ensure_generated_dirs", lambda: None)
    monkeypatch.setattr(_legacy, "fetch_url", lambda url: response)
    monkeypatch.setattr(_legacy, "audit_license_records", lambda: pytest.fail("Failed source must stop refresh before audits"))
    monkeypatch.setattr(_legacy, "build_agent_pack", lambda: pytest.fail("Failed source must not rebuild public artifacts"))
    args = ["sources", command, "--source", source_id]
    if command == "refresh":
        args.extend(["--skip-probe", "--skip-discovery"])
    result = CliRunner().invoke(app, args)
    return result, path, previous


@pytest.mark.parametrize("status,content_type,content", [
    (404, "text/html; charset=UTF-8", "<html><title>Not Found</title></html>"),
    (403, "application/rss+xml", RSS), (429, "application/rss+xml", RSS),
    (500, "application/rss+xml", RSS), (304, "application/rss+xml", ""),
    (200, "text/html", "<html>Sign in</html>"), (200, "application/json", "{}"),
    (200, "", RSS), (200, "application/rss+xml", EMPTY_RSS),
    (200, "application/atom+xml", EMPTY_ATOM), (200, "application/xml", ""),
    (200, "application/rss+xml", RSS.removesuffix("</channel></rss>")),
])
@pytest.mark.parametrize("source_id", ["rock_youtube", "rock_podcast_rss"])
def test_cli_failures_keep_last_good_bytes_and_timestamp(monkeypatch, tmp_path, status, content_type, content, source_id):
    result, path, previous = invoke_normalize(monkeypatch, tmp_path, {
        "status_code": status, "content_type": content_type, "content": content,
    }, source_id)
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert path.read_bytes() == previous
    assert "wrote 0" not in result.output


def test_daily_refresh_propagates_feed_failure_instead_of_reporting_success(monkeypatch, tmp_path):
    result, path, previous = invoke_normalize(monkeypatch, tmp_path, {
        "status_code": 404, "content_type": "text/html", "content": "<html>Not Found</html>",
    }, command="refresh")
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "HTTP 404" in str(result.exception)
    assert path.read_bytes() == previous
    assert "License and citation audit passed" not in result.output


def test_zero_record_normalizer_cannot_clobber_last_good(monkeypatch, tmp_path):
    monkeypatch.setattr(_legacy, "records_from_source_content", lambda *args: [])
    result, path, previous = invoke_normalize(monkeypatch, tmp_path, {
        "status_code": 200, "content_type": "application/rss+xml", "content": RSS,
    })
    assert result.exit_code != 0
    assert "no records" in str(result.exception)
    assert path.read_bytes() == previous


@pytest.mark.parametrize("content_type", ["application/rss+xml", "application/atom+xml; charset=utf-8", "application/xml", "text/xml"])
def test_valid_feed_replaces_last_good_through_canonical_cli(monkeypatch, tmp_path, content_type):
    result, path, previous = invoke_normalize(monkeypatch, tmp_path, {
        "status_code": 200, "content_type": content_type, "content": RSS,
    })
    assert result.exit_code == 0, result.output
    assert path.read_bytes() != previous
    records = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(records) == 1
    assert records[0]["source_url"] == "https://example.test/one"
