---
concept_id: serving-volunteer-ops
task_id: recipe-secure-an-embedded-volunteer-dashboard
title: Recipe: Secure an embedded volunteer dashboard
generated: true
---

# Recipe: Secure an embedded volunteer dashboard

The Rock page and external reporting provider both authorize only the intended viewers.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `Block`

## Entities And Tables

- `Page`
- `Block`

## Steps

1. Identify the Rock page and report block.
2. Inspect Rock page and block authorization.
3. Define the intended security roles.
4. Verify the external reporting product’s licensing and identity requirements.
5. Test with an authorized user.
6. Test with an unauthorized user.
7. Confirm that direct report access cannot bypass the intended controls.
8. Review the displayed volunteer and financial fields for minimum necessary exposure.

## Do Not Assume

- Rock authorization grants a provider license.
- A provider license grants Rock-page access.
- A successful administrator test proves ordinary-user access.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications
- https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/RapidAttendanceEntry/RapidAttendanceEntryLocationsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/Enums/Blocks/Group/Scheduling/toolboxScheduleRowConfirmationStatus.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/Scheduling/GroupScheduler/groupSchedulerSendConfirmationsResponseBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/Scheduling/GroupScheduler/groupSchedulerLocationsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/GetScheduledLocationsResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/groupLocationsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
