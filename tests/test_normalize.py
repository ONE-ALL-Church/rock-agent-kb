from pathlib import Path

from rock_kb.community import (
    developer_slug_from_url,
    documentation_slug_from_url,
    is_html_candidate,
    normalize_community_fetch,
    rockumentation_readable_text,
    rockumentation_book_api_url,
)
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


def test_rockumentation_slug_and_api_url_helpers():
    assert (
        documentation_slug_from_url("https://community.rockrms.com/documentation/core-concepts/workflows?Version=v19.0")
        == "core-concepts/workflows"
    )
    assert documentation_slug_from_url("https://community.rockrms.com/documentation") is None
    assert documentation_slug_from_url("https://community.rockrms.com/documentation/bookcontent/1/358") is None
    assert developer_slug_from_url("https://community.rockrms.com/developer/mobile-docs/app-factory") == "mobile-docs/app-factory"
    assert developer_slug_from_url("https://community.rockrms.com/developer") is None

    api_url = rockumentation_book_api_url("core-concepts/workflows/workflow-actions/people")

    assert "RefreshObsidianBlockInitialization" in api_url
    assert "slug=core-concepts%2Fworkflows%2Fworkflow-actions%2Fpeople" in api_url


def test_rock_documentation_normalizes_rockumentation_payload():
    source = get_source("rock_documentation")
    payload = {
        "configurationValues": {
            "title": "People",
            "slug": "people",
            "currentVersion": "v19.0",
            "versionId": 32,
            "versions": [
                {
                    "value": "/documentation/core-concepts/workflows/workflow-actions/people",
                    "text": "v19.0",
                    "category": None,
                    "disabled": None,
                }
            ],
            "tableOfContents": """
                <ul>
                  <li data-article-id="850" class="tree-item">
                    <span class="title"><a href="/documentation/core-concepts/workflows">Workflows</a></span>
                    <ul>
                      <li data-article-id="2647" class="tree-item trailblazer">
                        <span class="title"><a href="/documentation/core-concepts/workflows/workflow-actions/people">People</a></span>
                      </li>
                    </ul>
                  </li>
                </ul>
            """,
            "pageId": 3803,
            "entityGuid": "7dc9d697-b973-443e-adcf-785db4ae33ad",
            "entityTypeGuid": "8ca33e3f-60f5-4d29-977c-325b824c43a4",
            "isSearchable": True,
        },
        "initialContent": """
            <div>
              <div class="book-toc"><a href="/documentation/core-concepts">Core Concepts</a></div>
              <article class="rockumentation-article" data-main-article="true" data-article-id="2647">
                <h1>Family Inactivate</h1>
                <p>Inactivates a given person's entire family.</p>
                <a href="/documentation/core-concepts/workflows">Workflows</a>
              </article>
            </div>
        """,
    }

    record = normalize_community_fetch(
        source,
        {
            "url": "https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/people",
            "status_code": 200,
            "content_hash": "abc",
            "content": payload["initialContent"],
            "rockumentation_payload": payload,
            "extraction_tool": "rockumentation_block_action",
        },
    )

    assert record is not None
    assert record["id"] == "rock_documentation:article:2647"
    assert record["source_title"] == "People"
    assert record["detail_type"] == "documentation_article"
    assert record["extraction_tool"] == "rockumentation_block_action"
    assert record["documentation_article_id"] == 2647
    assert record["documentation_article_key"] == "documentation:2647"
    assert record["documentation_family"] == "documentation"
    assert record["documentation_path_parts"] == ["core-concepts", "workflows", "workflow-actions", "people"]
    assert record["documentation_path"] == "documentation/core-concepts/workflows/workflow-actions/people"
    assert record["documentation_branch"] == "documentation/core-concepts/workflows"
    assert record["documentation_branches"] == [
        "documentation/core-concepts",
        "documentation/core-concepts/workflows",
        "documentation/core-concepts/workflows/workflow-actions",
        "documentation/core-concepts/workflows/workflow-actions/people",
    ]
    assert record["documentation_parent_slugs"] == [
        "core-concepts",
        "core-concepts/workflows",
        "core-concepts/workflows/workflow-actions",
    ]
    assert record["documentation_current_version"] == "v19.0"
    assert record["documentation_version_id"] == 32
    assert record["documentation_versions"][0]["text"] == "v19.0"
    assert record["documentation_version_links"][0]["url"] == "https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/people"
    assert record["documentation_page_id"] == 3803
    assert record["documentation_entity_guid"] == "7dc9d697-b973-443e-adcf-785db4ae33ad"
    assert record["documentation_is_searchable"] is True
    assert record["documentation_table_of_contents_link_count"] == 2
    assert record["documentation_table_of_contents_links"][1]["trailblazer"] is True
    assert record["documentation_table_of_contents_links"][1]["parent_article_id"] == 850
    assert record["documentation_table_of_contents_links"][1]["depth"] == 1
    assert "Inactivates a given person's entire family" in record["excerpt"]
    assert "Core Concepts" not in record["excerpt"]


