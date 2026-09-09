---
concept_id: groups
task_id: recipe-configure-attendance-follow-up
title: Recipe: Configure attendance follow-up
generated: true
---

# Recipe: Configure attendance follow-up

Leaders receive the intended reminders, digests, or absence notifications without duplicate or misrouted messages.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`
- `Attribute`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`
- `Attribute`

## Steps

1. Choose the operational mechanism: reminder, digest, absence notification, or attendance-report attributes.
2. Confirm the Group Type’s attendance settings and leader roles.
3. For a digest, construct the required parent-region-attendance hierarchy and use Weekly schedules.
4. Configure the correct System Communication and date or absence settings.
5. Verify the job scope and cadence.
6. Run a bounded test using non-production delivery controls where available.
7. Inspect job results, occurrences, recipient selection, and duplicate-suppression state.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://community.rockrms.com/rocku/workflows
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/documentation/church-management/reporting/metrics
