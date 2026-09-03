---
concept_id: connections
title: Connections Open Questions
generated: true
---

# Connections Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (131 words)
- `agent-task-recipes-recipe-validate-status-automation`: Recipe: Validate status automation (143 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (240 words)

## Community-Supported Only

- `public-intake-and-cross-system-handoffs`: Public Intake And Cross-System Handoffs
- `agent-task-recipes-recipe-connect-preregistration-to-staff-follow-up`: Recipe: Connect preregistration to staff follow-up
- `source-map-community-reviewed-guidance-and-examples`: Community-reviewed guidance and examples

## Needs Live Verification

- `agent-summary`: Agent Summary
- `mental-model`: Mental Model
- `opportunities`: Opportunities
- `requests-and-statuses-state`: State
- `requests-and-statuses-status`: Status
- `requests-and-statuses-due-dates`: Due Dates
- `boards-and-lists-list-view`: List view
- `assignment-and-follow-up`: Assignment And Follow-Up
- `placement-completion-and-transfer`: Placement, Completion, And Transfer
- `workflows-and-status-automation`: Workflows And Status Automation
- `connection-campaigns`: Connection Campaigns
- `public-intake-and-cross-system-handoffs`: Public Intake And Cross-System Handoffs
- `reporting-ai-and-governance`: Reporting, AI, And Governance
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-connector-cannot-see-an-expected-request`: A connector cannot see an expected request
- `troubleshooting-decision-tree-a-list-field-source-grouping-option-or-view-is-missing`: A list field, source, grouping option, or view is missing
- `troubleshooting-decision-tree-a-request-cannot-skip-to-a-later-status-or-cannot-be-completed`: A request cannot skip to a later status or cannot be completed
- `troubleshooting-decision-tree-due-soon-or-overdue-counts-look-wrong`: Due-soon or overdue counts look wrong
- `troubleshooting-decision-tree-a-future-follow-up-request-did-not-return-to-the-active-queue`: A future follow-up request did not return to the active queue
- `troubleshooting-decision-tree-a-campaign-creates-no-requests-or-assigns-them-to-the-wrong-people`: A campaign creates no requests or assigns them to the wrong people
- `troubleshooting-decision-tree-a-workflow-did-not-launch-or-a-bulk-action-affected-only-some-requests`: A workflow did not launch or a bulk action affected only some requests
- `troubleshooting-decision-tree-an-ai-summary-is-unavailable-or-unreliable`: An AI summary is unavailable or unreliable
- `agent-task-recipes-recipe-configure-a-new-connection-pipeline`: Recipe: Configure a new connection pipeline
- `agent-task-recipes-recipe-triage-an-unassigned-or-overdue-queue`: Recipe: Triage an unassigned or overdue queue
- `agent-task-recipes-recipe-transfer-and-complete-a-request-safely`: Recipe: Transfer and complete a request safely
- `agent-task-recipes-recipe-launch-a-connection-campaign`: Recipe: Launch a connection campaign
- `agent-task-recipes-recipe-connect-preregistration-to-staff-follow-up`: Recipe: Connect preregistration to staff follow-up
- `agent-task-recipes-recipe-validate-status-automation`: Recipe: Validate status automation
- `source-map-community-reviewed-guidance-and-examples`: Community-reviewed guidance and examples

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
