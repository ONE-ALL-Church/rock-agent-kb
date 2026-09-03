---
concept_id: people-families
task_id: recipe-validate-family-preregistration-end-to-end
title: Recipe: Validate family preregistration end to end
generated: true
---

# Recipe: Validate family preregistration end to end

A visitor can preregister without producing preventable duplicates, and the resulting people data leads to check-in and staff action.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Campus`
- `Family`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `Campus`
- `Family`
- `Workflow`
- `Attribute`

## Steps

1. Review the public explanation and requested fields.
2. Review adult and child requiredness separately.
3. Review SMS opt-in, attributes, campus, visit date, and address handling.
4. Test one new family.
5. Test one existing-person match.
6. Verify people, family memberships, roles, address, and campus.
7. Verify check-in eligibility through the intended path.
8. Verify family, parent, and child workflows with the expected entities.
9. Verify staff follow-up or connection creation.
10. Review resulting duplicates, partial records, and failed workflow cases before launch.
11. Test with a controlled new-family case and a controlled existing-person case.
12. Record which adult, child, address, contact, and attribute fields are required.
13. Verify the duplicate-matching result before saving.
14. Confirm the family and person records created.
15. Confirm family roles, address, campus, and check-in eligibility.
16. Confirm the expected family, parent, and child workflows and their entity types.
17. Confirm staff follow-up or connection creation.
18. Stop broad launch if any path creates ambiguous, duplicate, or incomplete records. Pre-Register a Family

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
- https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz
