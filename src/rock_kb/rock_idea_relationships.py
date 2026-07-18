from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.parse import urlparse

from .extract import sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, REVIEW_DIR


ROCK_IDEA_RELATIONSHIP_PATH = AGENT_DIR / "rock-idea-relationships.jsonl"
ROCK_IDEA_RELATIONSHIP_CANDIDATE_PATH = REVIEW_DIR / "rock-ideas" / "relationship-candidates.jsonl"

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
    relationships, candidates = rock_idea_relationship_rows(
        idea_rows,
        model_rows=model_rows,
        release_rows=release_rows,
        issue_rows=issue_rows,
        source_rows=source_rows,
        checked_at=checked_at,
    )
    validate_rock_idea_relationship_rows(relationships, idea_rows=idea_rows)
    write_jsonl(ROCK_IDEA_RELATIONSHIP_PATH, relationships)
    write_jsonl(ROCK_IDEA_RELATIONSHIP_CANDIDATE_PATH, candidates)
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
    }


def rock_idea_relationship_rows(
    ideas: Iterable[dict[str, Any]],
    *,
    model_rows: Iterable[dict[str, Any]],
    release_rows: Iterable[dict[str, Any]],
    issue_rows: Iterable[dict[str, Any]],
    source_rows: Iterable[dict[str, Any]] = (),
    checked_at: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    idea_rows = list(ideas)
    releases = list(release_rows)
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

    deduped = {str(row["relationship_id"]): row for row in edges}
    candidate_rows = {str(row["candidate_id"]): row for row in candidates}
    return (
        sorted(deduped.values(), key=lambda row: (str(row["source_id"]), str(row["relationship_type"]), str(row.get("target_id") or row.get("target_url") or ""))),
        sorted(candidate_rows.values(), key=lambda row: (str(row["source_id"]), -float(row["title_token_coverage"]), str(row["release_record_id"]))),
    )


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
