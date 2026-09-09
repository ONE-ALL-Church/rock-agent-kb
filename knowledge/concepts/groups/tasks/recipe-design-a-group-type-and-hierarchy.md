---
concept_id: groups
task_id: recipe-design-a-group-type-and-hierarchy
title: Recipe: Design a Group Type and hierarchy
generated: true
---

# Recipe: Design a Group Type and hierarchy

A bounded Group Type design with explicit hierarchy, roles, attributes, and security.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Attribute`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Attribute`

## Steps

1. Inventory existing Group Types and look for a reusable common type before proposing another.
2. Define whether the tree is structured or flexible.
3. List allowed child types at every level.
4. Define roles and mark only genuine leader roles as `Is Leader`.
5. Assign role capabilities for viewing, editing, member management, attendance, and check-in.
6. Place shared attributes on the base type and specialized attributes on the specialized type.
7. Define schedule modes, location options, history, requirements, sync, and security.
8. Test creation at every intended hierarchy level.

## Do Not Assume

- Attribute inheritance means every setting is inherited.
- A role named Leader has `Is Leader` enabled.
- A valid hierarchy works with the Attendance Digest.

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
