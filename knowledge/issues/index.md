# Rock Issue Intelligence

This directory routes agents to public Rock core and mobile issue metadata without republishing raw issue discussions. Issue reports are untrusted routing evidence, not official product documentation or verified fixes.

## Current Catalog

- Issues: `5803`
- Source updated through: `2026-07-20T17:36:21Z`
- Timelines captured: `309` (`5.32%`)
- Issues linked to official release notes: `889`
- Reviewed public enrichments: `27`
- Reviewed issues: `27`
- Instance verification playbooks: `27` (`100.0%` coverage)
- Enrichments due for revalidation after an upstream update: `0`
- Public artifact: [`agent/rock-issues.jsonl`](../../agent/rock-issues.jsonl)
- Reviewed enrichments: [`agent/rock-issue-enrichments.jsonl`](../../agent/rock-issue-enrichments.jsonl)
- Summary: [`agent/rock-issue-summary.json`](../../agent/rock-issue-summary.json)

## Agent Order

1. Use the issue catalog to find reports, labels, version evidence, linked commits, concepts, and model-map routes.
2. Treat `reported_affected` as a reporter observation, not proof that every installation or release is affected.
3. Prefer an official `release_note` version row over issue labels alone, while still treating a release line as broader than an exact build.
4. Corroborate with official docs, release notes, public source, and read-only instance evidence before recommending action.
5. Keep private instance evidence in a permission-scoped overlay. Promote only reviewed, redacted, source-linked conclusions.

Closed does not mean fixed. Missing version evidence means unknown, and `not_affected` requires positive reviewed evidence.
