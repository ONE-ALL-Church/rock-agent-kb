---
concept_id: cms-websites
task_id: recipe-publish-a-page-and-block-safely
title: Recipe: Publish a page and block safely
generated: true
---

# Recipe: Publish a page and block safely

A page resolves through the intended site and route and shows only the intended blocks to each visitor class.

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

1. Identify the site, parent page, intended route, layout, zone, and block type.
2. Determine page, layout, or site scope before adding the block.
3. Inspect inherited page authorization.
4. Configure block view, edit, and administrative authorization.
5. Configure required parameters, context, content, and caching.
6. Review alternate routes, redirects, short links, and navigation placement.
7. Test anonymously, as the intended authenticated role, and as an administrator.
8. Confirm the final route, visible output, hidden output, and navigation behavior.
9. Verify the edit was made on the block, page, site, theme, or endpoint actually rendering the request.
10. Check page-, layout-, and site-scoped copies of similar blocks.
11. Check approval, versioning, display date range, and exclusive end-date behavior.
12. Check HTML, content-channel, application, and browser caching.
13. For themes, confirm the save compiled Less and inspect the generated CSS plus overrides.
14. For deployed file content, read back the saved artifact or hash.
15. Clear cache only after identifying which cache could retain the old value.
16. If a route edit is stale, compare the installation with the relevant route fix in release notes.

## Do Not Assume

- A friendly route grants access.
- A hidden navigation item secures a page.
- Page security automatically matches block security.
- Administrator success proves public behavior.

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
