---
concept_id: apple-tv
task_id: recipe-add-a-cache-aware-tvml-page
title: Recipe: Add a cache-aware TVML page
generated: true
---

# Recipe: Add a cache-aware TVML page

A new page that emits valid TVML and uses an intentional cache policy.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`

## Entities And Tables

- `Person`
- `Page`

## Steps

1. Select the TVML template that most closely matches the journey.
2. Create the page from the intended application.
3. Give it a clear internal name and description.
4. Write TVML using only supported elements for the selected template.
5. Add Lava using documented page merge fields.
6. Render the Lava output with anonymous and signed-in states where relevant.
7. Validate the rendered output as TVML.
8. Choose Public, Private, No-Cache, or No-Store.
9. Add navigation to the page through a documented Rock command.
10. Test focus, Back navigation, Light and Dark themes, and cached reload behavior.

## Do Not Assume

- HTML elements or browser CSS work.
- Template behavior is portable.
- Public caching is appropriate for personalized content.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
