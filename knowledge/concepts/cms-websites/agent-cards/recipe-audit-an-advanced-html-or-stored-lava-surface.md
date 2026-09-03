---
concept_id: cms-websites
task_id: recipe-audit-an-advanced-html-or-stored-lava-surface
title: Recipe: Audit an Advanced HTML or stored-Lava surface
generated: true
---

# Recipe: Audit an Advanced HTML or stored-Lava surface

Executable CMS content has a known owner, minimum command set, and verified exposure boundary.

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

1. Locate the page, block, scope, and all shared render points.
2. Identify who can view, edit, and administer it.
3. Inventory markup, Lava, stored values, context inputs, and query parameters.
4. Inventory enabled Lava Commands.
5. Remove commands that are not required.
6. Review every entity field emitted by the template.
7. Test cache separation between actors and contexts.
8. Test anonymous and intended-role output.
9. If stored text is processed through Lava, verify its editors and execution context.
10. Stop publication if sensitive output or command authority cannot be bounded. Advanced HTML Block,

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
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/website-fundamentals/seo
