# Source-Native Migration Batches

Use this workflow to prepare and review bounded legacy-to-source-native
migrations. The automatic coordinator is intentionally narrower than the
migration compiler: it stops at `ready_for_explicit_promotion` and cannot
approve, promote, rebuild public projections, deploy, or write to an external
service. Promotion is a separate explicit command that revalidates the sealed
batch and exact article-review hashes before writing tracked artifacts.

The migration is source-first, not a row-for-row rewrite. Each selected source
record is re-distilled from all current deterministic source units and may emit
useful typed artifacts that have no legacy equivalent. Legacy rows and prior
source-native artifacts are comparison inputs and loss-prevention ledgers; they
do not define the number, wording, or shape of the new artifacts.

A legacy source summary does not require another source summary as its primary
replacement. Use the current source's best primary type when one claim, task
card, recipe, structured reference, or genuine source summary independently
preserves the old row's useful landing value. Keep or create a source summary
only when the source actually contains useful overview or discovery context;
do not manufacture one to retire the legacy type.

Concept routing is article-specific. Source-registry topics describe the whole
source and become high-confidence routing evidence only when the article title,
path, summary, or excerpt independently corroborates that exact topic. Prefer
reviewed artifact seeds and API-derived documentation paths; do not route every
developer article to Lava or Obsidian merely because those topics apply to the
developer source as a whole.

## Preconditions

- Work in a clean current-main worktree.
- Restore and validate the ignored private corpus. Missing normalized source
  data can make valid legacy identities appear unresolved.
- Refresh records whose priority action is `refresh_source_first` before they
  enter a batch.
- Use a fixed `--as-of` and a complete priority report for reproducible work.
- Keep the batch under ignored `data/review/`.

Build the complete queue, then prepare a low-risk batch:

```bash
uv run kb tools source-native-migration-priority \
  --as-of <iso-8601> \
  --limit 2000 \
  --no-hosted-dashboard \
  --destination data/review/migration-batches/<batch>/priority-report.json

uv run kb tools source-native-migration-batch-prepare \
  --count 30 \
  --max-risk low \
  --as-of <same-iso-8601> \
  --priority-report data/review/migration-batches/<batch>/priority-report.json \
  --destination data/review/migration-batches/<batch>/prepared
```

Preparation fails if the priority report is truncated, identities are
unresolved, the tracked tree is dirty, source hashes changed, concept routing
is missing or lacks complete provenance, the hydrated reserve cannot fill the
exact requested size, or a selected record has no active legacy projection.
Automatic selection prehydrates a bounded priority reserve. A record that lacks
full text, exceeds the review-context or source-unit limit, or escalates under
hydrated risk checks is recorded in the sealed selection, moved to the
appropriate risk queue, and backfilled from that reserve. Exact record batches
may be specified with repeated `--source-record-id`; they never substitute a
different record, and every exact record must satisfy the selected risk policy.
The coordinator screens the entire reserve, not only records needed to fill the
batch, and seals each hydrated candidate ID, source-input hash, and unit count so
risk reclassification remains reproducible after temporary hydration files are
removed.

API-backed documentation, developer, and mobile prose also needs an exact
`article` source identity. Static discovery or landing-page hashes can remain
source leads, but they cannot enter a low-risk migration packet until the full
article is normalized under its stable API identity.

The risk policy is independent of priority. Priority estimates migration value;
risk controls batching and review intensity. Low risk requires an official,
fresh, summary-only legacy source with complete high-confidence concept-routing
provenance and no verification debt, prior source-native identity decision,
sensitive operational concept, or broad source shape. Medium or lexical-only
concept inference requires at least standard review. Editorial community blog
records also require at least standard review because one article can span
several ministry and product topics. Security, permissions, authentication,
SQL, writes, workflows, hosting, payments, and similar surfaces are high risk.
Legacy claims and version-sensitive or broad articles require at least standard
review.

Concept inference uses the strongest available evidence tier. Explicit
documentation paths and corroborated source topics are not padded with weaker
lexical facets; missing topics surface later as unmatched routing terms and move
the record out of the low-risk wave.

Hydrated full text is checked again before packet sealing. Sensitive terms and
broad code/table structure raise risk, while source binding uses meaningful
token coverage rather than a literal summary prefix so breadcrumbs and publish
metadata cannot masquerade as source drift. Insufficient coverage still fails
high risk as a possible wrong-page or parser mismatch. The sealed migration
input is checked a second time after legacy rows are attached; reused landing
pages, conflicting episode identities, `RockInternal` contracts, mutation
requirements, and explicit compatibility warnings cannot remain low risk.

## Immutable Packet

The content-addressed `batch-manifest.json` binds the batch to:

- base commit and clean-tree state;
- complete priority input hash and fixed ranking time;
- ordered source records, normalized hashes, concepts, and risk reasons;
- distillation and migration prompt versions and hashes;
- response-schema hashes;
- ordered candidate IDs and migration input hashes;
- hashes and record counts for every prepared file.

The packet also writes complete `queues/refresh-first.jsonl`,
`queues/high-risk.jsonl`, `queues/standard-risk.jsonl`, and
`queues/eligible-backlog.jsonl` files. These are separate work queues, not model
inputs. Filling one batch never hides the remaining migration debt.

Mutable phase status lives separately in `batch-state.json`; it cannot redefine
the sealed identity or prepared-file inventory. All stored paths are
batch-relative. Preparing the same batch again is a no-op
when every hash matches. A changed base commit, prompt, schema, source, selected
order, or prepared file fails instead of overwriting evidence. Use a new batch
directory after any intentional input change.

Successful review validation writes a second content-addressed
`review-validation-manifest.json`. It binds the exact generated output,
normalized reviewed output, article decisions, optional judge review,
comparison report, reviewer identities, timestamps, and generation model.
Promotion reruns article-decision validation from those sealed inputs instead
of trusting mutable phase state.

The coordinator writes one prompt per source record under `prompts/`. Run each
prompt without tools against the supplied strict migration schema. Store model
responses under an ignored batch-local `model-output/` directory. The
coordinator does not invoke the model and records token, latency, and cost
metrics as unavailable unless separately measured evidence exists.

Assemble all model shards:

```bash
uv run kb tools source-native-migration-batch-assemble \
  --batch data/review/migration-batches/<batch>/prepared \
  --model gpt-5.6-sol \
  --output data/review/migration-batches/<batch>/prepared/model-output/01.json \
  --output data/review/migration-batches/<batch>/prepared/model-output/02.json
```

Assembly requires exact candidate coverage, input order, current hashes,
explicit nullable fields, complete source-unit dispositions, promotable typed
artifacts, and exact legacy decisions. It stops at
`awaiting_maintainer_review`. Schema-valid output is not reviewed knowledge.
For a low-risk batch, any non-empty `unmatched_routing_terms` list rejects
assembly. Correct routing in a new sealed packet or move the record to a higher
risk review wave; do not force the artifact into an unrelated supplied concept.

## Explicit Review

Review every article against its source units, legacy projection, official
source links, and public code or read-only live evidence when useful. Preserve
source conflicts and mutable behavior as verification requests; do not silently
repair uncertain statements. Save the edited response separately from the raw
generated output.

Write one JSONL decision per article using
`rock-kb-source-native-article-review-v1`:

```json
{
  "schema": "rock-kb-source-native-article-review-v1",
  "candidate_id": "source-native-candidate:...",
  "source_record_id": "rock_documentation:article:...",
  "generated_article_hash": "<sha256>",
  "reviewed_article_hash": "<sha256>",
  "decision": "approved_with_corrections",
  "reviewer": "<reviewer-id>",
  "reviewed_at": "<iso-8601>",
  "notes": ["Narrowed the version scope to the source-supported condition."],
  "adjudications": []
}
```

Use `approved` only when the generated and reviewed article hashes match. Use
`approved_with_corrections` and at least one note when they differ. If a judge
review is supplied, every recommendation needs one `accept`, `modify`, or
`reject` adjudication with a substantive rationale. This prevents a rejected
judge correction from disappearing without an evidence-backed decision.

Validate the review:

```bash
uv run kb tools source-native-migration-batch-validate \
  --batch data/review/migration-batches/<batch>/prepared \
  --reviewed-output data/review/migration-batches/<batch>/reviewed-output.json \
  --review-decisions data/review/migration-batches/<batch>/review-decisions.jsonl \
  --judge-review data/review/migration-batches/<batch>/judge-review.json
```

The optional judge file is omitted when no independent judge was run. The
comparison report separates mechanical schema changes from verification,
version scope, legacy disposition, artifact shape, evidence scope,
relationship, and routing corrections. Missing model-cost or elapsed-time
evidence remains explicitly unavailable rather than becoming zero.

## Promotion And Release

`ready_for_explicit_promotion` means only that packet coverage, schema, hashes,
and explicit article reviews passed. Promotion remains a separate, explicit,
state-aware maintainer command:

```bash
uv run kb tools source-native-migration-batch-promote \
  --batch data/review/migration-batches/<batch>/prepared \
  --review-decisions data/review/migration-batches/<batch>/review-decisions.jsonl \
  --base canonical/source-native/v1 \
  --destination canonical/source-native/v1 \
  --reviewer <reviewer-id> \
  --model <exact-model-id> \
  --reviewed-at <same-review-iso-8601>
```

The promotion wrapper rejects a changed reviewed output, generated output,
decision file, judge file, comparison report, normalized source, prompt,
schema, base commit, generation model, reviewer, or review timestamp. Canonical
files are built in a sibling staging directory and installed with a rollback
journal, so an interrupted swap restores the prior complete directory instead
of leaving a partially copied bundle. Do not bypass this wrapper with the
lower-level promotion command for a coordinated batch.

After promotion, run the normal identity, verification, public-safety,
retrieval-shadow, evaluation, release, deployment, and hosted readback gates.
The coordinator deliberately does not run retrieval shadow before promotion
because that test reads the tracked canonical bundle, not an unpublished review
packet.

## Corpus Completion

Do not equate an empty legacy migration queue with complete source coverage.
The priority report is intentionally seeded by active legacy projections, so it
can discover new knowledge inside each selected full source record but cannot
by itself identify supported prose records that never had a legacy projection.

Whole-corpus completion requires two independently reconciled ledgers:

1. Every active supported-family legacy item is replaced by a reviewed artifact
   or explicitly retained with partial or unsupported coverage.
2. Every current supported prose source record has a reviewed source-native
   generation activity for its exact content hash, or a reviewed no-artifact
   disposition covering all of its deterministic source units.

Any source record absent from both ledgers is unreviewed source coverage, not a
successful migration. Before final migration closeout, compare the complete
normalized supported prose inventory with `source-snapshots.jsonl` and
`generation-activities.jsonl`; refresh stale records first and route uncovered
records through ordinary source-native distillation even when no legacy item
exists.
