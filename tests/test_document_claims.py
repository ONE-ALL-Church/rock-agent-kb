import json
from pathlib import Path

import pytest

import rock_kb.document_claims as document_claims
from rock_kb.jsonl import read_jsonl, write_jsonl


def documentation_record(record_id: str, path: str, title: str, summary: str) -> dict:
    return {
        "id": record_id,
        "source_id": "rock_documentation",
        "source_url": f"https://community.rockrms.com/{path}",
        "source_title": title,
        "summary": summary,
        "excerpt": summary,
        "content_hash": "a" * 64,
        "documentation_path": path,
        "documentation_branch": "documentation/core-concepts/documents",
        "documentation_branches": [
            "documentation/core-concepts/documents",
            path,
        ],
        "documentation_article_id": 100,
        "documentation_current_version": "v19.0",
        "documentation_table_of_contents_link_count": 0,
        "topics": ["documents"],
        "needs_review": False,
        "license_status": "public_rights_reserved",
        "allowed_extraction_mode": "cite_and_summarize",
    }


def test_build_document_claim_candidates_uses_full_text_and_stable_source_hash(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_documentation:test",
        "documentation/core-concepts/documents/electronic-signatures",
        "Electronic Signatures",
        "Electronic signature requests connect a generated document to a signer and retain the resulting signed document.",
    )
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    result = document_claims.build_document_claim_candidates(
        concept_ids=["documents-signatures"],
        limit_per_concept=1,
        output_path=output,
        records=[record],
        context_loader=lambda _record: "Full API article text describing signature requests, signer completion, and retained signed documents.",
    )
    row = next(read_jsonl(output))

    assert result["candidate_count"] == 1
    assert result["full_text_candidates"] == 1
    assert row["source_context_mode"] == "rockumentation_full_text"
    assert row["source_input_hash"] == document_claims.sha256_text(row["source_context"])
    assert row["concept_ids"] == ["documents-signatures"]


def test_build_document_claim_candidates_allows_concepts_without_path_constraints(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_documentation:rest-api-integration",
        "documentation/automation/rest-api-integration",
        "REST API Integration",
        "Rock API integrations should preserve authorization and use supported endpoints for bounded automation.",
    )
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    result = document_claims.build_document_claim_candidates(
        concept_ids=["api-integrations"],
        limit_per_concept=1,
        output_path=output,
        records=[record],
        context_loader=lambda _record: (
            "This full official article explains how Rock REST API integrations "
            "authenticate, authorize requests, and use supported endpoints."
        ),
    )

    assert result["candidate_count"] == 1
    assert next(read_jsonl(output))["concept_ids"] == ["api-integrations"]


def test_explicit_source_record_bypasses_automatic_path_constraint(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_documentation:signup-security",
        "documentation/engagement/sign-ups/configure-sign-up-permissions",
        "Configure Sign-Up Permissions",
        "Sign-Up projects can grant role-based permissions through explicit security settings.",
    )
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    result = document_claims.build_document_claim_candidates(
        concept_ids=["security-permissions"],
        limit_per_concept=1,
        output_path=output,
        records=[record],
        source_record_ids=[record["id"]],
        context_loader=lambda _record: (
            "This official article documents the permissions required to create, "
            "edit, and administer Sign-Up projects and attendees."
        ),
    )

    assert result["candidate_count"] == 1
    assert next(read_jsonl(output))["concept_ids"] == ["security-permissions"]


def test_explicit_source_records_bypass_per_concept_limit(monkeypatch, tmp_path: Path):
    records = [
        documentation_record(
            f"rock_documentation:exact-{index}",
            f"documentation/core-concepts/documents/exact-{index}",
            f"Exact Article {index}",
            "This official article contains enough source context for exact selection.",
        )
        for index in (1, 2, 3)
    ]
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    result = document_claims.build_document_claim_candidates(
        concept_ids=["documents-signatures"],
        limit_per_concept=1,
        output_path=output,
        records=records,
        source_record_ids=[record["id"] for record in records[:2]],
        context_loader=lambda record: (
            f"Full official text for {record['source_title']} explains a distinct "
            "document workflow with enough detail for source-native review."
        ),
    )

    assert result["candidate_count"] == 2
    assert {row["source_record_id"] for row in read_jsonl(output)} == {
        record["id"] for record in records[:2]
    }


