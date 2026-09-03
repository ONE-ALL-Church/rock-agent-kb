---
concept_id: prayer-care
task_id: recipe-introduce-ai-assistance-with-human-review
title: Recipe: Introduce AI assistance with human review
generated: true
---

# Recipe: Introduce AI assistance with human review

AI processing is limited to known categories and produces reviewable results.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Block`

## Entities And Tables

- `Block`

## Steps

1. Confirm an active AI provider.
2. Select a small pilot category.
3. Configure only the required capabilities.
4. If using inheritance, keep the pilot to direct child categories or configure deeper categories individually.
5. Confirm the entry block’s default category supports the intended automatic-categorization scope.
6. Enable an AI disclaimer where appropriate.
7. Submit synthetic examples covering names, formatting, private content, public appropriateness, and moderation concerns.
8. Compare processed text with the original.
9. Inspect public status, flag count, category, sentiment, and moderation results.
10. Establish a human review owner before broadening the scope.

## Do Not Assume

- AI inheritance reaches grandchildren.
- A non-public result is also unapproved.
- AI moderation satisfies crisis or safeguarding procedures.

## Source Links

- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-card-view-block
- https://community.rockrms.com/documentation/engagement/prayer/prayer-team-power-tools/prayer-ai-automations
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestList/prayerRequestListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/UpcomingFollowUpBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryPrayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestEntry/prayerRequestEntrySaveResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryPrayerRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/ConnectionOperationalSnapshot/upcomingFollowUpBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Prayer/PrayerRequestDetail/prayerRequestDetailAddPersonResponseBag.d.ts
