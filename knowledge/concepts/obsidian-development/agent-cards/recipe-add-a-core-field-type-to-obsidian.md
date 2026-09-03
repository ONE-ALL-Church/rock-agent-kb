---
concept_id: obsidian-development
task_id: recipe-add-a-core-field-type-to-obsidian
title: Recipe: Add A Core Field Type To Obsidian
generated: true
---

# Recipe: Add A Core Field Type To Obsidian

A registered core field type with compatible server and client representations.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Block`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Block`
- `Attribute`

## Steps

1. Declare Obsidian platform support in the C# field type.
2. Expose its GUID through the field-type system GUID definitions and generation process.
3. Create the TypeScript field implementation and components.
4. Import and register the implementation in the field-type index.
5. Define safe public value and configuration representations.
6. Implement conversion back to the private stored representations where required.
7. Ensure formatting functions accept both display and unsaved edit representations.
8. Test equivalent attribute configuration and editing through WebForms and Obsidian blocks.
9. Add an example to the field-type gallery when following the documented core workflow. (Converting Core Field Types)
10. Compare the public display and public edit representations.
11. Pass representative values from both forms through `getTextValue` and related formatting methods.
12. Update those methods to handle either representation.
13. Confirm the conversion back to the private stored representation.
14. Recheck public configuration-key compatibility before changing the contract. (Converting Core Field Types, Creating Field Types)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/creating-field-types/converting-core-field-types
- https://community.rockrms.com/developer/obsidian/browser-bus
- https://community.rockrms.com/developer/obsidian/creating-field-types
