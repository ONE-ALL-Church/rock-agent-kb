from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from rock_kb.contributions import validate_contribution_file
from rock_kb.schemas import Claim, ContributionRow, KBRecord, Private


def test_all_approved_claim_rows_parse_through_claim_schema():
    with open("claims/approved-claims.jsonl", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            row = json.loads(line)
            claim = Claim.model_validate(row)
            assert claim.claim_id == row["claim_id"], line_number


def test_public_dump_excludes_private_fields():
    row = json.loads(next(open("claims/approved-claims.jsonl", encoding="utf-8")))
    claim = Claim.model_validate(row)

    public = claim.public_dump()

    assert "private_corpus_pointer" not in public


def test_public_dump_excludes_nested_private_fields():
    row = None
    with open("claims/approved-claims.jsonl", encoding="utf-8") as handle:
        for line in handle:
            candidate = json.loads(line)
            if candidate.get("live_verification"):
                row = candidate
                break
    assert row is not None

    public = Claim.model_validate(row).public_dump()

    evidence_refs = public["live_verification"]["evidence_refs"]
    assert evidence_refs
    assert "path" not in evidence_refs[0]


def test_public_live_verification_scope_shape_is_valid():
    row = None
    with open("claims/approved-claims.jsonl", encoding="utf-8") as handle:
        for line in handle:
            candidate = json.loads(line)
            if candidate.get("live_verification"):
                row = candidate
                break
    assert row is not None
    live = row["live_verification"]
    live.pop("instance", None)
    live["verification_scope"] = "connected_read_only_rock_instance"

    claim = Claim.model_validate(row)

    assert claim.live_verification is not None
    assert claim.live_verification.verification_scope == "connected_read_only_rock_instance"


def test_unknown_claim_fields_are_rejected():
    row = json.loads(next(open("claims/approved-claims.jsonl", encoding="utf-8")))
    row["unexpected"] = True

    with pytest.raises(ValidationError):
        Claim.model_validate(row)


def test_live_verified_claim_requires_live_verification():
    row = json.loads(next(open("claims/approved-claims.jsonl", encoding="utf-8")))
    row["claim_tier"] = "live_verified"
    row.pop("live_verification", None)

    with pytest.raises(ValidationError, match="live_verified claim must include live_verification"):
        Claim.model_validate(row)


def test_private_marker_excludes_field_on_custom_record():
    class Example(KBRecord):
        public_value: str
        secret_value: str = Private()

    assert Example(public_value="ok", secret_value="no").public_dump() == {"public_value": "ok"}


def test_example_contribution_bundles_parse_through_schema():
    for path in [
        Path("contributions/example-org/bundle.example.jsonl"),
        Path("community-contributions/example-org/bundle.example.jsonl"),
    ]:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                row = json.loads(line)
                contribution = ContributionRow.model_validate(row)
                assert contribution.contribution_id == row["contribution_id"], (path, line_number)


def test_contribution_fixture_validates_through_public_validator():
    errors = validate_contribution_file(Path("tests/fixtures/contributions/valid-bundle.jsonl"))

    assert errors == []


def test_bad_contribution_type_and_unknown_field_are_rejected():
    errors = validate_contribution_file(Path("tests/fixtures/contributions/invalid-bundle.jsonl"))
    joined = "\n".join(errors)

    assert "schema error at contribution_type" in joined
    assert "task_card" in joined
    assert "schema error at unexpected" in joined
