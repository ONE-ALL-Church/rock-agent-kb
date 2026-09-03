---
concept_id: lava
task_id: recipe-review-an-existing-lava-surface-safely
title: Recipe: Review an existing Lava surface safely
generated: true
---

# Recipe: Review an existing Lava surface safely

A bounded risk assessment without changing the target.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`

## Steps

1. Identify the page, block, workflow action, endpoint, mobile block or other owner.
2. Record the Rock version, rendering engine and intended audience.
3. Inspect page, block, application and endpoint authorization where applicable.
4. List inputs: merge fields, page parameters, query strings, request body, headers, cookies and stored values.
5. List enabled commands and classify each as read, write, external call, code execution or physical effect.
6. Identify the expected output grammar.
7. Test missing values and the intended identities without enabling additional commands.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/workflows/advanced-workflows/lava-tips-for-workflows
- https://community.rockrms.com/lava/commands/workflow-activate-commands
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content
- https://community.rockrms.com/rocku/cms/advanced-html-block
- https://community.rockrms.com/developer/mobile-docs/essentials/lava
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://community.rockrms.com/developer/apple-tv-docs/building-your-first-app/tv-pages
- https://community.rockrms.com/developer/helix/overview
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Reporting/PageParameterFilter/updateFiltersResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaShortcodeDetail/lavaShortcodeBag.d.ts
