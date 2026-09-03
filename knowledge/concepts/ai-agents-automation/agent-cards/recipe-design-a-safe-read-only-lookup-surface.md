---
concept_id: ai-agents-automation
task_id: recipe-design-a-safe-read-only-lookup-surface
title: Recipe: Design a safe read-only lookup surface
generated: true
---

# Recipe: Design a safe read-only lookup surface

The agent can resolve a natural-language reference to an authorized Rock entity without receiving unnecessary data.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Identify the downstream tool and the exact identifier it needs.
2. Determine the smallest useful selection fields, normally an `IdKey`, name and limited disambiguating metadata.
3. Use a cache object when available; otherwise use a secured entity query.
4. Filter out inactive or unauthorized entries when required.
5. Return structured results through `AgentToolResult`.
6. Store a compact history representation.
7. Test no matches, one match, multiple matches and a denied record.

## Do Not Assume

- A small development dataset will stay small.
- A Public agent designation automatically sanitizes every field.
- Prompt instructions enforce data access.

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/lookup-tools
