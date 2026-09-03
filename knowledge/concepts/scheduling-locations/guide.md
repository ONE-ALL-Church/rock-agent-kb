---
id: authored-scheduling-locations
title: Scheduling And Locations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "0d767c57b8088b1c7f6877fbd459cdee0ac4308186401786847592ac0b0acd32"
---

# Scheduling And Locations

## Agent Summary

Treat scheduling in Rock as a relationship among four distinct concerns:

1. **Location** describes where something happens. Named Locations can form a campus/building/room hierarchy or represent operational positions such as “Audio.”
2. **Schedule** describes when something happens.
3. **Group-location-schedule configuration** determines which groups can use which locations at which times, especially in check-in and volunteer scheduling.
4. **Calendar or reservation records** serve different publication and resource-planning purposes and should not be assumed to synchronize automatically.

For check-in, first confirm the Named Location, then its group association, schedule assignment, kiosk scope, current open/closed state and threshold state. For volunteer scheduling, confirm the location and schedule definitions before examining assignments, preferences or communications. For calendar and reservation issues, identify the owning record and any explicit linkage before comparing dates, locations or contacts. These relationships are described in the official [location](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations), [check-in](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk) and [group scheduling](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule) documentation.

Rock v19 adds an important reporting behavior: occurrences from recurring iCalendar schedules are materialized as `ScheduleDate` rows. Date-based SQL or Lava written for v19 should use those generated dates instead of implementing a second recurrence-expansion system. This is an approved v19 claim supported by the official [Rock Cast episode at 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s).

## Scope And Boundaries

This guide owns operational guidance for:

- Positional and Named Locations.
- Campus, building, room and position-style location structures.
- Check-in group/location/schedule configuration.
- Room availability, open/closed state and check-in thresholds.
- Group schedule types, exclusions, volunteer availability and scheduling communications.
- Rock event calendars and iCalendar delivery where they intersect with schedules.
- Room-reservation-to-calendar coordination patterns supported by the supplied community evidence.

Detailed check-in workflows, group administration, event registration, CMS presentation and communication-provider configuration belong to their respective concepts. For example, this guide explains how a room becomes available at a scheduled check-in time, but not the entire check-in workflow. Similarly, it explains calendar publication settings but not the complete event-registration lifecycle. The official documentation separates these subjects into [Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations), [Group Schedules](https://community.rockrms.com/documentation/engagement/groups/group-schedules), [Calendars](https://community.rockrms.com/documentation/church-management/event-calendar/calendars) and [Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations).

The evidence pack contains cross-tagged v19 claims about Connections training and proof-of-work CAPTCHA. Those belong to the Connections, CMS, security and platform-configuration concepts and are not promoted into scheduling behavior here.

No live Rock instance was reviewed for this guide. Menu placement, block generation, installed plugins, permissions and local data must therefore be verified before changing a production system.

## Mental Model

A useful operating model is:

- A **positional location** supplies geographic position but gains meaning through its use by a family, group or another feature.
- A **Named Location** combines position with an organizational identity and can participate in a hierarchy.
- A **group location** associates a group with a location.
- A **group-location-schedule relationship** makes that pairing active at selected times.
- A **runtime location state** can still make a scheduled check-in room unavailable by closing it or reaching a threshold.
- A **calendar event occurrence** publishes an event occurrence; it is not automatically the same record as a room reservation or volunteer assignment.
- An **iCalendar feed or file** transports schedule information to external calendar software; it does not replace the Rock records that generated it.

Rock’s v19 location documentation distinguishes positional and Named Locations and describes address, point and geo-fence descriptors. It also states that Named Locations must be configured before use elsewhere in Rock. The check-in documentation then describes locations as hierarchical records tied to groups and enabled through schedules. [Intro to Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations) and [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk) provide the documented model.

An immutable source snapshot also models check-in as an explicit group, location and schedule combination. This is implementation evidence from commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, not proof of any installation’s configuration. [CheckInGroupLocationSchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/CheckIn/CheckInGroupLocationSchedule.cs)

## Locations

### Positional And Named Locations

Rock supports three location descriptors in the supplied v19 documentation:

- A street address.
- A latitude/longitude point, resolved from an address or selected with the location picker.
- A geo-fence drawn around a geographic area.

Positional Locations describe a place but depend on their context—such as a family residence or group meeting place—for meaning. Named Locations add an organizational name and can be arranged hierarchically. [Intro to Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations)

Do not treat every location-editing surface as interchangeable. A family address, group meeting location and Named Location share common address fields, but context-specific options differ. Named Locations can expose fields such as parent, Location Type, image, printer, beacon identifier, thresholds and geo-fence that are not necessarily available when editing a family or group address. [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations)

### Named Location Hierarchy

For check-in, the documented starting pattern is a loose hierarchy of campus, building and room. Create or rename the top-level campus, add its buildings and then add the rooms that check-in will use. Named Locations are maintained through the Named Locations administration area. [Configure Locations](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations)

The hierarchy should represent operational meaning, not merely a mailing address. Group Scheduling can also use locations that represent sections, areas or positions. The official example suggests position-style locations such as “Audio” or “Piano,” with an appropriate Location Type, when scheduling technical or music teams. Location Types are Defined Values associated with the Location category. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Only a location with the Campus Location Type can be selected when configuring a Campus. A Named Location’s parent controls its placement in the location tree. Rock v18.3 fixed an issue that allowed a location to be saved as its own parent or under one of its children, which could prevent nested location trees from loading. [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations) and [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Address And Geographic Integrity

Address standardization can verify and geocode a location. Enabling **Location Locked** prevents standardization services from automatically changing an address, but it does not prevent a person from editing that address manually. A point can also be selected directly, and a geo-fence can define a geographic boundary used by location-aware features. [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations)

The Location Editor at `Tools > Data Integrity > Location Editor` can filter for records that have not been geocoded. The documented remediation is to open the affected record, correct its address fields, allow Rock to resolve the coordinates and save it. [Location Editor](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor)

### Location Metadata That Changes Behavior

Several Named Location fields have operational effects:

- **Printer** associates a configured device with the location.
- **Beacon Identifier** associates Bluetooth beacon devices with a location for mobile check-in and must be between 1 and 65,535.
- **Threshold** acts as a soft check-in capacity: additional check-ins require a manager override after the threshold is reached.
- **Absolute Threshold** is a firm limit that cannot be overridden.
- **Location Locked** controls automatic address-standardization changes, not manual editing.

These behaviors are documented in [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations).

## Check-In Location Scheduling

### Building The Group-Location-Schedule Matrix

A check-in room is not made available merely by creating the Named Location. Locations are associated with check-in groups and then enabled for particular schedules. Rock’s Schedule Builder displays group/location combinations as rows and schedule times as columns. An administrator selects the allowed intersections and saves the grid. Filters can narrow the grid by campus or building, check-in area or schedule. [Use the Schedule Builder](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder)

The normal documented route is through the check-in configuration’s Schedule action. Device Manager can also expose **Schedule Locations**, allowing an operator to enable or disable schedules for the rooms configured for that kiosk. [Use Schedule Locations](https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations)

At immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`, the schedule-builder view model contains the group path, location path, group-location identifier and the schedule identifiers active for that pairing. This confirms the implementation shape but does not establish what a particular Rock version or instance has enabled. [GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs)

### Scheduled, Open And Within Capacity

Three checks are separate:

1. The room is associated with the correct group.
2. The group/location pairing is enabled for the selected schedule.
3. The location is currently open and below the applicable capacity limit.

An operator can close an otherwise scheduled room in Check-in Manager or Device Manager. A closed room is removed as a check-in option. It can later be reopened manually, or the Auto Open Locations job can be configured to reopen rooms at intervals. [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

The soft threshold permits an attendant override; the absolute threshold does not. Do not diagnose a full or closed room by changing its schedule assignment until the runtime state and threshold counts have been checked. [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### Cloning A Check-In Schedule

Rock v19 documentation describes cloning the enabled locations from a source schedule into a destination schedule. This is intended for special events that reuse a complex room configuration. The operation is initiated from the Schedule view of the check-in configuration by choosing **Clone Schedule** and supplying source and destination schedules. [Clone a Schedule](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule)

Cloning reduces setup repetition, but it does not replace verification. Review the destination matrix after cloning, especially when campuses, buildings or rooms should differ from the source. The documentation also warns custom deletion logic not to identify `GroupLocationSchedule` rows by `ScheduleId` alone because one schedule can be used by multiple check-in configurations; the group must be constrained to the current configuration. [Clone a Schedule](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule)

## Group And Volunteer Scheduling

### Prerequisites

Group Scheduling requires accurate Named Locations and Schedules before people are assigned. The location answers “where,” the schedule answers “when,” and Group Scheduler places volunteers into those combinations. The official guidance recommends one schedule for each time; campuses sharing the same start time can reuse that schedule. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Scheduling must also be enabled on the applicable Group Type. Group Type settings can select confirmation and reminder communications, define offsets, launch a cancellation workflow, require a decline reason, choose **Ask** or **Auto Accept** confirmation logic and configure coordinator notifications. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Changing confirmation logic after assignments exist requires caution. The official documentation warns that switching from **Ask** to **Auto Accept** before a person receives a confirmation can produce a message with a Decline action but no Accept action for an unconfirmed person. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

### Weekly, Custom And Named Group Schedules

A Group Type can permit three group schedule modes:

- **Weekly** records a weekday and start time. Of the three documented modes, this is the one that can be used as a Group Finder schedule filter.
- **Custom** lets a group define its own repeating schedule but is not available as a Group Finder schedule filter.
- **Named** selects from schedules configured under the general Schedules settings and is also not available as a Group Finder schedule filter.

Choose the mode based on the consuming workflow, not merely on recurrence flexibility. If website visitors need to filter groups by meeting day, the supplied v19 documentation specifically favors Weekly. [Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types)

Group Type schedule exclusions can apply a break to all groups of that type. The documentation notes that exclusions keep the schedule accurate and suppress attendance reminders while those groups are not meeting. [Intro to Group Schedules](https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules)

### Volunteer Preferences, Unavailability And Open Slots

The Schedule Toolbox lets a volunteer:

- Review accepted, declined and pending assignments.
- Accept, decline or cancel a confirmation.
- Declare an unavailable date range for one group or all groups and, where appropriate, selected family members.
- Choose reminder timing.
- Select a recurring schedule template.
- Set preferred schedules and locations for Auto-Schedule.
- Sign up for additional serving opportunities.

Only Named Schedules marked **Show Publicly** are listed as assignment preferences. A person may omit a location preference. The preferences are inputs to Auto-Schedule, not proof that an assignment has been created. [Set Schedule Availability](https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox)

Additional-time availability is calculated using desired and maximum capacity. Reaching the desired number marks a slot filled, but sign-up can continue until the maximum is reached. **Immediate Needs** is disabled by default and, when enabled, is bounded by settings such as cutoff time and the immediate-needs window. [Set Schedule Availability](https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox)

The Current Schedule view can download an `.ics` file or copy a calendar link, but those actions are not available until the person has at least one confirmed assignment. A downloaded file may need to be downloaded again after assignments change. [View your Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox)

### Confirmation And Reminder Delivery

Confirmation and reminder System Communications can use email or SMS. SMS requires configured SMS messaging, an SMS-enabled phone number and an SMS-capable System Communication. Rock chooses the medium using the group member’s communication preference, falling back to the person’s profile preference when the group member has no preference. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Outreach Toolbox uses a separate but related scheduling pattern: a signed-in person selects assignment days and reminder preferences, while configurable jobs supply reminder time-of-day values. The approved claim’s version scope is unprocessed, so confirm applicability before implementation and test both the job schedule and push delivery in the target mobile environment. [Outreach Toolbox is Here in v19 at 01:04](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s)

## Calendars And iCalendar

### Calendar Events Are Publication Records

After a calendar exists, events are managed from its Calendar Details page. The documented event fields include active and approved state, summary, description, audiences, photo, additional calendars, details URL, custom attribute values and occurrence-level attributes. Approval is available only to a person with Approval permission on the calendar. [Add an Event](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/add-an-event)

External display is block-driven. The Calendar Lava block can select a calendar, initial day/week/month view, details page, campus and audience filters, date-range controls, campus context and a Lava template. Specialty blocks can show a particular event item’s occurrences or occurrences for an audience. [Explore Different Event Blocks](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/explore-different-event-blocks)

### iCalendar Feeds

Rock can expose an event calendar through `GetEventCalendarFeed.ashx`. The feed URL can include a calendar identifier and optional template, campus, audience, start-date and end-date parameters. The Export Calendar Feed action can copy the generated URL. Calendar security remains enforced, including for non-public calendars accessed through the feed. [Configure the iCalendar Feed](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/configure-the-icalendar-feed)

Do not confuse two calendar delivery modes:

- The Schedule Toolbox can provide a file or link for a volunteer’s confirmed assignments.
- Event Calendar feeds publish occurrences from a Rock event calendar.

When diagnosing an external calendar, first identify which producer generated the file or URL. The applicable permissions, filters and source records differ. [View your Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox) and [Configure the iCalendar Feed](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/configure-the-icalendar-feed)

Rock v17.2 fixed unclear Group Schedule ICS summaries by changing them to a “Group - Location - Schedule” structure. An installation on an earlier release should not be expected to have that fix. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Recurring Schedule Dates In v19

The approved v19 claim states that Rock materializes occurrences from recurring iCalendar schedules into `ScheduleDate` rows. For v19 date-based SQL and Lava, query those generated occurrence dates rather than repeatedly parsing and expanding the recurrence rule. [Official Rock Cast at 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

This claim does not establish the generation horizon, refresh timing or behavior on earlier versions. Those details require current documentation, source inspection for the installed build or bounded live verification.

## Reservations And Calendar Coordination

The supplied evidence does not establish Room Management as universal Rock core behavior. Its reservation examples are community recipes that depend on a separately installed Room Management plugin and should be treated as implementation patterns, not official platform guarantees.

A current community pattern for Rock 15 uses the plugin’s reservation linkage to identify whether a reservation has a linked calendar occurrence and whether schedule information matches. It proposes a details-panel warning and a workflow that can push selected reservation changes to the linked calendar occurrence. The recipe explicitly requires the Room Management plugin and carries the Rock Community disclaimer that recipes are not reviewed or endorsed by the core team. [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)

Earlier community recipes used custom attributes, direct SQL and older plugin-specific assumptions. A later draft recommends using the plugin’s `ReservationLinkage` table instead of the older event-occurrence attribute pattern, but that draft is unpublished. Do not combine these generations of a recipe without verifying plugin version and schema. [Room Reservation to Calendar tools](https://community.rockrms.com/recipes/111/room-reservation-to-calendar-tools) and [draft Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444)

Another older recipe adds a calendar-style reservation view and explicitly requires Room Management plugin version 1.4.1. Its third-party JavaScript dependencies, legacy rendering assumptions and plugin version must be reviewed before reuse. [Room Management Calendar View](https://community.rockrms.com/recipes/112)

The operational lesson is bounded: reservation and event records can drift when maintained separately. An agent may compare an explicit linkage and surface a discrepancy, but must not assume which side should overwrite the other. That decision belongs to the organization’s documented ownership policy.

## Version And Authority Caveats

Most official documentation supplied for this guide is scoped to Rock v19.0. Verify the installed version and block generation before following paths or expecting the same controls.

Version-specific evidence includes:

- Rock v17.2 fixed Group Schedule ICS summaries.
- Rock v18.3 prevented a location from being its own parent or a descendant’s parent.
- Rock v19 materializes recurring iCalendar occurrences into `ScheduleDate` rows.
- The v19 Check-In Manager roster uses real-time updates, allowing attendance state changes to appear without a manual refresh. When updates lag, the approved claim directs agents to verify browser connectivity, block version and local check-in configuration. [Official Rock Cast at 04:28](https://www.youtube.com/watch?v=edanHiYSDIM&t=268s)
- Current release notes also describe later v19 patches affecting check-in and location behavior; patch-level applicability must be checked against the installed build. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- The hydrated release-notes page labels v20 as alpha. Alpha behavior should not be treated as deployed production behavior merely because it appears in current documentation or source.

The factual spine is explicitly bound to the approved answer-bearing claim set. `claim:4c4098a035a5ca256bfe` and its reviewed companion `claim:32f0173b23a7d2c356c0` support the `ScheduleDate` materialization guidance. `claim:9ad17cb08b8955d0d3ec` and companion `claim:dc7cb132c34cdde8cb4e` support the real-time Check-In Manager roster guidance. `claim:07a75e5ff71510d708de` and `claim:66eb84b2b9cc466ce78b` establish the staff-training caveat for redesigned Connections; `claim:2a9844acce5ba6150dec` and `claim:3e398ac03167b9c52704` establish the v19 proof-of-work CAPTCHA caveat. The official source links and exact wording remain in [Scheduling And Locations Approved Claims](approved-claims.md).

GitHub excerpts in this guide are pinned to commit `471fd303d111b2e46218228dbc1e93dba8856fa3` on the public `develop` branch. They clarify implementation structure but do not prove that a production installation contains that code.

Community recipes are examples. Their Rock versions range from older releases through Rock 15, some depend on paid plugins, and one supplied recipe is still a draft. Review security, performance, schema, page routes and plugin compatibility before adoption.

## Troubleshooting Decision Tree

### A Room Does Not Appear During Check-In

1. Confirm the room exists as the intended Named Location and is active in the correct hierarchy.
2. Confirm the check-in group is associated with that location.
3. Open the check-in Schedule Builder and confirm the group/location row is enabled for the selected schedule.
4. Confirm the kiosk is configured for the applicable rooms and scope.
5. Check whether the room is currently closed in Check-in Manager or Device Manager.
6. Check the soft and absolute thresholds and current count.
7. If a campus filter is active, confirm it has not excluded every location.
8. If the room was created recently, check the installed patch level and cache behavior before rebuilding the hierarchy.

The configuration sequence and runtime controls are documented in [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk) and [Use the Schedule Builder](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder). The immutable Rapid Attendance model also distinguishes the total group-location count from the campus-filtered result. [rapidAttendanceEntryLocationsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryLocationsBag.d.ts)

### A Schedule Does Not Appear In A Check-In Scheduling Screen

1. Confirm that the schedule is active.
2. Confirm it represents the intended check-in time and category.
3. Confirm the check-in configuration and screen are the expected generation for the installed version.
4. Confirm the schedule has the required check-in timing configuration.
5. Confirm filters on the Schedule Builder or kiosk screen are not hiding it.

At the supplied `develop` commit, the legacy Scheduled Locations block filters for active schedules with a check-in start offset in the service-times category. Treat this as a source-code observation to guide inspection, not as proof of behavior in another build. [CheckinScheduledLocations.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs)

### A Volunteer Cannot See, Accept Or Decline An Assignment

1. Confirm scheduling is enabled on the Group Type.
2. Confirm the person belongs to the applicable schedulable group.
3. Confirm an assignment actually exists; preferences alone do not create one.
4. Check whether the assignment is accepted, declined, pending or marked unavailable.
5. Review the Group Type’s confirmation logic and whether it changed after assignments were created.
6. Review block settings that can hide actions or change their labels.
7. If a decline reason is expected, confirm the Group Type requires one.

See [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule) and [View your Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox).

### A Volunteer Is Missing A Reminder

1. Confirm the assignment and its schedule time.
2. Confirm the Group Type reminder communication and offset.
3. Check the group member’s reminder and communication preferences.
4. If no group member communication preference exists, inspect the person’s profile preference.
5. For SMS, confirm the provider configuration, SMS-enabled phone and SMS-capable System Communication.
6. For Outreach Toolbox, separately inspect the reminder job time and push delivery in the target mobile environment.

The group-scheduling delivery rules are documented in [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule). Outreach Toolbox behavior is an approved claim with unprocessed version scope from [Outreach Toolbox is Here in v19 at 01:04](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s).

### A Calendar File Or Feed Is Empty, Stale Or Missing Events

1. Identify whether the source is a volunteer Schedule Toolbox export or an Event Calendar feed.
2. For Schedule Toolbox, confirm the person has at least one confirmed assignment.
3. For an Event Calendar feed, confirm calendar access and examine calendar, campus, audience and date parameters.
4. Confirm the URL still contains the required `GetEventCalendarFeed.ashx` handler.
5. Compare the Rock calendar occurrence with the exported result.
6. If a downloaded `.ics` file was used, regenerate it after schedule changes.
7. Check the Rock version when Group Schedule ICS summaries are unclear; the summary-format fix shipped in v17.2.

See [View your Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox), [Configure the iCalendar Feed](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/configure-the-icalendar-feed) and [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### A Date-Based Query Misses Recurring Schedule Occurrences

1. Confirm the installed Rock version.
2. On v19, inspect the generated `ScheduleDate` rows for the schedule.
3. Use those rows for date-based SQL or Lava rather than re-expanding the iCalendar rule.
4. If expected rows are absent, stop and verify generation behavior for the exact installed build.
5. On pre-v19 systems, do not assume the v19 materialization model exists.

This procedure follows approved claim `claim:4c4098a035a5ca256bfe`, supported by the [official Rock Cast at 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s).

### A Reservation And Calendar Event Do Not Match

1. Confirm the Room Management plugin is installed and identify its version.
2. Identify the reservation and its explicit calendar linkage.
3. Compare schedule, location and contact fields without modifying either record.
4. Determine which record is authoritative under local policy.
5. Review the recipe generation and schema assumptions before running a workflow or SQL.
6. Stop before synchronizing if ownership, linkage or compatibility is ambiguous.

The supplied workflow is a community pattern, not core behavior. [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20)

### The Named Location Tree Will Not Load

1. Check the installed Rock version and patch level.
2. Inspect the affected location’s parent relationship.
3. Check for a location set as its own parent or placed beneath one of its descendants.
4. Do not attempt broad hierarchy rewrites until the exact invalid relationship is identified.
5. If the installation predates the v18.3 fix, review the release path and correct the data through an approved, bounded process.

Rock v18.3 fixed this circular-parent condition. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Check-In Manager Attendance Changes Do Not Update In Real Time

1. Confirm the installation is on an applicable v19 build.
2. Verify browser connectivity.
3. Confirm the expected Check-In Manager block version is loaded.
4. Review local check-in configuration.
5. Compare the roster state with the authoritative attendance state before asking operators to refresh or re-enter attendance.

This follows approved claim `claim:9ad17cb08b8955d0d3ec`, supported by the [official Rock Cast at 04:28](https://www.youtube.com/watch?v=edanHiYSDIM&t=268s).

## Agent Task Recipes

### Recipe: Build A Check-In Location Hierarchy

**Outcome:** Named Locations represent the intended campus, building and room structure.

1. Inventory the operational hierarchy and the rooms that will participate in check-in.
2. Open Named Locations.
3. Confirm or create the top-level campus location.
4. Add buildings beneath the campus.
5. Add rooms beneath the appropriate buildings.
6. Assign the correct Location Type to each record.
7. Review parent relationships and names from the full tree.
8. Configure only the metadata required for each location, such as thresholds, printer, beacon, point or geo-fence.
9. Save and verify that the hierarchy reloads correctly.

**Inspect:**

- Parent Location.
- Location Type.
- Active state.
- Soft and absolute thresholds.
- Address, point and geo-fence where relevant.

**Do not assume:**

- A family address is a Named Location.
- A room needs a street address.
- Creating the room makes it available to check-in.
- A soft threshold and absolute threshold behave the same way.

**Stop when:**

- A parent relationship would create a cycle.
- The correct campus or Location Type is unclear.

Sources: [Configure Locations](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations) and [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations).

### Recipe: Prove Why A Check-In Room Is Not Available

**Outcome:** The intended group/location pairs are enabled for the intended check-in times.

1. Confirm the Named Locations, check-in groups and schedules already exist.
2. Open the applicable check-in configuration.
3. Open its Schedule Builder.
4. Filter to the target campus, building, area or schedule when helpful.
5. For each group/location row, select the schedule columns during which it should accept check-in.
6. Save the grid.
7. Reopen the grid and verify the selections.
8. Test the applicable kiosk scope and runtime open/closed state.

**Inspect:**

- Exact check-in configuration.
- Group path and location path.
- Schedule name and time.
- Kiosk location scope.
- Current room status and thresholds.

**Do not assume:**

- A location enabled for one schedule is enabled for another.
- One check-in configuration’s relationships apply to another configuration.
- A scheduled room is currently open.

**Stop when:**

- The same schedule name maps to ambiguous times.
- The location or group path is not the intended one.

Source: [Use the Schedule Builder](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder).

### Recipe: Clone A Check-In Schedule For A Special Event

**Outcome:** A destination schedule starts with the source schedule’s enabled locations.

1. Create or identify the destination schedule.
2. Open the applicable check-in configuration’s Schedule view.
3. Choose **Clone Schedule**.
4. Select the existing source schedule.
5. Select the destination schedule.
6. Complete the clone.
7. Review every enabled location in the destination.
8. Remove or add only the differences required for the special event.
9. Test the destination schedule through the intended kiosk configuration.

**Do not assume:**

- The special event uses every regular-service room.
- The clone copies unrelated event, reservation or calendar records.
- A destination schedule is safe merely because the operation completed.

**Stop when:**

- The source and destination schedule identities are uncertain.
- Custom cleanup logic targets records only by `ScheduleId`.

Source: [Clone a Schedule](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule).

### Recipe: Configure A Group Type For Volunteer Scheduling

**Outcome:** Groups of the selected type can schedule volunteers with defined confirmation and reminder behavior.

1. Confirm the required Named Locations and one-schedule-per-time definitions.
2. Open the target Group Type’s scheduling settings.
3. Enable scheduling.
4. Select the confirmation communication.
5. Select the reminder communication.
6. Set confirmation and reminder offsets.
7. Choose **Ask** or **Auto Accept** deliberately.
8. Configure decline reasons, cancellation workflow and coordinator notifications as required.
9. Confirm SMS prerequisites if either communication may use SMS.
10. Test with a non-production assignment before broad use.

**Inspect:**

- Existing pending assignments before changing confirmation logic.
- Group member and profile communication preferences.
- System Communication channel configuration.
- Schedule and location accuracy.

**Do not assume:**

- Enabling scheduling creates assignments.
- Auto Accept safely changes the state or actions of already-pending communications.
- Selecting an SMS communication guarantees delivery.

**Stop when:**

- Existing pending assignments could receive incompatible confirmation actions.
- The organization has not chosen its confirmation policy.

Source: [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule).

### Recipe: Prepare Volunteer Availability For Auto-Schedule

**Outcome:** A volunteer has usable availability, reminder and assignment preferences.

1. Open the Schedule Toolbox for the correct person.
2. Record unavailable date ranges, scope and optional notes.
3. Select the applicable schedule template.
4. Set reminder preference.
5. Select preferred schedules and locations.
6. Confirm required Named Schedules are marked **Show Publicly** if they should appear.
7. Review the Group Member Detail record where administrative confirmation is needed.
8. Run Auto-Schedule only after preferences for the relevant roster have been reviewed.
9. Review generated assignments before sending confirmations.

**Do not assume:**

- A preference guarantees assignment.
- No location preference means the person cannot be scheduled.
- A schedule template applies correctly to every weekday.

**Stop when:**

- The template’s weekday or recurrence meaning is ambiguous.
- A required schedule is missing from the public preference list.

Source: [Set Schedule Availability](https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox).

### Recipe: Publish And Test An Event Calendar Feed

**Outcome:** The intended Rock calendar is available through a bounded iCalendar feed.

1. Confirm the event, occurrences, active state, calendars and approval state.
2. Open the intended Event Calendar.
3. use **Export Calendar Feed** to obtain the URL.
4. Review its calendar, campus, audience and date parameters.
5. Confirm the requesting user can access any non-public calendar included.
6. Subscribe from a test calendar client.
7. Compare representative occurrences, dates and descriptions with Rock.
8. Retest after changing one test occurrence.
9. Document the feed’s audience and ownership.

**Do not assume:**

- A calendar feed bypasses Rock security.
- A volunteer Schedule Toolbox link is the same as an Event Calendar feed.
- A reservation automatically appears on the event calendar.

**Stop when:**

- The feed exposes a broader calendar, campus or audience than intended.
- The authoritative event occurrence cannot be identified.

Sources: [Add an Event](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/add-an-event) and [Configure the iCalendar Feed](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/configure-the-icalendar-feed).

### Recipe: Evaluate Reservation-To-Calendar Synchronization

**Outcome:** The organization has a safe compatibility and ownership decision before implementing synchronization.

1. Confirm whether the Room Management plugin is installed.
2. Record its exact version and linkage schema.
3. Identify the community recipe that matches that generation.
4. Determine whether reservations or calendar occurrences are authoritative for schedule, location and contact fields.
5. Inspect existing reservation linkages and mismatches read-only.
6. Review all proposed Lava, workflow actions, SQL, routes and permissions.
7. Test in a non-production environment with reversible sample records.
8. Verify create, update, missing-link and mismatch cases.
9. Approve a production workflow only after security, performance and rollback review.

**Do not assume:**

- Rock core synchronizes reservations and calendars.
- An older custom attribute and a newer linkage table are interchangeable.
- A recipe’s embedded IDs, paths or table names apply locally.
- A mismatch tells the agent which record should win.

**Stop when:**

- Plugin or schema compatibility is unknown.
- The authoritative system has not been chosen.
- The proposal requires unreviewed write SQL.

Sources: [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20) and [draft Room Reservation to Calendar 2.0](https://community.rockrms.com/recipes/444).

### Recipe: Audit A V19 Date-Based Schedule Query

**Outcome:** A date-based report uses Rock’s v19 materialized schedule occurrences.

1. Confirm the installed version is v19.
2. Identify the recurring Schedule records in scope.
3. Inspect their corresponding `ScheduleDate` rows.
4. Compare representative generated dates with the intended recurrence.
5. Update the report design to filter and join through generated dates.
6. Test inclusions, exclusions and date boundaries.
7. Stop rather than adding a parallel recurrence parser when generated dates are unexpectedly absent.

**Do not assume:**

- Pre-v19 systems have the same materialization.
- The supplied evidence defines the generation horizon or refresh mechanism.
- One organization’s observed row count is universal.

Source: approved claim `claim:4c4098a035a5ca256bfe`, [official Rock Cast at 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s).

## Known Gaps And Live Verification

The following questions remain installation-dependent and were not answered by live evidence:

- The installed Rock version, patch level and block generation.
- The actual Named Location hierarchy and whether parent relationships are valid.
- Which check-in configurations, groups, locations, schedules and kiosks are linked.
- Current room open/closed state, attendance counts and threshold behavior.
- Local cache behavior after creating a Named Location.
- The exact generation horizon and refresh behavior for v19 `ScheduleDate` rows.
- Group Type scheduling settings, pending assignments and communication preferences.
- Email, SMS and push-provider configuration and actual delivery.
- Calendar security, feed subscriptions and external-client behavior.
- Whether Room Management or any other reservation plugin is installed.
- The plugin version, linkage schema and applicability of community recipes.
- The organization’s source-of-truth policy when a reservation and event occurrence disagree.

A live review should be bounded and read-only until the exact entity, version and configuration are known. Report observed state separately from inferred behavior. Do not publish raw database results, organization-specific identifiers or private scheduling data.

## Source Map

### Approved Answer-Bearing Claims

- `claim:4c4098a035a5ca256bfe` — v19 recurring iCalendar occurrences are materialized into `ScheduleDate` rows. [Official video evidence](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)
- `claim:9ad17cb08b8955d0d3ec` — v19 Check-In Manager uses real-time roster updates; lagging updates require browser, block and configuration checks. [Official video evidence](https://www.youtube.com/watch?v=edanHiYSDIM&t=268s)
- `claim:9c8ce297c9c4a4cda982` — Outreach Toolbox assignment days, reminder preferences and reminder-job timing; version scope remains unprocessed. [Official video evidence](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s)

### Official Documentation

- [Intro to Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/intro-to-locations) — descriptors, positional locations and Named Locations.
- [Maintain Locations](https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/locations/maintain-locations) — context-specific fields, Location Types, locking, printers, beacons and thresholds.
- [Location Editor](https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor) — locating and correcting ungeocoded records.
- [Configure Locations](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-locations) — campus/building/room setup.
- [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk) — group/location/schedule relationships, runtime state and thresholds.
- [Use the Schedule Builder](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/use-the-schedule-builder) — schedule matrix workflow.
- [Use Schedule Locations](https://community.rockrms.com/documentation/church-management/check-in/device-manager/use-schedule-locations) — Device Manager scheduling controls.
- [Clone a Schedule](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/clone-a-schedule) — copying enabled locations between schedules.
- [Intro to Group Schedules](https://community.rockrms.com/documentation/engagement/groups/group-schedules/intro-to-group-schedules) — schedule modes and exclusions.
- [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule) — prerequisites, Group Type settings and communications.
- [Set Schedule Availability](https://community.rockrms.com/documentation/engagement/groups/group-schedules/set-schedule-availability-toolbox) — unavailability, preferences, additional times and Immediate Needs.
- [View your Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox) — assignment state and calendar export.
- [Add an Event](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/add-an-event) — event administration and approval.
- [Configure the iCalendar Feed](https://community.rockrms.com/documentation/church-management/event-calendar/calendars/configure-the-icalendar-feed) — feed security, URL and parameters.
- [Explore Different Event Blocks](https://community.rockrms.com/documentation/church-management/event-calendar/advanced-events/explore-different-event-blocks) — calendar presentation controls.

### Release Notes And Source Code

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — versioned location, check-in and ICS fixes.
- [CheckInGroupLocationSchedule.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/CheckIn/CheckInGroupLocationSchedule.cs) — implementation model for a check-in group/location/schedule combination.
- [GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs) — schedule-builder relationship data at the supplied immutable commit.
- [CheckinScheduledLocations.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx.cs) — legacy scheduled-location filtering at that commit.
- [rapidAttendanceEntryLocationsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/RapidAttendanceEntry/rapidAttendanceEntryLocationsBag.d.ts) — campus-filtered location behavior at that commit.

### Community Examples

- [Room Reservation to Calendar Tool 2.0](https://community.rockrms.com/recipes/516/room-reservation-to-calendar-tool-20) — plugin-dependent reservation linkage and discrepancy pattern.
- [Room Reservation to Calendar 2.0 draft](https://community.rockrms.com/recipes/444) — unpublished linkage-table update to an older pattern.
- [Room Reservation to Calendar tools](https://community.rockrms.com/recipes/111/room-reservation-to-calendar-tools) — older attribute and SQL-based pattern.
- [Room Management Calendar View](https://community.rockrms.com/recipes/112) — legacy plugin calendar-view example.
- [Group Viewer Meeting Details](https://community.rockrms.com/recipes/500) — community example of exposing linked locations and schedules to authorized staff; not core behavior.
- [Group Member Schedule Templates](https://community.rockrms.com/recipes/356) — community approaches to fifth-week and Auto-Schedule templates; not official scheduling semantics.
