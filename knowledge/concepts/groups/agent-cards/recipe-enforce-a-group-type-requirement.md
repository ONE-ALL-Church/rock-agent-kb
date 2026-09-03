---
concept_id: groups
task_id: recipe-enforce-a-group-type-requirement
title: Recipe: Enforce a Group Type requirement
generated: true
---

# Recipe: Enforce a Group Type requirement

The intended population is evaluated and manual additions are blocked or overrideable according to policy.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `GroupType`
- `Workflow`
- `Block`

## Entities And Tables

- `DataView`
- `Group`
- `GroupType`
- `Workflow`
- `Block`

## Steps

1. Open the Group Type’s Group Requirements section.
2. Select the requirement.
3. Scope it by role, age classification, and Data View as needed.
4. Decide whether leaders may override it.
5. Enable pre-add enforcement when required.
6. Test an eligible and ineligible manual addition.
7. Inspect every workflow or integration that can add members and implement a separate eligibility check there.
8. Configure notification recipients and the requirement-notification job if needed.

## Do Not Assume

- Manual-add enforcement applies to workflow additions.
- A requirement applies to every role or age when selectors narrow it.
- A leader receives notifications merely because the role is named Leader.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync
- https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history
- https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group
- https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types
- https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-groups
- https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history
- https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox
- https://community.rockrms.com/documentation/engagement/groups/group-history/enable-group-history
