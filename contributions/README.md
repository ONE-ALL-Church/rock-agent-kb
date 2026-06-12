# Contributions

This directory is for reviewed, public-safe contribution bundles from churches, consultants, vendors, and Rock implementers.

Do not place raw private docs, exports, transcripts, SQL dumps, screenshots, staff notes, live IDs, internal URLs, secrets, or copied proprietary material here.

In the public community repo, new external PRs should target `community-contributions/<org-id>/bundle.jsonl`, not this generated/imported `contributions/` directory. The public example bundle lives at `community-contributions/example-org/bundle.example.jsonl`. Maintainers import accepted public bundles back into this canonical build repo with:

```bash
uv run kb contribution-import-public --public-repo <public-repo-checkout>
```

After import, this directory becomes the reviewed contribution layer that guide synthesis and generated agent artifacts may use.

The implementation roadmap for owner-private and outside-org data is:

- [Org Data Implementation Roadmap](../docs/org-data-implementation-roadmap.md)

Public contribution bundles must be JSONL and pass:

```bash
uv run kb contribution-new --org-id <org-key> --org-display-name "Example Church"
uv run kb contribution-check --path contributions/<org-key>
uv run kb contribution-validate --path contributions/<org-key>/bundle.jsonl
uv run kb audit-public-export
```

For public-repo contributors, the equivalent validation target is:

```bash
uv run kb contribution-check --path community-contributions/<org-key>
```

Private material should be scanned and distilled locally first:

```bash
uv run kb private-scan --repo <private-docs> --source-id outside_org_contribution_candidates --org-id <org-key>
uv run kb private-review-report --scan-path data/review/private-scan-<name>.jsonl --source-id outside_org_contribution_candidates --org-id <org-key>
uv run kb distill-private --scan-path data/review/private-scan-<name>.jsonl --source-id outside_org_contribution_candidates --concept <concept-id> --org-id <org-key>
uv run kb contribution-promote --draft-path data/review/private-distill/outside_org_contribution_candidates-<concept-id>.jsonl --org-id <org-key>
```

Only redaction-reviewed, license-attested, source-linked distilled rows should be promoted into this directory.

`contribution-new` writes `bundle.example.jsonl`. That file is a local template and is intentionally skipped by contribution validation until a reviewed row is copied into `bundle.jsonl`.

`contribution-check` is the contributor-facing one-command audit. It validates public bundle rows, reports row counts by concept/type/status/org, lists example templates separately, and exits nonzero when a public bundle is not publishable.

`contribution-promote` writes a private staging skeleton by default. To write a public bundle, provide a reviewer rewrite file and explicit attestations:

```bash
uv run kb contribution-promote \
  --draft-path data/review/private-distill/outside_org_contribution_candidates-<concept-id>.jsonl \
  --org-id <org-key> \
  --rewrite-file data/review/rewrites/<org-key>-<concept-id>.jsonl \
  --reviewed \
  --redaction-attestation \
  --license-attestation \
  --output contributions/<org-key>/bundle.jsonl
```

After promotion, local maintainers can check whether private-derived public rows are stale:

```bash
uv run kb private-impact --scan-path data/review/private-scan-<name>.jsonl --source-id outside_org_contribution_candidates --org-id <org-key>
uv run kb concepts stale
```

Minimum public row shape:

```json
{
  "schema": "rock-kb-org-contribution-v1",
  "contribution_id": "org-key:short-stable-id",
  "org_id": "org-key",
  "org_display_name": "Example Church",
  "concept_ids": ["workflows"],
  "contribution_type": "troubleshooting_pattern",
  "title": "Short public-safe title",
  "distilled_summary": "Newly written public-safe guidance with no copied private text.",
  "source_urls": ["https://community.rockrms.com/documentation"],
  "source_record_ids": [],
  "redaction_attestation": true,
  "review_status": "redaction_reviewed",
  "license_attestation": true,
  "confidence": "medium",
  "needs_live_verification": true
}
```

Public bundles must not include private hashes, private paths, raw text, copied docs, transcripts, staff data, internal URLs, secrets, or live Rock IDs.

## Example Bundle

The local build repo keeps `contributions/example-org/bundle.example.jsonl` as a CLI template, but example bundles under `contributions/` are intentionally excluded from the default public export. Public contributors should use `community-contributions/example-org/bundle.example.jsonl` instead.

The example includes one template row for each contribution type:

- `task_card`
- `troubleshooting_pattern`
- `release_caveat`
- `entity_note`
- `guide_section`
- `source_link`
- `open_question`

These rows are intentionally `draft_private` and are skipped by validation because the filename ends in `.example.jsonl`. Copy the relevant shape into `contributions/<org-key>/bundle.jsonl` in the build repo or `community-contributions/<org-key>/bundle.jsonl` in the public repo, rewrite it with reviewed public-safe content, then set the review and attestation fields.

## Anonymous Orgs

Use a stable non-identifying `org_id` such as `anonymous-west-001` when an organization should not be named publicly. Set `org_display_name` to `Anonymous Organization`. The `org_id` must stay stable so duplicate detection, source maps, and future staleness checks keep working.
