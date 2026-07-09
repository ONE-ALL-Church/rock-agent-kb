# Media Claim Distillation Prompt

Prompt ID: `rock-kb-media-claim-distillation`

Prompt version: `1.0.0`

Use this prompt only after a media item has a private transcript candidate and a canonical public source URL. The output is a public-safe reviewer rewrite. It must not contain raw transcript passages, private paths, direct media files, signed player URLs, secrets, or organization-specific evidence.

## Inputs

- Candidate row, including `candidate_id`, canonical source metadata, `transcript_hash`, and allowed concept IDs.
- Complete transcript and timestamped segments when available.
- Current Rock version context, official documentation, release notes, or source-code references when needed to verify availability.
- Relevant approved claims for duplicate comparison.
- The exact model identifier used for review.

## Task

Review the complete source, not only a supplied timestamp. Produce a concise source summary and the smallest useful set of atomic claims. Each insight must express one reusable fact, caveat, recommendation, or implementation pattern that will help Rock administrators or developers beyond the source's original setting.

For every candidate insight:

1. Locate the strongest supporting timestamp.
2. Classify what the source is showing: current product behavior, a demonstration, partner or custom behavior, historical behavior, an operational recommendation, or exploratory roadmap work.
3. State release, configuration, permission, installation, or live-verification limits explicitly.
4. Separate built-in Rock behavior from examples that require a plugin, partner product, custom tool, Connected Service, or local configuration.
5. Remove filler such as "this source is useful" unless the row is intentionally routing-only.
6. Prefer a specific claim over a broad topic summary. Split claims joined by unrelated "and" clauses.
7. Reject claims that merely repeat a title, infer a capability from a model name, or cannot be traced to the source.
8. Compare the proposed claim against existing approved claims. Keep it only when it adds new detail, a better caveat, or stronger evidence.

Before returning output, perform an overclaiming check:

- Would a reader mistake a prototype or roadmap item for a shipped feature?
- Would a reader mistake one church's configuration for standard Rock behavior?
- Does the wording imply universal availability when permissions, versions, packaging, or installation matter?
- Does the claim combine multiple independently testable assertions?
- Does the cited timestamp actually support the complete sentence?

Rewrite or reject any item that fails this check.

## Output

Return one JSON object with this shape:

```json
{
  "candidate_id": "media-public-candidate:...",
  "source_url": "https://canonical-public-source.example/item",
  "source_title": "Source title",
  "summary": "A public-safe summary of the complete source and its authority limits.",
  "key_insights": [
    {
      "topic": "specific topic",
      "insight": "One atomic, source-supported claim with necessary availability or authority caveats.",
      "evidence_class": "current_behavior|demonstration|partner_or_custom|historical|operational_recommendation|exploratory_roadmap",
      "temporal_status": "current|release_sensitive|exploratory|unknown",
      "source_url": "https://canonical-public-source.example/item",
      "source_timestamp_url": "https://canonical-public-source.example/item?t=123s",
      "timestamp": "02:03",
      "timestamp_seconds": 123,
      "contains_verbatim_transcript": false
    }
  ],
  "concept_ids": ["existing-concept-id"],
  "topics": ["specific-topic"],
  "citations": [
    {
      "source_id": "registered-source-id",
      "url": "https://canonical-public-source.example/item"
    }
  ],
  "review_notes": [
    "Complete-source coverage and source limitations checked.",
    "Overclaiming, duplication, atomicity, and timestamp support checked."
  ],
  "generation_provenance": {
    "model": "exact-model-id",
    "prompt_id": "rock-kb-media-claim-distillation",
    "prompt_version": "1.0.0",
    "method": "agent_reviewed_whole_source",
    "source_input_hash": "candidate-transcript-sha256"
  }
}
```

Use only concept IDs already present in `concepts/registry.yaml`. Copy `source_input_hash` from the candidate's `transcript_hash`; do not recompute it from a truncated excerpt. The promotion command rejects provenance whose source hash does not match the candidate.

`evidence_class` and `temporal_status` are reviewer annotations retained with each insight. They supplement, but do not replace, current documentation, release notes, source code, model-map evidence, or read-only live verification.
