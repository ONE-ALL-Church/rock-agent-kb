---
concept_id: apple-tv
title: Apple TV Apps Agent Cheatsheet
generated: true
---

# Apple TV Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Create a minimal Rock Apple TV application](tasks/recipe-create-a-minimal-rock-apple-tv-application.md) | `Page` | `Page` |
| [Recipe: Add a cache-aware TVML page](tasks/recipe-add-a-cache-aware-tvml-page.md) | `Person`, `Page` | `Person`, `Page` |
| [Recipe: Implement remote sign-in](tasks/recipe-implement-remote-sign-in.md) | `Person`, `Device`, `Page`, `Block` | `Person`, `Device`, `Page`, `Block` |
| [Recipe: Add tracked video or audio playback](tasks/recipe-add-tracked-video-or-audio-playback.md) |  |  |
| [Recipe: Build a theme-safe styling pass](tasks/recipe-build-a-theme-safe-styling-pass.md) | `Family`, `Page` | `Family`, `Page` |
| [Recipe: Prepare the application image package](tasks/recipe-prepare-the-application-image-package.md) |  |  |
| [Recipe: Test through demo mode](tasks/recipe-test-through-demo-mode.md) | `Page` | `Page` |
| [Recipe: Review a Lava API before connecting it to Apple TV](tasks/recipe-review-a-lava-api-before-connecting-it-to-apple-tv.md) | `Person` | `Person` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
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
| `creating-and-configuring-an-application` | normal | live verification |
| `pages-lava-and-cache-behavior-page-content-and-merge-fields` | normal | live verification |
| `pages-lava-and-cache-behavior-creating-page-content` | normal | live verification |
| `pages-lava-and-cache-behavior-cacheability` | normal | live verification |
| `sign-in-logout-and-remote-authentication-tv-side-login-flow` | normal | live verification |
| `sign-in-logout-and-remote-authentication-logout-and-navigation-state` | normal | live verification |
| `javascript-and-rock-commands` | normal | live verification |
| `templates-and-rock-specific-controls-choosing-a-tvml-template` | normal | live verification |
| `styling-themes-and-text-tvml-styling-model` | normal | live verification |
| `styling-themes-and-text-light-and-dark-themes` | normal | live verification |
| `application-images-top-shelf-images` | normal | live verification |
| `testing-and-demo-mode` | normal | live verification |
| `lava-apis-and-security` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-the-application-or-start-screen-does-not-load` | normal | live verification |
| `troubleshooting-decision-tree-a-page-is-blank-malformed-or-rejected` | normal | live verification |
| `troubleshooting-decision-tree-login-shows-no-qr-code-or-manual-code` | normal | live verification |
| `troubleshooting-decision-tree-back-navigation-exposes-the-pre-login-or-personalized-page-unexpectedly` | normal | live verification |
| `troubleshooting-decision-tree-video-or-audio-does-not-play` | normal | live verification |
| `troubleshooting-decision-tree-playback-resumes-incorrectly-or-creates-duplicate-interactions` | normal | live verification |
| `troubleshooting-decision-tree-colors-or-badges-disappear-in-one-theme` | normal | live verification |
| `troubleshooting-decision-tree-a-template-change-does-not-appear` | normal | live verification |
| `troubleshooting-decision-tree-demo-commands-do-not-work` | normal | live verification |
| `troubleshooting-decision-tree-a-countdown-immediately-navigates-or-starts-media` | normal | live verification |
| `troubleshooting-decision-tree-a-lava-webhook-exposes-more-data-than-expected` | normal | live verification |
| `agent-task-recipes-recipe-create-a-minimal-rock-apple-tv-application` | normal | live verification |
| `agent-task-recipes-recipe-add-a-cache-aware-tvml-page` | normal | live verification |
| `agent-task-recipes-recipe-implement-remote-sign-in` | normal | live verification |
| `agent-task-recipes-recipe-add-tracked-video-or-audio-playback` | normal | live verification |
| `agent-task-recipes-recipe-build-a-theme-safe-styling-pass` | normal | live verification |
| `agent-task-recipes-recipe-prepare-the-application-image-package` | normal | live verification |
| `agent-task-recipes-recipe-test-through-demo-mode` | normal | live verification |
| `agent-task-recipes-recipe-review-a-lava-api-before-connecting-it-to-apple-tv` | normal | live verification |
| `known-gaps-and-live-verification` | normal | live verification |
| `source-map` | normal | live verification |
