# Rock KB Community Onboarding

This knowledge base is public-safe Rock RMS guidance for agents. It combines source-cited official docs, release knowledge, model-map references, reviewed community claims, and clearly labeled unreviewed community submissions.

## Read The KB

Most testers should use one of two co-primary online paths. Both query the same
hosted public projection and apply the same trust and retrieval rules:

- **MCP for agents:** use when the AI client supports native HTTP MCP tools.
- **CLI for terminal testing:** use when a person, script, or terminal-based
  agent wants to run searches and local commands.

MCP does not contain better knowledge than the CLI. OKF release bundles are for
offline, pinned, bulk, or cross-system use and are not needed for ordinary
community testing.

### Recommended: Let The CLI Configure Your Agent

For Codex, Claude Code, Cursor, or OpenCode, the published CLI can install the
Rock KB skill and hosted MCP entry together. Preview the exact paths first:
This requires `uvx`; installation steps are under Option 2 below.

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

The installer detects supported agents, verifies the hosted service, preserves
unrelated configuration, and backs up existing files before changing them.
Use `--agent <name>` to select one host or `--scope project --project-dir
<path>` for a project-local install. Restart the agent after installation.

### Option 1: Connect An MCP-Capable Agent

Use the hosted MCP endpoint when your agent supports HTTP MCP. This does not
require Python or `uv` on the tester's machine:

```json
{
  "mcpServers": {
    "rock-kb": {
      "type": "http",
      "url": "https://rock-agent-kb.oneandall.church/mcp"
    }
  }
}
```

### Option 2: Test From A Terminal

Terminal agents can use the `rock-kb` CLI. The examples below use `uvx`, which
comes from the `uv` Python toolchain and runs the published PyPI package without
a manual install.

First install `uv` if `uvx` is not already available:

```bash
uvx --version
```

If that command fails, install `uv` from the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS with Homebrew, this is also fine:

```bash
brew install uv
```

Then run a first smoke test:

```bash
uvx rock-kb search "check-in labels not printing"
```

After that, use the CLI for common lookups:

```bash
uvx rock-kb get check-in
uvx rock-kb result '<result-id>'
uvx rock-kb claim '<claim-id>'
uvx rock-kb claims security-permissions --min-tier source_backed
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb recipes list
uvx rock-kb recipe oneall:check-in-status-dashboard
uvx rock-kb recipe verify oneall:check-in-status-dashboard --rock-version 18
uvx rock-kb ideas search "workflow feature request"
uvx rock-kb test-round
uvx rock-kb dashboard
```

Search is intentionally compact: it returns ranked IDs, titles, snippets,
tiers, source URLs, and ranking signals. Open only the relevant hit with
`result <result-id>`, or fetch an approved claim directly with `claim
<claim-id>`. `search --full` remains available for older one-step workflows.

For repeated use on a server or shared agent environment, install the CLI
permanently instead:

```bash
uv tool install rock-kb
rock-kb search "check-in labels not printing"
```

If your organization runs a staging copy, set:

```bash
export ROCK_KB_URL=https://your-rock-kb-service.example.org
```

### Run The Standard Church Test Round

Run `uvx rock-kb test-round` after installation and after meaningful KB
releases. It performs nine bounded public checks and prints a JSON report with
automatic pass/fail evidence. To record a complete fixed-vocabulary manual
review without sending free text, queries, or private data, use:

```bash
ROCK_KB_COHORT=external-test uvx rock-kb test-round --review --submit
```

The command asks for one of `useful`, `incorrect`, `incomplete`, `unclear`, or
`unsure` for every case.
Three cases cover imported Rock issues: a reviewed core-issue enrichment, an
official mobile fixed-release link, and conservative version applicability.

Imported issues are routing evidence, not automatically trusted knowledge.
The upstream report remains `community-unreviewed`; only separately reviewed
enrichments can carry stronger claim and authority tiers. Closed does not mean
fixed, and a reporter version does not prove that every instance is affected.
Use the test's stable result IDs with `rock-kb feedback`; use
`rock-kb report-issue` only when the KB itself malfunctions. Never add church
names, private records, logs, internal URLs, or secrets to either path.

## Understand Trust Tiers

Every search hit and claim carries authority metadata:

