---
concept_id: serving-volunteer-ops
task_id: recipe-verify-schedule-confirmation-send-health
title: Recipe: Verify Schedule Confirmation Send Health
generated: true
---

# Recipe: Verify Schedule Confirmation Send Health

Complete Verify Schedule Confirmation Send Health with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`
- `Block`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`
- `Block`

## Steps

1. selected group/date/location/schedule;
2. eligible recipient count;
3. sent count;
4. warnings;
5. errors;
6. communication history;
7. failed recipients;
8. system communication template;
9. sender fallback;
10. confirmation link route.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://community.rockrms.com/rocku/groups/group-details
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
