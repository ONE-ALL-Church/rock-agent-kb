---
concept_id: engagement-tracking
task_id: recipe-correct-one-person-s-streak
title: Recipe: Correct one person’s streak
generated: true
---

# Recipe: Correct one person’s streak

A bounded correction is made without unnecessarily rebuilding the entire Streak Type.

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

1. Inspect the occurrence map and the person’s enrollment date.
2. Compare attendance with the engagement map.
3. Add or remove an engagement only if the map should differ from the source-driven result.
4. Add an individual exclusion when an absence should be ignored for that person.
5. Save and refresh.
6. Verify current streak, longest streak and engagement count.
7. Confirm the person’s enrollment date.
8. Inspect the occurrence map for eligible dates after enrollment.
9. Determine whether the engagement map contains participation.
10. If historical attendance should populate the map, consider an individual rebuild.
11. Before rebuilding, record any manual engagement-map changes because the rebuild deletes them. (Intro to Streak Enrollment, Rebuild Streaks Individually)

## Do Not Assume

- An exclusion removes or changes attendance.

## Source Links

- https://community.rockrms.com/documentation/engagement/additional-engagement-tools
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually
