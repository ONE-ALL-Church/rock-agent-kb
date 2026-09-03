---
concept_id: documents-signatures
title: Documents And Signatures Agent Cheatsheet
generated: true
---

# Documents And Signatures Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Configure an entity document type and management surface](tasks/recipe-configure-an-entity-document-type-and-management-surface.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Create and validate a merge template](tasks/recipe-create-and-validate-a-merge-template.md) | `Person`, `Group`, `GroupMember`, `Family` | `Person`, `Group`, `GroupMember`, `Family` |
| [Recipe: Configure a signature template](tasks/recipe-configure-a-signature-template.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Add an electronic signature to a workflow](tasks/recipe-add-an-electronic-signature-to-a-workflow.md) | `Person`, `Workflow`, `Attribute` | `Person`, `Workflow`, `Attribute` |
| [Recipe: Configure an event-registration signature requirement](tasks/recipe-configure-an-event-registration-signature-requirement.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Review a completed signature document and resend its receipt](tasks/recipe-review-a-completed-signature-document-and-resend-its-receipt.md) |  |  |
| [Recipe: Decide whether to offload signed-PDF rendering](tasks/recipe-decide-whether-to-offload-signed-pdf-rendering.md) |  |  |
| [Recipe: Evaluate a community resend or reset workaround](tasks/recipe-evaluate-a-community-resend-or-reset-workaround.md) | `Step`, `Group`, `Workflow` | `Step`, `Group`, `Workflow` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.0` | core | Updated Electronic Signatures to allow for inserting the signature at specific places in the document template using a new optional "<!--[[ SignatureDetails ]]-->" keyword. |
| `17.8` | core | Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules when someone tried to |
| `18.3` | core | Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant without a valid Signatur |
| `16.1` | core | Fixed Signature Document Templates filtering to not show inactive templates in Workflow Actions. Fixes: #5511 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | needs-citation | needs-citation |
| `mental-model` | normal | live verification |
| `entity-documents-document-types-and-storage` | normal | live verification |
| `document-templates-and-merge-documents-word-templates` | normal | live verification |
| `document-templates-and-merge-documents-html-templates` | normal | live verification |
| `electronic-signatures-electronic-signatures-in-event-registration` | high | live verification |
| `managing-completed-signature-documents` | high | live verification |
| `troubleshooting-decision-tree-a-document-type-is-missing-from-the-documents-block` | normal | live verification |
| `troubleshooting-decision-tree-an-entity-document-add-workflow-fails` | high | live verification |
| `troubleshooting-decision-tree-a-user-cannot-view-or-download-a-document` | high | live verification |
| `troubleshooting-decision-tree-lava-fails-in-a-word-merge-template` | normal | live verification |
| `troubleshooting-decision-tree-email-addresses-are-missing-from-an-html-merge-document` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-uses-the-wrong-signature-template` | high | live verification |
| `troubleshooting-decision-tree-the-wrong-person-is-expected-to-sign` | normal | live verification |
| `troubleshooting-decision-tree-event-registration-signatures-break-or-display-the-wrong-document` | high | live verification |
| `troubleshooting-decision-tree-a-signed-pdf-is-not-generated-or-delivery-stalls` | normal | live verification |
| `agent-task-recipes-recipe-configure-an-entity-document-type-and-management-surface` | normal | live verification |
| `agent-task-recipes-recipe-create-and-validate-a-merge-template` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-signature-template` | normal | live verification |
| `agent-task-recipes-recipe-add-an-electronic-signature-to-a-workflow` | normal | live verification |
| `agent-task-recipes-recipe-configure-an-event-registration-signature-requirement` | normal | live verification |
| `agent-task-recipes-recipe-review-a-completed-signature-document-and-resend-its-receipt` | normal | live verification |
| `agent-task-recipes-recipe-decide-whether-to-offload-signed-pdf-rendering` | normal | live verification |
| `agent-task-recipes-recipe-evaluate-a-community-resend-or-reset-workaround` | community-supported | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-training-and-community-examples` | community-supported | community-supported |
