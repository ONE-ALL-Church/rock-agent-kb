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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Find All Pending Signature Requests For A Template](tasks/recipe-find-all-pending-signature-requests-for-a-template.md): Complete Find All Pending Signature Requests For A Template with evidence-backed checks and a verifiable outcome.
- [Recipe: Verify A Person Has A Valid Signed Waiver](tasks/recipe-verify-a-person-has-a-valid-signed-waiver.md): Complete Verify A Person Has A Valid Signed Waiver with evidence-backed checks and a verifiable outcome.
- [Recipe: Diagnose A Failed Registration Signature](tasks/recipe-diagnose-a-failed-registration-signature.md): Complete Diagnose A Failed Registration Signature with evidence-backed checks and a verifiable outcome.
- [Recipe: Audit Public Exposure Risk](tasks/recipe-audit-public-exposure-risk.md): Complete Audit Public Exposure Risk with evidence-backed checks and a verifiable outcome.
- [Recipe: Build A Staff Resend Process](tasks/recipe-build-a-staff-resend-process.md): Prefer supported UI actions first. Manage Signature Documents notes that signed document detail can resend completion email. For invite resends or reissue scenarios, inspect current Rock-supported actions before using custom workflows.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-46: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 47-85: 2. Scope And Terminology (high)
- `3-documents-and-signatures-mental-model-entity-documents` lines 90-102: Entity Documents (normal)
- `3-documents-and-signatures-mental-model-merge-documents` lines 103-117: Merge Documents (normal)
- `3-documents-and-signatures-mental-model-electronic-signatures` lines 118-134: Electronic Signatures (normal)
- `3-documents-and-signatures-mental-model-generated-pdfs` lines 135-148: Generated PDFs (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the documents-signatures guide.
- `Block`: Rock concept/entity referenced by the documents-signatures guide.
- `Family`: Rock concept/entity referenced by the documents-signatures guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the documents-signatures guide.
- `Label`: Rock concept/entity referenced by the documents-signatures guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the documents-signatures guide.
- `Person`: Rock concept/entity referenced by the documents-signatures guide.
- `PersonAlias`: Rock concept/entity referenced by the documents-signatures guide.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the documents-signatures guide.

## Version Caveats

- `17.0`: Updated Electronic Signatures to allow for inserting the signature at specific places in the document template using a new optional "<!--[[ SignatureDetails ]]-->" keyword.
- `17.8`: Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules w
- `18.3`: Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant with
- `16.1`: Fixed Signature Document Templates filtering to not show inactive templates in Workflow Actions. Fixes: #5511
- `15.2`: Fixed inactive signature document template from being selected in event registration. Fixes: #5510

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
