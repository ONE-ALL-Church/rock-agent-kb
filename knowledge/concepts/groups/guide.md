---
id: authored-groups
title: Groups
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Groups

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Groups index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Groups are one of Rock RMS's core relationship and operational structures. A Rock group can represent a family, small group, serving team, class, room, coaching layer, check-in destination, security role, synced audience, or administrative folder. Do not treat "group" as a single ministry concept. Treat it as a configurable entity whose behavior is mostly inherited from its Group Type and then refined by the group record, member roles, locations, schedules, attributes, security, and related blocks.

For agent work, the first question is never "what is this group called?" The first question is "what Group Type controls this group, and what does that type allow?" Group Type configuration determines allowed child group types, roles, location behavior, whether attendance is taken, schedule behavior, group member attributes, requirements, workflows, sync behavior, and security assumptions. The official Rock Your Groups documentation places Group Type administration under `Admin Tools > Settings > General > Group Types` in newer navigation wording, with older references using `Admin Tools > General Settings > Group Types` for the same administrative area ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7), [Rock Your Groups v16 record](https://community.rockrms.com/documentation/bookcontent/7/296)).

The most reliable investigation path is:

1. Identify the exact `Group.Id`, `Group.Guid`, `GroupTypeId`, parent group, active/archive status, and campus.
2. Inspect the Group Type and inherited Group Type settings.
3. Inspect roles and current group members, including status, role, and member attributes.
4. Inspect group locations, schedules, and schedule exclusions.
5. Inspect attendance occurrences and attendance rows if the problem is reporting, reminders, or engagement.
6. Inspect security at the page, block, Group Type, group, and role/member-management layers.
7. Inspect version-specific behavior before assuming a block is wrong, especially Group Placement, Attendance Analytics, Group Scheduler, and Group Member Requirements.

RockU's Groups training catalog covers Group Viewer, Group Details, Group Attendance, Group Types, Group Type Inheritance, Group History, Group Location, Group Purposes, Alternate Placements, Group Requirements, Group Security, Extending Groups, Group Scheduling, RSVP, roster/communications, and Group Placement ([RockU Groups](https://community.rockrms.com/rocku/groups)). Use that training catalog as a topic map, but use official docs, source-code landmarks, Model Map records, and live instance inspection for operational certainty.

## 2. Scope And Terminology

This guide covers the Groups concept family: group types, groups, group members, group member roles, group hierarchy, group locations, schedules, attendance, group finder, group placement, scheduling, RSVP, group requirements, group workflows, security, reporting, and developer-facing landmarks.

Core terms:

- **Group**: A Rock entity representing a set of people or a container for other groups. It is governed by `GroupTypeId`, may have a parent group, may have locations and schedules, and may contain `GroupMember` rows.
- **Group Type**: The configuration template for groups. It controls hierarchy, roles, attendance behavior, schedule options, location options, member attributes, workflows, requirements, and other behavior. Model Map records `Group Type` as a Group-category model ([Model Map](https://community.rockrms.com/ModelMap)).
- **Group Type Role**: A role definition available to members of groups of a given type. Examples include Leader, Member, Host, Coach, Volunteer, or ministry-specific roles. Model Map records `Group Type Role` as a Group-category model ([Model Map](https://community.rockrms.com/ModelMap)).
- **Group Member**: A relationship row connecting a person to a group with a role, status, optional attributes, and historical/attendance-related behavior. Model Map records `Group Member` as a Group-category model ([Model Map](https://community.rockrms.com/ModelMap)).
- **Group Member Status**: The member's state in the group, commonly Active, Inactive, or Pending. Exact enum values and labels should be verified in the target Rock version and UI.
- **Group Location**: A relationship between a group and a location. A group may have one or more locations, and schedules can be tied through `GroupLocationSchedule`.
- **Schedule**: A time recurrence or schedule definition connected to group meeting or serving behavior. Schedules are configured under the Schedules administration area and may be selected by group types or groups ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Attendance Occurrence**: A meeting/occurrence record, normally connected to a group, location, schedule, and date, with individual attendance rows under it.
- **Group Finder**: A public or mobile search experience for groups by campus, day, time, location, and attributes. The mobile developer record notes filtering by campus, day of week, time of day, location, and custom attributes, and warns that returned groups do not automatically account for user security ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).
- **Group Placement**: A tool for assigning people into groups. Rock 18.1 documentation notes flexible placement from Group Viewer or standalone block with drag-and-drop, multi-select, and URL query string support ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Group Scheduling**: Volunteer/team scheduling behavior, including scheduler, status board, person preferences, auto-schedule, roster, communications, and analytics. RockU lists a dedicated sequence for these topics ([RockU Groups](https://community.rockrms.com/rocku/groups)).
- **Group Requirement**: A requirement attached to group membership, often used for eligibility, forms, checks, training, signature documents, or safety processes. Model Map records `Group Member Requirement` as a Group-category model ([Model Map](https://community.rockrms.com/ModelMap)).
- **Group Sync**: A configuration pattern where group membership can be driven by a Data View or similar source. Community recipes show this being used for communication audiences and automated email cohorts, but such recipes should be treated as examples, not official implementation requirements ([Send Emails to People in a DataView using a GroupSync Welcome Email](https://community.rockrms.com/recipes/124)).

This guide intentionally depends on the related topics of People, Attendance, Security, Locations, and Schedules. A groups issue often cannot be solved by looking only at the group row.

## 3. Groups Mental Model

A Rock group is best understood as an operational node in a typed tree.

The tree part matters because groups can have parent/child relationships. The type part matters because Group Type settings control which child types are allowed. Official documentation describes both structured hierarchies and flexible hierarchies. In a structured hierarchy, a leadership type can allow coach groups, which can allow small groups, while small groups allow no further child types. In a flexible hierarchy, a type such as Serving Teams can allow child groups of its own type, supporting an open-ended structure ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).

For agents, this produces a practical rule: when a group cannot be created under another group, do not start with permissions alone. Inspect the parent group's Group Type and its allowed child group type associations. Source-code snippets also reflect this structure: a Rock SQL archive view flattens `GroupTypeAssociation` to understand group type hierarchy and then joins groups, group types, locations, and schedules ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).

Groups are not just rosters. They can simultaneously provide:

- Membership: who belongs and in what role.
- Structure: parent/child ministry organization.
- Eligibility: requirements and member statuses.
- Security: access groups, management rights, and role-scoped behavior.
- Attendance: occurrence creation, reminders, and participation tracking.
- Scheduling: volunteer assignments, preferences, RSVP, cancellations, and status views.
- Search/discovery: group finder listings and registration paths.
- Automation: group member workflow triggers, sync, communications, and reporting.
- Content context: leader toolbox content, group-specific resources, notes, and attributes.

The most important implementation insight is that most behavior is not stored directly on the `Group` row alone. It is spread across `GroupType`, `GroupTypeRole`, `Group`, `GroupMember`, `GroupLocation`, `GroupLocationSchedule`, `Schedule`, `Location`, `AttendanceOccurrence`, `Attendance`, attributes, security authorization rows, workflow triggers, and block settings. Any guide or agent recipe that inspects only `Group.Name` and `Group.Id` is not operationally complete.

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Official documentation and release notes** for intended product behavior and version caveats. The Rock Your Groups manual is the main official source for group administration, hierarchy, schedules, attendance, group finder, and placement ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). Release notes are authoritative for version-specific fixes and changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
2. **RockU training** for UI workflows and operational topics. The Groups catalog is useful for knowing which screens and concepts Rock expects administrators to understand ([RockU Groups](https://community.rockrms.com/rocku/groups)).
3. **Developer docs** for mobile blocks, parameters, settings, merge fields, and security warnings. Examples include Group Finder, Group Registration, Group Attendance Entry, Group Member View, Group Member Edit, Schedule Preference, and CRM Group Members ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder), [Group Registration mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration), [Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).
4. **Model Map records** for entity coverage and naming, especially when building queries or dependency maps ([Model Map](https://community.rockrms.com/ModelMap)).
5. **GitHub source-code snippets** for implementation paths and payload shapes. Use source-code snippets to confirm relationships, request bags, and block naming, not to infer all UI behavior.
6. **Community recipes and Q&A** for patterns and operational examples. Treat these as examples that may be useful but may not match best practices, security expectations, or the current Rock version. Recipe pages themselves include a community disclaimer that recipes are contributed and not reviewed or endorsed by the core team ([Bulk Group Member Mover](https://community.rockrms.com/recipes/519), [Find Circular Group Type References](https://community.rockrms.com/recipes/110)).

When source material is thin, verify in a live Rock instance. Specifically inspect the current Rock version, the relevant Group Type, the block settings on the exact page, and the data rows behind the behavior. Do not assume that an example from a recipe is safe for a production instance without reviewing performance, permissions, current schema, and ministry fit.

## 5. Core Configuration And Data Model

### Group Type Configuration

The Group Type is the primary control surface. The official docs identify administration under `Admin Tools > Settings > General > Group Types` in the newer wording ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). Older docs and recipes may say `Admin Tools > General Settings > Group Types`; agents should map both to the same concept in the target version.

Important Group Type configuration areas include:

- **General identity**: name, description, icon/category behavior, and whether the type is active.
- **Allowed Child Group Types**: the child types that may be created beneath groups of this type. This is the basis of the group tree.
- **Location Types**: the kinds of locations that can be assigned to groups of this type.
- **Location Selection Modes**: controls whether a group can choose named locations, enter addresses, select points, draw geo-fences, or select from group member addresses. Official docs list Named, Address, Point, Geo-fence, and Group Member Address as options ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Schedule behavior**: whether and how groups can have schedules. Docs distinguish named schedules from custom options and note that some schedule options cannot be used as Group Finder filters ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Schedule Exclusions**: date ranges at the Group Type level that can apply to schedules for groups of that type. Use these for ministry-wide breaks rather than editing every group schedule manually ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Attendance/Check-in settings**: whether groups take attendance, whether reminders are sent, and check-in-related behavior.
- **Roles**: roles available to group members, including default roles and leader roles.
- **Group Member Attributes**: custom fields for the relationship between person and group.
- **Group Attributes**: custom fields on the group itself.
- **Group Member Workflows / Workflow Triggers**: automation triggered by membership events, attendance events, placement, or status/role changes.
- **Requirements**: eligibility rules and workflows for members.
- **Inherited Group Type**: a way to inherit attributes from another group type. Official docs describe inheritance as useful when two types are similar but one needs additional attributes ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Print Using**: a check-in-adjacent setting that determines printer behavior, with official docs noting device printer versus location printer behavior and limited value outside check-in configuration ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).
- **Allow Group Sync**: a configuration used in Data View sync-style groups, based on community examples ([Send Emails to People in a DataView using a GroupSync Welcome Email](https://community.rockrms.com/recipes/124)).

If an agent is asked why a field is missing, why a child group type cannot be added, why attendance does not work, or why a group finder filter is absent, inspect Group Type configuration first.

### Core Entity Relationships

At a practical level:

- `GroupType` defines allowed behavior.
- `GroupTypeRole` defines member roles for a group type.
- `Group` points to `GroupType` and may point to a parent group.
- `GroupMember` points to `Group`, `Person`, and `GroupTypeRole`.
- `GroupLocation` connects `Group` and `Location`.
- `GroupLocationSchedule` connects a group-location pairing to `Schedule`.
- `AttendanceOccurrence` normally references group/location/schedule/date context.
- `Attendance` references the occurrence and the attending person's alias.
- `GroupMemberRequirement` tracks requirement-related state for group members.
- `GroupMemberWorkflowTrigger` defines automation around group member events.
- `GroupMemberScheduleTemplate` supports scheduling patterns.

The source pack includes Model Map entries for `Group Member`, `Group Member Assignment`, `Group Member Historical`, `Group Member Requirement`, `Group Member Schedule Template`, `Group Member Workflow Trigger`, `Group Type`, and `Group Type Role` ([Model Map](https://community.rockrms.com/ModelMap)). Treat this as a model inventory, not a full schema definition. For field-level certainty, inspect the target Rock database schema, API endpoint metadata, source code, or the Model Map in the current instance.

### Locations And Schedules

Groups can be associated with locations and schedules. Source-code SQL examples join `Schedule` to `GroupLocationSchedule`, then to `GroupLocation`, `Group`, and `Location`, showing the operational path for schedule-to-group-location reporting ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)). The archived source snippet similarly joins groups, group types, locations, and schedules after flattening Group Type hierarchy ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).

For live troubleshooting, inspect:

- `Group.Id`, `Group.Guid`, `Group.Name`, `GroupTypeId`, `ParentGroupId`, `IsActive`, `IsArchived`.
- `GroupLocation.GroupId`, `LocationId`.
- `GroupLocationSchedule.GroupLocationId`, `ScheduleId`.
- `Schedule.Name`, start/end/frequency or iCalendar content.
- Group Type schedule options and schedule exclusions.

### Attributes

Attributes extend groups and members without schema changes. Group attributes store values on the group. Group member attributes store values on the membership relationship. The docs explain that Group Member Attributes are usually defined on the Group Type and then apply to members in groups of that type; they can also be added to a specific group when the configuration allows it and the user has appropriate administration access ([Rock Your Groups v16 record](https://community.rockrms.com/documentation/bookcontent/7/296)).

Attribute keys matter. Release notes mention Slingshot support for duplicate Attribute keys across different Group Types, allowing similar attributes to coexist if they belong to different group types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). For integrations, Lava, imports, and source control, verify whether an attribute is Group Type-scoped, group-specific, inherited, or duplicated across types.

## 6. Primary Entities And Relationships

### Group Type

`GroupType` is the configuration root. It defines the expected behavior for groups and often explains issues that appear to be group-specific.

Inspect Group Type when:

- A group cannot be added under a parent.
- A group cannot take attendance.
- A location mode is unavailable.
- Group Finder does not show a filter.
- A schedule option is unavailable.
- A member attribute is missing.
- A workflow does not fire.
- Requirements do not appear.
- A leader can view but not manage members.
- Group Type inheritance produces unexpected attributes.

The RockU catalog includes dedicated training for Group Types and Group Type Inheritance ([Group Types](https://community.rockrms.com/rocku/groups/group-types), [Group Type Inheritance](https://community.rockrms.com/rocku/groups/group-type-inheritance)). Use this as a signal that Group Type setup is central, not incidental.

### Group Type Association

Although administrators usually experience this as "Allowed Child Group Types," source snippets show the underlying concept as `GroupTypeAssociation` in a hierarchy query ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)). This is why a parent group type determines which child group types can appear underneath it.

Operational check:

- If the UI does not offer the desired child type, inspect the parent group's Group Type, not the child group.
- If a hierarchy loops or times out, inspect both allowed child type relationships and inherited group type relationships.
- If a report should include descendants, decide whether it should follow group parent hierarchy, group type allowed-child hierarchy, or both. These are different questions.

### Group

`Group` is the actual ministry/operational node. Important fields to verify in a live instance include:

- `Id`
- `Guid`
- `Name`
- `GroupTypeId`
- `ParentGroupId`
- `CampusId`
- `IsActive`
- `IsArchived`
- `GroupCapacity` and capacity rule behavior if the type uses capacity
- Attribute values
- Security authorization
- Group administrator or scheduler-related fields if scheduling is in scope

Archived and inactive groups can still matter. Release notes for Rock 18.3 mention a fix in Check-in where scheduled times should exclude schedules from archived or inactive groups that still have `GroupLocationSchedule` assigned ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If a schedule appears unexpectedly, check for stale group-location-schedule rows on inactive or archived groups.

### Group Member

`GroupMember` connects a person to a group. It is not just a list entry. It carries role, status, attributes, workflow triggers, requirement state, historical implications, and attendance context.

Inspect Group Member when:

- A person appears in a group but does not show in the expected roster.
- A person cannot be scheduled.
- A leader cannot manage a member.
- A member does not meet requirements.
- A pending member notification or activation flow is involved.
- Attendance reports count a person unexpectedly.
- A group placement operation did not move a person as expected.

The mobile Group Member View block uses `GroupMemberGuid` as a parameter and can expose group name, member count, selected member details, visible attributes, contact options, and edit access depending on configuration ([Group Member View mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-view)). The Group Member Edit mobile block also uses `GroupMemberGuid` and has settings such as allowing role change, status change, communication preference change, note edit, attribute category, member detail page, and delete behavior ([Group Member Edit mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-edit)).

### Group Type Role

Roles define relationship meaning and permissions implications. A "Leader" role is not the same as a "Member" role, and ministry-specific roles can affect scheduling, communications, and requirements.

Operational checks:

- Verify the role's `IsLeader` behavior.
- Verify default role.
- Verify whether role-specific security or management is configured.
- Verify whether workflows are filtered by role.
- Verify whether scheduling templates, assignments, or status board views group by role.

A workflow trigger source snippet notes that role qualifiers can be stored as `fromRoleGuid` and `toRoleGuid`, and that for some trigger types the UI label may use "With Role of" while still storing the value in the "to" slot ([groupTypeGroupMemberWorkflowTriggerBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupTypeDetail/groupTypeGroupMemberWorkflowTriggerBag.d.ts), [GroupTypeGroupMemberWorkflowTriggerBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs)). When debugging a workflow trigger, inspect the stored trigger type and from/to role/status fields rather than relying only on UI wording.

### Group Member Historical

Group history is a separate operational concern from current membership. Model Map includes `Group Member Historical` ([Model Map](https://community.rockrms.com/ModelMap)), and RockU includes Group History training ([Group History](https://community.rockrms.com/rocku/groups/group-history)). If a person was once in a group but is no longer active, reporting may need historical tables, audit details, or attendance rather than current `GroupMember`.

### Group Member Assignment

Model Map includes `Group Member Assignment` ([Model Map](https://community.rockrms.com/ModelMap)). Use this as a signal that scheduling/assignment can be distinct from membership. When a person is a group member but not appearing in schedule assignments, inspect assignment-related tables and scheduler block behavior, not only `GroupMember`.

### Group Member Requirement

Model Map includes `Group Member Requirement` ([Model Map](https://community.rockrms.com/ModelMap)). Release notes for Rock v19.1 mention an improved `GroupMemberRequirementState` property showing whether a requirement is met, met with warning, or not met ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). For versions before that behavior, inspect the target version and current requirement UI before assuming the state field exists.

## 7. Common Groups Workflows

### Create A New Group

Before creating a group:

1. Identify the parent group.
2. Inspect parent Group Type allowed child types.
3. Choose the correct child Group Type.
4. Confirm required roles and default role.
5. Confirm attendance and schedule expectations.
6. Confirm location mode.
7. Confirm whether the group should be active, archived, public, searchable, or hidden.
8. Confirm group attributes required by Group Finder, leader toolbox, scheduling, or reporting.

Community workflows like Mass Group Creator show bulk creation patterns, but they are contributed examples and should not replace a reviewed internal process ([Mass Group Creator](https://community.rockrms.com/recipes/144)). For production-scale group creation, use official UI, reviewed workflows, or migration scripts with rollback and audit plans.

### Add Or Move Group Members

A member add/move operation is more than inserting a row:

- Determine target group and role.
- Determine status: Active, Pending, or Inactive.
- Preserve or intentionally reset group member attributes.
- Check requirements.
- Check workflow triggers.
- Check history.
- Check scheduling assignments.
- Check attendance implications if reporting looks at current membership.
- Communicate with leaders if pending or active members affect roster workflows.

The Bulk Group Member Mover recipe illustrates a pattern where selected people are added to a destination group and removed from the old group, using workflows and Lava to pass old group, new group, and person context ([Bulk Group Member Mover](https://community.rockrms.com/recipes/519)). Treat it as a useful design example, not a universal script. For a live instance, verify role IDs, group IDs, workflow type IDs, permissions, and whether the ministry wants history preserved.

### Copy Or Clone Groups

A group copy may need:

- Group name and parent.
- Group Type.
- Group attributes.
- Member list or no member list.
- Group member attributes.
- Locations and schedules.
- Security.
- Requirements.
- Workflow triggers.
- Notes/content references.
- Capacity settings.

A community recipe describes copying a group and its attribute values for cases where many values should be reused ([Copy a Group and its Attribute Values](https://community.rockrms.com/recipes/143)). In production, decide whether copying attributes is appropriate. Some attributes are season-specific, leader-specific, registration-specific, or content-channel-specific and should not be blindly cloned.

### Archive Or Deactivate Groups

Archive/deactivate decisions affect UI, check-in, finder results, attendance, and reporting. Before archiving:

- Check whether the group has child groups.
- Check active group members.
- Check future schedule assignments.
- Check `GroupLocationSchedule` rows.
- Check active Group Finder results.
- Check communications and workflow dependencies.
- Check reports that filter only `IsActive` but not `IsArchived`, or vice versa.

The Rock 18.3 Check-in release note about excluding schedules from archived/inactive groups is a practical reminder: stale schedule relationships can remain even when a group is no longer operational ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Use Groups As Communication Audiences

Groups often act as communication cohorts. If using Group Sync or Data Views:

- Confirm Data View criteria.
- Confirm email preference filters.
- Confirm adult/minor filters.
- Confirm opt-in/consent and ministry policy.
- Confirm sync timing.
- Confirm whether group membership is informational or actionable.
- Do not mix "synced audience" groups into ministry hierarchies without clear naming and folder structure.

Community examples show Data View synced groups used for welcome or automated emails and recommend test Data Views before sending to large audiences ([Send Emails to People in a DataView using a GroupSync Welcome Email](https://community.rockrms.com/recipes/124), [Automate asking new givers to join a group](https://community.rockrms.com/recipes/136)).

## 8. Group Types Deep Dive

### Structured Versus Flexible Hierarchy

Official docs describe two broad hierarchy patterns: structured and flexible. Structured hierarchies enforce a known chain of types, such as leadership type to coach type to small group type. Flexible hierarchies let a type allow itself as a child type, supporting deep, variable trees ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).

Use structured hierarchy when:

- Ministry layers have clear responsibilities.
- Reporting depends on predictable levels.
- Group Finder should expose only leaf-level groups.
- Security differs by layer.
- Coaches or coordinators manage specific child groups.

Use flexible hierarchy when:

- Teams vary greatly by ministry.
- Departments need arbitrary nesting.
- The same type represents both containers and teams.
- The organization values adaptability more than strict reporting shape.

Operational warning: flexible hierarchy simplifies creation but complicates reporting and permissions. An agent building a report should not assume all children are ministry groups; some may be folders, coach groups, or administrative containers.

### Inherited Group Types

An inherited Group Type can receive attributes from another type. The official docs frame this as useful for similar group types where one needs additional attributes ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). Inheritance can reduce duplication, but it can also obscure why an attribute appears.

Troubleshooting inheritance:

- Inspect the Group Type's `InheritedGroupTypeId`.
- Inspect inherited attributes and local attributes separately.
- Verify whether duplicate keys exist across group types.
- Check for circular inheritance if pages time out or errors mention recursive behavior.

A community recipe describes circular inherited Group Type references as a possible cause of timeouts or cryptic errors and provides SQL patterns to find loops; it notes newer versions reduced this risk but did not eliminate every possibility ([Find Circular Group Type References](https://community.rockrms.com/recipes/110)). Use that as a troubleshooting concept, but verify with current schema and safe read-only SQL in the live instance.

### Roles

Roles are configured on the Group Type. A robust role plan defines:

- The default role for new members.
- Which role is considered leader.
- Whether multiple leader roles are needed.
- Whether role names need to match ministry language.
- Whether roles affect scheduling.
- Whether roles affect requirements.
- Whether roles affect workflow triggers.
- Whether roles should be shown publicly.

Do not use role names as the only source of behavior. Inspect role flags and IDs. In recipes, hard-coded role IDs appear in examples, but role IDs differ by instance and should always be verified live ([Bulk Group Member Mover](https://community.rockrms.com/recipes/519)).

### Group Attributes

Group attributes are useful for:

- Finder filters.
- Capacity metadata.
- Ministry categorization.
- Content-channel references.
- Leader toolbox configuration.
- Public descriptions.
- Registration options.
- RSVP or schedule behavior toggles.
- Workflow flags.

A community recipe shows adding a group attribute that points to a Content Channel so volunteer teams can access team-specific resources ([Adding Content/Resources for Volunteers to Group Scheduler](https://community.rockrms.com/recipes/334)). This pattern is useful because it keeps content association on the group rather than hard-coding group IDs in templates.

### Group Member Attributes

Group member attributes are useful for:

- Member-specific eligibility data.
- T-shirt size or onboarding data.
- Volunteer preferences.
- Cohort-specific notes.
- Ministry role metadata not covered by role.
- RSVP or registration answers.
- Training completion references.

The docs note Group Member Attributes are usually defined on the Group Type, and group-specific member attributes require appropriate configuration and administration access ([Rock Your Groups v16 record](https://community.rockrms.com/documentation/bookcontent/7/296)).

### Schedule Exclusions

Group Type schedule exclusions are the correct tool for broad group breaks. Rather than editing every small group's schedule for a two-week pause, configure the exclusion on the relevant Group Type so schedules of that type observe the break ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).

Source-code request bags for Group Type schedule exclusions model an exclusion with a unique identifier and date range ([groupTypeGroupScheduleExclusionBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupTypeDetail/groupTypeGroupScheduleExclusionBag.d.ts), [GroupTypeGroupScheduleExclusionBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs)). For live verification, inspect the Group Type schedule exclusion list and compare it to occurrence generation or block filtering for the relevant date.

### Group Capacity

Capacity is used heavily in Group Finder, placement, and registration contexts. Verify:

- Whether capacity is enabled.
- Whether the rule is hard, warning, or none.
- Which statuses count against capacity.
- Whether pending members count.
- Whether child groups or locations have separate capacity.
- Whether public registration prevents overcapacity.

The mobile Group Registration block includes a `Prevent Overcapacity Registrations` configuration item in the source pack headings ([Group Registration mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration)). For web Group Finder or registration, inspect the exact block settings in the target instance.

## 9. Group Finder Deep Dive

Group Finder is a search and discovery surface, not merely a list of active groups. It depends on group type, group status, location, schedules, attributes, campus, block settings, template logic, and security handling.

The mobile Group Finder developer documentation states that the block can search by campus, day of week, time of day, location, and custom attributes. It also includes an important security note: returned groups matching filters do not account for user security automatically, so templates should use `HasRightsToLava` where needed to check view permissions ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

### Finder Data Inputs

Inspect these inputs:

- Group Type(s) selected by the block.
- Campus context setting.
- Whether campus context is enabled.
- Group attributes selected as filters.
- Location radius/distance behavior.
- Schedules and whether they are named or custom.
- Whether results load immediately or only after filtering.
- Detail page setting.
- Registration page or detail-page handoff.
- Template logic.
- Security filtering in the template.
- Active/archive filters.

Mobile Group Finder has a `LoadResults=true` query string behavior that bypasses the filter and shows results immediately ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)). If an agent sees results on one URL but not another, inspect query strings before assuming data changed.

### Finder And Schedules

Official docs note that some schedule options, such as Custom or certain named schedule configurations, cannot be used as Group Finder filters ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). If day/time filters are not available or not working:

1. Inspect Group Type schedule options.
2. Inspect each group's schedules.
3. Inspect whether schedules are named or custom.
4. Inspect schedule exclusions.
5. Inspect the block's selected filters and template.
6. Inspect whether the mobile block or web block has different behavior.

### Finder And Locations

Location selection modes influence what data exists for Finder. Named locations, addresses, points, geo-fences, and member addresses support different search experiences ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). If map results are wrong:

- Verify `GroupLocation` exists.
- Verify `Location` has coordinates where needed.
- Verify the group type permits the location mode used.
- Verify campus and location hierarchy.
- Verify geocoding and Google API keys if the template uses maps.
- Verify radius/distance configuration.
- Verify whether member addresses are intended to be exposed.

### Finder And Security

Do not expose groups through Finder just because they match filters. The mobile developer warning is explicit that returned groups do not automatically account for user security, and templates should use a rights check as needed ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

Security troubleshooting:

- Check page permissions.
- Check block permissions.
- Check group type security.
- Check group-specific security.
- Check template use of rights filters.
- Check whether unauthenticated users can reach detail or registration pages.
- Check whether private addresses, leader phone numbers, or member data render in public templates.

### Finder Share Links

A community recipe describes a Post-HTML script that updates URL parameters as users select Group Finder filters so pre-filtered links can be shared ([Group Finder Share Filter](https://community.rockrms.com/recipes/374)). This is a useful pattern, especially for ministry campaigns, but it is not core behavior in every block/version. If asked for shareable finder URLs, inspect current block support first, then consider a reviewed client-side enhancement.

### Finder Registration Handoff

The mobile Group Registration block accepts `GroupGuid` as a page parameter and can limit registration to configured group type GUIDs. It also supports configuration for group member status, registration workflow, family options, phone/email behavior, connection status, record status, result page, completion message, overcapacity prevention, autofill, and button text ([Group Registration mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration)).

For public registration:

- Verify Group Type GUID allowlist.
- Verify the resulting Group Member status.
- Verify whether registration starts a workflow.
- Verify family member behavior.
- Verify person creation settings.
- Verify capacity behavior.
- Verify duplicate registration handling.
- Verify whether registration writes active or pending members.
- Verify leader notification flow.

## 10. Group Attendance Deep Dive

Group attendance connects groups to recurring ministry participation. It is used by small groups, serving teams, watch parties, check-in configurations, leader toolbox, reporting, engagement workflows, and pastoral care.

RockU includes Group Attendance in the Groups training sequence ([Group Attendance](https://community.rockrms.com/rocku/groups/group-attendance)). The official docs include group attendance and reminders in the groups manual updates ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).

### Attendance Configuration

For a group to take attendance reliably, inspect:

- Group Type `Takes Attendance` setting.
- Attendance reminder setting.
- Group schedule option.
- Group's location and schedule.
- Whether the group has active members.
- Whether attendance is entered from internal UI, external toolbox, email, mobile app, check-in, or workflow.
- Attendance occurrence creation behavior.
- Whether attendance can be entered for past/future dates.

A community watch-party example configured a Group Type with `Takes Attendance: Yes`, `Send Attendance Reminder: Yes`, and named schedule options, using workflows and metrics to track non-individual attendance counts ([Watch Party Attendance](https://community.rockrms.com/recipes/197)). That pattern is useful when attendance is conceptual or aggregate, but standard Rock attendance normally tracks individual attendance rows.

### Attendance Occurrence And Attendance Rows

Operationally, attendance reporting usually involves:

- `AttendanceOccurrence.GroupId`
- `AttendanceOccurrence.LocationId`
- `AttendanceOccurrence.ScheduleId`
- `AttendanceOccurrence.OccurrenceDate`
- `AttendanceOccurrence.DidNotOccur`
- `AttendanceOccurrence.Notes`
- `Attendance.OccurrenceId`
- `Attendance.PersonAliasId`
- `Attendance.DidAttend`
- `Attendance.StartDateTime`

A workflow source snippet for `PersonGetGroupTypeAttendance` queries attendance where `a.Occurrence.Group.GroupTypeId == groupType.Id`, person alias matches the person, and `DidAttend == true`, then orders by `StartDateTime` to find the last attended record ([PersonGetGroupTypeAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PersonGetGroupTypeAttendance.cs)). This confirms the common pattern: attendance is tied to a person through `PersonAlias` and to group context through occurrence.

### Mobile Attendance Entry

The mobile Group Attendance Entry block displays a list of group members to mark attendance for a specified date. The developer documentation includes an important distinction: unlike web, mobile groups must have a schedule configured to use this block. It takes `GroupGuid` and has settings for days forward/back, save redirect page, and whether to show a save button ([Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).

If mobile attendance fails:

1. Verify the group has a schedule.
2. Verify `GroupGuid` is passed correctly.
3. Verify the group takes attendance.
4. Verify days-forward/days-back settings.
5. Verify the user can view/manage the group.
6. Verify members have visible/eligible statuses.
7. Verify the save endpoint is reachable.
8. Verify app deployment and block settings.

Source-code request bags for the Obsidian Group Attendance Detail block include `groupGuid`, `locationGuid`, and `date` for schedule lookup ([groupAttendanceDetailGetGroupLocationSchedulesRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupAttendanceDetail/groupAttendanceDetailGetGroupLocationSchedulesRequestBag.d.ts), [GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs)). Another request bag includes `numberOfPreviousDaysToShow` and occurrence date context ([groupAttendanceDetailGetGroupLocationScheduleDatesRequestBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Group/GroupAttendanceDetail/groupAttendanceDetailGetGroupLocationScheduleDatesRequestBag.d.ts)).

### Attendance UX And Confirmation

A community recipe describes adding a toast confirmation to the Obsidian Group Attendance Detail block because real-time saves could be unclear to leaders; it listens for successful or unsuccessful posts to a MarkAttendance endpoint ([Enhancing the Obsidian Group Attendance Detail Block with a Toast Confirmation](https://community.rockrms.com/recipes/461)). This is a good example of an operational issue that is not data failure: leaders may think attendance did not save even when it did. Before altering code, inspect current block version, whether Rock has added confirmation behavior, and whether users are trained.

### Attendance Reporting

A community report recipe calculates attendance percentages by group and date range and includes notes as hoverable context ([Powerful Small Group Attendance Report](https://community.rockrms.com/recipes/209)). Treat the idea as useful: attendance percentage requires both attended count and active member count, plus clear handling for did-not-occur and notes. Do not copy old SQL directly into a current instance without reviewing schema, performance, and group type filters.

For reporting, define:

- Which groups are in scope.
- Whether child groups are included recursively.
- Which member statuses count in denominator.
- Which roles count.
- Whether leaders count.
- Whether pending members count.
- Whether `DidNotOccur` is excluded or shown.
- Whether attendance notes are included.
- Whether attendance is by occurrence date or start date/time.
- Whether attendance from check-in and group leader entry are both included.
- Whether archived/inactive groups are excluded.

Release notes for Rock 18.3 fixed an issue where the Attendance Analytics block included groups whose Group Type was only an allowed child type of a selected Group Type, rather than being directly selected in block settings ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If analytics counts look inflated or different across versions, inspect the Rock version and selected group types.

## 11. Related Rock Areas: People, Attendance, Security, Locations, Schedules

### People

Groups are person relationships. Every group member investigation eventually touches Person and PersonAlias. Check:

- Person record status.
- Connection status.
- Age classification.
- Family group.
- Primary alias.
- Communication preferences.
- Email/SMS availability.
- Security role membership.
- Duplicate records.

The mobile CRM Group Members block is designed to display other members in a configured group type for a person from context, with family as the main use case. It requires person context and can auto-create a group depending on configuration ([Group Members mobile CRM block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)). This is a reminder that family is also a group pattern in Rock.

### Attendance

Attendance has its own model and reporting logic. For groups, attendance is usually group occurrence-based. For check-in, attendance may be generated through check-in workflows and room/location schedules. Do not mix these without verifying occurrence source.

### Security

Group security can be layered:

- Page view/edit/admin rights.
- Block rights.
- Group Type rights.
- Group-specific rights.
- Group member role security.
- Leader toolbox access.
- Security groups used elsewhere in Rock.
- API/mobile permissions.
- Template-level rights checks.

RockU includes a dedicated Group Security session ([Group Security](https://community.rockrms.com/rocku/groups/group-security)). The mobile Group Finder doc's warning about result security is one of the most important practical security notes in the source pack ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

### Locations

Locations can be named, addresses, map points, geo-fences, or group member addresses, depending on Group Type selection mode ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). For check-in or room-based groups, location hierarchy and active status are critical. A source SQL tool populates locations and connects serving team groups to locations and schedules, with room/building/campus location type values ([Populate_LocationsAndGroupSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_LocationsAndGroupSchedules.sql)).

### Schedules

Schedules may be shared named schedules or custom schedules. Group scheduling and attendance both depend on schedule configuration, but not always the same way. Group Member Schedule Templates are separate scheduling patterns used for volunteer auto-scheduling.

The Web Forms Group Member Schedule Template Detail block saves a template name and `Schedule.iCalendarContent` from a schedule builder ([GroupMemberScheduleTemplateDetail.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/GroupScheduling/GroupMemberScheduleTemplateDetail.ascx.cs)). A newer Obsidian list block queries `GroupMemberScheduleTemplate` and orders by name ([GroupMemberScheduleTemplateList.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Group/Scheduling/GroupMemberScheduleTemplateList.cs)).

## 12. Administration And Operational Guardrails

### Naming And Hierarchy

Use names that distinguish folders, coach groups, small groups, serving teams, synced groups, security groups, and temporary groups. Avoid using only a ministry name when the group is a container. Good group tree hygiene prevents reporting errors.

This naming recommendation follows Rock's documented distinction between structured and flexible group hierarchies: names should make the operational role of each node clear when the hierarchy itself permits several kinds of child groups ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)).

Recommended naming checks:

- Does the group name identify its ministry or campus?
- Does a folder/container look different from a meeting group?
- Are coach groups clearly named?
- Are archived groups hidden from operational views?
- Are seasonal groups named with season/year?
- Are synced groups stored under a clear folder?

### Avoid Hard-Coded IDs In Long-Lived Templates

Recipes often use Group Type IDs, Page IDs, Role IDs, Workflow Type IDs, and Note Type IDs. Those are instance-specific. When adapting patterns:

- Prefer GUIDs where stable and appropriate.
- Document every ID.
- Add comments in Lava or block settings where maintainers will see them.
- Create a validation checklist.
- Store decisions in an implementation note.

### Use Read-Only Investigation First

For production investigations:

1. Inspect current state.
2. Confirm source of behavior.
3. Identify the smallest safe change.
4. Test in non-production or with a narrow scope.
5. Apply change.
6. Verify UI, data, and downstream reports.

Do not bulk move, bulk archive, or mass sync groups without proof of target records.

### Recipe Guardrails

Community recipes are valuable because they show real ministry patterns, but the recipe pages warn that they are contributed and not reviewed or endorsed by the Rock core team ([Bulk Group Member Mover](https://community.rockrms.com/recipes/519), [Schedule Cancellation Workflow](https://community.rockrms.com/recipes/481)). For each recipe-derived solution, verify:

- Rock version compatibility.
- Security.
- Performance.
- Hard-coded IDs.
- Lava commands enabled.
- SQL access.
- Workflow permissions.
- Person token handling.
- Communication consent.
- Logging and rollback.

### Group Type Change Guardrail

Changing a group's Group Type can be risky because roles, attributes, allowed children, requirements, attendance, and finder behavior may all change. A Rock Shop plugin called Group Type Change Tool exists to change a group's type while mapping roles and attributes, with required Rock version 6.0 listed in the source record ([Group Type Change Tool](https://www.rockrms.com/rockshop/plugin/53)). Before using any tool:

- Back up or export current group, members, roles, attributes, and child groups.
- Map old roles to new roles.
- Map old attributes to new attributes.
- Verify group member attributes.
- Verify child type compatibility.
- Verify security.
- Test with one non-critical group.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Mobile Blocks

Group-related mobile blocks in the source pack include:

- **Group Finder**: searches groups by campus, day, time, location, and custom attributes; includes `LoadResults=true`; exposes merge fields such as `DetailPage`, `Groups`, and `Distances`; warns about security filtering ([Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).
- **Group Registration**: registers a person for a group using `GroupGuid`; supports group member status, group type GUID allowlist, registration workflow, family options, contact fields, connection/record status, result page, completion message, overcapacity prevention, autofill, and button text ([Group Registration mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration)).
- **Group Attendance Entry**: marks attendance for a group using `GroupGuid`; mobile requires a configured group schedule; has days-forward/back and save-button behavior ([Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).
- **Group Member View**: views a specific member using `GroupMemberGuid`; exposes allowed actions, member details, attributes, and contact options ([Group Member View mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-view)).
- **Group Member Edit**: edits role, status, communication preference, note, attributes, and delete/navigation behavior depending on settings ([Group Member Edit mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-edit)).
- **Schedule Preference**: lets individuals set group scheduling preferences; introduced in mobile/core version context `M v4.0 C v13.3` in the source record ([Schedule Preference mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-preference)).
- **CRM Group Members**: displays other members in a configured Group Type for a person context, commonly family members; source record marks `M v5.0 C v15.2` ([Group Members mobile CRM block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)).

### Request Bags And Block Paths

Useful source-code landmarks:

- `Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs` models group/location/date input for schedule lookup ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs)).
- `Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationScheduleDatesRequestBag.cs` models group/location, previous days, and occurrence date context ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationScheduleDatesRequestBag.cs)).
- `Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs` models workflow trigger type, role/status qualifiers, first-attendance behavior, and placement note behavior ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs)).
- `Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs` models Group Type schedule exclusion ranges ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupScheduleExclusionBag.cs)).
- `Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs` models group name plus ordered location/schedule labels for the scheduler ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs)).
- `Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs` models available and selected locations for scheduler filtering ([source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerLocationsBag.cs)).

### Lava Landmarks

Lava commonly appears in:

- Group Detail Lava / leader toolbox templates.
- Group Finder templates.
- HTML blocks on custom group pages.
- Dynamic Data blocks.
- Workflow actions.
- Shortcodes.
- Emails and notifications.

Community examples show Lava used to list a person's groups, render content channels, activate workflows, display group health, query attendance, and extend leader toolbox tabs ([Adding Content/Resources for Volunteers to Group Scheduler](https://community.rockrms.com/recipes/334), [Improving Rock's Group Coaching](https://community.rockrms.com/recipes/217), [Extending the Group Toolbox](https://community.rockrms.com/recipes/329), [Lava shortcode to show last group attendance](https://community.rockrms.com/recipes/290)).

Agent rule: when editing Lava, identify the merge fields available in that block. Do not assume `Group`, `CurrentPerson`, `Person`, `AllowedActions`, or `PageParameter` exist unless the block documentation or live debug confirms it.

### API And SQL Landmarks

For API or SQL work:

- Prefer API/service-layer operations for writes.
- For read-only audits, SQL can clarify relationships quickly.
- Avoid direct SQL writes unless explicitly approved and fully reviewed.
- Use `Guid` when building stable links or integrations.
- Use `Id` for internal joins and verified local queries.
- Use `PersonAlias` when querying attendance.

Source-code/reporting snippets confirm common joins:

- `Schedule -> GroupLocationSchedule -> GroupLocation -> Group -> Location` ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql)).
- `GroupTypeAssociation` hierarchy plus group/location/schedule reporting ([View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)).
- `Attendance -> AttendanceOccurrence -> Group -> GroupType` plus `PersonAlias -> Person` for group type attendance ([PersonGetGroupTypeAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PersonGetGroupTypeAttendance.cs)).

## 14. Reporting, Analytics, And Model Map

### Reporting Questions To Define

Before building any groups report, define:

- Are we reporting on groups, people, group members, attendance, or schedules?
- Is the report scoped by Group Type, parent group, campus, role, status, location, schedule, or attribute?
- Are archived groups included?
- Are inactive groups included?
- Are pending members included?
- Are leaders included?
- Are child groups recursive?
- Is the reporting period based on occurrence date, attendance start date, or schedule date?
- Are did-not-occur rows included?
- Are notes included?
- Is this report for staff, leaders, public users, or automation?

These questions correspond to materially different join paths in Rock source: schedule reporting follows `Schedule -> GroupLocationSchedule -> GroupLocation`, hierarchy reporting includes `GroupTypeAssociation`, and attendance reporting traverses occurrences and person aliases ([View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql), [View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql), [PersonGetGroupTypeAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PersonGetGroupTypeAttendance.cs)).

### Model Map Coverage

Model Map records in the source pack identify these Group-category models:

- Group Member ([Model Map](https://community.rockrms.com/ModelMap))
- Group Member Assignment ([Model Map](https://community.rockrms.com/ModelMap))
- Group Member Historical ([Model Map](https://community.rockrms.com/ModelMap))
- Group Member Requirement ([Model Map](https://community.rockrms.com/ModelMap))
- Group Member Schedule Template ([Model Map](https://community.rockrms.com/ModelMap))
- Group Member Workflow Trigger ([Model Map](https://community.rockrms.com/ModelMap))
- Group Type ([Model Map](https://community.rockrms.com/ModelMap))
- Group Type Role ([Model Map](https://community.rockrms.com/ModelMap))

Use Model Map to identify likely entity names, then verify fields in the live instance or source code.

### Data Filters

A source-code data filter named `GroupMemberGroupTypeFilter` applies to `Rock.Model.GroupMember` and filters group members based on their group type ([GroupMemberGroupTypeFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/GroupMembers/GroupMemberGroupTypeFilter.cs)). This matters because reports may be person-based, group-member-based, or attendance-based. Choosing the wrong entity base changes available filters and count semantics.

### Attendance Analytics Caveat

Rock 18.3 fixed Attendance Analytics so it includes only groups whose Group Types are directly selected in block settings, rather than also including allowed child group types of selected types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If comparing analytics before and after upgrade, this change can alter counts. Inspect block settings and version before treating it as a data quality issue.

## 15. Version And Release Caveats

### Navigation Wording

Official docs may refer to `Admin Tools > Settings > General` while older docs and recipes may refer to `Admin Tools > General Settings`. Agents should not treat this as a contradiction; verify the navigation in the target Rock version.

### Rock 16

The source pack includes a Rock Your Groups record for Rock 16.0/16.7 noting individual groups can be manually synced on demand and Group Scheduler search can help find people when making assignments ([Rock Your Groups v16 record](https://community.rockrms.com/documentation/bookcontent/7/296)). If working in v16-era instances, confirm manual sync and scheduler search behavior in the UI.

### Rock 18.1

Rock Your Groups notes Group Placement updates for Rock 18.1: flexible tool access from Group Viewer or standalone block, drag-and-drop, multi-select, and URL query strings for streamlined group management ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7)). If a user expects these placement features, verify the instance is on the relevant version and that the block is the updated one.

### Rock 18.3

Release notes include:

- Attendance Analytics fix for selected Group Types versus allowed child Group Types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Check-in scheduled times list excludes schedules from archived/inactive groups with assigned group-location schedules ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Slingshot support for duplicate Attribute keys across different Group Types ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Removal of deprecated `GroupLocationHistoricalSchedule` table/model ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- Improved Group Placement with multi-select, advanced filtering, and sorting ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Rock 19.1 Beta Context

Release notes retrieved in the source pack list Rock v19.1 as released May 20, 2026 and currently in beta. Group v19.1 notes improved Group Member Requirements with `GroupMemberRequirementState`, and Group Scheduler improvements that keep occurrence date and schedules fixed while scrolling and show group names above locations ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Treat beta behavior as version-specific. Verify whether the production instance is on stable, alpha, beta, or a patched build before relying on these features.

### Mobile/Core Version Markers

Developer docs include mobile/core version markers for some blocks, such as Schedule Preference `M v4.0 C v13.3` and CRM Group Members `M v5.0 C v15.2` ([Schedule Preference mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-preference), [Group Members mobile CRM block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members)). Verify app shell version, Rock core version, and deployed mobile block availability.

## 16. Implementation Playbooks

### Playbook: Build A Small Group Structure

1. Define ministry hierarchy: top-level folder, coach layer, small group layer.
2. Create or verify Group Types:
   - Small Group Leadership or folder type.
   - Coach group type.
   - Small Group type.
3. Configure allowed child group types so the hierarchy is enforced.
4. Configure Small Group roles: Leader, Member, optional Co-Leader.
5. Configure location modes: address, named, or group member address depending on public finder needs.
6. Configure schedule options so Group Finder filters work as intended.
7. Configure attendance and reminders if leaders will report attendance.
8. Configure group attributes for public finder filters, capacity, childcare, topic, season, or campus.
9. Configure group member attributes only if membership-specific data is needed.
10. Configure security and leader toolbox access.
11. Configure Group Finder block and detail/registration pages.
12. Test with a public user, authenticated leader, and staff user.
13. Verify reporting counts and attendance entry.

### Playbook: Build A Serving Team Scheduling Structure

1. Define serving team hierarchy and whether flexible self-child hierarchy is needed.
2. Configure Serving Team Group Type roles.
3. Configure locations and schedules.
4. Configure Group Member Schedule Templates if auto-scheduling will be used.
5. Configure person schedule preference surfaces.
6. Configure group scheduler and status board.
7. Configure RSVP and cancellation workflows only after team communication policy is clear.
8. Configure group administrator/scheduler owner.
9. Verify future assignments, decline behavior, and communications.
10. Test a full cycle: preference set, auto-schedule, RSVP, decline, replacement, attendance.

RockU includes training for Group Scheduling overview, meeting details, scheduler/status board, person preferences/auto-schedule, analytics, RSVP, email requests, responses, roster, and communications ([RockU Groups](https://community.rockrms.com/rocku/groups)).

### Playbook: Set Up Group Finder

1. Confirm target Group Type(s).
2. Confirm groups are active and not archived.
3. Confirm schedules are filterable.
4. Confirm locations are geocoded or otherwise usable.
5. Configure campus context.
6. Configure attribute filters.
7. Configure result template.
8. Add security filtering where needed.
9. Configure detail page.
10. Configure registration page or workflow.
11. Test no-filter, filter, direct link, and mobile cases.
12. Test with a group at capacity.
13. Test unauthenticated access.

### Playbook: Add Group Requirements

1. Define requirement purpose: safety, training, signature, background check, form, or ministry approval.
2. Decide whether the requirement is Group Type-wide or specific to a group/role.
3. Define the requirement predicate and data source.
4. Configure "does not meet" workflow if needed.
5. Decide whether workflow auto-initiates.
6. Test requirement state for active, pending, and inactive members.
7. Test leader/admin visibility.
8. Document how to resend or reset requirement workflows.

A community recipe describes a helper workflow to clear and resend requirement workflows, especially with signature documents ([Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)). Use the concept carefully: deleting or clearing linked workflows can have audit and compliance implications.

### Playbook: Extend Group Leader Toolbox

1. Identify the external leader toolbox page and current block template.
2. Identify merge fields available in the block.
3. Decide whether new functionality is a page, tab, note block, workflow entry, content channel, or report.
4. Create any new pages with `GroupId` context where needed.
5. Add tabs or links in the template, gated by allowed actions.
6. Verify security for leaders and staff.
7. Test on a real group with active and pending members.
8. Document page IDs and group type IDs.

Community examples extend the toolbox with content, stories, prayer requests, and feedback tabs ([Extending the Group Toolbox](https://community.rockrms.com/recipes/329), [Group Leader Toolbox Enhancements](https://community.rockrms.com/recipes/220)).

## 17. Troubleshooting Decision Tree

### A Group Does Not Appear In Group Viewer

Check:

1. Is the group active?
2. Is it archived?
3. Is the current user authorized to view it?
4. Is it under the expected parent group?
5. Is the Group Type allowed in the viewer's tree/filter?
6. Is the Group Viewer block configured to show archived or inactive groups?
7. Does a circular inherited Group Type or hierarchy issue cause timeouts?
8. Is the page loading the correct parent group parameter?

### A Child Group Type Cannot Be Added

Check:

1. Parent group `GroupTypeId`.
2. Parent Group Type allowed child group types.
3. Whether the intended child Group Type is active.
4. Whether the user has edit/administrate access.
5. Whether the UI is scoped to a subset of group types.
6. Whether the group is archived or inactive.
7. Whether inheritance or circular references are producing errors.

### A Person Is In The Group But Not On The Roster

Check:

1. `GroupMemberStatus`.
2. Role filter.
3. Member start/end or inactive status if present.
4. Security rights.
5. Roster block settings.
6. Whether the person is a duplicate record.
7. Whether the roster page is using group ID or group GUID correctly.
8. Whether the member belongs to a child group, not the selected group.

### Attendance Cannot Be Entered

Check:

1. Group Type takes attendance.
2. Group has a schedule if using mobile attendance.
3. Group has location/schedule if required by the block.
4. User can manage attendance.
5. Block days-back/days-forward settings.
6. Occurrence date and schedule exclusions.
7. Group member statuses and roles.
8. Browser/mobile app errors.
9. Whether attendance saved but UI lacks confirmation.

Mobile attendance specifically requires configured schedules according to developer documentation ([Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)).

### Group Finder Missing Expected Groups

Check:

1. Group active/archive status.
2. Group Type selected by finder block.
3. Campus context.
4. Attribute filters.
5. Schedule options and whether they are filterable.
6. Location and geocoding.
7. Capacity and registration rules.
8. Template security filtering.
9. Query strings such as `LoadResults=true`.
10. Public detail page permissions.

### Attendance Counts Are Wrong

Check:

1. Report entity base: Person, GroupMember, Attendance, or AttendanceOccurrence.
2. Selected Group Types.
3. Child group recursion.
4. Archived/inactive group filters.
5. Member status denominator.
6. Role denominator.
7. Did-not-occur handling.
8. Duplicate person records.
9. Occurrence date range.
10. Rock version, especially the v18.3 Attendance Analytics fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Group Scheduler Looks Wrong

Check:

1. Group scheduling settings on Group Type.
2. Group locations and schedules.
3. Group member roles.
4. Active member status.
5. Schedule templates.
6. Person preferences.
7. Auto-schedule settings.
8. Status board display settings.
9. Rock version. v19.1 beta notes scheduler fixed occurrence date/schedule header behavior and group names above locations ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
10. Whether a custom print/report page is needed instead of altering the scheduler UI.

A Q&A response suggests custom Lava/SQL pages for print-specific volunteer lists when the scheduler board is not formatted as desired ([Remove Group member status from group scheduler board](https://community.rockrms.com/ask/developing/2801)).

### Group Requirement Cannot Be Resent

Check:

1. Requirement configuration.
2. Existing requirement workflow instance.
3. Whether auto-initiate is enabled.
4. Linked workflow state.
5. Whether the member meets the requirement now.
6. Whether v19.1 `GroupMemberRequirementState` behavior exists in this instance.
7. Whether clearing/deleting linked workflow state is allowed by policy.

## 18. Agent Task Recipes

### Recipe: Identify Why A Group Is Not Visible

Collect:

- Group name or GUID.
- Current page/block.
- User/person context.
- Expected viewer/finder path.

Inspect:

1. Group row: active, archived, parent, Group Type.
2. Security: page, block, group type, group.
3. Group Type: allowed hierarchy and finder settings.
4. Finder/viewer block settings.
5. Template logic and rights filters.
6. Query string/page parameters.

Return:

- Exact hidden cause.
- Evidence fields.
- Safe remediation.
- Whether the fix is data, security, block config, or template logic.

### Recipe: Audit A Group Type Before Launch

Inspect:

- Name and purpose.
- Allowed child group types.
- Roles and default role.
- Leader role.
- Attendance settings.
- Schedule options.
- Schedule exclusions.
- Location types and selection modes.
- Group attributes.
- Group member attributes.
- Requirements.
- Workflow triggers.
- Security.
- Finder/registration usage.
- Reports depending on it.

Return:

- Launch readiness.
- Missing configuration.
- Risky inherited settings.
- Live verification steps.

### Recipe: Debug Group Attendance Reminder Failures

Inspect:

1. Group Type takes attendance.
2. Send attendance reminder enabled.
3. Group schedule exists.
4. Schedule date applies and is not excluded.
5. Group has active members/leaders.
6. Reminder job is enabled and ran.
7. Communication/system email settings.
8. Member communication preferences.
9. Attendance already entered or occurrence marked did-not-occur.

Return:

- Whether the problem is configuration, schedule, job, communication, or data.
- Exact next action.

### Recipe: Build A Group Finder QA Checklist

Test:

- Public unauthenticated search.
- Authenticated search.
- Campus filter.
- Day/time filter.
- Attribute filters.
- Distance/location filter.
- Direct `LoadResults=true` behavior if used.
- Detail page.
- Registration page.
- Full group/capacity behavior.
- Security-hidden group behavior.
- Mobile rendering if mobile block is used.

Return:

- Pass/fail by filter.
- Missing groups and reason.
- Security exposure risks.
- Block settings to adjust.

### Recipe: Move Members Between Groups Safely

Before move:

- Export old group member IDs, people, roles, statuses, attributes.
- Confirm target group and role mapping.
- Check requirements.
- Check workflow triggers.
- Check scheduling assignments.
- Decide whether to remove old membership or mark inactive.
- Notify ministry owner.

After move:

- Verify old group membership.
- Verify new group membership.
- Verify role/status.
- Verify member attributes.
- Verify requirements.
- Verify leader roster.
- Verify reporting.

### Recipe: Create A Custom Scheduled Volunteer Communication Page

Use when Group Scheduler/status board cannot communicate with the exact cohort.

Inspect:

- Date range.
- Group Type(s).
- Groups.
- Locations.
- Schedules.
- Assignment/status records.
- Communication eligibility.
- Security.

Community examples show custom pages using Dynamic Data and communications for scheduled members ([View and Communicate with all Scheduled Group Members](https://community.rockrms.com/recipes/185)). Build the production version with reviewed SQL, permissions, and communication policy.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `173`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | configuration | Rapid Attendance Entry is configurable enough to support multiple page variants, so teams can create focused versions for different ministry workflows instead of using one catch-all setup everywhere. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | The block can combine attendance marking with family editing, adding family members, person notes, prayer requests, and workflow launch actions from the same operational screen. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | Rapid Attendance Entry starts from a selected group and attendance date, with location and schedule values available when the group and attendance context support them. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | source_summary | Rapid Attendance Entry can be used as a fast attendance-entry surface and can also collect related ministry information, such as family updates, notes, prayer requests, and workflow launches, when the block settings enable those actions. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | For staff training and operational readiness, Group Attendance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-attendance) |
| rocku-confirmed | operational_guidance | The Extending Groups RockU lesson provides training context for ministry process design; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/extending-groups) |
| rocku-confirmed | operational_guidance | The Group Viewer RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-viewer) |
| rocku-confirmed | operational_guidance | For ministry process design, Group Type Inheritance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |
| rocku-confirmed | operational_guidance | For ministry process design, Person Preferences and Auto Schedule should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/person-preferences-and-auto-schedule) |
| rocku-confirmed | operational_guidance | The Group Placements [Legacy] RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/event-registration/group-placement-in-event-registration) |
| rocku-confirmed | operational_guidance | For Rock operations and administration, Group Administrator should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-administrator) |
| rocku-confirmed | operational_guidance | The Group Placement Options [Legacy] RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. Because the lesson is legacy-labeled, check for a current replacement before using the guidance operationally. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/groups/group-placement-options-legacy) |
| More |  | 161 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `47`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Alternate Placements Transcript Insight](https://community.rockrms.com/rocku/groups/alternate-placements) | approved_for_public_distillation | 2 | media-insight:8cf70b8a9a49fe25 |
| [Data View Filter Groups Transcript Insight](https://community.rockrms.com/rocku/reporting/data-view-filter-groups) | approved_for_public_distillation | 2 | media-insight:94180d5ad9c59fef |
| [Episode 111: Special Edition with Tim Dear Transcript Insight](https://shows.acast.com/rock-cast/episodes/podcast-episode-111-special-edition-with-tim-dear) | approved_for_public_distillation | 3 | media-insight:05f4fce834300a65 |
| [Episode 24: Announcing RX2017 and Sparkability Group Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-24-announcing-rx2017-and-sparkability-group) | approved_for_public_distillation | 3 | media-insight:4e10e7d0e066fd89 |
| [Episode 40: v8 and more team updates Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) | approved_for_public_distillation | 3 | media-insight:6e8d02135da566a7 |
| [Episode 84: Special Edition with Red Rocks Transcript Insight](https://shows.acast.com/rock-cast/episodes/episode-84-special-edition-with-red-rocks) | approved_for_public_distillation | 3 | media-insight:40920b5275ce640a |
| [Extending Groups Transcript Insight](https://community.rockrms.com/rocku/groups/extending-groups) | approved_for_public_distillation | 3 | media-insight:0f8803186922d5aa |
| [Fundraising Group Transcript Insight](https://community.rockrms.com/rocku/finance/fundraising-group) | approved_for_public_distillation | 2 | media-insight:b4c0860821d5f9c1 |
| More |  | 39 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

### Primary Official Sources

- [Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7): official manual for group hierarchy, Group Type administration, locations, schedules, schedule exclusions, attributes, group viewer, attendance, finder, placement, and version updates.
- [Rock Your Groups v16 record](https://community.rockrms.com/documentation/bookcontent/7/296): useful for older navigation wording, member attribute details, v16 sync/scheduler notes.
- [RockU Groups](https://community.rockrms.com/rocku/groups): topic map for operational training across Group Viewer, Details, Attendance, Group Types, Inheritance, History, Locations, Purposes, Requirements, Security, Scheduling, RSVP, and Placement.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): version caveats for v18.3 and v19.1 group-related behavior.

### Developer Sources

- [Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder): filters, query strings, merge fields, security warning.
- [Group Registration mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-registration): `GroupGuid`, group type GUID allowlist, member status, workflow, capacity, person creation settings.
- [Group Attendance Entry mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry): `GroupGuid`, mobile schedule requirement, days-forward/back behavior.
- [Group Member View mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-view): `GroupMemberGuid`, allowed actions, attributes, contact options.
- [Group Member Edit mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-edit): role/status/member edit settings.
- [Schedule Preference mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-preference): scheduling preferences and version markers.
- [Group Members mobile CRM block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/group-members): person-context group member display, family use case.

### Source-Code Landmarks

- [View_GroupLocationSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/View_GroupLocationSchedules.sql): schedule to group-location relationship.
- [View_GroupTypeGroupLocationSchedule.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql): Group Type association hierarchy plus group/location/schedule reporting.
- [Populate_LocationsAndGroupSchedules.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_LocationsAndGroupSchedules.sql): example setup connecting serving teams, locations, and schedules.
- [PersonGetGroupTypeAttendance.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/Action/People/PersonGetGroupTypeAttendance.cs): workflow action pattern for person attendance by group type.
- [GroupTypeGroupMemberWorkflowTriggerBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs): workflow trigger fields.
- [GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs): group/location/date schedule lookup request.
- [GroupSchedulerGroupLocationScheduleNamesBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerGroupLocationScheduleNamesBag.cs): scheduler location/schedule label model.
- [GroupMemberScheduleTemplateDetail.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/GroupScheduling/GroupMemberScheduleTemplateDetail.ascx.cs): schedule template save behavior using schedule builder iCalendar content.

### Community Examples

Use these as patterns to evaluate, not as authoritative behavior:

- [Bulk Group Member Mover](https://community.rockrms.com/recipes/519): workflow-based member move pattern.
- [Group Finder Share Filter](https://community.rockrms.com/recipes/374): client-side shareable filter URL approach.
- [Powerful Small Group Attendance Report](https://community.rockrms.com/recipes/209): attendance percentage reporting concept.
- [Watch Party Attendance](https://community.rockrms.com/recipes/197): aggregate/special-purpose attendance setup.
- [Find Circular Group Type References](https://community.rockrms.com/recipes/110): troubleshooting concept for inherited Group Type loops.
- [Adding Content/Resources for Volunteers to Group Scheduler](https://community.rockrms.com/recipes/334): group attribute to content channel pattern.
- [Extending the Group Toolbox](https://community.rockrms.com/recipes/329) and [Group Leader Toolbox Enhancements](https://community.rockrms.com/recipes/220): leader toolbox extension patterns.
- [Schedule Cancellation Workflow](https://community.rockrms.com/recipes/481): schedule decline communication workflow pattern.
- [Group Member Schedule Templates - adding 5th week and using Auto Schedule](https://community.rockrms.com/recipes/356): scheduling template caveats for fifth-week patterns.
- [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482): requirement workflow reset/resend pattern.

### Dependency Notes

Groups depend on People because group membership is person-based and attendance uses person aliases. They depend on Attendance because group participation is occurrence-based. They depend on Security because visibility and management are layered across pages, blocks, groups, group types, and templates. They depend on Locations because finder, check-in, scheduling, and maps require correct location relationships. They depend on Schedules because attendance reminders, finder day/time filters, volunteer scheduling, RSVP, and mobile attendance all depend on schedule configuration.

The official groups manual covers the hierarchy, location, schedule, attendance, finder, and placement relationships together, while the mobile Group Finder documentation separately warns that returned groups do not automatically account for user security ([Rock Your Groups](https://community.rockrms.com/documentation/bookcontent/7), [Group Finder mobile block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)).

When an agent handles a groups task, the correct final answer should identify which dependency controlled the outcome. For example: "not visible because Group Finder block omitted the Group Type," "not schedulable because group has no location schedule," "attendance missing because mobile block requires a schedule," "counts changed because v18.3 Attendance Analytics no longer includes allowed child group types," or "member cannot be activated because a Group Member Requirement workflow remains unresolved."
