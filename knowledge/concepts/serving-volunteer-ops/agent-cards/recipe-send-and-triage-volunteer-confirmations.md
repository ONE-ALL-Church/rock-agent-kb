---
concept_id: serving-volunteer-ops
task_id: recipe-send-and-triage-volunteer-confirmations
title: Recipe: Send and triage volunteer confirmations
generated: true
---

# Recipe: Send and triage volunteer confirmations

The intended volunteers receive a confirmation request without an uncontrolled duplicate send.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`
- `Workflow`
- `Page`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`
- `Workflow`
- `Page`

## Steps

1. Select the correct groups, locations, schedules, and week.
2. Review current assignment states.
3. Determine whether the scheduled job has already sent the request.
4. Preview the confirmation communication and its response links.
5. Send only to the bounded eligible set.
6. Compare eligible-recipient count with sent count.
7. Review warnings and errors.
8. Monitor pending, confirmed, declined, and unavailable states.
9. Route declines or cancellations according to the configured workflow.
10. Verify coordinator notification separately.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp
- https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp
