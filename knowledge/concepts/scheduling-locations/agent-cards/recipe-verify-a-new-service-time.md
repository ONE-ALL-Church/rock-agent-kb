---
concept_id: scheduling-locations
task_id: recipe-verify-a-new-service-time
title: Recipe: Verify A New Service Time
generated: true
---

# Recipe: Verify A New Service Time

Complete Verify A New Service Time with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Device`
- `Family`

## Entities And Tables

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Device`
- `Family`

## Steps

1. Schedule record and category.
2. Effective dates.
3. Check-in start offset.
4. Group/location schedule rows copied or created.
5. Overflow location rows.
6. Device location scope.
7. Check-In Manager schedule filter.
8. Test family result.
9. Attendance occurrence creation after check-in.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://community.rockrms.com/documentation/bookcontent/42/350
- https://community.rockrms.com/lava/commands/calendar-events
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
- https://community.rockrms.com/rocku/groups
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs
