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

- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
- https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history
- https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-digest
