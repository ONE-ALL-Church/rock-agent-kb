# Canonical Knowledge Shadow

The canonical knowledge shadow tests a shared typed layer across claims,
recipes, Lava contexts, Rock issues, Rock Ideas, Model Map records, community
contributions, and source summaries. Canonical retrieval is the reviewed public
default after the 2026-08-03 cutover; the complete legacy projection remains a
runtime rollback. A separately authorized, anonymously opted-in canary remains
available for blind comparisons.

The current architecture decision, measured evidence, rollout blockers, and
ordered next work are recorded in
[Canonical Knowledge Architecture Status](../decisions/canonical-knowledge-architecture-status-2026-08-03.md).
Use this runbook for execution details; do not infer current readiness from an
older pilot count.

Run it with:

```bash
uv run kb tools canonical-shadow
uv run kb tools canonical-retrieval-shadow
```

The commands write ignored review artifacts under
`data/review/canonical-knowledge-pilot/`:

- `source-snapshots.jsonl`
- `source-units.jsonl`
- `generation-activities.jsonl`
- `knowledge-units.jsonl`
- `identity-registry.jsonl`
- `identity-migrations.jsonl`
- `retired-identity-migrations.jsonl`
- `evidence-links.jsonl`
- `relationships.jsonl`
- `summary.json`
- `baseline-search-rows.jsonl`
- `candidate-search-rows.jsonl`
- `retrieval-evaluation-set.jsonl`
- `endpoint-compatibility-cases.jsonl`
- `claim-collapse-review.json`
- `claim-collapse-maintainer-review.json` when a maintainer records decisions
- `retrieval-raw.json`
- `retrieval-report.json`

## Architecture

The projection separates seven concerns:

1. A source observation identifies the checked upstream revision, content
   hashes, parser version, and separate checked/changed timestamps.
2. A source unit identifies the exact paragraph, table, procedure, timestamp, code span, issue,
   idea, model, or recipe used as evidence.
3. A generation activity records the model, prompt, input hash, and review
   method that produced typed candidates.
4. A persistent identity registry separates durable identity from mutable
   wording and content hashes.
5. A knowledge unit carries one canonical retrieval identity, concept/topic
   facets, review metadata, and the original source-specific payload.
6. An evidence link connects primary source units to knowledge units.
7. A typed relationship records an accepted, rejected, replaced, or
   needs-review relationship decision.

Source-specific payloads remain intact inside the common envelope. Issue
lifecycle observations are not flattened into claims, recipes retain security
and adaptation fields, and Model Map records retain their structured model
payloads.

The reviewed machine-readable contracts live in
`canonical/source-family-contracts-v1.json`. Rebuild them with:

```bash
uv run kb tools source-family-contracts
```

Official documentation uses source-native distillation because prose must be
separated into independently useful claims, procedures, recipes, references,
and discovery summaries. Already structured issue, Idea, Model Map, Lava
context, recipe, and contribution records retain deterministic typed ingestion
contracts instead of being rewritten by a model. Legacy reviewed claims and
source summaries are explicitly labeled as legacy projections so remaining
migration work stays measurable.

The bundle validator rejects `existing_knowledge_projection` units as primary
evidence. Private source-unit text is schema-marked private and omitted from
public serialization.

## Current Pilot Rules

- Exact reviewed claim statements may share one canonical identity and use
  concepts as facets.
- Existing globally namespaced artifact IDs remain canonical for recipes, Lava
  contexts, issues, Ideas, Model Map records, contributions, and source
  summaries. The pilot's former opaque hashes remain aliases.
- Claim identities use an approved claim or distilled-artifact alias as their
  first registry anchor. Claim wording and supporting-claim IDs are not
  identities.
- Registry aliases survive wording changes. Migrations that still resolve to a
  current unit remain in `identity-migrations.jsonl`; migrations whose target
  was retired move to the private `retired-identity-migrations.jsonl` audit
  archive. Rerunning with unchanged inputs must produce byte-identical registry
  and migration files.
- Distilled-claim reviews bind to an exact source-input snapshot. A changed
  support set or generated conclusion receives a content-versioned ID and
  returns to reviewer approval instead of inheriting a stale decision.
- The tracked `canonical/identity/v1/` baseline stores durable identities and a
  separate compatibility map containing only result IDs already exposed by
  the public projection. Unpublished pilot migration IDs remain ignored.
- Rockcast podcast and YouTube locators with the same explicit episode number
  share a `source_work_id`; they are mirrors, not independent corroboration.
- Defined Value options in Model Map diffs are compared by portable option name
  and description, not instance-local numeric IDs.
- The complete generated review shadow remains ignored. The deployment build
  writes public-safe legacy and canonical service artifacts to separate D1
  tables. The active-reader marker selects canonical by default and preserves
  legacy as an explicit rollback.
- MCP remains the primary interactive interface, CLI is the local/operator
  fallback, and OKF is the portability projection. All read from the selected
  service projection rather than maintaining separate knowledge copies.

## Source-Native Documentation Bundle

The tracked `canonical/source-native/v1/` bundle contains reviewed official
documentation, developer and mobile documentation, Lava prose, and Rock
community articles. Concepts remain task-oriented facets rather than one copy
of each source navigation branch. The bundle feeds the canonical projection
used by ordinary retrieval and OKF; the same build also retains the complete
legacy projection for rollback and controlled comparisons.

The tracked bundle currently contains five source families, 64 articles, 2,052
source units, and 391 reviewed artifacts across 23 concept facets. All 64
generation activities use `gpt-5.6-sol`: 31 use source distillation prompt
`2.3.1`, 26 use legacy migration wrapper `1.3.0`, and seven use wrapper `1.3.1`.
The migration wrapper requires an exact identity decision for every prior
source-native artifact. The manifest records prompt versions instead of
presenting a mixed bundle as one generation run. Per-artifact concept lists
remain bounded at 20; the manifest's aggregate concept inventory is separately
bounded for repository-scale coverage.

Migration is source-first, not a same-type rewrite. Re-read every deterministic
unit in the current source and allow useful typed artifacts with no legacy
equivalent. Treat legacy rows as a loss-prevention ledger. In particular, a
legacy source summary can resolve through its public alias to a claim, task
card, recipe, structured reference, or genuine source summary when that primary
independently preserves the useful landing value. Source-registry topics are
source-wide metadata and need article-local corroboration before they qualify
as high-confidence concept routes.

Select a bounded migration batch before building private review inputs:

```bash
uv run kb tools source-native-migration-priority \
  --as-of <iso-8601> \
  --destination data/review/source-native-legacy-migration/priority-report.json
```

Use a fixed `--as-of` when the ranking must be reproduced. The report considers
only active legacy rows from the five supported official prose families. It
ranks source records by claim value, exact evaluation coverage, verification
debt, source-native completion value, and freshness. It does not auto-select or
promote anything. Refresh records marked `refresh_source_first`, manually
resolve records under `unresolved_source_records`, and review the proposed
concept IDs before choosing a coherent source-family batch. By default the
command reads the hosted operations dashboard. Use `--dashboard <capture.json>`
for a reproducible snapshot or `--no-hosted-dashboard` while offline.
Result-ID-only outcome signals are advisory and privacy-bounded; their score is
capped so they can prioritize a real field gap without overruling freshness or
concept-routing gates.

For routine legacy migration waves, use the fail-closed batch coordinator in
[`source-native-migration-batches.md`](source-native-migration-batches.md). It
preserves exact per-record concept routing, prepares one immutable model packet
per article, records machine-readable correction metrics, and requires one
hash-bound maintainer decision per article. The coordinator ends at
`ready_for_explicit_promotion`; it never invokes a model, approves output,
promotes knowledge, rebuilds public projections, deploys, or writes externally.
The commands below remain the lower-level manual workflow and the separate
promotion boundary.

Build deterministic private review inputs from the Rockumentation API:

```bash
uv run kb tools source-native-candidates \
  --source-id rock_documentation \
  --source-id rock_developer \
  --source-id rock_mobile_docs \
  --source-id rock_lava_docs \
  --source-id rock_community_blog \
  --concept workflows \
  --concept obsidian-development \
  --concept mobile \
  --limit-per-concept 4
uv run kb tools source-native-schema
uv run kb tools source-native-prompt \
  --source-record-id rock_documentation:article:<id>
```

