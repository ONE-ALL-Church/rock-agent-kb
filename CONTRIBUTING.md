# Contributing To The Rock Agent KB

Thanks for helping improve the public Rock RMS knowledge base. Contributions should be public-safe, source-linked, and easy for maintainers and agents to review.

## Choose A Path

### 1. Suggest A Source

Use this when you found a useful public page, doc, video, repo file, release note, recipe, or article but do not want to write a full contribution bundle.

1. Copy `source-suggestions/SUGGESTION_TEMPLATE.md`.
2. Save it as `source-suggestions/<org-id>/<short-topic>.md`.
3. Fill in the source URL, why it matters, and relevant concept IDs if known.
4. Open a PR that only changes files under `source-suggestions/<org-id>/`.

This is the easiest contribution path.

No Rock KB submit token is required for a normal GitHub PR. The contributor only needs a GitHub account that can fork the repo or open a PR. GitHub Actions will run the public validation checks.

### 2. Submit Reviewed Knowledge

Use this when you are submitting a distilled, original, public-safe summary that should eventually feed guides, task cards, claims, or answer packs.

Generate a starter JSONL bundle row:

```bash
python3 scripts/new_contribution.py \
  --org-id your-org \
  --org-name "Your Org" \
  --concept workflows \
  --type troubleshooting_pattern \
  --title "Workflow launch triage pattern" \
  --summary "When a workflow does not launch, first verify the trigger, active workflow type, entity context, action logs, and idempotency of notifications or webhooks before changing configuration." \
  --source-url https://community.rockrms.com/documentation \
  --needs-live-verification \
  --redaction-reviewed \
  --license-attested
```

Then validate:

```bash
python3 scripts/validate_bundle.py community-contributions/your-org
```

Open a PR that only changes files under `community-contributions/<org-id>/`.

No Rock KB submit token is required when the bundle is submitted as a GitHub PR. A token is required only for hosted agent submission through the KB service.

## Hosted Agent Auth

Contributor agents that submit through the hosted `kb_submit` endpoint use per-organization auth:

1. The organization opens the "Register a contributing organization" GitHub issue.
2. Maintainers review the request and add `orgs/<org-id>.yaml` with `status: reviewed`.
3. Maintainers generate a high-entropy submit token for that org.
4. Maintainers store only the token's SHA-256 digest in the hosted `ORG_TOKEN_SHA256_JSON` secret.
5. The raw token is delivered to the organization outside git.
6. The contributor agent sends the token as `ROCK_KB_TOKEN`, `ROCK_KB_TOKEN_FILE`, `--token-file`, `--token-stdin`, or an HTTP `Authorization: Bearer <token>` value when calling hosted submit.

Recommended local agent usage:

```bash
printf '%s' '<issued-token>' > ~/.rock-kb-<org-id>.token
chmod 600 ~/.rock-kb-<org-id>.token
rock-kb auth-check --org <org-id> --token-file ~/.rock-kb-<org-id>.token
rock-kb submit bundle.jsonl --token-file ~/.rock-kb-<org-id>.token --dry-run
rock-kb submit bundle.jsonl --token-file ~/.rock-kb-<org-id>.token
```

`rock-kb submit` infers `--org` from the bundle when all rows use the same `org_id`.

For CI, hosted agents, or app connectors, store the token as a secret named `ROCK_KB_TOKEN` or mount it as a secret file and set `ROCK_KB_TOKEN_FILE`. Do not put submit tokens in repo files, bundle rows, issues, PRs, screenshots, transcripts, prompt files, `.env`, or checked-in agent instructions. If a token is exposed, ask a maintainer to rotate it.

## Public Safety Rules

- Write original summaries. Do not paste private docs, transcripts, SQL exports, chat logs, screenshots, staff notes, vendor text, or proprietary material.
- Include public source URLs or existing KB source record IDs.
- Keep local-instance observations generalized unless your organization intentionally wants the operational detail public.
- Set `--needs-live-verification` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.
- Do not edit generated folders such as `agent/`, `claims/`, `concepts/`, `contributions/`, `knowledge/`, or `sources/`.

Maintainers review accepted rows, promote them into the build input, rebuild generated artifacts, and run the public-surface audits.
