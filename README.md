# Rock RMS General Knowledge Base

## Identity

This repository is an agent-first knowledge base for Rock RMS, combining curated Markdown with structured JSONL manifests, claims, citations, and indexes. It keeps public-safe knowledge in the tracked tree while raw transcripts, private scans, and local review artifacts stay in ignored private storage. The default posture is conservative: cite and summarize public web content, publish only reviewed distilled claims, and fail closed when privacy, licensing, or source authority is unclear.

## Use With An Agent

For ordinary online questions, use one of the two hosted interfaces. They read
the same current public projection and apply the same trust tiers and retrieval
rules:

- **MCP** is the natural choice when an agent host supports HTTP MCP and can use
  typed tools directly.
- **CLI** is the natural choice for terminal agents, scripts, local validation,
  and clients without MCP support.

Configure a supported agent host with the Rock KB skill and hosted MCP entry:

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

The installed skill is versioned. Check without changing agent configuration
or skill content, apply an approved update, or inspect the persisted policy and
source hash:

```bash
uvx rock-kb skill check
uvx rock-kb skill update
uvx rock-kb skill status --format json
```

The default policy is `notify`; `skill policy auto` requires explicit human
permission and is user-scope only, while `skill policy pinned` holds the
installed version. See [Agent Skill Lifecycle](docs/agent-skill-lifecycle.md).

Or query the same hosted knowledge from a terminal:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb result '<result-id>'
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text
uvx rock-kb freshness
uvx rock-kb test-round
```

MCP is not a higher-quality knowledge source than the CLI; it is a more native
tool interface for compatible agents. The default `/mcp` endpoint exposes
direct typed tools and is the right choice for normal use. An experimental
read-only Cloudflare Code Mode endpoint is available for agents that need to
compose several dependent KB calls, loops, or filters in one operation:

```bash
uvx rock-kb mcp-config --mode code
```

Code Mode excludes feedback, issue-report, test-review, and contribution
writes. It does not have better knowledge and should not replace direct MCP for
single searches or exact lookups. Do not download an OKF bundle merely to
answer an ordinary online question.

## Portable OKF Distribution

Each tagged release includes complete `full` and compact `core` read-only Open Knowledge Format v0.1 distributions of the canonical public KB. OKF is a secondary portability layer for offline operation, pinned snapshots, bulk analysis, local indexing or vectorization, archival, and cross-system interchange. It is not the default search interface.

When one of those use cases applies, download and validate a release:

```bash
uvx rock-kb okf download --profile core
uvx rock-kb okf verify rock-agent-kb-okf-core-vX.Y.Z.zip
```

Use the `core` profile for a smaller local agent corpus. Use `full` when a
downstream system needs lossless public records, Rock issue routing data, source
summaries, and contribution provenance. Use `okf conformance` for any
third-party OKF bundle and `okf verify` for the stricter Rock release integrity,
profile, licensing, and public-safety checks.

See the [OKF Distribution Runbook](docs/runbooks/okf-distribution.md) for contents, local builds, release assets, and the reviewed-import policy.

## Maintainer Quick Start

```bash
uv sync --extra dev
uv run kb status
uv run kb build --dry-run
uv run kb audit all
uv run --extra dev pytest
```

Generated content is meant to be reproducible from the registries, normalized records, reviewed claims, and CLI. For intentional rebuilds, pin `ROCK_KB_GENERATED_AT=<iso timestamp>` so generated `generated_at` metadata does not churn; standard `SOURCE_DATE_EPOCH` is also supported.

## Reporting And Product Issues

Agents can report a malfunction in the KB service, MCP, CLI, schema,
authentication, or retrieval path through the bounded structured reporter. See
the [Structured Issue Reporting Runbook](docs/runbooks/issue-reporting.md).

Agents can also search public Rock core and mobile product issues, compare their
structured version evidence with a bounded instance profile, and generate a
read-only multi-agent investigation plan. The published CLI can keep a private
local issue-assessment baseline with `uvx rock-kb issues watch
instance-profile.json --scope open` and report applicability, routing, risk,
remediation, and revalidation changes on later runs. Assessments expose source
freshness and evidence-backed risk; no severity is inferred when evidence is
absent. This is a separate surface from KB malfunction reporting. See the
[Rock Issue Intelligence Runbook](docs/runbooks/rock-issue-intelligence.md).

For explicit feature-gap and roadmap research, agents can search the bounded
Rock Community Ideas metadata catalog with `uvx rock-kb ideas search "<feature
request>"` or the dedicated MCP tools. Ideas remain unreviewed routing signals;
even a `Complete` label must be corroborated with documentation, release notes,
source, or live verification. Exact Idea and Issue retrieval can expose
evidence-backed typed links among Ideas, concepts, model maps, official release
records, and explicitly referenced issues. See the [Rock Ideas Intelligence Runbook](docs/runbooks/rock-ideas-intelligence.md).

