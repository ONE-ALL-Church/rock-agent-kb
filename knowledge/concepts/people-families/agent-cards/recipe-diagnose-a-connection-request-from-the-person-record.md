---
concept_id: people-families
task_id: recipe-diagnose-a-connection-request-from-the-person-record
title: Recipe: Diagnose a connection request from the person record
generated: true
---

# Recipe: Diagnose a connection request from the person record

The failure is classified as person context, request state, opportunity configuration, assignment, activity, or automation.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`

## Entities And Tables

- `Person`
- `Workflow`

## Steps

1. Open the exact person and check for duplicates.
2. Locate the exact Connection Request.
3. Record its type, opportunity, status, connector, activities, and next action.
4. Compare those values with the intended ministry process.
5. Inspect linked workflow or registration automation.
6. Identify the first state that differs from expectation.
7. Route remediation to the owner of that state.
8. Recheck the person profile and connection detail after correction.
9. Resolve the person and check for duplicates.
10. Confirm the Connection Type and Opportunity.
11. Confirm current request status.
12. Inspect assigned connector or staff owner.
13. Review activities and the next expected action.
14. Inspect related workflow state and automation.
15. Confirm whether a registration-to-connection transfer was expected.
16. Report the fault in the correct category rather than as a generic workflow failure.

## Do Not Assume

- A visible person record proves the request exists.
- A request-status issue is a workflow-engine failure.
- A created request has an assigned follow-up owner.

## Source Links

- https://community.rockrms.com/documentation/church-management/people/person-attributes/manage-person-attributes
- https://community.rockrms.com/documentation/church-management/people/families/add-a-family
- https://community.rockrms.com/documentation/church-management/people/people-basics/edit-a-person
- https://community.rockrms.com/documentation/church-management/people/people-basics/delete-a-person
- https://community.rockrms.com/documentation/church-management/people/families/configure-family-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/use-badges
- https://community.rockrms.com/documentation/church-management/people/people-basics/add-a-person
- https://community.rockrms.com/documentation/church-management/people/person-attributes/person-public-attributes
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/SetPersonAttribute.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/Crm/PersonAttributeForms.ascx.cs
- https://community.rockrms.com/rocku/cms/personalization
- https://community.rockrms.com/rocku/engagement/connections-overview
