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


def test_client_search_uses_compact_results_by_default(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-search-result-v2", "results": []}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "search", "check in labels"]) == 0
    assert urls == ["https://example.test/search?q=check%20in%20labels&limit=10&min_tier=routing_context_only&detail=compact"]
    assert "rock-kb-search-result-v2" in capsys.readouterr().out


def test_client_exact_result_and_claim_commands(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "result", "claim:claim:abc:check-in"]) == 0
    assert cli.main(["--url", "https://example.test", "claim", "claim:abc"]) == 0
    assert urls == [
        "https://example.test/results/claim%3Aclaim%3Aabc%3Acheck-in",
        "https://example.test/claims/id/claim%3Aabc",
    ]
    capsys.readouterr()


def test_client_model_command_hits_exact_model_endpoint(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-model-map-model-result-v1", "status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main([
        "--url",
        "https://example.test",
        "model",
        "Group",
        "--fields",
        "identity,required,diffs",
        "--property",
        "Members",
    ])

    assert exit_code == 0
    assert urls == ["https://example.test/model-map/models/Group?fields=identity%2Crequired%2Cdiffs&property=Members&format=json"]
    assert "rock-kb-model-map-model-result-v1" in capsys.readouterr().out


def test_client_model_map_list_command_hits_model_list_endpoint(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"schema": "rock-kb-model-map-model-list-v1", "count": 0, "models": []}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    exit_code = cli.main(["--url", "https://example.test", "model-map", "list"])

    assert exit_code == 0
    assert urls == ["https://example.test/model-map/models"]
    assert "rock-kb-model-map-model-list-v1" in capsys.readouterr().out


def test_client_recipe_commands_hit_recipe_endpoints(monkeypatch, capsys):
    cli = load_client_cli()
    urls: list[str] = []

    def fake_get_json(url: str):
        urls.append(url)
        return {"status": "ok"}

    monkeypatch.setattr(cli, "get_json", fake_get_json)

    assert cli.main(["--url", "https://example.test", "recipe", "oneall:check-in-status-dashboard"]) == 0
    assert cli.main(["--url", "https://example.test", "recipes", "list", "--concept", "check-in"]) == 0
    assert cli.main(["--url", "https://example.test", "recipes", "search", "attendance roster"]) == 0
    assert urls == [
        "https://example.test/recipes/oneall%3Acheck-in-status-dashboard",
        "https://example.test/recipes?concept=check-in",
        "https://example.test/search?q=attendance%20roster&limit=10&min_tier=routing_context_only&kind=recipe&detail=compact",
    ]
    capsys.readouterr()


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


def test_client_submit_infers_org_and_reads_token_file(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    row = json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))
    bundle = tmp_path / "bundle.jsonl"
    bundle.write_text(json.dumps(row) + "\n", encoding="utf-8")
    token_file = tmp_path / "token.txt"
    token_file.write_text("secret-token\n", encoding="utf-8")
    captured = {}

    def fake_post_json(url: str, payload: dict, token: str):
        captured["url"] = url
        captured["payload"] = payload
        captured["token"] = token
        return {"status": "validated"}

    monkeypatch.setattr(cli, "post_json", fake_post_json)

    exit_code = cli.main(["--url", "https://example.test", "submit", str(bundle), "--token-file", str(token_file), "--dry-run"])

    assert exit_code == 0
    assert captured["url"] == "https://example.test/submit"
    assert captured["payload"]["org_id"] == row["org_id"]
    assert captured["payload"]["dry_run"] is True
    assert captured["token"] == "secret-token"
    assert "validated" in capsys.readouterr().out


def test_client_auth_check_uses_token_file(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    token_file = tmp_path / "token.txt"
    token_file.write_text("secret-token\n", encoding="utf-8")
    captured = {}

    def fake_post_json(url: str, payload: dict, token: str):
        captured["url"] = url
        captured["payload"] = payload
        captured["token"] = token
        return {"status": "ok"}

    monkeypatch.setattr(cli, "post_json", fake_post_json)

    exit_code = cli.main(["--url", "https://example.test", "auth-check", "--org", "fixture-org", "--token-file", str(token_file)])

    assert exit_code == 0
    assert captured == {
        "url": "https://example.test/auth/check",
        "payload": {"org_id": "fixture-org"},
        "token": "secret-token",
    }
    assert "ok" in capsys.readouterr().out


def test_agent_installer_preserves_config_and_creates_backups(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    config = tmp_path / ".codex" / "config.toml"
    config.parent.mkdir(parents=True)
    config.write_text('# keep this comment\nmodel = "gpt-5"\n\n[mcp_servers.other]\nurl = "https://other.test/mcp"\n', encoding="utf-8")

    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok", "version": "test"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n\n# Rock KB Agent\n")

    exit_code = cli.main(["--url", "https://example.test", "install-agent", "--agent", "codex", "--home", str(tmp_path)])

    assert exit_code == 0
    updated = config.read_text(encoding="utf-8")
    assert "# keep this comment" in updated
    assert '[mcp_servers.rock-kb]\nurl = "https://example.test/mcp"' in updated
    assert '[mcp_servers.other]\nurl = "https://other.test/mcp"' in updated
    assert list(config.parent.glob("config.toml.rock-kb-backup-*"))
    assert (tmp_path / ".codex" / "skills" / "rock-kb-agent" / "SKILL.md").exists()
    assert '"status": "ok"' in capsys.readouterr().out


def test_agent_installer_dry_run_is_non_mutating(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n")

    exit_code = cli.main(["install-agent", "--agent", "cursor", "--home", str(tmp_path), "--dry-run"])

    assert exit_code == 0
    assert not (tmp_path / ".cursor" / "mcp.json").exists()
    output = capsys.readouterr().out
    assert '"status": "dry_run"' in output
    assert '"config_action": "would_update"' in output


def test_agent_installer_surgically_updates_json_config():
    load_client_cli()
    from rock_kb_client.installer import update_json_config

    original = '{\n    "theme": {"font": "large"},\n    "mcpServers": {\n      "other": {"url": "https://other.test/mcp"}\n    }\n}\n'

    updated = update_json_config(original, "mcpServers", "rock-kb", {"type": "http", "url": "https://kb.test/mcp"})

    parsed = json.loads(updated)
    assert parsed["theme"] == {"font": "large"}
    assert parsed["mcpServers"]["other"] == {"url": "https://other.test/mcp"}
    assert parsed["mcpServers"]["rock-kb"] == {"type": "http", "url": "https://kb.test/mcp"}
    assert '    "theme": {"font": "large"}' in updated


def test_agent_installer_preflights_all_hosts_before_writing(monkeypatch, tmp_path, capsys):
    cli = load_client_cli()
    cursor_config = tmp_path / ".cursor" / "mcp.json"
    cursor_config.parent.mkdir(parents=True)
    cursor_config.write_text('{"mcpServers": {}}\n', encoding="utf-8")
    (tmp_path / ".claude.json").write_text('{"mcpServers": ', encoding="utf-8")
    monkeypatch.setattr(cli, "get_json", lambda url: {"status": "ok"})
    monkeypatch.setattr(cli, "get_text", lambda url: "---\nname: rock-kb-agent\n---\n")

    try:
        cli.main(["install-agent", "--agent", "cursor", "--agent", "claude", "--home", str(tmp_path)])
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("malformed second config should abort installation")

    assert json.loads(cursor_config.read_text(encoding="utf-8")) == {"mcpServers": {}}
    assert not list(cursor_config.parent.glob("mcp.json.rock-kb-backup-*"))
    capsys.readouterr()