Churches can run `uvx rock-kb test-round` for the standard bounded public test
pack. It includes exact retrieval, a no-answer boundary, and three imported
issue checks. Imported reports remain unreviewed routing evidence unless a
separate public enrichment has passed review.

Anyone can inspect the authoritative scheduled-refresh and source state with
`uvx rock-kb freshness`. It reports workflow schedule health separately from
each source's last check, last content change, result count, content hash, and
check status. It does not expose private source content or maintainer paths.

The reusable agent skill asks the human once whether anonymous field validation
may be enabled and remembered privately. With consent, an agent can submit
fixed-vocabulary result-quality feedback and completed-task usefulness outcomes
against public result IDs. The service stores only a one-way hash of a random
installation marker; it does not retain questions, organizations, people, IP
addresses, free text, logs, or Rock data. This standing permission never covers
malfunction reports, test-round submissions, public contributions, or PRs. See
[community onboarding](docs/community-onboarding.md#let-your-agent-provide-ongoing-feedback)
and the [field-validation runbook](docs/runbooks/field-validation.md).

## Contribute

The easiest path is a source suggestion: copy `source-suggestions/SUGGESTION_TEMPLATE.md` to `source-suggestions/<org-id>/<topic>.md`, fill it in, and open a PR that only changes that folder.

Normal GitHub PR contributions do not need a Rock KB submit token. Hosted agent submission uses a per-organization token after the organization is reviewed in `orgs/<org-id>.yaml`; agents can check the token with `rock-kb auth-check --org <org-id>` and test with `rock-kb submit bundle.jsonl --dry-run`.

For reviewed public-safe knowledge, generate a starter bundle row:

```bash
python3 scripts/new_contribution.py \
  --org-id your-org \
  --org-name "Your Org" \
  --concept workflows \
  --type troubleshooting_pattern \
  --title "Workflow launch triage pattern" \
  --summary "When a workflow does not launch, first verify the trigger, active workflow type, entity context, action logs, and idempotency of notifications or webhooks before changing configuration." \
  --source-url https://community.rockrms.com/documentation \
  --needs-live-verification \
  --redaction-reviewed \
  --license-attested
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full public-safety rules.

## Layout

- `sources/` - source catalog, license posture, crawl strategy, refresh cadence, and preferred tooling.
- `data/` - gitignored raw manifests, normalized records, private media, review queues, indexes, and local rebuild state.
- `claims/` - public-safe approved claim graph generated from reviewed source-backed promotions.
- `knowledge/` - curated and generated Markdown organized by Rock topic, concept, source, and model-map area.
- `concepts/` - concept definitions, keywords, subguides, and source weighting.
- `agent/` - generated agent entrypoints, answer pack, topic indexes, release indexes, and citation maps.
- `contributions/` - reviewed public contribution bundles that can feed the claim graph.
- `community-contributions/` - outside-org public intake bundles.
- `source-suggestions/` - outside-org public source suggestion intake.
- `docs/` - maintainer goals, decisions, runbooks, and point-in-time review notes.
- `tools/` - helper scripts and local tooling support.
- `src/rock_kb/` - CLI and pipeline implementation.
- `tests/` - regression tests for the pipeline, audits, CLI surface, and source transformations.

## Command Groups

- `kb status` / `kb build` - pipeline status, stale-stage planning, dry runs, and deterministic rebuilds; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb sources ...` - source registry, discovery, fetch, normalize, summarize, refresh, endpoint probing, and source scans; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb extract ...` - targeted Markdown extraction and extractor diagnostics; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb media ...` - private media discovery, transcription, sidecars, review candidates, promotion, and Gemma enrichment; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb claims ...` - claim validation and live-verification planning; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb corpus ...` - private corpus portability, audit, sync, and rebuild verification; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb private ...` - private-source scanning, distillation, review reporting, staleness, and impact checks; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb contributions ...` - contribution bundle creation, validation, promotion, and import; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb concepts ...` - concept listing, authored synthesis, and hydration; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb modelmap ...` - stable/latest Rock model-map API fetch, build, stamping, and diffs; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb lava ...` - pinned Lava context source refresh, grouped exact retrieval, candidate discovery, and extension validation; see [Lava Context Directory](docs/runbooks/lava-context-directory.md).
- `kb audit ...` - guide, license, source-policy, public-export, readiness, and all-in-one audits; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb publish ...` - public scratch export and the versioned read-only OKF distribution; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb report ...` - refresh reports and maintainer dashboards; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb tools ...` - developer utility commands; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb issues ...` - refresh, validate, inspect, assess, and plan investigations for public Rock issue metadata.
- `kb ideas ...` - refresh, validate, inspect, and route public Rock Ideas lifecycle metadata.

## Where To Go Next

- [Project goal](docs/decisions/project-goal.md) records the durable project decisions.
- [Runbooks](docs/runbooks/) explain the rebuild, media, claim, corpus, answer-pack, and audit workflows.
- [Agent manifest](agent/rock-kb-manifest.json) is the primary machine-readable entrypoint for agents.
