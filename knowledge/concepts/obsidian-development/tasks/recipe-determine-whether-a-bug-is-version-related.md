---
concept_id: obsidian-development
task_id: recipe-determine-whether-a-bug-is-version-related
title: Recipe: Determine Whether A Bug Is Version-Related
generated: true
---

# Recipe: Determine Whether A Bug Is Version-Related

Complete Determine Whether A Bug Is Version-Related with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Record exact Rock version.
2. Search release notes for block name, field type, grid, module, and symptom.
3. If a later release fixes it, inspect whether the fix applies exactly.
4. If the instance is below the fix, recommend upgrade or targeted workaround.
5. If the instance includes the fix, inspect custom overrides, plugin code, cache, data, and configuration.
6. If the release note is vague, inspect linked GitHub issue or source diff when available.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/obsidian/blocks/creating-blocks
- https://community.rockrms.com/developer/obsidian/blocks/implementing-ihascustomactions
- https://community.rockrms.com/developer/obsidian/blocks/creating-list-blocks
- https://community.rockrms.com/developer/obsidian/grid-reference/columns
- https://community.rockrms.com/developer/obsidian/blocks/creating-detail-blocks
- https://community.rockrms.com/developer/obsidian/grids
- https://community.rockrms.com/developer/obsidian/blocks
- https://community.rockrms.com/developer/obsidian/null-vs-undefined
- https://community.rockrms.com/developer/obsidian
- https://community.rockrms.com/developer/obsidian/grid-reference/grid
- https://community.rockrms.com/developer/obsidian/grid-reference/filters
