---
concept_id: groups
task_id: recipe-audit-a-group-type-before-launch
title: Recipe: Audit A Group Type Before Launch
generated: true
---

# Recipe: Audit A Group Type Before Launch

Complete Audit A Group Type Before Launch with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Step`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Attendance`
- `Step`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`
- `Attribute`

## Steps

1. Name and purpose.
2. Allowed child group types.
3. Roles and default role.
4. Leader role.
5. Attendance settings.
6. Schedule options.
7. Schedule exclusions.
8. Location types and selection modes.
9. Group attributes.
10. Group member attributes.
11. Requirements.
12. Workflow triggers.
13. Security.
14. Finder/registration usage.
15. Reports depending on it.
16. Launch readiness.
17. Missing configuration.
18. Risky inherited settings.
19. Live verification steps.
20. Parent group `GroupTypeId`.
21. Parent Group Type allowed child group types.
22. Whether the intended child Group Type is active.
23. Whether the user has edit/administrate access.
24. Whether the UI is scoped to a subset of group types.
25. Whether the group is archived or inactive.
26. Whether inheritance or circular references are producing errors.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/7
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/ask/developing/2801
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/recipes/220
- https://community.rockrms.com/recipes/329
