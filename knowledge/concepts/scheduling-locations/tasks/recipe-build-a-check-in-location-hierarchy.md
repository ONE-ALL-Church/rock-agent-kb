---
concept_id: scheduling-locations
task_id: recipe-build-a-check-in-location-hierarchy
title: Recipe: Build A Check-In Location Hierarchy
generated: true
---

# Recipe: Build A Check-In Location Hierarchy

Named Locations represent the intended campus, building and room structure.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Campus`
- `Family`

## Entities And Tables

- `Location`
- `Campus`
- `Family`

## Steps

1. Inventory the operational hierarchy and the rooms that will participate in check-in.
2. Open Named Locations.
3. Confirm or create the top-level campus location.
4. Add buildings beneath the campus.
5. Add rooms beneath the appropriate buildings.
6. Assign the correct Location Type to each record.
7. Review parent relationships and names from the full tree.
8. Configure only the metadata required for each location, such as thresholds, printer, beacon, point or geo-fence.
9. Save and verify that the hierarchy reloads correctly.

## Do Not Assume

- A family address is a Named Location.
- A room needs a street address.
- Creating the room makes it available to check-in.
- A soft threshold and absolute threshold behave the same way.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations
