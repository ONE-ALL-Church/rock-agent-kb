---
concept_id: people-families
task_id: recipe-add-a-person-or-family-without-creating-a-duplicate
title: Recipe: Add a person or family without creating a duplicate
generated: true
---

# Recipe: Add a person or family without creating a duplicate

The correct person records are attached to the correct family with no avoidable duplicate.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Campus`
- `Family`

## Entities And Tables

- `Person`
- `Campus`
- `Family`

## Steps

1. Search for every adult and child using available current and alternate identity information.
2. Separate people already in Rock from genuinely new people.
3. Create the family through `People > New Family`.
4. Enter only people who are not already present.
5. Review possible duplicate warnings.
6. Save the family.
7. Edit the saved family to attach existing people.
8. Verify roles, campus, address, marital-status handling, and final family membership.
9. Confirm that the correct person record is open.
10. List every family membership and the role in each.
11. Identify which family is primary.
12. Compare the documented household situation with the dual-family and single-family-plus-relationship patterns.
13. Inspect each family’s campus and address.
14. Evaluate reporting, mailing, and check-in consequences before moving or removing membership.
15. Save and then verify the final family list and primary-family ordering. Edit a Family

## Do Not Assume

- A missing duplicate warning proves uniqueness.
- Two households require two person records.
- Similar names alone prove a match.

## Source Links

- https://community.rockrms.com/documentation/church-management/people/families/add-a-family
- https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes
- https://community.rockrms.com/documentation/church-management/people/families/pre-register-a-family
- https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes
- https://community.rockrms.com/documentation/church-management/people/families/edit-a-family
- https://community.rockrms.com/documentation/church-management/people/people-basics/edit-a-person
- https://community.rockrms.com/documentation/church-management/people/people-basics/delete-a-person
- https://community.rockrms.com/documentation/church-management/people/person-family-analytics/use-era
- https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes
- https://community.rockrms.com/documentation/church-management/people/person-family-analytics/calculate-analytics
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/families/blended-families
