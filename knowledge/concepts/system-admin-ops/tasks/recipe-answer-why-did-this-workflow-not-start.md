---
concept_id: system-admin-ops
task_id: recipe-answer-why-did-this-workflow-not-start
title: Recipe: Answer “Why Did This Workflow Not Start?”
generated: true
---

# Recipe: Answer “Why Did This Workflow Not Start?”

Complete Answer “Why Did This Workflow Not Start?” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`
- `Workflow`

## Entities And Tables

- `Schedule`
- `Workflow`

## Steps

1. Identify workflow type.
2. Identify trigger or launch job.
3. Check job history if scheduled.
4. Check workflow security/category permissions.
5. Check exception logs.
6. Check required form fields and entity context.
7. Check release notes for workflow fixes.
8. Verify whether it never started or started and failed.

## Do Not Assume

- Verify whether it never started or started and failed.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/32
- https://community.rockrms.com/lava/commands/cache-commands
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/developer/303---blast-off/exception-handling
- https://community.rockrms.com/rocku/cms/cache-tags
- https://community.rockrms.com/lava/lava-api
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://community.rockrms.com/recipes/503
