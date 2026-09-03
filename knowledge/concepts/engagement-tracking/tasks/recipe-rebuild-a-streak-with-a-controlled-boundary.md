---
concept_id: engagement-tracking
task_id: recipe-rebuild-a-streak-with-a-controlled-boundary
title: Recipe: Rebuild a Streak with a controlled boundary
generated: true
---

# Recipe: Rebuild a Streak with a controlled boundary

Attendance-derived streak data is regenerated at the smallest necessary scope.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Person`

## Entities And Tables

- `Attendance`
- `Person`

## Steps

1. Decide whether the problem affects one enrollment or the entire Streak Type.
2. Record existing manual map adjustments in the affected scope.
3. Confirm the Streak Type start date and occurrence map.
4. Use individual rebuild for one person; use type rebuild only for a type-wide regeneration need.
5. Verify enrollment dates, maps, current streaks and longest streaks after completion.
6. Reapply only reviewed manual exceptions that remain valid.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/additional-engagement-tools
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks
- https://community.rockrms.com/documentation/engagement/streaks/streak-types
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments
