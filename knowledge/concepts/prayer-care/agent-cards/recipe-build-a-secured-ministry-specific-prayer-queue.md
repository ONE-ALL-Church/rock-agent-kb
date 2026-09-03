---
concept_id: prayer-care
task_id: recipe-build-a-secured-ministry-specific-prayer-queue
title: Recipe: Build a secured ministry-specific prayer queue
generated: true
---

# Recipe: Build a secured ministry-specific prayer queue

A ministry team sees only the intended category scope through a secured page.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Page`
- `Block`

## Entities And Tables

- `Person`
- `Page`
- `Block`

## Steps

1. Create or select a page for the ministry prayer team.
2. Restrict page access to the intended security role.
3. Add Prayer Session or Prayer Card View.
4. Configure the block for the ministry’s category.
5. Decide whether the block should show public requests only.
6. Configure flagging, threshold, ordering, and maximum results.
7. Test with an administrator, intended team member, unrelated signed-in person, and anonymous visitor.
8. Confirm that the administrative Prayer Request List remains restricted to administrators.

## Do Not Assume

- Category security flows to request records.
- Page access automatically grants comment-entry rights.
- A small maximum-results value still gives the team complete coverage.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailAddPersonResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/UpcomingFollowUpBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryPrayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs
