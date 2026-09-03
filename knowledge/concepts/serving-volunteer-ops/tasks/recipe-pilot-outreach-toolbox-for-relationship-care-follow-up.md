---
concept_id: serving-volunteer-ops
task_id: recipe-pilot-outreach-toolbox-for-relationship-care-follow-up
title: Recipe: Pilot Outreach Toolbox for relationship-care follow-up
generated: true
---

# Recipe: Pilot Outreach Toolbox for relationship-care follow-up

A bounded group of signed-in mobile users can see, receive, complete, and review configured outreach touchpoints.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Schedule`
- `Page`
- `Block`
- `Person`

## Entities And Tables

- `Group`
- `Schedule`
- `Page`
- `Block`
- `Person`

## Steps

1. Confirm the target Rock server and mobile-shell versions.
2. Verify signed-in access and page placement.
3. Review block settings and contact-data permissions.
4. Configure assignment days and reminder preferences for test users.
5. Inspect the reminder job and time-of-day configuration.
6. Create bounded prayer and connection cadences.
7. Test dashboard visibility.
8. Test push delivery in the real target mobile environment.
9. Complete a touchpoint and verify history and pulse behavior.
10. Review who can see the resulting contact data before expanding access.
11. Confirm that the environment supports the documented v19 Rock Mobile experience.
12. Confirm that the person is signed in.
13. Inspect page placement, block settings, and authentication.
14. Confirm the person’s assignment days and reminder preferences.
15. Inspect the job’s configured time and recent execution.
16. Test push-notification delivery in the target mobile environment.
17. Inspect permissions for contact and touchpoint data.
18. Do not infer a completed follow-up from a scheduled or attempted notification.

## Do Not Assume

- Previewed v19 behavior exists in every mobile deployment.
- A successful job run proves push delivery.
- A scheduled touchpoint is a completed action.
- Do not infer a completed follow-up from a scheduled or attempted notification.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance
- https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp
- https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp
- https://www.youtube.com/watch?v=LNcx8t0mlQ4
