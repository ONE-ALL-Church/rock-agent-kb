# Canonical Knowledge Architecture Status

Date: 2026-08-03

Status: accepted architecture, shadow and opt-in canary only

## Decision

Continue evolving the current knowledge base. Do not rebuild it from scratch.
The source-native and canonical-shadow work has now demonstrated the right
architecture across every major source shape, while preserving the tested
legacy reader as the production default.

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

Legacy retrieval remains the default reader. The canonical projection remains
dual-written and available only through the explicitly selected canary until
both technical and external-usefulness gates pass.

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

The tracked source-native bundle now covers five source families, 38 articles,
15 concept facets, 1,488 addressable source units, and 239 reviewed artifacts:
66 claims, 24 recipes, 26 source summaries, 95 structured references, and 28
task cards. It also contains 77 typed relationships and 265 source-native
evaluation cases. All 38 generation activities used `gpt-5.6-sol`; the current
prompt is `source-knowledge-distillation-v2.3` version `2.3.1`.

The 2026-08-03 canonical retrieval shadow evaluated 430 questions through the
production Worker's local FTS and ranking implementation:

- 267 improved, 163 were unchanged, and none regressed;
- exact lookup, authority, no-answer, and endpoint compatibility regressions
  were all zero;
- all ten exact REST and stateless MCP compatibility cases passed; and
- serialized canonical projection storage increased by 5.402 percent, within
  the 10 percent gate.

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

This is strong evidence that the architecture is better than the legacy-only
projection. It is not enough to make the canary the default. Maintainer tests
can prove deterministic behavior and catch regressions, but cannot prove that
unfamiliar agents and churches find the new projection more useful.

The canonical projection still identifies measurable migration debt: 610
legacy claims and 5,566 legacy source summaries remain alongside 239
source-native artifacts and deterministic typed families. That inventory is a
migration queue, not a reason to discard the working system.

## Resolved Technical Gates

The 2026-08-03 live review closed the three technical and content-quality items
that were open at the start of the review:

1. The three `Configure Email` artifacts were revalidated against the unchanged
   current Rock article and current official provider evidence. The live audit
   now reports 69 of 69 resolutions verified, zero unresolved rows, and zero
   default-cutover verification blockers.
2. A maintainer approved all seven exact-statement collapse groups against the
   current packet hash. Canonical retrieval retains all source evidence,
   concept facets, and public aliases while removing nine redundant public
   rows from the candidate.
3. The privacy-bounded `concept:security-permissions` outcome was reproduced.
   The exact concept body was truncated and contained generated index tables
   instead of the detailed guide. Compact concept routing plus bounded
   `guide_section` rows fixes that retrieval contract. Two tracked security
   section evaluations now pass at rank two with official or
   source-code-confirmed authority.

The quantitative readiness report therefore passes every technical check.

## Remaining Gate

Default cutover remains blocked only by independent external usefulness
evidence. The canary currently has zero anonymously opted-in external
installations and zero external paired comparisons. The versioned policy
requires at least five installations, 50 decisive comparisons, coverage of
exact lookup, issue, no-answer, normal task, semantic, and version-sensitive
questions, and at least a 2:1 canonical-to-legacy preference ratio.

Maintainer, evaluation, and synthetic traffic cannot satisfy this gate. The
current readiness decision is `remain_opt_in_canary`; passing technical checks
does not authorize a default-reader change or a deployment.

## Next Sequence

1. Review, merge, and deploy the compact concept and guide-section projection
   through the normal public release workflow. Do not change the default
   reader during that release.
2. Run the blind paired canary with consenting external testers until the
   versioned policy thresholds are met. Do not retain queries, organization
   identifiers, Rock data, or free-form feedback.
3. Rerun the canonical retrieval shadow, live verification audit, source-native
   readiness gate, full tests, and public audits. A passing report still
   requires an explicit reviewed release to change the default reader.
4. After the cutover decision, migrate legacy claims and source summaries in
   bounded source-family batches. Each batch must demonstrate stable identity,
   no retrieval regressions, and rebuildable provenance before replacing its
   legacy projection.

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
- Do not count maintainer, synthetic, or evaluation traffic toward the external
  promotion gate.

## Revalidation

Reassess this decision when the default-cutover gate passes, a source-family
contract changes, a new source shape cannot be represented without loss, or a
future retrieval shadow demonstrates a material improvement over the current
canonical projection. Use the commands and review controls in
`docs/runbooks/canonical-knowledge-shadow.md`; do not update this status from
generated counts alone.
