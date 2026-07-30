---
concept_id: prayer-care
task_id: audit-prayer-configuration
title: Audit Prayer Configuration
generated: true
---

# Audit Prayer Configuration

Complete Audit Prayer Configuration with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `Group`
- `Workflow`
- `Page`
- `Block`

## Steps

1. Identify Rock version.
2. List prayer pages and block types.
3. Inspect Prayer Request Entry settings.
4. Inspect Prayer Request List and Detail settings.
5. Inspect Prayer Session/Card View pages.
6. Review categories.
7. Review Prayer Team and Prayer Administrator security.
8. Check Send Prayer Comments job and system communication.
9. Check custom prayer workflows.
10. Check prayer wall, SMS, urgent email, and group prayer pages.
11. Check release-note caveats for installed version.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://community.rockrms.com/recipes/135
- https://community.rockrms.com/recipes/338
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/PrayerRequestsController.CodeGenerated.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestList/PrayerRequestListOptionsBag.cs
- https://community.rockrms.com/rocku/individuals-in-rock/prayer-requests
- https://community.rockrms.com/recipes/121
- https://community.rockrms.com/recipes/389
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Prayer/PrayerRequestDetail/PrayerRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/MyPrayerRequests.cs
- https://community.rockrms.com/recipes/350
