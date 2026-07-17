---
concept_id: engagement-tracking
title: Engagement Tracking Open Questions
generated: true
---

# Engagement Tracking Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `17-implementation-playbooks-playbook-historical-baptism-step-import`: Playbook: Historical Baptism Step Import

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-engagement-tracking-mental-model`: 3. Engagement Tracking Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-steps-configuration`: Steps Configuration
- `5-core-configuration-and-data-model-step-status-and-completion`: Step Status And Completion
- `5-core-configuration-and-data-model-step-program-completion-model`: Step Program Completion Model
- `5-core-configuration-and-data-model-assessments-configuration`: Assessments Configuration
- `6-primary-entities-and-relationships-person-personalias-and-engagement-records`: Person, PersonAlias, And Engagement Records
- `6-primary-entities-and-relationships-step-program-to-step-type`: Step Program To Step Type
- `6-primary-entities-and-relationships-assessments-to-person-history-and-attributes`: Assessments To Person History And Attributes
- `7-common-engagement-tracking-workflows-workflow-build-a-discipleship-step-program`: Workflow: Build A Discipleship Step Program
- `7-common-engagement-tracking-workflows-workflow-enter-an-individual-step`: Workflow: Enter An Individual Step
- `7-common-engagement-tracking-workflows-workflow-bulk-add-or-update-steps`: Workflow: Bulk Add Or Update Steps
- `7-common-engagement-tracking-workflows-workflow-send-assessment-requests`: Workflow: Send Assessment Requests
- `7-common-engagement-tracking-workflows-workflow-configure-an-achievement-that-adds-a-step`: Workflow: Configure An Achievement That Adds A Step
- `8-steps-deep-dive-what-steps-are-for`: What Steps Are For
- `8-steps-deep-dive-completion-flow-and-prerequisites`: Completion Flow And Prerequisites
- `8-steps-deep-dive-step-type-design`: Step Type Design
- `8-steps-deep-dive-step-entry`: Step Entry
- `8-steps-deep-dive-step-badges`: Step Badges
- `8-steps-deep-dive-step-charts`: Step Charts
- `8-steps-deep-dive-moving-step-types`: Moving Step Types
- `8-steps-deep-dive-core-steps`: Core Steps
- `9-streaks-deep-dive-what-streaks-are-for`: What Streaks Are For
- `9-streaks-deep-dive-streak-maps`: Streak Maps
- `9-streaks-deep-dive-manual-tracking`: Manual Tracking
- `9-streaks-deep-dive-rebuild-behavior`: Rebuild Behavior
- `9-streaks-deep-dive-excluding-dates`: Excluding Dates
- `10-assessments-deep-dive-taking-assessments`: Taking Assessments
- `10-assessments-deep-dive-sending-requests`: Sending Requests
- `10-assessments-deep-dive-retakes`: Retakes
- `10-assessments-deep-dive-assessment-history`: Assessment History
- `10-assessments-deep-dive-assessment-results-and-data-views`: Assessment Results And Data Views
- `11-achievements-deep-dive-attempts`: Attempts
- `11-achievements-deep-dive-prerequisites`: Prerequisites
- `11-achievements-deep-dive-workflow-launches`: Workflow Launches
- `11-achievements-deep-dive-badges-and-lava`: Badges And Lava
- `11-achievements-deep-dive-add-step-on-success`: Add Step On Success

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
