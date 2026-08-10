# Source Scan And Rebuild Orchestration Runbook

This runbook describes the repeatable source-refresh path for the Rock General Knowledge Base. The orchestration layer does not replace the source registry, normalized records, claim graph, media review path, concept guides, answer pack, public export, or audits. It coordinates a lightweight daily check for daily-cadence sources and a comprehensive weekly refresh so both paths remain reviewable.

## Normal Flow

1. Capture the current source snapshot.

```bash
uv run kb sources scan \
  --output-dir data/review/source-scan-pre \
  --snapshot-output data/review/source-scan-pre/source-snapshot.json
```

2. Refresh source data without rebuilding public artifacts yet.

```bash
uv run kb sources refresh \
  --baseline-snapshot data/review/source-scan-pre/source-snapshot.json \
  --skip-indexes
```

The refresh also seeds bounded discovery from the current normalized records.
Passing the pre-refresh snapshot protects older valid pages when a changed site
navigation tree no longer reaches them within the crawl limit. The fetch stage
still removes URLs that no longer return usable source pages.

3. Compare refreshed source state to the pre-refresh snapshot.

```bash
uv run kb sources scan \
  --baseline-snapshot data/review/source-scan-pre/source-snapshot.json \
  --source-status data/review/source-scan/source-refresh-status.json \
  --output-dir data/review/source-scan
```

This writes:

- `data/review/source-scan/source-scan-report.json`
- `data/review/source-scan/source-scan-rows.jsonl`
- `data/review/source-scan/source-scan-summary.md`
- `data/review/source-scan/source-snapshot.json`

Classify every registered source against the cadence in
`sources/registry.yaml` and the age limits in
`sources/freshness-policy.yaml`:

```bash
uv run kb sources freshness \
  --baseline-snapshot data/review/source-scan-pre/source-snapshot.json \
  --source-status data/review/source-scan/source-refresh-status.json \
  --strict
```

The report classifies sources as `current`, `due_soon`, `overdue`, `failed`,
`missing`, or `manual`. Daily sources may be at most 48 hours old, weekly
sources 216 hours, and monthly sources 840 hours. Manual sources are reported
without blocking refresh. It also writes
`data/review/source-freshness/source-observations.json`, which records
`last_checked_at`, `content_changed_at`, `result_count`, aggregate
semantic `content_hash`, and the check `status` independently. The hash uses a
normalized summary hash plus stable routing metadata when available, with the
raw normalized content hash as a fallback; this prevents dynamic page chrome
from appearing as a content change. A successful check with no source delta advances `last_checked_at` while preserving
`content_changed_at`. Rock core and mobile issue observations use
`data/review/rock-issues/checkpoint.json` for the successful sync check time and
`agent/rock-issue-summary.json` for the upstream update time, repository counts,
and catalog hash instead of expecting normalized source files. Scheduled
workflows cache the previous observation file, upload the
freshness and scan reports, and fail when a required source is failed, missing,
or overdue.

Rockumentation API records use a semantic article hash rather than the complete
Obsidian initialization response. The hash includes normalized article text,
canonical URL, article identity, documentation revision metadata, and stable
configuration fields; it excludes request traces, preference timestamps, and
render-shell metadata. Static fallback pages likewise hash normalized title and
content rather than volatile HTML. Hydration uses the same rule. The API client
retries a bounded transient invalid response before falling back, which prevents
one failed request from silently changing an article's canonical identity. A
source-parser change touching these rules should be tested with two complete
refreshes whose sorted `(record ID, content hash)` sets are identical.
Canonical source-summary identity also excludes only volatile `retrieved_at`;
summary text, semantic source hashes, and routing metadata remain significant.
If that boundary changes hashes for an already reviewed migration without any
semantic change, use the fail-closed `source-native-migration-rebind` command.
Do not reuse the prior review when source text, routing, relationships, artifact
content, or identity changed.

After validation, each scheduled workflow publishes its owned rows to the
hosted D1 operations projection with `kb record-source-freshness`. This is the
authoritative public snapshot used by `/operations/freshness`, the operations
dashboard, CLI `freshness`, and MCP `kb_get_freshness`. The snapshot stores
workflow schedule state independently from source state, so an unchanged
source is still visibly checked and a missed workflow is not mistaken for a
content change. `sources/freshness-policy.yaml` is the single ownership policy:
every registered source must resolve to exactly one workflow. Publishing rejects
foreign or omitted owned sources, and the D1 upsert guard prevents later stale
observations from decreasing `last_checked_at` or `content_changed_at`.

Source freshness and deployed projection freshness are separate states. For
typed catalogs that can be compared exactly, currently Rock GitHub issues and
Rock Community Ideas, the service projection records the normalized source
hash and row count used at build time. `/operations/freshness`, CLI
`freshness`, and MCP `kb_get_freshness` compare those values with the latest
successful source observation. `source_status: ok` with
`projection_status: deployment_lag` means the upstream refresh succeeded but
the refreshed rows have not yet been deployed. Do not describe that state as a
current hosted KB. A matching count alone is insufficient; both count and
content hash must match.

4. Inspect the current build status and dry-run action plan.

```bash
mkdir -p data/review/rebuild-plan
uv run kb status > data/review/rebuild-plan/status.txt
uv run kb build --dry-run > data/review/rebuild-plan/build-dry-run.json
```

This writes:

- `data/review/rebuild-plan/status.txt`
- `data/review/rebuild-plan/build-dry-run.json`
- `data/review/rebuild-plan/pull-request-body.md` in the scheduled workflow

5. Build the maintainer refresh dashboard only when a rebuild-plan report is available.

```bash
uv run kb report dashboard \
  --scan-report data/review/source-scan/source-scan-report.json \
  --rebuild-plan data/review/rebuild-plan/rebuild-plan-report.json \
  --evaluation-report agent/evaluation-report.json \
  --output-dir data/review/refresh-dashboard
```

This writes:

- `data/review/refresh-dashboard/refresh-dashboard-report.json`
- `data/review/refresh-dashboard/refresh-dashboard-rows.jsonl`
- `data/review/refresh-dashboard/refresh-dashboard-summary.md`

The grouped workflow uses `status.txt`, `build-dry-run.json`, and the source-scan summary as the primary maintainer triage surface. The dashboard command remains useful when a compatible rebuild-plan report already exists.

6. Run deterministic rebuild work through the pipeline engine.

```bash
uv run kb status
uv run kb build --dry-run
ROCK_KB_GENERATED_AT=<iso timestamp> uv run kb build
uv run kb status
```

Use targeted `uv run kb build --stage <stage>` only when you intentionally want one stale stage and its stale upstream dependencies. Do not hand-maintain a stage-by-stage rebuild list in this runbook; the stage graph is the source of truth for ordering and manual gates.

7. Handle reviewer or local-Codex work when the plan flags it.

- New media or pending transcription: transcribe, optionally run Gemma enrichment, write public-safe rewrites, and promote only explicitly reviewed media claims.
- Claim promotion: review candidates manually; never auto-promote unreviewed claims from source-scan output.
- Live verification: run read-only probes before treating affected operational claims as answer-ready.
- Taxonomy review: run `uv run kb concepts audit`. Documentation branches are
  structured routing signals; they do not automatically become concepts.
- Authored guide synthesis: first hydrate and inspect one bounded concept pack.
  Then run `uv run kb concepts synthesize --concept <concept> --hydrate-sources
  --profile comprehensive --model gpt-5.6-sol --reasoning-effort xhigh`
  locally with Codex/reviewer oversight, followed by `uv run kb build --stage
  guide-intel`.
- The versioned synthesis prompt under `docs/prompts/` makes approved
  answer-bearing claims the factual spine. Routing-only claims may locate
  evidence but may not become guide facts.
- Hydrated public GitHub snippets must carry immutable commit references.
  Source code can clarify implementation, but it does not prove an
  installation's configuration.
- Run live-instance verification only when installed schema, configuration,
  version/plugin applicability, existence/count checks, or issue reproduction
  materially affects the answer. Keep it as a separate bounded read-only
  review. Promote only a reviewed public-safe conclusion, never raw SQL output
  or private Rock data.
- Pilot a changed model, prompt, or evidence shape on one high-value concept and
  compare guide quality and retrieval before regenerating every guide.
- Source conflicts: review `agent/source-conflicts.jsonl` and related claim-review queues before changing public answer prose.
- Open-question backlog: after every meaningful source scrape, transcript batch, media promotion, claim promotion, or guide synthesis run, rebuild guide intel for affected concepts and compare `knowledge/concepts/<concept>/open-questions.md` before and after the change. Treat this as a recurring quality gate, not a full manual re-review of every row.

8. Audit before merge.

```bash
uv run kb audit all
uv run --extra dev pytest
```

## What The Source Scan Reports

`kb sources scan` compares a prior source snapshot to the current repo state and reports:

- Changed source hashes.
- New and removed URLs.
- New, removed, and changed source records.
- Changed release-note records.
- Changed model-map rows.
- New and pending media items.
- Source retrieval timestamp ranges.
- Source families that were skipped or failed.
- Affected concepts, claims, source summaries, guides, and public export files.

The scan is intentionally read-only with respect to trusted public artifacts. It records source state and impact mapping; it does not rewrite guides, claims, answer prose, or public export files.

`--source-status` is optional for local runs. The scheduled workflow writes `data/review/source-scan/source-refresh-status.json` after the source refresh step so refresh failures can be reflected in the source-scan report before the job fails.

## Deterministic Vs Reviewer Work

`kb build --dry-run` and `kb status` separate safe deterministic work from reviewer or AI work.

Deterministic work can run in CI:

- Source normalization through the existing refresh path.
- Generated concept index rebuilds.
- Approved-claim and approved-media insert refreshes.
- Answer-pack/source-summary/model-map/Lava manifest rebuilds.
- Public export rebuilds.
- Audits and tests.

Claim graph rebuilds are deterministic only when the approved review inputs are present. The scheduled GitHub workflow preserves the committed `claims/approved-claims.jsonl` graph because some review/private media inputs are intentionally ignored working state. Run `uv run kb status` first, then `uv run kb build --stage claims` locally only when the approved review inputs are available and intentionally being republished.

Reviewer or local-Codex work stays manual:

- New media transcription.
- Gemma enrichment.
- Public-safe media rewrites.
- Claim promotion.
- Live verification.
- Source-conflict review.
- Authored long-form guide synthesis.
- Open-question triage for new or changed high-value rows.

## Open-Question Cadence

Open questions are generated from the current guide text and evidence layer. They should be refreshed after every meaningful data refresh, but they should not require a full manual backlog review every time.

Use this cadence:

1. After source scrapes, transcript batches, media promotions, claim promotions, or guide synthesis, run `uv run kb status` and then `uv run kb build --stage guide-intel` when guide intelligence is stale.
2. Compare the regenerated `knowledge/concepts/<concept>/open-questions.md` files against the previous state.
3. Resolve high-value `Needs Citation` rows before public export or PR review, especially for operational concepts such as Workflows, Data Views/Reports, Security/Permissions, Groups, Check-in, Lava, and Mobile.
4. Batch `Needs Live Verification` rows separately with read-only probes. Do not promote operational claims to answer-ready status without concrete evidence.
5. Leave `Community-Supported Only` rows as review backlog unless stronger evidence or a reviewer-approved rewrite exists.

Resolved rows should stay resolved after rescrapes when the fix lives in the durable generation path: source links in the guide, approved claims, source maps, or guide-intel logic. If the same `Needs Citation` rows return after a rebuild, treat that as a generator/source-map issue instead of repeating manual cleanup.

## Safety Boundaries

