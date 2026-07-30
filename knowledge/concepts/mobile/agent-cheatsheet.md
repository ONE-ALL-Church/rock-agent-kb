---
concept_id: mobile
title: Rock Mobile Agent Cheatsheet
generated: true
---

# Rock Mobile Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Inventory A Mobile App](tasks/recipe-inventory-a-mobile-app.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Determine Whether A Feature Can Be Used](tasks/recipe-determine-whether-a-feature-can-be-used.md) | `Page` | `Page` |
| [Recipe: Add Analytics To A Tap](tasks/recipe-add-analytics-to-a-tap.md) |  |  |
| [Recipe: Modernize Legacy Platform XAML](tasks/recipe-modernize-legacy-platform-xaml.md) | `Device` | `Device` |
| [Recipe: Review App Store Readiness](tasks/recipe-review-app-store-readiness.md) | `Page` | `Page` |

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
| `1-executive-summary-for-agents` | normal | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `3-rock-mobile-mental-model-deployment-flow` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | community-supported | live verification |
| `5-core-configuration-and-data-model-creating-the-mobile-application` | normal | live verification |
| `5-core-configuration-and-data-model-application-type` | normal | live verification |
| `5-core-configuration-and-data-model-lock-orientation` | normal | live verification |
| `5-core-configuration-and-data-model-application-pages` | normal | live verification |
| `5-core-configuration-and-data-model-api-key` | normal | live verification |
| `5-core-configuration-and-data-model-flyout-xaml` | normal | live verification |
| `5-core-configuration-and-data-model-homepage-routing-logic` | normal | live verification |
| `5-core-configuration-and-data-model-palette-colors-and-styling-values` | normal | live verification |
| `6-primary-entities-and-relationships` | structural | live verification |
| `6-primary-entities-and-relationships-mobile-application-relationship-map` | normal | live verification |
| `6-primary-entities-and-relationships-page-block-and-security-relationships` | normal | live verification |
| `6-primary-entities-and-relationships-check-in-source-code-landmarks` | normal | live verification |
| `7-common-rock-mobile-workflows-build-a-first-app` | normal | live verification |
| `7-common-rock-mobile-workflows-change-a-page-or-block` | structural | live verification |
| `7-common-rock-mobile-workflows-add-a-webview-integration` | normal | live verification |
| `7-common-rock-mobile-workflows-configure-push-notifications` | normal | live verification |
| `7-common-rock-mobile-workflows-upgrade-from-xamarin-forms-to-maui` | normal | live verification |
| `8-commands-deep-dive-command-binding-pattern` | normal | live verification |
| `8-commands-deep-dive-commandreference` | normal | live verification |
| `8-commands-deep-dive-operational-command-troubleshooting` | normal | live verification |
| `9-controls-deep-dive-webview` | normal | live verification |
| `9-controls-deep-dive-context-menu` | normal | live verification |
| `9-controls-deep-dive-ondeviceplatform-and-maui-platform-support` | normal | live verification |
| `9-controls-deep-dive-cards-and-styling` | normal | live verification |
| `9-controls-deep-dive-media-controls` | normal | live verification |
| `10-mobile-releases-deep-dive-release-version-table` | normal | live verification |
| `10-mobile-releases-deep-dive-v7-0` | normal | live verification |
| `10-mobile-releases-deep-dive-v6-0` | normal | live verification |
| `11-related-rock-areas-api-check-in-cms-security-api` | normal | live verification |
| `11-related-rock-areas-api-check-in-cms-security-check-in` | normal | live verification |
| `12-administration-and-operational-guardrails-deployment-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-shell-update-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-app-store-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-android-keystore-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-in-app-giving-guardrails` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-xaml-and-lava` | community-supported | live verification |
| `13-developer-api-lava-and-source-code-landmarks-styling` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-source-code-landmarks` | normal | live verification |
| `14-reporting-analytics-and-model-map-mobile-preferences` | normal | live verification |
| `14-reporting-analytics-and-model-map-communication-reporting` | normal | live verification |
| `14-reporting-analytics-and-model-map-check-in-reporting` | normal | live verification |
| `14-reporting-analytics-and-model-map-model-map` | structural | live verification |
| `16-implementation-playbooks-playbook-add-a-new-native-mobile-page` | structural | live verification |
| `16-implementation-playbooks-playbook-add-a-push-notification-campaign` | normal | live verification |
| `16-implementation-playbooks-playbook-add-in-app-giving` | normal | live verification |
| `16-implementation-playbooks-playbook-prepare-for-shell-update` | structural | live verification |
| `16-implementation-playbooks-playbook-diagnose-change-not-showing` | structural | live verification |
| `16-implementation-playbooks-playbook-diagnose-webview-blank-screen` | normal | live verification |
| `18-agent-task-recipes-recipe-determine-whether-a-feature-can-be-used` | structural | live verification |
| `18-agent-task-recipes-recipe-add-analytics-to-a-tap` | normal | live verification |
| `18-agent-task-recipes-recipe-modernize-legacy-platform-xaml` | normal | live verification |
| `approved-claim-coverage` | normal | live verification |
| `19-source-map-and-dependency-notes-primary-official-mobile-docs` | normal | live verification |
| `19-source-map-and-dependency-notes-community-examples` | community-supported | community-supported |
