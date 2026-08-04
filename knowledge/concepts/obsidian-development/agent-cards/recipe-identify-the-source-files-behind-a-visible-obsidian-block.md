---
concept_id: obsidian-development
task_id: recipe-identify-the-source-files-behind-a-visible-obsidian-block
title: Recipe: Identify The Source Files Behind A Visible Obsidian Block
generated: true
---

# Recipe: Identify The Source Files Behind A Visible Obsidian Block

Start from the live block type and follow the conventions documented in the Obsidian developer documentation and Grid Columns. Confirm paths against the exact source revision because core, generated view-model, and plugin layouts can differ by version.

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

1. Record page URL, block name, and visible UI text.
2. In Rock admin, inspect the page's block instance and Block Type.
3. Record C# block class, category, and component path.
4. Find the C# block under `Rock.Blocks` or plugin block path.
5. Find the `.obs` component under `Rock.JavaScript.Obsidian.Blocks/src/...` or plugin Obsidian path.
6. Find generated view model bags referenced by imports.
7. Inspect block actions.
8. Inspect block attributes and custom actions.
9. Compare target version with release notes.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/rockfieldcolumn
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/null-vs-undefined
