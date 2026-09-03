---
concept_id: system-admin-ops
task_id: recipe-triage-a-recurring-exception
title: Recipe: Triage a recurring exception
generated: true
---

# Recipe: Triage a recurring exception

Identify the narrowest supported failure boundary without claiming an unverified root cause.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Page`
- `Block`

## Entities And Tables

- `Group`
- `Page`
- `Block`

## Steps

1. Open the Exception List and locate the grouped exception type.
2. Record the recurrence count and relevant timestamps.
3. Open a detail record and identify the associated page, block, job, or action.
4. Correlate the first occurrence with recent configuration or version changes.
5. Check official release notes for the installed version.
6. Reproduce only through a bounded, non-destructive path.
7. Verify that the exception stops recurring after the demonstrated cause is corrected.

## Do Not Assume

- Missing notification email means no exception occurred.
- Every exception is a software defect; page and block misconfiguration are also documented causes.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching
- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexableEntityBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexStatusBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailEnteredDataViewSettingsBag.d.ts
