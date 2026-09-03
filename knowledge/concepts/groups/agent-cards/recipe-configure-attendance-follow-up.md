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

- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
- https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history
- https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-members/move-group-members
- https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
