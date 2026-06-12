---
concept_id: check-in
title: Check-In Open Questions
generated: true
---

# Check-In Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `13-administration-and-operational-guardrails-pre-service-checklist`: Pre-Service Checklist (90 words)
- `17-implementation-playbooks-playbook-build-a-basic-family-check-in-area`: Playbook: Build A Basic Family Check-In Area (127 words)
- `17-implementation-playbooks-playbook-add-a-new-room`: Playbook: Add A New Room (81 words)
- `17-implementation-playbooks-playbook-configure-rapid-attendance-entry`: Playbook: Configure Rapid Attendance Entry (86 words)
- `18-troubleshooting-decision-tree-a-is-the-problem-before-attendance-is-saved`: A. Is The Problem Before Attendance Is Saved? (103 words)
- `19-agent-task-recipes-recipe-prove-why-a-child-cannot-check-in`: Recipe: Prove Why A Child Cannot Check In (93 words)

## Community-Supported Only

- `6-primary-entities-and-relationships-grouptype-group-groupmember`: GroupType, Group, GroupMember
- `6-primary-entities-and-relationships-grouplocation-location-schedule`: GroupLocation, Location, Schedule
- `8-labels-deep-dive-legacy-labels-and-next-gen-labels`: Legacy Labels And Next-Gen Labels
- `8-labels-deep-dive-fonts-and-icons`: Fonts And Icons
- `10-attendance-deep-dive-count-only-attendance`: Count-Only Attendance
- `14-developer-api-lava-and-source-code-landmarks-lava-and-community-patterns`: Lava And Community Patterns
- `17-implementation-playbooks-playbook-implement-a-qr-code-attendance-pattern`: Playbook: Implement A QR Code Attendance Pattern
- `17-implementation-playbooks-playbook-implement-sms-text-attendance`: Playbook: Implement SMS/Text Attendance
- `19-agent-task-recipes-recipe-decide-between-check-in-group-attendance-rapid-attendance-qr-and-sms`: Recipe: Decide Between Check-In, Group Attendance, Rapid Attendance, QR, And SMS

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-check-in-mental-model`: 3. Check-In Mental Model
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-check-in-systems`: Check-In Systems
- `5-core-configuration-and-data-model-check-in-type-individual-vs-family`: Check-In Type: Individual vs Family
- `5-core-configuration-and-data-model-search`: Search
- `5-core-configuration-and-data-model-group-membership-behavior`: Group Membership Behavior
- `5-core-configuration-and-data-model-locations`: Locations
- `5-core-configuration-and-data-model-schedules`: Schedules
- `5-core-configuration-and-data-model-location-selection-strategy`: Location Selection Strategy
- `6-primary-entities-and-relationships-person-personalias-and-family`: Person, PersonAlias, And Family
- `6-primary-entities-and-relationships-grouptype-group-groupmember`: GroupType, Group, GroupMember
- `6-primary-entities-and-relationships-grouplocation-location-schedule`: GroupLocation, Location, Schedule
- `6-primary-entities-and-relationships-device-and-kiosk`: Device And Kiosk
- `6-primary-entities-and-relationships-attendance-and-attendanceoccurrence`: Attendance And AttendanceOccurrence
- `7-common-check-in-workflows-attended-check-in`: Attended Check-In
- `7-common-check-in-workflows-check-in-manager`: Check-In Manager
- `7-common-check-in-workflows-rapid-attendance-entry`: Rapid Attendance Entry
- `7-common-check-in-workflows-group-attendance`: Group Attendance
- `7-common-check-in-workflows-attendance-self-entry`: Attendance Self-Entry
- `7-common-check-in-workflows-proximity-attendance`: Proximity Attendance
- `8-labels-deep-dive-legacy-labels-and-next-gen-labels`: Legacy Labels And Next-Gen Labels
- `8-labels-deep-dive-label-data-model`: Label Data Model
- `8-labels-deep-dive-security-code-formatting`: Security Code Formatting
- `8-labels-deep-dive-merge-fields-and-lava`: Merge Fields And Lava
- `8-labels-deep-dive-fonts-and-icons`: Fonts And Icons
- `8-labels-deep-dive-label-troubleshooting-branches`: Label Troubleshooting Branches
- `9-mobile-check-in-deep-dive-configuration-checklist`: Configuration Checklist
- `9-mobile-check-in-deep-dive-mobile-and-eligibility`: Mobile And Eligibility
- `9-mobile-check-in-deep-dive-mobile-group-attendance-entry`: Mobile Group Attendance Entry
- `9-mobile-check-in-deep-dive-proximity-attendance`: Proximity Attendance
- `10-attendance-deep-dive-attendance-rows`: Attendance Rows
- `10-attendance-deep-dive-attendanceoccurrence-sundaydate`: AttendanceOccurrence SundayDate
- `10-attendance-deep-dive-attendance-analytics-block`: Attendance Analytics Block
- `10-attendance-deep-dive-count-only-attendance`: Count-Only Attendance
- `11-troubleshooting-deep-dive-symptom-no-check-in-locations-are-active`: Symptom: No Check-In Locations Are Active
- `11-troubleshooting-deep-dive-symptom-family-search-finds-nothing`: Symptom: Family Search Finds Nothing
- `11-troubleshooting-deep-dive-symptom-rapid-attendance-entry-too-slow-or-wrong-shape`: Symptom: Rapid Attendance Entry Too Slow Or Wrong Shape

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
