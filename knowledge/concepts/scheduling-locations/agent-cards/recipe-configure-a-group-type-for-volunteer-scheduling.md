---
concept_id: scheduling-locations
task_id: recipe-configure-a-group-type-for-volunteer-scheduling
title: Recipe: Configure A Group Type For Volunteer Scheduling
generated: true
---

# Recipe: Configure A Group Type For Volunteer Scheduling

Groups of the selected type can schedule volunteers with defined confirmation and reminder behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Entities And Tables

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Steps

1. Confirm the required Named Locations and one-schedule-per-time definitions.
2. Open the target Group Type’s scheduling settings.
3. Enable scheduling.
4. Select the confirmation communication.
5. Select the reminder communication.
6. Set confirmation and reminder offsets.
7. Choose **Ask** or **Auto Accept** deliberately.
8. Configure decline reasons, cancellation workflow and coordinator notifications as required.
9. Confirm SMS prerequisites if either communication may use SMS.
10. Test with a non-production assignment before broad use.

## Do Not Assume

- Enabling scheduling creates assignments.
- Auto Accept safely changes the state or actions of already-pending communications.
- Selecting an SMS communication guarantees delivery.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
