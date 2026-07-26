---
name: rock-kb-agent
description: Use when answering Rock RMS questions with the public Rock Agent Knowledge Base, configuring an agent to query the hosted KB, citing KB trust tiers, inspecting model-map details, or submitting public-safe community contribution bundles.
metadata:
  rock-kb-skill-version: "1.4.0"
  rock-kb-source: "https://github.com/ONE-ALL-Church/rock-agent-kb/tree/main/skills/rock-kb-agent"
  rock-kb-published-at: "2026-07-26T14:51:30Z"
  rock-kb-minimum-client-version: "0.17.0"
---

# Rock KB Agent

## Purpose

Use the Rock Agent Knowledge Base before web search for Rock RMS operational, development, Lava, model-map, mobile, workflow, security, reporting, check-in, group, API, or contribution questions.

The KB is source-tiered. Never blend community-only material into authoritative guidance without labeling it.

## Access Strategy

For ordinary online retrieval, MCP and the `rock-kb` CLI are co-primary
interfaces to the same hosted public projection:

- Use MCP when the agent host supports HTTP MCP and benefits from typed,
  discoverable tools and structured results without shell parsing.
- Prefer the default direct MCP tools for ordinary search, exact lookup, and
  any feedback or submission operation.
- Use the opt-in experimental Code Mode endpoint only when a read-only task
  needs several dependent KB calls, branching, loops, or intermediate
  filtering. It excludes every write tool.
- Use the CLI for terminal agents, scripts, local validation, stateful local
  commands, and environments without MCP support.
- Use OKF only when the task requires an offline corpus, a pinned release,
  bulk analysis, local indexing or vectorization, archival, or cross-system
  interchange.

MCP does not contain better or newer knowledge than the CLI. Do not download or
load an OKF bundle merely to answer an ordinary online Rock question.

## Capability Map

The KB can help agents do more than plain text search:

- Search public Rock RMS knowledge with authority and claim tiers.
- Open task-oriented concept guides and quickstarts.
- Inspect structured claims and source citations by concept.
- List valid concept IDs before writing or submitting contribution rows.
- Use the manifest to discover agent entrypoints and generated artifacts.
- Inspect the hosted skill manifest to detect a newer reviewed instruction
  package without trusting an unverified local copy.
- Inspect public operations counts, the anonymous field-validation funnel, and
  bounded maintainer review queues through the dashboard.
- Inspect authoritative daily/weekly workflow and source freshness, including
  separate last-check, content-change, count, hash, and status fields.
- List stable Rock Model Map models and get exact model digests.
- Inspect model fields, required fields, relationships, methods, version diffs,
  and one property at a time.
- List exact Lava rendering surfaces and retrieve grouped roots, inheritance,
  conditions, source versions, completeness, and Model Map links before
  guessing which merge fields exist.
- Find reusable community recipes with pinned code, adaptation points,
  security boundaries, compatibility, validation steps, and learnings.
- Assess open or historically relevant Rock product issues against bounded
  versions, concepts, platforms, capabilities, and configuration identifiers,
  with explicit evidence, exclusions, risk provenance, freshness, and
  read-only verification guidance.
- Use Rockumentation API metadata and branch paths as routing signals.
- Run the bounded external-church test round and preserve its stable public
  result IDs for structured feedback.
- With explicit consent, report whether an exact public result was useful,
  partially useful, or not useful without sending the question or private data.
- Validate and submit public-safe community contribution bundles.
- Connect through hosted HTTP MCP when the current agent client supports tools.
- Download, inspect, and verify full or compact core read-only OKF distributions for
  offline or cross-tool knowledge consumption.

## Install And Availability

Choose the hosted interface that fits the current agent. For MCP-capable Codex,
Claude Code, Cursor, or OpenCode hosts, the CLI can install this skill and the
hosted MCP entry:

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

### Skill Update Check