Use repeated `--source-record-id` options when a maintainer has selected exact
records, and always provide the reviewed `--concept` routing facets in the same
command. Exact selection fails closed without an explicit concept so the pilot
defaults cannot silently misroute a migration. Exact record IDs are explicit
routing decisions and are not dropped because their normalized summary has a
low concept score. Programmatic batch preparation supplies a validated
per-record concept map; passing the union of a batch's concepts to every exact
record is invalid because it would over-route unrelated articles. Records
surfaced under multiple concepts are coalesced into one candidate with only
their reviewed concept facets.

The parser assigns stable IDs before model review to sentences, tables, code
blocks, and individual list items. Nested field catalogs are separate child
units linked to their parent item. The snapshot also retains the API-derived
documentation path and branch hierarchy, separate check/change timestamps, the
upstream documentation revision, and parser version. Full article text and
source-unit text remain under ignored `data/review/`. The v2.3 prompt can
classify a supplied unit or request a deterministic split; it cannot invent
evidence addresses or target a fixed number of claims. Maintainer-approved,
content-hash-bound sentence splits are recorded in `split-rules.jsonl`; a rule
that no longer matches current source text fails closed.

For official static pages without Rockumentation content, parser `1.1.0` scopes
extraction to the page's nested `article` element when present. Do not flatten
site navigation into source units. Preserve redirect locations in
`location_aliases`, and increment the parser version whenever extraction
semantics change. A redirected source is coalesced before candidate generation
so one current URL produces one snapshot and one source-native candidate.

A source candidate may contain at most 200 units. Oversized articles stop before
model review and require a reviewed deterministic partitioning strategy; do not
truncate them or increase the limit just to make a batch pass.

The model input hash covers the stable source snapshot, parser and split-rule
revision, every source unit and locator, concept facets, existing-claim review
context, and documentation routing/version metadata. Volatile check timestamps
are excluded. A context-only change therefore invalidates stale generation
without forcing re-review when only `last_checked_at` advances.

Canonical source-summary hashes follow the same semantic boundary. They exclude
only volatile `retrieved_at`; summary text, semantic source content hashes, and
routing metadata remain hash-significant. This keeps observation time from
churning identities without allowing a real source or summary change to pass as
metadata-only.

Merge every schema-constrained model batch and run the semantic gate before
maintainer review:

```bash
uv run kb tools source-native-merge \
  --input data/review/source-native-expansion/distillation-input.jsonl \
  --batch data/review/source-native-expansion/model-output/batch-a.json \
  --batch data/review/source-native-expansion/model-output/batch-b.json \
  --destination data/review/source-native-expansion/generated-output.json
```

The strict merge rejects `split_required` feedback by default. If a model has
returned exact-coverage split feedback, use `--allow-review-blockers` only to
assemble the ignored private review packet. A maintainer must then either add a
content-hash-bound deterministic split or explicitly correct an overcalled
split in the reviewed output. Promotion always reruns the strict gate and never
accepts an unresolved blocker.

After maintainer review, promote only the public-safe paraphrases and provenance:

```bash
uv run kb tools source-native-promote \
  --input data/review/source-native-expansion/distillation-input.jsonl \
  --output data/review/source-native-expansion/reviewed-output.json \
  --generated-output data/review/source-native-expansion/generated-output.json \
  --base canonical/source-native/v1 \
  --destination canonical/source-native/v1 \
  --reviewer <reviewer-id> \
  --model <exact-model-id> \
  --reviewed-at <iso-8601>
```

Promotion fails unless every source unit has one decision, every useful unit
has exactly one primary artifact type, claim and procedure/reference material
are separated, mutable defaults carry verification status, and no split request
remains. Append mode replaces only refreshed source works, preserves unrelated
artifacts and holdouts, rejects stale holdout IDs, records model-versus-reviewer
change counts, and writes unresolved checks to `verification-queue.jsonl`.

### Legacy Migration Compiler

Use the migration compiler only after selecting a bounded set of existing
source-native candidates. It adds the active legacy claims, legacy source
summaries, and previously published source-native artifacts for each exact
source record to the private review input:

