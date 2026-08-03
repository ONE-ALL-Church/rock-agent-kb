# Canonical Knowledge Shadow

The canonical knowledge shadow tests a shared typed layer across claims,
recipes, Lava contexts, Rock issues, Rock Ideas, Model Map records, community
contributions, and source summaries. Legacy retrieval remains the public
default. A separately authorized, anonymously opted-in canary can read the
canonical projection without changing that default.

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
  writes a public-safe copy to dedicated service artifacts and separate D1
  canary tables. Default readers do not use it.
- Existing claims, answer packs, lexical retrieval, MCP behavior, CLI behavior,
  and OKF exports remain the default authoritative interface.

## Source-Native Documentation Bundle

The tracked `canonical/source-native/v1/` bundle contains reviewed official
documentation, developer and mobile documentation, Lava prose, and Rock
community articles. Concepts remain task-oriented facets rather than one copy
of each source navigation branch. The bundle is a non-default input to the
canonical shadow and opt-in canary, not to ordinary retrieval or OKF.

At the 2026-08-03 architecture review, the tracked bundle contains five source
families, 38 articles, 1,488 source units, and 239 reviewed artifacts across 15
concept facets. These figures supersede the 24-article first-expansion counts
for current planning, while the dated expansion decision preserves those
historical results.

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
records. Exact record IDs are explicit routing decisions and are not dropped
because their normalized summary has a low concept score. Records surfaced
under multiple concepts are coalesced into one candidate with multiple concept
facets.

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

A source candidate may contain at most 200 units. Oversized articles stop before
model review and require a reviewed deterministic partitioning strategy; do not
truncate them or increase the limit just to make a batch pass.

The model input hash covers the stable source snapshot, parser and split-rule
revision, every source unit and locator, concept facets, existing-claim review
context, and documentation routing/version metadata. Volatile check timestamps
are excluded. A context-only change therefore invalidates stale generation
without forcing re-review when only `last_checked_at` advances.

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

Use immutable GitHub commit evidence for implementation contracts and current
official documentation or source snapshots for mutable guidance. A resolution
may confirm, narrow, correct, or supersede an artifact. Narrowing and correction
must provide effective title and retrieval text; canonical retrieval uses that
reviewed text instead of the stale model wording. Superseded artifacts are
excluded. Source-hash and time-bound evidence reopen automatically when stale.

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
Synthetic, evaluation, and maintainer traffic may prove correctness but never counts as
external evidence. Keep those tests in the `maintainer` cohort and retain
legacy as the default until the external gate passes.

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

## Service Dual Write And Canary

`uv run kb deploy-service` generates the legacy service projection and a
complete canonical shadow in the same build. Canonical source snapshots, source
units, generation activities, knowledge units, evidence links, relationships,
search rows, retrieval documents, and a content-addressed manifest are written
under `service/dist/canonical-shadow/v1/`. The D1 seed also creates a parallel
`canonical_search_rows`, concept, alias, and FTS set. Table names come only from
the Worker's fixed projection map; request input is never interpolated into a
table name.

An applied deploy stores those files as dedicated R2 shadow objects and records
the projection hash and bounded counts in `kb_meta` plus
`canonical_projection_history_v1`. The Worker exposes that summary through
`/health`. Search, exact retrieval, MCP, CLI, and OKF read the legacy projection
by default; `active_retrieval_projection` must remain `legacy` and the canonical
manifest must report `active_reader: false`.

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
the bounded observation count. Building or deploying the parallel tables does
not authorize a default retrieval cutover.

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

## Promotion Gate

Do not make this projection the default public retrieval input until reviewed
shadow and canary evidence shows:

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
history. Promotion still requires explicit review and authorization; the
baseline itself is not a production retrieval switch. Keep the default on
legacy until real external opt-in outcomes demonstrate that semantic and
version-sensitive questions improve without degrading exact technical lookup,
authority correctness, duplicate rate, no-answer behavior, latency, or public
safety. Maintainer and evaluation traffic alone cannot satisfy that gate.
The machine gate also requires the reviewed minimum source-family and article
coverage, zero unresolved or stale verification blockers, a passing retrieval
shadow, zero exact, authority, no-answer, endpoint, or overall retrieval
regressions, and the configured external cohort, comparison, category, and
preference thresholds. Passing the technical half authorizes only continued
canary testing.

The current versioned policy requires five anonymously opted-in external
installations, 50 decisive comparisons across all six required categories, and
a canonical-to-legacy preference ratio of at least 2:1. Maintainer comparisons
are reported separately and cannot satisfy those thresholds.
