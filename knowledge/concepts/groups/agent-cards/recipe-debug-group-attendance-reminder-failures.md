---
concept_id: groups
task_id: recipe-debug-group-attendance-reminder-failures
title: Recipe: Debug Group Attendance Reminder Failures
generated: true
---

# Recipe: Debug Group Attendance Reminder Failures

Complete Debug Group Attendance Reminder Failures with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`

## Entities And Tables

- `Attendance`
- `Group`
- `GroupType`
- `Schedule`

## Steps

1. Group Type takes attendance.
2. Send attendance reminder enabled.
3. Group schedule exists.
4. Schedule date applies and is not excluded.
5. Group has active members/leaders.
6. Reminder job is enabled and ran.
7. Communication/system email settings.
8. Member communication preferences.
9. Attendance already entered or occurrence marked did-not-occur.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/7
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder
- https://community.rockrms.com/ask/developing/2801
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql
- https://community.rockrms.com/recipes/220
- https://community.rockrms.com/recipes/519
- https://community.rockrms.com/recipes/329
