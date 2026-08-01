---
concept_id: workflows
task_id: recipe-diagnose-an-active-workflow-instance
title: Recipe: Diagnose an active workflow instance
generated: true
---

# Recipe: Diagnose an active workflow instance

The first incorrect state or action is identified without unsafe replay.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Attribute`

## Steps

1. Open Workflow Detail.
2. Record workflow state, status, initiator, and activation time.
3. Inspect attributes and raw formats where relevant.
4. Inspect activated activities and assignments.
5. Locate the first incomplete or unexpected action.
6. Inspect its criteria and prior actions.
7. Read logs and notes.
8. Verify side effects in their owning Rock records.
9. Decide whether retry is idempotent.
10. Re-run only after duplicate and irreversible effects are ruled out.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form
- https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/navigate-the-form-builder
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/chain-entry-forms
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/intro-to-the-form-builder
- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/rocku/workflows/form-builder
