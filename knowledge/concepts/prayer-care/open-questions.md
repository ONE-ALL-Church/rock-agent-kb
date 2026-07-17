---
concept_id: prayer-care
title: Prayer And Care Open Questions
generated: true
---

# Prayer And Care Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `7-common-prayer-and-care-workflows-urgent-prayer-email`: Urgent Prayer Email
- `7-common-prayer-and-care-workflows-sms-prayer-request-capture`: SMS Prayer Request Capture
- `7-common-prayer-and-care-workflows-prayer-wall`: Prayer Wall
- `7-common-prayer-and-care-workflows-live-prayer-chat`: Live Prayer Chat
- `7-common-prayer-and-care-workflows-pastoral-care-summary`: Pastoral Care Summary
- `10-follow-up-and-communications-deep-dive-urgent-notifications`: Urgent Notifications
- `10-follow-up-and-communications-deep-dive-care-follow-up-beyond-prayer`: Care Follow-Up Beyond Prayer
- `14-reporting-analytics-and-model-map-metrics-to-avoid-misreading`: Metrics To Avoid Misreading

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-prayer-and-care-mental-model`: 3. Prayer And Care Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-prayer-request-entry-configuration`: Prayer Request Entry Configuration
- `5-core-configuration-and-data-model-prayer-request-detail-configuration`: Prayer Request Detail Configuration
- `5-core-configuration-and-data-model-prayer-request-list-configuration`: Prayer Request List Configuration
- `5-core-configuration-and-data-model-categories`: Categories
- `5-core-configuration-and-data-model-approval-visibility-expiration-and-activity`: Approval, Visibility, Expiration, And Activity
- `6-primary-entities-and-relationships-prayer-request-to-person`: Prayer Request To Person
- `6-primary-entities-and-relationships-prayer-request-to-campus`: Prayer Request To Campus
- `6-primary-entities-and-relationships-prayer-request-to-comments-and-notes`: Prayer Request To Comments And Notes
- `7-common-prayer-and-care-workflows-public-website-prayer-intake`: Public Website Prayer Intake
- `7-common-prayer-and-care-workflows-internal-staff-entry`: Internal Staff Entry
- `7-common-prayer-and-care-workflows-prayer-card-view`: Prayer Card View
- `7-common-prayer-and-care-workflows-group-prayer-requests`: Group Prayer Requests
- `7-common-prayer-and-care-workflows-urgent-prayer-email`: Urgent Prayer Email
- `7-common-prayer-and-care-workflows-prayer-wall`: Prayer Wall
- `7-common-prayer-and-care-workflows-pastoral-care-summary`: Pastoral Care Summary
- `8-prayer-requests-deep-dive-text-handling`: Text Handling
- `8-prayer-requests-deep-dive-approval`: Approval
- `8-prayer-requests-deep-dive-expiration`: Expiration
- `9-teams-and-moderation-deep-dive-ai-moderation-and-formatting`: AI Moderation And Formatting
- `10-follow-up-and-communications-deep-dive-comment-digest-email`: Comment Digest Email
- `10-follow-up-and-communications-deep-dive-communications-security`: Communications Security
- `11-related-rock-areas-people-groups-communications-workflows-security-cms-groups`: Groups
- `11-related-rock-areas-people-groups-communications-workflows-security-cms-communications`: Communications
- `12-administration-and-operational-guardrails-change-management`: Change Management
- `13-developer-api-lava-and-source-code-landmarks-lava`: Lava
- `15-version-and-release-caveats`: 15. Version And Release Caveats
- `16-implementation-playbooks-playbook-launch-basic-prayer-intake`: Playbook: Launch Basic Prayer Intake
- `16-implementation-playbooks-playbook-launch-prayer-team-page`: Playbook: Launch Prayer Team Page
- `16-implementation-playbooks-playbook-add-group-prayer`: Playbook: Add Group Prayer
- `16-implementation-playbooks-playbook-enable-comment-digest`: Playbook: Enable Comment Digest
- `16-implementation-playbooks-playbook-add-sms-prayer-intake`: Playbook: Add SMS Prayer Intake
- `16-implementation-playbooks-playbook-add-public-prayer-wall`: Playbook: Add Public Prayer Wall
- `18-agent-task-recipes-audit-prayer-configuration`: Audit Prayer Configuration
- `18-agent-task-recipes-safely-extend-prayer-intake`: Safely Extend Prayer Intake

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
