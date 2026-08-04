# Pipeline Overview

This runbook collects the operational detail that used to live in the README. Use it alongside [CLI Reference](cli-reference.md) when deciding what to rebuild, review, or audit.

## Reproducible Rebuilds

Generated content should be reproducible from `sources/registry.yaml`, raw manifests, normalized records, reviewed claims, and the CLI. For intentional rebuilds, set `ROCK_KB_GENERATED_AT=<iso timestamp>` so generated `generated_at` metadata does not churn across repeated runs; standard `SOURCE_DATE_EPOCH` is also supported.

The normal control loop is:

```bash
uv run kb status
uv run kb build --dry-run
uv run kb build --stage <stage>
python3 scripts/audit_tracked_tree.py
uv run kb audit all
uv run --extra dev pytest
```

`kb status` reports stale pipeline stages, manual gates, review queues, concept staleness, guide refresh needs, and suggested next commands. `kb build` runs deterministic stages only; source refresh, transcription, review, promotion, authored synthesis, and public push remain explicit human or local-agent decisions.

## Detailed Repository Layout

- `sources/registry.yaml` - source catalog, license posture, crawl strategy, refresh cadence, and preferred tooling.
- `data/raw-manifests/` - fetch records and discovered URLs.
- `data/normalized/` - machine-readable normalized source records.
- `data/media/` - private media manifests, downloads, transcripts, sidecars, and media indexes for local synthesis.
- `claims/` - public-safe approved claim graph exports generated from reviewed source-backed promotions.
- `knowledge/` - curated Markdown organized by Rock topic.
- `knowledge/sources/` - generated human-readable source pages from normalized records.
- `knowledge/topics/` - generated curated topic pages for API, Lava, mobile, releases, SQL, workflows, and plugins.
- `knowledge/concepts/` - generated concept guides with source dependency maps.
- `knowledge/model-map/` - generated Rock model-map mirror from stable/latest generic demo Obsidian block-action fetches, model/property/method rows, version diff, and category slices.
- `concepts/registry.yaml` - concept definitions, keywords, subguides, and source weighting.
- `agent/` - generated `llms.txt`, topic indexes, release indexes, and citation maps.
- `agent/rock-issues.jsonl`, `agent/rock-issue-enrichments.jsonl`, and `agent/rock-issue-summary.json` - count-reconciled, public-safe Rock core/mobile issue routing data, reviewed public enrichments, and coverage metrics.
- `issues/` - reviewed public issue enrichments; private investigation packets remain under ignored `data/review/rock-issues/`.
- `tools/` and `src/rock_kb/` - CLI and implementation.
- `docs/` - maintainer runbooks and contribution policy.
- `docs/runbooks/local-transcription.md` - local and hosted transcription model decision.
- `docs/decisions/topic-split-rules.md` - routing rules for deciding whether a domain belongs in a new concept or an existing guide.
- `docs/decisions/current-tooling-research.md` - current crawler, document conversion, and transcription research decisions.
- `docs/runbooks/model-map-rebuild-runbook.md` - stable/latest generic Rock Model Map API fetch, rebuild, validation, and review workflow.
- `docs/runbooks/canonical-knowledge-shadow.md` - non-production shared source/evidence/knowledge projection and promotion gate.
- `docs/runbooks/contributor-reviewer-workflow.md` - community contribution, media review, claim promotion, and rebuild workflow.
- `docs/decisions/private-and-org-data-integration-plan.md` - implementation plan for owner-private docs and outside-org contribution bundles.
- `docs/decisions/org-data-implementation-roadmap.md` - implementation roadmap for private org data, outside-org bundles, review gates, and rebuild tracking.

## Source And Extraction Rules

The default source posture is conservative: public web content is cited and summarized unless a source explicitly allows full-text mirroring. Private repositories are scanned only into a review queue until content is allowlisted.

