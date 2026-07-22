from __future__ import annotations

import json
import os
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path


TELEMETRY_STATE_SCHEMA = "rock-kb-telemetry-opt-in-v1"
CONSENT_NOTICE_VERSION = 2
COHORT_VALUES = ("community", "external-test", "maintainer")


def telemetry_state_path(home: Path | None = None) -> Path:
    home = (home or Path.home()).expanduser()
    configured = os.environ.get("ROCK_KB_STATE_DIR")
    if configured:
        root = Path(configured).expanduser()
    elif os.environ.get("XDG_STATE_HOME") and home == Path.home():
        root = Path(os.environ["XDG_STATE_HOME"]).expanduser() / "rock-kb"
    else:
        root = home / ".local" / "state" / "rock-kb"
    return root / "telemetry-opt-in.json"


def read_telemetry_state(path: Path | None = None) -> dict:
    path = path or telemetry_state_path()
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != TELEMETRY_STATE_SCHEMA:
        raise ValueError(f"Unsupported Rock KB telemetry state: {path}")
    return payload


def enable_telemetry(cohort: str, *, consent_attested: bool, path: Path | None = None) -> dict:
    if not consent_attested:
        raise ValueError("telemetry opt-in requires consent_attested=true")
    if cohort not in COHORT_VALUES:
        raise ValueError(f"cohort must be one of: {', '.join(COHORT_VALUES)}")
    path = path or telemetry_state_path()
    existing = read_telemetry_state(path)
    installation_id = str(existing.get("installation_id") or "")
    if not installation_id.startswith("rkbi_"):
        installation_id = f"rkbi_{secrets.token_urlsafe(32)}"
    now = utc_now()
    payload = {
        "schema": TELEMETRY_STATE_SCHEMA,
        "enabled": True,
        "consent_notice_version": CONSENT_NOTICE_VERSION,
        "cohort": cohort,
        "installation_id": installation_id,
        "created_at": existing.get("created_at") or now,
        "updated_at": now,
    }
    write_private_json(path, payload)
    return public_telemetry_status(payload, path)


def disable_telemetry(*, path: Path | None = None) -> dict:
    path = path or telemetry_state_path()
    if path.exists():
        path.unlink()
    return public_telemetry_status({}, path)


def telemetry_headers(path: Path | None = None) -> dict[str, str]:
    try:
        state = read_telemetry_state(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}
    if state.get("enabled") is not True or state.get("consent_notice_version") != CONSENT_NOTICE_VERSION:
        return {}
    cohort = str(state.get("cohort") or "")
    installation_id = str(state.get("installation_id") or "")
    if cohort not in COHORT_VALUES or not valid_installation_id(installation_id):
        return {}
    return {
        "x-rock-kb-cohort": cohort,
        "x-rock-kb-installation-id": installation_id,
    }


def telemetry_status(path: Path | None = None) -> dict:
    path = path or telemetry_state_path()
    try:
        state = read_telemetry_state(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schema": "rock-kb-telemetry-opt-in-status-v1",
            "status": "invalid",
            "enabled": False,
            "state_path": str(path),
            "error": type(exc).__name__,
        }
    return public_telemetry_status(state, path)


def public_telemetry_status(state: dict, path: Path) -> dict:
    enabled = bool(
        state.get("enabled") is True
        and state.get("consent_notice_version") == CONSENT_NOTICE_VERSION
        and state.get("cohort") in COHORT_VALUES
        and valid_installation_id(str(state.get("installation_id") or ""))
    )
    return {
        "schema": "rock-kb-telemetry-opt-in-status-v1",
        "status": "enabled" if enabled else "disabled",
        "enabled": enabled,
        "cohort": state.get("cohort") if enabled else None,
        "consent_notice_version": state.get("consent_notice_version") if enabled else None,
        "anonymous_installation_id_present": enabled,
        "state_path": str(path),
        "mcp_configuration_update_required": True,
        "next": "Re-run rock-kb install-agent or regenerate rock-kb mcp-config, then restart the agent host so MCP adds or removes the private headers.",
        "privacy": (
            "The raw random installation identifier remains in this private local file. The service stores only a one-way hash and never stores an organization, person, query, IP address, or Rock data with it."
            if enabled
            else "No local installation marker is enabled. The service receives no installation identifier from this client."
        ),
    }


def valid_installation_id(value: str) -> bool:
    if not value.startswith("rkbi_") or not 40 <= len(value) <= 80:
        return False
    return all(character.isalnum() or character in "_-" for character in value)


def write_private_json(path: Path, payload: dict) -> None:
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
