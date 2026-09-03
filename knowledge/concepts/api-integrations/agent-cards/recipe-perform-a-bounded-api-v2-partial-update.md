---
concept_id: api-integrations
task_id: recipe-perform-a-bounded-api-v2-partial-update
title: Recipe: Perform A Bounded API v2 Partial Update
generated: true
---

# Recipe: Perform A Bounded API v2 Partial Update

Only the integration-owned fields are changed and independently verified.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm that the installed endpoint supports `PATCH`.
2. Read the target record and retain a bounded pre-write comparison.
3. Identify exactly which fields the integration owns.
4. Exclude navigation objects and unrelated properties unless their behavior is explicitly tested.
5. Submit the partial update against a safe record.
6. Read the entity back through a separate request or UI.
7. Compare the intended fields and confirm unrelated fields remain unchanged.
8. Stop if the endpoint normalizes, ignores, or changes properties unexpectedly.
9. Promote the pattern only after target-version validation.
10. Determine whether the integration used `PUT` or `PATCH`.
11. Inspect the installed operation help and current Model Map.
12. Compare the submitted payload with a pre-write snapshot.
13. Read the entity back through an independent path.
14. If the integration owns only selected fields, test the documented partial-update operation on a non-production record.
15. Do not retry the same full payload until omitted/defaulted properties are understood. (Intro to the Rock API)

## Do Not Assume

- `PUT` is safe for a partial object.
- Omitted values are preserved by a full-update operation.
- Relationships behave like scalar properties.
- Do not retry the same full payload until omitted/defaulted properties are understood.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/data/api/intro-to-the-rock-api
