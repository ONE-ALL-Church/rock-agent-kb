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

- https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration
- https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance
- https://community.rockrms.com/rocku/check-in/mobile-check-in-overview
- https://community.rockrms.com/rocku/check-in/using-mobile-check-in
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/CheckIn/MobileCheckInLauncher/types.partial.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/CustomSettingsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs
