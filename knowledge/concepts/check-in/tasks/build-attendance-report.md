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

- https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry
- https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics
- https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry
- https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance
- https://community.rockrms.com/documentation/church-management/check-in/attendance
- https://community.rockrms.com/recipes/461
- https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile
- https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer
- https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in
- https://community.rockrms.com/rocku/check-in/attendance-analytics
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/rocku/check-in/attendance-self-entry
