---
concept_id: documents-signatures
task_id: recipe-configure-an-entity-document-type-and-management-surface
title: Recipe: Configure an entity document type and management surface
generated: true
---

# Recipe: Configure an entity document type and management surface

Users can manage an approved document category for the intended entity type.

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

1. Identify the target entity type and whether qualifiers should restrict the type to a subset.
2. Select the associated file type and review its security and required preferred-file settings.
3. Create or review the entity document type under `Admin Tools > Settings > Document Types`.
4. Configure manual selection, maximum documents, qualifiers, and default naming as needed.
5. For Person, inspect the existing Person Profile document surface.
6. For another entity, place a Documents block on a page with that entity in context.
7. Configure the block’s Entity Type, allowed Document Types, and security-button visibility.
8. Test with a non-sensitive file and an authorized test role.
9. Verify add, list, download, and security behavior separately. (Configure Entity Documents, Add the Block)
10. Confirm that the page supplies the intended entity in context.
11. Confirm that the Documents block’s Entity Type matches that context.
12. Inspect the block’s selected Document Types.
13. Inspect the document type’s Entity Type and any qualifier column and value.
14. Confirm that the document type is manually selectable if a user is trying to add it manually.
15. Confirm that any maximum-documents limit has not been reached. (Configure Entity Documents, Add the Block)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates
- https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateList/signatureDocumentTemplateListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/SignatureDocumentTemplateList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/SignatureDocumentTemplateBag.cs
