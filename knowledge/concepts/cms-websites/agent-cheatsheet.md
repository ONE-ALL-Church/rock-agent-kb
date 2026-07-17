---
concept_id: cms-websites
title: CMS And Websites Agent Cheatsheet
generated: true
---

# CMS And Websites Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: “Find The Block That Controls This Text”](tasks/recipe-find-the-block-that-controls-this-text.md) |  |  |
| [Recipe: “Why Is This Content Item Not Public?”](tasks/recipe-why-is-this-content-item-not-public.md) |  |  |
| [Recipe: “Can I Enable SQL In This HTML Block?”](tasks/recipe-can-i-enable-sql-in-this-html-block.md) |  |  |
| [Recipe: “Add A Detail Page For Channel Items”](tasks/recipe-add-a-detail-page-for-channel-items.md) |  |  |
| [Recipe: “Review A Community Recipe Before Installing”](tasks/recipe-review-a-community-recipe-before-installing.md) |  |  |
| [Recipe: “Build A Page View Report”](tasks/recipe-build-a-page-view-report.md) |  |  |
| [Recipe: “Troubleshoot Required Watching”](tasks/recipe-troubleshoot-required-watching.md) |  |  |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Device` | `Location` | Check kiosk/device assignment, physical printer, DPI, and Windows app version where relevant. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `17.1` | core | Fixed an issue in the Content Channel Item View block where breadcrumbs did not function correctly when accessing the page directly via a link rather than navigating through the site. This caused a 'Page Not Found' error when clicking a par |
| `16.1` | core | Fixed issue where editing the block settings on a Dynamic Data block would update the page name of the internal page editor page. Fixes: #5542 |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | citation-only | live verification |
| `2-scope-and-terminology` | normal | live verification |
| `4-source-authority-and-how-to-use-this-guide` | normal | live verification |
| `5-core-configuration-and-data-model-sites` | community-supported | live verification |
| `5-core-configuration-and-data-model-pages` | community-supported | live verification |
| `5-core-configuration-and-data-model-blocks` | normal | live verification |
| `5-core-configuration-and-data-model-layouts-and-zones` | structural | live verification |
| `5-core-configuration-and-data-model-themes` | normal | live verification |
| `5-core-configuration-and-data-model-content-channel-types` | normal | live verification |
| `5-core-configuration-and-data-model-content-channels` | normal | live verification |
| `5-core-configuration-and-data-model-content-channel-items` | normal | live verification |
| `5-core-configuration-and-data-model-media-and-linked-media-elements` | normal | live verification |
| `6-primary-entities-and-relationships-site-to-page` | citation-only | live verification |
| `6-primary-entities-and-relationships-page-to-layout-to-zone-to-block` | structural | live verification |
| `6-primary-entities-and-relationships-page-to-block-settings` | normal | live verification |
| `6-primary-entities-and-relationships-block-to-lava-commands` | normal | live verification |
| `6-primary-entities-and-relationships-content-channel-type-to-channel-to-item` | normal | live verification |
| `6-primary-entities-and-relationships-content-channel-item-to-media` | normal | live verification |
| `6-primary-entities-and-relationships-page-and-content-to-interactions` | normal | live verification |
| `6-primary-entities-and-relationships-files-binary-files-entity-documents-and-security` | normal | live verification |
| `7-common-cms-and-websites-workflows-create-a-new-public-page` | citation-only | live verification |
| `7-common-cms-and-websites-workflows-add-or-edit-an-html-content-block` | citation-only | live verification |
| `7-common-cms-and-websites-workflows-build-a-content-channel-listing-and-detail-flow` | normal | live verification |
| `7-common-cms-and-websites-workflows-publish-media-through-cms` | citation-only | live verification |
| `7-common-cms-and-websites-workflows-add-personalization-to-a-page-or-channel` | normal | live verification |
| `7-common-cms-and-websites-workflows-add-a-search-or-filter-interface-for-pages` | community-supported | community-supported |
| `7-common-cms-and-websites-workflows-build-page-view-reporting` | community-supported | community-supported |
| `8-pages-and-blocks-deep-dive-page-hierarchy-and-navigation` | community-supported | live verification |
| `8-pages-and-blocks-deep-dive-page-parameters` | normal | live verification |
| `8-pages-and-blocks-deep-dive-block-settings` | normal | live verification |
| `8-pages-and-blocks-deep-dive-block-security` | normal | live verification |
| `9-themes-deep-dive-what-themes-control` | citation-only | live verification |
| `9-themes-deep-dive-theme-selection` | structural | live verification |
| `9-themes-deep-dive-icon-systems` | citation-only | live verification |
| `9-themes-deep-dive-javascript-in-cms` | community-supported | community-supported |
| `10-content-channels-deep-dive-dates-and-ordering` | normal | live verification |
| `10-content-channels-deep-dive-categories-and-navigation` | normal | live verification |
| `10-content-channels-deep-dive-content-channel-item-view` | normal | live verification |
| `10-content-channels-deep-dive-content-channel-item-list` | normal | live verification |
| `11-related-rock-areas-lava-security-media-content-personalization-security` | normal | live verification |
| `11-related-rock-areas-lava-security-media-content-personalization-personalization` | normal | live verification |
| `12-administration-and-operational-guardrails-production-change-protocol` | citation-only | live verification |
| `12-administration-and-operational-guardrails-cache-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-shared-content-guardrails` | normal | live verification |
| `12-administration-and-operational-guardrails-community-recipe-guardrails` | community-supported | live verification |
| `12-administration-and-operational-guardrails-upgrade-guardrails` | structural | live verification |
| `13-developer-api-lava-and-source-code-landmarks-rock-source-repository` | normal | live verification |
| `13-developer-api-lava-and-source-code-landmarks-mobile-cms-landmark` | normal | live verification |
| `14-reporting-analytics-and-model-map-page-view-analytics` | community-supported | community-supported |
| `14-reporting-analytics-and-model-map-model-map-usage` | structural | live verification |
| `15-version-and-release-caveats-v19-1-cms-caveat-html-content-shared-deletion` | normal | live verification |
| `15-version-and-release-caveats-v18-2-cms-caveat-content-channel-delete-authorization` | normal | live verification |
| `15-version-and-release-caveats-v18-2-entity-document-caveat` | normal | live verification |
| `15-version-and-release-caveats-icon-version-caveats` | citation-only | live verification |
| `15-version-and-release-caveats-source-branch-caveat` | structural | live verification |
| `16-implementation-playbooks-playbook-diagnose-a-missing-page` | structural | live verification |
| `16-implementation-playbooks-playbook-diagnose-a-block-that-does-not-render` | structural | live verification |
| `16-implementation-playbooks-playbook-safely-modify-advanced-html` | structural | live verification |
| `16-implementation-playbooks-playbook-build-a-content-channel` | citation-only | live verification |
| `16-implementation-playbooks-playbook-audit-a-public-cms-page-for-security` | normal | live verification |
| `16-implementation-playbooks-playbook-add-content-item-analytics` | structural | live verification |
| `16-implementation-playbooks-playbook-troubleshoot-media-required-watching` | structural | live verification |
| `17-troubleshooting-decision-tree-the-page-returns-not-found` | normal | live verification |
| `17-troubleshooting-decision-tree-files-or-documents-are-accessible-to-the-wrong-users` | normal | live verification |
| `18-agent-task-recipes-recipe-find-the-block-that-controls-this-text` | structural | live verification |
| `18-agent-task-recipes-recipe-why-is-this-content-item-not-public` | structural | live verification |
| `18-agent-task-recipes-recipe-can-i-enable-sql-in-this-html-block` | normal | live verification |
| `18-agent-task-recipes-recipe-add-a-detail-page-for-channel-items` | citation-only | live verification |
| `18-agent-task-recipes-recipe-review-a-community-recipe-before-installing` | community-supported | live verification |
| `18-agent-task-recipes-recipe-build-a-page-view-report` | community-supported | live verification |
| `18-agent-task-recipes-recipe-troubleshoot-required-watching` | citation-only | live verification |
| `approved-claim-coverage` | normal | live verification |
| `19-source-map-and-dependency-notes-secondary-and-community-sources` | community-supported | community-supported |
