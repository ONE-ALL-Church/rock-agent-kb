---
concept_id: check-in
generated: true
artifact_level: live_probe_recipes
---

# Check-In Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Check-in configuration

- Recipe id: `live-probe-recipe:check-in:check-in-configuration`
- Target binding: Run only after identifying the exact live object or schema surface being inspected.
- Expected tables: `GroupType`

```sql
SELECT Id, Name, GroupTypePurposeValueId, TakesAttendance, EnableLocationSchedules, IsSchedulingEnabled, GroupAttendanceRequiresLocation, GroupAttendanceRequiresSchedule FROM GroupType WHERE Name LIKE '%check%';
```

Evidence to record:
- Rock version or migration context used for the review.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Check-in configuration` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Rooms and schedules

- Recipe id: `live-probe-recipe:check-in:rooms-and-schedules`
- Target binding: Bind `<group_type_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<group_type_id>`
- Expected tables: `Group`, `GroupLocation`, `GroupLocationSchedule`, `Location`, `Schedule`

```sql
SELECT g.Id, g.Name, l.Name AS LocationName, s.Name AS ScheduleName FROM [Group] g LEFT JOIN GroupLocation gl ON gl.GroupId = g.Id LEFT JOIN Location l ON l.Id = gl.LocationId LEFT JOIN GroupLocationSchedule gls ON gls.GroupLocationId = gl.Id LEFT JOIN Schedule s ON s.Id = gls.ScheduleId WHERE g.GroupTypeId = <group_type_id>;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Rooms and schedules` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Person eligibility

- Recipe id: `live-probe-recipe:check-in:person-eligibility`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Inspect person/family attributes, grade/age, data view filters, attendance history, and active family relationships.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Person eligibility` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Device and labels

- Recipe id: `live-probe-recipe:check-in:device-and-labels`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Verify kiosk/mobile device, printer, label merge fields, and campus/location mapping.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Device and labels` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
