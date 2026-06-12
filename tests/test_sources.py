from rock_kb.extract import canonicalize_url, choose_extraction_tier
from rock_kb.sources import get_source, load_sources, validate_registry


def test_registry_is_valid():
    assert validate_registry() == []
    assert len(load_sources()) >= 10
    assert all(source.public_publish_mode for source in load_sources())
    assert all(source.allowed_excerpt_chars >= 0 for source in load_sources())


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
