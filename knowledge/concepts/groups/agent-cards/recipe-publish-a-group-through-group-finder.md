---
concept_id: groups
task_id: recipe-publish-a-group-through-group-finder
title: Recipe: Publish a group through Group Finder
generated: true
---

# Recipe: Publish a group through Group Finder

An intended group is discoverable without exposing unnecessary location precision.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Page`
- `Block`
- `Campus`
- `Attribute`

## Entities And Tables

- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Page`
- `Block`
- `Campus`
- `Attribute`

## Steps

1. Confirm the group is active and public.
2. Confirm its Group Type is included in the finder.
3. Configure an appropriate location and privacy precision.
4. Use a Weekly schedule if visitors must filter by day or time.
5. Review capacity and the block’s overcapacity behavior.
6. Confirm the detail and registration linked pages.
7. Test initial load, each enabled filter, map behavior, details, and registration as an anonymous visitor.
8. If seasonal, test closed-state routes, redirects, blocks, and alternate surfaces.
9. Confirm the group is marked `Public`.
10. Confirm its Group Type is included in the block’s configured Group Types.
11. Check whether the group has reached capacity and whether overcapacity groups are hidden.
12. Inspect location-type, campus, geofence, and attribute filters.
13. If filtering by day or time, confirm the group uses a Weekly schedule.
14. Test the public route and any alternate or mobile surface as an anonymous visitor.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/View_GroupLocationSchedules.sql
- https://community.rockrms.com/rocku/workflows
- https://community.rockrms.com/rocku/check-in/rapid-attendance-entry
- https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix
- https://community.rockrms.com/developer/helix/lava-applications/content-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs
- https://community.rockrms.com/recipes/519
