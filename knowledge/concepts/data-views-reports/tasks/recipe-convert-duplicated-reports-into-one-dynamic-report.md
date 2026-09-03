---
concept_id: data-views-reports
task_id: recipe-convert-duplicated-reports-into-one-dynamic-report
title: Recipe: Convert duplicated Reports into one Dynamic Report
generated: true
---

# Recipe: Convert duplicated Reports into one Dynamic Report

One Report supports controlled viewer-selected criteria.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Campus`
- `Block`

## Entities And Tables

- `DataView`
- `Campus`
- `Block`

## Steps

1. Identify Reports that differ only by a dimension such as campus.
2. Consolidate their shared population logic into one Data View.
3. Leave the viewer-controlled criterion at a safe default.
4. Create or select one Report using that Data View.
5. Add a Dynamic Report block and select the Report.
6. Expose only the intended filters.
7. Set visibility, configurability, and toggle behavior separately.
8. Test default, modified, disabled, and URL-initialized states.
9. Test as intended and denied roles.
10. Remove duplicates only after confirming no downstream consumers remain.
11. Confirm that the selected Report uses the expected Data View.
12. Inspect whether the filter is visible, configurable, and toggleable.
13. Check whether the filter belongs to the top-level or nested Data View.
14. Validate the supported URL parameter name and value format.
15. Test with no URL parameters before testing prepopulation.
16. Verify that disabling the filter cannot broaden access beyond the intended population.

## Do Not Assume

- every Data View filter is safe to expose;
- URL initialization is an authorization boundary;
- a nested filter is controlled at the same level as a top-level filter.

## Source Links

- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-data-block
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceResult/BenevolenceRequestDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/GroupMemberDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Reporting/dataViewFilterBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Person/AttendanceDataViewFilter.cs
