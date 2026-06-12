from __future__ import annotations

from pathlib import Path

import pytest

from rock_kb.contributions import promote_private_contributions, validate_contribution_file
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.schemas import ContributionRow


def draft_row() -> dict:
    return {
        "schema": "rock-kb-org-contribution-v1",
        "contribution_id": "private-distill:workflow-launch",
        "org_id": "private",
        "org_display_name": "private",
        "source_id": "private_rock_repo_candidates",
        "concept_ids": ["workflows"],
        "contribution_type": "guide_section",
        "title": "Draft Private Pattern: Workflow Launch",
        "distilled_summary": "Private draft summary that must be rewritten before publication.",
        "source_urls": [],
        "source_record_ids": [],
        "redaction_attestation": False,
        "review_status": "draft_private",
        "license_attestation": False,
        "confidence": "needs_review",
        "needs_live_verification": True,
        "created_at": "2026-06-12T00:00:00Z",
        "publishability_status": "private_draft_not_public",
    }


def rewrite_row(**overrides) -> dict:
    row = {
        "contribution_id": "private-distill:workflow-launch",
        "title": "Workflow launch troubleshooting pattern",
        "distilled_summary": (
            "When troubleshooting workflow launch behavior, confirm the trigger, active workflow type, context entity, "
            "action logs, notification idempotency, and relevant public documentation before changing configuration."
        ),
        "source_urls": ["https://community.rockrms.com/documentation"],
        "source_record_ids": [],
        "confidence": "medium",
        "needs_live_verification": True,
    }
    row.update(overrides)
    return row


def write_bundle(path: Path, rows: list[dict]) -> Path:
    write_jsonl(path, rows)
    return path


def test_reviewed_promotion_without_attestations_fails_named_gate(tmp_path):
    draft_path = write_bundle(tmp_path / "draft.jsonl", [draft_row()])
    rewrite_path = write_bundle(tmp_path / "rewrite.jsonl", [rewrite_row()])

    with pytest.raises(ValueError) as exc:
        promote_private_contributions(
            draft_path,
            org_id="example-org",
            rewrite_path=rewrite_path,
            reviewed=True,
            redaction_attestation=False,
            license_attestation=False,
        )

    message = str(exc.value)
    assert "private-distill:workflow-launch" in message
    assert "status draft_private" in message
    assert "redaction_attestation" in message
    assert "license_attestation" in message


def test_legal_reviewed_promotion_emits_valid_contribution_row(tmp_path):
    draft_path = write_bundle(tmp_path / "draft.jsonl", [draft_row()])
    rewrite_path = write_bundle(tmp_path / "rewrite.jsonl", [rewrite_row()])
    output_path = tmp_path / "bundle.jsonl"

    result = promote_private_contributions(
        draft_path,
        org_id="example-org",
        output_path=output_path,
        rewrite_path=rewrite_path,
        reviewed=True,
        redaction_attestation=True,
        license_attestation=True,
    )

    assert result["status"] == "public_bundle"
    rows = list(read_jsonl(output_path))
    assert len(rows) == 1
    contribution = ContributionRow.model_validate(rows[0])
    assert contribution.review_status == "redaction_reviewed"
    assert validate_contribution_file(output_path) == []


def test_illegal_review_status_transition_is_rejected(tmp_path):
    draft_path = write_bundle(tmp_path / "draft.jsonl", [draft_row()])
    rewrite_path = write_bundle(tmp_path / "rewrite.jsonl", [rewrite_row()])

    with pytest.raises(ValueError) as exc:
        promote_private_contributions(
            draft_path,
            org_id="example-org",
            rewrite_path=rewrite_path,
            reviewed=True,
            redaction_attestation=True,
            license_attestation=True,
            review_status="draft_private",
        )

    message = str(exc.value)
    assert "illegal review_status transition" in message
    assert "draft_private -> draft_private" in message
    assert "not promotable" in message


def test_reviewed_promotion_rejects_private_path_leaks(tmp_path):
    draft_path = write_bundle(tmp_path / "draft.jsonl", [draft_row()])
    rewrite_path = write_bundle(
        tmp_path / "rewrite.jsonl",
        [rewrite_row(source_urls=["data/review/private-source.md"])],
    )

    with pytest.raises(ValueError) as exc:
        promote_private_contributions(
            draft_path,
            org_id="example-org",
            rewrite_path=rewrite_path,
            reviewed=True,
            redaction_attestation=True,
            license_attestation=True,
        )

    message = str(exc.value)
    assert "private path reference" in message
    assert "data/review/" in message