- `official`, `release-note-confirmed`, `rocku-confirmed`: strong public source-backed rows.
- `community-reviewed`: maintainer or trusted reviewer has approved the public-safe distilled claim.
- `community-unreviewed`: a registered organization submitted it and automated gates passed. Treat it as a lead, not authority.
- `live_verified`: a read-only verification probe confirmed the claim against a Rock instance or source surface.

Agents should cite the tier in answers and should not blend `community-unreviewed` rows into authoritative prose.

## Register Your Organization

Open a PR adding:

```text
orgs/<org-id>.yaml
```

Use `orgs/example-org.yaml` as the template. Do not include private URLs, database names, staff details, tokens, or internal runbook text.

Maintainers review registration once. After approval, your agent can submit contribution bundles with an org token issued outside git.

If you prefer a guided path, open a "Register a contributing organization" issue
and then submit the matching `orgs/<org-id>.yaml` PR after maintainer feedback.

A real registration is considered ready for hosted intake only after:

- the organization has a public-safe `orgs/<org-id>.yaml` file with `status: reviewed`;
- the maintainer has added that org's submit-token digest to the hosted `ORG_TOKEN_SHA256_JSON` secret;
- the contributor has made at least one reviewed public-safe submission or test submission through the hosted `/submit` or `kb_submit` path.

## Submit A Contribution

Prepare a JSONL bundle:

```bash
uvx rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl --org <org-id>
```

To test unreleased client changes from GitHub instead of the PyPI package, add:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb <command>
```

Valid rows must be newly written public-safe summaries. They cannot contain raw transcripts, private source paths, direct media URLs, copied proprietary text, secrets, or instance-specific private details.

Reusable implementations can be submitted as community recipes. Keep the code
in your organization's licensed public repository, then submit a `recipe`
contribution with an immutable commit pin, file hashes, adaptation points,
security, compatibility, validation, and learnings. See
`docs/community-recipes.md`.

Prioritize reusable recipes, difficult troubleshooting paths, failure modes,
version caveats, and verified workflows over broad documentation summaries.
Use `docs/community-content-priorities.md` and its candidate review template to
score prospective knowledge before spending time preparing a bundle.

On success, the hosted service opens a PR under:

```text
community-contributions/<org-id>/
```

Automated checks validate schema, attestations, source links, and leak patterns. Community material stays community-tier until reviewed.

Repository auto-merge support may be enabled, but contribution PRs still require
all runtime gates to pass. Auto-merge is attempted only when the hosted Worker
flag allows it, the org registry sets `intake.auto_merge_allowed: true`, and the
PR changes exactly the expected bundle path for that org. Otherwise the PR stays
review-required.

Use `rock-kb dashboard` to see public operational counts for community-unreviewed intake rows, review queues, source-conflict prompts, evaluation status, and aggregate telemetry. Evaluation traffic is reported separately from CLI, MCP, browser, and unknown clients. It does not expose private corpus data, raw query text, or free-text feedback.

After opening a search result, agents can report structured quality feedback:

```bash
uvx rock-kb feedback '<result-id>' --rating -1 --reason wrong_route
```

If the KB service, MCP tool, CLI, schema, authentication, or retrieval path
itself fails, use the separate structured issue reporter:

```bash
uvx rock-kb report-issue --failure-type retrieval --operation search --error-code search_unavailable --description "Search returned a temporary service failure." --redaction-attested
```

Never include logs, queries, secrets, private paths, or private Rock data. The
report is deduplicated, returns a stable report ID, and waits for maintainer
review rather than opening a GitHub issue automatically.

## Agent Prompt Starter

Use this in your local agent instructions:

```text
Before answering a Rock RMS operational question, search the Rock KB first.
Prefer official, release-note-confirmed, source-code-confirmed, and community-reviewed rows.
Use community-unreviewed rows only as leads and label them as unreviewed.
When you discover a reusable public-safe Rock RMS insight, write a distilled contribution row with source URLs and submit it through rock-kb submit or the kb_submit MCP tool.
Never submit private person data, internal URLs, raw transcripts, screenshots with private state, SQL exports, tokens, or copied proprietary source text.
```

For a reusable file version, use
`docs/templates/agent-contributor-instructions.md`.

For agents that support Codex-style skills, use the reusable skill package at
`docs/templates/rock-kb-agent/`. It teaches agents how to search the hosted KB,
respect trust tiers, use stable-first model-map references, and submit
public-safe contribution bundles.
