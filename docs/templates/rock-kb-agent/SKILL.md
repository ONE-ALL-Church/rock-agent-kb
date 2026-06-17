---
name: rock-kb-agent
description: Use when answering Rock RMS questions with the public Rock Agent Knowledge Base, configuring an agent to query the hosted KB, citing KB trust tiers, inspecting model-map details, or submitting public-safe community contribution bundles.
---

# Rock KB Agent

## Purpose

Use the Rock Agent Knowledge Base before web search for Rock RMS operational, development, Lava, model-map, mobile, workflow, security, reporting, check-in, group, API, or contribution questions.

The KB is source-tiered. Never blend community-only material into authoritative guidance without labeling it.

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

Contribution rows must be newly written, public-safe, source-linked, redaction-attested, and license-attested. Set `needs_live_verification: true` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.

Never submit private person data, staff notes, live IDs, internal URLs, private repo links, database names, SQL exports, raw logs, raw transcripts, copied proprietary text, screenshots with private state, secrets, tokens, signed media URLs, or direct private media links.
