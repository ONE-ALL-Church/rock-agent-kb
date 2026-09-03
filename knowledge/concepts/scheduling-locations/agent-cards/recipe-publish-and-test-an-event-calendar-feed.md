---
concept_id: scheduling-locations
task_id: recipe-publish-and-test-an-event-calendar-feed
title: Recipe: Publish And Test An Event Calendar Feed
generated: true
---

# Recipe: Publish And Test An Event Calendar Feed

The intended Rock calendar is available through a bounded iCalendar feed.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Campus`
- `Location`
- `Workflow`

## Entities And Tables

- `Schedule`
- `Campus`
- `Location`
- `Workflow`

## Steps

1. Confirm the event, occurrences, active state, calendars and approval state.
2. Open the intended Event Calendar.
3. use **Export Calendar Feed** to obtain the URL.
4. Review its calendar, campus, audience and date parameters.
5. Confirm the requesting user can access any non-public calendar included.
6. Subscribe from a test calendar client.
7. Compare representative occurrences, dates and descriptions with Rock.
8. Retest after changing one test occurrence.
9. Document the feed’s audience and ownership.
10. Confirm the Room Management plugin is installed and identify its version.
11. Identify the reservation and its explicit calendar linkage.
12. Compare schedule, location and contact fields without modifying either record.
13. Determine which record is authoritative under local policy.
14. Review the recipe generation and schema assumptions before running a workflow or SQL.
15. Stop before synchronizing if ownership, linkage or compatibility is ambiguous.

## Do Not Assume

- A calendar feed bypasses Rock security.
- A volunteer Schedule Toolbox link is the same as an Event Calendar feed.
- A reservation automatically appears on the event calendar.

## Source Links

- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://www.youtube.com/watch?v=edanHiYSDIM
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://community.rockrms.com/documentation/engagement/groups/group-schedules
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20
