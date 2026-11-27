from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
AUTH_COMMAND = ["claude", "auth", "status"]
VERSION_COMMAND = ["claude", "--version"]
CREDENTIAL_ENV = {
    "ANTHROPIC_API_KEY": "synthetic-key",
    "ANTHROPIC_AUTH_TOKEN": "synthetic-token",
    "ANTHROPIC_BASE_URL": "https://provider.invalid",
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "CLAUDE_CODE_USE_VERTEX": "1",
    "CLAUDE_CODE_USE_FOUNDRY": "1",
    "CLAUDE_CODE_OAUTH_TOKEN": "synthetic-token",
    "CLAUDE_CONFIG_DIR": "/synthetic/config",
    "CLAUDECODE": "1",
    "API_TIMEOUT_MS": "123",
    "AWS_ACCESS_KEY_ID": "synthetic-key",
    "AWS_SECRET_ACCESS_KEY": "synthetic-secret",
    "AWS_SESSION_TOKEN": "synthetic-token",
    "AWS_PROFILE": "synthetic-profile",
    "GOOGLE_APPLICATION_CREDENTIALS": "/synthetic/credentials.json",
    "GOOGLE_CLOUD_PROJECT": "synthetic-project",
    "AZURE_API_KEY": "synthetic-key",
    "OPENAI_API_KEY": "synthetic-key",
    "GH_TOKEN": "synthetic-token",
}


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def answer_for(packet: dict) -> dict:
    return {
        "case_id": packet["case_id"],
        "answerability": "answerable",
        "answer": "The supplied source supports this operation. [S1]",
        "citations": ["S1"],
    }


def response_for(runner, packet: dict) -> dict:
    return {
        "modelUsage": {runner.MODEL: {"inputTokens": 10, "outputTokens": 20, "webSearchRequests": 0}},
        "is_error": False,
        "structured_output": answer_for(packet),
        "usage": {"input_tokens": 10, "output_tokens": 20},
        "duration_ms": 100,
        "total_cost_usd": 0.001,
    }


