---
concept_id: tv-apps
title: TV Apps Agent Cheatsheet
generated: true
---

# TV Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Create an Apple TV application skeleton](tasks/recipe-create-an-apple-tv-application-skeleton.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Build a Roku content page](tasks/recipe-build-a-roku-content-page.md) | `Page` | `Page` |
| [Recipe: Add Roku navigation with application context](tasks/recipe-add-roku-navigation-with-application-context.md) | `Person`, `Page` | `Person`, `Page` |
| [Recipe: Configure remote TV sign-in](tasks/recipe-configure-remote-tv-sign-in.md) | `Person`, `Device`, `Page`, `Block`, `Label` | `Person`, `Device`, `Page`, `Block`, `Label` |
| [Recipe: Add tracked media playback with resume](tasks/recipe-add-tracked-media-playback-with-resume.md) |  |  |
| [Recipe: Make an Apple TV page theme-aware](tasks/recipe-make-an-apple-tv-page-theme-aware.md) | `Page` | `Page` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | normal | live verification |
| `mental-model` | normal | live verification |
| `apple-tv-application-configuration` | normal | live verification |
| `apple-tv-pages-and-lava-output` | normal | live verification |
| `apple-tv-commands` | normal | live verification |
| `roku-application-configuration` | normal | live verification |
| `security-and-authentication-remote-authentication-architecture` | normal | live verification |
| `security-and-authentication-source-code-observation` | normal | live verification |
| `security-and-authentication-api-and-webhook-boundary` | normal | live verification |
| `styling-and-controls-roku-controls-focus-and-layout` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-the-tv-application-administration-feature-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-a-page-is-blank-rejected-or-never-appears` | normal | live verification |
| `troubleshooting-decision-tree-a-roku-page-marked-show-in-menu-is-absent` | normal | live verification |
| `troubleshooting-decision-tree-roku-focus-does-not-move-or-starts-on-the-wrong-item` | normal | live verification |
| `troubleshooting-decision-tree-a-command-does-nothing` | normal | live verification |
| `troubleshooting-decision-tree-remote-sign-in-shows-no-qr-code-or-code` | normal | live verification |
| `troubleshooting-decision-tree-a-remote-authentication-code-is-rejected` | normal | live verification |
| `troubleshooting-decision-tree-media-does-not-start` | normal | live verification |
| `troubleshooting-decision-tree-playback-starts-at-the-wrong-position-or-creates-a-new-interaction` | normal | live verification |
| `troubleshooting-decision-tree-a-page-shows-stale-or-another-context-s-content` | normal | live verification |
| `agent-task-recipes-recipe-create-an-apple-tv-application-skeleton` | normal | live verification |
| `agent-task-recipes-recipe-build-a-roku-content-page` | normal | live verification |
| `agent-task-recipes-recipe-add-roku-navigation-with-application-context` | normal | live verification |
| `agent-task-recipes-recipe-configure-remote-tv-sign-in` | normal | live verification |
| `agent-task-recipes-recipe-add-tracked-media-playback-with-resume` | normal | live verification |
| `agent-task-recipes-recipe-make-an-apple-tv-page-theme-aware` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
