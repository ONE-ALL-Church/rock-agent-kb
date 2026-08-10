# Rock Issue Intelligence

This directory routes agents to public Rock core and mobile issue metadata without republishing raw issue discussions. Issue reports are untrusted routing evidence, not official product documentation or verified fixes.

## Current Catalog

- Issues: `5838`
- Source updated through: `2026-08-09T19:26:49Z`
- Timelines captured: `544` (`9.32%`)
- Issues linked to official release notes: `889`
- Reviewed public enrichments: `28`
- Reviewed issues: `28`
- Instance verification playbooks: `28` (`100.0%` coverage)
- Reviewed applicability prerequisites: `6`
- Reviewed risk assessments: `0`
- Enrichments due for revalidation after an upstream update: `4`
- Public artifact: [`agent/rock-issues.jsonl`](../../agent/rock-issues.jsonl)
- Reviewed enrichments: [`agent/rock-issue-enrichments.jsonl`](../../agent/rock-issue-enrichments.jsonl)
- Summary: [`agent/rock-issue-summary.json`](../../agent/rock-issue-summary.json)

## Agent Order

1. Assess `open` issues by default. Request `historical-unresolved` or `all-relevant` explicitly when preparing upgrades or investigating older behavior.
2. Use the issue catalog to find reports, labels, version evidence, linked commits, concepts, model-map routes, and reviewed prerequisites.
3. Treat `reported_affected` as a reporter observation, not proof that every installation or release is affected.
4. Prefer an official `release_note` version row over issue labels alone, while still treating a release line as broader than an exact build.
5. Keep risk `unrated` unless it comes from an upstream priority label or a current reviewed risk assessment.
6. Read `catalog.status` and `catalog.warning` before relying on a result, then use the linked read-only verification playbook where available.
7. Corroborate with official docs, release notes, public source, and read-only instance evidence before recommending action.
8. Keep private instance evidence in a permission-scoped overlay. Promote only reviewed, redacted, source-linked conclusions.

Closed does not mean fixed. Missing version evidence means unknown, and `not_affected` requires positive reviewed evidence.
