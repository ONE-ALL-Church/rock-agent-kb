# Rock RMS General Knowledge Base

## Identity

This repository is an agent-first knowledge base for Rock RMS, combining curated Markdown with structured JSONL manifests, claims, citations, and indexes. It keeps public-safe knowledge in the tracked tree while raw transcripts, private scans, and local review artifacts stay in ignored private storage. The default posture is conservative: cite and summarize public web content, publish only reviewed distilled claims, and fail closed when privacy, licensing, or source authority is unclear.

## Quick Start

```bash
uv sync --extra dev
uv run kb status
uv run kb build --dry-run
uv run kb audit all
uv run --extra dev pytest
```

Generated content is meant to be reproducible from the registries, normalized records, reviewed claims, and CLI. For intentional rebuilds, pin `ROCK_KB_GENERATED_AT=<iso timestamp>` so generated `generated_at` metadata does not churn; standard `SOURCE_DATE_EPOCH` is also supported.

## Portable OKF Distribution

Each tagged release includes a complete, read-only Open Knowledge Format v0.1 distribution of the canonical public KB. It packages concept guides, claims, answers, recipes, Lava contexts, Rock model digests, task cards, source summaries, contribution provenance, and evidence-source policy as typed Markdown with links and checksums.

Give an agent this command to download and validate the latest release:

```bash
uvx rock-kb okf download
uvx rock-kb okf validate rock-agent-kb-okf-vX.Y.Z.zip
```

See the [OKF Distribution Runbook](docs/runbooks/okf-distribution.md) for contents, local builds, release assets, and the reviewed-import policy.

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
- `kb audit ...` - guide, license, source-policy, public-export, readiness, and all-in-one audits; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb publish ...` - public scratch export and the versioned read-only OKF distribution; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb report ...` - refresh reports and maintainer dashboards; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb tools ...` - developer utility commands; see [CLI Reference](docs/runbooks/cli-reference.md).

## Where To Go Next

- [Project goal](docs/decisions/project-goal.md) records the durable project decisions.
- [Runbooks](docs/runbooks/) explain the rebuild, media, claim, corpus, answer-pack, and audit workflows.
- [Agent manifest](agent/rock-kb-manifest.json) is the primary machine-readable entrypoint for agents.
