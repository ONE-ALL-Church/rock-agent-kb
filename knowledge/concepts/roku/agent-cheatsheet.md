---
concept_id: roku
title: Roku Apps Agent Cheatsheet
generated: true
---

# Roku Apps Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Prepare A Roku Development Readiness Review](tasks/recipe-prepare-a-roku-development-readiness-review.md) | `Page` | `Page` |
| [Recipe: Author A Focusable Roku Page Skeleton](tasks/recipe-author-a-focusable-roku-page-skeleton.md) | `Group`, `Device`, `Page` | `Group`, `Device`, `Page` |
| [Recipe: Build And Validate A Navigation Action](tasks/recipe-build-and-validate-a-navigation-action.md) | `Page` | `Page` |
| [Recipe: Add Campus Or Other Application Context](tasks/recipe-add-campus-or-other-application-context.md) | `Page` | `Page` |
| [Recipe: Configure A Remote Login Journey](tasks/recipe-configure-a-remote-login-journey.md) | `Person`, `Label`, `Page` | `Person`, `Label`, `Page` |
| [Recipe: Configure Resumable Media Playback](tasks/recipe-configure-resumable-media-playback.md) |  |  |
| [Recipe: Review A Roku-Related Lava Endpoint](tasks/recipe-review-a-roku-related-lava-endpoint.md) | `Page` | `Page` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `getting-started-and-application-configuration` | normal | live verification |
| `page-authoring-and-caching` | normal | live verification |
| `roku-command-model` | normal | live verification |
| `application-context-commands` | normal | live verification |
| `remote-authentication-and-personal-commands` | normal | live verification |
| `media-playback-and-watch-progress` | normal | live verification |
| `layout-nodes-and-rowlist` | normal | live verification |
| `security-and-api-guardrails` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-the-roku-application-cannot-connect-to-rock` | normal | live verification |
| `troubleshooting-decision-tree-a-page-is-blank-or-does-not-render-as-expected` | normal | live verification |
| `troubleshooting-decision-tree-selecting-a-button-or-content-item-does-nothing` | normal | live verification |
| `troubleshooting-decision-tree-back-navigation-returns-to-the-wrong-screen` | normal | live verification |
| `troubleshooting-decision-tree-personalized-content-is-stale-or-appears-for-the-wrong-person` | normal | live verification |
| `troubleshooting-decision-tree-the-qr-login-flow-does-not-complete` | normal | live verification |
| `troubleshooting-decision-tree-video-or-audio-does-not-play` | normal | live verification |
| `troubleshooting-decision-tree-playback-resumes-but-creates-a-new-interaction` | normal | live verification |
| `troubleshooting-decision-tree-a-rowlist-has-no-rows-or-items` | normal | live verification |
| `agent-task-recipes-recipe-prepare-a-roku-development-readiness-review` | normal | live verification |
| `agent-task-recipes-recipe-author-a-focusable-roku-page-skeleton` | normal | live verification |
| `agent-task-recipes-recipe-build-and-validate-a-navigation-action` | normal | live verification |
| `agent-task-recipes-recipe-add-campus-or-other-application-context` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-remote-login-journey` | normal | live verification |
| `agent-task-recipes-recipe-configure-resumable-media-playback` | normal | live verification |
| `agent-task-recipes-recipe-review-a-roku-related-lava-endpoint` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
