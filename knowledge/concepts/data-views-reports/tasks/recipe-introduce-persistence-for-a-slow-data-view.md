---
concept_id: data-views-reports
task_id: recipe-introduce-persistence-for-a-slow-data-view
title: Recipe: Introduce persistence for a slow Data View
generated: true
---

# Recipe: Introduce persistence for a slow Data View

Faster consumer performance with an explicitly accepted freshness window.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `Attribute`

## Entities And Tables

- `DataView`
- `Group`
- `Attribute`

## Steps

1. Measure the current Data View and Report run times.
2. Identify consumers and their maximum acceptable staleness.
3. Inspect nested Data Views and current persistence settings.
4. Choose an interval no longer than the accepted staleness window.
5. Confirm the Update Persisted Dataviews job is present and operating in the target instance.
6. Enable persistence in an approved test scope.
7. Compare persisted and live results using known examples.
8. Measure the consumer again.
9. Document the interval, job dependency, owner, and rollback condition.
10. Recheck after one complete recalculation cycle.
11. Confirm the Data View entity type.
12. Read the full filter tree and identify all “all” versus “any” groups.
13. Inspect nested Data Views and their entity relationships.
14. Check whether the Data View or a child uses persisted results.
15. Compare known included and excluded examples.
16. Inspect source fields, attributes, aliases, and duplicate risk.
17. Review downstream consumers before editing.
18. If the installed filter component or schema is uncertain, stop and perform a bounded read-only live review. Add a Data View,

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/reporting/data-views/persist-data-views
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceResult/BenevolenceRequestDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/GroupMemberDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Reporting/dataViewFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Reporting/DataViewFilterBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Group/LocationDataViewFilter.cs
- https://community.rockrms.com/documentation/church-management/reporting/data-views/add-a-data-view
