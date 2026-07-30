---
concept_id: security-permissions
task_id: recipe-answer-who-has-access-to-this
title: Recipe: Answer “Who Has Access To This?”
generated: true
---

# Recipe: Answer “Who Has Access To This?”

Do not answer from direct `Auth` rows alone unless the question is explicitly “what rules are configured?” The role inspector recipe warns direct rows do not account for inheritance (Security Role Permissions Inspector).

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. Secured object.
2. Action verb.
3. Direct allows.
4. Direct denies.
5. Inherited source.
6. Effective roles.
7. Effective people, if needed.
8. Person-specific exceptions.
9. Public/all-user access.
10. Unknowns requiring live test.

## Do Not Assume

- Do not answer from direct `Auth` rows alone unless the question is explicitly “what rules are configured?” The role inspector recipe warns direct rows do not account for inheritance (Security Role Permissions Inspector).

## Source Links

- https://community.rockrms.com/recipes/337
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/developer/mobile-docs/app-factory/rock-logins
- https://community.rockrms.com/developer/303---blast-off/rock-security
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504091716317_AddPersonalDeviceLocationPermissionStatus.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Security/Authorization.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2017.0/Version%2017.1/202504091716317_AddPersonalDeviceLocationPermissionStatus.Designer.cs
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/recipes/522/security-management-data-integrity-and-qol
- https://community.rockrms.com/recipes/243
- https://community.rockrms.com/recipes/344
