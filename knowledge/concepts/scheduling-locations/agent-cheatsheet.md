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
| `17.2` | core | Fixed an issue where removing a Schedule from one Group Location also deleted capacity settings for that same Schedule in other Group Locations. Fixes: #6315 |
| `19.1` | core | Added a new Schedule Builder Field Type and Attribute that allows administrators to create and select custom schedules using the standard Schedule Builder interface. |
| `18.3` | core | Fixed the Check-In Type Detail Block "Scheduled Times" list to exclude schedules from Archived or Inactive Groups that still have a GroupLocationSchedule assigned. Previously, schedules from these Groups could appear in the list, resulting  |
| `17.5` | core | Added the ability to filter by Group Location Schedules to target more specific people based on their schedule for a group or sign up project in a data view. |
| `16.7` | core | Added a Group Schedule Coordinator that can be notified when a Person accepts, declines or self-schedules for a Schedule occurrence tied to the Group. |
| `16.6` | core | Fixed issue of Group Schedule Notifications and Group Schedule Reminders not honoring the schedule exlusions. Fixes: #5880 |
| `16.4` | core | Modified the calendar export to improve support for specific date schedules in Microsoft/Google/Apple calendar applications. Fixes: #5150 |
| `16.0` | core | Fixed an issue where the group schedule calendar feed would create duplicate calendar entries for the same scheduled occurrence. |
| `15.2` | core | Updated the SignUpFinder block to return the Schedule name and available date range for Schedules with multiple dates when displaying the Schedule filter. Fixes: #5513 |
| `19.1` | core | Improved the Group Scheduler block to keep the occurrence date and its Schedules fixed at the top of the screen while scrolling. Additionally, the Group name now appears above each Location. These updates make it easier for a scheduler to s |
| `18.3` | core | Improved the friendly schedule text display for single-date schedules to use a more friendly format (e.g., "Once on March 29, 2026 at 11:00 AM" instead of "Once at 3/29/2026 11:00 AM"). Fixes: #6694 |
| `17.5` | core | Improved the layout of the Next-Gen Check-In schedule select screen when too many schedules were available to fit in one row. The screen will now wrap the buttons to multiple rows of buttons. Fixes: #6371 |
| `17.5` | core | Fixed an issue where EventScheduledInstance Lava commands did not work in the Calendar Item List and Calendar Item Occurrence List blocks due to security changes. Fixes: #6386 |
| `17.1` | core | Fixed legacy check-in issue where it didn't check schedule categories for exclusions when loading schedules. Fixes: #6196 |
| `17.1` | core | Fixed the logic that sets a schedule's EffectiveEndDateTime to be more accurate when a schedule's duration passes midnight. This ensures it better aligns with iCal's DTEND behavior. Fixes: #6227 |
| `17.0` | core | Added ability to copy which locations are enabled for a check-in configuration from one schedule to another. |
| `17.0` | core | Updated the logic that opens/closes room (locations) to write the changes to history. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
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
| `approved-claim-coverage` | citation-only | live verification |
