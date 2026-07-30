---
concept_id: api-integrations
task_id: recipe-audit-a-rest-key
title: Recipe: Audit A REST Key
generated: true
---

# Recipe: Audit A REST Key

Complete Audit A REST Key with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Locate key in `Home > Security > REST Keys`.
2. Identify person/API user.
3. List allowed controllers/actions.
4. Identify unrestricted permissions.
5. Check entity security for target records.
6. Check last known use if logs exist.
7. Recommend least-privilege changes and rotation if needed.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/apple-tv-docs/javascript/commands/personal-commands
- https://community.rockrms.com/developer/303---blast-off/rock-security
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Security/OidcClientTests.cs
- https://community.rockrms.com/recipes/232
