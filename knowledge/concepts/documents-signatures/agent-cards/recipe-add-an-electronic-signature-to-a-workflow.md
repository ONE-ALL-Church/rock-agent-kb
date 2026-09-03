---
concept_id: documents-signatures
task_id: recipe-add-an-electronic-signature-to-a-workflow
title: Recipe: Add an electronic signature to a workflow
generated: true
---

# Recipe: Add an electronic signature to a workflow

The workflow presents the correct document to the correct signer and retains the resulting signed file.

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

1. Decide whether the action uses one fixed template or a dynamic template ID/GUID.
2. Do not populate the fixed field if dynamic selection is intended.
3. Map Applies To, Assigned To, and Signed By to explicit Person attributes.
4. Add a Binary File workflow attribute for the resulting signature document and select the intended signed-document file type.
5. Define a Lava-enabled document name.
6. Test logged-in and applicable non-logged-in behavior because login affects Signed By handling.
7. Verify the template selected, subject, assigned signer, actual signer, stored PDF, and receipt delivery.
8. If the workflow has multiple launch contexts, condition any unrelated entity mutations on the presence of their required context. (Use Electronic Signatures in a Workflow, RockU Workflows)
9. Inspect the fixed **Signature Document Template** action setting.
10. Inspect the dynamic template ID, GUID, or workflow attribute.
11. If both are populated, treat the fixed template as authoritative because it takes precedence.
12. Confirm that the selected template is active; Rock 16.1 fixed inactive-template filtering in workflow actions.
13. Confirm that attribute values contain the expected ID or GUID representation. (Use Electronic Signatures in a Workflow, Rock Core Release Notes)

## Do Not Assume

- Assigned To and Applies To are interchangeable.
- A dynamic template value overrides a fixed template.
- A bulk launch contains a ConnectionRequest or another pipeline entity.
- Do not populate the fixed field if dynamic selection is intended.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Attribute/SignatureDocumentTemplateFieldAttribute.cs
- https://community.rockrms.com/rocku/workflows/components-of-a-workflow
- https://community.rockrms.com/rocku/workflows/custom-grid-actions
- https://community.rockrms.com/rocku/workflows/electronic-signatures-1
- https://community.rockrms.com/recipes/482