```bash
uv run kb tools source-native-migration-input \
  --source-native-input data/review/source-native-expansion/distillation-input.jsonl \
  --destination data/review/source-native-legacy-migration/migration-input.jsonl
uv run kb tools source-native-migration-schema
uv run kb tools source-native-migration-prompt \
  --input data/review/source-native-legacy-migration/migration-input.jsonl \
  --source-record-id rock_documentation:article:<id>
uv run kb tools source-native-migration-merge \
  --input data/review/source-native-legacy-migration/migration-input.jsonl \
  --batch <model-output-a.json> \
  --batch <model-output-b.json> \
  --destination data/review/source-native-legacy-migration/generated-output.json
uv run kb tools source-native-migration-promote \
  --input data/review/source-native-legacy-migration/migration-input.jsonl \
  --output data/review/source-native-legacy-migration/reviewed-output.json \
  --generated-output data/review/source-native-legacy-migration/generated-output.json \
  --base canonical/source-native/v1 \
  --destination canonical/source-native/v1 \
  --reviewer <reviewer-id> \
  --model <exact-model-id> \
  --reviewed-at <iso-8601>
```

Promotion is fail closed. Every legacy row must be retained or replaced against
its exact content hash. Every prior source-native artifact must retain its
durable identity or be explicitly superseded by one complete replacement. The
compiler stores old public result IDs as exact-lookup aliases, binds every
replacement to its source snapshot and artifact hash, and turns source-summary
companions into typed `references` relationships. A legacy claim cannot use
companions to hide partial coverage. Raw source text, model output, and review
notes remain in ignored private review data; only approved migration records
enter the tracked bundle. Input-hash version `2` independently recomputes the
source candidate hash before binding the legacy and prior-artifact rows, so an
edited private packet fails rather than inheriting the original approval.

API-backed source records may replace an older URL-hash record ID with a stable
article ID. Runtime migration matching accepts the old ID only when it can be
recomputed from the reviewed source snapshot's exact canonical URL or redirect
aliases. Matching a different record from the same source family is not enough
and still fails closed.

When a static site shell changes only an article title or the contextual prefix
derived from that title, regenerate the exact source-native candidate and use
the presentation rebind. It recomputes the complete private input hash, requires
the snapshot identity, body hash, parser, source-unit IDs, locators, and unit
content hashes to remain identical, and preserves the original reviewed model
activity instead of pretending the model reran:

```bash
uv run kb tools source-native-presentation-rebind \
  --input <fresh-candidate-directory>/distillation-input.jsonl
```

Any content, routing, parser, locator, or source-unit change fails closed and
requires the normal reviewed distillation or migration path.

If a deterministic rebuild changes only legacy projection hashes after an
already reviewed migration, rebind the review instead of rerunning model
distillation:

```bash
uv run kb tools source-native-migration-rebind \
  --previous-input <previous-migration-input.jsonl> \
  --refreshed-input <refreshed-migration-input.jsonl> \
  --output <reviewed-output.json> \
  --destination <rebound-reviewed-output.json>
```

The command first validates the prior review against its original input. It
then permits only legacy content-hash and migration-hash refreshes. Previously
approved artifacts may be materialized only when their stable IDs and semantic
hashes exactly match the reviewed output. Any source, source-unit, artifact,
retrieval text, concept, relationship, or identity change fails closed and
requires a new review.

After promotion, rebuild the identity baseline and run the production-worker
retrieval shadow. A migration batch is not releasable unless verification has
zero blockers and every strict regression category remains at zero.

Compare refreshes with:

```bash
uv run kb tools source-native-impact \
  --previous <prior-reviewed-bundle> \
  --current canonical/source-native/v1
```

The impact report queues only knowledge units that depend on added, removed, or
changed source units. Unrelated knowledge and projections remain untouched.
Verification requests remain explicit caveats; they are not silently promoted
to live-verified facts.

Resolve verification requests through a separate hash-bound review packet:

```bash
uv run kb tools source-native-verification-packet \
  --destination data/review/source-native/verification-packet.jsonl
uv run kb tools source-native-verification-promote \
  --input data/review/source-native/verification-resolutions.jsonl \
  --reviewer <reviewer-id> \
  --reviewed-at <iso-8601>
uv run kb tools source-native-verification-audit \
  --check-live \
  --destination data/review/source-native/verification-report-live.json
```

