---
concept_id: platform-configuration
task_id: recipe-operate-seasonal-defined-value-options
title: Recipe: Operate seasonal Defined Value options
generated: true
---

# Recipe: Operate seasonal Defined Value options

A stable vocabulary exposes only the intended seasonal options.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Workflow`
- `Attribute`

## Entities And Tables

- `Workflow`
- `Attribute`

## Steps

1. Confirm the options are stable enough to remain in one Defined Type.
2. Define or verify a scoped visibility attribute on its Defined Values.
3. Update the attribute for the coming season.
4. Inspect the form’s selector filter.
5. Refresh any relevant cached or persisted output.
6. Render the form as a representative user.
7. Verify retired options are absent.
8. Verify newly enabled options submit and report correctly.
9. Add this verification to the recurring seasonal runbook.
10. Confirm the form uses the intended Defined Type.
11. Inspect the visibility attribute on every relevant Defined Value.
12. Inspect the selector’s filter.
13. Check caching or persisted output used by the form.
14. Confirm retired options are absent and new options are selectable.

## Do Not Assume

- A changed Defined Value attribute immediately changes a cached form.
- Hidden options cannot remain in historical records.
- A successfully submitted value came from the intended Defined Type.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
