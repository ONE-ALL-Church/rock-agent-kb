from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Mapping
from urllib.parse import quote


JsonGetter = Callable[[str], dict[str, Any]]
JsonPoster = Callable[[str, dict[str, Any]], dict[str, Any]]

TEST_ROUND_SCHEMA = "rock-kb-community-test-round-v1"
TEST_ROUND_REVIEW_SCHEMA = "rock-kb-community-test-round-review-v1"
REVIEW_OUTCOMES = ("useful", "incorrect", "incomplete", "unclear", "unsure")
CASE_DEFINITIONS = (
    ("service-health", "service"),
    ("exact-group-model", "exact_lookup"),
    ("check-in-lava-context", "lava_context"),
    ("reviewed-recipe", "recipe"),
    ("check-in-troubleshooting", "semantic_search"),
    ("idea-relationship-trust", "rock_idea"),
    ("core-issue-trust", "imported_issue"),
    ("mobile-issue-release-evidence", "imported_issue"),
    ("issue-version-assessment", "imported_issue"),
    ("no-answer-boundary", "no_answer"),
)


def run_cohort_test(*, base_url: str, get_json: JsonGetter, post_json: JsonPoster) -> dict[str, Any]:
    base = base_url.rstrip("/")
    cases = [
        run_case("service-health", "service", "GET /health", "Does the service respond consistently?", lambda: health_case(base, get_json)),
        run_case("exact-group-model", "exact_lookup", "GET Group model", "Is the Group digest direct and useful without unrelated models?", lambda: model_case(base, get_json)),
        run_case("check-in-lava-context", "lava_context", "Search Check-In label roots", "Does the result clearly identify which Lava root is available?", lambda: lava_case(base, get_json)),
        run_case("reviewed-recipe", "recipe", "GET Check-In Status Dashboard recipe", "Is the recipe reusable and are its adaptation and live-verification boundaries clear?", lambda: recipe_case(base, get_json)),
        run_case("check-in-troubleshooting", "semantic_search", "Search an eligibility-versus-availability symptom", "Would the top results lead an administrator to the right first checks?", lambda: troubleshooting_case(base, get_json)),
        run_case("idea-relationship-trust", "rock_idea", "GET Rock Community Idea 1307", "Do the concept, model, and issue links help without presenting an Idea or reference as implementation proof?", lambda: rock_idea_case(base, get_json)),
        run_case("core-issue-trust", "imported_issue", "GET core issue 6920", "Is the unreviewed report clearly separated from its reviewed, source-backed enrichment?", lambda: core_issue_case(base, get_json)),
        run_case("mobile-issue-release-evidence", "imported_issue", "GET mobile issue 116", "Is the fixed-release evidence useful without implying every local instance is fixed?", lambda: mobile_issue_case(base, get_json)),
        run_case("issue-version-assessment", "imported_issue", "Assess a bounded v19.1.8 profile", "Does the assessment help triage possible impact while still requiring local verification?", lambda: issue_assessment_case(base, post_json)),
        run_case("no-answer-boundary", "no_answer", "Search a deliberately unknown term", "Does the KB avoid inventing an answer when it has no matching evidence?", lambda: no_answer_case(base, get_json)),
    ]
    failures = [case for case in cases if case["status"] != "pass"]
    projection_version = next(
        (str(case.get("projection_version") or "") for case in cases if case.get("projection_version")),
        "",
    )
    return {
        "schema": TEST_ROUND_SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "service": base,
        "projection_version": projection_version,
        "status": "fail" if failures else "ok",
        "automatic_pass_count": len(cases) - len(failures),
        "automatic_fail_count": len(failures),
        "case_count": len(cases),
        "rock_idea_case_count": sum(1 for case in cases if case["category"] == "rock_idea"),
        "imported_issue_case_count": sum(1 for case in cases if case["category"] == "imported_issue"),
        "manual_review_required": True,
        "cases": cases,
        "next_steps": [
            "Run again with --review to record one bounded manual outcome for every case; add --submit with an external-test or maintainer cohort to aggregate it in the review dashboard.",
            "For a specific correct or incorrect search result, use rock-kb feedback with the exact result_id and a fixed reason.",
            "For a service, MCP, CLI, schema, authentication, or retrieval malfunction, use rock-kb report-issue with a redaction-attested generic description.",
            "Never include private Rock data, query logs, identifiers, secrets, screenshots, or internal URLs in feedback.",
        ],
    }


