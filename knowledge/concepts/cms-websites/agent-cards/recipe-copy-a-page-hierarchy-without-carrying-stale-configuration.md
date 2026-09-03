---
concept_id: cms-websites
task_id: recipe-copy-a-page-hierarchy-without-carrying-stale-configuration
title: Recipe: Copy a page hierarchy without carrying stale configuration
generated: true
---

# Recipe: Copy a page hierarchy without carrying stale configuration

A copied hierarchy is structurally complete and its settings point to the intended new or shared resources.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`

## Steps

1. Record the source page, descendants, blocks, routes, and external dependencies.
2. Copy the page with child pages only when the full hierarchy is intended.
3. Confirm Rock created the expected pages and blocks.
4. Review rewired references among the copies.
5. Review content channels, workflows, detail pages, parameters, routes, block scope, and security.
6. Remove or replace copied campaign content and dates.
7. Test every entry route and important child route.
8. Publish only after confirming no copied setting points to an unintended live resource.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/documentation
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/intro-to-pages
