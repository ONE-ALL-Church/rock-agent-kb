---
concept_id: scheduling-locations
title: Scheduling And Locations Open Questions
generated: true
---

# Scheduling And Locations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `6-primary-entities-and-relationships-schedule-entity`: Schedule Entity
- `6-primary-entities-and-relationships-grouplocationscheduleconfig`: GroupLocationScheduleConfig
- `6-primary-entities-and-relationships-reservation-entities`: Reservation Entities
- `7-common-scheduling-and-locations-workflows-manage-room-reservations`: Manage Room Reservations
- `8-locations-deep-dive-location-seo-and-public-pages`: Location SEO And Public Pages
- `9-schedules-deep-dive-schedule-templates-and-preferences`: Schedule Templates And Preferences
- `10-reservations-deep-dive-reservation-lifecycle`: Reservation Lifecycle
- `10-reservations-deep-dive-approvals`: Approvals
- `10-reservations-deep-dive-reservation-calendar-views`: Reservation Calendar Views
- `10-reservations-deep-dive-reservation-to-event-calendar-linkage`: Reservation To Event Calendar Linkage
- `10-reservations-deep-dive-reservation-ical-feeds`: Reservation iCal Feeds
- `12-administration-and-operational-guardrails-naming-conventions`: Naming Conventions
- `12-administration-and-operational-guardrails-security`: Security
- `12-administration-and-operational-guardrails-cache-and-time`: Cache And Time
- `14-reporting-analytics-and-model-map-schedule-status-board`: Schedule Status Board
- `14-reporting-analytics-and-model-map-facilities-reporting`: Facilities Reporting
- `16-implementation-playbooks-playbook-room-management-reservation-calendar-sync`: Playbook: Room Management Reservation Calendar Sync
- `16-implementation-playbooks-playbook-internal-staff-calendar`: Playbook: Internal Staff Calendar
- `17-troubleshooting-decision-tree-reservation-and-calendar-are-out-of-sync`: Reservation And Calendar Are Out Of Sync
- `18-agent-task-recipes-recipe-build-a-facilities-daily-report`: Recipe: Build A Facilities Daily Report
- `18-agent-task-recipes-recipe-build-a-calendar-feed`: Recipe: Build A Calendar Feed
- `18-agent-task-recipes-recipe-diagnose-schedule-api-issues`: Recipe: Diagnose Schedule API Issues

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-locations`: Locations
- `5-core-configuration-and-data-model-schedules`: Schedules
- `5-core-configuration-and-data-model-groups-group-locations-and-schedules`: Groups, Group Locations, And Schedules
- `5-core-configuration-and-data-model-attendance-and-assignments`: Attendance And Assignments
- `6-primary-entities-and-relationships-schedule-entity`: Schedule Entity
- `6-primary-entities-and-relationships-grouplocationscheduleconfig`: GroupLocationScheduleConfig
- `6-primary-entities-and-relationships-reservation-entities`: Reservation Entities
- `7-common-scheduling-and-locations-workflows-add-a-new-check-in-room`: Add A New Check-In Room
- `7-common-scheduling-and-locations-workflows-clone-a-check-in-schedule`: Clone A Check-In Schedule
- `7-common-scheduling-and-locations-workflows-create-event-calendar-occurrences`: Create Event Calendar Occurrences
- `7-common-scheduling-and-locations-workflows-manage-room-reservations`: Manage Room Reservations
- `8-locations-deep-dive-location-types`: Location Types
- `8-locations-deep-dive-thresholds-and-capacity`: Thresholds And Capacity
- `8-locations-deep-dive-location-selection-strategy`: Location Selection Strategy
- `9-schedules-deep-dive-effective-dates-and-recurrence`: Effective Dates And Recurrence
- `9-schedules-deep-dive-check-in-start-offsets`: Check-In Start Offsets
- `9-schedules-deep-dive-schedule-exclusions`: Schedule Exclusions
- `9-schedules-deep-dive-schedule-templates-and-preferences`: Schedule Templates And Preferences
- `9-schedules-deep-dive-schedule-builder-field-type`: Schedule Builder Field Type
- `10-reservations-deep-dive-reservation-calendar-views`: Reservation Calendar Views
- `10-reservations-deep-dive-reservation-to-event-calendar-linkage`: Reservation To Event Calendar Linkage
- `10-reservations-deep-dive-reservation-ical-feeds`: Reservation iCal Feeds
- `11-related-rock-areas-check-in-groups-events-cms-groups`: Groups
- `11-related-rock-areas-check-in-groups-events-cms-events`: Events
- `12-administration-and-operational-guardrails-avoid-raw-sql-writes-unless-necessary`: Avoid Raw SQL Writes Unless Necessary
- `12-administration-and-operational-guardrails-cache-and-time`: Cache And Time
- `13-developer-api-lava-and-source-code-landmarks-mobile-blocks-and-commands`: Mobile Blocks And Commands
- `14-reporting-analytics-and-model-map-basic-relationship-queries`: Basic Relationship Queries
- `14-reporting-analytics-and-model-map-scheduling-analytics`: Scheduling Analytics
- `14-reporting-analytics-and-model-map-facilities-reporting`: Facilities Reporting
- `15-version-and-release-caveats`: 15. Version And Release Caveats
- `16-implementation-playbooks-playbook-new-service-time-for-check-in`: Playbook: New Service Time For Check-In
- `16-implementation-playbooks-playbook-new-serving-team-scheduling-setup`: Playbook: New Serving Team Scheduling Setup
- `16-implementation-playbooks-playbook-room-management-reservation-calendar-sync`: Playbook: Room Management Reservation Calendar Sync
- `16-implementation-playbooks-playbook-internal-staff-calendar`: Playbook: Internal Staff Calendar
- `17-troubleshooting-decision-tree-a-schedule-is-missing-from-check-in`: A Schedule Is Missing From Check-In

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
