---
concept_id: security-permissions
task_id: recipe-preflight-a-least-privilege-rest-integration
title: Recipe: Preflight a least-privilege REST integration
generated: true
---

# Recipe: Preflight a least-privilege REST integration

A documented integration identity with only the access required for known routes and methods.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Inventory every route and HTTP method.
2. Classify each operation as read or write.
3. Identify the authenticated user session or REST key.
4. Map each operation to its entity and authorization action.
5. Grant only demonstrated permissions.
6. Store and transmit credentials outside templates, logs, and client-visible output.
7. Test against non-production or non-sensitive records where possible.
8. Read back intended writes and compare only integration-owned fields.
9. Document rotation, revocation, logging, and rollback.

## Do Not Assume

- A successful call proves least privilege.
- An IdKey authorizes access.
- An API key should have administrator-equivalent rights.
- Community PATCH guidance applies identically to every API v2 endpoint.

## Source Links

- https://community.rockrms.com/developer/303---blast-off/the-rock-rest-api
