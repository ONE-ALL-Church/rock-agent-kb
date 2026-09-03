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

- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history
- https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-digest
