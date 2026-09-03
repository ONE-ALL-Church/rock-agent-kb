---
concept_id: scheduling-locations
task_id: recipe-evaluate-reservation-to-calendar-synchronization
title: Recipe: Evaluate Reservation-To-Calendar Synchronization
generated: true
---

# Recipe: Evaluate Reservation-To-Calendar Synchronization

The organization has a safe compatibility and ownership decision before implementing synchronization.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Schedule`
- `Workflow`
- `Attribute`

## Entities And Tables

- `Location`
- `Schedule`
- `Workflow`
- `Attribute`

## Steps

1. Confirm whether the Room Management plugin is installed.
2. Record its exact version and linkage schema.
3. Identify the community recipe that matches that generation.
4. Determine whether reservations or calendar occurrences are authoritative for schedule, location and contact fields.
5. Inspect existing reservation linkages and mismatches read-only.
6. Review all proposed Lava, workflow actions, SQL, routes and permissions.
7. Test in a non-production environment with reversible sample records.
8. Verify create, update, missing-link and mismatch cases.
9. Approve a production workflow only after security, performance and rollback review.
10. Confirm the Room Management plugin is installed and identify its version.
11. Identify the reservation and its explicit calendar linkage.
12. Compare schedule, location and contact fields without modifying either record.
13. Determine which record is authoritative under local policy.
14. Review the recipe generation and schema assumptions before running a workflow or SQL.
15. Stop before synchronizing if ownership, linkage or compatibility is ambiguous.

## Do Not Assume

- Rock core synchronizes reservations and calendars.
- An older custom attribute and a newer linkage table are interchangeable.
- A recipe’s embedded IDs, paths or table names apply locally.
- A mismatch tells the agent which record should win.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations
- https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations
- https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder
- https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor
- https://www.rockrms.com/releasenotes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs
- https://www.youtube.com/watch?v=edanHiYSDIM
- https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20
