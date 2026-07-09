---
name: rock-kb-agent
description: Use when answering Rock RMS questions with the public Rock Agent Knowledge Base, configuring an agent to query the hosted KB, citing KB trust tiers, inspecting model-map details, or submitting public-safe community contribution bundles.
---

# Rock KB Agent

## Purpose

Use the Rock Agent Knowledge Base before web search for Rock RMS operational, development, Lava, model-map, mobile, workflow, security, reporting, check-in, group, API, or contribution questions.

The KB is source-tiered. Never blend community-only material into authoritative guidance without labeling it.

## Capability Map

The KB can help agents do more than plain text search:

- Search public Rock RMS knowledge with authority and claim tiers.
- Open task-oriented concept guides and quickstarts.
- Inspect structured claims and source citations by concept.
- List valid concept IDs before writing or submitting contribution rows.
- Use the manifest to discover agent entrypoints and generated artifacts.
- Inspect public operations counts through the dashboard.
- List stable Rock Model Map models and get exact model digests.
- Inspect model fields, required fields, relationships, methods, version diffs,
  and one property at a time.
- Find Lava context roots for specific rendering surfaces before guessing which
  merge fields exist.
- Use Rockumentation API metadata and branch paths as routing signals.
- Validate and submit public-safe community contribution bundles.
- Connect through hosted HTTP MCP when the current agent client supports tools.

## Install And Availability

Use the hosted MCP endpoint when the current agent client supports HTTP MCP.
The CLI can install this skill and the hosted MCP entry for detected Codex,
Claude Code, Cursor, or OpenCode hosts:

```bash
uvx rock-kb install-agent --dry-run
uvx rock-kb install-agent
```

Restart the host after installation. Use `--agent <name>` to select a host or
`--scope project --project-dir <path>` for a project-local install. The
installer backs up existing files before writing. For manual configuration,
print the MCP block:

```bash
uvx rock-kb mcp-config
```

Use the published `rock-kb` client from PyPI for terminal access. The examples
use `uvx`, which comes from the `uv` Python toolchain and runs the package
without a manual install. If `uvx --version` fails, install `uv` first from
`https://docs.astral.sh/uv/` or with `brew install uv` on macOS.

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb result '<result-id>'
uvx rock-kb claim '<claim-id>'
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

For repeated use on a server or persistent agent host, install the CLI once:

```bash
uv tool install rock-kb
rock-kb search "check-in labels not printing"
rock-kb mcp-config
```

To test unreleased client changes from GitHub instead of PyPI, use:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "check-in labels not printing"
```

When operating from a local `rock-agent-kb` checkout and testing local client
changes, use the checked-in client instead:

```bash
uv run --project clients/python rock-kb search "check-in labels not printing"
uv run --project clients/python rock-kb get check-in
uv run --project clients/python rock-kb claims workflows --min-tier source_backed
uv run --project clients/python rock-kb model-map list
uv run --project clients/python rock-kb model group
uv run --project clients/python rock-kb dashboard
uv run --project clients/python rock-kb mcp-config
```

Use these commands for specific jobs:

- `search`: first stop for symptoms, errors, workflow questions, Lava behavior, API/security questions, and broad triage.
- `result <result-id>`: expand one compact search hit into its full body and structured payload.
- `claim <claim-id>`: fetch one exact approved claim with all concept routes.
- `get <concept-id>`: open the concept guide after search identifies the right area.
- `claims <concept-id>`: inspect structured claims and trust tiers before giving precise guidance.
- `model-map list`: list stable Rock Model Map models when discovering the exact slug to inspect.
- `model <slug-or-name>`: fetch an exact stable Model Map digest for a known model, such as `group` or `Group Member`.
- `manifest`: inspect public agent entrypoints and generated artifact paths.
- `concepts`: list valid concept IDs and their guide paths.
- `dashboard`: check public contribution counts, review queues, and operational health.
- `mcp-config`: connect clients that support HTTP MCP to the hosted KB.
- `validate <bundle.jsonl>`: check a contribution bundle before submitting.
- `auth-check --org <org-id>`: verify hosted submission auth before sending a bundle.
- `submit <bundle.jsonl> [--dry-run] [--org <org-id>]`: submit reviewed public-safe knowledge for a registered org with `ROCK_KB_TOKEN`; `--org` is inferred when bundle rows share one `org_id`.

Do not fall back to copying raw KB artifacts into another repo.

## MCP Tool Map

When connected through hosted HTTP MCP, use the same retrieval pattern with MCP
tools instead of shell commands:

- `kb_search`: start here for symptoms, errors, broad Rock questions, and Lava
  context queries. Results are compact and include stable IDs, snippets, trust
  tiers, source URLs, scores, and ranking signals.
- `kb_get_result`: expand one `kb_search` result ID into its full body and
  structured payload.
- `kb_get_claim`: fetch one approved claim directly by `claim_id`, including
  all concept routes and result IDs.
- `kb_manifest`: discover public agent entrypoints such as model-map digests,
  Lava contexts, source authority rules, live checklists, and troubleshooting
  trees.
- `kb_list_concepts`: list valid concept IDs before using `kb_get_concept`,
  `kb_get_claims`, or writing contribution rows.
- `kb_get_concept`: open one concept package with guide, quickstart, task cards,
  caveats, answers, and claims.
- `kb_get_claims`: inspect structured claims and trust tiers for one concept.
- `kb_list_models`: list stable Model Map models with slugs, categories,
  versions, and property/method counts.
- `kb_get_model`: fetch an exact stable Model Map digest by slug or model name,
  optionally filtered by fields or one property.
- `kb_review_dashboard`: check public review queues, conflicts, community
  intake, hosted evaluation, and telemetry counts.
- `kb_submit`: validate and submit a contribution bundle for a registered org.

Use MCP for agent-native tool access when available. Use the CLI for terminal
agents, local testing, and environments without HTTP MCP support.

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

3. For broad questions, search first, expand only the relevant result IDs, then
open the matching concept guide. For exact behavior, inspect approved claims
and source citations before answering. Avoid `search --full` or MCP `full: true`
unless a compatibility workflow genuinely requires every result body.

4. For version-sensitive answers, call out Rock version when the KB provides it. If version is missing or behavior can vary by instance, say so.

Official Rock videos and Community Blog articles can establish product context,
demonstrations, rollout experience, and stated direction. They are not by
themselves proof that a demonstrated or exploratory feature is available in a
particular release. For implementation answers, confirm against current written
documentation, release notes, public source code, and live configuration.

## Manifest And Entry Points

Use `uvx rock-kb manifest` or `kb_manifest` when an agent needs to understand
what the KB can expose. Important manifest entrypoints include:

- `answer_pack`: concise answer rows for concept-level synthesis.
- `approved_claims` and `distilled_claims`: structured claims with trust tiers.
- `concepts`, `tasks`, `release_caveats`, and `troubleshooting`: concept guide,
  task, caveat, and troubleshooting surfaces.
- `source_authority_rules`, `source_summaries`, and `section_status`: source
  quality, authority, and staleness signals.
- `live_checklists` and `live_probe_recipes`: read-only verification guidance
  for agents that must inspect a live Rock instance.
- `model_map`, `model_map_digests`, `model_map_properties`,
  `model_map_methods`, and `model_map_version_diff`: model lookup and version
  comparison surfaces.
- `lava_contexts`, `lava_context_directory`, `lava_capabilities`,
  `lava_safety_matrix`, and `lava_agent_usage_examples`: Lava-specific context,
  syntax, safety, and usage surfaces.

Prefer the higher-level CLI or MCP tools first. Use manifest entrypoints when
the task needs a specific generated artifact or when direct tool output is not
specific enough.

## Rockumentation API Full Text

Rock's public Rockumentation pages can expose richer article content through the
same public block-action API used by the KB ingester. Use this only to inspect
public documentation, developer docs, and mobile docs; do not use it for private
Rock instances or authenticated content.

For `/documentation/<slug>` and `/developer/<slug>` article pages, POST to:

```text
https://community.rockrms.com/api/v2/BlockActions/6d657cde-b3b9-4acd-9cab-928234ab0fae/a6f974bc-6d59-46e7-a832-37525a343706/RefreshObsidianBlockInitialization?slug=<url-encoded-slug>
```

For the `/documentation` home page, POST to:

```text
https://community.rockrms.com/api/v2/BlockActions/85750a25-e864-4938-bde7-09cd32146a18/d30514c6-b51f-40b4-aa77-4108b35b7f13/RefreshObsidianBlockInitialization
```

The response is JSON. Article full text is in `initialContent`, usually inside
`article.rockumentation-article[data-main-article="true"]`. Metadata such as
title, current version, version links, table of contents, and slug is in
`configurationValues`; article IDs may appear as `data-article-id` attributes.
If operating inside this repo, prefer the existing helpers in
`src/rock_kb/community.py` instead of writing one-off parsing code.

Do not assume every Community page uses this API. Lava reference pages currently
work better through the static/parser source path unless the API is re-probed and
shown to return real article content.

## Rockumentation Branch Routing

The KB may expose Rockumentation routing metadata on public source summaries:
`documentation_path`, `documentation_branch`, and `documentation_branches`.
Use these fields as retrieval clues when an answer needs the right official doc
area. Examples include `documentation/engagement/prayer`,
`documentation/supporting-rock/hosting`, and `developer/obsidian`.

Do not treat Rock's documentation navigation as the same thing as the KB concept
taxonomy. Concepts are task-oriented for agents; official branches are structured
source signals that help confirm why a source belongs in a concept or subguide.

## Model Map

Use stable model-map data as the default public reference:

For known models, use exact lookup before generic search:

```bash
uvx rock-kb model-map list
uvx rock-kb model group
uvx rock-kb model group --fields identity,required,relationships,diffs
uvx rock-kb model group --property Members
uvx rock-kb model-map get group --format markdown
```

Exact lookup accepts model slugs or names, so `group`, `Group`, and `Group Model Map`
all target the stable `Group` model instead of related models such as
`ConnectionOpportunityGroup`. Use `search` only when you do not know the model
name or need broader concept context.

- Global index: `knowledge/model-map/index.md`
- Stable models: `knowledge/model-map/stable-models.jsonl`
- Stable properties: `knowledge/model-map/stable-properties.jsonl`
- Stable methods: `knowledge/model-map/stable-methods.jsonl`
- Agent model digests: `agent/model-map-digests.jsonl`
- Model detail pages: `knowledge/model-map/models/*.md`
- Latest/pre-alpha rows: `knowledge/model-map/latest-models.jsonl`
- Latest/pre-alpha methods: `knowledge/model-map/latest-methods.jsonl`
- Stable-to-latest diff: `knowledge/model-map/version-diff.jsonl`

The generated rows include Obsidian block-action provenance such as collection
method, initialization/detail endpoints, table names, obsolete flags, enum and
DefinedValue flags, and method signatures. Use those fields to judge staleness
and source quality before citing a row.

Do not treat latest/pre-alpha model data as the default. Use it only as an upcoming-version callout when it differs from stable.

## Lava Context Roots

For Lava questions, do not start by guessing which objects are available. First
identify the rendering surface, then use the generated Lava context directory to
find available root keys:

```bash
uvx rock-kb search "PersonAttendance Check-In Label Designer Lava roots"
uvx rock-kb search "communication recipient merge values"
uvx rock-kb search "workflow action Lava merge fields"
```

Use this lookup order:

1. Lava context directory: find the available root key or nested path for the
   specific surface.
2. Model Map: inspect properties and relationships for linked model roots.
3. Lava capabilities: confirm filters, commands, syntax behavior, and risk.
4. Official docs/source citations: final evidence for precise answers.

Important generated artifacts:

- Lava context rows: `agent/lava-contexts.jsonl`
- Lava context directory: `knowledge/concepts/lava/lava-context-directory.md`
- Lava context summary: `agent/lava-context-summary.json`

Rows marked `needs_live_verification: true` are source-code-backed leads whose
exact availability still depends on page, block, communication, workflow, label,
or instance configuration.

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
ROCK_KB_TOKEN=<issued-token> uvx rock-kb auth-check --org <org-id>
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl --dry-run
ROCK_KB_TOKEN=<issued-token> uvx rock-kb submit bundle.jsonl
```

Before submitting, make sure every `concept_ids` value is an existing KB concept
id. Do not invent plain-language ids. Use `uvx rock-kb concepts` or the local
`concepts/registry.yaml` as the source of truth, then run validation. For
example, use `event-registration` rather than `registrations`, and
`giving-finance` rather than `finance`.

If you are operating from a local `rock-agent-kb` checkout and need unreleased
client changes, use the checked-in client instead:

```bash
uv run --project clients/python rock-kb validate bundle.jsonl
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb auth-check --org <org-id>
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl --dry-run
ROCK_KB_TOKEN=<issued-token> uv run --project clients/python rock-kb submit bundle.jsonl
```

## Submit Token Setup

Hosted submission requires a per-organization token. If `ROCK_KB_TOKEN` is missing, do not guess a token, do not ask for it in a public issue or PR, and do not paste it into chat logs. Tell the user that the organization must be registered and reviewed in `orgs/<org-id>.yaml`, then a Rock KB maintainer must issue or rotate a submit token outside git. The hosted service stores only that token's SHA-256 digest; the raw token is shown only to the organization.

Use one of these safe local patterns after the maintainer provides the raw token:

```bash
export ROCK_KB_TOKEN='<issued-token>'
uvx rock-kb auth-check --org <org-id>
uvx rock-kb submit bundle.jsonl --dry-run
uvx rock-kb submit bundle.jsonl
```

For future terminal sessions on macOS, prefer Keychain over a repo-local file:

```bash
security add-generic-password -U -a "$USER" -s "rock-kb-token-<org-id>" -w '<issued-token>'
export ROCK_KB_TOKEN="$(security find-generic-password -a "$USER" -s "rock-kb-token-<org-id>" -w)"
```

For CI, hosted agents, or app connectors, save the token as a secret named `ROCK_KB_TOKEN` in that system's secret store, or mount it as a secret file and set `ROCK_KB_TOKEN_FILE`. Do not save tokens in `community-contributions/`, `orgs/`, `.env`, `.envrc`, checked-in agent instructions, prompt files, screenshots, transcripts, or bundle rows. If the token is lost or exposed, ask a maintainer to rotate it.

Contribution rows must be newly written, public-safe, source-linked, redaction-attested, and license-attested. Set `needs_live_verification: true` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.

Never submit private person data, staff notes, live IDs, internal URLs, private repo links, database names, SQL exports, raw logs, raw transcripts, copied proprietary text, screenshots with private state, secrets, tokens, signed media URLs, or direct private media links.
