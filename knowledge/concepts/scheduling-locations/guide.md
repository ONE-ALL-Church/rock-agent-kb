---
id: authored-scheduling-locations
title: Scheduling And Locations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Scheduling And Locations

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Scheduling And Locations index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Scheduling and Locations in Rock RMS are not a single feature. They are a shared operational layer used by check-in, group scheduling, attendance, events, mobile experiences, Lava content, and reservation workflows. The core pattern is simple: a `Schedule` answers *when*, a `Location` answers *where*, and linking tables such as `GroupLocation`, `GroupLocationSchedule`, and schedule-capacity configuration answer *which group or opportunity can use which place at which time*.

For agents doing real Rock work, the highest-value habit is to identify which scheduling surface is involved before troubleshooting:

- Check-in scheduling is driven by check-in configuration, group/location pairs, active schedules, device location scope, room status, thresholds, and workflow filters.
- Group scheduling is driven by group type scheduling settings, group locations, schedules, capacities, assignments, attendance records, RSVP or scheduling workflows, and person availability/preferences.
- Event calendars are driven by event items, event item occurrences, calendars, audiences, campuses, occurrence schedules, and Lava/mobile calendar rendering.
- Reservations are commonly handled through the Room Management plugin rather than Rock core. Reservation records, approval state, resources, room locations, and `ReservationLinkage` relationships may exist only if that plugin is installed and current.

When a schedule or location issue appears, do not start with broad assumptions. Inspect the live entity chain:

1. Identify the surface: check-in, group scheduling, calendar, reservation, LMS, mobile, or custom Lava.
2. Identify the expected `Schedule`, `Location`, `Group`, `Campus`, `Device`, `EventItemOccurrence`, or reservation record.
3. Confirm active/archive status and dates.
4. Confirm the linking rows that make the object available.
5. Confirm time behavior: Rock time zone, server time, schedule active window, exclusions, and effective start/end dates.
6. Confirm filters: check-in workflow filters, group type settings, campus context, audience/campus filters, schedule category exclusions, thresholds, and security.
7. Confirm version-specific behavior from release notes before treating an unexpected result as configuration error.

The most important source-backed operational warning is that schedules and locations are reused across contexts. A schedule can be attached to more than one group location, a location can sit in a hierarchy, a group can use multiple locations, and a check-in schedule builder can copy enabled locations between schedules. The NextGen check-in documentation specifically warns against deleting `GroupLocationSchedule` rows using only `ScheduleId` because the same schedule can be used in different check-in configurations; include the matching group/location context in any cleanup or repair operation ([Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42/350)).

## 2. Scope And Terminology

This guide covers the concept family called Scheduling And Locations:

- Locations, rooms, campuses, buildings, positions, addresses, and location hierarchy.
- Schedules, service times, schedule categories, recurring patterns, single-date schedules, effective dates, exclusions, check-in offsets, and display text.
- Group meeting details, group scheduler, schedule status board, person preferences, auto scheduling, RSVP, schedule cancellation, and attendance.
- Check-in scheduled locations, available rooms, overflow rooms, open/closed room state, room thresholds, device location scope, and location selection strategies.
- Event calendars, event item occurrences, calendar audiences, mobile event lists, iCalendar exports, and Lava calendar commands.
- Room reservations and reservation-to-calendar workflows where the Room Management plugin is installed.
- Operational reporting, version caveats, troubleshooting, and agent recipes.

Terms used throughout:

- **Location**: A Rock `Location` record representing a physical or logical place. It can be a campus, building, room, position, point, geofence, address, or other organization-specific place type. Rock documents Named Locations under check-in and describes them as hierarchical objects edited under Admin Tools > Check-in > Named Locations in check-in contexts ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).
- **Campus**: A Rock campus usually has a relationship to a location, and many scheduling views use campus as a filter or context. Event mobile blocks can accept `CampusGuid` or use campus context ([Calendar Event List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list)).
- **Schedule**: A Rock `Schedule` record describing a recurring or one-time time pattern. Schedules can be grouped in categories, selected by check-in and groups, used by Lava commands, exported as iCalendar, and referenced in APIs.
- **Group Location**: A link from a `Group` to a `Location`, often representing where a group meets or where a serving assignment occurs.
- **Group Location Schedule**: A link that says a specific group-location pair is active for a schedule. In check-in and group scheduling, this is the operational join that answers “this group at this location during this schedule.”
- **Attendance Occurrence**: A dated occurrence for a group/location/schedule combination, used for attendance, scheduling assignments, RSVP, and analytics.
- **Reservation**: In this guide, reservation usually means a Room Management plugin reservation unless a local Rock instance has a different reservation system. Verify the installed plugin, namespace, tables, and version before assuming a schema.
- **Resource**: In Room Management contexts, resources are items requested with rooms and may have approval routing separate from locations. The plugin schema and table names can differ by plugin version and vendor namespace.

## 3. Scheduling And Locations Mental Model

The mental model is a layered graph.

At the bottom, Rock has reusable primitives:

- `Location` records provide place identity.
- `Schedule` records provide time identity.
- Defined Values and Categories classify both of those records.
- Campuses connect ministry context to places and filters.
- Devices can be scoped to locations.

On top of those primitives, Rock builds feature-specific relationships:

- Check-in uses group types, groups, group locations, schedule builder rows, device location scope, and workflow filters to decide what a family can see.
- Group scheduling uses group types, group locations, schedules, capacities, assignments, and attendance occurrence rows to decide who is expected to serve.
- Events use event items, event item occurrences, calendars, audiences, campuses, and schedules to decide what appears on internal, external, mobile, or iCalendar surfaces.
- Reservations use plugin reservation records, reservation locations, reservation resources, approval state, and optionally calendar event linkages.

Think in triples: **group + location + schedule**. The source code names this directly. Rock has a `CheckInGroupLocationSchedule` object described as representing a group, location, and schedule combination for check-in ([CheckInGroupLocationSchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/CheckInGroupLocationSchedule.cs)). The schedule builder view models also carry group path, area path, location path, and active schedule identifiers for each group location ([GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs)).

For agents, the graph is more important than any single page. A room can exist and still not appear because:

- The room is inactive.
- The parent location hierarchy does not match the campus/device context.
- The group is inactive or archived.
- The group location exists but lacks the schedule row.
- The schedule exists but is inactive, excluded, out of effective range, or not currently active.
- The person fails age, grade, ability, requirement, or membership rules.
- The room is closed in Check-in Manager.
- The threshold filter removed or excluded the room.
- The location selection strategy auto-selected a room instead of presenting choices.
- A version-specific bug or behavior applies.

That is why a useful agent answer should usually list both the data path and the filters.

## 4. Source Authority And How To Use This Guide

Treat sources by authority and purpose:

1. **Official documentation and RockU** are the preferred authority for user-facing configuration paths and conceptual workflows. Use the check-in manuals for named locations, schedule builder, clone schedule, location selection strategy, thresholds, and check-in administration ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266), [Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42)).
2. **Source code and generated view models** are the preferred authority for entity relationships, block payload shape, workflow action behavior, and implementation landmarks. Use source links when the question depends on how the system filters, selects, or packages locations and schedules.
3. **Release notes** are the preferred authority for version caveats. They are especially important for check-in schedule/category exclusions, calendar exports, Group Scheduler UI behavior, schedule display text, and location tree bugs ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
4. **Developer and Lava docs** are the preferred authority for mobile blocks, Lava commands, iCalendar-style output, and safe rendering APIs ([Calendar Events Lava command](https://community.rockrms.com/lava/commands/calendar-events)).
5. **Community recipes** are useful examples, but they are contributed content. The recipe pages themselves warn that recipes are not reviewed or endorsed by the Rock core team. Use them as implementation patterns, not canonical behavior. Always verify permissions, plugin versions, Lava commands, table names, and performance before implementation.

When this guide says “verify in a live instance,” inspect the real record rather than inferring from documentation. In Rock work, similar labels can hide different IDs, inherited group type settings, inactive rows, archived groups, stale plugin tables, or custom Lava.

## 5. Core Configuration And Data Model

### Locations

Locations are edited through Named Locations in check-in contexts and are hierarchical. Official check-in documentation recommends building the hierarchy to match the structure of buildings and rooms ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). A practical hierarchy is often:

- Campus
- Building
- Area or floor
- Room
- Position or sub-room

Rock source and dev SQL examples show `Location` records with fields such as `Name`, `ParentLocationId`, `LocationTypeValueId`, `IsActive`, and `Guid`, with Location Type Defined Values for campus, building, and room ([Populate_LocationsAndGroupSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_LocationsAndGroupSchedules.sql)). Do not assume every instance uses the same hierarchy or location type list. Group type settings can constrain which location types are selectable for a group ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

Common location fields and concepts to inspect:

- `Id` and `Guid`
- `Name`
- `ParentLocationId`
- `LocationTypeValueId`
- `IsActive`
- Campus relationship, usually through `Campus.LocationId`
- Soft room threshold or capacity fields used by check-in
- Attributes such as approval group, room category, setup notes, room flags, or plugin-specific configuration
- Child locations
- Device-location links
- Group-location links
- Reservation-location links if Room Management is installed

Rock v18.3 fixed an Obsidian Location Detail issue where a location could be saved as its own parent or with a child as parent, breaking nested location loading. If a location tree fails to load or loops, inspect parent-child integrity and confirm the Rock version includes this fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Schedules

Schedules are reusable time definitions. They can represent weekly service times, one-time dates, ministry schedules, volunteer rotation templates, academic calendars, and event occurrence times. Rock documentation places schedules under Admin Tools > General Settings > Schedules for group scheduling setup ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)). Check-in schedule builder uses schedules to enable group/location pairs for check-in.

Fields and concepts to inspect:

- `Id` and `Guid`
- `Name`
- `Description`
- `iCalendarContent`
- `EffectiveStartDate`
- `EffectiveEndDate`
- `CategoryId`
- `WeeklyDayOfWeek`
- `WeeklyTimeOfDay`
- `StartTime` and `EndTime` in newer views or reporting examples
- `IsActive`
- `CheckInStartOffsetMinutes`
- Schedule category exclusions
- Friendly schedule text
- Next start date/time and active state in Lava/mobile contexts

Rock schedules often store recurrence information in iCalendar-style content. The Lava `calendarevents` command exists partly because recurring events can be difficult to query directly and performantly with raw SQL or basic entity commands ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)).

### Groups, Group Locations, And Schedules

The core join pattern is:

- `Group`
- `GroupLocation`
- `Location`
- `GroupLocationSchedule`
- `Schedule`

A source SQL view shows the basic join from `Schedule` to `GroupLocationSchedule`, then `GroupLocation`, then `Group` and `Location` ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)). That is the first join chain agents should inspect when a group appears to be missing a time or room.

Group type settings determine what kinds of locations can be assigned and how attendance/check-in rules behave. The Groups documentation lists concepts such as location types, location selection modes, group attendance requiring location, group attendance requiring schedule, check-in rules, and group scheduling options ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

For sign-up and scheduling capacity, inspect `GroupLocationScheduleConfig` if present. A community Sign-Ups reference uses `GroupLocation`, `GroupLocationScheduleConfig`, `Schedule`, and `GroupMemberAssignment` to reason about available slots and participant counts ([Reference for Sign-Ups](https://community.rockrms.com/recipes/531/Schedule-WithAvailableSlots)). Because this is a community recipe, verify the schema in the live instance before relying on exact fields.

### Attendance And Assignments

Group scheduling and check-in ultimately touch attendance. The `LoadSchedules` workflow action looks for attendance records where a person was scheduled or requested to attend for today, with `Occurrence.GroupId`, `Occurrence.LocationId`, and `Occurrence.ScheduleId` populated, when a group requires scheduling for check-in ([LoadSchedules.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs)). That is a useful implementation clue: when troubleshooting “scheduled person cannot check in,” inspect today’s attendance occurrences and assignment records, not just schedule setup.

Common tables and objects to inspect:

- `AttendanceOccurrence`
- `Attendance`
- `GroupMember`
- `GroupMemberAssignment`
- `GroupLocation`
- `GroupLocationSchedule`
- `Schedule`
- `Location`

## 6. Primary Entities And Relationships

### Location Entity

`Location` is both physical and logical. It can represent a room, campus, building, address, position, point, or geofence depending on group type settings and location type. The group documentation says group type location selection can include named locations, addresses, points, geofences, and group member addresses ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

Important relationships:

- `Location.ParentLocationId` creates hierarchy.
- `Campus.LocationId` maps a campus to a location.
- `GroupLocation.LocationId` maps a group to a location.
- `DeviceLocation.LocationId` scopes check-in devices.
- Reservation plugin location tables map reservations to locations.
- Event item occurrences may store location text or campus/location context depending on the event surface.

### Schedule Entity

`Schedule` is reusable and can be attached in several contexts:

- Check-in service times.
- Group meeting details.
- Group scheduler opportunities.
- Event item occurrences.
- Lava scheduled content and countdowns.
- Mobile blocks and utility commands.
- System jobs through cron expressions, though job scheduling is not the same as Rock `Schedule`.

Community examples use schedules for content countdowns and mobile redirects by checking next occurrence and active state ([Content Countdown Shortcode](https://community.rockrms.com/recipes/247), [Mobile App Countdown to Page Refresh or Redirect](https://community.rockrms.com/recipes/402)). Use those as examples of the concept, but verify Lava commands enabled and performance.

### GroupLocation

A `GroupLocation` is the place assignment for a group. It is central for:

- Group details.
- Group attendance.
- Check-in.
- Group scheduling.
- Sign-ups.
- RSVP occurrences.

The RockU Groups track explicitly includes Group Location, Group Scheduling - Meeting Details, Group Scheduler and Status Board, Person Preferences and Auto Schedule, and Group Scheduling Analytics as related training topics ([Groups RockU](https://community.rockrms.com/rocku/groups)).

### GroupLocationSchedule

`GroupLocationSchedule` is the schedule enablement row for a group-location pair. It answers: “Is this group allowed to use this location at this scheduled time?” In check-in, the schedule builder UI packages this as group path, area path, location path, and schedule IDs ([ScheduledLocationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs)).

Do not delete or repair these rows casually. The NextGen check-in docs explicitly warn that deleting by schedule alone can affect multiple check-in configurations; match group and location as well ([Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42/350)).

### GroupLocationScheduleConfig

This configuration layer appears in Sign-Ups and capacity-oriented scheduling. Community examples show fields such as minimum, desired, and maximum capacity, configuration name, location ID, schedule ID, and group location ID ([Reference for Sign-Ups](https://community.rockrms.com/recipes/531/Schedule-WithAvailableSlots)). Because Sign-Ups and related models evolve, verify the exact model in the installed Rock version.

### EventCalendar, EventItem, EventItemOccurrence

Event calendar surfaces use a different chain than check-in and group scheduling:

- Event calendars group events for display.
- Event items carry event identity, approval status, calendars, attributes, and audiences.
- Event item occurrences represent scheduled instances, usually pointing to a schedule.
- Mobile and Lava blocks render occurrences using campus, audience, calendar, and date filters.

The mobile Calendar Event List block accepts optional campus filtering and has settings for Calendar, Detail Page, Event Template, Day Header Template, Enable Campus Filtering, and Show Past Events ([Calendar Event List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list)). The Lava `calendarevents` command returns summary `EventScheduledInstances` with fields such as event occurrence, name, date/time, campus, location, calendar names, and audience names ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)).

### Reservation Entities

Room Management reservations are not covered as Rock core entities in the provided source material. The community recipes depend on the Room Management plugin from the Rock Shop and reference plugin tables and objects such as reservations, reservation locations, reservation resources, approval states, and reservation linkages ([Room Management Calendar View](https://community.rockrms.com/recipes/112), [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)).

For any reservation task, first verify:

- Is the Room Management plugin installed?
- Which vendor namespace and table prefix is used?
- Which plugin version is installed?
- Does the plugin include native event linkage?
- Is `ReservationLinkage` present?
- Are records in draft, pending, approved, denied, or another state?
- Are approval groups configured on locations, resources, reservation types, or attributes?

Older recipes reference CentralAZ plugin table names; newer recipes note moving away from `centralaz` tables toward BEMA Services table names and using `ReservationLinkage` instead of storing an event occurrence ID on the reservation ([Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444)).

## 7. Common Scheduling And Locations Workflows

### Add A New Check-In Room

1. Create or find the correct parent location under Named Locations.
2. Add the room as an active child location with the correct location type.
3. Set threshold values if the check-in process uses thresholds.
4. Add the location to the correct check-in group or group type configuration.
5. Open the check-in configuration schedule builder.
6. Enable the group/location pair for the desired schedules.
7. Confirm device location scope includes the campus/building/location path needed for the kiosk.
8. Run check-in in test mode or off-hours and inspect the selected family/person path.

Official docs describe locations as tied to check-in groups and enabled through schedules ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). Source code confirms check-in loads locations from active kiosk group/location relationships and filters them from there ([LoadLocations.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs)).

### Clone A Check-In Schedule

NextGen check-in documentation describes a Clone Schedule action that copies enabled locations from a source schedule to a destination schedule in the schedule builder ([Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42/350)). Use this when adding a new service time similar to an existing one.

After cloning, verify:

- Source schedule and destination schedule IDs are correct.
- Only intended group/location rows were copied.
- Overflow locations were scheduled if needed.
- Archived or inactive groups are not appearing in scheduled times.
- The new schedule has valid effective dates and active status.
- Check-in start offsets match operational expectations.

Rock v17.0 added the ability to copy enabled check-in locations from one schedule to another, and v18.3 fixed scheduled times listing archived or inactive groups that still had `GroupLocationSchedule` rows ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Configure Group Scheduling

A minimal group scheduling setup usually requires:

1. A group type with scheduling enabled.
2. Location schedules enabled for that group type.
3. Location types allowed for that group type.
4. One or more groups using that group type.
5. Group locations attached to each group.
6. Schedules attached to those group locations.
7. Capacities set where appropriate.
8. Group members in scheduleable roles.
9. Person preferences and unavailable dates configured if auto scheduling is used.
10. Schedule coordinator or cancellation workflow configured if notifications are desired.

A community Pastor of the Day example captures the core pattern: create a schedule, configure a group type with location schedules and scheduling enabled, create a group, add a group location, attach the schedule, and set capacities ([Pastor of the Day Scheduling](https://community.rockrms.com/recipes/414)). The official Groups documentation and RockU Group Scheduling lessons should be the authority for exact UI behavior ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296), [Group Scheduler and Status Board](https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board)).

### Create Event Calendar Occurrences

For calendar event work:

1. Confirm the calendar and event item.
2. Confirm approval status if the surface filters pending/unapproved events.
3. Confirm event item occurrence schedule.
4. Confirm campus and audience filters.
5. Confirm Lava/mobile block configuration.
6. Confirm whether specific-date schedules or recurrence patterns export correctly in the installed version.

The event registration RockU track includes Calendar Overview, Calendars and Events, Linkages, and iCalendar Feed lessons, indicating that calendars, event item occurrences, and linkages are distinct concepts ([Calendar Overview](https://community.rockrms.com/rocku/event-registration/calendar-overview)). For Lava rendering, prefer `calendarevents` rather than hand-querying recurrence patterns unless you have a tested reason ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)).

### Manage Room Reservations

If the Room Management plugin is installed:

1. Confirm the reservation record and approval state.
2. Confirm reservation locations and resources.
3. Confirm administrative and event contacts.
4. Confirm approval groups and outstanding approval items.
5. Confirm schedule and location consistency.
6. Confirm whether a reservation is linked to a calendar event through native linkage.
7. Use plugin-provided reports and views where possible.
8. Avoid raw SQL updates unless reviewed and tested.

Community patterns include adding a calendar view to reservations, daily facility reports, iCal feeds, dashboard approval lists, and reservation-calendar sync tooling ([Room Management Calendar View](https://community.rockrms.com/recipes/112), [Room Management - Daily Email Reports for Facilities Team](https://community.rockrms.com/recipes/198), [Add 'My Reservation Approvals' To Dashboard](https://community.rockrms.com/recipes/178)). Treat them as examples, not guaranteed-safe recipes.

## 8. Locations Deep Dive

### Hierarchy

Location hierarchy should match operational navigation. For check-in, common hierarchy is campus > building > room. For serving teams, it can be building > position. The Groups documentation explicitly notes that group scheduling may use locations for non-room positions such as lobby areas, greeter stations, audio, or piano, and that additional Location Types are Defined Values ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296)).

A good hierarchy supports:

- Device scoping.
- Campus-specific filtering.
- Human-readable paths in schedule builder and manager screens.
- Reporting by campus, building, area, or room.
- Reservation approval by room or parent area.
- SEO/location pages for public campus information.

### Location Types

Location Types are Defined Values. Typical types include Campus, Building, Room, but local instances often add Position, Area, Venue, Classroom, Office, or Ministry Zone. Before creating locations, inspect:

- Defined Type: Location Type.
- Group type allowed location types.
- Existing naming conventions.
- Whether campus records already point at location records.
- Plugin attributes attached to `Location`.

Do not add a new type merely because a label sounds better. If check-in or group type filters expect Room, a custom type may not appear where staff expect.

### Active State And Open/Closed State

`Location.IsActive` is a core record state. Check-in also has operational open/closed room status. Source view models show `LocationStatusItemBag` with an `IsOpen` flag for admin screens ([LocationStatusItemBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/LocationStatusItemBag.cs)). Release notes say v17.0 updated room open/close logic to write changes to history ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When a room does not appear, distinguish:

- Location record inactive.
- Room closed for check-in.
- Location not assigned to the group.
- Group/location not enabled for the schedule.
- Device cannot see that location.
- Threshold or selection strategy filtered the location.
- User is blocked by group eligibility.

### Thresholds And Capacity

Rock check-in has threshold logic for rooms. Official and source-backed concepts distinguish soft threshold behavior from strict enforcement. The source `FilterLocationsByThreshold` action removes or excludes locations when the current count reaches the location’s soft threshold, unless the person is already in that location’s attendance set ([FilterLocationsByThreshold.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByThreshold.cs)). A community recipe recommends configuring room threshold values and optionally changing workflow behavior to avoid silently hiding full rooms early in the check-in flow ([More User-Friendly Room Thresholds](https://community.rockrms.com/recipes/213)).

For operational checks:

- Inspect the room’s threshold fields.
- Inspect the current attendance count.
- Inspect whether the workflow action removes or marks excluded locations.
- Inspect final Save Attendance strict threshold behavior.
- Inspect Check-In Manager room counts.
- Test both an unscheduled/new attendee and an attendee already checked into the room.

### Location Selection Strategy

Rock has three location selection strategies in source: Ask, Balance, and Fill In Order ([LocationSelectionStrategy.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/CheckIn/LocationSelectionStrategy.cs)). Documentation describes similar behavior: ask the person, load balance across rooms, or fill rooms in configured order ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

The workflow action for location selection strategy applies to family check-in and assumes locations have already been filtered by schedule. It skips filtering when a manager is logged in, because a manager should see an unbalanced list and choose intentionally ([FilterLocationsByLocationSelectionStrategy.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs)).

If staff ask why the kiosk did not offer a room choice, inspect the location selection strategy before assuming the room is missing.

### Device Location Scope

Check-in devices can be associated with locations. Source SQL examples show `DeviceLocation` linking devices and locations ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)). Official docs also mention printers can be set for devices or locations in check-in contexts ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

When troubleshooting kiosk visibility:

- Confirm the device record.
- Confirm device type and campus/location context.
- Confirm `DeviceLocation` rows.
- Confirm the selected check-in configuration.
- Confirm the kiosk client is using the expected device.

### Location SEO And Public Pages

Locations also matter outside operations. A community SEO recipe recommends consistent name/address/phone information for each campus, separate campus landing pages, and structured data where appropriate ([Succeeding with Google Local Pack in a Rock Website](https://community.rockrms.com/recipes/83)). Treat this as marketing guidance rather than Rock core behavior, but it is operationally relevant when campus pages, calendars, and event locations disagree.

## 9. Schedules Deep Dive

### Schedule Categories

Schedules can be organized into categories. Source code for the legacy check-in scheduled locations block limits schedules to active schedules with `CheckInStartOffsetMinutes` and the service times category (`SCHEDULE_SERVICE_TIMES`) when adding schedule columns ([CheckinScheduledLocations.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs)). That means a schedule may exist but not appear in a particular admin surface if category or offset expectations are not met.

For any missing schedule:

- Confirm `IsActive`.
- Confirm category.
- Confirm effective date range.
- Confirm check-in start offset if applicable.
- Confirm it is linked to the group/location pair.
- Confirm schedule category exclusions.
- Confirm the block or workflow actually reads that schedule category.

### Effective Dates And Recurrence

Schedules can represent recurring or specific-date occurrences. Release notes include several schedule behavior fixes:

- v17.1 fixed `EffectiveEndDateTime` logic when a schedule duration passes midnight, aligning it better with iCal `DTEND` behavior ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v18.3 improved friendly text for single-date schedules ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- v16.4 improved calendar export support for specific-date schedules in Microsoft, Google, and Apple calendar apps ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

If a schedule crosses midnight, exports oddly, or displays confusing text, verify the Rock version before debugging custom code.

### Check-In Start Offsets

Check-in schedules can include start offsets. The check-in scheduled locations block filters to schedules with `CheckInStartOffsetMinutes` for one legacy schedule setup flow ([CheckinScheduledLocations.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs)). In live checks, inspect whether the expected schedule has an offset configured and whether the current time is inside the check-in window.

A community troubleshooting recipe emphasizes checking the schedule grid, server time, Rock time, and whether the schedule is active ([Troubleshooting Check-in Schedule Problems](https://community.rockrms.com/recipes/280)). Use that as a practical branch, but confirm current UI paths in the installed version.

### Schedule Exclusions

Schedules and schedule categories can have exclusions. Release notes highlight multiple exclusion-related fixes:

- v16.6 fixed group schedule notifications and reminders not honoring schedule exclusions.
- v17.1 fixed legacy check-in not checking schedule categories for exclusions.
- v18.3 and later sources include several check-in schedule display fixes.

Use exclusions when groups do not meet during holidays or breaks, but always verify whether the exclusion is on the schedule itself, the category, or the group type. If notifications or check-in availability ignore an exclusion, check the Rock version and release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Schedule Templates And Preferences

Group member schedule templates support volunteer preferences and auto scheduling. A community recipe notes that core templates may not include fifth Sundays and recommends naming templates by weekday for clarity, because a template schedule identifies the day of week it applies to ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)). Treat the specific pattern as community guidance, but the operational point is strong: template names should make the weekday and recurrence obvious to staff and volunteers.

For auto scheduling:

- Inspect group member schedule preferences.
- Inspect unavailable dates.
- Inspect group role requirements.
- Inspect group/location/schedule capacities.
- Inspect fifth-week or “last week” edge cases.
- Confirm the installed version includes any relevant auto schedule bug fixes. Triumph summarized a v16.9 highlight for an issue where Auto Schedule did not honor “Every Other Week” preferences in v16.7 ([GitHub Spotlight 2/6/2025](https://www.triumph.tech/resources/github-spotlight-262025)); verify against official release notes and installed version before acting.

### Schedule Builder Field Type

Rock v19.1 added a Schedule Builder Field Type and Attribute that lets administrators create and select custom schedules using the standard Schedule Builder interface ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Because v19.1 was listed as beta in the hydrated release notes, verify availability and stability in the live instance before designing production workflows around it.

## 10. Reservations Deep Dive

Reservations in this source pack mainly refer to the Room Management plugin, not Rock core. Many organizations use the plugin for room requests, approvals, setup notes, resources, reports, and calendar integration. Agents must treat reservation behavior as plugin-specific until verified.

### Reservation Lifecycle

A typical reservation lifecycle is:

1. Requester creates a reservation.
2. Reservation may be saved as draft.
3. Reservation is submitted for approval.
4. Location approvals and resource approvals are collected.
5. Facilities or ministry staff review setup details.
6. Reservation is approved, denied, changed, or canceled.
7. Optional calendar event linkage is created or updated.
8. Optional iCal or daily reports notify staff.

A community recipe highlights a draft problem where users thought reservations were submitted but the submit button was missed. Their mitigation was a dashboard/list of drafts and a detail warning for draft reservations ([Room Management Drafts](https://community.rockrms.com/recipes/418)). Use this as an operational pattern: if reservation volume is high, surface drafts and pending approval states directly.

### Approvals

Approval routing can depend on reservation type, location approval groups, resource approval groups, super-admin groups, and plugin-specific state. The “My Reservation Approvals” recipe uses a Dynamic Data block to list reservations needing approval by the current person, including location and resource approvals ([Add 'My Reservation Approvals' To Dashboard](https://community.rockrms.com/recipes/178)). Because the SQL references older plugin tables and attributes, do not copy it directly into a modern instance without mapping the current plugin schema.

Operational checks:

- Which approval state means draft, pending, approved, denied?
- Are location approval groups stored as location attributes?
- Are resource approval groups stored on resource records?
- Does a super-admin group bypass location/resource approver checks?
- Are approval states per reservation, per location, and per resource?
- Is the current person a member of the approval group?
- Are group member statuses active?

### Reservation Calendar Views

Community examples add calendar views to Room Management using FullCalendar and reservation summaries ([Room Management Calendar View](https://community.rockrms.com/recipes/112)). This is useful for staff, but verify:

- FullCalendar version and CDN policy.
- Lava command permissions.
- Reservation summary object shape.
- Approval-state color coding.
- Time zone display.
- Date range performance.
- Mobile rendering.
- Whether native plugin views now cover the need.

### Reservation To Event Calendar Linkage

Older recipes created calendar events and stored links manually. Newer recipes emphasize native Room Management event linkage and the `ReservationLinkage` table. One update specifically says to use `ReservationLinkage` rather than event item occurrence ID from the reservation when syncing or querying ([Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444)). A later tool recipe adds a details panel to show missing or mismatched linkages and offers workflow buttons to sync schedule, location, or contact information ([Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)).

Agent rule: if reservation and calendar are out of sync, first inspect linkage records. Do not assume the reservation stores the authoritative event occurrence ID.

### Reservation iCal Feeds

Community examples create room-specific or campus-specific iCal feeds via workflows, generated files, or Lava webhooks ([Room Management iCal Subscriptions](https://community.rockrms.com/recipes/231), [Room Management iCal Feed by Campus](https://community.rockrms.com/recipes/409)). These patterns are operationally useful but high-risk if implemented carelessly:

- iCal output must be valid.
- Time zone handling must be tested in Outlook, Google Calendar, and Apple Calendar.
- Query performance must be bounded.
- Public feed URLs must not leak private reservation details.
- Feed ownership and sharing behavior must be clear.
- Plugin schema and v14+ workflow differences must be verified.

A more general community recipe creates `.ics` files through a Lava Webhook with `text/calendar` response type and parameters for dates, times, location, and description ([Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540)). Use it as a pattern, not a guarantee.

## 11. Related Rock Areas: Check In, Groups, Events, Cms

### Check-In

Check-in is the most schedule-location-sensitive part of Rock. Official docs say locations are tied to check-in groups and enabled through schedules ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). NextGen docs add overflow locations, clone schedules, schedule builder behavior, and a warning about deleting schedule rows by schedule alone ([Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42/350)).

Important check-in branches:

- Legacy vs NextGen check-in.
- Check-in type/configuration selected by kiosk.
- Areas and groups.
- Group eligibility.
- Schedule selection.
- Location selection.
- Device/printer/location context.
- Check-In Manager open/close and roster filters.
- Labels and attendance analytics.
- Mobile check-in setup.

Release notes include check-in schedule-related fixes: v17.0 location-copying, v17.1 schedule category exclusions, v17.5 schedule select wrapping, v18.3 inactive/archived group schedules excluded from scheduled times, and location tree fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Groups

Groups use schedules and locations for meeting details, attendance, scheduling, RSVP, and volunteer operations. RockU Groups lists dedicated lessons for Group Location, Group Scheduling Overview, Meeting Details, Scheduler and Status Board, Person Preferences and Auto Schedule, Scheduling Analytics, RSVP, and scheduling communications ([Groups](https://community.rockrms.com/rocku/groups)).

Group type settings are key. Inspect:

- Scheduling enabled.
- Enable location schedules.
- Location types.
- Attendance requires location.
- Attendance requires schedule.
- Group attendance rules.
- Check-in rule.
- Role schedule eligibility.
- Requirements.
- Exclusion dates.
- Schedule cancellation workflow.
- Schedule coordinator.

Release notes add and fix group scheduling features such as Group Schedule Coordinator notifications in v16.7, duplicate calendar feed fixes in v16.0, Group Scheduler orientation improvements in v19.1, and capacity deletion fixes in v17.2 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Events

Events use schedules differently than check-in. An event occurrence may point to a schedule, and calendar output often needs recurrence expansion. Use Event Calendar blocks, mobile blocks, and Lava commands rather than raw recurrence SQL when possible. The mobile Calendar View and Event Item Occurrence List blocks accept campus context, audience, calendar, date range, and max occurrence settings ([Calendar View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-view), [Event Item Occurrence List By Audience Lava](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava)).

For one event with multiple campuses, the provided Q&A has an unanswered question about one calendar instance with multiple locations ([One Calendar Instance - Multiple Locations](https://community.rockrms.com/ask/using/2820)). Do not infer a canonical solution from that page. In a live instance, inspect whether separate event item occurrences, campus filters, event calendars, audiences, or custom Lava are the right implementation.

### CMS And Lava

CMS and Lava use schedules for conditional content, countdowns, calendar displays, staff calendars, and webhook outputs. Prefer built-in Lava commands and block merge fields where possible:

- `calendarevents` for event scheduled instances ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)).
- Scheduled content shortcodes or commands for live/not-live content, if enabled and appropriate.
- Mobile blocks for app-native calendar views.
- Lava webhooks for iCal only with careful security review.

Community examples show staff internal calendars with approval and calendar badges, schedule countdown bars, Google Calendar holiday requests, and workflow-to-calendar ideas ([Staff Calendar enhancement](https://community.rockrms.com/recipes/484), [Countdown to next Online Service](https://community.rockrms.com/recipes/165), [US Holidays Web Request](https://community.rockrms.com/recipes/499), [Workflow Form to Event to Visual Calendar](https://community.rockrms.com/recipes/504)).

## 12. Administration And Operational Guardrails

### Naming Conventions

Use names that encode operational meaning:

- Schedules: `Sunday 9:00 AM`, `Sunday 11:00 AM`, `Wednesday Youth 6:30 PM`, `1st and 3rd Sunday`, not ambiguous labels like `Early`.
- Locations: include parent hierarchy rather than repeating campus in every room if the tree already communicates it.
- Group locations: keep display order intentional.
- Schedule templates: include weekday and recurrence pattern.
- Reservation views: name by purpose, such as `Calendar`, `Pending Facility Approval`, `Upcoming Setup`.

Community guidance on fifth-week schedule templates specifically warns that a template schedule identifies the weekday and should be named clearly ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)).

### Security

Scheduling and locations often expose sensitive operational data:

- Kids room counts.
- Volunteer assignments.
- Internal staff schedules.
- Facility usage.
- Contact information.
- Reservation notes and setup diagrams.
- Calendar feeds.

Before adding Lava or Dynamic Data blocks, confirm:

- Page security.
- Block security.
- Lava command permissions.
- Entity command access.
- SQL command access.
- External route access.
- Whether output is cached.
- Whether the block is on internal or external site.
- Whether URLs include predictable IDs or GUIDs.

A group viewer meeting details recipe explicitly reminds implementers to set security because links go to schedule and location settings pages ([Group Viewer Meeting Details Accordion](https://community.rockrms.com/recipes/500)).

### Avoid Raw SQL Writes Unless Necessary

Many community recipes use SQL. For agents, read-only SQL is valuable for diagnosis, but write SQL is high risk. Prefer:

- Rock UI.
- Core services.
- Workflow actions.
- Plugin APIs or documented workflows.
- Lava entity commands only when safe and reviewed.
- SQL writes only with a tested rollback plan, exact predicates, and version/schema confirmation.

This is especially important for `GroupLocationSchedule`, schedule records, event occurrence schedules, and Room Management plugin linkage rows.

### Cache And Time

Schedule issues often look like logic errors but are really time or cache issues. The check-in schedule troubleshooting recipe recommends checking schedule configuration, server/Rock time, schedule active state, and keeping cache clearing as a low-cost tool ([Troubleshooting Check-in Schedule Problems](https://community.rockrms.com/recipes/280)).

For time-sensitive issues, inspect:

- Rock organization time zone.
- Server time zone and clock.
- SQL server time if separate.
- Schedule effective start/end.
- Check-in start offset.
- Current schedule active state.
- Browser/device time only if client-side countdowns are involved.
- Calendar export time zone behavior.

### Version Guardrails

Before changing behavior, identify:

- Rock version.
- Legacy vs NextGen check-in.
- Obsidian vs WebForms block.
- Plugin version.
- Mobile app version if mobile blocks are involved.
- Whether the release note fix is in the installed build.

Do not use v19.1 beta-only features in production guidance without calling out the version requirement.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Check-In Source Landmarks

Key implementation landmarks:

- `CheckInGroupLocationSchedule.cs`: a POCO for group/location/schedule combination in check-in ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/CheckInGroupLocationSchedule.cs)).
- `LocationAndScheduleBag.cs`: defines location/schedule pairs used to indicate valid locations for a group because a location might only be valid during one schedule ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/CheckIn/LocationAndScheduleBag.cs)).
- `LoadLocations.cs`: adds active kiosk locations to groups during check-in state loading ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs)).
- `LoadSchedules.cs`: loads schedules and checks schedule-required attendance records ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs)).
- `FilterLocationsBySchedule.cs`: removes or marks schedules not selected by the person ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsBySchedule.cs)).
- `FilterActiveLocations.cs`: removes or excludes inactive/unavailable locations ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterActiveLocations.cs)).
- `FilterLocationsByThreshold.cs`: removes or excludes rooms at soft threshold ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByThreshold.cs)).
- `FilterLocationsByLocationSelectionStrategy.cs`: auto-selects locations according to strategy after schedule filtering ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs)).
- `LocationSelectionStrategy.cs`: enum values Ask, Balance, Fill In Order ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/CheckIn/LocationSelectionStrategy.cs)).

### Schedule Builder View Models

The check-in schedule builder and kiosk admin screens use bags with group path, area path, location name/path, group location encrypted ID, and schedule IDs ([GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs), [ScheduledLocationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs)). These are useful for understanding UI behavior: the UI is editing schedules attached to group locations, not editing schedules in isolation.

### Group Scheduler View Models

Group Scheduler view models expose selected and available locations and unique ordered location/schedule names ([GroupSchedulerLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs), [GroupSchedulerGroupLocationScheduleNamesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs)). Use these when diagnosing Obsidian Group Scheduler behavior or API payload expectations.

### Lava Commands

Use `calendarevents` when rendering upcoming calendar events. It accepts calendar ID and optional max occurrences, date range, audience IDs, campus IDs, and start date; it returns `EventScheduledInstances` summaries ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events)). This is generally safer than trying to expand iCalendar recurrence manually in SQL for display.

### Mobile Blocks And Commands

Mobile event-related blocks include:

- Calendar Event List, with calendar, detail page, templates, campus filtering, and past-event settings ([Calendar Event List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list)).
- Calendar View, with campus context query string and calendar presentation merge fields ([Calendar View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-view)).
- Event Item Occurrence List By Audience Lava, with audience, calendar, campuses, date range, max occurrences, event detail page, Lava template, and enabled Lava commands ([Event Item Occurrence List By Audience Lava](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava)).
- Schedule Unavailability, for mobile group scheduling unavailable dates; mobile v4.0 and core v13.3 are noted in the docs ([Schedule Unavailability](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-unavailability)).
- AddEventToCalendar utility command for adding one-time event details to the user’s default calendar; verify mobile version support and required parameters in the live docs ([Utility Commands](https://community.rockrms.com/developer/mobile-docs/essentials/commands/utility-commands)).

## 14. Reporting, Analytics, And Model Map

### Basic Relationship Queries

For diagnosis, the simplest model-map query is:

- Schedule -> GroupLocationSchedule -> GroupLocation -> Group and Location.

The source dev SQL shows exactly that join ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)). Use it read-only to answer:

- Which groups use this schedule?
- Which locations are enabled for this schedule?
- Which schedules are attached to this group/location?
- Is the expected link row missing?

For check-in devices, inspect `DeviceLocation` joins to confirm which locations a device can see.

### Schedule Status Board

The Group Schedule Status Board is a staff-facing operational view. Community recipes add print and export buttons to the board ([Group Schedule Status Board Print Button](https://community.rockrms.com/recipes/201), [Export Schedule Status Board to Excel](https://community.rockrms.com/recipes/174)). These are useful patterns when staff need offline schedules, but first evaluate whether built-in export/reporting is now available in the installed version.

### Scheduling Analytics

RockU includes Group Scheduling Analytics as a dedicated topic ([Group Scheduling - Analytics](https://community.rockrms.com/rocku/groups/group-scheduling-analytics)). For agents, analytics questions usually require distinguishing:

- Scheduled to attend.
- Requested to attend.
- Confirmed.
- Declined.
- Attended.
- No-show.
- Unavailable.
- Unfilled capacity.
- Assignment by group, role, location, schedule, and date.

Do not collapse these into one “scheduled” count without verifying the fields used.

### Data Views

Release notes say v17.5 added a filter by Group Location Schedules to target more specific people based on their schedule for a group or sign-up project in a data view ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). That is important for agents writing communication or reporting recipes. Prefer native Data View filters where available over custom SQL embedded in Dynamic Data blocks.

### Facilities Reporting

Room Management community examples include daily PDF/email reports for facilities teams and approval dashboard blocks ([Room Management - Daily Email Reports for Facilities Team](https://community.rockrms.com/recipes/198), [Add 'My Reservation Approvals' To Dashboard](https://community.rockrms.com/recipes/178)). Use these patterns to design operational reports, but verify plugin schema and avoid exposing sensitive setup diagrams or contact details to broad audiences.

## 15. Version And Release Caveats

Important version-specific notes from the source pack:

- **v19.1 beta, May 20, 2026**: Added Schedule Builder Field Type and Attribute for custom schedules; improved Group Scheduler orientation by keeping occurrence date and schedules fixed while scrolling and showing group name above each location ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v18.3 alpha, May 20, 2026**: Fixed Obsidian Location Detail parent/child self-reference issue; improved friendly schedule text for single-date schedules; fixed scheduled times list excluding schedules from archived/inactive groups with lingering `GroupLocationSchedule` rows ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v17.5**: Added Group Location Schedules data view filter; improved Next-Gen check-in schedule select wrapping; fixed EventScheduledInstance Lava command behavior in Calendar Item List and Calendar Item Occurrence List blocks after security changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v17.2**: Fixed removal of a schedule from one group location deleting capacity settings for the same schedule in other group locations; improved group schedule ICS summaries to use group-location-schedule clarity ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v17.1**: Fixed legacy check-in schedule category exclusions and schedule effective end datetime for schedules crossing midnight ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v17.0**: Added copying enabled check-in locations from one schedule to another; updated room open/close logic to write to history ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v16.7**: Added Group Schedule Coordinator notifications when a person accepts, declines, or self-schedules for a group schedule occurrence ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v16.6**: Fixed group schedule notifications and reminders not honoring schedule exclusions ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v16.4**: Improved calendar export support for specific-date schedules in major calendar apps ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v16.0**: Fixed duplicate group schedule calendar feed entries; NextGen check-in docs also note clone schedules and grade/age matching behavior updates ([Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42)).
- **v15.2**: Updated SignUpFinder schedule filter display for schedules with multiple dates ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **v14.0**: Check-In Manager Roster can be filtered by schedule and checkout security changed in check-in documentation ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Always verify the exact installed Rock version and whether the instance is using legacy or Obsidian/NextGen blocks. Release note timing in the source pack includes alpha/beta labels; production instances may not have those fixes yet.

## 16. Implementation Playbooks

### Playbook: New Service Time For Check-In

1. Create or confirm the new service `Schedule`.
2. Put it in the expected service times category.
3. Configure check-in start offset and active/effective dates.
4. Use Clone Schedule from an existing similar schedule if available.
5. Review all copied group/location rows.
6. Add or remove rooms intentionally by campus and age/grade area.
7. Confirm overflow locations if using NextGen overflow.
8. Confirm location selection strategy.
9. Test as a family with expected ages/grades.
10. Test device context at each campus.
11. Verify Check-In Manager schedule filter.
12. Verify labels and room counts.

Citations: clone schedule and schedule builder guidance are in NextGen check-in docs ([Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42/350)); source code shows how schedules and locations are loaded and filtered ([LoadLocations.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs), [LoadSchedules.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs)).

### Playbook: New Serving Team Scheduling Setup

1. Confirm or create group type.
2. Enable scheduling.
3. Enable location schedules.
4. Add allowed location type, often Meeting Location or Position.
5. Create or select locations/positions.
6. Create or select schedules.
7. Create group.
8. Add group location and attach schedules.
9. Set capacities.
10. Add members in roles.
11. Confirm role eligibility for check-in or scheduling if needed.
12. Configure preferences/unavailability pages if volunteers self-manage availability.
13. Run a small scheduling test.

Citations: group scheduling setup patterns appear in official group docs and community implementation examples ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296), [Pastor of the Day Scheduling](https://community.rockrms.com/recipes/414)).

### Playbook: Room Management Reservation Calendar Sync

1. Verify Room Management plugin is installed and identify version/vendor namespace.
2. Confirm whether native event linkage exists.
3. Inspect reservation, schedule, locations, contact, and approval state.
4. Inspect `ReservationLinkage` or current equivalent.
5. Decide the system of record for schedule, location, and contact.
6. Use workflow or UI actions to sync only selected fields.
7. Add a detail panel showing missing or mismatched linkage.
8. Add data integrity reports for orphaned or stale links.
9. Test create, update schedule, update room, update contact, cancel, and delete cases.
10. Restrict permissions to facilities/event admins.

Citations: newer recipes recommend native linkage and `ReservationLinkage` ([Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444), [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)).

### Playbook: Internal Staff Calendar

1. Identify data sources: event items, room reservations, PTO, holidays, staff birthdays, LMS, custom workflows.
2. Prefer native calendar/event blocks where they meet requirements.
3. For custom internal views, use Lava commands or persisted datasets to precompute expensive sources.
4. Show approval status and calendars only to staff who need it.
5. Add campus filters if relevant.
6. Make time zone and recurrence behavior explicit.
7. Test mobile and desktop.
8. Document which data sources are authoritative.

Citations: staff calendar and Google holiday examples show common integration patterns ([Staff Calendar enhancement](https://community.rockrms.com/recipes/484), [US Holidays Web Request](https://community.rockrms.com/recipes/499)).

## 17. Troubleshooting Decision Tree

### A Schedule Is Missing From Check-In

1. Is the schedule active?
2. Is the current time inside the effective date/time and check-in offset window?
3. Is the schedule in the expected category?
4. Does the check-in configuration’s schedule builder show the schedule?
5. Is the group active and not archived?
6. Does the group location exist?
7. Does the `GroupLocationSchedule` row exist for the exact group/location/schedule?
8. Is the schedule excluded directly or by category?
9. Is the device scoped to the needed location?
10. Is the check-in type/configuration correct?
11. Is Rock/server time correct?
12. Does the installed version include known fixes for category exclusions or archived group schedule display?

Use the community troubleshooting recipe for practical time/configuration checks, then verify against current Rock version ([Troubleshooting Check-in Schedule Problems](https://community.rockrms.com/recipes/280), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### A Room Is Missing From Check-In

1. Is `Location.IsActive` true?
2. Is the room closed in Check-In Manager?
3. Is the room under the expected campus/building parent?
4. Is the location assigned to the group?
5. Is the group/location enabled for the schedule?
6. Is the device allowed to see that location?
7. Is the room full according to soft threshold?
8. Did location selection strategy auto-select a different room?
9. Does the person meet age, grade, ability, requirement, and group membership rules?
10. Is the room an overflow location that has not been scheduled?
11. Is a workflow filter removing or excluding it?

Source actions to inspect: active location filter, threshold filter, schedule filter, and location selection strategy filter ([FilterActiveLocations.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterActiveLocations.cs), [FilterLocationsByThreshold.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByThreshold.cs), [FilterLocationsBySchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsBySchedule.cs), [FilterLocationsByLocationSelectionStrategy.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs)).

### Volunteer Was Scheduled But Cannot Check In

1. Confirm today’s attendance occurrence exists for the group/location/schedule.
2. Confirm attendance or assignment has the person as scheduled/requested.
3. Confirm the group’s Attendance Record Required For Check-in setting.
4. Confirm the schedule attached to the group location matches the attendance occurrence schedule.
5. Confirm the person’s group membership and role are active.
6. Confirm group role can check in if the rule requires membership.
7. Confirm check-in configuration includes that group type.
8. Confirm the kiosk schedule and location match the assignment.

The `LoadSchedules` action checks scheduled/requested attendance for today with group, location, and schedule IDs populated when a group requires schedule attendance ([LoadSchedules.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs)).

### Group Scheduler Capacity Looks Wrong

1. Inspect `GroupLocationScheduleConfig` rows for the group location and schedule.
2. Inspect minimum, desired, maximum capacity fields.
3. Inspect group member assignments for matching group member, location, and schedule.
4. Inspect duplicate or stale assignments.
5. Confirm the installed version includes the v17.2 fix for deleting a schedule from one group location removing capacity settings in other group locations.
6. If using Sign-Ups, verify Sign-Up model relationships in the live instance.

Community Sign-Ups SQL shows the capacity and participant-count pattern, but verify before reuse ([Reference for Sign-Ups](https://community.rockrms.com/recipes/531/Schedule-WithAvailableSlots)); release notes document the capacity deletion fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Calendar Event Does Not Appear

1. Confirm event item exists.
2. Confirm event item approval status.
3. Confirm event item occurrence exists.
4. Confirm occurrence schedule is active and in range.
5. Confirm calendar membership.
6. Confirm audience filter.
7. Confirm campus filter or campus context.
8. Confirm date range and max occurrences.
9. Confirm Lava command security if using Lava.
10. Confirm version-specific EventScheduledInstance or calendar export fixes.

Use `calendarevents` or mobile block configuration before raw recurrence SQL ([Calendar Events](https://community.rockrms.com/lava/commands/calendar-events), [Calendar Event List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list)).

### Reservation And Calendar Are Out Of Sync

1. Verify plugin and schema.
2. Confirm reservation approval state.
3. Confirm reservation schedule and locations.
4. Confirm linked event item occurrence.
5. Inspect `ReservationLinkage` or current linkage object.
6. Compare schedule, location, contact, and note fields.
7. Identify the authoritative side.
8. Run or design a targeted sync workflow.
9. Add data integrity report for missing or stale linkages.
10. Do not use old recipes that store occurrence ID directly unless the live plugin still uses that model.

Newer recipes specifically direct implementers toward native linkage and `ReservationLinkage` ([Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444), [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)).

## 18. Agent Task Recipes

### Recipe: Prove Why A Check-In Room Is Not Available

Collect:

- Check-in configuration name and ID.
- Group ID and path.
- Location ID and path.
- Schedule ID and name.
- Device ID and device locations.
- Person ID and eligibility rule.
- Current Rock time.
- Relevant workflow filter states.

Then answer:

- Does the group/location/schedule link exist?
- Is the location active and open?
- Is the schedule active right now?
- Did a workflow filter exclude it?
- Is the person eligible?
- Is the device scoped correctly?
- Is there a version caveat?

### Recipe: Audit Group Location Schedules

Use a read-only join equivalent to the source dev view:

- `Schedule`
- `GroupLocationSchedule`
- `GroupLocation`
- `Group`
- `Location`

Report:

- Group name and ID.
- Location name and ID.
- Schedule name and ID.
- Active/archive status.
- Parent location path.
- Capacity config if applicable.
- Any rows attached to inactive or archived groups.

The source query shape is documented in `View_GroupLocationSchedules.sql` ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)).

### Recipe: Verify A New Service Time

Check:

- Schedule record and category.
- Effective dates.
- Check-in start offset.
- Group/location schedule rows copied or created.
- Overflow location rows.
- Device location scope.
- Check-In Manager schedule filter.
- Test family result.
- Attendance occurrence creation after check-in.

### Recipe: Build A Facilities Daily Report

Use official/plugin reporting first. If custom:

- Query approved and pending reservations for today and tomorrow.
- Include room, time, setup notes, setup diagram indicator, approval state, requester/contact, and resources.
- Highlight unapproved rows.
- Keep report internal.
- Avoid unbounded queries.
- Confirm plugin schema and file permissions.

Community precedent exists for daily facility reports, but requires plugin and possibly PDF Toolkit ([Room Management - Daily Email Reports for Facilities Team](https://community.rockrms.com/recipes/198)).

### Recipe: Build A Calendar Feed

Prefer native iCalendar feed if available. If custom:

- Choose source: event calendar, room reservations, group schedule, or custom workflow data.
- Limit date range.
- Validate iCal output.
- Set correct content type.
- Avoid exposing private notes or contact data.
- Test Outlook, Google Calendar, and Apple Calendar.
- Decide whether updates overwrite user edits.
- Use stable UID values.
- Document ownership and sharing.

Community examples include reservation iCal by campus, room-specific subscriptions, and generic Lava webhook `.ics` generation ([Room Management iCal Feed by Campus](https://community.rockrms.com/recipes/409), [Room Management iCal Subscriptions](https://community.rockrms.com/recipes/231), [Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540)).

### Recipe: Diagnose Schedule API Issues

If a browser call to schedules fails but Postman works, inspect:

- HTTP method.
- Authentication and authorization.
- CORS/browser constraints.
- Whether the payload attempts to set computed/read-only properties.
- Rock version.
- API endpoint shape.
- Browser console and server exception logs.

The provided Q&A mentions a v12.8 browser exception involving `FriendlyScheduleText` lacking a setter, but it has no answer in the source pack, so do not treat it as a solved known issue ([REST API for Schedules](https://community.rockrms.com/ask/developing/2710)).
























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `24`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | operational_guidance | The Scheduled Transactions RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/scheduled-transactions) |
| rocku-confirmed | operational_guidance | For ministry process design, Person Preferences and Auto Schedule should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule) |
| rocku-confirmed | operational_guidance | The Locations RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/check-in/locations) |
| rocku-confirmed | operational_guidance | The Group Location RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-location) |
| rocku-confirmed | operational_guidance | The Person Preferences and Auto Schedule RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule) |
| rocku-confirmed | operational_guidance | The Schedules RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/check-in/schedules) |
| rocku-confirmed | operational_guidance | For staff training and operational readiness, Group Scheduler and Status Board should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board) |
| rocku-confirmed | operational_guidance | The Campuses RockU lesson provides training context for staff training and operational readiness; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/core-concepts/campuses) |
| rocku-confirmed | operational_guidance | For ministry process design, Schedules should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/check-in/schedules) |
| rocku-confirmed | operational_guidance | For Rock operations and administration, Campuses should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/core-concepts/campuses) |
| rocku-confirmed | operational_guidance | The Group Scheduler and Status Board RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board) |
| rocku-confirmed | release_caveat | For version, roadmap, and release-caveat awareness, Group Scheduler and Status Board should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board) |
| More |  | 12 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->











































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `8`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Campuses Transcript Insight](https://community.rockrms.com/rocku/core-concepts/campuses) | approved_for_public_distillation | 2 | media-insight:3412bc01ca2880c8 |
| [Group Location Transcript Insight](https://community.rockrms.com/rocku/groups/group-location) | approved_for_public_distillation | 1 | media-insight:bcba31d4beb5a53b |
| [Group Scheduler and Status Board Transcript Insight](https://community.rockrms.com/rocku/groups/group-scheduler-and-status-board) | approved_for_public_distillation | 3 | media-insight:f0ede8a57e3ed4ac |
| [Locations Transcript Insight](https://community.rockrms.com/rocku/check-in/locations) | approved_for_public_distillation | 1 | media-insight:61af1407e6153473 |
| [Person Preferences and Auto Schedule Transcript Insight](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule) | approved_for_public_distillation | 2 | media-insight:97d2378d55d23ad1 |
| [Product Grooming & the Giving Landscape \| Ep 205 Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-205-product-grooming-the-giving-landscape) | approved_for_public_distillation | 3 | media-insight:457020f0b7d8dd97 |
| [Scheduled Transactions Transcript Insight](https://community.rockrms.com/rocku/finance/scheduled-transactions) | approved_for_public_distillation | 2 | media-insight:c28fc8fb8212eae5 |
| [Schedules Transcript Insight](https://community.rockrms.com/rocku/check-in/schedules) | approved_for_public_distillation | 2 | media-insight:70fee5b08ce0f4f2 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->
























## 19. Source Map And Dependency Notes

Primary official and training sources:

- Check-in locations, schedules, and NextGen schedule builder behavior: [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266), [Checking-out Check-in - NextGen](https://community.rockrms.com/documentation/bookcontent/42), [Check-In RockU](https://community.rockrms.com/rocku/check-in).
- Group location, scheduling, status board, preferences, analytics, RSVP, and group type settings: [Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7/296), [Groups RockU](https://community.rockrms.com/rocku/groups).
- Event calendars and registration calendar concepts: [Calendar Overview](https://community.rockrms.com/rocku/event-registration/calendar-overview).
- Release caveats and version behavior: [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Primary developer/source landmarks:

- Check-in group/location/schedule model: [CheckInGroupLocationSchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/CheckInGroupLocationSchedule.cs).
- Check-in location/schedule pair: [LocationAndScheduleBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/CheckIn/LocationAndScheduleBag.cs).
- Check-in schedule builder payloads: [GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs), [ScheduledLocationBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/ScheduledLocationBag.cs).
- Check-in workflow filters: [LoadLocations.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadLocations.cs), [LoadSchedules.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/LoadSchedules.cs), [FilterLocationsBySchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsBySchedule.cs), [FilterLocationsByThreshold.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByThreshold.cs), [FilterLocationsByLocationSelectionStrategy.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/CheckIn/FilterLocationsByLocationSelectionStrategy.cs).
- Group/location/schedule SQL model examples: [View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql), [View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql).
- Lava calendar command: [Calendar Events](https://community.rockrms.com/lava/commands/calendar-events).
- Mobile calendar and schedule-related blocks: [Calendar Event List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list), [Calendar View](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-view), [Event Item Occurrence List By Audience Lava](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/event-item-occurrence-list-by-audience-lava), [Schedule Unavailability](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-unavailability).

Community examples used as implementation patterns:

- Reservation-calendar sync and linkage: [Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444), [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20), [Room Reservation to Calendar tools](https://community.rockrms.com/recipes/111/room-reservation-to-calendar-tools).
- Reservation calendar/reporting/iCal: [Room Management Calendar View](https://community.rockrms.com/recipes/112), [Room Management iCal Subscriptions](https://community.rockrms.com/recipes/231), [Room Management iCal Feed by Campus](https://community.rockrms.com/recipes/409), [Room Management - Daily Email Reports for Facilities Team](https://community.rockrms.com/recipes/198).
- Group schedule utilities: [Group Viewer Meeting Details Accordion](https://community.rockrms.com/recipes/500), [Group Member Schedule Templates](https://community.rockrms.com/recipes/356), [Schedule Cancellation Workflow](https://community.rockrms.com/recipes/481), [View Serving Schedule on External Page](https://community.rockrms.com/recipes/459), [Pastor of the Day Scheduling](https://community.rockrms.com/recipes/414).
- Check-in and threshold troubleshooting: [Troubleshooting Check-in Schedule Problems](https://community.rockrms.com/recipes/280), [More User-Friendly Room Thresholds](https://community.rockrms.com/recipes/213).
- Calendar/Lava integrations: [Content Countdown Shortcode](https://community.rockrms.com/recipes/247), [Countdown to next Online Service](https://community.rockrms.com/recipes/165), [Lava Webhook to Create an iCal File](https://community.rockrms.com/recipes/540), [Staff Calendar enhancement](https://community.rockrms.com/recipes/484), [US Holidays Web Request](https://community.rockrms.com/recipes/499).

Dependency notes:

- The check-in topic depends heavily on groups because areas, groups, group types, group locations, requirements, and group membership determine availability.
- The groups topic depends on locations and schedules for attendance, serving assignments, RSVP, and auto scheduling.
- The events topic depends on schedules for occurrences and on campuses/audiences/calendars for display filtering.
- The CMS topic depends on schedules for conditional content, countdowns, and calendar rendering.
- Reservations depend on an installed Room Management plugin in the provided source pack; verify plugin presence, version, schema, and linkage model before implementing or troubleshooting.
