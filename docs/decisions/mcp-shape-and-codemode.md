# MCP Shape And Code Mode

Status: adopted with Code Mode opt-in and experimental.

## Decision

The hosted `/mcp` endpoint remains the default agent interface. It exposes 28
task-oriented tools for direct search, exact retrieval, operations, feedback,
and reviewed intake. Tools return MCP structured content plus compatible JSON
text and advertise read-only, idempotent, destructive, and open-world hints.

The hosted `/mcp/code` endpoint is an explicit alternative. It exposes one
Cloudflare Code Mode `code` tool over the 24 read-only Rock KB tools. It is for
dependent calls, branching, loops, or filtering that would otherwise move
large intermediate results through model context. Configure it only with:

```bash
uvx rock-kb mcp-config --mode code
```

The four write-capable operations are deliberately omitted: feedback, KB issue
reports, test-round review submission, and community knowledge submission.
Their consent, redaction, authentication, and review boundaries remain on the
direct interface.

## Alternatives

| Shape | Decision | Reason |
|---|---|---|
| Direct typed tools | Default | The catalog is bounded, tool intent is clear, and exact technical retrieval is the normal workload. |
| One Code Mode tool | Opt-in | Useful for multi-step read-only composition without making every client execute code. |
| Search plus execute | Not adopted | Intended for very large or changing API catalogs; 28 stable tools do not justify another discovery round trip. |
| Resources only | Not adopted | Rock questions need parameterized search and exact lookups, not only static file reads. |
| OKF download | Secondary | Best for offline, pinned, bulk, archival, or local-index workloads rather than live questions. |

## Safety And Compatibility

- Code Mode dependencies are exactly pinned because the Cloudflare feature is
  experimental.
- Generated code runs in an isolated Worker Loader sandbox. It cannot restore
  an omitted write tool or bypass the upstream service's authorization.
- Direct MCP remains backward compatible through JSON text content while newer
  clients can consume `structuredContent`.
- The service accepts the supported stable MCP protocol versions and selects
  the current stable version when a client requests an unknown version.
- A Code Mode failure must not impair `/mcp`, REST, CLI, or OKF access.

## Promotion Gate

Code Mode should remain opt-in until external client testing shows that it
reduces tool calls or model-context use for composed questions without harming
exact lookup accuracy, latency, reliability, or safety. No raw query, client
identity, church identity, IP address, or generated program should be retained
to evaluate that gate; bounded operation/error and cohort counts are enough.

Cloudflare documents Code Mode as experimental and distinguishes the single
code-tool pattern from search-plus-execute for very large catalogs. The MCP
tools contract supplies structured results and behavioral annotations; those
are useful on the direct endpoint whether or not Code Mode is enabled.

## References

- <https://developers.cloudflare.com/agents/tools/codemode/>
- <https://developers.cloudflare.com/agents/model-context-protocol/codemode/>
- <https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-mcp-server/>
- <https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-openapi-mcp-server/>
- <https://modelcontextprotocol.io/specification/2025-11-25/server/tools>
