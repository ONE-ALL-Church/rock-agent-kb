---
concept_id: tv-apps
task_id: recipe-build-a-roku-content-page
title: Recipe: Build a Roku content page
generated: true
---

# Recipe: Build a Roku content page

A Roku page whose rendered SceneGraph loads with deterministic initial focus.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Confirm Rock 16.7 or later and an available Roku development shell.
2. Open the intended Roku application record and review its application settings.
3. Create a page with the required name and cache settings.
4. Render a `Rock:Page` as the outer component.
5. Add one focusable `Rock:Button` with a unique ID.
6. Set `initialFocus` to that ID.
7. Validate the post-Lava SceneGraph.
8. Load the page on the Roku client and test directional focus.
9. Confirm that the page setting is enabled.
10. Inspect the Lava that constructs the menu.
11. Confirm that the page collection and Show in Menu value are actually read by that Lava.
12. Confirm that the resulting SceneGraph contains an actionable menu item.
13. Do not assume the Roku shell creates menus automatically from the setting.

## Do Not Assume

- Show in Menu creates navigation automatically.
- HTML or TVML can be reused as SceneGraph.
- A visible component is focusable.
- Do not assume the Roku shell creates menus automatically from the setting.

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/roku-docs/getting-started/applications
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/styling/media-queries
- https://community.rockrms.com/developer/apple-tv-docs/styling/themes
- https://community.rockrms.com/developer/apple-tv-docs/styling/tv-text-style
- https://community.rockrms.com/developer/roku-docs/commands/navigation
