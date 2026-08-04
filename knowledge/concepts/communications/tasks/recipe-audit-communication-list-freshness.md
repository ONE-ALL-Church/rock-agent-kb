---
concept_id: communications
task_id: recipe-audit-communication-list-freshness
title: Recipe: Audit communication list freshness
generated: true
---

# Recipe: Audit communication list freshness

Flag if the list is one of Rock's shipped lists and no sync path exists, because RockU notes shipped lists are not automatically synced (Communication Lists & Segments).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `GroupType`

## Entities And Tables

- `DataView`
- `Group`
- `GroupType`

## Steps

1. list group ID/name
2. group type
3. member count
4. active/inactive members
5. sync job
6. data view
7. last sync time
8. expected source population
9. segment usage
10. subscription/preference settings
11. security

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups
- https://community.rockrms.com/rocku/communication/communication-lists--segments
- https://community.rockrms.com/recipes/370
- https://community.rockrms.com/recipes/132
