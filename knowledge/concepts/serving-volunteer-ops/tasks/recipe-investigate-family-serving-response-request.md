---
concept_id: serving-volunteer-ops
task_id: recipe-investigate-family-serving-response-request
title: Recipe: Investigate Family Serving Response Request
generated: true
---

# Recipe: Investigate Family Serving Response Request

Source pattern: Manage Family Members' Serving Requests on MyAccount.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `Schedule`
- `Family`
- `Workflow`

## Entities And Tables

- `Attendance`
- `Person`
- `Schedule`
- `Family`
- `Workflow`

## Steps

1. Identify current logged-in person.
2. Identify target scheduled person.
3. Verify family relationship.
4. Verify age and role policy.
5. Verify scheduled attendance row.
6. Verify authorization to respond.
7. Verify workflow action updates only that row.
8. Log responder.
9. Preserve decline reason.
10. Test with spouse, minor child, adult child, and unrelated person.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
- https://community.rockrms.com/rocku/groups/group-attendance
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs
- https://community.rockrms.com/recipes/489
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/recipes/356
