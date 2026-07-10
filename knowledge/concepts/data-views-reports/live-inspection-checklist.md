---
id: live-checklist:data-views-reports
concept_id: data-views-reports
generated: true
artifact_level: live_checklist
---

# Data Views And Reports Live Inspection Checklist

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
12. Inspect `Communication recipient, medium, and send history` in the live instance when the question touches this surface.
13. Inspect `Financial transaction and gateway settings` in the live instance when the question touches this surface.
14. Inspect `Mobile shell version and mobile block settings` in the live instance when the question touches this surface.
15. Inspect `Registration instance and registrant records` in the live instance when the question touches this surface.

## Inspection Targets

- `Rock version`
- `Block settings`
- `Security roles and permissions`
- `WorkflowType and Workflow records`
- `DataView and report filters`
- `Group, GroupType, Location, and Schedule records`
- `Communication recipient, medium, and send history`
- `Financial transaction and gateway settings`
- `Mobile shell version and mobile block settings`
- `Registration instance and registrant records`
- `Person, family, alias, and attribute records`

## Read-Only Probes

- **Data view definition**

```sql
SELECT Id, Name, EntityTypeId, DataViewFilterId, PersistedScheduleIntervalMinutes, PersistedLastRefreshDateTime, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM DataView WHERE Id = <data_view_id>;
```
- **Report fields**

```sql
SELECT Id, Name, EntityTypeId, DataViewId, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM Report WHERE Id = <report_id>; SELECT Id, ReportId, ReportFieldType, ColumnHeaderText, ColumnOrder, SortOrder, SortDirection FROM ReportField WHERE ReportId = <report_id> ORDER BY ColumnOrder, Id;
```
- **Dynamic data blocks**

```sql
SELECT b.Id, b.Name, p.InternalName AS PageName FROM Block b JOIN Page p ON p.Id = b.PageId WHERE b.BlockTypeId IN (SELECT Id FROM BlockType WHERE Name LIKE '%Dynamic Data%');
```
- **Row-count validation**
  - Capture sample included and excluded records before and after changing a shared DataView or SQL report.
