---
concept_id: groups
task_id: recipe-build-a-group-finder-qa-checklist
title: Recipe: Build A Group Finder QA Checklist
generated: true
---

# Recipe: Build A Group Finder QA Checklist

Complete Build A Group Finder QA Checklist with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Campus`
- `Page`
- `Block`
- `Attribute`
- `GroupType`
- `Schedule`

## Entities And Tables

- `Group`
- `Location`
- `Campus`
- `Page`
- `Block`
- `Attribute`
- `GroupType`
- `Schedule`

## Steps

1. Public unauthenticated search.
2. Authenticated search.
3. Campus filter.
4. Day/time filter.
5. Attribute filters.
6. Distance/location filter.
7. Direct `LoadResults=true` behavior if used.
8. Detail page.
9. Registration page.
10. Full group/capacity behavior.
11. Security-hidden group behavior.
12. Mobile rendering if mobile block is used.
13. Pass/fail by filter.
14. Missing groups and reason.
15. Security exposure risks.
16. Block settings to adjust.
17. Group active/archive status.
18. Group Type selected by finder block.
19. Campus context.
20. Schedule options and whether they are filterable.
21. Location and geocoding.
22. Capacity and registration rules.
23. Template security filtering.
24. Query strings such as `LoadResults=true`.
25. Public detail page permissions.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/7
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration
- https://community.rockrms.com/ask/developing/2801
- https://community.rockrms.com/documentation/bookcontent/7/296
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs
- https://community.rockrms.com/recipes/220
