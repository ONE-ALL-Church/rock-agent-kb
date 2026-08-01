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

## Entities And Tables

- `Group`
- `Campus`
- `Workflow`
- `Page`
- `Attribute`

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
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/launch-a-workflow
- https://community.rockrms.com/documentation/core-concepts/workflows/entry-forms/chain-entry-forms
- https://community.rockrms.com/documentation/core-concepts/workflows/form-builder/intro-to-the-form-builder
- https://community.rockrms.com/lava/commands/workflow-activate-commands
