# Public/Private Knowledge System Goal

## Goal

Build the Rock RMS knowledge base as a two-tier system:

- **Private corpus:** raw fetched pages, transcripts, hydrated source packs, crawler caches, full extracted text, private repo review notes, embeddings, and deeper analysis inputs available only to the owner or approved agents.
- **Public distilled repo:** original synthesized guides, quickstarts, task cards, entity indexes, release caveats, source maps, source hashes, confidence labels, and links to authoritative sources.

The private layer lets agents deeply process source material. The public layer publishes the durable distilled value without exposing protected source material, private church data, secrets, or long copied passages.

## Why This Exists

Agents can search the web, but web search does not reliably rank Rock source authority, connect docs to release notes and source code, expose version caveats, map concepts to entities and tables, track source-driven rebuilds, or tell agents what live Rock records to inspect.

The public output should be an agent operating layer, not an internet mirror.

## Public Layer

The public layer may include:

- synthesized concept guides,
- one-page quickstarts,
- task cards,
- entity/model/table indexes,
- release caveat indexes,
- section-to-source maps,
- source URLs and hashes,
- short excerpts only when allowed and necessary,
- open questions and review flags,
- confidence labels such as `official`, `source-code-confirmed`, `release-note-confirmed`, `community-example`, `agent-inference`, and `needs-live-verification`.

It should not include raw full-text documentation, full transcripts, protected source mirrors, private repo content, secrets, private data, or long copied passages unless the source license explicitly allows it.

## Private Layer

The private layer may include raw HTML, full extracted Markdown, transcripts, hydrated source packs, crawler cache, local full-text/vector indexes, approved private repo packs, source hashes, and unpublished review notes.

Private storage is a working corpus, not a publication target. Private raw data may inform public synthesis, but it must pass export checks before becoming public.

## Required Tooling

The CLI should support:

- private ingest,
- private media discovery and transcription queues,
- public export,
- publish audit,
- source policy audit,
- section-level rebuild detection,
- concept/task/entity/release index generation,
- stale-section reports after source refresh.

Media discovery/transcription should remain private by default. Podcast audio, RockU video pages, and community hub media can be downloaded/transcribed for local synthesis, but raw transcripts are private corpus inputs and must not appear in the public export.

The private media layer should maintain one durable sidecar per media item plus a textless JSONL routing index. Sidecars may contain raw transcripts, transcript hashes, source metadata, media URLs, and future visual scene notes. The JSONL index should be safe for agents to scan locally because it stores paths, source URLs, status, hashes, and counts without transcript text. Public concept guides may use only reviewed, distilled media insights with citations and source hashes.

Private-derived normalized records, including media transcript insights, are not automatically part of the public agent pack. They remain local retrieval records until they are explicitly redaction reviewed or approved for public distillation. Use `kb media candidates` or `kb media candidates --all-sources` to produce textless review prompts, then use `kb media promote --rewrite-file <jsonl>` to record reviewer-written public claims before rebuilding public concept guides or public export. Placeholder candidate text must not feed the public dependency layer. Reviewed media claims may carry timestamps and canonical timestamp/source page URLs for citation routing, but public artifacts should not expose direct media file, HLS, or tokenized player URLs. Public export audits should fail if private transcript derivation markers or raw transcript fields appear in public JSON.

Raw transcript completion alone should not update public guides. Approved media promotions should update generated public layers after `kb build --stage claims`, `kb build --stage concepts`, `kb build --stage refresh-claims`, `kb build --stage agent-pack`, and `kb publish export`. Use `kb media review-status` to monitor transcribed, candidate, approved, pending, and affected-concept coverage. Use `kb status` to decide whether a long-form `guide.md` needs a reviewer-authored update or full synthesis refresh; the plan compares approved media insight hashes and approved claim hashes against generated concept dependency metadata and long-form guide dependency metadata, and it distinguishes generated `index.md` rebuilds from `guide.md` refreshes. Long-form guides should show bounded claim and media summaries; full per-concept tables belong in generated `knowledge/concepts/<concept>/approved-claims.md` and `knowledge/concepts/<concept>/approved-media.md` artifacts.

The answer layer should remain generated from approved claims, not raw transcripts. `agent/answer-pack.jsonl` is the compact first-pass retrieval artifact for common operational questions. High-value concepts may use reviewer-authored best-answer override text while retaining approved claim IDs, distilled claim IDs, and citations. `agent/live-inspection-checklists.jsonl` and per-concept `live-inspection-checklist.md` files tell agents what to verify in the live Rock instance before recommending changes, including concrete read-only SQL/check probes where known. `agent/claim-review-queue.jsonl` ranks approved claims for future merge, live-verification, and answer-pack review. `agent/distilled-claims.jsonl` groups duplicate and near-duplicate approved claims into generated reviewer-approval candidates. `agent/source-authority-rules.jsonl` records concept-specific source preference and community-source usage rules. `agent/evaluation-set.jsonl`, `agent/evaluation-results.jsonl`, and `agent/evaluation-report.json` are deterministic quality gates for answer body, citations, live-check steps, probes, and caveats. `agent/claim-review-dashboard.md` groups the queue by concept and action. `agent/source-conflicts.jsonl` is an authority-alignment report: it highlights community-derived and higher-authority claim clusters that deserve review, but it is not by itself proof of contradiction.

## Source Policy

Every source should declare owner, license posture, ingest mode, private storage permission, public publish mode, allowed excerpt length, refresh cadence, preferred tooling, and whether human review is required.

Suggested publish modes:

- `public_full_text_allowed`
- `public_excerpt_only`
- `public_cite_and_summarize_only`
- `private_only`
- `manual_review_required`

## Completion Criteria

This architecture is complete when agents can ingest the private corpus without public raw commits; public exports contain only distilled, source-linked, audit-passing artifacts; each concept has quickstart, task cards, entities, release caveats, source maps, section status, and open questions; every public claim traces to source URLs or records; changed sources identify stale sections or task cards; publish audits block private data, secrets, excessive copied text, and disallowed full text; and future agents can start from `agent/rock-kb-manifest.json`.
