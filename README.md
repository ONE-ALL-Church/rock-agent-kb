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
- `kb modelmap ...` - stable/latest Rock model-map build, stamping, and diffs; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb audit ...` - guide, license, source-policy, public-export, readiness, and all-in-one audits; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb publish ...` - public export and legacy public-repo push commands; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb report ...` - refresh reports and maintainer dashboards; see [CLI Reference](docs/runbooks/cli-reference.md).
- `kb tools ...` - developer utility commands; see [CLI Reference](docs/runbooks/cli-reference.md).

## Where To Go Next

- [Project goal](docs/decisions/project-goal.md) records the durable project decisions.
- [Runbooks](docs/runbooks/) explain the rebuild, media, claim, corpus, answer-pack, and audit workflows.
- [Agent manifest](agent/rock-kb-manifest.json) is the primary machine-readable entrypoint for agents.
