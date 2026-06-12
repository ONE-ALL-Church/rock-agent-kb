# Agent Serving Runbook

`kb serve` runs a read-only MCP stdio server over public KB artifacts. It does not expose private review, media, normalized, raw-manifest, or index internals directly.

Install the optional serve dependency:

```bash
uv sync --extra serve
```

Register the server with an MCP client:

```json
{ "mcpServers": { "rock-kb": { "command": "uv", "args": ["run", "--directory", "/path/to/Rock General Knowledge Base", "kb", "serve"] } } }
```

Available tools:

- `kb_search`: full-text search across public KB artifacts. Start here for most Rock questions.
- `kb_manifest`: public artifact manifest and entrypoints.
- `kb_list_concepts`: available concept ids, titles, guide paths, and dependency metadata.
- `kb_get_concept`: quickstart, answers, task cards, and release caveats for one concept.
- `kb_get_claims`: approved public claims for a concept, optionally filtered by claim tier.

If the optional dependency is missing, `kb serve` exits with:

```text
kb serve requires the serve extra: uv sync --extra serve
```
