---
concept_id: documents-signatures
title: Documents And Signatures Agent Cheatsheet
generated: true
---

# Documents And Signatures Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find All Pending Signature Requests For A Template](tasks/recipe-find-all-pending-signature-requests-for-a-template.md) |  |  |
| [Recipe: Verify A Person Has A Valid Signed Waiver](tasks/recipe-verify-a-person-has-a-valid-signed-waiver.md) |  |  |
| [Recipe: Diagnose A Failed Registration Signature](tasks/recipe-diagnose-a-failed-registration-signature.md) |  |  |
| [Recipe: Audit Public Exposure Risk](tasks/recipe-audit-public-exposure-risk.md) |  |  |
| [Recipe: Build A Staff Resend Process](tasks/recipe-build-a-staff-resend-process.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
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
| `15.2` | core | Fixed inactive signature document template from being selected in event registration. Fixes: #5510 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | high | live verification |
| `3-documents-and-signatures-mental-model-entity-documents` | normal | live verification |
| `3-documents-and-signatures-mental-model-merge-documents` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-entity-document-configuration` | normal | live verification |
| `6-primary-entities-and-relationships-entity-document-relationships` | normal | live verification |
| `7-common-documents-and-signatures-workflows-add-a-document-to-a-person` | normal | live verification |
| `7-common-documents-and-signatures-workflows-add-documents-to-groups-or-other-entities` | normal | live verification |
| `7-common-documents-and-signatures-workflows-add-entity-documents-from-workflows` | normal | live verification |
| `7-common-documents-and-signatures-workflows-generate-a-merge-document-from-a-grid` | normal | live verification |
| `7-common-documents-and-signatures-workflows-collect-a-signature-in-a-workflow` | normal | live verification |
| `7-common-documents-and-signatures-workflows-collect-a-signature-in-event-registration` | high | live verification |
| `8-document-templates-deep-dive-merge-templates` | normal | live verification |
| `8-document-templates-deep-dive-signature-document-templates` | high | live verification |
| `8-document-templates-deep-dive-signature-placement` | normal | live verification |
| `9-electronic-signatures-deep-dive-typed-versus-drawn-signatures` | normal | live verification |
| `9-electronic-signatures-deep-dive-validity-and-reuse` | normal | live verification |
| `9-electronic-signatures-deep-dive-workflows` | normal | live verification |
| `9-electronic-signatures-deep-dive-event-registrations` | normal | live verification |
| `9-electronic-signatures-deep-dive-managing-signed-documents` | normal | live verification |
| `10-generated-pdfs-deep-dive-what-the-pdf-represents` | normal | live verification |
| `10-generated-pdfs-deep-dive-pdf-preview-versus-signed-pdf` | structural | live verification |
| `10-generated-pdfs-deep-dive-performance-and-offloading` | normal | live verification |
| `10-generated-pdfs-deep-dive-pdf-troubleshooting` | normal | live verification |
| `11-related-rock-areas-people-workflows-communications-security-platform-configuration-cms-security` | high | live verification |
| `12-administration-and-operational-guardrails-before-creating-a-new-signature-template` | normal | live verification |
| `12-administration-and-operational-guardrails-data-integrity-guardrails` | community-supported | community-supported |
| `13-developer-api-lava-and-source-code-landmarks-api-considerations` | structural | live verification |
| `13-developer-api-lava-and-source-code-landmarks-lava-in-signature-templates` | normal | live verification |
| `14-reporting-analytics-and-model-map-model-map` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-signature-reporting` | citation-only | live verification |
| `14-reporting-analytics-and-model-map-entity-document-reporting` | structural | live verification |
| `14-reporting-analytics-and-model-map-merge-document-analytics` | structural | live verification |
| `15-version-and-release-caveats-inactive-signature-templates` | normal | live verification |
| `15-version-and-release-caveats-signature-placement-keyword` | normal | live verification |
| `15-version-and-release-caveats-signature-template-detail-pdf-viewer` | citation-only | live verification |
| `16-implementation-playbooks-playbook-build-a-new-event-waiver` | normal | live verification |
| `16-implementation-playbooks-playbook-add-documents-to-a-group-page` | structural | live verification |
| `16-implementation-playbooks-playbook-build-a-merge-letter-template` | normal | live verification |
| `16-implementation-playbooks-playbook-move-from-legacy-signature-provider-to-rock-native-signatures` | normal | live verification |
| `16-implementation-playbooks-playbook-audit-document-security-after-upgrade` | structural | live verification |
| `17-troubleshooting-decision-tree-merge-documents` | normal | live verification |
| `17-troubleshooting-decision-tree-electronic-signatures` | normal | live verification |
| `17-troubleshooting-decision-tree-generated-pdfs` | normal | live verification |
| `18-agent-task-recipes-recipe-find-all-pending-signature-requests-for-a-template` | structural | live verification |
| `18-agent-task-recipes-recipe-verify-a-person-has-a-valid-signed-waiver` | structural | live verification |
| `18-agent-task-recipes-recipe-diagnose-a-failed-registration-signature` | structural | live verification |
| `18-agent-task-recipes-recipe-audit-public-exposure-risk` | structural | live verification |
| `18-agent-task-recipes-recipe-build-a-staff-resend-process` | normal | live verification |
| `19-source-map-and-dependency-notes` | high | live verification |
