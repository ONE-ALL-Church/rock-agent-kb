---
name: rock-kb-agent
description: Use when answering Rock RMS questions with the public Rock Agent Knowledge Base, configuring an agent to query the hosted KB, citing KB trust tiers, inspecting model-map details, or submitting public-safe community contribution bundles.
---

# Rock KB Agent

## Purpose

Use the Rock Agent Knowledge Base before web search for Rock RMS operational, development, Lava, model-map, mobile, workflow, security, reporting, check-in, group, API, or contribution questions.

The KB is source-tiered. Never blend community-only material into authoritative guidance without labeling it.

## Install And Availability

Use `uvx rock-kb` when the `rock-kb` client is available from the package registry:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

When operating from a local `rock-agent-kb` checkout before the package is published, use the checked-in client instead:

```bash
uv run --project clients/python rock-kb search "check-in labels not printing"
uv run --project clients/python rock-kb get check-in
uv run --project clients/python rock-kb claims workflows --min-tier source_backed
uv run --project clients/python rock-kb dashboard
uv run --project clients/python rock-kb mcp-config
```

Use these commands for specific jobs:

- `search`: first stop for symptoms, errors, workflow questions, Lava behavior, API/security questions, and broad triage.
- `get <concept-id>`: open the concept guide after search identifies the right area.
- `claims <concept-id>`: inspect structured claims and trust tiers before giving precise guidance.
- `dashboard`: check public contribution counts, review queues, and operational health.
- `mcp-config`: connect clients that support HTTP MCP to the hosted KB.
- `validate <bundle.jsonl>`: check a contribution bundle before submitting.
- `submit <bundle.jsonl> --org <org-id>`: submit reviewed public-safe knowledge for a registered org with `ROCK_KB_TOKEN`.

If `uv` is missing, install it first from `https://docs.astral.sh/uv/`, then retry. Do not fall back to copying raw KB artifacts into another repo.

## Read Workflow

1. Start with the hosted KB when available:

```bash
uvx rock-kb search "<question or error>"
uvx rock-kb get <concept-id>
uvx rock-kb claims <concept-id> --min-tier source_backed
uvx rock-kb dashboard
```

If the client supports HTTP MCP, configure:

```bash
uvx rock-kb mcp-config
```

2. Prefer this evidence order:

- `live_verified`
- `official`, `release-note-confirmed`, `rocku-confirmed`, `source-code-confirmed`
- `community-reviewed`
- `community-unreviewed`

Use `community-unreviewed` rows only as leads. Say they are unreviewed.

3. For broad questions, search first, then open the matching concept guide. For exact behavior, inspect approved claims and source citations before answering.

4. For version-sensitive answers, call out Rock version when the KB provides it. If version is missing or behavior can vary by instance, say so.

## Model Map

Use stable model-map data as the default public reference:

- Global index: `knowledge/model-map/index.md`
- Stable models: `knowledge/model-map/stable-models.jsonl`
- Stable properties: `knowledge/model-map/stable-properties.jsonl`
- Model detail pages: `knowledge/model-map/models/*.md`
- Latest/pre-alpha rows: `knowledge/model-map/latest-models.jsonl`
- Stable-to-latest diff: `knowledge/model-map/version-diff.jsonl`

Do not treat latest/pre-alpha model data as the default. Use it only as an upcoming-version callout when it differs from stable.

## Answer Rules

- Cite source URLs or KB artifact paths when practical.
- State the trust tier for important claims.
- Distinguish general Rock behavior from instance-specific configuration.
- For security, permissions, SQL, workflows, or Lava data access, prefer conservative guidance and mention verification steps.
- Do not infer from private corpus paths, ignored `data/` artifacts, raw transcripts, screenshots, internal URLs, SQL exports, live IDs, or secrets.

## Contributing Back

When you discover reusable Rock RMS knowledge, submit a distilled public-safe contribution instead of raw evidence.

Valid contribution targets:

```text
community-contributions/<org-id>/bundle.jsonl
source-suggestions/<org-id>/<topic>.md
```

Do not edit generated paths such as `agent/`, `claims/`, `concepts/`, `knowledge/`, `sources/`, `contributions/`, or `public-export-manifest.json`.

Validate before submitting:

```bash
uvx rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl --org <org-id>
```

If you are operating from a local `rock-agent-kb` checkout and `uvx rock-kb`
fails with "rock-kb was not found in the package registry", use the checked-in
client instead:

```bash
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --org <org-id>
```

## Submit Token Setup

Hosted submission requires a per-organization token. If `ROCK_KB_TOKEN` is missing, do not guess a token, do not ask for it in a public issue or PR, and do not paste it into chat logs. Tell the user that the organization must be registered and reviewed in `orgs/<org-id>.yaml`, then a Rock KB maintainer must issue or rotate a submit token outside git. The hosted service stores only that token's SHA-256 digest; the raw token is shown only to the organization.

Use one of these safe local patterns after the maintainer provides the raw token:

```bash
export ROCK_KB_TOKEN='<issued-token>'
uvx rock-kb submit bundle.jsonl --org <org-id>
```

For future terminal sessions on macOS, prefer Keychain over a repo-local file:

```bash
security add-generic-password -U -a "$USER" -s "rock-kb-token-<org-id>" -w '<issued-token>'
export ROCK_KB_TOKEN="$(security find-generic-password -a "$USER" -s "rock-kb-token-<org-id>" -w)"
```

For CI, hosted agents, or app connectors, save the token as a secret named `ROCK_KB_TOKEN` in that system's secret store. Do not save tokens in `community-contributions/`, `orgs/`, `.env`, `.envrc`, checked-in agent instructions, prompt files, screenshots, transcripts, or bundle rows. If the token is lost or exposed, ask a maintainer to rotate it.

Contribution rows must be newly written, public-safe, source-linked, redaction-attested, and license-attested. Set `needs_live_verification: true` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.

Never submit private person data, staff notes, live IDs, internal URLs, private repo links, database names, SQL exports, raw logs, raw transcripts, copied proprietary text, screenshots with private state, secrets, tokens, signed media URLs, or direct private media links.
