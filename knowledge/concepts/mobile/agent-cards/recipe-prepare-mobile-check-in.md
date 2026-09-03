---
concept_id: mobile
task_id: recipe-prepare-mobile-check-in
title: Recipe: Prepare mobile check-in
generated: true
---

# Recipe: Prepare mobile check-in

A participant can identify, select, complete check-in and hand labels to a kiosk.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Campus`
- `Device`
- `Check-in Configuration`
- `Label`
- `Family`

## Entities And Tables

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Campus`
- `Device`
- `Check-in Configuration`
- `Label`
- `Family`

## Steps

1. Validate ordinary check-in for the target groups, locations, schedules and configuration.
2. Confirm HTTPS and geofencing prerequisites.
3. Create a virtual check-in kiosk device for each distinct campus boundary.
4. Configure campus geofences and relevant locations.
5. Configure the launcher’s devices, check-in configuration, theme and valid areas.
6. Review identity, welcome-back and fallback copy.
7. Test first-time identification.
8. Test a recognized returning device.
9. Test family and individual selection.
10. Test outside-boundary, closed-window and no-option states.
11. Complete check-in and scan the QR code at the label kiosk.
12. Add a selection and verify the updated handoff.
13. Confirm HTTPS and the geofencing API prerequisite.
14. Verify location permission and the participant’s current campus or boundary.
15. Inspect the virtual kiosk device type, campus geofence and associated campus locations.
16. Confirm that the launcher enables that device.
17. If campus boundaries differ, confirm separate device records exist.
18. Test campus selection as well as location-based resolution when the configured experience offers both.

## Do Not Assume

- A launcher record proves its selections are correct
- A successful check-in proves printing
- A generated QR code proves kiosk scanning or printer output

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-type
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/on-device-platform
- https://community.rockrms.com/rocku/check-in/using-mobile-check-in
- https://community.rockrms.com/developer/mobile-docs/essentials/controls/xaml-extensions/palette-color
- https://community.rockrms.com/developer/mobile-docs/app-factory/shell-update-requirements
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/getScheduledLocationsResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/saveFamilyOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/editFamilyResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/reprintAttendanceBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/getCurrentAttendanceResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/saveFamilyResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/CheckInKiosk/activeAttendanceBag.d.ts
- https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration
