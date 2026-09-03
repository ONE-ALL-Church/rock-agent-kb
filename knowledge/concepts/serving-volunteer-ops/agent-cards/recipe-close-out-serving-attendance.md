---
concept_id: serving-volunteer-ops
task_id: recipe-close-out-serving-attendance
title: Recipe: Close out serving attendance
generated: true
---

# Recipe: Close out serving attendance

The occurrence records who served or that the team did not meet, with discrepancies ready for human review.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Label`

## Entities And Tables

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Label`

## Steps

1. Open the correct group attendance occurrence.
2. Verify the date, schedule, and location.
3. Mark `We Did Not Meet` if that is what occurred.
4. Otherwise, record actual attendees.
5. Add only appropriate operational notes.
6. Compare the completed attendance list with confirmed assignments.
7. Investigate late changes and data-entry omissions.
8. Produce a bounded follow-up list of unresolved differences.
9. Launch follow-up only after confirming each difference’s meaning.

## Do Not Assume

- Pending means absent.
- Confirmed means attended.
- No attendance rows means the team met with zero volunteers.

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
