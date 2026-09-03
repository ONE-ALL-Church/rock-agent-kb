---
concept_id: documents-signatures
task_id: recipe-evaluate-a-community-resend-or-reset-workaround
title: Recipe: Evaluate a community resend or reset workaround
generated: true
---

# Recipe: Evaluate a community resend or reset workaround

A maintainer determines whether a community recipe is safe and still necessary without executing destructive steps by default.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Step`
- `Group`
- `Workflow`

## Entities And Tables

- `Step`
- `Group`
- `Workflow`

## Steps

1. First test the official completed-document resend action to determine whether it satisfies the need.
2. Define whether the desired outcome is receipt redelivery, a new signature request, clearing a group requirement, or replacing an invalid registrant signature.
3. Review the installed Rock version and relevant fixes.
4. Read the community recipe as a design example, not as approved core behavior.
5. Identify every delete, relationship reset, command SQL, security-disabled entity access, and bulk-action path.
6. Confirm backups, rollback, authorization, schema compatibility, record scope, and a non-production test plan.
7. Prefer supported workflow actions and current core behavior where they meet the requirement.
8. Stop before executing SQL, deleting signature documents, clearing registrant relationships, or deleting workflows unless those exact mutations are separately reviewed and authorized. (Re-Send Signature Documents from Registrant, Resend a Group Requirement Helper Workflow)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/recipes/482
- https://community.rockrms.com/rocku/workflows/components-of-a-workflow
- https://community.rockrms.com/rocku/workflows/custom-grid-actions
- https://community.rockrms.com/rocku/workflows/electronic-signatures-1
- https://community.rockrms.com/recipes/434
