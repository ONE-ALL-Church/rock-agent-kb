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

- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history
- https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history
- https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-history/enable-group-history
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/rocku/workflows
