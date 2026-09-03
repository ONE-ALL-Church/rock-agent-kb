---
concept_id: platform-configuration
task_id: recipe-plan-a-rock-upgrade-as-configuration-change
title: Recipe: Plan a Rock upgrade as configuration change
generated: true
---

# Recipe: Plan a Rock upgrade as configuration change

The upgrade covers technical validation, security maintenance, and staff adoption.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Page`
- `Block`
- `Attribute`

## Steps

1. Confirm the supported branches and current release notes.
2. Separate major-version test scope from patch-release test scope.
3. Inventory affected pages, blocks, workflows, integrations, attributes, categories, registrations, communications, and check-in surfaces.
4. Test with non-administrator roles as well as administrators.
5. Re-test previously affected version-specific defects.
6. Prepare short targeted training for visible workflow changes.
7. Assign role-based training where the configured LMS supports it.
8. Train staff before volunteer rollout.
9. Apply the upgrade through the organization’s controlled release process.
10. Verify the installed build and representative workflows after deployment.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/rocku/workflows
