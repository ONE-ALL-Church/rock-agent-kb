---
concept_id: serving-volunteer-ops
task_id: recipe-configure-an-rsvp-based-serving-invitation
title: Recipe: Configure an RSVP-based serving invitation
generated: true
---

# Recipe: Configure an RSVP-based serving invitation

A group occurrence can collect and display bounded accept or decline responses.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Entities And Tables

- `Attendance`
- `Person`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Steps

1. Confirm that RSVP is the intended workflow rather than Group Scheduling.
2. Confirm that the target group exists.
3. Enable RSVP on the group type.
4. Configure the reminder communication and offset at either group-type or group level.
5. Create the occurrence with its date, optional schedule, and location.
6. Add custom response messages when needed.
7. Enable and select decline reasons only when the ministry will use them.
8. Send the RSVP request and decide whether to register all recipients.
9. Monitor RSVP Detail.
10. Record verified phone or in-person response changes when authorized.

## Do Not Assume

- RSVP enables scheduling.
- A nonrespondent will appear when recipients were not registered.
- An acceptance proves attendance.

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
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details
