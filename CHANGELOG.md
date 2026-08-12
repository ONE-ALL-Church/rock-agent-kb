# Changelog

All notable public Rock KB service, client, source, concept, recipe, model-map,
and retrieval changes are recorded here. Releases use `rock-kb-vMAJOR.MINOR.PATCH`
tags and follow semantic versioning for public client and service contracts.

## [Unreleased]

### Changed

- The reviewed source-native bundle now covers 87 official prose records and
  498 typed artifacts. Apple TV articles 120, 128, 139, 146, and 173; Roku
  articles 186, 315, and 318; and Helix articles 348 and 358 now use the
  source-native path with 29 explicit legacy replacements and one reviewed
  partial retention.
- The Rock developer-documentation source was refreshed from its public API;
  generated source summaries, concept indexes, and dependency metadata now
  reflect the current 361-record normalized projection.

### Fixed

- Exact source-record candidate generation now requires explicit concept
  routing instead of silently inheriting the balanced-pilot defaults.
- Source-native model-output merging preserves required nullable contract
  fields, and migration promotion preserves hash-matching verification
  resolutions while appending a reviewed batch.
- Exact independent questions now retain precedence over nearby paraphrases,
  while high-overlap source-native recipes can outrank generic task cards for
  matching how-to questions without receiving an unconditional recipe boost.

## [0.23.1] - 2026-08-11

### Changed

- The reviewed source-native bundle now covers 77 official prose records and
  466 typed artifacts, with 122 exact legacy migrations and seven
  source-native artifact migrations. The batch completes the 19-record ready
  queue plus bounded hosting, security, engagement, and CMS groups.
- The old `/lava/commands` source identity now resolves to
  `/lava/commands/getting-started`, and the Navigate Rock and community
  deprecations records use exact source-record concept routing.
- Current source verification narrows mutable SQL Server, unsubscribe,
  Check-In, cache, File Manager, and content-channel guidance; all 71 active
  verification decisions resolve with no blocker.

### Fixed

- Exact source-native questions retain their ranking signal after a verified
  artifact correction, and field/property questions naming a distinctive code
  object prefer its reviewed structured reference over generic Lava contexts.
- Exact source-record migration selection is fail-closed, bypasses automatic
  per-concept limits, and no longer admits keyword-neighbor records or reserves
  the wrong subguide.
- Redistilling an unchanged artifact now preserves every prior verified
  correction, narrowing, or supersession. Changed source inputs and partial
  artifact replacements stop for explicit re-review instead of restoring the
  source's known-wrong wording; newer fully overlapping verified corrections
  explicitly supersede older decisions.
- Alternate-repository migration-priority reports consistently read and write
  within the requested root instead of mixing inputs from the default checkout.
- Public-safety scanning accepts literal ellipsis credential placeholders while
  still rejecting real password, token, key, and connection-string values on
  the same line.
- CI release gates use bounded local-Worker concurrency so retrieval quality
  remains strict without turning the isolated D1 check into an unstable load
  test on shared runners.
- Conversational search now preserves the technical `sa` identifier in SQL
  administration contexts and normalizes delete/deleted/deleting/deletion, so
  corrected source-native
  answers outrank neighboring setup task cards for those paraphrases.

## [0.23.0] - 2026-08-10

### Added

- Open Knowledge Format v0.2 full and core distributions with standard
  `generated` and `sources` provenance, file-relative graph links, and a
  versioned Rock extension profile.
- Exact client inspection of the OKF/profile/spec tuple and release gates that
  validate both profiles with the reviewed upstream v0.2 reference parser.
- A source-backed Check-In room-availability task card with an explicit
  decision order, bounded read-only checks, model-map links, and first-exclusion
  reporting guidance.
- Deployed-projection freshness checks for the Rock issue and Rock Ideas
  catalogs, including result-count and semantic content-hash comparisons,
  separate operational/projection timestamps, guarded hash contracts, and
  fail-closed handling when mismatch direction cannot be established.

### Changed

- Strict Rock verification accepts new v0.2 distributions and preserves
  verification of published v0.1 bundles only under their exact legacy
  manifest/profile/spec tuple.
- The release workflow verifies the prior full/core release before producing
  synchronized v0.2 archives and checks that the upstream specification pin is
  still current.
- The source-native bundle now covers 68 official prose records and 415 typed
  artifacts. Group Attendance Digest, Group Type Requirements, Core Field Type
  Patterns, Media Player, Communication Lists, and seven former parser-1.0
  sources now use the reviewed canonical path with explicit legacy retirement
  and identity decisions.
- Rock issue intelligence now contains 5,838 public issue records and 28
  reviewed enrichments; Rock Ideas now contains 1,089 records with refreshed
  concept, issue, release, and model-map relationships.
- Exact recipe and Rock Idea lookup accepts canonical URLs and common ID or
  slug forms without weakening identity validation.
- The operations dashboard limits the active usage funnel and review queue to
  the current service and retrieval-projection versions while retaining older
  signals only as a bounded historical count.
- The agent skill is version `1.12.1` and requires client `0.23.0`.

### Fixed

- Exact canonical results with verified corrections or narrowings now expose a
  compact effective artifact and a hash-addressed audit reference instead of
  embedding superseded pre-verification wording in the agent-facing payload.
- Source freshness now separates successful upstream checks, deployment lag,
  and a newer reviewed projection using per-source versioned hash contracts, so
  a stale hosted catalog is blocked without misclassifying a newer deployment.

## [0.22.0] - 2026-08-03

### Added

- Reviewed source-native coverage for the final 12 architecture-pilot
  documentation records, including artifact-specific verification corrections
  when one source check applies to several distinct knowledge artifacts.

### Changed

- Canonical retrieval is now the reviewed hosted default for REST, MCP, and the
  current CLI. The complete legacy projection remains available as an explicit,
  immediate rollback without a code deployment.
- All 38 source-native records now use `gpt-5.6-sol`, prompt version `2.3.1`,
  and input-hash version `2`; the canonical bundle contains 263 reviewed typed
  artifacts and 289 source-native evaluation cases.
- Search ignores the modal word `can` when measuring query overlap, preventing
  broad capability statements from displacing exact troubleshooting guidance.
- The agent skill is version `1.11.0` and requires client `0.22.0`.

### Fixed

- Canonical evaluation resolves retained legacy result IDs through public
  aliases, allowing strict hosted gates and automatic rollback to evaluate the
  active projection correctly.
- Source-native append promotion now removes stale verification resolutions,
  and multi-artifact verification rows retain distinct titles, text, and
  dispositions instead of flattening every artifact to one summary.

## [0.21.1] - 2026-08-01

### Fixed

- The community test round now validates the current Rock issue-assessment
  contract instead of requiring removed issue `#6920`.
- Search returns no public results for direct requests for private-instance
  secrets, local identifiers, person-level attendance, or private custom data.
- Exact queries phrased as `model slug for <model>` route to the requested
  Model Map record, while broad issue searches honor explicit open, closed, and
  critical constraints.
- Source-native verification corrections now carry their reviewed Rock-version
  scope into canonical retrieval, preventing a Rock 19.4 correction from being
  presented as a Rock 20 answer.
- Recipe package versions are no longer exposed as Rock RMS compatibility
  versions in search results.

## [0.21.0] - 2026-07-31

### Added

- Privacy-safe blind legacy-versus-canonical retrieval comparisons over REST,
  CLI, and direct MCP. Pending sessions expire after 30 minutes, never retain
  the question, and expose only randomized A/B results; reviewed outcomes use a
  fixed preference and reason vocabulary.
- `rock-kb --version`, comparison dashboard aggregates, and an explicit split
  between raw MCP transport failures, expected stateless `405` rejections, and
  actionable failures.

