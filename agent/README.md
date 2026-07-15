# Agent Entry Points

This directory contains generated public files for AI agents:

- `rock-kb-manifest.json` - canonical map of concept files and global agent entry points.
- `answer-pack.jsonl` - compact source-linked answers for common Rock questions.
- `concept-index.jsonl`, `concept-task-cards.jsonl`, `entity-index.jsonl`, and `release-index.jsonl` - cross-concept lookup indexes.
- `model-map-*.jsonl`, `model-map-digests.jsonl`, and `model-map-summary.json` - stable-first public Rock model-map details, exact model digests, and version differences.
- `lava-capabilities.jsonl`, `lava-capability-summary.json`, `lava-contexts.jsonl`, and `lava-context-summary.json` - public Lava capability and data-context reference data.
- `live-inspection-checklists.jsonl` and `live-probe-recipes.jsonl` - generic read-only verification patterns for local Rock instances.
- `recipes.jsonl` and `recipe-summary.json` - reusable community implementation patterns with immutable code pins, adaptation points, security, compatibility, and validation guidance.
- `rock-issues.jsonl`, `rock-issue-enrichments.jsonl`, and `rock-issue-summary.json` - public-safe Rock core and mobile issue routing metadata, typed version evidence, timeline coverage, official release-note links, and separately reviewed public conclusions. The upstream issue row remains a lead, not an approved product claim.
- `source-summaries.jsonl`, `source-citations.jsonl`, and `source-summary-report.json` - source coverage and citation metadata.
- `distilled-claims.jsonl`, `source-authority-rules.jsonl`, and `claims/approved-claims.jsonl` - public distilled claim data and authority rules.
- `llms.txt` - AI-readable source and repo map.

Review queues, conflict reports, evaluation sets, and private media indexes are build-internal by default. They are intentionally not part of the public export.

Maintainers rebuild with:

```bash
uv run kb build-agent-pack
uv run kb public-export
```
