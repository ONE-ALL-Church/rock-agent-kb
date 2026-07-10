import json

from rock_kb.cli._legacy import source_urls_from_snapshot
from rock_kb.extract import canonicalize_url, choose_extraction_tier
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


def test_extraction_tier_escalates_for_crawl4ai():
    source = get_source("rock_mobile_docs")
    assert choose_extraction_tier(source) == 2


def test_private_source_policy_is_private_only():
    source = get_source("private_rock_repo_candidates")
    assert source.public_publish_mode == "private_only"
    assert source.requires_human_review is True
    assert source.allowed_excerpt_chars == 0
