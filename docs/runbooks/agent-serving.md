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

`--apply` uploads the versioned R2 artifact payload first, then seeds the remote D1 database with `--remote`, then deploys the Worker. That order prevents the live Worker from flipping to a new `current_version` before the matching artifacts exist.

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
- `GET /search?q=<query>&min_tier=routing_context_only`
- `GET /operations/dashboard`
- `POST /mcp`
- `POST /submit`

When a reviewed public bundle under `community-contributions/<org-id>/` merges to `main`, the deploy workflow revalidates orgs and bundles, rebuilds the service projection, and includes those rows in hosted search as `kind: community_contribution`, `authority_tier: community-unreviewed`, and `claim_tier: routing_context_only`. `GET /search` and `kb_get_claims` include them by default; `GET /concepts/<concept-id>.md` and `kb_get_concept` continue to serve reviewed guide artifacts only.

`GET /operations/dashboard` and the `kb_review_dashboard` MCP tool expose public operational counts for the claim-review queue, source-conflict queue, community-unreviewed intake rows, section status, answer evaluation results, and aggregate telemetry. It summarizes already-public artifacts plus D1 row metadata; it does not expose private corpus files or raw query text.

Run the hosted evaluation gate after deployment:

```bash
uv run kb eval-service --base-url https://rock-agent-kb.oneandall.church
```

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
default is 45 seconds so a stalled hosted probe fails with evidence instead of
hanging the readiness job indefinitely.
The private-corpus restore check intentionally redacts the mounted checkout path
in its JSON evidence so readiness output can be pasted into public PRs without
leaking local or private repo paths.

For the second-org milestone, do not mark an example or placeholder org as
reviewed. The readiness gate expects two real reviewed orgs that also have
public contribution evidence under `community-contributions/<org-id>/` or
`contributions/<org-id>/`. Registry approval alone is not enough.

Operational review artifacts remain in the public repo and are deployed as normal artifacts:

- `agent/source-conflicts.jsonl`: community/higher-authority alignment prompts.
- `agent/claim-review-queue.jsonl`: promotion, merge, and live-verification review queue.
- `agent/section-status.jsonl`: section-level citation, confidence, and staleness hints.
- `agent/evaluation-set.jsonl`: hosted-service regression questions.

The hosted service should expose these through manifest/artifact retrieval, but answer synthesis must still prefer higher authority tiers over community rows.

## Terminal Client

The thin consumer client lives under `clients/python/` and is intended to be published as `rock-kb`:

```bash
uvx rock-kb search "check-in labels not printing"
uvx rock-kb concepts
uvx rock-kb get check-in
uvx rock-kb claims workflows --min-tier source_backed
uvx rock-kb dashboard
uvx rock-kb mcp-config
```

Set `ROCK_KB_URL` to use staging. Set `ROCK_KB_TOKEN` for `rock-kb submit`.