On the first Rock KB task in a session, run the bounded check below when a
terminal is available. It makes no network request if a successful check is
less than 24 hours old and never changes the installed skill:

```bash
uvx rock-kb skill check --if-due
```

Respect the returned persisted policy:

- `notify`: tell the human an update is available and wait for approval before
  running `uvx rock-kb skill update`.
- `auto`: run `uvx rock-kb skill update` when the check reports an update. This
  policy represents prior explicit user-level permission.
- `pinned`: do not update or repeatedly prompt. Update only when the human asks
  to run `uvx rock-kb skill update --unpin`.

Never infer update permission from feedback, test-round, contribution, or
GitHub consent. Ask once before setting `auto`, and persist the answer only with
permission through `uvx rock-kb skill policy auto`. Project-scoped skills may
not use `auto`; update them explicitly and ask the human to review the Git diff.
After an applied update with `restart_required: true`, explain that the host
must restart or reload before the new instructions take effect.

When no terminal is available, call `kb_skill_manifest` and compare its
`skill_version` with `metadata.rock-kb-skill-version` above. Notify the human if
they differ; do not claim that an MCP call can rewrite the local skill.

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
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text
uvx rock-kb recipes list
uvx rock-kb recipe oneall:check-in-status-dashboard
uvx rock-kb recipe oneall:registration-to-connection-request
uvx rock-kb recipe verify oneall:check-in-status-dashboard --rock-version 18
uvx rock-kb issues assess instance-profile.json --scope open
uvx rock-kb issues watch instance-profile.json --scope all-relevant
uvx rock-kb test-round
uvx rock-kb telemetry status
uvx rock-kb dashboard
uvx rock-kb freshness
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
uv run --project clients/python rock-kb lava-context list --family check-in-label
uv run --project clients/python rock-kb lava-context get check-in-label-checkout-dynamic-text
uv run --project clients/python rock-kb test-round
uv run --project clients/python rock-kb dashboard
uv run --project clients/python rock-kb freshness
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
- `lava-context list [--family <family>] [--surface-type <type>]`: discover exact Lava rendering-surface IDs.
- `lava-context get <context-id> [--root <root-key>]`: fetch one grouped context with direct and inherited roots, availability conditions, source pins, completeness, and model links.
- `recipes list [--concept <id>]`: discover reusable community implementation patterns.
- `recipes search <query>`: search recipe use cases and learnings.
- `recipe <recipe-id>`: fetch the full structured recipe before adapting code.
- `recipe verify <recipe-id> [--rock-version <version>]`: check immutable file hashes and declared compatibility without executing recipe code.
- `issues search <query>`: search public Rock core and mobile product issue metadata without mixing it with KB malfunction reports.
- `issues list [--repository core|mobile] [--state open|closed] [--version <version>] [--concept <id>]`: filter issue routing metadata and version evidence.
- `issue <url|id|number|mobile:number>`: fetch one exact issue record.
- `issues assess <profile.json> [--scope open|historical-unresolved|all-relevant] [--limit N] [--offset N]`: conservatively compare issues with a bounded profile containing only versions, platforms, concepts, capabilities, and public configuration identifiers. `open` is the default; use the historical scopes explicitly for upgrades or older behavior. Follow `has_more` and `next_offset` when calling REST or MCP directly.
- `issues watch <profile.json> [--scope ...]`: retrieve the complete assessment, keep an owner-only scope-specific baseline on the local machine, and report newly relevant, applicability, routing, risk, remediation, catalog freshness, population, exclusion, no-longer-routed, or revalidation changes. Never put logs, secrets, live IDs, person data, or private configuration values in the profile.
- `issues plan <issue>`: return a typed, read-only multi-agent investigation plan; `--include-private-instance` adds a private-only worker.
- `ideas search <query>`: search explicit feature-request, known-gap, and roadmap metadata without mixing it into normal implementation guidance.
- `ideas list [--status <status>] [--category <category>] [--concept <id>] [--planned-version <version>]`: filter the bounded Ideas catalog.
- `idea <number|id|url>`: fetch one exact idea metadata row and its bounded typed relationships; corroborate its status before making a product claim.
- `test-round`: run ten bounded public cohort checks, including Rock Idea
  relationship trust and core/mobile
  issue trust separation and version applicability. Review every manual prompt;
  an automatic pass proves the response contract, not that the answer is useful
  for a particular church.
- `test-round --review --submit`: for an opted-in `external-test` or maintainer
  cohort, record one fixed outcome for all ten cases. Never submit free text,
  raw queries, logs, identities, or private Rock data.
- `feedback <result-id> --rating <-1|1> --reason <helpful|outdated|missing|incorrect|wrong_route>`: record structured feedback without sending free text.
- `telemetry enable --cohort <community|external-test|maintainer> --consent-attested`: create a private random installation marker and opt into anonymous field validation. The service stores only its one-way hash. Run `telemetry disable` to revoke the opt-in.
- `outcome <result-id> --outcome <useful|partially_useful|not_useful> --reason <fixed-code> --consent-attested`: report the usefulness of an exact result after a completed task. Repeat `--reason` up to three times; never send prose or private data.
- `report-issue --failure-type <service|mcp|cli|schema|authentication|retrieval> --operation <id> --error-code <id> --description <redacted-summary> --redaction-attested`: report a KB malfunction for review. Never include logs, queries, secrets, private paths, or private Rock data.
- `manifest`: inspect public agent entrypoints and generated artifact paths.
- `concepts`: list valid concept IDs and their guide paths.
- `dashboard`: check public contribution counts, review queues, and operational health.
- `freshness`: inspect authoritative source and scheduled-refresh health without
  exposing source bodies, private paths, identities, or queries.
- `mcp-config`: connect clients that support HTTP MCP to the hosted direct tools.
- `mcp-config --mode code`: opt into the experimental read-only composition
  endpoint. Use direct tools for single calls and every write operation.
- `okf download [--profile full|core]`: download and digest-verify a read-only Open Knowledge Format release for offline, pinned, bulk, or interoperable use. Use `core` for a smaller local corpus and `full` for lossless public records.
- `okf inspect <bundle>`: show an OKF directory or archive's version, source commit, scope, and counts.
- `okf conformance <bundle>`: apply portable upstream OKF rules to any bundle; broken links and unknown versions are warnings.
- `okf verify <bundle>`: verify a Rock KB release's profile, licensing, complete checksums, structured records, archive safety, and public/private boundaries. `okf validate` is a compatibility alias.
- `validate <bundle.jsonl>`: check a contribution bundle before submitting.
- `auth-check --org <org-id>`: verify hosted submission auth before sending a bundle.
- `submit <bundle.jsonl> [--dry-run] [--org <org-id>]`: submit reviewed public-safe knowledge for a registered org with `ROCK_KB_TOKEN`; `--org` is inferred when bundle rows share one `org_id`.

Do not fall back to copying raw KB artifacts into another repo. Use the OKF
distribution when an agent or external tool needs a portable, offline corpus.
Do not import an arbitrary OKF bundle into trusted knowledge; route proposed
knowledge through the reviewed contribution workflow.

## Offline And Portable Access

Use OKF when the agent or an external knowledge system must operate without the
hosted service, retain a reproducible release, index the complete public corpus,
or exchange knowledge through standard Markdown and links:

```bash
uvx rock-kb okf download --profile core
uvx rock-kb okf inspect rock-agent-kb-okf-core-vX.Y.Z.zip
uvx rock-kb okf verify rock-agent-kb-okf-core-vX.Y.Z.zip
```

The `core` profile is the normal starting point for a local agent index. The
`full` profile adds routing-only claims, source summaries, contribution
provenance, and Rock issue records. An OKF bundle is a versioned release
snapshot, so check its source commit and version before relying on it for
current behavior. Do not place an entire bundle in one model context; index it
and retrieve bounded records.

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
- `kb_list_lava_contexts`: list exact Lava rendering surfaces with coverage,
  versions, and root counts.
