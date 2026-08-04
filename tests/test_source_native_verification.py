from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from rock_kb.extract import sha256_text
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.schemas import (
    ReviewedSourceNativeArtifact,
    SourceNativeVerificationResolution,
)
from rock_kb.source_native import canonical_records_for_source_native_artifacts
from rock_kb.source_native_readiness import (
    evaluate_source_native_promotion_readiness,
)
from rock_kb.source_native_verification import (
    audit_source_native_verifications,
    build_source_native_verification_packet,
    hash_live_evidence,
    hash_live_evidence_with_timeout_retry,
    promote_source_native_verification_resolutions,
    source_native_verification_queue_hash,
)


def queue_row(question: str = "Does current public source retain this behavior?") -> dict:
    return {
        "schema": "rock-kb-source-native-verification-request-v1",
        "verification_id": "source-native-verification:test",
        "source_candidate_id": "source-native-candidate:test",
        "artifact_ids": ["source-native:claim:test"],
        "concept_ids": ["workflows"],
        "source_unit_ids": ["source-unit:test"],
        "verification_surface": "public_source_code",
        "question": question,
        "why_material": "The release-sensitive behavior changes the recommended implementation.",
        "review_state": "needs_verification",
    }


def resolution_row(queue: dict) -> dict:
    commit = "1" * 40
    return {
        "schema": "rock-kb-source-native-verification-resolution-v1",
        "verification_id": queue["verification_id"],
        "queue_item_hash": source_native_verification_queue_hash(queue),
        "resolution_state": "verified",
        "finding": "The pinned public source retains the documented behavior.",
        "evidence": [
            {
                "evidence_type": "github_source",
                "source_url": (
                    "https://github.com/SparkDevNetwork/Rock/blob/"
                    f"{commit}/Rock/Workflow.cs"
                ),
                "source_ref": commit,
                "content_hash": "a" * 64,
                "hash_mode": "raw_content",
                "finding": "The source explicitly implements the behavior.",
                "locator": {
                    "kind": "source_code_span",
                    "value": "Workflow behavior",
                    "url": (
                        "https://github.com/SparkDevNetwork/Rock/blob/"
                        f"{commit}/Rock/Workflow.cs"
                    ),
                    "path": "Rock/Workflow.cs",
                    "line_start": 10,
                    "line_end": 20,
                },
                "revalidation_url": None,
            }
        ],
        "reviewer": "ignored-by-promotion",
        "reviewed_at": "2026-08-01T00:00:00+00:00",
        "revalidation_policy": "immutable",
        "revalidate_after": None,
        "rock_versions": [],
        "version_scope_status": "unprocessed",
    }


def test_verification_packet_and_promotion_are_hash_bound(tmp_path: Path):
    queue_path = tmp_path / "queue.jsonl"
    packet_path = tmp_path / "packet.jsonl"
    input_path = tmp_path / "reviewed.jsonl"
    destination = tmp_path / "bundle"
    queue = queue_row()
    write_jsonl(queue_path, [queue])

    packet = build_source_native_verification_packet(
        queue_path=queue_path,
        destination=packet_path,
    )
    assert packet["queue_count"] == 1
    assert next(read_jsonl(packet_path))["queue_item_hash"] == (
        source_native_verification_queue_hash(queue)
    )

    write_jsonl(input_path, [resolution_row(queue)])
    result = promote_source_native_verification_resolutions(
        queue_path=queue_path,
        input_path=input_path,
        destination=destination,
        reviewer="test-reviewer",
        reviewed_at="2026-08-01T12:00:00+00:00",
    )
    assert result["report"]["verified_count"] == 1
    promoted = next(read_jsonl(destination / "verification-resolutions.jsonl"))
    assert promoted["reviewer"] == "test-reviewer"


def test_verification_queue_rejects_duplicate_ids(tmp_path: Path):
    queue_path = tmp_path / "queue.jsonl"
    packet_path = tmp_path / "packet.jsonl"
    queue = queue_row()
    write_jsonl(queue_path, [queue, queue])

    with pytest.raises(ValueError, match="duplicates source-native-verification:test"):
        build_source_native_verification_packet(
            queue_path=queue_path,
            destination=packet_path,
        )


