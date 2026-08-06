---
concept_id: workflows
task_id: recipe-import-or-adapt-a-workflow-safely
title: Recipe: Import or adapt a workflow safely
generated: true
---

# Recipe: Import or adapt a workflow safely

An imported or cloned workflow is validated before activation.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`
- `Workflow`
- `Page`
- `Attribute`
- `Person`
- `Block`

## Entities And Tables

- `Group`
- `Campus`
- `Workflow`
- `Page`
- `Attribute`
- `Person`
- `Block`

## Steps

1. Identify source version, required plugins, action components, and external references.
2. Use Test Only mode for import.
3. Inspect import warnings and the exported package.
4. Place the workflow in an intentional security category.
5. Verify attributes, field types, forms, activities, action order, and component settings.
6. Replace organization-specific communications, groups, campuses, pages, Defined Values, and Connection Opportunities.
7. Test with disposable instances.
8. Verify logs, assignments, communications, and side effects.
9. Connect the live trigger only after validation.
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
- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/secure-workflows
