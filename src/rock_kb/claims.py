from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Optional

from pydantic import ValidationError

from .extract import generated_at_iso, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import CLAIMS_DIR, REPO_ROOT, REVIEW_DIR
from .private_leakage import direct_or_tokenized_media_url, find_leaks
from .schemas import Claim

CLAIM_SCHEMA = "rock-kb-claim-v1"
APPROVED_CLAIMS_PATH = CLAIMS_DIR / "approved-claims.jsonl"
CLAIM_EXPORT_REPORT_PATH = CLAIMS_DIR / "claim-export-report.json"
LIVE_CLAIM_VERIFICATIONS_PATH = REVIEW_DIR / "live-claim-verifications.jsonl"
LIVE_CLAIM_VERIFICATION_SUPPLEMENTAL_PATTERN = "live-claim-verifications-*.jsonl"
SOURCE_CLAIM_REVIEWS_DIR = REVIEW_DIR / "source-claim-reviews"
SOURCE_CLAIM_REVIEW_SCHEMA = "rock-kb-source-claim-review-v1"

CLAIM_TYPES = {
    "behavior",
    "configuration",
    "implementation_pattern",
    "release_caveat",
    "risk",
    "recipe",
    "source_summary",
    "operational_guidance",
}

AUTHORITY_TIERS = {
    "official",
    "rocku-confirmed",
    "release-note-confirmed",
    "source-code-confirmed",
    "community-reviewed",
    "community-unreviewed",
    "agent-inference",
    "private-draft",
    "needs-live-verification",
}

PUBLIC_REVIEW_STATUSES = {
    "approved_for_public_distillation",
    "redaction_reviewed",
    "public_reviewed",
}
CLAIM_TIERS = {
    "source_backed",
    "answer_pack_approved",
    "live_verified",
    "routing_context_only",
}

CONFIDENCE_LEVELS = {"low", "medium", "high", "needs_review"}
LICENSE_STATUSES = {"public", "cite_and_summarize_only", "manual_review_required", "private_only", "unknown"}
PUBLIC_PUBLISH_MODES = {"public", "public_cite_and_summarize_only", "manual_review_required"}

def approved_claims_path() -> Path:
    return APPROVED_CLAIMS_PATH


def build_approved_claims(output_path: Optional[Path] = None) -> dict[str, Any]:
    raw_claims = sorted(
        apply_live_claim_verifications(
            [
                *claims_from_media_public_promotions(),
                *claims_from_source_claim_reviews(),
            ]
        ),
        key=lambda row: row["claim_id"],
    )
    claims = [Claim.model_validate(row).public_dump() for row in raw_claims]
    output = output_path or APPROVED_CLAIMS_PATH
    errors = validate_claim_rows(claims, public=True)
    if errors:
        raise ValueError("\n".join(errors))
    count = write_jsonl(output, claims)
    report = claim_export_report(claims, output)
    CLAIM_EXPORT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLAIM_EXPORT_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema": "rock-kb-claim-build-result-v1",
        "status": "ok",
        "claim_count": count,
        "output": repo_relative_path(output),
        "report": repo_relative_path(CLAIM_EXPORT_REPORT_PATH),
    }


def validate_claim_file(path: Path = APPROVED_CLAIMS_PATH, public: bool = True) -> list[str]:
    return validate_claim_rows(list(read_jsonl(path)), public=public, label=str(path))


def validate_claim_rows(rows: Iterable[dict[str, Any]], public: bool = True, label: str = "claim") -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    known_concept_ids = load_known_concept_ids()
    for index, row in enumerate(rows, start=1):
        row_label = f"{label}:{index}"
        claim_id = str(row.get("claim_id") or "")
        if claim_id in seen:
            errors.append(f"{row_label} duplicate claim_id {claim_id}")
        if claim_id:
            seen.add(claim_id)
        errors.extend(validate_claim_row(row, row_label, public=public, known_concept_ids=known_concept_ids))
    return errors


