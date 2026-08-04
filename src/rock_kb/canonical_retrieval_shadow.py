from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from pathlib import Path
from time import perf_counter
from typing import Any, Iterable
from urllib.parse import quote

from .canonical_knowledge import (
    SHADOW_DIR,
    SUPPORTED_SEARCH_KINDS,
    write_canonical_knowledge_shadow,
)
from .extract import sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT
from .reviewed_cross_source import reviewed_cross_source_evaluation_rows
from .schemas import EvidenceLink, KnowledgeUnit, SourceSnapshot, SourceUnit
from .service_eval import EVALUATION_SET_PATH, evaluation_metrics, hit_concepts
from .service_projection import AUTHORITY_TIER_RANK, SERVICE_DIR, build_search_rows
from .source_native import source_native_evaluation_rows


RAW_RESULTS_PATH = SHADOW_DIR / "retrieval-raw.json"
RETRIEVAL_REPORT_PATH = SHADOW_DIR / "retrieval-report.json"
ENDPOINT_CASES_PATH = SHADOW_DIR / "endpoint-compatibility-cases.jsonl"
CLAIM_COLLAPSE_REVIEW_PATH = SHADOW_DIR / "claim-collapse-review.json"
CLAIM_COLLAPSE_MAINTAINER_REVIEW_PATH = (
    SHADOW_DIR / "claim-collapse-maintainer-review.json"
)
NODE_RUNNER_PATH = SERVICE_DIR / "tools" / "canonical-retrieval-shadow.mjs"
WORKER_BUNDLE_PATH = SERVICE_DIR / "dist" / "dry-run" / "index.js"
SHADOW_NO_ANSWER_EVALUATIONS = (
    {
        "schema": "rock-kb-service-evaluation-case-v1",
        "id": "shadow-no-answer-unknown-token",
        "question": "zzyzxquasar998877",
        "concept_id": "",
        "source": "canonical_shadow_no_answer",
        "evaluation_mode": "retrieval",
        "expect_no_results": True,
    },
)


def run_canonical_retrieval_shadow(
    destination: Path = SHADOW_DIR,
    *,
    limit: int = 5,
    build_worker: bool = True,
) -> dict[str, Any]:
    """Compare current and canonical rows through the bundled production Worker."""

    destination.mkdir(parents=True, exist_ok=True)
    projection_summary = write_canonical_knowledge_shadow(destination)
    baseline_rows = build_search_rows()
    knowledge_units = [
        KnowledgeUnit.model_validate(row)
        for row in read_jsonl(destination / "knowledge-units.jsonl")
    ]
    snapshots = [
        SourceSnapshot.model_validate(row)
        for row in read_jsonl(destination / "source-snapshots.jsonl")
    ]
    source_units = [
        SourceUnit.model_validate(row)
        for row in read_jsonl(destination / "source-units.jsonl")
    ]
    evidence_links = [
        EvidenceLink.model_validate(row)
        for row in read_jsonl(destination / "evidence-links.jsonl")
    ]
    candidate_rows = build_canonical_search_rows(
        baseline_rows=baseline_rows,
        knowledge_units=knowledge_units,
        source_snapshots=snapshots,
        source_units=source_units,
    )
    baseline_path = destination / "baseline-search-rows.jsonl"
    candidate_path = destination / "candidate-search-rows.jsonl"
    evaluation_path = destination / "retrieval-evaluation-set.jsonl"
    endpoint_cases_path = destination / "endpoint-compatibility-cases.jsonl"
    raw_path = destination / "retrieval-raw.json"
    report_path = destination / "retrieval-report.json"
    evaluations = [
        *read_jsonl(EVALUATION_SET_PATH),
        *SHADOW_NO_ANSWER_EVALUATIONS,
        *source_native_evaluation_rows(REPO_ROOT),
        *reviewed_cross_source_evaluation_rows(REPO_ROOT),
    ]
    endpoint_cases = build_endpoint_compatibility_cases(baseline_rows)
    claim_collapse_review = write_claim_collapse_review(
        destination,
        baseline_rows=baseline_rows,
        knowledge_units=knowledge_units,
        source_snapshots=snapshots,
        source_units=source_units,
        evidence_links=evidence_links,
    )
    write_jsonl(baseline_path, baseline_rows)
    write_jsonl(candidate_path, candidate_rows)
    write_jsonl(evaluation_path, evaluations)
    write_jsonl(endpoint_cases_path, endpoint_cases)

    if build_worker:
        subprocess.run(
            ["npm", "run", "wrangler:check"],
            cwd=SERVICE_DIR,
            check=True,
            env={
                **os.environ,
                "CI": "1",
                "WRANGLER_SEND_METRICS": "false",
            },
        )
    if not WORKER_BUNDLE_PATH.exists():
        raise RuntimeError(
            "The production Worker bundle is missing. Run "
            "`npm run wrangler:check` in `service/` first."
        )
    subprocess.run(
        [
            "node",
            str(NODE_RUNNER_PATH),
            "--baseline",
            str(baseline_path.resolve()),
            "--candidate",
            str(candidate_path.resolve()),
            "--evaluation",
            str(evaluation_path.resolve()),
            "--endpoint-cases",
            str(endpoint_cases_path.resolve()),
            "--artifact-root",
            str(REPO_ROOT.resolve()),
            "--output",
            str(raw_path.resolve()),
            "--limit",
            str(limit),
        ],
        cwd=SERVICE_DIR,
        check=True,
    )
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    report = evaluate_retrieval_shadow(
        raw,
        evaluations=evaluations,
        baseline_rows=baseline_rows,
        candidate_rows=candidate_rows,
        projection_summary=projection_summary,
        endpoint_cases=endpoint_cases,
        claim_collapse_review=claim_collapse_review,
    )
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        **report["summary"],
        "projection": projection_summary["output"],
        "destination": str(destination),
        "report": str(report_path),
    }


