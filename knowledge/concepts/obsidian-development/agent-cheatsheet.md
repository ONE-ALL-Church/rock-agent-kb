---
concept_id: obsidian-development
title: Obsidian Development Agent Cheatsheet
generated: true
---

# Obsidian Development Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Identify The Source Files Behind A Visible Obsidian Block](tasks/recipe-identify-the-source-files-behind-a-visible-obsidian-block.md) |  |  |
| [Recipe: Determine Whether A Bug Is Version-Related](tasks/recipe-determine-whether-a-bug-is-version-related.md) |  |  |
| [Recipe: Review An Obsidian Pull Request](tasks/recipe-review-an-obsidian-pull-request.md) |  |  |
| [Recipe: Audit A Block For Security](tasks/recipe-audit-a-block-for-security.md) |  |  |
| [Recipe: Audit A Grid For Operational Readiness](tasks/recipe-audit-a-grid-for-operational-readiness.md) |  |  |
| [Recipe: Decide Whether To Use Browser Bus](tasks/recipe-decide-whether-to-use-browser-bus.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Fixed editing configuration settings of Universal field types from inside an Obsidian block. This only affected some configuration setting types which might cause the raw value to be stored as JSON. |
| `16.1` | core | Fixed issue of Note Type Field Type not showing up in Following Event Type Detail Obsidian block. Fixes: #5605 |
| `17.1` | core | Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface. |
| `19.1` | core | Fixed an issue where the Obsidian Workflow List block would time out when loading workflows assigned to groups with many members. |
| `18.3` | core | Fixed an issue in Obsidian blocks where Memo Fields configured to allow HTML displayed the HTML tags as encoded text instead of rendering the formatted content within the block. Fixes: #6718 |
| `18.3` | core | Fixed an issue in the Defined Value picker component where Single-Select Defined Value attributes configured with "Enhanced for Long Lists" did not display the searchable enhanced experience in Obsidian blocks (e.g., Workflow Entry and Even |
| `18.3` | core | Fixed an issue in the Obsidian Location Detail block that allowed a Location to be saved with itself (or a child Location) as its parent. This caused the Location tree to fail when loading nested Locations. Fixes: #6669 |
| `18.3` | core | Fixed an issue in the Obsidian Group Requirement Type Detail block that caused Attribute Values to not load or save correctly when editing a requirement type. This prevented individuals from configuring or updating Group Requirement Types a |
| `18.3` | core | Fixed an issue where the Obsidian Group Attendance Detail Block did not function correctly when Predictive Ids were disabled. The block now correctly resolves the selected group using either the Group Guid or IdKey and prevents an unintende |
| `18.2` | core | Fixed a display issue in the Obsidian Signature Document List block, affecting the Document column. Fixes: #6552 |
| `18.2` | core | Fixed an issue where newly added Obsidian block types could fail to appear in the Page Zone Editor after initial startup. |
| `18.1` | core | Added an Obsidian Communication Detail block with improved message visualization and Communication Recipient insights, allowing administrators to review communication content, delivery status, and recipient activity more efficiently. |
| `18.1` | core | Added an Obsidian Communication List block with enhanced status display and optimized data loading, making it easier for administrators to quickly identify message progress and issues. |
| `18.1` | core | Updated the Obsidian Communication List block to disable custom columns, which are not supported by the high-performance query used by this block. Fixes: #6515 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `3-obsidian-development-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model` | normal | live verification |
| `6-primary-entities-and-relationships` | normal | live verification |
| `7-common-obsidian-development-workflows-build-a-new-core-list-block` | normal | live verification |
| `7-common-obsidian-development-workflows-build-a-detail-block` | normal | live verification |
| `7-common-obsidian-development-workflows-convert-webforms-behavior-to-obsidian` | normal | live verification |
| `7-common-obsidian-development-workflows-troubleshoot-an-existing-obsidian-screen` | normal | live verification |
| `8-blocks-deep-dive-c-block-responsibilities` | normal | live verification |
| `8-blocks-deep-dive-typescript-component-responsibilities` | normal | live verification |
| `8-blocks-deep-dive-block-actions` | normal | live verification |
| `8-blocks-deep-dive-blockcrumbs-and-navigation-context` | normal | live verification |
| `8-blocks-deep-dive-detail-blocks` | normal | live verification |
| `8-blocks-deep-dive-list-blocks` | normal | live verification |
| `8-blocks-deep-dive-person-preferences` | normal | live verification |
| `9-grid-reference-deep-dive-standard-column-properties` | normal | live verification |
| `9-grid-reference-deep-dive-textcolumn` | normal | live verification |
| `9-grid-reference-deep-dive-booleancolumn` | normal | live verification |
| `9-grid-reference-deep-dive-labelcolumn` | normal | live verification |
| `9-grid-reference-deep-dive-highlightdetailcolumn` | normal | live verification |
| `9-grid-reference-deep-dive-personcolumn` | normal | live verification |
| `9-grid-reference-deep-dive-selectcolumn` | normal | live verification |
| `9-grid-reference-deep-dive-reordercolumn` | normal | live verification |
| `9-grid-reference-deep-dive-securitycolumn` | normal | live verification |
| `10-field-types-deep-dive-converting-core-field-types` | normal | live verification |
| `10-field-types-deep-dive-field-type-gallery` | normal | live verification |
| `10-field-types-deep-dive-common-field-type-failure-modes` | normal | live verification |
| `11-development-environment-deep-dive-core-development-setup` | normal | live verification |
| `11-development-environment-deep-dive-vs-code-debugging` | normal | live verification |
| `11-development-environment-deep-dive-plugin-development-setup` | normal | live verification |
| `11-development-environment-deep-dive-build-and-type-checking` | normal | live verification |
| `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-cms` | normal | live verification |
| `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-platform-configuration` | normal | live verification |
| `12-related-rock-areas-developer-resources-api-integrations-security-cms-platform-configuration-workflows-workflows` | normal | live verification |
| `13-administration-and-operational-guardrails-security-first` | structural | live verification |
| `13-administration-and-operational-guardrails-configuration-hygiene` | normal | live verification |
| `13-administration-and-operational-guardrails-admin-ui-expectations` | normal | live verification |
| `15-reporting-analytics-and-model-map-field-types-and-filtering` | normal | live verification |
| `15-reporting-analytics-and-model-map-model-map-use` | citation-only | live verification |
| `15-reporting-analytics-and-model-map-export-caveats` | normal | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-create-a-safe-obsidian-list-block` | normal | live verification |
| `17-implementation-playbooks-playbook-add-a-person-column-correctly` | normal | live verification |
| `17-implementation-playbooks-playbook-add-dynamic-attribute-columns` | normal | live verification |
| `17-implementation-playbooks-playbook-build-a-field-type-edit-component` | normal | live verification |
| `17-implementation-playbooks-playbook-diagnose-a-broken-picker` | normal | live verification |
| `17-implementation-playbooks-playbook-add-browser-bus-interaction` | normal | live verification |
| `17-implementation-playbooks-playbook-cache-repeated-api-calls` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-block-does-not-appear-in-page-zone-editor` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-block-renders-blank` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-save-button-does-nothing` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-save-succeeds-but-data-does-not-change` | structural | live verification |
| `18-troubleshooting-decision-tree-symptom-grid-is-slow` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-grid-sort-duplicates-or-moves-wrong-rows` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-grid-export-fails` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-field-type-displays-raw-json` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-picker-cannot-be-cleared` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-lava-redirect-or-meta-tag-does-not-work` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-security-modal-opens-but-user-cannot-save` | normal | live verification |
| `18-troubleshooting-decision-tree-symptom-works-for-admin-but-not-staff` | structural | live verification |
| `19-agent-task-recipes-recipe-identify-the-source-files-behind-a-visible-obsidian-block` | normal | live verification |
| `19-agent-task-recipes-recipe-determine-whether-a-bug-is-version-related` | normal | live verification |
| `19-agent-task-recipes-recipe-review-an-obsidian-pull-request` | normal | live verification |
| `19-agent-task-recipes-recipe-audit-a-block-for-security` | structural | live verification |
| `19-agent-task-recipes-recipe-audit-a-grid-for-operational-readiness` | structural | live verification |
| `20-source-map-and-dependency-notes` | normal | live verification |
