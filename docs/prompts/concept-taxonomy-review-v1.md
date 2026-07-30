# Concept Taxonomy Review Prompt

Prompt ID: `rock-kb-concept-taxonomy-review`

Prompt version: `1.0.0`

Recommended model: `gpt-5.6-sol`

Recommended reasoning effort: `xhigh`

Use this prompt to propose changes to `concepts/registry.yaml`. The model is an
analyst, not the taxonomy owner: it may propose changes, but a maintainer must
review the evidence and edit the registry.

## Inputs

- The current concept registry and taxonomy audit.
- Current Rockumentation documentation and developer branch inventories.
- Per-concept answer-bearing, routing-only, source, issue, recipe, Lava-context,
  and model-map counts.
- Retrieval evaluation failures, repeated zero-result topics, exact-lookup
  failures, and consented outcome reason codes.
- A bounded sample of representative user questions.
- Public Rock source-code evidence when it clarifies distinct implementation
  areas. Use immutable commit references.
- Aggregated, public-safe conclusions from bounded read-only instance checks
  only when installed configuration or issue applicability affects routing.

## Decision Rules

1. Concepts are task-oriented retrieval facets, not a mirror of the
   documentation navigation tree.
2. Prefer an existing concept or subguide when a topic shares the same users,
   entities, operations, and troubleshooting path.
3. Propose a first-class concept only when evidence shows a durable,
   operationally distinct cluster with enough authoritative source material and
   answer demand to justify separate routing.
4. Treat official documentation branches as deterministic routing signals.
   They may support a concept but do not create one automatically.
5. Give each unambiguous branch one primary owner. Use cross-cutting or
   aggregate concepts for intentional secondary discovery.
6. Keep one canonical knowledge row with multiple concept facets. Do not copy a
   claim, recipe, issue, task card, or context row into concept-specific
   duplicates.
7. Identify scope overlap explicitly. Include examples that belong and examples
   that should route elsewhere.
8. Do not infer demand from source volume alone. Query evidence, operational
   importance, and failure cost matter.
9. Do not merge concepts merely to reduce the count when their user workflows
   differ.
10. Never use private organization data, raw queries, or private Rock evidence
    in the public proposal.
11. A single organization's instance may reveal a retrieval need, but it cannot
    establish a public concept or universal Rock behavior by itself.

## Output

Return one JSON object:

```json
{
  "schema": "rock-kb-concept-taxonomy-proposal-v1",
  "registry_version_reviewed": 2,
  "prompt_id": "rock-kb-concept-taxonomy-review",
  "prompt_version": "1.0.0",
  "model": "exact-model-id",
  "reasoning_effort": "xhigh",
  "proposals": [
    {
      "action": "add|change|merge|retire|keep",
      "concept_ids": ["existing-or-proposed-id"],
      "routing_role": "primary|cross_cutting|aggregate",
      "parent_concept_id": "",
      "scope_in": ["bounded example"],
      "scope_out": ["bounded example"],
      "documentation_branches": ["structured/branch"],
      "evidence": {
        "source_count": 0,
        "answer_bearing_claim_count": 0,
        "retrieval_failures": [],
        "representative_questions": []
      },
      "reason": "Concise evidence-backed rationale.",
      "risks": [],
      "required_evaluation_cases": []
    }
  ],
  "no_change_reasons": [],
  "review_notes": []
}
```

Return no registry edits. A proposal without source evidence and retrieval or
operational justification should be rejected.
