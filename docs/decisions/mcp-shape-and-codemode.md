# MCP Shape And Code Mode

Status: adopted with stateless MCP `2026-07-28`, automatic 2025 compatibility,
and Code Mode opt-in and experimental.

## Decision

The hosted `/mcp` endpoint is the default agent interface. It exposes 35
task-oriented tools for direct search, exact retrieval, operations, feedback,
and reviewed intake from one canonical tool-definition registry. Tools return
structured content plus compatible JSON text and advertise read-only,
idempotent, destructive, and open-world hints.

The direct endpoint uses `@modelcontextprotocol/server` v2 through Cloudflare's
stateless `createMcpHandler`. Modern clients use `server/discover`; protocol
version, client identity, and client capabilities travel with every request.
The server keeps no protocol session. Durable projection, telemetry, feedback,
outcome, issue-report, and intake state stays in D1 or R2.

The same `/mcp` URL automatically serves ordinary 2025 clients through the
handler's stateless compatibility path. It supports `initialize`, `tools/list`,
and `tools/call`, but does not create a persistent session ID or provide
session GET, DELETE, replay, pushed sampling, roots, or elicitation. Rock KB
does not use those features.

The hosted `/mcp/code` endpoint is an explicit alternative. Cloudflare Code
Mode still returns an MCP SDK v1 server, so this route uses the explicit legacy
handler. It exposes one `code` tool over the 27 read-only Rock KB operations.
It is for dependent calls, branching, loops, or filtering that would otherwise
move large intermediate results through model context. Configure it only with:

```bash
uvx rock-kb mcp-config --mode code
```

The eight write-capable operations are deliberately omitted: feedback,
completed-task usefulness outcomes, Lava-context verification, KB issue
reports, test-round review submission, community knowledge submission, blind
retrieval-comparison starts, and comparison-review submission. Their consent,
redaction, authentication, and review boundaries remain on the direct
interface.

## Caching And Validation

- `server/discover` and `tools/list` advertise `ttlMs: 3600000` and
  `cacheScope: public`. Definitions are identical for all callers and change
  only with a reviewed service deployment.
- Tool results are not covered by this cache policy.
- Modern HTTP protocol, method, name, and body metadata must agree. Invalid
  combinations fail rather than being guessed or silently downgraded.
- Unsupported modern versions return the MCP unsupported-version error and the
  supported version list.
- The direct handler owns its CORS response. Browser Origins are restricted to
  the hosted service and local development hosts; Origin-less desktop and
  server-to-server clients remain supported.
- Authentication, contribution tokens, telemetry consent, and write-tool
  validation are evaluated independently on every request.

## Transport Measurement

Direct and Code Mode requests update a separate
`mcp_transport_events_v1` daily aggregate after the response is produced. The
bounded dimensions are projection, endpoint, protocol generation, operation
category, fixed cohort, HTTP status, normalized error code, latency bucket,
response-size bucket, measurement basis, and count.

The public transport summary excludes evaluation and maintainer traffic by
default and keeps those scopes available separately. It can measure 2026 versus
2025 adoption, negotiation failure rate, response-size distribution, handler
latency distribution, and discovery/tool-list frequency relative to tool
calls. It cannot directly observe cache hits.

The table deliberately has no installation hash and no request-level record.
It excludes tool names, arguments, queries, headers, Origins, user agents, IP
addresses, bodies, logs, identities, and Rock data. Identical dimensions
upsert one row per day. This keeps storage bounded by bucket combinations;
row-write volume, not storage, is the relevant D1 cost signal.

Response-size measurement cannot change transport behavior. `Content-Length`
is exact when present, handler-generated errors are bounded and buffered,
direct tool payloads and direct tool-list metadata are estimated from values
already in memory, and all other responses are marked `unmeasured`. Successful
response streams are never cloned or consumed for telemetry.

## Alternatives

| Shape | Decision | Reason |
|---|---|---|
| Direct typed tools | Default | The catalog is bounded, tool intent is clear, and exact technical retrieval is the normal workload. |
| Stateless MCP 2026 only | Not yet | Client adoption will lag the new protocol; the official stateless compatibility path preserves ordinary 2025 clients without adding server sessions. |
| One Code Mode tool | Opt-in | Useful for multi-step read-only composition without making every client execute code. |
| Search plus execute | Not adopted | Intended for very large or changing API catalogs; 35 stable tools do not justify another discovery round trip. |
| Resources only | Not adopted | Rock questions need parameterized search and exact lookups, not only static file reads. |
| OKF download | Secondary | Best for offline, pinned, bulk, archival, or local-index workloads rather than live questions. |

## Safety And Compatibility

- Direct MCP and Code Mode use their required SDK generations side by side.
- Code Mode dependencies are exactly pinned because the Cloudflare feature is
  experimental.
- Generated Code Mode programs run in an isolated Worker Loader sandbox. They
  cannot restore an omitted write tool or bypass authorization.
- Direct MCP keeps JSON text alongside `structuredContent` for older consumers.
- A Code Mode failure must not impair `/mcp`, REST, CLI, or OKF access.
- Protocol migration tests use the official SDK v2 client and raw wire checks
  for discovery, cache hints, header mismatch, unsupported versions, Origin
  policy, no session ID, 2025 compatibility, and Code Mode isolation.

## Validation Snapshot

A 100-iteration warm local Miniflare comparison against the prior Worker found
that direct `tools/list` median handler time increased from about `1.0 ms` to
`1.4 ms`, while its response decreased from `29,976` to `16,921` bytes. The
prior `initialize` plus list sequence took about `2.0 ms` median; modern
discovery plus list took about `2.3-2.5 ms`. The 2025 compatibility list path
remained about `0.9 ms` median.

This is a transport-only local benchmark, not a WAN or retrieval-quality
result. The modern path accepts a small validation cost, cuts the tool-list
payload by roughly 44 percent, and allows clients to avoid repeated list
transfers through the one-hour cache hint.

## Promotion Gate

Code Mode should remain opt-in until external client testing shows that it
reduces tool calls or model-context use for composed questions without harming
exact lookup accuracy, latency, reliability, or safety. No raw query, client
identity, church identity, IP address, or generated program should be retained
to evaluate that gate; bounded operation/error and cohort counts are enough.

Stateless MCP is the direct endpoint's production transport, not a retrieval
experiment. Its success criteria are protocol compliance, compatibility,
availability, and connection overhead. It is not expected to improve ranking
quality.

## References

- <https://modelcontextprotocol.io/specification/2026-07-28>
- <https://modelcontextprotocol.io/seps/2575-stateless-mcp>
- <https://modelcontextprotocol.io/seps/2549-TTL-for-list-results>
- <https://developers.cloudflare.com/agents/model-context-protocol/apis/handler-api/>
- <https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-openapi-mcp-server/>
