---
concept_id: groups
task_id: recipe-enable-history-and-archive-a-group
title: Recipe: Enable history and archive a group
generated: true
---

# Recipe: Enable history and archive a group

Group changes are snapshotted and a retired group is recoverable.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Workflow`

## Entities And Tables

- `Group`
- `GroupType`
- `Workflow`

## Steps

1. Confirm the Group Type is stable enough for retained history.
2. Enable Group History on the Group Type.
3. Confirm the Process Group History job runs successfully.
4. Inspect the group timeline and member history.
5. Archive the group instead of deleting it.
6. Confirm it is absent from normal group-viewer surfaces.
7. Record the restoration path through Archived Groups.
8. Confirm **Enable Group History** is enabled on the Group Type.
9. Confirm the Process Group History job has run successfully since enablement.
10. Reopen the group after the job completes.
11. If restoring an archived group, use `Admin Tools > Settings > General > Archived Groups`.
12. Do not infer that missing history means no changes occurred before history was enabled.

## Do Not Assume

- Do not infer that missing history means no changes occurred before history was enabled.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
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
- https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/process-group-history
