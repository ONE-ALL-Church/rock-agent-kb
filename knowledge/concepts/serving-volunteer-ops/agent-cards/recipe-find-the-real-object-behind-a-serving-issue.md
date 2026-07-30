---
concept_id: serving-volunteer-ops
task_id: recipe-find-the-real-object-behind-a-serving-issue
title: Recipe: Find The Real Object Behind A Serving Issue
generated: true
---

# Recipe: Find The Real Object Behind A Serving Issue

Complete Find The Real Object Behind A Serving Issue with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Entities And Tables

- `Attendance`
- `Person`
- `Group`
- `GroupType`
- `Location`
- `Schedule`
- `Workflow`

## Steps

1. Ask for the person, date, team, and service time.
2. Resolve person and aliases.
3. Identify the serving group.
4. Identify group type.
5. Identify group location.
6. Identify schedule.
7. Identify attendance occurrence.
8. Identify attendance/scheduling row.
9. Identify communication/workflow history.
10. Report the exact broken link in the chain.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://community.rockrms.com/rocku/groups/group-details
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-security
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://community.rockrms.com/recipes/459
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
- https://community.rockrms.com/rocku/groups/group-attendance
- https://community.rockrms.com/rocku/groups/group-requirements