### Changed

- Anonymous field-validation consent is version `3`; version `2` state does not
  authorize paired comparison retention and is intentionally ignored by the
  updated client.
- Direct MCP exposes 35 tools. Code Mode remains limited to the same 27
  read-only operations and omits both comparison writes.
- The agent skill is version `1.10.0` and requires client `0.21.0`.

## [0.20.0] - 2026-07-30

### Added

- A reviewed source-native canonical bundle with deterministic sentence,
  list-item, table, code, and catalog units; typed knowledge artifacts; durable
  provenance; explicit version-scope caveats; and dependent-impact tracking.
- A generic reviewed cross-source synthesis pipeline that preserves issue
  reports, official release records, and immutable source-code evidence as
  distinct evidence roles with exact and paraphrased retrieval evaluations.
- An explicit `canonical-canary` reader for anonymously opted-in
  `external-test` and `maintainer` cohorts across CLI search/result/outcome and
  direct MCP `kb_search`, `kb_get_result`, and `kb_outcome`.

### Changed

- Service builds now load canonical search rows into parallel D1 row, concept,
  alias, and FTS tables while keeping `legacy` as the immutable default
  retrieval projection.
- Canary telemetry uses a separate privacy-bounded daily aggregate with no
  installation hash, query, topic, organization, person, IP address, logs, or
  Rock data. Outcome rows retain an explicit retrieval projection through an
  automatic additive D1 migration.
- Distilled-claim review IDs now bind to the exact source-input snapshot.
  Changed clusters return to review under a content-versioned ID, and retired
  shadow migration chains move to a private audit archive instead of breaking
  the current canonical bundle.
- Agent installation now upgrades older Codex MCP configurations that store
  private headers in a nested TOML table without creating a duplicate table.
- The agent skill is version `1.9.0` and requires client `0.20.0`. It documents
  tester opt-in, exact projection continuity, cross-source trust semantics, and
  the evidence gate that blocks a default cutover without real external
  usefulness outcomes.

## [0.19.0] - 2026-07-29

### Added

- Stateless MCP `2026-07-28` discovery, per-request capability negotiation,
  strict modern header validation, and one-hour public discovery/tool-list
  cache hints on the hosted direct endpoint.
- Official MCP SDK v2 client coverage alongside explicit 2025 stateless
  compatibility, browser-Origin, unsupported-version, and Code Mode regression
  tests.
- Privacy-bounded daily MCP transport aggregates for protocol generation,
  operation category, endpoint, fixed cohort, status/error, latency,
  response-size, projection, and count, exposed through the operations
  dashboard and `GET /telemetry/mcp-transport`.
- Intent-aware retrieval for tasks and troubleshooting, explicit Rock-version
  filtering, paginated claim tiers, debug-only ranking signals, compact
  manifests, and nonempty concept summaries.
- A versioned concept-taxonomy audit, focused guide-synthesis prompts, and a
  reviewed Workflows pilot generated with `gpt-5.6-sol` at `xhigh` reasoning.

### Changed

- The direct `/mcp` endpoint now uses the official MCP SDK v2 and Cloudflare
  stateless handler instead of a hand-written 2025 protocol parser. Ordinary
  2025 clients remain supported on the same URL without persistent sessions.
- `/mcp/code` now uses Cloudflare's explicit legacy handler and remains an
  independent, read-only MCP SDK v1 composition endpoint.
- The MCP transport table is emitted by the deployment projection. Runtime
  writes use one aggregate upsert and create the table only as a missing-schema
  fallback during a deployment transition.
- Routing-only source commentary is no longer published as approved claims.
  It remains discoverable through source summaries, while the public claim
  graph contains 609 concrete, tiered claims with explicit version-scope
  status.
- Concept quality now measures answer-bearing evidence separately from artifact
  completeness, and legacy guide regeneration is tracked as review debt rather
  than a false missing-artifact failure.
