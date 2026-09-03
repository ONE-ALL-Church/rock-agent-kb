---
concept_id: learning-lms-engagement
title: Learning, LMS, And Engagement Open Questions
generated: true
---

# Learning, LMS, And Engagement Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `scope-and-boundaries`: Scope And Boundaries

## Needs Live Verification

- `courses-and-lessons-revise-a-class-without-disrupting-the-current-one`: Revise a class without disrupting the current one
- `activity-design-and-staff-responsibilities-file-upload`: File upload
- `requirements-and-completion-course-requirements`: Course requirements
- `requirements-and-completion-grading-systems-and-class-completion`: Grading systems and class completion
- `engagement-journeys-and-learner-access`: Engagement Journeys And Learner Access
- `groups-workflows-and-operational-follow-up`: Groups, Workflows, And Operational Follow-Up
- `notifications-and-communications`: Notifications And Communications
- `staff-enablement-and-change-management`: Staff Enablement And Change Management
- `troubleshooting-decision-tree-a-learner-cannot-find-a-program-or-course`: A learner cannot find a program or course
- `troubleshooting-decision-tree-a-learner-is-blocked-from-enrollment`: A learner is blocked from enrollment
- `troubleshooting-decision-tree-a-facilitator-cannot-open-lms-administration-pages`: A facilitator cannot open LMS administration pages
- `troubleshooting-decision-tree-an-activity-is-submitted-but-still-incomplete`: An activity is submitted but still incomplete
- `troubleshooting-decision-tree-a-failed-learner-is-marked-complete`: A failed learner is marked complete
- `troubleshooting-decision-tree-program-completion-is-not-updating`: Program completion is not updating
- `troubleshooting-decision-tree-learning-notifications-are-delayed-or-absent`: Learning notifications are delayed or absent
- `troubleshooting-decision-tree-an-lms-dashboard-is-slow`: An LMS dashboard is slow
- `agent-task-recipes-recipe-create-a-self-paced-volunteer-training-course`: Recipe: Create a self-paced volunteer training course
- `agent-task-recipes-recipe-prepare-an-academic-calendar-class`: Recipe: Prepare an Academic Calendar class
- `agent-task-recipes-recipe-connect-course-completion-to-operational-follow-up`: Recipe: Connect course completion to operational follow-up
- `agent-task-recipes-recipe-roll-out-training-for-a-changed-rock-interface`: Recipe: Roll out training for a changed Rock interface
- `agent-task-recipes-recipe-build-a-bounded-lms-completion-report`: Recipe: Build a bounded LMS completion report
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