def test_verification_audit_reopens_changed_queue_items(tmp_path: Path):
    queue_path = tmp_path / "queue.jsonl"
    resolution_path = tmp_path / "resolutions.jsonl"
    original = queue_row()
    write_jsonl(resolution_path, [resolution_row(original)])
    write_jsonl(queue_path, [queue_row("Does changed source still retain this behavior?")])

    report = audit_source_native_verifications(
        queue_path=queue_path,
        resolution_path=resolution_path,
        checked_at="2026-08-01T12:00:00+00:00",
    )

    assert report["by_state"] == {"stale": 1}
    assert report["default_cutover_blocker_count"] == 1
    assert report["items"][0]["stale_reasons"] == ["queue_item_changed"]


def test_readiness_separates_technical_and_external_evidence():
    report = evaluate_source_native_promotion_readiness(
        manifest={
            "article_count": 40,
            "source_family_counts": {
                "rock_documentation": 24,
                "rock_developer": 6,
                "rock_mobile_docs": 6,
                "rock_lava_docs": 4,
            },
        },
        verification_report={
            "default_cutover_blocker_count": 0,
            "live_check_performed": True,
        },
        retrieval_report={
            "summary": {
                "regressed": 0,
                "exact_lookup_regressions": 0,
                "authority_regressions": 0,
                "no_answer_regressions": 0,
                "endpoint_compatibility_regressions": 0,
            },
            "promotion_gate": {"passed": True},
        },
        dashboard={
            "retrieval_comparisons": {
                "opted_in_installation_count": 0,
                "by_preference": {},
                "by_category": {},
                "decision_metrics": {"decisive_count": 0},
            }
        },
        policy={
            "schema": "rock-kb-source-native-promotion-policy-v1",
            "policy_id": "test-policy",
            "technical_evidence": {
                "min_source_family_count": 4,
                "min_article_count": 36,
                "max_default_cutover_verification_blockers": 0,
                "require_retrieval_shadow_pass": True,
                "max_retrieval_regressions": 0,
                "max_exact_lookup_regressions": 0,
                "max_authority_regressions": 0,
                "max_no_answer_regressions": 0,
                "max_endpoint_compatibility_regressions": 0,
                "require_live_verification_report": True,
            },
            "external_evidence": {
                "min_opted_in_installations": 5,
                "min_decisive_comparisons": 50,
                "canonical_to_legacy_preference_ratio_min": 2,
                "required_categories": ["semantic"],
            },
        },
        evaluated_at="2026-08-01T12:00:00+00:00",
    )

    assert report["technical_evidence"]["passed"] is True
    assert report["external_evidence"]["passed"] is False
    assert report["ready_for_default_cutover"] is False
    assert report["decision"] == "remain_opt_in_canary"


def test_readiness_requires_live_verification_when_policy_enables_it():
    report = evaluate_source_native_promotion_readiness(
        manifest={
            "article_count": 1,
            "source_family_counts": {"rock_documentation": 1},
        },
        verification_report={
            "default_cutover_blocker_count": 0,
            "live_check_performed": False,
        },
        retrieval_report={
            "summary": {},
            "promotion_gate": {"passed": True},
        },
        dashboard={"retrieval_comparisons": {}},
        policy={
            "schema": "rock-kb-source-native-promotion-policy-v1",
            "policy_id": "test-policy",
            "technical_evidence": {
                "min_source_family_count": 1,
                "min_article_count": 1,
                "max_default_cutover_verification_blockers": 0,
                "require_live_verification_report": True,
                "require_retrieval_shadow_pass": True,
                "max_retrieval_regressions": 0,
                "max_exact_lookup_regressions": 0,
                "max_authority_regressions": 0,
                "max_no_answer_regressions": 0,
                "max_endpoint_compatibility_regressions": 0,
            },
            "external_evidence": {
                "min_opted_in_installations": 1,
                "min_decisive_comparisons": 1,
                "canonical_to_legacy_preference_ratio_min": 1,
                "required_categories": [],
            },
        },
        evaluated_at="2026-08-01T12:00:00+00:00",
    )

    assert report["technical_evidence"]["checks"][
        "verification_live_check"
    ] is False
    assert report["technical_evidence"]["passed"] is False
    assert report["ready_for_default_cutover"] is False


