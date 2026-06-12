---
concept_id: check-in
task_id: audit-mobile-check-in
title: Audit Mobile Check-In
generated: true
---

# Audit Mobile Check-In

Confirm mobile check-in uses the intended configuration template, kiosk, areas, authentication, and print route.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Mobile Page`
- `Mobile Block`
- `Check-in Configuration`
- `Device/Kiosk`
- `Printer`

## Entities And Tables

- `Attendance`
- `AttendanceOccurrence`
- `Device`

## Steps

1. Verify Rock server version and Rock Mobile version.
2. Inspect mobile block settings for configuration template, kiosk, primary areas, and secondary areas.
3. Confirm the logged-in family/person context and shell route.
4. Test label routing to the venue printer or cloud print path.
5. Check mobile release notes for family-mode, page-parameter, proximity, and label printing fixes.

## Do Not Assume

- Do not treat mobile check-in as anonymous QR attendance.
- Do not assume mobile uses different attendance tables.

## Source Links

- https://community.rockrms.com/rocku/check-in
- https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md
- https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://community.rockrms.com/rocku/check-in/mobile-check-in-overview
- https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://community.rockrms.com/rocku/check-in/using-mobile-check-in
- https://community.rockrms.com/recipes/483
- https://community.rockrms.com/recipes/116
