---
concept_id: obsidian-development
task_id: recipe-add-a-custom-block-settings-screen
title: Recipe: Add A Custom Block Settings Screen
generated: true
---

# Recipe: Add A Custom Block Settings Screen

An administrate-only `.obs` settings interface backed by block actions.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Implement `IHasCustomActions`.
2. Return the custom action only when the caller can administrate the block.
3. Point its component URL to the dedicated `.obs` settings template.
4. Add a block action to load the current settings and required options.
5. Add a block action to validate and save changes.
6. Recheck administration authorization inside the save action.
7. Reload the settings independently after saving. (Implementing IHasCustomActions)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/browser-bus
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/AccountEntry/utils.partial.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/blockTemplateFieldComponents.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/tsconfig.json