Cloudflare Browser Run is supported only as an optional extractor. Set `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`, then use `kb extract markdown --tool cloudflare` for hard pages. Local extraction remains the default rebuild path so the corpus does not depend on hosted scraping.

Public source summaries are generated into `agent/source-summaries.jsonl` from records that are already eligible for the public agent pack. They are citation-first routing notes for agents: title, source URL, topics, source hash, summary, key insights, and an agent-use hint. They are not a replacement for authoritative concept guides; they help agents decide which source or guide to inspect next. Coverage and redaction-skip counts are written to `agent/source-summary-report.json` and exposed from `agent/rock-kb-manifest.json`.

Rock GitHub issues use the separate `kb issues sync` path because identity,
timeline history, transfer aliases, version evidence, and untrusted-content
rules do not fit the generic scraper. The issue metadata catalog is complete on
every pass; timeline history is incrementally backfilled. Issue rows remain
`routing_context_only`, while exact official release-note references are joined
from the generated release index. See [Rock Issue Intelligence](rock-issue-intelligence.md).

## Mobile Selector X-Ray

Rock Mobile selector x-ray resources are concept-owned public artifacts under `knowledge/concepts/mobile/resources/`. Rebuild them with `uv run kb build --stage mobile-selector-audit`; this regenerates the block selector audit from `knowledge/concepts/mobile/mobile-block-selector-xray.jsonl` and writes `knowledge/concepts/mobile/mobile-block-selector-xray-dependencies.json` so `uv run kb audit readiness` can warn when official block-page source hashes change.

## Media Sidecars And Review

Media sidecars follow the same public/private rule. `kb media sidecars` writes private Markdown sidecars under `data/media/sidecars/` and JSONL indexes under `data/media/index/`. Sidecars may include raw transcripts and timestamped segments for local synthesis; public guides should cite source URLs and use reviewed distilled insights, not copy sidecar transcript text.

Use `kb media candidates --source <id>` or `kb media candidates --all-sources` to create review prompts with timestamped slots and no raw transcript text. Generated candidates are not publishable by themselves. Promote only rewritten public-safe claims with:

```bash
uv run kb media promote \
  --source <id> \
  --candidate-id <candidate-id> \
  --rewrite-file data/review/media-rewrites/<source>.jsonl \
  --review-status approved_for_public_distillation \
  --concept-id <concept-id>
```

Reviewer-authored media claims may include `timestamp`, `timestamp_seconds`, and `source_timestamp_url` for citation routing, but public rewrites should use the canonical source page URL and must not include direct media file, HLS, or tokenized player URLs. Use `kb media review-status` to see candidate, approved, pending, and affected-concept coverage across transcribed sources.

Use `kb media queue` before bulk transcription. It writes a private prioritized queue to `data/media/index/transcription-priority-queue.jsonl` and a summary report to `data/media/index/transcription-priority-report.json`. `kb media batch` and `kb media transcribe` also select pending rows by priority within the requested source, so transcription coverage starts with higher-authority, higher-signal, shorter media instead of raw discovery order.

## Gemma Enrichment

For audio/video files, treat Gemma 4 12B as a private enrichment pass after baseline transcription, normalization, sidecars, and review-candidate generation. Use `kb media understand-benchmark --tool gemma4-12b` to create a private benchmark plan, `kb media understand-prepare --tool gemma4-12b` to prepare private clips and video frames, then `kb media understand-run --model gemma4:12b` to run local Gemma enrichment.

This is an enrichment evaluation path only: `mlx_whisper` remains the baseline transcript generator unless Gemma shows comparable transcript accuracy and better video understanding across broader samples. The benchmark artifact is written under `data/review/media-understanding-benchmarks/`; direct media URLs are omitted unless `--include-media-url` is explicitly passed. A local 2026-06-03 Ollama `gemma4:12b` run completed against five samples; the corrected runner prefers compressed MP3 audio payloads generated from prepared clips, adds video frames when available, and uses transcript excerpts only as comparison grounding.

## Claims And Guide Refresh

Approved claims are the durable public unit of knowledge. `kb build --stage claims` converts reviewed public-safe media promotions into `claims/approved-claims.jsonl` with stable claim IDs, claim text, concept IDs, source refs, source record IDs, authority tier, claim tier, confidence, review status, license/publication status, Rock version applicability, optional timestamps, safe evidence hashes, private corpus pointers, and live-verification flags.

Claim tiers are defined in [Claim Tier Policy](../decisions/claim-tier-policy.md): `routing_context_only` claims route agents to sources, `source_backed` claims are guide-safe but not operational proof, `answer_pack_approved` claims may feed generated answers, and `live_verified` claims include concrete read-only evidence. `kb claims live-plan` batches `source_backed` live-verification rows into read-only probe groups; promote rows through `data/review/live-claim-verifications.jsonl` only when evidence directly verifies the claim. `kb claims validate` enforces traceability and blocks direct media URLs, transcript fields, secrets, and other private-only data from the public claim graph.

The canonical knowledge architecture remains non-default. Its current decision,
evidence, blockers, and next sequence are recorded in
[Canonical Knowledge Architecture Status](../decisions/canonical-knowledge-architecture-status-2026-08-03.md).
Maintainers
can run `uv run kb tools canonical-shadow` to test shared source snapshots,
source units, generation activities, evidence links, typed relationships,
persistent identity records, and explicit identity migrations without changing
claims or retrieval. The reviewed source-native documentation bundle under
`canonical/source-native/v1/` is compiled from deterministic Rockumentation
sentence/table/code/list-item units and reviewer-approved adaptive v2.3 typed
artifacts. The public `canonical/source-family-contracts-v1.json` distinguishes
that model-assisted path from deterministic typed ingestion for issues, Ideas,
Model Map, Lava contexts, recipes, and contributions, while exposing remaining
legacy projections as migration debt.
Nested catalogs retain parent links, and source snapshots preserve API-derived
documentation path/branch routing plus independent check/change timestamps;
full source text stays ignored. Run
`uv run kb tools canonical-retrieval-shadow` to compare the current and
canonical projections through the production Worker's local FTS and ranking
implementation plus exact REST and stateless MCP compatibility. The tracked
`canonical/identity/v1/` baseline preserves durable identities and only
previously public compatibility aliases; ignored pilot migration history
remains private review evidence. Refresh that baseline with
`uv run kb tools canonical-identity-baseline`, without treating the command as
a retrieval cutover. Service builds dual-write both projections, stores
canonical files as R2 projection artifacts, and loads separate canonical D1
tables. Normal readers follow the runtime active-reader marker; canonical is
the reviewed default after the 2026-08-03 cutover and legacy remains the
guarded rollback. Only anonymously opted-in `external-test` and `maintainer`
callers may explicitly request the `canonical-canary` comparison projection.
See
[Canonical Knowledge Shadow](canonical-knowledge-shadow.md).

Public reviewer adjudications live in
`claims/claim-review-dispositions.jsonl`. They resolve bounded source-backed
rows into answer-approved or routing-only tiers with a public rationale. The
live-verification overlay is applied afterward and remains the only path to
`live_verified`.

Approved media promotions update generated public layers after:

```bash
uv run kb build --stage claims
uv run kb build --stage concepts
uv run kb build --stage refresh-claims
uv run kb build --stage agent-pack
uv run kb publish export
```

Pin `ROCK_KB_GENERATED_AT` during the rebuild when you want stable generated metadata. `kb build --stage refresh-claims` keeps `guide.md` readable by inserting bounded approved-claim and approved-media summaries, while writing full per-concept tables to `knowledge/concepts/<concept>/approved-claims.md` and `knowledge/concepts/<concept>/approved-media.md`.