- `kb_get_lava_context`: fetch one grouped Lava context with direct and
  inherited roots, conditions, model links, source pins, and completeness.
- `kb_list_recipes`: list community recipes, optionally filtered by concept.
- `kb_get_recipe`: fetch one recipe with its immutable source pin, adaptation
  points, security, compatibility, validation, and reusable learnings.
- `kb_verify_recipe`: verify immutable recipe hashes and optional target Rock
  version without executing community code.
- `kb_search_rock_issues`, `kb_list_rock_issues`, and `kb_get_rock_issue`:
  retrieve public Rock product issue routing metadata. Treat reports as leads,
  not proof of cause, fix, or local applicability. Exact results may include
  `reviewed_enrichments`; evaluate each enrichment's diagnosis status, claim
  tier, authority, confidence, citations, and version assertions separately
  from the unreviewed upstream report. When a `verification_playbook` is
  present, follow its read-only checks to determine whether the issue can affect
  the current instance. Record only the bounded evidence labels it requests;
  keep private IDs, names, logs, and query output out of public feedback. Never
  improvise a mutating reproduction in production. If an assessment returns
  `revalidation_due_enrichment_ids`, do not rely on those enrichments for
  applicability until a replacement review is published.
- `kb_assess_rock_issues`: compare issue version evidence with a bounded
  structured profile. Use `scope: open` by default; request
  `historical-unresolved` or `all-relevant` explicitly. Read `catalog.status`
  and `catalog.warning` first, then inspect `decision`, `evidence`,
  `requirement_evaluation`, `risk`, `live_verification`, and the bounded
  `exclusion_summary`. A missing prerequisite field is unknown; a provided
  list is treated as the complete declaration for that profile dimension.
  Treat `risk.level: unrated` as intentional, not missing analysis. Never send
  logs, queries, identifiers, secrets, person data, or private configuration
  values.
- `kb_plan_rock_issue_investigation`: create a credentialless, read-only
  orchestrator-worker plan. It never posts to GitHub; private instance evidence
  stays in a separate permission-scoped overlay.
- `kb_search_rock_ideas`, `kb_list_rock_ideas`, and `kb_get_rock_idea`:
  retrieve bounded Rock Community feature-request and roadmap metadata. Use
  these only for explicit idea, known-gap, feature-request, or roadmap intent.
  Treat every row as `community-unreviewed` routing context. A `Complete`,
  `Planned`, or `Started` label is not proof of release availability; confirm it
  with official documentation, release notes, public source, and authorized
  read-only instance evidence. Exact Idea results include outbound typed links,
  and exact issue results may include inbound Idea links. Interpret
  `references_issue` as an explicit link, not proof of implementation;
  `implemented_by_issue` requires official release-note corroboration.
- `kb_feedback`: record a fixed rating and reason for an exact result. Never put
  private data into feedback.
- `kb_outcome`: with current human consent and an opted-in anonymous
  installation marker, record whether an exact public result was `useful`,
  `partially_useful`, or `not_useful` plus one to three compatible fixed reason
  codes. It is task-usefulness evidence, not a free-form comment.
- `kb_report_issue`: report a service, MCP, CLI, schema, authentication, or
  retrieval malfunction. Send only structured fields and a short generic
  redaction-attested description. Never send a query, prompt, raw request or
  response, log, stack trace, secret, private path, person data, or private Rock
  identifier. Keep `kb_feedback` for incorrect, outdated, missing, or misrouted
  knowledge.
- `kb_review_dashboard`: check public review queues, conflicts, community
  intake, issue reports, hosted evaluation, and telemetry counts.
- `kb_get_freshness`: check daily/weekly schedule health and source
  `last_checked_at`, `content_changed_at`, result count, content hash, and
  status independently.
- `kb_submit`: validate and submit a contribution bundle for a registered org.

Use MCP for agent-native typed tools and the CLI for terminal or scripted
access. Both query the same hosted projection; choose by client capability, not
expected answer quality.

The default direct MCP endpoint exposes each operation as a typed tool with
read/write annotations and structured results. The optional `/mcp/code`
endpoint exposes one experimental `code` tool that can compose the read-only
subset. Use Code Mode only when composition reduces calls or intermediate
context; it is unnecessary overhead for one search, claim, model, recipe,
issue, or Idea lookup. Never use it to work around the omitted write tools.

When reporting a KB malfunction, retain the returned stable `report_id` for
maintainer follow-up. Repeated failures deduplicate and increment an occurrence
count. Reports remain pending review and do not create GitHub issues
automatically.

## Feedback Consent

Do not enable telemetry or submit feedback merely because the KB exposes these
tools. After the first completed KB-assisted task, check private user-level
memory for a current `rock_kb_feedback_consent` decision. If none exists, ask:

> Rock KB can use privacy-bounded field-validation signals to improve retrieval.
> It can retain a one-way hash of a random installation marker, a fixed cohort,
> the public result ID and kind, the KB projection and client version, a fixed
> quality rating or usefulness outcome, fixed reason codes, timestamps, and
> aggregate counts. It does not retain your question, prompt, organization,
> church or person identity, IP address, free text, logs, secrets, or private
> Rock data. May I enable this anonymous marker and submit these signals when I
> can confidently evaluate a completed task? Choose: Allow automatically, Ask
> each time, or Do not send. May I remember that choice in private user-level
> memory?

This is consent notice version `2`. A version `1` decision does not cover the
anonymous marker or usefulness outcomes; ask again before enabling either.

- `Allow automatically`: standing permission covers exact-result
  `kb_feedback` and `kb_outcome` only under the rules below.
- `Ask each time`: request confirmation before each feedback or outcome event.
- `Do not send`: do not enable the marker or submit either signal; do not ask
  again unless the human reopens the decision.

Ask separately whether the preference may be remembered. Store it only in
private user-level memory when the human explicitly permits persistence:

```yaml
rock_kb_feedback_consent:
  notice_version: 2
  quality_feedback: automatic  # automatic, ask, or disabled
  usefulness_outcomes: automatic  # automatic, ask, or disabled
  anonymous_installation: enabled  # enabled or disabled
  cohort: community  # community, external-test, or maintainer
  malfunction_reports: ask
  test_rounds: ask
  contributions: explicit_review
```

Never put this preference or the private installation marker in a public or
shared repository, KB payload, project artifact, contribution bundle, or church
data store. If private persistent memory is unavailable or not permitted, keep
the decision session-scoped and do not create a persistent marker.

After consent to persistent anonymous field validation, configure it locally:

```bash
uvx rock-kb telemetry enable --cohort community --consent-attested
uvx rock-kb install-agent
```

The first command writes a random marker to the user's private state directory;
its status output does not reveal the value and the service stores only its
one-way hash. The second places the marker in supported user-scoped MCP
configuration so that host can send it. Treat that local configuration as
private and restart or reload the host afterward. Project-scoped MCP
configuration does not receive the marker.

Standing permission is not permission to report every search:

- Submit `kb_feedback` only when an exact result's factual quality, freshness,
  completeness, or routing can be assessed confidently.
- Submit `kb_outcome` only after an exact result materially contributed to a
  completed task. Choose `useful`, `partially_useful`, or `not_useful` and one
  to three compatible fixed reason codes.
- Submit at most one quality rating and one usefulness outcome per exact result
  per completed task. Never repeat an event to increase its count.
- Never invent a result ID. Submit nothing when usefulness is uncertain. A
  zero-result search is not automatically a KB malfunction.

`kb_report_issue` still requires confirmation for each report because it needs
a short redaction-attested description. `test-round --review --submit` requires
explicit approval for each round. Contributions and public PRs always require
explicit human review. Field-validation consent grants none of those
permissions.

The human may revoke or change the decision at any time. To revoke persistent
field validation, run `uvx rock-kb telemetry disable`, rerun
`uvx rock-kb install-agent`, and restart the host. Ask again whenever the
consent notice version changes or retained fields expand.

## Read Workflow

1. Start with the hosted KB through MCP or the CLI. For terminal access:

```bash
uvx rock-kb search "<question or error>"
uvx rock-kb get <concept-id>
uvx rock-kb claims <concept-id> --min-tier source_backed
uvx rock-kb dashboard
```

For an MCP-capable client, configure the same hosted projection instead:

```bash
uvx rock-kb mcp-config
```

With current version `2` consent, ordinary participating installations use the
fixed `community` cohort. A church running the formal public test round may use
`external-test` instead:

```bash
uvx rock-kb telemetry enable --cohort community --consent-attested
ROCK_KB_COHORT=external-test uvx rock-kb test-round
uvx rock-kb telemetry enable --cohort external-test --consent-attested
uvx rock-kb mcp-config
```

Never replace a cohort with a church name or custom identifier. Cohorts are
self-declared telemetry labels, not authentication. Without consent, leave
telemetry disabled and do not send an installation marker.

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

For product issues, keep GitHub state, validation, applicability, and remediation
separate. Closed does not mean fixed. A reporter-provided version does not prove
all instances on that version are affected, and a `Fixed in vX.Y` label does not
prove every build in that release line contains the fix. Corroborate with
official docs, release notes, public source, and authorized read-only instance
evidence before recommending action.

For an instance issue review, assess `open` first. Read catalog freshness and
the risk source before describing urgency. Treat the issue projection as
current only when both `projection_count_matches_source` and
`projection_content_matches_source` are true; equal row counts alone do not
detect state, label, routing, or remediation changes. Fetch exact records for
the small set that may apply, then follow current reviewed read-only playbooks. Use
`historical-unresolved` or `all-relevant` for upgrades and older symptoms.
Never infer severity from an issue title or applicability result; risk is
evidence-backed or explicitly `unrated`.

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
- `rock_issues`, `rock_issue_enrichments`, `rock_issue_summary`, and
  `rock_issue_directory`: public-safe issue routing metadata, separately
  reviewed conclusions, coverage, and trust rules. Exact issue results join
  approved enrichments into the canonical issue instead of returning duplicates.
- `rock_issue_investigation_prompt`: the typed worker output and security
  contract for coordinated issue research.
- `rock_ideas`, `rock_idea_relationships`, `rock_idea_verification_queue`, `rock_idea_summary`, and
  `rock_idea_directory`: public-safe feature-gap and lifecycle metadata plus
  evidence-backed concept, model, issue, documentation, and release links.
  Verification queue states prioritize corroboration work but never prove that
  a lifecycle label is implemented. A
  `maintainer_reviewed_no_official_match` state means only that the current
  bounded evidence inputs produced no match; it is not proof that the feature
  is absent. Treat only an official typed relationship as corroboration.
  These rows stay separate from approved claims and ordinary implementation
  guidance. Concept packages include only a bounded Idea summary; use the
  dedicated Ideas tools for complete filtering.
- `model_map`, `model_map_digests`, `model_map_properties`,
  `model_map_methods`, and `model_map_version_diff`: model lookup and version
  comparison surfaces.
- `lava_contexts`, `lava_context_directory`, `lava_capabilities`,
  `lava_safety_matrix`, and `lava_agent_usage_examples`: Lava-specific context,
  syntax, safety, and usage surfaces.
- `recipes` and `recipe_directory`: reusable community implementation patterns
  and their human-readable generated pages.

Prefer the higher-level CLI or MCP tools first. Use manifest entrypoints when
the task needs a specific generated artifact or when direct tool output is not
specific enough.

## Community Recipes

Use recipes when the question asks how another organization implemented a
specific Rock workflow, report, Lava Application, integration, or automation.
Search first, then fetch the exact recipe:

```bash
uvx rock-kb recipes search "check-in registration attendance dashboard"
uvx rock-kb recipes search "registration to connection request workflow"
uvx rock-kb recipe oneall:check-in-status-dashboard
uvx rock-kb recipe oneall:registration-to-connection-request
uvx rock-kb recipe verify oneall:registration-to-connection-request --rock-version 18
```

Before adapting a recipe:

1. Confirm its community trust tier and `needs_live_verification` status.
2. Open the immutable source commit, not the repository's moving default branch.
3. Apply every required adaptation point and verify the target Rock version.
4. Preserve authentication, authorization, data-access, sensitive-data, and
   CSRF boundaries. A read-only recipe is not permission-free.
5. Run the listed validation and rollback steps in the target instance.
6. Cite the recipe and its authority tier; do not present it as official Rock
   behavior.
7. Use `recipe verify` before adaptation. Treat `expected` compatibility and
   missing consumer attestations as prompts for local testing, not as proof of
   failure.

When contributing a reusable implementation, keep substantial code in the code
owner's licensed public repository. Submit a `recipe` contribution containing
the structured digest, exact commit, file hashes, adaptation points, security,
compatibility, validation, and learnings. Never submit production IDs, private
routes, people, secrets, or private source paths.

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
identify the rendering surface, then use exact grouped context lookup:

```bash
uvx rock-kb lava-context list --family check-in-label
uvx rock-kb lava-context get check-in-label-family-dynamic-text
uvx rock-kb lava-context get check-in-label-checkout-dynamic-text --root CheckoutDateTime
```

Use generic search only when the surface ID is not yet known:

```bash
uvx rock-kb search "PersonAttendance Check-In Label Designer Lava roots"
uvx rock-kb search "communication recipient merge values"
uvx rock-kb search "workflow action Lava merge fields"
```

Use this lookup order:

1. Lava context list/get: identify the exact surface and retrieve all direct
   and inherited roots.
2. Model Map: inspect properties and relationships for linked model roots.
3. Lava capabilities: confirm filters, commands, syntax behavior, and risk.
4. Official docs/source citations: final evidence for precise answers.

Important generated artifacts:

- Lava context rows: `agent/lava-contexts.jsonl`
- Lava context directory: `knowledge/concepts/lava/lava-context-directory.md`
- Lava context summary: `agent/lava-context-summary.json`

Read context metadata conservatively:

- `coverage_status: complete_for_source_snapshot` means the parser captured the
  explicit roots in that pinned source snapshot. It does not guarantee that
  every root is populated in every request.
- `partial_curated` or `dynamic` means absence from the result is not proof that
  a field can never exist.
- `availability_condition`, `required_setting`, `execution_phase`, and
  `may_be_null` explain when a root is present or populated.
- `inherited: true` and `defined_in_context_id` identify composed common fields.
- `source_version` and `source_commit` identify the Rock source snapshot. Check
  the target instance version when behavior is version-sensitive.
- `needs_live_verification: true` means the source-backed row still depends on
  page, block, communication, workflow, label, or instance configuration.

Never infer an arbitrary Lava root merely because its type exists in Model Map.

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

Before preparing a contribution, use `docs/community-content-priorities.md`.
Prefer reusable recipes, difficult troubleshooting paths, failure modes,
precise version caveats, and verified workflows. Broad summaries of official
manuals or material already returned by the KB are low priority. Relate the
candidate to exact concept IDs and, when available, model slugs, recipe IDs, or
Lava-context IDs.

Never submit private person data, staff notes, live IDs, internal URLs, private repo links, database names, SQL exports, raw logs, raw transcripts, copied proprietary text, screenshots with private state, secrets, tokens, signed media URLs, or direct private media links.
