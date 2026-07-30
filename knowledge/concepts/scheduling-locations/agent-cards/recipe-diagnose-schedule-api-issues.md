---
concept_id: scheduling-locations
task_id: recipe-diagnose-schedule-api-issues
title: Recipe: Diagnose Schedule API Issues
generated: true
---

# Recipe: Diagnose Schedule API Issues

The provided Q&A mentions a v12.8 browser exception involving `FriendlyScheduleText` lacking a setter, but it has no answer in the source pack, so do not treat it as a solved known issue (REST API for Schedules).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. HTTP method.
2. Authentication and authorization.
3. CORS/browser constraints.
4. Whether the payload attempts to set computed/read-only properties.
5. Rock version.
6. API endpoint shape.
7. Browser console and server exception logs.

## Do Not Assume

- The provided Q&A mentions a v12.8 browser exception involving `FriendlyScheduleText` lacking a setter, but it has no answer in the source pack, so do not treat it as a solved known issue (REST API for Schedules).

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://community.rockrms.com/recipes/280
- https://community.rockrms.com/recipes/531/Schedule-WithAvailableSlots
- https://www.triumph.tech/resources/github-spotlight-262025
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/42
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs
