---
concept_id: helix
title: Helix Agent Cheatsheet
generated: true
---

# Helix Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inspect an existing Helix application before changing it](tasks/recipe-inspect-an-existing-helix-application-before-changing-it.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Build a read-only HTMX result fragment](tasks/recipe-build-a-read-only-htmx-result-fragment.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Build a validated mutation form](tasks/recipe-build-a-validated-mutation-form.md) |  |  |
| [Recipe: Render endpoint content on first paint](tasks/recipe-render-endpoint-content-on-first-paint.md) | `Page` | `Page` |
| [Recipe: Validate a rendered Helix dashboard](tasks/recipe-validate-a-rendered-helix-dashboard.md) | `Label`, `Page`, `Block` | `Label`, `Page`, `Block` |
| [Recipe: Decide whether to replace a Lava Application](tasks/recipe-decide-whether-to-replace-a-lava-application.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added Helix support for Lava Applications to core. This provides a great new way to build interactive pages in Rock powered by Lava for more advanced administrators. |
| `19.1` | core | Added Body and RawBody merge fields to Lava Applications. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `htmx` | normal | live verification |
| `lava-applications` | normal | live verification |
| `lava-applications-editing-with-magnus` | normal | live verification |
| `lava-endpoints` | normal | live verification |
| `lava-endpoints-security-modes` | normal | live verification |
| `lava-endpoints-request-merge-fields` | normal | live verification |
| `lava-endpoints-enabled-commands-and-endpoint-responses` | normal | live verification |
| `forms-and-controls-control-shortcodes` | normal | live verification |
| `forms-and-controls-loading-indicators` | normal | live verification |
| `security-and-observability-endpoint-security-review` | normal | live verification |
| `strategies-and-limitations-reviewed-community-patterns` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-an-htmx-action-does-nothing-or-updates-the-wrong-region` | normal | live verification |
| `troubleshooting-decision-tree-the-endpoint-returns-not-found-or-the-wrong-handler-runs` | normal | live verification |
| `troubleshooting-decision-tree-a-user-is-denied-while-an-administrator-succeeds` | normal | live verification |
| `troubleshooting-decision-tree-body-or-rawbody-is-empty-or-unavailable` | normal | live verification |
| `troubleshooting-decision-tree-a-loading-spinner-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-endpoint-injected-styles-or-scripts-do-not-load` | normal | live verification |
| `troubleshooting-decision-tree-an-endpoint-is-slow-or-makes-excessive-database-calls` | normal | live verification |
| `troubleshooting-decision-tree-sorting-or-filtering-resets-after-refresh` | normal | live verification |
| `agent-task-recipes-recipe-inspect-an-existing-helix-application-before-changing-it` | normal | live verification |
| `agent-task-recipes-recipe-build-a-read-only-htmx-result-fragment` | normal | live verification |
| `agent-task-recipes-recipe-build-a-validated-mutation-form` | normal | live verification |
| `agent-task-recipes-recipe-validate-a-rendered-helix-dashboard` | community-supported | live verification |
| `agent-task-recipes-recipe-decide-whether-to-replace-a-lava-application` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
| `source-map-community-examples` | community-supported | community-supported |
