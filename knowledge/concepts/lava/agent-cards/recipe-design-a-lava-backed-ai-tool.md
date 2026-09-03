---
concept_id: lava
task_id: recipe-design-a-lava-backed-ai-tool
title: Recipe: Design a Lava-backed AI tool
generated: true
---

# Recipe: Design a Lava-backed AI tool

A narrow tool the model can select and use without excessive access.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Name the tool with a clear verb and entity.
2. Define explicit parameters and sanitize them.
3. Enforce current-person and agent authorization.
4. Prefer cache or entity access over SQL when it fits the task.
5. If static SQL is necessary, review it and keep it bounded.
6. Return a structured `AgentToolResult`.
7. Include only fields needed for the task.
8. Use dedicated filters for instructions, history, metadata and Rock references.
9. Exercise the tool with allowed, denied, empty and maximum-size inputs.
10. Inspect built-in tool logs for calls, inputs and results.

## Do Not Assume

- Internal means unrestricted.
- Chat and MCP should expose the same tools.
- The model should generate SQL.
- More context improves tool selection.

## Source Links

- https://www.youtube.com/watch?v=UvW68dZBcJ8
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupPlacement/PersonFiltersBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupPlacement/personFiltersBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Plugin/HotFixes/295_FixGoupPlacementPersonFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataFilter/Person/FirstContributionDateFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Tests.Integration/Core/Lava/Filters/PersonFilterTests.cs
- https://community.rockrms.com/lava/workflows
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/lava/commands/entity-commands
