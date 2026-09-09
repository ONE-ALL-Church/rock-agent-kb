---
concept_id: groups
task_id: recipe-move-group-members-safely
title: Recipe: Move group members safely
generated: true
---

# Recipe: Move group members safely

Selected memberships move without unexpected loss of notes or attributes.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Label`
- `Workflow`
- `Attribute`
- `DataView`
- `GroupType`

## Entities And Tables

- `Person`
- `Group`
- `Label`
- `Workflow`
- `Attribute`
- `DataView`
- `GroupType`

## Steps

1. Confirm the exact source and destination groups.
2. Compare destination roles and capacity.
3. Compare Group Member Attribute keys.
4. Record values that will not transfer.
5. Decide whether member notes should move.
6. Move a representative member.
7. Verify the destination membership, role, status, notes, and retained attributes.
8. For bulk automation, add idempotency and per-person verification before scaling.
9. Confirm Group Sync is enabled for the Group Type.
10. Inspect the exact Data View result.
11. Inspect the role assigned by each sync definition.
12. Compare active group membership with the Data View population.
13. Check both the group sync interval and the Group Sync job’s latest execution.
14. Review overlapping syncs, manual memberships, and optional exit behavior.
15. Before a communication, refresh and reconcile the intended source count using locally reviewed procedures.

## Do Not Assume

- Matching attribute labels mean matching keys.
- A successful workflow means every per-person move succeeded.
- A draft community recipe is production-ready.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/documentation/church-management/reporting/metrics
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/7/361
- https://community.rockrms.com/documentation/bookcontent/7
