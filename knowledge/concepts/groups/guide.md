---
id: authored-groups
title: Groups
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "8ef211df4b8494486595d36da8996ab3f3b4e3abedf73b185a7330e92dde74cb"
---

# Groups

## Agent Summary

Groups are Rock’s configurable structure for organizing people, leadership, attendance, locations, schedules, security, and operational automation. Begin every group task by identifying the group type, hierarchy position, member role, membership status, and the relevant security scope. Those settings determine which children a group may contain, what attributes and roles are available, whether it appears in Group Finder, how attendance operates, and who may manage it. [Rock v19 Groups documentation](https://community.rockrms.com/documentation/engagement/groups)

Use this operating order:

1. Inspect the Group Type before changing an individual group.
2. Confirm the group’s parent, active/public state, member roles, locations, and schedules.
3. Separate group security from member-management rights and leader capabilities.
4. Treat attendance, reminders, history, requirements, sync, and workflows as configured features rather than automatic behavior.
5. Read back the resulting group, membership, attendance, or security state after automation or API work.
6. Put installation-specific questions under live verification rather than assuming that a documented feature is enabled locally.

## Scope And Boundaries

This guide covers Group Types, hierarchies, group lifecycle, members, roles, attributes, Group Finder, locations and schedules, attendance operations, security, Group Leader Toolbox, history, requirements, sync, and closely related reporting or workflow patterns supported by the evidence pack. The official v19 documentation organizes Groups into these operational areas. [Rock v19 Groups documentation](https://community.rockrms.com/documentation/engagement/groups)

People records, attendance internals, locations, schedules, workflows, communications, reporting, check-in, LMS configuration, and external BI licensing each have their own owning concepts. This guide explains where they intersect with groups without replacing those guides.

A configured possibility is not proof of local state. For example:

- A Group Type may allow a feature that an individual group has not configured.
- A group may be public but still fail other Group Finder filters.
- A role may be called “Leader” without its `Is Leader` setting being enabled.
- A requirement may block manual additions while still allowing workflow-based additions.
- Rock-side page authorization does not establish external BI licensing.
- Source-code support does not prove that a block, endpoint, plugin, or schema version is installed and authorized.

## Mental Model

A Group Type is the policy and schema layer. It defines the roles, inherited attributes, allowed child types, scheduling options, optional features, and base security available to groups of that type. Rock recommends beginning with fewer shared Group Types because adding a new type later is easier than merging overly specialized types. [Intro to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-types/intro-to-group-types)

A Group is an operational node in a tree. It has its own name, parent, status, public visibility, campus, locations, meeting details, attribute values, and possibly individual security or requirements. Rock can create a group at the root or beneath a selected parent, subject to the parent type’s allowed-child configuration. [Add a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group)

A Group Member joins a person to a group with a role, status, notes, communication preference, and any configured Group Member Attributes. The role is not merely a label: role settings can confer leader status, viewing, editing, member management, attendance entry, check-in eligibility, and requirement-notification behavior. [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

Locations and schedules describe where and when the group operates. Attendance is recorded in that group/location/schedule context. At the implementation level, the supplied immutable Rock source excerpt shows groups joined to locations through `GroupLocation`, with schedules joined through `GroupLocationSchedule`; use that as an implementation observation, not proof of any installation’s configuration. [Rock source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_GroupTypeGroupLocationSchedule.sql)

Security is layered. A group can receive base security from its Group Type and parent hierarchy, have direct rules of its own, and grant capabilities through member roles. Inspect all three layers before concluding that access is missing or excessive. [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group)

## Group Types And Hierarchies

Group Types are administered under `Admin Tools > Settings > General > Group Types`. Their configuration includes purpose and structure, allowed child types, locations and scheduling, roles, attributes, optional features, and advanced behavior. [Administer Group Types](https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types)

Rock supports two broad hierarchy patterns:

- A structured hierarchy uses different Group Types to enforce defined levels. A small-group structure might allow a leadership type to contain coach groups, coach groups to contain small groups, and small groups to contain no children.
- A flexible hierarchy allows a type to contain itself, supporting serving-team trees whose depth varies by ministry.

These structures are implemented through the allowed child Group Types. [Group Hierarchy](https://community.rockrms.com/documentation/engagement/groups/group-types/group-hierarchy)

A Group Type can inherit attributes from another Group Type. This supports a specialized type that needs all attributes from a shared base type plus additional attributes of its own—for example, a worship-serving type inheriting from a general serving-team type and adding an instruments attribute. This evidence supports attribute inheritance; it does not establish that every Group Type setting is inherited. [Administer Group Types](https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types)

When planning a hierarchy, determine:

- Which levels represent operational groups versus organizational containers.
- Which Group Types may appear as children at each level.
- Whether the structure must remain fixed or may recurse.
- Which roles exist at each level and which are actually marked `Is Leader`.
- Which attributes belong on a reusable base type and which belong only on a specialized type.
- Which downstream processes depend on an exact depth. The Group Attendance Digest, for example, requires a specific three-level structure and should not be treated as compatible with every valid group tree. [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email)

## Creating, Editing, Inactivating, And Archiving Groups

A group can be added at the root with **Add Top-Level** or beneath the selected group with **Add Child to Selected**. If child creation is disabled, inspect the selected parent’s Group Type; it does not permit the proposed child relationship. [Add a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group)

The group edit surface can control its name, active state, public visibility, description, Group Type, parent, administrator, security-role behavior, campus, meeting details, group attributes, member attributes, and member workflow configuration. Changing an existing group’s Group Type causes its group attribute data to be lost, so treat that as a migration rather than a cosmetic edit. [Edit a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group)

Changing the parent moves the group within the hierarchy; removing the parent moves it to the root. Before moving a group, inspect processes that depend on ancestry, including inherited security and the Attendance Digest’s parent-region-attendance structure. [Edit a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group)

Inactivation and archiving serve different purposes:

- Inactivation clears the group’s active state. Depending on Group Type configuration, Rock may request an inactive reason and optional note and can offer to inactivate child groups.
- Archiving is available after Group History is enabled for the Group Type and the Process Group History job has run. It removes the group from ordinary group-viewer surfaces without deleting it. An archived group can later be restored from `Admin Tools > Settings > General > Archived Groups`.

[Edit a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) [View Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history)

Do not substitute deletion for archiving when the group’s history must remain recoverable.

## Members, Roles, Statuses, And Attributes

Group Member Roles are defined on the Group Type. Supported role settings include:

- `Is Leader`
- requirement-notification eligibility
- group viewing and editing
- member management
- attendance entry
- check-in eligibility
- minimum and maximum member counts for the role
- default assignment for new members

Some blocks can override the type’s default role. Check-in eligibility through the role applies when the check-in area uses the “Already Enrolled In Group” rule. [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

Member status represents the person’s standing within that group:

- Active: currently participating.
- Inactive: no longer participating.
- Pending: not yet fully joined.

These statuses are group-membership state, not a replacement for the person’s record status. [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

A Group Member detail record can hold role, status, a membership note, Group Member Attributes, a group-specific communication preference, and a notification marker used by the Group Leader Notification job. The person linked to an existing Group Member record cannot be replaced in place; add the correct person and remove the incorrect membership instead. [Edit a Group Member](https://community.rockrms.com/documentation/engagement/groups/group-members/edit-a-group-member)

Group Member Attributes normally originate on the Group Type and therefore apply across its groups. A specific group can add member attributes when the user has Administrate access and the Group Type permits the relevant group-specific configuration. [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

When moving a member between groups, Rock can transfer member notes. Group Member Attribute values survive only when the source and destination share attributes with the same key; otherwise those values are lost. Fundraising Groups have an additional donation-movement concern owned by the finance concept. [Move Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/move-group-members)

A community-submitted bulk-move recipe demonstrates a workflow-driven approach for selecting a source group, choosing members, and launching a per-person move workflow. The recipe is marked Draft and explicitly carries the community-site disclaimer that recipes are not reviewed or endorsed by the Rock core team. Treat it as an example to review and test, not as official Rock behavior. [Bulk Group Member Mover recipe](https://community.rockrms.com/recipes/519)

## Group Security And Leader Operations

Group Type security establishes base security for every group of that type. It is configured from the Group Types administration list. Use it when a whole category of groups needs a common viewing or editing boundary. [Securing a Group Type](https://community.rockrms.com/documentation/engagement/groups/secure-groups/securing-a-group-type)

A specific group can have its own security rules. Rock’s documented group-security evaluation considers the current group, Group Type security, parent-group security up the hierarchy, Group entity-type security, and the global default. Direct rules can build on or override inherited rights. Roles on the Group Type can then provide group access to members in those roles. [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group)

`Manage Members` is narrower than editing the group itself. A person with that permission can add, edit, and delete memberships but cannot thereby edit or delete the group. Edit access includes member-management access by default. The documented group surface also allows group leaders to manage members even without an explicit `Manage Members` rule, while role settings can independently grant capabilities such as viewing, editing, member management, or attendance entry. [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group) [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

The Group Detail block’s **Add Administrate Security to Group Creator** setting controls whether a person who creates a group automatically receives Administrate permission. The v19 documentation says its default is No and notes that changing it does not retroactively alter older groups. [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group)

The Group Toolbox uses the Group Detail Lava block to expose group details and leader actions such as editing group or member information, managing the roster, and sending communications. Its default add-member search requires access to the People REST controller. Where that search would reveal too much of the database, configure an alternate add-member page that uses a workflow form, group registration block, or simple contact mechanism. [Use the Group Toolbox](https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox)

If a group is also configured as a security role, its members receive permissions granted to that role. Inspect membership automation carefully before enabling login creation or security-role sync. [Edit a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) [Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync)

## Locations And Schedules

A Group Type controls which scheduling modes its groups may use. The v19 documentation describes three modes:

- Weekly: day of week and start time.
- Custom: a group-specific repeating schedule.
- Named: a selection from schedules configured under `Admin Tools > Settings > General > Schedules`.

Only Weekly schedules are documented as usable by the standard Group Finder’s day and time filters. [Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types)

Group Types can also allow multiple locations and enable predefined schedules on group locations. The supplied immutable source excerpts show the implementation relationship `Group -> GroupLocation -> GroupLocationSchedule -> Schedule`, while Group Attendance request models accept group, location, and date context when retrieving applicable schedules. These are source-code observations from the referenced commit, not confirmation of a target installation’s UI or configuration. [Group-location schedule SQL](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/View_GroupLocationSchedules.sql) [Attendance schedule request model](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupAttendanceDetail/GroupAttendanceDetailGetGroupLocationSchedulesRequestBag.cs)

A reviewed community pattern warns that room capacity and schedule availability are separate concerns: a room threshold belongs to the Location, while service-time availability depends on the group-location-schedule relationship. That distinction requires validation on the target version and configuration before making changes. [Community evidence source: Model Map](https://community.rockrms.com/ModelMap)

Another reviewed community pattern recommends using the authorized Obsidian Check-in Schedule Builder action for schedule-link changes when that block action is installed and available, followed by a readback of the resulting relationships. Because the contribution references moving `develop` sources and is marked as needing live verification, do not assume that action exists or that its request contract matches the target version. [Referenced Schedule Builder source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/CheckIn/CheckInScheduleBuilder.cs)

## Group Finder

The standard Group Finder lets visitors search public groups and proceed toward group registration. Only groups marked `Public` are eligible to appear. The block can be configured with eligible Group Types, capacity handling, initial-result behavior, search filters, location types, geofencing, mapping behavior, displayed attributes, and linked group-detail and registration pages. [Intro to the Group Finder](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder)

Day-of-week and time-of-day filtering depend on groups using the Weekly schedule mode. Custom and Named schedules are not documented as usable by those standard filters. [Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types)

Location display requires privacy judgment. The block provides marker-scaling and location-precision settings that can reduce the precision shown for a home-based group. Confirm the rendered result rather than assuming the underlying address is adequately obscured. [Intro to the Group Finder](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder)

A vendor-published example describes a custom Helix-powered guided finder with a multi-step form, dynamic filtering, proximity search, group details, and map integration. It demonstrates a possible customized experience, not standard Group Finder behavior or a feature proven present in another installation. [Triumph Guided Group Finder](https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix)

For a seasonal finder, a reviewed community closeout pattern recommends testing the public route, redirects, page and block authorization, alternate or mobile surfaces, and the underlying visibility filters. When inspecting authorization records, qualify the secured entity type so a Page identifier is not confused with an unrelated Block identifier. This pattern needs target-instance verification. [Community evidence source: Model Map](https://community.rockrms.com/ModelMap)

## Group Attendance Entry

Rapid Attendance Entry begins with a selected group and attendance date. Location and schedule values are available when the group and attendance context support them. This behavior is an approved RockU-derived claim with a reviewed read-only verification of the required group, attendance, location, schedule, and relationship surfaces. [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) (`claim:dae53f2715a5838fd9fc`)

When enabled in the block settings, the same operational surface can combine attendance marking with family edits, adding family members, notes, prayer requests, and workflow launches. These actions are configurable; their presence should not be inferred merely because the attendance block exists. [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) (`claim:3b96546de8e62931465b`, `claim:81b7e563732881f9f61e`)

Teams can create focused Rapid Attendance Entry page variants for different ministries instead of putting every available action onto a single catch-all page. The approved claim was supported by a reviewed read-only verification that Group Attendance Entry is a block type with page and block surfaces; it does not prove that any particular variants have been configured locally. [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) (`claim:a69d0b49451cf59e5ef8`)

For an event-oriented read-only dashboard, a reviewed community pattern recommends starting from the registration roster, adding eligible active placement-group members when local process allows placement outside registration, and deriving check-in state from the latest relevant attendance and occurrence records. Missing placement and group-only rows should remain explicit states. This is an implementation pattern requiring schema, process, and target-instance review—not official universal behavior. [Helix Content Block documentation](https://community.rockrms.com/developer/helix/lava-applications/content-block)

## Attendance Reminders, Digests, Absence Follow-Up, And Reports

The Send Group Attendance Reminders job can handle multiple Group Types, but it sends only for types with **Send Attendance Reminder** enabled under Attendance/Check-in. Each type can retain its own reminder communication template. The v19 documentation describes the standard job as running every 15 minutes, sending when the configured offset is reached, and recording the last-sent time on the attendance occurrence so the same reminder is not sent twice in one day. [Send Group Attendance Reminders](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders)

The Group Attendance Digest requires exactly three hierarchy levels:

1. One top parent group, selected in the job.
2. Region or area groups beneath it, containing people whose role is marked `Is Leader`.
3. Attendance-recording groups beneath each region.

Every leader in a region group receives that region’s child-group digest. The **Email Leader** action targets the leader of the attendance group itself. The number of regions or attendance groups may vary, but all three hierarchy levels are required. [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) (`claim:07e2013c88bfc50be00a`, `claim:bde19ee62aa336ac343f`)

The digest job also requires the highest-level parent and a System Communication. The documented date range can be the current or previous week, and the attendance groups must meet on a regular Weekly schedule for the job to operate correctly. [Send Group Attendance Digest](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-digest)

The Group Leader Absence Notifications job evaluates consecutive absences and alerts leaders for follow-up. It runs for one Group Type per job instance, can filter evaluated members by role, and uses a configured minimum absence count. The v19 documentation says blank defaults to three and zero causes the job to fail. [Group Leader Absence Notifications](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/group-leader-absence-notifications)

The attendance-report job can create or update Person attributes for first attendance, last attendance, attendance in the previous 12 months, and attendance in the previous 16 weeks for groups returned by a Group Data View. It counts relevant attendance whether or not the person is currently an active group member. Attribute categories and security must be managed separately; changing the job’s reporting label can cause new attributes to be created. [View Group Attendance Reports](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/view-group-attendance-reports)

## Group History

Group History compiles group configuration and membership changes into timeline and table views. Rock v19 documentation says it ships enabled for small-group and serving-group types, while still allowing history to be enabled or disabled for any type. Because history can grow quickly, the documentation recommends using it for regular, comparatively stable groups rather than high-churn groups. [Intro to Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history)

Enable the feature on the Group Type under `Admin Tools > Settings > General > Group Types`. The Process Group History job then creates historical snapshots for enabled Group Types; the standard job is documented as running daily. After it runs, eligible groups expose Archive instead of Delete. [Enable Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/enable-group-history) [Process Group History](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/process-group-history)

The timeline can show member additions, member removals, group edits, and other group actions by date. Member History provides a person-centered view of involvement dates. [View Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history) (`claim:242010519d8a5aa432b1`)

A reviewed community reporting pattern recommends using historical group and member snapshots—not only current Group and Group Member rows—when answering point-in-time questions. That pattern should be validated against the target schema and known historical changes before adoption. [Community evidence source: Rock Metrics documentation](https://community.rockrms.com/documentation/church-management/reporting/metrics)

## Group Requirements

A member requirement attached at the Group Type level applies across groups of that type. Its population can be narrowed by Group Member Role, age classification, or a Data View. If those selectors are left broad, the requirement applies correspondingly broadly. [Applying Requirements to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) (`claim:cd55aeeeb6e608920a0a`)

Type-level requirements can permit leader overrides or require completion before a person is added. This supports enforceable eligibility rules such as requiring a completed background check before joining a serving team. [Applying Requirements to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) (`claim:d6e9271468584ba88a99`)

Individual-group requirements are available when **Enable Specific Group Requirements** is enabled for the Group Type and the operator has Administrate access to the group. A critical boundary is that the documented “must meet before adding” restriction applies to manual additions; workflow actions can still add someone who does not meet the requirement. Automation must therefore perform its own eligibility check when enforcement must cover workflow-driven membership. [Applying Requirements to Groups](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-groups)

Requirement notifications also depend on role and job configuration. The recipient role must have **Receive Requirements Notifications**, and the corresponding requirement-notification job must be configured. [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members)

## Group Sync And Communication Lists

Group Sync is enabled at the Group Type level. A sync compares people returned by a Data View with current group membership and updates membership to match. Each sync assigns one role, so separately managed leader and member populations require separate sync definitions. [Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync)

The sync interval should be no more frequent than operationally necessary because many frequently evaluated syncs can affect performance. The group-level interval and the Group Sync job’s execution cadence both matter. Optional welcome and exit communications can announce changes, and login creation can be enabled for security-role use cases. These options require careful security and communication review before activation. [Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync)

In Rock v19, communication lists are groups of a specific type. Membership can be maintained manually or synchronized from Data Views, so recipient troubleshooting must inspect both the underlying group and its sync configuration. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) (`claim:a774892d024b8bbe0560`)

A reviewed community send-preflight pattern recommends refreshing a Data View-backed communication-list group immediately before use, comparing the resulting membership count with the source population, and testing personalized call-to-action links with representative valid parameters. This is a local operational guardrail requiring instance verification, not a built-in guarantee. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

## Groups In Workflows, Training, And Reporting

The supplied immutable Rock source model shows Group Type member-workflow trigger configuration with trigger type, from/to status, from/to role, an active flag, workflow type, and a first-attendance option. This confirms implementation surfaces at commit `471fd303`; it does not establish which triggers are available, enabled, or configured in a target installation. [Group member workflow trigger source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/GroupTypeDetail/GroupTypeGroupMemberWorkflowTriggerBag.cs)

A reviewed community troubleshooting pattern warns that a launched workflow may report a later failure after an earlier action already changed group membership, sent a communication, or wrote an attribute. Before retrying, inspect action order, logs, and expected side effects, then make duplicate suppression account for partial success. This pattern needs reproduction against the actual workflow. [RockU Workflows](https://community.rockrms.com/rocku/workflows)

Other reviewed community workflow patterns in the pack include:

- Updating visible copy, hidden defaults, review workflows, and criteria across every linked Workflow Type during a seasonal rollover.
- Using attributes on reusable Defined Values to control which seasonal options a workflow renders.
- Using temporary per-ministry shadowing groups when onboarding state must affect rosters, check-in visibility, badges, or placement behavior.
- Preferring existing operational signals over adding new lifecycle statuses when the need is only visibility rather than a true change in ownership or next action.

Each pattern is a locally contributed example marked as needing live verification. [RockU Workflows](https://community.rockrms.com/rocku/workflows) [Rock Model Map](https://community.rockrms.com/ModelMap)

Community-reviewed evidence also describes Rock LMS programs, courses, class instances, learning plans, activities, and participants, with programs supporting on-demand or academic-calendar modes. Activities may include acknowledgements, video watching, quizzes, uploads, and facilitator scoring. Training design therefore needs both learner actions and staff review responsibilities. [Community LMS session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) (`claim:dd3b03571388d00cc80b`, `claim:882208fdf2bb82703931`)

Existing videos can be used as LMS activities, but completion, sequencing, and review must be intentionally configured. LMS completion can also participate in local group sync and workflow follow-up patterns. The reviewed verification confirmed relevant structural surfaces, not a specific ministry implementation. [Community LMS example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) (`claim:c538cf61594b1114dc41`) [Community LMS session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) (`claim:4bc0aee305fa6b1bd524`)

For analytics, community-reviewed claims support calculating expensive engagement journeys into a scheduled Persisted Dataset instead of reconstructing all historical detail on every page load. Rock’s metric, metric-value, Data View persistence, and Persisted Dataset surfaces can also support snapshot-style daily counts and trends for external reporting. These are implementation patterns rather than a universal reporting design. [Community analytics example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) (`claim:01d746f9a6bc23a6d503`) [Community reporting example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz) (`claim:a5f0a54f29d226cec5fc`)

When embedding Power BI or a similar report in Rock, pair Rock page and block authorization with external licensing checks. Rock-side authorization alone does not prove that the viewer is licensed by the external provider. [Community BI example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) (`claim:60d40983fd53c0173dd9`)

## Version And Authority Caveats

Most official documentation in this evidence pack is scoped to Rock v19.0. Verify behavior after upgrades, especially block settings, jobs, workflow triggers, authentication, and Obsidian replacements. [Rock v19 Groups documentation](https://community.rockrms.com/documentation/engagement/groups)

The Communication Lists claim is explicitly scoped to Rock 19.0. The Rapid Attendance Entry claims have unprocessed version scope and should be checked against the installed block version before configuration changes. [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)

The supplied GitHub excerpts use immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` and are implementation evidence. They do not prove installation state or local configuration. Community contributions that point only to `develop` are examples requiring renewed source and target-version review.

The Bulk Group Member Mover recipe is a draft community recipe identified with Rock 16.0 and is not endorsed by the Rock core team. [Bulk Group Member Mover](https://community.rockrms.com/recipes/519)

The approved community-reviewed analytics, LMS, workflow, and BI claims include reviewed public-safe conclusions from bounded read-only structural verification. That establishes the relevant surfaces used by those claims, not the configuration, population, licensing, or behavior of another organization’s installation.

## Troubleshooting Decision Tree

### Add Child to Selected is disabled

1. Confirm the intended parent group is selected.
2. Inspect its Group Type’s allowed child types.
3. Determine whether the proposed child type is allowed or whether the hierarchy is intentionally closed.
4. Do not move the group to the root merely to bypass the hierarchy without reviewing downstream security and digest effects.

[Add a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group)

### A group is missing from Group Finder

1. Confirm the group is marked `Public`.
2. Confirm its Group Type is included in the block’s configured Group Types.
3. Check whether the group has reached capacity and whether overcapacity groups are hidden.
4. Inspect location-type, campus, geofence, and attribute filters.
5. If filtering by day or time, confirm the group uses a Weekly schedule.
6. Test the public route and any alternate or mobile surface as an anonymous visitor.

[Intro to the Group Finder](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder) [Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types)

### The day or time filter does not return a group

1. Inspect the group’s schedule mode.
2. If it is Custom or Named, do not assume the standard Group Finder can filter it by day or time.
3. Confirm the Weekly day and start time on the group.
4. Confirm the corresponding finder filter is enabled.
5. Retest with the exact public-facing criteria.

[Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types)

### A leader cannot add a member from Group Toolbox

1. Confirm the person’s membership role and that it is actually marked as a leader or grants member management.
2. Inspect direct and inherited group security.
3. Check the Group Toolbox block’s add-member configuration.
4. If it uses the default database search, verify authorized access to the People REST controller.
5. If broad People search is inappropriate, configure and test an alternate add-member page.

[Use the Group Toolbox](https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox) [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group)

### A person was added even though a requirement was unmet

1. Determine whether the addition was manual or workflow-driven.
2. Confirm the requirement applies to the member’s role, age classification, and Data View population.
3. Confirm **Members must meet this requirement before adding** is enabled.
4. If a workflow added the person, add an explicit eligibility check to that workflow; the documented manual-add restriction does not block workflow actions.
5. Check for a permitted leader override.

[Applying Requirements to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) [Applying Requirements to Groups](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-groups)

### Attendance reminders are not sent

1. Confirm **Send Attendance Reminder** is enabled on the Group Type.
2. Confirm the group has the expected schedule and start time.
3. Inspect the configured reminder offset and Group Type communication template.
4. Check the reminder job’s status and recent execution.
5. Inspect whether the attendance occurrence already records a reminder sent for that day.
6. Verify recipient roles and addresses without sending a manual substitute until duplicate risk is understood.

[Send Group Attendance Reminders](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders)

### An attendance digest is missing groups or reaches the wrong leader

1. Confirm there is one top parent, an intermediate region/area level, and attendance groups beneath the regions.
2. Confirm the configured job parent is the single top parent.
3. Confirm recipients belong to the region group in a role marked `Is Leader`.
4. Confirm attendance is recorded in the child attendance groups.
5. Confirm those groups use regular Weekly schedules.
6. Distinguish region digest recipients from the attendance group leader targeted by **Email Leader**.

[Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) [Send Group Attendance Digest](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-digest)

### The absence-notification job fails or evaluates the wrong people

1. Confirm the job is scoped to the intended single Group Type.
2. Inspect the member-role filter.
3. Confirm the notification communication.
4. Check the minimum consecutive absences.
5. Do not set the minimum to zero; the v19 documentation says this causes failure.
6. Use another job instance for another Group Type.

[Group Leader Absence Notifications](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/group-leader-absence-notifications)

### Group History or Archive is unavailable

1. Confirm **Enable Group History** is enabled on the Group Type.
2. Confirm the Process Group History job has run successfully since enablement.
3. Reopen the group after the job completes.
4. If restoring an archived group, use `Admin Tools > Settings > General > Archived Groups`.
5. Do not infer that missing history means no changes occurred before history was enabled.

[Enable Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/enable-group-history) [Process Group History](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/process-group-history) [View Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history)

### A synced group or communication list has unexpected members

1. Confirm Group Sync is enabled for the Group Type.
2. Inspect the exact Data View result.
3. Inspect the role assigned by each sync definition.
4. Compare active group membership with the Data View population.
5. Check both the group sync interval and the Group Sync job’s latest execution.
6. Review overlapping syncs, manual memberships, and optional exit behavior.
7. Before a communication, refresh and reconcile the intended source count using locally reviewed procedures.

[Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync) [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists)

### Member attributes disappeared after a move

1. Identify the source and destination Group Types.
2. Compare the Group Member Attribute keys.
3. Determine whether notes were transferred.
4. Restore missing values only from an authorized source.
5. Before future moves, export or inspect values whose keys are not shared.

[Move Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/move-group-members)

### A location or schedule link is wrong after API work

1. Read the target Group, GroupLocation, Location, Schedule, and GroupLocationSchedule state.
2. Determine whether the change affected the Location itself or only its relationship to the group and schedule.
3. Inspect for unintended related records before retrying.
4. Do not submit partial navigation objects or delete suspected placeholders until the target endpoint behavior and references are verified.
5. If an authorized Schedule Builder block action is available for the installed version, evaluate that supported UI action.
6. Read back every affected relationship after correction.

[Immutable group-location-schedule source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/View_GroupLocationSchedules.sql) [Referenced generated REST controller](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs)

### A failed workflow may have partially changed group data

1. Inspect workflow action order and logs.
2. Check whether membership, communications, or attributes changed before the failure.
3. Identify which action actually failed.
4. Make retry logic account for already-completed side effects.
5. Stop before retrying if duplicate membership, duplicate communication, or repeated downstream actions remain possible.

[RockU Workflows](https://community.rockrms.com/rocku/workflows)

## Agent Task Recipes

### Recipe: Design a Group Type and hierarchy

**Outcome:** A bounded Group Type design with explicit hierarchy, roles, attributes, and security.

1. Inventory existing Group Types and look for a reusable common type before proposing another.
2. Define whether the tree is structured or flexible.
3. List allowed child types at every level.
4. Define roles and mark only genuine leader roles as `Is Leader`.
5. Assign role capabilities for viewing, editing, member management, attendance, and check-in.
6. Place shared attributes on the base type and specialized attributes on the specialized type.
7. Define schedule modes, location options, history, requirements, sync, and security.
8. Test creation at every intended hierarchy level.

**Inspect:**

- Existing types and purposes
- Attribute inheritance
- Allowed child types
- Role minimums and maximums
- Group Type security
- Attendance Digest depth requirements

**Do not assume:**

- Attribute inheritance means every setting is inherited.
- A role named Leader has `Is Leader` enabled.
- A valid hierarchy works with the Attendance Digest.

[Administer Group Types](https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types) [Group Hierarchy](https://community.rockrms.com/documentation/engagement/groups/group-types/group-hierarchy)

### Recipe: Publish a group through Group Finder

**Outcome:** An intended group is discoverable without exposing unnecessary location precision.

1. Confirm the group is active and public.
2. Confirm its Group Type is included in the finder.
3. Configure an appropriate location and privacy precision.
4. Use a Weekly schedule if visitors must filter by day or time.
5. Review capacity and the block’s overcapacity behavior.
6. Confirm the detail and registration linked pages.
7. Test initial load, each enabled filter, map behavior, details, and registration as an anonymous visitor.
8. If seasonal, test closed-state routes, redirects, blocks, and alternate surfaces.

**Stop when:**

- The public result exposes more location detail than intended.
- Registration points to an unverified page.
- The group is visible through an alternate route that should be closed.

[Intro to the Group Finder](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder)

### Recipe: Configure focused attendance entry

**Outcome:** Ministry staff can enter attendance and only the related actions appropriate to that workflow.

1. Select the target Group and attendance date.
2. Confirm the valid location and schedule context.
3. Review which related actions are needed: family changes, new family members, notes, prayer requests, or workflows.
4. Enable only those actions in the block settings.
5. Create separate page variants where ministries require different action sets.
6. Confirm operator permissions.
7. Test a representative attendance occurrence and read back the saved state.

**Do not assume:**

- Every group has a usable location or schedule.
- Every Rapid Attendance Entry page exposes the same actions.
- A visible workflow button proves that the workflow completed successfully.

[Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)

### Recipe: Configure attendance follow-up

**Outcome:** Leaders receive the intended reminders, digests, or absence notifications without duplicate or misrouted messages.

1. Choose the operational mechanism: reminder, digest, absence notification, or attendance-report attributes.
2. Confirm the Group Type’s attendance settings and leader roles.
3. For a digest, construct the required parent-region-attendance hierarchy and use Weekly schedules.
4. Configure the correct System Communication and date or absence settings.
5. Verify the job scope and cadence.
6. Run a bounded test using non-production delivery controls where available.
7. Inspect job results, occurrences, recipient selection, and duplicate-suppression state.

**Stop when:**

- The hierarchy does not match the digest’s three-level requirement.
- Recipient roles are ambiguous.
- The test could send a real communication without authorization.

[Common Group Jobs](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs)

### Recipe: Enforce a Group Type requirement

**Outcome:** The intended population is evaluated and manual additions are blocked or overrideable according to policy.

1. Open the Group Type’s Group Requirements section.
2. Select the requirement.
3. Scope it by role, age classification, and Data View as needed.
4. Decide whether leaders may override it.
5. Enable pre-add enforcement when required.
6. Test an eligible and ineligible manual addition.
7. Inspect every workflow or integration that can add members and implement a separate eligibility check there.
8. Configure notification recipients and the requirement-notification job if needed.

**Do not assume:**

- Manual-add enforcement applies to workflow additions.
- A requirement applies to every role or age when selectors narrow it.
- A leader receives notifications merely because the role is named Leader.

[Applying Requirements to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) [Applying Requirements to Groups](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-groups)

### Recipe: Synchronize a group from a Data View

**Outcome:** Membership for one role follows a reviewed population rule at a sustainable cadence.

1. Enable Group Sync on the Group Type.
2. Create and validate the source Data View.
3. Add the sync to the target group.
4. Choose one assigned role.
5. Set the lowest operationally acceptable frequency.
6. Review welcome, exit, and login-creation options.
7. Configure another sync only if another role needs independent management.
8. Run the Group Sync job and reconcile Data View results with resulting membership.
9. For communication lists, refresh and reconcile immediately before an authorized send.

**Stop when:**

- The Data View includes an unexplained population.
- The group is a security role and login or permission effects have not been reviewed.
- Counts do not reconcile.

[Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync)

### Recipe: Secure leader operations

**Outcome:** Leaders can perform approved group tasks without unnecessary database or group-administration access.

1. Inspect Group Type security.
2. Inspect parent-group and direct-group security.
3. Review the leader role’s capabilities.
4. Separate `Manage Members` from Edit or Administrate access.
5. Inspect Group Toolbox block settings and page security.
6. Decide whether the default People search is appropriate.
7. If not, configure an alternate controlled add-member path.
8. Test viewing, editing, roster management, attendance, and navigation as a representative leader.

**Do not assume:**

- Blank direct `Manage Members` rules mean no one can manage members.
- Group administrator designation grants leader security.
- Toolbox navigation limits replace entity security.

[Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group) [Use the Group Toolbox](https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox)

### Recipe: Enable history and archive a group

**Outcome:** Group changes are snapshotted and a retired group is recoverable.

1. Confirm the Group Type is stable enough for retained history.
2. Enable Group History on the Group Type.
3. Confirm the Process Group History job runs successfully.
4. Inspect the group timeline and member history.
5. Archive the group instead of deleting it.
6. Confirm it is absent from normal group-viewer surfaces.
7. Record the restoration path through Archived Groups.

**Stop when:**

- The job has not produced the expected history state.
- The operational request actually calls for temporary inactivation rather than archival.
- Downstream finder, scheduling, or workflow behavior has not been reviewed.

[Intro to Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history) [View Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history)

### Recipe: Move group members safely

**Outcome:** Selected memberships move without unexpected loss of notes or attributes.

1. Confirm the exact source and destination groups.
2. Compare destination roles and capacity.
3. Compare Group Member Attribute keys.
4. Record values that will not transfer.
5. Decide whether member notes should move.
6. Move a representative member.
7. Verify the destination membership, role, status, notes, and retained attributes.
8. For bulk automation, add idempotency and per-person verification before scaling.

**Do not assume:**

- Matching attribute labels mean matching keys.
- A successful workflow means every per-person move succeeded.
- A draft community recipe is production-ready.

[Move Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/move-group-members) [Bulk Group Member Mover](https://community.rockrms.com/recipes/519)

## Known Gaps And Live Verification

Before acting on an installation, verify:

- The installed Rock version and whether the relevant Group, Attendance, Finder, Toolbox, Scheduler, History, LMS, and Helix blocks are present.
- Actual Group Type settings, inherited attributes, allowed child types, roles, requirements, sync enablement, and security.
- Group active/public state, parentage, capacity, locations, schedules, and Group Finder block filters.
- Job existence, enabled state, cadence, last result, and communication templates.
- Whether Group History has produced snapshots since it was enabled.
- Whether workflow-based membership paths enforce requirements independently.
- Whether external BI viewers have the necessary provider licensing in addition to Rock access.
- Whether local reports use current membership, historical snapshots, persisted datasets, or another defined truth source.

The following reviewed community patterns remain hypotheses until verified against the target installation:

- Partial navigation objects in generated REST requests may create unintended related records.
- A successful Group Member POST may require a subsequent readback before another record can reliably link to the new membership.
- An Obsidian Schedule Builder action may be the appropriate way to change group-location schedule links.
- Location-level room thresholds and group-location schedule availability may require separate checks.
- Group metric categories may need resolution from the nearest configured ancestor.
- Historical group metrics may need point-in-time group/member snapshots.
- Registration segments such as staff, serving, or department require explicitly configured local truth and precedence.
- Temporary shadowing groups may be more operationally useful than a status label.
- A failed workflow may retain successful earlier side effects.
- Seasonal workflows may need coordinated updates across several Workflow Types and reusable Defined Values.
- Public seasonal features may remain reachable through alternate routes or surfaces after a template flag changes.

The pack supplies no reviewed live result for any reader’s target installation. Do not claim that a group, job, workflow, endpoint, security rule, plugin, or report is currently configured until a bounded read-only review confirms it.

## Source Map

### Official Rock documentation

- [Groups](https://community.rockrms.com/documentation/engagement/groups): concept structure and routing.
- [Administer Group Types](https://community.rockrms.com/documentation/engagement/groups/group-types/administer-group-types): Group Type configuration, roles, attributes, hierarchy, scheduling, and inheritance.
- [Group Hierarchy](https://community.rockrms.com/documentation/engagement/groups/group-types/group-hierarchy): structured and flexible hierarchies.
- [Add a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group) and [Edit a Group](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group): lifecycle and group configuration.
- [Intro to Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/intro-to-group-members), [Edit a Group Member](https://community.rockrms.com/documentation/engagement/groups/group-members/edit-a-group-member), and [Move Group Members](https://community.rockrms.com/documentation/engagement/groups/group-members/move-group-members): roles, statuses, member fields, and movement.
- [Group Schedule Types](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types): Weekly, Custom, and Named schedule behavior.
- [Intro to the Group Finder](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder): visibility, filters, maps, and linked pages.
- [Secure a Group](https://community.rockrms.com/documentation/engagement/groups/secure-groups/secure-a-group) and [Securing a Group Type](https://community.rockrms.com/documentation/engagement/groups/secure-groups/securing-a-group-type): security layers.
- [Use the Group Toolbox](https://community.rockrms.com/documentation/engagement/groups/group-leader-toolbox/use-the-group-toolbox): leader operations and People search security.
- [Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance) and [Common Group Jobs](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs): attendance workflow routing.
- [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email): required hierarchy and recipient behavior.
- [Group History](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history): history purpose, enablement, processing, and archive behavior.
- [Applying Requirements to Group Types](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) and [Applying Requirements to Groups](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-groups): requirement scope and enforcement limits.
- [Configure Group Sync](https://community.rockrms.com/documentation/engagement/groups/group-sync/configure-group-sync): Data View-driven membership.
- [Communication Lists](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists): Rock 19.0 communication-list group behavior.

### Approved RockU and community-reviewed claims

- [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry): approved claims for attendance context, configurable ministry actions, and focused page variants.
- [Community LMS session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN): reviewed LMS structure, activities, group interaction, and staff-review patterns.
- [Community persisted-data example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW): scheduled persisted analytics.
- [Community reporting example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz): snapshot-style reporting.
- [Community BI example](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz): Rock authorization plus external licensing.

### Implementation and community examples

- [Rock source at immutable commit `471fd303`](https://github.com/SparkDevNetwork/Rock/tree/471fd303d111b2e46218228dbc1e93dba8856fa3): bounded implementation evidence for group-location-schedule relationships, attendance request context, and workflow-trigger models.
- [Bulk Group Member Mover](https://community.rockrms.com/recipes/519): draft, non-endorsed community recipe.
- [Triumph Guided Group Finder](https://www.triumph.tech/resources/enhancing-community-connection-triumphs-guided-group-finder-powered-by-helix): vendor example of a customized finder.
- [Rock Model Map](https://community.rockrms.com/ModelMap), [RockU Workflows](https://community.rockrms.com/rocku/workflows), and [Helix Content Blocks](https://community.rockrms.com/developer/helix/lava-applications/content-block): public sources referenced by reviewed community patterns that still require target-instance verification.