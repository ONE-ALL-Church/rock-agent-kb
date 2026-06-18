## Contribution Safety Checklist

- [ ] I did not add raw private docs, exports, transcripts, SQL dumps, screenshots, staff notes, live IDs, internal URLs, secrets, or copied proprietary material.
- [ ] Every public contribution row is newly written, redaction-reviewed, and license-attested.
- [ ] Every public contribution row includes `source_urls` or `source_record_ids`.
- [ ] Community or org-derived guidance is presented as an example or pattern, not official Rock guidance.
- [ ] Rows that depend on local configuration set `needs_live_verification` to `true`.
- [ ] For public-repo contribution PRs, I used `community-contributions/<org-key>/bundle.jsonl` rather than editing generated files.
- [ ] I ran `uv run kb contributions check --path community-contributions/<org-key>` or `uv run kb contributions check --path contributions/<org-key>` as appropriate.
- [ ] I ran `uv run kb audit source-url-duplicates`.
- [ ] I ran `uv run kb audit public-export`.

## Notes

Describe what concept(s) this changes and whether the contribution should influence guide synthesis, task cards, source maps, or open questions.