def test_explicit_source_record_ids_accepts_all_known_ids(monkeypatch, tmp_path: Path):
    records = [
        documentation_record(
            f"rock_documentation:known-{index}",
            f"documentation/core-concepts/documents/known-{index}",
            f"Known Article {index}",
            "This official article contains enough source context for exact selection.",
        )
        for index in (1, 2)
    ]
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    result = document_claims.build_document_claim_candidates(
        concept_ids=["documents-signatures"],
        limit_per_concept=1,
        output_path=output,
        records=records,
        source_record_ids=[record["id"] for record in records],
        context_loader=lambda record: f"Full official text for {record['source_title']} with sufficient detail for review.",
    )

    assert result["candidate_count"] == 2


def test_explicit_source_record_ids_reject_any_unknown_id(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_documentation:known",
        "documentation/core-concepts/documents/known",
        "Known Article",
        "This official article contains enough source context for exact selection.",
    )
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    with pytest.raises(ValueError, match="Unknown source_record_ids: rock_documentation:missing"):
        document_claims.build_document_claim_candidates(
            concept_ids=["documents-signatures"],
            limit_per_concept=1,
            output_path=tmp_path / "candidates.jsonl",
            records=[record],
            source_record_ids=[record["id"], "rock_documentation:missing"],
            context_loader=lambda _record: "Full official text with sufficient detail for review.",
        )


def test_explicit_source_record_ids_reject_source_family_mismatch(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_community_blog:wrong-family",
        "blog/rock-documentation-reference",
        "Wrong Source Family",
        "This record exists but belongs to a different source family than the requested documentation source.",
    )
    record["source_id"] = "rock_community_blog"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})

    with pytest.raises(
        ValueError,
        match="source_record_ids outside allowed source_ids: rock_community_blog:wrong-family",
    ):
        document_claims.build_document_claim_candidates(
            concept_ids=["documents-signatures"],
            limit_per_concept=1,
            output_path=tmp_path / "candidates.jsonl",
            records=[record],
            source_ids=["rock_documentation"],
            source_record_ids=[record["id"]],
            context_loader=lambda _record: "Full source text with sufficient detail for review.",
        )


def test_build_document_claim_candidates_skips_truncated_full_article(monkeypatch, tmp_path: Path):
    record = documentation_record(
        "rock_documentation:test-long",
        "documentation/core-concepts/documents/long-article",
        "Long Document Article",
        "A sufficiently descriptive summary for selecting this official document article for claim review.",
    )
    output = tmp_path / "candidates.jsonl"
    monkeypatch.setattr(document_claims, "existing_claims_by_concept", lambda: {})
    monkeypatch.setattr(document_claims, "MAX_SOURCE_CONTEXT_CHARS", 40)

    result = document_claims.build_document_claim_candidates(
        concept_ids=["documents-signatures"],
        limit_per_concept=1,
        output_path=output,
        records=[record],
        context_loader=lambda _record: "This API article is longer than the configured full-article review boundary.",
    )

    assert result["candidate_count"] == 0
    assert result["skipped"][0]["reason"] == "rockumentation_full_text_exceeds_review_limit"


def test_promote_document_claim_rewrite_builds_public_safe_review(monkeypatch, tmp_path: Path):
    candidate_path = tmp_path / "candidates.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    output_path = tmp_path / "reviews.jsonl"
    source_context = "The article explains how a signature request links a generated document to a signer and stores the completed result."
    source_hash = document_claims.sha256_text(source_context)
    candidate = {
        "schema": "rock-kb-document-claim-candidate-v1",
        "id": "document-claim-candidate:test",
        "source_record_id": "rock_documentation:test",
        "source_id": "rock_documentation",
        "source_url": "https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures",
        "source_title": "Electronic Signatures",
        "concept_ids": ["documents-signatures"],
        "documentation_path": "documentation/core-concepts/documents/electronic-signatures",
        "documentation_article_id": 100,
        "documentation_current_version": "v19.0",
        "normalized_content_hash": "a" * 64,
        "source_input_hash": source_hash,
        "source_context": source_context,
    }
    rewrite = {
        "schema": "rock-kb-document-claim-rewrite-v1",
        "candidate_id": candidate["id"],
        "source_input_hash": source_hash,
        "claims": [
            {
                "claim": "A Rock signature request associates a generated document with its signer and preserves the completed signed result.",
                "claim_type": "behavior",
                "evidence_class": "current_behavior",
                "temporal_status": "current",
                "rock_versions": ["19.0"],
                "version_scope_status": "scoped",
                "needs_live_verification": False,
            }
        ],
    }
    write_jsonl(candidate_path, [candidate])
    write_jsonl(rewrite_path, [rewrite])
    monkeypatch.setattr(document_claims, "approved_claim_rows", lambda: [])

    result = document_claims.promote_document_claim_rewrites(
        candidate_path,
        rewrite_path,
        output_path=output_path,
        reviewer="test-reviewer",
        model="gpt-test",
    )
    row = next(read_jsonl(output_path))
    public_claim = document_claims.source_claim_review_to_claim(row)

    assert result["promoted_claim_count"] == 1
    assert result["next_command"] == "uv run kb build --stage claims --force"
    assert row["generation_provenance"]["model"] == "gpt-test"
    assert row["safe_evidence_hash"] == source_hash
    assert row["version_scope_status"] == "scoped"
    assert row["rock_versions"] == ["19.0"]
    assert "source_context" not in json.dumps(row)
    assert public_claim["evidence_class"] == "current_behavior"
    assert public_claim["temporal_status"] == "current"
    assert public_claim["version_scope_status"] == "scoped"
    assert public_claim["derived_from"]["candidate_id"] == candidate["id"]


