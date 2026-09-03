---
concept_id: cms-websites
task_id: recipe-retire-a-seasonal-public-feature
title: Recipe: Retire a seasonal public feature
generated: true
---

# Recipe: Retire a seasonal public feature

Expired content can no longer be viewed or submitted through any supported route.

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

1. Inventory public routes, short links, redirects, blocks, alternate pages, mobile surfaces, and underlying filters.
2. Identify date flags, Lava conditions, workflow or registration state, and block authorization.
3. Disable or expire the owning feature using its supported configuration.
4. Verify page and block exposure independently.
5. Test direct URLs, old shared links, alternate routes, and mobile entry points.
6. Confirm submissions or actions are rejected as intended.
7. Verify replacement messaging or redirects.
8. Stop only after the public and authenticated paths are both retested.

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
