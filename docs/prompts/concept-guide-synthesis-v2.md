# Concept Guide Synthesis Prompt

Prompt ID: `rock-kb-concept-guide-synthesis`

Prompt version: `2.0.0`

Recommended model: `gpt-5.6-sol`

Recommended reasoning effort: `xhigh`

Write an original, agent-first Rock RMS guide from the supplied structured
evidence pack.

## Evidence Order

1. Approved answer-bearing claims are the factual spine.
2. Official documentation, release notes, source code, Model Map records, and
   Lava capability/context rows may add detail when the supplied excerpt
   directly supports it.
3. Reviewed community contributions and recipes are examples, not official Rock
   behavior.
4. Routing-only claims and source summaries help locate material; they are not
   facts to restate as answers.
5. Private draft records, when explicitly present, are local hypothesis inputs
   only. Never quote or cite them publicly.
6. Public GitHub source excerpts may clarify implementation when the pack
   includes an immutable commit reference. Treat code as implementation
   evidence, not proof of an installation's configuration.
7. Live-instance evidence is optional and belongs in a separate bounded,
   read-only review. Use only a reviewed public-safe conclusion supplied in the
   pack. Never invent a SQL result or treat one organization's data as universal.

Do not invent a fact to complete an outline. Mark a gap instead.

## Writing Rules

- Prefer a bounded operational guide over an encyclopedic essay. Typical length
  is 2,500-6,000 words; use less when evidence is thin.
- Every factual section needs an inline source link or a clearly identified
  approved claim source.
- Preserve permissions, configuration, version, packaging, provider, and
  live-verification conditions.
- Distinguish current documented behavior, source-code observations, community
  patterns, historical behavior, and upcoming or pre-alpha behavior.
- Do not infer functionality from a title, model name, property name, branch
  name, or nearby article.
- Avoid generic advice such as "check the documentation" when the evidence
  supports a concrete inspection.
- Keep one topic in its owning concept; link related concepts instead of
  reproducing their guides.
- Never include secrets, local paths, raw transcripts, raw API payloads,
  organization-specific IDs, or private instance evidence.
- When the answer depends on installed schema, configuration, plugin state,
  version applicability, or issue reproduction and no reviewed live evidence is
  supplied, put that check under `Known Gaps And Live Verification`.

## Required Structure

Output Markdown only with this frontmatter:

```yaml
---
id: authored-<concept-id>
title: <concept-title>
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---
```

Then include:

1. `# <concept-title>`
2. `## Agent Summary`
3. `## Scope And Boundaries`
4. `## Mental Model`
5. One `##` section for each evidence-supported subguide.
6. `## Version And Authority Caveats`
7. `## Troubleshooting Decision Tree`
8. `## Agent Task Recipes`
9. `## Known Gaps And Live Verification`
10. `## Source Map`

Under `Troubleshooting Decision Tree`, use one `###` heading per actual symptom.
Give ordered or bulleted checks in the order an agent should perform them.

Under `Agent Task Recipes`, use one `### Recipe: ...` heading per task. Give a
specific outcome and ordered steps. Include `Inspect:`, `Do not assume:`, or
`Stop when:` lists when relevant. These sections are parsed into first-class
retrieval records, so do not use placeholder steps.

Before returning, verify that each assertion follows from the evidence pack,
that routing-only text was not promoted into factual prose, and that the guide
does not imply live verification that did not occur.
