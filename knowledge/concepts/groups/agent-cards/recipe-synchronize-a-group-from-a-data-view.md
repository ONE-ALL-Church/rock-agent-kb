---
concept_id: groups
task_id: recipe-synchronize-a-group-from-a-data-view
title: Recipe: Synchronize a group from a Data View
generated: true
---

# Recipe: Synchronize a group from a Data View

Membership for one role follows a reviewed population rule at a sustainable cadence.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `GroupType`
- `Workflow`
- `Attribute`

## Entities And Tables

- `DataView`
- `Group`
- `GroupType`
- `Workflow`
- `Attribute`

## Steps

1. Enable Group Sync on the Group Type.
2. Create and validate the source Data View.
3. Add the sync to the target group.
4. Choose one assigned role.
5. Set the lowest operationally acceptable frequency.
6. Review welcome, exit, and login-creation options.
7. Configure another sync only if another role needs independent management.
8. Run the Group Sync job and reconcile Data View results with resulting membership.
9. For communication lists, refresh and reconcile immediately before an authorized send.
10. Inspect workflow action order and logs.
11. Check whether membership, communications, or attributes changed before the failure.
12. Identify which action actually failed.
13. Make retry logic account for already-completed side effects.
14. Stop before retrying if duplicate membership, duplicate communication, or repeated downstream actions remain possible.

## Do Not Assume

- Counts do not reconcile.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/documentation/church-management/reporting/metrics
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/7/361
- https://community.rockrms.com/documentation/bookcontent/7