The orchestration layer must preserve the existing public/private model:

- Public artifacts must not include raw transcripts, downloaded media, tokenized media URLs, private repo paths, secrets, internal URLs, or copied protected source text.
- Source-derived changes may generate review candidates and routing context.
- Public answer prose should continue to use only approved answer-pack and live-verified claim paths.
- Media and private corpus material must remain private until rewritten and explicitly approved.
- CI may flag long-form guides that need authored refresh, but it must not pretend to produce reviewed prose without Codex/reviewer involvement.

## Scheduled Workflow

`.github/workflows/refresh-daily.yml` runs on every day except Monday, when the
weekly workflow covers the same cadence. It refreshes only registered
daily-cadence sources handled by the general source pipeline, skips the broad
endpoint probe, compares the result with a pre-refresh snapshot, writes source
observations, runs focused regression tests, and uploads one
`daily-source-refresh` artifact. Its strict gate uses
`--required-workflow daily-sources`, so a clean CI checkout does not require
sources owned by another workflow; those rows remain visible in the report.
Rock GitHub issues remain owned by the separate
daily `.github/workflows/refresh-rock-issues.yml` pipeline; their summary feeds
the shared freshness report.

The three required hosted workflow records are `daily-sources`, `daily-issues`,
and `weekly-comprehensive`. Their maximum schedule ages are 52, 36, and 216
hours respectively. The issue workflow publishes `rock_core_issues` and
`rock_mobile_issues` from `agent/rock-issue-summary.json`; the dashboard reports
their catalog hash, count, last check, last content change, and status without
republishing issue bodies. The weekly workflow owns weekly, monthly, and manual
sources. Selector validation guarantees that these ownership sets are complete
and non-overlapping when sources are added or reclassified.

`.github/workflows/refresh.yml` runs the safe path on schedule and on manual dispatch:

1. Pre-refresh source scan snapshot.
2. Source refresh with `--skip-indexes`, plus a source-refresh status file.
3. Post-refresh source scan diff, including failed/skipped source family status when available.
4. Status, build dry-run, and PR body generation.
5. Refresh dashboard generation only when both an evaluation report and a compatible rebuild-plan report exist.
6. Refresh-scope classification, including source delta count and whether `data/media/index` is available to the runner.
7. Deterministic public rebuild commands that preserve the committed claim graph. Default-branch CI skips this step when private media indexes are absent, because rebuilding without ignored sidecars would remove approved-media routing from public artifacts. Non-default branch dispatches may still run the rebuild path as validation because they do not create automation PRs.
8. Public export/readiness audits and tests. In CI this uses `uv run kb audit readiness --public-only` because private media sidecars and raw review artifacts are not checked in.
9. Pull request creation only when the workflow is running on the default branch and the source scan found source deltas. Manual dispatches on feature branches are validation runs; they still execute source refresh, public-only readiness, and tests, but skip automated refresh PR creation.

If source refresh fails, the workflow still writes the source-scan report and build status outputs, skips deterministic public rebuilds, and fails the job instead of opening a public-artifact PR from incomplete source state.

If the source scan finds no source deltas, the default-branch workflow exits cleanly without opening a refresh PR. If source deltas exist but private media indexes are unavailable in CI, treat the automation PR as a source-refresh/status PR; run the private-media-aware rebuild locally before publishing guide and agent-pack artifact changes.

The generated PR body includes source-scan counts, affected concepts, claim impact counts, guide refresh/synthesis flags, media review counts, live-verification counts, commands, and audit/test expectations.

`.github/workflows/network-operations.yml` checks the public freshness endpoint
daily. It fails when a required workflow is missed or a source is failed,
missing, genuinely overdue, or newer than the deployed typed catalog. A normal
no-change check remains healthy because `last_checked_at` advances while
`content_changed_at` and `content_hash` remain stable. A source-only refresh
that changes issues or Ideas intentionally reports `deployment_lag` until the
reviewed deployment includes the new normalized hash and row count.
