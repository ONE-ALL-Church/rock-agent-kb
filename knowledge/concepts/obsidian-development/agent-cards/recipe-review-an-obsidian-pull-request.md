---
concept_id: obsidian-development
task_id: recipe-review-an-obsidian-pull-request
title: Recipe: Review An Obsidian Pull Request
generated: true
---

# Recipe: Review An Obsidian Pull Request

Review against the current Obsidian developer documentation, Null vs Undefined, and Rock Core Release Notes. Build and exercise the changed block on its supported Rock version; static review alone cannot establish authorization, payload, grid, or lifecycle behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Does every block action validate authorization?
2. Does the browser receive only necessary data?
3. Are null/undefined/empty states handled?
4. Are field type configuration values normalized?
5. Does the grid have stable keys?
6. Is client-side grid row count acceptable?
7. Are filters/sort/export values correct?
8. Are destructive actions confirmed?
9. Are async buttons disabled while pending?
10. Are standard controls used instead of custom UI where appropriate?
11. Are plugin paths and core paths kept separate?
12. Are release caveats considered?
13. Are tests or gallery coverage included for field types?

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/null-vs-undefined
- https://community.rockrms.com/developer/obsidian
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/grid-reference/grid
- https://community.rockrms.com/developer/obsidian/grid-reference/filters
