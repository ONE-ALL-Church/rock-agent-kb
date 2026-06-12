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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Prove Why A Check-In Room Is Not Available](tasks/recipe-prove-why-a-check-in-room-is-not-available.md): Follow the guide section for Recipe: Prove Why A Check-In Room Is Not Available.
- [Recipe: Audit Group Location Schedules](tasks/recipe-audit-group-location-schedules.md): Follow the guide section for Recipe: Audit Group Location Schedules.
- [Recipe: Verify A New Service Time](tasks/recipe-verify-a-new-service-time.md): Follow the guide section for Recipe: Verify A New Service Time.
- [Recipe: Build A Facilities Daily Report](tasks/recipe-build-a-facilities-daily-report.md): Follow the guide section for Recipe: Build A Facilities Daily Report.
- [Recipe: Build A Calendar Feed](tasks/recipe-build-a-calendar-feed.md): Follow the guide section for Recipe: Build A Calendar Feed.
- [Recipe: Diagnose Schedule API Issues](tasks/recipe-diagnose-schedule-api-issues.md): Follow the guide section for Recipe: Diagnose Schedule API Issues.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-49: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 50-72: 2. Scope And Terminology (normal)
- `3-scheduling-and-locations-mental-model` lines 73-108: 3. Scheduling And Locations Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 109-120: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-locations` lines 123-151: Locations (high)
- `5-core-configuration-and-data-model-schedules` lines 152-175: Schedules (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `AttendanceOccurrence`: Occurrence context for attendance, including group, schedule, location, date, and SundayDate.
- `Attribute`: Rock concept/entity referenced by the scheduling-locations guide.
- `Block`: Rock concept/entity referenced by the scheduling-locations guide.
- `Campus`: Rock concept/entity referenced by the scheduling-locations guide.
- `Check-in Configuration`: Rock concept/entity referenced by the scheduling-locations guide.
- `Device`: Kiosk, printer, or device record that affects check-in availability and label routing.
- `Family`: Rock concept/entity referenced by the scheduling-locations guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the scheduling-locations guide.
- `Label`: Rock concept/entity referenced by the scheduling-locations guide.
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
