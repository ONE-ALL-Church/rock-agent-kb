import json

from bs4 import BeautifulSoup

from rock_kb.cli._legacy import deduplicate_source_records, deduplicate_urls, source_urls_from_snapshot
from rock_kb.community import lava_elements_from_page, readable_title
from rock_kb.extract import canonicalize_url, choose_extraction_tier, main_markdown
from rock_kb.sources import get_source, load_sources, validate_registry


def test_registry_is_valid():
    assert validate_registry() == []
    assert len(load_sources()) >= 10
    assert all(source.public_publish_mode for source in load_sources())
    assert all(source.allowed_excerpt_chars >= 0 for source in load_sources())


def test_source_snapshot_urls_are_grouped_for_refresh_seeding(tmp_path):
    snapshot = tmp_path / "source-snapshot.json"
    snapshot.write_text(
        json.dumps(
            {
                "source_records": {
                    "record:one": {
                        "source_id": "rock_recipes",
                        "source_url": "https://community.rockrms.com/recipes/107/older-recipe",
                    },
                    "record:two": {
                        "source_id": "triumph_resources",
                        "source_url": "https://www.triumph.tech/resources/older-article",
                    },
                }
            }
        ),
        encoding="utf-8",
    )

    urls = source_urls_from_snapshot(snapshot)

    assert urls["rock_recipes"] == {
        "https://community.rockrms.com/recipes/107/older-recipe"
    }
    assert urls["triumph_resources"] == {
        "https://www.triumph.tech/resources/older-article"
    }


def test_url_canonicalization():
    assert canonicalize_url("HTTPS://Community.RockRMS.com//developer//mobile-docs/") == "https://community.rockrms.com/developer/mobile-docs"


def test_community_refresh_urls_are_deduplicated_in_discovery_order():
    assert deduplicate_urls(["https://example.test/a", "https://example.test/b", "https://example.test/a"]) == [
        "https://example.test/a",
        "https://example.test/b",
    ]


def test_community_refresh_records_collapse_redirect_aliases():
    first = {"id": "source:one", "source_url": "https://example.test/final", "title": "First", "location_aliases": []}
    duplicate = {
        "id": "source:one",
        "source_url": "https://example.test/final",
        "title": "Duplicate",
        "location_aliases": ["https://example.test/old"],
    }
    second = {"id": "source:two", "source_url": "https://example.test/two", "title": "Second"}

    assert deduplicate_source_records([first, duplicate, second]) == [
        {**first, "location_aliases": ["https://example.test/old"]},
        second,
    ]


def test_extraction_tier_escalates_for_crawl4ai():
    source = get_source("rock_mobile_docs")
    assert choose_extraction_tier(source) == 2


def test_main_markdown_can_prefer_article_over_site_chrome():
    markdown = main_markdown(
        """
        <main>
          <nav>Documentation links</nav>
          <article><h1>Lava API</h1><p>Configure the webhook.</p></article>
          <footer>Copyright and promotions</footer>
        </main>
        """,
        prefer_article=True,
    )

    assert "Lava API" in markdown
    assert "Configure the webhook." in markdown
    assert "Documentation links" not in markdown
    assert "Copyright and promotions" not in markdown


def test_lava_command_uses_document_title_instead_of_generic_shell_heading():
    html = """
        <html>
          <head><title>SQL | Rock Community | Rock Community</title></head>
          <body>
            <h1 class="page-title">Lava Tags/Commands</h1>
            <article><h1>SQL Command</h1><p>Run a SQL query.</p></article>
          </body>
        </html>
    """
    source = get_source("rock_lava_docs")
    soup = BeautifulSoup(html, "html.parser")

    assert readable_title(html, source) == "SQL"
    assert [element["name"] for element in lava_elements_from_page(
        soup,
        "https://community.rockrms.com/lava/commands/sql-commands",
        "command",
    )] == ["SQL"]


def test_private_source_policy_is_private_only():
    source = get_source("private_rock_repo_candidates")
    assert source.public_publish_mode == "private_only"
    assert source.requires_human_review is True
    assert source.allowed_excerpt_chars == 0
