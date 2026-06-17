---
id: authored-serving-volunteer-ops
title: Serving And Volunteer Operations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Serving And Volunteer Operations

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Serving And Volunteer Operations index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Serving and volunteer operations in Rock RMS are built on the Groups system, then extended through scheduling, locations, attendance, communications, workflow, requirements, security, and reporting. An agent working on this area should not treat "serving" as one isolated feature. A volunteer serving experience is usually a coordinated chain:

1. A person expresses interest or is added to a serving team.
2. That serving team is represented as a `Group`, usually under a ministry-specific `GroupType`.
3. The person's team membership is represented by `GroupMember` and a `GroupRole`.
4. The team's where-and-when service options are represented through `GroupLocation`, `GroupLocationSchedule`, and `Schedule`.
5. Future service assignments, confirmations, declines, and attendance are represented through attendance-related records tied to an `AttendanceOccurrence`.
6. Requirements such as background checks, training, applications, or policy acknowledgements are represented through group requirements, workflows, person attributes, document records, or ministry-specific data.
7. Communication is delivered through group scheduling communications, system communications, reminders, workflow messages, or custom Lava.
8. Follow-up is handled through group attendance, no-show reporting, connection requests, workflows, communications, and ministry dashboards.

The highest-value agent behavior is to trace the complete operational path instead of editing only the visible page or email. For example, if a volunteer says "I cannot accept my serving request," inspect the scheduled attendance record, the person alias, the group, the group location schedule, the confirmation workflow or endpoint, the system communication, and any relevant release caveats. Rock v17.2 fixed a bug where the Group Scheduling Confirmation workflow could process automated link-checker opens or mishandle required decline reasons, so instances below or around that version need special scrutiny when confirmations behave unexpectedly ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Serving operations depend heavily on the exact instance configuration. When source material is thin, do not infer. Inspect the live Rock instance: the group type, inherited group type configuration, block settings, system communication, workflow actions, group requirements, schedule assignments, location assignments, and attendance rows. Community recipes are useful examples, but Rock explicitly warns that recipes are community-contributed and not reviewed or endorsed by the core team, so agents should use them as patterns to evaluate, not as canonical implementation rules ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459), [Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238)).

The operational model is:

- `GroupType` defines what kind of serving team exists and what behavior is available.
- `Group` is the actual serving team.
- `GroupRole` defines a person's role on the team.
- `GroupMember` links the person to the serving team and role.
- `Location` and `Schedule` define where and when the team can serve.
- `AttendanceOccurrence` is the service instance.
- `Attendance` records carry attendance, scheduled assignment, RSVP/confirmation, and related tracking depending on version and configuration.
- `SystemCommunication`, workflow, and block actions drive confirmations, reminders, and response handling.
- `GroupRequirement`, person attributes, workflows, and external integrations drive eligibility.
- Security on pages, blocks, groups, group types, and check-in verbs determines who can view, manage, schedule, confirm, or delete records.

For agents, the key guardrail is this: serving operations are ministry-facing and people-facing at the same time. A technically valid configuration can still be operationally broken if it hides schedules from volunteers, sends replies to a generic inbox, allows unqualified people to be scheduled, suppresses attendance reminders incorrectly, or exposes private volunteer data on an external page.

## 2. Scope And Terminology

This guide covers Rock RMS serving and volunteer operations: serving teams, volunteer schedules, schedule preferences, confirmations, RSVP-style responses, decline flows, attendance, volunteer requirements, communications, follow-up, reporting, and agent troubleshooting.

It does not replace the broader Rock guides for Groups, Check-In, Communications, Workflows, People, Security, or Reporting. It explains how those areas intersect when a church uses Rock to recruit, qualify, schedule, communicate with, and track volunteers.

### Core Terms

**Serving team**  
A ministry team represented as a Rock group. Examples: Elementary 9:00 Room 1, Worship Vocalists, Parking Team, Cafe Team, Communion Prep, Youth Small Group Leaders. In Rock data terms this is normally a `Group`.

**Serve team / volunteer team**  
Common church-facing language for a serving team. Treat it as the same operational object unless the instance has separate group types for sign-up opportunities, interest forms, or volunteer pools.

**Serving opportunity**  
A place where a person can serve. Depending on implementation, this may be a group, a sign-up group, a connection opportunity, a workflow option, or a content item that eventually routes into a group or connection request. A community example for serving interest uses a public ministry listing, a workflow form, observation scheduling, connector notification, and follow-up application steps ([Serving Interest Process](https://community.rockrms.com/recipes/169)).

**Group type**  
The configuration container for a family of groups. It controls roles, attributes, hierarchy, requirements, attendance behavior, scheduling behavior, security patterns, and block behavior. RockU separates training for Group Types, Group Type Inheritance, Group Requirements, Group Security, and Group Scheduling, which is a useful signal that agents should inspect group type configuration before assuming a problem is inside one group ([Group Types](https://community.rockrms.com/rocku/groups/group-types), [Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements), [Group Security](https://community.rockrms.com/rocku/groups/group-security)).

**Group role**  
A role a member holds in the serving team. Examples: Leader, Coach, Coordinator, Member, Volunteer, Substitute, Trainee. Roles determine leadership, communication targeting, attendance permissions in some blocks, and filtering.

**Schedule**  
The reusable date/time pattern assigned to group locations. A schedule might be Sunday 9:00 AM, Sunday 11:00 AM, Wednesday 6:30 PM, 1st and 3rd Sunday, or 5th Sunday. The community recipe on fifth-week templates highlights that template schedules must match the day they apply to; a "1st and 3rd Week" Sunday schedule is not a valid template for a Tuesday ministry just because the words look generic ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)).

**Group location**  
The location assigned to a group. For serving, this may be a room, ministry area, campus zone, parking lot, auditorium, production booth, classroom, or a broad campus location. Check-in documentation recommends broad locations in some cases so kiosks can see groups without excessive configuration ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

**Group location schedule**  
The join between a group location and a schedule. Source snippets show this relationship explicitly through `GroupLocationSchedule` joined from `GroupLocation` to `Schedule` ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).

**Scheduled attendance / scheduled assignment**  
A future attendance-related record indicating that a person has been scheduled or requested to serve. The exact fields and enum names should be verified in the live instance and Rock version. Source-code view models show that the scheduler sends confirmations and reports counts of eligible recipients, sent communications, warnings, and errors ([GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

**Confirmation**  
The volunteer's response to a scheduled serving request. Source-code enums for the schedule toolbox show row statuses of `Pending`, `Confirmed`, `Declined`, and `Unavailable` ([ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs), [toolboxScheduleRowConfirmationStatus.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Blocks/Group/Scheduling/toolboxScheduleRowConfirmationStatus.ts)).

**Schedule Toolbox**  
A volunteer-facing block for managing scheduled attendances. The mobile developer documentation says it lets an individual accept, decline, cancel a prior response, and optionally provide a decline reason. It is available for mobile v4.0 / core v13.1 and is customizable through templates ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)).

**Attendance**  
The actual record of whether someone attended or served. Attendance in Rock is also used by scheduling and RSVP features in ways that matter operationally. Rock v18.3 fixed the Send Attendance Reminder job so scheduling/RSVP tracking records alone do not suppress reminders as if real attendance had been taken ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Requirement**  
An eligibility rule that must be met before someone should serve, lead, check in, or be scheduled. Examples: background check, child safety training, application, reference check, membership, baptism, age, grade, ministry approval, abuse-prevention acknowledgement. RockU has a specific Group Requirements training topic ([Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements)).

**Follow-up**  
The operational response after attendance, decline, no-show, interest submission, requirement failure, or inactivity. This can be manual, report-driven, workflow-driven, communication-driven, or connection-request-driven.

## 3. Serving And Volunteer Operations Mental Model

Think of serving operations as five layers.

### Layer 1: Team Structure

Rock's group system provides the durable structure. Every serving team needs a clear group type, group hierarchy, roles, active/archive rules, campus strategy, and security model. If the team structure is wrong, scheduling and reporting will become fragile.

Good team structure answers:

- What ministry owns this team?
- Is this a real team, a sign-up opportunity, a serving pool, or a one-time event slot?
- Which group type owns it?
- Does the group type inherit attributes or behavior from another group type?
- What roles exist?
- Which roles are leaders, schedulers, coordinators, volunteers, substitutes, trainees, or inactive members?
- Does the group have a campus?
- Does the group have a parent group?
- Should the group be visible externally?
- Is the group active and not archived?
- Does this group need check-in behavior?
- Does this group need scheduling behavior?
- Are requirements enforced at group type, group, or ministry process level?

RockU's training path is useful here: Group Viewer, Group Details, Group Types, Group Type Inheritance, Group Location, Group Purposes, Requirements, Security, and Scheduling are separate training topics because each contributes to the final behavior ([Group Viewer](https://community.rockrms.com/rocku/groups/group-viewer), [Group Details](https://community.rockrms.com/rocku/groups/group-details), [Group Types](https://community.rockrms.com/rocku/groups/group-types)).

### Layer 2: Where And When

Serving is not only membership. A person serves at a time and usually a place. Rock represents that through schedules and locations assigned to groups. Source-code and SQL snippets show the common join path:

`Group` -> `GroupLocation` -> `GroupLocationSchedule` -> `Schedule`

A source snippet also includes `Location` and schedule fields such as name, start time, end time, frequency, and frequency qualifier in a query that lists group type, group, location, and schedule relationships ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).

Agent rule: when a schedule is missing from a volunteer page, scheduler, check-in, or sign-up finder, inspect both the group and the group-location-schedule assignment. Do not stop at the `Schedule` table. A schedule may exist but not be assigned to the serving group's active location.

### Layer 3: Assignment And Response

Scheduling creates a future assignment. The volunteer then confirms, declines, remains pending, or becomes unavailable. Source-code enums explicitly identify `Pending`, `Confirmed`, `Declined`, and `Unavailable` as statuses used by the group schedule toolbox ([ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs)).

The mobile Schedule Toolbox documentation frames the volunteer-facing actions as accepting, declining, cancelling a previous response, and providing a decline reason where configured ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)). Release notes add an important operational caveat: the confirmation workflow has had bugs around automated link checkers and required decline reasons, fixed in v17.2 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent rule: if responses look wrong, verify the Rock version, the system communication links, the confirmation workflow, whether a decline reason is required, and whether an email-security tool may be opening links.

### Layer 4: Actual Attendance

Attendance is the record of reality: who served, who checked in, who was present, and who did not attend. Rock's data model separates occurrence-level context from person-level attendance. A source SQL view uses `AttendanceOccurrence` joined to `Attendance`, `PersonAlias`, and `Group`, including occurrence group, schedule, location, occurrence date, Sunday date, and attended person ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

That separation matters. A scheduled serving request is not always the same thing as actual attendance. Rock v18.3's reminder fix demonstrates the operational risk: scheduling/RSVP-related attendance records can exist before actual attendance is taken, and jobs must distinguish tracking records from real attendance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent rule: when reporting attendance, no-shows, or reminder suppression, distinguish scheduled/requested/RSVP tracking from `DidAttend` records and from "group did not meet" markers. Inspect the exact columns in the live version before writing SQL.

### Layer 5: Operational Feedback Loop

Volunteer operations are not complete when a schedule is sent. Real operations include:

- recruiting new volunteers,
- qualifying them,
- assigning them,
- reminding them,
- collecting confirmation responses,
- recording attendance,
- following up on absences,
- monitoring roster health,
- replacing declined volunteers,
- auditing requirement compliance,
- measuring serve frequency,
- detecting over-scheduled volunteers,
- keeping team data clean,
- ensuring security boundaries remain appropriate.

RockU includes scheduling analytics, roster and communications, RSVP, attendance, and group history as separate topics in the Groups track ([Group Scheduling - Analytics](https://community.rockrms.com/rocku/groups/group-scheduling-analytics), [Group Scheduling Roster and Communications](https://community.rockrms.com/rocku/groups/group-scheduling-roster-and-communications), [Group History](https://community.rockrms.com/rocku/groups/group-history)). Agents should treat reporting and follow-up as part of the system, not an afterthought.

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. Live Rock instance configuration and data.
2. Official Rock documentation.
3. RockU training pages.
4. Rock release notes.
5. Rock source code and model-map records.
6. Developer docs.
7. Community recipes and Q&A.

Official docs and release notes are generally stronger than recipes. Source code is strong for entity relationships and implementation landmarks, but it still must be mapped to the deployed Rock version. Community recipes are valuable because they show real ministry patterns, but they are not canonical and may be insecure, inefficient, or version-specific.

### How Agents Should Use This Guide

Use this guide to plan inspections and changes. Do not assume every field, block, or route exists in every Rock version. Before editing or writing SQL, inspect:

- Rock version.
- Group type configuration.
- Group type inheritance.
- Group role definitions.
- Group active/archive state.
- Campus assignment.
- Group location schedule assignments.
- Schedule recurrence and date constraints.
- Attendance occurrence records.
- Attendance response/status fields.
- System communications.
- Workflow actions.
- Block settings.
- Security.
- Jobs and job history.
- Release-note caveats around the affected feature.

### When To Prefer Live Verification

Live verification is required when the question depends on:

- a specific group, group type, schedule, location, or campus;
- whether a person is eligible to serve;
- why a volunteer cannot accept, decline, or view a request;
- whether a schedule was sent;
- whether attendance was recorded;
- which communication was sent;
- who received a message;
- whether a workflow acted on a record;
- whether a check-in kiosk should show a group;
- whether a job suppressed reminders;
- whether a release-note fix is present.

The source pack gives strong landmarks, but not enough to infer instance-specific behavior. Say what to inspect rather than inventing certainty.

## 5. Core Configuration And Data Model

### Group Types

The serving system starts with the group type. In Rock, a group type defines how a category of groups behaves. For serving, group types commonly represent ministries or operational patterns:

- Weekend Serving Teams.
- Kids Ministry Serving Teams.
- Youth Serving Teams.
- Worship Teams.
- Guest Services Teams.
- Production Teams.
- One-time Event Volunteer Opportunities.
- Seasonal Sign-Up Teams.
- Check-In Serving Groups.
- Volunteer Interest or Placement Groups.

A group type should be inspected for:

- name and purpose;
- inherited group type;
- allowed child group types;
- roles;
- attributes;
- requirements;
- scheduling settings;
- attendance settings;
- location behavior;
- group member attributes;
- security;
- lava templates or block behavior that depend on group type;
- active/inactive and archive policies.

RockU's group-type training is the best authority in the pack for the breadth of group type behavior ([Group Types](https://community.rockrms.com/rocku/groups/group-types)). Check-in documentation also emphasizes group type inheritance for check-in scenarios, where attributes such as age range or grade range are inherited by child group types rather than duplicated manually ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

### Group Type Inheritance

Inheritance matters when serving intersects with check-in or specialized ministry group types. Check-in documentation describes inheritance as a way for one group type to use attributes from another, such as check-in by grade inheriting from check-in by age, and ability-level check-in inheriting from age-based check-in ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

For serving operations, inheritance can explain why:

- a visible group does not expose the expected attributes;
- age or grade restrictions are enforced even if they are not obvious on the current group type;
- check-in availability differs between rooms;
- the group scheduler sees unexpected group paths;
- an inherited group type creates a hierarchy the agent did not account for.

Agent inspection path:

1. Open the group type.
2. Record its inherited group type.
3. Record parent/child group type associations.
4. Inspect inherited attributes.
5. Inspect requirements at each layer.
6. Inspect whether scheduling/check-in behavior is enabled at the expected layer.
7. Confirm whether the block or query uses the group type itself, its descendants, or a hard-coded group type id.

Source code for `CheckinAreaPath` shows Rock must account for parent group type paths and even guard against circular references or multiple parents when building check-in area paths ([CheckinAreaPath.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Group/GroupType/CheckinAreaPath.cs)). That is a warning against assuming a simple one-parent hierarchy without inspecting the live configuration.

### Groups

The group is the serving team itself. Inspect:

- `Id`;
- `Guid`;
- `Name`;
- `GroupTypeId`;
- `ParentGroupId`;
- `CampusId`;
- active status;
- archive status;
- leader/coordinator fields;
- schedule coordinator, if used;
- group attributes;
- group member count;
- group locations;
- group schedules;
- group requirements;
- group security.

A community dynamic-sender recipe uses `Attendance.Occurrence.Group.ScheduleCoordinatorPersonAliasId`, which is a practical source signal that groups may carry a schedule coordinator person alias used in scheduling communications ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)). Do not assume it is populated. Inspect the group record and fallback behavior.

### Group Roles

Roles define function inside the team. For serving operations, common roles include:

- Team Leader.
- Coach.
- Coordinator.
- Scheduler.
- Volunteer.
- Substitute.
- Trainee.
- Observer.
- Inactive.
- Applicant.

Operationally, roles can drive:

- who receives leader emails;
- who can take attendance;
- who appears as a volunteer;
- who is eligible for scheduling;
- who is excluded from scheduling;
- who receives requirement notices;
- which people are included in reports;
- who is considered a leader for security or communication purposes.

Agent guardrail: do not assume every `GroupMember` is an active schedulable volunteer. Inspect role, status, group member attributes, requirements, and scheduling preferences.

### Group Members

A `GroupMember` links a person to a group and role. For volunteer operations, inspect:

- person;
- person alias;
- group;
- role;
- member status;
- communication preference;
- group member attributes;
- requirement status;
- schedule preferences;
- whether the member is active, inactive, pending, or otherwise excluded by local convention.

Community examples around filtering volunteers by schedule preference stress that volunteers must be part of a scheduling group and have preferences set before they appear in that pattern ([Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238)). That is an example, not a universal rule, but it is a useful troubleshooting branch: if a volunteer is missing from a schedule-preference report, verify membership and preference records before blaming the block.

### Locations

Locations define where serving happens. They may be physical rooms, broad campus areas, or named operational locations. Check-in documentation notes that broader locations can make check-in kiosk visibility easier in some configurations ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Inspect:

- `Location.Id`;
- `Location.Name`;
- parent location path;
- campus association, if relevant;
- whether the location is active;
- whether the location has printers for check-in scenarios;
- whether the group is assigned to this location through `GroupLocation`;
- whether schedules are assigned through `GroupLocationSchedule`.

Source-code view models for check-in schedule building expose `groupLocationId`, `groupPath`, `locationName`, `locationPath`, and active `scheduleIds`, which confirms that group-location-schedule configuration is a first-class operational surface in check-in schedule tools ([GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs)).

### Schedules

Schedules define time. They can represent single service times, recurring patterns, fifth-week exceptions, seasonal patterns, and ministry-specific rhythms.

Inspect:

- schedule name;
- iCalendar or recurrence pattern where used;
- start time;
- end time;
- frequency;
- frequency qualifier;
- effective start/end dates;
- whether it is active;
- whether it applies to the expected day of week;
- whether it is assigned to the group location;
- whether it is used as a template preference or actual serving time.

Community guidance on schedule templates emphasizes naming clarity and day-of-week correctness, especially when adding fifth-week schedules for auto-scheduling ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)). If a schedule is used for auto-scheduling, verify that the template corresponds to the same day and pattern as the ministry event.

### AttendanceOccurrence

`AttendanceOccurrence` represents the occurrence context: group, schedule, location, occurrence date, Sunday date, and related metadata. The source SQL view joins `AttendanceOccurrence` as `O` to `Attendance`, then uses `O.GroupId`, `O.ScheduleId`, `O.LocationId`, `O.OccurrenceDate`, and `O.SundayDate` ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

For agents, this means attendance questions usually require both occurrence and person-level attendance inspection:

- Which group was this occurrence for?
- Which schedule?
- Which location?
- Which date?
- Was this actual attendance, a scheduled assignment, an RSVP artifact, or a reminder-related record?
- Is there more than one occurrence that looks similar?
- Did the group meet?
- Was attendance recorded for the person?

### Attendance

`Attendance` is person-level and occurrence-linked. In serving contexts it may carry attendance, scheduled assignment, RSVP/confirmation, decline, and related flags depending on version and feature path.

Inspect live columns rather than guessing. Commonly relevant concepts include:

- person alias;
- occurrence;
- start/end datetime;
- attended status;
- scheduled/requested status;
- RSVP or confirmation status;
- decline reason;
- scheduled by person alias;
- created/modified audit fields.

The source SQL view filters real attendance with `A.DidAttend = 1`, which is a reminder that not every attendance row should be counted as attended service ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)). Release notes further distinguish scheduling/RSVP tracking records from actual attendance for reminder suppression ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Communications

Serving communications include:

- scheduling confirmation email;
- scheduling response email;
- reminders;
- roster messages;
- decline notifications;
- coordinator emails;
- workflow emails;
- SMS reminders;
- family-serving pages;
- app push or mobile block actions, if implemented.

The mobile Schedule Toolbox documentation includes sections for scheduler receipt of confirmation emails and scheduling response email behavior ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)). A community dynamic-sender recipe shows how one organization used Lava in the scheduling confirmation system communication to choose a sender from the group schedule coordinator, scheduled-by person, or organization default ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)). Treat that as a pattern to evaluate and test, not as a core guarantee.

### Workflows

Workflows often fill gaps between Rock's core scheduling features and local ministry process. Common workflow uses:

- serving interest intake;
- observation scheduling;
- background check request;
- application routing;
- manual approval;
- requirement reminders;
- decline follow-up;
- no-show follow-up;
- family serving request management;
- coordinator alerts.

A community serving-interest recipe describes a flow from public interest form to observation, connector notification, reminders, application/background check, and connection-request activity notes ([Serving Interest Process](https://community.rockrms.com/recipes/169)). A family-serving recipe describes custom workflows to accept or decline serving requests for family members from a My Account page ([Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489)). Both are community examples; inspect security, authorization, person scoping, and workflow entity updates before using similar patterns.

## 6. Primary Entities And Relationships

### Relationship Map

The practical relationship map for serving operations is:

`Person`  
-> `PersonAlias`  
-> `GroupMember`  
-> `GroupRole`  
-> `Group`  
-> `GroupType`  
-> `GroupLocation`  
-> `Location`  
-> `GroupLocationSchedule`  
-> `Schedule`  
-> `AttendanceOccurrence`  
-> `Attendance`  
-> `Communication`, `Workflow`, `Requirement`, and reporting outputs.

For check-in-related serving:

`GroupTypeAssociation` and group type inheritance influence check-in area paths, available group types, and inherited eligibility attributes ([CheckinAreaPath.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Group/GroupType/CheckinAreaPath.cs), [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

For scheduling UI and block responses:

Group Scheduler view models expose selected locations, location names, schedule names, and send-confirmation outcomes ([GroupSchedulerLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs), [GroupSchedulerGroupLocationScheduleNamesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs), [GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

### GroupType -> Group

A group type can have many groups. A serving team is usually one group inside a serving group type. If a problem affects many teams, start at the group type. If it affects one team, inspect the group first but still compare inherited group type settings.

Common symptoms of group type issues:

- all teams missing from scheduler;
- all teams missing from check-in;
- all teams missing required fields;
- all volunteers failing requirements;
- all teams hidden from external finder;
- all teams using wrong role labels;
- all team attendance reminders failing.

Common symptoms of group-level issues:

- one team missing from schedule board;
- one team missing location;
- one team archived or inactive;
- one team has wrong campus;
- one team missing schedule coordinator;
- one team has no members in schedulable role;
- one team has stale requirements;
- one team has incorrect security.

### Group -> GroupMember -> PersonAlias -> Person

A person can have multiple aliases; Rock commonly uses `PersonAliasId` in attendance and scheduling records. The SQL view joins `Attendance.PersonAliasId` to `PersonAlias.Id` and then uses `PersonAlias.PersonId` ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)). Agents should resolve aliases to the person rather than assuming the id on the attendance row is the person id.

Troubleshooting steps:

1. Identify the person.
2. Resolve current and historical person aliases.
3. Inspect group membership for the relevant group.
4. Verify role and status.
5. Verify communication fields and preferences.
6. Verify requirement status.
7. Verify schedule preferences.
8. Inspect attendance records by person alias, not only person id.
9. Check merged records if a person appears duplicated or missing.

### Group -> GroupLocation -> Location

Groups can have locations. Some groups have one location; others have multiple rooms or areas. The scheduler and check-in tools may display group and location paths, not just names. Source view models include `groupPath`, `locationPath`, and `locationName` ([GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs)).

Common issues:

- group has no location;
- location is too narrow for kiosk visibility;
- wrong location path;
- inactive or archived group still has group-location-schedule records;
- schedule exists but is not assigned to the location;
- duplicate similarly named locations confuse operators.

Rock v18.3 fixed a check-in issue where scheduled times could include schedules from archived or inactive groups that still had group-location-schedule assignments, reinforcing the need to clean up inactive/archived group scheduling relationships ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### GroupLocation -> GroupLocationSchedule -> Schedule

A group can be assigned to a location and that group location can be assigned one or more schedules. Source SQL shows `GroupLocationSchedule` as the link between `GroupLocation` and `Schedule` ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).

Agent checks:

- Does the schedule exist?
- Is it active?
- Is it assigned to the group's location?
- Is the group active and not archived?
- Does the schedule match the expected campus/service time?
- Does the recurring pattern produce the requested date?
- Is a schedule exclusion date range configured at the group type? Source view models include a group type schedule exclusion bag with start/end date semantics ([GroupTypeGroupScheduleExclusionBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs)).

### AttendanceOccurrence -> Attendance

`AttendanceOccurrence` is the occurrence. `Attendance` is the person-level record. The SQL view in the source pack exists for backward compatibility with pre-v8 attendance formats, which is itself a version caveat: older scripts may query attendance differently than modern Rock models ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

Agent checks:

- Does an occurrence exist for the group, schedule, location, and date?
- Are there attendance rows for the person alias?
- Are the rows actual attendance or scheduling/RSVP tracking?
- Was `DidAttend` set?
- Was the group marked did not meet?
- Is the occurrence duplicated?
- Did a workflow or confirmation route update the correct row?
- Did an automated link checker trigger an update in affected versions?

### GroupRequirement And Eligibility Data

The source pack does not provide full model details for group requirements. It does provide RockU's Group Requirements training page as a topic anchor ([Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements)). Therefore, agents should not invent exact schema behavior when requirements matter. Inspect the live instance:

- group type requirements;
- group-specific requirements;
- requirement type;
- whether requirement is warning-only or blocking;
- whether applies to all roles or selected roles;
- person data source used by requirement;
- workflow or attribute backing the requirement;
- last calculated status;
- failure reason;
- requirement cache or recalculation behavior, if present in that version.

## 7. Common Serving And Volunteer Operations Workflows

### New Volunteer Interest Intake

A serving-interest intake process usually has these stages:

1. Public serving opportunities are displayed.
2. A person selects a ministry or role.
3. A form collects basic contact and preference information.
4. A workflow or connection request is created.
5. A coordinator is notified.
6. The potential volunteer may select an observation date.
7. The volunteer receives confirmation.
8. The coordinator follows up.
9. The person completes application, training, or background check.
10. The person is approved or redirected.
11. The person is added to the serving team.
12. Schedule preferences are collected.
13. The person is scheduled for first serve.
14. Attendance and follow-up begin.

A community example describes an interest form, communication preference capture, optional observation date selection, email/text confirmation, connector notification, reminder before observation, and later serving application/background check trigger ([Serving Interest Process](https://community.rockrms.com/recipes/169)). That pattern is operationally useful because it separates interest from eligibility and placement. Do not add a person directly to a sensitive serving team until requirements and approval are satisfied.

Agent implementation checks:

- Is the public form creating a workflow, connection request, group member, or all three?
- Is the ministry selection stored as a structured value?
- Is the person's communication preference captured and honored?
- Are minors handled correctly?
- Is observation optional or required?
- Are coordinator notifications routed to a person, group role, or static email?
- Are reminders scheduled with a workflow timer or job?
- Are applications and background checks integrated securely?
- Is every workflow action auditable?
- Is there a dead-end state where a volunteer submits interest but no owner is notified?

### Build Or Audit A Serving Team

A serving team should have:

- a correct group type;
- a clear parent group;
- a campus if the ministry is campus-specific;
- active state;
- archive state false;
- correct roles;
- correct leader/coordinator;
- correct members;
- location assignment;
- schedule assignment;
- requirements;
- security;
- attendance settings;
- scheduling settings;
- communication settings;
- reporting inclusion.

Agent audit path:

1. Open the group.
2. Confirm active and not archived.
3. Confirm group type.
4. Confirm campus.
5. Confirm parent hierarchy.
6. Confirm roles and member status.
7. Confirm leader/coordinator.
8. Confirm group location.
9. Confirm assigned schedule.
10. Confirm requirements.
11. Confirm security.
12. Confirm scheduling block visibility.
13. Confirm attendance and reporting outputs.

### Volunteer Schedule Preference Collection

Schedule preferences let volunteers tell the scheduler when they prefer to serve. RockU includes "Person Preferences and Auto Schedule" as a dedicated scheduling training topic ([Person Preferences and Auto Schedule](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule)). The community schedule-preference recipe uses Page Parameter Filter and Dynamic Data to find volunteers by group, schedule, and location preference, with the explicit caveat that volunteers must be in a scheduling group and have preferences set ([Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238)).

Operational guidance:

- Collect preferences only after a person is in the correct serving group.
- Use ministry-specific schedule templates where needed.
- Name template schedules clearly.
- Include fifth-week patterns if the ministry needs auto-scheduling for fifth Sundays.
- Do not reuse Sunday templates for weekday ministries without verifying schedule day.
- Teach volunteers where preferences live.
- Build a report for volunteers missing preferences.
- Periodically audit stale preferences.

### Auto-Scheduling

Auto-scheduling depends on:

- group membership;
- schedule preferences;
- group location schedules;
- template schedules;
- role eligibility;
- requirement eligibility;
- exclusions;
- date range;
- ministry constraints;
- operator review.

The fifth-week community recipe exists because Rock Core did not ship fifth-Sunday group member schedule templates in that example, creating a recurring operational gap for auto-scheduling four times per year ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)). Before trusting auto-scheduling, simulate or review generated assignments for edge cases:

- fifth Sundays;
- holiday weekends;
- special services;
- multi-campus weekends;
- one-off events;
- people with multiple teams;
- people serving in family units;
- minors;
- requirement-expired volunteers;
- people already scheduled elsewhere.

### Send Schedule Confirmations

Scheduling confirmations should be sent only after the schedule has been reviewed. Source view models for sending confirmations distinguish:

- whether there are communications to send;
- eligible recipient count;
- communications sent count;
- warnings;
- errors ([GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

Agent checks after sending:

- Were any eligible recipients found?
- Were communications actually sent?
- Were warnings produced?
- Were errors produced?
- Were volunteers without email or phone excluded?
- Did security or communication preferences suppress delivery?
- Did the system communication render correctly?
- Did confirmation links point to the correct Rock route?
- Does the sender address route replies to the ministry owner?

A community recipe shows a dynamic sender pattern that falls back from group schedule coordinator to scheduled-by person to organization defaults ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)). If implementing that pattern, verify the sender field accepts Lava in the local version and system communication, that the schedule coordinator has a valid email, and that SPF/DMARC alignment is still valid for the sending domain.

### Volunteer Confirms Or Declines

Volunteer response paths can include:

- one-click confirmation email;
- Schedule Toolbox;
- mobile Schedule Toolbox;
- custom workflow page;
- family account page;
- staff manual update.

The mobile Schedule Toolbox documentation says the block manages opportunities for an individual and supports accept, decline, cancel, decline reason, and customization through templates ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)). Source-code enums identify `Pending`, `Confirmed`, `Declined`, and `Unavailable` statuses for toolbox rows ([ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs)).

Troubleshooting response failure:

1. Identify the scheduled attendance row.
2. Verify it belongs to the correct person alias.
3. Verify occurrence group, location, schedule, and date.
4. Verify the response endpoint or workflow.
5. Verify the confirmation token or parameters.
6. Verify whether decline reason is required.
7. Verify Rock version for the v17.2 link-checker/decline-reason fix.
8. Check communication history.
9. Check exception log.
10. Check workflow history if response is workflow-driven.

### View Serving Schedule Externally

Some churches want volunteers to view serving schedules without internal-site access. A community recipe creates separate external pages, copies the group toolbox page structure, adds a Schedule tab to Group Detail, and uses Dynamic Data plus Page Parameter Filter to show the schedule for a selected date ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459)).

