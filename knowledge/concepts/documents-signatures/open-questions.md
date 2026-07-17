---
concept_id: documents-signatures
title: Documents And Signatures Open Questions
generated: true
---

# Documents And Signatures Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `7-common-documents-and-signatures-workflows-add-a-document-to-a-person`: Add A Document To A Person (133 words)
- `10-generated-pdfs-deep-dive-pdf-troubleshooting`: PDF Troubleshooting (154 words)
- `12-administration-and-operational-guardrails-before-creating-a-new-signature-template`: Before Creating A New Signature Template (105 words)
- `13-developer-api-lava-and-source-code-landmarks-lava-in-signature-templates`: Lava In Signature Templates (97 words)
- `16-implementation-playbooks-playbook-build-a-new-event-waiver`: Playbook: Build A New Event Waiver (163 words)
- `16-implementation-playbooks-playbook-build-a-merge-letter-template`: Playbook: Build A Merge Letter Template (85 words)
- `16-implementation-playbooks-playbook-move-from-legacy-signature-provider-to-rock-native-signatures`: Playbook: Move From Legacy Signature Provider To Rock-Native Signatures (88 words)
- `17-troubleshooting-decision-tree-merge-documents`: Merge Documents (91 words)

## Community-Supported Only

- `12-administration-and-operational-guardrails-data-integrity-guardrails`: Data Integrity Guardrails

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `3-documents-and-signatures-mental-model-entity-documents`: Entity Documents
- `3-documents-and-signatures-mental-model-merge-documents`: Merge Documents
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-entity-document-configuration`: Entity Document Configuration
- `6-primary-entities-and-relationships-entity-document-relationships`: Entity Document Relationships
- `7-common-documents-and-signatures-workflows-add-a-document-to-a-person`: Add A Document To A Person
- `7-common-documents-and-signatures-workflows-add-documents-to-groups-or-other-entities`: Add Documents To Groups Or Other Entities
- `7-common-documents-and-signatures-workflows-add-entity-documents-from-workflows`: Add Entity Documents From Workflows
- `7-common-documents-and-signatures-workflows-generate-a-merge-document-from-a-grid`: Generate A Merge Document From A Grid
- `7-common-documents-and-signatures-workflows-collect-a-signature-in-a-workflow`: Collect A Signature In A Workflow
- `7-common-documents-and-signatures-workflows-collect-a-signature-in-event-registration`: Collect A Signature In Event Registration
- `8-document-templates-deep-dive-merge-templates`: Merge Templates
- `8-document-templates-deep-dive-signature-document-templates`: Signature Document Templates
- `8-document-templates-deep-dive-signature-placement`: Signature Placement
- `9-electronic-signatures-deep-dive-typed-versus-drawn-signatures`: Typed Versus Drawn Signatures
- `9-electronic-signatures-deep-dive-validity-and-reuse`: Validity And Reuse
- `9-electronic-signatures-deep-dive-workflows`: Workflows
- `9-electronic-signatures-deep-dive-event-registrations`: Event Registrations
- `9-electronic-signatures-deep-dive-managing-signed-documents`: Managing Signed Documents
- `10-generated-pdfs-deep-dive-what-the-pdf-represents`: What The PDF Represents
- `10-generated-pdfs-deep-dive-pdf-preview-versus-signed-pdf`: PDF Preview Versus Signed PDF
- `10-generated-pdfs-deep-dive-performance-and-offloading`: Performance And Offloading
- `10-generated-pdfs-deep-dive-pdf-troubleshooting`: PDF Troubleshooting
- `11-related-rock-areas-people-workflows-communications-security-platform-configuration-cms-security`: Security
- `12-administration-and-operational-guardrails-before-creating-a-new-signature-template`: Before Creating A New Signature Template
- `13-developer-api-lava-and-source-code-landmarks-api-considerations`: API Considerations
- `13-developer-api-lava-and-source-code-landmarks-lava-in-signature-templates`: Lava In Signature Templates
- `14-reporting-analytics-and-model-map-model-map`: Model Map
- `14-reporting-analytics-and-model-map-signature-reporting`: Signature Reporting
- `14-reporting-analytics-and-model-map-entity-document-reporting`: Entity Document Reporting
- `14-reporting-analytics-and-model-map-merge-document-analytics`: Merge Document Analytics
- `15-version-and-release-caveats-inactive-signature-templates`: Inactive Signature Templates
- `15-version-and-release-caveats-signature-placement-keyword`: Signature Placement Keyword
- `15-version-and-release-caveats-signature-template-detail-pdf-viewer`: Signature Template Detail PDF Viewer
- `16-implementation-playbooks-playbook-build-a-new-event-waiver`: Playbook: Build A New Event Waiver
- `16-implementation-playbooks-playbook-add-documents-to-a-group-page`: Playbook: Add Documents To A Group Page
- `16-implementation-playbooks-playbook-build-a-merge-letter-template`: Playbook: Build A Merge Letter Template

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
