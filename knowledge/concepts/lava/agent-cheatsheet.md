---
concept_id: lava
title: Lava Agent Cheatsheet
generated: true
---

# Lava Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Review an existing Lava surface safely](tasks/recipe-review-an-existing-lava-surface-safely.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Build a bounded read-only entity view](tasks/recipe-build-a-bounded-read-only-entity-view.md) | `DataView` | `DataView` |
| [Recipe: Prepare a Lava entity write](tasks/recipe-prepare-a-lava-entity-write.md) | `Attribute` | `Attribute` |
| [Recipe: Preflight a workflow activation](tasks/recipe-preflight-a-workflow-activation.md) | `Person`, `PersonAlias`, `Workflow`, `Attribute` | `Person`, `PersonAlias`, `Workflow`, `Attribute` |
| [Recipe: Publish a reusable shortcode](tasks/recipe-publish-a-reusable-shortcode.md) | `Block` | `Block` |
| [Recipe: Build a read-only Helix active-search page](tasks/recipe-build-a-read-only-helix-active-search-page.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Validate a Rock Mobile Lava block](tasks/recipe-validate-a-rock-mobile-lava-block.md) | `Block`, `Person` | `Block`, `Person` |
| [Recipe: Design a Lava-backed AI tool](tasks/recipe-design-a-lava-backed-ai-tool.md) | `Person` | `Person` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `PersonAlias` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | needs-citation |
| `core-syntax-and-engine` | normal | live verification |
| `core-syntax-and-engine-fluid-and-dotliquid` | normal | live verification |
| `filters-text-and-output-encoding` | community-supported | live verification |
| `filters-dates-and-time-zones` | normal | live verification |
| `filters-where-and-short-link-caveats` | community-supported | live verification |
| `commands` | community-supported | live verification |
| `commands-entity-retrieval` | normal | live verification |
| `commands-workflow-activation` | community-supported | live verification |
| `shortcodes` | high | live verification |
| `execution-contexts-and-output-contracts-advanced-html-and-communications` | normal | live verification |
| `execution-contexts-and-output-contracts-rock-mobile` | normal | live verification |
| `execution-contexts-and-output-contracts-tv-applications` | normal | live verification |
| `remote-lava-and-apis` | normal | live verification |
| `helix-and-lava-applications` | normal | live verification |
| `workflows-and-lava` | normal | live verification |
| `reporting-and-persisted-results` | community-supported | community-supported |
| `lava-backed-ai-tools` | citation-only | live verification |
| `troubleshooting-decision-tree-lava-renders-blank-or-a-merge-field-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-a-parser-error-points-at-an-innocent-looking-line` | normal | live verification |
| `troubleshooting-decision-tree-an-entity-command-returns-no-rows-or-fails-before-iteration` | community-supported | live verification |
| `troubleshooting-decision-tree-a-modify-command-appears-to-succeed-but-data-is-unchanged` | normal | live verification |
| `troubleshooting-decision-tree-a-later-write-fails-with-an-earlier-validation-error` | normal | live verification |
| `troubleshooting-decision-tree-a-workflow-starts-but-submitted-values-are-missing` | community-supported | live verification |
| `troubleshooting-decision-tree-a-shortcode-displays-as-raw-text` | normal | live verification |
| `troubleshooting-decision-tree-a-helix-endpoint-works-for-administrators-but-not-its-audience` | community-supported | live verification |
| `troubleshooting-decision-tree-an-htmx-fragment-loses-scripts-styles-or-ui-state` | normal | live verification |
| `troubleshooting-decision-tree-rock-mobile-content-is-stale-anonymous-or-invalid-xaml` | normal | live verification |
| `troubleshooting-decision-tree-a-remote-lava-route-exposes-more-than-intended` | normal | live verification |
| `agent-task-recipes-recipe-review-an-existing-lava-surface-safely` | community-supported | live verification |
| `agent-task-recipes-recipe-build-a-bounded-read-only-entity-view` | normal | live verification |
| `agent-task-recipes-recipe-preflight-a-workflow-activation` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-reusable-shortcode` | normal | live verification |
| `agent-task-recipes-recipe-build-a-read-only-helix-active-search-page` | normal | live verification |
| `agent-task-recipes-recipe-validate-a-rock-mobile-lava-block` | normal | live verification |
| `agent-task-recipes-recipe-design-a-lava-backed-ai-tool` | citation-only | live verification |
| `known-gaps-and-live-verification` | community-supported | live verification |
| `source-map-immutable-implementation-evidence` | normal | live verification |
| `source-map-reviewed-community-patterns` | community-supported | community-supported |
