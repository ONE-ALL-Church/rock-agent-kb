# Private And Org Data Integration Plan

## Purpose

The KB should benefit from local church operating knowledge without turning private runbooks, live configuration, staff data, IDs, URLs, or incident history into public source material.

This plan covers two related inputs:

- Owner-private data from `/path/to/private-rock-docs`.
- Outside organization contributions from churches, consultants, vendors, and Rock implementers.

Both inputs enter through private review first. Public output must be newly written, distilled, source-linked, and audit-passing.

The implementation roadmap for turning this policy into commands, review gates, private dependency maps, and public promotion workflow is [org-data-implementation-roadmap.md](org-data-implementation-roadmap.md).

## Principles

- Private raw data is an input corpus, not a publication target.
- Public artifacts may contain generalized guidance, task cards, troubleshooting trees, entities, caveats, and source links.
- Public artifacts must not contain raw private docs, private paths, live Rock IDs, people data, staff emails, phone numbers, secrets, access tokens, internal URLs, or confidential business context.
- Private source hashes may be retained in private review manifests to support rebuilds, but private paths and content should not appear in public export.
- Other orgs should be able to contribute value without exposing their raw internal data.

## Source Families

### Private Organization Docs

Registered source: `rockproduction_docs_private_candidates`

Default command:

```bash
uv run kb private scan \
  --repo /path/to/private-rock-docs \
  --source-id rockproduction_docs_private_candidates \
  --org-id oneall
```

Use `--allowlist <file>` to scan only approved relative paths after a human review pass. The allowlist file should be private and should not be used as a public index of internal docs.

Output:

```text
data/review/private-scan-docs.jsonl
```

Expected classifications:

- `instance_private`: contains sensitive values or obviously instance-specific live configuration.
- `needs_human_review`: contains instance markers such as emails, phone numbers, ONE&ALL identifiers, production hostnames, or Rock numeric IDs.
- `generalizable_pattern`: appears to describe Rock behavior, workflow patterns, Lava, groups, check-in, reports, finance, APIs, or operational practices without detected private markers.
- `source_pointer_only`: useful locally, but not a good public-distillation candidate.

### Outside Org Contributions

Registered source: `outside_org_contribution_candidates`

Outside orgs should run the scanner locally against their private data and submit only a reviewed contribution bundle.

Recommended local workflow for contributors:

```bash
uv run kb private scan --repo <org-private-docs> --source-id outside_org_contribution_candidates --org-id <org-key>
uv run kb private ingest --repo <reviewed-allowlisted-dir> --source-id outside_org_contribution_candidates --org-id <org-key>
uv run kb contributions new --org-id <org-key> --org-display-name "Example Church"
uv run kb contributions check --path contributions/<org-key>
uv run kb contributions validate --path contributions/<org-key>/bundle.jsonl
```

The public repo should accept contribution bundles only after review.

`uv run kb contributions new` creates `bundle.example.jsonl`, which is a non-public template and intentionally skipped by validation. Contributors should copy only the relevant shapes into `bundle.jsonl`, rewrite them as public-safe distilled guidance, add public source links, then run `uv run kb contributions check` or `python scripts/validate_bundle.py` before opening a PR.

## Contribution Bundle Schema

Contribution bundles should be JSONL or Markdown plus JSONL under `contributions/<org-key>/`.

Each contribution row should include:

- `schema`: `rock-kb-org-contribution-v1`
- `contribution_id`
- `org_id`
- `org_display_name` or `anonymous`
- `concept_ids`
- `contribution_type`: `task_card`, `troubleshooting_pattern`, `release_caveat`, `entity_note`, `guide_section`, `source_link`, or `open_question`
- `title`
- `distilled_summary`
- `source_urls`
- `source_record_ids`
- `private_source_hashes`: optional, private review only
- `private_source_paths`: prohibited in public bundles
- `redaction_attestation`
- `review_status`
- `license_attestation`
- `confidence`
- `needs_live_verification`

Allowed `review_status` values:

- `draft_private`
- `redaction_reviewed`
- `approved_for_public_distillation`
- `rejected_private`
- `needs_followup`

## Distillation Workflow

