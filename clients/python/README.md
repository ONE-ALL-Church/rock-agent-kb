# rock-kb

Thin terminal client for the public Rock RMS agent knowledge base.

Current public install from GitHub, before the PyPI package is released:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "check-in labels not printing"
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb get check-in
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb claims workflows --min-tier source_backed
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb dashboard
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb mcp-config
```

After the client is published to PyPI, the shorter package-registry form works:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

From a local `rock-agent-kb` checkout before the package is published:

```bash
uv run --project clients/python rock-kb search "check-in labels not printing"
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --org <org-id>
```

Set `ROCK_KB_URL` to point at a staging service. Set `ROCK_KB_TOKEN` when submitting bundles.

Hosted submission is token-gated per organization. If `rock-kb submit` reports
that `ROCK_KB_TOKEN` is required, ask a Rock KB maintainer to issue a token for
the reviewed `orgs/<org-id>.yaml` registration. Store the token in an
environment variable, CI/app secret, or local secret store such as macOS
Keychain; do not save it in repo files.
