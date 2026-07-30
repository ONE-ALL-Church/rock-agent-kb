---
concept_id: cms-websites
task_id: recipe-can-i-enable-sql-in-this-html-block
title: Recipe: “Can I Enable SQL In This HTML Block?”
generated: true
---

# Recipe: “Can I Enable SQL In This HTML Block?”

Default answer: only after review.

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

1. Page is staff-only or data is public.
2. SQL command is strictly necessary.
3. Query is read-only.
4. Query is bounded.
5. Query does not expose sensitive data.
6. Parameters are constrained.
7. Output is encoded.
8. Block security is locked down.
9. A Dynamic Data/reporting page would not be safer.
10. The enabled command list is minimal.

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
