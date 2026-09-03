---
concept_id: system-admin-ops
task_id: recipe-review-a-data-automation-change-before-execution
title: Recipe: Review a Data Automation change before execution
generated: true
---

# Recipe: Review a Data Automation change before execution

Define the expected affected population and side effects before a job mutates records.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `DataView`
- `Group`
- `Schedule`
- `Campus`
- `Family`
- `Workflow`

## Entities And Tables

- `Person`
- `DataView`
- `Group`
- `Schedule`
- `Campus`
- `Family`
- `Workflow`

## Steps

1. Identify the exact automation function being changed.
2. Inspect all inclusion and exclusion Data Views.
3. Inspect inactive-reason restrictions when reactivation is involved.
4. Review effects on family structure, campus, connection status, family status, groups, security roles, and launched workflows as applicable.
5. Review the maximum records processed per run.
6. Record the expected population and expected field changes.
7. Obtain authorization before saving material changes or running the job.
8. After execution, compare job history and a bounded sample of resulting records.
9. Identify which automation function changed the records.
10. Inspect its inclusion and exclusion Data Views, inactive-reason settings, and processing limit.
11. Check whether affected people were also changed in groups or security roles.
12. Correlate the changes with the Data Automation job’s execution history and audit information already available.
13. Do not rerun the job until the criteria and downstream effects are understood.
14. If temporary auditing is proposed, account for its significant performance cost. Use Data Automation

## Do Not Assume

- A Data View name proves its current membership logic.
- Person inactivation affects only the person’s Active flag.
- The documented Tuesday schedule is still configured locally.
- Do not rerun the job until the criteria and downstream effects are understood.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records
- https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-data-automation
- https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-audit-information
