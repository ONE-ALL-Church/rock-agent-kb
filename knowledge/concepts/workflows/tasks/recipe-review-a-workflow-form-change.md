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
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Workflow`
- `Attribute`
- `Page`
- `Block`

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
10. Identify the exact surface: Workflow navigation, direct Workflow Entry page, Workflow List, Workflow Detail, My Workflows, or Form Builder.
11. Confirm the workflow type is active and the expected category is selected in the block settings.
12. Check category and workflow-type View permissions.
13. For Workflow Entry, confirm there is an active Form action assigned to the current person and that the person can view the activity.
14. For My Workflows, confirm the activity is active, has an active form, is assigned appropriately, and the person can view it.
15. Verify login, form start/end dates, and share-link settings when using Form Builder.
16. Stop when visibility is explained; do not alter the workflow instance merely to force it onto a list.

## Do Not Assume

- Stop when visibility is explained; do not alter the workflow instance merely to force it onto a list.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/configure-a-webhook-to-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/understand-form-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/manage-workflow-instances/edit-workflow-details
- https://community.rockrms.com/documentation/core-concepts/workflows/workflow-components/workflow-actions
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/sms-pipeline-workflows
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/create-a-form
- https://community.rockrms.com/documentation/core-concepts/workflows/build-a-workflow/define-workflow-activities
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/navigate-the-form-builder
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/chain-entry-forms
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/intro-to-the-form-builder
- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows
