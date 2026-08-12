# Canonical Knowledge Architecture Status

Date: 2026-08-03

Last updated: 2026-08-12

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
| Legacy claims and source summaries | Explicit loss-prevention debt. Re-read the complete current source, emit any useful new typed artifacts, and preserve exact lookup through reviewed aliases. A legacy source summary may resolve to the best independently useful typed primary; do not manufacture a same-type summary merely to retire it. |

The reviewed machine-readable source-family contracts in
`canonical/source-family-contracts-v1.json` are authoritative when prose and
code disagree.

Concept routing is also source-native. Reviewed artifact assignments and exact
API-derived article paths are strong routing evidence. Registry topics describe
the source as a whole and require independent corroboration in the article
title, path, summary, or excerpt before they can become high-confidence article
facets. This prevents broad developer-source tags such as Lava or Obsidian from
being copied onto unrelated C# articles.

## Current Evidence

The tracked source-native bundle now covers five source families, 147 articles,
27 concept facets, 2,889 addressable source units, and 603 reviewed artifacts:
143 claims, 57 recipes, 107 source summaries, 226 structured references, and 70
task cards. It also contains 723 typed relationships and 629 source-native
evaluation cases. All 147 generation activities use `gpt-5.6-sol` and input
hash version `2`. The manifest preserves the exact prompt history: four initial
distillations at version `2.3.1`, 26 migration activities at wrapper version
`1.3.0`, 57 at wrapper version `1.3.1`, and 60 at wrapper version `1.3.3`.

The corrected 2026-08-12 low-risk pilot selected 30 Apple TV developer records
exactly once under hydrated risk policy v8 and processed 269 source units into
44 reviewed artifacts: four claims, ten recipes, ten source summaries, 18
structured references, and two task cards. All 30 legacy records were replaced.
Explicit review changed nine articles across 37 exact paths: 25 artifact-shape,
two relationship, and ten verification corrections. Review raised 15
verification requests, all of which were corrected or narrowed against current
official documentation or immutable public source before promotion. The final
bundle therefore records 211 exact legacy migrations, seven artifact
migrations, and 99 of 99 resolved verification decisions with no blocker.

The 2026-08-12 deterministic migration pilot selected 30 current source records
exactly once and processed 450 source units into 61 reviewed artifacts. Twelve
model outputs required maintainer changes across 47 exact correction paths.
Promotion recorded 59 additional legacy replacements and no new source-native
artifact migration, bringing the bundle to 181 exact legacy migrations and
seven artifact migrations. Hydrated risk policy v8 subsequently classified 27
of those records as low risk and three as high risk because they document
persistent mutation or permission-gated administration surfaces. Those three
records had explicit source-level maintainer review, so their knowledge remains
reviewed, but the mixed batch is not evidence for a 30-record low-risk run. The
compiler distilled each complete source record without trying to reproduce each
legacy row. Legacy knowledge is an explicit loss-prevention ledger: it must be
replaced, retained, or retired, but it neither caps artifact count nor prevents
the source from yielding useful knowledge that had no legacy counterpart.

The closest preserved 10-record comparison is one reviewed worker shard from
the prior pilot, not a standalone sealed batch. It processed 195 units into 26
artifacts and required two relationship corrections. The corrected pilot
processed three times as many records, 1.379 times as many units, and 1.692
times as many artifacts. Its preparation, assembly, and review-validation
phases took 34.631, 0.018, and 0.027 seconds. Generation time, active maintainer
review time, token counts, and billing records were not captured for either
comparison and remain explicitly unavailable; no cost estimate is presented as
observed evidence.

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
and preserve the redirected `/lava/commands` identity. The seven older static
parser-`1.0.0` records have now been refreshed and reviewed under parser
`1.1.0`: AI Agents v19, Types of Shortcodes, Fluid Differences, Volunteer
Onboarding, RockCast 197, Mobile v19, and Tag List. Their legacy and
source-native identities were explicitly retained or replaced; none remains as
hidden parser debt.

The 2026-08-10 migration completed the next coherent Group, Communication,
Core, Media, and parser-refresh batch. It migrated Group Attendance Digest,
Group Type Requirements, Core Field Type Patterns, Media Player, and
Communication Lists, then refreshed the seven parser records above. The batch
records 81 exact legacy migrations and five source-native artifact migrations.
Communication Lists was additionally checked against immutable current Rock
source for its seeded categories and sample lists; mutable Mailgun references
were rebound to current official content hashes without changing their reviewed
meaning.

The 2026-08-11 migration compiled all 19 records that were already ready for
review, including the HighlightDetailColumn, Check-In, communication, security,
and system-administration groups. It then migrated the bounded hosting and
security set for articles 1044, 1046, 1047, and 2137 plus selected engagement
and CMS records. The manifest now records 122 exact legacy migrations and seven
source-native artifact migrations. The same batch reconciled the old
`/lava/commands` identity to `/lava/commands/getting-started` and replaced two
keyword-only concept routes with exact source-record routes. Source verification
corrected or narrowed mutable SQL Server, Mailgun/Gmail unsubscribe, Check-In,
cache, File Manager, and content-channel details instead of promoting their
earlier wording unchanged. All 71 active verification decisions resolve with no
blocker: 34 confirm source wording, 22 correct it, and 15 narrow its scope.
Redistillation now carries those knowledge-changing decisions forward only when
the stable artifact identity and source-input hash are unchanged; changed or
partially replaced inputs require explicit re-review. A newer verified decision
can retire an older correction only when it fully covers the older artifact set.