def build_test_round_review(report: Mapping[str, Any], outcomes: Mapping[str, str]) -> dict[str, Any]:
    if report.get("schema") != TEST_ROUND_SCHEMA:
        raise ValueError(f"Expected {TEST_ROUND_SCHEMA}")
    cases = report.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Test round cases are missing")
    expected = {case_id: category for case_id, category in CASE_DEFINITIONS}
    actual = {str(case.get("case_id") or ""): case for case in cases if isinstance(case, dict)}
    if set(actual) != set(expected):
        raise ValueError("Test round must contain every canonical case exactly once")
    if set(outcomes) != set(expected):
        raise ValueError("Review outcomes must cover every canonical case exactly once")

    review_cases = []
    for case_id, category in CASE_DEFINITIONS:
        case = actual[case_id]
        outcome = str(outcomes[case_id]).strip().lower()
        if outcome not in REVIEW_OUTCOMES:
            raise ValueError(f"Unsupported outcome for {case_id}: {outcome}")
        result_ids = [str(value) for value in case.get("result_ids") or [] if str(value)]
        review_cases.append(
            {
                "case_id": case_id,
                "category": category,
                "automatic_status": "pass" if case.get("status") == "pass" else "fail",
                "outcome": outcome,
                "result_id": result_ids[0] if result_ids and category != "no_answer" else None,
            }
        )
    return {
        "schema": TEST_ROUND_REVIEW_SCHEMA,
        "test_round_schema": TEST_ROUND_SCHEMA,
        "projection_version": str(report.get("projection_version") or ""),
        "automatic_status": "ok" if report.get("status") == "ok" else "fail",
        "cases": review_cases,
    }


