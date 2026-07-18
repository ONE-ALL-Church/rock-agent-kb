# rock-kb

Thin terminal client for the public Rock RMS agent knowledge base.

## Quick Start

The published client is available from PyPI as `rock-kb`. It queries the same
hosted public projection as the MCP server. Use MCP when an agent host supports
native typed tools; use this CLI for terminal agents, scripts, local validation,
and environments without MCP support. Neither interface has better knowledge.

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

The same client manages updates with source provenance and an exact hosted
SHA-256:

```bash
uvx rock-kb skill check
uvx rock-kb skill update
uvx rock-kb skill status --format json
uvx rock-kb skill policy notify
```

`notify` is the default. A human can explicitly choose `auto` for a user-level
installation or `pinned` to remain on the installed version. Project-level
automatic updates are rejected so the changed skill can be reviewed through
Git. `skill check --if-due` and ordinary managed CLI use limit passive checks
to once per 24 hours. Restart or reload the agent when an applied update
reports `restart_required: true`.

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
uvx rock-kb recipe verify oneall:check-in-status-dashboard --rock-version 18
uvx rock-kb issues search "Azure blob CPU issue"
uvx rock-kb issues list --repository core --state open --version 19.2
uvx rock-kb issue 6919
uvx rock-kb issues assess instance-profile.json
uvx rock-kb issues watch instance-profile.json
uvx rock-kb issues plan 6919
uvx rock-kb test-round
uvx rock-kb feedback '<result-id>' --rating -1 --reason outdated
uvx rock-kb report-issue --failure-type retrieval --operation search --error-code search_unavailable --description "Search returned a temporary service failure." --redaction-attested
uvx rock-kb dashboard
uvx rock-kb mcp-config
uvx rock-kb skill status --format json
```

Churches participating in the public external test can opt into aggregate
cohort reporting without identifying their church or users:

```bash
ROCK_KB_COHORT=external-test uvx rock-kb test-round
uvx rock-kb --cohort external-test mcp-config
```

The second command includes the same bounded header in the generated MCP
configuration. Maintainers can use `ROCK_KB_COHORT=maintainer`. The service
accepts only `external-test` or `maintainer`; omitted or invalid values become
`unattributed`. This self-declared marker is not authentication and never
contains an organization name, installation ID, user ID, or query text.

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

`recipe verify` checks immutable source hashes and declared compatibility. It
uses the hosted service's immutable-byte cache and GitHub Contents API fallback
when needed; it does not execute recipe code or change Rock. `feedback` accepts
only a fixed rating and reason; it does not send free-text comments or query
text. `report-issue` is for failures in the KB service, MCP, CLI, schema,
authentication, or retrieval path. Its description is limited and must be
redaction-attested; never include logs, queries, secrets, private paths, or
private Rock data. It returns a stable report ID and does not create a GitHub
issue automatically.

Rock product issue commands are read-only and separate from `report-issue`,
which reports a malfunction in the KB itself. Product issue reports are routing
evidence, not proof of local impact or cause. `issues assess` accepts only a
bounded JSON profile containing versions, platforms, concept IDs, and capability
names; never include logs, queries, private identifiers, or person data.
`issues watch` follows every assessment page and stores an owner-only local
snapshot so later runs can report issue applicability, remediation, and
revalidation changes. The snapshot defaults under the user state directory;
override it with `--state`, preview with `--no-write`, or replace the baseline
with `--reset`. Only the bounded profile is sent to the hosted service. The
snapshot is never uploaded and does not retain the profile itself.

`test-round` runs the same bounded public test pack used with the external
church cohort. It checks service health, exact Model Map lookup, Lava context
retrieval, a reviewed recipe, semantic troubleshooting, core and mobile issue
trust boundaries, version-aware issue assessment, and a deliberate no-answer
case. The JSON report contains stable public result IDs plus a manual review
question for each case. It sends only the built-in public test queries and
profile; it never collects church identifiers or private instance data.

## Offline And Portable Access

OKF is a secondary distribution for offline operation, pinned releases, bulk
analysis, local indexing or vectorization, archival, and cross-system
interchange. Do not download an OKF bundle merely to answer an ordinary online
question through this client.

Download, inspect, and verify a full or compact core read-only release without
cloning the repository:

```bash
uvx rock-kb okf download --profile core
uvx rock-kb okf inspect rock-agent-kb-okf-core-vX.Y.Z.zip
uvx rock-kb okf conformance third-party-okf.zip
uvx rock-kb okf verify rock-agent-kb-okf-core-vX.Y.Z.zip
```

Use `core` as the normal starting point for a smaller local agent index. Use
`full` when a downstream system needs lossless public records, Rock issue
routing data, source summaries, and contribution provenance. Options include
`--format tar.gz`, `--version X.Y.Z`, and `--destination <path>`. Downloads
require published SHA-256 evidence. `conformance` handles generic OKF bundles;
`verify` applies Rock release integrity and safety rules. The client does not
import OKF into trusted knowledge.

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
