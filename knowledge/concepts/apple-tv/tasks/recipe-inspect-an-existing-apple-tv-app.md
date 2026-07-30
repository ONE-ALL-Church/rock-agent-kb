---
concept_id: apple-tv
task_id: recipe-inspect-an-existing-apple-tv-app
title: Recipe: Inspect An Existing Apple TV App
generated: true
---

# Recipe: Inspect An Existing Apple TV App

Complete Inspect An Existing Apple TV App with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Device`
- `Page`

## Entities And Tables

- `Person`
- `Device`
- `Page`

## Steps

1. Open Apple TV app detail in Rock.
2. Record name, description, API key identity, page views, retention, app styles, login page.
3. List all TV pages and GUIDs.
4. Open Start Screen.
5. Render and validate TVML.
6. Search for `rockCommand`.
7. Map every command to a target page, media action, context action, or personal action.
8. Identify pages using `CurrentPerson`, `Context`, `PageParameter`, or `DeviceData`.
9. Identify public vs personalized pages.
10. Report risks and unknowns.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs
- https://community.rockrms.com/developer/apple-tv-docs/javascript
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
