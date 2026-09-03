---
concept_id: engagement-tracking
task_id: recipe-build-a-streak-type-safely
title: Recipe: Build a Streak Type safely
generated: true
---

# Recipe: Build a Streak Type safely

A Streak Type calculates the intended cadence from the intended source.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`

## Entities And Tables

- `Person`
- `Page`

## Steps

1. Define the activity source, target population, frequency and earliest applicable date.
2. Decide whether enrollment is required.
3. Decide whether Sync Linked Activity’s bidirectional behavior is appropriate.
4. Configure and inspect the occurrence map.
5. Enroll a small test population.
6. Verify engagement, non-engagement and exclusion examples.
7. Confirm the operational job timing before expanding use.
8. Distinguish an occurrence-map edit from an individual engagement- or exclusion-map edit.
9. For an individual map edit, save and refresh the page.
10. For an occurrence-map edit, confirm that the nightly cleanup job has run.
11. Inspect enrollment dates because earlier dates remain outside each person’s calculation. (Streak Type Detail, Manually Track Streaks)

## Do Not Assume

- Start date or frequency can be corrected later; both are locked after save. (Add a New Streak Type, Streaks Maps)

## Source Links

- https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type
- https://community.rockrms.com/documentation/engagement/streaks
- https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks
