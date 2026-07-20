---
concept_id: groups
title: Groups Agent Cheatsheet
generated: true
---

# Groups Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Identify Why A Group Is Not Visible](tasks/recipe-identify-why-a-group-is-not-visible.md) |  |  |
| [Recipe: Audit A Group Type Before Launch](tasks/recipe-audit-a-group-type-before-launch.md) |  |  |
| [Recipe: Debug Group Attendance Reminder Failures](tasks/recipe-debug-group-attendance-reminder-failures.md) |  |  |
| [Recipe: Build A Group Finder QA Checklist](tasks/recipe-build-a-group-finder-qa-checklist.md) |  |  |
| [Recipe: Move Members Between Groups Safely](tasks/recipe-move-members-between-groups-safely.md) |  |  |
| [Recipe: Create A Custom Scheduled Volunteer Communication Page](tasks/recipe-create-a-custom-scheduled-volunteer-communication-page.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `AttendanceOccurrence` | `Attendance`, `Group`, `Schedule`, `Location`, `Campus` | Use this for reporting context. Check group, location, schedule, and SundayDate before blaming the UI. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupMemberRequirement` | `GroupMember`, `Person`, `Group` | Keep LMS completion separate from serving eligibility unless a requirement explicitly connects them. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed an issue where the Attendance Analytics block incorrectly included groups whose Group Type was listed as an "Allowed Child Group Type" of a selected Group Type, even though it was not explicitly selected in the block settings. The blo |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `3-groups-mental-model` | high | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-group-type-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-core-entity-relationships` | citation-only | live verification |
| `5-core-configuration-and-data-model-locations-and-schedules` | normal | live verification |
| `5-core-configuration-and-data-model-attributes` | high | live verification |
| `6-primary-entities-and-relationships-group-type` | citation-only | live verification |
| `6-primary-entities-and-relationships-group-type-association` | normal | live verification |
| `6-primary-entities-and-relationships-group` | normal | live verification |
| `6-primary-entities-and-relationships-group-member` | normal | live verification |
| `6-primary-entities-and-relationships-group-type-role` | normal | live verification |
| `6-primary-entities-and-relationships-group-member-assignment` | citation-only | live verification |
| `6-primary-entities-and-relationships-group-member-requirement` | normal | live verification |
| `7-common-groups-workflows-create-a-new-group` | community-supported | live verification |
| `7-common-groups-workflows-add-or-move-group-members` | community-supported | live verification |
| `7-common-groups-workflows-copy-or-clone-groups` | community-supported | community-supported |
| `7-common-groups-workflows-use-groups-as-communication-audiences` | community-supported | live verification |
| `8-group-types-deep-dive-inherited-group-types` | normal | live verification |
| `8-group-types-deep-dive-roles` | community-supported | live verification |
| `8-group-types-deep-dive-group-attributes` | community-supported | community-supported |
| `8-group-types-deep-dive-schedule-exclusions` | high | live verification |
| `8-group-types-deep-dive-group-capacity` | normal | live verification |
| `9-group-finder-deep-dive-finder-data-inputs` | normal | live verification |
| `9-group-finder-deep-dive-finder-and-schedules` | normal | live verification |
| `9-group-finder-deep-dive-finder-and-locations` | normal | live verification |
| `9-group-finder-deep-dive-finder-share-links` | community-supported | live verification |
| `9-group-finder-deep-dive-finder-registration-handoff` | normal | live verification |
| `10-group-attendance-deep-dive-attendance-configuration` | community-supported | live verification |
| `10-group-attendance-deep-dive-mobile-attendance-entry` | normal | live verification |
| `10-group-attendance-deep-dive-attendance-ux-and-confirmation` | community-supported | live verification |
| `10-group-attendance-deep-dive-attendance-reporting` | normal | live verification |
| `11-related-rock-areas-people-attendance-security-locations-schedules-attendance` | structural | live verification |
| `12-administration-and-operational-guardrails-use-read-only-investigation-first` | structural | live verification |
| `12-administration-and-operational-guardrails-recipe-guardrails` | community-supported | live verification |
| `12-administration-and-operational-guardrails-group-type-change-guardrail` | citation-only | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava-landmarks` | community-supported | live verification |
| `14-reporting-analytics-and-model-map-model-map-coverage` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-attendance-analytics-caveat` | normal | live verification |
| `15-version-and-release-caveats-navigation-wording` | structural | live verification |
| `15-version-and-release-caveats-rock-18-1` | normal | live verification |
| `15-version-and-release-caveats-rock-19-1-beta-context` | normal | live verification |
| `15-version-and-release-caveats-mobile-core-version-markers` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-small-group-structure` | normal | live verification |
| `16-implementation-playbooks-playbook-build-a-serving-team-scheduling-structure` | citation-only | live verification |
| `16-implementation-playbooks-playbook-set-up-group-finder` | structural | live verification |
| `16-implementation-playbooks-playbook-add-group-requirements` | community-supported | live verification |
| `16-implementation-playbooks-playbook-extend-group-leader-toolbox` | community-supported | live verification |
| `18-agent-task-recipes-recipe-identify-why-a-group-is-not-visible` | structural | live verification |
| `18-agent-task-recipes-recipe-audit-a-group-type-before-launch` | structural | live verification |
| `18-agent-task-recipes-recipe-debug-group-attendance-reminder-failures` | structural | live verification |
| `18-agent-task-recipes-recipe-build-a-group-finder-qa-checklist` | structural | live verification |
| `18-agent-task-recipes-recipe-move-members-between-groups-safely` | structural | live verification |
| `18-agent-task-recipes-recipe-create-a-custom-scheduled-volunteer-communication-page` | community-supported | live verification |
| `approved-claim-coverage` | normal | live verification |
| `19-source-map-and-dependency-notes-community-examples` | community-supported | community-supported |
