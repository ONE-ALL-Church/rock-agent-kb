---
concept_id: lava
task_id: recipe-validate-a-rock-mobile-lava-block
title: Recipe: Validate a Rock Mobile Lava block
generated: true
---

# Recipe: Validate a Rock Mobile Lava block

Correct, fresh and valid mobile output for the supported shells.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`
- `Person`

## Entities And Tables

- `Block`
- `Person`

## Steps

1. Decide whether the content must be dynamic or can be bundled.
2. Confirm local versus server Lava processing.
3. List required merge fields and commands.
4. Check local-shell filter support.
5. Escape every user, title and URL value for its XAML position.
6. Put any required shell-version gate inside the rendered fragment.
7. Test anonymous and authenticated states.
8. Test punctuation-heavy content.
9. Validate both old and new shells when supporting a migration window.
10. Confirm whether a deployment is required for future edits.
11. Check whether the Content block is static or dynamic.
12. Confirm whether Lava runs locally or on the server.
13. Do not expect `CurrentPerson` in bundled static content.
14. Check whether every filter used is supported in the shell.
15. Escape markup-sensitive text and encode URL components.
16. Validate XAML with punctuation-heavy test records.
17. Test the actual shell versions in scope. Mobile Content,

## Do Not Assume

- Do not expect `CurrentPerson` in bundled static content.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Lava/Blocks/WebRequestBlock.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupPlacement/PersonFiltersBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/SqlCommand.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupPlacement/personFiltersBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Lava/Core/Shortcodes/DynamicShortcodeBlock.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Reporting/SqlCommand.ascx
- https://community.rockrms.com/rocku/cms/advanced-html-block
