---
concept_id: workflows
task_id: recipe-design-background-orchestration
title: Recipe: Design background orchestration
generated: true
---

# Recipe: Design background orchestration

Slow work proceeds asynchronously with explicit operational state.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Define queued, processing, completed, retryable-failure, and terminal-failure states.
2. Store only the identifiers needed to inspect the external work.
3. Define retry limits and duplicate suppression.
4. Define a completion check.
5. Keep the user-facing request path non-blocking.
6. Link output into public pages or apps only after completion is verified.
7. Surface concise staff status without unnecessary raw provider payloads.
8. Test timeout, duplicate callback, partial success, and final failure.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock.ViewModels/Blocks/WorkFlow/FormBuilder/FormPersonEntryViewModel.cs
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/RockWeb/Blocks/WorkFlow/ActivateWorkflow.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://community.rockrms.com/lava
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/25BMk3Glnr
