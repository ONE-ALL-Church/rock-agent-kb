---
concept_id: developer-resources
task_id: recipe-review-an-obsidian-block-change
title: Recipe: Review an Obsidian block change
generated: true
---

# Recipe: Review an Obsidian block change

Identify and validate all layers affected by an Obsidian block change.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Page`
- `Block`
- `Attribute`

## Steps

1. Inspect the C# block and its permissions and server logic.
2. Inspect the TypeScript component and UI state.
3. Identify the relevant block actions and their request/response contracts.
4. Inspect block settings and decide whether entity or CMS security owns access.
5. Check for Lava behavior that depends on a full-page response.
6. Rebuild the server and client projects.
7. Test initial load, each changed action, validation, authorization, and persisted readback.
8. Confirm the model change is present.
9. Build Rock and inspect the DLL selected by the code generator.
10. Run model generation.
11. Add any new C# files to the projects.
12. Build Rock and the view-model project.
13. Preview Obsidian view-model generation.
14. Investigate unexpected files before saving.
15. Rebuild and retest the block.

## Do Not Assume

- A successful action response proves persistence.
- A legacy Lava redirect will work after an asynchronous block action. Creating Obsidian Blocks and

## Source Links

- https://community.rockrms.com/developer/roku-docs/getting-started/pages
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.ListBlocks.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Jobs/PostUpdateDataMigrationsReplaceWebFormsBlocksWithObsidianBlocks.cs
- https://community.rockrms.com/developer/obsidian
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://community.rockrms.com/lava/obsidian
- https://community.rockrms.com/developer/roku-docs
- https://community.rockrms.com/developer/developer-codex/coding-standards/code-generator/model-changes
- https://community.rockrms.com/developer/roku-docs/resources/controls/page
- https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak
- https://community.rockrms.com/developer/developer-codex/coding-standards/obsidian-chop-swap-sneak/process-to-chop-or-swap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Tv/AppleTvPageDetail/appleTvPageBag.d.ts
