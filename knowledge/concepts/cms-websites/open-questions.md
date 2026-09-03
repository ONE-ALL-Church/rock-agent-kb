---
concept_id: cms-websites
title: CMS And Websites Open Questions
generated: true
---

# CMS And Websites Open Questions

This file is for human reviewers and future agents. It lists guide areas where source confidence, live-instance verification, or citation coverage should be improved.

## Needs Citation

- `scope-and-boundaries`: Scope And Boundaries (175 words)
- `agent-task-recipes-recipe-retire-a-seasonal-public-feature`: Recipe: Retire a seasonal public feature (100 words)
- `known-gaps-and-live-verification`: Known Gaps And Live Verification (252 words)

## Community-Supported Only

- `page-parameters-filters-and-short-links`: Page Parameters, Filters, And Short Links
- `troubleshooting-decision-tree-a-page-parameter-filter-does-not-update-its-consumer`: A Page Parameter Filter does not update its consumer
- `troubleshooting-decision-tree-a-helix-endpoint-works-for-an-administrator-but-fails-for-the-intended-visitor`: A Helix endpoint works for an administrator but fails for the intended visitor
- `troubleshooting-decision-tree-a-generated-short-link-is-blank-or-uses-the-wrong-options`: A generated short link is blank or uses the wrong options
- `agent-task-recipes-recipe-connect-a-page-parameter-filter-to-a-consumer`: Recipe: Connect a Page Parameter Filter to a consumer
- `agent-task-recipes-recipe-build-a-bounded-helix-active-search-page`: Recipe: Build a bounded Helix active-search page
- `agent-task-recipes-recipe-publish-background-generated-video`: Recipe: Publish background-generated video

## Needs Live Verification

- `agent-summary`: Agent Summary
- `sites-routes-and-navigation`: Sites, Routes, And Navigation
- `pages-layouts-zones-and-blocks`: Pages, Layouts, Zones, And Blocks
- `advanced-html-lava-and-context`: Advanced HTML, Lava, And Context
- `personalization`: Personalization
- `content-channels-and-media-presentation`: Content Channels And Media Presentation
- `page-parameters-filters-and-short-links`: Page Parameters, Filters, And Short Links
- `obsidian-helix-htmx-and-forms`: Obsidian, Helix, HTMX, And Forms
- `mobile-content-boundary`: Mobile Content Boundary
- `version-and-authority-caveats`: Version And Authority Caveats
- `troubleshooting-decision-tree-a-page-is-missing-or-visible-to-the-wrong-visitor`: A page is missing or visible to the wrong visitor
- `troubleshooting-decision-tree-a-saved-page-block-route-or-style-change-does-not-appear`: A saved page, block, route, or style change does not appear
- `troubleshooting-decision-tree-the-wrong-personalized-or-contextual-content-appears`: The wrong personalized or contextual content appears
- `troubleshooting-decision-tree-a-content-channel-item-is-missing-duplicated-or-exposed`: A content-channel item is missing, duplicated, or exposed
- `troubleshooting-decision-tree-a-page-parameter-filter-does-not-update-its-consumer`: A Page Parameter Filter does not update its consumer
- `troubleshooting-decision-tree-a-helix-endpoint-works-for-an-administrator-but-fails-for-the-intended-visitor`: A Helix endpoint works for an administrator but fails for the intended visitor
- `troubleshooting-decision-tree-an-htmx-result-is-correct-but-its-controls-assets-or-metadata-are-wrong`: An HTMX result is correct but its controls, assets, or metadata are wrong
- `troubleshooting-decision-tree-a-page-is-slow`: A page is slow
- `troubleshooting-decision-tree-a-web-form-fails-validation-nests-incorrectly-or-receives-bot-submissions`: A web form fails validation, nests incorrectly, or receives bot submissions
- `troubleshooting-decision-tree-mobile-content-is-stale-or-lacks-currentperson`: Mobile content is stale or lacks `CurrentPerson`
- `troubleshooting-decision-tree-a-generated-short-link-is-blank-or-uses-the-wrong-options`: A generated short link is blank or uses the wrong options
- `troubleshooting-decision-tree-background-generated-media-is-linked-before-it-is-ready`: Background-generated media is linked before it is ready
- `agent-task-recipes-recipe-publish-a-page-and-block-safely`: Recipe: Publish a page and block safely
- `agent-task-recipes-recipe-copy-a-page-hierarchy-without-carrying-stale-configuration`: Recipe: Copy a page hierarchy without carrying stale configuration
- `agent-task-recipes-recipe-audit-an-advanced-html-or-stored-lava-surface`: Recipe: Audit an Advanced HTML or stored-Lava surface
- `agent-task-recipes-recipe-change-a-theme-without-surprising-other-sites-or-pages`: Recipe: Change a theme without surprising other sites or pages
- `agent-task-recipes-recipe-publish-a-content-channel-list-and-detail-experience`: Recipe: Publish a content-channel list and detail experience
- `agent-task-recipes-recipe-build-and-verify-personalized-content`: Recipe: Build and verify personalized content
- `agent-task-recipes-recipe-connect-a-page-parameter-filter-to-a-consumer`: Recipe: Connect a Page Parameter Filter to a consumer
- `agent-task-recipes-recipe-build-a-bounded-helix-active-search-page`: Recipe: Build a bounded Helix active-search page
- `agent-task-recipes-recipe-launch-a-landing-page`: Recipe: Launch a landing page
- `agent-task-recipes-recipe-retire-a-seasonal-public-feature`: Recipe: Retire a seasonal public feature
- `agent-task-recipes-recipe-publish-background-generated-video`: Recipe: Publish background-generated video
- `agent-task-recipes-recipe-configure-mobile-cms-content-with-the-correct-freshness-and-identity`: Recipe: Configure mobile CMS content with the correct freshness and identity

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
