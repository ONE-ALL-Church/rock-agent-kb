# Canonical Knowledge Architecture Status

Date: 2026-08-03

Last updated: 2026-08-04

Status: accepted architecture, canonical active, legacy rollback retained

## Decision

Continue evolving the current knowledge base. Do not rebuild it from scratch.
The source-native and canonical-shadow work has now demonstrated the right
architecture across every major source shape. Canonical retrieval is approved
as the production default, with the complete tested legacy projection retained
as an immediate runtime rollback.

The durable architecture is:

1. Record an immutable, hash-addressed observation of each upstream source.
2. Split that observation into the smallest useful source-native units without
   discarding the source family's original structure.
3. Normalize already structured sources deterministically. Use reviewed,
   adaptive model distillation only where prose needs semantic separation.
4. Assign one durable canonical identity to each knowledge unit. Concepts are
   facets and routing signals, not copied knowledge identities.
5. Link knowledge to exact evidence and to other knowledge with typed,
   reviewable relationships.
6. Compile purpose-specific search, MCP, CLI, guide, and OKF projections from
   the same canonical layer.

The service continues to dual-write both projections. Omitted REST, MCP, and
current CLI requests follow the D1-backed active-reader marker. The reviewed
release changes that marker to `canonical`; explicit `legacy` retrieval remains
available for diagnostics and the guarded workflow can restore it without a
code deployment.

## Source Contracts

The shared envelope must not flatten unlike sources into generic prose:

| Source shape | Canonical treatment |
| --- | --- |
| Official documentation, developer docs, mobile docs, Lava prose, and community articles | Deterministic source units followed by schema-constrained, maintainer-reviewed source-native distillation into claims, task cards, recipes, structured references, and source summaries. |
| Rock issues and Rock Ideas | Deterministic typed records that preserve lifecycle, version, state, trust, and relationship semantics. |
| Model Map and Lava contexts | Deterministic structured records with exact lookup fields and source/version provenance. |
| Reviewed recipes and community contributions | Deterministic typed records that preserve adaptation, security, organization provenance, and concept facets. |
| Cross-source conclusions | Separately reviewed synthesis with typed evidence roles; never an automatic merge based only on similar wording. |
| Legacy claims and source summaries | Explicit migration debt. Keep serving them until their source family is safely converted; do not mass-rewrite them. |

The reviewed machine-readable source-family contracts in
`canonical/source-family-contracts-v1.json` are authoritative when prose and
code disagree.

## Current Evidence

The tracked source-native bundle now covers five source families, 43 articles,
16 concept facets, 1,624 addressable source units, and 293 reviewed artifacts:
88 claims, 25 recipes, 34 source summaries, 109 structured references, and 37
task cards. It also contains 185 typed relationships and 319 source-native
evaluation cases. All 43 generation activities use `gpt-5.6-sol` and input
hash version `2`. The manifest preserves the exact prompt history: 33 initial
distillations at version `2.3.1` and ten migration activities at wrapper
version `1.3.0`.

The final 12 prompt-`2.3.0` documentation records were refreshed before
reprocessing. Their upstream content hashes were unchanged, so the change
isolates the extraction method rather than conflating it with source edits. The
reviewed pass processed 342 units into 100 artifacts, replacing 76 earlier
artifacts. Six exact-hash split rules separated mixed source units, and
maintainer review added one missed verification boundary for a release-sensitive
cache-tag deletion claim.

The final 2026-08-04 canonical retrieval shadow evaluated 484 questions through the
production Worker's local FTS and ranking implementation:

- 321 improved, 163 were unchanged, none regressed, and no failures were shared
  by both projections;
- exact lookup, authority, no-answer, and endpoint compatibility regressions
  were all zero;
- all ten exact REST and stateless MCP compatibility cases passed; and
- serialized canonical projection storage increased by 5.681 percent, within
  the 10 percent gate.

The final isolated service quality gate also passed all 162 tracked questions:
availability, mean reciprocal rank, recall at the target rank, and authority
correctness were all `1.0`, with zero duplicate results and zero rank-below-first
cases. This gate exercises the same generated D1 projection and Worker bundle
used by the deployment workflow.

The default projection now compiles each concept as a compact quickstart plus
an explicit live-verification boundary instead of concatenating its generated
source index and reviewer queue. It separately exposes 186 first-class
`guide_section` rows: at most six high- or normal-confidence, source-backed
sections for each of 31 concepts. Each row preserves its guide line range,
citations, source IDs and records, authority, section status, content hash,
evidence hash, and live-verification boundary. No concept body exceeds the D1
search-body limit. The OKF projection retains these typed sections under
`guide-sections/<concept-id>/` so its directory indexes remain bounded and
concept-oriented.

A direct pre-change versus post-change Worker comparison found one improved
question, 427 unchanged questions, and no regressions. Mean reciprocal rank
increased from 0.369718 to 0.370892, and the baseline search JSONL became 1.798
percent smaller despite the 186 additional addressable sections. A first pass
found that a broad hosting database section could displace the exact direct
database-access claim; the final ranking removes generic concept-route boosts
from guide sections, and the tracked regression now keeps the claim first while
still returning and exactly expanding the guide section.

This is strong technical evidence that the canonical architecture is better
than the legacy-only projection. Independent church outcomes would still add
useful evidence, but the project does not currently have a realistic external
sample. The maintainer therefore approved a reversible technical cutover rather
than leaving the demonstrably better reader in an indefinite canary.

The canonical projection still identifies measurable migration debt: 594
legacy claims and 5,553 legacy source summaries remain alongside 293
source-native artifacts and deterministic typed families. That inventory is a
migration queue, not a reason to discard the working system.

Semantic source hashes now exclude transport and observation metadata while
retaining article identity, normalized content, routing, and revision fields.
Source-summary identity likewise ignores `retrieved_at` but changes when the
summary, semantic content hash, or routing metadata changes. The refresh was
propagated through deterministic concept and agent-pack stages without
regenerating authored guide prose. Guide dependency maps now bind sections to
individual Rockumentation articles and concrete public source files instead of
broad parent pages or repository-wide placeholders. The same rebuild
revalidated the existing mobile selector inventory: 225 source-backed rows
across 91 source URLs, comprising 200 selectors, 18 setting or x-ray context
rows, and seven notes, with no missing URL or stale dependency findings.

## Resolved Technical Gates

The 2026-08-03 live review closed the three technical and content-quality items
that were open at the start of the review:

1. The verification layer now reports 83 of 83 resolutions verified against
   exact source snapshots, immutable public source, or bounded official API
   observations, with zero unresolved rows, zero stale evidence, and zero
   default-cutover blockers. The 2026-08-04 refresh corrected blanket cache-tag
   immutability, narrowed cache-tag normalization by release, and corrected
   check-in helper timestamp types from `DateTime` to `DateTimeOffset` where the
   Rock 19.4 source requires it. It also reconciled the current Rock workspace
   debugger configuration against immutable public source and kept mutable web
   evidence bound to semantic article content rather than volatile page chrome.
   The final live pass also rebound two unchanged Mailgun SMTP conclusions to
   the current official page hash without changing their reviewed wording.
2. A maintainer approved all seven exact-statement collapse groups against the
   current packet hash. Canonical retrieval retains all source evidence,
   concept facets, and public aliases while removing nine redundant public
   rows from the candidate.
3. The privacy-bounded `concept:security-permissions` outcome was reproduced.
   The exact concept body was truncated and contained generated index tables
   instead of the detailed guide. Compact concept routing plus bounded
   `guide_section` rows fixes that retrieval contract. Two tracked security
   section evaluations now pass at rank one with official or
   source-code-confirmed authority.

The quantitative readiness report therefore passes every technical check.

## Cutover Decision

The versioned policy records a
`maintainer_approved_reversible_technical_cutover`. Canonical was activated on
2026-08-03 only after the hosted gate passed, and explicit legacy retrieval was
tested as the rollback. The technical gate remains strict: zero retrieval,
exact-lookup, authority, no-answer, endpoint, or live-verification regressions
are allowed. Every release must preserve that rollback and expose the active
projection plus content hash in health.

The prior external thresholds remain as advisory post-cutover validation goals:
five opted-in installations, 50 decisive comparisons, all six question
categories, and a 2:1 canonical-to-legacy preference ratio. Maintainer,
evaluation, and synthetic traffic still do not count as external evidence, and
no missing external data is represented as if it existed.

## Next Sequence

Two bounded legacy-migration batches now cover four workflow articles, five
Engagement Steps articles, and the refreshed developer debugger article. Across
the reviewed bundle, 26 exact legacy retirement or retention decisions and
three source-native identity migrations are recorded. The final projection has
293 typed artifacts; 594 legacy claims and 5,553 legacy source summaries remain.
The 484-question production-worker shadow reported 321 improvements, 163 ties,
and zero retrieval, exact-lookup, authority, no-answer, or endpoint regressions.
All 83 verification rows remain resolved with no blocker.

The deterministic migration-priority compiler currently identifies 1,618
actionable official-prose source records: 1,265 are migration-ready, 351 require
a source refresh first, and two require concept-routing review. Three prior
records are deliberately retained, two same-family legacy IDs resolve through
exact canonical-URL aliases, and no source identity remains unresolved. A fixed
`--as-of` run reproduced the same input and report hashes on consecutive builds.

1. Continue privacy-bounded outcomes and blind comparisons as post-cutover
   validation. Do not retain queries, organization identifiers, Rock data, or
   free-form comparison feedback.
2. Migrate legacy claims and source summaries in
   bounded source-family batches. Each batch must demonstrate stable identity,
   exact hash-bound retirement decisions, no silent loss of previously exposed
   source-native IDs, no retrieval regressions, and rebuildable provenance
   before replacing its legacy projection.
3. Select each migration batch from measured retrieval value, source freshness,
   and verification debt rather than bulk-converting the remaining queue.
4. Re-run the guarded canonical activation checks after each deployed batch and
   keep legacy available until the new projection and public client are verified.

## Not Next

- Do not rebuild the repository from scratch; the shadow results favor an
  incremental migration with less identity and safety risk.
- Do not make vector retrieval the default. The prior vector shadow did not
  justify promotion, and the current canonical lexical projection already
  improves semantic cases without exact-lookup regressions.
- Do not flatten issues, Ideas, recipes, Model Map records, Lava contexts, or
  contributions into prose claims.
- Do not make OKF the primary online agent interface. It remains the versioned
  portability and bulk-distribution projection; MCP is the primary interactive
  interface and CLI is the local/operator fallback.
- Do not count maintainer, synthetic, or evaluation traffic as independent
  external evidence.

## Revalidation

Reassess this decision if hosted canonical retrieval fails a strict regression
gate, a source-family contract changes, a new source shape cannot be represented
without loss, or a future retrieval shadow demonstrates a material improvement
over the current canonical projection. Use the commands and review controls in
`docs/runbooks/canonical-knowledge-shadow.md`; do not update this status from
generated counts alone.
