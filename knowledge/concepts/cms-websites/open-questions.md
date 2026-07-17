---
concept_id: cms-websites
title: CMS And Websites Open Questions
generated: true
---

# CMS And Websites Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation


## Community-Supported Only

- `5-core-configuration-and-data-model-sites`: Sites
- `5-core-configuration-and-data-model-pages`: Pages
- `7-common-cms-and-websites-workflows-add-a-search-or-filter-interface-for-pages`: Add A Search Or Filter Interface For Pages
- `7-common-cms-and-websites-workflows-build-page-view-reporting`: Build Page View Reporting
- `8-pages-and-blocks-deep-dive-page-hierarchy-and-navigation`: Page Hierarchy And Navigation
- `9-themes-deep-dive-javascript-in-cms`: JavaScript In CMS
- `12-administration-and-operational-guardrails-community-recipe-guardrails`: Community Recipe Guardrails
- `14-reporting-analytics-and-model-map-page-view-analytics`: Page View Analytics
- `18-agent-task-recipes-recipe-review-a-community-recipe-before-installing`: Recipe: “Review A Community Recipe Before Installing”
- `18-agent-task-recipes-recipe-build-a-page-view-report`: Recipe: “Build A Page View Report”
- `19-source-map-and-dependency-notes-secondary-and-community-sources`: Secondary And Community Sources

## Needs Live Verification

- `generated-model-map-pointers`: Generated Model Map Pointers
- `1-executive-summary-for-agents`: 1. Executive Summary For Agents
- `2-scope-and-terminology`: 2. Scope And Terminology
- `4-source-authority-and-how-to-use-this-guide`: 4. Source Authority And How To Use This Guide
- `5-core-configuration-and-data-model-sites`: Sites
- `5-core-configuration-and-data-model-pages`: Pages
- `5-core-configuration-and-data-model-blocks`: Blocks
- `5-core-configuration-and-data-model-layouts-and-zones`: Layouts And Zones
- `5-core-configuration-and-data-model-themes`: Themes
- `5-core-configuration-and-data-model-content-channel-types`: Content Channel Types
- `5-core-configuration-and-data-model-content-channels`: Content Channels
- `5-core-configuration-and-data-model-content-channel-items`: Content Channel Items
- `5-core-configuration-and-data-model-media-and-linked-media-elements`: Media And Linked Media Elements
- `6-primary-entities-and-relationships-site-to-page`: Site To Page
- `6-primary-entities-and-relationships-page-to-layout-to-zone-to-block`: Page To Layout To Zone To Block
- `6-primary-entities-and-relationships-page-to-block-settings`: Page To Block Settings
- `6-primary-entities-and-relationships-block-to-lava-commands`: Block To Lava Commands
- `6-primary-entities-and-relationships-content-channel-type-to-channel-to-item`: Content Channel Type To Channel To Item
- `6-primary-entities-and-relationships-content-channel-item-to-media`: Content Channel Item To Media
- `6-primary-entities-and-relationships-page-and-content-to-interactions`: Page And Content To Interactions
- `6-primary-entities-and-relationships-files-binary-files-entity-documents-and-security`: Files, Binary Files, Entity Documents, And Security
- `7-common-cms-and-websites-workflows-create-a-new-public-page`: Create A New Public Page
- `7-common-cms-and-websites-workflows-add-or-edit-an-html-content-block`: Add Or Edit An HTML Content Block
- `7-common-cms-and-websites-workflows-build-a-content-channel-listing-and-detail-flow`: Build A Content Channel Listing And Detail Flow
- `7-common-cms-and-websites-workflows-publish-media-through-cms`: Publish Media Through CMS
- `7-common-cms-and-websites-workflows-add-personalization-to-a-page-or-channel`: Add Personalization To A Page Or Channel
- `8-pages-and-blocks-deep-dive-page-hierarchy-and-navigation`: Page Hierarchy And Navigation
- `8-pages-and-blocks-deep-dive-page-parameters`: Page Parameters
- `8-pages-and-blocks-deep-dive-block-settings`: Block Settings
- `8-pages-and-blocks-deep-dive-block-security`: Block Security
- `9-themes-deep-dive-what-themes-control`: What Themes Control
- `9-themes-deep-dive-theme-selection`: Theme Selection
- `9-themes-deep-dive-icon-systems`: Icon Systems
- `10-content-channels-deep-dive-dates-and-ordering`: Dates And Ordering
- `10-content-channels-deep-dive-categories-and-navigation`: Categories And Navigation
- `10-content-channels-deep-dive-content-channel-item-view`: Content Channel Item View
- `10-content-channels-deep-dive-content-channel-item-list`: Content Channel Item List
- `11-related-rock-areas-lava-security-media-content-personalization-security`: Security
- `11-related-rock-areas-lava-security-media-content-personalization-personalization`: Personalization
- `12-administration-and-operational-guardrails-production-change-protocol`: Production Change Protocol

## Live Verification Clarification

Read-only SQL can verify the current state of exact live objects named by a user, but it does not globally close every section listed above. Keep a section in this list until the answer names a specific page, block, workflow type, data view, report, group, route, or other configured record and verifies that record live.

Schema corrections from the 2026-06-07 read-only production/source pass:

- `DataView` does not have an `IsActive` column; use persisted/run fields and the root `DataViewFilter` relationship instead.
- `Workflow.Status` is text, not a numeric enum; use exact status strings such as `Active` or `Completed`.
- `ReportField` ordering uses `ColumnOrder` and `Id`, not `[Order]`.
- `GroupType` does not have an `IsActive` column; inspect attendance, purpose, scheduling, and location/schedule requirement fields.
- `Page` does not have a `Route` column in this schema; join `PageRoute` when route data is needed.
- There is no dedicated `Webhook` table in this schema; inspect Lava endpoints, REST routes, workflow launch paths, jobs, attributes, blocks, and source code.
- `RockMigration` is not present; confirm the installed Rock version in the application/system information and use SQL migration history only as database migration context.

Detailed live-verification evidence is retained in internal review notes and is intentionally excluded from the public export. Public guidance should cite official docs, source code, release notes, approved claims, or public community examples; live-instance checks should be rerun against the exact instance and object being discussed.
