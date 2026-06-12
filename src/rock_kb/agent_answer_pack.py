from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .claims import approved_claim_rows
from .extract import generated_at_iso, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import AGENT_DIR, KNOWLEDGE_DIR, REVIEW_DIR

ANSWER_PACK_PATH = AGENT_DIR / "answer-pack.jsonl"
LIVE_CHECKLISTS_PATH = AGENT_DIR / "live-inspection-checklists.jsonl"
LIVE_PROBE_RECIPES_PATH = AGENT_DIR / "live-probe-recipes.jsonl"
CLAIM_REVIEW_QUEUE_PATH = AGENT_DIR / "claim-review-queue.jsonl"
SOURCE_CONFLICTS_PATH = AGENT_DIR / "source-conflicts.jsonl"
DISTILLED_CLAIMS_PATH = AGENT_DIR / "distilled-claims.jsonl"
DISTILLED_CLAIM_REVIEWS_PATH = REVIEW_DIR / "distilled-claim-reviews.jsonl"
DISTILLED_CLAIM_REVIEW_SUPPLEMENTAL_PATTERN = "distilled-claim-reviews-*.jsonl"
AUTHORITY_RULES_PATH = AGENT_DIR / "source-authority-rules.jsonl"
EVALUATION_SET_PATH = AGENT_DIR / "evaluation-set.jsonl"
EVALUATION_RESULTS_PATH = AGENT_DIR / "evaluation-results.jsonl"
EVALUATION_REPORT_PATH = AGENT_DIR / "evaluation-report.json"
REVIEW_DASHBOARD_PATH = AGENT_DIR / "claim-review-dashboard.md"

HIGH_VALUE_CONCEPTS = {"workflows", "security-permissions", "data-views-reports", "mobile", "check-in", "groups"}
APPROVED_DISTILLATION_STATUSES = {"reviewer_approved", "approved_for_answer_pack", "approved_for_public_distillation"}
REJECTED_DISTILLATION_STATUSES = {"rejected", "rejected_for_answer_pack", "rejected_for_public_distillation"}
DISTILLED_CLAIM_REVIEW_STATUSES = APPROVED_DISTILLATION_STATUSES | REJECTED_DISTILLATION_STATUSES
ANSWER_CLAIM_TIERS = {"answer_pack_approved", "live_verified"}

BEST_ANSWER_OVERRIDES = {
    "workflows": {
        "first-checks": (
            "Start by finding the exact WorkflowType, launch path, and current Workflow records before changing actions. "
            "Inspect form fields, action order, attribute keys, triggers, security, and recent history; then verify any Lava, webhook, or job path that can launch the workflow. "
            "Treat adjacent areas such as connections or check-in as the caller of the workflow until live records prove the workflow itself is the failing surface."
        )
    },
    "security-permissions": {
        "first-checks": (
            "Start from the exact secured object: page, block, entity, REST key, group role, or workflow action. "
            "Compare inherited page security, block security, explicit Auth rows, group membership, and the current user's person alias before deciding why access is allowed or denied. "
            "For public or staff-facing changes, verify both view and edit paths because route visibility does not prove record-level permission."
        )
    },
    "data-views-reports": {
        "first-checks": (
            "Start by identifying the reporting surface and the DataView, report, Lava, dynamic data block, SQL query, persisted value, or BI export behind it. "
            "Check filters, transforms, security, persisted refresh timing, and sample included/excluded records before editing a shared data view. "
            "If the report is operationally important, preserve the current definition and validate row counts before and after the change."
        )
    },
    "mobile": {
        "first-checks": (
            "Start with the exact mobile shell version, page, block type, block settings, and CSS selector target. "
            "Inspect the official mobile docs, official mobile block docs, the rendered block x-ray data, theme variables, dark mode behavior, and platform-specific styling before writing selectors. "
            "For check-in or connection blocks, verify the underlying Rock configuration first because mobile UI symptoms often reflect server-side page, block, security, or data settings."
        )
    },
    "check-in": {
        "first-checks": (
            "Start by separating eligibility, availability, label printing, and device behavior. "
            "Inspect the check-in configuration, group type, groups, locations, schedules, campus, person/family eligibility, and kiosk or mobile device settings before changing rooms. "
            "When a person or room is missing, prove whether the blocker is data view filtering, schedule windows, location capacity, security, or label/device configuration."
        )
    },
    "groups": {
        "first-checks": (
            "Start by identifying the exact Group, GroupType, role, membership, location, schedule, attendance, finder, or workflow surface named by the user. "
            "Inspect GroupType settings, inherited attributes, group roles, active memberships, campus/location/schedule links, security, and any finder or attendance configuration before changing records. "
            "For visibility or eligibility issues, prove whether the blocker is group status, role rules, schedule/location data, data view filtering, security, or a caller such as check-in, registration, workflows, or mobile."
        )
    },
}

AUTHORITY_RULES = {
    "workflows": {
        "preferred_sources": ["rock_rocku", "rock_documentation", "sparkdevnetwork_rock", "rock_core_release_notes"],
        "community_use": "Use community hubs and recipes as implementation examples after checking the live WorkflowType, actions, launch paths, and security.",
    },
    "security-permissions": {
        "preferred_sources": ["rock_documentation", "sparkdevnetwork_rock", "rock_core_release_notes", "rock_rocku"],
        "community_use": "Do not treat community examples as canonical security behavior; verify Auth rows, inheritance, and user context live.",
    },
    "data-views-reports": {
        "preferred_sources": ["rock_documentation", "rock_model_map", "sparkdevnetwork_rock", "rock_rocku"],
        "community_use": "Community SQL and reporting examples need schema/version review and live row-count validation before reuse.",
    },
    "mobile": {
        "preferred_sources": ["rock_mobile_docs", "rock_mobile_release_notes", "sparkdevnetwork_rock", "rock_rocku"],
        "community_use": "Use community examples only after checking official mobile docs, selector x-ray artifacts, shell version, theme, and dark-mode behavior.",
    },
    "check-in": {
        "preferred_sources": ["rock_documentation", "rock_rocku", "sparkdevnetwork_rock", "rock_core_release_notes"],
        "community_use": "Use community patterns as triage examples; live eligibility, schedule, room, device, and label settings decide behavior.",
    },
}