Keep live audit output under ignored `data/review/`. The tracked
`canonical/source-native/v1/verification-report.json` is part of the signed
bundle manifest and records the reproducible non-network bundle audit. The CLI
rejects writing a live audit over that tracked file because doing so would
invalidate the manifest and mix current network state into the reviewed bundle.

Use immutable GitHub commit evidence for implementation contracts and current
official documentation or source snapshots for mutable guidance. A resolution
may confirm, narrow, correct, or supersede an artifact. Narrowing and correction
must provide effective title and retrieval text; canonical retrieval uses that
reviewed text instead of the stale model wording. Superseded artifacts are
excluded. Source-hash and time-bound evidence reopen automatically when stale.
If one verification request covers multiple artifacts and its result affects
them differently, use `artifact_overrides` to provide one disposition for every
artifact ID in that queue item. Partial coverage is rejected so a correction
cannot accidentally replace distinct artifacts with the same public wording.
For corrected or narrowed records, the public canonical payload exposes a
compact `effective_artifact` containing only the verified title, retrieval
text, scope, and identity metadata. It links to the original reviewed artifact
by content hash and public bundle path, but does not embed pre-verification
wording in exact-result responses. This preserves the audit trail without
presenting superseded text as current agent guidance.

After retrieval evaluation, run the quantitative readiness gate:

```bash
uv run kb tools source-native-readiness \
  --retrieval-report data/review/canonical-knowledge-pilot/retrieval-report.json \
  --verification-report data/review/source-native/verification-report-live.json \
  --destination data/review/source-native/readiness-report.json
```

The versioned policy in `canonical/source-native/promotion-policy-v1.json`
requires a live verification report and separates technical evidence from real
external usefulness evidence. Omitting `--verification-report` makes readiness
perform the live audit itself; a captured non-live report cannot pass the gate.
Synthetic, evaluation, and maintainer traffic may prove correctness but never
counts as external evidence. The current policy treats external evidence as an
advisory post-cutover signal because a maintainer approved a reversible
technical cutover after every strict technical check passed. That approval does
not fabricate external outcomes or weaken the technical checks.

## Reviewed Cross-Source Synthesis

The tracked `canonical/cross-source/v1/` bundle tests the evidence model on a
version-sensitive behavior that spans distinct source types. Promote reviewed
decisions with:

```bash
uv run kb tools reviewed-cross-source-promote \
  --input data/review/cross-source/<reviewed-decisions.jsonl>
```

Follow
[`cross-source-evidence-synthesis-v1.md`](../prompts/cross-source-evidence-synthesis-v1.md).
A synthesis requires at least two distinct public sources and keeps their roles
separate:

- issue evidence `reports` an observed symptom or affected version;
- an official release record `supports` a shipped version statement;
- immutable public source code `demonstrates` implementation at a pinned commit
  and line span.

The promotion compiler emits source snapshots, addressable source units,
generation provenance, one canonical knowledge unit, evidence links, typed
relationships, and exact plus paraphrased retrieval cases. It rejects private
source text, unknown relationship evidence, duplicate units, unscoped version
claims, and fewer than two distinct sources. Mutable issue state is never
treated as equivalent to an official release statement or immutable code.

## Retrieval Comparison

Concept search rows are routing summaries, not containers for every generated
concept artifact. The service uses `quickstart.md` plus an explicit
live-verification boundary for each concept. Detailed authored guidance is
projected separately as `guide_section` rows using the same deterministic
high-signal policy as the quickstart: confidence `high` or `normal`, at least 75
words, and at most six sections per concept. Each row includes the exact guide
path and line range, citations, source IDs and records, source authority,
freshness status, content hash, evidence hash, and live-verification flag.

Do not concatenate `index.md` or `open-questions.md` into concept search rows.
Those are generated navigation and reviewer artifacts, and large concepts can
exceed D1's bounded search body before useful guide detail appears. Guide
sections receive no generic concept-route boost; they rely on their title and
content unless the query explicitly asks for a guide or section. This keeps an
exact claim or operational answer ahead of broad background while preserving
direct section search and exact `kb_get_result` expansion.