@pytest.fixture(autouse=True)
def block_live_processes(monkeypatch):
    blocked = Mock(side_effect=AssertionError("live subprocesses are forbidden in runner tests"))
    monkeypatch.setattr(subprocess, "run", blocked)
    monkeypatch.setattr(subprocess, "Popen", blocked)


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("paired_architecture_runner_tests", SCRIPTS / "run_paired_architecture.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "timestamp", lambda: "2026-10-14T00:00:00+00:00")
    return module


@pytest.fixture
def sealed(runner, tmp_path, monkeypatch):
    pa = importlib.import_module("paired_architecture")
    destination = tmp_path / "sealed"
    entries = []
    for index in range(80):
        packet_id = f"packet-{index:03}"
        relative = f"generator/packets/{packet_id}.json"
        packet = {
            "case_id": f"case-{index // 2:03}",
            "instructions": pa.GENERATOR_INSTRUCTIONS,
            "question": "What does the supplied source establish?",
            "evidence": [{"label": "S1", "text": "This operation is supported."}],
            "output_schema": pa.ANSWER_SCHEMA,
        }
        save_json(destination / relative, packet)
        entries.append({"packet_id": packet_id, "packet": relative,
                        "output": f"outputs/{packet_id}.json", **pa.hashes(destination / relative)})
    save_json(destination / "protocol.json", {"round": 1})
    save_json(destination / "generator/dispatch.json", {"packets": entries})
    save_json(destination / "generator/instructions.json", {"instructions": pa.GENERATOR_INSTRUCTIONS})
    save_json(destination / "generator/answer.schema.json", pa.ANSWER_SCHEMA)
    save_json(destination / "seal.json", {
        "schema": "paired-architecture-seal-v1",
        "files": {str(path.relative_to(destination)): pa.hashes(path)
                  for path in sorted(destination.rglob("*.json"))},
    })
    boundary = Mock(return_value=destination)
    monkeypatch.setattr(runner, "private_destination", boundary)
    return SimpleNamespace(destination=destination, entry=entries[0], boundary=boundary)


@pytest.fixture
def client(runner, monkeypatch):
    state = SimpleNamespace(auth={"loggedIn": True, "authMethod": "claude.ai"})

    def generate(command, **kwargs):
        packet = json.loads(kwargs["input"])
        return subprocess.CompletedProcess(command, 0, json.dumps(response_for(runner, packet)), "")

    state.generate = Mock(side_effect=generate)

    def invoke(command, **kwargs):
        if command == AUTH_COMMAND:
            return subprocess.CompletedProcess(command, 0, json.dumps(state.auth), "")
        if command == VERSION_COMMAND:
            return subprocess.CompletedProcess(command, 0, "synthetic-cli-version\n", "")
        assert command[:3] == ["claude", "--safe-mode", "--print"]
        return state.generate(command, **kwargs)

    state.process = Mock(side_effect=invoke)
    monkeypatch.setattr(runner.subprocess, "run", state.process)
    return state


def receipt_path(sealed, attempt=1):
    return sealed.destination / "execution" / f"{sealed.entry['packet_id']}.attempt-{attempt}.json"


def test_model_environment_strips_credentials_and_provider_overrides(runner):
    safe = {"HOME": "/synthetic/home", "PATH": "/synthetic/bin", "LANG": "en_US.UTF-8"}
    with patch.dict(os.environ, {**safe, **CREDENTIAL_ENV}, clear=True):
        assert runner.model_environment() == safe
        assert os.environ["ANTHROPIC_API_KEY"] == "synthetic-key"


def test_success_uses_sanitized_subscription_context_without_tools(runner, sealed, client):
    safe = {"HOME": "/synthetic/home", "PATH": "/synthetic/bin"}
    with patch.dict(os.environ, {**safe, **CREDENTIAL_ENV}, clear=True):
        result = runner.run(sealed.destination, limit=1)

    assert result == {"status": "ok", "packet_count": 1, "strict_invalid_count": 0}
    sealed.boundary.assert_called_once()
    assert client.process.call_count == 3
    for call in client.process.call_args_list:
        assert call.kwargs["env"] == safe
    command = client.generate.call_args.args[0]
    assert command[command.index("--tools") + 1] == ""
    assert "--strict-mcp-config" in command
    assert json.loads(command[command.index("--mcp-config") + 1]) == {"mcpServers": {}}
    assert "--disable-slash-commands" in command
    assert "--no-session-persistence" in command
    assert command[command.index("--model") + 1] == runner.MODEL
    assert "$schema" not in json.loads(command[command.index("--json-schema") + 1])
    assert client.generate.call_args.kwargs["timeout"] == 180
    assert Path(client.generate.call_args.kwargs["cwd"]) != sealed.destination
    receipt = read_json(receipt_path(sealed))
    assert receipt["status"] == "ok"
    assert receipt["packet_hash"] == sealed.entry["canonical_json_sha256"]
    assert receipt["output_hash"] == runner.canonical_hash(read_json(sealed.destination / sealed.entry["output"]))


@pytest.mark.parametrize("auth", [
    {"loggedIn": False, "authMethod": "claude.ai"},
    {"loggedIn": True, "authMethod": "api_key"},
    {"loggedIn": True, "authMethod": "console"},
    {"loggedIn": True, "authMethod": "bedrock"},
    {"loggedIn": True},
])
def test_non_subscription_auth_is_rejected_before_generation(runner, sealed, client, auth):
    client.auth = auth

    with pytest.raises(ValueError, match="API billing is disabled"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()
    assert client.process.call_count == 1
    assert not (sealed.destination / "generator-runtime.json").exists()


@pytest.mark.parametrize("tamper", ["packet", "packet_bytes", "dispatch"])
def test_sealed_input_tampering_is_rejected_before_auth(runner, sealed, client, tamper):
    if tamper == "dispatch":
        path = sealed.destination / "generator/dispatch.json"
        value = read_json(path)
        value["packets"][0]["output"] = "outputs/changed.json"
        save_json(path, value)
    else:
        path = sealed.destination / sealed.entry["packet"]
        if tamper == "packet_bytes":
            path.write_text(path.read_text() + "\n", encoding="utf-8")
        else:
            value = read_json(path)
            value["question"] = "Tampered question."
            save_json(path, value)

    with pytest.raises(ValueError, match="sealed file hash mismatch"):
        runner.run(sealed.destination, limit=1)

    client.process.assert_not_called()


@pytest.mark.parametrize("field", ["packet_hash", "output_hash", "status", "packet_id", "model_usage", "exit_code"])
def test_existing_output_requires_untampered_receipt(runner, sealed, client, field):
    runner.run(sealed.destination, limit=1)
    path = receipt_path(sealed)
    receipt = read_json(path)
    receipt[field] = {"different-model": {}} if field == "model_usage" else "tampered"
    save_json(path, receipt)
    original_output = (sealed.destination / sealed.entry["output"]).read_bytes()
    client.generate.reset_mock()

    with pytest.raises(ValueError, match="execution receipt"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()
    assert (sealed.destination / sealed.entry["output"]).read_bytes() == original_output


def test_changed_output_cannot_reuse_original_receipt(runner, sealed, client):
    runner.run(sealed.destination, limit=1)
    path = sealed.destination / sealed.entry["output"]
    answer = read_json(path)
    answer["answer"] = "Changed answer. [S1]"
    save_json(path, answer)
    client.generate.reset_mock()

    with pytest.raises(ValueError, match="execution receipt"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()


@pytest.mark.parametrize(("change", "message"), [
    ({"modelUsage": {}}, "silently changed model"),
    ({"modelUsage": {"different-model": {}}}, "silently changed model"),
    ({"is_error": True}, "generator failed"),
    ({"subagent_stats": {"spawned": 1}}, "attempted tool use"),
    ({"permission_denials": [{"tool_name": "Bash"}]}, "attempted tool use"),
    ({"web_search": True}, "external search"),
])
def test_model_errors_and_tool_attempts_are_rejected_without_retry(runner, sealed, client, change, message):
    packet = read_json(sealed.destination / sealed.entry["packet"])
    response = response_for(runner, packet)
    if change.get("web_search"):
        response["modelUsage"][runner.MODEL]["webSearchRequests"] = 1
    else:
        response.update(change)
    client.generate.side_effect = None
    client.generate.return_value = subprocess.CompletedProcess([], 0, json.dumps(response), "")

    with pytest.raises(ValueError, match=message):
        runner.run(sealed.destination, limit=1)

    assert client.generate.call_count == 1
    assert not (sealed.destination / sealed.entry["output"]).exists()
    assert read_json(sealed.destination / "execution" / f"{sealed.entry['packet_id']}.response-1.json") == response


@pytest.mark.parametrize("usage", [None, {"webSearchRequests": 1}])
def test_receipt_rejects_malformed_or_external_search_usage(runner, sealed, client, usage):
    runner.run(sealed.destination, limit=1)
    path = receipt_path(sealed)
    receipt = read_json(path)
    receipt["model_usage"] = {runner.MODEL: usage}
    save_json(path, receipt)
    client.generate.reset_mock()

    with pytest.raises(ValueError, match="execution receipt"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()


def test_strict_validation_failure_retains_answer_and_receipt_without_retry(runner, sealed, client):
    packet = read_json(sealed.destination / sealed.entry["packet"])
    response = response_for(runner, packet)
    response["structured_output"]["citations"] = []
    client.generate.side_effect = None
    client.generate.return_value = subprocess.CompletedProcess([], 0, json.dumps(response), "")

    result = runner.run(sealed.destination, limit=1)

    assert result == {"status": "completed_with_validation_failures", "packet_count": 1, "strict_invalid_count": 1}
    assert client.generate.call_count == 1
    path = sealed.destination / sealed.entry["output"]
    original = path.read_bytes()
    receipt = read_json(receipt_path(sealed))
    assert read_json(path) == response["structured_output"]
    assert receipt["status"] == "validation_failure"
    assert receipt["validation_errors"] == ["inline citations and citation list differ"]
    assert receipt["output_hash"] == runner.canonical_hash(response["structured_output"])

    assert runner.run(sealed.destination, limit=1) == result
    assert client.generate.call_count == 1
    assert path.read_bytes() == original
    assert read_json(receipt_path(sealed)) == receipt


def test_only_transport_timeout_retries_once(runner, sealed, client):
    packet = read_json(sealed.destination / sealed.entry["packet"])
    completed = subprocess.CompletedProcess([], 0, json.dumps(response_for(runner, packet)), "")
    client.generate.side_effect = [subprocess.TimeoutExpired("claude", 180), completed]

    result = runner.run(sealed.destination, limit=1)

    assert result["status"] == "ok"
    assert client.generate.call_count == 2
    assert read_json(receipt_path(sealed, 1))["status"] == "transport_timeout"
    assert read_json(receipt_path(sealed, 2))["status"] == "ok"
    assert all(call.kwargs["timeout"] == 180 for call in client.generate.call_args_list)
    assert client.generate.call_args_list[0].kwargs["input"] == client.generate.call_args_list[1].kwargs["input"]


def test_two_transport_timeouts_stop_with_both_receipts(runner, sealed, client):
    client.generate.side_effect = subprocess.TimeoutExpired("claude", 180)

    with pytest.raises(RuntimeError, match="timed out twice"):
        runner.run(sealed.destination, limit=1)

    assert client.generate.call_count == 2
    assert read_json(receipt_path(sealed, 1))["status"] == "transport_timeout"
    assert read_json(receipt_path(sealed, 2))["status"] == "transport_timeout"
    assert not receipt_path(sealed, 3).exists()
    assert not (sealed.destination / sealed.entry["output"]).exists()


@pytest.mark.parametrize("failure", ["client_exit", "malformed_json", "os_error"])
def test_non_timeout_process_failures_never_retry(runner, sealed, client, failure):
    if failure == "os_error":
        client.generate.side_effect = OSError("synthetic launch failure")
        error, message = OSError, "synthetic launch failure"
    else:
        client.generate.side_effect = None
        code = 1 if failure == "client_exit" else 0
        client.generate.return_value = subprocess.CompletedProcess([], code, "{not-json", "synthetic stderr")
        error, message = (RuntimeError, "generator client failed") if code else (ValueError, None)

    with pytest.raises(error, match=message):
        runner.run(sealed.destination, limit=1)

    assert client.generate.call_count == 1
    assert not receipt_path(sealed, 2).exists()
    assert not (sealed.destination / sealed.entry["output"]).exists()
    if failure == "client_exit":
        assert read_json(receipt_path(sealed))["status"] == "client_failure"


@pytest.mark.parametrize("response_state", ["valid_json", "empty", "missing"])
def test_recovery_never_promotes_client_failure_or_rewrites_its_evidence(runner, sealed, client, response_state):
    packet = read_json(sealed.destination / sealed.entry["packet"])
    client.generate.side_effect = None
    client.generate.return_value = subprocess.CompletedProcess(
        [], 1, "" if response_state == "empty" else json.dumps(response_for(runner, packet)), "original client failure"
    )
    with pytest.raises(RuntimeError, match="generator client failed"):
        runner.run(sealed.destination, limit=1)
    if response_state == "missing":
        (sealed.destination / "execution" / f"{sealed.entry['packet_id']}.response-1.json").unlink()
    before = {path.name: path.read_bytes() for path in (sealed.destination / "execution").iterdir()}

    with pytest.raises(ValueError, match="original successful process"):
        runner.run(sealed.destination, limit=1)

    assert client.generate.call_count == 1
    assert {path.name: path.read_bytes() for path in (sealed.destination / "execution").iterdir()} == before
    assert read_json(receipt_path(sealed))["exit_code"] == 1
    assert read_json(receipt_path(sealed))["status"] == "client_failure"
    assert not (sealed.destination / sealed.entry["output"]).exists()


def test_response_without_success_proof_is_not_recovered(runner, sealed, client):
    path = sealed.destination / "execution" / f"{sealed.entry['packet_id']}.response-1.json"
    save_json(path, response_for(runner, read_json(sealed.destination / sealed.entry["packet"])))
    original = path.read_bytes()

    with pytest.raises(ValueError, match="original successful process"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()
    assert path.read_bytes() == original
    assert not receipt_path(sealed).exists()


@pytest.mark.parametrize("tamper", [False, True])
def test_interrupted_validation_recovers_only_hash_bound_success(runner, sealed, client, monkeypatch, tamper):
    validate = runner.validation_errors
    with monkeypatch.context() as scoped:
        scoped.setattr(runner, "validation_errors", Mock(side_effect=RuntimeError("validator interrupted")))
        with pytest.raises(RuntimeError, match="validator interrupted"):
            runner.run(sealed.destination, limit=1)
    proof = read_json(receipt_path(sealed))
    assert proof["exit_code"] == 0
    assert proof["status"] == "response_saved"
    path = sealed.destination / "execution" / f"{sealed.entry['packet_id']}.response-1.json"
    if tamper:
        path.write_text(path.read_text() + "\n", encoding="utf-8")
        with pytest.raises(ValueError, match="original successful process"):
            runner.run(sealed.destination, limit=1)
        assert read_json(receipt_path(sealed)) == proof
    else:
        assert runner.validation_errors is validate
        assert runner.run(sealed.destination, limit=1)["status"] == "ok"
        assert read_json(receipt_path(sealed))["recovered_response"] is True
    assert client.generate.call_count == 1


@pytest.mark.parametrize("target", ["outputs", "execution", "runtime", "output", "attempt", "response", "stderr"])
@pytest.mark.parametrize("outside_boundary", [False, True])
def test_symlinked_write_files_and_parents_are_rejected(
    runner, sealed, client, tmp_path, target, outside_boundary
):
    storage = tmp_path / "outside" if outside_boundary else sealed.destination / "other-storage"
    storage.mkdir()
    marker = storage / "unchanged.txt"
    marker.write_text("original evidence", encoding="utf-8")
    if target in {"outputs", "execution"}:
        path = sealed.destination / target
        path.symlink_to(storage, target_is_directory=True)
    else:
        relative = {
            "runtime": "generator-runtime.json",
            "output": sealed.entry["output"],
            "attempt": f"execution/{sealed.entry['packet_id']}.attempt-1.json",
            "response": f"execution/{sealed.entry['packet_id']}.response-1.json",
            "stderr": f"execution/{sealed.entry['packet_id']}.stderr-1.txt",
        }[target]
        path = sealed.destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(marker)
    before = {p.name: p.read_bytes() for p in storage.iterdir()}

    with pytest.raises(ValueError, match="write path"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()
    assert {p.name: p.read_bytes() for p in storage.iterdir()} == before
    assert path.is_symlink()


def test_symlinked_destination_parent_is_rejected(runner, sealed, client, tmp_path):
    alias = tmp_path / "alias"
    alias.symlink_to(sealed.destination.parent, target_is_directory=True)

    with pytest.raises(ValueError, match="symlinked destination"):
        runner.run(alias / sealed.destination.name, limit=1)

    client.process.assert_not_called()


def test_runtime_archive_target_cannot_be_a_symlink(runner, sealed, client, tmp_path, monkeypatch):
    save_json(sealed.destination / "generator-runtime.json", {"old": "configuration"})
    marker = tmp_path / "unchanged.json"
    marker.write_text("original", encoding="utf-8")
    monkeypatch.setattr(runner.time, "time_ns", lambda: 123)
    (sealed.destination / "preflight-runtime-123.json").symlink_to(marker)

    with pytest.raises(ValueError, match="write path"):
        runner.run(sealed.destination, limit=1)

    client.generate.assert_not_called()
    assert marker.read_text(encoding="utf-8") == "original"
    assert read_json(sealed.destination / "generator-runtime.json") == {"old": "configuration"}
