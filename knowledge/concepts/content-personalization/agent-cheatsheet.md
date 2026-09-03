---
concept_id: content-personalization
title: Content And Personalization Agent Cheatsheet
generated: true
---

# Content And Personalization Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Publish a governed Content Channel Item](tasks/recipe-publish-a-governed-content-channel-item.md) | `Person`, `Schedule`, `Page`, `Block`, `Attribute` | `Person`, `Schedule`, `Page`, `Block`, `Attribute` |
| [Recipe: Add personalization to Content Channel Items](tasks/recipe-add-personalization-to-content-channel-items.md) | `Person`, `DataView`, `Group`, `Block` | `Person`, `DataView`, `Group`, `Block` |
| [Recipe: Refresh personalization membership](tasks/recipe-refresh-personalization-membership.md) | `Person`, `DataView` | `Person`, `DataView` |
| [Recipe: Build and refresh a Content Collection](tasks/recipe-build-and-refresh-a-content-collection.md) | `Person`, `Block`, `Attribute` | `Person`, `Block`, `Attribute` |
| [Recipe: Configure a Content Component template](tasks/recipe-configure-a-content-component-template.md) | `Block`, `Attribute` | `Block`, `Attribute` |
| [Recipe: Automate a channel item attribute with Lava](tasks/recipe-automate-a-channel-item-attribute-with-lava.md) | `Schedule`, `Page`, `Attribute` | `Schedule`, `Page`, `Attribute` |
| [Recipe: Publish a Media Element through a channel](tasks/recipe-publish-a-media-element-through-a-channel.md) | `Page`, `Attribute` | `Page`, `Attribute` |
| [Recipe: Share or refresh Content Library material](tasks/recipe-share-or-refresh-content-library-material.md) | `Person`, `DataView`, `Location`, `Device`, `Block` | `Person`, `DataView`, `Location`, `Device`, `Block` |
| [Recipe: Configure localized currency display safely](tasks/recipe-configure-localized-currency-display-safely.md) | `Person`, `Label` | `Person`, `Label` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `19.3` | core | Fixed the Content Channel Item List block to show the add and delete options for individuals with Edit access to the content channel, rather than requiring Edit access on the Content Channel Item entity itself. Fixes: #6914 |
| `17.5` | core | Fixed an issue where the Content Channel Item View block and the InteractionContentChannelItemWrite Lava command logged interactions using the Content Channel entity type instead of the Content Channel Item entity type. This caused interact |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | normal | live verification |
| `content-channels-manage-editorial-work` | high | live verification |
| `content-channels-relate-items` | normal | live verification |
| `content-channels-automate-item-attributes` | normal | live verification |
| `social-metadata` | normal | live verification |
| `localization` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-content-item-does-not-appear` | normal | live verification |
| `troubleshooting-decision-tree-content-collection-results-are-stale-or-empty` | normal | live verification |
| `troubleshooting-decision-tree-personalized-content-is-wrong-or-stale` | normal | live verification |
| `troubleshooting-decision-tree-one-visitor-sees-another-visitor-s-personalized-values` | normal | live verification |
| `troubleshooting-decision-tree-an-adaptive-message-adaptation-does-not-display` | normal | live verification |
| `troubleshooting-decision-tree-an-externally-uploaded-asset-is-missing` | normal | live verification |
| `troubleshooting-decision-tree-media-analytics-or-resume-behavior-is-unexpected` | high | live verification |
| `troubleshooting-decision-tree-a-required-media-watch-form-cannot-be-submitted` | normal | live verification |
| `troubleshooting-decision-tree-a-social-share-preview-is-wrong` | normal | live verification |
| `troubleshooting-decision-tree-dates-phone-numbers-currency-or-addresses-appear-incorrectly-localized` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-governed-content-channel-item` | normal | live verification |
| `agent-task-recipes-recipe-add-personalization-to-content-channel-items` | normal | live verification |
| `agent-task-recipes-recipe-refresh-personalization-membership` | normal | live verification |
| `agent-task-recipes-recipe-build-and-refresh-a-content-collection` | normal | live verification |
| `agent-task-recipes-recipe-configure-a-content-component-template` | normal | live verification |
| `agent-task-recipes-recipe-automate-a-channel-item-attribute-with-lava` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-media-element-through-a-channel` | normal | live verification |
| `agent-task-recipes-recipe-configure-localized-currency-display-safely` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
