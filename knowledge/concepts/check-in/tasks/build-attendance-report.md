---
concept_id: check-in
task_id: build-attendance-report
title: Build Or Debug Attendance Reporting
generated: true
---

# Build Or Debug Attendance Reporting

Use the attendance data model correctly so reports match check-in behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `AttendanceOccurrence`
- `Group`
- `Schedule`
- `Location`
- `Campus`

## Entities And Tables

- `Attendance`
- `AttendanceOccurrence`
- `PersonAlias`
- `Group`
- `Schedule`
- `Location`
- `Campus`

## Steps

1. Join Attendance through AttendanceOccurrence before interpreting group, schedule, location, or date.
2. Filter on DidAttend when the report should count actual attendance.
3. Decide whether the report counts rows, people, dates, families, occurrences, or groups.
4. Use SundayDate carefully for weekly reporting.
5. Compare results against Attendance Analytics before shipping a custom report.

## Do Not Assume

- Do not report from group membership alone.
- Do not ignore duplicate attendance across schedules or services.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_AttendeeLastAttendance.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/059_MigrationRollupsForV8_5_2_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeFirstDates.sql
