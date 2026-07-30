---
concept_id: serving-volunteer-ops
task_id: recipe-build-a-serving-health-dashboard
title: Recipe: Build A Serving Health Dashboard
generated: true
---

# Recipe: Build A Serving Health Dashboard

Cite reporting model landmarks where appropriate: Model Map, vCheckin_GroupTypeAttendance.sql.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`

## Steps

1. active volunteer count;
2. volunteers missing preferences;
3. volunteers with expired requirements;
4. pending confirmations by date;
5. declined confirmations by date;
6. unfilled role slots;
7. no-shows;
8. first-time servers;
9. inactive volunteers still scheduled;
10. archived groups with schedules;
11. communications failed;
12. attendance reminders not sent.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://community.rockrms.com/rocku/groups/group-details
- https://community.rockrms.com/rocku/groups/group-attendance
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/recipes/530/dynamic-sender-for-group-scheduling-confirmations-coordinator-fallback