def test_readiness_allows_explicit_reversible_technical_cutover():
    report = evaluate_source_native_promotion_readiness(
        manifest={
            "article_count": 40,
            "source_family_counts": {
                "rock_documentation": 24,
                "rock_developer": 6,
                "rock_mobile_docs": 6,
                "rock_lava_docs": 4,
            },
        },
        verification_report={
            "default_cutover_blocker_count": 0,
            "live_check_performed": True,
        },
        retrieval_report={
            "summary": {
                "regressed": 0,
                "exact_lookup_regressions": 0,
                "authority_regressions": 0,
                "no_answer_regressions": 0,
                "endpoint_compatibility_regressions": 0,
            },
            "promotion_gate": {"passed": True},
        },
        dashboard={"retrieval_comparisons": {}},
        policy={
            "schema": "rock-kb-source-native-promotion-policy-v1",
            "policy_id": "technical-cutover-policy",
            "technical_evidence": {
                "min_source_family_count": 4,
                "min_article_count": 36,
                "max_default_cutover_verification_blockers": 0,
                "require_live_verification_report": True,
                "require_retrieval_shadow_pass": True,
                "max_retrieval_regressions": 0,
                "max_exact_lookup_regressions": 0,
                "max_authority_regressions": 0,
                "max_no_answer_regressions": 0,
                "max_endpoint_compatibility_regressions": 0,
            },
            "external_evidence": {
                "required_for_default_cutover": False,
                "min_opted_in_installations": 5,
                "min_decisive_comparisons": 50,
                "canonical_to_legacy_preference_ratio_min": 2,
                "required_categories": ["semantic"],
            },
            "cutover_authorization": {
                "status": "approved",
                "mode": "maintainer_approved_reversible_technical_cutover",
                "approved_at": "2026-08-03",
                "requires_legacy_rollback": True,
            },
        },
        evaluated_at="2026-08-03T12:00:00+00:00",
    )

    assert report["technical_evidence"]["passed"] is True
    assert report["external_evidence"]["passed"] is False
    assert report["external_evidence"]["gate_satisfied"] is True
    assert report["cutover_authorization"]["passed"] is True
    assert report["ready_for_default_cutover"] is True
    assert report["production_change_authorized"] is True
    assert report["decision"] == "maintainer_approved_reversible_cutover"


def test_corrected_verification_requires_effective_retrieval_text() -> None:
    queue = queue_row()
    payload = resolution_row(queue)
    payload["artifact_disposition"] = "corrects"

    with pytest.raises(ValueError, match="effective retrieval text"):
        SourceNativeVerificationResolution.model_validate(payload)


def test_article_scoped_hash_ignores_dynamic_page_chrome() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            request=request,
            text=(
                f"<html><body><div>dynamic-{calls}</div>"
                "<article><h1>Stable guidance</h1><p>Use the current rule.</p>"
                "</article></body></html>"
            ),
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        first = hash_live_evidence(
            client,
            "https://example.com/guidance",
            "normalized_article_text",
        )
        second = hash_live_evidence(
            client,
            "https://example.com/guidance",
            "normalized_article_text",
        )

    assert first == second == sha256_text(
        "Stable guidance Use the current rule."
    )


def test_live_hash_retries_one_timeout_only() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("temporary timeout", request=request)
        return httpx.Response(
            200,
            request=request,
            text="<article><p>Current official guidance.</p></article>",
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        value = hash_live_evidence_with_timeout_retry(
            client,
            "https://example.com/guidance",
            "normalized_article_text",
        )

    assert calls == 2
    assert value == sha256_text("Current official guidance.")


def test_live_hash_does_not_retry_http_errors() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.HTTPStatusError):
            hash_live_evidence_with_timeout_retry(
                client,
                "https://example.com/guidance",
                "normalized_article_text",
            )

    assert calls == 1


