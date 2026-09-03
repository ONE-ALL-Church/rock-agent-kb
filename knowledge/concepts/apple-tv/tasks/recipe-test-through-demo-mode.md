---
concept_id: apple-tv
task_id: recipe-test-through-demo-mode
title: Recipe: Test through demo mode
generated: true
---

# Recipe: Test through demo mode

The community shell loads the intended Rock application configuration for bounded testing.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Verify that the demo-request form and Rock Core application remain available.
2. Request a demo key.
3. Install or open Rock Core on Apple TV.
4. Open the Demo screen.
5. Enter the key.
6. Restart the application.
7. Confirm the loaded application identity.
8. Test page rendering, navigation, themes, authentication, and media separately.
9. Use `clearDemo` when the intended outcome is to restore compiled settings.

## Do Not Assume

- Demo success proves App Store packaging.
- Demo support exists in every compiled shell.
- Clearing settings is reversible without knowing the compiled destination.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/testing-your-app
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/demo-commands
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
