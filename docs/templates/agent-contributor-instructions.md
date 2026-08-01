# Rock KB Agent Contributor Instructions

Use these instructions for an agent operating on behalf of a registered Rock KB
organization.

## Read First

Before answering a Rock RMS operational question, query the hosted Rock KB
through either the CLI or MCP. They expose the same hosted projection; choose
MCP for native typed tools or the CLI for terminal and scripted access:

```bash
uvx rock-kb search "<question or error>"
uvx rock-kb get <concept-id>
uvx rock-kb claims <concept-id> --min-claim-tier source_backed
```

When your client supports HTTP MCP, add the hosted MCP endpoint:

```bash
uvx rock-kb mcp-config
```

Do not download an OKF release merely to answer an ordinary online question.
Use OKF only for offline operation, a pinned snapshot, bulk/local indexing, or
cross-system interchange.

Prefer `official`, `release-note-confirmed`, `rocku-confirmed`,
`source-code-confirmed`, and `community-reviewed` results. Treat
`community-unreviewed` rows as useful leads, not authoritative guidance, and
label that tier in answers.

## Ask Before Providing Feedback

After the first completed KB-assisted task, do not silently enable telemetry or
submit feedback. If no current preference exists in private user-level memory,
explain that field validation may retain only a one-way hash of a random local
    installation marker, a fixed cohort, public result IDs and kinds, current KB
    projection and client version, fixed quality rating or usefulness outcome,
    fixed reason codes, timestamps, and aggregate counts. A blind retrieval
    comparison additionally retains a fixed category, paired public result IDs,
    projection versions, randomized A/B assignment, and fixed preference/reason
    codes; its pending session expires after 30 minutes. It does not retain the
question, prompt, organization, church or person identity, IP address, free
text, logs, secrets, or private Rock data. Ask the human to choose:

- `Allow automatically`: enable the anonymous marker and submit `kb_feedback`
  or `kb_outcome` only when an exact result can be evaluated confidently.
- `Ask each time`: request confirmation before each feedback or outcome event.
- `Do not send`: keep telemetry disabled, submit nothing, and do not ask again
  unless the human reopens the decision.

Ask separately whether the human permits remembering that choice. Persist any
decision only when the human explicitly agrees and the host provides private
persistent memory. Use consent notice version `3`; version `2` does not cover
comparison retention and is ignored by the updated client. Never put consent in a
repository, KB payload, project artifact, contribution bundle, or church data
store. Without private persistence or permission to use it, keep the choice
session-scoped.

Standing permission applies only to exact-result `kb_feedback` and completed-task
`kb_outcome`. Submit at most one of each per result per task and never repeat an
event to inflate a count. If usefulness is uncertain, submit nothing. Use
`uvx rock-kb telemetry enable --cohort community --consent-attested`, then rerun
`uvx rock-kb install-agent` and restart the host. Ask separately before
`kb_compare_retrieval` or `rock-kb compare` unless current private memory
explicitly permits comparisons. Also ask before every redaction-attested
`kb_report_issue`, reviewed test-round submission, public
contribution, or PR. To revoke, disable telemetry, rerun the installer, and
restart. Ask again if the consent notice or retained fields change.

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

## Lava Context Roots

For Lava questions, identify the rendering surface before recommending syntax or
model properties. Use exact grouped context retrieval first:

```bash
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-person-dynamic-text
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text --root CheckoutDateTime
```

Use search when the exact surface ID is unknown:

```bash
uvx rock-kb search "PersonAttendance Check-In Label Designer Lava roots"
uvx rock-kb search "communication recipient merge values"
uvx rock-kb search "workflow action Lava merge fields"
```

The grouped result identifies direct and inherited roots, conditions,
nullability, source version, source commit, completeness, and Model Map links.
Then use the Model Map for properties and the Lava capability reference for
filters, commands, and safety notes. `complete_for_source_snapshot` means the
explicit source contract was captured at the pinned commit, not that every value
is populated in every request. Rows marked `needs_live_verification: true` still
require checking the specific page, block, communication, workflow, label, or
instance configuration.

## Submit Reusable Public Knowledge

When you discover a reusable Rock RMS insight, submit a distilled contribution
row instead of raw evidence. The row must be newly written and public-safe.

```bash
uvx rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx rock-kb auth-check --org <org-id>
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl --dry-run
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl
```

If you are working from a local `rock-agent-kb` checkout and need unreleased
client changes, use the checked-in client:

```bash
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb auth-check --org <org-id>
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --dry-run
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl
```

To test an unreleased public branch without a local checkout, use the Git-backed
`uvx --from` form:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb validate bundle.jsonl
```

Hosted submission requires a per-organization token. If `ROCK_KB_TOKEN` is
missing, ask the user to have a Rock KB maintainer issue a token for the
reviewed `orgs/<org-id>.yaml` registration. Do not request the token in a public
issue, PR, or chat log. If a token is provided, use it only through an
environment variable or a secret store:

```bash
export ROCK_KB_TOKEN='<issued-token>'
uvx rock-kb auth-check --org <org-id>
uvx rock-kb submit bundle.jsonl --dry-run
uvx rock-kb submit bundle.jsonl
```

For repeat use on macOS, store it in Keychain and load it into the environment
when needed:

```bash
security add-generic-password -U -a "$USER" -s "rock-kb-token-<org-id>" -w '<issued-token>'
export ROCK_KB_TOKEN="$(security find-generic-password -a "$USER" -s "rock-kb-token-<org-id>" -w)"
```

For CI, hosted agents, or app connectors, save it as a secret named
`ROCK_KB_TOKEN`, or mount it as a secret file and set `ROCK_KB_TOKEN_FILE`.
Never save submit tokens in repo files, bundle rows, screenshots, transcripts,
or generated artifacts. Ask a maintainer to rotate the token if it is lost or
exposed.

`rock-kb submit` infers `--org` from the bundle when all rows use the same
`org_id`. Use `--org <org-id>` only when submitting mixed or unusual test
bundles.

Use `community-contributions/example-org/bundle.example.jsonl` as the row-shape
reference. Set `needs_live_verification: true` when behavior depends on local
configuration, plugins, custom code, or a specific Rock version.

Before submitting, verify that every `concept_ids` value is an existing KB
concept id. Do not invent natural-language ids. Use one of these checks:

```bash
uvx rock-kb concepts
uvx rock-kb validate bundle.jsonl
```

From a local checkout, `concepts/registry.yaml` is the source of truth. For
example, registration-related rows should use `event-registration`, not
`registrations`; giving and finance rows should use `giving-finance`, not
`finance`.

## Never Submit

- Private person data, staff notes, live IDs, or screenshots with private state.
- Internal URLs, private repo links, database names, SQL exports, or raw logs.
- Raw transcripts, copied proprietary docs, or copied source text.
- Secrets, tokens, signed media URLs, or direct private media links.

If a useful finding depends on private evidence, rewrite it as a generalized
public-safe pattern and cite public source URLs where possible.
