---
id: concept-serving-volunteer-ops
title: Serving And Volunteer Operations
generated: true
last_built: 2026-08-10T22:17:14+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
source_freshness_status: complete
source_last_checked_at: 2026-08-10T21:32:58+00:00
source_native_migration_status: partial
source_native_article_coverage: 1/28
legacy_summary_retirement_coverage: 2/28
depends_on_topics:
  - groups
  - scheduling
  - locations
  - check-in
  - communications
  - workflows
  - people
  - security
---

# Serving And Volunteer Operations

Serving teams, volunteer schedules, requirements, confirmations, attendance, volunteer communications, and follow-up.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Serving And Volunteer Operations` spans groups, scheduling, locations, check-in, communications, workflows. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_podcast_rss, rock_community_hubs, rock_youtube, rock_documentation, rock_recipes, rock_rocku.
- Related tags found in source records: usage, check-in, workflow, operations, security, admin, training, sql.
- Source detail types include: developer_doc, documentation_article, question, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | release readiness | 00:25 | Release-roadmap podcast material is useful as historical context but should not override current release notes when agents answer version-specific questions. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | volunteer scheduling | 01:11 | Volunteer scheduling was framed as a major roadmap item, so serving and group-scheduling guides should route scheduling questions through both release history and current model/feature documentation. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | Wi-Fi presence | 02:01 | Wi-Fi presence connects campus network signals to person attendance-style insight, which makes data ownership, vendor behavior, and privacy review part of the implementation guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Media Watch Transcript Insight | guest retention | 02:33 | First-time guest retention is a useful ministry health signal when it is measured consistently and connected to the church's actual follow-up process. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | benchmarking | 02:49 | Retention benchmarks can help leadership interpret results, but local context and data definitions should be documented before comparing one church's numbers to another's. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | connection workflow | 03:00 | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | metric framing | 01:25 | Spiritual-growth dashboards should combine several observable practices rather than rely on a single proxy metric that leadership may overinterpret. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) |
| Media Watch Transcript Insight | group and serving measures | 02:47 | Group participation, serving involvement, giving patterns, and attendance can be useful dashboard inputs when each is framed as an engagement signal with known limitations. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) |
| Media Watch Transcript Insight | leadership dashboard design | 01:52 | A leadership-facing Rock dashboard should make metric definitions explicit so teams know which values are current-state snapshots, historical trends, or ministry-specific targets. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) |
| Media Watch Transcript Insight | youth digital strategy | 03:24 | Youth digital strategy should be designed around relational ministry outcomes, not only channel choice or content volume. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | ministry alignment | 04:38 | Lessons from youth digital ministry can inform adult services and broader church mobile strategy when they are translated into repeatable Rock-backed workflows. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | community practice | 03:12 | Informal peer review is valuable for youth digital work because teams can compare what is actually creating connection rather than relying on assumptions about student behavior. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | LMS migration | 02:29 | When moving from another LMS into Rock, plan for differences in platform logic instead of assuming videos and lessons can be imported without redesign. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | media reuse | 04:02 | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | volunteer training | 03:41 | LMS is most valuable when the church treats it as part of a broader volunteer readiness system, not just a content repository. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | LMS adoption | 00:11 | Early LMS work should start with a few clear training use cases, such as volunteer or staff onboarding, before attempting a large content migration. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | content reuse | 01:42 | Existing teaching series or training videos can become LMS content, but teams should still design the course path, completion expectations, and follow-up communication around the learner. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | ministry learning paths | 02:23 | A binge-style content idea can become a structured learning path when the church defines sequence, purpose, and completion signals rather than only embedding videos. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | daily engagement | 02:23 | A daily mobile experience can make the app valuable beyond weekend utility by giving people a simple reason to return for scripture, prayer, or ministry stories. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPb9Y9lR4) |
| Media Watch Transcript Insight | missions and prayer | 02:14 | Prayer or missions content can be designed as a lightweight daily action that connects app users to people and ministry work they may not otherwise see. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPb9Y9lR4) |
| Media Watch Transcript Insight | mobile app open | 01:41 | The first screen after app open should be intentionally chosen because it can shape whether users treat the app as a ministry companion or only a transactional tool. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPb9Y9lR4) |
| Media Watch Transcript Insight | reporting suite design | 06:04 | A mature reporting suite can separate executive dashboards, campus or ministry dashboards, and functional operational dashboards so each audience sees the level of detail needed for its decisions. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | executive dashboards | 12:09 | Executive dashboards work better when they expose a small set of organization-wide goals with clear current values, goal values, and status indicators instead of hiding many rolled-up metrics behind ambiguous scores. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | campus dashboards | 14:24 | Campus dashboards should help leaders compare current year-to-date values against both goals and prior-year context, while leaving deeper campus-specific measures available without crowding the organization-wide dashboard. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | ministry dashboards | 21:16 | Ministry and program dashboards should avoid standalone numbers when possible; compare measures to goals, historical baselines, or funnels so teams can interpret whether a result needs action. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | connection requests | 39:51 | Functional dashboards such as connection-request views may justify live database connections when leaders need up-to-date queues, while slower-changing attendance or giving dashboards can usually use scheduled refreshes. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | report access | 49:32 | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| Media Watch Transcript Insight | LMS structure | 02:52 | Rock LMS organizes training into programs, courses, class instances, learning plans, activities, and learning participants, with the program deciding whether the experience is on-demand or academic-calendar based. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| Media Watch Transcript Insight | activity design | 07:17 | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| Media Watch Transcript Insight | workflow integration | 26:43 | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| Media Watch Transcript Insight | communications beta | 42:38 | The communications beta wizard introduces topic tagging and reachable-audience counts by medium, helping senders choose email, SMS, or push based on actual contactability rather than only the size of a communication list. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| Media Watch Transcript Insight | email editor | 51:40 | Reusable communication sections and global style controls can reduce template drift when churches standardize common layouts, buttons, text styles, columns, and Lava/code blocks. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| Outreach Toolbox is Here in v19 Transcript Insight | Outreach Toolbox availability | 00:00 | Outreach Toolbox is presented as a Rock Mobile v19 signed-in experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Verify current mobile-shell support, page placement and authentication requirements before rollout. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=0s) |
| Outreach Toolbox is Here in v19 Transcript Insight | outreach schedules and reminders | 01:04 | Outreach Toolbox onboarding lets a signed-in person choose assignment days and reminder preferences, while configurable jobs define reminder time-of-day values. Test job scheduling and push-notification delivery in the target mobile environment. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s) |
| Outreach Toolbox is Here in v19 Transcript Insight | outreach touchpoint lifecycle | 07:56 | Outreach Toolbox can track contact-specific prayer and connection cadences, completed touchpoint history and periodic pulse updates, with configurable milestone prompts. Review who can see the contact data and which block settings are enabled before ministry use. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s) |
| Your People are Ministers on the Ground with the Outreach Toolbox Transcript Insight | Outreach Toolbox dashboard | 00:00 | The Outreach Toolbox dashboard can surface people due for outreach and prayer touchpoints, helping a signed-in user see today's relationship-care actions. Verify current mobile availability and permissions before relying on it operationally. | [source](https://www.youtube.com/shorts/c6T9Ha13jKE) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | operational_guidance | Train and activate staff before expecting them to train volunteers. Staff-first sequencing creates training multipliers and reduces the risk that inconsistent volunteer practices damage data quality. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | release_caveat | Outreach Toolbox is presented as a Rock Mobile v19 signed-in experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Verify current mobile-shell support, page placement and authentication requirements before rollout. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| official | release_caveat | The Outreach Toolbox dashboard can surface people due for outreach and prayer touchpoints, helping a signed-in user see today's relationship-care actions. Verify current mobile availability and permissions before relying on it operationally. | [source](https://www.youtube.com/shorts/c6T9Ha13jKE) |
| official | release_caveat | Outreach Toolbox onboarding lets a signed-in person choose assignment days and reminder preferences, while configurable jobs define reminder time-of-day values. Test job scheduling and push-notification delivery in the target mobile environment. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| official | release_caveat | Outreach Toolbox can track contact-specific prayer and connection cadences, completed touchpoint history and periodic pulse updates, with configurable milestone prompts. Review who can see the contact data and which block settings are enabled before ministry use. | [source](https://www.youtube.com/watch?v=LNcx8t0mlQ4) |
| community-reviewed | implementation_pattern | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | When embedding Power BI or similar reports in Rock, pair report pages with appropriate Rock security roles and licensing checks so only authorized, licensed users can access the embedded dashboards. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz) |
| community-reviewed | operational_guidance | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Rock LMS organizes training into programs, courses, class instances, learning plans, activities, and learning participants, with the program deciding whether the experience is on-demand or academic-calendar based. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |

## Source Coverage

- `rock_community_hubs`: 8
- `rock_core_release_notes`: 2
- `rock_documentation`: 27
- `rock_mobile_docs`: 1
- `rock_model_map`: 12
- `rock_podcast_rss`: 1
- `rock_qa`: 1
- `rock_recipes`: 8
- `rock_rocku`: 27
- `rock_youtube`: 2
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Skills Rubric | triumph_resources | Level 1: Foundational Awareness Basic understanding and vocabulary; competently follows guidance of experienced team members. Understands the core components of Azure (VMs, SQL, Resource Groups, Networking). Can follow step-by-step documentation to create or configure basic Azure resources (e.g., create VM, attach disk). Follows all Triumph’s Azure naming conventions and resource group structure. Can navigate the... | [source](https://www.triumph.tech/resources/skills-rubric) |
| Add RSVP Occurrences | rock_documentation | Let’s look at how to add an occurrence to the RSVP List. You'll need to have at least one occurrence set up for the group before you can start sending your RSVP emails. 1. **Name** - You can optionally set a unique name for an occurrence. This applies only to the occurrence being viewed. Invitees will see the name you provide on the external website when they *Accept* or *Decline*. 2. **Date** - Set the date of the... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) |
| Add RSVP Request to Email | rock_documentation | Now that we have an occurrence set up, we’re ready to send out some invitations. Adding an RSVP request to an e-mail is as simple as clicking and dragging the RSVP tool button (look for the icon) into your email. If you’re not sure how to get to this point, check out the [Communication Wizard](/documentation/engagement/communications/send-a-communication/communication-wizard) article in the Communication guide.... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-request-to-email) |
| Attendance | rock_documentation | [Use Attendance Analytics](/documentation/church-management/check-in/attendance/use-attendance-analytics?Version=v19.0) [Rapid Attendance Entry](/documentation/church-management/check-in/attendance/rapid-attendance-entry?Version=v19.0) [Attendance Self Entry](/documentation/church-management/check-in/attendance/attendance-self-entry?Version=v19.0) | [source](https://community.rockrms.com/documentation/church-management/check-in/attendance) |
| Attendance Self Entry | rock_documentation | With the advancement of online services, getting accurate engagement data can be a challenge. To address this need, Rock lets attendees report their own attendance from your external site. All a person needs to do is check a few boxes to indicate who’s watching the service with them. Pictured above, Ted is watching the service at home with Cindy and Alex. Noah is at grandma’s house this weekend, so isn’t selected.... | [source](https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry) |
| Configure Attendance Reminders | rock_documentation | You can also configure Rock to send a communication to the group leader on the day that their group meets to remind them to take attendance. This communication will include a link to take them straight to the attendance detail screen. Since each group leader gets an individual communication, we have enabled this link to not require a login to help simplify the process (either the *Manage Members* or the *Edit*... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-attendance-reminders) |
| Configure Group Attendance | rock_documentation | Before a group can take attendance, its group type must first be configured to enable attendance tracking under `Admin Tools > Settings > General > Group Types`. From here you should select the group type you'd like to configure check-in for. Under the *Attendance / Check-in* tab enable the setting *Takes Attendance*. While this one setting is all you need to enable the attendance features, there are a couple of... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance) |
| Configure Group Schedule | rock_documentation | This article delves into the administrative setup and management capabilities of the Group Scheduling feature. We’ll show you how that all gets set up, and what Group Scheduling looks like on the administrative side. Before starting to schedule volunteers, you’ll need to configure things like locations and schedules. Locations ensure volunteers know where they're needed, while Schedules pinpoint when their help is... | [source](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule) |
| Configure RSVP Reminder Job | rock_documentation | The *Send Rsvp Reminders* job will send a reminder to people who have accepted an RSVP invitation. Those who have declined or who haven’t responded won’t receive a reminder. The job is ready for you to use out of the box, but it must be manually configured and is intended to be run daily. It will use the *RSVP Reminder System Communication* for the content, as configured at either the group or group type level. If... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/configure-rsvp-reminder-job) |
| Enable Group RSVP | rock_documentation | The RSVP function is enabled in group type settings, making RSVP features available to any groups within that type. All RSVP features are tied directly to a group. That means you must have a group created before you can use RSVP. The group doesn't need to have any members, but it needs to exist so individuals who accept your RSVP can be added to it. To enable RSVP for a group type, navigate to `Admin Tools > General... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp) |
| Entering Attendance | rock_documentation | ## Internal Attendance Features There are several ways to collect group attendance. The first is to use the internal attendance features built into the Group Viewer under `People > Group Viewer`. You'll notice an attendance button on the group details block for groups that are configured to take attendance. Selecting this option will bring up the group attendance grid. This grid lists the previously entered... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance) |
| Group Attendance | rock_documentation | [Intro to Group Attendance](/documentation/engagement/groups/group-attendance/intro-to-group-attendance?Version=v19.0) [Configure Group Attendance](/documentation/engagement/groups/group-attendance/configure-group-attendance?Version=v19.0) [Entering Attendance](/documentation/engagement/groups/group-attendance/entering-attendance?Version=v19.0) [Configure Attendance... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Analytics Fact Attendance](../../model-map/models/analytics-fact-attendance.md) | Reporting | 19.2.0 | 51 | 37 | 44 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Analytics Source Attendance](../../model-map/models/analytics-source-attendance.md) | Reporting | 19.2.0 | 40 | 26 | 33 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Attendance](../../model-map/models/attendance.md) | Event | 19.2.0 | 82 | 39 | 65 | 26 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Attendance Check In Session](../../model-map/models/attendance-check-in-session.md) | Event | 19.2.0 | 21 | 7 | 14 | 7 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Attendance Code](../../model-map/models/attendance-code.md) | Event | 19.2.0 | 20 | 7 | 12 | 5 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Attendance Occurrence](../../model-map/models/attendance-occurrence.md) | Event | 19.2.0 | 64 | 27 | 47 | 20 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Campus Schedule](../../model-map/models/campus-schedule.md) | Core | 19.2.0 | 43 | 13 | 28 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Requirement](../../model-map/models/group-member-requirement.md) | Group | 19.2.0 | 58 | 25 | 41 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Member Schedule Template](../../model-map/models/group-member-schedule-template.md) | Group | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Requirement](../../model-map/models/group-requirement.md) | Group | 19.2.0 | 52 | 19 | 37 | 18 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Requirement Type](../../model-map/models/group-requirement-type.md) | Group | 19.2.0 | 65 | 33 | 50 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Group Schedule Exclusion](../../model-map/models/group-schedule-exclusion.md) | Group | 19.2.0 | 40 | 12 | 25 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Campus Schedule.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.Campus` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Campus Schedule.ModifiedAuditValuesAlreadyUpdated` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 19.3 | Group | Fixed an issue with the RSVP Response block where the heading would show the generic "RSVP for Event" text instead of the Attendance Occurrence Name when accessed through the Accept or Decline link in an RSVP email. Fixes: #6872 | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Group | Fixed the Send Attendance Reminder job so Group leaders still receive reminders when a Group only has scheduling/RSVP-related Attendance records. The job now treats those tracking records as not being “attendance” and only suppresses reminders when at least one individual attended or the Group was marked as did not meet. Fixes: #6685 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Serving Teams And Roles