- The Rock KB agent skill is version `1.8.0` and requires client `0.19.0`.

## [0.18.0] - 2026-07-26

### Added

- Canonical Lava context rows with source-backed observations for Rock
  `19.0.11`, stable `19.2.0`, and develop `20.0.5`.
- Exact `--rock-version` selection and typed Lava context diffs in the CLI,
  REST service, hosted MCP, and local MCP server.
- Consent-attested, privacy-safe Lava context verification outcomes restricted
  to context ID, root key, numeric Rock version, and a fixed availability value.

### Changed

- The agent skill is version `1.5.0` and requires client `0.18.0`.
- GitHub Actions use current Node 24 action runtimes.
- The completed architecture-refactor checklist is retained as retired
  historical context instead of an active execution plan.

## [0.17.0] - 2026-07-26

### Added

- Exact grouped Lava context retrieval through `lava-context list|get`,
  `kb_list_lava_contexts`, `kb_get_lava_context`, and matching REST routes.
- Source-backed Check-In Attendance, Family, Checkout, and Person Location
  label contexts, including conditions, nullability, execution phases,
  completeness, source versions, immutable commits, and Model Map links.
- A private source-discovery review queue plus reviewed public extension and
  non-exportable private-overlay validation paths.

### Changed

- Lava context row IDs no longer depend on source line numbers. Prior IDs remain
  cumulative aliases for saved links and feedback.
- The Rock KB agent skill is version `1.4.0`, requires client `0.17.0`, and
  directs agents to exact grouped context retrieval before generic search or
  Model Map inspection.

## [0.16.1] - 2026-07-25

### Fixed

- Telemetry status now inspects managed user-level agent configurations and
  reports an MCP update only when their private headers are actually stale.
- The Rock 18.2.4 issue-watch regression now evaluates deterministic reviewed
  issue snapshots instead of assuming a live GitHub issue remains open.
- Lava context generation now follows the public Obsidian
  `FundraisingOpportunityView` source after its legacy WebForms file was
  removed upstream.

## [0.16.0] - 2026-07-21

### Added

- Opt-in anonymous field validation with a private random installation marker,
  fixed `community`, `external-test`, or `maintainer` cohorts, and one-way
  server-side hashing. No organization, person, query, IP address, free text,
  or Rock data is stored with the marker.
- Consent-attested `useful`, `partially_useful`, and `not_useful` outcomes with
  bounded compatible reason codes for canonical public result IDs.
- A default field-validation dashboard funnel and bounded review queue for
  searches, exact retrieval, outcomes, feedback, issue reports, negative
  outcomes, repeated zero-result topics, and failed exact lookups. Evaluation
  and maintainer traffic are excluded by default.
- A source-supported review of Rock issue `#6928`, including a public-source
  diagnosis of the workflow-backed signature-document parent-security path and
  an aggregate read-only verification playbook.

### Fixed

- Rock issue catalog freshness now compares per-source content hashes as well
  as row counts, so a state, label, routing, or remediation change cannot be
  hidden by an unchanged catalog size.
- Service evaluation retries exactly once after a transport timeout and does
  not retry HTTP, response, or ranking failures. Availability is reported
  separately from retrieval quality while both remain release-blocking.

### Changed

- The Rock KB agent skill is version `1.3.0`, requires client `0.16.0`, and
  adds versioned consent, opt-in identity, outcome, and revocation guidance.

## [0.15.0] - 2026-07-21

### Added

- Issue Watch V2 assessment scopes for current open issues, relevant closed
  history, or their union.
- Reviewed platform, capability, and configuration prerequisites; bounded
  exclusion explanations; evidence-backed risk provenance; and Rock issue
  catalog freshness in assessment results.

### Changed

- Issue watch baselines are scope-specific and now report routing, risk,
  freshness, population, and exclusion changes in addition to applicability,
  remediation, and revalidation changes.
