---
concept_id: groups
task_id: recipe-secure-leader-operations
title: Recipe: Secure leader operations
generated: true
---

# Recipe: Secure leader operations

Leaders can perform approved group tasks without unnecessary database or group-administration access.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Page`
- `Block`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Page`
- `Block`

## Steps

1. Inspect Group Type security.
2. Inspect parent-group and direct-group security.
3. Review the leader role’s capabilities.
4. Separate `Manage Members` from Edit or Administrate access.
5. Inspect Group Toolbox block settings and page security.
6. Decide whether the default People search is appropriate.
7. If not, configure an alternate controlled add-member path.
8. Test viewing, editing, roster management, attendance, and navigation as a representative leader.

## Do Not Assume

- Blank direct `Manage Members` rules mean no one can manage members.
- Group administrator designation grants leader security.
- Toolbox navigation limits replace entity security.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/workflows
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/documentation/church-management/reporting/metrics
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/7/361