This is useful but risky. Before exposing schedules externally:

- create separate pages for serving teams instead of editing shared group pages;
- restrict to authenticated volunteers if personal data is shown;
- avoid exposing private contact information;
- filter by group membership or ministry permissions;
- parameterize group id safely;
- avoid raw SQL injection risks in Dynamic Data;
- test with a non-staff volunteer account;
- verify no small group or unrelated group pages were changed;
- avoid showing minors' private data;
- include only fields needed by volunteers.

### Manage Family Members' Serving Requests

The core Schedule Toolbox is individual-centered in the community example. A draft recipe describes creating a custom page where a signed-in person can see future serving requests for family members and trigger workflows to accept or decline them ([Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489)).

This is a high-risk customization because family membership does not automatically mean permission to update another person's serving commitments in every context. Before implementing:

- verify family relationship rules;
- verify age/minor policy;
- verify whether spouses can respond for each other;
- verify whether parents can respond for minors;
- verify whether adult children are excluded;
- authorize by family role and age, not just shared family id;
- prevent arbitrary attendance id updates;
- use encrypted identifiers or server-side lookup;
- log who responded;
- preserve decline reason;
- test merged-family and split-household cases.

### Record Serving Attendance

Attendance can be recorded through:

- Group Attendance blocks;
- Check-In;
- Check-In Manager;
- manual entry;
- workflow;
- API;
- custom pages.

RockU includes Group Attendance as a training topic ([Group Attendance](https://community.rockrms.com/rocku/groups/group-attendance)). A community recipe for the Obsidian Group Attendance Detail block adds a toast confirmation because the block saves in real time without a page reload, which can confuse leaders who expect a traditional Save button ([Enhancing the Obsidian Group Attendance Detail Block with a Toast Confirmation](https://community.rockrms.com/recipes/461)).

Agent checks:

- Does the page use legacy or Obsidian block?
- Does attendance save immediately?
- Is the leader expecting a save button?
- Are permissions correct?
- Is the occurrence date correct?
- Are scheduled but absent people handled?
- Are no-shows reported?
- Are scheduling rows being confused with attended rows?
- Is `DidAttend` set correctly?
- Does the group have the right schedule and location?

### Follow Up On Declines And No-Shows

Declines and no-shows are operational signals.

Decline follow-up should answer:

- Did the volunteer decline early enough to replace them?
- Was a decline reason required?
- Was the decline reason stored?
- Was the coordinator notified?
- Is this a one-time decline or pattern?
- Is the person unavailable for future dates?
- Should schedule preferences be updated?

No-show follow-up should answer:

- Was the person actually scheduled?
- Did they confirm?
- Did they check in elsewhere?
- Was attendance taken?
- Was the group marked did not meet?
- Did the volunteer serve but attendance was missed?
- Should the volunteer receive care, correction, or schedule adjustment?
- Should the coordinator be notified?

Rock v18.3's reminder fix is relevant when follow-up depends on attendance reminders: scheduling/RSVP tracking rows should not suppress reminders as though real attendance exists ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 8. Serving Teams And Roles Deep Dive

### Designing Serving Group Types

A serving group type should reflect operational behavior, not only ministry branding. Design for:

- roster management;
- scheduling;
- attendance;
- check-in integration;
- requirements;
- communications;
- reporting;
- security;
- lifecycle.

Recommended group type questions:

- Will these groups be scheduled?
- Will volunteers take attendance?
- Will children or vulnerable populations be involved?
- Are background checks required?
- Are training requirements role-specific?
- Do groups need locations?
- Do groups need schedules?
- Do groups appear externally?
- Do volunteers self-join, apply, or get placed?
- Are groups campus-specific?
- Are groups seasonal?
- Are groups event-specific?
- Are groups reused or archived after use?
- Do groups need parent/child hierarchy?
- Will the group type be used by Check-In?

### Real Team vs Sign-Up Opportunity vs Interest Pipeline

Do not overload one group type if the lifecycle differs. Three common objects look similar but behave differently:

**Real serving team**  
A durable group used for scheduling, attendance, communication, and reporting.

**Sign-up opportunity**  
A public or seasonal opportunity where people indicate availability. A community Q&A example solved campus/service-specific Christmas volunteer sign-ups by creating separate sign-up group types for each campus/service time, then limiting the finder to the relevant sign-up group ([Sign-Up Registration - Limit to particular schedule / campus](https://community.rockrms.com/ask/using/2808)).

**Interest pipeline**  
A workflow or connection flow for people not yet approved or placed. The serving-interest recipe uses workflow and connector actions before the person reaches full serving application/background-check steps ([Serving Interest Process](https://community.rockrms.com/recipes/169)).

Agent rule: before changing membership or schedule behavior, identify which object you are working with. A sign-up group may not be the final serving team.

### Role Design

Roles should be stable and meaningful. Avoid creating a new role for every schedule or location; use group locations and schedules for where/when. Use roles for responsibility and eligibility.

Good role examples:

- Leader.
- Assistant Leader.
- Coordinator.
- Scheduler.
- Volunteer.
- Substitute.
- Trainee.
- Observer.
- Applicant.
- Inactive.

Poor role examples:

- Sunday 9:00.
- Sunday 11:00.
- Room 101.
- June Volunteer.
- Christmas Eve 4 PM.

Those are usually schedules, locations, or event assignments, not roles.

### Role-Based Scheduling

Before scheduling a person, verify:

- group member status;
- role;
- whether role is schedulable by local convention;
- whether requirement applies to that role;
- whether the person has opted out;
- whether they have schedule preferences;
- whether they are already scheduled elsewhere.

Some ministries use substitute or trainee roles. Decide whether those roles should be auto-scheduled, manually scheduled only, or excluded entirely.

### Team Coordinator Fields

The dynamic sender recipe uses group schedule coordinator as the first sender fallback for scheduling confirmations ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)). If your instance uses schedule coordinators:

- populate the field consistently;
- require valid email addresses;
- define fallback behavior;
- document ownership when a coordinator leaves staff;
- include coordinator in security groups only where appropriate;
- monitor blank coordinator fields.

### Group History

RockU includes Group History as a training topic ([Group History](https://community.rockrms.com/rocku/groups/group-history)). For serving teams, history can help diagnose:

- who added a volunteer;
- who changed a role;
- when a person left;
- whether a schedule or location was changed;
- whether a group was archived;
- whether a leader field changed;
- whether a role was renamed.

If history is incomplete or not sufficient for the question, inspect audit fields, communication history, workflow history, and SQL row timestamps in the live instance.

## 9. Schedules And Confirmations Deep Dive

### Meeting Details

RockU separates "Group Scheduling - Overview" and "Group Scheduling - Meeting Details," which reflects the two-part model: scheduling is not only picking people, it also depends on the meeting's date/time/location context ([Group Scheduling - Overview](https://community.rockrms.com/rocku/groups/group-scheduling-overview), [Group Scheduling - Meeting Details](https://community.rockrms.com/rocku/groups/group-scheduling-meeting-details)).

Meeting detail checks:

- group;
- occurrence date;
- schedule;
- location;
- campus;
- capacity or needed count, if used;
- roles needed;
- excluded dates;
- existing scheduled people;
- confirmed count;
- declined count;
- pending count;
- attendance state after the event.

### Scheduler And Status Board

RockU includes a "Group Scheduler and Status Board" topic in the scheduling sequence, although the source pack only includes compact metadata for it through the RockU navigation list. Use it as an authority pointer and inspect the live block/page for settings. The source-code view models show that the scheduler handles selected locations, group schedule names, and send-confirmation outcomes ([GroupSchedulerLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs), [GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

Status board checks:

- Which group type or group is selected?
- Which date range is selected?
- Which locations are selected?
- Which schedules are selected?
- Are inactive or archived groups excluded?
- Are all required roles filled?
- Are pending confirmations visible?
- Are declines visible?
- Can the operator send confirmations?
- Are warnings/errors displayed after sending?

### Confirmation Statuses

Source-code enums define the schedule toolbox row statuses:

- `Pending`: person has not confirmed availability.
- `Confirmed`: person has committed.
- `Declined`: person declined.
- `Unavailable`: person is unavailable.

Use those statuses conceptually, but verify the live storage fields and enum values before writing SQL or API updates. The C# and TypeScript enum records are implementation landmarks for current/develop code, not a guarantee that every deployed version stores responses identically ([ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs), [toolboxScheduleRowConfirmationStatus.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Blocks/Group/Scheduling/toolboxScheduleRowConfirmationStatus.ts)).

### Decline Reasons

The Schedule Toolbox documentation says decline can include a reason ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)). Release notes say v17.2 fixed a case where the Group Scheduling Confirmation workflow could incorrectly record a response if a decline reason was required but not provided ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent checks:

- Is decline reason required?
- Is the confirmation link one-button or multi-step?
- Does the workflow block response until a reason exists?
- Are automated link checkers opening decline links?
- Does the deployed version include the v17.2 fix?
- Are decline reasons defined values, free text, or workflow attributes?
- Does the scheduler receive the reason?

### Automated Link Checkers

Email security tools may open links before a person does. Release notes explicitly mention automated link-checker behavior in the Group Scheduling Confirmation workflow fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Symptoms:

- volunteers appear confirmed immediately after send;
- volunteers appear declined without action;
- responses occur at send time;
- response user agent looks like a scanner;
- decline reason missing;
- many responses happen at the same timestamp.

Mitigations to inspect:

- Rock version and fix availability;
- confirmation workflow design;
- one-click vs confirmation landing page;
- token handling;
- required human action before mutating attendance;
- email security logs;
- communication open/click logs.

### Mobile Schedule Toolbox

The mobile Schedule Toolbox block is documented for mobile v4.0 / core v13.1 and supports accept, decline, cancel, templates, scheduler confirmation emails, and scheduling response email configuration ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)).

Agent checks for mobile:

- Is the app using the mobile block or a web page?
- Is the person authenticated?
- Does the block scope to the current individual only?
- Are templates customized?
- Did custom template syntax break?
- Are commands wired correctly?
- Does the response email send?
- Are push notifications involved?
- Is the mobile shell caching old content?
- Does the same request work on web?

The developer doc warns that the default template had invalid `|` characters on specific lines until a fix was in place. If an older instance has a broken template, compare against the deployed block documentation and local template carefully without copying remote text wholesale ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)).

## 10. Volunteer Requirements Deep Dive

### Requirement Categories

Serving requirements commonly fall into these categories:

- identity and profile completeness;
- age or grade minimum;
- membership or covenant status;
- baptism or spiritual milestone;
- background check;
- child safety training;
- mandated reporter training;
- ministry-specific training;
- application approval;
- reference approval;
- interview;
- observation;
- signed policy or document;
- driver's license or insurance;
- medical certification;
- recurring renewal.

RockU's Group Requirements page is the primary source pointer in the pack for core requirement behavior ([Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements)). The serving-interest community recipe shows an operational flow where application and background check are triggered after observation and connector review ([Serving Interest Process](https://community.rockrms.com/recipes/169)).

### Requirement Placement

Requirements can be implemented at different layers:

- group type requirement;
- group-specific requirement;
- role-specific requirement;
- workflow step;
- connection opportunity status;
- person attribute;
- group member attribute;
- document/signature record;
- external integration;
- data view/report used by staff.

Agent rule: do not assume a visible "requirements" list is the only eligibility system. Many churches combine Rock requirements with workflows and external background-check integrations.

### Blocking vs Warning

Some requirements block scheduling or service. Others warn staff but allow scheduling. Inspect the live configuration:

- Does the requirement block adding a person?
- Does it block scheduling?
- Does it block check-in?
- Does it only display a warning?
- Does it apply to all roles?
- Does it apply to leaders only?
- Does the block enforce it or only report it?
- Is there an override path?
- Who can override?

### Requirement Failure Troubleshooting

If a volunteer is marked ineligible:

1. Identify the requirement name.
2. Inspect whether it is group type, group, or role-specific.
3. Inspect the underlying data source.
4. Inspect the person's record.
5. Inspect person aliases if requirement logic joins alias-based tables.
6. Inspect expired records.
7. Inspect workflow state.
8. Inspect background-check integration state.
9. Inspect requirement recalculation timing.
10. Inspect permissions: the operator may not be able to see the sensitive requirement detail.

### Sensitive Data Guardrails

Requirements often involve sensitive data. Agents should avoid exposing:

- background-check details;
- abuse-prevention flags;
- legal documents;
- minor information;
- medical certifications;
- rejection reasons;
- private notes.

Report only the operational state needed: satisfied, missing, expired, pending, failed, needs review. If detail is required, direct the operator to the secure Rock page and role authorized to view it.

## 11. Attendance And Follow-Up Deep Dive

### Attendance vs Scheduled Assignment

A scheduled assignment says a person was asked or expected to serve. Attendance says whether they actually did. Do not count scheduled rows as attendance without verifying attended status.

The source SQL view counts attendance by joining `Attendance` to `AttendanceOccurrence` and filtering `DidAttend = 1` ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)). Release notes show that Rock itself had to distinguish scheduling/RSVP tracking records from actual attendance in the Send Attendance Reminder job ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Group Attendance Blocks

RockU has Group Attendance as a training topic ([Group Attendance](https://community.rockrms.com/rocku/groups/group-attendance)). A community recipe notes that the Obsidian Group Attendance Detail block can save without a page reload, making user feedback important ([Enhancing the Obsidian Group Attendance Detail Block with a Toast Confirmation](https://community.rockrms.com/recipes/461)).

Rapid Attendance Entry is another attendance-capture surface that can matter for volunteer follow-up. A reviewed RockU transcript insight says the block can combine attendance marking with family edits, person notes, prayer requests, and workflow launch actions when its settings enable those actions; use that as a prompt to inspect page variants and enabled actions before assuming attendance entry is only recording present/absent state ([Rapid Attendance Entry, 02:17](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)).

Agent checks:

- Which attendance block is used?
- Does the page pass group id and occurrence date correctly?
- Are schedules and locations included?
- Is attendance saved automatically?
- Is there a visible save confirmation?
- Does the leader have permission?
- Are absent scheduled people displayed?
- Are additions allowed?
- Are check-in records also writing attendance?

### Check-In Attendance

Serving teams that intersect with check-in require special care. Check-in documentation describes group types, inherited attributes, group location, schedules, printers, check-in manager, and roster filtering by schedule in later versions ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Agent checks for check-in serving:

- Is this a serving team or a check-in group?
- Does the group belong to the configured check-in area?
- Does the group type inherit the right attributes?
- Are age/grade/ability restrictions correct?
- Is the group assigned a broad enough location?
- Is the schedule active at check-in time?
- Is the kiosk configured for the location?
- Is the group active and not archived?
- Are inactive or archived groups still leaking schedules?
- Is the roster filter set to the expected schedule?

### Attendance Reminder Job

Rock v18.3 fixed the Send Attendance Reminder job so group leaders still receive reminders when a group only has scheduling/RSVP-related attendance records. The job should suppress reminders only when real attendance exists or the group was marked did not meet ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

If leaders are not receiving reminders:

1. Verify Rock version.
2. Inspect the job configuration.
3. Inspect job history.
4. Inspect group leader role and email addresses.
5. Inspect occurrence records for the date.
6. Inspect whether actual `DidAttend` rows exist.
7. Inspect whether group was marked did not meet.
8. Inspect scheduling/RSVP rows that may be mistaken for attendance in older versions.
9. Inspect communication failures.

### No-Show Reporting

No-show logic should compare:

- scheduled/confirmed people;
- actual attendance;
- group did not meet state;
- late attendance entry;
- substitute attendance;
- check-in attendance;
- declined/unavailable status.

Avoid shaming reports that confuse data-entry lag with absence. Operationally, no-show follow-up should usually run after attendance entry is expected to be complete.

### Follow-Up Workflows

Follow-up workflows can be triggered by:

- decline;
- no response;
- no-show;
- requirement expiration;
- schedule conflict;
- serving frequency threshold;
- inactivity;
- new volunteer first serve;
- leader attendance not submitted.

For each workflow, inspect:

- trigger;
- entity type;
- person alias resolution;
- deduplication;
- reminders;
- escalation;
- completion criteria;
- communication templates;
- security;
- logging.

## 12. Related Rock Areas: Groups, Scheduling, Locations, Check In, Communications, Workflows, People, Security

### Groups

Groups are the backbone. Almost every serving operation eventually traces to group type, group, role, membership, requirement, location, schedule, attendance, or security. RockU's Groups track is the strongest source set in this pack for the conceptual spread of group features ([Group Viewer](https://community.rockrms.com/rocku/groups/group-viewer), [Group Details](https://community.rockrms.com/rocku/groups/group-details), [Group Types](https://community.rockrms.com/rocku/groups/group-types)).

### Scheduling

Scheduling is a layer on group membership and meeting details. It includes meeting details, scheduler/status board, preferences, auto-schedule, analytics, RSVP, requests, responses, roster, and communications. RockU's scheduling sequence is an important navigation map for staff training and agent triage ([Group Scheduling - Overview](https://community.rockrms.com/rocku/groups/group-scheduling-overview), [Person Preferences and Auto Schedule](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule), [Group Scheduling Roster and Communications](https://community.rockrms.com/rocku/groups/group-scheduling-roster-and-communications)).

### Locations

Locations affect scheduler visibility, check-in visibility, reporting, campus service filtering, and volunteer communication. Source view models expose group path, location path, and active schedule ids for group locations ([GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs)).

### Check-In

Check-in can record attendance and can also expose scheduling/location issues. Check-in documentation notes version-specific features such as a security verb controlling attendance deletion, check-out configuration, and roster filtering by schedule in Rock 14.0 updates ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

### Communications

Communications include system communications, group communications, scheduling confirmations, response emails, reminders, and workflow messages. The Schedule Toolbox developer doc includes scheduler confirmation and scheduling response email sections ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)). Community sender customization shows practical Lava usage in system communication fields ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)).