Keywords: `serving team, serve team, group type, group role, team member, volunteer`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | release readiness | 00:25 | Release-roadmap podcast material is useful as historical context but should not override current release notes when agents answer version-specific questions. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | volunteer scheduling | 01:11 | Volunteer scheduling was framed as a major roadmap item, so serving and group-scheduling guides should route scheduling questions through both release history and current model/feature documentation. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | Wi-Fi presence | 02:01 | Wi-Fi presence connects campus network signals to person attendance-style insight, which makes data ownership, vendor behavior, and privacy review part of the implementation guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Media Watch Transcript Insight | youth digital strategy | 03:24 | Youth digital strategy should be designed around relational ministry outcomes, not only channel choice or content volume. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | ministry alignment | 04:38 | Lessons from youth digital ministry can inform adult services and broader church mobile strategy when they are translated into repeatable Rock-backed workflows. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | community practice | 03:12 | Informal peer review is valuable for youth digital work because teams can compare what is actually creating connection rather than relying on assumptions about student behavior. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | LMS migration | 02:29 | When moving from another LMS into Rock, plan for differences in platform logic instead of assuming videos and lessons can be imported without redesign. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | media reuse | 04:02 | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | volunteer training | 03:41 | LMS is most valuable when the church treats it as part of a broader volunteer readiness system, not just a content repository. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | LMS adoption | 00:11 | Early LMS work should start with a few clear training use cases, such as volunteer or staff onboarding, before attempting a large content migration. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | content reuse | 01:42 | Existing teaching series or training videos can become LMS content, but teams should still design the course path, completion expectations, and follow-up communication around the learner. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | ministry learning paths | 02:23 | A binge-style content idea can become a structured learning path when the church defines sequence, purpose, and completion signals rather than only embedding videos. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | rock_podcast_rss | This RockCast update is useful public roadmap context: v8 was discussed as moving toward alpha testing, v9 was framed around volunteer scheduling, and Wi-Fi presence was described as an integration that maps campus Wi-Fi signals into Rock attendance-style insight. The episode also highlights privacy and data-ownership concerns when external services participate in presence tracking. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session gives public-safe context for youth digital strategy and mobile engagement. It discusses how youth ministry digital work should connect app, group, volunteer, and communication practices instead of treating mobile or social channels as separate from discipleship and relational ministry. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/4xB9KJEl8W) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session adds implementation-oriented LMS guidance from a church activating the LMS engine and migrating content from another learning platform. It is useful for planning how existing videos and course material can be restructured into Rock LMS while preserving the ministry logic of training paths, groups, and volunteer readiness. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session adds practical LMS guidance from churches beginning to build training content in Rock. It treats LMS as a way to deliver volunteer and staff training, reuse existing teaching assets, and pair content with communications that invite people into structured learning rather than leaving training scattered across unrelated pages. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Configure Group Attendance | rock_documentation | Before a group can take attendance, its group type must first be configured to enable attendance tracking under `Admin Tools > Settings > General > Group Types`. From here you should select the group type you'd like to configure check-in for. Under the *Attendance / Check-in* tab enable the setting *Takes Attendance*. While this one setting is all you need to enable the attendance features, there are a couple of... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance) |
| Managing Schedule Coordinator Notifications | rock_documentation | Ever been caught off guard by a last-minute volunteer change? Picture this: It’s Sunday morning, the next service is starting soon, and a crucial volunteer has dropped out. As the *Schedule Coordinator* for your serving team, you'll be the first to know, giving you time to adjust and ensure everything runs smoothly. The Schedule Coordinator can be notified when a volunteer accepts or declines a serving opportunity,... | [source](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications) |
| Enable Group RSVP | rock_documentation | The RSVP function is enabled in group type settings, making RSVP features available to any groups within that type. All RSVP features are tied directly to a group. That means you must have a group created before you can use RSVP. The group doesn't need to have any members, but it needs to exist so individuals who accept your RSVP can be added to it. To enable RSVP for a group type, navigate to `Admin Tools > General... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp) |
| Problem to Solve | rock_recipes | 2 View Serving Schedule on External Page Shared by Aiden Bailey , Mosaic Christian Church one year ago 14.4 Group, Serving Intermediate Problem to Solve Viewing the serving schedule isn't very accessible on the external page. You have to go to the internal site, have access to the schedule status board, navigate to the team you're trying to view, and then look at it. To do that, every volunteer needs the proper... | [source](https://community.rockrms.com/recipes/459) |
| Use the Group Viewer with RSVP | rock_documentation | After you’ve enabled RSVP for a group type, you’ll see a couple of changes when viewing groups of that type from the *Group Viewer* page. First, you’ll notice the addition of a new icon that will take you to the *Group RSVP List* page, where you can view or add occurrences. We’ll talk more about occurrences in the [RSVP Occurrences](/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) article. Second,... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp) |
| Group Member Schedule Templates - adding 5th week and using Auto Schedule | rock_recipes | 1 Group Member Schedule Templates - adding 5th week and using Auto Schedule Shared by Cecillia Fountain , Centerpoint Church 3 years ago 9.0 Serving, Group Beginner The main reason to create Group Member Schedule Templates is to use the "Auto-Schedule" button in the Group Scheduler . The solutions below are designed to work with Auto-Scheduling and (for the most part) will not need to be maintained. Rock Core does... | [source](https://community.rockrms.com/recipes/356) |

### Schedules And Confirmations

Keywords: `schedule, scheduling, confirmation, decline, RSVP, reminder, serving schedule`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | release readiness | 00:25 | Release-roadmap podcast material is useful as historical context but should not override current release notes when agents answer version-specific questions. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | volunteer scheduling | 01:11 | Volunteer scheduling was framed as a major roadmap item, so serving and group-scheduling guides should route scheduling questions through both release history and current model/feature documentation. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Episode 40: v8 and more team updates Transcript Insight | Wi-Fi presence | 02:01 | Wi-Fi presence connects campus network signals to person attendance-style insight, which makes data ownership, vendor behavior, and privacy review part of the implementation guidance. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | rock_podcast_rss | This RockCast update is useful public roadmap context: v8 was discussed as moving toward alpha testing, v9 was framed around volunteer scheduling, and Wi-Fi presence was described as an integration that maps campus Wi-Fi signals into Rock attendance-style insight. The episode also highlights privacy and data-ownership concerns when external services participate in presence tracking. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Your People are Ministers on the Ground with the Outreach Toolbox Transcript Insight | rock_youtube | This official short demonstrates the Outreach Toolbox dashboard as a reminder surface for due outreach and prayer touchpoints. Use the full v19 walkthrough and current mobile documentation for configuration details. | [source](https://www.youtube.com/shorts/c6T9Ha13jKE) |
| Group RSVP | rock_documentation | [Intro to Group RSVP](/documentation/engagement/groups/group-rsvp/intro-to-group-rsvp?Version=v19.0) [Enable Group RSVP](/documentation/engagement/groups/group-rsvp/enable-group-rsvp?Version=v19.0) [Use the Group Viewer with RSVP](/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp?Version=v19.0) [View RSVP Lists](/documentation/engagement/groups/group-rsvp/view-rsvp-lists?Version=v19.0) [Add... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp) |
| Configure Group Attendance | rock_documentation | Before a group can take attendance, its group type must first be configured to enable attendance tracking under `Admin Tools > Settings > General > Group Types`. From here you should select the group type you'd like to configure check-in for. Under the *Attendance / Check-in* tab enable the setting *Takes Attendance*. While this one setting is all you need to enable the attendance features, there are a couple of... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance) |
| Managing Schedule Coordinator Notifications | rock_documentation | Ever been caught off guard by a last-minute volunteer change? Picture this: It’s Sunday morning, the next service is starting soon, and a crucial volunteer has dropped out. As the *Schedule Coordinator* for your serving team, you'll be the first to know, giving you time to adjust and ensure everything runs smoothly. The Schedule Coordinator can be notified when a volunteer accepts or declines a serving opportunity,... | [source](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications) |
| Enable Group RSVP | rock_documentation | The RSVP function is enabled in group type settings, making RSVP features available to any groups within that type. All RSVP features are tied directly to a group. That means you must have a group created before you can use RSVP. The group doesn't need to have any members, but it needs to exist so individuals who accept your RSVP can be added to it. To enable RSVP for a group type, navigate to `Admin Tools > General... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp) |
| Problem to Solve | rock_recipes | 2 View Serving Schedule on External Page Shared by Aiden Bailey , Mosaic Christian Church one year ago 14.4 Group, Serving Intermediate Problem to Solve Viewing the serving schedule isn't very accessible on the external page. You have to go to the internal site, have access to the schedule status board, navigate to the team you're trying to view, and then look at it. To do that, every volunteer needs the proper... | [source](https://community.rockrms.com/recipes/459) |
| Use the Group Viewer with RSVP | rock_documentation | After you’ve enabled RSVP for a group type, you’ll see a couple of changes when viewing groups of that type from the *Group Viewer* page. First, you’ll notice the addition of a new icon that will take you to the *Group RSVP List* page, where you can view or add occurrences. We’ll talk more about occurrences in the [RSVP Occurrences](/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) article. Second,... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp) |
| Group Member Schedule Templates - adding 5th week and using Auto Schedule | rock_recipes | 1 Group Member Schedule Templates - adding 5th week and using Auto Schedule Shared by Cecillia Fountain , Centerpoint Church 3 years ago 9.0 Serving, Group Beginner The main reason to create Group Member Schedule Templates is to use the "Auto-Schedule" button in the Group Scheduler . The solutions below are designed to work with Auto-Scheduling and (for the most part) will not need to be maintained. Rock Core does... | [source](https://community.rockrms.com/recipes/356) |
| Add RSVP Occurrences | rock_documentation | Let’s look at how to add an occurrence to the RSVP List. You'll need to have at least one occurrence set up for the group before you can start sending your RSVP emails. 1. **Name** - You can optionally set a unique name for an occurrence. This applies only to the occurrence being viewed. Invitees will see the name you provide on the external website when they *Accept* or *Decline*. 2. **Date** - Set the date of the... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) |

### Volunteer Requirements

Keywords: `requirement, requirements, background check, training, eligibility`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | LMS migration | 02:29 | When moving from another LMS into Rock, plan for differences in platform logic instead of assuming videos and lessons can be imported without redesign. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | media reuse | 04:02 | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | volunteer training | 03:41 | LMS is most valuable when the church treats it as part of a broader volunteer readiness system, not just a content repository. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | LMS adoption | 00:11 | Early LMS work should start with a few clear training use cases, such as volunteer or staff onboarding, before attempting a large content migration. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | content reuse | 01:42 | Existing teaching series or training videos can become LMS content, but teams should still design the course path, completion expectations, and follow-up communication around the learner. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Media Watch Transcript Insight | ministry learning paths | 02:23 | A binge-style content idea can become a structured learning path when the church defines sequence, purpose, and completion signals rather than only embedding videos. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session adds implementation-oriented LMS guidance from a church activating the LMS engine and migrating content from another learning platform. It is useful for planning how existing videos and course material can be restructured into Rock LMS while preserving the ministry logic of training paths, groups, and volunteer readiness. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session adds practical LMS guidance from churches beginning to build training content in Rock. It treats LMS as a way to deliver volunteer and staff training, reuse existing teaching assets, and pair content with communications that invite people into structured learning rather than leaving training scattered across unrelated pages. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| Group Attendance Training | rock_rocku | Group Attendance Jon Edmiston Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group Scheduling -... | [source](https://community.rockrms.com/rocku/groups/group-attendance) |
| Group RSVP Occurrences Training | rock_rocku | Group RSVP Occurrences Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group Scheduling -... | [source](https://community.rockrms.com/rocku/groups/group-rsvp-occurrences) |
| Group RSVP Overview Training | rock_rocku | Group RSVP Overview Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group Scheduling -... | [source](https://community.rockrms.com/rocku/groups/group-rsvp-overview) |
| Setting up Group RSVP Training | rock_rocku | Setting up Group RSVP Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group Scheduling -... | [source](https://community.rockrms.com/rocku/groups/setting-up-group-rsvp) |
| Group Scheduling - Analytics Training | rock_rocku | Group Scheduling - Analytics Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group... | [source](https://community.rockrms.com/rocku/groups/group-scheduling-analytics) |
| Group Scheduling - Meeting Details Training | rock_rocku | Group Scheduling - Meeting Details Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group... | [source](https://community.rockrms.com/rocku/groups/group-scheduling-meeting-details) |
| Group Scheduling - Overview Training | rock_rocku | Group Scheduling - Overview Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview 4:29 Group... | [source](https://community.rockrms.com/rocku/groups/group-scheduling-overview) |
| Group Scheduling Roster and Communications Training | rock_rocku | Group Scheduling Roster and Communications Cullen McCoy Experience Mode Trailblazer Essentials Trailblazer Group Viewer 6:21 Group Details 9:27 Group Attendance 2:43 Group Types 26:16 Group Type Inheritance 3:08 Group History 5:10 Group Location 2:53 Group Purposes 3:36 Alternate Placements 2:55 Group Requirements 6:57 Group Security 8:53 Extending Groups 7:51 Group Administrator 3:47 Group Scheduling - Overview... | [source](https://community.rockrms.com/rocku/groups/group-scheduling-roster-and-communications) |

### Attendance And Follow-Up

Keywords: `attendance, check-in, follow-up, no show, serving attendance`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Media Watch Transcript Insight | guest retention | 02:33 | First-time guest retention is a useful ministry health signal when it is measured consistently and connected to the church's actual follow-up process. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | benchmarking | 02:49 | Retention benchmarks can help leadership interpret results, but local context and data definitions should be documented before comparing one church's numbers to another's. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | connection workflow | 03:00 | Rock connection work should use retention data to prioritize human follow-up, volunteer assignment, and next-step invitations rather than only reporting historical attendance. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Episode 40: v8 and more team updates Transcript Insight | rock_podcast_rss | This RockCast update is useful public roadmap context: v8 was discussed as moving toward alpha testing, v9 was framed around volunteer scheduling, and Wi-Fi presence was described as an integration that maps campus Wi-Fi signals into Rock attendance-style insight. The episode also highlights privacy and data-ownership concerns when external services participate in presence tracking. | [source](https://shows.acast.com/rock-cast/episodes/episode-40-v8-and-more-team-updates) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub session gives public-safe guidance for using first-time guest and retention measures as a connection strategy input. It emphasizes defining the few metrics that matter, comparing retention patterns over time, and using data to improve follow-up without replacing the relational work of connecting new people to ministry. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/KQmK8D2l8G) |
| Media Watch Transcript Insight | rock_community_hubs | This Digital Strategy Hub discussion gives public-safe guidance for measuring spiritual growth without reducing discipleship to a single score. The session compares measures such as group involvement, serving, giving, attendance, and engagement trends, and emphasizes dashboards that help leadership ask better ministry questions instead of treating metrics as proof of spiritual maturity. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/QvPN40xmA2) |
| Group Attendance | rock_documentation | [Intro to Group Attendance](/documentation/engagement/groups/group-attendance/intro-to-group-attendance?Version=v19.0) [Configure Group Attendance](/documentation/engagement/groups/group-attendance/configure-group-attendance?Version=v19.0) [Entering Attendance](/documentation/engagement/groups/group-attendance/entering-attendance?Version=v19.0) [Configure Attendance... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance) |
| Configure Group Attendance | rock_documentation | Before a group can take attendance, its group type must first be configured to enable attendance tracking under `Admin Tools > Settings > General > Group Types`. From here you should select the group type you'd like to configure check-in for. Under the *Attendance / Check-in* tab enable the setting *Takes Attendance*. While this one setting is all you need to enable the attendance features, there are a couple of... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance) |
| Entering Attendance | rock_documentation | ## Internal Attendance Features There are several ways to collect group attendance. The first is to use the internal attendance features built into the Group Viewer under `People > Group Viewer`. You'll notice an attendance button on the group details block for groups that are configured to take attendance. Selecting this option will bring up the group attendance grid. This grid lists the previously entered... | [source](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance) |
| Attendance | rock_documentation | [Use Attendance Analytics](/documentation/church-management/check-in/attendance/use-attendance-analytics?Version=v19.0) [Rapid Attendance Entry](/documentation/church-management/check-in/attendance/rapid-attendance-entry?Version=v19.0) [Attendance Self Entry](/documentation/church-management/check-in/attendance/attendance-self-entry?Version=v19.0) | [source](https://community.rockrms.com/documentation/church-management/check-in/attendance) |
| Rapid Attendance Entry | rock_documentation | The *Rapid Attendance Entry* block allows you to record attendance for lots of people very quickly. This could come in handy for certain situations, such as checking a lot of people in for a worship service and wanting to do so as fast as possible. *Rapid Attendance Entry* can also be very useful outside of attendance. It's great for entering communication cards, prayer cards or other information you might collect... | [source](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry) |
| Volunteer Generosity | rock_documentation | This report is used to compare and capture insights on your volunteer team and their giving. It shows which volunteers have donated within a specific time range and lets you filter by Attendance Date Ranges, Campuses, and Teams. This helps you understand how volunteering relates to financial giving. Note **Just a Note**This tool tracks the connection between volunteers' giving and their service, not their exact... | [source](https://community.rockrms.com/documentation/church-management/finance/finance-reports/volunteer-generosity) |
| Add RSVP Occurrences | rock_documentation | Let’s look at how to add an occurrence to the RSVP List. You'll need to have at least one occurrence set up for the group before you can start sending your RSVP emails. 1. **Name** - You can optionally set a unique name for an occurrence. This applies only to the occurrence being viewed. Invitees will see the name you provide on the external website when they *Accept* or *Decline*. 2. **Date** - Set the date of the... | [source](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) |


## Source Lifecycle

- Official article records in the bounded guide selection: `28`
- Upstream check range: `2026-07-10T17:16:12+00:00` through `2026-08-10T21:32:58+00:00`
- Source-native typed articles: `1` of `28`
- Legacy source summaries retired: `2`; still active: `26`
- Migration status: `partial`

A recent source check or concept rebuild does not imply that every legacy summary has been replaced by reviewed source-native artifacts.

## Rebuild Dependencies

- Source records: `91`
- Approved claims: `10`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
