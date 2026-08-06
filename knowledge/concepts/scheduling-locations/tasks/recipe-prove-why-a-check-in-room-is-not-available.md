---
concept_id: scheduling-locations
task_id: recipe-prove-why-a-check-in-room-is-not-available
title: Recipe: Prove Why A Check-In Room Is Not Available
generated: true
---

# Recipe: Prove Why A Check-In Room Is Not Available

Complete Prove Why A Check-In Room Is Not Available with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Location`
- `Schedule`
- `Device`
- `Check-in Configuration`
- `Workflow`
- `Campus`

## Entities And Tables

- `Person`
- `Group`
- `Location`
- `Schedule`
- `Device`
- `Check-in Configuration`
- `Workflow`
- `Campus`

## Steps

1. Check-in configuration name and ID.
2. Group ID and path.
3. Location ID and path.
4. Schedule ID and name.
5. Device ID and device locations.
6. Person ID and eligibility rule.
7. Current Rock time.
8. Relevant workflow filter states.
9. Does the group/location/schedule link exist?
10. Is the location active and open?
11. Is the schedule active right now?
12. Did a workflow filter exclude it?
13. Is the person eligible?
14. Is the device scoped correctly?
15. Is there a version caveat?
16. Is `Location.IsActive` true?
17. Is the room closed in Check-In Manager?
18. Is the room under the expected campus/building parent?
19. Is the location assigned to the group?
20. Is the group/location enabled for the schedule?
21. Is the device allowed to see that location?
22. Is the room full according to soft threshold?
23. Did location selection strategy auto-select a different room?
24. Does the person meet age, grade, ability, requirement, and group membership rules?
25. Is the room an overflow location that has not been scheduled?
26. Is a workflow filter removing or excluding it?

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
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterActiveLocations.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByThreshold.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsBySchedule.cs
