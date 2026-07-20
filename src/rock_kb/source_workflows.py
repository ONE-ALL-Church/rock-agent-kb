from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import yaml

from .paths import REPO_ROOT
from .sources import ALLOWED_REFRESH_CADENCES, Source, load_sources


POLICY_PATH = REPO_ROOT / "sources" / "freshness-policy.yaml"
POLICY_SCHEMA = "rock-kb-source-freshness-policy-v1"


def load_source_freshness_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict) or value.get("schema") != POLICY_SCHEMA:
        raise ValueError("Unsupported source freshness policy schema.")
    return value


def source_workflow_policies(
    *,
    policy: dict[str, Any] | None = None,
    sources: Iterable[Source] | None = None,
) -> dict[str, dict[str, Any]]:
    policy = policy if policy is not None else load_source_freshness_policy()
    source_rows = list(sources) if sources is not None else load_sources()
    raw_workflows = policy.get("workflows")
    if not isinstance(raw_workflows, dict) or not raw_workflows:
        raise ValueError("Source freshness policy must define workflow ownership.")

    resolved: dict[str, dict[str, Any]] = {}
    owners: dict[str, list[str]] = {source.id: [] for source in source_rows}
    errors: list[str] = []
    for workflow_id, raw_config in raw_workflows.items():
        workflow_id = str(workflow_id)
        if not workflow_id or not all(character.isalnum() or character in "_-" for character in workflow_id):
            errors.append(f"invalid workflow id: {workflow_id or '<empty>'}")
            continue
        if not isinstance(raw_config, dict):
            errors.append(f"{workflow_id} must be a mapping")
            continue

        try:
            maximum_age_hours = float(raw_config.get("maximum_age_hours"))
        except (TypeError, ValueError):
            errors.append(f"{workflow_id} maximum_age_hours must be a positive number")
            continue
        if maximum_age_hours <= 0:
            errors.append(f"{workflow_id} maximum_age_hours must be a positive number")
            continue

        try:
            cadences = string_set(raw_config.get("cadences"))
            include_kinds = string_set(raw_config.get("include_kinds"))
            exclude_kinds = string_set(raw_config.get("exclude_kinds"))
        except ValueError as error:
            errors.append(f"{workflow_id} {error}")
            continue
        if not cadences:
            errors.append(f"{workflow_id} must select at least one cadence")
            continue
        unknown_cadences = cadences - ALLOWED_REFRESH_CADENCES
        if unknown_cadences:
            errors.append(f"{workflow_id} has unknown cadences: {', '.join(sorted(unknown_cadences))}")
            continue
        if include_kinds & exclude_kinds:
            errors.append(f"{workflow_id} includes and excludes the same source kind")
            continue

        source_ids = sorted(
            source.id
            for source in source_rows
            if source.refresh_cadence in cadences
            and (not include_kinds or source.kind in include_kinds)
            and source.kind not in exclude_kinds
        )
        if not source_ids:
            errors.append(f"{workflow_id} does not own any registered sources")
            continue
        for source_id in source_ids:
            owners[source_id].append(workflow_id)
        resolved[workflow_id] = {
            "workflow_id": workflow_id,
            "maximum_age_hours": maximum_age_hours,
            "source_ids": source_ids,
        }

    for source_id, workflow_ids in sorted(owners.items()):
        if not workflow_ids:
            errors.append(f"{source_id} has no owning workflow")
        elif len(workflow_ids) > 1:
            errors.append(f"{source_id} has multiple owning workflows: {', '.join(sorted(workflow_ids))}")
    if errors:
        raise ValueError("Invalid source workflow policy: " + "; ".join(errors))
    return dict(sorted(resolved.items()))


def source_workflow_policy(
    workflow_id: str,
    *,
    policy: dict[str, Any] | None = None,
    sources: Iterable[Source] | None = None,
) -> dict[str, Any]:
    workflows = source_workflow_policies(policy=policy, sources=sources)
    try:
        return workflows[workflow_id]
    except KeyError as error:
        raise ValueError(f"Unknown source workflow: {workflow_id}") from error


def string_set(value: Any) -> set[str]:
    if value is None:
        return set()
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError("Source workflow selectors must be lists of non-empty strings.")
    return {str(item) for item in value}
