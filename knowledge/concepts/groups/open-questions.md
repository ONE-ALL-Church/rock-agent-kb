---
concept_id: groups
title: Groups Open Questions
generated: true
---

# Groups Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `12-administration-and-operational-guardrails-naming-and-hierarchy`: Naming And Hierarchy (86 words)
- `14-reporting-analytics-and-model-map-reporting-questions-to-define`: Reporting Questions To Define (83 words)
- `16-implementation-playbooks-playbook-build-a-small-group-structure`: Playbook: Build A Small Group Structure (144 words)
- `19-source-map-and-dependency-notes-dependency-notes`: Dependency Notes (150 words)

## Community-Supported Only

- `7-common-groups-workflows-create-a-new-group`: Create A New Group
- `7-common-groups-workflows-add-or-move-group-members`: Add Or Move Group Members
- `7-common-groups-workflows-copy-or-clone-groups`: Copy Or Clone Groups
- `7-common-groups-workflows-use-groups-as-communication-audiences`: Use Groups As Communication Audiences
- `8-group-types-deep-dive-roles`: Roles
- `8-group-types-deep-dive-group-attributes`: Group Attributes
- `9-group-finder-deep-dive-finder-share-links`: Finder Share Links
- `10-group-attendance-deep-dive-attendance-configuration`: Attendance Configuration
- `10-group-attendance-deep-dive-attendance-ux-and-confirmation`: Attendance UX And Confirmation
- `12-administration-and-operational-guardrails-recipe-guardrails`: Recipe Guardrails
- `13-developer-api-lava-and-source-code-landmarks-lava-landmarks`: Lava Landmarks
- `16-implementation-playbooks-playbook-add-group-requirements`: Playbook: Add Group Requirements
- `16-implementation-playbooks-playbook-extend-group-leader-toolbox`: Playbook: Extend Group Leader Toolbox
- `18-agent-task-recipes-recipe-create-a-custom-scheduled-volunteer-communication-page`: Recipe: Create A Custom Scheduled Volunteer Communication Page
- `19-source-map-and-dependency-notes-community-examples`: Community Examples

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `3-groups-mental-model`: 3. Groups Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-group-type-configuration`: Group Type Configuration
- `5-core-configuration-and-data-model-core-entity-relationships`: Core Entity Relationships
- `5-core-configuration-and-data-model-locations-and-schedules`: Locations And Schedules
- `5-core-configuration-and-data-model-attributes`: Attributes
- `6-primary-entities-and-relationships-group-type`: Group Type
- `6-primary-entities-and-relationships-group-type-association`: Group Type Association
- `6-primary-entities-and-relationships-group`: Group
- `6-primary-entities-and-relationships-group-member`: Group Member
- `6-primary-entities-and-relationships-group-type-role`: Group Type Role
- `6-primary-entities-and-relationships-group-member-assignment`: Group Member Assignment
- `6-primary-entities-and-relationships-group-member-requirement`: Group Member Requirement
- `7-common-groups-workflows-create-a-new-group`: Create A New Group
- `7-common-groups-workflows-add-or-move-group-members`: Add Or Move Group Members
- `7-common-groups-workflows-use-groups-as-communication-audiences`: Use Groups As Communication Audiences
- `8-group-types-deep-dive-inherited-group-types`: Inherited Group Types
- `8-group-types-deep-dive-roles`: Roles
- `8-group-types-deep-dive-schedule-exclusions`: Schedule Exclusions
- `8-group-types-deep-dive-group-capacity`: Group Capacity
- `9-group-finder-deep-dive-finder-data-inputs`: Finder Data Inputs
- `9-group-finder-deep-dive-finder-and-schedules`: Finder And Schedules
- `9-group-finder-deep-dive-finder-and-locations`: Finder And Locations
- `9-group-finder-deep-dive-finder-share-links`: Finder Share Links
- `9-group-finder-deep-dive-finder-registration-handoff`: Finder Registration Handoff
- `10-group-attendance-deep-dive-attendance-configuration`: Attendance Configuration
- `10-group-attendance-deep-dive-mobile-attendance-entry`: Mobile Attendance Entry
- `10-group-attendance-deep-dive-attendance-ux-and-confirmation`: Attendance UX And Confirmation
- `10-group-attendance-deep-dive-attendance-reporting`: Attendance Reporting
- `11-related-rock-areas-people-attendance-security-locations-schedules-attendance`: Attendance
- `12-administration-and-operational-guardrails-use-read-only-investigation-first`: Use Read-Only Investigation First
- `12-administration-and-operational-guardrails-recipe-guardrails`: Recipe Guardrails
- `12-administration-and-operational-guardrails-group-type-change-guardrail`: Group Type Change Guardrail
- `13-developer-api-lava-and-source-code-landmarks-lava-landmarks`: Lava Landmarks
- `14-reporting-analytics-and-model-map-model-map-coverage`: Model Map Coverage
- `14-reporting-analytics-and-model-map-attendance-analytics-caveat`: Attendance Analytics Caveat
- `15-version-and-release-caveats-navigation-wording`: Navigation Wording
- `15-version-and-release-caveats-rock-18-1`: Rock 18.1

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
