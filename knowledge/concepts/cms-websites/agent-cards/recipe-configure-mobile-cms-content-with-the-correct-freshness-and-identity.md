---
concept_id: cms-websites
task_id: recipe-configure-mobile-cms-content-with-the-correct-freshness-and-identity
title: Recipe: Configure mobile CMS content with the correct freshness and identity
generated: true
---

# Recipe: Configure mobile CMS content with the correct freshness and identity

Mobile content updates on the intended schedule and uses only context available in its processing mode.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Schedule`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Schedule`
- `Page`
- `Block`

## Steps

1. Decide whether content must be bundled or fetched on page initialization.
2. Enable Dynamic Content when fresh server content is required.
3. Confirm where Lava is processed.
4. Verify available person and context data.
5. Review enabled commands and secure lookups.
6. For static content, deploy a new shell artifact.
7. Test the exact target shell version and authenticated state.
8. Do not publish identity-dependent static Lava that assumes `CurrentPerson`.
9. Determine whether the Content block is static or dynamic.
10. Confirm whether Lava is processed on the server.
11. Inspect enabled commands and context entity.
12. For static content, verify the latest shell deployment.
13. Do not expect `CurrentPerson` in bundled static processing.
14. Test the actual target shell and account state.

## Do Not Assume

- Do not publish identity-dependent static Lava that assumes `CurrentPerson`.
- Do not expect `CurrentPerson` in bundled static processing.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/documentation
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
