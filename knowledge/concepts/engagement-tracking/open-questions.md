---
concept_id: engagement-tracking
title: Engagement Tracking Open Questions
generated: true
---

# Engagement Tracking Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `source-map-community-example`: Community example

## Needs Live Verification

- `steps-workflows-and-permissions`: Workflows and permissions
- `steps-badges-metrics-and-charts`: Badges, metrics and charts
- `streaks-types-and-maps`: Types and maps
- `assessments-retake-controls`: Retake controls
- `achievements-overrides-and-rebuilds`: Overrides and rebuilds
- `sign-ups`: Sign-Ups
- `troubleshooting-decision-tree-a-step-has-a-completion-date-but-is-not-counted-as-complete`: A Step has a completion date but is not counted as complete
- `troubleshooting-decision-tree-step-automation-did-not-create-or-complete-a-record`: Step automation did not create or complete a record
- `troubleshooting-decision-tree-step-metrics-or-charts-appear-inflated-or-use-unexpected-dates`: Step metrics or charts appear inflated or use unexpected dates
- `troubleshooting-decision-tree-a-manually-enrolled-person-has-a-streak-of-zero`: A manually enrolled person has a streak of zero
- `troubleshooting-decision-tree-a-streak-type-map-was-changed-but-participant-totals-have-not-updated`: A Streak Type map was changed but participant totals have not updated
- `troubleshooting-decision-tree-a-streak-spans-a-date-that-still-looks-absent`: A streak spans a date that still looks absent
- `troubleshooting-decision-tree-a-person-cannot-retake-an-assessment`: A person cannot retake an assessment
- `troubleshooting-decision-tree-an-assessment-request-cannot-be-canceled`: An assessment request cannot be canceled
- `troubleshooting-decision-tree-achievement-progress-or-attempt-state-looks-wrong`: Achievement progress or attempt state looks wrong
- `troubleshooting-decision-tree-a-reminder-was-created-but-no-notification-occurred`: A Reminder was created but no notification occurred
- `troubleshooting-decision-tree-a-following-notification-is-missing`: A Following notification is missing
- `troubleshooting-decision-tree-an-interactive-experience-response-is-missing-from-the-visualizer`: An Interactive Experience response is missing from the visualizer
- `troubleshooting-decision-tree-a-sign-up-communication-or-attendance-link-fails`: A Sign-Up communication or attendance link fails
- `agent-task-recipes-recipe-configure-a-step-journey-with-reliable-completion-signals`: Recipe: Configure a Step journey with reliable completion signals
- `agent-task-recipes-recipe-bulk-record-a-step`: Recipe: Bulk-record a Step
- `agent-task-recipes-recipe-automate-step-completion-from-a-data-view`: Recipe: Automate Step completion from a Data View
- `agent-task-recipes-recipe-build-a-streak-type-safely`: Recipe: Build a Streak Type safely
- `agent-task-recipes-recipe-correct-one-person-s-streak`: Recipe: Correct one person’s streak
- `agent-task-recipes-recipe-rebuild-a-streak-with-a-controlled-boundary`: Recipe: Rebuild a Streak with a controlled boundary
- `agent-task-recipes-recipe-request-and-monitor-assessments`: Recipe: Request and monitor assessments
- `agent-task-recipes-recipe-build-an-assessment-result-segment`: Recipe: Build an assessment-result segment
- `agent-task-recipes-recipe-connect-an-achievement-to-workflows-and-steps`: Recipe: Connect an Achievement to workflows and Steps
- `agent-task-recipes-recipe-configure-reminder-processing`: Recipe: Configure Reminder processing
- `agent-task-recipes-recipe-configure-a-secure-following-event`: Recipe: Configure a secure Following event
- `agent-task-recipes-recipe-operate-a-moderated-interactive-experience`: Recipe: Operate a moderated Interactive Experience
- `agent-task-recipes-recipe-configure-a-sign-up-registration-and-attendance-route`: Recipe: Configure a Sign-Up registration and attendance route
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

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
