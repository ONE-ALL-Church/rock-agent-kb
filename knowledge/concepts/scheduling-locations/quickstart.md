---
concept_id: scheduling-locations
title: Scheduling And Locations Quickstart
generated: true
---

# Scheduling And Locations Quickstart

Locations, schedules, rooms, resources, reservations, calendars, and operational planning.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Build A Check-In Location Hierarchy](tasks/recipe-build-a-check-in-location-hierarchy.md): Named Locations represent the intended campus, building and room structure.
- [Recipe: Prove Why A Check-In Room Is Not Available](tasks/recipe-prove-why-a-check-in-room-is-not-available.md): Identify the first configuration, schedule, device, capacity, eligibility, or workflow filter that removes a specific room for a specific person and check-in attempt.
- [Recipe: Clone A Check-In Schedule For A Special Event](tasks/recipe-clone-a-check-in-schedule-for-a-special-event.md): A destination schedule starts with the source schedule’s enabled locations.
- [Recipe: Configure A Group Type For Volunteer Scheduling](tasks/recipe-configure-a-group-type-for-volunteer-scheduling.md): Groups of the selected type can schedule volunteers with defined confirmation and reminder behavior.
- [Recipe: Prepare Volunteer Availability For Auto-Schedule](tasks/recipe-prepare-volunteer-availability-for-auto-schedule.md): A volunteer has usable availability, reminder and assignment preferences.
- [Recipe: Publish And Test An Event Calendar Feed](tasks/recipe-publish-and-test-an-event-calendar-feed.md): The intended Rock calendar is available through a bounded iCalendar feed.
- [Recipe: Evaluate Reservation-To-Calendar Synchronization](tasks/recipe-evaluate-reservation-to-calendar-synchronization.md): The organization has a safe compatibility and ownership decision before implementing synchronization.
- [Recipe: Audit A V19 Date-Based Schedule Query](tasks/recipe-audit-a-v19-date-based-schedule-query.md): A date-based report uses Rock’s v19 materialized schedule occurrences.

## High-Signal Sections

- `agent-summary` lines 34-46: Agent Summary (normal)
- `scope-and-boundaries` lines 47-64: Scope And Boundaries (normal)
- `mental-model` lines 65-80: Mental Model (high)
- `locations-positional-and-named-locations` lines 83-94: Positional And Named Locations (normal)
- `locations-named-location-hierarchy` lines 95-102: Named Location Hierarchy (high)
- `locations-address-and-geographic-integrity` lines 103-108: Address And Geographic Integrity (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the scheduling-locations guide.
- `Block`: Rock concept/entity referenced by the scheduling-locations guide.
- `Campus`: Rock concept/entity referenced by the scheduling-locations guide.
- `Check-in Configuration`: Rock concept/entity referenced by the scheduling-locations guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the scheduling-locations guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupLocation`: Rock concept/entity referenced by the scheduling-locations guide.
- `GroupLocationSchedule`: Rock concept/entity referenced by the scheduling-locations guide.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.

## Version Caveats

- `18.3`: Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669
- `17.2`: Fixed an issue where Group Schedule ICS calendar events had unclear summaries. The Summary now uses the format "Group - Location - Schedule" to provide clarity for calendar events. Fixes: #6174
- `17.2`: Fixed an issue where removing a Schedule from one Group Location also deleted capacity settings for that same Schedule in other Group Locations. Fixes: #6315
- `19.1`: Added a new Schedule Builder Field Type and Attribute that allows administrators to create and select custom schedules using the standard Schedule Builder interface.
- `18.3`: Fixed the Check-In Type Detail Block "Scheduled Times" list to exclude schedules from Archived or Inactive Groups that still have a GroupLocationSchedule assigned. Previously, schedules from these Groups could appear in
- `17.5`: Added the ability to filter by Group Location Schedules to target more specific people based on their schedule for a group or sign up project in a data view.
- `16.7`: Added a Group Schedule Coordinator that can be notified when a Person accepts, declines or self-schedules for a Schedule occurrence tied to the Group.
- `16.6`: Fixed issue of Group Schedule Notifications and Group Schedule Reminders not honoring the schedule exlusions. Fixes: #5880

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
