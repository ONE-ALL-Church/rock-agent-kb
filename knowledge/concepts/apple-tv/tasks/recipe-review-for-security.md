---
concept_id: apple-tv
task_id: recipe-review-for-security
title: Recipe: Review For Security
generated: true
---

# Recipe: Review For Security

Complete Review For Security with evidence-backed checks and a verifiable outcome.

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

1. Identify API key and owner.
2. List pages using `CurrentPerson`.
3. List pages using Lava entity commands or APIs.
4. Inspect page cacheability.
5. Inspect command cache controls.
6. Inspect Remote Authentication block route.
7. Inspect remote session REST access if enabled.
8. Confirm no secrets in TVML.
9. Confirm no private data in public pages.
10. Confirm retention settings.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/navigation-commands
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/media-commands
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://community.rockrms.com/developer/apple-tv-docs/styling/getting-started
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/catalog-template
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/div-template
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates/product-template
