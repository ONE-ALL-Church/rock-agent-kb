# Community Contributions

This folder is the public intake area for churches, consultants, vendors, and agents from other organizations.

Submit reviewed, public-safe JSONL bundles here:

```text
community-contributions/<org-id>/bundle.jsonl
```

Use `community-contributions/example-org/bundle.example.jsonl` as a row-shape reference. Example rows are intentionally marked `draft_private`; copy the relevant shape into your own `bundle.jsonl`, rewrite it with reviewed public-safe content, and set the review and attestation fields before submitting.

Use this folder for proposed knowledge that should flow back into the canonical build repo. Do not edit generated `agent/`, `knowledge/`, `claims/`, `sources/`, `concepts/`, or `contributions/` files directly in the public repo.

Accepted rows must:

- Use schema `rock-kb-org-contribution-v1`.
- Be newly written public-safe summaries, not copied private docs or transcripts.
- Include `source_urls` or `source_record_ids`.
- Set `redaction_attestation` and `license_attestation` to `true`.
- Use `review_status` of `redaction_reviewed` or `approved_for_public_distillation`.
- Set `needs_live_verification` to `true` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.

Validate locally before opening a PR:

```bash
python scripts/validate_bundle.py community-contributions/<org-id>/bundle.jsonl
```

The PR workflow runs the same validator for contribution and source-suggestion changes. Accepted rows remain community-tier evidence until promoted by the review workflow.

Maintainers use `uv run kb contributions validate`, `uv run kb contributions promote`, and the normal `uv run kb build` stages when reviewing or promoting accepted contribution rows.
