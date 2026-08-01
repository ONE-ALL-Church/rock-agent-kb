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