def review_outcomes_from_payload(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("Review file must contain a JSON object")
    value = payload.get("outcomes", payload)
    if not isinstance(value, dict):
        raise ValueError("Review outcomes must be a JSON object keyed by case_id")
    return {str(case_id): str(outcome) for case_id, outcome in value.items()}


def run_case(case_id: str, category: str, operation: str, manual_prompt: str, execute: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    try:
        evidence = execute()
        passed = bool(evidence.pop("passed", False))
        return {
            "case_id": case_id,
            "category": category,
            "operation": operation,
            "status": "pass" if passed else "fail",
            "manual_review_prompt": manual_prompt,
            **evidence,
        }
    except Exception as exc:
        return {
            "case_id": case_id,
            "category": category,
            "operation": operation,
            "status": "fail",
            "manual_review_prompt": manual_prompt,
            "error_type": type(exc).__name__,
            "error": str(exc)[:300],
        }


def health_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    payload = get_json(f"{base}/health")
    version = str(payload.get("version") or "")
    return {
        "passed": payload.get("status") == "ok" and bool(version),
        "projection_version": version,
        "artifact_prefix": payload.get("artifact_prefix"),
    }


def model_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    payload = get_json(f"{base}/model-map/models/group?fields=identity%2Crequired%2Crelationships%2Cdiffs")
    model = payload.get("model") or {}
    identity = model.get("identity") or {}
    relationships = model.get("relationships") or []
    members = [row for row in relationships if row.get("property_name") == "Members"]
    return {
        "passed": payload.get("status") == "ok" and identity.get("model_slug") == "group" and bool(members),
        "result_ids": ["model_map:stable:group"],
        "model_slug": identity.get("model_slug"),
        "rock_version": identity.get("rock_version"),
        "members_relationship_found": bool(members),
    }


def lava_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    query = quote("Check-In Label Designer PersonAttendance Lava roots", safe="")
    payload = get_json(f"{base}/search?q={query}&limit=3&min_tier=source_backed&detail=compact")
    results = payload.get("results") or []
    result_ids = [str(row.get("id") or "") for row in results]
    return {
        "passed": bool(results) and results[0].get("kind") == "lava_context" and result_ids[0].startswith("lava_context:check-in-label"),
        "result_ids": result_ids,
        "top_kind": results[0].get("kind") if results else None,
        "top_authority_tier": results[0].get("authority_tier") if results else None,
    }


def recipe_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    recipe_id = "oneall:check-in-status-dashboard"
    payload = get_json(f"{base}/recipes/{quote(recipe_id, safe='')}")
    recipe = payload.get("recipe") or {}
    implementation = recipe.get("implementation") or {}
    commit_sha = str(implementation.get("commit_sha") or "")
    return {
        "passed": payload.get("status") == "ok" and recipe.get("authority_tier") == "community-reviewed" and len(commit_sha) == 40,
        "result_ids": [f"recipe:{recipe_id}"],
        "authority_tier": recipe.get("authority_tier"),
        "needs_live_verification": recipe.get("needs_live_verification"),
        "immutable_commit_present": len(commit_sha) == 40,
    }


def troubleshooting_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    query = quote("child eligible but not available at checkin", safe="")
    payload = get_json(f"{base}/search?q={query}&limit=5&min_tier=routing_context_only&detail=compact")
    results = payload.get("results") or []
    ranked = [row for row in results[:2] if "check-in" in (row.get("concepts") or [row.get("concept")])]
    return {
        "passed": bool(ranked),
        "result_ids": [str(row.get("id") or "") for row in results],
        "top_concepts": results[0].get("concepts") if results else [],
        "top_authority_tier": results[0].get("authority_tier") if results else None,
    }


def rock_idea_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    payload = get_json(f"{base}/rock-ideas/1307")
    idea = payload.get("idea") or {}
    relationships = payload.get("relationships") or []
    relationship_types = {str(row.get("relationship_type") or "") for row in relationships}
    targets = {str(row.get("target_id") or "") for row in relationships}
    forbidden_fields = {"description", "body", "response", "response_text", "comments", "author", "submitter", "organization"}
    return {
        "passed": (
            payload.get("status") == "ok"
            and idea.get("idea_id") == "rock_idea:1307"
            and idea.get("authority_tier") == "community-unreviewed"
            and idea.get("needs_live_verification") is True
            and not (forbidden_fields & set(idea))
            and {"about", "about_model", "references_issue"}.issubset(relationship_types)
            and "concept:communications" in targets
            and "model_map:stable:phone-number" in targets
            and "rock_issue:SparkDevNetwork/Rock#2935" in targets
            and not any(
                row.get("relationship_type") == "implemented_by_issue"
                for row in relationships
                if row.get("target_id") == "rock_issue:SparkDevNetwork/Rock#2935"
            )
        ),
        "result_ids": ["rock_idea:1307"],
        "authority_tier": idea.get("authority_tier"),
        "needs_live_verification": idea.get("needs_live_verification"),
        "verification_state": (idea.get("verification") or {}).get("verification_state"),
        "relationship_types": sorted(relationship_types),
        "relationship_targets": sorted(targets),
        "raw_content_republished": bool(forbidden_fields & set(idea)),
        "reference_presented_as_implementation": any(
            row.get("relationship_type") == "implemented_by_issue"
            for row in relationships
            if row.get("target_id") == "rock_issue:SparkDevNetwork/Rock#2935"
        ),
    }


def core_issue_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    payload = get_json(f"{base}/rock-issues/6920")
    issue = payload.get("issue") or {}
    enrichments = issue.get("reviewed_enrichments") or []
    source_backed = [row for row in enrichments if row.get("claim_tier") == "source_backed"]
    return {
        "passed": (
            payload.get("status") == "ok"
            and issue.get("authority_tier") == "community-unreviewed"
            and "body" not in issue
            and bool(source_backed)
        ),
        "result_ids": [str(payload.get("issue_id") or "")],
        "report_authority_tier": issue.get("authority_tier"),
        "raw_body_republished": "body" in issue,
        "reviewed_enrichment_count": len(enrichments),
        "source_backed_enrichment_count": len(source_backed),
    }


def mobile_issue_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    payload = get_json(f"{base}/rock-issues/{quote('mobile:116', safe='')}")
    issue = payload.get("issue") or {}
    fixed = [
        row
        for row in issue.get("version_evidence") or []
        if row.get("relationship") == "fixed" and row.get("authority_tier") == "official"
    ]
    return {
        "passed": payload.get("status") == "ok" and issue.get("state") == "closed" and bool(fixed),
        "result_ids": [str(payload.get("issue_id") or "")],
        "state": issue.get("state"),
        "evidence_state": issue.get("evidence_state"),
        "official_fixed_versions": [row.get("normalized_version") for row in fixed],
        "needs_live_verification": issue.get("needs_live_verification"),
    }


def issue_assessment_case(base: str, post_json: JsonPoster) -> dict[str, Any]:
    payload = post_json(
        f"{base}/rock-issues/assess",
        {"profile": {"core_version": "19.1.8", "concepts": ["connections", "workflows"]}, "limit": 100},
    )
    results = payload.get("results") or []
    match = next((row for row in results if row.get("issue_id") == "rock_issue:SparkDevNetwork/Rock#6920"), None)
    return {
        "passed": bool(match) and match.get("needs_live_verification") is True and bool(payload.get("caveat")),
        "result_ids": [str(match.get("issue_id"))] if match else [],
        "applicability": match.get("applicability") if match else None,
        "needs_live_verification": match.get("needs_live_verification") if match else None,
        "assessment_caveat_present": bool(payload.get("caveat")),
    }


def no_answer_case(base: str, get_json: JsonGetter) -> dict[str, Any]:
    query = quote("qzvwx9417 frobnication", safe="")
    payload = get_json(f"{base}/search?q={query}&limit=5&min_tier=routing_context_only&detail=compact")
    results = payload.get("results") or []
    return {"passed": len(results) == 0, "result_ids": [], "result_count": len(results)}
