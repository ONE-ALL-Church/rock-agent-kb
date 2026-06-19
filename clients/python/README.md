# rock-kb

Thin terminal client for the public Rock RMS agent knowledge base.

Install and run the published client from PyPI with `uvx`:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

To test unreleased client changes directly from GitHub, use:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "check-in labels not printing"
```

From a local `rock-agent-kb` checkout:

```bash
uv run --project clients/python rock-kb search "check-in labels not printing"
uv run --project clients/python rock-kb model-map list
uv run --project clients/python rock-kb model group --fields identity,required,relationships,diffs
uv run --project clients/python rock-kb model group --property Members
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --org <org-id>
```

Set `ROCK_KB_URL` to point at a staging service. Set `ROCK_KB_TOKEN` when submitting bundles.

Hosted submission is token-gated per organization. If `rock-kb submit` reports
that `ROCK_KB_TOKEN` is required, ask a Rock KB maintainer to issue a token for
the reviewed `orgs/<org-id>.yaml` registration. Store the token in an
environment variable, CI/app secret, or local secret store such as macOS
Keychain; do not save it in repo files.
