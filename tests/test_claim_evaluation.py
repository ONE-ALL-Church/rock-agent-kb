from pathlib import Path

import rock_kb.claim_evaluation as evaluation
from rock_kb.jsonl import read_jsonl, write_jsonl


def test_evaluation_sample_joins_legacy_claim_to_private_transcript(monkeypatch, tmp_path: Path):
    review_dir = tmp_path / "review"
    normalized_dir = tmp_path / "normalized"
    claims_path = tmp_path / "claims.jsonl"
    transcript_path = tmp_path / "media" / "source.transcripts.jsonl"
    output_path = review_dir / "claim-model-evaluations" / "sample.jsonl"
    promotion_path = review_dir / "public-media-promotions" / "source.jsonl"
    transcript = (
        "The workflow tool uses explicit permissions and a bounded result. "
        "Administrators should verify the current person's authorization before exposing the tool. "
    ) * 20
    write_jsonl(
        claims_path,
        [
            {
                "claim_id": "claim:legacy",
                "claim": "Workflow tools should expose bounded results and verify the current person's permissions.",
                "claim_type": "implementation_pattern",
                "claim_tier": "source_backed",
                "authority_tier": "official",
                "concept_ids": ["workflows", "security-permissions"],
                "source_refs": [{"source_id": "source", "url": "https://example.com/source"}],
                "source_record_ids": ["source:record"],
                "derived_from": {"type": "media_public_promotion", "id": "promotion:1", "source_id": "source"},
            }
        ],
    )
    write_jsonl(
        promotion_path,
        [{"id": "promotion:1", "media_id": "media:1", "transcript_hash": evaluation.sha256_text(transcript.strip())}],
    )
    write_jsonl(transcript_path, [{"media_id": "media:1", "transcript": transcript}])
    monkeypatch.setattr(evaluation, "REVIEW_DIR", review_dir)
    monkeypatch.setattr(evaluation, "NORMALIZED_DIR", normalized_dir)
    monkeypatch.setattr(evaluation, "transcript_index_path", lambda _source_id: transcript_path)

    result = evaluation.build_claim_model_evaluation_sample(
        model="gpt-test",
        sample_size=1,
        claims_path=claims_path,
        output_path=output_path,
    )
    row = next(read_jsonl(output_path))

    assert result["source_context_available"] == 1
    assert row["source_context_kind"] == "private_transcript_window"
    assert "explicit permissions" in row["source_context"]
    assert row["rubric"]["source_fidelity"] is None


def test_stratified_sample_is_deterministic_and_crosses_strata():
    rows = [
        {
            "claim_id": f"claim:{index}",
            "claim_type": "risk" if index % 2 else "configuration",
            "source_refs": [{"source_id": "one" if index < 4 else "two"}],
        }
        for index in range(8)
    ]

    first = evaluation.stratified_claim_sample(rows, 4, "gpt-test")
    second = evaluation.stratified_claim_sample(rows, 4, "gpt-test")

    assert [row["claim_id"] for row in first] == [row["claim_id"] for row in second]
    assert len({f"{evaluation.primary_source_id(row)}|{row['claim_type']}" for row in first}) == 4


def test_source_context_falls_back_to_canonical_url_after_record_id_changes(monkeypatch, tmp_path: Path):
    normalized_dir = tmp_path / "normalized"
    write_jsonl(
        normalized_dir / "source.jsonl",
        [
            {
                "id": "source:new-record-id",
                "source_url": "https://example.com/docs/item",
                "source_title": "Current API Record",
                "summary": "The application requires Rock version 14 or greater.",
                "citations": [{"url": "https://example.com/docs/item"}],
            }
        ],
    )
    monkeypatch.setattr(evaluation, "NORMALIZED_DIR", normalized_dir)
    claim = {
        "claim": "The application requires Rock version 14 or greater.",
        "source_record_ids": ["source:old-record-id"],
        "source_refs": [{"source_id": "source", "url": "https://example.com/docs/item"}],
    }

    context, kind, _context_hash = evaluation.source_context_for_claim(
        claim,
        source_id="source",
        promotions={},
        normalized=evaluation.normalized_record_index(),
        transcript_cache={},
        max_chars=1_000,
    )

    assert kind == "normalized_source_url_window"
    assert "version 14" in context
