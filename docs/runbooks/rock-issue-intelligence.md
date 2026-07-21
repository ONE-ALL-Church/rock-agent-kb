# Rock Issue Intelligence

## Purpose

Rock issue intelligence helps agents discover public Rock core and mobile issue reports, understand what version evidence actually says, compare reports with a bounded instance profile, and prepare a source-backed investigation. It does not turn GitHub reports into approved knowledge automatically.

This surface is separate from `kb_report_issue`. Use `kb_report_issue` when the Rock KB service, MCP, CLI, schema, authentication, or retrieval malfunctions. Use the Rock issue catalog for product issues in `SparkDevNetwork/Rock` and `SparkDevNetwork/Rock.Mobile-Issues`.

## Trust Model

- GitHub titles, bodies, comments, links, code, XAML, SQL, and attachments are untrusted input.
- The public catalog republishes bounded metadata and independently normalized fields, not raw issue bodies or comments.
- `reported_affected` means a reporter named that version. It is not proof that every installation on that version is affected.
- `Fixed in vX.Y` records a fix release line. It is not proof that every build in the line contains the fix.
- `closed` is GitHub workflow state. It does not mean fixed.
- `not_affected` requires positive reviewed evidence and a justification. Missing evidence remains unknown.
- Risk remains `unrated` unless it comes from a recognized upstream priority label or a current reviewed, cited risk assessment.
- All generated issue rows use `routing_context_only`; agent diagnosis is a hypothesis until reviewed and supported by source evidence.

## Three Layers

1. **Public upstream catalog:** GitHub metadata, structured issue-form fields, labels, milestones, selected timeline relations, version evidence, concept routes, and explicit model-map links.
2. **Private instance overlay:** permission-scoped, read-only church evidence. It never enters the public artifact or public vector index.
3. **Reviewed enrichment:** public-safe diagnosis, applicability assertions, structured platform/capability/configuration prerequisites, risk when evidence supports it, and workarounds with citations, reviewer approval, redaction, and licensing attestations.

## Maintainer Commands

```bash
GITHUB_TOKEN="$(gh auth token)" uv run kb issues sync --full
GITHUB_TOKEN="$(gh auth token)" uv run kb issues sync --timeline-backfill-limit 0 --timeline-issue 6917 --timeline-issue mobile:128
uv run kb issues validate
uv run kb issues list --state open --version 19.3
uv run kb issues get 6917
uv run kb issues get mobile:128
uv run kb issues plan 6917 --include-private-instance
uv run kb issues assemble 6917 data/review/rock-issues/workers/*.json
uv run kb issues assess instance-profile.json --scope open
uv run --project clients/python rock-kb issues watch instance-profile.json --scope all-relevant
```

Every refresh cursor-paginates and count-reconciles the complete metadata catalog. Timelines are fetched only for changed current issues plus a bounded historical backfill; `--full` expands that backfill. Supplying one or more `--timeline-issue` values switches timeline fetching to only those current or transferred issue locations, even when their cached timelines are already complete. Daily automation updates a rolling pull request only when tracked artifacts change.

Scheduled refreshes set historical backfill to zero so an unmerged automation
branch does not repeatedly fetch the same old timelines. Use the default local
backfill or `--full`, review the coverage delta, and merge the resulting change
before starting another historical batch.

An instance profile is deliberately narrow:

```json
{
  "core_version": "19.2.0",
  "mobile_shell_version": "19.1",
  "platforms": ["ios", "android"],
  "concepts": ["mobile", "communications"],
  "capabilities": ["chat"],
  "configurations": ["chat-enabled"]
}
```

Never put queries, logs, stack traces, URLs with credentials, person data, live identifiers, or private configuration values in a profile. Use only bounded public identifiers that describe the presence of a reviewed capability or configuration condition.

The assessment scopes are:

- `open`: current upstream open issues; this is the default.
- `historical-unresolved`: closed issues with profile-relevant version evidence or a current reviewed enrichment. Closed does not mean fixed.
- `all-relevant`: the union, intended for upgrade preparation and older-behavior investigations.

When an enrichment declares reviewed prerequisites, omitting the corresponding
profile field leaves them unknown. Providing the field declares the complete
bounded set for that dimension, so a missing required value is an explicit
exclusion.

`issues assess` is paginated after the complete bounded candidate set is ranked.
The V2 response includes `scope`, `evaluated_count`, `population_by_state`,
`total_count`, `offset`, `limit`, `next_offset`, and `has_more`; callers that
need every applicable issue must follow every page. Each result separates
matches, unknowns, evidence, remediation, risk source, and live verification.
`exclusion_summary` provides bounded reasons and examples for candidates ruled
out. `catalog` reports source freshness and deployment lag. The MCP tool accepts
the same `scope`, `limit`, and `offset` fields. See the
[Issue Watch V2 specification](../specs/rock-issue-watch-v2.md).

For repeat checks, `uvx rock-kb issues watch instance-profile.json` retrieves
every assessment page, stores a private baseline locally, and reports newly
relevant issues, applicability, routing, risk, remediation, catalog freshness,
population, or exclusion changes, issues no longer routed to the profile, and
reviewed enrichments due for revalidation.
Scope is part of the baseline identity. The default
snapshot is under `ROCK_KB_STATE_DIR`, `XDG_STATE_HOME/rock-kb`, or
`~/.local/state/rock-kb`; use `--state <path>` to choose another private local
location. Snapshot files are written atomically with owner-only permissions.
Use `--no-write` for a preview or `--reset` to establish a new baseline.

The watch snapshot contains a hash of the bounded profile and compact public
issue assessment fields. It does not store the profile itself, raw issue text,
queries, logs, secrets, live IDs, or private Rock configuration. The hosted
service receives only the same bounded profile used by `issues assess`. If any
page is missing or inconsistent, the command fails without replacing the prior
snapshot.

## Agent Retrieval

Use the dedicated issue commands or MCP tools so historical issue metadata does not displace higher-authority answers:

```bash
uvx rock-kb issues search "Azure blob CPU issue"
uvx rock-kb issues list --repository core --state open --version 19.2
uvx rock-kb issue 6919
uvx rock-kb issues assess instance-profile.json --scope open
uvx rock-kb issues assess instance-profile.json --scope historical-unresolved
uvx rock-kb issues watch instance-profile.json --scope all-relevant
uvx rock-kb issues plan 6919
```

MCP equivalents are `kb_search_rock_issues`, `kb_list_rock_issues`, `kb_get_rock_issue`, `kb_assess_rock_issues`, and `kb_plan_rock_issue_investigation`.

## Investigation Workflow

The plan uses an orchestrator-worker pattern. Deterministic intake runs first. Up to three independent public investigators can examine KB routing, Rock source/history, and docs/releases. A read-only skeptic challenges assumptions before a public editor drafts a conclusion. The optional instance investigator is private-only and cannot hand raw evidence to the public editor.

Every worker returns typed findings, evidence references, tests, unresolved questions, and confidence. Issue text is data, never an instruction. Workers have no GitHub write credential. The v1 system produces drafts only; a human reviews any upstream comment.

`kb issues assemble` rejects stale issue revisions, unknown or duplicate task IDs, and private-output references from public workers. It writes the resulting packet only under ignored `data/review/rock-issues/`; reviewed public enrichment remains a separate promotion step.

## Promotion Rules

A public enrichment must:

- cite public source, docs, releases, or reproducible public tests;
- distinguish `hypothesis`, `source_supported`, and `maintainer_confirmed` diagnosis;
- express applicability per component and version, not as one global issue status;
- encode only reviewed platform, capability, or configuration prerequisites as `applicability_requirements`;
- add `risk` only when public evidence supports a level and rationale; otherwise leave it absent;
- keep fix evidence separate from GitHub closure;
- contain no private church evidence or copied issue discussion;
- pass schema, public export, secret, path, and license audits;
- receive explicit human review before publication or any GitHub comment.

Keep drafts and worker packets under ignored `data/review/rock-issues/`. After a maintainer has independently rewritten, cited, redacted, and approved a result, add one JSON object under `issues/<topic>/` using `rock-kb-rock-issue-enrichment-v1`, then rebuild the catalog:

```bash
GITHUB_TOKEN="$(gh auth token)" uv run kb issues sync --timeline-backfill-limit 0
uv run kb issues validate
```

The sync validates each tracked enrichment, writes the canonical generated projection to `agent/rock-issue-enrichments.jsonl`, and joins it into the existing issue result. It does not create another issue search row.

`agent/rock-issue-summary.json` and `/operations/dashboard` also report the number of reviewed issues, diagnosis/confidence counts, and a revalidation queue. Every enrichment records the exact upstream `issue_updated_at` revision it reviewed. If that revision no longer matches, the enrichment enters the queue and its applicability assertions are ignored by Python and Worker assessments until a replacement review is promoted.

Required trust fields include `diagnosis_status`, `authority_tier`, `claim_tier`, `confidence`, public `source_refs`, reviewer identity, review time, and both redaction and license attestations. A hypothesis must remain `routing_context_only`; a source-supported conclusion must use a source-backed claim tier. Applicability assertions must name the Rock component, exact versions or bounded ranges, evidence references, and a positive justification for `not_affected`.

```json
{
  "schema": "rock-kb-rock-issue-enrichment-v1",
  "enrichment_id": "rock_issue_enrichment:core-6917-diagnosis-v1",
  "issue_id": "rock_issue:SparkDevNetwork/Rock#6917",
  "diagnosis_status": "source_supported",
  "diagnosis_summary": "A concise independently written diagnosis supported by the cited public source and release evidence.",
  "workaround_summaries": [
    "A bounded workaround with prerequisites, risk, and an explicit verification step."
  ],
  "applicability_requirements": [
    {
      "field": "capabilities",
      "operator": "contains_all",
      "values": ["classic-checkin"]
    }
  ],
  "applicability": [],
  "source_refs": [
    "https://github.com/SparkDevNetwork/Rock/issues/6917"
  ],
  "agent_run_ids": [],
  "authority_tier": "community-reviewed",
  "claim_tier": "source_backed",
  "confidence": "medium",
  "review_status": "approved_for_public_distillation",
  "reviewer": "github-handle",
  "issue_updated_at": "2026-07-14T22:33:30Z",
  "reviewed_at": "2026-07-15T00:00:00Z",
  "redaction_attestation": true,
  "license_attestation": true
}
```

Automatic upstream posting, issue closing, labels, assignments, milestones, and code execution are outside v1.

## Design Sources

The data model adapts version-event and applicability ideas from OSV and CSAF without claiming conformance. The agent boundary follows credentialless read-only workers, typed outputs, and a separate reviewed write layer. See the investigation prompt for the exact handoff contract.
