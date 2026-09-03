---
concept_id: platform-configuration
title: Platform Configuration Agent Cheatsheet
generated: true
---

# Platform Configuration Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Add and verify a campus attribute](tasks/recipe-add-and-verify-a-campus-attribute.md) | `Campus`, `Attribute` | `Campus`, `Attribute` |
| [Recipe: Place person attributes on a profile tab](tasks/recipe-place-person-attributes-on-a-profile-tab.md) | `Person`, `Location`, `Block`, `Attribute` | `Person`, `Location`, `Block`, `Attribute` |
| [Recipe: Audit a Defined Value source mismatch](tasks/recipe-audit-a-defined-value-source-mismatch.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Operate seasonal Defined Value options](tasks/recipe-operate-seasonal-defined-value-options.md) | `Workflow`, `Attribute` | `Workflow`, `Attribute` |
| [Recipe: Stage a campus](tasks/recipe-stage-a-campus.md) | `Location`, `Schedule`, `Campus`, `Block`, `Attribute` | `Location`, `Schedule`, `Campus`, `Block`, `Attribute` |
| [Recipe: Move an expensive dashboard calculation to scheduled storage](tasks/recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage.md) | `Schedule` | `Schedule` |
| [Recipe: Secure an embedded BI report](tasks/recipe-secure-an-embedded-bi-report.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Preflight a v19 configuration change](tasks/recipe-preflight-a-v19-configuration-change.md) | `Workflow`, `Block` | `Workflow`, `Block` |
| [Recipe: Design a bounded Rock agent tool](tasks/recipe-design-a-bounded-rock-agent-tool.md) | `Person` | `Person` |
| [Recipe: Plan a Rock upgrade as configuration change](tasks/recipe-plan-a-rock-upgrade-as-configuration-change.md) | `Workflow`, `Page`, `Block`, `Attribute` | `Workflow`, `Page`, `Block`, `Attribute` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DefinedType` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.1` | core | Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729 |
| `17.2` | core | Fixed an issue where the list of attribute categories shown when editing a Content Channel Item attribute from the Content Channel Type Detail block included incorrect or unrelated categories. This made it difficult to assign attributes to  |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `attributes-and-attribute-values-separate-the-definition-from-stored-values` | normal | live verification |
| `attributes-and-attribute-values-present-attributes-intentionally` | normal | live verification |
| `attributes-and-attribute-values-account-for-channel-specific-support` | normal | live verification |
| `defined-types-and-values-defined-value-attributes` | normal | live verification |
| `defined-types-and-values-detect-source-mismatches` | citation-only | live verification |
| `categories-and-entity-types-categories-are-scoped-configuration` | high | live verification |
| `campuses-and-global-settings-campus-configuration` | normal | live verification |
| `campuses-and-global-settings-campus-attributes` | normal | live verification |
| `campuses-and-global-settings-room-capacity-and-schedule-availability` | citation-only | live verification |
| `campuses-and-global-settings-global-attributes-and-system-settings` | normal | live verification |
| `analytics-and-reporting-configuration` | community-supported | live verification |
| `ai-agents-lava-tools-and-extensions` | normal | live verification |
| `cross-domain-version-19-configuration-captcha` | citation-only | live verification |
| `cross-domain-version-19-configuration-check-in` | citation-only | live verification |
| `cross-domain-version-19-configuration-event-registration` | citation-only | live verification |
| `cross-domain-version-19-configuration-communications-and-workflows` | citation-only | live verification |
| `cross-domain-version-19-configuration-person-merge-and-record-provenance` | citation-only | live verification |
| `version-and-authority-caveats` | needs-citation | needs-citation |
| `troubleshooting-decision-tree-an-attribute-exists-but-is-not-visible` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-stores-a-value-but-the-report-shows-the-wrong-label` | citation-only | live verification |
| `troubleshooting-decision-tree-seasonal-options-are-missing-or-still-selectable` | citation-only | live verification |
| `troubleshooting-decision-tree-a-campus-selector-is-absent-or-chooses-a-campus-automatically` | normal | live verification |
| `troubleshooting-decision-tree-a-campus-cannot-use-the-intended-location` | normal | live verification |
| `troubleshooting-decision-tree-check-in-room-capacity-or-availability-is-wrong` | citation-only | live verification |
| `troubleshooting-decision-tree-a-dashboard-is-slow` | community-supported | community-supported |
| `troubleshooting-decision-tree-an-embedded-bi-report-is-inaccessible-or-overexposed` | community-supported | live verification |
| `troubleshooting-decision-tree-the-v19-check-in-manager-roster-does-not-update-live` | citation-only | live verification |
| `troubleshooting-decision-tree-a-v19-registration-rejects-an-apparently-eligible-person` | citation-only | live verification |
| `troubleshooting-decision-tree-an-agent-chooses-the-wrong-tool-or-returns-too-much-data` | citation-only | live verification |
| `agent-task-recipes-recipe-add-and-verify-a-campus-attribute` | normal | live verification |
| `agent-task-recipes-recipe-place-person-attributes-on-a-profile-tab` | normal | live verification |
| `agent-task-recipes-recipe-audit-a-defined-value-source-mismatch` | citation-only | live verification |
| `agent-task-recipes-recipe-operate-seasonal-defined-value-options` | citation-only | live verification |
| `agent-task-recipes-recipe-stage-a-campus` | normal | live verification |
| `agent-task-recipes-recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage` | community-supported | live verification |
| `agent-task-recipes-recipe-secure-an-embedded-bi-report` | community-supported | live verification |
| `agent-task-recipes-recipe-preflight-a-v19-configuration-change` | citation-only | live verification |
| `agent-task-recipes-recipe-design-a-bounded-rock-agent-tool` | citation-only | live verification |
| `agent-task-recipes-recipe-plan-a-rock-upgrade-as-configuration-change` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-reviewed-community-evidence` | community-supported | community-supported |
