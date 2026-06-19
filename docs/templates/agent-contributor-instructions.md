# Rock KB Agent Contributor Instructions

Use these instructions for an agent operating on behalf of a registered Rock KB
organization.

## Read First

Before answering a Rock RMS operational question, query the hosted Rock KB:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "<question or error>"
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb get <concept-id>
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb claims <concept-id> --min-tier source_backed
```

When your client supports HTTP MCP, add the hosted MCP endpoint:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb mcp-config
```

After the client is published to PyPI, the shorter `uvx rock-kb ...` form is
equivalent. Until then, use the Git-backed `uvx --from ... rock-kb` command
above or the local-checkout fallback below.

Prefer `official`, `release-note-confirmed`, `rocku-confirmed`,
`source-code-confirmed`, and `community-reviewed` results. Treat
`community-unreviewed` rows as useful leads, not authoritative guidance, and
label that tier in answers.

## Rockumentation API Full Text

For public Rockumentation pages, the hosted page may not contain the richest
article payload. Public `/documentation/<slug>` and `/developer/<slug>` article
pages can be inspected by POSTing to Rock's block-action API:

```text
https://community.rockrms.com/api/v2/BlockActions/6d657cde-b3b9-4acd-9cab-928234ab0fae/a6f974bc-6d59-46e7-a832-37525a343706/RefreshObsidianBlockInitialization?slug=<url-encoded-slug>
```

The `/documentation` home page uses:

```text
https://community.rockrms.com/api/v2/BlockActions/85750a25-e864-4938-bde7-09cd32146a18/d30514c6-b51f-40b4-aa77-4108b35b7f13/RefreshObsidianBlockInitialization
```

The JSON response's `initialContent` contains the article HTML, usually under
`article.rockumentation-article[data-main-article="true"]`, and
`configurationValues` contains title, version, table-of-contents, and slug
metadata. Use this only for public documentation/developer/mobile docs and cite
the public article URL, not the API URL. Do not use this API as a shortcut for
private Rock instance content or secrets.

## Submit Reusable Public Knowledge

When you discover a reusable Rock RMS insight, submit a distilled contribution
row instead of raw evidence. The row must be newly written and public-safe.

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb submit bundle.jsonl --org <org-id>
```

If you are working from a local `rock-agent-kb` checkout and `uvx rock-kb`
reports that the package was not found, use the checked-in client:

```bash
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --org <org-id>
```

Hosted submission requires a per-organization token. If `ROCK_KB_TOKEN` is
missing, ask the user to have a Rock KB maintainer issue a token for the
reviewed `orgs/<org-id>.yaml` registration. Do not request the token in a public
issue, PR, or chat log. If a token is provided, use it only through an
environment variable or a secret store:

```bash
export ROCK_KB_TOKEN='<issued-token>'
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb submit bundle.jsonl --org <org-id>
```

For repeat use on macOS, store it in Keychain and load it into the environment
when needed:

```bash
security add-generic-password -U -a "$USER" -s "rock-kb-token-<org-id>" -w '<issued-token>'
export ROCK_KB_TOKEN="$(security find-generic-password -a "$USER" -s "rock-kb-token-<org-id>" -w)"
```

For CI, hosted agents, or app connectors, save it as a secret named
`ROCK_KB_TOKEN`. Never save submit tokens in repo files, bundle rows,
screenshots, transcripts, or generated artifacts. Ask a maintainer to rotate the
token if it is lost or exposed.

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
