---
concept_id: documents-signatures
task_id: recipe-build-a-staff-resend-process
title: Recipe: Build A Staff Resend Process
generated: true
---

# Recipe: Build A Staff Resend Process

Prefer supported UI actions first. Manage Signature Documents notes that signed document detail can resend completion email. For invite resends or reissue scenarios, inspect current Rock-supported actions before using custom workflows.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`

## Entities And Tables

- `Person`
- `Workflow`

## Steps

1. Do not delete signed records by default.
2. Capture applies-to person, assigned-to person, template, and source entity.
3. Create a new signature request if legally appropriate.
4. Preserve the old request for audit unless approved.
5. Log who initiated resend and why.
6. Test parent/guardian and registrar scenarios.

## Do Not Assume

- Do not delete signed records by default.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents
- https://community.rockrms.com/rocku/workflows/electronic-signatures-1
- https://community.rockrms.com/rocku/cms/entity-documents
- https://community.rockrms.com/recipes/482
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/rocku/workflows/workflow-person-entry
- https://community.rockrms.com/rocku/workflows/workflow-entry
- https://community.rockrms.com/rocku/workflows/components-of-a-workflow
- https://community.rockrms.com/rocku/workflows/persisted-workflows