1. Scan private docs into `data/review/*.jsonl`.
2. Review records with `publishability_status`, `review_classification`, `candidate_concepts`, and `risk_flags`.
3. Run `kb private distill` to turn eligible generalizable records into private draft contribution rows.
4. Run `kb contributions promote` without `--reviewed` to create a private staging skeleton.
5. Rewrite staged rows into new public-safe language and provide public source links.
6. Run `kb contributions promote --reviewed --rewrite-file <file> --redaction-attestation --license-attestation` to create a public bundle.
7. Generate new public artifacts such as task cards, guide sections, troubleshooting trees, or open questions.
8. Remove raw copied private text, private paths, IDs, people data, and org-specific labels.
9. Preserve private source hashes in private dependency records.
10. Run public export and audits.

Example:

```bash
uv run kb private distill \
  --scan-path data/review/private-scan-docs.jsonl \
  --source-id rockproduction_docs_private_candidates \
  --concept workflows \
  --org-id oneall
```

This writes private draft rows under `data/review/private-distill/` and private dependency rows under `data/review/private-dependencies/`. These rows are not public contribution bundles until a human redaction/license review promotes them.

Create a private staging skeleton:

```bash
uv run kb contributions promote \
  --draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl \
  --org-id oneall
```

Create a reviewed public bundle only after rewriting the row in a separate reviewer JSONL file:

```bash
uv run kb contributions promote \
  --draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl \
  --org-id oneall \
  --rewrite-file data/review/rewrites/oneall-workflows.jsonl \
  --reviewed \
  --redaction-attestation \
  --license-attestation \
  --output contributions/oneall/bundle.jsonl
```

Reviewed promotion writes private dependency rows under `data/review/private-promotion-dependencies/`. Check local public impact after rescanning private data:

```bash
uv run kb private impact \
  --scan-path data/review/private-scan-docs.jsonl \
  --source-id rockproduction_docs_private_candidates \
  --org-id oneall
```

`kb status` reads these private dependency rows when they exist locally and marks affected concepts as needing rebuild without exposing private paths or source text.

Approved public contribution bundles are included in synthesis packs by default:

```bash
uv run kb concepts synthesize --concept workflows --hydrate-sources --include-contributions --model gpt-5.5
```

Private draft contribution rows are excluded unless explicitly requested for local-only synthesis:

```bash
uv run kb concepts hydrate \
  --concept workflows \
  --include-private-drafts \
  --private-draft-path data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl
```

Private draft packs remain under `data/review/concept-synthesis/` and must not be published.

After a new private scan, check whether private-derived drafts are stale:

```bash
uv run kb private stale \
  --scan-path data/review/private-scan-docs.jsonl \
  --source-id rockproduction_docs_private_candidates \
  --concept workflows
```

The stale report compares private source hashes only. It does not expose raw private content or private paths.

## Agent Rules

Agents may use private review manifests to decide what to inspect locally, but they must not quote or publish private source text.

When using private organization docs or outside-org private material, agents should label derived public guidance as:

- generalized from private operational patterns,
- not official Rock guidance unless backed by official docs/source/release notes,
- needs local verification when behavior depends on a live Rock instance.

## Public Export Requirements

Public export must continue to pass:

```bash
uv run kb contributions check --path contributions/<org-key>
uv run kb contributions validate
uv run kb audit public-export
uv run kb audit licenses
uv run kb audit source-policy
```

Additional bundle audits should fail on:

- raw private paths,
- staff emails or phone numbers,
- secrets or tokens,
- copied private docs,
- live Rock numeric IDs unless intentionally abstracted,
- unreviewed `draft_private` rows,
- missing redaction or license attestations.

## Implementation Next Steps

- Implemented: `kb contributions validate` command for `contributions/**/*.jsonl`.
- Implemented: `kb private distill --source-id <id> --concept <id>` command that reads eligible generalizable private scan records into private draft rows.
- Implemented: `kb contributions promote` command for private staging and reviewed public bundle promotion.
- Implemented: private dependency map rows under `data/review/private-dependencies/`.
- Implemented: `kb private stale` for private-derived draft rows.
- Implemented: private promoted public dependency rows under `data/review/private-promotion-dependencies/`.
- Implemented: `kb private impact` and `concepts stale` integration for changed private source hashes.
- Implemented: approved public contribution bundles flow into concept synthesis by default, while private drafts require explicit local-only flags.
- Add CI checks for contribution bundle schema and privacy rules.
