# Canonical Knowledge Shadow

The canonical knowledge shadow tests a shared typed layer across claims,
recipes, Lava contexts, Rock issues, Rock Ideas, Model Map records, community
contributions, and source summaries. Legacy retrieval remains the public
default. A separately authorized, anonymously opted-in canary can read the
canonical projection without changing that default.

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

## Source-Native Documentation Pilot

The tracked `canonical/source-native/v1/` pilot tests source-native ingestion
for `system-admin-ops` and `check-in`. It is a non-default input to the
canonical shadow and opt-in canary, not to ordinary retrieval or OKF.

Build deterministic private review inputs from the Rockumentation API:

```bash
uv run kb tools source-native-candidates \
  --concept system-admin-ops \
  --concept check-in \
  --limit-per-concept 6
uv run kb tools source-native-schema
uv run kb tools source-native-prompt --concept system-admin-ops
```

The parser assigns stable IDs before model review to sentences, tables, code
blocks, and individual list items. Nested field catalogs are separate child
units linked to their parent item. The snapshot also retains the API-derived
documentation path and branch hierarchy, separate check/change timestamps, the
upstream documentation revision, and parser version. Full article text and
source-unit text remain under ignored `data/review/`. The v2.3 prompt can
classify a supplied unit or request a deterministic split; it cannot invent
evidence addresses.

Merge every schema-constrained model batch and run the semantic gate before
maintainer review:

```bash
uv run kb tools source-native-merge \
  --input data/review/source-native-pilot/distillation-input.jsonl \
  --batch data/review/source-native-pilot/output-a.json \
  --batch data/review/source-native-pilot/output-b.json \
  --destination data/review/source-native-pilot/reviewed-output.json
```

After maintainer review, promote only the public-safe paraphrases and provenance:

```bash
uv run kb tools source-native-promote \
  --input data/review/source-native-pilot/distillation-input.jsonl \
  --output data/review/source-native-pilot/reviewed-output.json \
  --reviewer <reviewer-id> \
  --model <exact-model-id> \
  --reviewed-at <iso-8601>
```

Promotion fails unless every source unit has one decision, every useful unit
has exactly one primary artifact type, claim and procedure/reference material
are separated, mutable defaults carry verification status, and no split request
remains. Compare refreshes with:

```bash
uv run kb tools source-native-impact \
  --previous <prior-reviewed-bundle> \
  --current canonical/source-native/v1
```

The impact report queues only knowledge units that depend on added, removed, or
changed source units. Unrelated knowledge and projections remain untouched.

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

A report status of `pass` means the candidate did not regress from the
baseline. It does not erase failures shared by both variants. Shared defects are
listed under `promotion_gate.shared_failures`, and production readiness remains
false until review and a separately authorized release.

Exact claim collapse is also gated. The generated review records every public
claim ID, concept facet, authority tier, evidence link, independent source work,
and mirrored source record. A maintainer approval is valid only while its input
hash and complete group coverage still match.

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