def build_canonical_search_rows(
    *,
    baseline_rows: Iterable[dict[str, Any]],
    knowledge_units: Iterable[KnowledgeUnit],
    source_snapshots: Iterable[SourceSnapshot],
    source_units: Iterable[SourceUnit],
) -> list[dict[str, Any]]:
    baseline = [dict(row) for row in baseline_rows]
    retained = [
        row
        for row in baseline
        if str(row.get("kind") or "") not in SUPPORTED_SEARCH_KINDS
    ]
    snapshots_by_id = {row.source_snapshot_id: row for row in source_snapshots}
    source_units_by_id = {row.source_unit_id: row for row in source_units}
    canonical = [
        canonical_search_row(item, snapshots_by_id, source_units_by_id)
        for item in knowledge_units
    ]
    by_id: dict[str, dict[str, Any]] = {}
    for row in [*retained, *canonical]:
        row_id = str(row.get("id") or "")
        if row_id in by_id:
            raise ValueError(f"duplicate canonical shadow search row: {row_id}")
        by_id[row_id] = row
    return sorted(by_id.values(), key=lambda row: str(row.get("id") or ""))


def build_endpoint_compatibility_cases(
    baseline_rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [dict(row) for row in baseline_rows]
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_kind.setdefault(str(row.get("kind") or ""), []).append(row)
    for values in by_kind.values():
        values.sort(key=lambda row: str(row.get("id") or ""))

    claim = preferred_row(
        by_kind.get("claim", []),
        ["claim:claim:9cd70d19320375c27cb3"],
    )
    issue = preferred_row(
        by_kind.get("rock_issue", []),
        ["rock_issue:SparkDevNetwork/Rock#6919"],
    )
    idea = preferred_row(
        by_kind.get("rock_idea", []),
        ["rock_idea:2250"],
    )
    model = preferred_row(
        by_kind.get("model_map", []),
        ["model_map:stable:group"],
    )
    recipe = preferred_row(
        by_kind.get("recipe", []),
        ["recipe:oneall:check-in-status-dashboard"],
    )
    lava = preferred_lava_row(by_kind.get("lava_context", []))
    required = {
        "claim": claim,
        "rock_issue": issue,
        "rock_idea": idea,
        "model_map": model,
        "recipe": recipe,
        "lava_context": lava,
    }
    missing = sorted(kind for kind, row in required.items() if row is None)
    if missing:
        raise ValueError(
            "endpoint compatibility shadow is missing representative rows: "
            + ", ".join(missing)
        )

    assert claim is not None
    assert issue is not None
    assert idea is not None
    assert model is not None
    assert recipe is not None
    assert lava is not None
    claim_payload = dict(claim.get("payload") or {})
    issue_payload = dict(issue.get("payload") or {})
    idea_payload = dict(idea.get("payload") or {})
    model_payload = dict(model.get("payload") or {})
    model_identity = dict(model_payload.get("identity") or {})
    recipe_payload = dict(recipe.get("payload") or {})
    lava_payload = dict(lava.get("payload") or {})
    claim_id = str(claim_payload.get("claim_id") or "")
    claim_aliases = sorted(
        str(value)
        for value in claim.get("legacy_ids") or []
        if str(value)
    )
    if not claim_id or not claim_aliases:
        raise ValueError(
            "endpoint compatibility claim requires a claim ID and legacy alias"
        )
    issue_id = str(issue_payload.get("issue_id") or issue.get("id") or "")
    idea_id = str(idea_payload.get("idea_id") or idea.get("id") or "")
    model_slug = str(
        model_identity.get("model_slug")
        or str(model.get("id") or "").rsplit(":", 1)[-1]
    )
    recipe_id = str(recipe_payload.get("recipe_id") or "")
    context_id = str(lava_payload.get("context_id") or "")
    root_key = str(lava_payload.get("root_key") or "")
    return [
        endpoint_case(
            "endpoint:public-result-id",
            "result",
            f"/results/{quote(str(claim['id']), safe='')}",
            requested_result_id=str(claim["id"]),
            result_kind="claim",
        ),
        endpoint_case(
            "endpoint:legacy-result-alias",
            "result",
            f"/results/{quote(claim_aliases[0], safe='')}",
            requested_result_id=claim_aliases[0],
            result_kind="claim",
        ),
        endpoint_case(
            "endpoint:claim",
            "claim",
            f"/claims/id/{quote(claim_id, safe='')}",
            claim_id=claim_id,
        ),
        endpoint_case(
            "endpoint:rock-issue",
            "rock_issue",
            f"/rock-issues/{quote(issue_id, safe='')}",
            issue_id=issue_id,
        ),
        endpoint_case(
            "endpoint:rock-issue-missing",
            "rock_issue_missing",
            "/rock-issues/999999999",
            http_status=404,
            payload_status="not_found",
        ),
        endpoint_case(
            "endpoint:rock-idea",
            "rock_idea",
            f"/rock-ideas/{quote(idea_id, safe='')}",
            idea_id=idea_id,
        ),
        endpoint_case(
            "endpoint:model-map",
            "model_map",
            f"/model-map/models/{quote(model_slug, safe='')}",
            model_slug=model_slug,
        ),
        endpoint_case(
            "endpoint:lava-context",
            "lava_context",
            (
                f"/lava-contexts/{quote(context_id, safe='')}"
                f"?root={quote(root_key, safe='')}"
            ),
            context_id=context_id,
            root_key=root_key,
        ),
        endpoint_case(
            "endpoint:recipe",
            "recipe",
            f"/recipes/{quote(recipe_id, safe='')}",
            recipe_id=recipe_id,
        ),
        {
            "schema": "rock-kb-endpoint-compatibility-case-v1",
            "id": "endpoint:mcp-public-result-id",
            "surface": "mcp_result",
            "transport": "mcp",
            "tool": "kb_get_result",
            "arguments": {"id": str(claim["id"])},
            "expected": {
                "http_status": 200,
                "payload_status": "ok",
                "requested_result_id": str(claim["id"]),
                "result_kind": "claim",
            },
        },
    ]


def endpoint_case(
    case_id: str,
    surface: str,
    path: str,
    **expected: Any,
) -> dict[str, Any]:
    return {
        "schema": "rock-kb-endpoint-compatibility-case-v1",
        "id": case_id,
        "surface": surface,
        "transport": "rest",
        "method": "GET",
        "path": path,
        "expected": {
            "http_status": 200,
            "payload_status": "ok",
            **expected,
        },
    }


def preferred_row(
    rows: list[dict[str, Any]],
    preferred_ids: list[str],
) -> dict[str, Any] | None:
    by_id = {str(row.get("id") or ""): row for row in rows}
    for row_id in preferred_ids:
        if row_id in by_id:
            return by_id[row_id]
    return rows[0] if rows else None


def preferred_lava_row(
    rows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    return next(
        (
            row
            for row in rows
            if str((row.get("payload") or {}).get("root_key") or "").lower()
            == "personattendance"
        ),
        rows[0] if rows else None,
    )


def write_claim_collapse_review(
    destination: Path,
    *,
    baseline_rows: Iterable[dict[str, Any]] | None = None,
    knowledge_units: Iterable[KnowledgeUnit] | None = None,
    source_snapshots: Iterable[SourceSnapshot] | None = None,
    source_units: Iterable[SourceUnit] | None = None,
    evidence_links: Iterable[EvidenceLink] | None = None,
) -> dict[str, Any]:
    baseline = (
        [dict(row) for row in baseline_rows]
        if baseline_rows is not None
        else [dict(row) for row in read_jsonl(destination / "baseline-search-rows.jsonl")]
    )
    units = (
        list(knowledge_units)
        if knowledge_units is not None
        else [
            KnowledgeUnit.model_validate(row)
            for row in read_jsonl(destination / "knowledge-units.jsonl")
        ]
    )
    snapshots = (
        list(source_snapshots)
        if source_snapshots is not None
        else [
            SourceSnapshot.model_validate(row)
            for row in read_jsonl(destination / "source-snapshots.jsonl")
        ]
    )
    source_unit_rows = (
        list(source_units)
        if source_units is not None
        else [
            SourceUnit.model_validate(row)
            for row in read_jsonl(destination / "source-units.jsonl")
        ]
    )
    links = (
        list(evidence_links)
        if evidence_links is not None
        else [
            EvidenceLink.model_validate(row)
            for row in read_jsonl(destination / "evidence-links.jsonl")
        ]
    )
    report = build_claim_collapse_review(
        baseline_rows=baseline,
        knowledge_units=units,
        source_snapshots=snapshots,
        source_units=source_unit_rows,
        evidence_links=links,
    )
    report = apply_claim_collapse_maintainer_review(
        report,
        destination / "claim-collapse-maintainer-review.json",
    )
    (destination / "claim-collapse-review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def build_claim_collapse_review(
    *,
    baseline_rows: Iterable[dict[str, Any]],
    knowledge_units: Iterable[KnowledgeUnit],
    source_snapshots: Iterable[SourceSnapshot],
    source_units: Iterable[SourceUnit],
    evidence_links: Iterable[EvidenceLink],
) -> dict[str, Any]:
    baseline_claims = {
        str(row.get("id") or ""): dict(row)
        for row in baseline_rows
        if row.get("kind") == "claim"
    }
    claim_units = sorted(
        (
            row
            for row in knowledge_units
            if row.knowledge_type == "claim"
        ),
        key=lambda row: row.knowledge_unit_id,
    )
    snapshots_by_id = {
        row.source_snapshot_id: row for row in source_snapshots
    }
    source_units_by_id = {
        row.source_unit_id: row for row in source_units
    }
    links_by_knowledge: dict[str, list[EvidenceLink]] = {}
    for link in evidence_links:
        links_by_knowledge.setdefault(link.knowledge_unit_id, []).append(link)
    groups = []
    distilled_only_count = 0
    for unit in claim_units:
        public_ids = sorted(
            set(unit.legacy_ids) & set(baseline_claims)
        )
        if not public_ids:
            distilled_only_count += 1
            continue
        if len(public_ids) == 1:
            continue
        public_rows = [baseline_claims[row_id] for row_id in public_ids]
        statements = {
            normalize_review_text(
                str(
                    (row.get("payload") or {}).get("claim")
                    or row.get("body")
                    or ""
                )
            )
            for row in public_rows
        }
        claim_types = {
            str((row.get("payload") or {}).get("claim_type") or "")
            for row in public_rows
        }
        links = sorted(
            links_by_knowledge.get(unit.knowledge_unit_id, []),
            key=lambda row: row.evidence_link_id,
        )
        linked_source_unit_ids = {
            row.source_unit_id for row in links
        }
        source_work_ids = []
        source_ids = []
        snapshot_counts: Counter[str] = Counter()
        for source_unit_id in unit.source_unit_ids:
            source_unit = source_units_by_id.get(source_unit_id)
            if source_unit is None:
                continue
            snapshot = snapshots_by_id.get(source_unit.source_snapshot_id)
            if snapshot is None:
                continue
            source_ids.append(snapshot.source_id)
            independence_id = (
                snapshot.source_work_id or snapshot.source_snapshot_id
            )
            source_work_ids.append(independence_id)
            snapshot_counts[independence_id] += 1
        evidence_retained = (
            set(unit.source_unit_ids) == linked_source_unit_ids
            and len(unit.source_unit_ids) >= len(public_rows)
        )
        aliases_retained = all(
            row_id in unit.legacy_ids for row_id in public_ids
        )
        exact_statement_match = (
            len(statements) == 1
            and normalize_review_text(unit.retrieval_text) in statements
        )
        claim_type_match = len(claim_types) == 1
        reviewable = (
            exact_statement_match
            and claim_type_match
            and aliases_retained
            and evidence_retained
        )
        groups.append(
            {
                "knowledge_unit_id": unit.knowledge_unit_id,
                "statement": unit.retrieval_text,
                "claim_type": next(iter(claim_types), ""),
                "public_result_ids": public_ids,
                "public_row_count": len(public_rows),
                "redundant_public_row_count": len(public_rows) - 1,
                "concept_facets": unit.concept_facets,
                "authority_tiers": unit.authority_tiers,
                "source_ids": sorted(set(source_ids)),
                "source_work_ids": sorted(set(source_work_ids)),
                "evidence_link_count": len(links),
                "source_unit_count": len(unit.source_unit_ids),
                "independent_source_work_count": len(set(source_work_ids)),
                "mirrored_evidence_count": sum(
                    count - 1
                    for count in snapshot_counts.values()
                    if count > 1
                ),
                "exact_statement_match": exact_statement_match,
                "claim_type_match": claim_type_match,
                "public_aliases_retained": aliases_retained,
                "all_source_units_linked": evidence_retained,
                "reviewable": reviewable,
            }
        )
    review_input = [
        {
            "knowledge_unit_id": row["knowledge_unit_id"],
            "public_result_ids": row["public_result_ids"],
            "source_work_ids": row["source_work_ids"],
            "authority_tiers": row["authority_tiers"],
        }
        for row in groups
    ]
    review_input_sha256 = sha256_text(
        json.dumps(
            review_input,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    redundant_count = sum(
        int(row["redundant_public_row_count"]) for row in groups
    )
    return {
        "schema": "rock-kb-claim-collapse-review-v1",
        "review_input_sha256": review_input_sha256,
        "status": "generated_needs_reviewer_approval",
        "baseline_claim_row_count": len(baseline_claims),
        "canonical_claim_unit_count": len(claim_units),
        "net_claim_row_delta": len(baseline_claims) - len(claim_units),
        "collapsed_group_count": len(groups),
        "redundant_public_row_count": redundant_count,
        "distilled_only_claim_unit_count": distilled_only_count,
        "all_groups_reviewable": all(
            row["reviewable"] for row in groups
        ),
        "groups": groups,
        "maintainer_review": {
            "status": "not_recorded",
            "approved_group_count": 0,
        },
    }


def apply_claim_collapse_maintainer_review(
    report: dict[str, Any],
    review_path: Path,
) -> dict[str, Any]:
    if not review_path.exists():
        return report
    review = json.loads(review_path.read_text(encoding="utf-8"))
    expected_group_ids = {
        str(row.get("knowledge_unit_id") or "")
        for row in report.get("groups") or []
    }
    decisions = {
        str(row.get("knowledge_unit_id") or ""): str(
            row.get("decision") or ""
        )
        for row in review.get("decisions") or []
    }
    hash_matches = (
        review.get("review_input_sha256")
        == report.get("review_input_sha256")
    )
    coverage_matches = set(decisions) == expected_group_ids
    all_approved = (
        coverage_matches
        and all(value == "approve" for value in decisions.values())
    )
    status = (
        "approved"
        if hash_matches
        and all_approved
        and report.get("all_groups_reviewable")
        else "stale_or_incomplete"
    )
    return {
        **report,
        "status": (
            "reviewer_approved"
            if status == "approved"
            else "generated_needs_reviewer_approval"
        ),
        "maintainer_review": {
            "status": status,
            "reviewed_at": review.get("reviewed_at"),
            "reviewer": review.get("reviewer"),
            "hash_matches": hash_matches,
            "coverage_matches": coverage_matches,
            "approved_group_count": sum(
                value == "approve" for value in decisions.values()
            ),
        },
    }


def normalize_review_text(value: str) -> str:
    return " ".join(str(value or "").lower().split())


def canonical_search_row(
    item: KnowledgeUnit,
    snapshots_by_id: dict[str, SourceSnapshot],
    source_units_by_id: dict[str, SourceUnit],
) -> dict[str, Any]:
    snapshots = [
        snapshots_by_id[source_units_by_id[source_unit_id].source_snapshot_id]
        for source_unit_id in item.source_unit_ids
        if source_unit_id in source_units_by_id
        and source_units_by_id[source_unit_id].source_snapshot_id in snapshots_by_id
    ]
    if not snapshots:
        snapshot_ids = {
            row.source_snapshot_id
            for row in snapshots_by_id.values()
            if row.source_work_id and row.source_work_id in item.source_work_ids
        }
        snapshots = [
            snapshots_by_id[source_id]
            for source_id in sorted(snapshot_ids)
        ]
    payload = dict(item.payload)
    if item.payload_schema == "rock-kb-source-native-artifact-payload-v1":
        artifact_payload = (
            item.payload.get("effective_artifact")
            or item.payload.get("artifact")
            or {}
        )
        verification_payload = item.payload.get("verification") or {}
        payload = {
            **payload,
            "rock_versions": item.rock_versions,
            "version_scope_status": item.version_scope_status,
            "needs_live_verification": bool(
                artifact_payload.get("needs_live_verification")
            ),
            "verification_state": str(
                verification_payload.get("state")
                or (
                    "unresolved"
                    if artifact_payload.get("needs_live_verification")
                    else "not_required"
                )
            ),
        }
    title = item.title
    if item.knowledge_type == "claim":
        title = canonical_claim_search_title(item)
        payload = {
            **payload,
            "knowledge_unit_id": item.knowledge_unit_id,
            "claim": item.retrieval_text,
            "concept_ids": item.concept_facets,
            "rock_versions": item.rock_versions,
            "version_scope_status": item.version_scope_status,
        }
    authority_tier = highest_authority(item.authority_tiers)
    body = canonical_search_body(item)
    source_revisions = sorted(
        {
            str(snapshot.upstream_revision)
            for snapshot in snapshots
            if snapshot.upstream_revision
        }
    )
    source_observation = {
        "upstream_revisions": source_revisions,
        "last_checked_at": max(
            (
                str(snapshot.last_checked_at)
                for snapshot in snapshots
                if snapshot.last_checked_at
            ),
            default="",
        )
        or None,
        "content_changed_at": max(
            (
                str(snapshot.content_changed_at)
                for snapshot in snapshots
                if snapshot.content_changed_at
            ),
            default="",
        )
        or None,
    }
    if any(source_observation.values()):
        payload = {**payload, "source_observation": source_observation}
    if item.version_scope_status == "unprocessed" and source_revisions:
        version_note = (
            "Source observation: the supporting documentation revision is "
            f"{', '.join(source_revisions)}; Rock product-version "
            "applicability is unprocessed, so verify this detail for the "
            "target version."
        )
        body = f"{body}\n\n{version_note}"
        payload = {**payload, "version_scope_note": version_note}
    return {
        "id": item.knowledge_unit_id,
        "kind": item.knowledge_type,
        "title": title,
        "body": body,
        "path": f"shadow/canonical/{item.knowledge_type}.jsonl",
        "url": next(
            (
                row.canonical_url
                for row in snapshots
                if row.canonical_url
            ),
            "",
        ),
        "concept": item.concept_facets[0] if item.concept_facets else "",
        "concepts": item.concept_facets,
        "topics": item.topic_facets,
        "legacy_ids": item.legacy_ids,
        "authority_tier": authority_tier,
        "claim_tier": item.claim_tier or "routing_context_only",
        "source_id": ",".join(
            sorted({row.source_id for row in snapshots if row.source_id})
        ),
        "payload": payload,
    }


def canonical_search_body(item: KnowledgeUnit) -> str:
    values = [item.retrieval_text]
    if item.payload_schema != "rock-kb-source-native-artifact-payload-v1":
        return item.retrieval_text
    artifact = (
        item.payload.get("effective_artifact")
        or item.payload.get("artifact")
        or {}
    )
    typed_payload = artifact.get("payload") or {}
    verification = item.payload.get("verification") or {}
    if verification.get("effective_override"):
        values = [
            item.retrieval_text,
            str(artifact.get("independent_question") or ""),
            *[
                str(row.get("finding") or "")
                for row in verification.get("resolutions") or []
                if isinstance(row, dict)
            ],
        ]
        normalized = [" ".join(value.split()) for value in values if value]
        return " ".join(dict.fromkeys(normalized))[:20_000]
    values.extend(
        [
            str(artifact.get("independent_question") or ""),
            str(typed_payload.get("summary") or ""),
            *[
                " ".join(
                    [
                        str(reference.get("label") or ""),
                        str(reference.get("detail") or ""),
                    ]
                )
                for reference in typed_payload.get("reference_items") or []
                if isinstance(reference, dict)
            ],
            *[
                str(step.get("instruction") or "")
                for step in typed_payload.get("steps") or []
                if isinstance(step, dict)
            ],
            *[
                str(value)
                for value in typed_payload.get("implementation_elements") or []
            ],
            *[str(value) for value in typed_payload.get("cautions") or []],
            str(typed_payload.get("completion_or_use") or ""),
            *[
                str(row.get("finding") or "")
                for row in verification.get("resolutions") or []
                if isinstance(row, dict)
            ],
        ]
    )
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = " ".join(value.split())
        key = text.casefold()
        if not text or key in seen:
            continue
        seen.add(key)
        normalized.append(text)
    return " ".join(normalized)[:20_000]


def highest_authority(values: Iterable[str]) -> str:
    candidates = [str(value) for value in values if value]
    return max(
        candidates,
        key=lambda value: (AUTHORITY_TIER_RANK.get(value, -1), value),
        default="community-unreviewed",
    )


def canonical_claim_search_title(item: KnowledgeUnit) -> str:
    approved_claims = [
        row
        for row in item.payload.get("approved_claims") or []
        if isinstance(row, dict)
    ]
    corroborates_contribution = any(
        isinstance(row.get("derived_from"), dict)
        and row["derived_from"].get("related_contribution_ids")
        for row in approved_claims
    )
    if corroborates_contribution:
        return item.retrieval_text
    claim_types = sorted(
        {
            str(row.get("claim_type"))
            for row in approved_claims
            if row.get("claim_type")
        }
    )
    if claim_types:
        return claim_types[0]
    return str(item.payload.get("claim_type") or item.title)


def evaluate_retrieval_shadow(
    raw: dict[str, Any],
    *,
    evaluations: Iterable[dict[str, Any]],
    baseline_rows: Iterable[dict[str, Any]],
    candidate_rows: Iterable[dict[str, Any]],
    projection_summary: dict[str, Any],
    endpoint_cases: Iterable[dict[str, Any]] = (),
    claim_collapse_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    baseline_rows = list(baseline_rows)
    candidate_rows = list(candidate_rows)
    evaluation_by_id = {
        str(row.get("id") or ""): dict(row)
        for row in evaluations
    }
    baseline = score_variant(
        raw.get("variants", {}).get("baseline") or {},
        evaluation_by_id=evaluation_by_id,
        alias_map=search_row_alias_map(baseline_rows),
    )
    candidate = score_variant(
        raw.get("variants", {}).get("candidate") or {},
        evaluation_by_id=evaluation_by_id,
        alias_map=search_row_alias_map(candidate_rows),
    )
    baseline_by_id = {str(row.get("id") or ""): row for row in baseline["results"]}
    candidate_by_id = {str(row.get("id") or ""): row for row in candidate["results"]}
    expected_evaluation_ids = set(evaluation_by_id)
    if set(baseline_by_id) != expected_evaluation_ids:
        raise ValueError("baseline shadow results do not cover the evaluation set exactly")
    if set(candidate_by_id) != expected_evaluation_ids:
        raise ValueError("candidate shadow results do not cover the evaluation set exactly")
    comparisons = [
        compare_evaluation_rows(
            baseline_by_id[evaluation_id],
            candidate_by_id[evaluation_id],
        )
        for evaluation_id in sorted(set(baseline_by_id) & set(candidate_by_id))
    ]
    comparison_counts = Counter(row["outcome"] for row in comparisons)
    regressions = [row for row in comparisons if row["outcome"] == "regressed"]
    shared_failures = [
        row
        for row in comparisons
        if row["baseline_status"] == "fail"
        and row["candidate_status"] == "fail"
    ]
    exact_regressions = [
        row
        for row in regressions
        if baseline_by_id[row["id"]].get("expected_result_ids")
    ]
    authority_regressions = [
        row
        for row in regressions
        if baseline_by_id[row["id"]].get("required_authority_tiers")
    ]
    no_answer_regressions = [
        row
        for row in regressions
        if baseline_by_id[row["id"]].get("expect_no_results")
    ]
    baseline_metrics = baseline["metrics"]
    candidate_metrics = candidate["metrics"]
    endpoint_compatibility = evaluate_endpoint_compatibility(
        raw,
        endpoint_cases=endpoint_cases,
    )
    collapse_review = claim_collapse_review or {
        "collapsed_group_count": 0,
        "redundant_public_row_count": 0,
        "maintainer_review": {"status": "not_required"},
    }
    collapse_review_passed = (
        int(collapse_review.get("collapsed_group_count") or 0) == 0
        or (
            collapse_review.get("all_groups_reviewable") is True
            and (collapse_review.get("maintainer_review") or {}).get("status")
            == "approved"
        )
    )
    baseline_size = serialized_rows_size(baseline_rows)
    candidate_size = serialized_rows_size(candidate_rows)
    metric_gate = {
        "mean_reciprocal_rank_not_lower": (
            candidate_metrics["mean_reciprocal_rank"]
            >= baseline_metrics["mean_reciprocal_rank"]
        ),
        "recall_not_lower": (
            candidate_metrics["recall_at_target_rank"]
            >= baseline_metrics["recall_at_target_rank"]
        ),
        "duplicate_rate_not_higher": (
            candidate_metrics["duplicate_result_rate"]
            <= baseline_metrics["duplicate_result_rate"]
        ),
        "authority_rate_not_lower": (
            candidate_metrics["authority_pass_rate"]
            >= baseline_metrics["authority_pass_rate"]
        ),
        "mean_latency_within_20_percent": (
            candidate_metrics["mean_latency_ms"]
            <= baseline_metrics["mean_latency_ms"] * 1.2
        ),
        "p95_latency_within_20_percent": (
            candidate_metrics["p95_latency_ms"]
            <= baseline_metrics["p95_latency_ms"] * 1.2
        ),
        "serialized_storage_within_10_percent": (
            candidate_size <= baseline_size * 1.1
        ),
    }
    passed = (
        not regressions
        and not exact_regressions
        and not authority_regressions
        and not no_answer_regressions
        and endpoint_compatibility["status"] == "pass"
        and collapse_review_passed
        and all(metric_gate.values())
    )
    return {
        "schema": "rock-kb-canonical-retrieval-shadow-report-v1",
        "mode": "shadow_only",
        "public_retrieval_changed": False,
        "summary": {
            "status": "pass" if passed else "fail",
            "question_count": len(comparisons),
            "improved": comparison_counts["improved"],
            "unchanged": comparison_counts["unchanged"],
            "regressed": comparison_counts["regressed"],
            "exact_lookup_regressions": len(exact_regressions),
            "authority_regressions": len(authority_regressions),
            "no_answer_regressions": len(no_answer_regressions),
            "shared_failure_count": len(shared_failures),
            "endpoint_compatibility_case_count": endpoint_compatibility[
                "case_count"
            ],
            "endpoint_compatibility_regressions": endpoint_compatibility[
                "regression_count"
            ],
            "claim_collapse_group_count": collapse_review.get(
                "collapsed_group_count", 0
            ),
            "claim_redundant_public_row_count": collapse_review.get(
                "redundant_public_row_count", 0
            ),
            "baseline_row_count": len(list(baseline_rows)),
            "candidate_row_count": len(list(candidate_rows)),
        },
        "promotion_gate": {
            "passed": passed,
            "retrieval_equivalence_passed": passed,
            "metric_checks": metric_gate,
            "endpoint_compatibility_passed": (
                endpoint_compatibility["status"] == "pass"
            ),
            "claim_collapse_review_passed": collapse_review_passed,
            "identity_migration_count": projection_summary["output"][
                "identity_migrations"
            ],
            "content_fallback_identity_count": projection_summary["output"][
                "content_fallback_identities"
            ],
            "requires_review": True,
            "production_change_authorized": False,
            "ready_for_production_promotion": False,
            "shared_failures": [
                {
                    "id": row["id"],
                    "question": row["question"],
                    "baseline_result_ids": row["baseline_result_ids"],
                    "candidate_result_ids": row["candidate_result_ids"],
                }
                for row in shared_failures
            ],
        },
        "storage": {
            "baseline_jsonl_bytes": baseline_size,
            "candidate_jsonl_bytes": candidate_size,
            "delta_bytes": candidate_size - baseline_size,
            "delta_percent": round(
                (candidate_size - baseline_size) / max(1, baseline_size) * 100,
                3,
            ),
        },
        "variants": {
            "baseline": baseline,
            "candidate": candidate,
        },
        "endpoint_compatibility": endpoint_compatibility,
        "claim_collapse_review": collapse_review,
        "comparisons": comparisons,
    }


def evaluate_endpoint_compatibility(
    raw: dict[str, Any],
    *,
    endpoint_cases: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    cases = {
        str(row.get("id") or ""): dict(row)
        for row in endpoint_cases
    }
    if not cases:
        return {
            "status": "pass",
            "case_count": 0,
            "regression_count": 0,
            "baseline_failure_count": 0,
            "candidate_failure_count": 0,
            "contract_mismatch_count": 0,
            "cases": [],
        }
    variants: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in ("baseline", "candidate"):
        results = {
            str(row.get("id") or ""): dict(row)
            for row in (
                raw.get("variants", {})
                .get(variant, {})
                .get("endpoint_results", [])
            )
        }
        if set(results) != set(cases):
            raise ValueError(
                f"{variant} endpoint shadow results do not cover cases exactly"
            )
        variants[variant] = {
            case_id: score_endpoint_case(cases[case_id], results[case_id])
            for case_id in sorted(cases)
        }
    comparisons = []
    for case_id in sorted(cases):
        baseline = variants["baseline"][case_id]
        candidate = variants["candidate"][case_id]
        contract_matches = baseline["contract"] == candidate["contract"]
        regressed = baseline["passed"] and (
            not candidate["passed"] or not contract_matches
        )
        comparisons.append(
            {
                "id": case_id,
                "surface": cases[case_id].get("surface"),
                "baseline_passed": baseline["passed"],
                "candidate_passed": candidate["passed"],
                "contract_matches": contract_matches,
                "regressed": regressed,
                "baseline": baseline,
                "candidate": candidate,
            }
        )
    baseline_failures = sum(
        not row["baseline_passed"] for row in comparisons
    )
    candidate_failures = sum(
        not row["candidate_passed"] for row in comparisons
    )
    contract_mismatches = sum(
        not row["contract_matches"] for row in comparisons
    )
    regressions = sum(row["regressed"] for row in comparisons)
    passed = (
        baseline_failures == 0
        and candidate_failures == 0
        and contract_mismatches == 0
    )
    return {
        "status": "pass" if passed else "fail",
        "case_count": len(comparisons),
        "regression_count": regressions,
        "baseline_failure_count": baseline_failures,
        "candidate_failure_count": candidate_failures,
        "contract_mismatch_count": contract_mismatches,
        "cases": comparisons,
    }


def score_endpoint_case(
    case: dict[str, Any],
    raw_result: dict[str, Any],
) -> dict[str, Any]:
    expected = dict(case.get("expected") or {})
    payload = dict(raw_result.get("payload") or {})
    data = payload
    if case.get("transport") == "mcp":
        data = dict((payload.get("result") or {}).get("structuredContent") or {})
    surface = str(case.get("surface") or "")
    contract: dict[str, Any] = {
        "http_status": int(raw_result.get("http_status") or 0),
        "payload_status": data.get("status"),
    }
    if surface in {"result", "mcp_result"}:
        contract.update(
            {
                "requested_result_id": data.get("requested_result_id"),
                "result_kind": (data.get("result") or {}).get("kind"),
            }
        )
    elif surface == "claim":
        contract["claim_id"] = data.get("claim_id")
    elif surface == "rock_issue":
        contract["issue_id"] = data.get("issue_id")
    elif surface == "rock_idea":
        contract["idea_id"] = data.get("idea_id")
    elif surface == "model_map":
        contract["model_slug"] = (
            data.get("matched_model") or {}
        ).get("model_slug")
    elif surface == "lava_context":
        contract["context_id"] = (
            data.get("surface") or {}
        ).get("context_id") or data.get("context_id")
        contract["root_keys"] = sorted(
            {
                str(row.get("root_key") or "")
                for row in data.get("roots") or []
                if row.get("root_key")
            }
        )
    elif surface == "recipe":
        contract["recipe_id"] = (data.get("recipe") or {}).get("recipe_id")
    observed = {
        key: contract.get(key)
        for key in expected
        if key not in {"root_key"}
    }
    if "root_key" in expected:
        observed["root_key"] = expected["root_key"] in contract.get(
            "root_keys", []
        )
    expected_observed = {
        key: value
        for key, value in expected.items()
        if key != "root_key"
    }
    if "root_key" in expected:
        expected_observed["root_key"] = True
    return {
        "passed": observed == expected_observed,
        "latency_ms": raw_result.get("latency_ms"),
        "contract": contract,
        "observed": observed,
        "expected": expected_observed,
        "resolved_canonical_id": data.get("canonical_result_id"),
    }


def score_variant(
    raw_variant: dict[str, Any],
    *,
    evaluation_by_id: dict[str, dict[str, Any]],
    alias_map: dict[str, str],
) -> dict[str, Any]:
    scored = []
    for raw_result in raw_variant.get("results") or []:
        evaluation_id = str(raw_result.get("id") or "")
        evaluation = evaluation_by_id[evaluation_id]
        scored.append(
            score_evaluation_hits(
                evaluation,
                raw_result.get("hits") or [],
                alias_map=alias_map,
                latency_ms=float(raw_result.get("latency_ms") or 0),
            )
        )
    return {
        "setup_ms": raw_variant.get("setup_ms"),
        "query_ms": raw_variant.get("query_ms"),
        "metrics": evaluation_metrics(scored),
        "cohorts": {
            "exact_technical": cohort_metrics(
                row for row in scored if row.get("expected_result_ids")
            ),
            "semantic": cohort_metrics(
                row
                for row in scored
                if not row.get("expected_result_ids")
                and not row.get("expect_no_results")
            ),
            "authority": cohort_metrics(
                row for row in scored if row.get("required_authority_tiers")
            ),
            "wrong_ranking_guardrails": cohort_metrics(
                row for row in scored if row.get("forbidden_result_ids")
            ),
            "no_answer": cohort_metrics(
                row for row in scored if row.get("expect_no_results")
            ),
        },
        "results": scored,
    }


def score_evaluation_hits(
    row: dict[str, Any],
    hits: list[dict[str, Any]],
    *,
    alias_map: dict[str, str],
    latency_ms: float,
) -> dict[str, Any]:
    expected_concept = str(row.get("concept_id") or "")
    limit = max(1, len(hits))
    max_rank = max(
        1,
        min(
            int(row.get("max_rank") or row.get("max_allowed_rank") or 2),
            limit,
        ),
    )
    original_expected_ids = [
        str(value) for value in row.get("expected_result_ids") or []
    ]
    expected_ids = [
        alias_map.get(value, value) for value in original_expected_ids
    ]
    expected_kinds = [
        str(value) for value in row.get("expected_result_kinds") or []
    ]
    original_forbidden_ids = [
        str(value) for value in row.get("forbidden_result_ids") or []
    ]
    forbidden_ids = [
        alias_map.get(value, value) for value in original_forbidden_ids
    ]
    ordered_ids = [str(hit.get("id") or "") for hit in hits]
    ordered_kinds = [str(hit.get("kind") or "") for hit in hits]
    ordered_authorities = [
        str(hit.get("authority_tier") or "") for hit in hits
    ]
    ordered_concepts = [hit_concepts(hit) for hit in hits]
    expected_id_rank = first_rank(ordered_ids, expected_ids)
    expected_kind_rank = first_rank(ordered_kinds, expected_kinds)
    expected_concept_rank = next(
        (
            index + 1
            for index, concepts in enumerate(ordered_concepts)
            if expected_concept in concepts
        ),
        None,
    )
    forbidden_rank = first_rank(ordered_ids, forbidden_ids)
    relevant_rank = (
        expected_id_rank
        if expected_ids
        else expected_kind_rank
        if expected_kinds
        else expected_concept_rank
    )
    relevant_indexes = [
        index
        for index, hit in enumerate(hits)
        if (
            expected_ids
            and str(hit.get("id") or "") in expected_ids
        )
        or (
            not expected_ids
            and expected_kinds
            and str(hit.get("kind") or "") in expected_kinds
        )
        or (
            not expected_ids
            and not expected_kinds
            and expected_concept in hit_concepts(hit)
        )
    ]
    required_authorities = [
        str(value) for value in row.get("required_authority_tiers") or []
    ]
    authority_passed = not required_authorities or any(
        ordered_authorities[index] in required_authorities
        for index in relevant_indexes
        if index < max_rank
    )
    required_terms = [str(value).lower() for value in row.get("required_terms") or []]
    serialized = json.dumps(hits, ensure_ascii=False).lower()
    missing_terms = [term for term in required_terms if term not in serialized]
    duplicate_count = len(ordered_ids) - len(set(ordered_ids))
    expect_no_results = bool(row.get("expect_no_results"))
    if expect_no_results:
        passed = not hits
    else:
        rank_passed = (
            not expected_concept
            or (
                expected_concept_rank is not None
                and expected_concept_rank <= max_rank
            )
        )
        id_passed = (
            not expected_ids
            or (expected_id_rank is not None and expected_id_rank <= max_rank)
        )
        kind_passed = (
            not expected_kinds
            or (expected_kind_rank is not None and expected_kind_rank <= max_rank)
        )
        forbidden_max_rank = max(
            1,
            min(int(row.get("forbidden_max_rank") or max_rank), limit),
        )
        forbidden_passed = (
            not forbidden_ids
            or forbidden_rank is None
            or forbidden_rank > forbidden_max_rank
        )
        passed = (
            bool(hits)
            and rank_passed
            and id_passed
            and kind_passed
            and forbidden_passed
            and authority_passed
            and len(hits) >= int(row.get("min_hits") or 1)
            and not missing_terms
            and duplicate_count == 0
        )
    return {
        "id": row.get("id"),
        "question": row.get("question"),
        "source": row.get("source"),
        "evaluation_mode": row.get("evaluation_mode"),
        "expected_concept": expected_concept,
        "expected_result_ids": expected_ids,
        "original_expected_result_ids": original_expected_ids,
        "expected_result_kinds": expected_kinds,
        "forbidden_result_ids": forbidden_ids,
        "original_forbidden_result_ids": original_forbidden_ids,
        "required_authority_tiers": required_authorities,
        "expect_no_results": expect_no_results,
        "max_allowed_rank": max_rank,
        "hit_count": len(hits),
        "result_ids": ordered_ids,
        "result_kinds": ordered_kinds,
        "authority_tiers": ordered_authorities,
        "expected_result_id_rank": expected_id_rank,
        "expected_result_kind_rank": expected_kind_rank,
        "expected_concept_rank": expected_concept_rank,
        "forbidden_result_id_rank": forbidden_rank,
        "authority_passed": authority_passed,
        "has_relevance_expectation": bool(
            expected_ids or expected_kinds or expected_concept
        ),
        "relevant_rank": relevant_rank,
        "reciprocal_rank": round(1 / relevant_rank, 6)
        if relevant_rank
        else 0.0,
        "duplicate_count": duplicate_count,
        "missing_terms": missing_terms,
        "latency_ms": round(latency_ms, 3),
        "availability_status": "available",
        "status": "pass" if passed else "fail",
    }


def compare_evaluation_rows(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    baseline_score = evaluation_quality_key(baseline)
    candidate_score = evaluation_quality_key(candidate)
    outcome = (
        "improved"
        if candidate_score > baseline_score
        else "regressed"
        if candidate_score < baseline_score
        else "unchanged"
    )
    return {
        "id": baseline.get("id"),
        "question": baseline.get("question"),
        "outcome": outcome,
        "baseline_status": baseline.get("status"),
        "candidate_status": candidate.get("status"),
        "baseline_rank": baseline.get("relevant_rank"),
        "candidate_rank": candidate.get("relevant_rank"),
        "baseline_hit_count": baseline.get("hit_count"),
        "candidate_hit_count": candidate.get("hit_count"),
        "baseline_result_ids": baseline.get("result_ids"),
        "candidate_result_ids": candidate.get("result_ids"),
    }


def evaluation_quality_key(row: dict[str, Any]) -> tuple[int, int, int, int]:
    rank = int(row.get("relevant_rank") or 1_000_000)
    no_answer_hits = (
        int(row.get("hit_count") or 0)
        if row.get("expect_no_results")
        else 0
    )
    return (
        1 if row.get("status") == "pass" else 0,
        -rank,
        -int(row.get("duplicate_count") or 0),
        -no_answer_hits,
    )


def cohort_metrics(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    selected = list(rows)
    return {
        "question_count": len(selected),
        "pass_count": sum(1 for row in selected if row.get("status") == "pass"),
        "fail_count": sum(1 for row in selected if row.get("status") == "fail"),
        "metrics": evaluation_metrics(selected),
    }


def search_row_alias_map(rows: Iterable[dict[str, Any]]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for row in rows:
        row_id = str(row.get("id") or "")
        aliases[row_id] = row_id
        for alias in row.get("legacy_ids") or []:
            alias_id = str(alias)
            existing = aliases.get(alias_id)
            if existing and existing != row_id:
                raise ValueError(
                    f"search row alias maps to multiple rows: {alias_id}"
                )
            aliases[alias_id] = row_id
    return aliases


def first_rank(values: list[str], expected: list[str]) -> int | None:
    return next(
        (
            index + 1
            for index, value in enumerate(values)
            if value in expected
        ),
        None,
    )


def serialized_rows_size(rows: Iterable[dict[str, Any]]) -> int:
    return sum(
        len(
            (
                json.dumps(
                    row,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")
        )
        for row in rows
    )
