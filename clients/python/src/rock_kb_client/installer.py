from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

import yaml

from .telemetry import telemetry_headers, telemetry_state_path


SKILL_ARTIFACT = "skills/rock-kb-agent/SKILL.md"
SKILL_MANIFEST_ENDPOINT = "skill/manifest.json"
SKILL_STATE_SCHEMA = "rock-kb-skill-state-v1"
SKILL_MANIFEST_SCHEMA = "rock-kb-skill-manifest-v1"
SKILL_CHECK_INTERVAL_HOURS = 24
SKILL_ERROR_RETRY_HOURS = 1
SKILL_POLICIES = ("notify", "auto", "pinned")
SUPPORTED_AGENTS = ("codex", "claude", "cursor", "opencode")


@dataclass(frozen=True)
class AgentPaths:
    config: Path
    skill: Path
    format: str
    server_key: str


@dataclass(frozen=True)
class InstallPlan:
    agent: str
    paths: AgentPaths
    updated_config: str
    config_changed: bool
    config_update_reasons: tuple[str, ...]
    skill_changed: bool


@dataclass(frozen=True)
class SkillRelease:
    manifest: dict
    source_text: str
    installed_text: str
    source_sha256: str


def detect_agents(home: Path | None = None) -> list[str]:
    home = (home or Path.home()).expanduser()
    markers = {
        "codex": [home / ".codex", shutil.which("codex")],
        "claude": [home / ".claude", home / ".claude.json", shutil.which("claude")],
        "cursor": [home / ".cursor", shutil.which("cursor")],
        "opencode": [home / ".config" / "opencode", shutil.which("opencode")],
    }
    return [name for name in SUPPORTED_AGENTS if any(marker and Path(marker).exists() for marker in markers[name])]


def selected_agents(values: list[str] | None, home: Path | None = None) -> list[str]:
    requested = values or []
    if "all" in requested:
        return list(SUPPORTED_AGENTS)
    if requested:
        return list(dict.fromkeys(requested))
    return detect_agents(home)


def agent_paths(agent: str, scope: str, home: Path, project_dir: Path) -> AgentPaths:
    if scope == "project":
        paths = {
            "codex": AgentPaths(project_dir / ".codex" / "config.toml", project_dir / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md", "toml", "mcp_servers"),
            "claude": AgentPaths(project_dir / ".mcp.json", project_dir / ".claude" / "skills" / "rock-kb-agent" / "SKILL.md", "json", "mcpServers"),
            "cursor": AgentPaths(project_dir / ".cursor" / "mcp.json", project_dir / ".cursor" / "skills" / "rock-kb-agent" / "SKILL.md", "json", "mcpServers"),
            "opencode": AgentPaths(project_dir / "opencode.json", project_dir / ".opencode" / "skills" / "rock-kb-agent" / "SKILL.md", "opencode", "mcp"),
        }
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")) if home == Path.home() else home / ".codex"
        xdg_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config")) if home == Path.home() else home / ".config"
        paths = {
            "codex": AgentPaths(codex_home / "config.toml", codex_home / "skills" / "rock-kb-agent" / "SKILL.md", "toml", "mcp_servers"),
            "claude": AgentPaths(home / ".claude.json", home / ".claude" / "skills" / "rock-kb-agent" / "SKILL.md", "json", "mcpServers"),
            "cursor": AgentPaths(home / ".cursor" / "mcp.json", home / ".cursor" / "skills" / "rock-kb-agent" / "SKILL.md", "json", "mcpServers"),
            "opencode": AgentPaths(xdg_home / "opencode" / "opencode.json", xdg_home / "opencode" / "skills" / "rock-kb-agent" / "SKILL.md", "opencode", "mcp"),
        }
    return paths[agent]


def install_agents(
    *,
    base_url: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
    dry_run: bool,
    verify: bool,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str = "dev",
) -> dict:
    report = sync_agents(
        operation="install",
        base_url=base_url,
        agents=agents,
        scope=scope,
        home=home,
        project_dir=project_dir,
        dry_run=dry_run,
        verify=verify,
        fetch_text=fetch_text,
        fetch_json=fetch_json,
        client_version=client_version,
        allow_config_only=True,
    )
    report["schema"] = "rock-kb-agent-install-v1"
    return report


def update_agents(
    *,
    base_url: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
    verify: bool,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str = "dev",
    unpin: bool = False,
) -> dict:
    state_path = skill_state_path(base_url, scope, home, project_dir)
    state = read_skill_state(state_path)
    if state.get("policy") == "pinned" and not unpin:
        report = check_agents(
            base_url=base_url,
            agents=agents,
            scope=scope,
            home=home,
            project_dir=project_dir,
            verify=verify,
            fetch_text=fetch_text,
            fetch_json=fetch_json,
            client_version=client_version,
        )
        if not report.get("skill_update_available"):
            return report
        report["status"] = "pinned"
        report["next"] = "Run rock-kb skill update --unpin to clear the pin and install the current reviewed skill."
        return report
    if unpin and state:
        state["policy"] = "notify"
        state.pop("pinned_skill_version", None)
        state.pop("pinned_source_sha256", None)
        write_skill_state(state_path, state)
    return sync_agents(
        operation="update",
        base_url=base_url,
        agents=agents,
        scope=scope,
        home=home,
        project_dir=project_dir,
        dry_run=False,
        verify=verify,
        fetch_text=fetch_text,
        fetch_json=fetch_json,
        client_version=client_version,
        allow_config_only=False,
    )


def sync_agents(
    *,
    operation: str,
    base_url: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
    dry_run: bool,
    verify: bool,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str,
    allow_config_only: bool,
) -> dict:
    if not agents:
        return {
            "schema": "rock-kb-skill-sync-v1",
            "operation": operation,
            "status": "no_agents_detected",
            "supported_agents": list(SUPPORTED_AGENTS),
            "next": "Re-run with --agent codex, --agent claude, --agent cursor, --agent opencode, or --agent all.",
        }

    base_url = base_url.rstrip("/")
    health = fetch_json(f"{base_url}/health") if verify else {"status": "skipped"}
    if verify and (not isinstance(health, dict) or health.get("status") != "ok"):
        raise RuntimeError("Hosted Rock KB health check did not return status=ok")
    release = fetch_skill_release(base_url, fetch_text, fetch_json, client_version)
    plans = plan_agent_sync(base_url, agents, scope, home, project_dir, release.installed_text)
    skill_update_available = any(plan.skill_changed for plan in plans)
    config_update_available = any(plan.config_changed for plan in plans)
    config_only_deferred = bool(config_update_available and not skill_update_available and not allow_config_only)

    reports = []
    any_changed = False
    installed_file_sha256: dict[str, str] = {}
    for plan in plans:
        paths = plan.paths
        backups: list[str] = []
        apply_config = bool(plan.config_changed and not config_only_deferred)
        any_changed = any_changed or apply_config or plan.skill_changed

        if not dry_run:
            if apply_config:
                backup = backup_file(paths.config)
                if backup:
                    backups.append(str(backup))
                paths.config.parent.mkdir(parents=True, exist_ok=True)
                paths.config.write_text(plan.updated_config, encoding="utf-8")
            if plan.skill_changed:
                backup = backup_file(paths.skill)
                if backup:
                    backups.append(str(backup))
                paths.skill.parent.mkdir(parents=True, exist_ok=True)
                paths.skill.write_text(release.installed_text, encoding="utf-8")
            if paths.skill.exists():
                installed_file_sha256[plan.agent] = sha256_text(paths.skill.read_text(encoding="utf-8"))
            current_config = paths.config.read_text(encoding="utf-8") if paths.config.exists() else ""
            request_headers = telemetry_headers(telemetry_state_path(home)) if scope == "user" else {}
            remaining_config_reasons = config_update_reasons(
                current_config,
                paths.format,
                paths.server_key,
                f"{base_url}/mcp",
                request_headers,
            )
            skill_current = paths.skill.exists() and paths.skill.read_text(encoding="utf-8") == release.installed_text
            if apply_config and remaining_config_reasons:
                raise RuntimeError(f"Rock KB {plan.agent} MCP configuration did not match after installation")
            if plan.skill_changed and not skill_current:
                raise RuntimeError(f"Rock KB {plan.agent} skill did not match after installation")
        else:
            remaining_config_reasons = plan.config_update_reasons
            skill_current = not plan.skill_changed

        reports.append(
            {
                "agent": plan.agent,
                "config_path": str(paths.config),
                "skill_path": str(paths.skill),
                "config_action": (
                    "would_update"
                    if dry_run and plan.config_changed
                    else "deferred_to_install_agent"
                    if config_only_deferred and plan.config_changed
                    else "updated"
                    if apply_config
                    else "unchanged"
                ),
                "config_status": "update_available" if remaining_config_reasons else "current",
                "config_update_reasons": list(remaining_config_reasons),
                "skill_action": "would_update" if dry_run and plan.skill_changed else "updated" if plan.skill_changed else "unchanged",
                "skill_status": "current" if skill_current else "update_available",
                "backups": backups,
            }
        )

    state_path = skill_state_path(base_url, scope, home, project_dir)
    state = read_skill_state(state_path)
    policy = str(state.get("policy") or release.manifest.get("default_update_policy") or "notify")
    if policy not in SKILL_POLICIES or (scope == "project" and policy == "auto"):
        policy = "notify"
    if not dry_run:
        now = utc_now()
        state = {
            **state,
            "schema": SKILL_STATE_SCHEMA,
            "service": base_url,
            "scope": scope,
            "project_dir": str(project_dir) if scope == "project" else None,
            "policy": policy,
            "agents": sorted(set(state.get("agents") or []) | set(agents)),
            "last_checked_at": now,
            "last_attempted_at": now,
            "last_status": "agent_config_update_available" if config_only_deferred else "updated" if any_changed else "current",
            "remote_manifest": release.manifest,
            "installed_skill_version": release.manifest["skill_version"],
            "installed_source_sha256": release.source_sha256,
            "installed_file_sha256": {**(state.get("installed_file_sha256") or {}), **installed_file_sha256},
        }
        if any_changed:
            state["last_updated_at"] = now
        state.pop("last_error", None)
        write_skill_state(state_path, state)

    status = "dry_run" if dry_run else "agent_config_update_available" if config_only_deferred else "ok"
    return {
        "schema": "rock-kb-skill-sync-v1",
        "operation": operation,
        "status": status,
        "scope": scope,
        "policy": policy,
        "service_health": health,
        "skill_manifest": public_skill_manifest(release.manifest),
        "state_path": str(state_path),
        "state_written": not dry_run,
        "agents": reports,
        "skill_update_available": bool(dry_run and skill_update_available),
        "agent_config_update_available": bool((dry_run and config_update_available) or config_only_deferred),
        "applied_components": [
            name
            for name, changed in (("skill", skill_update_available), ("agent_config", config_update_available and not config_only_deferred))
            if changed and not dry_run
        ],
        "restart_required": bool(not dry_run and any_changed and release.manifest.get("restart_required", True)),
        "review_required": bool(scope == "project" and any_changed),
        "recommended_action": recommended_action(status, policy),
        "recommended_command": recommended_command(status),
    }


def plan_agent_sync(
    base_url: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
    skill_text: str,
) -> list[InstallPlan]:
    plans: list[InstallPlan] = []
    request_headers = telemetry_headers(telemetry_state_path(home)) if scope == "user" else {}
    for agent in agents:
        paths = agent_paths(agent, scope, home, project_dir)
        config_text = paths.config.read_text(encoding="utf-8") if paths.config.exists() else ""
        updated_config = update_config(config_text, paths.format, paths.server_key, f"{base_url}/mcp", request_headers)
        local_skill = paths.skill.read_text(encoding="utf-8") if paths.skill.exists() else ""
        plans.append(
            InstallPlan(
                agent,
                paths,
                updated_config,
                updated_config != config_text,
                config_update_reasons(config_text, paths.format, paths.server_key, f"{base_url}/mcp", request_headers),
                local_skill != skill_text,
            )
        )
    return plans


def check_agents(
    *,
    base_url: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
    verify: bool,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str = "dev",
    if_due: bool = False,
) -> dict:
    base_url = base_url.rstrip("/")
    state_path = skill_state_path(base_url, scope, home, project_dir)
    state = read_skill_state(state_path)
    agents = effective_agents(agents, state)
    if if_due and not skill_check_due(state):
        report = skill_status(base_url=base_url, agents=agents, scope=scope, home=home, project_dir=project_dir)
        report.update(
            {
                "schema": "rock-kb-skill-check-v1",
                "operation": "check",
                "cached_status": report.get("status"),
                "status": "not_due",
                "state_written": False,
                "skill_update_available": False,
                "agent_config_update_available": False,
                "recommended_action": "none",
                "recommended_command": None,
            }
        )
        return report
    if not agents:
        return {
            "schema": "rock-kb-skill-check-v1",
            "operation": "check",
            "status": "no_agents_detected",
            "scope": scope,
            "state_path": str(state_path),
            "state_written": False,
            "supported_agents": list(SUPPORTED_AGENTS),
        }

    health = fetch_json(f"{base_url}/health") if verify else {"status": "skipped"}
    if verify and (not isinstance(health, dict) or health.get("status") != "ok"):
        raise RuntimeError("Hosted Rock KB health check did not return status=ok")
    release = fetch_skill_release(base_url, fetch_text, fetch_json, client_version)
    plans = plan_agent_sync(base_url, agents, scope, home, project_dir, release.installed_text)
    reports = [
        {
            "agent": plan.agent,
            "config_path": str(plan.paths.config),
            "skill_path": str(plan.paths.skill),
            "config_action": "would_update" if plan.config_changed else "unchanged",
            "config_status": "update_available" if plan.config_changed else "current",
            "config_update_reasons": list(plan.config_update_reasons),
            "skill_action": "would_update" if plan.skill_changed else "unchanged",
            "skill_status": "update_available" if plan.skill_changed else "current",
        }
        for plan in plans
    ]
    skill_update_available = any(plan.skill_changed for plan in plans)
    config_update_available = any(plan.config_changed for plan in plans)
    policy = str(state.get("policy") or release.manifest.get("default_update_policy") or "notify")
    if policy not in SKILL_POLICIES or (scope == "project" and policy == "auto"):
        policy = "notify"
    status = lifecycle_status(skill_update_available, config_update_available, policy)

    now = utc_now()
    installed_hashes = dict(state.get("installed_file_sha256") or {})
    for plan in plans:
        if not plan.skill_changed and plan.paths.skill.exists():
            installed_hashes[plan.agent] = sha256_text(plan.paths.skill.read_text(encoding="utf-8"))
    state = {
        **state,
        "schema": SKILL_STATE_SCHEMA,
        "service": base_url,
        "scope": scope,
        "project_dir": str(project_dir) if scope == "project" else None,
        "policy": policy,
        "agents": sorted(set(state.get("agents") or []) | set(agents)),
        "last_checked_at": now,
        "last_attempted_at": now,
        "last_status": status,
        "remote_manifest": release.manifest,
        "installed_file_sha256": installed_hashes,
    }
    state.pop("last_error", None)
    write_skill_state(state_path, state)
    return {
        "schema": "rock-kb-skill-check-v1",
        "operation": "check",
        "status": status,
        "scope": scope,
        "policy": policy,
        "service_health": health,
        "skill_manifest": public_skill_manifest(release.manifest),
        "state_path": str(state_path),
        "state_written": True,
        "checked_at": now,
        "agents": reports,
        "skill_update_available": skill_update_available,
        "agent_config_update_available": config_update_available,
        "restart_required": False,
        "recommended_action": recommended_action(status, policy),
        "recommended_command": recommended_command(status),
    }


def skill_status(*, base_url: str, agents: list[str], scope: str, home: Path, project_dir: Path) -> dict:
    base_url = base_url.rstrip("/")
    state_path = skill_state_path(base_url, scope, home, project_dir)
    state = read_skill_state(state_path)
    agents = effective_agents(agents, state)
    reports = [local_agent_status(base_url, agent, scope, home, project_dir, state) for agent in agents]
    statuses = {str(report["status"]) for report in reports}
    policy = "notify" if scope == "project" and state.get("policy") == "auto" else str(state.get("policy") or "notify")
    skill_update_available = any(report.get("skill_status") == "update_available" for report in reports)
    config_update_available = any(report.get("config_status") == "update_available" for report in reports)
    if "locally_modified" in statuses:
        status = "locally_modified"
    elif "invalid_configuration" in statuses:
        status = "invalid_configuration"
    elif skill_update_available or config_update_available:
        status = lifecycle_status(skill_update_available, config_update_available, policy)
    elif reports and statuses == {"current"}:
        status = "current"
    elif reports and statuses == {"not_installed"}:
        status = "not_installed"
    else:
        status = "unknown" if reports else "no_agents_detected"
    return {
        "schema": "rock-kb-skill-status-v1",
        "operation": "status",
        "status": status,
        "service": base_url,
        "scope": scope,
        "policy": policy,
        "state_path": str(state_path),
        "state_exists": state_path.exists(),
        "last_checked_at": state.get("last_checked_at"),
        "last_updated_at": state.get("last_updated_at"),
        "check_due": skill_check_due(state),
        "remote_manifest": public_skill_manifest(state.get("remote_manifest") or {}),
        "agents": reports,
        "skill_update_available": skill_update_available,
        "agent_config_update_available": config_update_available,
        "recommended_action": recommended_action(status, policy),
        "recommended_command": recommended_command(status),
    }


def set_skill_policy(
    *,
    base_url: str,
    policy: str,
    agents: list[str],
    scope: str,
    home: Path,
    project_dir: Path,
) -> dict:
    if policy not in SKILL_POLICIES:
        raise ValueError(f"Skill policy must be one of: {', '.join(SKILL_POLICIES)}")
    if policy == "auto" and scope == "project":
        raise ValueError("Project-scoped skills cannot use auto policy; use notify and review the resulting Git change.")
    base_url = base_url.rstrip("/")
    state_path = skill_state_path(base_url, scope, home, project_dir)
    state = read_skill_state(state_path)
    agents = effective_agents(agents, state)
    installed = [local_agent_status(base_url, agent, scope, home, project_dir, state) for agent in agents]
    installed = [row for row in installed if row["installed"]]
    if not state and not installed:
        return {
            "schema": "rock-kb-skill-policy-v1",
            "status": "not_installed",
            "policy": policy,
            "scope": scope,
            "state_path": str(state_path),
            "next": "Install the Rock KB agent integration before setting its update policy.",
        }

    state = {
        **state,
        "schema": SKILL_STATE_SCHEMA,
        "service": base_url,
        "scope": scope,
        "project_dir": str(project_dir) if scope == "project" else None,
        "policy": policy,
        "agents": sorted(set(state.get("agents") or []) | {str(row["agent"]) for row in installed}),
        "policy_updated_at": utc_now(),
    }
    if policy == "pinned":
        source_hashes = {str(row.get("source_sha256") or "") for row in installed}
        source_hashes.discard("")
        versions = {str(row.get("skill_version") or "") for row in installed}
        versions.discard("")
        if len(source_hashes) > 1 or len(versions) > 1:
            raise ValueError("Installed agent hosts do not share one skill version; update them before pinning.")
        state["pinned_source_sha256"] = next(iter(source_hashes), str(state.get("installed_source_sha256") or ""))
        state["pinned_skill_version"] = next(iter(versions), str(state.get("installed_skill_version") or ""))
    else:
        state.pop("pinned_source_sha256", None)
        state.pop("pinned_skill_version", None)
    write_skill_state(state_path, state)
    return {
        "schema": "rock-kb-skill-policy-v1",
        "status": "updated",
        "policy": policy,
        "scope": scope,
        "state_path": str(state_path),
        "pinned_skill_version": state.get("pinned_skill_version"),
        "pinned_source_sha256": state.get("pinned_source_sha256"),
    }


def passive_skill_checks(
    *,
    base_url: str,
    home: Path,
    project_dir: Path,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str,
) -> list[dict]:
    if os.environ.get("ROCK_KB_SKIP_SKILL_CHECK", "").lower() in {"1", "true", "yes"}:
        return []
    notices: list[dict] = []
    for scope in ("user", "project"):
        state_path = skill_state_path(base_url, scope, home, project_dir)
        if not state_path.exists():
            continue
        try:
            state = read_skill_state(state_path)
            if not skill_check_due(state):
                continue
            agents = [agent for agent in state.get("agents") or [] if agent in SUPPORTED_AGENTS]
            report = check_agents(
                base_url=base_url,
                agents=agents,
                scope=scope,
                home=home,
                project_dir=project_dir,
                verify=True,
                fetch_text=fetch_text,
                fetch_json=fetch_json,
                client_version=client_version,
                if_due=True,
            )
            status = str(report.get("status") or "")
            skill_update_available = bool(report.get("skill_update_available"))
            config_update_available = bool(report.get("agent_config_update_available"))
            if not skill_update_available and not config_update_available:
                continue
            if report.get("policy") == "auto" and scope == "user":
                if skill_update_available:
                    update = update_agents(
                        base_url=base_url,
                        agents=agents,
                        scope=scope,
                        home=home,
                        project_dir=project_dir,
                        verify=False,
                        fetch_text=fetch_text,
                        fetch_json=fetch_json,
                        client_version=client_version,
                    )
                else:
                    update = install_agents(
                        base_url=base_url,
                        agents=agents,
                        scope=scope,
                        home=home,
                        project_dir=project_dir,
                        dry_run=False,
                        verify=False,
                        fetch_text=fetch_text,
                        fetch_json=fetch_json,
                        client_version=client_version,
                    )
                components = [name for name, available in (("skill", skill_update_available), ("agent_config", config_update_available)) if available]
                notices.append({"scope": scope, "status": "updated", "components": components, "restart_required": update.get("restart_required", False)})
            elif status == "pinned_skill_update_available":
                continue
            else:
                notices.append(
                    {
                        "scope": scope,
                        "status": status,
                        "policy": report.get("policy"),
                        "recommended_command": report.get("recommended_command"),
                    }
                )
        except Exception as exc:  # A passive check must never block the requested KB operation.
            record_skill_check_error(state_path, exc)
    return notices


def fetch_skill_release(
    base_url: str,
    fetch_text: Callable[[str], str],
    fetch_json: Callable[[str], object],
    client_version: str,
) -> SkillRelease:
    base_url = base_url.rstrip("/")
    manifest = fetch_json(f"{base_url}/{SKILL_MANIFEST_ENDPOINT}")
    if not isinstance(manifest, dict):
        raise RuntimeError("Hosted Rock KB skill manifest must contain a JSON object")
    validate_skill_manifest(manifest)
    if str(manifest["source_url"]).rstrip("/") != f"{base_url}/artifacts/{SKILL_ARTIFACT}":
        raise RuntimeError("Hosted Rock KB skill manifest source URL does not match the configured service")
    if not client_meets_minimum(client_version, str(manifest["minimum_client_version"])):
        raise RuntimeError(
            f"Rock KB skill {manifest['skill_version']} requires rock-kb client {manifest['minimum_client_version']} or newer; current client is {client_version}."
        )
    source_text = fetch_text(f"{base_url}/artifacts/{SKILL_ARTIFACT}")
    source_sha256 = sha256_text(source_text)
    if source_sha256 != manifest["sha256"]:
        raise RuntimeError("Hosted Rock KB skill content does not match its published manifest hash")
    if "name: rock-kb-agent" not in source_text:
        raise RuntimeError("Hosted skill artifact is missing the rock-kb-agent identity marker")
    installed_text = render_installed_skill(source_text, manifest)
    return SkillRelease(dict(manifest), source_text, installed_text, source_sha256)


def validate_skill_manifest(manifest: dict) -> None:
    required = {
        "schema",
        "name",
        "skill_version",
        "published_at",
        "source_url",
        "source_path",
        "sha256",
        "minimum_client_version",
        "restart_required",
        "update_check_interval_hours",
        "default_update_policy",
        "supported_agents",
    }
    missing = sorted(required - set(manifest))
    if missing:
        raise RuntimeError(f"Hosted Rock KB skill manifest is missing: {', '.join(missing)}")
    if manifest.get("schema") != SKILL_MANIFEST_SCHEMA or manifest.get("name") != "rock-kb-agent":
        raise RuntimeError("Hosted Rock KB skill manifest has an unsupported identity or schema")
    if manifest.get("source_path") != SKILL_ARTIFACT:
        raise RuntimeError("Hosted Rock KB skill manifest points to an unsupported source path")
    if not re.fullmatch(r"[0-9a-f]{64}", str(manifest.get("sha256") or "")):
        raise RuntimeError("Hosted Rock KB skill manifest has an invalid SHA-256")
    if manifest.get("default_update_policy") not in SKILL_POLICIES:
        raise RuntimeError("Hosted Rock KB skill manifest has an invalid default update policy")
    supported = manifest.get("supported_agents")
    if not isinstance(supported, list) or not set(SUPPORTED_AGENTS).issubset(set(supported)):
        raise RuntimeError("Hosted Rock KB skill manifest does not cover every supported agent")
    interval = manifest.get("update_check_interval_hours")
    if not isinstance(interval, int) or not 1 <= interval <= 168:
        raise RuntimeError("Hosted Rock KB skill manifest has an invalid update interval")


def render_installed_skill(source_text: str, manifest: dict) -> str:
    frontmatter, body = parse_skill(source_text)
    metadata = frontmatter.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise RuntimeError("Rock KB skill metadata must be a mapping")
    declared_version = str(metadata.get("rock-kb-skill-version") or "")
    if declared_version and declared_version != str(manifest["skill_version"]):
        raise RuntimeError("Rock KB skill frontmatter and hosted manifest versions disagree")
    frontmatter["metadata"] = {
        **metadata,
        "rock-kb-skill-version": str(manifest["skill_version"]),
        "rock-kb-source": str(manifest["source_url"]),
        "rock-kb-source-sha256": str(manifest["sha256"]),
        "rock-kb-published-at": str(manifest["published_at"]),
        "rock-kb-minimum-client-version": str(manifest["minimum_client_version"]),
        "rock-kb-managed-by": "rock-kb",
    }
    encoded = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False, width=4096).rstrip()
    return f"---\n{encoded}\n---\n{body}"


def parse_skill(text: str) -> tuple[dict, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise RuntimeError("Rock KB skill is missing YAML frontmatter")
    closing = next((index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if closing is None:
        raise RuntimeError("Rock KB skill YAML frontmatter is not closed")
    payload = yaml.safe_load("".join(lines[1:closing])) or {}
    if not isinstance(payload, dict) or payload.get("name") != "rock-kb-agent":
        raise RuntimeError("Rock KB skill frontmatter has an invalid identity")
    return payload, "".join(lines[closing + 1 :])


def local_agent_status(base_url: str, agent: str, scope: str, home: Path, project_dir: Path, state: dict) -> dict:
    paths = agent_paths(agent, scope, home, project_dir)
    installed = paths.skill.exists()
    metadata: dict = {}
    file_sha256 = ""
    if installed:
        text = paths.skill.read_text(encoding="utf-8")
        file_sha256 = sha256_text(text)
        try:
            frontmatter, _ = parse_skill(text)
            metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
        except RuntimeError:
            metadata = {}
    source_sha256 = str(metadata.get("rock-kb-source-sha256") or "")
    latest_sha256 = str((state.get("remote_manifest") or {}).get("sha256") or "")
    managed_hash = str((state.get("installed_file_sha256") or {}).get(agent) or "")
    if not installed:
        skill_status = "not_installed"
    elif managed_hash and managed_hash != file_sha256:
        skill_status = "locally_modified"
    elif latest_sha256 and source_sha256 == latest_sha256:
        skill_status = "current"
    elif latest_sha256:
        skill_status = "update_available"
    else:
        skill_status = "unknown"
    config_reasons: tuple[str, ...] = ()
    try:
        config_text = paths.config.read_text(encoding="utf-8") if paths.config.exists() else ""
        request_headers = telemetry_headers(telemetry_state_path(home)) if scope == "user" else {}
        config_reasons = config_update_reasons(config_text, paths.format, paths.server_key, f"{base_url}/mcp", request_headers)
        config_status = "update_available" if config_reasons else "current"
    except (ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        config_status = "invalid"
    policy = str(state.get("policy") or "notify")
    if skill_status == "locally_modified":
        status = "locally_modified"
    elif config_status == "invalid":
        status = "invalid_configuration"
    elif skill_status == "not_installed":
        status = "not_installed"
    elif skill_status == "unknown" and config_status == "current":
        status = "unknown"
    else:
        status = lifecycle_status(skill_status == "update_available", config_status == "update_available", policy)
    return {
        "agent": agent,
        "installed": installed,
        "status": status,
        "skill_status": skill_status,
        "skill_version": metadata.get("rock-kb-skill-version"),
        "source_sha256": source_sha256 or None,
        "file_sha256": file_sha256 or None,
        "skill_path": str(paths.skill),
        "config_path": str(paths.config),
        "config_status": config_status,
        "config_update_reasons": list(config_reasons),
    }


def recommended_action(status: str, policy: str) -> str:
    if status in {"current", "not_due", "ok", "dry_run"}:
        return "none"
    if status == "agent_config_update_available":
        return "run_install_agent"
    if status in {"skill_update_available", "skill_and_agent_config_update_available"}:
        return "run_skill_update"
    if status in {"pinned_skill_update_available", "pinned_skill_and_agent_config_update_available", "pinned"}:
        return "remain_pinned"
    if status == "invalid_configuration":
        return "review_agent_configuration"
    if status == "locally_modified":
        return "review_local_skill"
    return "none"


def recommended_command(status: str) -> str | None:
    if status == "agent_config_update_available":
        return "uvx rock-kb install-agent"
    if status in {"skill_update_available", "skill_and_agent_config_update_available"}:
        return "uvx rock-kb skill update"
    if status == "pinned_skill_and_agent_config_update_available":
        return "uvx rock-kb install-agent --dry-run"
    if status == "invalid_configuration":
        return "uvx rock-kb install-agent --dry-run"
    return None


def lifecycle_status(skill_update_available: bool, config_update_available: bool, policy: str) -> str:
    if skill_update_available and config_update_available:
        return "pinned_skill_and_agent_config_update_available" if policy == "pinned" else "skill_and_agent_config_update_available"
    if skill_update_available:
        return "pinned_skill_update_available" if policy == "pinned" else "skill_update_available"
    if config_update_available:
        return "agent_config_update_available"
    return "current"


def effective_agents(agents: list[str], state: dict) -> list[str]:
    return list(dict.fromkeys([agent for agent in (agents or state.get("agents") or []) if agent in SUPPORTED_AGENTS]))


def skill_state_path(base_url: str, scope: str, home: Path, project_dir: Path) -> Path:
    configured = os.environ.get("ROCK_KB_STATE_DIR")
    if configured:
        root = Path(configured).expanduser()
    elif os.environ.get("XDG_STATE_HOME") and home == Path.home():
        root = Path(os.environ["XDG_STATE_HOME"]).expanduser() / "rock-kb"
    else:
        root = home.expanduser() / ".local" / "state" / "rock-kb"
    identity = {"service": base_url.rstrip("/"), "scope": scope}
    if scope == "project":
        identity["project_dir"] = str(project_dir.expanduser().resolve())
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    return root / f"skill-{scope}-{digest}.json"


def read_skill_state(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != SKILL_STATE_SCHEMA:
        raise ValueError(f"Unsupported Rock KB skill state: {path}")
    return payload


def write_skill_state(path: Path, payload: dict) -> None:
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


def skill_check_due(state: dict, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    last_checked = parse_timestamp(state.get("last_checked_at"))
    if last_checked and now - last_checked < timedelta(hours=check_interval_hours(state)):
        return False
    last_attempted = parse_timestamp(state.get("last_attempted_at"))
    if state.get("last_error") and last_attempted and now - last_attempted < timedelta(hours=SKILL_ERROR_RETRY_HOURS):
        return False
    return True


def check_interval_hours(state: dict) -> int:
    value = (state.get("remote_manifest") or {}).get("update_check_interval_hours", SKILL_CHECK_INTERVAL_HOURS)
    return value if isinstance(value, int) and 1 <= value <= 168 else SKILL_CHECK_INTERVAL_HOURS


def record_skill_check_error(path: Path, exc: Exception) -> None:
    try:
        state = read_skill_state(path)
        state["last_attempted_at"] = utc_now()
        state["last_error"] = type(exc).__name__
        write_skill_state(path, state)
    except (OSError, ValueError, json.JSONDecodeError):
        return


def parse_timestamp(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def client_meets_minimum(current: str, minimum: str) -> bool:
    if current == "dev":
        return True
    current_match = re.match(r"^(\d+)\.(\d+)\.(\d+)", current)
    minimum_match = re.match(r"^(\d+)\.(\d+)\.(\d+)", minimum)
    if not current_match or not minimum_match:
        return False
    return tuple(map(int, current_match.groups())) >= tuple(map(int, minimum_match.groups()))


def public_skill_manifest(manifest: dict) -> dict:
    allowed = {
        "schema",
        "name",
        "skill_version",
        "published_at",
        "source_repository",
        "source_url",
        "source_path",
        "legacy_source_path",
        "sha256",
        "minimum_client_version",
        "restart_required",
        "update_check_interval_hours",
        "default_update_policy",
        "supported_agents",
    }
    return {key: manifest[key] for key in allowed if key in manifest}


def update_config(text: str, format_name: str, server_key: str, mcp_url: str, headers: dict[str, str] | None = None) -> str:
    headers = headers or {}
    if format_name == "toml":
        return update_toml_config(text, mcp_url, headers)
    entry = expected_config_entry(format_name, mcp_url, headers)
    return update_json_config(text, server_key, "rock-kb", entry)


def update_toml_config(text: str, mcp_url: str, headers: dict[str, str] | None = None) -> str:
    headers = headers or {}
    if text.strip():
        parsed = tomllib.loads(text)
        actual = ((parsed.get("mcp_servers") or {}).get("rock-kb") if isinstance(parsed.get("mcp_servers"), dict) else None)
        if config_entries_equal(actual, expected_config_entry("toml", mcp_url, headers)):
            return text
    section = f'[mcp_servers.rock-kb]\nurl = {json.dumps(mcp_url)}\n'
    if headers:
        values = ", ".join(f"{json.dumps(key)} = {json.dumps(value)}" for key, value in sorted(headers.items()))
        section += f"http_headers = {{ {values} }}\n"
    table_pattern = re.compile(r"(?m)^[ \t]*\[(?!\[)([^\]\r\n]+)\][ \t]*(?:#.*)?(?:\r?\n|\Z)")
    table_headers = list(table_pattern.finditer(text))
    managed_ranges: list[tuple[int, int]] = []
    for index, match in enumerate(table_headers):
        table_path = re.sub(r"\s+", "", match.group(1))
        if not re.fullmatch(r'mcp_servers\.(?:rock-kb|"rock-kb")(?:\..+)?', table_path):
            continue
        end = table_headers[index + 1].start() if index + 1 < len(table_headers) else len(text)
        managed_ranges.append((match.start(), end))

    if managed_ranges:
        parts: list[str] = []
        cursor = 0
        for index, (start, end) in enumerate(managed_ranges):
            parts.append(text[cursor:start])
            if index == 0:
                parts.append(section + "\n")
            cursor = end
        parts.append(text[cursor:])
        updated = "".join(parts).rstrip() + "\n"
    else:
        updated = text.rstrip() + ("\n\n" if text.strip() else "") + section
    tomllib.loads(updated)
    return updated


def update_json_config(text: str, server_key: str, server_name: str, entry: dict) -> str:
    text = text or "{}\n"
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("Agent config root must be a JSON object")
    servers = parsed.get(server_key)
    if isinstance(servers, dict) and config_entries_equal(servers.get(server_name), entry):
        return text

    root_members, root_close = json_object_members(text, text.index("{"))
    entry_text = json.dumps(entry, separators=(", ", ": "))
    if server_key not in root_members:
        value = json.dumps({server_name: entry}, separators=(", ", ": "))
        return insert_json_member(text, root_close, server_key, value, bool(root_members))

    map_start, _ = root_members[server_key]
    if not isinstance(parsed.get(server_key), dict):
        raise ValueError(f"Agent config {server_key} value must be a JSON object")
    server_members, server_close = json_object_members(text, map_start)
    if server_name in server_members:
        value_start, value_end = server_members[server_name]
        return text[:value_start] + entry_text + text[value_end:]
    return insert_json_member(text, server_close, server_name, entry_text, bool(server_members))


def expected_config_entry(format_name: str, mcp_url: str, headers: dict[str, str]) -> dict:
    if format_name == "toml":
        entry: dict = {"url": mcp_url}
        if headers:
            entry["http_headers"] = headers
        return entry
    entry = {"type": "remote", "url": mcp_url, "enabled": True} if format_name == "opencode" else {"type": "http", "url": mcp_url}
    if headers:
        entry["headers"] = headers
    return entry


def config_entries_equal(actual: object, expected: dict) -> bool:
    if not isinstance(actual, dict):
        return False
    normalized_actual = dict(actual)
    normalized_expected = dict(expected)
    for key in ("headers", "http_headers"):
        if normalized_actual.get(key) == {}:
            normalized_actual.pop(key)
        if normalized_expected.get(key) == {}:
            normalized_expected.pop(key)
    return normalized_actual == normalized_expected


def config_update_reasons(
    text: str,
    format_name: str,
    server_key: str,
    mcp_url: str,
    headers: dict[str, str] | None = None,
) -> tuple[str, ...]:
    headers = headers or {}
    expected = expected_config_entry(format_name, mcp_url, headers)
    if format_name == "toml":
        parsed = tomllib.loads(text) if text.strip() else {}
        servers = parsed.get(server_key)
    else:
        parsed = json.loads(text or "{}\n")
        if not isinstance(parsed, dict):
            raise ValueError("Agent config root must be a JSON object")
        servers = parsed.get(server_key)
    if servers is not None and not isinstance(servers, dict):
        raise ValueError(f"Agent config {server_key} value must be an object")
    actual = servers.get("rock-kb") if isinstance(servers, dict) else None
    if config_entries_equal(actual, expected):
        return ()
    if actual is not None and not isinstance(actual, dict):
        raise ValueError("Agent config rock-kb value must be an object")

    reasons: list[str] = []
    actual = actual or {}
    endpoint_keys = {"url"} if format_name == "toml" else {"type", "url", "enabled"} if format_name == "opencode" else {"type", "url"}
    if any(actual.get(key) != expected.get(key) for key in endpoint_keys):
        reasons.append("mcp_endpoint")
    header_key = "http_headers" if format_name == "toml" else "headers"
    if actual.get(header_key, {}) != expected.get(header_key, {}):
        reasons.append("telemetry_headers")
    if set(actual) - endpoint_keys - {header_key}:
        reasons.append("managed_entry")
    return tuple(reasons or ["managed_entry"])


def json_object_members(text: str, object_start: int) -> tuple[dict[str, tuple[int, int]], int]:
    decoder = json.JSONDecoder()
    position = skip_space(text, object_start)
    if position >= len(text) or text[position] != "{":
        raise ValueError("Expected JSON object")
    position += 1
    members: dict[str, tuple[int, int]] = {}
    while True:
        position = skip_space(text, position)
        if text[position] == "}":
            return members, position
        key, key_end = decoder.raw_decode(text, position)
        if not isinstance(key, str):
            raise ValueError("Expected JSON object key")
        position = skip_space(text, key_end)
        if text[position] != ":":
            raise ValueError("Expected JSON colon")
        value_start = skip_space(text, position + 1)
        _, value_end = decoder.raw_decode(text, value_start)
        members[key] = (value_start, value_end)
        position = skip_space(text, value_end)
        if text[position] == ",":
            position += 1
            continue
        if text[position] == "}":
            return members, position
        raise ValueError("Expected JSON comma or object close")


def insert_json_member(text: str, close: int, key: str, value: str, has_members: bool) -> str:
    line_start = text.rfind("\n", 0, close) + 1
    parent_indent = text[line_start:close] if not text[line_start:close].strip() else ""
    child_indent = parent_indent + "  "
    if has_members:
        last_content = close - 1
        while last_content >= 0 and text[last_content].isspace():
            last_content -= 1
        insertion = f',\n{child_indent}{json.dumps(key)}: {value}'
        return text[: last_content + 1] + insertion + text[last_content + 1 :]
    insertion = f'\n{child_indent}{json.dumps(key)}: {value}\n{parent_indent}'
    return text[:close] + insertion + text[close:]


def skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = path.with_name(f"{path.name}.rock-kb-backup-{stamp}")
    counter = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.rock-kb-backup-{stamp}-{counter}")
        counter += 1
    shutil.copy2(path, backup)
    return backup
