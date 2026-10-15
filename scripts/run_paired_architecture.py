#!/usr/bin/env python3
"""Run sealed public-source packets through an existing Claude subscription."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from paired_architecture import canonical_hash, digest, private_destination, validate_answer, verify


MODEL = "claude-sonnet-5-5"


def model_environment() -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        if key.startswith(("ANTHROPIC_", "CLAUDE_", "AWS_", "GOOGLE_", "GCLOUD_",
                           "GCP_", "VERTEX_", "CLOUD_ML_", "AZURE_", "OPENAI_")) or {
            "TOKEN", "KEY", "SECRET", "PASSWORD", "CREDENTIAL", "CREDENTIALS",
        }.intersection(key.upper().split("_")) or key in {"CLAUDECODE", "API_TIMEOUT_MS"}:
            env.pop(key, None)
    return env


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def validation_errors(answer: dict, packet: dict) -> list[str]:
    try:
        validate_answer(answer, packet)
    except ValueError as exc:
        return [str(exc)]
    return []


def safe_write_path(destination: Path, path: Path) -> Path:
    if not path.absolute().is_relative_to(destination) or not path.resolve().is_relative_to(destination):
        raise ValueError("write path escapes the private destination")
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError("symlinked write path is forbidden")
        if parent == destination:
            break
    return path


def write_evidence(destination: Path, path: Path, text: str) -> None:
    safe_write_path(destination, path).write_text(text)


def run(destination: Path, limit: int | None = None) -> dict:
    destination = destination.absolute()
    if destination != destination.resolve():
        raise ValueError("symlinked destination is forbidden")
    private_destination(Path(__file__).resolve().parents[1], destination)
    verify(destination)
    for name in ("generator-runtime.json", "outputs", "execution"):
        safe_write_path(destination, destination / name)
    env = model_environment()
    auth = json.loads(subprocess.run(
        ["claude", "auth", "status"], env=env, capture_output=True,
        text=True, check=True, timeout=20,
    ).stdout)
    if not auth.get("loggedIn") or auth.get("authMethod") != "claude.ai":
        raise ValueError("an existing Claude subscription is required; API billing is disabled")
    dispatch = json.loads((destination / "generator/dispatch.json").read_text())
    entries = dispatch["packets"][:limit] if limit else dispatch["packets"]
    for entry in entries:
        safe_write_path(destination, destination / entry["output"])
        for attempt in (1, 2):
            for kind, suffix in (("attempt", "json"), ("response", "json"), ("stderr", "txt")):
                safe_write_path(destination, destination / "execution" / f"{entry['packet_id']}.{kind}-{attempt}.{suffix}")
    schema = json.loads((destination / "generator/answer.schema.json").read_text())
    # Claude's validator supports this schema's keywords, but not its dialect annotation.
    schema.pop("$schema", None)
    instructions = json.loads((destination / "generator/instructions.json").read_text())["instructions"]
    configuration = {
        "schema": "rock-kb-paired-generator-runtime-v1", "model": MODEL,
        "client_version": subprocess.run(["claude", "--version"], env=env, capture_output=True,
                                         text=True, check=True, timeout=20).stdout.strip(),
        "auth": "existing_claude_subscription", "effort": "high",
        "tools": [], "mcp_servers": [], "session_persistence": False,
        "customizations": "safe_mode", "temperature": "provider_default_not_configurable",
        "seed": "not_supported_by_cli", "context_window": 1000000,
        "output_limit": "provider_default_128000", "concurrency": 1,
        "retry": "one_subprocess_transport_timeout_only", "timeout_seconds": 180,
        "instructions_hash": canonical_hash(instructions),
        "cli_schema_hash": canonical_hash(schema),
        "pricing": "CLI list-price estimate; not money charged to the subscription",
    }
    runtime_path = destination / "generator-runtime.json"
    if runtime_path.exists() and json.loads(runtime_path.read_text()) != configuration:
        if any((destination / "outputs").glob("*.json")):
            raise ValueError("generator configuration changed; use a separate complete run")
        runtime_path.rename(safe_write_path(destination, destination / f"preflight-runtime-{time.time_ns()}.json"))
    write_evidence(destination, runtime_path, json.dumps(configuration, indent=2, sort_keys=True) + "\n")
    safe_write_path(destination, destination / "outputs").mkdir(exist_ok=True)
    logs = destination / "execution"
    safe_write_path(destination, logs).mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rock-kb-tool-free-") as cwd:
        for number, entry in enumerate(entries, 1):
            packet_path = destination / entry["packet"]
            packet_bytes = packet_path.read_bytes()
            packet = json.loads(packet_bytes)
            if digest(packet_bytes) != entry["file_bytes_sha256"] or canonical_hash(packet) != entry["canonical_json_sha256"]:
                raise ValueError("sealed generator packet changed")
            output = destination / entry["output"]
            if output.exists():
                receipts = [json.loads(safe_write_path(destination, path).read_text()) for path in sorted(logs.glob(f"{entry['packet_id']}.attempt-*.json"))]
                output_hash = canonical_hash(json.loads(output.read_text()))
                if not any(isinstance(receipt, dict) and receipt.get("packet_id") == entry["packet_id"]
                           and type(receipt.get("exit_code")) is int and receipt["exit_code"] == 0
                           and isinstance(receipt.get("model_usage"), dict) and set(receipt["model_usage"]) == {MODEL}
                           and all(isinstance(usage, dict) for usage in receipt["model_usage"].values())
                           and not any(usage.get("webSearchRequests", 0) for usage in receipt["model_usage"].values())
                           and receipt.get("output_hash") == output_hash and receipt.get("packet_hash") == entry["canonical_json_sha256"]
                           and receipt.get("status") in {"ok", "validation_failure"} for receipt in receipts):
                    raise ValueError("existing output does not match its execution receipt")
                continue
            command = [
                "claude", "--safe-mode", "--print", "--tools", "",
                "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                "--disable-slash-commands", "--no-session-persistence",
                "--model", MODEL, "--effort", "high", "--output-format", "json",
                "--json-schema", json.dumps(schema), "--system-prompt", instructions,
            ]
            for attempt in range(2):
                record = {"packet_id": entry["packet_id"], "started_at": timestamp(), "attempt": attempt + 1}
                started = time.monotonic()
                response_path = logs / f"{entry['packet_id']}.response-{attempt + 1}.json"
                attempt_path = logs / f"{entry['packet_id']}.attempt-{attempt + 1}.json"
                stderr_path = logs / f"{entry['packet_id']}.stderr-{attempt + 1}.txt"
                original = json.loads(attempt_path.read_text()) if attempt_path.exists() else {}
                if original.get("status") == "client_failure":
                    raise ValueError("response recovery requires proof of an original successful process")
                try:
                    if response_path.exists():
                        response_bytes = response_path.read_bytes()
                        if (original.get("exit_code") != 0 or type(original.get("exit_code")) is not int
                                or original.get("status") not in {"response_saved", "ok", "validation_failure"}
                                or original.get("packet_id") != entry["packet_id"]
                                or original.get("packet_hash") != entry["canonical_json_sha256"]
                                or original.get("response_hash") != digest(response_bytes)):
                            raise ValueError("response recovery requires proof of an original successful process")
                        completed = subprocess.CompletedProcess(command, original["exit_code"], response_bytes.decode(),
                                                                stderr_path.read_text() if stderr_path.exists() else "")
                        record = dict(original)
                        record["recovered_response"] = True
                    else:
                        completed = subprocess.run(command, input=json.dumps(packet), cwd=cwd, env=env,
                                                   capture_output=True, text=True, timeout=180)
                except subprocess.TimeoutExpired:
                    record.update(status="transport_timeout", elapsed_seconds=time.monotonic() - started)
                    write_evidence(destination, attempt_path, json.dumps(record) + "\n")
                    if attempt:
                        raise RuntimeError("generator transport timed out twice")
                    continue
                record.update(elapsed_seconds=time.monotonic() - started, completed_at=timestamp(),
                              exit_code=completed.returncode)
                if not record.get("recovered_response"):
                    write_evidence(destination, response_path, completed.stdout)
                    write_evidence(destination, stderr_path, completed.stderr)
                    record.update(status="client_failure" if completed.returncode else "response_saved",
                                  packet_hash=entry["canonical_json_sha256"],
                                  response_hash=digest(completed.stdout.encode()))
                    write_evidence(destination, attempt_path, json.dumps(record) + "\n")
                if completed.returncode:
                    record["status"] = "client_failure"
                    write_evidence(destination, attempt_path, json.dumps(record) + "\n")
                    raise RuntimeError(f"generator client failed; inspect private evidence for {entry['packet_id']}")
                response = json.loads(completed.stdout)
                if record.get("recovered_response"):
                    record["elapsed_seconds"] = response.get("duration_ms", 0) / 1000
                    record["latency_source"] = "original_cli_duration_ms"
                else:
                    record["latency_source"] = "process_wall_time"
                model_usage = response.get("modelUsage") or {}
                if set(model_usage) != {MODEL} or response.get("is_error"):
                    raise ValueError("generator failed or silently changed model")
                if any(value.get("webSearchRequests", 0) for value in model_usage.values()):
                    raise ValueError("generator used external search")
                if (response.get("subagent_stats") or {}).get("spawned", 0) or response.get("permission_denials"):
                    raise ValueError("generator attempted tool use")
                answer = response.get("structured_output")
                if answer is None:
                    answer = json.loads(response["result"])
                errors = validation_errors(answer, packet)
                write_evidence(destination, output, json.dumps(answer, ensure_ascii=False, sort_keys=True) + "\n")
                record.update(status="validation_failure" if errors else "ok", validation_errors=errors,
                              usage=response.get("usage"), model_usage=model_usage,
                              output_hash=canonical_hash(answer),
                              packet_hash=entry["canonical_json_sha256"],
                              reported_list_price_usd=response.get("total_cost_usd"))
                write_evidence(destination, attempt_path, json.dumps(record, indent=2) + "\n")
                print(json.dumps({"completed": number, "total": len(entries), "status": record["status"]}), flush=True)
                break
    invalid = sum(bool(validation_errors(json.loads((destination / entry["output"]).read_text()),
                                         json.loads((destination / entry["packet"]).read_text()))) for entry in entries)
    return {"status": "completed_with_validation_failures" if invalid else "ok",
            "packet_count": len(entries), "strict_invalid_count": invalid}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    print(json.dumps(run(args.destination, args.limit)))
