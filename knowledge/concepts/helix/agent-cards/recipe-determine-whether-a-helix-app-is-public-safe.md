---
concept_id: helix
task_id: recipe-determine-whether-a-helix-app-is-public-safe
title: Recipe: Determine Whether A Helix App Is Public-Safe
generated: true
---

# Recipe: Determine Whether A Helix App Is Public-Safe

Complete Determine Whether A Helix App Is Public-Safe with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Attribute`

## Entities And Tables

- `Person`
- `Attribute`

## Steps

1. Identify every endpoint.
2. Mark each endpoint read-only or write/destructive.
3. Confirm GET endpoints do not modify data.
4. Confirm public endpoints expose only public data.
5. Confirm identifiers use GUIDs or IdKeys where appropriate.
6. Confirm direct endpoint calls cannot access unauthorized records.
7. Confirm SQL input is sanitized or removed.
8. Confirm no sensitive attribute security bypass exists.
9. Confirm cache settings cannot leak personalized fragments.
10. Document residual risk.

## Do Not Assume

- Confirm GET endpoints do not modify data.

## Source Links

- https://community.rockrms.com/developer/helix/lava-applications/observability
- https://community.rockrms.com/lava/filters/attribute-filters
