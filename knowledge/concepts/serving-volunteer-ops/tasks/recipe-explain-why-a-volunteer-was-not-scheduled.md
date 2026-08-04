---
concept_id: serving-volunteer-ops
task_id: recipe-explain-why-a-volunteer-was-not-scheduled
title: Recipe: Explain Why A Volunteer Was Not Scheduled
generated: true
---

# Recipe: Explain Why A Volunteer Was Not Scheduled

Complete Explain Why A Volunteer Was Not Scheduled with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `Location`
- `Schedule`

## Entities And Tables

- `Group`
- `Location`
- `Schedule`

## Steps

1. group membership;
2. schedulable role;
3. schedule preferences;
4. availability/unavailability;
5. existing schedule conflicts;
6. group location schedule;
7. required role counts;
8. requirements;
9. manual exclusions;
10. auto-schedule settings;
11. scheduler warnings.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/10/266
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql
- https://community.rockrms.com/rocku/groups/group-types
- https://community.rockrms.com/rocku/groups/group-scheduling-overview
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://community.rockrms.com/rocku/groups/group-details
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs
- https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule
- https://community.rockrms.com/rocku/groups/group-security
