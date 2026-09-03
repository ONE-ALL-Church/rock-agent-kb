---
concept_id: api-integrations
task_id: recipe-configure-and-review-a-rest-key
title: Recipe: Configure And Review A REST Key
generated: true
---

# Recipe: Configure And Review A REST Key

An active external credential with a named owner, bounded permissions, and a revocation plan.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. In the installed administration UI, navigate to REST Keys.
2. Create or locate a clearly named key for one integration purpose.
3. Add a description identifying its operational owner and use.
4. Verify the active state.
5. Grant only the controller operations the integration requires.
6. Store the token in an approved secret store, never public source or browser code.
7. Test the narrowest read operation first.
8. Test writes only after defining readback and rollback.
9. Record how the key will be revoked or replaced.

## Do Not Assume

- Store the token in an approved secret store, never public source or browser code.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/data/api/rest-keys
- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
