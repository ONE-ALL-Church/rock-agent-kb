# Changelog

All notable public Rock KB service, client, source, concept, recipe, model-map,
and retrieval changes are recorded here. Releases use `rock-kb-vMAJOR.MINOR.PATCH`
tags and follow semantic versioning for public client and service contracts.

## [Unreleased]

## [0.5.0] - 2026-07-10

### Added

- Canonical contextual retrieval projection with authority, version, review,
  source-hash, concept, and index-policy metadata.
- Retrieval quality metrics for MRR, recall, duplicate rate, and authority.
- Isolated Cloudflare hybrid-search shadow evaluation with latency and cost.
- Typed OKF relationship edges and source-change revalidation reports.
- Actionable structured feedback tied to public canonical result IDs and
  projection versions without retaining query text.
- Local production-size lexical quality gate for pull requests and deployments.
- Source freshness policy and operational status reporting.

### Changed

- Corrected FTS5 BM25 handling and intent-gated recipe/concept boosts.
- Claims, recipes, Lava contexts, and contributions now use one canonical search
  row with concept facets and legacy result-ID aliases.
- The Python client version is `0.5.0` for the canonical result and feedback-v2
  service contract.

### Decision

- Production search remains lexical. The measured hybrid shadow pilot did not
  beat lexical MRR or latency and was not promoted.