def test_rock_developer_normalizes_rockumentation_payload():
    source = get_source("rock_developer")
    payload = {
        "configurationValues": {
            "title": "App Factory",
            "slug": "app-factory",
            "currentVersion": "1.0.0",
            "versionId": 23,
            "versions": [
                {
                    "value": "/developer/mobile-docs/app-factory",
                    "text": "1.0.0",
                    "category": None,
                    "disabled": None,
                }
            ],
            "tableOfContents": """
                <ul>
                  <li data-article-id="2721" class="tree-item trailblazer">
                    <span class="title"><a href="/developer/mobile-docs/app-factory">App Factory</a></span>
                  </li>
                </ul>
            """,
            "pageId": 3803,
            "entityGuid": "b64d7f5a-853a-42e5-8b62-b6f0ee81ec10",
            "entityTypeGuid": "8ca33e3f-60f5-4d29-977c-325b824c43a4",
            "isSearchable": True,
        },
        "initialContent": """
            <div>
              <div class="book-toc"><a href="/developer/mobile-docs">Mobile Docs</a></div>
              <article class="rockumentation-article" data-main-article="true" data-article-id="2721">
                <h1>App Factory</h1>
                <p>Package and publish Rock Mobile applications.</p>
                <code>public class MobileShell</code>
              </article>
            </div>
        """,
    }

    record = normalize_community_fetch(
        source,
        {
            "url": "https://community.rockrms.com/developer/mobile-docs/app-factory",
            "status_code": 200,
            "content_hash": "abc",
            "content": payload["initialContent"],
            "rockumentation_payload": payload,
            "extraction_tool": "rockumentation_block_action",
        },
    )

    assert record is not None
    assert record["id"] == "rock_developer:article:2721"
    assert record["source_title"] == "App Factory"
    assert record["detail_type"] == "developer_doc"
    assert record["developer_doc_path"] == ["mobile-docs", "app-factory"]
    assert record["documentation_article_id"] == 2721
    assert record["documentation_article_key"] == "developer:2721"
    assert record["documentation_family"] == "developer"
    assert record["documentation_slug"] == "mobile-docs/app-factory"
    assert record["documentation_path"] == "developer/mobile-docs/app-factory"
    assert record["documentation_branch"] == "developer/mobile-docs"
    assert record["documentation_branches"] == ["developer/mobile-docs", "developer/mobile-docs/app-factory"]
    assert record["documentation_version_links"][0]["url"] == "https://community.rockrms.com/developer/mobile-docs/app-factory"
    assert record["documentation_table_of_contents_links"][0]["url"] == "https://community.rockrms.com/developer/mobile-docs/app-factory"
    assert "Package and publish Rock Mobile applications" in record["excerpt"]
    assert "Mobile Docs" not in record["excerpt"]


def test_rock_developer_excludes_dedicated_mobile_source_urls():
    source = get_source("rock_developer")

    assert is_html_candidate("https://community.rockrms.com/developer/helix", source)
    assert not is_html_candidate("https://community.rockrms.com/developer/mobile-docs/app-factory", source)
    assert not is_html_candidate("https://community.rockrms.com/lava/commands/sql-commands", source)


def test_rockumentation_readable_text_strips_decorative_images():
    payload = {
        "initialContent": """
            <article class="rockumentation-article" data-main-article="true" data-article-id="188">
              <p><img src="/GetImage.ashx?Id=67647" alt="&lt;br&gt;" /></p>
              <h2>Welcome</h2>
              <p><i class="ti ti-gift"></i> Rock Mobile is a native mobile extension of Rock RMS.</p>
            </article>
        """
    }

    text = rockumentation_readable_text(payload)

    assert not text.startswith("![")
    assert "ti ti-gift" not in text
    assert "Rock Mobile is a native mobile extension" in text


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


def test_rock_community_site_excludes_urls_owned_by_narrower_sources():
    source = get_source("rock_community_site")

    excluded_urls = [
        "https://community.rockrms.com/api-docs",
        "https://community.rockrms.com/ask/using/2872",
        "https://community.rockrms.com/community-hubs/administrators",
        "https://community.rockrms.com/developer/helix",
        "https://community.rockrms.com/developer/mobile-docs/app-factory",
        "https://community.rockrms.com/documentation/core-concepts/workflows",
        "https://community.rockrms.com/lava/commands/sql-commands",
        "https://community.rockrms.com/recipes/543",
        "https://community.rockrms.com/rocku/workflows/workflow-basics",
    ]

    for url in excluded_urls:
        assert not is_html_candidate(url, source), url

    residual_urls = [
        "https://community.rockrms.com/learn",
        "https://community.rockrms.com/podcast",
        "https://community.rockrms.com/styling",
    ]

    for url in residual_urls:
        assert is_html_candidate(url, source), url

    assert not is_html_candidate("https://community.rockrms.com/subscriptions", source)


def test_triumph_url_candidate_filtering():
    source = get_source("triumph_resources")
    assert is_html_candidate("https://www.triumph.tech/resources/github-spotlight-5212026", source)
    assert is_html_candidate("https://www.triumph.tech/resources/page/2", source)
    assert not is_html_candidate("https://www.triumph.tech/services", source)
