# Rockumentation API Source Quality Follow-up

Date: 2026-06-18

## Decision

Keep the Rockumentation block-action API as the preferred ingestion path for
`rock_documentation`, `rock_developer`, and `rock_mobile_docs`.

Keep `rock_lava_docs` on the static/custom parser path until a future probe
shows that Lava pages return real article content through a comparable API
payload.

Keep `/subscriptions` out of `rock_community_site`. Add a dedicated
`rock_subscriptions` source only if subscription pages later produce reusable
Rock implementation guidance and can pass their own timeout, scope, and quality
tests.

## Findings

- API-ingested documentation records now carry stable article metadata such as
  `documentation_article_id`, `documentation_slug`, `documentation_family`,
  table-of-contents links, content links, current version, and version links.
- Public artifacts still cite and summarize; they do not mirror full article
  text. The fuller API text is used as the normalization input for summaries,
  excerpts, concept dependencies, and guide intelligence.
- Spot checks found no duplicate normalized IDs in the API-backed
  `rock_documentation`, `rock_developer`, or `rock_mobile_docs` records.
- Static residual sources can still produce duplicate normalized records when a
  crawl discovers the same canonical page more than once. The public build now
  deduplicates normalized records by ID before building public source summaries,
  citations, topics, source pages, guide intelligence, and the hosted export.

## Current Quality Signals

- `rock_documentation`: 921 normalized records before dedupe, 909 via
  `rockumentation_block_action`, zero duplicate IDs.
- `rock_developer`: 361 normalized records before dedupe, 347 via
  `rockumentation_block_action`, zero duplicate IDs.
- `rock_mobile_docs`: 275 normalized records before dedupe, 274 via
  `rockumentation_block_action`, zero duplicate IDs.
- `rock_lava_docs`: deduped from 54 to 53 public source records.
- `rock_community_site`: deduped from 30 to 26 public source records.
- Claim review queue after the pass: 0 actionable rows. Existing
  `routing_context_only` claims remain available through explicit source-routing
  retrieval, but ordinary search excludes them and they no longer keep
  `kb status` open as pending review work.

## Follow-up

Use source-refresh scans and the duplicate source URL audit after future
community-site or Rockumentation changes. If duplicate normalized IDs reappear
in a source-specific crawl, prefer fixing the discoverer; the public-agent-pack
dedupe is a defensive boundary for generated artifacts.
