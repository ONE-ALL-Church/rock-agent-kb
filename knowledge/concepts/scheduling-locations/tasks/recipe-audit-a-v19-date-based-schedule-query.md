---
concept_id: scheduling-locations
task_id: recipe-audit-a-v19-date-based-schedule-query
title: Recipe: Audit A V19 Date-Based Schedule Query
generated: true
---

# Recipe: Audit A V19 Date-Based Schedule Query

A date-based report uses Rock’s v19 materialized schedule occurrences.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Confirm the installed version is v19.
2. Identify the recurring Schedule records in scope.
3. Inspect their corresponding `ScheduleDate` rows.
4. Compare representative generated dates with the intended recurrence.
5. Update the report design to filter and join through generated dates.
6. Test inclusions, exclusions and date boundaries.
7. Stop rather than adding a parallel recurrence parser when generated dates are unexpectedly absent.
8. Confirm the installed Rock version.
9. On v19, inspect the generated `ScheduleDate` rows for the schedule.
10. Use those rows for date-based SQL or Lava rather than re-expanding the iCalendar rule.
11. If expected rows are absent, stop and verify generation behavior for the exact installed build.
12. On pre-v19 systems, do not assume the v19 materialization model exists.

## Do Not Assume

- Pre-v19 systems have the same materialization.
- The supplied evidence defines the generation horizon or refresh mechanism.
- One organization’s observed row count is universal.
- On pre-v19 systems, do not assume the v19 materialization model exists.

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
