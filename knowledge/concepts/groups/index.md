---
id: concept-groups
title: Groups
generated: true
last_built: 2026-08-12T12:50:00+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
source_freshness_status: complete
source_last_checked_at: 2026-08-12T06:18:46+00:00
source_native_migration_status: partial
source_native_article_coverage: 2/89
legacy_summary_retirement_coverage: 2/89
depends_on_topics:
  - people
  - attendance
  - security
  - locations
  - schedules
---

# Groups

Group types, group members, attendance, group finder, small groups, serving teams, and security.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Groups` spans people, attendance, security, locations, schedules. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_rocku, rock_recipes, rock_model_map, triumph_resources.
- Related tags found in source records: operations, usage, admin, check-in, security, workflow, api, lava.
- Source detail types include: documentation_article, recipe, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Group Type Inheritance Transcript Insight | Rock operations | 02:29 | The Group Type Inheritance RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |
| Group Type Inheritance Transcript Insight | staff training | 01:04 | For staff training and operational readiness, Group Type Inheritance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |
| Group Type Inheritance Transcript Insight | ministry process | 00:50 | For ministry process design, Group Type Inheritance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Archiving a group removes it from normal group-viewer surfaces without deleting it and allows restoration later from the Archived Groups administration page. | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history) |
| official | behavior | Each person in an intermediate region group whose role is marked as a leader receives that region's child-group attendance digest, while the attendance group's own leader is the target of the digest's Email Leader action. | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) |
| official | configuration | The Group Attendance Digest expects a three-level hierarchy: one top parent, leader-bearing region or area groups beneath it, and attendance-recording groups below those regions. | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) |
| official | configuration | Group History becomes available after the Group Type enables history and the Process Group History job has run; its timeline can show group edits and member additions or removals by date. | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history) |
| official | configuration | Rock can add a group at the root of the group tree or as a child of the selected group, but child creation is unavailable when that Group Type does not permit child groups. | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group) |
| official | configuration | Rock communication lists are groups of a specific type; membership can be managed manually or synchronized from data views, so recipient troubleshooting should inspect the underlying group and its sync configuration. | [source](https://community.rockrms.com/documentation/engagement/communications/prepare-for-communications/communication-lists) |
| official | configuration | A member requirement attached to a Group Type applies across that type's groups and can be limited by group role, age classification, or a Data View-defined population. | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) |
| official | configuration | Group Type requirements can allow leader overrides or prevent a person from being added until the requirement is met, enabling enforceable eligibility rules such as completed background checks. | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) |
| rocku-confirmed | configuration | Rapid Attendance Entry is configurable enough to support multiple page variants, so teams can create focused versions for different ministry workflows instead of using one catch-all setup everywhere. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | The block can combine attendance marking with family editing, adding family members, person notes, prayer requests, and workflow launch actions from the same operational screen. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | operational_guidance | Rapid Attendance Entry starts from a selected group and attendance date, with location and schedule values available when the group and attendance context support them. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| rocku-confirmed | source_summary | Rapid Attendance Entry can be used as a fast attendance-entry surface and can also collect related ministry information, such as family updates, notes, prayer requests, and workflow launches, when the block settings enable those actions. | [source](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry) |
| community-reviewed | implementation_pattern | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | For dashboard speed, expensive journey analytics can be calculated into a persisted dataset on a schedule rather than recalculating all historical engagement data on each page load. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | Rock's analytics-enabled tables can be used as a snapshot layer for engagement-style metrics, allowing external reporting tools to query daily counts or trends without repeatedly reconstructing every operational detail. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdREmjz) |
| community-reviewed | operational_guidance | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| More |  | 1 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_documentation`: 76
- `rock_model_map`: 12
- `rock_recipes`: 1
- `rock_rocku`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Groups | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Manage Groups](?Version=v19.0#manage-groups) [Group Types](?Version=v19.0#group-types) [Group Schedules](?Version=v19.0#group-schedules) [Group Scheduler Page](?Version=v19.0#group-scheduler-page) [Group Finder](?Version=v19.0#group-finder) [Group Leader Toolbox](?Version=v19.0#group-leader-toolbox) [Group Placements](?Version=v19.0#group-placements) [Group... | [source](https://community.rockrms.com/documentation/engagement/groups) |
| Group Requirements | rock_documentation | [Intro to Group Requirements](/documentation/engagement/groups/group-requirements/intro-to-group-requirements?Version=v19.0) [Defining Group Requirements](/documentation/engagement/groups/group-requirements/defining-group-requirements?Version=v19.0) [Applying Requirements to Groups](/documentation/engagement/groups/group-requirements/applying-requirements-to-groups?Version=v19.0) [Applying Requirements to Group... | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements) |
| Common Group Jobs | rock_documentation | [Send Attendance Reminders by Group Type](/documentation/engagement/groups/common-group-jobs/send-attendance-reminders-by-group-type?Version=v19.0) [Send Group Attendance Reminders](/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders?Version=v19.0) [Send Group Leader Pending... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs) |
| View Group History | rock_documentation | Now that you have Group History enabled, you can jump to that 40,000ft view. Locate the group in the Group Viewer and click the button. Note **Archived Groups**You can Archive a group instead of deleting it. Archiving removes the group from the Group Viewer and other places where groups can be seen but allows you to restore it later. When a group has been marked as Archived and you want to bring it back go to:... | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history) |
| Applying Requirements to Group Types | rock_documentation | You can also set group member requirements at the Group Type level. This allows you to apply member requirements to all groups of a certain type rather than to each individual group. To access your group types, go to `Admin Tools > Settings > General > Group Types`. Select the group type you want to add requirements to from the Group Type list. In the Group Type Detail screen, expand the Group Requirements section.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) |
| Group RSVP | rock_documentation | [Intro to Group RSVP](/documentation/engagement/groups/group-rsvp/intro-to-group-rsvp?Version=v19.0) [Enable Group RSVP](/documentation/engagement/groups/group-rsvp/enable-group-rsvp?Version=v19.0) [Use the Group Viewer with RSVP](/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp?Version=v19.0) [View RSVP Lists](/documentation/engagement/groups/group-rsvp/view-rsvp-lists?Version=v19.0) [Add... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp) |
| Add a Group | rock_documentation | You can add a new group to the tree by clicking the icon and then selecting the location from the list. Adding a group using *Add Top-Level* will place the group at the root or top of the tree. Selecting Add Child to Selected will place the group under the currently selected group. Note If you have a group selected but `Add Child to Selected` is disabled, then this group type does not allow child groups. See the... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group) |
| Intro to Group History | rock_documentation | As you work with groups—adding and removing members, adjusting schedules and member roles, etc.—there may be times when you want to get a 40,000ft view to see how they're doing. Rock's Group History feature allows you to do just that. Group History takes all of the configurations and changes made to a group and compiles them into timeline and table views that let you easily view the life and health of that group.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history) |
| Use the Group Attendance Digest Email | rock_documentation | The *Group Attendance Digest* is an email containing a summary of attendance information for one or more groups. See the [Common Group Jobs](/documentation/engagement/groups/common-group-jobs) section for information on setting up the Send Group Attendance Digest job. The Group Attendance Digest may not be the right fit for all of your groups. It’s only intended for a specific type of groups structure that we’ll... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) |
| Edit a Group | rock_documentation | Clicking the Edit button from the detail section will allow you to edit information about the group and provide additional configuration settings. The key features of the edit screen are discussed below. 1. **Name**- Update this field to change the name of the group. 2. **Active** - You can inactivate the group by deselecting this checkbox. See [Inactivating a... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) |
| Group Schedule Types | rock_documentation | There are three types of group schedules that can be configured for a group. To help simplify the editing of a group we allow you to configure which of these options are available to groups of each particular type. For instance, you'll probably want to configure your *Small Groups* to only be configured to allow the *Weekly* schedule. You can select which of these options are available for a specific group type... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types) |
| Group Members | rock_documentation | [Intro to Group Members](/documentation/engagement/groups/group-members/intro-to-group-members?Version=v19.0) [Edit a Group Member](/documentation/engagement/groups/group-members/edit-a-group-member?Version=v19.0) [Move Group Members](/documentation/engagement/groups/group-members/move-group-members?Version=v19.0) [Group Member... | [source](https://community.rockrms.com/documentation/engagement/groups/group-members) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Group Member](../../model-map/models/group-member.md) | Group | 19.2.0 | 64 | 30 | 49 | 19 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Assignment](../../model-map/models/group-member-assignment.md) | Group | 19.2.0 | 46 | 15 | 28 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Historical](../../model-map/models/group-member-historical.md) | Group | 19.2.0 | 53 | 22 | 38 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Requirement](../../model-map/models/group-member-requirement.md) | Group | 19.2.0 | 58 | 25 | 41 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Schedule Template](../../model-map/models/group-member-schedule-template.md) | Group | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Workflow Trigger](../../model-map/models/group-member-workflow-trigger.md) | Group | 19.2.0 | 29 | 14 | 22 | 8 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Type](../../model-map/models/group-type.md) | Group | 19.2.0 | 135 | 86 | 113 | 27 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Group Type Role](../../model-map/models/group-type-role.md) | Group | 19.2.0 | 54 | 26 | 39 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group](../../model-map/models/group.md) | Group | 19.2.0 | 115 | 61 | 93 | 32 | 5 | [source](https://community.rockrms.com/ModelMap) |
| [Group Demographic Type](../../model-map/models/group-demographic-type.md) | Group | 19.2.0 | 46 | 17 | 31 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Demographic Value](../../model-map/models/group-demographic-value.md) | Group | 19.2.0 | 48 | 18 | 33 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Historical](../../model-map/models/group-historical.md) | Group | 19.2.0 | 61 | 28 | 46 | 18 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Group.ArchivedByPersonAlias` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.Campus` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.ChatChannelAvatarBinaryFile` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Group.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Subguides

### Group Types

Keywords: `group type, inherited, role`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Group Type Inheritance Transcript Insight | Rock operations | 02:29 | The Group Type Inheritance RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |
| Group Type Inheritance Transcript Insight | staff training | 01:04 | For staff training and operational readiness, Group Type Inheritance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |
| Group Type Inheritance Transcript Insight | ministry process | 00:50 | For ministry process design, Group Type Inheritance should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/groups/group-type-inheritance) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Groups | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Manage Groups](?Version=v19.0#manage-groups) [Group Types](?Version=v19.0#group-types) [Group Schedules](?Version=v19.0#group-schedules) [Group Scheduler Page](?Version=v19.0#group-scheduler-page) [Group Finder](?Version=v19.0#group-finder) [Group Leader Toolbox](?Version=v19.0#group-leader-toolbox) [Group Placements](?Version=v19.0#group-placements) [Group... | [source](https://community.rockrms.com/documentation/engagement/groups) |
| Group Requirements | rock_documentation | [Intro to Group Requirements](/documentation/engagement/groups/group-requirements/intro-to-group-requirements?Version=v19.0) [Defining Group Requirements](/documentation/engagement/groups/group-requirements/defining-group-requirements?Version=v19.0) [Applying Requirements to Groups](/documentation/engagement/groups/group-requirements/applying-requirements-to-groups?Version=v19.0) [Applying Requirements to Group... | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements) |
| Common Group Jobs | rock_documentation | [Send Attendance Reminders by Group Type](/documentation/engagement/groups/common-group-jobs/send-attendance-reminders-by-group-type?Version=v19.0) [Send Group Attendance Reminders](/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders?Version=v19.0) [Send Group Leader Pending... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs) |
| View Group History | rock_documentation | Now that you have Group History enabled, you can jump to that 40,000ft view. Locate the group in the Group Viewer and click the button. Note **Archived Groups**You can Archive a group instead of deleting it. Archiving removes the group from the Group Viewer and other places where groups can be seen but allows you to restore it later. When a group has been marked as Archived and you want to bring it back go to:... | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/view-group-history) |
| Applying Requirements to Group Types | rock_documentation | You can also set group member requirements at the Group Type level. This allows you to apply member requirements to all groups of a certain type rather than to each individual group. To access your group types, go to `Admin Tools > Settings > General > Group Types`. Select the group type you want to add requirements to from the Group Type list. In the Group Type Detail screen, expand the Group Requirements section.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-requirements/applying-requirements-to-group-types) |
| Add a Group | rock_documentation | You can add a new group to the tree by clicking the icon and then selecting the location from the list. Adding a group using *Add Top-Level* will place the group at the root or top of the tree. Selecting Add Child to Selected will place the group under the currently selected group. Note If you have a group selected but `Add Child to Selected` is disabled, then this group type does not allow child groups. See the... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group) |
| Intro to Group History | rock_documentation | As you work with groups—adding and removing members, adjusting schedules and member roles, etc.—there may be times when you want to get a 40,000ft view to see how they're doing. Rock's Group History feature allows you to do just that. Group History takes all of the configurations and changes made to a group and compiles them into timeline and table views that let you easily view the life and health of that group.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-history/intro-to-group-history) |
| Use the Group Attendance Digest Email | rock_documentation | The *Group Attendance Digest* is an email containing a summary of attendance information for one or more groups. See the [Common Group Jobs](/documentation/engagement/groups/common-group-jobs) section for information on setting up the Send Group Attendance Digest job. The Group Attendance Digest may not be the right fit for all of your groups. It’s only intended for a specific type of groups structure that we’ll... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) |
| Edit a Group | rock_documentation | Clicking the Edit button from the detail section will allow you to edit information about the group and provide additional configuration settings. The key features of the edit screen are discussed below. 1. **Name**- Update this field to change the name of the group. 2. **Active** - You can inactivate the group by deselecting this checkbox. See [Inactivating a... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) |
| Group Schedule Types | rock_documentation | There are three types of group schedules that can be configured for a group. To help simplify the editing of a group we allow you to configure which of these options are available to groups of each particular type. For instance, you'll probably want to configure your *Small Groups* to only be configured to allow the *Weekly* schedule. You can select which of these options are available for a specific group type... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types) |

### Group Finder

Keywords: `group finder, location, map`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Groups | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Manage Groups](?Version=v19.0#manage-groups) [Group Types](?Version=v19.0#group-types) [Group Schedules](?Version=v19.0#group-schedules) [Group Scheduler Page](?Version=v19.0#group-scheduler-page) [Group Finder](?Version=v19.0#group-finder) [Group Leader Toolbox](?Version=v19.0#group-leader-toolbox) [Group Placements](?Version=v19.0#group-placements) [Group... | [source](https://community.rockrms.com/documentation/engagement/groups) |
| Add a Group | rock_documentation | You can add a new group to the tree by clicking the icon and then selecting the location from the list. Adding a group using *Add Top-Level* will place the group at the root or top of the tree. Selecting Add Child to Selected will place the group under the currently selected group. Note If you have a group selected but `Add Child to Selected` is disabled, then this group type does not allow child groups. See the... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/add-a-group) |
| Edit a Group | rock_documentation | Clicking the Edit button from the detail section will allow you to edit information about the group and provide additional configuration settings. The key features of the edit screen are discussed below. 1. **Name**- Update this field to change the name of the group. 2. **Active** - You can inactivate the group by deselecting this checkbox. See [Inactivating a... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/edit-a-group) |
| Group Schedule Types | rock_documentation | There are three types of group schedules that can be configured for a group. To help simplify the editing of a group we allow you to configure which of these options are available to groups of each particular type. For instance, you'll probably want to configure your *Small Groups* to only be configured to allow the *Weekly* schedule. You can select which of these options are available for a specific group type... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types) |
| Intro to the Group Finder | rock_documentation | The group finder is another very powerful block that allows your website visitors to search for a group and register quickly. The group finder has been configured on the external website under `Connect > Small Groups`. If configured in the block settings, it allows for searching by the day of the week that the group meets and the study topic. Selecting your criteria and clicking `Search` returns all of the groups... | [source](https://community.rockrms.com/documentation/engagement/groups/group-finder/intro-to-the-group-finder) |
| Intro to the Group Scheduler | rock_documentation | Now the moment of truth…the *Group Scheduler* page. This is where the magic happens. Okay, maybe not actual magic, but it is where the scheduling happens. This page will become very familiar to your staff, since it’s the "magic page" for organizing group members into a location. Note **Obsidian Group Scheduler**The following Group Scheduler documentation shows the newer *Obsidian* version. For the previous version,... | [source](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/intro-to-the-group-scheduler) |
| Use Group Maps | rock_documentation | Clicking the map marker button will take you to an interactive group map showing the members of the group. Depending on the configuration of the group other features may be enabled. If the group has a geopoint (determined through the address geocoding process or by selecting the point on the map) the location of the group will also be present on the map. If the group has a defined geofence this fence will be shown... | [source](https://community.rockrms.com/documentation/engagement/groups/manage-groups/use-group-maps) |
| Group Finder | rock_documentation | [Intro to the Group Finder](/documentation/engagement/groups/group-finder/intro-to-the-group-finder?Version=v19.0) [Group Registration](/documentation/engagement/groups/group-finder/group-registration?Version=v19.0) | [source](https://community.rockrms.com/documentation/engagement/groups/group-finder) |
| Configure Groups for Scheduling | rock_documentation | We're almost to the fun part. The *Group Scheduler* requires some information from the group before it’s ready. In the *Group Viewer*, add *Meeting Details* for every location that needs assigned people. This might be a pretty long list for some groups like the list we see in the screenshot below. At the end of the day, the goal for this page is to have separation and customization for each group. You can break your... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-groups-for-scheduling) |
| View Schedule Analytics | rock_documentation | Scheduling is a process. You plan, they respond, and hopefully, they show up. The *Group Schedule Analytics* page closes the loop. It helps you see how well your teams are responding to requests and fulfilling their commitments. This page relies entirely on the *[Group Scheduler](/documentation/engagement/groups/group-scheduler-page) being*set up, once it is set you can view all sorts of analytics. To access this... | [source](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/view-schedule-analytics) |

### Group Attendance

Keywords: `attendance, meeting, schedule`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Groups | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Manage Groups](?Version=v19.0#manage-groups) [Group Types](?Version=v19.0#group-types) [Group Schedules](?Version=v19.0#group-schedules) [Group Scheduler Page](?Version=v19.0#group-scheduler-page) [Group Finder](?Version=v19.0#group-finder) [Group Leader Toolbox](?Version=v19.0#group-leader-toolbox) [Group Placements](?Version=v19.0#group-placements) [Group... | [source](https://community.rockrms.com/documentation/engagement/groups) |
| Common Group Jobs | rock_documentation | [Send Attendance Reminders by Group Type](/documentation/engagement/groups/common-group-jobs/send-attendance-reminders-by-group-type?Version=v19.0) [Send Group Attendance Reminders](/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders?Version=v19.0) [Send Group Leader Pending... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs) |
| Use the Group Attendance Digest Email | rock_documentation | The *Group Attendance Digest* is an email containing a summary of attendance information for one or more groups. See the [Common Group Jobs](/documentation/engagement/groups/common-group-jobs) section for information on setting up the Send Group Attendance Digest job. The Group Attendance Digest may not be the right fit for all of your groups. It’s only intended for a specific type of groups structure that we’ll... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) |
| Group Schedule Types | rock_documentation | There are three types of group schedules that can be configured for a group. To help simplify the editing of a group we allow you to configure which of these options are available to groups of each particular type. For instance, you'll probably want to configure your *Small Groups* to only be configured to allow the *Weekly* schedule. You can select which of these options are available for a specific group type... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/group-schedule-types) |
| Group Schedules | rock_documentation | [Intro to Group Schedules](/documentation/engagement/groups/group-schedules/intro-to-group-schedules?Version=v19.0) [Group Schedule Types](/documentation/engagement/groups/group-schedules/group-schedule-types?Version=v19.0) [Configure Group Schedule](/documentation/engagement/groups/group-schedules/configure-group-schedule?Version=v19.0) [Configure Groups for... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules) |
| Send Group Attendance Reminders | rock_documentation | This job is very similar to the *Send Attendance Reminders for Group Type* job discussed [in this article](/documentation/engagement/groups/common-group-jobs/send-attendance-reminders-by-group-type). This job sends a reminder to group leaders about entering attendance for their group meeting. The key difference between the two jobs is that *Send Attendance Reminders for Group Type* requires a group type, while *Send... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-reminders) |
| Send Group Attendance Digest | rock_documentation | This job sends a summary of group attendance information to certain group *Leaders*. See the [Group Attendance Digest](/documentation/engagement/groups/group-attendance) section for more on the group structure requirements for this job. When you’re configuring this job, pay close attention to the following configuration options: * **Parent Group**: The job needs to know the highest-level parent group in the group... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/send-group-attendance-digest) |
| Group Scheduler Page | rock_documentation | [Intro to the Group Scheduler](/documentation/engagement/groups/group-scheduler-page/intro-to-the-group-scheduler?Version=v19.0) [View Schedule Analytics](/documentation/engagement/groups/group-scheduler-page/view-schedule-analytics?Version=v19.0) [Use the Schedule Status Board](/documentation/engagement/groups/group-scheduler-page/use-the-schedule-status-board?Version=v19.0) [View Group Schedule... | [source](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page) |
| Group Attendance | rock_documentation | [Intro to Group Attendance](/documentation/engagement/groups/group-attendance/intro-to-group-attendance?Version=v19.0) [Configure Group Attendance](/documentation/engagement/groups/group-attendance/configure-group-attendance?Version=v19.0) [Entering Attendance](/documentation/engagement/groups/group-attendance/entering-attendance?Version=v19.0) [Configure Attendance... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance) |
| View Group Attendance Reports | rock_documentation | This job will create new Person attributes to track a person's *First Attended Date*, *Last Attended Date*, *Times Attended in Last 12 Months* and/or *Times Attended in Last 16 Weeks* for groups specified by a Data View. These attributes can be manually assigned categories and security as needed. This job considers all attendance in the specified groups, regardless of whether the person is currently an active member... | [source](https://community.rockrms.com/documentation/engagement/groups/common-group-jobs/view-group-attendance-reports) |


## Source Lifecycle

- Official article records routed here: `89`
- Upstream check range: `2026-08-12T06:18:41+00:00` through `2026-08-12T06:18:46+00:00`
- Source-native typed articles: `2` of `89`
- Legacy source summaries retired: `2`; still active: `87`
- Migration status: `partial`

A recent source check or concept rebuild does not imply that every legacy summary has been replaced by reviewed source-native artifacts.

## Rebuild Dependencies

- Source records: `91`
- Approved claims: `19`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
