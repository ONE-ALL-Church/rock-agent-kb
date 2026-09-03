---
concept_id: scheduling-locations
task_id: recipe-enable-rooms-for-a-check-in-schedule
title: Recipe: Enable Rooms For A Check-In Schedule
generated: true
---

# Recipe: Enable Rooms For A Check-In Schedule

The intended group/location pairs are enabled for the intended check-in times.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`
- `Campus`
- `Check-in Configuration`
- `Block`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`
- `Campus`
- `Check-in Configuration`
- `Block`

## Steps

1. Confirm the Named Locations, check-in groups and schedules already exist.
2. Open the applicable check-in configuration.
3. Open its Schedule Builder.
4. Filter to the target campus, building, area or schedule when helpful.
5. For each group/location row, select the schedule columns during which it should accept check-in.
6. Save the grid.
7. Reopen the grid and verify the selections.
8. Test the applicable kiosk scope and runtime open/closed state.
9. Confirm that the schedule is active.
10. Confirm it represents the intended check-in time and category.
11. Confirm the check-in configuration and screen are the expected generation for the installed version.
12. Confirm the schedule has the required check-in timing configuration.
13. Confirm filters on the Schedule Builder or kiosk screen are not hiding it.

## Do Not Assume

- A location enabled for one schedule is enabled for another.
- One check-in configuration’s relationships apply to another configuration.
- A scheduled room is currently open.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
