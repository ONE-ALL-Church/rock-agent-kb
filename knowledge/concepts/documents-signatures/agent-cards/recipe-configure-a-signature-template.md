---
concept_id: documents-signatures
task_id: recipe-configure-a-signature-template
title: Recipe: Configure a signature template
generated: true
---

# Recipe: Configure a signature template

A reviewed signature template can generate and store signed documents using the intended signer experience.

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

1. Open `Admin Tools > Settings > Signature Documents`.
2. Define a clear name, description, and document term.
3. Select typed or drawn input; prefer typed unless an approved requirement justifies storing drawn-signature PII.
4. Select the signed-document file type.
5. Select the completion System Communication.
6. Decide whether completed documents can remain valid for future use.
7. Author the Lava body and verify that its attribute keys match the intended workflow or registration inputs.
8. Add `<!-- [[ SignatureDetails ]] -->` wherever explicit or repeated signature placement is required.
9. Preview or test with non-sensitive representative data.
10. Verify the stored document and completion email as separate outcomes. (Set Up Electronic Signatures)
11. Inspect the fixed **Signature Document Template** action setting.
12. Inspect the dynamic template ID, GUID, or workflow attribute.
13. If both are populated, treat the fixed template as authoritative because it takes precedence.
14. Confirm that the selected template is active; Rock 16.1 fixed inactive-template filtering in workflow actions.
15. Confirm that attribute values contain the expected ID or GUID representation. (Use Electronic Signatures in a Workflow, Rock Core Release Notes)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Attribute/SignatureDocumentTemplateFieldAttribute.cs
- https://community.rockrms.com/rocku/workflows/components-of-a-workflow
- https://community.rockrms.com/rocku/workflows/custom-grid-actions
- https://community.rockrms.com/rocku/workflows/electronic-signatures-1
- https://community.rockrms.com/recipes/482
