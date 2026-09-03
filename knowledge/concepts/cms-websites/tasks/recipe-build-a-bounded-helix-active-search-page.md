---
concept_id: cms-websites
task_id: recipe-build-a-bounded-helix-active-search-page
title: Recipe: Build a bounded Helix active-search page
generated: true
---

# Recipe: Build a bounded Helix active-search page

The initial page is useful, HTMX updates only the result region, and authorization is verified for the intended actors.

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

1. Put the shell, form, loading indicator, target container, and first render in the Lava Application Content block.
2. Use the caret route for application endpoint calls.
3. Make the endpoint return only inner result markup.
4. Pass filters, pagination, sort, and direction through one server-side contract.
5. Keep the endpoint query bounded.
6. Validate application, page, block, and endpoint authorization.
7. Enable only required Lava Commands and apply CSRF protection to state changes.
8. Put scripts, shared styles, and crawl-critical metadata in the host response.
9. Test anonymous, intended-role, administrator, no-JavaScript, refresh, and back-button behavior.
10. Read back deployed content before declaring the change live.

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
