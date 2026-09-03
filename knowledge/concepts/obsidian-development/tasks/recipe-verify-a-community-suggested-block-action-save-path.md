---
concept_id: obsidian-development
task_id: recipe-verify-a-community-suggested-block-action-save-path
title: Recipe: Verify A Community-Suggested Block-Action Save Path
generated: true
---

# Recipe: Verify A Community-Suggested Block-Action Save Path

A proposed operational save path is evaluated without treating one organization’s experience as universal Rock behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`
- `Workflow`
- `Block`
- `Person`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`
- `Workflow`
- `Block`
- `Person`

## Steps

1. Identify the installed block, its version, action key, current initialization payload, and required permissions.
2. Confirm from applicable source or runtime metadata that the action is intended to own the relationship or configuration.
3. Read the current state.
4. Submit the smallest authorized change.
5. Read the state again through an independent source.
6. Compare the persisted relationships and normalized values with the intended result.
7. Roll the finding into public guidance only after a public-safe review.
8. Confirm the server action checks the current person’s ordinary authorization.
9. If a child control needs delegated access, confirm the block created and provided a security grant.
10. Confirm the control injected the current token and included it in the request.
11. Confirm the endpoint reconstructs the grant and checks the authorization action needed for this operation.
12. Check whether the one-hour default token lifetime requires renewal.
13. Stop when authorization succeeds through an intentional rule; do not bypass the server check or trust client visibility. (Creating UI Controls)

## Do Not Assume

- Stop when authorization succeeds through an intentional rule; do not bypass the server check or trust client visibility.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/creating-ui-controls
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/developer/obsidian/browser-bus
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/AccountEntry/utils.partial.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/FieldTypes/blockTemplateFieldComponents.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/Security/tsconfig.json