def validate_claim_row(
    row: dict[str, Any],
    label: str = "claim",
    public: bool = True,
    known_concept_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    try:
        Claim.model_validate(row)
    except ValidationError as exc:
        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc") or [])
            errors.append(f"{label} schema error at {location or '$'}: {error.get('msg')}")
    errors.extend(validate_claim_concepts(row, label, known_concept_ids=known_concept_ids))
    if not row.get("source_refs") and not row.get("source_record_ids"):
        errors.append(f"{label} must include source_refs or source_record_ids")
    if public:
        errors.extend(f"{label} {message}" for message in find_leaks(row))
    return errors


def load_known_concept_ids() -> set[str]:
    from .concepts import load_concepts

    return {concept.id for concept in load_concepts()}


def validate_claim_concepts(row: dict[str, Any], label: str, known_concept_ids: set[str] | None = None) -> list[str]:
    values = row.get("concept_ids")
    if not isinstance(values, list) or not values:
        return [f"{label} concept_ids must be a non-empty list"]
    known = known_concept_ids if known_concept_ids is not None else load_known_concept_ids()
    unknown = sorted(str(value) for value in values if str(value) not in known)
    if unknown:
        return [f"{label} unknown concept_ids: {', '.join(unknown)}"]
    return []


def approved_claim_rows(path: Path = APPROVED_CLAIMS_PATH) -> list[dict[str, Any]]:
    return [row for row in read_jsonl(path) if row.get("review_status") in PUBLIC_REVIEW_STATUSES]


def approved_claim_dependencies_for_concept(
    concept_id: str,
    guide_text: str = "",
    coverage_text: str = "",
    path: Path = APPROVED_CLAIMS_PATH,
) -> list[dict[str, Any]]:
    dependencies = []
    search_text = "\n".join(value for value in [guide_text, coverage_text] if value)
    for row in approved_claim_rows(path):
        if concept_id not in {str(value) for value in row.get("concept_ids") or []}:
            continue
        refs = row.get("source_refs") or []
        ref_urls = [
            str(ref.get("url") or "")
            for ref in refs
            if isinstance(ref, dict)
        ]
        timestamp_urls = [
            str(ref.get("source_timestamp_url") or "")
            for ref in refs
            if isinstance(ref, dict)
        ]
        claim_text = str(row.get("claim") or "")
        mentioned = bool(
            search_text
            and (
                str(row.get("claim_id") or "") in search_text
                or any(url and url in search_text for url in [*ref_urls, *timestamp_urls])
                or (claim_text[:90] and claim_text[:90] in search_text)
            )
        )
        dependencies.append(
            {
                "claim_id": row.get("claim_id"),
                "claim_hash": approved_claim_hash(row),
                "claim": claim_text,
                "claim_type": row.get("claim_type"),
                "authority_tier": row.get("authority_tier"),
                "claim_tier": row.get("claim_tier"),
                "confidence": row.get("confidence"),
                "review_status": row.get("review_status"),
                "concept_ids": row.get("concept_ids") or [],
                "source_record_ids": row.get("source_record_ids") or [],
                "source_refs": refs,
                "safe_evidence_hash": row.get("safe_evidence_hash"),
                "needs_live_verification": bool(row.get("needs_live_verification")),
                "live_verification": public_safe_live_verification(row.get("live_verification") or {}),
                "community_derived": bool(row.get("community_derived")),
                "mentioned_in_guide": mentioned,
            }
        )
    return sorted(dependencies, key=lambda item: str(item.get("claim_id") or ""))


def approved_claim_hash(row: dict[str, Any]) -> str:
    stable_payload = {
        "claim_id": row.get("claim_id"),
        "claim": row.get("claim"),
        "claim_type": row.get("claim_type"),
        "concept_ids": row.get("concept_ids") or [],
        "source_refs": row.get("source_refs") or [],
        "source_record_ids": row.get("source_record_ids") or [],
        "authority_tier": row.get("authority_tier"),
        "confidence": row.get("confidence"),
        "review_status": row.get("review_status"),
        "license_status": row.get("license_status"),
        "public_publish_mode": row.get("public_publish_mode"),
        "rock_versions": row.get("rock_versions") or [],
        "safe_evidence_hash": row.get("safe_evidence_hash"),
        "needs_live_verification": row.get("needs_live_verification"),
        "claim_tier": row.get("claim_tier"),
        "live_verification": row.get("live_verification") or {},
    }
    return sha256_text(json.dumps(stable_payload, ensure_ascii=False, sort_keys=True))


def public_safe_live_verification(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or not value:
        return {}
    refs = []
    for ref in value.get("evidence_refs") or []:
        if not isinstance(ref, dict):
            continue
        public_ref = {
            key: ref.get(key)
            for key in ["probe_id", "probe_type", "tables"]
            if ref.get(key)
        }
        if public_ref:
            refs.append(public_ref)
    return {
        "verification_scope": value.get("verification_scope") or "connected_read_only_rock_instance",
        "verified_at": value.get("verified_at") or now_iso(),
        "verified_by": "read_only_verification",
        "verification_method": value.get("verification_method") or "read_only_live_probe",
        "evidence_refs": refs,
        "notes": [sanitize_public_verification_note(str(note)) for note in value.get("notes") or [] if note],
    }


def sanitize_public_verification_note(value: str) -> str:
    replacements = {
        "ONE&ALL RockDB": "a connected Rock instance",
        "ONE&ALL's Rock production SQL surface": "a connected Rock instance",
        "RockProduction source": "a private source checkout",
        "RockProduction": "a private source checkout",
        "RockDB": "a connected Rock database",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def claims_from_media_public_promotions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((REVIEW_DIR / "public-media-promotions").glob("*.jsonl")):
        for promotion in read_jsonl(path):
            if promotion.get("review_status") not in PUBLIC_REVIEW_STATUSES:
                continue
            rows.extend(media_promotion_to_claims(promotion))
    return rows


def claims_from_source_claim_reviews(path: Path | None = None) -> list[dict[str, Any]]:
    review_path = path or SOURCE_CLAIM_REVIEWS_DIR
    if not review_path.exists():
        return []
    files = sorted(review_path.glob("*.jsonl")) if review_path.is_dir() else [review_path]
    rows: list[dict[str, Any]] = []
    for file_path in files:
        for row in read_jsonl(file_path):
            if row.get("review_status") not in PUBLIC_REVIEW_STATUSES:
                continue
            rows.append(source_claim_review_to_claim(row))
    return rows


def source_claim_review_to_claim(row: dict[str, Any]) -> dict[str, Any]:
    source_refs = safe_source_refs(row.get("source_refs") or [])
    if not source_refs:
        url = safe_source_url(row.get("source_url"))
        if url:
            source_refs = [
                {
                    "source_id": row.get("source_id"),
                    "url": url,
                    "title": row.get("source_title") or row.get("title"),
                }
            ]
    reviewed_at = row.get("reviewed_at") or now_iso()
    claim = {
        "schema": CLAIM_SCHEMA,
        "claim_type": row.get("claim_type") or claim_type_from_topic(str(row.get("topic") or "")),
        "concept_ids": sorted({str(value) for value in row.get("concept_ids") or [] if value}),
        "source_refs": source_refs,
        "source_record_ids": [str(value) for value in row.get("source_record_ids") or [] if value],
        "authority_tier": row.get("authority_tier") or "official",
        "confidence": row.get("confidence") or "high",
        "review_status": row.get("review_status"),
        "license_status": row.get("license_status") or "cite_and_summarize_only",
        "public_publish_mode": row.get("public_publish_mode") or "public_cite_and_summarize_only",
        "rock_versions": row.get("rock_versions") or [],
        "safe_evidence_hash": row.get("safe_evidence_hash") or sha256_text(
            json.dumps(
                {
                    "claim": row.get("claim"),
                    "source_refs": source_refs,
                    "source_record_ids": row.get("source_record_ids") or [],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        ),
        "needs_live_verification": bool(row.get("needs_live_verification")),
        "created_at": reviewed_at,
        "updated_at": reviewed_at,
        "claim": str(row.get("claim") or "").strip(),
        "derived_from": {
            "type": "source_claim_review",
            "id": row.get("id"),
            "schema": row.get("schema") or SOURCE_CLAIM_REVIEW_SCHEMA,
            "reviewer": row.get("reviewer"),
        },
        "community_derived": str(row.get("authority_tier") or "").startswith("community"),
    }
    return claim_with_id(claim)


def safe_source_refs(values: list[Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for value in values:
        if not isinstance(value, dict):
            continue
        url = safe_source_url(value.get("url"))
        if not url:
            continue
        ref = {
            "source_id": value.get("source_id"),
            "url": url,
            "title": value.get("title"),
        }
        for key in ["timestamp", "timestamp_seconds", "source_timestamp_url"]:
            if value.get(key) is not None:
                ref[key] = value.get(key)
        refs.append(ref)
    return refs


def live_claim_verification_paths(path: Path | None = None) -> list[Path]:
    verification_path = path or LIVE_CLAIM_VERIFICATIONS_PATH
    paths = [verification_path] if verification_path.exists() else []
    if path is None:
        for candidate in sorted(verification_path.parent.glob(LIVE_CLAIM_VERIFICATION_SUPPLEMENTAL_PATTERN)):
            if candidate != verification_path and candidate.exists():
                paths.append(candidate)
    return paths


def load_live_claim_verifications(path: Path | None = None) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for verification_path in live_claim_verification_paths(path):
        for line_number, row in enumerate(read_jsonl(verification_path), start=1):
            claim_id = str(row.get("claim_id") or "").strip()
            if not claim_id:
                raise ValueError(f"{verification_path}:{line_number} is missing claim_id")
            claim_tier = str(row.get("claim_tier") or row.get("verification_status") or "").strip()
            if claim_tier not in CLAIM_TIERS:
                raise ValueError(f"{verification_path}:{line_number} claim_tier must be one of: {', '.join(sorted(CLAIM_TIERS))}")
            rows[claim_id] = row
    return rows


def apply_live_claim_verifications(claims: list[dict[str, Any]], verifications_by_claim_id: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    verifications = verifications_by_claim_id if verifications_by_claim_id is not None else load_live_claim_verifications()
    if not verifications:
        return claims
    updated_claims = []
    for claim in claims:
        verification = verifications.get(str(claim.get("claim_id") or ""))
        if not verification:
            updated_claims.append(claim)
            continue
        updated = dict(claim)
        claim_tier = str(verification.get("claim_tier") or verification.get("verification_status") or "")
        updated["claim_tier"] = claim_tier
        if claim_tier == "live_verified":
            updated["needs_live_verification"] = False
            updated["live_verification"] = public_safe_live_verification({
                "instance": verification.get("instance") or "connected-rock-instance",
                "verified_at": verification.get("verified_at") or now_iso(),
                "verified_by": verification.get("verified_by") or "codex-readonly-sql",
                "verification_method": verification.get("verification_method") or "read_only_sql",
                "evidence_refs": verification.get("evidence_refs") or [],
                "notes": verification.get("notes") or [],
            })
        elif verification.get("notes"):
            updated["verification_notes"] = verification.get("notes")
        updated_claims.append(updated)
    return updated_claims


def media_promotion_to_claims(row: dict[str, Any]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    base_refs = source_refs_from_promotion(row)
    base = {
        "schema": CLAIM_SCHEMA,
        "claim_type": "source_summary",
        "concept_ids": sorted({str(value) for value in row.get("concept_ids") or [] if value}),
        "source_refs": base_refs,
        "source_record_ids": [str(row.get("source_record_id"))] if row.get("source_record_id") else [],
        "authority_tier": authority_tier_for_promotion(row),
        "confidence": "medium",
        "review_status": row.get("review_status"),
        "license_status": "cite_and_summarize_only",
        "public_publish_mode": "public_cite_and_summarize_only",
        "rock_versions": [],
        "timestamp": None,
        "timestamp_seconds": None,
        "source_timestamp_url": None,
        "safe_evidence_hash": row.get("transcript_hash") or row.get("content_hash"),
        "private_corpus_pointer": private_corpus_pointer_for_promotion(row),
        "needs_live_verification": row.get("source_kind") not in {"rock_documentation", "rock_release_notes", "github_repo"},
        "created_at": row.get("reviewed_at") or now_iso(),
        "updated_at": row.get("reviewed_at") or now_iso(),
        "derived_from": {
            "type": "media_public_promotion",
            "id": row.get("id"),
            "candidate_id": row.get("candidate_id"),
            "source_id": row.get("source_id"),
        },
        "community_derived": authority_tier_for_promotion(row).startswith("community"),
    }
    summary = str(row.get("summary") or "").strip()
    if summary:
        claims.append(claim_with_id({**base, "claim": summary}))
    for item in row.get("key_insights") or []:
        if not isinstance(item, dict):
            continue
        text = str(item.get("insight") or item.get("claim") or "").strip()
        if not text:
            continue
        item_refs = source_refs_from_insight(row, item) or base_refs
        claim = {
            **base,
            "claim": text,
            "claim_type": claim_type_from_topic(str(item.get("topic") or "")),
            "concept_ids": sorted({*base["concept_ids"], *[str(value) for value in item.get("concept_ids") or [] if value]}),
            "source_refs": item_refs,
            "timestamp": item.get("timestamp"),
            "timestamp_seconds": item.get("timestamp_seconds"),
            "source_timestamp_url": safe_timestamp_url(item.get("source_timestamp_url") or item.get("source_url")),
        }
        claims.append(claim_with_id(claim))
    return claims


def claim_with_id(row: dict[str, Any]) -> dict[str, Any]:
    stable_payload = {
        "claim": row.get("claim"),
        "source_refs": row.get("source_refs") or [],
        "source_record_ids": row.get("source_record_ids") or [],
        "concept_ids": row.get("concept_ids") or [],
        "authority_tier": row.get("authority_tier"),
    }
    row["claim_id"] = "claim:" + sha256_text(json.dumps(stable_payload, sort_keys=True))[:20]
    row.update(claim_concept_assignment_metadata(row))
    row.update(claim_usefulness_metadata(row))
    row["claim_tier"] = claim_tier_for_claim(row)
    return row


def claim_tier_for_claim(row: dict[str, Any]) -> str:
    if not row.get("answer_candidate"):
        return "routing_context_only"
    if row.get("needs_live_verification") or row.get("requires_live_instance"):
        return "source_backed"
    return "answer_pack_approved"


def claim_concept_assignment_metadata(row: dict[str, Any]) -> dict[str, Any]:
    concept_ids = [str(value) for value in row.get("concept_ids") or []]
    if not concept_ids:
        return {"primary_concept_id": "", "secondary_concept_ids": [], "concept_assignment_reason": "no_concept_ids"}
    text = " ".join(
        [
            str(row.get("claim") or ""),
            *[
                " ".join(str(ref.get(key) or "") for key in ["title", "url", "source_id"])
                for ref in row.get("source_refs") or []
                if isinstance(ref, dict)
            ],
        ]
    ).lower()
    scores = {concept_id: concept_assignment_score(concept_id, text) for concept_id in concept_ids}
    primary = max(concept_ids, key=lambda concept_id: (scores[concept_id], -concept_ids.index(concept_id), concept_id))
    explicit_secondaries = [
        concept_id
        for concept_id in concept_ids
        if concept_id != primary and scores[concept_id] >= 2
    ]
    reason = "source_text_matched_primary_concept" if scores[primary] else "fallback_first_concept"
    return {
        "primary_concept_id": primary,
        "secondary_concept_ids": explicit_secondaries,
        "concept_assignment_reason": reason,
    }


def concept_assignment_score(concept_id: str, text: str) -> int:
    aliases = {
        "workflows": ["workflow", "workflows", "workflowtype", "/workflows/"],
        "security-permissions": ["security", "permission", "permissions", "auth", "role"],
        "data-views-reports": ["data view", "dataview", "report", "reports", "sql", "analytics"],
        "mobile": ["mobile", "shell", "css", "dark mode", "ios", "android"],
        "check-in": ["check-in", "check in", "attendance", "kiosk", "label"],
        "connections": ["connection", "connections", "opportunity", "request status"],
        "groups": ["group", "groups", "group type", "group member"],
        "communications": ["communication", "email", "sms", "recipient"],
        "cms-websites": ["cms", "website", "page", "block", "content channel"],
        "api-integrations": ["api", "webhook", "integration", "rest"],
        "developer-resources": ["developer", "obsidian", "plugin", "package", "api", "code"],
        "helix": ["helix", "htmx", "lava application", "lava endpoint", "lava command"],
        "tv-apps": ["tv app", "tv apps", "tvml", "scenegraph", "apple tv", "roku"],
        "apple-tv": ["apple tv", "tvml", "tvos"],
        "roku": ["roku", "scenegraph"],
    }
    terms = aliases.get(concept_id, [concept_id.replace("-", " ")])
    score = 0
    for term in terms:
        if term and term in text:
            score += 2 if " " in term or "/" in term else 1
    return score


def claim_usefulness_metadata(row: dict[str, Any]) -> dict[str, Any]:
    text = f"{row.get('claim') or ''} {row.get('claim_type') or ''}".lower()
    authority_scores = {
        "official": 100,
        "source-code-confirmed": 92,
        "release-note-confirmed": 88,
        "rocku-confirmed": 84,
        "community-reviewed": 64,
        "community-unreviewed": 28,
        "agent-inference": 20,
        "needs-live-verification": 18,
        "private-draft": 5,
    }
    type_scores = {
        "risk": 18,
        "configuration": 16,
        "implementation_pattern": 14,
        "operational_guidance": 12,
        "release_caveat": 10,
        "behavior": 8,
        "recipe": 6,
        "source_summary": 4,
    }
    failure_terms = {
        "missing": ["missing", "not appear", "not showing", "invisible", "unavailable"],
        "permission": ["security", "permission", "access", "role", "auth"],
        "configuration": ["setting", "configuration", "configure", "option"],
        "workflow": ["workflow", "action", "trigger", "launch"],
        "data": ["data view", "report", "sql", "analytics", "filter"],
        "mobile": ["mobile", "app", "shell", "block", "css", "dark mode"],
        "release": ["release", "version", "upgrade", "deprecated"],
    }
    matched_failure_modes = [
        name
        for name, terms in failure_terms.items()
        if any(term in text for term in terms)
    ]
    priority = authority_scores.get(str(row.get("authority_tier") or ""), 0)
    priority += type_scores.get(str(row.get("claim_type") or ""), 0)
    priority += min(12, len(matched_failure_modes) * 3)
    if row.get("needs_live_verification"):
        priority -= 8
    generic_training_context = any(
        phrase in text
        for phrase in [
            "training context",
            "not as a substitute",
            "canonical lesson page",
            "helps route agents",
            "when applying ",
            "convert the episode context into source-backed rock guidance",
            "gives public operational perspective",
            "use it to frame questions",
        ]
    )
    if generic_training_context:
        priority -= 28
    requires_live_instance = bool(
        row.get("needs_live_verification")
        or any(term in text for term in ["live", "instance", "configuration", "setting", "permission", "data view", "workflow"])
    )
    return {
        "operational_priority": max(0, min(100, priority)),
        "common_failure_mode": matched_failure_modes,
        "answer_candidate": not generic_training_context
        and (priority >= 72 or str(row.get("claim_type") or "") in {"configuration", "implementation_pattern", "operational_guidance"}),
        "requires_live_instance": requires_live_instance,
    }


def source_refs_from_promotion(row: dict[str, Any]) -> list[dict[str, Any]]:
    refs = []
    citations = row.get("citations") or []
    for citation in citations:
        if not isinstance(citation, dict):
            continue
        url = safe_source_url(citation.get("url"))
        if not url:
            continue
        refs.append(
            {
                "source_id": citation.get("source_id") or row.get("source_id"),
                "url": url,
                "title": citation.get("title") or row.get("source_title"),
            }
        )
    if not refs:
        url = safe_source_url(row.get("source_url"))
        if url:
            refs.append({"source_id": row.get("source_id"), "url": url, "title": row.get("source_title")})
    return refs


def source_refs_from_insight(row: dict[str, Any], item: dict[str, Any]) -> list[dict[str, Any]]:
    url = safe_source_url(item.get("source_url") or row.get("source_url"))
    if not url:
        return []
    ref: dict[str, Any] = {"source_id": row.get("source_id"), "url": url, "title": row.get("source_title")}
    if item.get("timestamp"):
        ref["timestamp"] = item.get("timestamp")
    if item.get("timestamp_seconds") is not None:
        ref["timestamp_seconds"] = item.get("timestamp_seconds")
    source_timestamp_url = safe_timestamp_url(item.get("source_timestamp_url"))
    if source_timestamp_url:
        ref["source_timestamp_url"] = source_timestamp_url
    return [ref]


def safe_source_url(value: Any) -> str:
    url = str(value or "").strip()
    if not url or direct_or_tokenized_media_url(url):
        return ""
    return url


def safe_timestamp_url(value: Any) -> Optional[str]:
    url = safe_source_url(value)
    return url or None


def authority_tier_for_promotion(row: dict[str, Any]) -> str:
    source_id = str(row.get("source_id") or "")
    source_kind = str(row.get("source_kind") or "")
    if source_id == "rock_rocku" or source_kind == "rocku":
        return "rocku-confirmed"
    if source_id == "rock_youtube":
        return "official"
    if source_id.startswith("rock_core_release") or source_kind == "rock_release_notes":
        return "release-note-confirmed"
    if source_kind == "github_repo":
        return "source-code-confirmed"
    if "community" in source_id or "community" in source_kind:
        return "community-reviewed"
    return "community-reviewed"


def claim_type_from_topic(topic: str) -> str:
    lowered = topic.lower()
    if "risk" in lowered or "security" in lowered:
        return "risk"
    if "release" in lowered or "version" in lowered:
        return "release_caveat"
    if "configuration" in lowered or "setting" in lowered:
        return "configuration"
    if "workflow" in lowered or "implementation" in lowered or "pattern" in lowered:
        return "implementation_pattern"
    return "operational_guidance"


def private_corpus_pointer_for_promotion(row: dict[str, Any]) -> Optional[dict[str, str]]:
    source_id = str(row.get("source_id") or "")
    media_id = str(row.get("media_id") or "")
    if not source_id or not media_id:
        return None
    return {"kind": "media_transcript", "source_id": source_id, "media_id": media_id}


def claim_export_report(rows: list[dict[str, Any]], output: Path) -> dict[str, Any]:
    return {
        "schema": "rock-kb-claim-export-report-v1",
        "generated_at": generated_at_iso(),
        "output": repo_relative_path(output),
        "claim_count": len(rows),
        "authority_tiers": count_values(row.get("authority_tier") for row in rows),
        "claim_tiers": count_values(row.get("claim_tier") for row in rows),
        "claim_types": count_values(row.get("claim_type") for row in rows),
        "concept_ids": count_values(concept for row in rows for concept in row.get("concept_ids") or []),
        "review_statuses": count_values(row.get("review_status") for row in rows),
    }


def repo_relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def count_values(values: Iterable[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))