### Workflows

Workflows bridge gaps between core objects and local ministry process. Use workflows for serving interest, observation, applications, background checks, family responses, no-show follow-up, and coordinator notifications where core scheduling does not cover the full process ([Serving Interest Process](https://community.rockrms.com/recipes/169), [Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489)).

### People

People data affects every serving process:

- contact information;
- email validity;
- phone/SMS;
- family relationships;
- age;
- grade;
- connection status;
- aliases;
- duplicate/merged records;
- communication preferences;
- background-check attributes;
- training status.

Resolve person aliases when tracing attendance and scheduling records. Source SQL joins `Attendance.PersonAliasId` to `PersonAlias.Id`, then uses `PersonAlias.PersonId` ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

### Security

Serving security covers:

- who can view groups;
- who can edit groups;
- who can schedule;
- who can take attendance;
- who can view requirements;
- who can view minors;
- who can access external schedule pages;
- who can respond for family members;
- who can delete attendance;
- who can send communications.

RockU has Group Security as a dedicated topic ([Group Security](https://community.rockrms.com/rocku/groups/group-security)). Check-in documentation notes a version update adding a security verb controlling who can delete attendance from Check-in Manager roster ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

## 13. Administration And Operational Guardrails

### Configuration Guardrails

Maintain a serving operations register with:

- group type id/name;
- ministry owner;
- coordinator;
- default roles;
- requirements;
- schedule templates;
- locations;
- system communications;
- workflows;
- pages/blocks;
- reports;
- security groups;
- known version caveats.

### Page And Block Guardrails

Before editing a serving page:

- identify whether the page is shared with small groups, families, or other group types;
- copy pages when customization should apply only to serving teams;
- inspect page parameters;
- inspect block settings;
- test with staff and non-staff users;
- avoid exposing internal status boards externally;
- avoid raw person/contact data in public pages.

The external schedule recipe specifically copied the Group Toolbox page family to avoid changing small group pages when customizing serving team pages ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459)). That is a useful pattern: isolate serving customizations when shared pages would create unintended changes.

### Communication Guardrails

Before sending scheduling communications:

- verify recipient count;
- verify eligible count;
- preview the message;
- verify merge fields;
- verify from address and reply-to;
- verify coordinator fallback;
- verify confirmation links;
- verify unsubscribe/communication preference implications;
- send a test to staff;
- inspect warnings/errors after send.

The scheduler send-confirmation response model explicitly includes eligible recipient count, sent count, warnings, and errors, so agents should use those as operational checks where exposed by the UI/API ([GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

### Data Hygiene Guardrails

Regularly audit:

- inactive groups with schedules;
- archived groups with group-location-schedule rows;
- groups without coordinators;
- groups without leaders;
- active volunteers without email;
- active volunteers without preferences;
- expired requirements;
- duplicate schedules;
- schedules assigned to wrong day;
- fifth-week gaps;
- stale sign-up groups;
- old workflow states;
- old attendance occurrences without attendance;
- people scheduled after becoming inactive.

Rock v18.3's check-in fix around archived/inactive groups appearing in scheduled times is a specific warning that stale group-location-schedule data can leak into operational surfaces ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Security Guardrails

Use least privilege:

- volunteers can view only their schedules and appropriate team context;
- leaders can manage their teams;
- schedulers can schedule appropriate group types;
- ministry admins can edit group configuration;
- system admins can edit system communications and workflow definitions;
- sensitive requirement details are limited to authorized roles.

For family-serving customizations, do not authorize updates solely because two people share a family group. Verify relationship, age, and local policy ([Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489)).

## 14. Developer, API, Lava, And Source-Code Landmarks

### Schedule Toolbox Developer Doc

The Schedule Toolbox mobile developer doc is a key implementation landmark. It describes:

- accepting scheduled attendances;
- declining;
- cancelling a previous response;
- decline reason support;
- customizable toolbox template;
- merge fields;
- commands;
- confirm decline template;
- scheduler confirmation emails;
- scheduling response email;
- styling ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)).

Use it when diagnosing mobile volunteer response issues or customizing the mobile serving experience.

### Confirmation Status Enum

Use `ToolboxScheduleRowConfirmationStatus` as a source-code landmark for statuses:

- `Pending = 0`;
- `Confirmed = 1`;
- `Declined = 2`;
- `Unavailable = 3`.

Cite and inspect the C# or TypeScript enum, then verify deployed-version storage before writing data updates ([ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs), [toolboxScheduleRowConfirmationStatus.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/Enums/Blocks/Group/Scheduling/toolboxScheduleRowConfirmationStatus.ts)).

### Scheduler Send Confirmation Response

The scheduler send-confirmation response bag is useful for expected operational output:

- `AnyCommunicationsToSend`;
- `CommunicationsSentCount`;
- `EligibleRecipientCount`;
- `Errors`;
- `Warnings` ([GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

If a UI says "no confirmations sent," distinguish "no eligible recipients" from "eligible recipients found but errors occurred."

### Group Scheduler Location Bags

The scheduler location bags expose available and selected locations and group schedule names ([GroupSchedulerLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs), [GroupSchedulerGroupLocationScheduleNamesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs)). Use them as landmarks when tracing why a scheduler page shows or hides locations.

### Check-In Scheduled Locations

Check-in scheduled location source files and view models show that check-in can present group, group path, location, location path, and schedules as editable scheduling surfaces ([CheckinScheduledLocations.ascx](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/CheckIn/CheckinScheduledLocations.ascx), [GetScheduledLocationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/CheckInKiosk/GetScheduledLocationsResponseBag.cs)). Use these when check-in and volunteer scheduling disagree.

### Attendance View

`vCheckin_GroupTypeAttendance.sql` is a backward-compatibility view that exposes attendance by group type with joins across attendance occurrence, attendance, person alias, and group. It is useful as a model-map landmark but should not be treated as the only reporting path ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

### Lava Landmarks

Community recipes use Lava for:

- external schedule display;
- Dynamic Data blocks;
- system communication sender fallback;
- custom Schedule Toolbox pages;
- family serving request pages ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459), [Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530), [Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489)).

Lava guardrails:

- avoid exposing sensitive fields;
- avoid unparameterized SQL;
- sanitize page parameters;
- test with non-admin users;
- avoid editing shared Lava files unless intended;
- keep custom Lava under source control where possible;
- document page/block dependencies.

## 15. Reporting, Analytics, And Model Map

### Reporting Concepts

Serving reporting should answer:

- How many active volunteers do we have?
- Which teams are under-filled?
- Which dates are under-filled?
- Which scheduled volunteers have not responded?
- Which volunteers declined?
- Which confirmed volunteers did not attend?
- Which volunteers served most often?
- Which volunteers have not served recently?
- Which volunteers have expired requirements?
- Which teams have no leader or coordinator?
- Which schedules lack fifth-week coverage?
- Which inactive groups still have schedules?
- Which communications failed?

RockU includes "Group Scheduling - Analytics" as a training topic ([Group Scheduling - Analytics](https://community.rockrms.com/rocku/groups/group-scheduling-analytics)). The Model Map record in the source pack identifies `Analytics Fact Attendance` as a reporting model ([Model Map](https://community.rockrms.com/ModelMap)). Use Model Map as a discovery path, then inspect the live schema and reporting model in the deployed version.

### Attendance Reporting

For attendance reporting, distinguish:

- scheduled;
- requested;
- pending;
- confirmed;
- declined;
- unavailable;
- attended;
- absent/no-show;
- group did not meet.

Use `AttendanceOccurrence` for context and `Attendance` for person-level state. The source SQL view demonstrates occurrence fields such as group, schedule, location, occurrence date, and Sunday date ([vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql)).

### Schedule Coverage Reporting

Coverage reports should group by:

- ministry;
- campus;
- group type;
- group;
- role;
- schedule;
- location;
- occurrence date;
- needed count;
- scheduled count;
- confirmed count;
- declined count;
- pending count;
- attended count.

If needed count is not in the source pack, inspect live group scheduling configuration, group attributes, or custom ministry configuration. Do not invent a capacity model.

### Requirement Reporting

Requirement reports should show:

- person;
- group;
- role;
- requirement;
- status;
- expiration date;
- owner;
- next action.

Avoid exposing sensitive details. Use summary states unless the report is restricted to authorized staff.

### Schedule Preference Reporting

The community recipe for filtering volunteers by schedule preference uses Page Parameter Filter and Dynamic Data to filter by groups, schedules, and locations ([Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238)). Use that as a pattern only after validating schema and performance in the live instance.

### Analytics Caveats

Analytics can be wrong if:

- scheduled rows are counted as attended;
- inactive groups are included;
- archived groups are included;
- duplicate schedules exist;
- group hierarchy is misread;
- person aliases are not resolved;
- requirements are cached;
- attendance was entered late;
- check-in and group attendance both wrote rows;
- historical group memberships changed;
- reports ignore campus or location.

## 16. Version And Release Caveats

### Rock v17.2 Group Scheduling Confirmation Fix

Rock v17.2 fixed an issue where Group Scheduling Confirmation workflow could incorrectly record a response if an automated link checker opened the email link or if decline reason was required but missing ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent impact:

- For versions before the fix, suspect email security scanners when responses appear without volunteer action.
- For any version, inspect decline-reason behavior when declines are malformed.
- Verify the confirmation workflow and system communication route.
- Consider requiring a human confirmation page before mutating records if local email security tools are aggressive.

### Rock v18.3 Attendance Reminder Fix

Rock v18.3 fixed the Send Attendance Reminder job so scheduling/RSVP-related attendance records alone do not suppress reminders ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent impact:

- If leaders are not receiving attendance reminders, inspect version and attendance row types.
- Do not assume any attendance-related row means real attendance exists.
- Verify `DidAttend` and group did-not-meet state.

### Rock v18.3 Check-In Scheduled Times Fix

Rock v18.3 fixed Check-In Type Detail block scheduled times so schedules from archived or inactive groups with lingering `GroupLocationSchedule` assignments are excluded ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agent impact:

- Clean up archived/inactive group schedule assignments.
- If old schedules appear in check-in, inspect group active/archive state and group-location-schedule rows.
- Verify deployed version before assuming the filter exists.

### Rock v14 Check-In Manager Roster Updates

Check-in documentation notes Rock 14.0 updates including a new security verb for deleting attendance from Check-in Manager roster, check-out enablement scope, and roster filtering by schedule ([Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266)).

Agent impact:

- If a user cannot delete attendance, inspect the security verb.
- If roster filtering by schedule is expected, verify version.
- If check-out behavior differs by kiosk vs manager, inspect check-in configuration.

### Mobile Schedule Toolbox Version

The mobile Schedule Toolbox documentation indicates mobile v4.0 / core v13.1 ([Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox)).

Agent impact:

- Verify mobile and core versions.
- Verify customized templates against local version.
- Do not assume mobile block behavior exists in older apps.

## 17. Implementation Playbooks

### Playbook: Launch A New Serving Ministry Team

1. Define the ministry owner and coordinator.
2. Decide whether this is a durable serving team, sign-up opportunity, or intake pipeline.
3. Select or create the group type.
4. Define roles.
5. Define requirements.
6. Create the group.
7. Assign campus.
8. Assign parent group.
9. Assign group location.
10. Assign schedules.
11. Add leader/coordinator.
12. Add initial volunteers.
13. Collect schedule preferences.
14. Configure scheduling communications.
15. Configure attendance page.
16. Configure reports.
17. Test with one volunteer.
18. Test confirmation and decline.
19. Test attendance entry.
20. Document owner and maintenance path.

### Playbook: Add Fifth-Sunday Auto-Schedule Coverage

1. Identify ministries using auto-schedule.
2. List template schedules volunteers can select.
3. Identify missing fifth-week templates.
4. Create schedules with clear day-specific names.
5. Assign templates only to matching ministry days.
6. Update volunteer preference instructions.
7. Test auto-schedule for a fifth Sunday.
8. Review generated assignments.
9. Watch for duplicate or wrong-day assignments.

This playbook is based on the fifth-week template issue described in the community recipe ([Group Member Schedule Templates](https://community.rockrms.com/recipes/356)).

### Playbook: Build External Serving Schedule View

1. Identify target volunteers and data needed.
2. Avoid exposing internal status board directly.
3. Copy page structure if existing group pages are shared.
4. Create serving-specific pages.
5. Add group detail schedule tab or equivalent.
6. Add safe filters for date, group, schedule, or location.
7. Use Dynamic Data only with parameter safety.
8. Restrict access appropriately.
9. Test with non-staff volunteer.
10. Verify no unrelated group pages changed.
11. Document page ids, block ids, and SQL/Lava source.

This follows the isolation pattern from the external schedule recipe while adding security checks ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459)).

### Playbook: Configure Dynamic Sender For Scheduling Confirmations

1. Identify the system communication.
2. Verify it supports Lava in sender fields.
3. Decide fallback order.
4. Populate group schedule coordinators.
5. Configure from address and name.
6. Ensure fallback organization sender is valid.
7. Test groups with coordinator.
8. Test groups without coordinator.
9. Test scheduled-by fallback.
10. Verify reply handling.
11. Verify DMARC/SPF alignment.

The community recipe uses coordinator, scheduled-by person, and organization defaults as fallback levels ([Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530)).

### Playbook: Add Serving Interest Intake

1. Publish ministry opportunities.
2. Use a workflow or connection request for interest.
3. Collect contact and communication preference.
4. Route to connector/coordinator.
5. Offer observation scheduling if needed.
6. Send confirmation.
7. Send reminder before observation.
8. Trigger application/background check only when appropriate.
9. Record activity on the request.
10. Move approved person into serving team.
11. Collect schedule preferences.
12. Schedule first serve.
13. Follow up after first serve.

This mirrors the operational stages in the serving-interest recipe without copying its implementation details ([Serving Interest Process](https://community.rockrms.com/recipes/169)).

### Playbook: Audit Scheduling Confirmation Failures

1. Identify affected person.
2. Identify scheduled attendance record.
3. Identify occurrence group, schedule, location, and date.
4. Inspect communication history.
5. Inspect confirmation URL or workflow parameters.
6. Inspect Rock version.
7. Check for v17.2 confirmation workflow fix.
8. Inspect decline reason requirement.
9. Check exception log.
10. Check whether email security opened links.
11. Re-send test confirmation to controlled account.
12. Verify response writes the expected status.

### Playbook: Audit Attendance Reminder Failure

1. Identify group and date.
2. Verify group leaders and email addresses.
3. Verify attendance reminder job configuration.
4. Inspect job history.
5. Inspect attendance occurrences.
6. Separate scheduling/RSVP rows from attended rows.
7. Check group did-not-meet status.
8. Verify Rock version for v18.3 reminder fix.
9. Send test communication if needed.
10. Document root cause.

### Playbook: Clean Up Archived Groups With Schedules

1. List inactive or archived groups in serving/check-in group types.
2. Identify group locations.
3. Identify group-location-schedule assignments.
4. Decide whether to reactivate, archive fully, or remove schedule assignments.
5. Verify check-in scheduled times no longer show stale entries.
6. Verify scheduler no longer shows stale entries.
7. Document cleanup rules.

This is especially relevant to the v18.3 check-in scheduled-times fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 18. Troubleshooting Decision Tree

### Volunteer Cannot See Schedule

Check:

- Is the person logged in?
- Is the person in the serving group?
- Is the group active and not archived?
- Is the group type included by the page/block?
- Does the page filter by campus, group, schedule, or location?
- Does the group have a group location schedule?
- Is the occurrence within the date range?
- Is the volunteer scheduled?
- Is the block scoped to current person only?
- Does security allow viewing?
- Is this web Schedule Toolbox, mobile Schedule Toolbox, or custom external page?

Sources: [Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox), [View Serving Schedule on External Page](https://community.rockrms.com/recipes/459).

### Volunteer Cannot Accept Or Decline

Check:

- scheduled attendance exists;
- person alias matches the volunteer;
- attendance occurrence matches group/date/schedule/location;
- confirmation status is pending;
- confirmation link has valid token/parameters;
- decline reason requirement;
- workflow errors;
- Rock version and v17.2 fix;
- automated link checker behavior;
- user is trying to respond for a family member but block only supports self;
- custom workflow authorization.

Sources: [Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox), [Rock Core Release Notes](https://www.rockrms.com/releasenotes), [Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489).

### Confirmation Recorded Without Volunteer Action

Check:

- communication click/open logs;
- response timestamp compared to send timestamp;
- user agent if available;
- automated email-security scanning;
- Rock version;
- v17.2 fix;
- workflow route;
- whether one-click links mutate state immediately;
- required decline reason behavior.

Source: [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Scheduler Shows No Eligible Recipients

Check:

- group members exist;
- members have valid person aliases;
- members have email/SMS contact;
- members are in schedulable roles;
- members meet requirements;
- schedule assignments exist;
- date range has occurrences;
- communication preferences allow send;
- scheduler response eligible recipient count;
- warnings/errors.

Source: [GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs).

### Schedule Missing From Group

Check:

- schedule exists;
- schedule active;
- schedule recurrence produces target date;
- schedule assigned to group location;
- group has correct location;
- group active and not archived;
- group type schedule exclusions;
- schedule day matches ministry day;
- fifth-week schedule exists if needed.

Sources: [View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql), [Group Member Schedule Templates](https://community.rockrms.com/recipes/356).

### Check-In Does Not Show Serving Group

Check:

- group type belongs to check-in area;
- inherited group type attributes;
- age/grade/ability requirements;
- group active and not archived;
- location configured broadly enough;
- kiosk configured for location;
- schedule active at current time;
- group-location-schedule exists;
- check-in type scheduled times not polluted by archived groups;
- version-specific check-in behavior.

Sources: [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266), [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Attendance Reminder Not Sent

Check:

- job configuration;
- job history;
- leader role and emails;
- communication failures;
- attendance occurrence exists;
- actual attended rows exist;
- group did not meet marker;
- scheduling/RSVP rows only;
- Rock version and v18.3 fix.

Source: [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Attendance Looks Too High

Check:

- scheduled rows counted as attended;
- duplicate occurrences;
- check-in plus manual attendance duplicates;
- person alias merges;
- date range includes multiple services;
- group hierarchy includes child groups unexpectedly;
- report joins attendance without `DidAttend`;
- archived groups included;
- test data included.

Source: [vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql).

### Volunteers Missing From Preference Report

Check:

- person is in a scheduling group;
- group is active;
- group type matches report filter;
- volunteer has preferences set;
- schedule id matches;
- location id matches;
- campus filter;
- role filter;
- person alias/person id join;
- custom SQL parameter handling.

Source: [Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238).

### External Schedule Page Shows Wrong Groups

Check:

- page was copied or shared;
- block settings;
- page parameter;
- Dynamic Data SQL;
- group type filter;
- security;
- whether small group pages share same Lava file;
- cached content;
- archived/inactive group filters.

Source: [View Serving Schedule on External Page](https://community.rockrms.com/recipes/459).

## 19. Agent Task Recipes

### Recipe: Find The Real Object Behind A Serving Issue

1. Ask for the person, date, team, and service time.
2. Resolve person and aliases.
3. Identify the serving group.
4. Identify group type.
5. Identify group location.
6. Identify schedule.
7. Identify attendance occurrence.
8. Identify attendance/scheduling row.
9. Identify communication/workflow history.
10. Report the exact broken link in the chain.

### Recipe: Confirm A Volunteer Is Eligible To Serve

Inspect:

- person active status;
- age/grade if relevant;
- group membership;
- role;
- group member status;
- group requirements;
- person attributes backing requirements;
- background check/training state;
- workflow/application state;
- schedule preferences;
- local ministry approval.

If requirement source is unclear, say: "Inspect the group requirement definition and its backing data source in the live Rock instance."

### Recipe: Explain Why A Volunteer Was Not Scheduled

Inspect:

- group membership;
- schedulable role;
- schedule preferences;
- availability/unavailability;
- existing schedule conflicts;
- group location schedule;
- required role counts;
- requirements;
- manual exclusions;
- auto-schedule settings;
- scheduler warnings.

### Recipe: Verify Schedule Confirmation Send Health

Inspect:

- selected group/date/location/schedule;
- eligible recipient count;
- sent count;
- warnings;
- errors;
- communication history;
- failed recipients;
- system communication template;
- sender fallback;
- confirmation link route.

Use the send-confirmation response model as a checklist where available ([GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)).

### Recipe: Safely Customize A Volunteer-Facing Page

1. Identify whether the page is shared.
2. Copy shared pages when customization is serving-specific.
3. Limit page data to current person or authorized group.
4. Avoid exposing private contact fields.
5. Use safe parameters.
6. Test with non-admin account.
7. Document page ids and block settings.
8. Keep Lava and SQL in source control where possible.

The external schedule recipe demonstrates why copied pages may be necessary when serving teams share a toolbox with other group categories ([View Serving Schedule on External Page](https://community.rockrms.com/recipes/459)).

### Recipe: Investigate Family Serving Response Request

1. Identify current logged-in person.
2. Identify target scheduled person.
3. Verify family relationship.
4. Verify age and role policy.
5. Verify scheduled attendance row.
6. Verify authorization to respond.
7. Verify workflow action updates only that row.
8. Log responder.
9. Preserve decline reason.
10. Test with spouse, minor child, adult child, and unrelated person.

Source pattern: [Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489).

### Recipe: Build A Serving Health Dashboard

Include:

- active volunteer count;
- volunteers missing preferences;
- volunteers with expired requirements;
- pending confirmations by date;
- declined confirmations by date;
- unfilled role slots;
- no-shows;
- first-time servers;
- inactive volunteers still scheduled;
- archived groups with schedules;
- communications failed;
- attendance reminders not sent.

Cite reporting model landmarks where appropriate: [Model Map](https://community.rockrms.com/ModelMap), [vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql).























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `41`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Rock LMS organizes training into programs, courses, class instances, learning plans, activities, and learning participants, with the program deciding whether the experience is on-demand or academic-calendar based. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | implementation_pattern | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| community-reviewed | operational_guidance | A leadership-facing Rock dashboard should make metric definitions explicit so teams know which values are current-state snapshots, historical trends, or ministry-specific targets. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) |
| community-reviewed | operational_guidance | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | When moving from another LMS into Rock, plan for differences in platform logic instead of assuming videos and lessons can be imported without redesign. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Lessons from youth digital ministry can inform adult services and broader church mobile strategy when they are translated into repeatable Rock-backed workflows. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| More |  | 29 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->









































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `10`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Episode 40: v8 and more team updates Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) | approved_for_public_distillation | 3 | media-insight:6e8d02135da566a7 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) | approved_for_public_distillation | 3 | media-insight:0a89bf5f60ad43fb |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) | approved_for_public_distillation | 6 | media-insight:392aedce4cf2d99c |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) | approved_for_public_distillation | 3 | media-insight:4634d7d6cd38df2c |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) | approved_for_public_distillation | 3 | media-insight:a5cb300eafd257ca |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) | approved_for_public_distillation | 3 | media-insight:a8361b8714eb62ff |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPb9Y9lR4) | approved_for_public_distillation | 3 | media-insight:c664b64e781d5fbb |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) | approved_for_public_distillation | 5 | media-insight:d1eb1a265dd0762b |
| More |  | 2 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->























## 20. Source Map And Dependency Notes

### Highest-Authority Source Links In This Pack

- RockU Groups track pages provide training landmarks for group configuration, attendance, requirements, security, scheduling, RSVP, roster, and analytics: [Group Types](https://community.rockrms.com/rocku/groups/group-types), [Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements), [Group Security](https://community.rockrms.com/rocku/groups/group-security), [Group Scheduling - Overview](https://community.rockrms.com/rocku/groups/group-scheduling-overview), [Person Preferences and Auto Schedule](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule), [Group Scheduling - Analytics](https://community.rockrms.com/rocku/groups/group-scheduling-analytics), [Group Scheduling Roster and Communications](https://community.rockrms.com/rocku/groups/group-scheduling-roster-and-communications).
- Official check-in documentation anchors group type inheritance, group location, schedule, kiosk visibility, roster filtering, and check-in security caveats: [Checking-out Check-in](https://community.rockrms.com/documentation/bookcontent/10/266).
- Release notes provide version caveats for scheduling confirmations, attendance reminders, and check-in scheduled times: [Rock Core Release Notes](https://www.rockrms.com/releasenotes).
- Mobile developer docs provide Schedule Toolbox behavior and customization landmarks: [Schedule Toolbox](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-toolbox).
- Rock source code provides entity and view-model landmarks: [ToolboxScheduleRowConfirmationStatus.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs), [GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs), [vCheckin_GroupTypeAttendance.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/database/Views/vCheckin_GroupTypeAttendance.sql), [GroupLocationsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/CheckIn/Configuration/CheckInScheduleBuilder/GroupLocationsBag.cs), [View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql).

### Community Example Sources

Community sources are useful operational examples but should be reviewed for security, performance, version fit, and local policy:

- External serving schedule page pattern: [View Serving Schedule on External Page](https://community.rockrms.com/recipes/459).
- Fifth-week schedule template pattern: [Group Member Schedule Templates](https://community.rockrms.com/recipes/356).
- Volunteer preference filtering pattern: [Find & Filter for Volunteers by Schedule Preference](https://community.rockrms.com/recipes/238).
- Dynamic sender pattern for scheduling confirmations: [Dynamic Sender for Group Scheduling Confirmations](https://community.rockrms.com/recipes/530).
- Serving interest workflow pattern: [Serving Interest Process](https://community.rockrms.com/recipes/169).
- Family serving response customization pattern: [Manage Family Members' Serving Requests on MyAccount](https://community.rockrms.com/recipes/489).
- Attendance save feedback pattern: [Enhancing the Obsidian Group Attendance Detail Block with a Toast Confirmation](https://community.rockrms.com/recipes/461).
- Campus/service sign-up finder scoping example: [Sign-Up Registration - Limit to particular schedule / campus](https://community.rockrms.com/ask/using/2808).

### Dependency Notes

Serving and volunteer operations depend on these topics:

- **Groups:** group types, groups, roles, members, inheritance, requirements, security.
- **Scheduling:** schedule preferences, group scheduler, confirmations, RSVP, auto-schedule, status board.
- **Locations:** group locations, location paths, campus-specific service contexts.
- **Check-In:** kiosk visibility, check-in groups, schedule activation, attendance, roster filtering.
- **Communications:** system communications, reminders, response emails, coordinator sender logic.
- **Workflows:** interest intake, application, background check, observation, family response, follow-up.
- **People:** aliases, family relationships, contact information, communication preferences, age/grade.
- **Security:** page/block access, group security, attendance deletion, requirement visibility, family authorization.
- **Reporting:** attendance facts, group scheduling analytics, no-show reporting, requirement compliance.

### Live Verification Required

The source pack is not sufficient to determine any specific church's live behavior for:

- exact group type settings;
- exact requirement enforcement;
- exact attendance columns and enum storage in the deployed version;
- exact workflow actions;
- exact system communication ids;
- exact page/block settings;
- exact security rules;
- exact group hierarchy;
- exact schedule recurrence;
- exact check-in kiosk configuration;
- exact external page exposure.

When performing real Rock work, inspect the live instance first, then use this guide to choose the right branch and source landmarks.
