---
concept_id: documents-signatures
title: Documents And Signatures Quickstart
generated: true
---

# Documents And Signatures Quickstart

Documents, document templates, generated PDFs, electronic signatures, signature requests, storage, and document-related workflow patterns.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Configure an entity document type and management surface](tasks/recipe-configure-an-entity-document-type-and-management-surface.md): Users can manage an approved document category for the intended entity type.
- [Recipe: Create and validate a merge template](tasks/recipe-create-and-validate-a-merge-template.md): A global or personal template generates the intended output from a known grid source.
- [Recipe: Configure a signature template](tasks/recipe-configure-a-signature-template.md): A reviewed signature template can generate and store signed documents using the intended signer experience.
- [Recipe: Add an electronic signature to a workflow](tasks/recipe-add-an-electronic-signature-to-a-workflow.md): The workflow presents the correct document to the correct signer and retains the resulting signed file.
- [Recipe: Configure an event-registration signature requirement](tasks/recipe-configure-an-event-registration-signature-requirement.md): Each registrant receives the correct signature requirement through the supported registration flow.
- [Recipe: Review a completed signature document and resend its receipt](tasks/recipe-review-a-completed-signature-document-and-resend-its-receipt.md): An authorized administrator verifies the signed record and resends the existing completion email when appropriate.
- [Recipe: Decide whether to offload signed-PDF rendering](tasks/recipe-decide-whether-to-offload-signed-pdf-rendering.md): The organization has a justified local or external rendering path.
- [Recipe: Evaluate a community resend or reset workaround](tasks/recipe-evaluate-a-community-resend-or-reset-workaround.md): A maintainer determines whether a community recipe is safe and still necessary without executing destructive steps by default.

## High-Signal Sections

- `agent-summary` lines 18-27: Agent Summary (normal)
- `mental-model` lines 48-67: Mental Model (normal)
- `entity-documents-document-types-and-storage` lines 70-86: Document types and storage (normal)
- `entity-documents-page-context-and-documents-block` lines 87-94: Page context and Documents block (normal)
- `entity-documents-adding-entity-documents-through-workflows` lines 95-107: Adding entity documents through workflows (high)
- `document-templates-and-merge-documents-global-and-personal-templates` lines 110-115: Global and personal templates (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the documents-signatures guide.
- `Block`: Rock concept/entity referenced by the documents-signatures guide.
- `Family`: Rock concept/entity referenced by the documents-signatures guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the documents-signatures guide.
- `Page`: Rock concept/entity referenced by the documents-signatures guide.
- `Person`: Rock concept/entity referenced by the documents-signatures guide.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the documents-signatures guide.

## Version Caveats

- `17.0`: Updated Electronic Signatures to allow for inserting the signature at specific places in the document template using a new optional "<!--[[ SignatureDetails ]]-->" keyword.
- `17.8`: Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules w
- `18.3`: Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant with
- `16.1`: Fixed Signature Document Templates filtering to not show inactive templates in Workflow Actions. Fixes: #5511

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
