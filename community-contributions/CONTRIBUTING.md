# Contributing Community Knowledge

Community contribution bundles are public-safe JSONL files that suggest reusable Rock RMS guidance for this knowledge base. They are reviewed by maintainers before they affect generated guides or agent answers.

## Where To Contribute

Create or update:

```text
community-contributions/<org-id>/bundle.jsonl
```

Use a stable lowercase `org-id` with letters, numbers, dashes, or underscores. If the organization should stay anonymous, use a stable non-identifying value such as `anonymous-west-001` and set `org_display_name` to `Anonymous Organization`.

The planned public org registry lives under `orgs/<org-id>.yaml`. Until that registry validator and server-side GitHub rulesets are active, every public contribution PR requires maintainer review.

For lightweight source ideas without a full bundle, add notes under:

```text
source-suggestions/<org-id>/
```

Do not edit generated paths such as `agent/`, `claims/`, `concepts/`, `contributions/`, `knowledge/`, `sources/`, or `public-export-manifest.json`.

## Bundle Row Fields

Each line in `bundle.jsonl` is one JSON object with:

- `schema`: must be `rock-kb-org-contribution-v1`
- `contribution_id`: stable id such as `example-org:workflow-timeout-pattern`
- `org_id`: must match the folder name; `community-contributions/test-org/bundle.jsonl` may contain only rows with `org_id: test-org`
- `org_display_name`: public display name or `Anonymous Organization`
- `contribution_type`: one of `task_card`, `troubleshooting_pattern`, `release_caveat`, `entity_note`, `guide_section`, `source_link`, `open_question`
- `concept_ids`: one or more KB concept ids
- `title`: short public-safe title
- `distilled_summary`: newly written public-safe guidance
- `source_urls`: public source URLs, or an empty list when using `source_record_ids`
- `source_record_ids`: source ids from this KB, or an empty list when using `source_urls`
- `confidence`: one of `low`, `medium`, `high`, `needs_review`
- `review_status`: `redaction_reviewed` or `approved_for_public_distillation`
- `needs_live_verification`: `true` when local config, plugins, custom code, or Rock version may change behavior
- `redaction_attestation`: `true` after private details are removed
- `license_attestation`: `true` only if you have rights to submit the summary and sources

## Rules

- Write original summaries; do not copy private docs, transcripts, SQL exports, chat logs, staff notes, screenshots, or vendor material.
- Use canonical public source URLs when possible.
- Do not include private paths, direct media file URLs, HLS manifests, tokenized player URLs, secrets, staff/person data, internal Rock ids, or organization-only operational details.
- Submissions remain community-tier evidence after acceptance unless maintainers later verify the claim against stronger sources.
- Do not assume auto-merge. Automated acceptance is allowed only after org registration, server-side path restrictions, and required checks are active.

## Agent Submission Flow

Agents from other organizations should keep pull requests narrow and reviewable:

1. Change only `community-contributions/<org-id>/bundle.jsonl` or `source-suggestions/<org-id>/`.
2. Include a short PR summary listing the concepts touched and source URLs used.
3. Do not rebuild generated files in the PR. Maintainers rebuild `agent/`, `claims/`, `concepts/`, and `knowledge/` after review.
4. Treat local-instance observations as examples unless the row explicitly says `needs_live_verification: true`.
5. Keep organization-specific operational details generalized unless the organization intentionally wants them public.

## Validate

Run this before opening a PR:

```bash
python scripts/validate_bundle.py
```

The PR workflow runs the same validator for changes under `community-contributions/**` and `source-suggestions/**`.
