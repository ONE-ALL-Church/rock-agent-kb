# Structured Issue Reporting

Use issue reporting when the Rock KB itself malfunctions. It is separate from
knowledge-quality feedback and community contributions.

| Situation | Use |
|---|---|
| A result is incorrect, outdated, missing, or routed poorly | `kb_feedback` or `rock-kb feedback` |
| The service, MCP tool, CLI, schema, authentication, or retrieval path fails | `kb_report_issue` or `rock-kb report-issue` |
| New reusable Rock knowledge should be added | `kb_submit` or the contribution workflow |

## Agent Use

Report only a short generic description. Never include a query, prompt, raw
request or response, stack trace, log line, secret, private path, person data,
or private Rock identifier. The service rejects unknown fields and descriptions
that look unsafe. The caller must explicitly attest that redaction is complete.

CLI example:

```bash
uvx rock-kb report-issue \
  --failure-type retrieval \
  --operation search \
  --error-code search_unavailable \
  --http-status 503 \
  --description "Search returned a temporary service failure." \
  --redaction-attested
```

Add `--result-id '<public-result-id>'` only when the failure concerns a public
Rock KB result ID. Do not use it for a Rock entity ID or another private value.

MCP clients can call `kb_report_issue` with the same fields. Supported
`failure_type` values are `service`, `mcp`, `cli`, `schema`, `authentication`,
and `retrieval`.

The service captures the active projection version and client class. The
published CLI also sends its package version. It returns a stable `report_id`
that agents can cite in later maintainer conversations.

## Deduplication And Review

The service fingerprints the structured failure type, operation, projection,
public result ID, HTTP status, and error code. Repeated reports increment one
row's `occurrence_count`; changing the prose does not create a duplicate.

`GET /operations/dashboard`, `rock-kb dashboard`, and `kb_review_dashboard`
show issue counts and the bounded redacted description. New reports are always
`pending_review`. Reporting never creates a GitHub issue automatically. A
maintainer must review the report, confirm it is actionable and public-safe,
and deliberately create or link a GitHub issue in a later reviewed workflow.

## Abuse And Safety Controls

- Request bodies are limited to 4 KiB; descriptions are limited to 280 bytes.
- Failure types are enumerated; operations and error codes are bounded
  structured identifiers; unknown fields are rejected.
- A Cloudflare rate-limit binding limits callers, and D1 applies global and
  same-fingerprint burst limits.
- The application does not retain caller IP addresses in issue-report tables.
- Reports store the first and most recent client class/version and timestamps,
  but not raw logs or queries.
- The dashboard exposes only reports that passed the public-safety validator.

`kb_feedback` remains deliberately free of prose. Do not expand it to carry
malfunction reports.
