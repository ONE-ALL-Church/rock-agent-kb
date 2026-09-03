---
concept_id: system-admin-ops
task_id: recipe-refresh-stale-cached-output-with-minimum-scope
title: Recipe: Refresh stale cached output with minimum scope
generated: true
---

# Recipe: Refresh stale cached output with minimum scope

Refresh the affected output without unnecessarily clearing unrelated caches.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Step`
- `Page`
- `Block`

## Entities And Tables

- `Step`
- `Page`
- `Block`

## Steps

1. Identify the stale block and its caching mode.
2. Open its settings and identify assigned cache tags.
3. Open Cache Manager.
4. Clear the most specific applicable tag.
5. Reload the affected page and confirm that the intended content changed.
6. If it remains stale, determine whether the data comes from a Persisted Dataset or another cache layer before taking broader action.

## Do Not Assume

- The linked-key count must decrease after a tag clear.
- A global cache clear will regenerate a Persisted Dataset.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-manager
- https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/clear-cache-tags
- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexableEntityBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexStatusBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
