---
concept_id: lava
task_id: recipe-build-a-bounded-read-only-entity-view
title: Recipe: Build a bounded read-only entity view
generated: true
---

# Recipe: Build a bounded read-only entity view

A limited list using an Entity command.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Confirm the entity command name with current documentation or `taglist`.
2. Enable only Rock Entity access on the owning surface.
3. Choose one lookup strategy: `id`, `where` or Data View.
4. Quote command parameters correctly.
5. Add sorting and a strict result limit.
6. Render only the required properties.
7. Test no-result, one-result and maximum-result cases.
8. Verify audience authorization independently.

## Do Not Assume

- `where` still applies when `id` is supplied.
- A registered command is enabled.
- Entity access automatically enforces every business rule.
- A working administrator view is audience-safe.

## Source Links

- https://community.rockrms.com/lava/commands/taglist-commands
- https://community.rockrms.com/lava/commands/entity-commands
