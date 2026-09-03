---
concept_id: platform-configuration
task_id: recipe-place-person-attributes-on-a-profile-tab
title: Recipe: Place person attributes on a profile tab
generated: true
---

# Recipe: Place person attributes on a profile tab

A selected category of Person Attributes appears in the intended profile location.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Location`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Location`
- `Block`
- `Attribute`

## Steps

1. Confirm that the attributes belong to the Person entity.
2. Assign the intended category or categories.
3. Use the Admin Toolbar and Zone Editor to add an Attribute Values block to the intended profile tab.
4. Configure the block for the specific category.
5. Review block authorization.
6. Test a person with populated values.
7. Test the edit path with a permitted user.
8. Test the view path with a user who should not edit.
9. Remember that the Extended Attributes area may omit attributes without values.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://www.rockrms.com/releasenotes
- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses
