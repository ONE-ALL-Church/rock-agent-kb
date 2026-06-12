---
concept_id: data-views-reports
generated: true
artifact_level: live_probe_recipes
---

# Data Views And Reports Live Probe Recipes

These recipes provide schema-correct read-only probes for exact live objects. They do not globally close open questions; bind each recipe to the named page, block, workflow type, data view, report, group, route, person context, or configured record before using it.

## Data view definition

- Recipe id: `live-probe-recipe:data-views-reports:data-view-definition`
- Target binding: Bind `<data_view_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<data_view_id>`
- Expected tables: `DataView`

```sql
SELECT Id, Name, EntityTypeId, DataViewFilterId, PersistedScheduleIntervalMinutes, PersistedLastRefreshDateTime, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM DataView WHERE Id = <data_view_id>;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Data view definition` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Report fields

- Recipe id: `live-probe-recipe:data-views-reports:report-fields`
- Target binding: Bind `<report_id>` from the exact live object named by the user before running this probe.
- Required parameters: `<report_id>`
- Expected tables: `Report`, `ReportField`

```sql
SELECT Id, Name, EntityTypeId, DataViewId, LastRunDateTime, RunCount, TimeToRunDurationMilliseconds FROM Report WHERE Id = <report_id>; SELECT Id, ReportId, ReportFieldType, ColumnHeaderText, ColumnOrder, SortOrder, SortDirection FROM ReportField WHERE ReportId = <report_id> ORDER BY ColumnOrder, Id;
```

Evidence to record:
- Rock version or migration context used for the review.
- The exact placeholder values used, with private values redacted when needed.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Report fields` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Dynamic data blocks

- Recipe id: `live-probe-recipe:data-views-reports:dynamic-data-blocks`
- Target binding: Run only after identifying the exact live object or schema surface being inspected.
- Expected tables: `Block`, `BlockType`, `Page`

```sql
SELECT b.Id, b.Name, p.InternalName AS PageName FROM Block b JOIN Page p ON p.Id = b.PageId WHERE b.BlockTypeId IN (SELECT Id FROM BlockType WHERE Name LIKE '%Dynamic Data%');
```

Evidence to record:
- Rock version or migration context used for the review.
- A bounded row count or small redacted sample proving the target record or schema surface exists.
- Reviewer note explaining what the `Dynamic data blocks` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.

## Row-count validation

- Recipe id: `live-probe-recipe:data-views-reports:row-count-validation`
- Target binding: This is a manual inspection recipe; bind it to the exact page, block, workflow, report, mobile screen, or configured object named by the user.

Manual check: Capture sample included and excluded records before and after changing a shared DataView or SQL report.

Evidence to record:
- Rock version or migration context used for the review.
- Reviewer note explaining what the `Row-count validation` evidence verifies and what it does not verify.

Safety rules:
- Run only read-only SELECT or INFORMATION_SCHEMA probes.
- Replace placeholder values before running SQL; never run a placeholder literally.
- Do not use schema or row-existence evidence as proof that a specific configured object is correct.
- Do not expose private production row values in public KB artifacts.
