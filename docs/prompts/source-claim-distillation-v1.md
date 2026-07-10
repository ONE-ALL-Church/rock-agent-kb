# Source Claim Distillation Prompt

Prompt ID: `rock-kb-source-claim-distillation`

Prompt version: `1.0.0`

Use this prompt for one official Rockumentation article candidate at a time. The candidate contains private working context hydrated from the public Rockumentation API. Return public-safe paraphrases only; do not copy article sentences, private paths, raw API payloads, or local review context.

## Inputs

- Candidate metadata, including `candidate_id`, source URL, article ID, documentation path, current documentation version, concept IDs, and `source_input_hash`.
- `source_context`, containing the exact bounded article text represented by `source_input_hash`.
- Relevant existing claims for duplicate comparison.
- Current release notes, source code, model-map evidence, or live verification only when needed to qualify the article.

## Task

Decide whether the article contains durable, reusable knowledge that should enter the canonical claim graph. Navigational pages, headings without explanatory content, marketing language, and statements already covered by stronger claims should produce no claim.

For each retained claim:

1. Express one independently testable behavior, configuration rule, implementation pattern, risk, recipe, or release caveat.
2. Preserve the article's operational conditions, such as required permissions, configuration, provider, installation, or Rock version.
3. Distinguish current documented behavior from recommendations, historical behavior, and release-sensitive details.
4. Prefer a specific fact that helps an agent answer or troubleshoot a Rock question. Do not write generic phrases such as "this article is useful" or "verify the documentation."
5. Do not infer behavior from an article title, navigation tree, model name, or adjacent article.
6. Split unrelated assertions into separate claims. Keep closely coupled cause-and-effect behavior together.
7. Compare against `existing_claims`; reject duplicates unless this article supplies materially stronger authority or a missing caveat.
8. Use only concept IDs present in the candidate or the current concept registry.

Before returning output, check:

- Does the full sentence follow from this article alone?
- Could a reader mistake version-specific documentation for universal behavior?
- Is the displayed version a Rock product version or only the version of a developer documentation set? Do not put documentation-set versions in `rock_versions`.
- Is the claim a paraphrase rather than copied article prose?
- Is it more useful than routing an agent directly to the article?
- Does it add knowledge not already represented by an existing claim?

Return zero claims when those checks fail.

## Output

Return one JSON object with this shape:

```json
{
  "schema": "rock-kb-document-claim-rewrite-v1",
  "candidate_id": "document-claim-candidate:...",
  "source_input_hash": "candidate-source-input-sha256",
  "claims": [
    {
      "claim": "One atomic, public-safe, source-supported claim.",
      "claim_type": "behavior|configuration|implementation_pattern|release_caveat|risk|recipe|source_summary|operational_guidance",
      "concept_ids": ["existing-concept-id"],
      "evidence_class": "current_behavior|demonstration|partner_or_custom|historical|operational_recommendation|exploratory_roadmap",
      "temporal_status": "current|release_sensitive|exploratory|unknown",
      "rock_versions": ["19.0"],
      "confidence": "high",
      "needs_live_verification": false
    }
  ],
  "review_notes": [
    "Full article reviewed.",
    "Atomicity, version scope, duplicate coverage, and paraphrase checked."
  ]
}
```

Use the candidate's `source_input_hash` unchanged. Do not calculate it from the claim or a smaller excerpt. The promotion command rejects mismatched hashes, unknown concepts, exact duplicate claims, invalid claim types, and verbatim article sentences.

Candidates using the default `agent_reviewed_full_article` method are never truncated. If an article exceeds the configured review boundary, the candidate builder skips it instead of presenting bounded text as a full-article review.
