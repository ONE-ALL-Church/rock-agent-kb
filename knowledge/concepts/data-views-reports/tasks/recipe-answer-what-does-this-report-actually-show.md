---
concept_id: data-views-reports
task_id: recipe-answer-what-does-this-report-actually-show
title: Recipe: Answer "What Does This Report Actually Show?"
generated: true
---

# Recipe: Answer "What Does This Report Actually Show?"

Complete Answer "What Does This Report Actually Show?" with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Page`
- `Block`

## Entities And Tables

- `DataView`
- `Page`
- `Block`

## Steps

1. Find the Report.
2. Record Report ID, name, category.
3. Open its Data View.
4. Translate filter tree into plain English.
5. List Report columns.
6. Inspect Dynamic Report block if page-rendered.
7. Run count as admin and target user.
8. Identify sensitive fields.
9. Cite dependent Data Views.
10. Return a concise definition and caveats.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/recipes/264
- https://community.rockrms.com/recipes/240
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block
- https://community.rockrms.com/lava/commands/sql-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Reporting/DataViewFilterBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
