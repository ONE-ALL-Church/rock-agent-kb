---
concept_id: serving-volunteer-ops
task_id: recipe-configure-a-serving-team-for-scheduling
title: Recipe: Configure a serving team for scheduling
generated: true
---

# Recipe: Configure a serving team for scheduling

A bounded serving group is ready for assignments at verified locations and times.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`
- `Block`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`
- `Block`

## Steps

1. Identify the intended group type and group.
2. Inspect existing named locations and schedules before creating anything.
3. Add only the missing locations or positions and schedules.
4. Associate them with the serving group.
5. Enable Group Scheduling on the group type.
6. Select confirmation and reminder System Communications.
7. Set the confirmation and reminder offsets.
8. Choose `Ask` or `Auto Accept`.
9. Configure decline-reason and cancellation-workflow behavior.
10. Assign a Schedule Coordinator and choose notification events.
11. Test one assignment through the volunteer-facing Schedule Toolbox.
12. Verify the resulting assignment state and communication outcome.
13. Confirm that the operator is inspecting the intended group and group type.
14. Inspect whether `Scheduling Enabled` is active on that group type.
15. Confirm that the required named locations or positions exist.
16. Confirm that the required named schedules exist and have accurate times.
17. Confirm that the locations and schedules are associated with the group.
18. Inspect the scheduler’s current group and location selections.
19. If all configuration appears correct, verify permissions and the installed version before changing data.

## Do Not Assume

- A group name makes it schedulable.
- A saved assignment was communicated.
- An accepted assignment is attendance.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp
- https://community.rockrms.com/documentation/engagement/groups/group-attendance
