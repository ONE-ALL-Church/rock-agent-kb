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
- `kb_get_result`: full public record for one exact compact search result id.
- `kb_get_claim`: one exact approved claim and all of its concept routes.
- `kb_manifest`: public artifact manifest and entrypoints.
- `kb_list_concepts`: available concept ids, titles, guide paths, and dependency metadata.
- `kb_get_concept`: quickstart, answers, task cards, and release caveats for one concept.
- `kb_get_claims`: approved public claims for a concept, optionally filtered by claim tier.
- `kb_search_rock_issues`, `kb_list_rock_issues`, and `kb_get_rock_issue`: public Rock product issue routing metadata; exact results join separately reviewed enrichments without duplicating the issue result.
- `kb_assess_rock_issues`: scoped conservative comparison with a bounded version, concept, platform, capability, and configuration profile. The V2 response separates matches, exclusions, unknowns, evidence, remediation, risk provenance, catalog freshness, and read-only verification.
- `kb_plan_rock_issue_investigation`: typed read-only orchestrator-worker plan with no GitHub write path.
- `kb_search_rock_ideas`, `kb_list_rock_ideas`, and `kb_get_rock_idea`: explicit feature-gap and roadmap routing; exact Idea and Issue lookups expose bounded typed relationships when evidence exists.
- `kb_feedback`: fixed quality feedback for a public result.
- `kb_outcome`: consent-attested completed-task usefulness for an exact public result; requires the opted-in anonymous installation marker.
- `kb_report_issue`: bounded, redaction-attested reports when the KB itself malfunctions.
- `kb_review_dashboard`: public review, issue-report, evaluation, and telemetry counts.
- `kb_submit`: hosted-only contribution intake for registered organizations.

If the optional dependency is missing, `kb serve` exits with:

```text
kb serve requires the serve extra: uv sync --extra serve
```

## Hosted Service

The hosted service lives under `service/` and is deployed with Cloudflare Workers, D1, and R2. Build the deployment projection locally:

```bash
uv run kb deploy-service
```

That command writes ignored deployment payloads under `service/dist/`:

- `projection.json`: deployment metadata and current version hash.
- `d1-seed.sql`: D1 schema and search/org seed data.
- `search-rows.jsonl`: public search rows with `authority_tier` and `claim_tier`.
- `artifacts/`: R2 artifact payload keyed by the public export paths.

Apply the projection only when Cloudflare credentials and bindings are configured:

```bash
uv run kb deploy-service --apply --env production --database rock-agent-kb --bucket rock-agent-kb-artifacts
```

`--apply` reads `/health`, selects the inactive fixed R2 slot (`slots/a` or
`slots/b`), uploads all shards there, deploys Worker code that understands both
slots and legacy version prefixes, and then updates D1 metadata to switch the
active projection. It fails closed when current slot state cannot be read.
This bounds future artifact storage to two projections while retaining a
legacy fallback during migration.

After the hosted smoke test confirms a slot-backed deployment, run:

```bash
uv run kb service-retention --apply \
  --base-url https://rock-agent-kb.oneandall.church \
  --bucket rock-agent-kb-artifacts
```

The command first verifies that `/health` reports a bounded slot, then
idempotently upserts a 30-day expiration rule scoped only to the old
`versions/` prefix. It preserves unrelated lifecycle rules and will not create
an age rule for either active slot. The deploy workflow performs this step only
after hosted smoke tests pass.

Before the production GitHub Action can deploy, configure these repository environment values:

| Name | Type | Required | Notes |
|---|---|---:|---|
| `CLOUDFLARE_API_TOKEN` | `production` secret | Yes | Cloudflare API token with Worker, D1, and R2 deploy permissions. Wrangler OAuth login is not sufficient for GitHub Actions. |
| `CLOUDFLARE_ACCOUNT_ID` | `production` secret | Yes | Cloudflare account id. |
| `ROCK_KB_WORKER_GITHUB_TOKEN` | `production` secret | Yes for `kb_submit` PRs | GitHub token/App token the Worker uses to create contribution PRs and enable auto-merge when allowed. |
| `ORG_TOKEN_SHA256_JSON` | `production` secret | Yes for `kb_submit` auth | JSON object mapping `org_id` to SHA-256 token digest. |
| `ROCK_KB_D1_DATABASE_ID` | repository or `production` variable | Yes | Real D1 database id injected into `service/wrangler.jsonc` during CI. |
| `ROCK_KB_D1_DATABASE` | repository or `production` variable | No | Defaults to `rock-agent-kb`. |
| `ROCK_KB_R2_BUCKET` | repository or `production` variable | No | Defaults to `rock-agent-kb-artifacts`. |
| `ROCK_KB_BASE_URL` | repository or `production` variable | Yes for smoke/eval | Enables live `/health`, `/manifest.json`, and `kb eval-service` checks. |

The checked-in `service/wrangler.jsonc` keeps a placeholder D1 id so public source does not encode account-specific infrastructure. The deploy workflow runs `scripts/configure_service_bindings.py` when the real id is configured.

To create the Cloudflare resources and set the GitHub deployment variables in one pass, first review the dry run:

```bash
python3 scripts/bootstrap_service_infra.py
```

Then run it with `--apply` from an environment that has a valid Wrangler login plus `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `ROCK_KB_WORKER_GITHUB_TOKEN`, and `ORG_TOKEN_SHA256_JSON` exported. The script creates or reuses the D1 database and R2 bucket, sets `ROCK_KB_D1_DATABASE_ID`, `ROCK_KB_D1_DATABASE`, `ROCK_KB_R2_BUCKET`, and `ROCK_KB_BASE_URL`, and writes the Cloudflare and intake GitHub environment secrets.

Create `CLOUDFLARE_API_TOKEN` in the Cloudflare dashboard as a durable API token,
then write it to the GitHub production environment without printing it:

```bash
printf '%s' '<cloudflare-api-token>' \
  | gh secret set CLOUDFLARE_API_TOKEN \
      --repo ONE-ALL-Church/rock-agent-kb \
      --env production
```

Do not use Wrangler's local OAuth token as the production CI secret; it is an
interactive login credential, not the durable API token expected by Actions.

Private corpus automation uses a separate repository secret and variables. From
a trusted shell with `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
`PRIVATE_CORPUS_REPO`, and `PRIVATE_R2_BUCKET` exported, run
`python3 scripts/bootstrap_private_corpus_infra.py --dispatch --apply` to write
the private repo settings, verify or create the private R2 bucket, and dispatch a
restore-only ingest check. Add `--run-media-batch --media-limit 1` only when you
are ready to prove hosted transcription.

To issue or rotate one organization's hosted submit token, start from the
current `ORG_TOKEN_SHA256_JSON` value and add the new digest without printing the
raw token:

```bash
printf '%s' "$RAW_SUBMIT_TOKEN" \
  | python3 scripts/update_org_token_digest.py \
      --org-id <org-id> \
      --existing-json "$ORG_TOKEN_SHA256_JSON" \
  | gh secret set ORG_TOKEN_SHA256_JSON \
      --repo ONE-ALL-Church/rock-agent-kb \
      --env production
```

The org must already be reviewed in `orgs/<org-id>.yaml`; pending examples must
not receive live submit tokens.

The Worker exposes:

- `GET /health`
- `GET /manifest.json`
- `GET /llms.txt`
- `GET /concepts`
- `GET /concepts/<concept-id>.md`
- `GET /claims/<concept-id>?min_tier=source_backed`
- `GET /claims/id/<claim-id>`
- `GET /search?q=<query>&min_tier=routing_context_only` (compact by default; add `detail=full` for compatibility)
- `GET /results/<result-id>`
- `GET /lava-contexts?family=<family>&surface_type=<type>`
- `GET /lava-contexts/<context-id>?root=<root-key>`
- `GET /rock-issues/search?q=<query>`
- `GET /rock-issues?repository=core&state=open&version=19.2&concept=<concept-id>`
- `GET /rock-issues/<issue-ref>`
- `GET /rock-issues/<issue-ref>/plan`
- `POST /rock-issues/assess`
- `GET /rock-ideas/search?q=<query>`
- `GET /rock-ideas?status=<status>&concept=<concept-id>`
- `GET /rock-ideas/<idea-ref>`

MCP exposes the same exact Lava surface operations as
`kb_list_lava_contexts` and `kb_get_lava_context`. Use them before Model Map
lookup when an agent needs to determine which roots exist in a rendering
surface. Search remains the discovery fallback when the surface ID is unknown.

Exact Idea responses include outbound typed relationships. Exact issue
responses include inbound Idea relationships. `references_issue` records an
explicit public-page link; only an official release-note-backed
`implemented_by_issue` edge carries stronger implementation evidence. Concept
packages returned by `kb_get_concept` include aggregate Idea status counts and
at most eight lifecycle-prioritized highlights. Lifecycle Ideas also include a
verification queue state and revalidation hash; neither is product evidence.
- `GET /operations/dashboard`
- `POST /feedback`
- `POST /outcomes`
- `POST /issues/report`
- `POST /mcp`
- `POST /submit`

When a reviewed public bundle under `community-contributions/<org-id>/` merges to `main`, the deploy workflow revalidates orgs and bundles, rebuilds the service projection, and includes those rows in hosted search as `kind: community_contribution`, `authority_tier: community-unreviewed`, and `claim_tier: routing_context_only`. `GET /search` and `kb_get_claims` include them by default; `GET /concepts/<concept-id>.md` and `kb_get_concept` continue to serve reviewed guide artifacts only. Recipe intake is the exception: after a recipe is promoted under `recipes/<org-id>/` with the same `contribution_id`, serving indexes only the canonical recipe and suppresses the older intake summary. Canonical recipes may also name exact older rows in `supersedes_contribution_ids`; only those rows are omitted. Claims, recipes, Lava contexts, and contributions each use one canonical search row with concept facets in `search_row_concepts`; legacy concept-specific result IDs resolve through `search_row_aliases` so saved links and feedback remain compatible.

`GET /operations/dashboard` and `kb_review_dashboard` expose public operational
counts for review queues, source conflicts, community intake, KB issue reports,
Rock issues and Ideas, guide status, evaluations, test rounds, and telemetry.
The `field_validation` section is the default real-use view. It excludes
evaluation and maintainer traffic and reports a funnel for search, exact
retrieval success/failure, usefulness outcome, quality feedback, and KB
malfunction reports. Its bounded review queue contains negative outcomes,
public topic categories with at least three zero-result searches, and failed
exact-lookup operation types. Funnel stages use only the v5 event stream that
starts with service v0.16.0; historical aggregate telemetry remains available
outside this funnel.

With version `2` human consent, the client keeps a private random installation
marker and sends it only with one of three fixed cohorts: `community`,
`external-test`, or `maintainer`. The Worker stores a SHA-256 hash scoped to
Rock KB, never the raw marker. It does not store raw or hashed query text,
attempted exact IDs for misses, organization or person identifiers, IP
addresses, free-form cohort labels, logs, secrets, or Rock data. Search misses
are categorized into bounded public topics before storage. PyPI downloads and
`uvx` cache/install activity occur outside the hosted service and are not usage
events.

Structured quality feedback stores the canonical public result ID and kind,
projection version, rating, fixed reason, and bounded client/cohort fields.
Usefulness outcomes additionally require the opted-in anonymous marker and
store `useful`, `partially_useful`, or `not_useful` with one to three compatible
fixed reason codes. Complete test-round reviews remain a separate fixed public
test path. None of these paths accepts a question or free text.

Enable field validation only after current consent:

```bash
uvx rock-kb telemetry enable --cohort community --consent-attested
uvx rock-kb install-agent
ROCK_KB_COHORT=external-test uvx rock-kb test-round
ROCK_KB_COHORT=external-test uvx rock-kb test-round --review --submit
ROCK_KB_COHORT=maintainer uvx rock-kb dashboard
```

Restart the host after `install-agent`. Never place a church name, user
identifier, or custom label in the cohort header. Disable participation with
`uvx rock-kb telemetry disable`, rerun the installer, and restart the host.

Structured issue reports are a separate, rate-limited path for service, MCP, CLI, schema, authentication, and retrieval failures. They accept only bounded structured fields plus a short redaction-attested description; descriptions that look like logs, queries, secrets, private paths, or private Rock data are rejected. Reports deduplicate to a stable ID and occurrence count, remain `pending_review`, and never create a GitHub issue automatically. See [Structured Issue Reporting](issue-reporting.md).

Run the hosted evaluation gate after deployment:

```bash
uv run kb eval-service --base-url https://rock-agent-kb.oneandall.church
```

Before merge or deployment, run the same evaluation set against an isolated
local Worker and production-size D1 projection:

```bash
uv run kb quality-gate
```

Each evaluation request receives one bounded retry only when the HTTP transport
times out. Connection failures, HTTP errors, malformed responses, and ranking
failures are never retried. The report separates availability from retrieval
quality: unavailable cases fail the availability gate, while available cases
must have zero failed questions, MRR of at least `0.99`, recall at the target
rank of `1.0`, duplicate rate of `0`, and authority correctness of `1.0`.
Ranking remains strict even when a timeout retry recovers. The gate writes its report to
`service/dist/lexical-quality-gate.json`. Pull-request and production-deploy
workflows run this gate before changes can reach the hosted Worker.

To evaluate semantic retrieval without changing production routing, build the
stratified contextual payload first, then apply it to the isolated AI Search
shadow instance:

```bash
uv run kb hybrid-shadow
uv run kb hybrid-shadow --apply
```

The full report is ignored at `service/dist/hybrid-shadow-results.json`. Keep
the D1 lexical path primary unless the curated shadow cohort improves on lexical
MRR and recall without regressing authority correctness, duplicate rate,
latency, or cost. Exact model-map lookup remains lexical-only by design.

The July 17, 2026 shadow did not meet that bar and its instance was deleted.
See [Hybrid Retrieval Shadow Decision](../decisions/hybrid-shadow-evaluation-2026-07-17.md).
Do not recreate it without a materially different experiment and a new active
lifecycle record.

Every managed shadow instance must be listed in
`service/shadow-lifecycle.yaml` with a public-safe purpose, owner, review date,
expiration date, deletion action, and `production_routing: false`. Check the
policy with:

```bash
uv run kb shadow-lifecycle --strict
```

Scheduled network operations and production deployment enforce the policy.
An expired instance blocks those workflows until it is deleted or a documented
active experiment extends both lifecycle dates.

The evaluation set combines generated answer-structure checks with authored
real-world retrieval cases from `evaluations/real-world.jsonl`. Curated cases
can require an exact result ID, result kind, concept rank, and source-supported
terms. Add cases when a real agent query routes poorly; do not weaken a case to
preserve a perfect score.

The evaluator requests five search results per question and, by default,
requires the expected concept to appear in the top two results
(`--target-rank 2`). It runs hosted searches concurrently with a conservative
default of six concurrent requests. Use `--concurrency` only when intentionally
tuning the gate; excessive concurrency can create avoidable D1/Worker request
timeouts.

## Network Operations

`.github/workflows/network-operations.yml` is the non-secret hosted-service
monitor. It runs on a schedule and can be triggered manually with an optional
`base_url` input. The workflow delegates its probes to
`scripts/network_operations_smoke.py`, which is covered by local regression
tests. The smoke path checks:

- `GET /health`
- `GET /manifest.json`
- `GET /operations/dashboard`
- `kb eval-service --limit 5 --target-rank 2`
- `POST /mcp` tool listing for the expected read and intake tools
- `POST /submit` without a valid token, which must be rejected rather than
  opening a PR or returning a server error

This workflow does not deploy Cloudflare resources and does not require private
corpus access. It is the public uptime/regression signal for the hosted read
service and autonomous intake boundary between deploys.

Run the full Agent Knowledge Network milestone gate when deciding whether the hosted read service, contribution intake, network operations, and laptop-free private corpus path are actually complete:

```bash
uv run kb network-readiness --repo ONE-ALL-Church/rock-agent-kb --pr 2 --private-corpus-path /path/to/private-corpus
```

Use `--strict` in automation when incomplete live gates should fail the run. The command checks the repo-side implementation, PR approval state, deploy secrets/variables, auto-merge policy, reviewed-org count, and private-corpus restore artifacts.
Set `ROCK_KB_NETWORK_READINESS_TIMEOUT` to tune the per-command timeout. The
default is 120 seconds so the full hosted evaluation suite can complete while a
stalled probe still fails instead of hanging the readiness job indefinitely.
The private-corpus restore check intentionally redacts the mounted checkout path
in its JSON evidence so readiness output can be pasted into public PRs without
leaking local or private repo paths.

For the second-org milestone, do not mark an example or placeholder org as
reviewed. The readiness gate expects two real reviewed orgs that also have
public contribution evidence under `community-contributions/<org-id>/` or
`contributions/<org-id>/`. Registry approval alone is not enough.

Operational review artifacts remain in the public repo and are deployed as normal artifacts:

- `agent/source-conflicts.jsonl`: claim pairs with shared topic terms and opposing operational language.
- `agent/claim-review-queue.jsonl`: promotion, merge, and live-verification review queue.
- `agent/section-status.jsonl`: section-level citation, confidence, and staleness hints.
- `agent/evaluation-set.jsonl`: hosted-service regression questions.

The hosted service should expose these through manifest/artifact retrieval, but answer synthesis must still prefer higher authority tiers over community rows.

## Terminal Client

The thin consumer client lives under `clients/python/` and is published to PyPI
as `rock-kb`:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb concepts
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb test-round
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

To test unreleased client changes directly from GitHub, use the Git-backed
`uvx --from` form:

```bash
uvx --from 'git+https://github.com/ONE-ALL-Church/rock-agent-kb#subdirectory=clients/python' rock-kb search "check-in labels not printing"
```

Set `ROCK_KB_URL` to use staging. Set `ROCK_KB_TOKEN` for `rock-kb submit`.

To release a new PyPI version, bump `clients/python/pyproject.toml`, then run
`.github/workflows/release-client.yml` from `main` after merge. The workflow
builds the wheel and source distribution, smoke-tests both, and publishes via
PyPI trusted publishing. Tags such as `rock-kb-v0.1.0` are useful release
markers, but the `production` environment currently allows protected branches,
so the publish job should be run from `main`.
