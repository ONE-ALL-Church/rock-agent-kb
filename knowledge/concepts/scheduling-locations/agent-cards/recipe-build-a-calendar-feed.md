---
concept_id: scheduling-locations
task_id: recipe-build-a-calendar-feed
title: Recipe: Build A Calendar Feed
generated: true
---

# Recipe: Build A Calendar Feed

Complete Build A Calendar Feed with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Schedule`
- `Campus`
- `Workflow`

## Entities And Tables

- `Group`
- `Schedule`
- `Campus`
- `Workflow`

## Steps

1. Choose source: event calendar, room reservations, group schedule, or custom workflow data.
2. Limit date range.
3. Validate iCal output.
4. Set correct content type.
5. Avoid exposing private notes or contact data.
6. Test Outlook, Google Calendar, and Apple Calendar.
7. Decide whether updates overwrite user edits.
8. Use stable UID values.
9. Document ownership and sharing.

## Do Not Assume

- Avoid exposing private notes or contact data.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/42/350
- https://community.rockrms.com/lava/commands/calendar-events
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
- https://community.rockrms.com/rocku/groups
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs
- https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board
- https://community.rockrms.com/recipes/531/Schedule-WithAvailableSlots
