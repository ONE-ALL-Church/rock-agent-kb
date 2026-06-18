from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

VALID_FIXTURE = Path("tests/fixtures/contributions/valid-bundle.jsonl")


def load_client_validator():
    path = Path("clients/python/src/rock_kb_client/validator.py")
    spec = importlib.util.spec_from_file_location("client_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_client_cli():
    source_root = str(Path("clients/python/src").resolve())
    if source_root not in sys.path:
        sys.path.insert(0, source_root)
    import rock_kb_client.cli as cli

    return cli


def test_client_validator_accepts_valid_fixture():
    validator = load_client_validator()

    assert validator.validate_bundle(VALID_FIXTURE) == []


def test_client_validator_rejects_private_path(tmp_path):
    validator = load_client_validator()
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    row["source_urls"] = ["data/review/private-source.md"]
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")

    errors = validator.validate_bundle(bundle)

    assert any("private path reference" in error for error in errors)


def test_client_validator_rejects_duplicate_contribution_ids(tmp_path):
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")

    errors = load_client_validator().validate_bundle(bundle)

    assert any("duplicate contribution_id fixture-org:workflow-troubleshooting" in error for error in errors)


def test_client_dashboard_command_hits_operations_dashboard(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-operations-dashboard-v1"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main(["--url", "https://example.test", "dashboard"])

    assert exit_code == 0
    assert urls == ["https://example.test/operations/dashboard"]
    assert "rock-kb-operations-dashboard-v1" in capsys.readouterr().out


def test_client_get_text_sends_user_agent(monkeypatch):
    cli = load_client_cli()
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return b"ok"

    def fake_urlopen(req):
        captured["user_agent"] = req.headers.get("User-agent")
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.get_text("https://example.test/manifest.json") == "ok"
    assert captured["user_agent"] == cli.USER_AGENT


def test_client_post_json_sends_user_agent_and_accept(monkeypatch):
    cli = load_client_cli()
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return b'{"status":"ok"}'

    def fake_urlopen(req):
        captured["user_agent"] = req.headers.get("User-agent")
        captured["accept"] = req.headers.get("Accept")
        return FakeResponse()

    monkeypatch.setattr(cli.request, "urlopen", fake_urlopen)

    assert cli.post_json("https://example.test/submit", {"ok": True}, token="secret") == {"status": "ok"}
    assert captured["user_agent"] == cli.USER_AGENT
    assert captured["accept"] == "application/json"
