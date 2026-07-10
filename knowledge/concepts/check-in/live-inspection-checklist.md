---
id: live-checklist:check-in
concept_id: check-in
generated: true
artifact_level: live_checklist
---

# Check-In Live Inspection Checklist

## Steps

1. Confirm the Rock version and any relevant release-note caveats.
2. Open the exact page, block, workflow, group, data view, or mobile screen named by the user.
3. Inspect configured settings before inferring behavior from documentation.
4. Check security roles, inherited permissions, and feature flags where applicable.
5. Verify current data rows and recent history before changing production behavior or recommending writes.
6. Inspect `Rock version` in the live instance when the question touches this surface.
7. Inspect `Block settings` in the live instance when the question touches this surface.
8. Inspect `Security roles and permissions` in the live instance when the question touches this surface.
9. Inspect `WorkflowType and Workflow records` in the live instance when the question touches this surface.
10. Inspect `DataView and report filters` in the live instance when the question touches this surface.
11. Inspect `Group, GroupType, Location, and Schedule records` in the live instance when the question touches this surface.
12. Inspect `Financial transaction and gateway settings` in the live instance when the question touches this surface.
13. Inspect `Mobile shell version and mobile block settings` in the live instance when the question touches this surface.
14. Inspect `Person, family, alias, and attribute records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `DataView and report filters`
- `Group, GroupType, Location, and Schedule records`
- `Financial transaction and gateway settings`
- `Mobile shell version and mobile block settings`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Check-in configuration**

```sql
SELECT Id, Name, GroupTypePurposeValueId, TakesAttendance, EnableLocationSchedules, IsSchedulingEnabled, GroupAttendanceRequiresLocation, GroupAttendanceRequiresSchedule FROM GroupType WHERE Name LIKE '%check%';
```
- **Rooms and schedules**

```sql
SELECT g.Id, g.Name, l.Name AS LocationName, s.Name AS ScheduleName FROM [Group] g LEFT JOIN GroupLocation gl ON gl.GroupId = g.Id LEFT JOIN Location l ON l.Id = gl.LocationId LEFT JOIN GroupLocationSchedule gls ON gls.GroupLocationId = gl.Id LEFT JOIN Schedule s ON s.Id = gls.ScheduleId WHERE g.GroupTypeId = <group_type_id>;
```
- **Person eligibility**
  - Inspect person/family attributes, grade/age, data view filters, attendance history, and active family relationships.
- **Device and labels**
  - Verify kiosk/mobile device, printer, label merge fields, and campus/location mapping.
