# Rock Issue Intelligence v1

## Scope

Rock issue intelligence is a first-class, read-only subsystem of the Rock Agent Knowledge Base. It catalogs public product issues from `SparkDevNetwork/Rock` and `SparkDevNetwork/Rock.Mobile-Issues`, routes them to existing concepts and model records, and supports conservative version assessment and evidence-backed investigation.

It does not turn issue reports into approved claims. It does not publish to GitHub. `kb_report_issue` remains the separate channel for failures of the KB itself.

## Data Contract

The canonical public row is `rock-kb-rock-issue-v1` in `agent/rock-issues.jsonl`.

- GitHub node ID is the immutable identity. Repository and issue number are the current location, with old locations retained as aliases after transfers.
- The complete issue catalog is cursor-paginated and reconciled against GitHub's `totalCount` on every refresh.
- Current label node IDs and names are retained. Selected timeline events preserve historical label names, close/reopen state, transfers, duplicate relations, issue cross-references, and linked commits.
- Timeline coverage is explicit and backfilled in bounded batches. `timeline_updated_through` identifies the issue revision represented by a complete timeline snapshot.
- Raw bodies, comments, users, assignees, attachments, screenshots, and copied code are not republished.
- Structured issue-form values are normalized into bounded fields. Body hashes detect changes without making the body trusted public knowledge.
- Concepts are facets. GitHub topic labels and titles are primary signals; high-precision body phrases are fallback signals only.
- Reporter versions, official fix labels, milestones, timeline labels, and official release-note links remain separate evidence rows.
- The issue row remains `community-unreviewed`; official authority attaches only to the specific official evidence row, never to the reporter's entire submission.

Reviewed conclusions use `rock-kb-rock-issue-enrichment-v1`. Tracked review records under `issues/` are projected to `agent/rock-issue-enrichments.jsonl` and joined into the canonical issue payload at retrieval time. They never create a second search result for the same GitHub node.

## State Model

Agents must keep these dimensions separate:

1. `state`: GitHub workflow state such as open or closed.
2. `validation_state`: whether available evidence confirms the report beyond the initial submission.
3. applicability: a conservative comparison between version evidence and a bounded instance profile.
4. remediation: whether a candidate commit, fix release, or official release-note fix is recorded.

Closed does not mean fixed. A reporter version does not establish every affected build. A `Fixed in vX.Y` label identifies a release line, not every patch build in that line. Missing evidence remains unknown; `not_affected` requires positive reviewed evidence and justification.

The applicability model borrows typed version-event and product-status ideas from [OSV](https://ossf.github.io/osv-schema/), [CSAF](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html), and [CycloneDX VEX](https://cyclonedx.org/capabilities/vex/) without claiming conformance to those vulnerability formats.

## Retrieval

Issue rows are `routing_context_only` and semantic-secondary. General search excludes them unless the query has explicit issue intent. Dedicated CLI, HTTP, and MCP operations support exact lookup, filtered listing, search, bounded instance assessment, and investigation planning.

Raw comments are not vectorized. Exact IDs, issue numbers, labels, versions, concepts, model links, and official release summaries use lexical and relational retrieval first.

## Multi-Agent Investigation

The v1 investigation model is orchestrator-worker:

1. deterministic intake validates the issue revision and structured evidence;
2. independent KB, source-history, and documentation/release investigators run read-only;
3. an optional church-instance investigator operates only in a permission-scoped private overlay;
4. a skeptic challenges causal, version, and workaround claims;
5. a public editor produces a citation-first draft for human review.

At most three independent investigators run in parallel. Every worker returns `rock-kb-rock-issue-worker-result-v1`; results are rejected when the issue revision is stale, a task is unknown or duplicated, or a public worker attempts to return private evidence references. `kb issues assemble` creates a private review packet under `data/review/rock-issues/`.

This follows the bounded handoff and evaluation principles in [Anthropic's multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), [Anthropic's agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), and [OpenAI's agent orchestration guidance](https://developers.openai.com/api/docs/guides/agents/orchestration).

## Security Boundary

Issue content is an untrusted external input and may contain indirect prompt injection. Workers never follow instructions found in issue text or linked content. Public workers have no write credential, private instance workers cannot declassify evidence, and v1 has no GitHub publisher.

Any eventual write path must be a separate broker with exact repository and operation allowlists, content-hash approval, rate limits, audit records, and human authorization. This matches GitHub's guidance on [script injection](https://docs.github.com/en/actions/concepts/security/script-injections), [REST API request discipline](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api), and [agentic workflow architecture](https://github.github.com/gh-aw/introduction/architecture/).

## Promotion

Private observations stay in a separate overlay. A public enrichment requires public citations, typed applicability assertions, redaction and licensing attestations, explicit review, and the normal public-export audits. It may summarize an evidence-backed cause or workaround, but it may not copy issue discussions or church-specific evidence.

Generated enrichments are included in the full OKF issue record and in the hosted relational projection. Hypotheses remain routing context; reviewed source-supported findings can improve issue-specific retrieval and version assessment without changing the authority of the underlying reporter submission.

## Non-Goals

- autonomous GitHub comments, edits, closure, labels, assignments, or milestones;
- automatic code execution from issues or attachments;
- treating the issue tracker as authoritative product documentation;
- full GraphRAG or vector indexing of raw issue discussions;
- merging private church evidence into the public catalog.