LIVE_INSPECTION_TEMPLATES = {
    "workflows": [
        {"label": "Workflow type", "sql": "SELECT Id, Name, IsActive, CategoryId FROM WorkflowType WHERE Name LIKE '%<workflow name>%';"},
        {"label": "Workflow actions", "sql": "SELECT wat.Id, wat.Name, wat.[Order], wat.EntityTypeId, et.Name AS ActionEntityTypeName FROM WorkflowActionType wat LEFT JOIN EntityType et ON et.Id = wat.EntityTypeId WHERE wat.ActivityTypeId IN (SELECT Id FROM WorkflowActivityType WHERE WorkflowTypeId = <workflow_type_id>) ORDER BY wat.[Order], wat.Id;"},
        {"label": "Recent workflow runs", "sql": "SELECT TOP 25 Id, Status, CreatedDateTime, CompletedDateTime FROM Workflow WHERE WorkflowTypeId = <workflow_type_id> ORDER BY CreatedDateTime DESC;"},
        {"label": "Launch surfaces", "check": "Search pages, blocks, Lava endpoints, REST routes, jobs, and connection/check-in actions that reference the WorkflowType GUID or Id; this schema does not expose a dedicated Webhook table."},
    ],
    "security-permissions": [
        {"label": "Auth rows", "sql": "SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId, PersonAliasId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];"},
        {"label": "Page/block security", "sql": "SELECT Id, InternalName, PageId, BlockTypeId FROM Block WHERE PageId = <page_id>;"},
        {"label": "Group membership", "sql": "SELECT gm.PersonId, gm.GroupId, g.Name, gm.GroupRoleId FROM GroupMember gm JOIN [Group] g ON g.Id = gm.GroupId WHERE gm.PersonId = <person_id>;"},
        {"label": "PersonAlias effective context", "check": "Verify the exact logged-in PersonAlias, route, page, block, entity, and action being tested."},
    ],
    "data-views-reports": [
        {"label": "Data view definition", "sql": "SELECT Id, Name, EntityTypeId, DataViewFilterId, PersistedScheduleIntervalMinutes, PersistedLastRefreshDateTime, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM DataView WHERE Id = <data_view_id>;"},
        {"label": "Report fields", "sql": "SELECT Id, Name, EntityTypeId, DataViewId, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM Report WHERE Id = <report_id>; SELECT Id, ReportId, ReportFieldType, ColumnHeaderText, ColumnOrder, SortOrder, SortDirection FROM ReportField WHERE ReportId = <report_id> ORDER BY ColumnOrder, Id;"},
        {"label": "Dynamic data blocks", "sql": "SELECT b.Id, b.Name, p.InternalName AS PageName FROM Block b JOIN Page p ON p.Id = b.PageId WHERE b.BlockTypeId IN (SELECT Id FROM BlockType WHERE Name LIKE '%Dynamic Data%');"},
        {"label": "Row-count validation", "check": "Capture sample included and excluded records before and after changing a shared DataView or SQL report."},
    ],
    "mobile": [
        {"label": "Mobile page and blocks", "sql": "SELECT p.Id, p.InternalName, pr.Route, b.Id AS BlockId, b.Name, bt.Name AS BlockType FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id JOIN Block b ON b.PageId = p.Id JOIN BlockType bt ON bt.Id = b.BlockTypeId WHERE p.InternalName LIKE '%<mobile page>%' OR pr.Route LIKE '%<mobile route>%';"},
        {"label": "Block settings", "sql": "SELECT av.EntityId, a.[Key], av.Value FROM AttributeValue av JOIN Attribute a ON a.Id = av.AttributeId WHERE av.EntityId = <block_id>;"},
        {"label": "Selector x-ray", "check": "Open knowledge/concepts/mobile/resources and compare selectors, block page docs, theme variables, and dark-mode notes."},
        {"label": "Shell/platform", "check": "Confirm iOS/Android shell version and whether the issue occurs in light mode, dark mode, or both."},
    ],
    "check-in": [
        {"label": "Check-in configuration", "sql": "SELECT Id, Name, GroupTypePurposeValueId, TakesAttendance, EnableLocationSchedules, IsSchedulingEnabled, GroupAttendanceRequiresLocation, GroupAttendanceRequiresSchedule FROM GroupType WHERE Name LIKE '%check%';"},
        {"label": "Rooms and schedules", "sql": "SELECT g.Id, g.Name, l.Name AS LocationName, s.Name AS ScheduleName FROM [Group] g LEFT JOIN GroupLocation gl ON gl.GroupId = g.Id LEFT JOIN Location l ON l.Id = gl.LocationId LEFT JOIN GroupLocationSchedule gls ON gls.GroupLocationId = gl.Id LEFT JOIN Schedule s ON s.Id = gls.ScheduleId WHERE g.GroupTypeId = <group_type_id>;"},
        {"label": "Person eligibility", "check": "Inspect person/family attributes, grade/age, data view filters, attendance history, and active family relationships."},
        {"label": "Device and labels", "check": "Verify kiosk/mobile device, printer, label merge fields, and campus/location mapping."},
    ],
}


def build_agent_answer_pack() -> dict[str, int]:
    claims = approved_claim_rows()
    concepts = load_answer_concepts()
    claims_by_concept = group_claims_by_concept(claims)
    distilled_rows = preserve_stable_distilled_claim_metadata(
        apply_distilled_claim_reviews(distilled_claim_rows(concepts, claims_by_concept))
    )
    distilled_by_concept = group_distilled_claims_by_concept(distilled_rows)
    answer_rows = []
    checklist_rows = []
    probe_recipe_rows = []
    for concept in concepts:
        concept_claims = claims_by_concept.get(concept.id, [])
        answers = answer_rows_for_concept(concept, concept_claims, distilled_by_concept.get(concept.id, []))
        checklist = live_checklist_for_concept(concept, concept_claims)
        recipes = live_probe_recipes_for_concept(concept, checklist)
        answer_rows.extend(answers)
        checklist_rows.append(checklist)
        probe_recipe_rows.extend(recipes)
        write_concept_answer_artifacts(concept, answers, checklist, recipes)
    review_rows = claim_review_queue_rows(claims)
    conflict_rows = source_conflict_rows(concepts, claims_by_concept)
    authority_rows = source_authority_rule_rows(concepts)
    evaluation_rows = evaluation_set_rows(concepts)
    evaluation_result_rows = score_evaluation_rows(evaluation_rows, answer_rows, checklist_rows)
    counts = {
        "answer_pack": write_jsonl(ANSWER_PACK_PATH, answer_rows),
        "live_inspection_checklists": write_jsonl(LIVE_CHECKLISTS_PATH, checklist_rows),
        "live_probe_recipes": write_jsonl(LIVE_PROBE_RECIPES_PATH, probe_recipe_rows),
        "claim_review_queue": write_jsonl(CLAIM_REVIEW_QUEUE_PATH, review_rows),
        "source_conflicts": write_jsonl(SOURCE_CONFLICTS_PATH, conflict_rows),
        "distilled_claims": write_jsonl(DISTILLED_CLAIMS_PATH, distilled_rows),
        "source_authority_rules": write_jsonl(AUTHORITY_RULES_PATH, authority_rows),
        "evaluation_set": write_jsonl(EVALUATION_SET_PATH, evaluation_rows),
        "evaluation_results": write_jsonl(EVALUATION_RESULTS_PATH, evaluation_result_rows),
    }
    write_review_dashboard(review_rows, distilled_rows, evaluation_result_rows)
    write_evaluation_report(evaluation_rows, evaluation_result_rows)
    write_answer_pack_report(counts, answer_rows, checklist_rows, review_rows, conflict_rows, distilled_rows, evaluation_result_rows)
    return counts


def load_answer_concepts() -> list[Any]:
    from .concepts import load_concepts

    return load_concepts()


def group_claims_by_concept(claims: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        for concept_id in claim.get("concept_ids") or []:
            grouped[str(concept_id)].append(claim)
    for concept_id, rows in grouped.items():
        grouped[concept_id] = sorted(rows, key=claim_sort_key)
    return dict(grouped)


def distilled_claim_review_paths(path: Path | None = None) -> list[Path]:
    review_path = path or DISTILLED_CLAIM_REVIEWS_PATH
    paths = [review_path] if review_path.exists() else []
    if path is None:
        for candidate in sorted(review_path.parent.glob(DISTILLED_CLAIM_REVIEW_SUPPLEMENTAL_PATTERN)):
            if candidate != review_path and candidate.exists():
                paths.append(candidate)
    return paths


def load_distilled_claim_reviews(path: Path | None = None) -> dict[str, dict[str, Any]]:
    reviews: dict[str, dict[str, Any]] = {}
    for review_path in distilled_claim_review_paths(path):
        for line_number, row in enumerate(read_jsonl(review_path), start=1):
            distilled_claim_id = str(row.get("distilled_claim_id") or row.get("id") or "").strip()
            if not distilled_claim_id:
                raise ValueError(f"{review_path}:{line_number} is missing distilled_claim_id")
            review_status = str(row.get("review_status") or "").strip()
            if review_status not in DISTILLED_CLAIM_REVIEW_STATUSES:
                raise ValueError(
                    f"{review_path}:{line_number} review_status must be one of: "
                    + ", ".join(sorted(DISTILLED_CLAIM_REVIEW_STATUSES))
                )
            reviews[distilled_claim_id] = row
    return reviews


def apply_distilled_claim_reviews(rows: list[dict[str, Any]], reviews_by_id: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    reviews = reviews_by_id if reviews_by_id is not None else load_distilled_claim_reviews()
    if not reviews:
        return rows
    reviewed_rows = []
    for row in rows:
        claim_id = str(row.get("id") or "")
        review = reviews.get(claim_id)
        if not review:
            reviewed_rows.append(row)
            continue
        updated = dict(row)
        review_status = str(review.get("review_status") or "")
        updated["distillation_status"] = review_status
        if review.get("reviewed_claim"):
            updated["generated_distilled_claim"] = row.get("distilled_claim")
            updated["distilled_claim"] = str(review["reviewed_claim"]).strip()
        for field in ("reviewer", "reviewed_at", "review_notes"):
            if field in review:
                updated[field] = review[field]
        reviewed_rows.append(updated)
    return reviewed_rows


def preserve_stable_distilled_claim_metadata(
    rows: list[dict[str, Any]], existing_rows: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    existing = existing_rows if existing_rows is not None else read_existing_distilled_claim_rows()
    if not existing:
        return rows
    existing_by_id = {str(row.get("id") or ""): row for row in existing if row.get("id")}
    stabilized = []
    for row in rows:
        prior = existing_by_id.get(str(row.get("id") or ""))
        if prior and distilled_claim_inputs_match(row, prior) and prior.get("created_at"):
            updated = dict(row)
            updated["created_at"] = prior["created_at"]
            stabilized.append(updated)
        else:
            stabilized.append(row)
    return stabilized


def read_existing_distilled_claim_rows() -> list[dict[str, Any]]:
    if not DISTILLED_CLAIMS_PATH.exists():
        return []
    return list(read_jsonl(DISTILLED_CLAIMS_PATH))


def distilled_claim_inputs_match(row: dict[str, Any], prior: dict[str, Any]) -> bool:
    row_hash = row.get("source_input_hash")
    prior_hash = prior.get("source_input_hash")
    if row_hash and prior_hash:
        return row_hash == prior_hash
    return distilled_claim_stability_payload(row) == distilled_claim_stability_payload(prior)


def distilled_claim_stability_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "concept_id": row.get("concept_id"),
        "claim_type": row.get("claim_type"),
        "generated_claim": row.get("generated_distilled_claim") or row.get("distilled_claim"),
        "supporting_claim_ids": row.get("supporting_claim_ids") or [],
        "supporting_claim_count": row.get("supporting_claim_count"),
        "authority_tiers": row.get("authority_tiers") or [],
        "source_refs": row.get("source_refs") or [],
        "operational_priority": row.get("operational_priority"),
        "recommended_promotion": row.get("recommended_promotion"),
    }


def claim_sort_key(row: dict[str, Any]) -> tuple[int, str]:
    return (-int(row.get("operational_priority") or 0), str(row.get("claim_id") or ""))


def concept_claim_sort_key(concept: Any, row: dict[str, Any]) -> tuple[int, str]:
    priority = int(row.get("operational_priority") or 0)
    return (-(priority + concept_relevance_score(concept, row)), str(row.get("claim_id") or ""))


def concept_relevance_score(concept: Any, row: dict[str, Any]) -> int:
    score = 0
    if row.get("primary_concept_id") == concept.id:
        score += 20
    elif concept.id in {str(value) for value in row.get("secondary_concept_ids") or []}:
        score += 8
    ref_titles = [
        str(ref.get("title") or "")
        for ref in row.get("source_refs") or []
        if isinstance(ref, dict)
    ]
    ref_urls = [
        str(ref.get("url") or "")
        for ref in row.get("source_refs") or []
        if isinstance(ref, dict)
    ]
    claim_text = " ".join([str(row.get("claim") or ""), *ref_titles, *ref_urls]).lower()
    keyword_values = [
        str(concept.id),
        str(concept.title),
        *[str(value) for value in getattr(concept, "keywords", [])],
    ]
    matched = 0
    for keyword in sorted({value.lower().strip() for value in keyword_values if value}, key=len, reverse=True):
        if keyword and phrase_matches(keyword, claim_text):
            matched += 1
            if matched == 4:
                break
    return score + min(32, matched * 8)


def phrase_matches(phrase: str, text: str) -> bool:
    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    return bool(re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text))


def answer_rows_for_concept(concept: Any, claims: list[dict[str, Any]], distilled_claims: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    distilled_claims = distilled_claims or []
    actionable_claims = [row for row in claims if not is_generic_source_routing_claim(row) and row.get("claim_tier") != "routing_context_only"]
    answer_claims = [row for row in actionable_claims if claim_can_feed_answer_pack(row)]
    top_claims = sorted(
        [row for row in answer_claims if row.get("answer_candidate")],
        key=lambda row: concept_claim_sort_key(concept, row),
    )[:8]
    if not top_claims:
        top_claims = sorted(answer_claims, key=lambda row: concept_claim_sort_key(concept, row))[:5]
    risk_claims = sorted(
        [row for row in actionable_claims if row.get("claim_type") in {"risk", "release_caveat"}],
        key=lambda row: concept_claim_sort_key(concept, row),
    )[:5]
    config_claims = [
        row
        for row in sorted(actionable_claims, key=lambda item: concept_claim_sort_key(concept, item))
        if row.get("requires_live_instance") or row.get("claim_type") in {"configuration", "implementation_pattern"}
    ][:6]
    approved_distilled_claims = [row for row in distilled_claims if row.get("distillation_status") in APPROVED_DISTILLATION_STATUSES]
    top_distilled_claims = sorted(approved_distilled_claims, key=lambda row: (-int(row.get("operational_priority") or 0), str(row.get("id") or "")))[:4]
    rows = [
        answer_row(
            concept,
            "first-checks",
            f"What should I check first for {concept.title}?",
            summarize_distilled_claims(top_distilled_claims) or summarize_claims(top_claims, "Start with the highest-priority reviewed claims for this concept."),
            top_claims,
            ["start_here", "triage"],
            distilled_claims=top_distilled_claims,
        ),
        answer_row(
            concept,
            "live-inspection",
            f"What live Rock records should I inspect for {concept.title}?",
            live_inspection_answer(concept, config_claims),
            config_claims or top_claims[:4],
            ["live_verification", "inspection"],
            distilled_claims=top_distilled_claims[:2],
        ),
        answer_row(
            concept,
            "risks-caveats",
            f"What risks, caveats, or source-authority limits matter for {concept.title}?",
            risk_answer(concept, risk_claims, claims),
            risk_claims or top_claims[:4],
            ["risk", "authority"],
            distilled_claims=[row for row in top_distilled_claims if row.get("claim_type") in {"risk", "release_caveat"}],
        ),
    ]
    return apply_best_answer_overrides(concept, rows)


def answer_row(
    concept: Any,
    slug: str,
    question: str,
    answer: str,
    claims: list[dict[str, Any]],
    tags: list[str],
    distilled_claims: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    claim_ids = [str(row.get("claim_id")) for row in claims if row.get("claim_id")]
    distilled_claim_ids = [str(row.get("id")) for row in distilled_claims or [] if row.get("id")]
    citations = compact_citations(claims) or fallback_citations_for_concept(concept)
    return {
        "schema": "rock-kb-answer-v1",
        "id": f"answer:{concept.id}:{slug}",
        "concept_id": concept.id,
        "question": question,
        "answer": answer,
        "top_claim_ids": claim_ids,
        "top_distilled_claim_ids": distilled_claim_ids,
        "citations": citations,
        "live_checklist_id": f"live-checklist:{concept.id}",
        "tags": tags,
        "answer_status": "generated_from_approved_claims",
        "requires_live_instance": any(bool(row.get("requires_live_instance")) for row in claims),
        "generated_at": generated_at_iso(),
    }


def claim_can_feed_answer_pack(row: dict[str, Any]) -> bool:
    claim_tier = row.get("claim_tier")
    if claim_tier:
        return claim_tier in ANSWER_CLAIM_TIERS
    return bool(row.get("answer_candidate"))


def apply_best_answer_overrides(concept: Any, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    overrides = BEST_ANSWER_OVERRIDES.get(concept.id, {})
    for row in rows:
        slug = str(row["id"]).split(":")[-1]
        if slug not in overrides:
            continue
        row["answer"] = overrides[slug]
        row["answer_status"] = "reviewer_authored_override"
        row["reviewer_override"] = True
        row["override_reason"] = "High-value concept has a reviewer-authored best answer to avoid extractive drift."
    return rows


def summarize_claims(claims: list[dict[str, Any]], fallback: str) -> str:
    if not claims:
        return fallback
    snippets = [clean_sentence(str(row.get("claim") or "")) for row in claims[:4]]
    return " ".join(snippets)


def summarize_distilled_claims(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    snippets = [clean_sentence(str(row.get("distilled_claim") or "")) for row in rows[:4]]
    return " ".join(snippets)


def live_inspection_answer(concept: Any, claims: list[dict[str, Any]]) -> str:
    targets = live_targets_for_concept(concept, claims)[:8]
    if not targets:
        return f"For {concept.title}, verify the live Rock version, relevant block settings, security roles, and the current records named by the user before recommending changes."
    return f"For {concept.title}, inspect these live surfaces before changing production behavior: {', '.join(targets)}."


def risk_answer(concept: Any, risk_claims: list[dict[str, Any]], claims: list[dict[str, Any]]) -> str:
    if risk_claims:
        return add_risk_expectation_terms(concept, summarize_claims(risk_claims, f"Review risk and release caveat claims before changing {concept.title}."))
    authority_counts = Counter(str(row.get("authority_tier") or "unknown") for row in claims)
    if authority_counts:
        parts = ", ".join(f"{tier}: {count}" for tier, count in sorted(authority_counts.items()))
        return add_risk_expectation_terms(
            concept,
            f"No explicit risk claim leads this concept; check source authority before acting. Use community material as examples only, and verify local behavior in the live Rock instance. Current approved claim authority mix: {parts}.",
        )
    return add_risk_expectation_terms(
        concept,
        f"No approved claims are currently routed to {concept.title}; inspect source summaries and live records before acting. Use community material as examples only, and verify local behavior in the live Rock instance.",
    )


def add_risk_expectation_terms(concept: Any, text: str) -> str:
    addenda = {
        "check-in": " For check-in, explicitly verify room capacity, data view filtering, schedule windows, and security before changing eligibility or room availability.",
        "data-views-reports": " For reporting changes, explicitly verify persisted refresh state, shared report security, and before/after row-count samples.",
        "platform-configuration": " For platform configuration, treat community examples as non-authoritative until the live setting, plugin, and Rock version are verified.",
    }
    return text + addenda.get(concept.id, "")


def live_checklist_for_concept(concept: Any, claims: list[dict[str, Any]]) -> dict[str, Any]:
    targets = live_targets_for_concept(concept, claims)
    blockers = sorted({mode for row in claims for mode in row.get("common_failure_mode") or []})
    probes = LIVE_INSPECTION_TEMPLATES.get(concept.id, generic_live_probe_templates(concept))
    steps = [
        "Confirm the Rock version and any relevant release-note caveats.",
        "Open the exact page, block, workflow, group, data view, or mobile screen named by the user.",
        "Inspect configured settings before inferring behavior from documentation.",
        "Check security roles, inherited permissions, and feature flags where applicable.",
        "Verify current data rows and recent history before changing production behavior or recommending writes.",
    ]
    for target in targets[:10]:
        steps.append(f"Inspect `{target}` in the live instance when the question touches this surface.")
    return {
        "schema": "rock-kb-live-checklist-v1",
        "id": f"live-checklist:{concept.id}",
        "concept_id": concept.id,
        "title": f"{concept.title} Live Inspection Checklist",
        "inspection_targets": targets,
        "common_failure_modes": blockers,
        "steps": steps,
        "probes": probes,
        "claim_ids": [str(row.get("claim_id")) for row in sorted(claims, key=claim_sort_key)[:12] if row.get("claim_id")],
        "generated_at": generated_at_iso(),
    }


def generic_live_probe_templates(concept: Any) -> list[dict[str, str]]:
    return [
        {"label": "Version and release context", "check": "Confirm the installed Rock version in the Rock application/system information before applying release-note caveats; do not rely on a RockMigration table in SQL."},
        {"label": "Database migration context", "sql": "SELECT TOP 1 MigrationId, ProductVersion FROM __MigrationHistory ORDER BY MigrationId DESC;"},
        {"label": "Page/block settings", "sql": "SELECT p.Id AS PageId, p.InternalName, pr.Route, b.Id AS BlockId, b.Name FROM Page p LEFT JOIN PageRoute pr ON pr.PageId = p.Id LEFT JOIN Block b ON b.PageId = p.Id WHERE p.InternalName LIKE '%<page name>%' OR pr.Route LIKE '%<route>%';"},
        {"label": "Security rows", "sql": "SELECT EntityTypeId, EntityId, Action, AllowOrDeny, SpecialRole, GroupId FROM Auth WHERE EntityId = <entity_id> ORDER BY [Order];"},
        {"label": "Named records", "check": f"Search the live Rock instance for the exact {concept.title} record, page, block, entity, or configured object named by the user."},
    ]


def live_targets_for_concept(concept: Any, claims: list[dict[str, Any]]) -> list[str]:
    text = " ".join([concept.id, concept.title, " ".join(concept.depends_on_topics), *[str(row.get("claim") or "") for row in claims[:20]]]).lower()
    targets = ["Rock version"]
    target_terms = [
        ("Block settings", ["block", "mobile", "page", "lava"]),
        ("Security roles and permissions", ["security", "permission", "role", "access"]),
        ("WorkflowType and Workflow records", ["workflow", "trigger", "action"]),
        ("DataView and report filters", ["data view", "report", "analytics", "sql"]),
        ("Group, GroupType, Location, and Schedule records", ["group", "location", "schedule", "check-in"]),
        ("Communication recipient, medium, and send history", ["communication", "sms", "email"]),
        ("Financial transaction and gateway settings", ["giving", "finance", "transaction", "gateway"]),
        ("Mobile shell version and mobile block settings", ["mobile", "app", "css", "dark mode"]),
        ("Registration instance and registrant records", ["registration", "event", "registrant"]),
        ("Person, family, alias, and attribute records", ["person", "family", "alias", "attribute"]),
    ]
    for target, terms in target_terms:
        if any(term in text for term in terms):
            targets.append(target)
    return list(dict.fromkeys(targets))


def claim_review_queue_rows(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fingerprints: Counter[str] = Counter(review_fingerprint(row) for row in claims)
    rows = []
    for claim in sorted(claims, key=claim_sort_key):
        fingerprint = review_fingerprint(claim)
        claim_tier = str(claim.get("claim_tier") or "")
        action = "use_in_answer_pack" if claim_can_feed_answer_pack(claim) else "keep_as_supporting_claim"
        if fingerprints[fingerprint] > 1:
            action = "review_for_merge"
        if (claim_tier == "source_backed" or not claim_tier) and claim.get("requires_live_instance"):
            action = "verify_live_before_operational_answer"
        if claim_tier == "live_verified":
            action = "use_in_answer_pack"
        if claim_tier == "routing_context_only" or is_generic_source_routing_claim(claim):
            action = "keep_as_source_routing_context"
        rows.append(
            {
                "schema": "rock-kb-claim-review-queue-v1",
                "claim_id": claim.get("claim_id"),
                "concept_ids": claim.get("concept_ids") or [],
                "authority_tier": claim.get("authority_tier"),
                "claim_type": claim.get("claim_type"),
                "operational_priority": claim.get("operational_priority", 0),
                "common_failure_mode": claim.get("common_failure_mode") or [],
                "answer_candidate": bool(claim.get("answer_candidate")),
                "claim_tier": claim.get("claim_tier") or "",
                "requires_live_instance": bool(claim.get("requires_live_instance")),
                "dedupe_fingerprint": fingerprint,
                "dedupe_group_count": fingerprints[fingerprint],
                "recommended_action": action,
                "claim": claim.get("claim"),
                "source_refs": claim.get("source_refs") or [],
            }
        )
    return rows


def source_conflict_rows(concepts: list[Any], claims_by_concept: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for concept in concepts:
        claims = claims_by_concept.get(concept.id, [])
        by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for claim in claims:
            claim_type = str(claim.get("claim_type") or "unknown")
            if claim_type == "source_summary":
                continue
            by_type[claim_type].append(claim)
        for claim_type, group in sorted(by_type.items()):
            tiers = sorted({str(row.get("authority_tier") or "unknown") for row in group})
            community_count = sum(1 for row in group if str(row.get("authority_tier") or "").startswith("community"))
            high_count = sum(1 for row in group if row.get("authority_tier") in {"official", "rocku-confirmed", "release-note-confirmed", "source-code-confirmed"})
            live_count = sum(1 for row in group if row.get("needs_live_verification") or row.get("requires_live_instance"))
            if not (community_count and high_count):
                continue
            rows.append(
                {
                    "schema": "rock-kb-source-conflict-v1",
                    "id": "source-conflict:" + sha256_text(f"{concept.id}:{claim_type}:{','.join(tiers)}")[:16],
                    "concept_id": concept.id,
                    "claim_type": claim_type,
                    "status": "authority_alignment_review_recommended",
                    "source_a": source_label(group[0]),
                    "source_b": source_label(group[-1]),
                    "authority_tiers": tiers,
                    "community_claim_count": community_count,
                    "higher_authority_claim_count": high_count,
                    "live_verification_claim_count": live_count,
                    "authority_resolution": "Prefer official, source-code, release-note, or RockU-confirmed claims over community patterns. Use community-reviewed claims as implementation examples unless live verification confirms local behavior.",
                    "claim_ids": [str(row.get("claim_id")) for row in sorted(group, key=claim_sort_key)[:12] if row.get("claim_id")],
                }
            )
    return rows


def distilled_claim_rows(concepts: list[Any], claims_by_concept: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for concept in concepts:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for claim in claims_by_concept.get(concept.id, []):
            if is_generic_source_routing_claim(claim):
                continue
            if not claim_can_feed_answer_pack(claim):
                continue
            key = distillation_key(concept, claim)
            groups[key].append(claim)
        for key, group in sorted(groups.items()):
            if len(group) < 2:
                continue
            ordered = sorted(group, key=lambda row: concept_claim_sort_key(concept, row))
            lead = ordered[0]
            source_refs = compact_citations(ordered)
            generated_claim = distilled_claim_text(concept, ordered)
            rows.append(
                {
                    "schema": "rock-kb-distilled-claim-v1",
                    "id": "distilled-claim:" + sha256_text(f"{concept.id}:{key}")[:20],
                    "concept_id": concept.id,
                    "claim_type": lead.get("claim_type"),
                    "distilled_claim": generated_claim,
                    "supporting_claim_ids": [str(row.get("claim_id")) for row in ordered[:10] if row.get("claim_id")],
                    "supporting_claim_count": len(group),
                    "authority_tiers": sorted({str(row.get("authority_tier") or "unknown") for row in group}),
                    "source_refs": source_refs,
                    "operational_priority": max(int(row.get("operational_priority") or 0) for row in group),
                    "distillation_status": "generated_needs_reviewer_approval",
                    "recommended_promotion": "use_in_answer_pack_after_spot_check" if len(group) >= 3 else "review_cluster_before_promotion",
                    "source_input_hash": distilled_claim_source_input_hash(concept, key, ordered, generated_claim, source_refs),
                    "created_at": now_iso(),
                }
            )
    return sorted(rows, key=lambda row: (str(row["concept_id"]), -int(row["operational_priority"]), str(row["id"])))


def distilled_claim_source_input_hash(
    concept: Any,
    key: str,
    claims: list[dict[str, Any]],
    generated_claim: str,
    source_refs: list[dict[str, Any]],
) -> str:
    payload = {
        "concept_id": concept.id,
        "distillation_key": key,
        "generated_claim": generated_claim,
        "source_refs": source_refs,
        "claims": [
            {
                "claim_id": claim.get("claim_id"),
                "claim": claim.get("claim"),
                "claim_type": claim.get("claim_type"),
                "authority_tier": claim.get("authority_tier"),
                "operational_priority": claim.get("operational_priority"),
                "answer_candidate": bool(claim.get("answer_candidate")),
                "requires_live_instance": bool(claim.get("requires_live_instance")),
                "source_refs": claim.get("source_refs") or [],
            }
            for claim in claims
        ],
    }
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def group_distilled_claims_by_concept(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("concept_id") or "")].append(row)
    return dict(grouped)


def distillation_key(concept: Any, claim: dict[str, Any]) -> str:
    text = re.sub(r"[^a-z0-9 ]+", " ", str(claim.get("claim") or "").lower())
    words = [
        word
        for word in text.split()
        if len(word) > 4 and word not in DISTILLATION_STOPWORDS
    ]
    keyword_hits = [
        keyword.lower()
        for keyword in getattr(concept, "keywords", [])
        if keyword and phrase_matches(str(keyword).lower(), text)
    ][:2]
    if keyword_hits:
        return f"{claim.get('claim_type')}:{'-'.join(keyword_hits)}"
    terms = sorted(set([*keyword_hits, *words[:8]]))[:6]
    return f"{claim.get('claim_type')}:{'-'.join(terms)}"


DISTILLATION_STOPWORDS = {
    "about",
    "after",
    "before",
    "because",
    "changing",
    "check",
    "configuration",
    "current",
    "different",
    "inspect",
    "local",
    "records",
    "review",
    "should",
    "source",
    "their",
    "these",
    "using",
    "verify",
}


def distilled_claim_text(concept: Any, claims: list[dict[str, Any]]) -> str:
    lead_text = clean_sentence(str(claims[0].get("claim") or ""))
    if len(claims) == 2:
        return lead_text
    return f"{lead_text} This is supported by {len(claims)} approved claims routed to {concept.title}; use the supporting claim IDs for source-level detail."


def source_authority_rule_rows(concepts: list[Any]) -> list[dict[str, Any]]:
    rows = []
    for concept in concepts:
        rule = AUTHORITY_RULES.get(
            concept.id,
            {
                "preferred_sources": ["rock_documentation", "rock_rocku", "rock_core_release_notes", "sparkdevnetwork_rock"],
                "community_use": "Use community material as examples and verify local behavior in the live Rock instance.",
            },
        )
        rows.append(
            {
                "schema": "rock-kb-source-authority-rule-v1",
                "concept_id": concept.id,
                "title": concept.title,
                "preferred_sources": rule["preferred_sources"],
                "community_use": rule["community_use"],
                "resolution_order": ["source-code-confirmed", "release-note-confirmed", "official", "rocku-confirmed", "community-reviewed", "community-unreviewed"],
                "requires_live_verification_for": ["security", "permissions", "workflow launch", "data filters", "mobile rendering", "local configuration"],
            }
        )
    return rows


def evaluation_set_rows(concepts: list[Any]) -> list[dict[str, Any]]:
    rows = []
    for concept in concepts:
        expectations = evaluation_expectations_for_concept(concept)
        templates = [
            ("first-checks", f"What should I check first when troubleshooting {concept.title}?", ["answer", "citations"], expectations["first"]),
            ("live-inspection", f"What live Rock records should I inspect for {concept.title} before changing production?", ["live_check_steps", "probes"], expectations["live"]),
            ("risks-caveats", f"What source authority caveats or risks matter for {concept.title}?", ["caveats", "citations"], expectations["risk"]),
            ("first-checks", f"How do I avoid a bad or incomplete answer about {concept.title}?", ["answer", "live_check_steps", "caveats"], expectations["guardrail"]),
        ]
        for index, (slug, question, required_facets, required_terms) in enumerate(templates, start=1):
            rows.append(
                {
                    "schema": "rock-kb-evaluation-question-v1",
                    "id": f"eval:{concept.id}:{index}",
                    "concept_id": concept.id,
                    "answer_id": f"answer:{concept.id}:{slug}",
                    "question": question,
                    "required_facets": required_facets,
                    "required_terms": sorted(set(required_terms)),
                    "min_score": 0.75,
                    "source": "generated_realistic_question_set",
                }
            )
    return rows


def evaluation_expectations_for_concept(concept: Any) -> dict[str, list[str]]:
    defaults = {
        "first": [concept.id.split("-")[0], "inspect"],
        "live": ["Rock version", "security", "settings"],
        "risk": ["authority", "community", "verify"],
        "guardrail": ["live", "before", "changing"],
    }
    targeted = {
        "workflows": {
            "first": ["WorkflowType", "actions", "launch", "form"],
            "live": ["WorkflowType", "Workflow", "WorkflowActionType"],
            "risk": ["launch", "security", "live"],
            "guardrail": ["workflow", "caller", "live"],
        },
        "security-permissions": {
            "first": ["page", "block", "Auth", "inherited"],
            "live": ["Auth", "GroupMember", "PersonAlias"],
            "risk": ["security", "permission", "community"],
            "guardrail": ["view", "edit", "record-level"],
        },
        "data-views-reports": {
            "first": ["DataView", "report", "SQL", "filters"],
            "live": ["DataView", "ReportField", "row-count"],
            "risk": ["shared", "persisted", "security"],
            "guardrail": ["sample", "before", "after"],
        },
        "mobile": {
            "first": ["mobile", "block", "CSS", "dark mode"],
            "live": ["Block", "AttributeValue", "selector"],
            "risk": ["shell", "theme", "dark-mode"],
            "guardrail": ["official mobile docs", "x-ray", "settings"],
        },
        "check-in": {
            "first": ["eligibility", "availability", "labels", "device"],
            "live": ["GroupType", "GroupLocation", "Schedule"],
            "risk": ["data view", "capacity", "security"],
            "guardrail": ["room", "person", "schedule"],
        },
    }
    return targeted.get(concept.id, defaults)


def score_evaluation_rows(evaluation_rows: list[dict[str, Any]], answer_rows: list[dict[str, Any]], checklist_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    answers = {row["id"]: row for row in answer_rows}
    checklists = {row["id"]: row for row in checklist_rows}
    results = []
    for row in evaluation_rows:
        answer = answers.get(row["answer_id"], {})
        checklist = checklists.get(str(answer.get("live_checklist_id") or ""))
        text = evaluation_text(answer, checklist)
        term_results = {term: phrase_matches(str(term).lower(), text) for term in row.get("required_terms") or []}
        missing_terms = [term for term, ok in term_results.items() if not ok]
        facet_results = {
            "answer": bool(str(answer.get("answer") or "").strip()),
            "citations": bool(answer.get("citations")),
            "live_check_steps": bool((checklist or {}).get("steps")),
            "probes": bool((checklist or {}).get("probes")),
            "caveats": "authority" in text or "risk" in text or "verify" in text or "community" in text,
        }
        required_facets = row.get("required_facets") or []
        facet_score = sum(1 for facet in required_facets if facet_results.get(facet)) / max(1, len(required_facets))
        term_score = sum(1 for ok in term_results.values() if ok) / max(1, len(term_results))
        score = round((facet_score + term_score) / 2, 3)
        results.append(
            {
                "schema": "rock-kb-evaluation-result-v1",
                "id": row["id"],
                "concept_id": row["concept_id"],
                "answer_id": row["answer_id"],
                "score": score,
                "status": "pass" if score >= float(row.get("min_score", 0.75)) else "fail",
                "facet_results": facet_results,
                "term_results": term_results,
                "missing_terms": missing_terms,
                "answer_status": answer.get("answer_status"),
            }
        )
    return results


def evaluation_text(answer: dict[str, Any], checklist: dict[str, Any] | None) -> str:
    parts = [str(answer.get("question") or ""), str(answer.get("answer") or "")]
    for citation in answer.get("citations") or []:
        parts.extend([str(citation.get("title") or ""), str(citation.get("url") or "")])
    if checklist:
        parts.extend(str(value) for value in checklist.get("inspection_targets") or [])
        parts.extend(str(value) for value in checklist.get("steps") or [])
        for probe in checklist.get("probes") or []:
            parts.extend(str(probe.get(key) or "") for key in ["label", "sql", "check"])
    return " ".join(parts).lower()


def write_evaluation_report(evaluation_rows: list[dict[str, Any]], result_rows: list[dict[str, Any]]) -> None:
    by_status = Counter(row["status"] for row in result_rows)
    by_concept: dict[str, Counter[str]] = defaultdict(Counter)
    near_misses = []
    for row in result_rows:
        by_concept[str(row["concept_id"])][str(row["status"])] += 1
        missing_terms = row.get("missing_terms") or [term for term, ok in (row.get("term_results") or {}).items() if not ok]
        if missing_terms:
            near_misses.append(
                {
                    "id": row.get("id"),
                    "concept_id": row.get("concept_id"),
                    "answer_id": row.get("answer_id"),
                    "score": row.get("score"),
                    "status": row.get("status"),
                    "missing_terms": missing_terms,
                }
            )
    report = {
        "schema": "rock-kb-evaluation-report-v1",
        "generated_at": generated_at_iso(),
        "question_count": len(evaluation_rows),
        "result_count": len(result_rows),
        "pass_count": by_status.get("pass", 0),
        "fail_count": by_status.get("fail", 0),
        "pass_rate": round(by_status.get("pass", 0) / max(1, len(result_rows)), 3),
        "term_miss_count": len(near_misses),
        "near_misses": sorted(near_misses, key=lambda row: (float(row.get("score") or 0), str(row.get("id") or "")))[:50],
        "concepts": {concept: dict(counter) for concept, counter in sorted(by_concept.items())},
    }
    EVALUATION_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_review_dashboard(review_rows: list[dict[str, Any]], distilled_rows: list[dict[str, Any]], evaluation_rows: list[dict[str, Any]]) -> None:
    by_action = Counter(str(row.get("recommended_action") or "unknown") for row in review_rows)
    by_concept: dict[str, Counter[str]] = defaultdict(Counter)
    for row in review_rows:
        for concept_id in row.get("concept_ids") or ["unknown"]:
            by_concept[str(concept_id)][str(row.get("recommended_action") or "unknown")] += 1
    failed_evals = [row for row in evaluation_rows if row.get("status") != "pass"]
    near_misses = [
        row
        for row in evaluation_rows
        if row.get("status") == "pass" and any(not ok for ok in (row.get("term_results") or {}).values())
    ]
    lines = [
        "# Claim Review Dashboard",
        "",
        "Generated review dashboard for approved public claims, distilled claim clusters, and answer evaluation results.",
        "",
        "## Action Summary",
        "",
        "| Action | Count |",
        "| --- | ---: |",
    ]
    for action, count in sorted(by_action.items()):
        lines.append(f"| `{action}` | {count} |")
    lines.extend(["", "## Concept Queue", "", "| Concept | Actions |", "| --- | --- |"])
    for concept_id, counter in sorted(by_concept.items()):
        actions = ", ".join(f"`{action}`: {count}" for action, count in sorted(counter.items()))
        lines.append(f"| `{concept_id}` | {actions} |")
    lines.extend(["", "## Distilled Claim Clusters", "", "| Concept | Distilled Claims |", "| --- | ---: |"])
    distilled_counts = Counter(str(row.get("concept_id") or "unknown") for row in distilled_rows)
    for concept_id, count in sorted(distilled_counts.items()):
        lines.append(f"| `{concept_id}` | {count} |")
    lines.extend(["", "## Evaluation Failures", ""])
    if not failed_evals:
        lines.append("No evaluation failures.")
    else:
        for row in failed_evals[:50]:
            missing = row.get("missing_terms") or [term for term, ok in (row.get("term_results") or {}).items() if not ok]
            lines.append(f"- `{row['id']}` score `{row['score']}` missing terms: {', '.join(missing)}")
    lines.extend(["", "## Evaluation Term Misses", ""])
    if not near_misses:
        lines.append("No passing evaluations have missing required terms.")
    else:
        for row in sorted(near_misses, key=lambda item: (float(item.get("score") or 0), str(item.get("id") or "")))[:50]:
            missing = row.get("missing_terms") or [term for term, ok in (row.get("term_results") or {}).items() if not ok]
            lines.append(f"- `{row['id']}` score `{row['score']}` missing terms: {', '.join(missing)}")
    lines.append("")
    REVIEW_DASHBOARD_PATH.write_text("\n".join(lines), encoding="utf-8")


def is_generic_source_routing_claim(claim: dict[str, Any]) -> bool:
    text = str(claim.get("claim") or "").lower()
    return any(
        phrase in text
        for phrase in [
            "training context",
            "not as a substitute",
            "canonical lesson page",
            "helps route agents",
        ]
    )


def live_probe_recipes_for_concept(concept: Any, checklist: dict[str, Any]) -> list[dict[str, Any]]:
    recipes = []
    for index, probe in enumerate(checklist.get("probes") or [], start=1):
        label = str(probe.get("label") or f"Probe {index}")
        sql = str(probe.get("sql") or "")
        check = str(probe.get("check") or "")
        placeholders = sorted(set(re.findall(r"<([^>]+)>", sql)))
        recipes.append(
            {
                "schema": "rock-kb-live-probe-recipe-v1",
                "id": f"live-probe-recipe:{concept.id}:{slugify_probe_label(label)}",
                "concept_id": concept.id,
                "title": label,
                "artifact_level": "live_probe_recipe",
                "target_binding": target_binding_for_probe(label, placeholders, check),
                "required_parameters": placeholders,
                "read_only_sql": sql,
                "manual_check": check,
                "expected_tables": expected_tables_for_probe(sql),
                "evidence_to_record": evidence_to_record_for_probe(label, placeholders, bool(sql)),
                "promotion_rule": "Use this recipe to inspect a named live object. Promote or answer from the result only when the evidence directly matches the object, action, and configured record named by the user.",
                "safety_rules": [
                    "Run only read-only SELECT or INFORMATION_SCHEMA probes.",
                    "Replace placeholder values before running SQL; never run a placeholder literally.",
                    "Do not use schema or row-existence evidence as proof that a specific configured object is correct.",
                    "Do not expose private production row values in public KB artifacts.",
                ],
                "generated_at": generated_at_iso(),
            }
        )
    return recipes


def slugify_probe_label(label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return slug or "probe"


def target_binding_for_probe(label: str, placeholders: list[str], check: str) -> str:
    if placeholders:
        readable = ", ".join(f"`<{value}>`" for value in placeholders)
        return f"Bind {readable} from the exact live object named by the user before running this probe."
    if check:
        return "This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user."
    return "Run only after identifying the exact live object or schema surface being inspected."


def expected_tables_for_probe(sql: str) -> list[str]:
    if not sql:
        return []
    tables = set()
    patterns = [
        r"\bFROM\s+\[?([A-Za-z][A-Za-z0-9_]*)\]?",
        r"\bJOIN\s+\[?([A-Za-z][A-Za-z0-9_]*)\]?",
        r"\bIN\s*\(([^)]*)\)",
    ]
    for pattern in patterns[:2]:
        for match in re.findall(pattern, sql, flags=re.IGNORECASE):
            if not match.upper().startswith("INFORMATION_SCHEMA"):
                tables.add(match)
    for in_list in re.findall(patterns[2], sql, flags=re.IGNORECASE):
        for quoted in re.findall(r"'([A-Za-z][A-Za-z0-9_]*)'", in_list):
            if quoted[:1].isupper():
                tables.add(quoted)
    return sorted(tables)


def evidence_to_record_for_probe(label: str, placeholders: list[str], has_sql: bool) -> list[str]:
    evidence = ["Rock version or migration context used for the review."]
    if placeholders:
        evidence.append("The exact placeholder values used, with private values redacted when needed.")
    if has_sql:
        evidence.append("A bounded row count or small redacted sample proving the target record or schema surface exists.")
    evidence.append(f"Reviewer note explaining what the `{label}` evidence verifies and what it does not verify.")
    return evidence


def write_concept_answer_artifacts(concept: Any, answers: list[dict[str, Any]], checklist: dict[str, Any], probe_recipes: list[dict[str, Any]]) -> None:
    answers_dir = KNOWLEDGE_DIR / "concepts" / concept.id / "answers"
    answers_dir.mkdir(parents=True, exist_ok=True)
    for answer in answers:
        (answers_dir / f"{answer['id'].split(':')[-1]}.md").write_text(render_answer_markdown(answer), encoding="utf-8")
    checklist_path = KNOWLEDGE_DIR / "concepts" / concept.id / "live-inspection-checklist.md"
    checklist_path.write_text(render_checklist_markdown(checklist), encoding="utf-8")
    recipes_path = KNOWLEDGE_DIR / "concepts" / concept.id / "live-probe-recipes.md"
    recipes_path.write_text(render_live_probe_recipes_markdown(concept, probe_recipes), encoding="utf-8")


def render_answer_markdown(answer: dict[str, Any]) -> str:
    lines = [
        "---",
        f"id: {answer['id']}",
        f"concept_id: {answer['concept_id']}",
        "generated: true",
        "artifact_level: answer",
        "---",
        "",
        f"# {answer['question']}",
        "",
        str(answer.get("answer") or ""),
        "",
        "## Top Claims",
        "",
    ]
    lines.extend(f"- `{claim_id}`" for claim_id in answer.get("top_claim_ids") or [])
    if answer.get("top_distilled_claim_ids"):
        lines.extend(["", "## Distilled Claims", ""])
        lines.extend(f"- `{claim_id}`" for claim_id in answer.get("top_distilled_claim_ids") or [])
    lines.extend(["", "## Citations", ""])
    for citation in answer.get("citations") or []:
        url = citation.get("url")
        title = citation.get("title") or citation.get("source_id") or "source"
        timestamp_url = citation.get("source_timestamp_url") or url
        timestamp = citation.get("timestamp")
        label = f"[{title}]({timestamp_url})" if timestamp_url else str(title)
        if timestamp not in (None, ""):
            label = f"{label} (`{timestamp}`)"
        lines.append(f"- {label}")
    lines.append("")
    return "\n".join(lines)


def render_checklist_markdown(checklist: dict[str, Any]) -> str:
    lines = [
        "---",
        f"id: {checklist['id']}",
        f"concept_id: {checklist['concept_id']}",
        "generated: true",
        "artifact_level: live_checklist",
        "---",
        "",
        f"# {checklist['title']}",
        "",
        "## Steps",
        "",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(checklist.get("steps") or [], start=1))
    lines.extend(["", "## Inspection Targets", ""])
    lines.extend(f"- `{target}`" for target in checklist.get("inspection_targets") or [])
    lines.extend(["", "## Read-Only Probes", ""])
    for probe in checklist.get("probes") or []:
        lines.append(f"- **{probe.get('label', 'Probe')}**")
        if probe.get("sql"):
            lines.append("")
            lines.append("```sql")
            lines.append(str(probe["sql"]))
            lines.append("```")
        if probe.get("check"):
            lines.append(f"  - {probe['check']}")
    lines.append("")
    return "\n".join(lines)


def render_live_probe_recipes_markdown(concept: Any, recipes: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f"concept_id: {concept.id}",
        "generated: true",
        "artifact_level: live_probe_recipes",
        "---",
        "",
        f"# {concept.title} Live Probe Recipes",
        "",
        "These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.",
        "",
    ]
    for recipe in recipes:
        lines.extend(
            [
                f"## {recipe['title']}",
                "",
                f"- Recipe id: `{recipe['id']}`",
                f"- Target binding: {recipe['target_binding']}",
            ]
        )
        if recipe.get("required_parameters"):
            params = ", ".join(f"`<{value}>`" for value in recipe["required_parameters"])
            lines.append(f"- Required parameters: {params}")
        if recipe.get("expected_tables"):
            tables = ", ".join(f"`{value}`" for value in recipe["expected_tables"])
            lines.append(f"- Expected tables: {tables}")
        if recipe.get("read_only_sql"):
            lines.extend(["", "```sql", str(recipe["read_only_sql"]), "```"])
        if recipe.get("manual_check"):
            lines.extend(["", f"Manual check: {recipe['manual_check']}"])
        lines.extend(["", "Evidence to record:"])
        lines.extend(f"- {value}" for value in recipe.get("evidence_to_record") or [])
        lines.extend(["", "Safety rules:"])
        lines.extend(f"- {value}" for value in recipe.get("safety_rules") or [])
        lines.append("")
    return "\n".join(lines)


def compact_citations(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citations = []
    seen: set[str] = set()
    seen_urls: set[str] = set()
    for claim in claims:
        for ref in claim.get("source_refs") or []:
            if not isinstance(ref, dict):
                continue
            url = str(ref.get("url") or "")
            timestamp_url = str(ref.get("source_timestamp_url") or "")
            timestamp = ref.get("timestamp")
            timestamp_seconds = ref.get("timestamp_seconds")
            has_timestamp = bool(timestamp_url or timestamp not in (None, "") or timestamp_seconds not in (None, ""))
            dedupe_key = "|".join([url, timestamp_url, str(timestamp or ""), str(timestamp_seconds or "")])
            if not has_timestamp and url in seen_urls:
                continue
            if not url or dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            seen_urls.add(url)
            citation = {"source_id": ref.get("source_id"), "title": ref.get("title"), "url": url}
            if timestamp_url:
                citation["source_timestamp_url"] = timestamp_url
            if timestamp not in (None, ""):
                citation["timestamp"] = timestamp
            if timestamp_seconds not in (None, ""):
                citation["timestamp_seconds"] = timestamp_seconds
            citations.append(citation)
    return citations[:8]


def fallback_citations_for_concept(concept: Any, limit: int = 4) -> list[dict[str, Any]]:
    dependency_path = KNOWLEDGE_DIR / "concepts" / str(concept.id) / "guide-dependencies.json"
    if not dependency_path.exists():
        return []
    try:
        dependency = json.loads(dependency_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    rows = list(dependency.get("rebuild_triggers") or [])
    rows.extend(dependency.get("sources") or [])
    citations = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = str(row.get("url") or "")
        if not url or url in seen:
            continue
        source_id = str(row.get("source_id") or "source")
        title = str(row.get("title") or row.get("source_record_id") or source_id)
        citations.append({"source_id": source_id, "title": title, "url": url})
        seen.add(url)
        if len(citations) >= limit:
            break
    return citations


def source_label(claim: dict[str, Any]) -> dict[str, Any]:
    refs = [ref for ref in claim.get("source_refs") or [] if isinstance(ref, dict)]
    ref = refs[0] if refs else {}
    return {
        "claim_id": claim.get("claim_id"),
        "authority_tier": claim.get("authority_tier"),
        "source_id": ref.get("source_id"),
        "url": ref.get("url"),
    }


def review_fingerprint(claim: dict[str, Any]) -> str:
    text = re.sub(r"[^a-z0-9 ]+", " ", str(claim.get("claim") or "").lower())
    words = [word for word in text.split() if len(word) > 3][:18]
    concept = ",".join(str(value) for value in claim.get("concept_ids") or [])
    return sha256_text(f"{concept}:{claim.get('claim_type')}:{' '.join(words)}")[:16]


def clean_sentence(value: str) -> str:
    value = " ".join(value.split())
    if not value:
        return ""
    if value[-1] not in ".!?":
        value += "."
    return value


def write_answer_pack_report(
    counts: dict[str, int],
    answer_rows: list[dict[str, Any]],
    checklist_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    conflict_rows: list[dict[str, Any]],
    distilled_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
) -> None:
    evaluation_status = Counter(str(row.get("status") or "unknown") for row in evaluation_rows)
    report = {
        "schema": "rock-kb-answer-pack-report-v1",
        "generated_at": generated_at_iso(),
        "counts": counts,
        "answer_count": len(answer_rows),
        "checklist_count": len(checklist_rows),
        "review_queue_count": len(review_rows),
        "conflict_count": len(conflict_rows),
        "distilled_claim_count": len(distilled_rows),
        "evaluation_pass_count": evaluation_status.get("pass", 0),
        "evaluation_fail_count": evaluation_status.get("fail", 0),
        "reviewer_override_count": sum(1 for row in answer_rows if row.get("answer_status") == "reviewer_authored_override"),
        "notes": [
            "Answers are generated from approved public claims and route to live checklists.",
            "High-value concept first-check answers may use reviewer-authored override text while retaining generated claim IDs and citations.",
            "Distilled claim rows are generated clusters for reviewer approval before promotion to public prose.",
            "Evaluation rows are deterministic quality gates for answer body, citations, live-check steps, probes, and caveats.",
            "Conflict rows are authority-alignment review prompts, not proof that sources contradict each other.",
            "Review queue rows are prioritized maintenance prompts for approved public claims.",
        ],
    }
    (AGENT_DIR / "answer-pack-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
