---
concept_id: scheduling-locations
title: Scheduling And Locations Open Questions
generated: true
---

# Scheduling And Locations Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `known-gaps-and-live-verification`: Known Gaps And Live Verification (163 words)

## Community-Supported Only

- `reservations-and-calendar-coordination`: Reservations And Calendar Coordination
- `troubleshooting-decision-tree-a-reservation-and-calendar-event-do-not-match`: A Reservation And Calendar Event Do Not Match
- `agent-task-recipes-recipe-evaluate-reservation-to-calendar-synchronization`: Recipe: Evaluate Reservation-To-Calendar Synchronization
- `source-map-community-examples`: Community Examples

## Needs Live Verification

- `scope-and-boundaries`: Scope And Boundaries
- `locations-address-and-geographic-integrity`: Address And Geographic Integrity
- `group-and-volunteer-scheduling-confirmation-and-reminder-delivery`: Confirmation And Reminder Delivery
- `calendars-and-icalendar-recurring-schedule-dates-in-v19`: Recurring Schedule Dates In v19
- `reservations-and-calendar-coordination`: Reservations And Calendar Coordination
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-schedule-does-not-appear-in-a-check-in-scheduling-screen`: A Schedule Does Not Appear In A Check-In Scheduling Screen
- `troubleshooting-decision-tree-a-volunteer-is-missing-a-reminder`: A Volunteer Is Missing A Reminder
- `troubleshooting-decision-tree-a-calendar-file-or-feed-is-empty-stale-or-missing-events`: A Calendar File Or Feed Is Empty, Stale Or Missing Events
- `troubleshooting-decision-tree-a-date-based-query-misses-recurring-schedule-occurrences`: A Date-Based Query Misses Recurring Schedule Occurrences
- `troubleshooting-decision-tree-the-named-location-tree-will-not-load`: The Named Location Tree Will Not Load
- `troubleshooting-decision-tree-check-in-manager-attendance-changes-do-not-update-in-real-time`: Check-In Manager Attendance Changes Do Not Update In Real Time
- `agent-task-recipes-recipe-build-a-check-in-location-hierarchy`: Recipe: Build A Check-In Location Hierarchy
- `agent-task-recipes-recipe-prove-why-a-check-in-room-is-not-available`: Recipe: Prove Why A Check-In Room Is Not Available
- `agent-task-recipes-recipe-clone-a-check-in-schedule-for-a-special-event`: Recipe: Clone A Check-In Schedule For A Special Event
- `agent-task-recipes-recipe-configure-a-group-type-for-volunteer-scheduling`: Recipe: Configure A Group Type For Volunteer Scheduling
- `agent-task-recipes-recipe-prepare-volunteer-availability-for-auto-schedule`: Recipe: Prepare Volunteer Availability For Auto-Schedule
- `agent-task-recipes-recipe-publish-and-test-an-event-calendar-feed`: Recipe: Publish And Test An Event Calendar Feed
- `agent-task-recipes-recipe-evaluate-reservation-to-calendar-synchronization`: Recipe: Evaluate Reservation-To-Calendar Synchronization
- `agent-task-recipes-recipe-audit-a-v19-date-based-schedule-query`: Recipe: Audit A V19 Date-Based Schedule Query

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
