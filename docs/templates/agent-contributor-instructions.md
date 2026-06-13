# Rock KB Agent Contributor Instructions

Use these instructions for an agent operating on behalf of a registered Rock KB
organization.

## Read First

Before answering a Rock RMS operational question, query the hosted Rock KB:

```bash
uvx rock-kb search "<question or error>"
uvx rock-kb get <concept-id>
uvx rock-kb claims <concept-id> --min-tier source_backed
```

When your client supports HTTP MCP, add the hosted MCP endpoint:

```bash
uvx rock-kb mcp-config
```

Prefer `official`, `release-note-confirmed`, `rocku-confirmed`,
`source-code-confirmed`, and `community-reviewed` results. Treat
`community-unreviewed` rows as useful leads, not authoritative guidance, and
label that tier in answers.

## Submit Reusable Public Knowledge

When you discover a reusable Rock RMS insight, submit a distilled contribution
row instead of raw evidence. The row must be newly written and public-safe.

```bash
uvx rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl --org <org-id>
```

Use `community-contributions/example-org/bundle.example.jsonl` as the row-shape
reference. Set `needs_live_verification: true` when behavior depends on local
configuration, plugins, custom code, or a specific Rock version.

## Never Submit

- Private person data, staff notes, live IDs, or screenshots with private state.
- Internal URLs, private repo links, database names, SQL exports, or raw logs.
- Raw transcripts, copied proprietary docs, or copied source text.
- Secrets, tokens, signed media URLs, or direct private media links.

If a useful finding depends on private evidence, rewrite it as a generalized
public-safe pattern and cite public source URLs where possible.
