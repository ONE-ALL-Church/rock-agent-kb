---
concept_id: platform-configuration
task_id: recipe-preflight-a-v19-configuration-change
title: Recipe: Preflight a v19 configuration change
generated: true
---

# Recipe: Preflight a v19 configuration change

A version-sensitive feature is enabled with its dependencies and risks tested.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Block`

## Entities And Tables

- `Workflow`
- `Block`

## Steps

1. Confirm the installed Rock version and relevant block version.
2. Read the current documentation and release notes for that build.
3. Identify organization-level, block-level, security, provider, and workflow dependencies.
4. Build representative success, denial, and boundary cases.
5. Test the feature in the actual consuming surface.
6. Review privacy and disclosure effects, especially duplicate-registration warnings and retained communication history.
7. Prepare brief staff training for changed interfaces.
8. Obtain the appropriate operational approval.
9. Deploy in a bounded window.
10. Verify visible behavior and retained records after deployment.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/EntityTypes/entityTypesOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/EntityTypes/EntityTypesBag.cs
- https://community.rockrms.com/rocku/workflows
