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

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/261
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/page-builder
- https://community.rockrms.com/lava/commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts
- https://community.rockrms.com/rocku/cms/tabler-icons
- https://community.rockrms.com/rocku/cms/font-awesome-5-1
