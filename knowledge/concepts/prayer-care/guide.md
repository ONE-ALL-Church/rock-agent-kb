---
id: authored-prayer-care
title: Prayer And Care
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Prayer And Care

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Prayer And Care index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept for prayer requests, prayer teams, care follow-up, request visibility, moderation, categories, communication, and privacy-sensitive ministry workflows.

The primary official branch is `documentation/engagement/prayer` ([Prayer](https://community.rockrms.com/documentation/engagement/prayer)). This should be a first-class concept because prayer and care workflows have distinct privacy, security, communication, and ministry-follow-up concerns that are easy to lose inside broad engagement or groups guidance.

Agents should assume prayer and care data can be sensitive. Before changing visibility, communication, or automation, inspect security, category settings, moderation behavior, notification recipients, and whether the content should be public, staff-only, team-only, or confidential.

## 2. Agent Workflow

Start by determining whether the user is asking about request submission, request approval, team assignment, communication, follow-up, reporting, or security ([Prayer Overview](https://community.rockrms.com/documentation/engagement/prayer/prayer-overview)).

For troubleshooting, inspect the request category, campus or group association, approval state, expiration/archive behavior, page/block settings, security roles, and communication settings. If a person cannot see or manage a request, check both page/block access and data-level visibility.

For automation, prefer conservative workflows that minimize unnecessary disclosure. Avoid sending prayer text into broad communication channels unless the request category and consent expectations support that behavior.

## 3. Boundaries

Do not include real prayer request text, names, pastoral notes, health details, or care history in public contributions. Distill only generic patterns and cite public documentation ([Prayer](https://community.rockrms.com/documentation/engagement/prayer)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `2`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Prayer Requests Transcript Insight](https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests) | approved_for_public_distillation | 2 | media-insight:762111bd5a9d1218 |
| [Rapid Attendance Entry Transcript Insight](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) | approved_for_public_distillation | 3 | media-insight:f131f156d62b7d38 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 4. Source Map And Dependency Notes

Durable official routing:

- `documentation/engagement/prayer`

Use Groups for team membership, Communications for notifications, Workflows for custom follow-up, and Security And Permissions for visibility and authorization questions ([Prayer](https://community.rockrms.com/documentation/engagement/prayer)).
