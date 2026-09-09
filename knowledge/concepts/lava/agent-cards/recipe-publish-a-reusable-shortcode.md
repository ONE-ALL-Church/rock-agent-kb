---
concept_id: lava
task_id: recipe-publish-a-reusable-shortcode
title: Recipe: Publish a reusable shortcode
generated: true
---

# Recipe: Publish a reusable shortcode

A stable shortcode contract for content authors.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Decide whether the shortcode is inline or block.
2. Choose a unique, descriptive tag name.
3. Define explicit parameters and defaults.
4. Keep enabled commands to the minimum.
5. Document the output and accepted content.
6. Test omitted, valid and malformed parameters.
7. Test anonymous and intended authenticated contexts.
8. Search existing templates before making any type or parameter-breaking change.

## Do Not Assume

- Stored shortcode text will execute automatically.
- A shortcode is safe because its caller is short.
- Changing inline versus block type is backward compatible.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/documentation/digital-publishing/websites/web-design-frameworks/lava-shortcodes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava
- https://community.rockrms.com/lava/shortcodes/the-power-of-shortcode-blocks
- https://community.rockrms.com/lava/shortcodes/types-of-shortcodes
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/Blocks/WebRequestBlock.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeListBox.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/SqlCommand.ascx
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Cms/LavaShortcodeDetail/LavaShortcodeBag.cs
