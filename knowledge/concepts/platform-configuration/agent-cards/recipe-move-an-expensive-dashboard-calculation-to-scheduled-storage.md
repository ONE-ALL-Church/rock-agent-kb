---
concept_id: platform-configuration
task_id: recipe-move-an-expensive-dashboard-calculation-to-scheduled-storage
title: Recipe: Move an expensive dashboard calculation to scheduled storage
generated: true
---

# Recipe: Move an expensive dashboard calculation to scheduled storage

The dashboard reads a verified stored result instead of rebuilding all history on every request.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Schedule`

## Entities And Tables

- `Schedule`

## Steps

1. Define the decision the dashboard supports.
2. Measure or reproduce the expensive calculation.
3. Choose a Rock metric, persisted dataset, or analytics snapshot based on the required output.
4. Set an acceptable refresh interval.
5. Schedule the calculation away from peak use where appropriate.
6. Store enough context to reconcile the result to its operational source.
7. Compare several stored results with direct calculations.
8. Update the dashboard to read the stored layer.
9. Monitor refresh failures and data age.
10. Retain a documented fallback for stale or missing results.

## Do Not Assume

- Stored means correct.
- A schedule exists merely because the schema supports one.
- One organization’s verified schema proves the same feature is configured elsewhere.

## Source Links

- https://www.youtube.com/watch?v=c-wycR9HEuQ
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/check-in/check-in-manager-1
- https://www.youtube.com/watch?v=edanHiYSDIM
- https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/OLmWVZzBAp
- https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW
