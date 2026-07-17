# Hybrid Retrieval Shadow Decision

Date: 2026-07-17

## Decision

Keep the hosted D1 lexical retriever as the production path. Do not promote the
Cloudflare AI Search hybrid shadow. The isolated shadow instance was deleted
after evaluation.

## Evidence

The shadow indexed the exact current 290-document stratified projection. Of 151
evaluation questions, 144 were eligible for the bounded shadow and seven were
skipped because their expected result was intentionally excluded by index
policy.

| Metric | Hybrid shadow | Production lexical baseline |
| --- | ---: | ---: |
| Passed questions | 100 / 144 | 151 / 151 |
| Mean reciprocal rank | 0.777389 | 0.993377 |
| Recall at target rank | 0.777778 | 1.0 |
| Duplicate rate | 0 | 0 |
| Authority correctness | 1.0 | 1.0 |
| Mean latency | 1,424.74 ms | not used as a promotion advantage |
| P95 latency | 2,173.63 ms | not used as a promotion advantage |
| Maximum latency | 50,324.23 ms | not used as a promotion advantage |

The smaller curated retrieval cohort performed better than the full shadow but
still trailed lexical retrieval: 18 of 20 passed, MRR was 0.844643, and recall
at target rank was 0.9. The generated cohort passed 82 of 124 eligible cases.
Estimated embedding cost was about $0.007542, but cost did not offset the
substantial relevance and latency regressions.

## Operational Outcome

- Production routing remains lexical-only.
- Exact model-map and stable-ID lookup remain lexical by design.
- The reusable shadow tooling remains available for a materially different,
  explicitly registered experiment.
- Any future vector experiment must beat the current lexical quality gate
  without regressing exact technical retrieval, authority, duplicates, latency,
  or privacy.
- The shadow runner reconciles exact current item keys, removes obsolete items,
  retries failed or stale items, and evaluates only after the desired set is
  fully indexed.
