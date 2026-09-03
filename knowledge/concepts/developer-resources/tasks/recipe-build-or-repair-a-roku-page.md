---
concept_id: developer-resources
task_id: recipe-build-or-repair-a-roku-page
title: Recipe: Build or repair a Roku page
generated: true
---

# Recipe: Build or repair a Roku page

Produce a navigable, correctly cached Lava-driven SceneGraph page.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Page`
- `Person`

## Entities And Tables

- `Group`
- `Page`
- `Person`

## Steps

1. Confirm the Rock version supports Roku.
2. Inspect the target Roku application and page.
3. Place page content beneath an outer `Rock:Page`.
4. Give focusable controls stable IDs.
5. Set a valid initial focus.
6. Add `rockCommand` and only the parameters required by that command.
7. Use a `FocusGroup` for explicit horizontal or vertical focus handling where needed.
8. Choose cacheability based on data sensitivity and freshness.
9. Render with representative merge-field states.
10. Test navigation, login state, playback where applicable, back behavior, and focus on a Roku client.
11. Confirm that the page has an outer `Rock:Page`.
12. Confirm that `initialFocus` names an existing focusable control.
13. Inspect the control’s `rockCommand` and every required command parameter.
14. If commands are chained, verify their comma-separated order.
15. Use a `FocusGroup` where directional focus needs explicit management.
16. Check whether stale personalized or shared cache content is being rendered.
17. Test with the actual Roku client and remote-navigation flow. Roku Page, Roku Commands, and

## Do Not Assume

- “Show in Menu” automatically creates Roku shell navigation.
- Apple TV focus or command behavior transfers to Roku.
- Documentation-backed command chaining has been verified in the target shell. Roku Pages and

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/roku-docs/resources/controls/focus-group
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/timeIntervalBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetPageAvailableAttributes.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.ListBlocks.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
