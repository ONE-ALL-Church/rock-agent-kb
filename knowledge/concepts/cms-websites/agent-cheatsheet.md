---
concept_id: cms-websites
title: CMS And Websites Agent Cheatsheet
generated: true
---

# CMS And Websites Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Publish a page and block safely](tasks/recipe-publish-a-page-and-block-safely.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Copy a page hierarchy without carrying stale configuration](tasks/recipe-copy-a-page-hierarchy-without-carrying-stale-configuration.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Audit an Advanced HTML or stored-Lava surface](tasks/recipe-audit-an-advanced-html-or-stored-lava-surface.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Change a theme without surprising other sites or pages](tasks/recipe-change-a-theme-without-surprising-other-sites-or-pages.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Publish a content-channel list and detail experience](tasks/recipe-publish-a-content-channel-list-and-detail-experience.md) | `Person`, `Page`, `Block`, `Attribute` | `Person`, `Page`, `Block`, `Attribute` |
| [Recipe: Build and verify personalized content](tasks/recipe-build-and-verify-personalized-content.md) | `Person`, `Page`, `Block`, `Group`, `Campus` | `Person`, `Page`, `Block`, `Group`, `Campus` |
| [Recipe: Connect a Page Parameter Filter to a consumer](tasks/recipe-connect-a-page-parameter-filter-to-a-consumer.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Build a bounded Helix active-search page](tasks/recipe-build-a-bounded-helix-active-search-page.md) | `Page`, `Block` | `Page`, `Block` |
| [Recipe: Launch a landing page](tasks/recipe-launch-a-landing-page.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Retire a seasonal public feature](tasks/recipe-retire-a-seasonal-public-feature.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Publish background-generated video](tasks/recipe-publish-background-generated-video.md) | `Workflow`, `Page`, `Block` | `Workflow`, `Page`, `Block` |
| [Recipe: Configure mobile CMS content with the correct freshness and identity](tasks/recipe-configure-mobile-cms-content-with-the-correct-freshness-and-identity.md) | `Person`, `Schedule`, `Page`, `Block` | `Person`, `Schedule`, `Page`, `Block` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.1` | core | Fixed an issue in the Content Channel Item View block where breadcrumbs did not function correctly when accessing the page directly via a link rather than navigating through the site. This caused a 'Page Not Found' error when clicking a par |
| `16.1` | core | Fixed issue where editing the block settings on a Dynamic Data block would update the page name of the internal page editor page. Fixes: #5542 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `scope-and-boundaries` | needs-citation | needs-citation |
| `sites-routes-and-navigation` | normal | live verification |
| `pages-layouts-zones-and-blocks` | normal | live verification |
| `advanced-html-lava-and-context` | normal | live verification |
| `personalization` | citation-only | live verification |
| `content-channels-and-media-presentation` | normal | live verification |
| `page-parameters-filters-and-short-links` | community-supported | live verification |
| `obsidian-helix-htmx-and-forms` | normal | live verification |
| `mobile-content-boundary` | normal | live verification |
| `version-and-authority-caveats` | normal | live verification |
| `troubleshooting-decision-tree-a-page-is-missing-or-visible-to-the-wrong-visitor` | normal | live verification |
| `troubleshooting-decision-tree-a-saved-page-block-route-or-style-change-does-not-appear` | normal | live verification |
| `troubleshooting-decision-tree-the-wrong-personalized-or-contextual-content-appears` | normal | live verification |
| `troubleshooting-decision-tree-a-content-channel-item-is-missing-duplicated-or-exposed` | normal | live verification |
| `troubleshooting-decision-tree-a-page-parameter-filter-does-not-update-its-consumer` | community-supported | live verification |
| `troubleshooting-decision-tree-a-helix-endpoint-works-for-an-administrator-but-fails-for-the-intended-visitor` | community-supported | live verification |
| `troubleshooting-decision-tree-an-htmx-result-is-correct-but-its-controls-assets-or-metadata-are-wrong` | structural | live verification |
| `troubleshooting-decision-tree-a-page-is-slow` | normal | live verification |
| `troubleshooting-decision-tree-a-web-form-fails-validation-nests-incorrectly-or-receives-bot-submissions` | normal | live verification |
| `troubleshooting-decision-tree-mobile-content-is-stale-or-lacks-currentperson` | normal | live verification |
| `troubleshooting-decision-tree-a-generated-short-link-is-blank-or-uses-the-wrong-options` | community-supported | live verification |
| `troubleshooting-decision-tree-background-generated-media-is-linked-before-it-is-ready` | citation-only | live verification |
| `agent-task-recipes-recipe-publish-a-page-and-block-safely` | normal | live verification |
| `agent-task-recipes-recipe-copy-a-page-hierarchy-without-carrying-stale-configuration` | normal | live verification |
| `agent-task-recipes-recipe-audit-an-advanced-html-or-stored-lava-surface` | normal | live verification |
| `agent-task-recipes-recipe-change-a-theme-without-surprising-other-sites-or-pages` | normal | live verification |
| `agent-task-recipes-recipe-publish-a-content-channel-list-and-detail-experience` | citation-only | live verification |
| `agent-task-recipes-recipe-build-and-verify-personalized-content` | citation-only | live verification |
| `agent-task-recipes-recipe-connect-a-page-parameter-filter-to-a-consumer` | community-supported | live verification |
| `agent-task-recipes-recipe-build-a-bounded-helix-active-search-page` | community-supported | live verification |
| `agent-task-recipes-recipe-launch-a-landing-page` | normal | live verification |
| `agent-task-recipes-recipe-retire-a-seasonal-public-feature` | needs-citation | live verification |
| `agent-task-recipes-recipe-publish-background-generated-video` | community-supported | live verification |
| `agent-task-recipes-recipe-configure-mobile-cms-content-with-the-correct-freshness-and-identity` | normal | live verification |
| `known-gaps-and-live-verification` | needs-citation | needs-citation |