The read-only OKF distribution retains the same typed guide sections under
`guide-sections/<concept-id>/`. Do not flatten them into one directory: the
concept hierarchy keeps generated indexes within the bundle's entry and byte
limits and gives offline agents a bounded navigation path.

`kb tools canonical-retrieval-shadow` builds both row sets, bundles the current
production Worker, creates two temporary Miniflare D1 databases, and runs the
same evaluation questions through the Worker's actual FTS5 and ranking code.
Both projections remain loaded while query order alternates per evaluation, so
the latency comparison does not systematically penalize the second projection.
It does not call Cloudflare or alter the hosted database. The same command runs
inside the required `public-surface` pull-request check.

The report separates:

- exact technical lookups;
- semantic and paraphrased questions;
- authority requirements;
- known wrong-ranking guardrails;
- duplicate results;
- no-answer probes;
- exact REST and stateless MCP compatibility for public result IDs, legacy
  aliases, claims, issues, Ideas, Model Map, Lava contexts, and recipes;
- latency and serialized storage; and
- improved, unchanged, and regressed query results.

Source-native artifacts expose an `independent_question` as reviewed retrieval
metadata. Ranking gives an exact normalized question a bounded direct-match
signal and gives only high-overlap paraphrases a smaller signal. This separates
neighboring references from the same article without unconditional concept or
artifact-type boosts. Verified corrections retain the signal from the
`effective_artifact` projection. A structured reference receives an additional
bounded exact-lookup signal only when a field/property/type/schema/member query
contains a distinctive code-style identifier that its reviewed question,
retrieval text, title, or reference-item label names; a body-only mention gets a
smaller signal. Every change remains subject to the complete shadow.

Run the report against the pre-change bundle as well as the current bundle when
expanding source families. That comparison makes source coverage gains,
corrected mutable facts, ranking regressions, and exact-lookup behavior visible
without treating newly added self-authored evaluation questions as independent
proof.

A report status of `pass` means the candidate did not regress from the
baseline. It does not erase failures shared by both variants. Shared defects are
listed under `promotion_gate.shared_failures`, and production readiness remains
false until review and a separately authorized release.

Exact claim collapse is also gated. The generated review records every public
claim ID, concept facet, authority tier, evidence link, independent source work,
and mirrored source record. A maintainer approval is valid only while its input
hash and complete group coverage still match. A zero-regression retrieval
report remains `fail` until every generated collapse group has an explicit,
hash-matching maintainer decision; do not waive this as a cosmetic duplicate
cleanup.

Use `--skip-worker-build` only when `service/dist/dry-run/index.js` already
matches the current Worker source:

```bash
uv run kb tools canonical-retrieval-shadow --skip-worker-build
```

Persist or refresh the reviewed public-safe identity baseline separately:

```bash
uv run kb tools canonical-identity-baseline
```

The command writes `identity-registry.jsonl`,
`public-result-aliases.jsonl`, and `manifest.json` under
`canonical/identity/v1/`. It excludes every migration whose source was only an
unpublished pilot ID. Active ignored migrations remain in
`identity-migrations.jsonl`; retired ones remain in the separate private audit
archive.

## Service Dual Write, Active Reader, And Canary

`uv run kb deploy-service` generates the legacy and canonical service
projections in the same build. Canonical source snapshots, source
units, generation activities, knowledge units, evidence links, relationships,
search rows, retrieval documents, and a content-addressed manifest are written
under `service/dist/canonical-shadow/v1/`. The D1 seed also creates a parallel
`canonical_search_rows`, concept, alias, and FTS set. Table names come only from
the Worker's fixed projection map; request input is never interpolated into a
table name.

An applied deploy stores those files as dedicated R2 shadow objects and records
the projection hash and bounded counts in `kb_meta` plus
`canonical_projection_history_v1`. The Worker exposes that summary through
`/health`. Search, exact retrieval, MCP, and current CLI clients follow
`kb_meta.active_retrieval_projection` when no override is supplied. Deploys
preserve that value and initialize it to `legacy` only when it is absent.

Change the active reader only through the guarded manual workflow or its local
maintainer command:

```bash
uv run kb retrieval-projection canonical --base-url "$ROCK_KB_BASE_URL"
uv run kb retrieval-projection canonical --apply --env production \
  --database rock-agent-kb --base-url "$ROCK_KB_BASE_URL"
```

