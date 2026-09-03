---
concept_id: mobile
title: Rock Mobile Agent Cheatsheet
generated: true
---

# Rock Mobile Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Create and test a minimal mobile application](tasks/recipe-create-and-test-a-minimal-mobile-application.md) | `Device`, `Page`, `Block` | `Device`, `Page`, `Block` |
| [Recipe: Build personalized Content block output safely](tasks/recipe-build-personalized-content-block-output-safely.md) | `Person`, `Page`, `Block` | `Person`, `Page`, `Block` |
| [Recipe: Add a command-driven interaction](tasks/recipe-add-a-command-driven-interaction.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Migrate a page from Shell v5 to v6+](tasks/recipe-migrate-a-page-from-shell-v5-to-v6.md) | `Page` | `Page` |
| [Recipe: Prepare mobile check-in](tasks/recipe-prepare-mobile-check-in.md) | `Attendance`, `Group`, `Location`, `Schedule`, `Campus`, `Device`, `Check-in Configuration`, `Label`, `Family` | `Attendance`, `Group`, `Location`, `Schedule`, `Campus`, `Device`, `Check-in Configuration`, `Label`, `Family` |
| [Recipe: Prepare an App Factory publication](tasks/recipe-prepare-an-app-factory-publication.md) | `Device`, `Workflow` | `Device`, `Workflow` |
| [Recipe: Validate push notifications](tasks/recipe-validate-push-notifications.md) | `Device`, `Page` | `Device`, `Page` |
| [Recipe: Orchestrate slow media or content work](tasks/recipe-orchestrate-slow-media-or-content-work.md) | `Workflow`, `Person`, `Page`, `Block` | `Workflow`, `Person`, `Page`, `Block` |
| [Recipe: Validate Outreach Toolbox for ministry use](tasks/recipe-validate-outreach-toolbox-for-ministry-use.md) | `Device`, `Workflow`, `Page`, `Block`, `Schedule` | `Device`, `Workflow`, `Page`, `Block`, `Schedule` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
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
| `19.1` | mobile | Fixed external links silently failing on Android when the address belonged to a site that also has an installed app handler (for example, opening a YouTube link on a device with the YouTube app installed). The link now falls back to the dev |
| `19.1` | mobile | Fixed Android media playback so audio from other apps now lowers in volume when Rock Mobile starts playing audio. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | live verification |
| `application-configuration-and-deployment` | normal | live verification |
| `content-xaml-and-lava-dynamic-versus-static-content` | normal | live verification |
| `content-xaml-and-lava-escaping-xaml-producing-lava` | community-supported | live verification |
| `controls-context-menus` | normal | live verification |
| `controls-borders-and-migration-era-controls` | normal | live verification |
| `mobile-check-in-prerequisites-and-configuration` | normal | live verification |
| `mobile-engagement-and-background-work` | citation-only | live verification |
| `outreach-toolbox` | citation-only | live verification |
| `push-notifications` | normal | live verification |
| `app-publishing-android-signing` | normal | live verification |
| `mobile-releases-xamarin-forms-to-net-maui` | normal | live verification |
| `version-and-authority-caveats` | needs-citation | needs-citation |
| `troubleshooting-decision-tree-changes-do-not-appear-in-the-app` | normal | live verification |
| `troubleshooting-decision-tree-the-app-crashes-immediately-after-opening` | normal | live verification |
| `troubleshooting-decision-tree-personalized-content-is-blank-or-anonymous` | normal | live verification |
| `troubleshooting-decision-tree-one-record-causes-a-xaml-page-to-fail` | community-supported | live verification |
| `troubleshooting-decision-tree-a-command-does-nothing` | normal | live verification |
| `troubleshooting-decision-tree-a-page-layout-breaks-after-moving-to-shell-v6` | normal | live verification |
| `troubleshooting-decision-tree-a-context-menu-works-differently-on-android` | normal | live verification |
| `troubleshooting-decision-tree-push-notifications-are-not-arriving` | normal | live verification |
| `troubleshooting-decision-tree-mobile-check-in-cannot-find-a-kiosk` | citation-only | live verification |
| `troubleshooting-decision-tree-mobile-check-in-finds-a-kiosk-but-says-no-service-is-available` | citation-only | live verification |
| `troubleshooting-decision-tree-check-in-completes-but-labels-do-not-print` | citation-only | live verification |
| `troubleshooting-decision-tree-the-app-is-unavailable-on-newer-android-devices` | normal | live verification |
| `troubleshooting-decision-tree-outreach-toolbox-is-missing-or-reminders-do-not-fire` | citation-only | live verification |
| `agent-task-recipes-recipe-create-and-test-a-minimal-mobile-application` | normal | live verification |
| `agent-task-recipes-recipe-build-personalized-content-block-output-safely` | normal | live verification |
| `agent-task-recipes-recipe-add-a-command-driven-interaction` | normal | live verification |
| `agent-task-recipes-recipe-migrate-a-page-from-shell-v5-to-v6` | normal | live verification |
| `agent-task-recipes-recipe-prepare-mobile-check-in` | citation-only | live verification |
| `agent-task-recipes-recipe-prepare-an-app-factory-publication` | normal | live verification |
| `agent-task-recipes-recipe-validate-push-notifications` | normal | live verification |
| `agent-task-recipes-recipe-orchestrate-slow-media-or-content-work` | citation-only | live verification |
| `agent-task-recipes-recipe-validate-outreach-toolbox-for-ministry-use` | citation-only | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
| `source-map-official-rock-mobile-documentation` | normal | live verification |
