---
concept_id: prayer-care
task_id: build-a-prayer-team-coverage-report
title: Build A Prayer-Team Coverage Report
generated: true
---

# Build A Prayer-Team Coverage Report

Complete Build A Prayer-Team Coverage Report with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Campus`

## Entities And Tables

- `Group`
- `Campus`

## Steps

1. Use Prayer Request as the model.
2. Filter active approved non-expired requests.
3. Group by category and campus.
4. Include prayer count and entered date.
5. Highlight zero-prayer requests older than a threshold.
6. Separate group-scoped requests.
7. Add flagged and urgent counts.
8. Use the Category data select where available (CategorySelect.cs).

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs
- https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://community.rockrms.com/recipes/338
- https://community.rockrms.com/recipes/135
- https://community.rockrms.com/recipes/121
- https://community.rockrms.com/recipes/389
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs
