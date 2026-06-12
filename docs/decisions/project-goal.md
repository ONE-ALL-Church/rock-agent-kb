# Project Goal

Build a universal Rock RMS knowledge base that is useful to humans and optimized for AI agents.

The project is a two-tier knowledge system:

- **Private processing layer:** ingest, cache, transcribe, hydrate, index, and analyze the full source corpus available to the owner or approved agents.
- **Public distilled layer:** publish original synthesized guidance, quickstarts, task cards, entity indexes, release caveats, source maps, source hashes, confidence labels, and links without republishing protected full-text source material unless explicitly allowed.

The goal is not a mirror of Rock documentation. The goal is a source-ranked, task-oriented agent operating layer that helps agents work faster than web search by connecting official docs, release notes, source code, RockU, recipes, Q&A, and live Rock records.

## Primary Outcomes

- Git-native Markdown and JSONL that humans and agents can review, diff, rebuild, and cite.
- Public artifacts that are publishable, distilled, source-linked, and audit-passing.
- Private raw-corpus workflows that support deeper local analysis without leaking protected material.
- Per-source policy for license posture, ingest mode, publish mode, refresh cadence, and review requirements.
- Agent entrypoints for each concept: `quickstart.md`, `task-cards.jsonl`, `entities.jsonl`, `release-caveats.jsonl`, `section-source-map.jsonl`, `section-status.jsonl`, `troubleshooting-tree.json`, and `open-questions.md`.
- CLI tooling for discovery, ingest, hydration, normalization, synthesis, guide intelligence, publish/export audit, source policy audit, indexing, and stale-section reporting.

## Completion Goal

The system is complete enough for real use when an agent can start at `agent/rock-kb-manifest.json`, choose a concept or task, load the relevant quickstart, task card, entity map, release caveats, and source map, then know what official documentation, source code, release notes, community examples, and live Rock records to inspect next.

## Done Criteria

- Private ingest can collect the working corpus without committing raw protected material publicly.
- Public export emits only distilled guides, quickstarts, task cards, entity indexes, release caveats, source maps, source hashes, and citations.
- Every public artifact traces back to source records or source URLs.
- Guide audits check authority coverage, release-note coverage, source-code coverage, task-card coverage, entity coverage, citations, and live-verification flags.
- Publish audits fail on secrets, private data, private repo content, excessive copied text, disallowed full text, and community examples presented as official guidance.
- Rebuild metadata identifies which sections or task cards depend on changed source hashes.
- The public layer remains useful without private access; private access gives agents deeper retrieval before producing public distilled outputs.

## Goal Readiness Audit

Run `uv run kb audit readiness` before claiming the project is complete. This audit collects evidence for the goal-level criteria: source registry validity, normalized corpus coverage, public export/policy audits, agent manifest entrypoints, concept artifact quality, staleness, source-hash rebuild metadata, private media coverage, and private/public boundary checks.

The audit can return `incomplete` even when tests and publish audits pass. That is expected while private media transcription or other private corpus ingestion remains partial.

## Non-Goals For V1

- Do not mirror all public web content by default.
- Do not publish private repo content automatically.
- Do not make vector search the source of truth.
- Do not rely on a hosted scraping or AI service as the only rebuild path.
