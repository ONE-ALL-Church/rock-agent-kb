---
concept_id: cms-websites
title: CMS And Websites Quickstart
generated: true
---

# CMS And Websites Quickstart

Pages, blocks, themes, content channels, personalization, media, and website operations.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Publish a page and block safely](tasks/recipe-publish-a-page-and-block-safely.md): A page resolves through the intended site and route and shows only the intended blocks to each visitor class.
- [Recipe: Copy a page hierarchy without carrying stale configuration](tasks/recipe-copy-a-page-hierarchy-without-carrying-stale-configuration.md): A copied hierarchy is structurally complete and its settings point to the intended new or shared resources.
- [Recipe: Audit an Advanced HTML or stored-Lava surface](tasks/recipe-audit-an-advanced-html-or-stored-lava-surface.md): Executable CMS content has a known owner, minimum command set, and verified exposure boundary.
- [Recipe: Change a theme without surprising other sites or pages](tasks/recipe-change-a-theme-without-surprising-other-sites-or-pages.md): The intended site receives the new styling while layouts, zones, and shared blocks remain functional.
- [Recipe: Publish a content-channel list and detail experience](tasks/recipe-publish-a-content-channel-list-and-detail-experience.md): Intended items appear with correct metadata and detail links without exposing restricted information.
- [Recipe: Build and verify personalized content](tasks/recipe-build-and-verify-personalized-content.md): Each target audience receives the intended content while authorization remains independently enforced.
- [Recipe: Connect a Page Parameter Filter to a consumer](tasks/recipe-connect-a-page-parameter-filter-to-a-consumer.md): One configured key controls the intended redirect, Lava lookup, or listening block consistently.
- [Recipe: Build a bounded Helix active-search page](tasks/recipe-build-a-bounded-helix-active-search-page.md): The initial page is useful, HTMX updates only the result region, and authorization is verified for the intended actors.
- [Recipe: Launch a landing page](tasks/recipe-launch-a-landing-page.md): A campaign page has the intended route, content, call to action, metadata, and retirement plan.
- [Recipe: Retire a seasonal public feature](tasks/recipe-retire-a-seasonal-public-feature.md): Expired content can no longer be viewed or submitted through any supported route.
- [Recipe: Publish background-generated video](tasks/recipe-publish-background-generated-video.md): A public page references a completed and readable media output.
- [Recipe: Configure mobile CMS content with the correct freshness and identity](tasks/recipe-configure-mobile-cms-content-with-the-correct-freshness-and-identity.md): Mobile content updates on the intended schedule and uses only context available in its processing mode.

## High-Signal Sections

- `agent-summary` lines 18-31: Agent Summary (normal)
- `mental-model` lines 42-58: Mental Model (normal)
- `sites-routes-and-navigation` lines 59-76: Sites, Routes, And Navigation (normal)
- `pages-layouts-zones-and-blocks` lines 77-90: Pages, Layouts, Zones, And Blocks (normal)
- `html-content-scheduling-and-shared-components` lines 91-104: HTML Content, Scheduling, And Shared Components (normal)
- `advanced-html-lava-and-context` lines 105-126: Advanced HTML, Lava, And Context (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the cms-websites guide.
- `Block`: Rock concept/entity referenced by the cms-websites guide.
- `Campus`: Rock concept/entity referenced by the cms-websites guide.
- `Family`: Rock concept/entity referenced by the cms-websites guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the cms-websites guide.
- `Person`: Rock concept/entity referenced by the cms-websites guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the cms-websites guide.

## Version Caveats

- `17.1`: Fixed an issue in the Content Channel Item View block where breadcrumbs did not function correctly when accessing the page directly via a link rather than navigating through the site. This caused a 'Page Not Found' error
- `16.1`: Fixed issue where editing the block settings on a Dynamic Data block would update the page name of the internal page editor page. Fixes: #5542

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
