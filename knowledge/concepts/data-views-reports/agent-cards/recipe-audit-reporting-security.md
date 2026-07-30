---
concept_id: data-views-reports
task_id: recipe-audit-reporting-security
title: Recipe: Audit Reporting Security
generated: true
---

# Recipe: Audit Reporting Security

Complete Audit Reporting Security with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `DataView`
- `Page`
- `Block`

## Entities And Tables

- `Attendance`
- `DataView`
- `Page`
- `Block`

## Steps

1. List Data Views by category.
2. List Reports by category.
3. List Dynamic Report pages.
4. List Dynamic Data pages.
5. List HTML blocks with SQL enabled.
6. List BI embed pages.
7. Test as representative users.
8. Flag finance/minor/care/attendance reports.
9. Verify exports.
10. Produce remediation list.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://community.rockrms.com/lava/commands/sql-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report
- https://www.triumph.tech/resources/grouping-sets
- https://www.triumph.tech/resources/sql-window-functions
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/recipes/264
- https://community.rockrms.com/rocku/lava/sql-command
- https://community.rockrms.com/recipes/397
