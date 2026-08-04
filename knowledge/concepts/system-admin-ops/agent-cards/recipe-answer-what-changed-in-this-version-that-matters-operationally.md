---
concept_id: system-admin-ops
task_id: recipe-answer-what-changed-in-this-version-that-matters-operationally
title: Recipe: Answer “What Changed In This Version That Matters Operationally?”
generated: true
---

# Recipe: Answer “What Changed In This Version That Matters Operationally?”

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`

## Entities And Tables

- `Workflow`

## Steps

1. Identify current version and target version.
2. Read official release notes.
3. Extract Core, Workflow, Reporting, CMS, Security, Lava, API, and Mobile items if relevant.
4. Map each change to local features in use.
5. Produce test checklist.
6. Include source links.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs
- https://community.rockrms.com/documentation/bookcontent/32
- https://community.rockrms.com/lava/commands/cache-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/developer/303---blast-off/exception-handling
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistoryService.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://community.rockrms.com/rocku/cms/cache-tags
