from __future__ import annotations

from datetime import datetime, timezone

from rock_kb.hybrid_shadow import (
    prepare_shadow_documents,
    score_shadow_row,
    shadow_cost_estimate,
    shadow_hits,
    shadow_item_counts,
    shadow_reconciliation_plan,
)


def test_prepare_shadow_documents_only_includes_hybrid_primary(tmp_path):
    rows = prepare_shadow_documents(
        [
            {
                "id": "claim:claim:abc",
                "text": "Rock authorization mediates access.",
                "content_hash": "a" * 64,
                "index_policy": "hybrid_primary",
                "metadata": {"kind": "claim", "concepts": "security-permissions"},
            },
            {
                "id": "model_map:stable:group",
                "text": "Group model.",
                "content_hash": "b" * 64,
                "index_policy": "exact_lexical_only",
                "metadata": {"kind": "model_map", "concepts": "model-map"},
            },
        ],
        destination=tmp_path / "manifest.jsonl",
        claim_limit=10,
    )

    assert [row["id"] for row in rows] == ["claim:claim:abc"]
    assert rows[0]["key"].endswith("-aaaaaaaaaaaa.md")
    assert rows[0]["metadata"]["kind"] == "claim"


def test_prepare_shadow_documents_keeps_non_claim_kinds_and_bounds_claims(tmp_path, monkeypatch):
    monkeypatch.setattr("rock_kb.hybrid_shadow.read_jsonl", lambda _path: [])
    documents = [
        {
            "id": f"claim:{index}",
            "kind": "claim",
            "text": f"Claim {index}",
            "index_policy": "hybrid_primary",
            "metadata": {"kind": "claim"},
        }
        for index in range(10)
    ]
    documents.append(
        {"id": "recipe:a", "kind": "recipe", "text": "Recipe", "index_policy": "hybrid_primary", "metadata": {"kind": "recipe"}}
    )

    rows = prepare_shadow_documents(documents, destination=tmp_path / "manifest.jsonl", claim_limit=3, lava_limit=3)

    assert len([row for row in rows if row["metadata"]["kind"] == "claim"]) == 3
    assert any(row["id"] == "recipe:a" for row in rows)


def test_shadow_hits_maps_item_keys_and_metadata():
    hits = shadow_hits(
        {
            "result": {
                "data": [
                    {
                        "text": "PersonAttendance is available.",
                        "score": 0.9,
                        "item": {
                            "key": "rock-kb/abc.md",
                            "metadata": {"kind": "lava_context", "concepts": "lava|check-in"},
                        },
                    }
                ]
            }
        },
        {"rock-kb/abc.md": "lava_context:abc"},
    )

    assert hits[0]["id"] == "lava_context:abc"
    assert hits[0]["concepts"] == ["lava", "check-in"]


def test_shadow_hits_supports_current_chunks_shape_and_collapses_document_chunks():
    hits = shadow_hits(
        {
            "result": {
                "chunks": [
                    {"text": "first", "item": {"key": "rock-kb/a.md", "metadata": {"kind": "concept", "concepts": "check-in"}}},
                    {"text": "second", "item": {"key": "rock-kb/a.md", "metadata": {"kind": "concept", "concepts": "check-in"}}},
                ]
            }
        },
        {"rock-kb/a.md": "concept:check-in"},
    )

    assert len(hits) == 1
    assert hits[0]["id"] == "concept:check-in"
    assert hits[0]["text"] == "first\nsecond"


def test_score_shadow_row_enforces_expected_rank_and_terms():
    result = score_shadow_row(
        {
            "id": "eval:claim",
            "question": "Should AI use direct database access?",
            "concept_id": "security-permissions",
            "expected_result_ids": ["claim:claim:abc"],
            "expected_result_kinds": ["claim"],
            "required_terms": ["authorization"],
            "max_rank": 2,
        },
        [
            {
                "id": "claim:claim:abc",
                "kind": "claim",
                "concepts": ["security-permissions"],
                "text": "Use Rock authorization.",
            }
        ],
        ["claim:claim:abc"],
        10,
    )

    assert result["status"] == "pass"
    assert result["relevant_rank"] == 1


def test_shadow_item_counts_supports_current_stats_shape():
    assert shadow_item_counts({"queued": 2, "running": 3, "completed": 10, "error": 1}) == {
        "completed": 10,
        "pending": 5,
    }


def test_shadow_reconciliation_removes_obsolete_failed_and_stuck_items():
    now = datetime(2026, 7, 17, 22, 0, tzinfo=timezone.utc)
    plan = shadow_reconciliation_plan(
        [
            {"id": "obsolete", "key": "old.md", "status": "completed", "created_at": "2026-07-17 21:59:00"},
            {"id": "failed", "key": "failed.md", "status": "error", "created_at": "2026-07-17 21:59:00"},
            {"id": "stuck", "key": "stuck.md", "status": "running", "created_at": "2026-07-17 20:00:00"},
            {"id": "recent", "key": "recent.md", "status": "running", "created_at": "2026-07-17 21:59:00"},
            {"id": "ready", "key": "ready.md", "status": "completed", "created_at": "2026-07-17 20:00:00"},
        ],
        {"failed.md", "stuck.md", "recent.md", "ready.md"},
        now=now,
    )

    assert [(row["item"]["id"], row["reason"]) for row in plan] == [
        ("obsolete", "obsolete"),
        ("failed", "retryable_status"),
        ("stuck", "stuck_pending"),
    ]


def test_shadow_cost_estimate_is_explicit_and_small_for_fixture():
    estimate = shadow_cost_estimate([{"text": "a" * 4000}], query_count=10)

    assert estimate["estimated_tokens"] == 1320
    assert estimate["estimated_usd_before_free_allocation"] > 0
    assert estimate["pricing_url"].startswith("https://developers.cloudflare.com/")
