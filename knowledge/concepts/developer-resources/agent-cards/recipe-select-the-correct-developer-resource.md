---
concept_id: developer-resources
task_id: recipe-select-the-correct-developer-resource
title: Recipe: Select the correct developer resource
generated: true
---

# Recipe: Select the correct developer resource

Route a request to the narrowest applicable Rock development surface.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Block`

## Entities And Tables

- `Workflow`
- `Block`

## Steps

1. Describe the user-visible behavior and where it runs.
2. Identify whether the owner is a block, endpoint, API, workflow, job, mobile shell, TV shell, plugin, theme, or migration.
3. Record the Rock version and any shell or plugin version.
4. Select the corresponding specialist documentation.
5. Require a direct source before asserting implementation details.
6. Record unresolved version or installation dependencies as gaps.

## Do Not Assume

- A feature title proves its behavior.
- A core-development workflow applies to plugins.
- Similar concepts behave the same in web, Mobile, Apple TV, and Roku.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/developer/obsidian
- https://community.rockrms.com/lava/obsidian
- https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes
- https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak
- https://community.rockrms.com/developer
- https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationDetail/lavaApplicationBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaEndpointList/lavaEndpointListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Cms/LavaApplicationList/lavaApplicationListOptionsBag.d.ts
