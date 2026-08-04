from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from .extract import USER_AGENT, now_iso
from .paths import REPO_ROOT


SOURCE_NATIVE_PROMOTION_POLICY_PATH = (
    REPO_ROOT / "canonical" / "source-native" / "promotion-policy-v1.json"
)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"required JSON input does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object at {path}")
    return value


def fetch_operations_dashboard(url: str) -> dict[str, Any]:
    with httpx.Client(
        follow_redirects=True,
        timeout=30,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        value = response.json()
    if not isinstance(value, dict):
        raise ValueError("operations dashboard did not return a JSON object")
    return value


def evaluate_source_native_promotion_readiness(
    *,
    manifest: dict[str, Any],
    verification_report: dict[str, Any],
    retrieval_report: dict[str, Any],
    dashboard: dict[str, Any],
    policy: dict[str, Any],
    evaluated_at: str | None = None,
) -> dict[str, Any]:
    if policy.get("schema") != "rock-kb-source-native-promotion-policy-v1":
        raise ValueError("unsupported source-native promotion policy")
    technical_policy = dict(policy.get("technical_evidence") or {})
    external_policy = dict(policy.get("external_evidence") or {})
    authorization_policy = dict(policy.get("cutover_authorization") or {})
    retrieval_summary = dict(retrieval_report.get("summary") or {})
    retrieval_gate = dict(retrieval_report.get("promotion_gate") or {})

    technical_checks = {
        "source_family_count": (
            len(manifest.get("source_family_counts") or {})
            >= int(technical_policy["min_source_family_count"])
        ),
        "article_count": (
            int(manifest.get("article_count") or 0)
            >= int(technical_policy["min_article_count"])
        ),
        "verification_blockers": (
            int(
                verification_report.get(
                    "default_cutover_blocker_count",
                    verification_report.get("unresolved_count") or 0,
                )
                or 0
            )
            <= int(
                technical_policy[
                    "max_default_cutover_verification_blockers"
                ]
            )
        ),
        "verification_live_check": (
            not technical_policy.get("require_live_verification_report")
            or verification_report.get("live_check_performed") is True
        ),
        "retrieval_shadow": (
            not technical_policy.get("require_retrieval_shadow_pass")
            or retrieval_gate.get("passed") is True
        ),
        "retrieval_regressions": (
            int(retrieval_summary.get("regressed") or 0)
            <= int(technical_policy["max_retrieval_regressions"])
        ),
        "exact_lookup_regressions": (
            int(retrieval_summary.get("exact_lookup_regressions") or 0)
            <= int(technical_policy["max_exact_lookup_regressions"])
        ),
        "authority_regressions": (
            int(retrieval_summary.get("authority_regressions") or 0)
            <= int(technical_policy["max_authority_regressions"])
        ),
        "no_answer_regressions": (
            int(retrieval_summary.get("no_answer_regressions") or 0)
            <= int(technical_policy["max_no_answer_regressions"])
        ),
        "endpoint_compatibility_regressions": (
            int(
                retrieval_summary.get(
                    "endpoint_compatibility_regressions"
                )
                or 0
            )
            <= int(
                technical_policy[
                    "max_endpoint_compatibility_regressions"
                ]
            )
        ),
    }

    comparisons = dict(dashboard.get("retrieval_comparisons") or {})
    preferences = dict(comparisons.get("by_preference") or {})
    categories = dict(comparisons.get("by_category") or {})
    decision_metrics = dict(comparisons.get("decision_metrics") or {})
    canonical_better = int(preferences.get("canonical_better") or 0)
    legacy_better = int(preferences.get("legacy_better") or 0)
    decisive_count = int(decision_metrics.get("decisive_count") or 0)
    opted_in_installations = int(
        comparisons.get("opted_in_installation_count") or 0
    )
    required_categories = set(external_policy.get("required_categories") or [])
    observed_categories = {
        str(category)
        for category, count in categories.items()
        if int(count or 0) > 0
    }
    preference_ratio = (
        float("inf")
        if canonical_better and not legacy_better
        else canonical_better / max(1, legacy_better)
    )
    external_checks = {
        "opted_in_installations": (
            opted_in_installations
            >= int(external_policy["min_opted_in_installations"])
        ),
        "decisive_comparisons": (
            decisive_count
            >= int(external_policy["min_decisive_comparisons"])
        ),
        "category_coverage": required_categories <= observed_categories,
        "canonical_preference_ratio": (
            preference_ratio
            >= float(
                external_policy[
                    "canonical_to_legacy_preference_ratio_min"
                ]
            )
        ),
    }
    technical_passed = all(technical_checks.values())
    external_passed = all(external_checks.values())
    external_required = bool(
        external_policy.get("required_for_default_cutover", True)
    )
    external_gate_satisfied = external_passed or not external_required
    ready_for_default_cutover = technical_passed and external_gate_satisfied
    maintainer_authorized = (
        authorization_policy.get("status") == "approved"
        and authorization_policy.get("requires_legacy_rollback") is True
    )
    production_change_authorized = (
        ready_for_default_cutover and maintainer_authorized
    )
    return {
        "schema": "rock-kb-source-native-promotion-readiness-v1",
        "policy_id": policy["policy_id"],
        "evaluated_at": evaluated_at or now_iso(),
        "technical_evidence": {
            "passed": technical_passed,
            "checks": technical_checks,
            "source_family_count": len(
                manifest.get("source_family_counts") or {}
            ),
            "article_count": int(manifest.get("article_count") or 0),
            "verification_blocker_count": int(
                verification_report.get(
                    "default_cutover_blocker_count",
                    verification_report.get("unresolved_count") or 0,
                )
                or 0
            ),
            "retrieval_summary": retrieval_summary,
        },
        "external_evidence": {
            "passed": external_passed,
            "required_for_default_cutover": external_required,
            "gate_satisfied": external_gate_satisfied,
            "checks": external_checks,
            "opted_in_installation_count": opted_in_installations,
            "decisive_comparison_count": decisive_count,
            "canonical_better_count": canonical_better,
            "legacy_better_count": legacy_better,
            "canonical_to_legacy_preference_ratio": (
                None if preference_ratio == float("inf") else preference_ratio
            ),
            "observed_categories": sorted(observed_categories),
            "missing_categories": sorted(
                required_categories - observed_categories
            ),
        },
        "cutover_authorization": {
            "status": authorization_policy.get("status", "not_recorded"),
            "mode": authorization_policy.get("mode", "separate_review"),
            "approved_at": authorization_policy.get("approved_at"),
            "requires_legacy_rollback": authorization_policy.get(
                "requires_legacy_rollback", False
            ),
            "passed": maintainer_authorized,
        },
        "ready_for_default_cutover": ready_for_default_cutover,
        "production_change_authorized": production_change_authorized,
        "decision": (
            "maintainer_approved_reversible_cutover"
            if production_change_authorized
            else (
                "eligible_for_separate_review"
                if ready_for_default_cutover
                else "remain_opt_in_canary"
            )
        ),
        "notes": [
            (
                "Independent external evidence is a required pre-cutover gate."
                if external_required
                else "Independent external evidence remains an advisory post-cutover validation signal."
            ),
            "Passing this report never changes the default reader; a separate reviewed release is required.",
        ],
    }
