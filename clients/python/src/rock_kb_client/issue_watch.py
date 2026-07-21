from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

ASSESSMENT_SCHEMA = "rock-kb-rock-issue-assessment-v2"
STATE_SCHEMA = "rock-kb-issue-watch-state-v2"
RESULT_SCHEMA = "rock-kb-issue-watch-result-v2"
ASSESSMENT_SCOPES = {"open", "historical-unresolved", "all-relevant"}
PROFILE_VALUE_PATTERN = re.compile(r"^[A-Za-z0-9._ -]+$")
MAX_RESULTS = 10_000
SNAPSHOT_FIELDS = (
    "issue_id",
    "title",
    "url",
    "state",
    "assessment_scope",
    "applicability",
    "reason",
    "remediation",
    "target_version",
    "fixed_release_lines",
    "fix_target_relations",
    "reviewed_assertion_ids",
    "revalidation_due_enrichment_ids",
    "decision",
    "requirement_evaluation",
    "risk",
    "live_verification",
)


def validate_profile(profile: dict) -> None:
    allowed = {"core_version", "mobile_shell_version", "platforms", "concepts", "capabilities", "configurations"}
    unsupported = sorted(set(profile) - allowed)
    if unsupported:
        raise ValueError(f"Unsupported instance profile fields: {', '.join(unsupported)}")
    if not profile.get("core_version") and not profile.get("mobile_shell_version"):
        raise ValueError("Instance profile requires core_version or mobile_shell_version")
    for key in ["platforms", "concepts", "capabilities", "configurations"]:
        values = profile.get(key)
        if values is None:
            continue
        if (
            not isinstance(values, list)
            or len(values) > 50
            or any(
                not isinstance(value, str)
                or not value
                or len(value) > 80
                or not PROFILE_VALUE_PATTERN.fullmatch(value)
                for value in values
            )
        ):
            raise ValueError(f"{key} must contain at most 50 bounded identifiers")
    if len(canonical_json(profile).encode("utf-8")) > 8192:
        raise ValueError("Instance profile exceeds 8192 bytes")


def profile_sha256(profile: dict) -> str:
    return hashlib.sha256(canonical_json(profile).encode("utf-8")).hexdigest()


def validate_scope(scope: str) -> None:
    if scope not in ASSESSMENT_SCOPES:
        raise ValueError("Issue watch scope must be open, historical-unresolved, or all-relevant")


def default_state_path(profile: dict, service: str, scope: str = "open") -> Path:
    configured = os.environ.get("ROCK_KB_STATE_DIR")
    if configured:
        root = Path(configured).expanduser()
    elif os.environ.get("XDG_STATE_HOME"):
        root = Path(os.environ["XDG_STATE_HOME"]).expanduser() / "rock-kb"
    else:
        root = Path.home() / ".local" / "state" / "rock-kb"
    validate_scope(scope)
    identity = canonical_json({"profile_sha256": profile_sha256(profile), "scope": scope, "service": service.rstrip("/")})
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    return root / f"issue-watch-{digest}.json"


def run_issue_watch(
    *,
    profile: dict,
    service: str,
    fetch_page: Callable[[dict], dict],
    scope: str = "open",
    state_path: Path | None = None,
    page_size: int = 500,
    reset: bool = False,
    write: bool = True,
) -> dict:
    validate_profile(profile)
    validate_scope(scope)
    if not 1 <= page_size <= 500:
        raise ValueError("Issue watch page size must be between 1 and 500")

    service = service.rstrip("/")
    profile_hash = profile_sha256(profile)
    state_path = (state_path or default_state_path(profile, service, scope)).expanduser()
    previous = None if reset else read_state(state_path)
    if previous:
        if previous.get("schema") != STATE_SCHEMA:
            raise ValueError(f"Unsupported issue watch state schema in {state_path}")
        if previous.get("profile_sha256") != profile_hash or previous.get("service") != service or previous.get("scope") != scope:
            raise ValueError("Issue watch state belongs to a different profile, scope, or service; use --reset or another --state path")

    assessment = collect_assessment_pages(profile, scope, page_size, fetch_page)
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    current_issues = {str(row["issue_id"]): snapshot_row(row) for row in assessment["results"]}
    previous_issues = previous.get("issues", {}) if previous else {}
    changes = compare_snapshots(previous_issues, current_issues, assessment["results"]) if previous else empty_changes()
    if previous:
        if previous.get("catalog") != assessment.get("catalog"):
            changes["catalog_changed"] = {
                "before": previous.get("catalog"),
                "after": assessment.get("catalog"),
            }
        if previous.get("exclusion_summary") != assessment.get("exclusion_summary"):
            changes["exclusion_summary_changed"] = {
                "before": previous.get("exclusion_summary"),
                "after": assessment.get("exclusion_summary"),
            }
        population_before = {
            "evaluated_count": previous.get("evaluated_count"),
            "population_by_state": previous.get("population_by_state"),
        }
        population_after = {
            "evaluated_count": assessment.get("evaluated_count"),
            "population_by_state": assessment.get("population_by_state"),
        }
        if population_before != population_after:
            changes["population_changed"] = {"before": population_before, "after": population_after}

    state = {
        "schema": STATE_SCHEMA,
        "profile_sha256": profile_hash,
        "service": service,
        "scope": scope,
        "projection_version": assessment.get("projection_version"),
        "catalog": assessment.get("catalog"),
        "exclusion_summary": assessment.get("exclusion_summary"),
        "evaluated_count": assessment.get("evaluated_count"),
        "population_by_state": assessment.get("population_by_state"),
        "observed_at": observed_at,
        "issue_count": len(current_issues),
        "issues": current_issues,
    }
    if write:
        write_state_atomic(state_path, state)

    if previous:
        status = "updated" if any(changes[key] for key in changes if key != "unchanged_count") else "unchanged"
    else:
        status = "reset" if reset and state_path.exists() else "initialized"
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "state_path": str(state_path),
        "snapshot_written": write,
        "profile_sha256": profile_hash,
        "service": service,
        "scope": scope,
        "projection_version": assessment.get("projection_version"),
        "catalog": assessment.get("catalog"),
        "exclusion_summary": assessment.get("exclusion_summary"),
        "evaluated_count": assessment.get("evaluated_count"),
        "population_by_state": assessment.get("population_by_state"),
        "observed_at": observed_at,
        "count": assessment["count"],
        "total_count": assessment["total_count"],
        "counts": assessment["counts"],
        "results": assessment["results"],
        "changes": changes,
    }


def collect_assessment_pages(profile: dict, scope: str, page_size: int, fetch_page: Callable[[dict], dict]) -> dict:
    offset = 0
    results: list[dict] = []
    seen_ids: set[str] = set()
    total_count: int | None = None
    counts: dict | None = None
    projection_version: str | None = None
    catalog: dict | None = None
    exclusion_summary: dict | None = None
    evaluated_count: int | None = None
    population_by_state: dict | None = None

    while True:
        page = fetch_page({"profile": profile, "scope": scope, "limit": page_size, "offset": offset})
        if not isinstance(page, dict) or page.get("schema") != ASSESSMENT_SCHEMA:
            raise RuntimeError("Issue assessment service does not support scoped Issue Watch V2 responses")
        required = {
            "count",
            "total_count",
            "evaluated_count",
            "population_by_state",
            "offset",
            "limit",
            "next_offset",
            "has_more",
            "results",
            "counts",
            "exclusion_summary",
            "catalog",
        }
        if not required.issubset(page):
            raise RuntimeError("Issue assessment service does not support complete pagination")
        page_results = page.get("results")
        if not isinstance(page_results, list) or any(not isinstance(row, dict) for row in page_results):
            raise RuntimeError("Issue assessment returned invalid results")
        if page.get("offset") != offset or page.get("count") != len(page_results):
            raise RuntimeError("Issue assessment pagination metadata is inconsistent")
        if page.get("scope") != scope:
            raise RuntimeError("Issue assessment returned a different scope")
        page_total = page.get("total_count")
        if not isinstance(page_total, int) or page_total < 0 or page_total > MAX_RESULTS:
            raise RuntimeError("Issue assessment total is outside the supported safety bound")
        if total_count is None:
            total_count = page_total
            counts = page.get("counts") if isinstance(page.get("counts"), dict) else {}
            projection_version = str(page.get("projection_version") or "") or None
            catalog = page.get("catalog") if isinstance(page.get("catalog"), dict) else {}
            exclusion_summary = page.get("exclusion_summary") if isinstance(page.get("exclusion_summary"), dict) else {}
            evaluated_count = page.get("evaluated_count") if isinstance(page.get("evaluated_count"), int) else None
            population_by_state = page.get("population_by_state") if isinstance(page.get("population_by_state"), dict) else {}
        elif page_total != total_count or page.get("counts") != counts:
            raise RuntimeError("Issue assessment changed while pages were being collected")
        elif (str(page.get("projection_version") or "") or None) != projection_version:
            raise RuntimeError("Issue assessment projection changed while pages were being collected")
        elif page.get("catalog") != catalog:
            raise RuntimeError("Issue assessment catalog freshness changed while pages were being collected")
        elif page.get("exclusion_summary") != exclusion_summary:
            raise RuntimeError("Issue assessment exclusions changed while pages were being collected")
        elif page.get("evaluated_count") != evaluated_count or page.get("population_by_state") != population_by_state:
            raise RuntimeError("Issue assessment population changed while pages were being collected")

        for row in page_results:
            issue_id = str(row.get("issue_id") or "")
            if not issue_id or issue_id in seen_ids:
                raise RuntimeError("Issue assessment returned a missing or duplicate issue ID")
            seen_ids.add(issue_id)
            results.append(row)

        has_more = page.get("has_more") is True
        if not has_more:
            if page.get("next_offset") is not None or len(results) != total_count:
                raise RuntimeError("Issue assessment ended before the complete result set was collected")
            break
        next_offset = page.get("next_offset")
        if not isinstance(next_offset, int) or next_offset <= offset or next_offset != offset + len(page_results):
            raise RuntimeError("Issue assessment returned an invalid next offset")
        offset = next_offset

    return {
        "schema": ASSESSMENT_SCHEMA,
        "scope": scope,
        "projection_version": projection_version,
        "catalog": catalog or {},
        "exclusion_summary": exclusion_summary or {},
        "evaluated_count": evaluated_count or 0,
        "population_by_state": population_by_state or {},
        "count": len(results),
        "total_count": total_count or 0,
        "counts": counts or {},
        "results": results,
    }


def compare_snapshots(previous: dict, current: dict, current_results: list[dict]) -> dict:
    result_by_id = {str(row["issue_id"]): row for row in current_results}
    previous_ids = set(previous)
    current_ids = set(current)
    changes = empty_changes()
    changes["newly_relevant"] = [result_by_id[issue_id] for issue_id in sorted(current_ids - previous_ids)]
    changes["no_longer_relevant"] = [previous[issue_id] for issue_id in sorted(previous_ids - current_ids)]

    changed_ids: set[str] = set()
    for issue_id in sorted(previous_ids & current_ids):
        before = previous[issue_id]
        after = current[issue_id]
        if before.get("applicability") != after.get("applicability"):
            changes["applicability_changed"].append(
                {"issue_id": issue_id, "before": before.get("applicability"), "after": after.get("applicability"), "current": result_by_id[issue_id]}
            )
            changed_ids.add(issue_id)
        remediation_fields = ("remediation", "fixed_release_lines", "fix_target_relations", "reviewed_assertion_ids")
        if any(before.get(field) != after.get(field) for field in remediation_fields):
            changes["remediation_changed"].append(
                {"issue_id": issue_id, "before": {field: before.get(field) for field in remediation_fields}, "after": {field: after.get(field) for field in remediation_fields}, "current": result_by_id[issue_id]}
            )
            changed_ids.add(issue_id)
        if before.get("risk") != after.get("risk"):
            changes["risk_changed"].append(
                {"issue_id": issue_id, "before": before.get("risk"), "after": after.get("risk"), "current": result_by_id[issue_id]}
            )
            changed_ids.add(issue_id)
        routing_fields = ("reason", "decision", "requirement_evaluation", "live_verification")
        if any(before.get(field) != after.get(field) for field in routing_fields):
            changes["routing_changed"].append(
                {"issue_id": issue_id, "before": {field: before.get(field) for field in routing_fields}, "after": {field: after.get(field) for field in routing_fields}, "current": result_by_id[issue_id]}
            )
            changed_ids.add(issue_id)
        due = after.get("revalidation_due_enrichment_ids") or []
        if due and due != (before.get("revalidation_due_enrichment_ids") or []):
            changes["revalidation_due"].append(result_by_id[issue_id])
            changed_ids.add(issue_id)
    changes["unchanged_count"] = len((previous_ids & current_ids) - changed_ids)
    return changes


def empty_changes() -> dict:
    return {
        "newly_relevant": [],
        "applicability_changed": [],
        "remediation_changed": [],
        "risk_changed": [],
        "routing_changed": [],
        "catalog_changed": None,
        "exclusion_summary_changed": None,
        "population_changed": None,
        "no_longer_relevant": [],
        "revalidation_due": [],
        "unchanged_count": 0,
    }


def snapshot_row(row: dict) -> dict:
    return {field: row.get(field) for field in SNAPSHOT_FIELDS}


def read_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Issue watch state must contain a JSON object: {path}")
    return payload


def write_state_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        path.chmod(0o600)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def canonical_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
