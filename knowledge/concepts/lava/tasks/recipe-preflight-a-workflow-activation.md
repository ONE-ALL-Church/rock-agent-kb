---
concept_id: lava
task_id: recipe-preflight-a-workflow-activation
title: Recipe: Preflight a workflow activation
generated: true
---

# Recipe: Preflight a workflow activation

A workflow is activated with verified attribute values.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Workflow`
- `Attribute`

## Steps

1. Identify the target workflow type and activity.
2. Enumerate the workflow and activity attribute keys.
3. Map each submitted input to exactly one key.
4. Convert each value to the field type’s stored format.
5. Remove parameters with no matching attribute.
6. Activate one controlled workflow.
7. Read back its stored attributes and rendered state.
8. Test the downstream action that consumes each critical value.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/documentation/digital-publishing/personalization/personalization-segments/personalize-using-lava
- https://community.rockrms.com/lava/commands/entity-commands
- https://community.rockrms.com/lava/filters/attribute-filters
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupPlacement/PersonFiltersBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/Person/FirstContributionDateFilter.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupPlacement/personFiltersBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Core/Lava/Filters/PersonFilterTests.cs
