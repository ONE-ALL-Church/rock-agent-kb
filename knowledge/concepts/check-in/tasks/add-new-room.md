---
concept_id: check-in
task_id: add-new-room
title: Add A New Check-In Room
generated: true
---

# Add A New Check-In Room

Add a room without breaking eligibility, labels, printer routing, capacity, or reporting.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`
- `Device`
- `Label`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`
- `AttendanceOccurrence`

## Steps

1. Create or verify the named location and campus.
2. Create or update the group under the correct group type and area.
3. Attach the location and schedule expected for check-in.
4. Set capacity and printer behavior if used.
5. Run a test check-in and inspect the AttendanceOccurrence group, location, and schedule.

## Do Not Assume

- Do not add a room only in the UI; verify the data written after a test check-in.

## Source Links

- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/use-grade-and-age-matching-behavior
- https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/configure-by-birthdate
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/use-url-parameters-for-check-in
- https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in
- https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-settings-for-a-check-in-type
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs
