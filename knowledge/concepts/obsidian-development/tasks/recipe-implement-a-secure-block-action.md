---
concept_id: obsidian-development
task_id: recipe-implement-a-secure-block-action
title: Recipe: Implement A Secure Block Action
generated: true
---

# Recipe: Implement A Secure Block Action

A server action that accepts client data without trusting client state.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Block`

## Entities And Tables

- `Person`
- `Block`

## Steps

1. Define a typed request and response contract.
2. Validate required values and identifier formats.
3. Load the authoritative entity in the action.
4. Evaluate the current person’s authorization for the exact operation.
5. Apply business rules and persist the change.
6. Return a structured result.
7. Invoke the action from TypeScript and handle both success and failure.
8. Verify the result through a fresh read when persistence is material. (Creating Blocks)
9. Confirm the server action checks the current person’s ordinary authorization.
10. If a child control needs delegated access, confirm the block created and provided a security grant.
11. Confirm the control injected the current token and included it in the request.
12. Confirm the endpoint reconstructs the grant and checks the authorization action needed for this operation.
13. Check whether the one-hour default token lifetime requires renewal.
14. Stop when authorization succeeds through an intentional rule; do not bypass the server check or trust client visibility. (Creating UI Controls)

## Do Not Assume

- A hidden control prevents unauthorized requests.
- Authorization checked during initialization remains valid.
- A previous C# block instance retains state.
- A success response proves that all submitted values were persisted.
- Stop when authorization succeeds through an intentional rule; do not bypass the server check or trust client visibility.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/grid-reference/columns/attributecolumns
- https://community.rockrms.com/developer/obsidian/grid-reference
- https://community.rockrms.com/developer/obsidian/browser-bus
