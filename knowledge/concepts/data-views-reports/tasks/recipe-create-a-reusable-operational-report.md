---
concept_id: data-views-reports
task_id: recipe-create-a-reusable-operational-report
title: Recipe: Create a reusable operational Report
generated: true
---

# Recipe: Create a reusable operational Report

One governed population definition and one Report that presents it without duplicating filter logic.

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

1. Define the entity grain and intended audience.
2. Locate an existing Data View that exactly matches the population, or create a clearly described one.
3. Validate known included and excluded records.
4. Inspect persistence and downstream consumers.
5. Create the Report with the matching entity type and selected Data View.
6. Add only required fields, sorting, and a justified row limit.
7. Mark supplemental fields as export-only only when needed.
8. Apply Report security.
9. Test the grid, export, and available actions as the intended role.
10. Record the owner, purpose, and freshness expectation.

## Do Not Assume

- preview rows represent the full population;
- ordinary entity security will constrain Report results;
- the ability to communicate or export authorizes the action.

## Source Links

- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-report-block
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/dynamic-data-block
- https://community.rockrms.com/documentation/church-management/reporting/reports/secure-report-data
- https://community.rockrms.com/documentation/church-management/reporting/reports/create-a-report
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceRequest/BenevolenceResultDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/Person/StepDataViewDataFilterTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/BenevolenceResult/BenevolenceRequestDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/ConnectionRequest/GroupMemberDataViewFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Reporting/DataFilter/DataViewTests.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/DataViewFilter/DataViewFilter.SaveHook.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Reporting/dataViewFilterBag.d.ts
