---
concept_id: groups
title: Groups Open Questions
generated: true
---

# Groups Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `group-attendance-entry`: Group Attendance Entry
- `troubleshooting-decision-tree-a-failed-workflow-may-have-partially-changed-group-data`: A failed workflow may have partially changed group data

## Needs Live Verification

- `agent-summary`: Agent Summary
- `mental-model`: Mental Model
- `creating-editing-inactivating-and-archiving-groups`: Creating, Editing, Inactivating, And Archiving Groups
- `members-roles-statuses-and-attributes`: Members, Roles, Statuses, And Attributes
- `group-security-and-leader-operations`: Group Security And Leader Operations
- `locations-and-schedules`: Locations And Schedules
- `group-finder`: Group Finder
- `group-attendance-entry`: Group Attendance Entry
- `group-sync-and-communication-lists`: Group Sync And Communication Lists
- `groups-in-workflows-training-and-reporting`: Groups In Workflows, Training, And Reporting
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-add-child-to-selected-is-disabled`: Add Child to Selected is disabled
- `troubleshooting-decision-tree-a-group-is-missing-from-group-finder`: A group is missing from Group Finder
- `troubleshooting-decision-tree-the-day-or-time-filter-does-not-return-a-group`: The day or time filter does not return a group
- `troubleshooting-decision-tree-a-leader-cannot-add-a-member-from-group-toolbox`: A leader cannot add a member from Group Toolbox
- `troubleshooting-decision-tree-attendance-reminders-are-not-sent`: Attendance reminders are not sent
- `troubleshooting-decision-tree-the-absence-notification-job-fails-or-evaluates-the-wrong-people`: The absence-notification job fails or evaluates the wrong people
- `troubleshooting-decision-tree-a-synced-group-or-communication-list-has-unexpected-members`: A synced group or communication list has unexpected members
- `troubleshooting-decision-tree-member-attributes-disappeared-after-a-move`: Member attributes disappeared after a move
- `troubleshooting-decision-tree-a-location-or-schedule-link-is-wrong-after-api-work`: A location or schedule link is wrong after API work
- `troubleshooting-decision-tree-a-failed-workflow-may-have-partially-changed-group-data`: A failed workflow may have partially changed group data
- `agent-task-recipes-recipe-design-a-group-type-and-hierarchy`: Recipe: Design a Group Type and hierarchy
- `agent-task-recipes-recipe-publish-a-group-through-group-finder`: Recipe: Publish a group through Group Finder
- `agent-task-recipes-recipe-configure-focused-attendance-entry`: Recipe: Configure focused attendance entry
- `agent-task-recipes-recipe-configure-attendance-follow-up`: Recipe: Configure attendance follow-up
- `agent-task-recipes-recipe-enforce-a-group-type-requirement`: Recipe: Enforce a Group Type requirement
- `agent-task-recipes-recipe-secure-leader-operations`: Recipe: Secure leader operations
- `agent-task-recipes-recipe-enable-history-and-archive-a-group`: Recipe: Enable history and archive a group
- `agent-task-recipes-recipe-move-group-members-safely`: Recipe: Move group members safely
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
