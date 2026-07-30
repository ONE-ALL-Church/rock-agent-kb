# Claim Tier Policy

The KB separates public-source review from live-operational verification. A claim can be safe to cite publicly without being safe to use as a concrete operational answer.

## Tiers

- `routing_context_only`: An internal review disposition for text that helps
  route an agent to a source, concept, or training page but does not assert
  concrete Rock knowledge. These rows remain in source-summary and review
  indexes; they are excluded from the public approved-claim graph.
- `source_backed`: The claim is public-safe and source-backed, but still needs a live Rock instance or concrete object before it is used operationally. It can appear in guides with caveats and in review queues.
- `answer_pack_approved`: The claim is reviewed enough for generated answer prose without additional live evidence. Use this only for claims that do not depend on a local configured object.
- `live_verified`: The claim has concrete read-only evidence from a connected Rock instance, model map, source code, or other verified surface. The evidence must be recorded in `data/review/live-claim-verifications.jsonl`.

## Promotion Rules

- Do not promote `source_backed` claims to `live_verified` from source text alone.
- Reviewer dispositions under `claims/claim-review-dispositions.jsonl` may move
  a source-backed claim to `answer_pack_approved` when the cited public source
  directly supports bounded, non-instance-specific guidance, or to
  `routing_context_only` when the claim is preview, partner, roadmap, or
  external-policy context. These dispositions never create `live_verified`
  evidence.
- A read-only SQL probe can verify structural inspection claims, such as the existence of `Auth`, `Page`, `Block`, `DataView`, `Report`, `ConnectionRequest`, `NoteType`, or related columns.
- A schema probe cannot verify that a specific page, workflow, Data View, API key, check-in area, security role, or ministry process is configured correctly. Those claims need a named live object and object-specific evidence.
- Generated answer-pack prose may use only `answer_pack_approved` and `live_verified` claims. Reviewed distilled claims are built only from those same tiers.
- Ordinary hosted search defaults to `source_backed`, so
  source summaries and other routing-only records require an explicit opt-in.
  Dedicated issue and Idea tools remain available for explicit report or
  roadmap intent.
- `answer_candidate` is derived from the final claim tier and is true only for
  `answer_pack_approved` and `live_verified` claims.

## Current Batch

The first connected-instance pass used read-only SQL against a connected Rock instance and promoted only structural claims backed by private schema evidence retained outside the public tree.