def test_matching_verification_corrections_replace_retrieval_text() -> None:
    reviewed = ReviewedSourceNativeArtifact.model_validate(
        {
            "schema": "rock-kb-reviewed-source-native-artifact-v1",
            "artifact_id": "source-native:task_card:test:configure-debugging",
            "source_candidate_id": "source-native-candidate:test",
            "generation_activity_id": "generation:test",
            "artifact": {
                "artifact_key": "configure-debugging",
                "artifact_type": "task_card",
                "source_unit_ids": ["source-unit:test"],
                "title": "Configure the legacy shortcut",
                "retrieval_text": (
                    "Configure the legacy shortcut with only a remote-debugging port."
                ),
                "independent_question": "How do I configure the debugger shortcut?",
                "rationale": "The source provides an ordered setup procedure.",
                "concept_ids": ["obsidian-development"],
                "temporal_status": "release_sensitive",
                "payload": {
                    "summary": "Configure the browser debugger shortcut.",
                    "steps": [
                        {"order": 1, "instruction": "Create a browser shortcut."},
                        {"order": 2, "instruction": "Add the debugger options."},
                    ],
                },
            },
            "review_state": "reviewer_approved",
            "reviewer": "test-reviewer",
            "reviewed_at": "2026-08-01T00:00:00Z",
            "review_notes": [],
            "source_input_hash": "a" * 64,
        }
    )
    correction = {
        "verification_id": "source-native-verification:test-one",
        "resolution_state": "verified",
        "artifact_disposition": "corrects",
        "finding": "Current browser behavior requires an isolated profile.",
        "effective_title": "Use an isolated browser profile.",
        "effective_retrieval_text": (
            "Current browser debugging requires a non-default user-data directory."
        ),
        "reviewed_at": "2026-08-01T00:00:00Z",
        "revalidation_policy": "time_bound",
        "revalidate_after": "2026-11-01T00:00:00Z",
        "rock_versions": [],
        "version_scope_status": "version_independent",
        "evidence": [],
    }

    units, links = canonical_records_for_source_native_artifacts(
        [reviewed],
        verification_by_artifact={
            reviewed.artifact_id: [
                correction,
                {
                    **correction,
                    "verification_id": "source-native-verification:test-two",
                },
            ]
        },
    )

    assert len(units) == 1
    assert units[0].title == "Use an isolated browser profile."
    assert units[0].retrieval_text == (
        "Current browser debugging requires a non-default user-data directory."
    )
    assert units[0].payload["verification"]["effective_override"] is True
    assert units[0].rock_versions == []
    assert units[0].version_scope_status == "version_independent"
    assert {link.relation for link in links} == {"contradicts"}

    scoped_units, _ = canonical_records_for_source_native_artifacts(
        [reviewed],
        verification_by_artifact={
            reviewed.artifact_id: [
                {
                    **correction,
                    "rock_versions": ["19.4"],
                    "version_scope_status": "scoped",
                }
            ]
        },
    )
    assert scoped_units[0].rock_versions == ["19.4"]
    assert scoped_units[0].version_scope_status == "scoped"


def test_superseding_verification_removes_artifact_from_canonical_projection() -> None:
    reviewed = ReviewedSourceNativeArtifact.model_validate(
        {
            "schema": "rock-kb-reviewed-source-native-artifact-v1",
            "artifact_id": "source-native:claim:test:obsolete",
            "source_candidate_id": "source-native-candidate:test",
            "generation_activity_id": "generation:test",
            "artifact": {
                "artifact_key": "obsolete",
                "artifact_type": "claim",
                "source_unit_ids": ["source-unit:test"],
                "title": "Obsolete claim",
                "retrieval_text": "The obsolete behavior remains available.",
                "independent_question": "Is the obsolete behavior available?",
                "rationale": "The source once documented the behavior.",
                "concept_ids": ["system-admin-ops"],
                "claim_type": "behavior",
                "evidence_class": "historical",
                "payload": {"summary": "The source once documented the behavior."},
            },
            "review_state": "reviewer_approved",
            "reviewer": "test-reviewer",
            "reviewed_at": "2026-08-01T00:00:00Z",
            "review_notes": [],
            "source_input_hash": "a" * 64,
        }
    )

    units, links = canonical_records_for_source_native_artifacts(
        [reviewed],
        verification_by_artifact={
            reviewed.artifact_id: [
                {
                    "verification_id": "source-native-verification:superseded",
                    "resolution_state": "verified",
                    "artifact_disposition": "supersedes",
                }
            ]
        },
    )

    assert units == []
    assert links == []
