---
concept_id: obsidian-development
task_id: recipe-audit-a-block-for-security
title: Recipe: Audit A Block For Security
generated: true
---

# Recipe: Audit A Block For Security

Complete Audit A Block For Security with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Identify all block actions.
2. For each action, identify data read/write scope.
3. Confirm server-side authorization.
4. Confirm entity-level authorization.
5. Confirm page/block permissions.
6. Inspect security grants.
7. Inspect whether private configuration values are sent to browser.
8. Inspect route parameters and entity identifiers.
9. Test as admin, staff, view-only, and unauthorized user.
10. Confirm hidden buttons are not the only protection.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://community.rockrms.com/developer/obsidian/grid-reference
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/null-vs-undefined
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/form-validation
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/obsidian-component-structure
