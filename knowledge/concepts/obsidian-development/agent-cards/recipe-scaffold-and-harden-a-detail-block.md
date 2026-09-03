---
concept_id: obsidian-development
task_id: recipe-scaffold-and-harden-a-detail-block
title: Recipe: Scaffold And Harden A Detail Block
generated: true
---

# Recipe: Scaffold And Harden A Detail Block

A standardized detail block with an explicit write boundary.

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

1. Choose entity or CMS security.
2. If replacing an unsecured WebForms block, start with CMS security and review effective page permissions.
3. Generate the core detail block and related view models when the core generator is available.
4. Include properties needed for rendering or UI decisions.
5. Remove UI-only properties from the saveable-property list.
6. Confirm the entity metadata required by the detail component.
7. Build and run the boilerplate before adding custom logic.
8. Test view, edit, unauthorized access, validation failure, and save readback. (Creating Detail Blocks)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/browser-bus
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/AccountEntry/utils.partial.ts
