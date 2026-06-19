# API Branch Concept Routing Review

Date: 2026-06-19

## Decision

Keep the API-derived documentation branch metadata as a first-class routing signal for concept guides and agent artifacts. The current concept split is working as intended: the newer concepts route to coherent official documentation branches instead of relying only on keyword matches.

## Reviewed Concepts

| Concept | Primary API branch coverage | Total routed sources | Guide sources | Guide quality |
|---|---:|---:|---:|---:|
| `documents-signatures` | 20 articles from `documentation/core-concepts/documents` | 71 | 15 | 100, pass |
| `hosting-infrastructure` | 21 articles from `documentation/supporting-rock/hosting` | 72 | 32 | 100, pass |
| `prayer-care` | 17 articles from `documentation/engagement/prayer` | 61 | 29 | 100, pass |
| `engagement-tracking` | 72 articles across `documentation/engagement/steps`, `documentation/engagement/streaks`, `documentation/engagement/assessments`, and `documentation/engagement/additional-engagement-tools` | 91 | 15 | 100, pass |
| `obsidian-development` | 47 articles from `developer/obsidian` | 91 | 29 | 100, pass |
| `content-personalization` | 73 articles across `documentation/digital-publishing/content-management` and `documentation/digital-publishing/personalization` | 92 | 12 | 100, pass |

## Findings

- The high-confidence concepts are not sparse shell categories. Each one pulls a meaningful official API branch cluster plus supporting model-map, release-note, source-code, recipe, training, or community records.
- `documents-signatures`, `hosting-infrastructure`, and `prayer-care` now capture the exact official branch clusters that were previously too easy to bury under broader admin concepts.
- `engagement-tracking` is intentionally broad because the API shows Steps, Streaks, Assessments, Achievements, and adjacent engagement tooling as a connected operational cluster.
- `obsidian-development` has enough developer-documentation density to justify its own concept rather than remaining only a developer-resources subsection.
- `content-personalization` remains worth keeping as a first-class concept because the API data separates content management and personalization into a large digital-publishing workflow area.

## Follow-Up Watch Items

- Watch query logs for whether `content-personalization` should later split into narrower content-management and personalization concepts.
- Keep `search`, `caching`, `event-calendar`, `developer-codex`, and `mobile-app-publishing` as subguides until query evidence shows repeated direct demand.
- Continue treating API branch/path metadata as routing evidence, not as the only routing rule. Model-map, release, source-code, and reviewed community evidence still matter for final guide shape.
