---
concept_id: documents-signatures
task_id: recipe-diagnose-a-failed-registration-signature
title: Recipe: Diagnose A Failed Registration Signature
generated: true
---

# Recipe: Diagnose A Failed Registration Signature

Complete Diagnose A Failed Registration Signature with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Block`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Block`

## Steps

1. Registration instance.
2. Registration template required signature template.
3. External Registration Entry block generation.
4. Registrant person alias.
5. Registrant `SignatureDocumentId`.
6. Existing valid signatures for that person and template.
7. Signature document status.
8. Exception logs.
9. Whether the signature was required.
10. Whether it was skipped because a valid signature already existed.
11. Whether a Signature Document was created.
12. Whether the registrant is linked to it.
13. Whether the signer completed it.
14. Whether the PDF and completion email exist.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentDetail/signatureDocumentBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/SignatureDocumentTemplateDetailOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/SignatureDocumentTemplateBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateList/signatureDocumentTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/SignatureDocumentTemplateList.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/GetPdfPreviewUrlRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/SignatureDocumentTemplateDetail.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateBag.d.ts
