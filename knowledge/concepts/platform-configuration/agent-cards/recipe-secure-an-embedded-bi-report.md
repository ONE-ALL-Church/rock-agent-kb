---
concept_id: platform-configuration
task_id: recipe-secure-an-embedded-bi-report
title: Recipe: Secure an embedded BI report
generated: true
---

# Recipe: Secure an embedded BI report

Only appropriately authorized and licensed users can open the embedded report.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Identify the Rock page and block that host the report.
2. Define the Rock roles that should have access.
3. Apply and inspect page and block authorization.
4. Identify the external BI license and identity requirements.
5. Test an authorized, licensed user.
6. Test an authorized but unlicensed user.
7. Test an unauthorized Rock user.
8. Confirm that report links or embed behavior do not create a bypass.
9. Document both Rock-side and provider-side ownership.
10. Check Rock page and block authorization.
11. Test an authorized Rock account.
12. Test an unauthorized Rock account.
13. Check the external BI identity and license.
14. Confirm that embedding does not bypass the intended external access boundary.
15. Stop when both Rock authorization and provider access are independently demonstrated.

## Do Not Assume

- Confirm that report links or embed behavior do not create a bypass.

## Source Links

- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs
- https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz
