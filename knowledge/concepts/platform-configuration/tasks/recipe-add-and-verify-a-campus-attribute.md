---
concept_id: platform-configuration
task_id: recipe-add-and-verify-a-campus-attribute
title: Recipe: Add and verify a campus attribute
generated: true
---

# Recipe: Add and verify a campus attribute

A secured campus attribute is visible and stores the intended value on Campus Details.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Campus`
- `Attribute`

## Entities And Tables

- `Campus`
- `Attribute`

## Steps

1. Define the value’s purpose and confirm Campus is the correct owner.
2. Open `Admin Tools > Settings > Entity Attributes`.
3. Add an attribute with Entity Type `Campus`.
4. Leave the qualifier field and value empty, as directed by the campus documentation.
5. Configure the field type and presentation details supported by the requirement.
6. Save the attribute.
7. Configure attribute security.
8. Open Campus Details and set a test value.
9. Verify visibility and editability as representative authorized and unauthorized users.
10. Record downstream consumers that rely on the value.

## Do Not Assume

- Saving the definition creates values for existing campuses.
- Administrative access implies every user can view or edit the value.
- Web support proves mobile support.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/rocku/check-in/check-in-manager-1
