# Changelog

All notable public Rock KB service, client, source, concept, recipe, model-map,
and retrieval changes are recorded here. Releases use `rock-kb-vMAJOR.MINOR.PATCH`
tags and follow semantic versioning for public client and service contracts.

## [Unreleased]

## [0.6.0] - 2026-07-13

### Added

- Complete, read-only OKF v0.1 distribution covering canonical concept guides,
  agent answers, approved claims, public contribution provenance, reviewed
  recipes, Lava contexts, stable model digests, source summaries, task cards,
  and public evidence-source policies.
- Versioned ZIP and tarball release assets with a manifest, source commit,
  per-file integrity records, typed relationships, and SHA-256 checksums.
- `rock-kb okf download`, `rock-kb okf inspect`, and `rock-kb okf validate`
  commands for read-only distribution use through `uvx` or a permanent install.

### Changed

- OKF validation now enforces v0.1 reserved-file behavior, date-only log
  headings, internal-link integrity, canonical contribution deduplication,
  archive path safety, and public/private boundary checks.

### Decision

- OKF remains a generated portability layer rather than the canonical store.
  Arbitrary OKF import is deferred until it can use the existing reviewed
  contribution, licensing, redaction, authority, and deduplication gates.

## [0.5.1] - 2026-07-10

### Changed

- Prefer concise claims containing exact multi-word query phrases, including the
  observed short direct-database-access paraphrase.
- Collapse Lava context search hits that share a context and root key while
  preserving their exact nested-path result IDs.
- Count successful claim, concept, model-map, recipe, and exact-result access by
  aggregate event, client class, result kind, and count without retaining IDs or
  query text.
- Include failed evaluation rows in lexical quality-gate reports for actionable
  CI diagnosis.

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
