# MCP Retrieval Quality V3

Date: 2026-07-29

## Decision

Ordinary search returns source-backed or stronger material by default. Routing
metadata remains available only through an explicit
`min_claim_tier: routing_context_only` request or a dedicated issue or Idea
operation.

Routing-only source commentary is not published as an approved claim. Its
reviewed source record remains discoverable through `source_summary` rows, so
source navigation is preserved without inflating the claim graph.

Task cards and troubleshooting-tree branches are first-class search result
kinds. A deterministic query-intent classifier promotes them for symptoms and
keeps exact Model Map, Lava context, recipe, issue, and Idea tools available for
their narrower jobs.

Search responses are compact by default. Detailed ranking signals require
`debug: true`; scores are rounded. Claim lists use explicit authority and claim
tier fields plus bounded pagination. Concept result expansion returns its full
indexed body.

## Quality Metrics

Guide artifact presence is reported as `completeness_score` and
`completeness_status`. It is not a knowledge-quality measure.

Knowledge quality is reported separately from:

- answer-bearing claim share;
- version scope on version-sensitive, retrieval-eligible claims;
- source-evidence coverage;
- primary and routed claim counts; and
- hosted retrieval evaluation status when measured.

A concept with no primary claim cannot report a passing knowledge-quality
status. The manifest also reports total, retrieval-eligible, answer-bearing,
routing-only, version-scoped, version-independent, and unprocessed claim
counts.

## Source-Cohort Finding

The prior concept-quality split was primarily a source-mix difference. Newer
concepts had reviewed full-article official-document claims. Older concepts
were dominated by public media summaries that intentionally route agents to a
source and require stronger evidence before becoming operational answers.

The fix is to expand the full-article official-document review queue across the
under-covered concepts. Generic media routing notes must not be relabeled as
technical answers to improve a percentage.

## No Server-Side Answer Synthesis

The Worker does not expose a `kb_answer` tool. It has no hosted language model,
and deterministic string assembly would blur retrieval evidence with
synthesis. Agents should use intent-aware search, exact retrieval, and the
structured trust fields to compose an answer in their own model context.

A future composite evidence-pack operation may bundle bounded result IDs,
citations, caveats, live checks, and related issues without claiming to
synthesize an answer. It should be added only if usage telemetry shows that the
remaining follow-up calls materially harm outcomes.
