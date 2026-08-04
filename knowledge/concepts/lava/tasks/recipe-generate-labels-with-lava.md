---
concept_id: lava
task_id: recipe-generate-labels-with-lava
title: Recipe: Generate Labels With Lava
generated: true
---

# Recipe: Generate Labels With Lava

Source: Print ZPL.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Device`
- `Label`

## Entities And Tables

- `Group`
- `Device`
- `Label`

## Steps

1. Enable `PrintZPL` only in trusted staff contexts.
2. Use `deviceid` for configured Rock devices when possible.
3. Validate ZPL.
4. Avoid duplicate execution.
5. Escape dynamic text.
6. Test printer output physically.

## Do Not Assume

- Avoid duplicate execution.

## Source Links

- https://community.rockrms.com/lava/commands/print-zpl
- https://community.rockrms.com/recipes/386
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupPlacement/PersonFiltersBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupPlacement/personFiltersBag.d.ts
- https://community.rockrms.com/recipes/290
- https://community.rockrms.com/recipes/370
