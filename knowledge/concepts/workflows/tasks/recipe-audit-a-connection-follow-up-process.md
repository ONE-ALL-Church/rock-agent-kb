---
concept_id: workflows
task_id: recipe-audit-a-connection-follow-up-process
title: Recipe: Audit a connection follow-up process
generated: true
---

# Recipe: Audit a connection follow-up process

A Connection process is understood as both person context and operational state.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Campus`
- `Workflow`

## Entities And Tables

- `Person`
- `Campus`
- `Workflow`

## Steps

1. Identify the person and request.
2. Record Connection Type, Opportunity, status, campus, connector, assignee, and next action.
3. Inspect activity and workflow relationships.
4. Compare Board and List visibility.
5. Check filters and current-user security.
6. Identify staff ownership and completion criteria.
7. Inspect active requests before changing Type or Opportunity configuration.
8. Reconcile reporting dependencies.
9. Verify the final staff work queue after any approved change.

## Do Not Assume

- A missing card means the request itself is wrong.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows
- https://community.rockrms.com/rocku/workflows/form-builder
- https://community.rockrms.com/lava
- https://community.rockrms.com/lava/commands/entity-commands
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://community.rockrms.com/rocku/engagement/connections-overview
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-control
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances
- https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities
