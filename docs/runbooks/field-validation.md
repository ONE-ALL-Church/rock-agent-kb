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

## Canonical Canary

The `external-test` and `maintainer` cohorts may explicitly test the
non-default canonical retrieval projection:

```bash
uvx rock-kb --projection canonical-canary search "<question>"
uvx rock-kb --projection canonical-canary result "<result-id>"
uvx rock-kb --projection canonical-canary outcome "<result-id>" \
  --outcome partially_useful \
  --reason incomplete \
  --consent-attested
```

Use the same projection on search, expansion, and outcome. MCP clients pass
`projection: "canonical-canary"` to `kb_search`, `kb_get_result`, and
`kb_outcome`. Do not silently retry against legacy when the purpose is to test
the canary; record the bounded failure or compare legacy in a separate,
explicit call.

Canary traffic adds a separate daily aggregate containing only projection hash,
event, client class, fixed cohort, result count, primary result kind, and count.
It does not add the marker or its hash, query text or hash, topic, result ID,
identity, IP address, or Rock data to that aggregate. A consented outcome still
uses the normal outcome record so maintainers can review the public result ID,
fixed usefulness value, reason codes, and exact projection hash.

## Retained And Excluded Data

Field validation may retain the hashed installation marker, fixed cohort,
client class/version, operation, public result ID and kind, projection version,
fixed rating/outcome/reasons, timestamps, and aggregate counts. It never stores
the raw installation marker, question or prompt, organization, church or person
identity, IP address, raw or hashed query text, attempted exact IDs for misses,
free text, logs, secrets, or Rock data.

The service rate-limits outcomes to 100 per opted-in installation per UTC day.
Every accepted outcome returns a stable `kbo_...` identifier.

## MCP Transport Aggregates

MCP transport health is measured separately from opt-in result usefulness.
Every direct or Code Mode request contributes only to a daily aggregate keyed
by projection, endpoint, protocol generation, operation category, fixed
cohort, HTTP status, normalized error, latency bucket, and response-size
bucket plus its measurement basis. No installation marker or hash is retained
in this transport table.

The default transport summary excludes evaluation and maintainer cohorts. It
can show adoption, negotiation failures, and tool-list frequency relative to
tool calls. It cannot observe a cache hit because a request that a client
avoids never reaches the service. Transport aggregates never contain tool
names, arguments, prompts, queries, headers, Origins, user agents, IP
addresses, bodies, logs, identities, or Rock data.

Use `response_size_coverage_rate` and `by_response_size_basis` before comparing
payload sizes. Unmeasured responses are explicit rather than treated as zero,
and successful streams are never consumed just to collect telemetry.

## Dashboard And Review Queue

`uvx rock-kb dashboard` and `kb_review_dashboard` expose a `field_validation`
section plus an `mcp_transport` section. Both default views exclude evaluation
and maintainer traffic. The field-validation funnel counts search, exact
retrieval success/failure, outcome, feedback, and report-issue events. Every
stage uses the v5 event stream beginning with service v0.16.0; older telemetry
is intentionally excluded from this funnel so its stages share one coverage
window. The broader telemetry summary retains historical aggregate continuity.

The service builds a bounded queue of at most 50 aggregate review items from:

- `partially_useful` and `not_useful` outcomes grouped by canonical public result;
- public topic categories that produce at least three zero-result searches;
- failed exact-lookup operation types.

The queue does not expose queries, unknown attempted IDs, installation hashes,
or private data. It directs maintainers to investigate; it does not
automatically change ranking, edit knowledge, or create GitHub issues.
