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
uvx rock-kb claims workflows --min-claim-tier source_backed
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text --root CheckoutDateTime
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
uvx rock-kb --version
uvx rock-kb telemetry status
uvx rock-kb telemetry enable --cohort community --consent-attested
uvx rock-kb feedback '<result-id>' --rating -1 --reason outdated
uvx rock-kb outcome '<result-id>' --outcome partially_useful --reason incomplete --consent-attested
uvx rock-kb report-issue --failure-type retrieval --operation search --error-code search_unavailable --description "Search returned a temporary service failure." --redaction-attested
uvx rock-kb dashboard
uvx rock-kb freshness
uvx rock-kb mcp-config
uvx rock-kb skill status --format json
```

After the human accepts consent notice version 3, a participating installation
can opt into anonymous field validation without identifying its church or users:

```bash
uvx rock-kb telemetry enable --cohort community --consent-attested
uvx rock-kb install-agent
```

The client creates a private random `rkbi_...` marker; `telemetry status` does
not print its value. The service stores only a one-way hash. `install-agent`
adds the marker and fixed
cohort to supported user-scoped MCP configurations; restart the host afterward.
Use `external-test` for a formal public test round and `maintainer` only for
maintainer work. These self-declared labels are not authentication and must
never contain a church, organization, or person name. Disable participation
with `uvx rock-kb telemetry disable`, rerun `install-agent`, and restart the
host. Treat user-scoped agent configuration as private. Project-scoped MCP
configuration never receives the marker.

The same opt-in enables the experimental canonical retrieval canary. Legacy
retrieval remains the default:

```bash
uvx rock-kb --projection canonical-canary search "content channel item permissions"
uvx rock-kb --projection canonical-canary result '<result-id>'
uvx rock-kb --projection canonical-canary outcome '<result-id>' \
  --outcome useful \
  --reason answered \
  --consent-attested
uvx rock-kb compare "content channel item permissions" --category version_sensitive
uvx rock-kb compare "content channel item permissions" --category version_sensitive \
  --review --submit --consent-attested
