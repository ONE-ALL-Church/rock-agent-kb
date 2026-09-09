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

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/documentation/church-management/reporting/metrics
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/documentation/bookcontent/7/361