- The agent skill now directs agents to inspect freshness, evidence, risk
  provenance, and read-only verification before claiming an issue affects an
  instance.

## [0.14.0] - 2026-07-18

### Added

- Authoritative hosted source freshness reporting with independent workflow
  schedule, last-check, content-change, result-count, content-hash, and source
  status fields through REST, MCP, the operations dashboard, and the CLI.
- Privacy-bounded external test-round funnel counts for rounds started,
  completed, reviewed, and feedback submitted.
- An opt-in experimental Cloudflare Code Mode MCP endpoint for composed
  read-only retrieval.

### Changed

- Direct MCP tools now advertise read/write and idempotency annotations,
  return structured content alongside compatible JSON text, and negotiate the
  current stable MCP protocol version.
- The direct 28-tool MCP remains the default. Code Mode wraps only its 24
  read-only tools; submission and feedback operations remain direct and
  separately consented.

## [0.13.0] - 2026-07-17

### Added

- Source-aware Rock KB agent skill lifecycle commands for read-only update
  checks, backup-protected updates, local status, and persisted notify, auto, or
  pinned policies.
- A hosted REST and MCP skill manifest with a stable skill version, source
  SHA-256, minimum client version, restart behavior, and update cadence.
- Standard `skills/rock-kb-agent/` distribution for cross-agent discovery while
  retaining the legacy hosted artifact path for older clients.

### Changed

- Installed skills now carry source provenance in standard Agent Skills
  metadata, and ordinary CLI use performs a throttled daily check without
  interrupting the requested operation.
- Project-scoped skills reject automatic updates so changes can be reviewed in
  Git before they are committed.

## [0.12.1] - 2026-07-17

### Fixed

- Structured test-round and issue-report validation now accepts canonical Rock
  issue result IDs containing `#`, matching the IDs in the public projection.
- `rock-kb test-round --submit` now exits nonzero when the hosted service
  rejects the review instead of reporting process success for a failed submit.

## [0.12.0] - 2026-07-17

### Added

- First-class Rock Community Ideas retrieval through the hosted REST, MCP, and
  CLI surfaces, with concept, model-map, issue, release-note, and source links.
- A generated Ideas verification queue for lifecycle claims such as Complete,
  Planned, Started, and Under Review. Queue rows expose stable review hashes,
  priorities, and recommended actions without publishing private candidates.
- A tenth external test-round case that checks exact Idea retrieval, trust-tier
  labeling, concept/model/issue routing, and relationship semantics.

### Changed

- The maintainer operations dashboard now exposes Rock Ideas catalog and
  verification-queue summaries alongside issue and freshness reporting.
- Exact lifecycle-Idea results include their current verification context so
  agents can distinguish corroborated state from claims still needing evidence.

### Decision

- Idea lifecycle labels, relationship candidates, and verification priority
  remain `routing_context_only`. They help agents investigate feature gaps but
  do not prove implementation, release availability, or instance applicability.

## [0.11.0] - 2026-07-17

### Added

- Opt-in `external-test` and `maintainer` telemetry cohorts for the published
  CLI and MCP configuration. Cohorts remain self-declared aggregate labels and
  do not collect organization, installation, user, or query identity.
- Exact Cloudflare AI Search shadow-index reconciliation, including bounded
  cleanup of obsolete, failed, and stale in-progress items before evaluation.

### Changed

- Hosted telemetry now reports cohort-separated usage, result-kind, zero-result,
  and structured-feedback counts while retaining historical rows as
  `unattributed`.
- Rock issue `#6925` was revalidated after upstream activity without changing
  its source-confirmed diagnosis, fix, or public verification playbook.
- The Python package's exported version now stays aligned with the release
  metadata used by the CLI and PyPI package.

### Decision

- The bounded Cloudflare hybrid shadow did not outperform lexical retrieval,
  so vectors remain out of production and the temporary shadow instance was
  deleted. Lexical retrieval remains the authoritative production path.

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
