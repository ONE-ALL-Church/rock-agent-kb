---
concept_id: obsidian-development
task_id: recipe-build-a-grid-with-reliable-actions
title: Recipe: Build A Grid With Reliable Actions
generated: true
---

# Recipe: Build A Grid With Reliable Actions

A grid whose filters, exports, and actions operate on the intended rows.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Attribute`

## Entities And Tables

- `Person`
- `Page`
- `Attribute`

## Steps

1. Bound the server query to an acceptable total result size.
2. Build the grid definition and row data.
3. Set a unique key field.
4. Choose typed columns for standard data and a generic `Column` only for custom markup.
5. Configure `hideOnScreen` and `excludeFromExport` independently.
6. Add filters, selection, edit, delete, security, copy, or reorder columns as needed.
7. For asynchronous handlers, return their Promises so controls remain disabled while work is pending.
8. Test row identity after sorting and filtering.
9. Test export behavior separately from on-screen visibility. (Grid, Standard Columns)
10. Measure or inspect the total row count, not only the configured page size.
11. Confirm whether the complete result set is being transferred to the browser.
12. Reduce or constrain the server result set if the business requirement permits.
13. Reassess attribute payloads and other per-row data.
14. Stop when the initial transfer and browser work are acceptable; changing only client page size does not reduce the payload. (Grids)

## Do Not Assume

- Paging reduces data transfer.
- A person link proves access to the destination.
- A hidden column is excluded from export.
- A visual delete confirmation replaces server authorization.

## Source Links

- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://community.rockrms.com/developer/obsidian/grid-reference
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
