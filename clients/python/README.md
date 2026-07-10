# rock-kb

Thin terminal client for the public Rock RMS agent knowledge base.

## Quick Start

The published client is available from PyPI as `rock-kb`.

For one-off use, run it with `uvx`. `uvx` is part of the `uv` Python toolchain;
it downloads or reuses a cached copy of the package and runs the command in an
isolated environment.

Check whether `uvx` is installed:

```bash
uvx --version
```

If it is missing, install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:

```bash
brew install uv
```

Then run a smoke test:

```bash
uvx rock-kb search "check-in labels not printing"
```

To configure a detected Codex, Claude Code, Cursor, or OpenCode installation
with both the hosted MCP server and the Rock KB skill:

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

The installer changes only the `rock-kb` MCP entry and the
`rock-kb-agent/SKILL.md` path. It backs up existing files before writing and
reports every path it touched. Use `--agent codex` (repeatable) to select hosts
explicitly, or `--scope project --project-dir <path>` for project-local setup.

Common commands:

```bash
uvx rock-kb get check-in
uvx rock-kb result '<result-id>'
uvx rock-kb claim '<claim-id>'
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb recipes list
uvx rock-kb recipes search "registration attendance dashboard"
uvx rock-kb recipe oneall:check-in-status-dashboard
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

For repeated use on a server or agent host, install the CLI permanently:

```bash
uv tool install rock-kb
rock-kb search "check-in labels not printing"
rock-kb mcp-config
```

`rock-kb mcp-config` prints the hosted HTTP MCP config. It does not start a
local server.

Search output is compact by default. It returns stable IDs, snippets, trust
tiers, source URLs, scores, and ranking signals. Use `rock-kb result <id>` or
`rock-kb claim <claim-id>` for full detail. Use `search --full` only for
compatibility with workflows that still need full rows in one response.

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
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb auth-check --org <org-id>
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --dry-run
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl
```

Set `ROCK_KB_URL` to point at a staging service. Set `ROCK_KB_TOKEN` when submitting bundles. `rock-kb submit` infers `--org` from the bundle when all rows use the same `org_id`.

Secret-file usage is also supported, which is often easier for hosted agents:

```bash
rock-kb auth-check --org <org-id> --token-file /run/secrets/rock-kb-token
rock-kb submit bundle.jsonl --token-file /run/secrets/rock-kb-token --dry-run
rock-kb submit bundle.jsonl --token-file /run/secrets/rock-kb-token
```

Hosted submission is token-gated per organization. If `rock-kb submit` reports
that `ROCK_KB_TOKEN` is required, ask a Rock KB maintainer to issue a token for
the reviewed `orgs/<org-id>.yaml` registration. Store the token in an
environment variable, CI/app secret, mounted secret file, or local secret store
such as macOS Keychain; do not save it in repo files.
