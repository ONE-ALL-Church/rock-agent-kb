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
- `Page`
- `Block`

## Entities And Tables

- `Group`
- `Campus`
- `Page`
- `Block`

## Steps

1. Use Prayer Request as the model.
2. Filter active approved non-expired requests.
3. Group by category and campus.
4. Include prayer count and entered date.
5. Highlight zero-prayer requests older than a threshold.
6. Separate group-scoped requests.
7. Add flagged and urgent counts.
8. Use the Category data select where available (CategorySelect.cs).
9. Is the request active?
10. Is it expired?
11. Is it approved?
12. Is it public/private, and does the prayer-team block filter by public?
13. Is it assigned to a category selected by the prayer team?
14. Is it urgent but hidden by a custom filter?
15. Is it group-associated? If yes, is `GroupGuid` present in the prayer-team URL?
16. Is the prayer-team user authenticated and in the right role?
17. Is the block configured to show the relevant categories?
18. Is the request on a campus filtered out by the block?

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs
- https://community.rockrms.com/documentation/engagement/prayer
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://community.rockrms.com/recipes/338
- https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/recipes/135
- https://community.rockrms.com/recipes/121
- https://community.rockrms.com/recipes/389
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs
