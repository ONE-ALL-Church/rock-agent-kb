---
concept_id: roku
title: Roku Apps Agent Cheatsheet
generated: true
---

# Roku Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inventory Existing Roku App](tasks/recipe-inventory-existing-roku-app.md) |  |  |
| [Recipe: Review A Roku Page For Safety](tasks/recipe-review-a-roku-page-for-safety.md) |  |  |
| [Recipe: Convert A Static Media List To Dynamic RowList](tasks/recipe-convert-a-static-media-list-to-dynamic-rowlist.md) |  |  |
| [Recipe: Diagnose A Cache Leak](tasks/recipe-diagnose-a-cache-leak.md) |  |  |
| [Recipe: Add A Safe Diagnostic Page](tasks/recipe-add-a-safe-diagnostic-page.md) |  |  |
| [Recipe: Validate Post-Upgrade Roku Behavior](tasks/recipe-validate-post-upgrade-roku-behavior.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | normal | live verification |
| `3-roku-apps-mental-model` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-application-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-page-configuration` | normal | live verification |
| `5-core-configuration-and-data-model-lava-merge-fields` | normal | live verification |
| `6-primary-entities-and-relationships` | normal | live verification |
| `7-common-roku-apps-workflows-build-a-first-app` | normal | live verification |
| `7-common-roku-apps-workflows-add-a-page` | needs-citation | needs-citation |
| `7-common-roku-apps-workflows-build-a-menu` | normal | live verification |
| `7-common-roku-apps-workflows-add-login` | normal | live verification |
| `8-roku-getting-started-deep-dive-provisioning` | normal | live verification |
| `8-roku-getting-started-deep-dive-page-construction` | normal | live verification |
| `8-roku-getting-started-deep-dive-device-validation` | normal | live verification |
| `9-roku-commands-deep-dive-navigation-commands` | normal | live verification |
| `9-roku-commands-deep-dive-media-commands` | normal | live verification |
| `10-roku-controls-deep-dive-rock-page` | normal | live verification |
| `10-roku-controls-deep-dive-rock-button` | normal | live verification |
| `10-roku-controls-deep-dive-rock-focusgroup` | normal | live verification |
| `10-roku-controls-deep-dive-built-in-scenegraph-nodes` | normal | live verification |
| `11-roku-layouts-and-resources-deep-dive-rowlist` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-api-integrations` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-lava` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-cms` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-security` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-media` | normal | live verification |
| `12-related-rock-areas-api-integrations-lava-cms-security-media-tv-apps-tv-apps` | normal | live verification |
| `13-administration-and-operational-guardrails-version-gate` | normal | live verification |
| `13-administration-and-operational-guardrails-environment-separation` | structural | live verification |
| `13-administration-and-operational-guardrails-secret-handling` | structural | live verification |
| `13-administration-and-operational-guardrails-interaction-tracking` | normal | live verification |
| `13-administration-and-operational-guardrails-content-governance` | structural | live verification |
| `15-reporting-analytics-and-model-map` | normal | live verification |
| `16-version-and-release-caveats` | normal | live verification |
| `17-implementation-playbooks-playbook-create-a-minimal-roku-home-page` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-build-a-media-row` | normal | live verification |
| `17-implementation-playbooks-playbook-add-campus-selection` | normal | live verification |
| `17-implementation-playbooks-playbook-add-login` | normal | live verification |
| `17-implementation-playbooks-playbook-tune-caching` | normal | live verification |
| `19-agent-task-recipes-recipe-review-a-roku-page-for-safety` | structural | live verification |
| `19-agent-task-recipes-recipe-convert-a-static-media-list-to-dynamic-rowlist` | structural | live verification |
| `19-agent-task-recipes-recipe-diagnose-a-cache-leak` | structural | live verification |
| `19-agent-task-recipes-recipe-add-a-safe-diagnostic-page` | structural | live verification |
| `19-agent-task-recipes-recipe-validate-post-upgrade-roku-behavior` | structural | live verification |
| `20-source-map-and-dependency-notes-release-notes-and-community-examples` | normal | live verification |
