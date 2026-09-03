---
concept_id: documents-signatures
title: Documents And Signatures Open Questions
generated: true
---

# Documents And Signatures Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (189 words)

## Community-Supported Only

- `agent-task-recipes-recipe-evaluate-a-community-resend-or-reset-workaround`: Recipe: Evaluate a community resend or reset workaround
- `source-map-training-and-community-examples`: Training and community examples

## Needs Live Verification

- `mental-model`: Mental Model
- `entity-documents-document-types-and-storage`: Document types and storage
- `document-templates-and-merge-documents-word-templates`: Word templates
- `document-templates-and-merge-documents-html-templates`: HTML templates
- `electronic-signatures-electronic-signatures-in-event-registration`: Electronic signatures in event registration
- `managing-completed-signature-documents`: Managing Completed Signature Documents
- `troubleshooting-decision-tree-a-document-type-is-missing-from-the-documents-block`: A document type is missing from the Documents block
- `troubleshooting-decision-tree-an-entity-document-add-workflow-fails`: An Entity Document Add workflow fails
- `troubleshooting-decision-tree-a-user-cannot-view-or-download-a-document`: A user cannot view or download a document
- `troubleshooting-decision-tree-lava-fails-in-a-word-merge-template`: Lava fails in a Word merge template
- `troubleshooting-decision-tree-email-addresses-are-missing-from-an-html-merge-document`: Email addresses are missing from an HTML merge document
- `troubleshooting-decision-tree-a-workflow-uses-the-wrong-signature-template`: A workflow uses the wrong signature template
- `troubleshooting-decision-tree-the-wrong-person-is-expected-to-sign`: The wrong person is expected to sign
- `troubleshooting-decision-tree-event-registration-signatures-break-or-display-the-wrong-document`: Event registration signatures break or display the wrong document
- `troubleshooting-decision-tree-a-signed-pdf-is-not-generated-or-delivery-stalls`: A signed PDF is not generated or delivery stalls
- `agent-task-recipes-recipe-configure-an-entity-document-type-and-management-surface`: Recipe: Configure an entity document type and management surface
- `agent-task-recipes-recipe-create-and-validate-a-merge-template`: Recipe: Create and validate a merge template
- `agent-task-recipes-recipe-configure-a-signature-template`: Recipe: Configure a signature template
- `agent-task-recipes-recipe-add-an-electronic-signature-to-a-workflow`: Recipe: Add an electronic signature to a workflow
- `agent-task-recipes-recipe-configure-an-event-registration-signature-requirement`: Recipe: Configure an event-registration signature requirement
- `agent-task-recipes-recipe-review-a-completed-signature-document-and-resend-its-receipt`: Recipe: Review a completed signature document and resend its receipt
- `agent-task-recipes-recipe-decide-whether-to-offload-signed-pdf-rendering`: Recipe: Decide whether to offload signed-PDF rendering
- `agent-task-recipes-recipe-evaluate-a-community-resend-or-reset-workaround`: Recipe: Evaluate a community resend or reset workaround
- `known-gaps-and-live-verification`: Known Gaps And Live Verification

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