Use `kb status` after promotions; it compares approved media and approved claim hashes against generated concept dependency metadata and long-form guide dependency metadata. If concepts are flagged, run the suggested `kb build --stage ...` commands. If a long-form guide still needs authored work, refresh the authored guide body, then run `kb build --stage guide-intel`, `kb build --stage agent-pack`, and `kb publish export`.

Open-question cleanup is part of the refresh quality gate. After meaningful source scrapes, transcript batches, promotions, or guide synthesis, run `kb build --stage guide-intel` for affected concepts and compare regenerated `open-questions.md` files. Resolved `Needs Citation` rows should persist after rescrapes when citations, approved claims, source maps, or guide-intel logic are fixed durably; recurring rows usually mean the generator path needs correction. See [Source Scan And Rebuild Orchestration Runbook](source-rebuild-orchestration-runbook.md) for the cadence.

## Private Corpus

Private corpus commands make ignored local artifacts portable without publishing them. `kb corpus init --path <private-repo>` creates the expected private checkout layout. `kb corpus report` reports ignored text/JSON artifacts and large media. `kb corpus sync --path <private-repo>` copies ignored text/JSON artifacts such as transcript JSON, sidecars, review candidates, private promotions, normalized records, manifests, and benchmark outputs.

`kb corpus media-manifest --path <private-repo>` writes restore pointers for large media and frames that should live in Git LFS, DVC, rclone/restic, S3/R2/Backblaze, or another private object store. `kb corpus audit` checks that public artifacts do not contain private corpus paths, direct media fields, raw transcript fields, or other private leakage. `kb corpus verify-rebuild --path <private-repo>` verifies that the mounted private corpus has the portable raw, normalized, review, and media text artifacts needed to continue processing; with `--public-export-destination`, it also runs a scratch public export rebuild check.

## Contribution And Publishing

Private-source contribution work starts in ignored review artifacts and reaches tracked public rows only after review, redaction, and license attestation. The current command sequence is `kb private scan`, `kb private review-report`, `kb private distill`, `kb contributions promote`, `kb build`, and audit. See [Contributor Reviewer Workflow](contributor-reviewer-workflow.md) for the full review path.

The single-public-repo goal in [Agent Knowledge Network Goal](../decisions/agent-knowledge-network-goal.md) makes this repository's public tree the community-facing surface. The committed public surface is `agent/`, `claims/`, `concepts/`, `knowledge/`, `sources/`, public docs, and contribution intake paths. `kb publish export` remains a local scratch/audit payload for now; do not commit `data/public-export/` or treat it as the source of truth. The legacy split push/import commands are retired. See [Public Publish Runbook](public-publish-runbook.md) for the current transition rules.

## Answer Pack And Agent Layer

The generated answer layer sits above claims and guides. `kb build --stage answers` writes `agent/answer-pack.jsonl`, `agent/live-inspection-checklists.jsonl`, `agent/claim-review-queue.jsonl`, `agent/source-conflicts.jsonl`, `agent/distilled-claims.jsonl`, `agent/source-authority-rules.jsonl`, `agent/evaluation-set.jsonl`, `agent/evaluation-results.jsonl`, `agent/evaluation-report.json`, `agent/claim-review-dashboard.md`, and per-concept `answers/*.md` plus `live-inspection-checklist.md`.

The answer pack is the best first retrieval target for agents; it routes common questions to top approved claims, reviewer-authored best-answer overrides for high-value concepts, distilled claim clusters, live-instance inspection probes, citations, source-authority rules, and authority/conflict review prompts. `kb build --stage agent-pack` runs answer-pack generation automatically as part of the agent layer.

## Readiness Audit

Use `uv run kb audit readiness` as the goal-level audit, or `uv run kb audit all` when you need licenses, source policy, public export, and readiness in one sequence. Readiness reports hard failures and incomplete areas against the project goal, including source policy, public export, concept entrypoints, source-hash metadata, private media coverage, and private/public boundary checks. A report status of `incomplete` means the safety gates can pass while the corpus still needs more private ingestion or transcription.
