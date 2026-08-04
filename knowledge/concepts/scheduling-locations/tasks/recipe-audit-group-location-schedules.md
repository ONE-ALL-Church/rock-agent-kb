---
concept_id: scheduling-locations
task_id: recipe-audit-group-location-schedules
title: Recipe: Audit Group Location Schedules
generated: true
---

# Recipe: Audit Group Location Schedules

The source query shape is documented in `View_GroupLocationSchedules.sql` (source).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`

## Steps

1. `Schedule`
2. `GroupLocationSchedule`
3. `GroupLocation`
4. `Group`
5. `Location`
6. Group name and ID.
7. Location name and ID.
8. Schedule name and ID.
9. Active/archive status.
10. Parent location path.
11. Capacity config if applicable.
12. Any rows attached to inactive or archived groups.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/documentation/bookcontent/42/350
- https://community.rockrms.com/lava/commands/calendar-events
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
- https://community.rockrms.com/rocku/groups
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs
