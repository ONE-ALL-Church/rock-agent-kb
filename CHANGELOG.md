# Changelog

All notable public Rock KB service, client, source, concept, recipe, model-map,
and retrieval changes are recorded here. Releases use `rock-kb-vMAJOR.MINOR.PATCH`
tags and follow semantic versioning for public client and service contracts.

## [Unreleased]

## [0.10.0] - 2026-07-16

### Added

- `rock-kb test-round`, a nine-case structured external-church test pack for
  exact model retrieval, Lava contexts, recipes, troubleshooting, no-answer
  behavior, and three imported Rock issue trust/applicability paths.
- Fail-safe two-slot R2 artifact deployment with health-visible active-prefix
  metadata and idempotent legacy-prefix retention enforcement.

### Changed

- Fifteen high-value ONE&ALL submissions are now reviewed community results,
  including API/Obsidian readback, check-in relationship, document-signature,
  communication-list, connection-history, and payment-safety guidance.
- Thirty-one sections across the four largest guide queues now carry direct
  official or public-source citations, reducing the review backlog from 94 to
  63 sections.

### Decision

- Imported GitHub issues remain a separate routing surface. Upstream reports
  stay `community-unreviewed`; only separately reviewed, cited enrichments can
  provide stronger conclusions, and instance applicability remains a bounded
  read-only assessment.

## [0.9.1] - 2026-07-15

### Added

- `rock-kb issues watch` for complete, paginated instance assessments with
  private local snapshots, stable profile hashes, restrictive file
  permissions, and categorized changes between observations.
- Reviewed public issue enrichments for Connections, CMS, LMS, Obsidian,
  workflows, mobile, and hosting behavior, with exact public-source or
  maintainer evidence and explicit abstention where evidence was insufficient.

### Changed

- Rock issue assessments now rank the complete bounded candidate set before
  applying `offset` and `limit`; REST, MCP, local serving, and the published
  client expose matching pagination metadata and projection versions.
- Stable Model Map data now reflects Rock `19.2.0`, with `20.0.5` retained as
  the latest comparison track and dependent model, concept, search, and agent
  projections rebuilt.
- Fourteen high-value Check-In, Connections, and Lava guide sections now link
  directly to official documentation, training, Model Map, or public source
  evidence.
- Public export traversal excludes operating-system metadata at every nested
  path rather than only at the export root.

### Decision

- Issue watch state remains local and private. It stores only the profile hash,
  public normalized issue fields, projection metadata, and observation time;
  it never stores raw GitHub content, private Rock data, secrets, or queries.

## [0.9.0] - 2026-07-15

### Added

- Canonical Rock core and mobile issue intelligence with immutable GitHub
  identity, version evidence, concept/model-map routing, release-note links,
  transfer aliases, explicit timeline coverage, and reviewed enrichments.
- Dedicated `rock-kb issue` and `rock-kb issues` commands plus matching REST
  and MCP surfaces for exact lookup, search, listing, conservative instance
  assessment, and bounded investigation planning.
- Private orchestrator-worker review packets, public-safe enrichment schemas,
  scheduled metadata refresh, D1 projections, and full-profile OKF issue
  records.
- First reviewed public enrichments for a source-confirmed check-in CSS failure,
  Azure Blob cache concurrency risk, one-click unsubscribe behavior, and a
  next-generation check-in security duplicate.

### Changed

- General search keeps issue reports out of unrelated answers while dedicated
  issue retrieval prefers exact references, distinctive titles, versions, and
  official release evidence.
- Product issue reports remain `community-unreviewed` routing evidence;
  reporter versions, fix labels, release notes, closure state, and reviewed
  applicability conclusions remain separate evidence.
- Maintainers can request exact issue timelines, see enrichment coverage and
  upstream-change revalidation counts, and safely validate the expanded full
  OKF distribution under a 50,000-entry archive ceiling.

### Decision

- Raw issue bodies, comments, users, screenshots, attachments, and private
  instance evidence are not republished. Agents produce drafts only; GitHub
  comments and public enrichments continue to require explicit human review.

## [0.8.0] - 2026-07-14

### Added

- Structured `kb_report_issue`, `POST /issues/report`, and `rock-kb
  report-issue` surfaces for service, MCP, CLI, schema, authentication, and
  retrieval failures, with stable report IDs and dashboard triage.
- Deterministic issue deduplication, occurrence counts, projection/client
  context, public-safety validation, redaction attestation, bounded payloads,
  and Cloudflare plus D1 rate limits.

### Decision

- `kb_feedback` remains fixed result-quality feedback. Issue reports remain
  pending review and cannot create GitHub issues automatically.

## [0.7.0] - 2026-07-14

### Added

- Synchronized lossless `full` and compact `core` OKF profiles with stable
  canonical IDs, sharded indexes, and lossless JSON structured records.
- Explicit MIT and CC BY 4.0 licensing, third-party notices, a versioned Rock
  OKF extension profile, release deltas, and reproducible archive metadata.
- Generic `okf conformance` and strict `okf verify` client commands, plus exact
  profile downloads backed by SHA-256 release evidence.
- Official Google reference-parser interoperability checks, weekly upstream
  specification monitoring, and GitHub release artifact attestations.

### Changed

- Archive readers now reject duplicate or unsafe paths, symlinks, encrypted
  ZIP entries, oversized files/bundles, and suspicious compression ratios.
- Strict verification requires complete checksum coverage, licensing,
  structured-record links, profile metadata, and public-safety checks across
  all readable bundle files. `okf validate` remains a compatibility alias.

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
