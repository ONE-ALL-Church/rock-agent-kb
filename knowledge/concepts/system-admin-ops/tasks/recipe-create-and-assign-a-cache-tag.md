---
concept_id: system-admin-ops
task_id: recipe-create-and-assign-a-cache-tag
title: Recipe: Create and assign a cache tag
generated: true
---

# Recipe: Create and assign a cache tag

Establish a durable, targeted invalidation boundary for related cached blocks.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Block`

## Entities And Tables

- `Group`
- `Block`

## Steps

1. Define the content group whose caches should be invalidated together.
2. Choose a short lowercase name without spaces.
3. Write a description that explains the tag’s intended scope.
4. Add the tag in `Admin Tools > CMS Configuration > Cache Manager`.
5. Open each caching-enabled block in scope and assign the tag.
6. Test the relationship by changing non-sensitive content, clearing the tag, and verifying all intended blocks.
7. Record the tag as permanent because the documentation says it cannot be modified or deleted.

## Do Not Assume

- Similar block names imply that blocks share a cache.
- A tag can be renamed later. Add Cache Tags

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/add-cache-tags
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/documentation/supporting-rock/caching/cache-tags/use-cache-tags
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexableEntityBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/UniversalSearchControlPanel/indexStatusBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailEnteredDataViewSettingsBag.d.ts
