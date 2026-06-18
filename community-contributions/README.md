# Community Contributions

This folder is the public intake area for churches, consultants, vendors, and agents from other organizations.

Submit reviewed, public-safe JSONL bundles here:

```text
community-contributions/<org-id>/bundle.jsonl
```

Use `community-contributions/example-org/bundle.example.jsonl` as a row-shape reference. Example rows are intentionally marked `draft_private`; copy the relevant shape into your own `bundle.jsonl`, rewrite it with reviewed public-safe content, and set the review and attestation fields before submitting.

Use this folder for proposed knowledge that should flow back into the canonical build repo. Do not edit generated `agent/`, `knowledge/`, `claims/`, `sources/`, `concepts/`, or `contributions/` files directly in the public repo.

## Agent Checklist

1. Pick a stable `org-id` and create `community-contributions/<org-id>/bundle.jsonl`.
2. Copy only the relevant row shape from `community-contributions/example-org/bundle.example.jsonl`.
3. Rewrite the content as an original public-safe summary. Do not paste raw source text, transcripts, screenshots, SQL, or private notes.
4. Add public `source_urls` or KB `source_record_ids` for every row.
5. Set `redaction_attestation`, `license_attestation`, and `review_status` only after a reviewer has checked the row.
6. Run `python scripts/validate_bundle.py community-contributions/<org-id>/bundle.jsonl`.
7. Open a PR that changes only `community-contributions/<org-id>/` or `source-suggestions/<org-id>/`.

Accepted rows must:

- Use schema `rock-kb-org-contribution-v1`.
- Match `org_id` to the folder name. The validator rejects bundles whose rows claim a different organization than the `community-contributions/<org-id>/` path.
- Be newly written public-safe summaries, not copied private docs or transcripts.
- Include `source_urls` or `source_record_ids`.
- Set `redaction_attestation` and `license_attestation` to `true`.
- Use `review_status` of `redaction_reviewed` or `approved_for_public_distillation`.
- Set `needs_live_verification` to `true` when behavior depends on local configuration, plugins, custom code, or a specific Rock version.

Validate locally before opening a PR:

```bash
python scripts/validate_bundle.py community-contributions/<org-id>/bundle.jsonl
```

The PR workflow runs the same validator for contribution and source-suggestion changes, including the `org_id` path-boundary check. Accepted rows remain candidate/community-tier evidence until maintainers import, promote, rebuild, and audit the generated public surface.

Maintainers use `uv run kb contributions validate`, `uv run kb contributions promote`, and the normal `uv run kb build` stages when reviewing or promoting accepted contribution rows.
