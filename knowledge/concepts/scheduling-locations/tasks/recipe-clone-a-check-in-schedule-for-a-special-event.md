---
concept_id: scheduling-locations
task_id: recipe-clone-a-check-in-schedule-for-a-special-event
title: Recipe: Clone A Check-In Schedule For A Special Event
generated: true
---

# Recipe: Clone A Check-In Schedule For A Special Event

A destination schedule starts with the source schedule’s enabled locations.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Schedule`
- `Check-in Configuration`
- `Block`

## Entities And Tables

- `Location`
- `Schedule`
- `Check-in Configuration`
- `Block`

## Steps

1. Create or identify the destination schedule.
2. Open the applicable check-in configuration’s Schedule view.
3. Choose **Clone Schedule**.
4. Select the existing source schedule.
5. Select the destination schedule.
6. Complete the clone.
7. Review every enabled location in the destination.
8. Remove or add only the differences required for the special event.
9. Test the destination schedule through the intended kiosk configuration.
10. Confirm that the schedule is active.
11. Confirm it represents the intended check-in time and category.
12. Confirm the check-in configuration and screen are the expected generation for the installed version.
13. Confirm the schedule has the required check-in timing configuration.
14. Confirm filters on the Schedule Builder or kiosk screen are not hiding it.

## Do Not Assume

- The special event uses every regular-service room.
- The clone copies unrelated event, reservation or calendar records.
- A destination schedule is safe merely because the operation completed.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://www.youtube.com/watch?v=edanHiYSDIM
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
