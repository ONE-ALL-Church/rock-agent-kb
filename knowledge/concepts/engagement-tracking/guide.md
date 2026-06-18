---
id: authored-engagement-tracking
title: Engagement Tracking
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Engagement Tracking

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Engagement Tracking index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept for Steps, Step Programs, Step Types, Streaks, Assessments, Achievements, badges, completion signals, journey-style tracking, and engagement reporting.

The durable official branches are:

- `documentation/engagement/steps` ([Steps](https://community.rockrms.com/documentation/engagement/steps))
- `documentation/engagement/streaks`
- `documentation/engagement/assessments`
- `documentation/engagement/additional-engagement-tools`

This concept is separate from Learning, LMS, And Engagement because these branches describe broad ministry engagement signals, not course/class training delivery. Use LMS when the unit of work is a course, class, learning activity, or program completion. Use Engagement Tracking when the unit of work is a milestone, behavior, assessment, achievement, or participation signal.

## 2. Agent Workflow

Start by identifying the tracking primitive: step, streak, assessment, achievement, badge, or report. Then identify the person, program/type configuration, date or occurrence, source automation, and reporting surface ([Assessments](https://community.rockrms.com/documentation/engagement/assessments)).

For configuration, inspect whether the signal is manually entered, workflow-generated, imported, inferred from attendance, or computed by Rock. For reporting, inspect whether the report is counting people, step records, achievements, streak state, assessment results, or some derived KPI.

For troubleshooting, determine whether the issue is missing source activity, wrong person, wrong date, inactive program/type, security, duplicate records, stale analytics, or report criteria.

## 3. Boundaries

Do not collapse all engagement work into this concept. Connections belongs in Connections. LMS course/class training belongs in Learning, LMS, And Engagement. Prayer belongs in Prayer And Care. Group attendance belongs in Groups or Check-In depending on the workflow ([Streaks](https://community.rockrms.com/documentation/engagement/streaks)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 4. Source Map And Dependency Notes

Use official documentation first for configuration semantics. Use model-map records when a task requires entity orientation. Use RockU as operational training context. Use release notes for analytics, KPI, Step, Assessment, Streak, and Achievement behavior changes ([Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools)).
