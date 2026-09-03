---
concept_id: cms-websites
task_id: recipe-change-a-theme-without-surprising-other-sites-or-pages
title: Recipe: Change a theme without surprising other sites or pages
generated: true
---

# Recipe: Change a theme without surprising other sites or pages

The intended site receives the new styling while layouts, zones, and shared blocks remain functional.

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

1. Identify every site using the theme.
2. Copy an upgrade-managed or shared theme before customization.
3. Inventory layout names, zones, layout blocks, site blocks, variables, overrides, and assets.
4. Make the smallest theme or override change.
5. Save and confirm Less compilation.
6. Test representative pages across each layout.
7. Test responsive sizes, interactive controls, accessibility, and staff editing.
8. Verify no unrelated site changed.
9. Retain a recoverable prior theme configuration.
10. Verify the edit was made on the block, page, site, theme, or endpoint actually rendering the request.
11. Check page-, layout-, and site-scoped copies of similar blocks.
12. Check approval, versioning, display date range, and exclusive end-date behavior.
13. Check HTML, content-channel, application, and browser caching.
14. For themes, confirm the save compiled Less and inspect the generated CSS plus overrides.
15. For deployed file content, read back the saved artifact or hash.
16. Clear cache only after identifying which cache could retain the old value.
17. If a route edit is stale, compare the installation with the relevant route fix in release notes.

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
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/themes
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo
