---
concept_id: obsidian-development
task_id: recipe-coordinate-same-page-blocks-with-browser-bus
title: Recipe: Coordinate Same-Page Blocks With Browser Bus
generated: true
---

# Recipe: Coordinate Same-Page Blocks With Browser Bus

One block reacts to an event from another block on the same page.

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

1. Obtain a block Browser Bus when the source block identity should be attached automatically.
2. Choose a message name and typed data contract.
3. Subscribe broadly or constrain the subscription by block or block type.
4. Publish after the source operation reaches the state the subscriber needs.
5. Unsubscribe according to the component lifecycle.
6. Test on one page.
7. Verify that no requirement depends on cross-tab or cross-user delivery. (Browser Bus)
8. Measure or inspect the total row count, not only the configured page size.
9. Confirm whether the complete result set is being transferred to the browser.
10. Reduce or constrain the server result set if the business requirement permits.
11. Reassess attribute payloads and other per-row data.
12. Stop when the initial transfer and browser work are acceptable; changing only client page size does not reduce the payload. (Grids)

## Do Not Assume

- Unrelated block instances do not respond when the subscription is scoped.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/blocks
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/browser-bus
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/AccountEntry/utils.partial.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/blockTemplateFieldComponents.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/tsconfig.json
