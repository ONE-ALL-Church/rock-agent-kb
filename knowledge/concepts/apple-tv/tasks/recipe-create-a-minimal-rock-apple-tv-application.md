---
concept_id: apple-tv
task_id: recipe-create-a-minimal-rock-apple-tv-application
title: Recipe: Create a minimal Rock Apple TV application
generated: true
---

# Recipe: Create a minimal Rock Apple TV application

A Rock-managed application with a valid Start Screen and documented baseline settings.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Confirm Rock 14 or later.
2. Open `Admin Tools > CMS Configuration > Apple TV Apps`.
3. Create the application record with an internal name and description.
4. Review Application Styles, Enable Page Views, API Key, Page View Retention Period, and Authentication Page.
5. Save the record.
6. Open the generated Start Screen.
7. Add a minimal supported TVML template.
8. Render any Lava and validate the final TVML.
9. Select cacheability from the page’s sensitivity and freshness requirements.
10. Test through the exact target or demo shell.

## Do Not Assume

- The Rock name is the App Store name.
- The API key secures a Lava webhook.
- A saved template is valid after Lava renders.
- A preview proves production-shell behavior.

## Source Links

- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/adding-content
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/templates
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tips
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-a-sign-in-page
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/creating-an-app
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageList/appleTvPageListOptionsBag.d.ts
