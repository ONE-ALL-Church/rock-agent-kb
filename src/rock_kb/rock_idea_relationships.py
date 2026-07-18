from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.parse import urlparse

from .extract import sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, REPO_ROOT, REVIEW_DIR


ROCK_IDEA_RELATIONSHIP_PATH = AGENT_DIR / "rock-idea-relationships.jsonl"
ROCK_IDEA_RELATIONSHIP_CANDIDATE_PATH = REVIEW_DIR / "rock-ideas" / "relationship-candidates.jsonl"
ROCK_IDEA_VERIFICATION_QUEUE_PATH = AGENT_DIR / "rock-idea-verification-queue.jsonl"
ROCK_IDEA_VERIFICATION_REVIEW_PATH = REPO_ROOT / "ideas" / "verification-reviews.jsonl"

VERIFICATION_LIFECYCLE_STATUSES = {"complete", "planned", "started", "under_review"}
CORROBORATING_RELATIONSHIP_TYPES = {"corroborated_by_release_note", "implemented_by_issue"}
REFERENCE_RELATIONSHIP_TYPES = {
    "references_issue",
    "references_idea",
    "references_release_notes",
    "references_official_documentation",
    "references_official_source",
}

RELATIONSHIP_TYPES = {
    "about",
    "about_model",
    "references_issue",
    "references_idea",
    "references_release_notes",
    "references_official_documentation",
    "references_official_source",
    "corroborated_by_release_note",
    "implemented_by_issue",
}

RELEASE_TITLE_STOPWORDS = {
    "a",
    "ability",
    "add",
    "allow",
    "an",
    "and",
    "block",
    "for",
    "from",
    "in",
    "new",
    "of",
    "on",
    "or",
    "rock",
    "support",
    "the",
    "to",
    "with",
}

VERIFICATION_REVIEW_OUTCOMES = {
    "corroborated_by_release_note",
    "references_only",
    "no_official_match",
}

VERIFICATION_REVIEW_REASON_CODES = {
    "official_release_note_describes_same_shipped_behavior",
    "explicit_reference_does_not_confirm_planned_release",
    "no_matching_official_evidence_in_current_inputs",
}


def build_rock_idea_relationship_artifacts(
    ideas: Iterable[dict[str, Any]],
    *,
    checked_at: str | None = None,
) -> dict[str, Any]:
    idea_rows = list(ideas)
    model_rows = list(read_jsonl(AGENT_DIR / "model-map-digests.jsonl"))
    release_rows = list(read_jsonl(AGENT_DIR / "release-index.jsonl"))
    issue_rows = list(read_jsonl(AGENT_DIR / "rock-issues.jsonl"))
    source_rows = list(read_jsonl(AGENT_DIR / "source-summaries.jsonl"))
    verification_reviews = list(read_jsonl(ROCK_IDEA_VERIFICATION_REVIEW_PATH))
    validate_rock_idea_verification_reviews(verification_reviews, idea_rows=idea_rows)
    relationships, candidates = rock_idea_relationship_rows(
        idea_rows,
        model_rows=model_rows,
        release_rows=release_rows,
        issue_rows=issue_rows,
        source_rows=source_rows,
        verification_reviews=verification_reviews,
        checked_at=checked_at,
    )
    validate_rock_idea_relationship_rows(relationships, idea_rows=idea_rows)
    write_jsonl(ROCK_IDEA_RELATIONSHIP_PATH, relationships)
    write_jsonl(ROCK_IDEA_RELATIONSHIP_CANDIDATE_PATH, candidates)
    verification_queue, verification_summary = build_rock_idea_verification_queue(
        idea_rows,
        relationships=relationships,
        candidates=candidates,
        verification_reviews=verification_reviews,
        checked_at=checked_at,
    )
    validate_rock_idea_verification_queue(verification_queue, idea_rows=idea_rows)
    write_jsonl(ROCK_IDEA_VERIFICATION_QUEUE_PATH, verification_queue)
    by_type = Counter(str(row["relationship_type"]) for row in relationships)
    sources_by_type: dict[str, set[str]] = {}
    for row in relationships:
        sources_by_type.setdefault(str(row["relationship_type"]), set()).add(str(row["source_id"]))
    return {
        "schema": "rock-kb-rock-idea-relationship-summary-v1",
        "relationship_count": len(relationships),
        "candidate_count": len(candidates),
        "by_type": dict(sorted(by_type.items())),
        "ideas_with_relationships": len({str(row["source_id"]) for row in relationships}),
        "ideas_with_model_links": len(sources_by_type.get("about_model", set())),
        "ideas_with_issue_links": len(
            sources_by_type.get("references_issue", set()) | sources_by_type.get("implemented_by_issue", set())
        ),
        "ideas_with_release_evidence": len(
            sources_by_type.get("references_release_notes", set())
            | sources_by_type.get("corroborated_by_release_note", set())
        ),
        "verification_queue": verification_summary,
    }