Canonical activation requires a capable Worker, ready non-empty canonical
tables, a content hash, and deployment history. The command updates the active
history row and marker as one Wrangler D1 transactional batch, then polls hosted
health. It deliberately omits explicit transaction statements because D1 owns
the batch transaction. Use the same command with `legacy` for rollback. The manual
`Set Retrieval Projection` workflow serializes with deployments and verifies
the selected default, explicit legacy lookup, and hosted retrieval evaluation.

Only a caller with a private anonymous installation marker and the fixed
`external-test` or `maintainer` cohort can request
`projection=canonical-canary`. The caller must preserve that projection across
search, `kb_get_result`, and `kb_outcome`. The service rejects missing opt-in,
unknown projections, community-cohort canary requests, and unavailable
canonical data.

The canary telemetry table stores only UTC day, canonical projection hash,
event, client class, fixed cohort, result count, primary result kind, and
aggregate count. It contains no installation hash, raw marker, query, topic,
organization, person, IP address, log, secret, or Rock data. Structured
outcomes remain in the existing consented outcome table so they can be tied to
the public result ID and exact projection hash.

Local files remain plain JSONL for review. R2 receives deterministic gzip
objects plus the manifest; every manifest row records both uncompressed and
compressed hashes and byte counts.

The history record exists to compare identity and projection stability across
source-refresh cycles. It retains the latest 32 timestamped observations, so an
unchanged projection still records a distinct successful cycle. Health reports
the bounded observation count, active projection, active projection version,
activation capability, and rollback projection. Building or deploying the
parallel tables does not itself change the active reader.

### Tester Commands

After the human accepts consent notice version 3:

```bash
uvx rock-kb telemetry enable --cohort external-test --consent-attested
uvx rock-kb install-agent
uvx rock-kb --projection canonical-canary search "<question>"
uvx rock-kb --projection canonical-canary result "<result-id>"
uvx rock-kb --projection canonical-canary outcome "<result-id>" \
  --outcome useful \
  --reason answered \
  --consent-attested
uvx rock-kb compare "<question>" --category normal_task
uvx rock-kb compare "<question>" --category version_sensitive \
  --review --submit --consent-attested
```

For MCP, pass `projection: "canonical-canary"` to `kb_search`,
`kb_get_result`, and `kb_outcome`. Restart the host after `install-agent` so its
user-scoped MCP configuration receives the private marker. Never place the
marker in a project file or prompt.

For a blind paired test, use `kb_compare_retrieval` followed by
`kb_submit_retrieval_comparison`. The start tool returns randomized A/B results
with option-local result keys but without projection labels, public IDs, or
internal paths, and does not retain the question. Review submission
accepts only the comparison ID, fixed preference, fixed reason codes, and
consent attestation.

## Promotion And Rollback Gate

Do not make a candidate projection the default public retrieval input until
reviewed evidence shows:

- no loss on exact technical lookups;
- improved duplicate rate without unsupported semantic merges;
- correct authority and source-independence handling;
- stable IDs or an explicit identity migration map;
- acceptable latency and storage cost;
- no unresolved shared defect that should block the architecture change;
- all exact REST and stateless MCP compatibility cases pass;
- source-specific schema round-trip coverage; and
- clean tracked-tree, bundle, public-export, and full test-suite results.

The versioned identity registry and public compatibility aliases are durable.
The ignored pilot directory remains the only home for unpublished migration
history. Promotion requires explicit review and authorization; the baseline
itself is not a production retrieval switch. The machine gate requires the
reviewed minimum source-family and article coverage, zero unresolved or stale
verification blockers, a passing retrieval shadow, and zero exact, authority,
no-answer, endpoint, or overall retrieval regressions.

The current release additionally requires a tested runtime legacy rollback. It
uses explicit maintainer authorization because independent external comparison
volume is unavailable. The prior goals of five anonymously opted-in external
installations, 50 decisive comparisons across all six categories, and a 2:1
canonical-to-legacy preference ratio remain advisory post-cutover signals.
Maintainer comparisons are reported separately and cannot be described as
external evidence. A strict hosted regression or projection-availability
failure is sufficient reason to restore `legacy` immediately.
