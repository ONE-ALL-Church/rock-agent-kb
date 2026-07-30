# Canonical Knowledge Shadow

The canonical knowledge shadow is an internal architecture projection. It tests
a shared typed layer across claims, recipes, Lava contexts, Rock issues, Rock
Ideas, Model Map records, community contributions, and source summaries without
changing the public agent pack or hosted retrieval.

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
- Registry aliases survive wording changes. Every move from a prior pilot ID is
  retained in `identity-migrations.jsonl`; rerunning with unchanged inputs must
  produce byte-identical registry and migration files.
- The tracked `canonical/identity/v1/` baseline stores durable identities and a
  separate compatibility map containing only result IDs already exposed by
  the public projection. Unpublished pilot migration IDs remain ignored.
- Rockcast podcast and YouTube locators with the same explicit episode number
  share a `source_work_id`; they are mirrors, not independent corroboration.
- Defined Value options in Model Map diffs are compared by portable option name
  and description, not instance-local numeric IDs.
- The complete generated review shadow remains ignored. The deployment build
  writes a public-safe inactive copy to dedicated service artifacts; active
  readers do not use it.
- Existing claims, answer packs, lexical retrieval, MCP behavior, CLI behavior,
  and OKF exports remain authoritative.

## Source-Native Documentation Pilot

The tracked `canonical/source-native/v1/` pilot tests source-native ingestion
for `system-admin-ops` and `check-in`. It is not a public retrieval input.

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
unpublished pilot ID. The ignored migration file remains the audit trail.

## Service Dual Write

`uv run kb deploy-service` generates the legacy service projection and a
complete canonical shadow in the same build. Canonical source snapshots, source
units, generation activities, knowledge units, evidence links, relationships,
search rows, retrieval documents, and a content-addressed manifest are written under
`service/dist/canonical-shadow/v1/`.

An applied deploy stores those files as dedicated R2 shadow objects and records
the projection hash and bounded counts in `kb_meta` plus
`canonical_projection_history_v1`. The Worker exposes that summary through
`/health`. Search, exact retrieval, MCP, CLI, and OKF continue to read the
legacy projection; `active_retrieval_projection` must remain `legacy` and the
canonical manifest must report `active_reader: false`.

Local files remain plain JSONL for review. R2 receives deterministic gzip
objects plus the manifest; every manifest row records both uncompressed and
compressed hashes and byte counts.

The history record exists to compare identity and projection stability across
source-refresh cycles. It retains the latest 32 timestamped observations, so an
unchanged projection still records a distinct successful cycle. Health reports
the bounded observation count. This does not authorize a canary or retrieval
cutover.

## Promotion Gate

Do not make this projection a public retrieval input until a reviewed shadow
evaluation shows:

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
baseline itself is not a production retrieval switch.
