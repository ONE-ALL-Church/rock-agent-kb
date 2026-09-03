---
concept_id: prayer-care
title: Prayer And Care Open Questions
generated: true
---

# Prayer And Care Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `community-implementation-patterns`: Community Implementation Patterns
- `source-map-community-examples`: Community examples

## Needs Live Verification

- `prayer-request-intake-and-lifecycle`: Prayer Request Intake And Lifecycle
- `categories-visibility-and-page-security`: Categories, Visibility, And Page Security
- `teams-approval-and-human-moderation`: Teams, Approval, And Human Moderation
- `ai-assisted-processing-and-moderation`: AI-Assisted Processing And Moderation
- `prayer-sessions-and-prayer-card-view`: Prayer Sessions And Prayer Card View
- `group-specific-prayer-requests`: Group-Specific Prayer Requests
- `comments-communications-and-follow-up`: Comments, Communications, And Follow-Up
- `troubleshooting-decision-tree-a-submitted-request-does-not-appear-for-the-prayer-team`: A submitted request does not appear for the prayer team
- `troubleshooting-decision-tree-a-sensitive-request-is-still-visible`: A sensitive request is still visible
- `troubleshooting-decision-tree-prayer-team-members-cannot-add-comments`: Prayer-team members cannot add comments
- `troubleshooting-decision-tree-prayer-comment-digests-are-not-being-delivered`: Prayer-comment digests are not being delivered
- `troubleshooting-decision-tree-a-group-prayer-page-is-empty-or-shows-the-wrong-scope`: A group prayer page is empty or shows the wrong scope
- `troubleshooting-decision-tree-ai-processing-is-inconsistent-across-categories`: AI processing is inconsistent across categories
- `troubleshooting-decision-tree-outreach-reminders-do-not-arrive`: Outreach reminders do not arrive
- `agent-task-recipes-recipe-configure-moderated-public-prayer-intake`: Recipe: Configure moderated public prayer intake
- `agent-task-recipes-recipe-operate-the-administrator-moderation-queue`: Recipe: Operate the administrator moderation queue
- `agent-task-recipes-recipe-build-a-secured-ministry-specific-prayer-queue`: Recipe: Build a secured ministry-specific prayer queue
- `agent-task-recipes-recipe-create-and-verify-a-group-prayer-route`: Recipe: Create and verify a group prayer route
- `agent-task-recipes-recipe-enable-prayer-comment-digests`: Recipe: Enable prayer-comment digests
- `agent-task-recipes-recipe-add-workflow-based-care-follow-up`: Recipe: Add workflow-based care follow-up
- `agent-task-recipes-recipe-introduce-ai-assistance-with-human-review`: Recipe: Introduce AI assistance with human review
- `agent-task-recipes-recipe-validate-outreach-toolbox-for-prayer-touchpoints`: Recipe: Validate Outreach Toolbox for prayer touchpoints
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
