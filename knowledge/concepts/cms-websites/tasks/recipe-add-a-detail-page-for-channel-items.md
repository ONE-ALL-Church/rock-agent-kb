---
concept_id: cms-websites
task_id: recipe-add-a-detail-page-for-channel-items
title: Recipe: “Add A Detail Page For Channel Items”
generated: true
---

# Recipe: “Add A Detail Page For Channel Items”

Complete “Add A Detail Page For Channel Items” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Create detail page.
2. Add Content Channel Item View.
3. Configure content channel.
4. Configure query parameter.
5. Configure allowed statuses.
6. Configure Lava template.
7. Configure cache duration and tags.
8. Configure page title update.
9. Configure meta description/image fields if available.
10. Configure interaction logging if needed.
11. Link list page’s detail page setting to this page.
12. Test direct URL and list navigation.
13. Test invalid item ID/key.
14. Test future/pending/expired items.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/261
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/page-builder
- https://community.rockrms.com/recipes/432
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts
- https://community.rockrms.com/rocku/cms/short-links
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
