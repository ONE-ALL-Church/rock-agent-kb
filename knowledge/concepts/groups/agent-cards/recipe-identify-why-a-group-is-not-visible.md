---
concept_id: groups
task_id: recipe-identify-why-a-group-is-not-visible
title: Recipe: Identify Why A Group Is Not Visible
generated: true
---

# Recipe: Identify Why A Group Is Not Visible

Complete Identify Why A Group Is Not Visible with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `GroupType`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Group`
- `GroupType`
- `Page`
- `Block`

## Steps

1. Group row: active, archived, parent, Group Type.
2. Security: page, block, group type, group.
3. Group Type: allowed hierarchy and finder settings.
4. Finder/viewer block settings.
5. Template logic and rights filters.
6. Query string/page parameters.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/7
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/ask/developing/2801
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs
- https://community.rockrms.com/recipes/220
- https://community.rockrms.com/recipes/329
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-view
