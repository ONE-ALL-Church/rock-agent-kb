# Source-Native Documentation Expansion

Date: 2026-07-31

> **Updated status, 2026-08-03:** This document records the first expansion and
> its point-in-time evidence. The reviewed bundle has since expanded to five
> source families, 38 articles, 1,488 source units, and 239 reviewed artifacts.
> The current architecture decision, readiness evidence, and ordered next work are
> in
> [Canonical Knowledge Architecture Status](canonical-knowledge-architecture-status-2026-08-03.md).
> The historical counts below remain unchanged so the expansion stays
> auditable.

## Decision

Expand the reviewed source-native documentation bundle from the original
`system-admin-ops` and `check-in` pilot into `workflows`, `communications`, and
`security-permissions`. Keep the bundle in canonical shadow and opt-in canary
only. Legacy retrieval remains the production default.

Official documentation is distilled adaptively into claims, task cards,
recipes, structured references, and source summaries. The pipeline does not
target a fixed artifact count per article. Already structured source families,
including Rock issues, Ideas, Model Map, Lava contexts, recipes, and reviewed
contributions, retain deterministic typed ingestion contracts and are not
rewritten as prose claims.

## Evidence

- The expansion fetched 12 full-text Rockumentation articles through the
  official block-action API, four for each added concept.
- Deterministic parsing produced 386 addressable source units: 258 paragraphs,
  121 list items, five tables, and two code blocks.
- Maintainer review approved 74 typed artifacts: 19 claims, four recipes, nine
  source summaries, 30 structured references, and 12 task cards.
- The append-safe promotion preserved the original 12 articles and produced a
  24-article bundle with 722 source units and 150 reviewed artifacts.
- Twelve natural-language paraphrase holdouts supplement the exact artifact
  questions, bringing the source-native evaluation set to 176 cases.
- The canonical retrieval shadow evaluated 339 questions. The final comparison
  improved 178, left 161 unchanged, and regressed none. Exact lookup,
  authority, no-answer, endpoint-compatibility, and ranking regression counts
  remained zero.
- Candidate projection storage increased by 2,125,183 serialized JSONL bytes,
  or 4.132 percent, within the 10 percent gate.

## Review Controls

The stable model-input hash now includes the source snapshot, parser and split
derivation, every source unit and locator, concept facets, existing-claim
context, and documentation routing/version metadata. Volatile check timestamps
do not invalidate an unchanged input.

Eleven reviewed, content-hash-bound split rules repair only source units that a
maintainer confirmed contain independently useful material. A stale rule fails
closed. The model returned two additional split requests for one article; the
maintainer classified one sentence as a bounded reference detail and excluded
one speculative sentence. The generated and reviewed hashes preserve that
correction in generation provenance. Review also corrected inaccurate
model-authored schema notes in two articles. Three generation activities are
therefore marked as changed by maintainer review. Promotion never accepts
unresolved split requests.

Thirty-four source-native verification requests remain explicit in the public
safe queue. They identify mutable defaults, release-sensitive controls, or
external behavior that should be checked before an agent treats the detail as a
current live contract.

## Rollout Boundary

This result proves that the source-native typed architecture scales to three
additional documentation families without degrading retrieval. It does not
authorize a production-default cutover. Default MCP, CLI, hosted search, and
OKF behavior remain on the legacy projection until external canary outcomes
satisfy the existing reviewed promotion gate.
