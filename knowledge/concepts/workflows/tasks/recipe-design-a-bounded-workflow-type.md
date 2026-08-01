---
concept_id: workflows
task_id: recipe-design-a-bounded-workflow-type
title: Recipe: Design a bounded workflow type
generated: true
---

# Recipe: Design a bounded workflow type

A reviewable process model before configuration begins.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Label`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Label`
- `Workflow`
- `Attribute`

## Steps

1. Restate the underlying ministry problem without naming the proposed screen or automation.
2. Generate at least three materially different approaches, including a non-workflow option when credible.
3. Select the workflow approach only if it adds useful state, assignment, branching, automation, or auditability.
4. Define the subject person or entity.
5. List initiation data, derived data, and retained data as attributes.
6. Define activities by responsibility or stage.
7. Define actions in execution order.
8. Define commands, branch criteria, completion, retries, and failure handling.
9. Define security and sensitive-data retention.
10. Define the launch surface and acceptance evidence.

## Do Not Assume

- A status is sufficient to represent every state.
- A visible label is the stored value.
- A successful final message proves every side effect.
- A documented action is installed.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form
- https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/navigate-the-form-builder
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/chain-entry-forms
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/intro-to-the-form-builder
- https://community.rockrms.com/lava/commands/workflow-activate-commands
