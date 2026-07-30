---
concept_id: workflows
task_id: recipe-review-a-workflow-form-change
title: Recipe: Review a workflow form change
generated: true
---

# Recipe: Review a workflow form change

A field change that preserves validation, visibility, and downstream behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Workflow`
- `Attribute`

## Steps

1. Identify the workflow type, Form action, and attribute key.
2. Record the current field type and stored-value format.
3. Inspect visible, editable, required, and conditional settings.
4. Inspect Person Entry implications.
5. Find every action filter, Set Attribute action, communication, report, and integration that consumes the value.
6. Test every conditional branch, including omitted-field behavior.
7. Submit a disposable instance.
8. Inspect stored values and downstream outcomes.
9. Verify access as public user, staff user, assignee, and unauthorized user where applicable.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows
- https://community.rockrms.com/rocku/workflows/form-builder
- https://community.rockrms.com/lava
- https://community.rockrms.com/lava/commands/entity-commands
- https://github.com/SparkDevNetwork/Rock/blob/e9c98b9bc6cd4ce2b04115df835a316e49f4ff91/Rock/Lava/Blocks/WorkflowActivateBlock.cs
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-attributes
- https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-attributes
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-actions/workflow-control
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances
