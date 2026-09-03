---
concept_id: people-families
task_id: recipe-prepare-a-duplicate-person-merge-for-authorized-review
title: Recipe: Prepare a duplicate-person merge for authorized review
generated: true
---

# Recipe: Prepare a duplicate-person merge for authorized review

A reviewer receives a bounded comparison and can merge without relying on recency alone.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Family`
- `Attribute`

## Entities And Tables

- `Person`
- `Family`
- `Attribute`

## Steps

1. Confirm that the records represent the same person.
2. Compare core identity, contact information, statuses, family memberships, attributes, notes, accounts, and history.
3. Inspect aliases and record-source information where available.
4. Compare last-modified time and actor data in supported v19 interfaces.
5. Identify the intended surviving values field by field.
6. Document downstream reporting and process impact.
7. Route the request to an authorized merger.
8. If supported, request completion notification.
9. After the merge, verify the surviving profile, family links, Previous Last Names behavior, and downstream reports.
10. Search using current identity information.
11. Check relevant alternate or former email Search Keys, remembering that they are matching aids rather than communication destinations.
12. Inspect possible duplicate results and any record-source information available in the installed version.
13. Confirm whether Account Protection Profile behavior affected duplicate checking.
14. Inspect inactive or pending records before creating a new person.
15. If multiple records exist, stop creation and begin a merge review; do not delete one record. Add a Family

## Do Not Assume

- The newest record is correct.
- The most complete record should survive unchanged.
- Merge permission follows from permission to submit a request.
- Former-name visibility matches local policy.
- If multiple records exist, stop creation and begin a merge review; do not delete one record.

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
