---
concept_id: documents-signatures
task_id: recipe-configure-an-event-registration-signature-requirement
title: Recipe: Configure an event-registration signature requirement
generated: true
---

# Recipe: Configure an event-registration signature requirement

Each registrant receives the correct signature requirement through the supported registration flow.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Confirm the external page uses the Obsidian Registration Entry block.
2. Confirm the signature template uses Rock’s built-in electronic-signature system.
3. Edit the registration template under `Tools > Event Registration`.
4. Select the required signature document.
5. Review whether birthdate should be required so adult/child assignment is reliable.
6. Test an adult registering themselves.
7. Test an adult registering a child.
8. Test a matched person with an existing valid document for the same required template.
9. Verify the registrant relationship and displayed completion state from the registration instance.
10. Confirm receipt PDF generation and delivery separately. (Use Electronic Signatures in Event Registrations)
11. Confirm the external registration page uses the Obsidian Registration Entry block.
12. Confirm the required template is a current built-in electronic-signature template rather than a legacy-provider document.
13. Inspect the registration template’s Required Signature Document selection.
14. Confirm the registrant’s person match, signature-document relationship, required template, and validity.
15. Determine whether the installation includes the Rock 18.3 registrant relationship fix and migration. (Use Electronic Signatures in Event Registrations, Rock Core Release Notes)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateList/signatureDocumentTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/SignatureDocumentTemplateList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/SignatureDocumentTemplateBag.cs
- https://www.rockrms.com/releasenotes
