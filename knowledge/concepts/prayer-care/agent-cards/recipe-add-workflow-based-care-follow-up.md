---
concept_id: prayer-care
task_id: recipe-add-workflow-based-care-follow-up
title: Recipe: Add workflow-based care follow-up
generated: true
---

# Recipe: Add workflow-based care follow-up

A qualifying prayer event creates a bounded care action without exposing the request broadly.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Workflow`
- `Block`
- `Attribute`

## Entities And Tables

- `Person`
- `Workflow`
- `Block`
- `Attribute`

## Steps

1. Choose the supported trigger: request submission, Prayer Card prayed action, or Prayer Card flagged action.
2. Define the workflow’s entity and required attributes.
3. For Prayer Card actions, define the appropriate actor attribute: `PrayerOfferedByPersonId` or `FlaggedByPersonId`.
4. Add explicit criteria for the ministry condition being handled.
5. Assign the resulting activity only to authorized care workers.
6. Limit communication content to the minimum necessary.
7. Add an auditable completion or disposition state.
8. Test with synthetic requests that should and should not trigger.
9. Verify that unauthorized users cannot open the workflow or linked request.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailAddPersonResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/UpcomingFollowUpBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryPrayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Workflow/Action/People/PrayerRequestAdd.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/upcomingFollowUpBag.d.ts
