---
concept_id: api-integrations
task_id: recipe-preflight-a-rest-integration
title: Recipe: Preflight A REST Integration
generated: true
---

# Recipe: Preflight A REST Integration

A documented, least-privilege integration contract ready for safe testing.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Record the target Rock environment and version.
2. Open the installed API v1 or v2 documentation.
3. Identify the exact controller, route, and operation.
4. Identify the caller’s session or REST Key without copying the secret into notes.
5. Classify the task as read-only, create, partial update, full replacement, or delete.
6. Inspect controller permissions and applicable entity security.
7. Define the smallest request and response fields.
8. Prepare a non-production or otherwise safe test record.
9. Define the independent readback and rollback expectation before sending a write.
10. Stop before production if unrestricted access is the only known way to make the call succeed.

## Do Not Assume

- A matching model name guarantees an exposed route.
- Authentication grants controller or entity access.
- v1 and v2 have identical behavior.
- An HTTP success proves the intended persisted state.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/data/api/secure-the-api
- https://community.rockrms.com/api-docs
