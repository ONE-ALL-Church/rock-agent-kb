---
concept_id: groups
task_id: recipe-move-members-between-groups-safely
title: Recipe: Move Members Between Groups Safely
generated: true
---

# Recipe: Move Members Between Groups Safely

Complete Move Members Between Groups Safely with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Group`
- `Workflow`
- `Attribute`

## Steps

1. Export old group member IDs, people, roles, statuses, attributes.
2. Confirm target group and role mapping.
3. Check requirements.
4. Check workflow triggers.
5. Check scheduling assignments.
6. Decide whether to remove old membership or mark inactive.
7. Notify ministry owner.
8. Verify old group membership.
9. Verify new group membership.
10. Verify role/status.
11. Verify member attributes.
12. Verify requirements.
13. Verify leader roster.
14. Verify reporting.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/7
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/ask/developing/2801
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/recipes/220
- https://community.rockrms.com/recipes/329
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs
