---
concept_id: ai-agents-automation
task_id: recipe-build-a-bounded-list-and-get-pair
title: Recipe: Build a bounded List and Get pair
generated: true
---

# Recipe: Build a bounded List and Get pair

The agent can search a large entity set and retrieve details only for the selected item.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`

## Entities And Tables

- `Page`

## Steps

1. Define a `List<Entity>` tool with explicit filters and deterministic ordering.
2. Use cursor pagination when per-item authorization is required.
3. Return only the fields needed to distinguish candidates.
4. Define a `Get<Entity>` tool accepting the selected `IdKey`.
5. Enforce security while loading the entity.
6. Shape and sanitize the full result.
7. Keep only a compact reference in conversation history.
8. Test pagination, invalid keys, denied entities and repeated retrieval.

## Do Not Assume

- Page-number pagination is safe with per-item filtering.
- Every entity property belongs in the agent context. Native List Tools and

## Source Links

- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/list-tools
- https://community.rockrms.com/developer/ai-agents/writing-custom-tools/native-tools/get-tools
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.AI.Agent/Skills/CmsSkill.GetPageAvailableAttributes.cs
