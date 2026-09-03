---
concept_id: prayer-care
task_id: recipe-configure-moderated-public-prayer-intake
title: Recipe: Configure moderated public prayer intake
generated: true
---

# Recipe: Configure moderated public prayer intake

Public submissions enter the intended category and do not reach the prayer team without the chosen approval gate.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`
- `Attribute`

## Entities And Tables

- `Page`
- `Block`
- `Attribute`

## Steps

1. Open the external Prayer Request Entry block.
2. Set the category parent and default category deliberately.
3. Choose whether category selection is visible.
4. Decide whether automatic approval is appropriate.
5. If automatic approval is enabled, set the supported expiration period and establish a flagged-request review cadence.
6. Configure urgent, comments, and public-display choices.
7. Review which prayer attributes are public.
8. Submit test requests covering ordinary, urgent, private, comment-disabled, and sensitive cases.
9. Verify administrative state and prayer-team visibility for each test.

## Do Not Assume

- Category security protects the request.
- Expiration is a deletion policy.
- Automatic approval is safe merely because flagging is enabled.
- Public submissions enter the intended category and do not reach the prayer team without the chosen approval gate.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-overview/prayer-categories
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/enter-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/pray-for-group-prayer-requests
- https://community.rockrms.com/documentation/engagement/prayer/prayer-requests/create-group-prayer-requests
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/UpcomingFollowUpBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryPrayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs
