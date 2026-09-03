---
concept_id: cms-websites
task_id: recipe-connect-a-page-parameter-filter-to-a-consumer
title: Recipe: Connect a Page Parameter Filter to a consumer
generated: true
---

# Recipe: Connect a Page Parameter Filter to a consumer

One configured key controls the intended redirect, Lava lookup, or listening block consistently.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Choose a stable parameter key.
2. Configure the filter control and its value source.
3. Configure the consumer to use the exact same key.
4. Select virtual-parameter delivery for listening Obsidian blocks or legacy reload for query-string consumers.
5. Configure defaults, redirects, sort, and pagination state.
6. Test first load, filter change, reload, copied URL, and back navigation.
7. Test no-JavaScript behavior when the route requires a usable fallback.
8. Verify that untrusted parameter values cannot expose unauthorized data.
9. Compare the configured filter key with the consumer’s expected key.
10. Determine whether the consumer is an Obsidian listener, legacy block, redirect, or Lava lookup.
11. Inspect legacy reload mode.
12. For virtual parameters, verify the Obsidian block is listening.
13. For query-string consumers, verify the full reload and resulting URL.
14. Check defaults, pagination, sorting, and HTMX include behavior.
15. Test first load, change, refresh, and back navigation.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/documentation
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/intro-to-pages
