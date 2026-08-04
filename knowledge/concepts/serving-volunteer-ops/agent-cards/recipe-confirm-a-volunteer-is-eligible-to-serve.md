---
concept_id: serving-volunteer-ops
task_id: recipe-confirm-a-volunteer-is-eligible-to-serve
title: Recipe: Confirm A Volunteer Is Eligible To Serve
generated: true
---

# Recipe: Confirm A Volunteer Is Eligible To Serve

If requirement source is unclear, say: "Inspect the group requirement definition and its backing data source in the live Rock instance."

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Schedule`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Group`
- `Schedule`
- `Workflow`
- `Attribute`

## Steps

1. person active status;
2. age/grade if relevant;
3. group membership;
4. role;
5. group member status;
6. group requirements;
7. person attributes backing requirements;
8. background check/training state;
9. workflow/application state;
10. schedule preferences;
11. local ministry approval.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/rocku/groups/group-details
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
