# Contribution Module Runbook

This runbook is the canonical map for organization and community contributions. It documents the current code path; later schema and state-machine tasks should update this file when the enforcement layer changes.

## Boundary Contract

| Stage | Artifact | Location | Visibility |
|---|---|---|---|
| 1. Scan | Raw scan rows from a private repo (`kb private scan`) | `data/review/private-scan-<repo-name>.jsonl` | Private: gitignored review data; may summarize private text and private paths |
| 2. Distill | Concept-routed draft candidates (`kb private distill`) | `data/review/private-distill/<source-id>-<concept-id>.jsonl` | Private: draft wording, not public-safe |
| 3. Rewrite | Reviewer-authored public-safe rewrites | `data/review/rewrites/*.jsonl` | Private: input to promotion |
| 4. Promote | Attested public bundle rows (`kb contributions promote --reviewed --redaction-attestation --license-attestation`) | `contributions/<org-id>/bundle.jsonl` | Public in this build repo: first public artifact in the chain |
| 5. Outside-org intake | Bundles and source suggestions submitted to the public repo | `community-contributions/<org-id>/bundle.jsonl`, `source-suggestions/<org-id>/` | Public and untrusted: candidate material, never auto-trusted |
| 6. Validate | Accepted public bundles are validated in this single public repo before maintainer promotion | `community-contributions/<org-id>/`, `source-suggestions/<org-id>/` | Public and untrusted: candidate material until reviewed |
| 7. Build | Contribution rows become claims, then guides, agent pack, and the public surface | `claims/`, `knowledge/`, `agent/`, `concepts/`, `sources/` | Public: community authority tier stays visible and is never relabeled as official |

Nothing crosses from stage 3 to stage 4 without an approved public review status plus redaction and license attestations. No public row may carry private paths, raw transcript text, secrets, tokenized or HLS media URLs, or non-generalized organization-internal details.

## Lifecycle Vocabulary

Current contribution rows use `schema: rock-kb-org-contribution-v1`.

Contribution types:

- `task_card`
- `troubleshooting_pattern`
- `release_caveat`
- `entity_note`
- `guide_section`
- `source_link`
- `open_question`

Review statuses:

- `draft_private`: private draft from scan or template output; not valid as a public bundle row.
- `needs_followup`: staging row that still needs reviewer rewrite, source links, or attestations.
- `redaction_reviewed`: reviewer has rewritten/redacted the row for public use.
- `approved_for_public_distillation`: reviewer has approved the row for public distillation.
- `rejected_private`: private row should not be promoted.

Public bundle validation currently accepts only:

- `redaction_reviewed`
- `approved_for_public_distillation`

Confidence values:

- `low`
- `medium`
- `high`
- `needs_review`

Required public bundle fields are enforced in `src/rock_kb/contributions.py`: `schema`, `contribution_id`, `org_id`, `concept_ids`, `contribution_type`, `title`, `distilled_summary`, `source_urls`, `source_record_ids`, `redaction_attestation`, `review_status`, `license_attestation`, `confidence`, and `needs_live_verification`.

## End-To-End Example

Scan a private repo into the private review queue:

```bash
uv run kb private scan \
  --repo /path/to/private-rock-material \
  --source-id private_rock_repo_candidates \
  --org-id example-org
```

Review the sanitized scan report:

```bash
uv run kb private review-report \
  --scan-path data/review/private-scan-private-rock-material.jsonl \
  --source-id private_rock_repo_candidates \
  --org-id example-org
```

Distill eligible rows for one concept:

```bash
uv run kb private distill \
  --scan-path data/review/private-scan-private-rock-material.jsonl \
  --source-id private_rock_repo_candidates \
  --concept workflows \
  --org-id example-org
```

Write reviewer-authored rewrites under `data/review/rewrites/`. The rewrite file should reference the private draft `contribution_id` and provide newly written public text:

```json
{"contribution_id":"private-distill:<id>","title":"Workflow launch troubleshooting pattern","distilled_summary":"Newly written public-safe guidance with no copied private text, no staff names, no internal IDs, and no private paths.","source_urls":["https://community.rockrms.com/documentation"],"source_record_ids":[],"confidence":"medium","needs_live_verification":true}
```

Promote reviewed rows into a public build-repo bundle:

```bash
uv run kb contributions promote \
  --draft-path data/review/private-distill/private_rock_repo_candidates-workflows.jsonl \
  --org-id example-org \
  --rewrite-file data/review/rewrites/example-org-workflows.jsonl \
  --reviewed \
  --redaction-attestation \
  --license-attestation \
  --review-status redaction_reviewed \
  --output contributions/example-org/bundle.jsonl
```

Validate and summarize the bundle:

```bash
uv run kb contributions validate --path contributions/example-org/bundle.jsonl
uv run kb contributions check --path contributions/example-org
```

Rebuild the public layers:

```bash
uv run kb status
ROCK_KB_GENERATED_AT=<iso timestamp> uv run kb build
uv run kb audit public-export
```

Use targeted `uv run kb build --stage <stage>` only when the status plan says a specific stage is stale and you intentionally want that smaller rebuild.

## Public Repo Contributor Scope

In the public community repo, contributors and outside agents may edit only:

- `community-contributions/<org-id>/`
- `source-suggestions/<org-id>/`

They should not edit generated public export paths:

- `agent/`
- `claims/`
- `concepts/`
- `contributions/`
- `knowledge/`
- `sources/`
- `public-export-manifest.json`

Maintainers validate accepted single-repo intake bundles before promotion:

```bash
python scripts/validate_bundle.py
uv run kb contributions check --path contributions
```

The PR workflow runs `python scripts/validate_bundle.py` for changes under `community-contributions/**` and `source-suggestions/**`. Accepted community material remains community-tier evidence unless a later reviewer and stronger evidence promote related claims under the normal claim-tier policy.

## Contribution Validator

The stdlib validator and PR workflow live at their real single-repo paths:

```bash
scripts/validate_bundle.py
.github/workflows/validate-contributions.yml
community-contributions/CONTRIBUTING.md
```

Run this locally before opening or reviewing an intake PR:

```bash
python scripts/validate_bundle.py
```

## Reviewer Gate

Before promotion, verify:

- The row is a reusable Rock RMS pattern, caveat, task card, source link, entity note, guide section, or open question.
- The public text is newly written or safely paraphrased; it is not copied from private docs, raw transcripts, SQL exports, chat logs, staff notes, or internal runbooks.
- `source_urls` or `source_record_ids` point to public or otherwise allowed sources.
- `redaction_attestation` and `license_attestation` are affirmative.
- `concept_ids` are specific and exist in `concepts/registry.yaml`.
- The row contains no private paths under `data/review/`, `data/media/`, `data/normalized/`, `data/raw-manifests/`, or `data/index/`.
- The row contains no direct media file URL, tokenized player URL, HLS manifest, secret-like value, or raw transcript marker.

Run these gates before public export:

```bash
uv run kb contributions validate --path contributions
uv run kb audit public-export
```
