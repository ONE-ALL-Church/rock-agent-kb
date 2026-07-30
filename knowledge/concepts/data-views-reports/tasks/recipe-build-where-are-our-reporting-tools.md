---
concept_id: data-views-reports
task_id: recipe-build-where-are-our-reporting-tools
title: Recipe: Build "Where Are Our Reporting Tools?"
generated: true
---

# Recipe: Build "Where Are Our Reporting Tools?"

Complete Build "Where Are Our Reporting Tools?" with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Label`
- `Page`
- `Block`

## Entities And Tables

- `DataView`
- `Label`
- `Page`
- `Block`

## Steps

1. Create admin inventory page.
2. Include Reports and Data Views.
3. Include pages with Dynamic Report blocks.
4. Include pages with Dynamic Data blocks.
5. Include embedded BI pages.
6. Add search.
7. Include route, category, owner, description.
8. Respect security or clearly label admin-only.
9. Add review status.
10. Use community finder recipes as patterns, not direct production code (Reporting Dashboard, Reporting Tool Finder).

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/recipes/264
- https://community.rockrms.com/recipes/397
- https://community.rockrms.com/recipes/240
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Reporting/DataViewFilterBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
