---
concept_id: data-views-reports
task_id: recipe-diagnose-slow-reporting
title: Recipe: Diagnose Slow Reporting
generated: true
---

# Recipe: Diagnose Slow Reporting

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Page`

## Entities And Tables

- `DataView`
- `Page`

## Steps

1. Identify exact report/page.
2. Measure load time.
3. Measure Data View execution time.
4. Check row count.
5. Inspect filters.
6. Check SQL/Lava columns.
7. Check related Data Views.
8. Check database CPU/worker waits.
9. Test with narrower date range.
10. Recommend Data View simplification, caching, analytics table, SQL optimization, or BI.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/recipes/264
- https://community.rockrms.com/recipes/397
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Reporting/DataViewFilterBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Reporting/DataFilter/Group/LocationDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilterOverride.cs
