## Contribution Safety Checklist

- [ ] I did not add raw private docs, exports, transcripts, SQL dumps, screenshots, staff notes, live IDs, internal URLs, secrets, or copied proprietary material.
- [ ] Every public contribution row is newly written, redaction-reviewed, license-attested, and includes `source_urls` or `source_record_ids`.
- [ ] Community or org-derived guidance is presented as an example or pattern, not official Rock guidance.
- [ ] Rows that depend on local configuration set `needs_live_verification` to `true`.
- [ ] For public-repo contribution PRs, I changed only `community-contributions/<org-key>/` or `source-suggestions/<org-key>/`.
- [ ] For bundle PRs, I ran `python3 scripts/validate_bundle.py community-contributions/<org-key>`.

## Maintainer Checklist

- [ ] Run `uv run kb contributions check --path community-contributions/<org-key>` or `uv run kb contributions check --path contributions/<org-key>` as appropriate.
- [ ] Run `uv run kb audit source-url-duplicates`.
- [ ] Run `uv run kb audit public-export`.

## Notes

Describe what concept(s) this changes and whether the contribution should influence guide synthesis, task cards, source maps, or open questions.
