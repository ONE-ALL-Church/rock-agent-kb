---
concept_id: groups
task_id: recipe-configure-focused-attendance-entry
title: Recipe: Configure focused attendance entry
generated: true
---

# Recipe: Configure focused attendance entry

Ministry staff can enter attendance and only the related actions appropriate to that workflow.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Family`
- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Family`
- `Workflow`
- `Page`
- `Block`

## Steps

1. Select the target Group and attendance date.
2. Confirm the valid location and schedule context.
3. Review which related actions are needed: family changes, new family members, notes, prayer requests, or workflows.
4. Enable only those actions in the block settings.
5. Create separate page variants where ministries require different action sets.
6. Confirm operator permissions.
7. Test a representative attendance occurrence and read back the saved state.

## Do Not Assume

- Every group has a usable location or schedule.
- Every Rapid Attendance Entry page exposes the same actions.
- A visible workflow button proves that the workflow completed successfully.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/recipes/519
