import json

import rock_kb.claims as claims_module
from rock_kb.claims import build_approved_claims, claim_usefulness_metadata, validate_claim_file, validate_claim_rows
from rock_kb.jsonl import read_jsonl


def test_build_approved_claims_from_media_public_promotions(monkeypatch, tmp_path):
    review_dir = tmp_path / "review"
    claims_dir = tmp_path / "claims"
    promotions_dir = review_dir / "public-media-promotions"
    promotions_dir.mkdir(parents=True)
    monkeypatch.setattr(claims_module, "REVIEW_DIR", review_dir)
    monkeypatch.setattr(claims_module, "SOURCE_CLAIM_REVIEWS_DIR", review_dir / "source-claim-reviews")
    monkeypatch.setattr(claims_module, "APPROVED_CLAIMS_PATH", claims_dir / "approved-claims.jsonl")
    monkeypatch.setattr(claims_module, "CLAIM_EXPORT_REPORT_PATH", claims_dir / "claim-export-report.json")

    promotion = {
        "id": "media-public-promotion:abc",
        "candidate_id": "media-public-candidate:abc",
        "source_id": "rock_community_hubs",
        "source_kind": "rock_community_hubs",
        "source_record_id": "rock_community_hubs:abc",
        "source_url": "https://community.rockrms.com/community-hubs/example",
        "source_title": "Community Hub Example",
        "media_id": "media:abc",
        "media_url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret",
        "transcript_hash": "hash123",
        "review_status": "approved_for_public_distillation",
        "reviewed_at": "2026-06-06T00:00:00+00:00",
        "concept_ids": ["communications"],
        "summary": "Reviewed community material recommends checking audience reach by communication medium before sending.",
        "key_insights": [
            {
                "topic": "communications",
                "insight": "The communication wizard material is useful for planning email and SMS sends, but it should be treated as community-derived guidance.",
                "source_url": "https://community.rockrms.com/community-hubs/example",
            }
        ],
        "citations": [{"source_id": "rock_community_hubs", "url": "https://community.rockrms.com/community-hubs/example"}],
    }
    (promotions_dir / "rock_community_hubs.media-public-promotions.jsonl").write_text(json.dumps(promotion) + "\n", encoding="utf-8")

    result = build_approved_claims()
    rows = list(read_jsonl(claims_dir / "approved-claims.jsonl"))
    errors = validate_claim_file(claims_dir / "approved-claims.jsonl")

    assert result["claim_count"] == 2
    assert not errors
    assert {row["authority_tier"] for row in rows} == {"community-reviewed"}
    assert all("media_url" not in json.dumps(row) for row in rows)
    assert rows[0]["source_refs"][0]["url"] == "https://community.rockrms.com/community-hubs/example"
    assert all("private_corpus_pointer" not in row for row in rows)
    assert all("operational_priority" in row for row in rows)
    assert all("answer_candidate" in row for row in rows)
    assert all("claim_tier" in row for row in rows)
    assert {row["claim_tier"] for row in rows} == {"source_backed", "routing_context_only"}
    assert all("primary_concept_id" in row for row in rows)
    assert rows[0]["primary_concept_id"] == "communications"


def test_validate_claim_rows_loads_known_concepts_once(monkeypatch):
    row = next(read_jsonl(claims_module.APPROVED_CLAIMS_PATH))
    calls = {"count": 0}

    def known_concepts():
        calls["count"] += 1
        return set(row["concept_ids"])

    monkeypatch.setattr(claims_module, "load_known_concept_ids", known_concepts)

    assert validate_claim_rows([dict(row), dict(row)]) == [f"claim:2 duplicate claim_id {row['claim_id']}"]
    assert calls["count"] == 1


def test_episode_routing_claims_do_not_enter_live_verification_queue():
    row = {
        "claim": "When applying reporting, analytics, and measurement ideas from Episode 32, convert the episode context into source-backed Rock guidance and verify current-version behavior before acting.",
        "claim_type": "operational_guidance",
        "authority_tier": "community-reviewed",
        "needs_live_verification": True,
    }

    metadata = claim_usefulness_metadata(row)
    row.update(metadata)

    assert metadata["answer_candidate"] is False
    assert claims_module.claim_tier_for_claim(row) == "routing_context_only"


def test_build_approved_claims_from_source_claim_reviews(monkeypatch, tmp_path):
    review_dir = tmp_path / "review"
    claims_dir = tmp_path / "claims"
    source_claims_dir = review_dir / "source-claim-reviews"
    source_claims_dir.mkdir(parents=True)
    monkeypatch.setattr(claims_module, "REVIEW_DIR", review_dir)
    monkeypatch.setattr(claims_module, "SOURCE_CLAIM_REVIEWS_DIR", source_claims_dir)
    monkeypatch.setattr(claims_module, "APPROVED_CLAIMS_PATH", claims_dir / "approved-claims.jsonl")
    monkeypatch.setattr(claims_module, "CLAIM_EXPORT_REPORT_PATH", claims_dir / "claim-export-report.json")

    review = {
        "schema": "rock-kb-source-claim-review-v1",
        "id": "source-claim:helix-overview",
        "claim": "Helix combines HTMX, Lava Applications, Lava Commands, and Control Shortcodes as a Rock web-development surface.",
        "claim_type": "source_summary",
        "concept_ids": ["helix", "developer-resources"],
        "source_refs": [
            {
                "source_id": "rock_developer",
                "url": "https://community.rockrms.com/developer/helix/overview",
                "title": "Helix Overview",
            }
        ],
        "source_record_ids": ["rock_developer:802567c280193bd0"],
        "authority_tier": "official",
        "confidence": "high",
        "review_status": "approved_for_public_distillation",
        "reviewed_at": "2026-06-09T00:00:00+00:00",
        "reviewer": "test",
    }
    (source_claims_dir / "thin-concepts.jsonl").write_text(json.dumps(review) + "\n", encoding="utf-8")

    result = build_approved_claims()
    rows = list(read_jsonl(claims_dir / "approved-claims.jsonl"))
    errors = validate_claim_file(claims_dir / "approved-claims.jsonl")

    assert result["claim_count"] == 1
    assert not errors
    assert rows[0]["authority_tier"] == "official"
    assert rows[0]["source_record_ids"] == ["rock_developer:802567c280193bd0"]
    assert rows[0]["primary_concept_id"] == "helix"
    assert rows[0]["derived_from"]["type"] == "source_claim_review"


def test_claim_usefulness_metadata_prioritizes_operational_claims():
    metadata = claim_usefulness_metadata(
        {
            "claim": "Verify workflow permissions and configuration settings before launch.",
            "claim_type": "configuration",
            "authority_tier": "rocku-confirmed",
            "needs_live_verification": False,
        }
    )

    assert metadata["operational_priority"] >= 90
    assert metadata["answer_candidate"] is True
    assert metadata["requires_live_instance"] is True
    assert "permission" in metadata["common_failure_mode"]


def test_claim_usefulness_metadata_deprioritizes_source_routing_claims():
    metadata = claim_usefulness_metadata(
        {
            "claim": "This lesson provides training context and helps route agents, not as a substitute for official documentation.",
            "claim_type": "source_summary",
            "authority_tier": "rocku-confirmed",
            "needs_live_verification": False,
        }
    )

    assert metadata["answer_candidate"] is False
    assert metadata["operational_priority"] < 70


def test_live_claim_verification_overlay_promotes_claim_to_live_verified(monkeypatch, tmp_path):
    review_dir = tmp_path / "review"
    claims_dir = tmp_path / "claims"
    promotions_dir = review_dir / "public-media-promotions"
    promotions_dir.mkdir(parents=True)
    monkeypatch.setattr(claims_module, "REVIEW_DIR", review_dir)
    monkeypatch.setattr(claims_module, "LIVE_CLAIM_VERIFICATIONS_PATH", review_dir / "live-claim-verifications.jsonl")
    monkeypatch.setattr(claims_module, "SOURCE_CLAIM_REVIEWS_DIR", review_dir / "source-claim-reviews")
    monkeypatch.setattr(claims_module, "APPROVED_CLAIMS_PATH", claims_dir / "approved-claims.jsonl")
    monkeypatch.setattr(claims_module, "CLAIM_EXPORT_REPORT_PATH", claims_dir / "claim-export-report.json")

    promotion = {
        "id": "media-public-promotion:abc",
        "candidate_id": "media-public-candidate:abc",
        "source_id": "rock_community_hubs",
        "source_kind": "rock_community_hubs",
        "source_record_id": "rock_community_hubs:abc",
        "source_url": "https://community.rockrms.com/community-hubs/example",
        "source_title": "Community Hub Example",
        "media_id": "media:abc",
        "transcript_hash": "hash123",
        "review_status": "approved_for_public_distillation",
        "reviewed_at": "2026-06-06T00:00:00+00:00",
        "concept_ids": ["data-views-reports"],
        "summary": "",
        "key_insights": [
            {
                "topic": "data and reporting",
                "insight": "Data Views should be treated as reusable record-set definitions before reports decide how to display records.",
                "source_url": "https://community.rockrms.com/community-hubs/example",
            }
        ],
        "citations": [{"source_id": "rock_community_hubs", "url": "https://community.rockrms.com/community-hubs/example"}],
    }
    (promotions_dir / "rock_community_hubs.media-public-promotions.jsonl").write_text(json.dumps(promotion) + "\n", encoding="utf-8")
    result = build_approved_claims()
    rows = list(read_jsonl(claims_dir / "approved-claims.jsonl"))
    claim_id = rows[0]["claim_id"]
    (review_dir / "live-claim-verifications.jsonl").write_text(
        json.dumps(
            {
                "schema": "rock-kb-live-claim-verification-v1",
                "claim_id": claim_id,
                "claim_tier": "live_verified",
                "instance": "test",
                "verified_at": "2026-06-08T00:00:00+00:00",
                "verified_by": "test",
                "verification_method": "read_only_sql",
                "evidence_refs": [{"probe_id": "live-probe:test", "tables": ["DataView", "Report"]}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = build_approved_claims()
    rows = list(read_jsonl(claims_dir / "approved-claims.jsonl"))

    assert result["claim_count"] == 1
    assert rows[0]["claim_tier"] == "live_verified"
    assert rows[0]["needs_live_verification"] is False
    assert rows[0]["live_verification"]["verification_method"] == "read_only_sql"
    assert "path" not in json.dumps(rows[0]["live_verification"])


def test_live_claim_verification_supplements_override_base_rows(monkeypatch, tmp_path):
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    verification_path = review_dir / "live-claim-verifications.jsonl"
    verification_path.write_text(
        json.dumps(
            {
                "schema": "rock-kb-live-claim-verification-v1",
                "claim_id": "claim:changed",
                "claim_tier": "live_verified",
                "instance": "test",
                "verified_at": "2026-06-09T00:00:00+00:00",
                "verified_by": "test",
                "verification_method": "read_only_sql",
                "evidence_refs": [{"probe_id": "live-probe:test", "tables": ["DataView"]}],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (review_dir / "live-claim-verifications-2026-06-10.jsonl").write_text(
        json.dumps(
            {
                "schema": "rock-kb-live-claim-verification-v1",
                "claim_id": "claim:changed",
                "claim_tier": "routing_context_only",
                "instance": "review-overlay",
                "verified_at": "2026-06-10T00:00:00+00:00",
                "verified_by": "codex-review",
                "verification_method": "reviewer_tier_triage",
                "evidence_refs": [],
                "notes": ["Later review found the SQL evidence only verified a related surface."],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(claims_module, "LIVE_CLAIM_VERIFICATIONS_PATH", verification_path)

    rows = claims_module.load_live_claim_verifications()

    assert rows["claim:changed"]["claim_tier"] == "routing_context_only"
    assert rows["claim:changed"]["verified_by"] == "codex-review"
