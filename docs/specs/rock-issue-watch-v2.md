# Rock Issue Watch V2

## Purpose

Issue Watch V2 compares a bounded, public-safe instance profile with Rock core
and mobile issue routing metadata. It narrows an investigation; it does not
prove that an issue affects an instance, establish a root cause, or authorize a
production change.

The same contract is exposed by hosted REST, direct MCP, the published CLI, and
the local maintainer CLI.

## Assessment Scopes

- `open` is the default. It evaluates the current upstream open-issue
  population.
- `historical-unresolved` evaluates closed issues that have version evidence
  relevant to the profile or a current reviewed enrichment. Closed does not
  mean fixed.
- `all-relevant` evaluates the union of the two populations. Use it for upgrade
  preparation or when investigating behavior that may predate the current open
  queue.

Scopes are explicit and are part of the local watch-state identity. A baseline
for one scope is never reused for another.

## Bounded Profile

The profile accepts only:

```json
{
  "core_version": "18.2.4",
  "mobile_shell_version": "19.1",
  "platforms": ["web", "ios", "android"],
  "concepts": ["communications", "mobile"],
  "capabilities": ["scheduled-communications"],
  "configurations": ["bus-transport-in-memory"]
}
```

At least one version is required. List values are bounded public identifiers,
not prose. Never include URLs with credentials, queries, logs, stack traces,
IDs, names, secrets, or private Rock data.

When a reviewed enrichment declares an `applicability_requirement`, a missing
profile field is `unknown`. A present list is treated as the profile's complete
declaration for that field: it either matches or explicitly excludes the
requirement. Requirements can use `contains_any`, `contains_all`, or
`contains_none` over `platforms`, `capabilities`, or `configurations`.

## Result Contract

Each returned applicable result separates:

- `applicability`: `confirmed`, `likely`, `possible`, or
  `insufficient_evidence`;
- `decision.matched_on`, `decision.excluded_by`, and `decision.unknowns`;
- compact version and reviewed-enrichment `evidence`;
- `remediation`, fixed release lines, and fix-to-target relationships;
- evidence-backed `risk`;
- `live_verification`, including whether a current read-only playbook exists;
- stale enrichment IDs that require revalidation.

Candidates assessed as `not_applicable` are omitted from normal result
pagination. The bounded top-level `exclusion_summary` reports their count,
reason bases, and up to 20 examples so exclusions remain inspectable without
making every watch noisy.

The response also includes the evaluated population, state counts, pagination,
projection version, and `catalog` freshness. Callers must follow `has_more` and
`next_offset` for a complete applicable result set.

## Risk Rules

Risk is `unrated` unless one of these exists:

1. a recognized priority label applied in the upstream Rock issue tracker; or
2. a current, reviewed enrichment with a cited risk assessment.

Issue title wording, applicability, comments, agent judgment, and local anxiety
must not be converted into a severity rating. Risk affects secondary ordering
only; it never replaces applicability evidence.

## Freshness Rules

Hosted `catalog.status` is one of:

- `current`: source checks are current and source/result counts match the
  deployed projection;
- `source_stale`: one or more Rock issue sources are failed, missing, or
  overdue;
- `deployment_lag`: source checks succeeded but source and deployed projection
  counts differ;
- `not_recorded`: authoritative source-check metadata is unavailable.

Read `catalog.warning` before relying on the assessment. A stale source or
deployment lag is a reason to refresh or wait for deployment, not a reason to
silently treat old results as current.

The local maintainer CLI cannot read hosted source-operation state. It reports
`projection_consistent`, `projection_mismatch`, or `projection_only` and sets
`freshness_authority: local_projection_summary`. Only a hosted assessment with
`freshness_authority: hosted_source_operations` can report authoritative source
check age and deployment lag.

## Agent Sequence

1. Assess the `open` scope with the most specific public-safe profile available.
2. Read catalog freshness, matches, unknowns, exclusions, risk source, and
   revalidation flags.
3. Fetch exact issue records for the small set that may apply.
4. Follow only current reviewed read-only verification playbooks. Never invent
   a mutating production reproduction.
5. Use `historical-unresolved` or `all-relevant` when preparing an upgrade or
   investigating older behavior.
6. Keep local observations in a permission-scoped private overlay. Promote only
   independently reviewed, redacted, public-source-backed conclusions.

## Compatibility

Issue Watch V2 uses assessment schema
`rock-kb-rock-issue-assessment-v2`, local state schema
`rock-kb-issue-watch-state-v2`, and client result schema
`rock-kb-issue-watch-result-v2`. It requires `rock-kb` client `0.15.0` or newer.
