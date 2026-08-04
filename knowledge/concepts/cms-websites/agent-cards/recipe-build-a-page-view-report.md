---
concept_id: cms-websites
task_id: recipe-build-a-page-view-report
title: Recipe: “Build A Page View Report”
generated: true
---

# Recipe: “Build A Page View Report”

The community page-view recipe provides the basic pattern but should be hardened for security and performance (Easy Page Views Reporting).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Confirm site Log Page Views.
2. Create internal reporting page.
3. Restrict View to staff/reporting role.
4. Add filters for page, person, and date range.
5. Add Dynamic Data or report block.
6. Use schema-verified SQL.
7. Add date limits and defaults.
8. Validate against known test views.
9. Document whether anonymous, crawler, and duplicate views are included.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/lava/commands
- https://community.rockrms.com/recipes/261
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelItemView/contentChannelItemViewCustomSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx.cs
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelDetail/contentChannelBag.d.ts
- https://community.rockrms.com/rocku/cms/adding-pages-and-blocks-legacy
- https://community.rockrms.com/rocku/cms/page-builder
- https://community.rockrms.com/rocku/cms/personalization
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Cms/ContentChannelItemPersonalListLava.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/ContentChannelNavigation/contentChannelNavigationBag.d.ts
