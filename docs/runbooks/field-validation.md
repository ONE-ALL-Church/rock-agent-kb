# Anonymous Field Validation

Rock KB field validation is an opt-in, privacy-bounded way for agents to report
whether public results work in real tasks. It is separate from formal
evaluation, the external test round, malfunction reports, and community
contributions.

## Consent And Setup

Use consent notice version `2`. Version `1` quality-feedback permission does not
cover an anonymous installation marker or usefulness outcomes. The human must
choose `Allow automatically`, `Ask each time`, or `Do not send`, and must
separately permit storing that choice in private user-level memory.

After persistent consent:

```bash
uvx rock-kb telemetry enable --cohort community --consent-attested
uvx rock-kb install-agent
```

Restart or reload the agent host. Use `external-test` only for the formal public
church test cohort and `maintainer` only for maintainer work. The client keeps a
random `rkbi_...` marker in the user's private state directory with restrictive
permissions. `telemetry status` does not print the raw marker. User-scoped MCP
configuration must contain the marker so the host can send it; treat that local
configuration as private. The Worker stores only a one-way Rock-KB-scoped hash.

Project-scoped MCP configuration does not receive the user-private marker. To
revoke consent, run `uvx rock-kb telemetry disable`, rerun `install-agent`, and
restart the host.

## Signals

Use quality feedback when an exact result itself is helpful, outdated, missing,
incorrect, or routed incorrectly:

```bash
uvx rock-kb feedback '<result-id>' --rating -1 --reason outdated
```

Use an outcome only after an exact result materially contributed to a completed
task:

```bash
uvx rock-kb outcome '<result-id>' \
  --outcome partially_useful \
  --reason incomplete \
  --consent-attested
```

Allowed outcomes and compatible reasons are:

| Outcome | Reason codes |
|---|---|
| `useful` | `answered`, `actionable`, `well_sourced`, `correct_route` |
| `partially_useful` | `incomplete`, `unclear`, `needed_other_sources`, `version_gap`, `weak_evidence` |
| `not_useful` | `incorrect`, `outdated`, `wrong_route`, `missing_detail`, `not_actionable`, `source_conflict` |

Send one to three unique reason codes. Submit at most one quality rating and one
outcome per exact result per completed task. Submit nothing when the result was
not materially used or its usefulness is uncertain.

## Retained And Excluded Data

Field validation may retain the hashed installation marker, fixed cohort,
client class/version, operation, public result ID and kind, projection version,
fixed rating/outcome/reasons, timestamps, and aggregate counts. It never stores
the raw installation marker, question or prompt, organization, church or person
identity, IP address, raw or hashed query text, attempted exact IDs for misses,
free text, logs, secrets, or Rock data.

The service rate-limits outcomes to 100 per opted-in installation per UTC day.
Every accepted outcome returns a stable `kbo_...` identifier.

## Dashboard And Review Queue

`uvx rock-kb dashboard` and `kb_review_dashboard` expose a `field_validation`
section. By default it excludes evaluation and maintainer traffic. The funnel
counts search, exact retrieval success/failure, outcome, feedback, and
report-issue events. Every stage uses the v5 event stream beginning with service
v0.16.0; older telemetry is intentionally excluded from this funnel so its
stages share one coverage window. The broader telemetry summary retains
historical aggregate continuity.

The service builds a bounded queue of at most 50 aggregate review items from:

- `partially_useful` and `not_useful` outcomes grouped by canonical public result;
- public topic categories that produce at least three zero-result searches;
- failed exact-lookup operation types.

The queue does not expose queries, unknown attempted IDs, installation hashes,
or private data. It directs maintainers to investigate; it does not
automatically change ranking, edit knowledge, or create GitHub issues.