def build_rock_idea_verification_queue(
    ideas: Iterable[dict[str, Any]],
    *,
    relationships: Iterable[dict[str, Any]],
    candidates: Iterable[dict[str, Any]],
    verification_reviews: Iterable[dict[str, Any]] = (),
    checked_at: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    idea_rows = list(ideas)
    observed_at = checked_at or utc_now()
    relationships_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    candidates_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    reviews_by_source = {
        str(review.get("idea_id") or ""): review
        for review in verification_reviews
        if review.get("idea_id")
    }
    for relationship in relationships:
        relationships_by_source[str(relationship.get("source_id") or "")].append(relationship)
    for candidate in candidates:
        candidates_by_source[str(candidate.get("source_id") or "")].append(candidate)

    queue: list[dict[str, Any]] = []
    for idea in idea_rows:
        status = str(idea.get("status") or "")
        if status not in VERIFICATION_LIFECYCLE_STATUSES:
            continue
        idea_id = str(idea.get("idea_id") or "")
        related = relationships_by_source.get(idea_id, [])
        evidence = [
            row
            for row in related
            if str(row.get("relationship_type") or "")
            in CORROBORATING_RELATIONSHIP_TYPES | REFERENCE_RELATIONSHIP_TYPES
        ]
        corroborating = [
            row
            for row in evidence
            if str(row.get("relationship_type") or "") in CORROBORATING_RELATIONSHIP_TYPES
            and str(row.get("authority_tier") or "") == "official"
            and str(row.get("confidence") or "") == "high"
        ]
        candidate_rows = candidates_by_source.get(idea_id, [])
        base_evidence = [row for row in evidence if row.get("review_state") != "maintainer_reviewed"]
        candidate_hash = verification_candidate_set_hash(candidate_rows)
        evidence_hash = verification_evidence_set_hash(base_evidence)
        active_review = current_verification_review(
            idea,
            related=base_evidence,
            candidates=candidate_rows,
            review=reviews_by_source.get(idea_id),
        )
        if active_review and active_review.get("outcome") == "corroborated_by_release_note" and not any(
            row.get("review_state") == "maintainer_reviewed"
            and (row.get("metadata") or {}).get("review_id") == active_review.get("review_id")
            for row in corroborating
        ):
            active_review = None
        if active_review and active_review.get("outcome") == "references_only" and not base_evidence:
            active_review = None
        verification_state = (
            "officially_corroborated"
            if corroborating
            else "maintainer_reviewed_references_only"
            if active_review and active_review.get("outcome") == "references_only"
            else "maintainer_reviewed_no_official_match"
            if active_review and active_review.get("outcome") == "no_official_match"
            else "candidate_review_pending"
            if candidate_rows
            else "references_available"
            if evidence
            else "evidence_needed"
        )
        recommended_action = verification_recommended_action(status, verification_state)
        priority_score, priority_reasons = verification_priority(
            idea,
            verification_state=verification_state,
            evidence_count=len(evidence),
            candidate_count=len(candidate_rows),
        )
        review_input_hash = sha256_text(
            json.dumps(
                {
                    "source_content_hash": idea.get("content_hash"),
                    "evidence_relationship_set_hash": evidence_hash,
                    "candidate_set_hash": candidate_hash,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        row = {
            "schema": "rock-kb-rock-idea-verification-queue-v1",
            "queue_id": f"rock_idea_verification:{idea_id.split(':', 1)[-1]}",
            "idea_id": idea_id,
            "number": idea.get("number"),
            "title": idea.get("title"),
            "url": idea.get("url"),
            "status": status,
            "status_label": idea.get("status_label"),
            "planned_version": idea.get("planned_version"),
            "vote_count": int(idea.get("vote_count") or 0),
            "concept_ids": list(idea.get("concept_ids") or []),
            "verification_state": verification_state,
            "recommended_action": recommended_action,
            "priority_score": priority_score,
            "priority_band": "high" if priority_score >= 90 else "medium" if priority_score >= 60 else "low",
            "priority_reasons": priority_reasons,
            "evidence_relationship_ids": sorted(str(value.get("relationship_id") or "") for value in evidence),
            "evidence_relationship_types": sorted({str(value.get("relationship_type") or "") for value in evidence}),
            "candidate_match_count": len(candidate_rows),
            "source_content_hash": idea.get("content_hash"),
            "evidence_relationship_set_hash": evidence_hash,
            "candidate_set_hash": candidate_hash,
            "review_input_hash": review_input_hash,
            "verification_review_id": active_review.get("review_id") if active_review else None,
            "verification_review_outcome": active_review.get("outcome") if active_review else None,
            "revalidation_triggers": [
                "idea_content_hash_changed",
                "evidence_relationship_hash_changed",
                "candidate_set_changed",
            ],
            "authority_tier": "community-unreviewed",
            "claim_tier": "routing_context_only",
            "needs_live_verification": True,
            "last_checked_at": str(idea.get("last_checked_at") or observed_at),
        }
        row["content_hash"] = sha256_text(
            json.dumps(
                {key: value for key, value in row.items() if key not in {"last_checked_at", "content_hash"}},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        queue.append(row)

    queue.sort(
        key=lambda row: (
            -int(row["priority_score"]),
            -int(row["vote_count"]),
            int(row.get("number") or 0),
        )
    )
    by_state = Counter(str(row["verification_state"]) for row in queue)
    summary = {
        "schema": "rock-kb-rock-idea-verification-queue-summary-v1",
        "queue_count": len(queue),
        "high_priority_count": sum(1 for row in queue if row["priority_band"] == "high"),
        "candidate_review_count": sum(1 for row in queue if row["candidate_match_count"]),
        "officially_corroborated_count": by_state.get("officially_corroborated", 0),
        "maintainer_reviewed_count": sum(1 for row in queue if row.get("verification_review_id")),
        "by_status": dict(sorted(Counter(str(row["status"]) for row in queue).items())),
        "by_verification_state": dict(sorted(by_state.items())),
        "queue_content_hash": sha256_text(
            json.dumps(
                [(row["queue_id"], row["content_hash"]) for row in queue],
                separators=(",", ":"),
            )
        ),
        "trust_boundary": "Queue priority identifies lifecycle claims needing public corroboration; it is not implementation evidence.",
    }
    return queue, summary


def verification_recommended_action(status: str, verification_state: str) -> str:
    if verification_state == "officially_corroborated":
        return "confirm_version_and_instance_applicability"
    if verification_state in {
        "maintainer_reviewed_references_only",
        "maintainer_reviewed_no_official_match",
    }:
        return "revalidate_when_review_inputs_change"
    if status == "complete":
        return "corroborate_completed_state"
    if status in {"planned", "started"}:
        return "verify_roadmap_state_and_release_evidence"
    return "monitor_review_outcome"


def verification_priority(
    idea: dict[str, Any],
    *,
    verification_state: str,
    evidence_count: int,
    candidate_count: int,
) -> tuple[int, list[str]]:
    status = str(idea.get("status") or "")
    votes = int(idea.get("vote_count") or 0)
    score = {"started": 70, "planned": 65, "complete": 55, "under_review": 45}.get(status, 0)
    reasons = [f"lifecycle_{status}"]
    score += min(votes, 50)
    if votes:
        reasons.append("community_vote_signal")
    if idea.get("planned_version"):
        score += 15
        reasons.append("planned_version_present")
    if candidate_count:
        score += 20
        reasons.append("private_candidate_available")
    if evidence_count:
        score += 10
        reasons.append("explicit_public_reference_available")
    if verification_state == "officially_corroborated" or verification_state.startswith("maintainer_reviewed_"):
        score = min(score, 40 if verification_state == "officially_corroborated" else 30)
        reasons.append(
            "official_release_evidence_present"
            if verification_state == "officially_corroborated"
            else "current_inputs_maintainer_reviewed"
        )
    return score, reasons


def validate_rock_idea_verification_queue(
    rows: Iterable[dict[str, Any]],
    *,
    idea_rows: Iterable[dict[str, Any]],
) -> None:
    ideas = {str(row.get("idea_id") or ""): row for row in idea_rows}
    seen: set[str] = set()
    forbidden = {"description", "body", "response", "response_text", "comments", "author", "submitter", "organization"}
    allowed_states = {
        "officially_corroborated",
        "maintainer_reviewed_references_only",
        "maintainer_reviewed_no_official_match",
        "candidate_review_pending",
        "references_available",
        "evidence_needed",
    }
    for index, row in enumerate(rows, 1):
        queue_id = str(row.get("queue_id") or "")
        idea_id = str(row.get("idea_id") or "")
        if row.get("schema") != "rock-kb-rock-idea-verification-queue-v1" or not queue_id.startswith("rock_idea_verification:"):
            raise ValueError(f"Rock idea verification queue row {index} has an invalid schema or ID")
        if queue_id in seen:
            raise ValueError(f"Duplicate Rock idea verification queue ID: {queue_id}")
        seen.add(queue_id)
        if idea_id not in ideas or row.get("source_content_hash") != ideas[idea_id].get("content_hash"):
            raise ValueError(f"Rock idea verification queue {queue_id} has stale or unknown source input")
        if row.get("status") not in VERIFICATION_LIFECYCLE_STATUSES or row.get("verification_state") not in allowed_states:
            raise ValueError(f"Rock idea verification queue {queue_id} has an invalid lifecycle or verification state")
        if forbidden & set(row):
            raise ValueError(f"Rock idea verification queue {queue_id} contains disallowed raw content")
        if row.get("needs_live_verification") is not True or row.get("claim_tier") != "routing_context_only":
            raise ValueError(f"Rock idea verification queue {queue_id} overstates verification authority")
        if not row.get("review_input_hash") or not row.get("content_hash"):
            raise ValueError(f"Rock idea verification queue {queue_id} has incomplete hash traceability")
        if not row.get("candidate_set_hash") or not row.get("evidence_relationship_set_hash"):
            raise ValueError(f"Rock idea verification queue {queue_id} has incomplete review input hashes")
        if str(row.get("verification_state") or "").startswith("maintainer_reviewed_") and not (
            row.get("verification_review_id") and row.get("verification_review_outcome")
        ):
            raise ValueError(f"Rock idea verification queue {queue_id} has an incomplete maintainer review")


def verification_candidate_set_hash(rows: Iterable[dict[str, Any]]) -> str:
    return sha256_text(
        json.dumps(
            [
                {
                    "candidate_id": row.get("candidate_id"),
                    "release_record_id": row.get("release_record_id"),
                    "title_token_coverage": row.get("title_token_coverage"),
                }
                for row in sorted(rows, key=lambda value: str(value.get("candidate_id") or ""))
            ],
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def verification_evidence_set_hash(rows: Iterable[dict[str, Any]]) -> str:
    evidence = [
        row
        for row in rows
        if str(row.get("relationship_type") or "")
        in CORROBORATING_RELATIONSHIP_TYPES | REFERENCE_RELATIONSHIP_TYPES
        and row.get("review_state") != "maintainer_reviewed"
    ]
    return sha256_text(
        json.dumps(
            sorted(
                str(row.get("content_hash") or row.get("relationship_id") or "")
                for row in evidence
            ),
            separators=(",", ":"),
        )
    )


def release_evidence_hash(row: dict[str, Any]) -> str:
    return sha256_text(
        json.dumps(
            {
                "id": row.get("id"),
                "version": row.get("version"),
                "module": row.get("module"),
                "release_family": row.get("release_family"),
                "summary": row.get("summary"),
                "issue_refs": list(row.get("issue_refs") or []),
                "change_type": row.get("change_type"),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def current_verification_review(
    idea: dict[str, Any],
    *,
    related: Iterable[dict[str, Any]],
    candidates: Iterable[dict[str, Any]],
    review: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not review or review.get("source_content_hash") != idea.get("content_hash"):
        return None
    if review.get("candidate_set_hash") != verification_candidate_set_hash(candidates):
        return None
    if review.get("evidence_relationship_set_hash") != verification_evidence_set_hash(related):
        return None
    return review


def validate_rock_idea_verification_reviews(
    rows: Iterable[dict[str, Any]],
    *,
    idea_rows: Iterable[dict[str, Any]],
) -> None:
    idea_ids = {str(row.get("idea_id") or "") for row in idea_rows}
    seen_reviews: set[str] = set()
    seen_ideas: set[str] = set()
    allowed_keys = {
        "schema",
        "review_id",
        "idea_id",
        "source_content_hash",
        "evidence_relationship_set_hash",
        "candidate_set_hash",
        "outcome",
        "reason_code",
        "candidate_id",
        "release_record_id",
        "release_evidence_hash",
        "reviewer",
        "reviewed_at",
        "redaction_attestation",
        "license_attestation",
    }
    hash_pattern = re.compile(r"^[0-9a-f]{64}$")
    for index, row in enumerate(rows, 1):
        review_id = str(row.get("review_id") or "")
        idea_id = str(row.get("idea_id") or "")
        if row.get("schema") != "rock-kb-rock-idea-verification-review-v1" or not review_id.startswith(
            "rock_idea_verification_review:"
        ):
            raise ValueError(f"Rock idea verification review row {index} has an invalid schema or ID")
        if review_id in seen_reviews or idea_id in seen_ideas:
            raise ValueError(f"Duplicate Rock idea verification review for {idea_id or review_id}")
        seen_reviews.add(review_id)
        seen_ideas.add(idea_id)
        if idea_id not in idea_ids:
            raise ValueError(f"Rock idea verification review {review_id} has an unknown idea")
        if review_id != f"rock_idea_verification_review:{idea_id.split(':', 1)[-1]}":
            raise ValueError(f"Rock idea verification review {review_id} does not match its idea")
        if set(row) - allowed_keys:
            raise ValueError(f"Rock idea verification review {review_id} contains unsupported fields")
        if row.get("outcome") not in VERIFICATION_REVIEW_OUTCOMES:
            raise ValueError(f"Rock idea verification review {review_id} has an invalid outcome")
        if row.get("reason_code") not in VERIFICATION_REVIEW_REASON_CODES:
            raise ValueError(f"Rock idea verification review {review_id} has an invalid reason code")
        expected_reason = {
            "corroborated_by_release_note": "official_release_note_describes_same_shipped_behavior",
            "references_only": "explicit_reference_does_not_confirm_planned_release",
            "no_official_match": "no_matching_official_evidence_in_current_inputs",
        }[str(row["outcome"])]
        if row.get("reason_code") != expected_reason:
            raise ValueError(f"Rock idea verification review {review_id} has an inconsistent reason code")
        for key in ("source_content_hash", "evidence_relationship_set_hash", "candidate_set_hash"):
            if not hash_pattern.fullmatch(str(row.get(key) or "")):
                raise ValueError(f"Rock idea verification review {review_id} has an invalid {key}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", str(row.get("reviewer") or "")):
            raise ValueError(f"Rock idea verification review {review_id} has an invalid reviewer")
        try:
            reviewed_at = datetime.fromisoformat(str(row.get("reviewed_at") or "").replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Rock idea verification review {review_id} has an invalid reviewed_at") from exc
        if reviewed_at.tzinfo is None:
            raise ValueError(f"Rock idea verification review {review_id} reviewed_at must include a timezone")
        if row.get("redaction_attestation") is not True or row.get("license_attestation") is not True:
            raise ValueError(f"Rock idea verification review {review_id} is missing required attestations")
        if row.get("outcome") == "corroborated_by_release_note":
            if not (
                str(row.get("candidate_id") or "").startswith("rock_idea_relationship_candidate:")
                and str(row.get("release_record_id") or "").startswith("rock_")
                and hash_pattern.fullmatch(str(row.get("release_evidence_hash") or ""))
            ):
                raise ValueError(f"Rock idea verification review {review_id} has incomplete release evidence")
        elif any(row.get(key) for key in ("candidate_id", "release_record_id", "release_evidence_hash")):
            raise ValueError(f"Rock idea verification review {review_id} attaches release evidence to a negative outcome")


def rock_idea_relationship_rows(
    ideas: Iterable[dict[str, Any]],
    *,
    model_rows: Iterable[dict[str, Any]],
    release_rows: Iterable[dict[str, Any]],
    issue_rows: Iterable[dict[str, Any]],
    source_rows: Iterable[dict[str, Any]] = (),
    verification_reviews: Iterable[dict[str, Any]] = (),
    checked_at: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    idea_rows = list(ideas)
    releases = list(release_rows)
    review_rows = list(verification_reviews)
    validate_rock_idea_verification_reviews(review_rows, idea_rows=idea_rows)
    observed_at = checked_at or utc_now()
    issue_ids = issue_id_index(issue_rows)
    source_targets = source_target_index(source_rows)
    aliases = model_aliases(model_rows)
    edges: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for idea in idea_rows:
        idea_id = str(idea.get("idea_id") or "")
        idea_url = str(idea.get("url") or "")
        edge_checked_at = str(idea.get("last_checked_at") or observed_at)
        concept_routes = idea.get("concept_routes") or [
            {"concept_id": value, "basis": "legacy_concept_id", "signal": value}
            for value in idea.get("concept_ids") or []
        ]
        for route in concept_routes:
            if not isinstance(route, dict) or not route.get("concept_id"):
                continue
            basis = str(route.get("basis") or "legacy_concept_id")
            edges.append(
                relationship_row(
                    source_id=idea_id,
                    target_id=f"concept:{route['concept_id']}",
                    target_kind="concept",
                    relationship_type="about",
                    basis=basis,
                    signal=str(route.get("signal") or route["concept_id"]),
                    evidence_url=idea_url,
                    authority_tier="community-unreviewed",
                    confidence="high" if basis == "official_category" else "medium",
                    review_state="deterministic",
                    checked_at=edge_checked_at,
                )
            )

        for route in model_relationships_for_idea(str(idea.get("title") or ""), aliases):
            edges.append(
                relationship_row(
                    source_id=idea_id,
                    target_id=route["target_id"],
                    target_kind="model_map",
                    relationship_type="about_model",
                    basis="exact_model_title_alias",
                    signal=route["signal"],
                    evidence_url=idea_url,
                    authority_tier="community-unreviewed",
                    confidence="high",
                    review_state="deterministic",
                    checked_at=edge_checked_at,
                )
            )

        for link in idea.get("evidence_links") or []:
            if not isinstance(link, dict):
                continue
            relationship_type = {
                "github_issue": "references_issue",
                "rock_idea": "references_idea",
                "release_notes": "references_release_notes",
                "official_documentation": "references_official_documentation",
                "official_source": "references_official_source",
            }.get(str(link.get("link_kind") or ""))
            if not relationship_type:
                continue
            target_id = str(link.get("target_id") or "") or source_targets.get(
                canonical_evidence_url(str(link.get("url") or ""))
            )
            edges.append(
                relationship_row(
                    source_id=idea_id,
                    target_id=target_id or None,
                    target_url=str(link.get("url") or "") or None,
                    target_kind=(
                        "source_summary"
                        if target_id and target_id.startswith("source:")
                        else str(link.get("target_kind") or link.get("link_kind") or "evidence")
                    ),
                    relationship_type=relationship_type,
                    basis=f"explicit_{link.get('origin') or 'idea'}_link",
                    signal=str(link.get("link_kind") or "evidence"),
                    evidence_url=idea_url,
                    authority_tier=str(link.get("authority_tier") or "community-unreviewed"),
                    confidence="high",
                    review_state="source_observed",
                    checked_at=edge_checked_at,
                )
            )

        public_release_matches, release_candidates = release_relationships_for_idea(idea, releases)
        for match in public_release_matches:
            release_record_id = str(match["record_id"])
            release_url = str(match["url"])
            edges.append(
                relationship_row(
                    source_id=idea_id,
                    target_id=f"source:{release_record_id}",
                    target_url=release_url,
                    target_kind="source_summary",
                    relationship_type="corroborated_by_release_note",
                    basis="exact_planned_version_and_full_title_token_coverage",
                    signal=release_record_id,
                    evidence_url=release_url,
                    authority_tier="official",
                    confidence="high",
                    review_state="deterministic",
                    checked_at=edge_checked_at,
                    metadata={
                        "release_record_id": release_record_id,
                        "release_version": match["version"],
                        "release_module": match.get("module"),
                        "title_token_coverage": match["coverage"],
                    },
                )
            )
            family = str(match.get("release_family") or "core")
            for raw_issue_ref in match.get("issue_refs") or []:
                if not str(raw_issue_ref).isdigit():
                    continue
                target_id = issue_ids.get((family, int(raw_issue_ref)))
                if not target_id:
                    continue
                edges.append(
                    relationship_row(
                        source_id=idea_id,
                        target_id=target_id,
                        target_kind="rock_issue",
                        relationship_type="implemented_by_issue",
                        basis="official_release_note_match_and_issue_ref",
                        signal=f"#{raw_issue_ref}",
                        evidence_url=release_url,
                        authority_tier="official",
                        confidence="high",
                        review_state="deterministic",
                        checked_at=edge_checked_at,
                        metadata={"release_record_id": release_record_id, "release_version": match["version"]},
                    )
                )
        candidates.extend(release_candidates)

    candidate_rows = {str(row["candidate_id"]): row for row in candidates}
    edges.extend(
        reviewed_release_relationship_rows(
            idea_rows,
            relationships=edges,
            candidates=candidate_rows.values(),
            releases=releases,
            verification_reviews=review_rows,
        )
    )
    deduped = {str(row["relationship_id"]): row for row in edges}
    return (
        sorted(deduped.values(), key=lambda row: (str(row["source_id"]), str(row["relationship_type"]), str(row.get("target_id") or row.get("target_url") or ""))),
        sorted(candidate_rows.values(), key=lambda row: (str(row["source_id"]), -float(row["title_token_coverage"]), str(row["release_record_id"]))),
    )


def reviewed_release_relationship_rows(
    ideas: Iterable[dict[str, Any]],
    *,
    relationships: Iterable[dict[str, Any]],
    candidates: Iterable[dict[str, Any]],
    releases: Iterable[dict[str, Any]],
    verification_reviews: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    relationships_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    candidates_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relationship in relationships:
        relationships_by_source[str(relationship.get("source_id") or "")].append(relationship)
    for candidate in candidates:
        candidates_by_source[str(candidate.get("source_id") or "")].append(candidate)
    ideas_by_id = {str(idea.get("idea_id") or ""): idea for idea in ideas}
    releases_by_id = {str(release.get("id") or ""): release for release in releases}

    rows: list[dict[str, Any]] = []
    for review in verification_reviews:
        if review.get("outcome") != "corroborated_by_release_note":
            continue
        idea_id = str(review.get("idea_id") or "")
        idea = ideas_by_id.get(idea_id)
        related = relationships_by_source.get(idea_id, [])
        candidate_rows = candidates_by_source.get(idea_id, [])
        if not idea or not current_verification_review(
            idea,
            related=related,
            candidates=candidate_rows,
            review=review,
        ):
            continue
        candidate = next(
            (
                row
                for row in candidate_rows
                if row.get("candidate_id") == review.get("candidate_id")
                and row.get("release_record_id") == review.get("release_record_id")
            ),
            None,
        )
        release = releases_by_id.get(str(review.get("release_record_id") or ""))
        if not candidate or not release or review.get("release_evidence_hash") != release_evidence_hash(release):
            continue
        release_record_id = str(release["id"])
        evidence_url = release_url(release)
        rows.append(
            relationship_row(
                source_id=idea_id,
                target_id=f"source:{release_record_id}",
                target_url=evidence_url,
                target_kind="source_summary",
                relationship_type="corroborated_by_release_note",
                basis="maintainer_reviewed_official_release_match",
                signal=release_record_id,
                evidence_url=evidence_url,
                authority_tier="official",
                confidence="high",
                review_state="maintainer_reviewed",
                checked_at=str(review.get("reviewed_at") or idea.get("last_checked_at") or utc_now()),
                metadata={
                    "review_id": review.get("review_id"),
                    "release_record_id": release_record_id,
                    "release_version": release.get("version"),
                    "release_module": release.get("module"),
                    "title_token_coverage": candidate.get("title_token_coverage"),
                },
            )
        )
    return rows


def relationship_row(
    *,
    source_id: str,
    relationship_type: str,
    basis: str,
    signal: str,
    evidence_url: str,
    authority_tier: str,
    confidence: str,
    review_state: str,
    checked_at: str,
    target_id: str | None = None,
    target_url: str | None = None,
    target_kind: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = {
        "source_id": source_id,
        "target_id": target_id or "",
        "target_url": target_url or "",
        "relationship_type": relationship_type,
        "basis": basis,
        "evidence_url": evidence_url,
    }
    digest = sha256_text(json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    row = {
        "schema": "rock-kb-rock-idea-relationship-v1",
        "relationship_id": f"rock_idea_relationship:{digest[:24]}",
        "source_id": source_id,
        "target_id": target_id,
        "target_url": target_url,
        "target_kind": target_kind,
        "relationship_type": relationship_type,
        "basis": basis,
        "signal": signal,
        "evidence_url": evidence_url,
        "authority_tier": authority_tier,
        "confidence": confidence,
        "review_state": review_state,
        "needs_live_verification": True,
        "last_checked_at": checked_at,
        "metadata": metadata or {},
    }
    row["content_hash"] = sha256_text(
        json.dumps({key: value for key, value in row.items() if key not in {"last_checked_at", "content_hash"}}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )
    return row


def model_aliases(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    aliases: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        identity = row.get("identity") if isinstance(row.get("identity"), dict) else {}
        slug = str(identity.get("model_slug") or "").strip()
        model_name = str(identity.get("model_name") or "").strip()
        model_title = str(identity.get("model_title") or "").strip()
        if not slug or not (model_name or model_title):
            continue
        human_tokens = normalized_phrase(model_name).split()
        if len(human_tokens) < 2:
            continue
        for name, alias_kind in ((model_name, "model_name"), (model_title, "model_title")):
            phrase = normalized_phrase(name)
            tokens = phrase.split()
            if not phrase:
                continue
            aliases[(slug, phrase)] = {
                "target_id": f"model_map:stable:{slug}",
                "signal": name,
                "phrase": phrase,
                "compact": re.sub(r"[^a-z0-9]", "", name.lower()),
                "token_count": len(tokens),
                "alias_kind": alias_kind,
            }
    return sorted(aliases.values(), key=lambda row: (-int(row["token_count"]), -len(str(row["phrase"])), str(row["target_id"])))


def model_relationships_for_idea(title: str, aliases: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    normalized = f" {normalized_phrase(title)} "
    raw_words = {value.lower() for value in re.findall(r"\b[A-Za-z][A-Za-z0-9]+\b", title)}
    matches: list[dict[str, str]] = []
    seen: set[str] = set()
    for alias in aliases:
        target_id = str(alias.get("target_id") or "")
        phrase = str(alias.get("phrase") or "")
        compact = str(alias.get("compact") or "")
        token_count = int(alias.get("token_count") or 0)
        matched = token_count >= 2 and f" {phrase} " in normalized
        if not matched and compact:
            matched = compact in raw_words
        if matched and target_id and target_id not in seen:
            matches.append({"target_id": target_id, "signal": str(alias.get("signal") or phrase)})
            seen.add(target_id)
        if len(matches) >= 8:
            break
    return matches


def release_relationships_for_idea(
    idea: dict[str, Any],
    releases: Iterable[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    version = str(idea.get("planned_version") or "")
    status = str(idea.get("status") or "")
    title_tokens = release_title_tokens(str(idea.get("title") or ""))
    if not version or status not in {"complete", "planned", "started"} or len(title_tokens) < 3:
        return [], []
    public: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for release in releases:
        if str(release.get("version") or "") != version:
            continue
        release_tokens = release_title_tokens(str(release.get("summary") or ""))
        overlap = title_tokens & release_tokens
        coverage = len(overlap) / len(title_tokens)
        if len(overlap) < 2 or coverage < 0.6:
            continue
        record_id = str(release.get("id") or "")
        if not record_id:
            continue
        enriched = {
            **release,
            "record_id": record_id,
            "url": release_url(release),
            "coverage": round(coverage, 4),
        }
        if coverage == 1.0:
            public.append(enriched)
            continue
        candidate_identity = {
            "source_id": idea.get("idea_id"),
            "release_record_id": record_id,
            "coverage": round(coverage, 4),
        }
        digest = sha256_text(json.dumps(candidate_identity, sort_keys=True, separators=(",", ":")))
        candidates.append(
            {
                "schema": "rock-kb-rock-idea-relationship-candidate-v1",
                "candidate_id": f"rock_idea_relationship_candidate:{digest[:24]}",
                "source_id": idea.get("idea_id"),
                "release_record_id": record_id,
                "release_version": version,
                "release_module": release.get("module"),
                "title_token_coverage": round(coverage, 4),
                "basis": "planned_version_and_partial_title_token_overlap",
                "review_required": True,
            }
        )
    return public, candidates


def validate_rock_idea_relationship_rows(
    rows: Iterable[dict[str, Any]],
    *,
    idea_rows: Iterable[dict[str, Any]],
) -> None:
    idea_ids = {str(row.get("idea_id") or "") for row in idea_rows}
    seen: set[str] = set()
    forbidden = {"description", "body", "response", "response_text", "comments", "author", "submitter", "organization"}
    for index, row in enumerate(rows, 1):
        relationship_id = str(row.get("relationship_id") or "")
        if row.get("schema") != "rock-kb-rock-idea-relationship-v1" or not relationship_id.startswith("rock_idea_relationship:"):
            raise ValueError(f"Rock idea relationship row {index} has an invalid schema or ID")
        if relationship_id in seen:
            raise ValueError(f"Duplicate Rock idea relationship ID: {relationship_id}")
        seen.add(relationship_id)
        if row.get("source_id") not in idea_ids:
            raise ValueError(f"Rock idea relationship {relationship_id} has an unknown source idea")
        if row.get("relationship_type") not in RELATIONSHIP_TYPES:
            raise ValueError(f"Rock idea relationship {relationship_id} has an invalid type")
        if not row.get("target_id") and not row.get("target_url"):
            raise ValueError(f"Rock idea relationship {relationship_id} has no target")
        if forbidden & set(row):
            raise ValueError(f"Rock idea relationship {relationship_id} contains disallowed raw content")
        if row.get("needs_live_verification") is not True:
            raise ValueError(f"Rock idea relationship {relationship_id} must require verification")
        if row.get("relationship_type") == "implemented_by_issue" and not (
            str(row.get("target_id") or "").startswith("rock_issue:")
            and row.get("authority_tier") == "official"
            and row.get("confidence") == "high"
            and row.get("basis") == "official_release_note_match_and_issue_ref"
        ):
            raise ValueError(f"Rock idea relationship {relationship_id} overstates issue implementation evidence")


def issue_id_index(rows: Iterable[dict[str, Any]]) -> dict[tuple[str, int], str]:
    indexed: dict[tuple[str, int], str] = {}
    for row in rows:
        repository = str(row.get("repository") or "")
        family = "mobile" if repository == "SparkDevNetwork/Rock.Mobile-Issues" else "core"
        number = int(row.get("number") or 0)
        issue_id = str(row.get("issue_id") or "")
        if number and issue_id:
            indexed[(family, number)] = issue_id
    return indexed


def source_target_index(rows: Iterable[dict[str, Any]]) -> dict[str, str]:
    indexed: dict[str, str] = {}
    for row in rows:
        source_record_id = str(row.get("source_record_id") or "")
        if not source_record_id:
            continue
        target_id = f"source:{source_record_id}"
        urls = [str(row.get("source_url") or "")]
        urls.extend(
            str(citation.get("url") or "")
            for citation in row.get("citations") or []
            if isinstance(citation, dict)
        )
        for url in urls:
            canonical = canonical_evidence_url(url)
            if canonical:
                indexed.setdefault(canonical, target_id)
    return indexed


def canonical_evidence_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        return ""
    path = re.sub(r"/{2,}", "/", parsed.path).rstrip("/").lower()
    return f"https://{parsed.hostname.lower()}{path}"


def release_title_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2 and token not in RELEASE_TITLE_STOPWORDS
    }


def normalized_phrase(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def release_url(row: dict[str, Any]) -> str:
    return (
        "https://www.rockrms.com/mobilereleasenotes"
        if str(row.get("release_family") or "") == "mobile"
        else "https://www.rockrms.com/releasenotes"
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
