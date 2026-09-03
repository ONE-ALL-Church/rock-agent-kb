---
concept_id: developer-resources
title: Rock Developer Resources Agent Cheatsheet
generated: true
---

# Rock Developer Resources Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Select the correct developer resource](tasks/recipe-select-the-correct-developer-resource.md) | `Workflow`, `Block` | `Workflow`, `Block` |
| [Recipe: Review an Obsidian block change](tasks/recipe-review-an-obsidian-block-change.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Regenerate artifacts after a model change](tasks/recipe-regenerate-artifacts-after-a-model-change.md) |  |  |
| [Recipe: Review a Helix endpoint before changing it](tasks/recipe-review-a-helix-endpoint-before-changing-it.md) | `Page` | `Page` |
| [Recipe: Validate Rock Mobile compatibility](tasks/recipe-validate-rock-mobile-compatibility.md) | `Device` | `Device` |
| [Recipe: Build or repair a Roku page](tasks/recipe-build-or-repair-a-roku-page.md) | `Group`, `Page`, `Person` | `Group`, `Page`, `Person` |
| [Recipe: Prepare a plugin or theme package](tasks/recipe-prepare-a-plugin-or-theme-package.md) | `Workflow` | `Workflow` |
| [Recipe: Validate a Slingshot migration](tasks/recipe-validate-a-slingshot-migration.md) | `Attendance`, `Workflow` | `Attendance`, `Workflow` |
| [Recipe: Inspect page content with a Rock AI agent](tasks/recipe-inspect-page-content-with-a-rock-ai-agent.md) | `Page`, `Block`, `Attribute` | `Page`, `Block`, `Attribute` |
| [Recipe: Verify a save or Rock-managed file deployment](tasks/recipe-verify-a-save-or-rock-managed-file-deployment.md) | `Block` | `Block` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.2` | core | Fixed an issue that caused the wrong theme type to be displayed after cloning a theme until the Rock server rebooted. Fixes: #6603 |
| `17.1` | core | Added the obsidian Communication Template Detail block for viewing and editing communication templates using the Obsidian UI. This lays the foundation for managing versioned templates with a cleaner interface. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | live verification |
| `mental-model` | normal | live verification |
| `learning-path-quickstart-101-202-and-303` | normal | live verification |
| `developer-codex` | normal | live verification |
| `developer-codex-naming-and-compatibility` | normal | live verification |
| `obsidian-development` | normal | live verification |
| `obsidian-development-plugin-development` | normal | live verification |
| `obsidian-development-replacing-webforms-blocks` | normal | live verification |
| `helix-development-applications-and-endpoints` | normal | live verification |
| `helix-development-content-blocks-and-routing` | community-supported | live verification |
| `helix-development-security-and-data-integrity` | normal | live verification |
| `helix-development-packaging-status-conflict` | normal | live verification |
| `ai-agents` | normal | live verification |
| `rock-mobile-development` | normal | live verification |
| `apple-tv-and-roku-development-apple-tv` | normal | live verification |
| `apple-tv-and-roku-development-roku` | normal | live verification |
| `packaging-plugins-and-themes` | normal | live verification |
| `utility-design-query-branch-and-release-references` | normal | live verification |
| `version-and-authority-caveats` | needs-citation | needs-citation |
| `troubleshooting-decision-tree-a-rest-request-returns-an-authorization-error` | normal | live verification |
| `troubleshooting-decision-tree-an-obsidian-action-works-but-redirect-or-metadata-lava-does-nothing` | normal | live verification |
| `troubleshooting-decision-tree-an-obsidian-block-shows-stale-or-mismatched-generated-types` | normal | live verification |
| `troubleshooting-decision-tree-a-webforms-to-obsidian-replacement-loses-settings` | normal | live verification |
| `troubleshooting-decision-tree-a-helix-request-does-not-update-the-target-content` | normal | live verification |
| `troubleshooting-decision-tree-a-helix-form-submits-or-validates-unpredictably` | normal | live verification |
| `troubleshooting-decision-tree-a-mobile-feature-works-on-one-device-but-not-another` | normal | live verification |
| `troubleshooting-decision-tree-roku-navigation-or-focus-is-broken` | normal | live verification |
| `troubleshooting-decision-tree-slingshot-imported-records-but-downstream-reporting-is-wrong` | normal | live verification |
| `agent-task-recipes-recipe-select-the-correct-developer-resource` | normal | live verification |
| `agent-task-recipes-recipe-review-an-obsidian-block-change` | normal | live verification |
| `agent-task-recipes-recipe-regenerate-artifacts-after-a-model-change` | normal | live verification |
| `agent-task-recipes-recipe-review-a-helix-endpoint-before-changing-it` | normal | live verification |
| `agent-task-recipes-recipe-validate-rock-mobile-compatibility` | normal | live verification |
| `agent-task-recipes-recipe-build-or-repair-a-roku-page` | normal | live verification |
| `agent-task-recipes-recipe-prepare-a-plugin-or-theme-package` | normal | live verification |
| `agent-task-recipes-recipe-validate-a-slingshot-migration` | normal | live verification |
| `agent-task-recipes-recipe-inspect-page-content-with-a-rock-ai-agent` | normal | live verification |
| `agent-task-recipes-recipe-verify-a-save-or-rock-managed-file-deployment` | needs-citation | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
