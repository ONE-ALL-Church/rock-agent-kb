from pathlib import Path

from rock_kb.community import is_html_candidate, normalize_community_fetch
from rock_kb.normalize import (
    normalize_github_repo_metadata,
    parse_mobile_doc_children,
    parse_release_notes,
    parse_rss,
)
from rock_kb.sources import get_source

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_core_release_notes():
    source = get_source("rock_core_release_notes")
    html = (FIXTURES / "html" / "release_notes.html").read_text()
    records = parse_release_notes(source, html)
    assert len(records) == 3
    assert records[0]["version"] == "19.1"
    assert records[0]["module"] == "CMS"
    assert records[0]["change_type"] == "improvement"
    assert records[0]["issue_refs"] == ["6830"]


def test_parse_mobile_release_notes():
    source = get_source("rock_mobile_release_notes")
    html = (FIXTURES / "html" / "mobile_release_notes.html").read_text()
    records = parse_release_notes(source, html)
    assert len(records) == 2
    assert records[0]["release_family"] == "mobile"
    assert records[0]["minimum_os"]["ios"] == "12.0"
    assert records[0]["minimum_rock_version"] == "12.6"


def test_parse_mobile_doc_children():
    source = get_source("rock_mobile_docs")
    html = (FIXTURES / "html" / "mobile_docs.html").read_text()
    records = parse_mobile_doc_children(source, html)
    assert len(records) == 3
    assert {record["component_type"] for record in records} >= {"command", "control"}


def test_parse_rss():
    source = get_source("rock_podcast_rss")
    xml = (FIXTURES / "rss.xml").read_text()
    records = parse_rss(source, xml)
    assert len(records) == 1
    assert records[0]["episode_number"] == "214"
    assert records[0]["rock_versions"] == ["19"]
    assert records[0]["media_url"] == "https://example.com/audio/episode-214.mp3"
    assert records[0]["media_type"] == "audio/mpeg"


def test_parse_rss_resolves_relative_links():
    source = get_source("triumph_resources")
    xml = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Resources</title>
<item><title>GitHub Spotlight</title><guid>/resources/github-spotlight</guid><link>/resources/github-spotlight</link><description>Rock v20 update.</description></item>
</channel></rss>"""

    records = parse_rss(source, xml)

    assert records[0]["source_url"] == "https://www.triumph.tech/resources/github-spotlight"
    assert records[0]["source_id"] == "triumph_resources"
    assert records[0]["canonical_path"] == "knowledge/triumph/resources-github-spotlight.md"


def test_github_repo_normalization():
    source = get_source("sparkdevnetwork_rock")
    record = normalize_github_repo_metadata(
        source,
        {
            "html_url": "https://github.com/SparkDevNetwork/Rock",
            "full_name": "SparkDevNetwork/Rock",
            "description": "Rock RMS",
            "pushed_at": "2026-05-27T00:00:00Z",
            "default_branch": "develop",
            "language": "C#",
            "license": {"spdx_id": "NOASSERTION"},
        },
    )
    assert record["repo"] == "SparkDevNetwork/Rock"
    assert record["default_branch"] == "develop"
    assert record["publishability_status"] == "license-gated"


def test_community_recipe_normalization():
    source = get_source("rock_recipes")
    html = (FIXTURES / "html" / "community_recipe.html").read_text()
    record = normalize_community_fetch(
        source,
        {
            "url": "https://community.rockrms.com/recipes/543",
            "status_code": 200,
            "content_hash": "abc",
            "content": html,
        },
    )
    assert record is not None
    assert record["source_title"] == "Manually Removing Plugins"
    assert record["detail_type"] == "recipe"
    assert "18" in record["rock_versions"]
    assert record["recipe_id"] == 543
    assert record["author"] is None or isinstance(record["author"], str)
    assert record["community_notice"].startswith("Community recipe")
    assert record["citations"][0]["url"] == "https://community.rockrms.com/recipes/543"


def test_triumph_content_body_normalization():
    source = get_source("triumph_resources")
    html = """
<html><head><title>GitHub Spotlight | Triumph Tech</title></head>
<body><div itemprop="mainEntityOfPage"><h1>GitHub Spotlight</h1><div class="content-body">
<p>Here is what is new in Rock GitHub.</p><h2>v20 Highlights</h2>
<ul><li>Improved Group Sync performance.</li></ul>
</div></div></body></html>
"""
    record = normalize_community_fetch(
        source,
        {
            "url": "https://www.triumph.tech/resources/github-spotlight",
            "status_code": 200,
            "content_hash": "abc",
            "content": html,
        },
    )

    assert record is not None
    assert "Improved Group Sync performance" in record["excerpt"]
    assert record["source_id"] == "triumph_resources"


def test_community_missing_recipe_is_skipped():
    source = get_source("rock_recipes")
    record = normalize_community_fetch(
        source,
        {
            "url": "https://community.rockrms.com/recipes/100",
            "status_code": 200,
            "content": "<html><title>New Recipe</title><body>That recipe does not exist.</body></html>",
        },
    )
    assert record is None


def test_community_url_candidate_filtering():
    source = get_source("rock_recipes")
    assert is_html_candidate("https://community.rockrms.com/recipes/543", source)
    assert not is_html_candidate("https://community.rockrms.com/GetImage.ashx?id=1", source)
    assert not is_html_candidate("https://community.rockrms.com/ask/using/2872", source)


def test_triumph_url_candidate_filtering():
    source = get_source("triumph_resources")
    assert is_html_candidate("https://www.triumph.tech/resources/github-spotlight-5212026", source)
    assert is_html_candidate("https://www.triumph.tech/resources/page/2", source)
    assert not is_html_candidate("https://www.triumph.tech/services", source)
