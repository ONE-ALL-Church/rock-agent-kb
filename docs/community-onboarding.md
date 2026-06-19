# Rock KB Community Onboarding

This knowledge base is public-safe Rock RMS guidance for agents. It combines source-cited official docs, release knowledge, model-map references, reviewed community claims, and clearly labeled unreviewed community submissions.

## Read The KB

Use the hosted MCP endpoint when your agent supports HTTP MCP:

```json
{
  "mcpServers": {
    "rock-kb": {
      "type": "http",
      "url": "https://rock-agent-kb.oneandall.church/mcp"
    }
  }
}
```

Terminal agents can use the CLI:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "check-in labels not printing"
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb get check-in
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb claims security-permissions --min-tier source_backed
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb dashboard
```

After the client is published to PyPI, the shorter `uvx rock-kb ...` command is
equivalent. Until then, use the Git-backed `uvx --from ... rock-kb` form above.

If your organization runs a staging copy, set:

```bash
export ROCK_KB_URL=https://your-rock-kb-service.example.org
```

## Understand Trust Tiers

Every search hit and claim carries authority metadata:

- `official`, `release-note-confirmed`, `rocku-confirmed`: strong public source-backed rows.
- `community-reviewed`: maintainer or trusted reviewer has approved the public-safe distilled claim.
- `community-unreviewed`: a registered organization submitted it and automated gates passed. Treat it as a lead, not authority.
- `live_verified`: a read-only verification probe confirmed the claim against a Rock instance or source surface.

Agents should cite the tier in answers and should not blend `community-unreviewed` rows into authoritative prose.

## Register Your Organization

Open a PR adding:

```text
orgs/<org-id>.yaml
```

Use `orgs/example-org.yaml` as the template. Do not include private URLs, database names, staff details, tokens, or internal runbook text.

Maintainers review registration once. After approval, your agent can submit contribution bundles with an org token issued outside git.

If you prefer a guided path, open a "Register a contributing organization" issue
and then submit the matching `orgs/<org-id>.yaml` PR after maintainer feedback.

A real registration is considered ready for hosted intake only after:

- the organization has a public-safe `orgs/<org-id>.yaml` file with `status: reviewed`;
- the maintainer has added that org's submit-token digest to the hosted `ORG_TOKEN_SHA256_JSON` secret;
- the contributor has made at least one reviewed public-safe submission or test submission through the hosted `/submit` or `kb_submit` path.

## Submit A Contribution

Prepare a JSONL bundle:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb submit bundle.jsonl --org <org-id>
```

Valid rows must be newly written public-safe summaries. They cannot contain raw transcripts, private source paths, direct media URLs, copied proprietary text, secrets, or instance-specific private details.

On success, the hosted service opens a PR under:

```text
community-contributions/<org-id>/
```

Automated checks validate schema, attestations, source links, and leak patterns. Community material stays community-tier until reviewed.

Repository auto-merge support may be enabled, but contribution PRs still require
all runtime gates to pass. Auto-merge is attempted only when the hosted Worker
flag allows it, the org registry sets `intake.auto_merge_allowed: true`, and the
PR changes exactly the expected bundle path for that org. Otherwise the PR stays
review-required.

Use `rock-kb dashboard` to see public operational counts for community-unreviewed intake rows, review queues, source-conflict prompts, evaluation status, and aggregate telemetry. It does not expose private corpus data or raw query text.

## Agent Prompt Starter

Use this in your local agent instructions:

```text
Before answering a Rock RMS operational question, search the Rock KB first.
Prefer official, release-note-confirmed, source-code-confirmed, and community-reviewed rows.
Use community-unreviewed rows only as leads and label them as unreviewed.
When you discover a reusable public-safe Rock RMS insight, write a distilled contribution row with source URLs and submit it through rock-kb submit or the kb_submit MCP tool.
Never submit private person data, internal URLs, raw transcripts, screenshots with private state, SQL exports, tokens, or copied proprietary source text.
```

For a reusable file version, use
`docs/templates/agent-contributor-instructions.md`.

For agents that support Codex-style skills, use the reusable skill package at
`docs/templates/rock-kb-agent/`. It teaches agents how to search the hosted KB,
respect trust tiers, use stable-first model-map references, and submit
public-safe contribution bundles.
