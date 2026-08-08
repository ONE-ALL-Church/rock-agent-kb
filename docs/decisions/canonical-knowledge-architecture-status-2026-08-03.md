# Canonical Knowledge Architecture Status

Date: 2026-08-03

Last updated: 2026-08-08

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

The tracked source-native bundle now covers five source families, 64 articles,
23 concept facets, 2,052 addressable source units, and 391 reviewed artifacts:
117 claims, 26 recipes, 54 source summaries, 145 structured references, and 49
task cards. It also contains 343 typed relationships and 417 source-native
evaluation cases. All 64 generation activities use `gpt-5.6-sol` and input
hash version `2`. The manifest preserves the exact prompt history: 31 initial
distillations at version `2.3.1`, 26 migration activities at wrapper version
`1.3.0`, and seven at wrapper version `1.3.1`.

The final 12 prompt-`2.3.0` documentation records were refreshed before
reprocessing. Their upstream content hashes were unchanged, so the change
isolates the extraction method rather than conflating it with source edits. The
reviewed pass processed 342 units into 100 artifacts, replacing 76 earlier
artifacts. Six exact-hash split rules separated mixed source units, and
maintainer review added one missed verification boundary for a release-sensitive
cache-tag deletion claim.

The 2026-08-08 TV, Helix, Obsidian, Roku, and Lava batch processed seven
refreshed records and 156 deterministic source units into 25 independently
retrievable artifacts. Review made 29 exact legacy decisions: 11 replacements
and 18 explicit retentions, with no unmatched routing terms. Static Lava pages
now extract the nested article rather than navigation chrome; this reduced the
Lava Commands candidate from 100 units to 13 and the Lava API candidate from
130 to 45. Parser version `1.1.0` and URL aliases make that change observable
and preserve the redirected `/lava/commands` identity. Seven older static
parser-`1.0.0` records remain distinguishable refresh debt: four community
articles and three Lava pages.

The same refresh now yields 60 normalized Lava records and 285 distinct
capability rows, including 26 named command rows and 36 high-risk rows with
mandatory security and live-verification guidance. The parser now uses the
document title when the page shell exposes the generic `Lava Tags/Commands`
heading. A hash-verified presentation rebind corrected the reviewed Getting
Started snapshot and all 13 contextual prefixes while preserving its source
snapshot identity, content hash, source-unit IDs, redirect alias, reviewed
artifact, and original Sol generation activity.

The final 2026-08-08 canonical retrieval shadow evaluated 586 questions through the
production Worker's local FTS and ranking implementation:

- 422 improved, 164 were unchanged, none regressed, and no failures were shared
  by both projections;
- exact lookup, authority, no-answer, and endpoint compatibility regressions
  were all zero;
- all ten exact REST and stateless MCP compatibility cases passed; and
- serialized canonical projection storage increased by 6.576 percent, within
  the 10 percent gate.

The final isolated service quality gate also passed all 166 tracked questions.
Availability and recall were `1.0`, mean reciprocal rank was `0.99596`,
authority correctness was `1.0`, and duplicate rate was zero. One broad Check-In
setup question placed an accepted source-native result at rank three, within its
tracked target. This gate exercises the same generated D1 projection and Worker
bundle used by the deployment workflow.

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

The canonical projection still identifies measurable migration debt: 578
legacy claims and 5,541 legacy source summaries remain alongside 391
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

1. The verification layer now reports 91 of 91 resolutions verified against
   exact source snapshots, immutable public source, or bounded official API
   observations, with zero unresolved rows, zero stale evidence, and zero
   default-cutover blockers. The 2026-08-04 refresh corrected blanket cache-tag
   immutability, narrowed cache-tag normalization by release, and corrected
   check-in helper timestamp types from `DateTime` to `DateTimeOffset` where the
   Rock 19.4 source requires it. It also reconciled the current Rock workspace
   debugger configuration against immutable public source and kept mutable web
   evidence bound to semantic article content rather than volatile page chrome.
   The final live pass also rebound eight unchanged Google, Mailgun, Android,
   and mobile-shell conclusions to current official page hashes without
   changing their reviewed corrections or narrowings. Immutable Rock source
   separately confirms the Helix endpoint authorization map and the Default
   Enabled Lava Commands fallback introduced by the latest batch.
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

The reviewed source-native bundle now records 61 exact legacy replacement
migrations and three source-native identity migrations. The final projection
has 391 typed artifacts; 578 legacy claims and 5,541 legacy source summaries
remain. The 586-question production-worker shadow reported 422 improvements,
164 ties, no shared failures, and zero retrieval, exact-lookup, authority,
no-answer, or endpoint regressions. All 91 verification rows remain resolved
with no blocker.

The deterministic migration-priority compiler currently identifies 1,602
actionable official-prose source records: 1,302 are migration-ready, 298 require
a source refresh first, and two require concept-routing review. Twelve prior
records are deliberately retained, five legacy URL-hash IDs resolve through
exact reviewed source URLs, and no source identity remains unresolved. The
highest-value fresh candidates are the Group Attendance Digest Email, applying
requirements to group types, the Media Player Lava Shortcode, Communication
Lists, and the already-distilled Core Field Type Patterns migration compiler.

1. Continue privacy-bounded outcomes and blind comparisons as post-cutover
   validation. Do not retain queries, organization identifiers, Rock data, or
   free-form comparison feedback.
2. Migrate the next coherent group-operations batch, starting with the Group
   Attendance Digest Email, group requirements, and Communication Lists. Each
   batch must demonstrate stable identity,
   exact hash-bound retirement decisions, no silent loss of previously exposed
   source-native IDs, no retrieval regressions, and rebuildable provenance
   before replacing its legacy projection.
3. Run the legacy compiler for already-distilled Core Field Type Patterns, and
   keep the Media Player Lava Shortcode in a separate CMS/Lava batch.
4. Refresh the remaining seven parser-`1.0.0` static records and source records
   that the priority compiler marks stale before model work.
5. Re-run the guarded canonical activation checks after each deployed batch and
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