def test_promote_document_claim_rewrite_rejects_source_hash_mismatch(monkeypatch, tmp_path: Path):
    candidate_path = tmp_path / "candidates.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    candidate = {
        "id": "document-claim-candidate:test",
        "source_input_hash": "a" * 64,
        "source_context": "Private candidate context that must not leak.",
    }
    write_jsonl(candidate_path, [candidate])
    write_jsonl(
        rewrite_path,
        [
            {
                "candidate_id": candidate["id"],
                "source_input_hash": "b" * 64,
                "claims": [{"claim": "This sufficiently long claim should never be promoted because the source hash is wrong."}],
            }
        ],
    )
    monkeypatch.setattr(document_claims, "approved_claim_rows", lambda: [])

    with pytest.raises(ValueError, match="source_input_hash does not match"):
        document_claims.promote_document_claim_rewrites(candidate_path, rewrite_path, output_path=tmp_path / "reviews.jsonl")


def test_developer_documentation_version_is_not_treated_as_rock_version():
    candidate = {
        "source_id": "rock_developer",
        "documentation_current_version": "1.0.0",
    }

    assert document_claims.normalized_rock_versions(candidate, {}) == []
    assert document_claims.normalized_rock_versions(candidate, {"rock_versions": ["19.0"]}) == ["19.0"]
    assert document_claims.normalized_rock_versions(
        {"source_id": "rock_documentation", "documentation_current_version": "v19.0"},
        {},
    ) == []
    assert document_claims.normalized_version_scope_status({}, []) == "unprocessed"
    assert document_claims.normalized_version_scope_status({"version_scope_status": "version_independent"}, []) == "version_independent"
    with pytest.raises(ValueError, match="version_scope_status must be"):
        document_claims.normalized_version_scope_status({"version_scope_status": "scoped"}, [])


def test_promote_document_claim_rewrite_accepts_reviewed_candidate_with_no_claims(monkeypatch, tmp_path: Path):
    candidate_path = tmp_path / "candidates.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    output_path = tmp_path / "reviews.jsonl"
    source_hash = "a" * 64
    candidate = {
        "id": "document-claim-candidate:no-claim",
        "source_input_hash": source_hash,
        "source_context": "A navigational article without durable operational knowledge.",
    }
    write_jsonl(candidate_path, [candidate])
    write_jsonl(
        rewrite_path,
        [
            {
                "schema": "rock-kb-document-claim-rewrite-v1",
                "candidate_id": candidate["id"],
                "source_input_hash": source_hash,
                "claims": [],
                "review_notes": ["Full article reviewed; no non-duplicate durable claim found."],
            }
        ],
    )
    monkeypatch.setattr(document_claims, "approved_claim_rows", lambda: [])

    result = document_claims.promote_document_claim_rewrites(
        candidate_path,
        rewrite_path,
        output_path=output_path,
    )

    assert result["reviewed_candidate_count"] == 1
    assert result["promoted_candidate_count"] == 0
    assert result["promoted_claim_count"] == 0
    assert list(read_jsonl(output_path)) == []


def test_promote_document_claim_rewrite_is_idempotent_for_same_candidate(monkeypatch, tmp_path: Path):
    candidate_path = tmp_path / "candidates.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    output_path = tmp_path / "reviews.jsonl"
    source_context = "The source describes a reusable operational behavior in sufficient detail."
    source_hash = document_claims.sha256_text(source_context)
    candidate = {
        "id": "document-claim-candidate:idempotent",
        "source_input_hash": source_hash,
        "source_context": source_context,
        "concept_ids": ["documents-signatures"],
        "source_id": "rock_documentation",
        "source_record_id": "rock_documentation:test-idempotent",
        "source_url": "https://community.rockrms.com/documentation/core-concepts/documents/idempotent",
        "source_title": "Idempotent Promotion",
        "documentation_current_version": "v19.0",
    }
    claim_text = "This sufficiently detailed claim can be safely promoted again for the exact same reviewed candidate."
    write_jsonl(candidate_path, [candidate])
    write_jsonl(
        rewrite_path,
        [
            {
                "candidate_id": candidate["id"],
                "source_input_hash": source_hash,
                "claims": [{"claim": claim_text, "claim_type": "behavior"}],
            }
        ],
    )
    monkeypatch.setattr(
        document_claims,
        "approved_claim_rows",
        lambda: [
            {
                "claim": claim_text,
                "derived_from": {"candidate_id": candidate["id"]},
            }
        ],
    )

    result = document_claims.promote_document_claim_rewrites(
        candidate_path,
        rewrite_path,
        output_path=output_path,
    )

    assert result["promoted_claim_count"] == 1


def test_candidate_selection_reserves_subguide_coverage():
    concept = document_claims.get_concept("engagement-tracking")
    eligible = [
        (
            1_100 - index,
            path,
            {
                "id": f"record:{index}",
                "documentation_path": path,
                "documentation_branches": [branch],
                "source_title": title,
                "summary": title,
            },
        )
        for index, (path, branch, title) in enumerate(
            [
                ("documentation/engagement/steps/configure", "documentation/engagement/steps", "Configure Steps"),
                ("documentation/engagement/steps/types", "documentation/engagement/steps", "Step Types"),
                ("documentation/engagement/streaks/types", "documentation/engagement/streaks", "Streak Types"),
                ("documentation/engagement/assessments/types", "documentation/engagement/assessments", "Assessment Types"),
                (
                    "documentation/engagement/additional-engagement-tools/achievements/types",
                    "documentation/engagement/additional-engagement-tools",
                    "Achievement Types",
                ),
            ]
        )
    ]

    selected = document_claims.reserve_subguide_coverage(concept, eligible, 4)
    paths = [item[1] for item in selected]

    assert any("/steps/" in path for path in paths)
    assert any("/streaks/" in path for path in paths)
    assert any("/assessments/" in path for path in paths)
    assert any("/additional-engagement-tools/" in path for path in paths)


def test_candidate_selection_reserves_exact_source_record_subguide_before_keywords():
    concept = type("Concept", (), {"subguides": [{"source_record_ids": ["record:exact"], "keywords": ["steps"]}]})()
    eligible = [
        (
            1_100,
            "documentation/engagement/steps/keyword-match",
            {
                "id": "record:keyword",
                "documentation_path": "documentation/engagement/steps/keyword-match",
                "source_title": "Configure Steps",
                "summary": "Configure steps",
            },
        ),
        (
            1_000,
            "documentation/other/exact",
            {
                "id": "record:exact",
                "documentation_path": "documentation/other/exact",
                "source_title": "Exact Source Record",
                "summary": "A source record selected by exact ID.",
            },
        ),
    ]

    selected = document_claims.reserve_subguide_coverage(concept, eligible, 1)

    assert [item[2]["id"] for item in selected] == ["record:exact"]
    assert not document_claims.record_matches_subguide(eligible[0][2], concept.subguides[0])


def test_subguide_exact_source_records_are_additive_with_branches():
    subguide = {
        "source_record_ids": ["record:exact"],
        "documentation_branches": ["documentation/supporting-rock/caching"],
        "keywords": ["navigate"],
    }
    exact = {
        "id": "record:exact",
        "documentation_branch": "documentation/getting-started",
    }
    branch = {
        "id": "record:cache",
        "documentation_branch": "documentation/supporting-rock/caching",
    }
    unrelated = {
        "id": "record:unrelated",
        "documentation_branch": "documentation/church-management/groups",
        "source_title": "Navigate unrelated content",
    }

    assert document_claims.record_matches_subguide(exact, subguide)
    assert document_claims.record_matches_subguide(branch, subguide)
    assert not document_claims.record_matches_subguide(unrelated, subguide)
