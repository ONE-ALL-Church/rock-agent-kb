---
concept_id: system-admin-ops
task_id: recipe-review-and-resolve-a-duplicate-person-candidate
title: Recipe: Review and resolve a duplicate-person candidate
generated: true
---

# Recipe: Review and resolve a duplicate-person candidate

Merge only records demonstrated to belong to the same person while preserving the intended values.

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

1. Open the pair in Duplicate Finder.
2. Compare identity evidence and Record Source.
3. Review Account Protection Profile and operator permissions.
4. If uncertain, defer rather than merge.
5. If confirmed, select the primary record.
6. Review each surviving value, including the address separately.
7. Submit a Merge Request if the operator lacks merge authority.
8. Verify the resulting profile and any expected notification after completion.

## Do Not Assume

- A high confidence score proves identity.
- The primary record automatically supplies the correct address.
- Access to start a merge means access to complete it.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/use-duplicate-finder
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/merge-duplicate-records
- https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities
- https://community.rockrms.com/documentation/core-concepts/search/searching-for-people/search-by-name
- https://www.rockrms.com/releasenotes
