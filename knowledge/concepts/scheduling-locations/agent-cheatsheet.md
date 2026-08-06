---
concept_id: scheduling-locations
title: Scheduling And Locations Agent Cheatsheet
generated: true
---

# Scheduling And Locations Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Prove Why A Check-In Room Is Not Available](tasks/recipe-prove-why-a-check-in-room-is-not-available.md) | `Person`, `Group`, `Location`, `Schedule`, `Device`, `Check-in Configuration`, `Workflow`, `Campus` | `Person`, `Group`, `Location`, `Schedule`, `Device`, `Check-in Configuration`, `Workflow`, `Campus` |
| [Recipe: Audit Group Location Schedules](tasks/recipe-audit-group-location-schedules.md) | `Group`, `Location`, `Schedule` | `Group`, `Location`, `Schedule` |
| [Recipe: Verify A New Service Time](tasks/recipe-verify-a-new-service-time.md) | `Attendance`, `Group`, `Location`, `Schedule`, `Device`, `Family` | `Attendance`, `Group`, `Location`, `Schedule`, `Device`, `Family` |
| [Recipe: Build A Facilities Daily Report](tasks/recipe-build-a-facilities-daily-report.md) |  |  |
| [Recipe: Build A Calendar Feed](tasks/recipe-build-a-calendar-feed.md) | `Group`, `Schedule`, `Campus`, `Workflow` | `Group`, `Schedule`, `Campus`, `Workflow` |
| [Recipe: Diagnose Schedule API Issues](tasks/recipe-diagnose-schedule-api-issues.md) | `Schedule` | `Schedule` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `AttendanceOccurrence` | `Attendance`, `Group`, `Schedule`, `Location`, `Campus` | Use this for reporting context. Check group, location, schedule, and SundayDate before blaming the UI. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
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
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-locations` | high | live verification |
| `5-core-configuration-and-data-model-schedules` | normal | live verification |
| `5-core-configuration-and-data-model-groups-group-locations-and-schedules` | high | live verification |
| `5-core-configuration-and-data-model-attendance-and-assignments` | normal | live verification |
| `6-primary-entities-and-relationships-schedule-entity` | community-supported | live verification |
| `6-primary-entities-and-relationships-grouplocationscheduleconfig` | community-supported | live verification |
| `6-primary-entities-and-relationships-reservation-entities` | community-supported | live verification |
| `7-common-scheduling-and-locations-workflows-add-a-new-check-in-room` | high | live verification |
| `7-common-scheduling-and-locations-workflows-clone-a-check-in-schedule` | high | live verification |
| `7-common-scheduling-and-locations-workflows-create-event-calendar-occurrences` | normal | live verification |
| `7-common-scheduling-and-locations-workflows-manage-room-reservations` | community-supported | live verification |
| `8-locations-deep-dive-location-types` | normal | live verification |
| `8-locations-deep-dive-thresholds-and-capacity` | normal | live verification |
| `8-locations-deep-dive-location-selection-strategy` | high | live verification |
| `8-locations-deep-dive-location-seo-and-public-pages` | community-supported | community-supported |
| `9-schedules-deep-dive-effective-dates-and-recurrence` | normal | live verification |
| `9-schedules-deep-dive-check-in-start-offsets` | normal | live verification |
| `9-schedules-deep-dive-schedule-exclusions` | normal | live verification |
| `9-schedules-deep-dive-schedule-templates-and-preferences` | community-supported | live verification |
| `9-schedules-deep-dive-schedule-builder-field-type` | normal | live verification |
| `10-reservations-deep-dive-reservation-lifecycle` | community-supported | community-supported |
| `10-reservations-deep-dive-approvals` | community-supported | community-supported |
| `10-reservations-deep-dive-reservation-calendar-views` | community-supported | live verification |
| `10-reservations-deep-dive-reservation-to-event-calendar-linkage` | community-supported | live verification |
| `10-reservations-deep-dive-reservation-ical-feeds` | community-supported | live verification |
| `11-related-rock-areas-check-in-groups-events-cms-groups` | normal | live verification |
| `11-related-rock-areas-check-in-groups-events-cms-events` | normal | live verification |
| `12-administration-and-operational-guardrails-naming-conventions` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-security` | community-supported | community-supported |
| `12-administration-and-operational-guardrails-avoid-raw-sql-writes-unless-necessary` | structural | live verification |
| `12-administration-and-operational-guardrails-cache-and-time` | community-supported | live verification |
| `13-developer-api-lava-and-source-code-landmarks-mobile-blocks-and-commands` | normal | live verification |
| `14-reporting-analytics-and-model-map-basic-relationship-queries` | normal | live verification |
| `14-reporting-analytics-and-model-map-schedule-status-board` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-scheduling-analytics` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-facilities-reporting` | community-supported | live verification |
| `15-version-and-release-caveats` | high | live verification |
| `16-implementation-playbooks-playbook-new-service-time-for-check-in` | high | live verification |
| `16-implementation-playbooks-playbook-new-serving-team-scheduling-setup` | normal | live verification |
| `16-implementation-playbooks-playbook-room-management-reservation-calendar-sync` | community-supported | live verification |
| `16-implementation-playbooks-playbook-internal-staff-calendar` | community-supported | live verification |
| `17-troubleshooting-decision-tree-a-schedule-is-missing-from-check-in` | normal | live verification |
| `17-troubleshooting-decision-tree-a-room-is-missing-from-check-in` | normal | live verification |
| `17-troubleshooting-decision-tree-group-scheduler-capacity-looks-wrong` | normal | live verification |
| `17-troubleshooting-decision-tree-reservation-and-calendar-are-out-of-sync` | community-supported | live verification |
| `18-agent-task-recipes-recipe-verify-a-new-service-time` | structural | live verification |
| `18-agent-task-recipes-recipe-build-a-facilities-daily-report` | community-supported | community-supported |
| `18-agent-task-recipes-recipe-build-a-calendar-feed` | community-supported | live verification |
| `18-agent-task-recipes-recipe-diagnose-schedule-api-issues` | community-supported | live verification |
| `approved-claim-coverage` | citation-only | live verification |
| `19-source-map-and-dependency-notes` | high | live verification |