```

`--projection` is a global option and therefore appears before the command.
Only `search`, `result`, and `outcome` accept the global canary option. Use the
same projection for all three so an outcome is attached to the exact projection
that produced the result. `compare` instead queries both projections, randomizes
them as A/B choices, and never labels either option. The service rejects canary
or comparison requests without a private anonymous marker and the fixed
`external-test` or `maintainer` cohort.

MCP clients use the installed private headers and pass
`projection: "canonical-canary"` to `kb_search`, `kb_get_result`, and
`kb_outcome`. The canary does not receive or store query text, the raw marker,
organization or person identity, IP address, logs, secrets, or Rock data.
Canary results may differ from legacy results, but they do not carry a higher
authority tier merely because they came from the canonical projection.

Consent notice version 3 adds comparison-specific retention. A pending
comparison is usable for 30 minutes and stores only a one-way installation hash,
fixed category/cohort, paired public result IDs, projection versions, and the
randomized A/B assignment. Expired rows are purged on the next comparison start,
review attempt, or dashboard read. A submitted review adds one fixed preference
and up to three compatible reason codes. The question is used transiently for
both searches and is never retained. Version 2 state is not accepted by the
updated client; ask again and rerun `telemetry enable` before participating.

For repeated use on a server or agent host, install the CLI permanently:

```bash
uv tool install rock-kb
rock-kb search "check-in labels not printing"
rock-kb mcp-config
```

`rock-kb mcp-config` prints the hosted direct HTTP MCP config. It does not start
a local server. Direct tools are the default and are best for normal search and
exact lookup. The same URL supports stateless MCP `2026-07-28` and ordinary
2025 clients automatically; no session option is needed.

`rock-kb mcp-config --mode code` prints the opt-in experimental Cloudflare Code
Mode endpoint for composed read-only calls. Code Mode excludes feedback,
usefulness outcomes, Lava-context verification, malfunction reports,
test-review submission, and knowledge submission; it is not a more current
knowledge source.

Search output is compact by default and excludes routing-only rows unless
`--min-claim-tier routing_context_only` is explicitly requested. It returns
stable IDs, inferred intent, snippets, trust tiers, version-scope state, source
URLs, and rounded scores. Detailed ranking signals require `--debug`. Symptom
queries prefer task cards and troubleshooting nodes. Use `rock-kb result <id>`
or `rock-kb claim <claim-id>` for full detail, and use `search --full` only for
compatibility with workflows that still need full rows in one response.

Claim listing is paginated:

```bash
uvx rock-kb claims check-in --authority-tier official --limit 25
uvx rock-kb claims workflows --min-claim-tier source_backed --rock-version 19.2
```

Use the returned `next_offset` while `has_more` is true. Authority and claim
tiers are different vocabularies; do not pass `official` as a claim tier.

For Lava merge-field questions, use `lava-context list` to discover an exact
rendering-surface ID and `lava-context get` to retrieve its grouped roots,
conditions, source version, completeness, and Model Map links. Use generic
search only when the surface is unknown. A complete source snapshot does not
guarantee that every conditional root is populated in every request.

`recipe verify` checks immutable source hashes and declared compatibility. It
uses the hosted service's immutable-byte cache and GitHub Contents API fallback
when needed; it does not execute recipe code or change Rock. `feedback` accepts
only a fixed result-quality rating and reason. With anonymous telemetry enabled,
`outcome` accepts `useful`, `partially_useful`, or `not_useful` plus one to three
compatible fixed reason codes for a completed task. Neither sends free-text
comments or query text. `report-issue` is for failures in the KB service, MCP, CLI, schema,
authentication, or retrieval path. Its description is limited and must be
redaction-attested; never include logs, queries, secrets, private paths, or
private Rock data. It returns a stable report ID and does not create a GitHub
issue automatically.

Rock product issue commands are read-only and separate from `report-issue`,
which reports a malfunction in the KB itself. Product issue reports are routing
evidence, not proof of local impact or cause. `issues assess` accepts only a
bounded JSON profile containing versions, platforms, concept IDs, capability
names, and public configuration identifiers; never include logs, queries,
private identifiers, configuration values, or person data. Use `--scope open`
by default, `--scope historical-unresolved` for relevant closed reports, or
`--scope all-relevant` for upgrade preparation.

The V2 assessment exposes matched, excluded, and unknown signals; compact
evidence; remediation; evidence-backed risk; source freshness; and available
read-only verification. Risk remains `unrated` without an upstream priority
label or current reviewed risk evidence. `issues watch` follows every
assessment page and stores an owner-only, scope-specific local snapshot so
later runs can report applicability, routing, risk, remediation, freshness,
population, exclusion, and revalidation changes. The snapshot defaults under the user state directory;
override it with `--state`, preview with `--no-write`, or replace the baseline
with `--reset`. Only the bounded profile is sent to the hosted service. The
snapshot is never uploaded and does not retain the profile itself.

`test-round` runs the same bounded public test pack used with the external
church cohort. It checks service health, exact Model Map lookup, Lava context
retrieval, a reviewed recipe, semantic troubleshooting, core and mobile issue
trust boundaries, version-aware issue assessment, and a deliberate no-answer
case. The JSON report contains stable public result IDs plus a manual review
question for each case. It sends only the built-in public test queries and
profile; it never collects church identifiers or private instance data. The
client also emits bounded `started` and `completed` funnel counts with its
cohort and automatic pass/fail status. This dedicated test-round path does not
retain an installation marker, query text, or private Rock data.

`freshness` reports the authoritative hosted daily/weekly workflow schedule
state and each source's last check, last content change, result count, content
hash, and status. A failed status means a scheduled workflow was missed or a
required source is failed, missing, or genuinely overdue.

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
uv run --project clients/python rock-kb lava-context list --family check-in-label
uv run --project clients/python rock-kb lava-context get check-in-label-family-dynamic-text
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
