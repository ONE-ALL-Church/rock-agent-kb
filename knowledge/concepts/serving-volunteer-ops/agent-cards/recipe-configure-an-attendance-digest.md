---
concept_id: serving-volunteer-ops
task_id: recipe-configure-an-attendance-digest
title: Recipe: Configure an attendance digest
generated: true
---

# Recipe: Configure an attendance digest

Leaders at the intended regional level receive attendance summaries for their child attendance groups.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `Group`

## Entities And Tables

- `Attendance`
- `Person`
- `Group`

## Steps

1. Confirm that the group hierarchy has all three required levels.
2. Identify the single top parent group.
3. Identify the region or area groups.
4. Confirm that intended recipients have a role marked `Is Leader` in those groups.
5. Confirm the child attendance groups where attendance is recorded.
6. Configure the Send Group Attendance Digest job for the top parent.
7. Run a bounded test.
8. Verify each recipient and the child groups represented.
9. Confirm the attendance-group leader link routes to the intended person.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-attendance
- https://community.rockrms.com/documentation/church-management/check-in/attendance
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp
