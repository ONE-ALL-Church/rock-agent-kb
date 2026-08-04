---
concept_id: prayer-care
task_id: safely-extend-prayer-intake
title: Safely Extend Prayer Intake
generated: true
---

# Safely Extend Prayer Intake

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `PersonAlias`
- `Group`
- `Campus`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Person`
- `PersonAlias`
- `Group`
- `Campus`
- `Workflow`
- `Attribute`

## Steps

1. Prefer workflow action `Prayer Request Add`.
2. Avoid direct SQL unless there is no supported alternative.
3. Set approval false by default.
4. Set public false by default.
5. Assign category deliberately.
6. Attach campus if known.
7. Attach person alias only after confident matching.
8. Log source through a custom public-safe attribute if useful.
9. Test public, private, urgent, and group cases.

## Do Not Assume

- Avoid direct SQL unless there is no supported alternative.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-request-comments-communication
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/recipes/135
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/recipes/338
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/PrayerRequest/ContainsPeopleFilter.cs
- https://community.rockrms.com/recipes/121
- https://community.rockrms.com/recipes/389
