---
concept_id: check-in
task_id: diagnose-person-not-eligible
title: Diagnose Person Found But No Eligible Rooms
generated: true
---

# Diagnose Person Found But No Eligible Rooms

Trace eligibility from person/family search through configuration, group type, group, location, schedule, campus, capacity, and version caveats.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Family Group`
- `GroupType`
- `Group`
- `Location`
- `Schedule`
- `Campus`

## Entities And Tables

- `Person`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `AttendanceOccurrence`

## Steps

1. Confirm the person is searchable in the current check-in configuration and family context.
2. Inspect age, grade, status, campus, family relationship, and can-check-in relationship assumptions.
3. Verify the target group type takes attendance and its check-in behavior matches the desired model.
4. Verify active group, active location, linked schedule, check-in window, campus, and capacity.
5. Check release notes for known age/grade, inactive group, schedule exclusion, and capacity fixes.

## Do Not Assume

- Do not assume a missing room means the group is missing.
- Do not ignore schedule windows and kiosk/device location filters.

## Source Links

- https://community.rockrms.com/rocku/check-in
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx
- https://community.rockrms.com/rocku/check-in/attendance-analytics
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md
- https://community.rockrms.com/ask/using/2804
- https://community.rockrms.com/recipes/483
- https://community.rockrms.com/recipes/116
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql
