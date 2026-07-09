from __future__ import annotations

import json
import os
import re
import shutil
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


SKILL_ARTIFACT = "docs/templates/rock-kb-agent/SKILL.md"
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
    skill_changed: bool


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
) -> dict:
    if not agents:
        return {
            "status": "no_agents_detected",
            "supported_agents": list(SUPPORTED_AGENTS),
            "next": "Re-run with --agent codex, --agent claude, --agent cursor, --agent opencode, or --agent all.",
        }

    base_url = base_url.rstrip("/")
    health = fetch_json(f"{base_url}/health") if verify else {"status": "skipped"}
    if verify and (not isinstance(health, dict) or health.get("status") != "ok"):
        raise RuntimeError("Hosted Rock KB health check did not return status=ok")
    skill_text = fetch_text(f"{base_url}/artifacts/{SKILL_ARTIFACT}")
    if "name: rock-kb-agent" not in skill_text:
        raise RuntimeError("Hosted skill artifact is missing the rock-kb-agent identity marker")

    plans: list[InstallPlan] = []
    for agent in agents:
        paths = agent_paths(agent, scope, home, project_dir)
        config_text = paths.config.read_text(encoding="utf-8") if paths.config.exists() else ""
        updated_config = update_config(config_text, paths.format, paths.server_key, f"{base_url}/mcp")
        config_changed = updated_config != config_text
        skill_changed = not paths.skill.exists() or paths.skill.read_text(encoding="utf-8") != skill_text
        plans.append(InstallPlan(agent, paths, updated_config, config_changed, skill_changed))

    reports = []
    for plan in plans:
        paths = plan.paths
        backups: list[str] = []

        if not dry_run:
            if plan.config_changed:
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
                paths.skill.write_text(skill_text, encoding="utf-8")

        reports.append(
            {
                "agent": plan.agent,
                "config_path": str(paths.config),
                "skill_path": str(paths.skill),
                "config_action": "would_update" if dry_run and plan.config_changed else "updated" if plan.config_changed else "unchanged",
                "skill_action": "would_update" if dry_run and plan.skill_changed else "updated" if plan.skill_changed else "unchanged",
                "backups": backups,
            }
        )

    return {
        "schema": "rock-kb-agent-install-v1",
        "status": "dry_run" if dry_run else "ok",
        "scope": scope,
        "service_health": health,
        "agents": reports,
        "restart_required": not dry_run,
    }


def update_config(text: str, format_name: str, server_key: str, mcp_url: str) -> str:
    if format_name == "toml":
        return update_toml_config(text, mcp_url)
    entry = {"type": "remote", "url": mcp_url, "enabled": True} if format_name == "opencode" else {"type": "http", "url": mcp_url}
    return update_json_config(text, server_key, "rock-kb", entry)


def update_toml_config(text: str, mcp_url: str) -> str:
    if text.strip():
        tomllib.loads(text)
    section = f'[mcp_servers.rock-kb]\nurl = {json.dumps(mcp_url)}\n'
    pattern = re.compile(r"(?ms)^\[mcp_servers\.(?:rock-kb|\"rock-kb\")\]\s*\n.*?(?=^\[|\Z)")
    if pattern.search(text):
        updated = pattern.sub(section + "\n", text, count=1).rstrip() + "\n"
    else:
        updated = text.rstrip() + ("\n\n" if text.strip() else "") + section
    tomllib.loads(updated)
    return updated


def update_json_config(text: str, server_key: str, server_name: str, entry: dict) -> str:
    text = text or "{}\n"
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("Agent config root must be a JSON object")

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
