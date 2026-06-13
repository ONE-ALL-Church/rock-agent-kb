# Organization Registry

This folder is the public registry for organizations that contribute Rock KB bundles.

Registration is reviewed once by maintainers. After that, automated intake can validate the org identity, token, and path boundary before opening a contribution PR.

Repository auto-merge capability can be enabled without allowing every intake PR to merge automatically. The hosted Worker attempts auto-merge only when all of these are true:

- the Worker runtime flag explicitly enables intake auto-merge;
- the org registry sets `intake.auto_merge_allowed: true` for that reviewed org;
- the generated PR changes exactly one eligible file under `community-contributions/<org-id>/`.

Leave `intake.auto_merge_allowed: false` until the organization has enough reviewed submissions to trust its automated path.

Only `status: reviewed` organizations are accepted by hosted `kb_submit`. `pending` rows are examples or registration requests and must not receive live submission tokens.

Registration files use:

```text
orgs/<org-id>.yaml
```

New organizations can start with the "Register a contributing organization"
GitHub issue template, then open a PR that adds the matching registry file.

Use a stable lowercase `org-id` with letters, numbers, dashes, or underscores. The same id should be used for:

```text
community-contributions/<org-id>/bundle.jsonl
source-suggestions/<org-id>/
```

Do not include private database details, instance URLs, staff contact details, access tokens, internal repo links, or confidential operational context in registry files. Public contact and GitHub organization/team handles are acceptable when the contributor wants them public.

Required fields:

- `schema: rock-kb-org-v1`
- `org_id`: lowercase slug matching the filename.
- `display_name`: public organization name.
- `status`: `pending`, `reviewed`, or `suspended`.
- `github_accounts`: GitHub users or app identities allowed to submit.
- `standing_attestations.redaction`: public-redaction obligation accepted.
- `standing_attestations.license`: source/license obligation accepted.

Submit tokens are never stored here. The hosted Worker reads per-org token SHA-256 digests from the `ORG_TOKEN_SHA256_JSON` secret.

Maintainers can update the digest JSON without printing raw tokens:

```bash
printf '%s' "$RAW_SUBMIT_TOKEN" \
  | python3 scripts/update_org_token_digest.py \
      --org-id <org-id> \
      --existing-json "$ORG_TOKEN_SHA256_JSON" \
  | gh secret set ORG_TOKEN_SHA256_JSON \
      --repo ONE-ALL-Church/rock-agent-kb \
      --env production
```

Use a new high-entropy token per organization and deliver the raw token outside
git. Only the SHA-256 digest JSON belongs in the hosted secret.
