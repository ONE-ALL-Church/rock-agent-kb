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

- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in
- https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks
- https://community.rockrms.com/rocku/check-in/check-in-manager-1
- https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/use-grade-and-age-matching-behavior
- https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/configure-by-birthdate
- https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics
- https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile
- https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label
- https://community.rockrms.com/documentation/church-management/check-in/prepare-for-check-in/view-the-administration-screen
- https://community.rockrms.com/documentation/church-management/check-in/registration/intro-to-registration
