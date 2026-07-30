---
concept_id: platform-configuration
title: Platform Configuration Agent Cheatsheet
generated: true
---

# Platform Configuration Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Find Available Attributes For An Add Or Update Operation](tasks/recipe-find-available-attributes-for-an-add-or-update-operation.md) | `Attribute` | `Attribute` |
| [Recipe: Explain A Platform Configuration Object To A User](tasks/recipe-explain-a-platform-configuration-object-to-a-user.md) |  |  |
| [Recipe: Safely Answer “Can We Delete This?”](tasks/recipe-safely-answer-can-we-delete-this.md) | `Workflow`, `Block`, `Attribute` | `Workflow`, `Block`, `Attribute` |
| [Recipe: Build A Source-Backed Explanation](tasks/recipe-build-a-source-backed-explanation.md) | `Attribute` | `Attribute` |
| [Recipe: Triage Attribute Security](tasks/recipe-triage-attribute-security.md) | `Block`, `Attribute` | `Block`, `Attribute` |
| [Recipe: Convert A Free-Text Attribute To A Defined Value](tasks/recipe-convert-a-free-text-attribute-to-a-defined-value.md) | `Attribute` | `Attribute` |
| [Recipe: Diagnose Attribute Field Type Mismatch](tasks/recipe-diagnose-attribute-field-type-mismatch.md) | `Workflow`, `Block`, `Attribute` | `Workflow`, `Block`, `Attribute` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DefinedType` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `GroupMember` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupType` | `Group` | Confirm the type takes attendance and supports the intended check-in pattern. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 |
| `17.2` | core | Fixed an issue where the list of attribute categories shown when editing a Content Channel Item attribute from the Content Channel Type Detail block included incorrect or unrelated categories. This made it difficult to assign attributes to  |
| `18.2` | core | Fixed an issue where the Attribute Editor did not correctly save configuration changes when creating an Attribute designed to store other Attributes (e.g., an Attribute of type Attribute). This affected scenarios such as defining filters in |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-platform-configuration-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model-entity-types` | normal | live verification |
| `5-core-configuration-and-data-model-attribute-values` | normal | live verification |
| `5-core-configuration-and-data-model-field-types` | normal | live verification |
| `5-core-configuration-and-data-model-categories` | high | live verification |
| `5-core-configuration-and-data-model-global-attributes-and-system-settings` | normal | live verification |
| `6-primary-entities-and-relationships` | structural | live verification |
| `6-primary-entities-and-relationships-campus-relationship-map` | structural | live verification |
| `7-common-platform-configuration-workflows-add-a-person-attribute` | normal | live verification |
| `7-common-platform-configuration-workflows-add-a-connection-request-attribute` | normal | live verification |
| `7-common-platform-configuration-workflows-configure-a-campus-aware-report` | normal | live verification |
| `7-common-platform-configuration-workflows-add-mobile-site-attributes` | normal | live verification |
| `7-common-platform-configuration-workflows-use-attributes-in-custom-blocks` | normal | live verification |
| `8-attributes-and-attribute-values-deep-dive-attribute-definition-fields` | normal | live verification |
| `8-attributes-and-attribute-values-deep-dive-qualifiers` | normal | live verification |
| `8-attributes-and-attribute-values-deep-dive-raw-values-versus-formatted-values` | normal | live verification |
| `8-attributes-and-attribute-values-deep-dive-attribute-values-in-lava` | normal | live verification |
| `9-defined-types-and-values-deep-dive-defined-type-fields-to-inspect` | normal | live verification |
| `9-defined-types-and-values-deep-dive-defined-value-fields-to-inspect` | normal | live verification |
| `9-defined-types-and-values-deep-dive-categorizing-defined-values` | citation-only | live verification |
| `10-categories-and-entity-types-deep-dive-entity-type-security` | normal | live verification |
| `10-categories-and-entity-types-deep-dive-category-version-caveats` | normal | live verification |
| `11-campuses-and-global-settings-deep-dive-campus-as-context` | citation-only | live verification |
| `11-campuses-and-global-settings-deep-dive-campus-filters-in-reports` | community-supported | live verification |
| `11-campuses-and-global-settings-deep-dive-global-attributes` | normal | live verification |
| `11-campuses-and-global-settings-deep-dive-system-settings` | normal | live verification |
| `12-related-rock-areas-people-groups-workflows-cms-security-data-views-reports-operations-groups` | community-supported | community-supported |
| `12-related-rock-areas-people-groups-workflows-cms-security-data-views-reports-operations-data-views` | structural | live verification |
| `13-administration-and-operational-guardrails-change-management` | structural | live verification |
| `13-administration-and-operational-guardrails-public-exposure` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-field-types-and-field-attributes` | normal | live verification |
| `15-reporting-analytics-and-model-map-reporting-rules` | normal | live verification |
| `16-version-and-release-caveats-rock-v10-3` | normal | live verification |
| `16-version-and-release-caveats-rock-v15-0` | normal | live verification |
| `16-version-and-release-caveats-rock-v17-and-v17-5` | normal | live verification |
| `16-version-and-release-caveats-rock-v19-1` | normal | live verification |
| `17-implementation-playbooks-playbook-audit-an-attribute-before-editing` | structural | live verification |
| `17-implementation-playbooks-playbook-create-a-safe-defined-type` | structural | live verification |
| `17-implementation-playbooks-playbook-replace-a-defined-value` | structural | live verification |
| `17-implementation-playbooks-playbook-diagnose-missing-attribute-in-a-block` | structural | live verification |
| `17-implementation-playbooks-playbook-diagnose-lava-attribute-output` | structural | live verification |
| `17-implementation-playbooks-playbook-build-a-campus-aware-workflow-or-report` | normal | live verification |
| `19-agent-task-recipes-recipe-find-available-attributes-for-an-add-or-update-operation` | normal | live verification |
| `19-agent-task-recipes-recipe-explain-a-platform-configuration-object-to-a-user` | structural | live verification |
| `19-agent-task-recipes-recipe-safely-answer-can-we-delete-this` | structural | live verification |
| `19-agent-task-recipes-recipe-build-a-source-backed-explanation` | normal | live verification |
| `19-agent-task-recipes-recipe-diagnose-attribute-field-type-mismatch` | structural | live verification |
| `approved-claim-coverage` | normal | live verification |
| `20-source-map-and-dependency-notes` | high | live verification |
