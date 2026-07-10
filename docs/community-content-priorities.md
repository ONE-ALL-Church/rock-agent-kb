# Community Content Priorities

The Rock KB already imports broad official documentation. Community submissions
are most valuable when they capture reusable operational knowledge that official
documentation does not fully express.

## Highest Priority

1. Reusable recipes with public code, immutable commit pins, adaptation points,
   validation evidence, security boundaries, and tested Rock versions.
2. Difficult troubleshooting paths that distinguish similar symptoms and show
   the order of checks that identified the real cause.
3. Failure modes and recovery guidance, especially where a normal-looking Rock
   configuration can still produce incorrect behavior.
4. Version caveats that identify when an entity, field, Lava root, API, block,
   workflow action, or operational behavior changed.
5. Verified reusable workflows that connect multiple Rock areas without copying
   production IDs or private organizational data.

Broad summaries of official manuals, generic feature descriptions, copied
documentation, raw transcripts, and organization-specific configuration dumps
are low priority.

## Review Score

Score a candidate before submission. Candidates scoring 14 or more should be
reviewed first.

| Signal | Points |
|---|---:|
| Solves a recurring operational task | +4 |
| Documents a hard-to-diagnose failure or decision tree | +4 |
| Includes public evidence or immutable public code | +4 |
| Names tested Rock versions or a precise version caveat | +3 |
| Reusable across organizations with explicit adaptation points | +3 |
| Connects to exact KB concepts, model slugs, recipes, or Lava contexts | +2 |
| Requires live verification but clearly defines it | +1 |
| Merely repeats an official manual or existing KB result | -5 |
| Depends on private IDs, URLs, data, or unreleasable code | reject |

Use [the candidate review template](templates/content-candidate-review.md) to
record the score and evidence. A high score prioritizes review; it does not
bypass contribution validation, trust tiers, redaction, licensing, or live
verification.
