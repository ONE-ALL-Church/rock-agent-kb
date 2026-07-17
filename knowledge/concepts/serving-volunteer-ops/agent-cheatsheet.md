---
concept_id: serving-volunteer-ops
title: Serving And Volunteer Operations Agent Cheatsheet
generated: true
---

# Serving And Volunteer Operations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find The Real Object Behind A Serving Issue](tasks/recipe-find-the-real-object-behind-a-serving-issue.md) |  |  |
| [Recipe: Confirm A Volunteer Is Eligible To Serve](tasks/recipe-confirm-a-volunteer-is-eligible-to-serve.md) |  |  |
| [Recipe: Explain Why A Volunteer Was Not Scheduled](tasks/recipe-explain-why-a-volunteer-was-not-scheduled.md) |  |  |
| [Recipe: Verify Schedule Confirmation Send Health](tasks/recipe-verify-schedule-confirmation-send-health.md) |  |  |
| [Recipe: Safely Customize A Volunteer-Facing Page](tasks/recipe-safely-customize-a-volunteer-facing-page.md) |  |  |
| [Recipe: Investigate Family Serving Response Request](tasks/recipe-investigate-family-serving-response-request.md) |  |  |
| [Recipe: Build A Serving Health Dashboard](tasks/recipe-build-a-serving-health-dashboard.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `AttendanceOccurrence` | `Attendance`, `Group`, `Schedule`, `Location`, `Campus` | Use this for reporting context. Check group, location, schedule, and SundayDate before blaming the UI. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed the Send Attendance Reminder job so Group leaders still receive reminders when a Group only has scheduling/RSVP-related Attendance records. The job now treats those tracking records as not being “attendance” and only suppresses remind |
| `17.2` | core | Fixed an issue where the Group Scheduling Confirmation workflow could incorrectly record a response if the confirmation email was opened by an automated link-checker, or if a decline reason was required but not provided. This ensures that o |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology-core-terms` | high | live verification |
| `3-serving-and-volunteer-operations-mental-model-layer-2-where-and-when` | normal | live verification |
| `3-serving-and-volunteer-operations-mental-model-layer-3-assignment-and-response` | normal | live verification |
| `3-serving-and-volunteer-operations-mental-model-layer-4-actual-attendance` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide-how-agents-should-use-this-guide` | structural | live verification |
| `4-source-authority-and-how-to-use-this-guide-when-to-prefer-live-verification` | citation-only | live verification |
| `5-core-configuration-and-data-model-group-types` | normal | live verification |
| `5-core-configuration-and-data-model-group-type-inheritance` | high | live verification |
| `5-core-configuration-and-data-model-groups` | community-supported | live verification |
| `5-core-configuration-and-data-model-group-roles` | citation-only | live verification |
| `5-core-configuration-and-data-model-group-members` | community-supported | live verification |
| `5-core-configuration-and-data-model-locations` | high | live verification |
| `5-core-configuration-and-data-model-schedules` | community-supported | live verification |
| `5-core-configuration-and-data-model-attendanceoccurrence` | normal | live verification |
| `5-core-configuration-and-data-model-attendance` | normal | live verification |
| `5-core-configuration-and-data-model-communications` | normal | live verification |
| `5-core-configuration-and-data-model-workflows` | community-supported | live verification |
| `6-primary-entities-and-relationships-grouptype-group` | citation-only | live verification |
| `6-primary-entities-and-relationships-group-groupmember-personalias-person` | normal | live verification |
| `6-primary-entities-and-relationships-grouprequirement-and-eligibility-data` | citation-only | live verification |
| `7-common-serving-and-volunteer-operations-workflows-new-volunteer-interest-intake` | community-supported | community-supported |
| `7-common-serving-and-volunteer-operations-workflows-volunteer-schedule-preference-collection` | community-supported | live verification |
| `7-common-serving-and-volunteer-operations-workflows-auto-scheduling` | community-supported | community-supported |
| `7-common-serving-and-volunteer-operations-workflows-send-schedule-confirmations` | normal | live verification |
| `7-common-serving-and-volunteer-operations-workflows-volunteer-confirms-or-declines` | normal | live verification |
| `7-common-serving-and-volunteer-operations-workflows-view-serving-schedule-externally` | community-supported | live verification |
| `7-common-serving-and-volunteer-operations-workflows-manage-family-members-serving-requests` | community-supported | live verification |
| `7-common-serving-and-volunteer-operations-workflows-record-serving-attendance` | community-supported | community-supported |
| `8-serving-teams-and-roles-deep-dive-real-team-vs-sign-up-opportunity-vs-interest-pipeline` | community-supported | community-supported |
| `8-serving-teams-and-roles-deep-dive-role-based-scheduling` | structural | live verification |
| `8-serving-teams-and-roles-deep-dive-team-coordinator-fields` | community-supported | community-supported |
| `8-serving-teams-and-roles-deep-dive-group-history` | citation-only | live verification |
| `9-schedules-and-confirmations-deep-dive-scheduler-and-status-board` | normal | live verification |
| `9-schedules-and-confirmations-deep-dive-confirmation-statuses` | normal | live verification |
| `9-schedules-and-confirmations-deep-dive-automated-link-checkers` | normal | live verification |
| `10-volunteer-requirements-deep-dive-requirement-categories` | community-supported | community-supported |
| `10-volunteer-requirements-deep-dive-requirement-placement` | structural | live verification |
| `10-volunteer-requirements-deep-dive-blocking-vs-warning` | structural | live verification |
| `10-volunteer-requirements-deep-dive-requirement-failure-troubleshooting` | structural | live verification |
| `11-attendance-and-follow-up-deep-dive-attendance-vs-scheduled-assignment` | normal | live verification |
| `11-attendance-and-follow-up-deep-dive-group-attendance-blocks` | community-supported | live verification |
| `11-attendance-and-follow-up-deep-dive-attendance-reminder-job` | normal | live verification |
| `11-attendance-and-follow-up-deep-dive-follow-up-workflows` | structural | live verification |
| `12-related-rock-areas-groups-scheduling-locations-check-in-communications-workflows-people-security-workflows` | community-supported | community-supported |
| `13-administration-and-operational-guardrails-page-and-block-guardrails` | community-supported | live verification |
| `13-administration-and-operational-guardrails-communication-guardrails` | normal | live verification |
| `13-administration-and-operational-guardrails-security-guardrails` | community-supported | live verification |
| `14-developer-api-lava-and-source-code-landmarks-confirmation-status-enum` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-landmarks` | community-supported | live verification |
| `15-reporting-analytics-and-model-map-reporting-concepts` | citation-only | live verification |
| `15-reporting-analytics-and-model-map-schedule-coverage-reporting` | structural | live verification |
| `15-reporting-analytics-and-model-map-schedule-preference-reporting` | community-supported | live verification |
| `16-version-and-release-caveats-rock-v17-2-group-scheduling-confirmation-fix` | normal | live verification |
| `16-version-and-release-caveats-rock-v18-3-attendance-reminder-fix` | normal | live verification |
| `16-version-and-release-caveats-rock-v18-3-check-in-scheduled-times-fix` | normal | live verification |
| `16-version-and-release-caveats-rock-v14-check-in-manager-roster-updates` | normal | live verification |
| `16-version-and-release-caveats-mobile-schedule-toolbox-version` | normal | live verification |
| `17-implementation-playbooks-playbook-launch-a-new-serving-ministry-team` | citation-only | live verification |
| `17-implementation-playbooks-playbook-add-fifth-sunday-auto-schedule-coverage` | community-supported | live verification |
| `17-implementation-playbooks-playbook-build-external-serving-schedule-view` | community-supported | live verification |
| `17-implementation-playbooks-playbook-configure-dynamic-sender-for-scheduling-confirmations` | community-supported | live verification |
| `17-implementation-playbooks-playbook-add-serving-interest-intake` | community-supported | community-supported |
| `17-implementation-playbooks-playbook-audit-scheduling-confirmation-failures` | structural | live verification |
| `17-implementation-playbooks-playbook-audit-attendance-reminder-failure` | structural | live verification |
| `17-implementation-playbooks-playbook-clean-up-archived-groups-with-schedules` | normal | live verification |
| `18-troubleshooting-decision-tree-attendance-looks-too-high` | normal | live verification |
| `18-troubleshooting-decision-tree-volunteers-missing-from-preference-report` | community-supported | community-supported |
| `18-troubleshooting-decision-tree-external-schedule-page-shows-wrong-groups` | community-supported | community-supported |
| `19-agent-task-recipes-recipe-confirm-a-volunteer-is-eligible-to-serve` | structural | live verification |
| `19-agent-task-recipes-recipe-explain-why-a-volunteer-was-not-scheduled` | structural | live verification |
| `19-agent-task-recipes-recipe-verify-schedule-confirmation-send-health` | normal | live verification |
| `19-agent-task-recipes-recipe-safely-customize-a-volunteer-facing-page` | community-supported | live verification |
| `19-agent-task-recipes-recipe-investigate-family-serving-response-request` | community-supported | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `20-source-map-and-dependency-notes-community-example-sources` | community-supported | community-supported |
| `20-source-map-and-dependency-notes-live-verification-required` | citation-only | live verification |
