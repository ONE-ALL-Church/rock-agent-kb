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
| `7.0` | mobile | Fixed an issue where the ShowPopUp command displayed the popup on a white screen instead of overlaying the triggering page when running in MAUI. Fixes: #38 |
| `7.0` | mobile | Added the ExecuteCommand control, enabling command execution with configurable timing and repetition. |
| `4.0` | mobile | Added a custom ScrollView control that allows you to disable the native iOS bounce when scrolling. |
| `2.1` | mobile | Fixed bug that prevented Flyout Shell from working properly if ListItem was not the root XAML element. |
| `2.0` | mobile | Fixed bug in iOS that prevented a person from choosing the "Save..." option during a ShareFile command. |
| `6.0` | mobile | Updated all of the mobile blocks to follow the new design system. |
| `7.0` | mobile | Added the CopyToClipboard command, allowing text to be copied to the clipboard. |
| `7.0` | mobile | Fixed an issue that caused the AddEventToCalendar command to not function properly. |
| `7.0` | mobile | Fixed an issue where the TextColor property of the Tag control was not being respected. |
| `7.0` | mobile | Added the EventToCommandBehavior, which triggers a command when a specified event occurs. |
| `7.0` | mobile | Fixed an issue where the FollowHyperlinks property on the Rock:Html control was not functioning properly. Fixes: #46 |
| `7.0` | mobile | Fixed an issue where the scheduled location was not recorded when an individual self-scheduled through the mobile Group Schedule Signup block. |
| `7.0` | mobile | Added the AllowsPictureInPicturePlayback property to the MediaPlayer control, allowing PiP playback to be enabled or disabled. |
| `4.0` | mobile | Added responsive Memo fields, specifically seen in mobile workflows. |
| `4.0` | mobile | Added a ReloadPage command, used to reload the current page. |
| `4.0` | mobile | Added Toast functionality, used by the ShowToast command. |
| `4.0` | mobile | Added the ability to save specific, mobile-related user preferences. |
| `4.0` | mobile | Fixed a bug in which being in dark mode on iOS caused the BibleBrowser picker to display white text on a white background. |
| `3.0` | mobile | Added new Mobile Connection blocks for managing Connection Requests (requires Rock Server v13.0). |
| `3.0` | mobile | Added new Add To Group mobile block that handles prompting individual for information in order to add them to a group. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | live verification |
| `application-configuration-and-deployment` | normal | live verification |
| `content-xaml-and-lava-dynamic-versus-static-content` | normal | live verification |
| `content-xaml-and-lava-escaping-xaml-producing-lava` | normal | live verification |
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
| `troubleshooting-decision-tree-one-record-causes-a-xaml-page-to-fail` | normal | live verification |
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
