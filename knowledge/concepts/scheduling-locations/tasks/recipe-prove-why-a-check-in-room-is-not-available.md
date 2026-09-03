---
concept_id: scheduling-locations
task_id: recipe-prove-why-a-check-in-room-is-not-available
title: Recipe: Prove Why A Check-In Room Is Not Available
generated: true
---

# Recipe: Prove Why A Check-In Room Is Not Available

Identify the first configuration, schedule, device, capacity, eligibility, or workflow filter that removes a specific room for a specific person and check-in attempt.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Check-in Configuration`
- `Person`
- `Device`
- `Group`
- `GroupLocation`
- `GroupLocationSchedule`
- `Location`
- `Schedule`
- `Workflow`

## Entities And Tables

- `Person`
- `Device`
- `Group`
- `GroupLocation`
- `Location`
- `Schedule`
- `Workflow`

## Decision Order

1. Reproduce the exact person, device, check-in configuration, campus, and Rock time.
2. Prove the room, group, and group-location-schedule chain is active and complete.
3. Prove the current schedule and device scope include that chain.
4. Evaluate person eligibility and room capacity against the same attempt.
5. Trace location-selection and workflow filters in execution order; stop at the first removal.
6. Check version-specific behavior only after current data and filter state are known.

## Read-Only Checks

- Read the Location record and parent path; record IsActive and any Check-In Manager open or closed state.
- Read the GroupLocation joining the expected Group and Location; confirm the link is not inferred from matching names.
- Read the schedule configuration on that GroupLocation and compare it with the current date and time.
- Read the Device location scope and check-in configuration used by the failing kiosk or workflow.
- Evaluate age, grade, ability, requirements, group membership, capacity threshold, and overflow rules for the exact person without changing them.
- Inspect the workflow action log or equivalent diagnostic state and record which filter first excluded the location.

## Related KB Results

- `concept:check-in`
- `model_map:stable:device`
- `model_map:stable:group`
- `model_map:stable:group-location`
- `model_map:stable:location`
- `model_map:stable:schedule`

## Steps

1. Record the exact check-in configuration, person, device, campus, occurrence, and current Rock time for one reproducible attempt.
2. Confirm the expected Location is active, open, and under the intended campus and building hierarchy.
3. Confirm the expected Group is active and included by the selected check-in configuration.
4. Confirm a GroupLocation record joins that exact Group and Location.
5. Confirm the GroupLocation schedule configuration includes the intended Schedule and occurrence.
6. Confirm the Schedule is active at the recorded Rock time, including start date, end date, weekly time, and exclusions.
7. Confirm the Device and kiosk configuration are allowed to display the expected location path.
8. Evaluate the person's age, grade, ability, requirements, group membership, and other eligibility rules for that occurrence.
9. Evaluate hard or soft capacity, room-closed state, overflow behavior, and location-selection strategy.
10. Trace Check-In workflow filters in configured execution order and capture the first filter whose input contains the room but whose output does not.
11. Compare the observed filter behavior with the cited Rock source and release caveats for the installed version.
12. Report the first proven exclusion, the supporting record IDs or public model references, and the smallest safe configuration correction; do not change production during diagnosis.

## Do Not Assume

- A room with the right name is linked to the intended group or schedule.
- An active Location is open for Check-In or visible to the current device.
- A schedule is active now merely because it exists on the group.
- A full room, eligibility failure, or workflow filter is the cause until the same attempt proves it.
- The last configured filter caused the removal; identify the first input-to-output transition.

## Source Links

- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryLocationsBag.d.ts