The same refresh now yields 60 normalized Lava records and 285 distinct
capability rows, including 26 named command rows and 36 high-risk rows with
mandatory security and live-verification guidance. The parser now uses the
document title when the page shell exposes the generic `Lava Tags/Commands`
heading. A hash-verified presentation rebind corrected the reviewed Getting
Started snapshot and all 13 contextual prefixes while preserving its source
snapshot identity, content hash, source-unit IDs, redirect alias, reviewed
artifact, and original Sol generation activity.

The final 2026-08-12 canonical retrieval shadow evaluated 800 questions through
the production Worker's local FTS and ranking implementation:

- 636 improved, 164 were unchanged, none regressed, and no failures were shared
  by both projections;
- exact lookup, authority, no-answer, and endpoint compatibility regressions
  were all zero;
- all ten exact REST and stateless MCP compatibility cases passed; and
- serialized canonical projection storage increased by 7.789 percent, within
  the 10 percent gate.

The candidate achieved recall `1.0`, mean reciprocal rank `0.992063`, authority
correctness `1.0`, and duplicate rate zero. A repeated paired run against the
same pinned Worker bundle measured mean latency at 85.273 milliseconds and p95
at 127.32 milliseconds, both within the unchanged 20 percent limits. Ranking
now reads reviewed independent questions from both the
original and verified-effective artifact shapes, and exact schema-object
questions receive a bounded identifier signal only when they name both a
distinctive code identifier and field, property, type, schema, or member intent.

The final isolated service quality gate also passed all 166 tracked questions.
Availability and recall were `1.0`, mean reciprocal rank was `0.992929`,
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

The canonical projection still identifies measurable migration debt: 1,512
active legacy-backed source records remain alongside 603 source-native
artifacts and deterministic typed families. Of those records, 1,495 are
actionable and migration-ready and 17 are reviewed retentions. That inventory
is a loss-prevention queue, not a reason to discard the working system and not
a complete inventory of current sources that never had a legacy projection.

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

1. The current source-native verification layer reports 99 of 99 resolutions
   verified against exact source snapshots, immutable public source, or bounded
   official API
   observations, with zero unresolved rows, zero stale evidence, and zero
   default-cutover blockers. The 2026-08-04 refresh corrected blanket cache-tag
   immutability, narrowed cache-tag normalization by release, and corrected
   check-in helper timestamp types from `DateTime` to `DateTimeOffset` where the
   Rock 19.4 source requires it. It also reconciled the current Rock workspace
   debugger configuration against immutable public source and kept mutable web
   evidence bound to semantic article content rather than volatile page chrome.
   The August 10 live pass additionally rebound three unchanged Mailgun
   conclusions to current official page hashes without changing their reviewed
   corrections or narrowings. The August 11 pass compacted the active queue to
   71 fully resolved decisions and added the SQL Server, unsubscribe, Check-In,
   cache, File Manager, and content-channel corrections described above. The
   first August 12 pilot added 13 reviewed verification decisions, leaving 84
   fully resolved decisions. The corrected low-risk Apple TV pilot added 15
   more corrected or narrowed decisions, leaving 99 fully resolved decisions
   and no blocker.
   Immutable Rock source separately confirms the Helix endpoint authorization
   map and the Default Enabled Lava Commands fallback introduced by the prior
   batch.
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

The reviewed source-native bundle now records 211 exact legacy migrations and
seven source-native artifact migrations. The final projection has 603 typed
artifacts. The 800-question production-worker shadow reported 636 improvements,
164 ties, no shared failures, and zero retrieval, exact-lookup, authority,
no-answer, or endpoint regressions. All 99 current verification rows remain
resolved with no blocker.

The regenerated deterministic migration-priority queue contains 1,512 active
legacy source records: 1,495 are actionable and migration-ready and 17 are
reviewed retentions. It has zero unresolved source identities and six
reconciled aliases after the Lava alias
and exact-route work. The highest current ready cluster is Obsidian developer
content. The legacy-backed queue is not the complete source inventory; each
source family must also be audited for current public records that have no
legacy projection so fresh-source knowledge is not omitted.
The queue must be regenerated after every reviewed batch; stale counts from a
prior batch must not drive selection.

1. Continue privacy-bounded outcomes and blind comparisons as post-cutover
   validation. Do not retain queries, organization identifiers, Rock data, or
   free-form comparison feedback.
2. Select the next coherent compiler-ready group from the regenerated queue,
   favoring high-demand official prose with current source hashes. Each batch
   must demonstrate stable identity, exact hash-bound retirement decisions, no
   silent loss of previously exposed source-native IDs, no retrieval
   regressions, and rebuildable provenance.
3. Refresh stale sources only when they enter a bounded migration batch; do not
   broaden a migration into an unconditional corpus refresh.
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
