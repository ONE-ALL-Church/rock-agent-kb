---
concept_id: prayer-care
task_id: investigate-person-prayer-history
title: Investigate Person Prayer History
generated: true
---

# Investigate Person Prayer History

Complete Investigate Person Prayer History with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`

## Entities And Tables

- `Person`
- `Group`

## Steps

1. Use person profile and aliases.
2. Use reporting filter for Prayer Requests containing selected people where available (ContainsPeopleFilter.cs).
3. Check manually entered name/email requests that may not link to the person.
4. Check duplicate person records.
5. Check group-scoped requests if relevant.
6. Respect privacy and security policy before exposing history.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs
- https://community.rockrms.com/documentation/engagement/prayer
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs
- https://community.rockrms.com/recipes/338
- https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests
- https://community.rockrms.com/rocku/individuals-in-rock
- https://community.rockrms.com/recipes/135
- https://community.rockrms.com/recipes/121
