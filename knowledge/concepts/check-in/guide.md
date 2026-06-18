---
id: authored-check-in
title: Check-In
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Check-In

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Check-In index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock Check-In is not a single screen. It is a coordinated system that combines check-in configurations, group types, groups, locations, schedules, devices, printers, labels, attendance records, family search, security codes, mobile flows, and management tools. The user-facing kiosk is only the visible edge. The operational truth lives in the configuration graph and the attendance rows it creates.

For agent work, the most important rule is this: diagnose Check-In by walking the chain in order. A person can appear missing, a room can appear closed, a printer can fail, or analytics can look wrong because any one of these layers is misconfigured:

1. The check-in configuration is inactive, wrong type, or scoped to the wrong group type.
2. The check-in area, group, location, or schedule is not active for the current date and time.
3. The person is not eligible by membership, age, grade, data view, relationship, campus, capacity, or group type rules.
4. The device is pointed at the wrong check-in configuration, printer, campus, or kiosk profile.
5. The print path is resolving to a device printer when the expected printer is attached to a location, or the reverse.
6. The label template, merge fields, icon font, or next-generation label definition is not compatible with the active print path.
7. Attendance was written but is being interpreted differently by analytics, group attendance, mobile attendance, or custom reporting.
8. A version-specific feature, security verb, or block setting changed the behavior.

The official Rock documentation’s "Checking-out Check-in" manual is the main conceptual source for traditional Check-In configuration, including check-in system types, family and individual flows, group membership behavior, printer routing, and release updates through later Rock versions ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). RockU provides the training map for the operational sequence: getting started, locations, schedules, types and groups, settings, devices, labels, running Check-In, analytics, manager, rapid attendance, mobile Check-In, attendance self-entry, celebrations, and next-generation labels ([RockU Check-In](https://community.rockrms.com/rocku/check-in)). Source-code records add implementation detail for mobile Check-In, Rapid Attendance Entry, Attendance Analytics, label data, and analytics stored procedures in the Rock repository ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md), [Mobile CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs), [RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs), [AttendanceAnalytics.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs)).

Agents should treat Check-In as an event-time eligibility engine. The correct question is rarely "Why is this person not in Check-In?" The better question is:

> For this check-in configuration, on this device, at this campus, during this schedule window, for this person and family, what groups, locations, schedules, labels, and attendance records does Rock believe are available?

When the source material is thin, verify in the live instance instead of assuming. Inspect block settings, group type settings, group locations, schedules, devices, labels, security permissions, and actual `Attendance` / `AttendanceOccurrence` rows.

## 2. Scope And Terminology

This guide covers Rock RMS Check-In as an operational concept: attendance, kiosks, labels, families, schedules, locations, mobile check-in, rapid attendance entry, self-entry, analytics, and troubleshooting. It intentionally includes related areas because Check-In depends on them.

The main terms are:

**Check-in configuration**: The administrator-defined setup that controls a Check-In flow. It defines whether the flow is individual or family-oriented, which check-in areas and groups are considered, how locations are selected, how people are searched, whether inactive people are prevented, and how printing works. The official manual identifies "Check-in Type" as the field that selects Individual vs. Family and notes that Family allows multiple family members to be checked in at once ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

**Check-in area**: Usually a group type used as an attendance area. RockU separates "Types and Groups" from "Locations" and "Schedules", which is a useful operational division: the area describes the ministry category, groups represent classes or rooms, locations represent physical or named places, and schedules represent meeting times ([Types and Groups](https://community.rockrms.com/rocku/check-in/types-and-groups), [Locations](https://community.rockrms.com/rocku/check-in/locations), [Schedules](https://community.rockrms.com/rocku/check-in/schedules)).

**Group type**: The template for groups. For attendance and Check-In, the group type is where an agent should verify whether groups can take attendance, whether check-in is supported, and whether inherited settings are shaping child groups. Community examples also rely on group type settings such as "Takes Attendance", attendance reminders, schedule options, group history, and allowed workflows ([Watch Party Attendance](https://community.rockrms.com/recipes/197)).

**Group**: The ministry unit into which a person is checked. In children's ministry this may be a room or class. In adult attendance, it may be a worship service group, congregation group, small group, event group, or special attendance group.

**Location**: The named place associated with a group. It may map to a physical room, a check-in location, or another named location. The official manual states that printer routing can be tied to either devices or locations through Admin Tools > Check-in > Devices and Admin Tools > Check-in > Named Locations ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

**Schedule**: The time window or meeting schedule attached to check-in opportunities. A person may be eligible for a group but not offered it because the schedule is not active for the current moment. Attendance analytics stored procedures also use schedule filters and derive date windows from `AttendanceOccurrence.SundayDate` in the source snippets ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)).

**Device**: The kiosk, tablet, or virtual device through which check-in is run. RockU has a separate Devices topic, and mobile check-in configuration depends on virtual kiosk devices in the source pack ([Devices](https://community.rockrms.com/rocku/check-in/devices), [Mobile Check-in Configuration insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).

**Kiosk**: The active check-in station. In traditional check-in this is the physical device or browser session. In mobile check-in, a virtual kiosk can be used as a configured endpoint for mobile sessions and label handoff.

**Label**: A print artifact produced from a check-in session. The v2 label source shows attendance labels are generated per attendance record, not simply per person, and label data includes attendance, person, location, family, session attendance, and achievement context ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)).

**Security code**: The family or attendance security code printed on labels and used for pickup or checkout. Source-code snippets show next-generation label formatters can render security-code combinations such as nickname plus code, code plus nickname, or code only ([SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs)).

**Attendance**: The persisted record that a person attended or was checked in. In source snippets, attendance analytics queries join `Attendance` to `AttendanceOccurrence`, `PersonAlias`, groups, schedules, campuses, and locations, and filter by `DidAttend = 1` ([AttendanceAnalytics attendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql)).

**Attendance occurrence**: The group/schedule/location occurrence against which attendance is recorded. Analytics and troubleshooting must inspect this table because the group, location, schedule, occurrence date, and Sunday date generally live there rather than only on the attendance row.

**Rapid Attendance Entry**: A block for efficiently entering attendance manually for a group of people. Source code describes it as a way to manually enter attendance for a large group efficiently, with settings for group selection, schedule, attendance date, campus, relationships, age limit, and related contact/family entry behavior ([RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs)).

**Mobile Check-In**: A phone-app version of the check-in flow. The source docs describe it as using the same v2 engine as kiosks through `CheckInSession`, with the same opportunity filters and attendance rows, while presenting a mobile-native UI ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)).

**Proximity Attendance**: A mobile feature introduced in the source pack as requiring mobile v7.0 and Rock v17.1. It uses beacon monitoring to trigger automatic check-in/check-out behavior when a mobile device enters or leaves a beacon area ([Proximity Attendance](https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance)).

## 3. Check-In Mental Model

The most useful mental model is a pipeline:

1. A user starts from a kiosk, mobile app, Check-In Manager, Rapid Attendance Entry, group attendance block, workflow, QR code page, SMS keyword, or proximity trigger.
2. Rock resolves a person or family.
3. Rock evaluates available check-in opportunities from the selected configuration.
4. Rock filters those opportunities by group type, group, location, schedule, person eligibility, family relationships, active status, age/grade, capacity, campus, and any configured check-in rules.
5. Rock presents choices or auto-selects them depending on configuration.
6. Rock writes attendance.
7. Rock generates labels or other output.
8. Rock surfaces the result through roster, checkout, analytics, reports, dashboards, or custom integrations.

The official manual explains that the screen flow depends on whether the guest checks in an individual or a family and on the administrator’s check-in system settings ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). That means the UI is not the source of truth. It is a projection of configuration plus current availability.

For a family check-in, Rock first identifies the family, then offers family members and eligible opportunities. The manual uses a family example and describes the Welcome and Search steps; it also notes that phone search can require only four digits by default, with that behavior configurable ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). Agents should never assume a phone search failure means the family record does not exist. It may mean the search key is not available, a phone number is not attached where expected, search length rules differ, or the kiosk is not using the intended configuration.

For eligibility, think in terms of "opportunities." A check-in opportunity is the combination of:

- Area / group type
- Group
- Location
- Schedule
- Campus
- Person
- Family / relationship context
- Date and time
- Device and configuration context

If any component is missing or excluded, the opportunity may not appear. This is why a room can be configured but unavailable, or a child can be in the database but missing from the kiosk.

For attendance, think in terms of `Attendance` plus `AttendanceOccurrence`. Source snippets for analytics repeatedly join `Attendance` to `AttendanceOccurrence` and filter `DidAttend = 1`; they also use fields such as `GroupId`, `ScheduleId`, `LocationId`, `CampusId`, `StartDateTime`, and `SundayDate` ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql), [AttendeeLastAttendance procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_AttendeeLastAttendance.sql)). If analytics disagree with a roster, inspect both tables and verify the filters.

For labels, think in terms of per-attendance output. Source code states that attendance labels are printed for every attendance record, so a person checked into two service times can receive two attendance labels ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)). A parent label, child label, security label, allergy label, achievement label, or custom icon label can all be affected by the same underlying session data but may be configured independently.

For mobile, think "same engine, different shell" when using the v2 mobile check-in path. The GitHub docs explicitly describe mobile check-in as using the same v2 engine and standard `CheckInSession`, with mobile UI differences but shared eligibility, attendance, and label generation behavior ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)). However, the live instance must be checked for the actual Rock version, app shell version, mobile block settings, and whether the instance is using legacy or next-generation check-in components.

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. Official Rock documentation and manuals.
2. Rock source code and repository docs.
3. RockU training pages and approved transcript insights.
4. Developer docs.
5. Release notes and source-adjacent release summaries.
6. Model Map / database inspection in the live Rock instance.
7. Community recipes and Q&A, only as examples or implementation patterns.

The main official documentation source in this pack is [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266). It is the anchor for configuration concepts and version updates. It includes release notes for multiple Rock versions and describes check-in systems, registration mode, lingo, individual/family check-in, previous check-ins, and important settings.

The main training index is [RockU Check-In](https://community.rockrms.com/rocku/check-in). Its topic list is operationally useful even where hydrated excerpts are limited: Getting Started, Locations, Schedules, Types and Groups, Settings, Devices, Labels, Running Check-In, Attendance Analytics, Check-In Manager, Rapid Attendance Entry, Person Attributes in Check-In Manager, Aero Check-In Theme, Mobile Check-In, Attendance Self-Entry, Celebrations, and Next-Gen Labels.

The most useful source-code records in this pack are:

- [docs/check-in/mobile-check-in.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md): mobile check-in concept and architecture.
- [Rock.Blocks/Mobile/CheckIn/CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs): mobile Check-In block attributes and custom settings.
- [RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs): Rapid Attendance Entry block attributes.
- [RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs): Attendance Analytics block settings.
- [Rock/CheckIn/v2/Labels/AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs), [LabelAttendanceDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelAttendanceDetail.cs), and [SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs): label data model and formatter behavior.
- Attendance analytics procedures such as [spCheckin_AttendanceAnalyticsQuery_AttendeeDates](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql), [spCheckin_AttendanceAnalyticsQuery_Attendees](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql), and [spCheckin_AttendanceAnalyticsQuery_NonAttendees](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql).

Community recipes should not be treated as authoritative Rock behavior. They are useful examples for custom patterns, such as QR-code attendance workflows, text-to-check-in, custom labels, group check-in summaries, or Obsidian attendance confirmation. The Rock Community recipe pages themselves warn that recipes are community-contributed and not reviewed or endorsed by the core team ([QR Code Check-in System](https://community.rockrms.com/recipes/483), [Text to Check In](https://community.rockrms.com/recipes/116), [Group Check-In Summary Template](https://community.rockrms.com/recipes/370)).

For live work, use this guide as a reasoning map, not a substitute for inspection. Before making configuration recommendations, inspect:

- Rock version and mobile shell version.
- Whether the instance is using legacy Check-In, next-generation Check-In, or a hybrid.
- Check-in configuration settings.
- Group type inheritance.
- Group locations and schedules.
- Device and kiosk configuration.
- Printer assignment and print path.
- Label definitions and merge fields.
- Security permissions and verbs.
- Actual attendance rows and occurrences.
- Block settings for Check-In Manager, Rapid Attendance Entry, Attendance Analytics, mobile Check-In, group attendance, or custom workflow pages.

## 5. Core Configuration And Data Model

Check-In configuration begins with ministry structure. The order matters.

### Check-In Systems

The official manual describes multiple check-in system patterns: centralized self-service, decentralized check-in, and centralized attended check-in ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). These are not merely deployment styles. They shape how devices, staff, families, printers, and troubleshooting are arranged.

Centralized self-service check-in usually means families walk to a kiosk, search themselves, make selections, and receive labels. The operational risk is kiosk availability, printer reliability, and search/eligibility clarity.

Decentralized check-in usually means check-in happens closer to rooms, classes, or ministry areas. The operational risk is device sprawl, inconsistent configurations, room-level printer mappings, and local volunteer permissions.

Centralized attended check-in usually means staff or volunteers operate the flow. The operational risk is security role design, speed, mistaken family selection, and the need for staff-only override or add-person workflows.

Registration mode appears in the manual as a related concept. Use it when the flow is not simply "record attendance now" but includes the process of registering or adding people into a check-in context. Because the source pack does not include the full registration-mode details, verify the exact behavior in the live Rock version before relying on it for production.

### Check-In Type: Individual vs Family

The official manual identifies the check-in type as the field that selects individual vs family. Family check-in allows multiple family members to be checked in together ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). This choice affects screens, labels, and family selection.

Use Individual Check-In when the person is the main unit of interaction: volunteers, students, adult classes, or self-entry style attendance. Use Family Check-In when the family is the interaction unit: parents checking in children, guardians receiving pickup labels, or a mobile user checking in multiple family members.

Agents should verify whether a complaint is about the person being missing from the family search, the person being present but not eligible for any group, or the family member not being included due to family/relationship data.

### Search

The official manual states that the Search By Phone screen lets guests enter their phone number and that the default can require only four digits, with configurability ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). Search problems should be separated into:

- No family/person found.
- Too many families found.
- Family found, but intended person absent.
- Person found, but no check-in opportunities.
- Person found, opportunities shown, but save or print fails.

Inspect phone numbers, search keys, family membership, duplicate records, record status, connection status, and configuration-level search settings. If the source pack does not specify a particular setting name in the live Rock version, inspect the block and check-in configuration fields directly.

### Group Membership Behavior

The official manual excerpt includes two important membership modes: `Add On Check In` and `Already Belongs`. If `Add On Check In` is selected, the person is added to the check-in group when they check in. If `Already Belongs` is selected, the person must already be a group member or they cannot check in ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

This one setting explains many "missing child" or "missing attendee" problems. If a room is configured as `Already Belongs`, a person can satisfy age and schedule rules but still not appear because they do not have a group member row. If the group is `Add On Check In`, the first check-in can create membership, which changes future eligibility and reporting.

Agents should inspect:

- Group type check-in membership setting.
- Specific group membership records.
- Group member status.
- Group member role.
- Whether group type inheritance overrides the visible group setting.
- Whether a data view or custom filter is used in addition to membership.

### Locations

Locations in Check-In are both operational and analytical. Operationally, they can represent rooms and printer routing. Analytically, they are part of the `AttendanceOccurrence` record and can affect reports.

The manual states that printers can be assigned through Admin Tools > Check-in > Named Locations and Admin Tools > Check-in > Devices, depending on print routing ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). RockU also separates the Locations topic, reinforcing that location setup is a core step rather than decoration ([Locations](https://community.rockrms.com/rocku/check-in/locations)).

Inspect:

- Named location exists.
- Group has the location assigned.
- Location has expected schedules.
- Location is active and in the correct campus context.
- Location printer is configured if print routing uses location printer.
- Capacity is configured if the room should fill or close.
- Location naming is consistent enough for staff and analytics.

### Schedules

Schedules determine availability and reporting windows. RockU has a dedicated schedules lesson ([Schedules](https://community.rockrms.com/rocku/check-in/schedules)). Source-code analytics records show that attendance reporting uses date-window logic against `AttendanceOccurrence.SundayDate`, and schedule filters appear in stored procedures ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)).

For troubleshooting, inspect:

- Schedule exists.
- Schedule is assigned to the group location or relevant group.
- Current date/time falls within check-in start/end windows.
- Time zone is correct.
- Schedule is attached at the level the check-in engine expects.
- Attendance occurrence was created for the expected date.
- Analytics report uses the same schedule filter as the check-in flow.

A common operational problem is that staff inspect a group and see a schedule but the active check-in flow is evaluating a different schedule path, a parent group type, a location schedule, or an occurrence-specific schedule. In live work, query the actual group-location-schedule relationships rather than relying on one screen.

### Print Routing

The official manual excerpt identifies a `Print To` setting with at least two choices: `Device Printer` and `Location Printer`. Device printers are configured under Admin Tools > Check-in > Devices. Location printers are configured under Admin Tools > Check-in > Named Locations ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Agents should diagnose printing as a routing problem first, then a printer problem:

1. Which labels were requested by the check-in session?
2. Which printer routing mode is configured?
3. Which device or location was selected?
4. Which printer is assigned to that device or location?
5. Does the label template use a format supported by that printer?
6. Does the printer have fonts or image support required by the label?
7. Did Rock generate the print job but fail to deliver it?
8. Did the printer receive the job but fail to print correctly?

### Location Selection Strategy

The official manual excerpt identifies `Location Selection Strategy` and says the default option is `Ask` ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). The source pack excerpt does not include all options, so do not invent exact option names. In live work, inspect the configuration field and version-specific help text. Operationally, this setting answers whether Rock asks the family to choose a room, selects automatically, or uses a fill strategy.

For capacity-sensitive ministries, verify this setting with actual check-in tests. A room can appear "wrong" because Rock is filling rooms by strategy rather than presenting every option.

## 6. Primary Entities And Relationships

The minimum Check-In entity graph is:

- `Person`
- `PersonAlias`
- Family `Group`
- Check-in area `GroupType`
- Check-in `Group`
- `GroupMember`
- `Location` / named location cache
- `Schedule`
- `Device`
- `Attendance`
- `AttendanceOccurrence`
- Label definitions and label data
- Campus
- Security roles and permissions

### Person, PersonAlias, And Family

Attendance source snippets join `Attendance.PersonAliasId` through `PersonAlias` to person identity ([AttendanceAnalytics attendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql)). When troubleshooting attendance, use `PersonAlias` correctly. Do not assume `Attendance` directly stores `PersonId`.

Family matters because family check-in presents family members and creates a shared pickup context. Source-code label data includes a `Family` object determined through kiosk search or primary family when checking in a single person by API call ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)). For family-related issues, inspect:

- Primary family group.
- Family roles.
- Adult/child relationships.
- `Can check-in` relationship if relevant.
- Phone numbers and search keys.
- Custody/security notes if local policy uses them.
- Whether inactive people are prevented by configuration.

### GroupType, Group, GroupMember

Group type is the source of inherited attendance behavior. Community examples show group type settings such as `Takes Attendance`, attendance reminders, named schedule options, group history, and role configuration being used to build attendance workflows ([Watch Party Attendance](https://community.rockrms.com/recipes/197)). The Q&A example for smaller churches also points to group attendance as a practical pattern, with the key requirement that the group type has `Takes Attendance` enabled ([How rapid can Rapid Attendance be?](https://community.rockrms.com/ask/using/2804)).

For Check-In eligibility, inspect:

- Group type takes attendance / supports check-in.
- Group type inheritance.
- Group active status.
- Group membership requirement mode.
- Group members and roles.
- Group campus.
- Group locations.
- Group schedule options.
- Group attributes used by custom Lava, workflows, or data views.

### GroupLocation, Location, Schedule

A group may be eligible generally but unavailable because no active group-location-schedule combination exists. Community Lava examples inspect group locations and schedules to show whether a group is check-in ready ([Group Check-In Summary Template](https://community.rockrms.com/recipes/370)). Treat that recipe as an example pattern, not core behavior.

In live work, inspect the actual relational shape in the instance. Depending on Rock version and configuration, the relevant data may be visible through group detail screens, group location screens, named locations, schedule lists, or direct SQL.

### Device And Kiosk

Devices carry operational context: campus, printer, check-in configuration, and sometimes kiosk behavior. RockU includes a Devices lesson ([Devices](https://community.rockrms.com/rocku/check-in/devices)). Mobile check-in configuration depends on virtual kiosk devices, geofenced campus boundaries, and the Mobile Check-in Launcher block being pointed at the correct devices, configuration, theme, and areas ([Mobile Check-in Configuration insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).

For device troubleshooting, inspect:

- Device record exists and is active.
- Device is assigned to the expected campus.
- Device is tied to the expected printer.
- Device points to the intended check-in configuration.
- Device-specific settings do not override the expected flow.
- For mobile, virtual kiosk devices exist and match the launcher settings.
- For label handoff, the iPad or kiosk scanning QR codes is configured for the intended print target.

### Attendance And AttendanceOccurrence

The attendance persistence model is central. Source snippets show analytics queries using:

- `Attendance.PersonAliasId`
- `Attendance.CampusId`
- `Attendance.StartDateTime`
- `Attendance.DidAttend`
- `AttendanceOccurrence.GroupId`
- `AttendanceOccurrence.ScheduleId`
- `AttendanceOccurrence.LocationId`
- `AttendanceOccurrence.SundayDate`
- joins to `PersonAlias`, `Group`, `Campus`, and `Location` ([AttendeeLastAttendance procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_AttendeeLastAttendance.sql), [AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)).

When an agent needs to prove whether someone checked in, do not rely only on the UI. Inspect:

- `Attendance` row for person alias and date.
- `DidAttend`.
- `StartDateTime` and `EndDateTime`.
- `AttendanceOccurrence` group/location/schedule.
- Campus.
- Whether checkout wrote `EndDateTime`.
- Whether duplicate attendance exists for multiple service times.
- Whether analytics filters include the same group, campus, schedule, and date basis.

### Labels

The v2 label model includes data objects that carry attendance, person, location, all attendance in a session, family, and achievement context ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)). `LabelAttendanceDetail` includes properties such as person, start and end date/time, first-time flag, area, campus, checked-in-by person, device, group, location, schedule, group members, and search type context ([LabelAttendanceDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelAttendanceDetail.cs)).

This matters because a label issue can be caused by data not existing, data existing under a different attendance record, or the formatter using a different field than expected.

## 7. Common Check-In Workflows

### Family Kiosk Check-In

A typical family kiosk flow is:

1. Family arrives at kiosk.
2. Welcome screen appears. If no locations are active, the manual says the guest may see a countdown to opening time ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).
3. Family searches, often by phone.
4. Rock resolves matching families.
5. Family selects children or family members.
6. Rock evaluates available groups, locations, and schedules.
7. Rock asks for or auto-selects location depending on configuration.
8. Attendance records are saved.
9. Labels print for child, parent, security, or other configured labels.
10. Check-In Manager or roster surfaces the checked-in people.

Operational checks:

- Confirm the current time is inside the active check-in window.
- Confirm the intended family is found by search.
- Confirm the child is active and in the family.
- Confirm the group is available for the child’s age/grade/membership.
- Confirm the room has capacity.
- Confirm the correct printer route is active.
- Confirm attendance rows were written.

### Individual Check-In

Individual check-in is useful for volunteers, adult services, student ministries, or any context where a single person checks in without family selection. The official manual ties this to the `Check-in Type` field ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Operational checks:

- Person can be found.
- Person is active unless configuration allows inactive people.
- The group allows the person to check in.
- The group/location/schedule is currently active.
- The device is scoped to the correct check-in area.
- Attendance rows write to the expected group occurrence.

### Attended Check-In

In attended check-in, staff or volunteers operate the flow. This increases the importance of permissions, training, and confirmation.

Verify:

- Staff have access to the check-in page or manager.
- Staff can search and select families.
- Staff can add or edit families if local policy allows.
- Version-specific settings permit family edits if using next-generation Check-In. A release summary notes v17.1 added kiosk device settings allowing individuals to add or edit family information using Next-Gen Check-In ([Triumph GitHub Spotlight 4/16/2025](https://www.triumph.tech/resources/github-spotlight-4162025)); verify against official release notes and the live Rock version before enabling.

### Check-In Manager

Check-In Manager is an operational tool for rosters and intervention. RockU includes both legacy/current Check-In Manager topics, including a 10:23 lesson and a newer 8:40 lesson in the hydrated RockU index ([Check-in Manager](https://community.rockrms.com/rocku/check-in/check-in-manager), [Check-In Manager](https://community.rockrms.com/rocku/check-in/check-in-manager-1)). The official manual excerpt says Rock 14 added a security verb controlling who can delete attendance from the Check-In Manager roster, allowed checkout to be enabled for kiosk, Check-In Manager, or both, and allowed roster filtering by schedule ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

For agents:

- Verify which Check-In Manager version/page/block is in use.
- Check security verbs before concluding a user "cannot delete" or "cannot checkout" due to a bug.
- Check whether checkout is enabled for kiosk, Check-In Manager, or both.
- Use schedule filters when comparing roster to attendance rows.
- Inspect person attributes if the issue involves display or special handling; RockU includes a Person Attributes - Check-In Manager lesson ([Person Attributes - Check-In Manager](https://community.rockrms.com/rocku/check-in/person-attributes-check-in-manager)).

### Rapid Attendance Entry

Rapid Attendance Entry is for fast manual attendance entry. The source code describes it as a block that "provides a way to manually enter attendance for a large group of people in an efficient manner" ([RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs)). Its UI includes group, location, schedule, attendance date, and campus selection controls in the source markup ([RapidAttendanceEntry.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx)).

Important block settings from source snippets include:

- `Add Family Page`
- `Attendance List Page`
- `Enable Attendance`
- `Parent Group`
- `Attendance Group`
- `Show Can Check-In Relationships`
- `Attendance Age Limit`
- `Show Campus`
- `Campus Types`

The approved RockU transcript insight says Rapid Attendance Entry can collect related ministry information such as family updates, notes, prayer requests, and workflow launches when block settings enable those actions ([Rapid Attendance Entry insight](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)).

Use Rapid Attendance Entry when:

- The attendance taker knows who attended.
- The group list is the primary interaction.
- A kiosk and labels are unnecessary.
- Staff need related updates or workflow actions during attendance entry.

Do not assume Rapid Attendance Entry is the best path for all small churches. A Q&A example suggests group attendance can be as simple as creating general groups for congregations and clicking names in group attendance, with `Takes Attendance` enabled on the group type ([How rapid can Rapid Attendance be?](https://community.rockrms.com/ask/using/2804)). Compare the operational burden of Rapid Attendance, group attendance, and custom workflows.

### Group Attendance

Group attendance is related but distinct from full Check-In. RockU has a Group Attendance lesson ([Group Attendance](https://community.rockrms.com/rocku/groups/group-attendance)). Mobile developer docs also include a Group Attendance Entry block that displays group members for attendance entry on a specified date. The mobile doc states that, unlike web, groups must have a schedule configured to use that mobile block ([Group Attendance Entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).

Use group attendance for:

- Small groups.
- Adult classes.
- Services where a known roster is sufficient.
- Ministry leader self-reporting.
- Situations where labels, pickup security, and room assignment are unnecessary.

Inspect group type `Takes Attendance`, group schedule, group members, and permissions.

### Attendance Self-Entry

RockU includes Attendance Self-Entry as a Check-In training topic ([Attendance Self-Entry](https://community.rockrms.com/rocku/check-in/attendance-self-entry)). The source pack does not include enough details to state exact configuration fields. In a live Rock instance, inspect the self-entry page, block type, block settings, security, and target attendance group. Confirm whether self-entry creates ordinary attendance rows, whether it allows family members, and whether it supports workflows or notes.

### Mobile Check-In

Mobile check-in lets people start check-in from a mobile device. An approved RockU insight says mobile check-in is contactless and can hand off completed check-ins to label printing through a QR code scanned by a configured iPad kiosk ([Mobile Check-in Overview insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)). Another insight says configuration depends on virtual check-in kiosk devices, geofenced campus boundaries, and pointing the Mobile Check-in Launcher block at the correct devices, check-in configuration, theme, and areas ([Mobile Check-in Configuration insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).

The repository docs describe mobile check-in as using the same v2 engine as kiosk check-in, including `CheckInSession`, opportunity filters, attendance row writing, and label generation ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)). The mobile Check-In block source includes custom settings for `Configuration Template`, `Areas`, and `Kiosk` ([Mobile CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs)).

For live validation:

- Confirm mobile app version and Rock version.
- Confirm the mobile block is present on the expected page.
- Confirm `Configuration Template`, `Areas`, and `Kiosk` settings.
- Confirm virtual kiosk device exists.
- Confirm geofence/campus boundary if used.
- Confirm label handoff device can scan and print.
- Confirm attendance rows match kiosk behavior.

### Proximity Attendance

Developer docs state Proximity Attendance uses iBeacon-style beacons so a mobile device can detect entry/exit and trigger check-in/check-out behavior. The pack marks it as mobile v7.0 and Rock v17.1 ([Proximity Attendance](https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance)).

Because proximity attendance touches mobile background behavior, device permissions, beacon configuration, and automatic attendance records, agents should verify:

- Rock version supports it.
- Mobile app/shell version supports it.
- Beacon UUID/major/minor configuration.
- Mobile shell `StartBeaconMonitoring` and `StopBeaconMonitoring` actions if used.
- User permission prompts for Bluetooth/location/background behavior.
- Attendance record creation and checkout/end time behavior in test conditions.
- Privacy and ministry policy approval.

## 8. Labels Deep Dive

Labels are operationally critical because they connect attendance records to physical custody, room assignment, allergies, special instructions, and pickup security.

### Legacy Labels And Next-Gen Labels

RockU includes both `Labels [Legacy]` and `Next-Gen Labels` topics ([Labels Legacy](https://community.rockrms.com/rocku/check-in/labels-legacy), [Next-Gen Labels](https://community.rockrms.com/rocku/check-in/next-gen-labels)). The hydrated excerpts do not include full behavior, so agents must inspect the live instance to determine whether a label is legacy, next-generation, or a mix.

Use official docs and source code first. Community recipes are useful examples but not core authority. For example, the parent/child label recipe describes creating custom 3x2 parent and child labels using the Rock Icon Font and a label merge field under Admin Tools > Check-in > Label Merge Fields and Check-in Labels ([Check-in Parent and Child Labels](https://community.rockrms.com/recipes/125)). Treat that as a customization pattern.

### Label Data Model

Source code gives the clearest model. `AttendanceLabelData` says attendance labels print for every attendance record, not merely every person. It also exposes:

- Current `Attendance`
- `Person`
- `Location`
- `PersonAttendance`
- `AllAttendance`
- `Family`
- Completed and in-progress achievement names and IDs ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs))

`LabelAttendanceDetail` exposes:

- Person
- Start date/time
- End date/time
- First-time flag
- Area
- Campus
- Checked-in-by person
- Device
- Group
- Location
- Schedule
- Group members
- Search context ([LabelAttendanceDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelAttendanceDetail.cs))

This means label fields can be tied to the actual attendance occurrence, not just the selected person. When a label says the wrong room, inspect the attendance occurrence. When it says the wrong campus, inspect the attendance row and selected opportunity. When it does not show a first-time icon, verify how the current Rock version computes `IsFirstTime`, and compare against prior attendance records.

### Security Code Formatting

The security-code formatter source shows options for nickname/code combinations and code-only output ([SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs)). Agents should inspect the label field configuration before assuming a missing security code is a check-in engine failure.

Troubleshooting steps:

1. Confirm attendance was saved.
2. Confirm a security code was generated for the session/attendance.
3. Confirm the label includes a security-code field.
4. Confirm the formatter option is correct.
5. Confirm the print job uses the expected label definition.
6. Confirm the printer output is not clipping the field.

### Merge Fields And Lava

Community label recipes often use Lava and merge fields. The parent/child label recipe gives an example of creating a label merge field using group, location, and schedule data ([Check-in Parent and Child Labels](https://community.rockrms.com/recipes/125)). Use recipes cautiously:

- Verify Lava commands enabled on the label.
- Verify merge field entity context.
- Verify field names against the current label engine.
- Test with a real check-in session, not only a design preview.
- Use Labelary or a printer-compatible preview where possible; the official manual’s version notes mention a tip about using Labelary when creating custom labels ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

### Fonts And Icons

Labels can depend on Zebra fonts, Rock Icon Font, or custom fonts. Community recipes describe installing the Rock Icon Font and custom icon fonts for printer labels ([Check-in Parent and Child Labels](https://community.rockrms.com/recipes/125), [Install CUSTOM Icon Font on Printer Label](https://community.rockrms.com/recipes/424)). These are not official guarantees. Before production:

- Verify printer model.
- Verify ZPL support.
- Verify font file size and encoding.
- Verify installation commands.
- Print a test label from the same device and printer path used in Check-In.
- Confirm fallback behavior if the font is absent.

### Label Troubleshooting Branches

If no labels print:

- Confirm attendance records were created.
- Confirm labels are enabled for the selected configuration/group.
- Confirm print routing: device printer vs location printer.
- Confirm printer assigned to the selected device or location.
- Confirm printer service/cloud print is online.
- Confirm device can reach the printer path.
- Confirm the label type matches the engine in use.

If labels print for the wrong room:

- Inspect `AttendanceOccurrence.LocationId`.
- Inspect location selection strategy.
- Inspect room capacity/fill strategy.
- Inspect whether the person selected multiple schedules or rooms.
- Confirm label field uses attendance location, not group default or stale custom Lava.

If labels print duplicates:

- Confirm whether the person checked into multiple schedules.
- Remember v2 attendance labels can print per attendance record ([AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)).
- Inspect `Attendance` rows for duplicate occurrences.
- Inspect retry behavior if the kiosk was refreshed.
- Inspect custom workflows that may reprint labels.

If parent label and child label codes differ:

- Inspect whether both labels are generated from the same session.
- Inspect custom label merge fields.
- Inspect whether a reprint occurred from a different attendance context.
- Verify security-code formatter and label data source.

## 9. Mobile Check-In Deep Dive

Mobile Check-In is best understood as a separate UI surface over shared check-in logic, but only for the v2 path described in the source docs. The repository docs say mobile uses `CheckInSession`, the same opportunity filter chain, the same attendance rows, and the same label generation as kiosk check-in ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)).

### Architecture

The mobile shell renders mobile blocks. The server-side mobile Check-In block is defined in `Rock.Blocks.Mobile.CheckIn.CheckIn` and is categorized as `Mobile > Check-in` with the description "Check yourself or family members in/out" ([Mobile CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs)).

The source snippet exposes these key custom settings:

- `Configuration Template`: the check-in configuration to use for the block.
- `Areas`: the check-in areas to use.
- `Kiosk`: the kiosk to use for the block.

That means a mobile failure can be caused by a block-level setting even when the normal kiosk works.

### Configuration Checklist

For mobile check-in, inspect:

1. Mobile site/page exists.
2. Mobile Check-In block is present.
3. Block points to the correct configuration template.
4. Block areas are correct.
5. Block kiosk is correct.
6. Virtual kiosk device exists and is active.
7. Campus/geofence boundary is configured if required.
8. Mobile launcher points to the intended devices, configuration, theme, and areas ([Mobile Check-in Configuration insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).
9. User authentication and family resolution work.
10. Label handoff process is configured if labels are required.

### QR Label Handoff

RockU insight says mobile check-in can hand off completed check-ins to label printing through a QR code scanned by a configured iPad kiosk ([Mobile Check-in Overview insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)). Operationally, this means the mobile device may not print directly. The label print may happen only after the family arrives and scans.

Troubleshoot QR handoff by checking:

- Mobile session completed.
- QR code appears and is current.
- iPad/kiosk is configured for the intended virtual or physical kiosk.
- Scanning app has camera permission.
- Label printer is assigned to the kiosk or location.
- The mobile attendance session has not expired.
- The scanned session maps to the same check-in configuration.

### Mobile And Eligibility

Because source docs describe mobile as sharing the same opportunity filters, if kiosk and mobile disagree, inspect the settings that differ:

- Kiosk/device context.
- Campus/geofence context.
- Areas configured on the mobile block.
- Kiosk setting on the mobile block.
- Authentication state.
- Family resolution.
- Version mismatch between mobile shell and Rock server.
- Legacy vs v2 / next-generation components.

Do not assume mobile has a separate eligibility engine unless the live version or custom code proves it.

### Mobile Group Attendance Entry

The mobile developer docs include a Group Attendance Entry block. It displays a list of group members that can be selected to mark attendance for a specified date. The docs state that unlike web, groups must have a schedule configured for this mobile block ([Group Attendance Entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).

Important settings from the excerpt include:

- Number of days forward to allow.
- Number of days back to allow.
- Save redirect page.
- Show save button.

Use this for leader-entered attendance, not for label-driven family check-in. Verify permissions and schedule configuration.

### Proximity Attendance

Proximity Attendance uses beacons and mobile background detection. The developer docs identify `StartBeaconMonitoring`, `StopBeaconMonitoring`, a Beacon Debug View, and a merge field section ([Proximity Attendance](https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance)). For agents, this is a high-risk automation area because false positives or background-permission issues can affect attendance accuracy.

Before enabling:

- Confirm version requirements: mobile v7.0 and Rock v17.1 in the source pack.
- Confirm the organization has consent/privacy policy approval.
- Test beacon range in the physical venue.
- Test entry and exit.
- Inspect actual attendance rows and `EndDateTime`.
- Verify battery, Bluetooth, location, and app background settings.
- Document fallback attendance method.

## 10. Attendance Deep Dive

Attendance is where Check-In becomes reporting data. The same person-facing check-in action becomes rows that power rosters, analytics, metrics, dashboards, and pastoral follow-up.

### Attendance Rows

Source snippets show the analytics layer treating `Attendance` as the person-level fact table and `AttendanceOccurrence` as the occurrence-level context. Common joins include:

- `Attendance` to `AttendanceOccurrence` on occurrence ID.
- `Attendance.PersonAliasId` to `PersonAlias`.
- Occurrence group to `Group`.
- Attendance campus to `Campus`.
- Occurrence location to `Location`.
- Occurrence schedule to `Schedule`.

The procedures filter `DidAttend = 1` for attended records ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql), [AttendanceAnalytics attendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql)).

Agent checks:

- If someone appears on a roster but not analytics, verify `DidAttend`.
- If someone appears in analytics but not a room roster, verify the occurrence group/location/schedule.
- If attendance date looks off, compare `StartDateTime`, `OccurrenceDate`, and `SundayDate`.
- If campus filtering looks wrong, inspect `Attendance.CampusId`.
- If schedule filtering looks wrong, inspect `AttendanceOccurrence.ScheduleId`.

### AttendanceOccurrence SundayDate

Multiple analytics snippets derive reporting windows against `AttendanceOccurrence.SundayDate` ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)). Sunday-date bucketing is useful for weekly church reporting, but it can surprise agents investigating events outside weekend service patterns.

When debugging a report:

- Determine whether the report filters by `StartDateTime`, `OccurrenceDate`, or `SundayDate`.
- Confirm the date range includes the SundayDate, not only the literal event date.
- For multi-day events, inspect how occurrences were created.
- For non-Sunday ministries, verify whether the organization expects Sunday-week reporting.

### Attendance Analytics Block

The Attendance Analytics block source describes it as showing a graph of attendance statistics configurable by groups and date range ([AttendanceAnalytics.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs)). Source snippets show block settings including:

- `Group Types`
- `Detail Page`
- `Check-in Detail Page`
- `Chart Style`
- `Data View Category(s)`
- `Group Specific`
- `Show Schedule Filter`
- `Show View By Option`
- `Show Bulk Update Option`

The markup includes an Attendance Area picker, date range warning, copy report link, Check-in Detail button, and invalid group warning ([AttendanceAnalytics.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx)).

Troubleshoot analytics by inspecting:

- Block settings.
- Group type filters.
- Group-specific mode.
- Schedule filter visibility and selected values.
- Data view filters.
- Campus filters.
- Date range.
- User authorization for selected group.
- Stored procedures present and current for the Rock version.

### Attendees, Non-Attendees, First Dates, Last Attendance

Source snippets identify stored procedures for:

- Attendee dates.
- Attendee first dates.
- Attendee last attendance.
- Attendees.
- Non-attendees.

These use group IDs, group type IDs, date ranges, campus IDs, null campus inclusion, and schedule IDs in different combinations ([AttendeeFirstDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeFirstDates.sql), [NonAttendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql), [AttendeeLastAttendance procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_AttendeeLastAttendance.sql)).

Agent implication: a person can be counted differently across reports because the report answers a different question. "Attended during range", "first attended", "last attended", "non-attendee", and "attendance dates" are not interchangeable.

### Count-Only Attendance

Some ministries do not need person-level attendance. A community watch-party recipe describes a pattern where the ministry wanted hosts to report only numbers of adults/kids present, not individuals, and used workflows and metrics around a group type configured for attendance ([Watch Party Attendance](https://community.rockrms.com/recipes/197)). This is a custom pattern, not a core Check-In guarantee. If count-only attendance exists in a live instance, inspect whether it writes standard attendance rows, metric values, workflow attributes, or custom tables.

## 11. Troubleshooting Deep Dive

Troubleshooting Check-In requires disciplined narrowing. Start from the exact symptom and the exact context.

### Symptom: No Check-In Locations Are Active

The manual says the welcome screen can show a countdown if no check-in locations are active ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). Diagnose:

- Current server time and time zone.
- Check-in schedule start/end windows.
- Group location schedule assignment.
- Location active status.
- Check-in configuration active dates.
- Device configuration.
- Campus context.
- Whether the wrong check-in configuration is loaded.

If the countdown time is wrong, inspect the schedule definition and server/local timezone assumptions.

### Symptom: Family Search Finds Nothing

Check:

- Search mode and required digit count.
- Phone number exists on the adult/family record.
- Phone number formatting.
- Person record active status.
- Family membership.
- Duplicate records.
- Search keys.
- Kiosk configuration.
- Security restrictions.

Do not assume missing search results mean the person is not in Rock.

### Symptom: Family Found, Child Missing

Check:

- Child is in the primary family.
- Child record is active.
- Child age/grade is in range.
- Check-in configuration prevents inactive people.
- Relationship or custody restrictions.
- Group membership mode: `Already Belongs` vs `Add On Check In` ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).
- Required group membership exists.
- Can-check-in relationship settings, especially if Rapid Attendance Entry or other family relationship display is involved ([RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs)).

### Symptom: Child Present, No Rooms Available

Check:

- Group type included in configuration.
- Group active.
- Group location assigned.
- Location active.
- Schedule active now.
- Capacity not full.
- Campus context.
- Age/grade/ability rules.
- Data view filters.
- Group membership requirement.
- Location selection strategy.

### Symptom: Wrong Room Selected

Check:

- Location selection strategy.
- Capacity/fill behavior.
- Available locations for that group.
- Campus filter.
- The selected schedule.
- Whether the family selected manually.
- Whether mobile/kiosk contexts differ.
- Actual `AttendanceOccurrence.LocationId`.

### Symptom: Attendance Saved But Label Did Not Print

Check:

- Attendance rows exist.
- Label configuration for the check-in area/group.
- Print routing: device vs location printer.
- Assigned printer record.
- Printer connectivity.
- Label engine type.
- Label template errors.
- Font dependencies.
- Cloud print or kiosk handoff if mobile.
- Reprint from Check-In Manager if available.

### Symptom: Label Printed But Data Wrong

Check:

- `AttendanceOccurrence` group/location/schedule.
- `Attendance.CampusId`.
- Label field source.
- Custom Lava merge fields.
- Next-gen label formatter.
- Whether person checked into multiple occurrences.
- Whether stale or cached label definition is used.

### Symptom: Check-In Manager Cannot Delete Or Checkout

Rock 14 release notes in the manual mention a new security verb for deleting attendance from the Check-In Manager roster, checkout enablement for kiosk and/or Check-In Manager, and roster filtering by schedule ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)). Check:

- Rock version.
- User security roles.
- Block/page security.
- Delete attendance security verb.
- Checkout enabled for Check-In Manager.
- Schedule filter.
- Attendance row has not already been checked out.
- Attendance row belongs to selected manager context.

### Symptom: Rapid Attendance Entry Too Slow Or Wrong Shape

Rapid Attendance Entry may not be the right tool if the desired behavior is simply clicking known group members. The Q&A example points to group attendance for smaller congregations when a roster click workflow is desired ([How rapid can Rapid Attendance be?](https://community.rockrms.com/ask/using/2804)). Compare:

- Rapid Attendance Entry.
- Group Attendance block.
- Mobile Group Attendance Entry.
- Custom workflow.
- QR code workflow.
- SMS keyword workflow.

Inspect Rapid Attendance block settings such as attendance group, parent group, campus visibility, age limit, and relationship display ([RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs)).

### Symptom: Analytics Do Not Match Headcount

Check:

- Are analytics counting individuals or occurrences?
- Does the source use `DidAttend = 1`?
- Are multiple service times counted separately?
- Are date filters based on `SundayDate`?
- Are campus filters including null campuses?
- Are schedule filters applied?
- Is the correct group type selected?
- Is group-specific mode enabled?
- Are data view filters applied?
- Are non-person count metrics being compared to person attendance rows?

## 12. Related Rock Areas: Attendance, Groups, Locations, Schedules, Labels, Mobile, Security

### Attendance

Attendance is the persisted result. Check-In is one way to create attendance, but group attendance, rapid attendance, mobile attendance, workflows, SMS, QR pages, and proximity attendance can also create attendance-like records or related metrics. Always determine the data-writing path before troubleshooting reports.

### Groups

Groups define ministry structure. Group type inheritance can quietly control attendance and check-in behavior. If a group appears configured correctly but does not work, inspect the group type and parent settings.

### Locations

Locations are both rooms and reporting dimensions. They can also carry printers. Location naming consistency matters because volunteers, labels, and analytics all expose location names.

### Schedules

Schedules are eligibility gates. They also drive attendance occurrence timing and analytics windows. A schedule error can look like a person error, room error, or printer error.

### Labels

Labels operationalize safety. Parent/child labels, security codes, room labels, allergy notes, first-time icons, and custom fonts all depend on correct attendance context and printer compatibility.

### Mobile

Mobile Check-In adds authentication, mobile shell versioning, geofencing, virtual kiosks, QR handoff, and app permissions to the normal check-in graph. The source docs say the v2 engine is shared, but the surrounding context is different ([mobile Check-In docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)).

### Security

Security affects who can run Check-In Manager, delete attendance, checkout, edit families, access attendance analytics, view group attendance, and run custom workflows. The Rock 14 manual update around Check-In Manager delete attendance is a specific reminder that permissions can change behavior across versions ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

## 13. Administration And Operational Guardrails

### Pre-Service Checklist

Before each service or event:

- Confirm the correct check-in configuration is active.
- Confirm schedules are active for the current date.
- Confirm locations are active and mapped to groups.
- Confirm room capacities are correct.
- Confirm devices are online and assigned to the correct campus/configuration.
- Confirm printers are online, loaded, and mapped.
- Print test labels from each kiosk path.
- Confirm Check-In Manager roster loads.
- Confirm checkout behavior if used.
- Confirm mobile check-in launcher and QR handoff if used.
- Confirm staff have required permissions.
- Confirm fallback process for printer or network outage.

### Configuration Change Control

Check-In changes should be treated as production operations. A small change can affect every arriving family. Use:

- A test check-in configuration.
- A test group/location/schedule.
- A test family/person.
- A test device.
- A test printer.
- Versioned notes for changes.
- Screenshots or exported configuration evidence.
- Rollback notes.

Avoid changing group type inheritance, label definitions, or print routing immediately before a service unless the current production flow is already broken.

### Label Safety

For children's ministry:

- Test parent and child labels together.
- Confirm security codes match.
- Confirm allergy/special notes policy.
- Confirm checkout process.
- Confirm reprint policy.
- Confirm staff can handle duplicate or missing labels.
- Confirm label disposal policy for abandoned printouts.

### Data Hygiene

Check-In quality depends on data hygiene:

- Family membership accuracy.
- Child birthdate/grade accuracy.
- Phone numbers.
- Active/inactive statuses.
- Duplicate records.
- Group memberships.
- Campus assignment.
- Relationship records.
- Medical/allergy attributes if labels use them.

### Observability

Agents should recommend operational dashboards only after identifying the data source. Useful checks include:

- Active check-ins by group/location/schedule.
- Printer error rate or manual reports.
- Kiosk online status.
- Attendance rows written in the last N minutes.
- Rooms at capacity.
- Duplicate attendance rows.
- Missing checkout/end time.
- Mobile sessions started vs printed labels.
- Check-In Manager roster count vs attendance rows.

## 14. Developer, API, Lava, And Source-Code Landmarks

### Mobile Check-In Block

Source path: [Rock.Blocks/Mobile/CheckIn/CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs)

Key facts from source snippets:

- Category: `Mobile > Check-in`
- Description: "Check yourself or family members in/out."
- Supported site type: mobile.
- Custom settings include `Configuration Template`, `Areas`, and `Kiosk`.
- Uses namespaces including `Rock.CheckIn`, `Rock.CheckIn.v2`, `Rock.CheckIn.v2.Labels`, and view models for Check-In.

Use this file when diagnosing mobile block behavior, custom actions, or whether the block is pointed at the right configuration.

### Mobile Check-In Docs

Source path: [docs/check-in/mobile-check-in.md](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md)

Key facts from source snippets:

- Mobile Check-In is the phone-app version of kiosk flow.
- It uses the same v2 engine as kiosk.
- It uses `CheckInSession`.
- It writes the same `Attendance` rows.
- It applies the same opportunity filters.
- Labels can be produced and routed through cloud print if configured.

Use this when explaining why mobile and kiosk should usually agree, then inspect configuration differences if they do not.

### Rapid Attendance Entry

Source paths:

- [RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs)
- [RapidAttendanceEntry.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx)
- [RapidAttendanceEntry.css](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Styles/Blocks/Checkin/RapidAttendanceEntry.css)

Key block attributes include `Add Family Page`, `Attendance List Page`, `Enable Attendance`, `Parent Group`, `Attendance Group`, `Show Can Check-In Relationships`, `Attendance Age Limit`, `Show Campus`, and `Campus Types`.

Use this when the request involves fast manual attendance, contact entry, campus filtering, age limits, or relationship-based display.

### Attendance Analytics

Source paths:

- [AttendanceAnalytics.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs)
- [AttendanceAnalytics.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx)

Key block settings include group types, detail pages, chart style, data view categories, group-specific mode, schedule filter visibility, view-by option, and bulk update option.

Use this when analytics output differs from expected attendance.

### Label Data

Source paths:

- [AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs)
- [LabelAttendanceDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelAttendanceDetail.cs)
- [ILabelDataHasAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/ILabelDataHasAttendance.cs)
- [SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs)

Use these when troubleshooting label fields, security code formatting, multiple attendance labels, or custom label data.

### Attendance Analytics Stored Procedures

Source paths:

- [spCheckin_AttendanceAnalyticsQuery_AttendeeDates](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)
- [spCheckin_AttendanceAnalyticsQuery_AttendeeFirstDates](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeFirstDates.sql)
- [spCheckin_AttendanceAnalyticsQuery_Attendees](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql)
- [spCheckin_AttendanceAnalyticsQuery_NonAttendees](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql)

Use these when reconciling analytics to raw attendance rows.

### Lava And Community Patterns

Community recipes show common extension patterns:

- Toast confirmation around Obsidian Group Attendance Detail ([recipe 461](https://community.rockrms.com/recipes/461)).
- QR-code attendance workflow ([recipe 483](https://community.rockrms.com/recipes/483)).
- Text-to-check-in workflow using SMS and Workflow Import/Export in Rock v9+ ([recipe 116](https://community.rockrms.com/recipes/116)).
- Group check-in summary Lava template ([recipe 370](https://community.rockrms.com/recipes/370)).
- Custom label fonts and icons ([recipe 424](https://community.rockrms.com/recipes/424)).

Treat all recipes as implementation ideas requiring security, performance, and version review.

## 15. Reporting, Analytics, And Model Map

### Reporting Basis

When building reports, first decide the unit of analysis:

- Person attended at least once.
- Person attendance occurrence.
- Family check-in session.
- Room count.
- Group attendance count.
- First-time attendee.
- Non-attendee.
- Last attendance.
- Checkout status.
- Label print success.

Then map to data:

- Person identity: `Person` through `PersonAlias`.
- Attendance fact: `Attendance`.
- Occurrence context: `AttendanceOccurrence`.
- Group context: `Group` and `GroupType`.
- Time context: `StartDateTime`, `OccurrenceDate`, `SundayDate`, `ScheduleId`.
- Location context: `LocationId`.
- Campus context: `CampusId`.

### Analytics Caveats

The source stored procedures demonstrate that Rock analytics can use `SundayDate`, campus filters, schedule filters, group IDs, group type IDs, and `DidAttend = 1` ([AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql)). That means a custom SQL report that filters `Attendance.StartDateTime` differently may not match Attendance Analytics.

For live reporting, inspect:

- Exact stored procedure version in the database.
- View definitions such as `vCheckin_GroupTypeAttendance` if used.
- Current Rock version migrations.
- Whether null campuses are included.
- Whether schedule filters are visible or hidden on the block.
- Whether data views are limiting the population.
- Whether a metric is count-only rather than person-based.

### Model Map Use

Use the Model Map or live schema inspection to confirm table and column names before writing SQL. The source pack provides enough to identify major tables, but not every relationship. For version-safe agent work:

- Inspect `INFORMATION_SCHEMA.COLUMNS` or Model Map for the target version.
- Confirm `AttendanceOccurrence` fields.
- Confirm whether views and procedures exist.
- Confirm entity type and attribute storage when dealing with custom fields.
- Confirm block attribute storage for page-specific settings.

Do not invent schema fields from memory.

## 16. Version And Release Caveats

Version matters heavily.

The official manual includes update sections for many Rock versions and the source pack excerpt specifically mentions Rock 14.0 Check-In updates: a new security verb for deleting attendance from Check-In Manager roster, checkout enablement for kiosk and/or Check-In Manager, and schedule filtering in Check-In Manager roster ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

The source pack includes developer docs marking Proximity Attendance as mobile v7.0 and Rock v17.1 ([Proximity Attendance](https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance)).

A Triumph release summary says v17.1 added kiosk device settings for adding or editing family information using Next-Gen Check-In ([GitHub Spotlight 4/16/2025](https://www.triumph.tech/resources/github-spotlight-4162025)). Because this is not an official Rock release-note page in the pack, verify against official release notes and the live instance before treating it as final.

RockU lists newer Check-In Manager and Next-Gen Labels lessons with release dates around June 1, 2026 in compact records, and hydrated excerpts show newer lessons present in the RockU Check-In sequence ([RockU Check-In](https://community.rockrms.com/rocku/check-in), [Next-Gen Labels](https://community.rockrms.com/rocku/check-in/next-gen-labels)). Since the current source pack is a June 2026 hydration, live sites may be ahead or behind. Always inspect the installed Rock version.

Version-sensitive areas:

- Legacy vs next-generation labels.
- Legacy vs next-generation Check-In.
- Check-In Manager roster security.
- Checkout behavior.
- Mobile check-in engine.
- Proximity attendance.
- Family edit/add settings on kiosks.
- Obsidian vs Web Forms blocks.
- Attendance analytics procedures and filters.
- Mobile Group Attendance Entry schedule requirement.

## 17. Implementation Playbooks

### Playbook: Build A Basic Family Check-In Area

1. Define the ministry area and intended check-in system type.
2. Create or verify the check-in group type.
3. Configure group type attendance/check-in behavior.
4. Create groups for rooms/classes.
5. Assign group locations.
6. Assign schedules to the correct group/location level.
7. Configure age/grade/membership rules.
8. Create or update named locations.
9. Configure printers on devices or locations depending on `Print To`.
10. Create or verify label definitions.
11. Create or configure the check-in configuration.
12. Select Individual or Family check-in type.
13. Configure search behavior and inactive-person rules.
14. Configure location selection strategy.
15. Create devices/kiosks.
16. Test with a known family and child.
17. Verify attendance rows.
18. Verify labels.
19. Verify Check-In Manager roster.
20. Document the configuration.

### Playbook: Add A New Room

1. Create or identify the group.
2. Assign the named location.
3. Assign the schedule.
4. Set capacity if used.
5. Confirm group active status.
6. Confirm age/grade rules.
7. Confirm group type inheritance.
8. Confirm printer if using location printer.
9. Test during an active schedule window or temporarily with a controlled test schedule.
10. Verify the room appears for an eligible test person.
11. Verify attendance occurrence uses the new location.
12. Verify labels show the room correctly.

### Playbook: Configure Mobile Check-In

1. Confirm Rock and mobile shell versions.
2. Confirm mobile check-in feature support.
3. Create or verify virtual kiosk devices.
4. Configure campus boundaries/geofence if used.
5. Add the mobile Check-In block.
6. Set `Configuration Template`.
7. Set `Areas`.
8. Set `Kiosk`.
9. Configure mobile launcher to target the correct devices, configuration, theme, and areas ([Mobile Check-in Configuration insight](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)).
10. Test authenticated family selection.
11. Test opportunity selection.
12. Test QR handoff to kiosk/iPad if labels are required.
13. Verify attendance rows match kiosk behavior.
14. Verify labels print from the correct printer.

### Playbook: Configure Rapid Attendance Entry

1. Choose the group or parent group.
2. Confirm group type takes attendance.
3. Add Rapid Attendance Entry block.
4. Configure `Enable Attendance`.
5. Set `Parent Group` or `Attendance Group`.
6. Decide whether to show `Can check-in` relationships.
7. Set attendance age limit if needed.
8. Configure campus display and campus types.
9. Link add-family and attendance-list pages if used.
10. Enable related updates, notes, prayer requests, or workflows only if operationally needed.
11. Test with real group data.
12. Verify attendance rows and occurrence context.

### Playbook: Implement A QR Code Attendance Pattern

Community recipe 483 describes a custom QR-code check-in workflow where guests use a logged-in page to check in family members to a group ([QR Code Check-in System](https://community.rockrms.com/recipes/483)). Treat this as a custom workflow pattern.

Before implementing:

- Verify the use case does not require child-security labels.
- Verify login requirements.
- Verify workflow security.
- Verify group attendance write behavior.
- Verify duplicate prevention.
- Verify family member selection.
- Verify audit trail.
- Verify mobile usability.
- Verify reporting output.

### Playbook: Implement SMS/Text Attendance

Community recipe 116 describes a text keyword pattern using workflow import/export in Rock v9+ and a text-to-workflow defined type ([Text to Check In](https://community.rockrms.com/recipes/116)). Treat it as a custom integration.

Before implementing:

- Verify SMS transport.
- Verify workflow import safety.
- Verify phone matching.
- Verify ambiguous person handling.
- Verify attendance target group.
- Verify opt-in/consent policy.
- Verify failure responses.
- Verify duplicate prevention.
- Verify reporting.

## 18. Troubleshooting Decision Tree

Start here.

### A. Is The Problem Before Attendance Is Saved?

If yes, determine which stage fails:

- Kiosk unavailable.
- Search fails.
- Family/person selection fails.
- Opportunity selection fails.
- Save fails.

If kiosk unavailable:

- Check device.
- Check configuration.
- Check schedule windows.
- Check no-active-location countdown.
- Check page/block error logs.

If search fails:

- Check phone/search settings.
- Check person/family data.
- Check inactive status.
- Check duplicate families.
- Check permissions.

If opportunities fail:

- Check group type.
- Check group.
- Check location.
- Check schedule.
- Check campus.
- Check age/grade.
- Check membership mode.
- Check capacity.
- Check data views/custom filters.

If save fails:

- Check exception logs.
- Check required occurrence fields.
- Check permissions.
- Check duplicate/validation rules.
- Check custom workflow hooks.

### B. Was Attendance Saved?

If no:

- Reproduce with test person.
- Inspect exception logs.
- Inspect Check-In Manager.
- Inspect database rows.
- Inspect block/device logs if available.

If yes:

- Proceed to labels, roster, or analytics.

### C. Is The Problem Labels?

If labels absent:

- Attendance exists?
- Label enabled?
- Print route correct?
- Printer assigned?
- Printer online?
- Label template valid?
- Mobile QR handoff complete?

If labels wrong:

- Inspect attendance occurrence.
- Inspect label data fields.
- Inspect custom Lava.
- Inspect formatter.
- Inspect duplicate attendance.

### D. Is The Problem Check-In Manager?

- Verify version.
- Verify page/block.
- Verify security.
- Verify roster filters.
- Verify schedule filter.
- Verify checkout enablement.
- Verify delete attendance verb.
- Verify attendance rows.

### E. Is The Problem Analytics?

- Verify block settings.
- Verify group types/groups.
- Verify campus and null-campus filters.
- Verify schedule filters.
- Verify date basis.
- Verify `DidAttend`.
- Verify stored procedure version.
- Verify custom report logic.

### F. Is The Problem Mobile?

- Verify mobile app/shell version.
- Verify block settings.
- Verify virtual kiosk.
- Verify geofence/campus.
- Verify authentication.
- Verify shared engine assumptions.
- Verify QR handoff.
- Compare mobile attendance rows to kiosk attendance rows.

## 19. Agent Task Recipes

### Recipe: Prove Why A Child Cannot Check In

Inspect:

1. Person record: active status, age, grade.
2. Family group: membership and role.
3. Search path: phone/search key.
4. Check-in configuration: family vs individual, inactive-person behavior.
5. Group type: check-in/attendance settings and inheritance.
6. Candidate groups: active, membership mode, age/grade rules.
7. Group locations: active location and schedule.
8. Current schedule window.
9. Campus/device context.
10. Capacity.
11. Exception logs if the UI errors.

Report:

- The first failing predicate.
- The exact record IDs inspected.
- Whether this is configuration, data hygiene, schedule timing, or version behavior.
- The safest change.

### Recipe: Prove Which Printer Should Print A Label

Inspect:

1. Check-in configuration `Print To`.
2. Device printer if device route.
3. Location printer if location route.
4. Selected attendance occurrence location.
5. Label definition.
6. Printer service status.
7. Recent print attempts.
8. Test label output.

Report:

- Expected printer.
- Actual route.
- Missing assignment or failed delivery point.
- Whether attendance was saved.

### Recipe: Reconcile Attendance Analytics To Raw Rows

Inspect:

1. Attendance Analytics block settings.
2. Group type/group filters.
3. Date range.
4. Schedule filter.
5. Campus filter.
6. Data view filters.
7. Stored procedure used.
8. Raw `Attendance` joined to `AttendanceOccurrence`.
9. `DidAttend = 1`.
10. SundayDate vs StartDateTime.

Report:

- Query basis.
- Count from raw rows.
- Count from block/report.
- Difference by filter.
- Whether analytics or expectation is wrong.

### Recipe: Decide Between Check-In, Group Attendance, Rapid Attendance, QR, And SMS

Use Check-In when:

- Labels, pickup security, room assignment, or family kiosk flow matter.

Use Group Attendance when:

- A leader needs to mark a known roster present.

Use Rapid Attendance when:

- Staff need fast manual attendance plus possible family updates, notes, prayer requests, or workflows ([Rapid Attendance Entry insight](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)).

Use QR workflow when:

- The event needs lightweight self-attendance and does not require full check-in hardware or labels ([QR Code Check-in System](https://community.rockrms.com/recipes/483)).

Use SMS workflow when:

- Group members can self-report by keyword and the organization accepts the matching/consent tradeoffs ([Text to Check In](https://community.rockrms.com/recipes/116)).

### Recipe: Validate Mobile Check-In Readiness

Inspect:

1. Rock version.
2. Mobile shell version.
3. Mobile Check-In block.
4. `Configuration Template`.
5. `Areas`.
6. `Kiosk`.
7. Virtual kiosk device.
8. Campus/geofence.
9. Authentication and family resolution.
10. QR handoff printer.
11. Attendance rows after test.
12. Labels after test.

Report:

- Mobile path status.
- Kiosk comparison.
- Any setting mismatch.
- Version caveats.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `109`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | configuration | The Mobile Check-in Launcher page should enable the virtual kiosk devices and list the check-in configuration and areas that are valid for the campuses served by that page. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | configuration | Rapid Attendance Entry is configurable enough to support multiple page variants, so teams can create focused versions for different ministry workflows instead of using one catch-all setup everywhere. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | Mobile check-in should be designed around an initial identity step, such as login or phone lookup, followed by a returning-user experience that can begin closer to the check-in selection screen when the device is recognized. | [source](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) |
| rocku-confirmed | operational_guidance | The block can combine attendance marking with family editing, adding family members, person notes, prayer requests, and workflow launch actions from the same operational screen. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | Next-Gen Labels should be reviewed as part of the full check-in print path: label definition, merge data, printer routing, room configuration, and live attendance context all matter. | [source](https://community.rockrms.com/rocku/check-in/next-gen-labels) |
| rocku-confirmed | operational_guidance | Mobile check-in block text can be customized and Lava-enabled, but copy should account for where the visitor is in the flow because Rock may not know the person's identity on early screens. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | operational_guidance | When labels fail or show unexpected data, agents should inspect label template configuration and the active check-in context before assuming a printer-only problem. | [source](https://community.rockrms.com/rocku/check-in/next-gen-labels) |
| rocku-confirmed | operational_guidance | Treat each mobile check-in device record like a virtual kiosk: use the check-in kiosk device type, configure the campus geofence, associate the relevant campus locations, and create separate devices when campuses need distinct boundaries. | [source](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration) |
| rocku-confirmed | operational_guidance | Rapid Attendance Entry starts from a selected group and attendance date, with location and schedule values available when the group and attendance context support them. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | When a check-in problem appears only during service, agents should verify current schedule windows, location/group availability, label printer state, and manager-side edits before changing permanent configuration. | [source](https://community.rockrms.com/rocku/check-in/check-in-manager-1) |
| rocku-confirmed | operational_guidance | Check-In Manager should be treated as an operational control surface for live check-in sessions; troubleshoot rooms, schedules, attendance, labels, and manager actions from the exact active configuration. | [source](https://community.rockrms.com/rocku/check-in/check-in-manager-1) |
| rocku-confirmed | operational_guidance | The participant-facing flow can show fallback screens when a person is outside the configured geofence, outside the valid check-in time window, or has no eligible check-in option available. | [source](https://community.rockrms.com/rocku/check-in/using-mobile-check-in) |
| More |  | 97 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `31`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Aero Check-in Theme Transcript Insight](https://community.rockrms.com/rocku/check-in/aero-check-in-theme) | approved_for_public_distillation | 2 | media-insight:6177a74e098f3302 |
| [Attendance Analytics Transcript Insight](https://community.rockrms.com/rocku/check-in/attendance-analytics) | approved_for_public_distillation | 3 | media-insight:e066ef3153b2cc3d |
| [Attendance Self-Entry Transcript Insight](https://community.rockrms.com/rocku/check-in/attendance-self-entry) | approved_for_public_distillation | 3 | media-insight:1fb05cc8930bc9e2 |
| [BI Attendance Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-attendance-report) | approved_for_public_distillation | 1 | media-insight:b32a4e808360fabc |
| [Check-In Manager Transcript Insight](https://community.rockrms.com/rocku/check-in/check-in-manager-1) | approved_for_public_distillation | 2 | media-insight:b9cfbae2df04e08f |
| [Check-in Celebrations Transcript Insight](https://community.rockrms.com/rocku/check-in/check-in-celebrations) | approved_for_public_distillation | 2 | media-insight:726c382b13da37a9 |
| [Check-in Manager Transcript Insight](https://community.rockrms.com/rocku/check-in/check-in-manager) | approved_for_public_distillation | 2 | media-insight:b9ebb5bbd2009098 |
| [Check-in Settings Transcript Insight](https://community.rockrms.com/rocku/check-in/settings) | approved_for_public_distillation | 3 | media-insight:43111d964e899603 |
| More |  | 23 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

Primary official/documentation sources:

- [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266): official manual anchor for Check-In concepts, family/individual flow, settings, print routing, membership behavior, and version updates.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) and [Rock Mobile Release Notes](https://www.rockrms.com/mobilereleasenotes): required version-caveat checks for Check-In fixes, mobile label printing, inactive groups, schedule exclusions, capacity behavior, proximity attendance, and mobile shell requirements.
- [RockU Check-In](https://community.rockrms.com/rocku/check-in): training map for Check-In configuration and operations.
- [RockU Locations](https://community.rockrms.com/rocku/check-in/locations), [Schedules](https://community.rockrms.com/rocku/check-in/schedules), [Types and Groups](https://community.rockrms.com/rocku/check-in/types-and-groups), [Settings](https://community.rockrms.com/rocku/check-in/settings), [Devices](https://community.rockrms.com/rocku/check-in/devices), [Running Check-in](https://community.rockrms.com/rocku/check-in/running-check-in): training topics for the core configuration chain.
- [Check-in Manager](https://community.rockrms.com/rocku/check-in/check-in-manager) and [newer Check-In Manager](https://community.rockrms.com/rocku/check-in/check-in-manager-1): operational manager topics.
- [Attendance Analytics](https://community.rockrms.com/rocku/check-in/attendance-analytics), [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry), [Attendance Self-Entry](https://community.rockrms.com/rocku/check-in/attendance-self-entry): attendance-related training topics.
- [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview), [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration), [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in): mobile training topics.
- [Labels Legacy](https://community.rockrms.com/rocku/check-in/labels-legacy) and [Next-Gen Labels](https://community.rockrms.com/rocku/check-in/next-gen-labels): label training topics.

Developer and source-code sources:

- [Mobile Check-In repo docs](https://github.com/SparkDevNetwork/Rock/blob/develop/docs/check-in/mobile-check-in.md): v2 mobile architecture and shared engine model.
- [Mobile CheckIn.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Mobile/CheckIn/CheckIn.cs): mobile block settings and implementation path.
- [RapidAttendanceEntry.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx.cs): Rapid Attendance settings and implementation path.
- [RapidAttendanceEntry.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/RapidAttendanceEntry.ascx): Rapid Attendance UI controls.
- [AttendanceAnalytics.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx.cs): Attendance Analytics block settings.
- [AttendanceAnalytics.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/AttendanceAnalytics.ascx): Attendance Analytics UI controls.
- [AttendanceLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/AttendanceLabelData.cs), [LabelAttendanceDetail.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelAttendanceDetail.cs), [ILabelDataHasAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/ILabelDataHasAttendance.cs), [SecurityCodeAndNameDataFormatter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/Formatters/SecurityCodeAndNameDataFormatter.cs): next-generation label data and formatting landmarks.
- [AttendeeDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeDates.sql), [AttendeeFirstDates procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Procedures/spCheckin_AttendanceAnalyticsQuery_AttendeeFirstDates.sql), [Attendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_Attendees.sql), [NonAttendees procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2013.0/Version%201.13.4/202204271322510_UpdateAttendanceAnalyticsQuerySP_spCheckin_AttendanceAnalyticsQuery_NonAttendees.sql), [AttendeeLastAttendance procedure](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Plugin/HotFixes/104_MigrationRollupsFor10_3_0_spCheckin_AttendanceAnalyticsQuery_AttendeeLastAttendance.sql): analytics SQL landmarks.
- [Proximity Attendance](https://community.rockrms.com/developer/mobile-docs/essentials/advanced-topics/proximity-attendance): mobile beacon attendance concept and version markers.
- [Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry): mobile group attendance block behavior and settings.

Community examples and lower-authority patterns:

- [QR Code Check-in System](https://community.rockrms.com/recipes/483): custom QR workflow pattern.
- [Text to Check In](https://community.rockrms.com/recipes/116): SMS/workflow attendance pattern.
- [Watch Party Attendance](https://community.rockrms.com/recipes/197): count/report workflow pattern.
- [Check-in Parent and Child Labels](https://community.rockrms.com/recipes/125): custom parent/child label pattern.
- [Install CUSTOM Icon Font on Printer Label](https://community.rockrms.com/recipes/424): custom font label pattern.
- [Group Check-In Summary Template](https://community.rockrms.com/recipes/370): Lava summary pattern for group check-in readiness.
- [Obsidian Group Attendance Detail toast recipe](https://community.rockrms.com/recipes/461): UX enhancement pattern for attendance confirmation.
- [How rapid can Rapid Attendance be?](https://community.rockrms.com/ask/using/2804): community Q&A comparing group attendance to rapid-style needs.

Dependency notes:

- Check-In depends on attendance, groups, locations, schedules, labels, mobile, and security.
- Most troubleshooting should start with the check-in configuration and end by verifying attendance rows.
- Mobile Check-In adds block settings, virtual kiosk devices, geofence/campus boundaries, authentication, and QR print handoff.
- Labels depend on attendance context, label engine version, print routing, printer compatibility, and custom fields.
- Analytics depends on stored procedures, date basis, group/group-type filters, campus filters, schedule filters, `DidAttend`, and data view settings.
- Version-specific behavior must be verified in the live instance before making production changes.
