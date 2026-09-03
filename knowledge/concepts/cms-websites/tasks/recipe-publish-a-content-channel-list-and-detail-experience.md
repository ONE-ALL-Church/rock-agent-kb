---
concept_id: cms-websites
task_id: recipe-publish-a-content-channel-list-and-detail-experience
title: Recipe: Publish a content-channel list and detail experience
generated: true
---

# Recipe: Publish a content-channel list and detail experience

Intended items appear with correct metadata and detail links without exposing restricted information.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Identify the channel, items, statuses, dates, attributes, media, and personalization settings.
2. Configure the list block’s channel, filters, Lava template, and detail page.
3. Configure the detail route and required item parameter.
4. Inspect page and block authorization on list and detail pages.
5. Review every field exposed in cards, lists, attributes, and links.
6. Test missing, expired, future, targeted, and unauthorized items.
7. Test direct detail links as well as navigation from the list.
8. Confirm anonymous, intended-role, and administrator behavior separately.
9. Confirm the channel and item.
10. Check item status, dates, attributes, and personalization.
11. Inspect the list block’s channel, filters, Lava template, and detail-page settings.
12. Inspect the page, route, context parameters, and block security.
13. Review what the list exposes even when the detail view is restricted.
14. Check for duplicate attribute keys if the item list fails to load on an affected version.
15. If direct-link breadcrumbs fail on an older installation, compare against the v17.1 fix.
16. Test list and detail routes independently. Content Channel View,

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/set-up-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-layouts
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/page-load-time
- https://community.rockrms.com/documentation/digital-publishing/websites/landing-pages/sample-landing-pages
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/html-block-context
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/documentation
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/documentation/digital-publishing/websites/block-context/context-on-the-person-profile
- https://community.rockrms.com/rocku/content-channels/content-channel-view
- https://www.rockrms.com/releasenotes
