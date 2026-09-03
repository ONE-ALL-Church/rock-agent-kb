---
concept_id: scheduling-locations
title: Scheduling And Locations Agent Cheatsheet
generated: true
---

# Scheduling And Locations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Build A Check-In Location Hierarchy](tasks/recipe-build-a-check-in-location-hierarchy.md) | `Location`, `Campus`, `Family` | `Location`, `Campus`, `Family` |
| [Recipe: Prove Why A Check-In Room Is Not Available](tasks/recipe-prove-why-a-check-in-room-is-not-available.md) | `Check-in Configuration`, `Person`, `Device`, `Group`, `GroupLocation`, `GroupLocationSchedule`, `Location`, `Schedule`, `Workflow` | `Person`, `Device`, `Group`, `GroupLocation`, `Location`, `Schedule`, `Workflow` |
| [Recipe: Clone A Check-In Schedule For A Special Event](tasks/recipe-clone-a-check-in-schedule-for-a-special-event.md) | `Location`, `Schedule`, `Check-in Configuration`, `Block` | `Location`, `Schedule`, `Check-in Configuration`, `Block` |
| [Recipe: Configure A Group Type For Volunteer Scheduling](tasks/recipe-configure-a-group-type-for-volunteer-scheduling.md) | `Group`, `GroupType`, `Location`, `Schedule`, `Workflow` | `Group`, `GroupType`, `Location`, `Schedule`, `Workflow` |
| [Recipe: Prepare Volunteer Availability For Auto-Schedule](tasks/recipe-prepare-volunteer-availability-for-auto-schedule.md) | `Person`, `Group`, `Location`, `Schedule`, `GroupType` | `Person`, `Group`, `Location`, `Schedule`, `GroupType` |
| [Recipe: Publish And Test An Event Calendar Feed](tasks/recipe-publish-and-test-an-event-calendar-feed.md) | `Schedule`, `Campus`, `Location`, `Workflow` | `Schedule`, `Campus`, `Location`, `Workflow` |
| [Recipe: Evaluate Reservation-To-Calendar Synchronization](tasks/recipe-evaluate-reservation-to-calendar-synchronization.md) | `Location`, `Schedule`, `Workflow`, `Attribute` | `Location`, `Schedule`, `Workflow`, `Attribute` |
| [Recipe: Audit A V19 Date-Based Schedule Query](tasks/recipe-audit-a-v19-date-based-schedule-query.md) | `Schedule` | `Schedule` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupLocation` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupLocationSchedule` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669 |
| `17.2` | core | Fixed an issue where Group Schedule ICS calendar events had unclear summaries. The Summary now uses the format "Group - Location - Schedule" to provide clarity for calendar events. Fixes: #6174 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | normal | live verification |
| `locations-address-and-geographic-integrity` | normal | live verification |
| `group-and-volunteer-scheduling-confirmation-and-reminder-delivery` | normal | live verification |
| `calendars-and-icalendar-recurring-schedule-dates-in-v19` | citation-only | live verification |
| `reservations-and-calendar-coordination` | community-supported | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-schedule-does-not-appear-in-a-check-in-scheduling-screen` | normal | live verification |
| `troubleshooting-decision-tree-a-volunteer-is-missing-a-reminder` | normal | live verification |
| `troubleshooting-decision-tree-a-calendar-file-or-feed-is-empty-stale-or-missing-events` | high | live verification |
| `troubleshooting-decision-tree-a-date-based-query-misses-recurring-schedule-occurrences` | citation-only | live verification |
| `troubleshooting-decision-tree-a-reservation-and-calendar-event-do-not-match` | community-supported | community-supported |
| `troubleshooting-decision-tree-the-named-location-tree-will-not-load` | normal | live verification |
| `troubleshooting-decision-tree-check-in-manager-attendance-changes-do-not-update-in-real-time` | citation-only | live verification |
| `agent-task-recipes-recipe-build-a-check-in-location-hierarchy` | normal | live verification |
| `agent-task-recipes-recipe-prove-why-a-check-in-room-is-not-available` | normal | live verification |
| `agent-task-recipes-recipe-clone-a-check-in-schedule-for-a-special-event` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-group-type-for-volunteer-scheduling` | normal | live verification |
| `agent-task-recipes-recipe-prepare-volunteer-availability-for-auto-schedule` | normal | live verification |
| `agent-task-recipes-recipe-publish-and-test-an-event-calendar-feed` | normal | live verification |
| `agent-task-recipes-recipe-evaluate-reservation-to-calendar-synchronization` | community-supported | live verification |
| `agent-task-recipes-recipe-audit-a-v19-date-based-schedule-query` | citation-only | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
| `source-map-community-examples` | community-supported | community-supported |
