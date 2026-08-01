---
concept_id: workflows
task_id: recipe-configure-a-selective-workflow-webhook
title: Recipe: Configure a selective workflow webhook
generated: true
---

# Recipe: Configure a selective workflow webhook

One intended request starts only the intended workflow with inspectable input.

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

1. Define a stable request discriminator.
2. Create or inspect the Workflow Webhook Defined Value.
3. Make Process Request Lava return true only for the intended request.
4. Compare the rule against every other webhook Defined Value.
5. Map only bounded request data into workflow attributes.
6. Store the raw body when structured parsing is needed.
7. Parse and validate inside the workflow.
8. Test no-match, one-match, and accidental-multiple-match cases.
9. Verify authentication and secret handling separately.
10. Inspect the resulting workflow instance.

## Do Not Assume

- Defined Values are evaluated as an exclusive first-match list.

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
