---
concept_id: scheduling-locations
task_id: recipe-prepare-volunteer-availability-for-auto-schedule
title: Recipe: Prepare Volunteer Availability For Auto-Schedule
generated: true
---

# Recipe: Prepare Volunteer Availability For Auto-Schedule

A volunteer has usable availability, reminder and assignment preferences.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Location`
- `Schedule`
- `GroupType`

## Entities And Tables

- `Person`
- `Group`
- `Location`
- `Schedule`
- `GroupType`

## Steps

1. Open the Schedule Toolbox for the correct person.
2. Record unavailable date ranges, scope and optional notes.
3. Select the applicable schedule template.
4. Set reminder preference.
5. Select preferred schedules and locations.
6. Confirm required Named Schedules are marked **Show Publicly** if they should appear.
7. Review the Group Member Detail record where administrative confirmation is needed.
8. Run Auto-Schedule only after preferences for the relevant roster have been reviewed.
9. Review generated assignments before sending confirmations.
10. Confirm the assignment and its schedule time.
11. Confirm the Group Type reminder communication and offset.
12. Check the group member’s reminder and communication preferences.
13. If no group member communication preference exists, inspect the person’s profile preference.
14. For SMS, confirm the provider configuration, SMS-enabled phone and SMS-capable System Communication.
15. For Outreach Toolbox, separately inspect the reminder job time and push delivery in the target mobile environment.

## Do Not Assume

- A preference guarantees assignment.
- No location preference means the person cannot be scheduled.
- A schedule template applies correctly to every weekday.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s
