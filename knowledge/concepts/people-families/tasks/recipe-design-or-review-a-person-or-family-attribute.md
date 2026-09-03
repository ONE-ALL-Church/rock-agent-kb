---
concept_id: people-families
task_id: recipe-design-or-review-a-person-or-family-attribute
title: Recipe: Design or review a person or family attribute
generated: true
---

# Recipe: Design or review a person or family attribute

The attribute has a clear owner, correct entity, maintainable value, appropriate display, and bounded security.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `Family`
- `Workflow`
- `Block`
- `Attribute`
- `Campus`

## Entities And Tables

- `Person`
- `Group`
- `Family`
- `Workflow`
- `Block`
- `Attribute`
- `Campus`

## Steps

1. Define the operational question the value must answer.
2. Search for a standard field or existing attribute.
3. Select the correct entity: person, family, or group membership.
4. Define the owner and update lifecycle.
5. Choose the field type and allowed values.
6. Choose a stable key and appropriate categories.
7. Configure requiredness only where every relevant editing path can supply the value.
8. Configure view and edit security.
9. Place the attribute in the required internal or external block.
10. Test creation, display, editing, blank submission, workflow updates, reporting, and search behavior.
11. Confirm that the correct person record is open.
12. List every family membership and the role in each.
13. Identify which family is primary.
14. Compare the documented household situation with the dual-family and single-family-plus-relationship patterns.
15. Inspect each family’s campus and address.
16. Evaluate reporting, mailing, and check-in consequences before moving or removing membership.
17. Save and then verify the final family list and primary-family ordering. Edit a Family

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes
- https://community.rockrms.com/documentation/church-management/people/families/add-a-family
- https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family
- https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes
- https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes
- https://community.rockrms.com/documentation/church-management/people/families/edit-a-family
- https://community.rockrms.com/documentation/church-management/people/people-basics/edit-a-person
- https://community.rockrms.com/documentation/church-management/people/people-basics/delete-a-person
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-family-analytics/use-era
- https://community.rockrms.com/documentation/church-management/people/person-family-analytics/calculate-analytics
- https://community.rockrms.com/documentation/church-management/people/families/blended-families
