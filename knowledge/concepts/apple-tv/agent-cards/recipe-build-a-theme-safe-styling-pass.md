---
concept_id: apple-tv
task_id: recipe-build-a-theme-safe-styling-pass
title: Recipe: Build a theme-safe styling pass
generated: true
---

# Recipe: Build a theme-safe styling pass

Text, badges, images, and focus states remain legible in both Light and Dark themes.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Family`
- `Page`

## Entities And Tables

- `Family`
- `Page`

## Steps

1. Start with predefined `tv-text-style` values.
2. Add font weight or family only where the design requires it.
3. Add Light and Dark media-query branches.
4. Inspect badge tint and image contrast in each theme.
5. Add text shadows only when necessary.
6. Keep shadow offsets and blur close enough to avoid wrapper clipping.
7. Test system-selected themes.
8. Test any page-level theme override.
9. Test focus and highlighted states with the remote.

## Do Not Assume

- Browser CSS support.
- A native-app reference layout is reproducible in TVML.
- A single theme test is sufficient.
- Keep shadow offsets and blur close enough to avoid wrapper clipping.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
