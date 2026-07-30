---
concept_id: cms-websites
task_id: recipe-find-the-block-that-controls-this-text
title: Recipe: “Find The Block That Controls This Text”
generated: true
---

# Recipe: “Find The Block That Controls This Text”

Complete “Find The Block That Controls This Text” with evidence-backed checks and a verifiable outcome.

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

1. Open the page as staff with block edit controls.
2. Identify visible block names and zones.
3. Search page blocks for HTML Content, Advanced HTML, Content Channel Item View, Dynamic Data, and custom Lava blocks.
4. If content is in a content channel, identify channel and item.
5. If content is in a shared HTML context, identify all linked blocks.
6. Export current content before editing.
7. Make a scoped change.
8. Test as public.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/rocku/cms
- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/261
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/recipes/432
- https://community.rockrms.com/documentation/digital-publishing/websites/manage-pages/block-configuration
- https://community.rockrms.com/documentation/church-management/reporting/reporting-blocks/page-parameter-filter-block
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/lava-item-list
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
