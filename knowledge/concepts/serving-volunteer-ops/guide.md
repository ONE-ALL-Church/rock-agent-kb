---
id: authored-serving-volunteer-ops
title: Serving And Volunteer Operations
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "fbd19496aa3ad20405854d0570318a0232e0403aa42235affd7b75d9b894cbc5"
---

# Serving And Volunteer Operations

## Agent Summary

Rock’s serving workflow is built from several related but distinct layers:

1. A group type enables and supplies defaults for scheduling, RSVP, attendance, reminders, decline handling, and coordinator notifications.
2. A group represents the operating team and carries its roster, group-level overrides, schedule coordinator, locations, and schedules.
3. Group Scheduling places volunteers into a location or position at a scheduled time.
4. Confirmation state records whether the volunteer is pending, confirmed, declined, or unavailable; it does not by itself prove that the person served.
5. Attendance must be recorded separately after the gathering or serving occurrence.
6. Training, workflows, communications, reporting, and mobile follow-up can extend the process, but each needs its own configuration and verification.

For Rock v19’s documented Group Scheduling configuration, named locations answer where a person serves, schedules answer when, and the Group Scheduler assigns people to those positions. Scheduling must be enabled on the relevant group type before its scheduling features become available. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

An agent should therefore diagnose serving operations in this order: establish the correct group and group type, inspect locations and schedules, inspect the assignment and response state, inspect communication configuration and jobs, then inspect actual attendance. Do not treat a sent request, an accepted assignment, or an attendance reminder as proof that a volunteer served.

## Scope And Boundaries

This guide covers:

- Serving teams represented through groups and group types.
- Locations or positions and serving schedules.
- Schedule confirmations, declines, reminders, coordinator alerts, and volunteer self-service.
- Group RSVP when it is used for an invitation-based serving workflow.
- Training requirements that can be supported through Rock LMS.
- Attendance entry, attendance reminders, digest emails, and bounded follow-up.
- Related reporting, embedded-dashboard security, and mobile relationship-care follow-up.
- Community patterns for schedule exceptions and external schedule visibility.

This guide does not replace the owning guides for Groups, Scheduling, Locations, Check-in, Communications, Workflows, People, Security, or LMS. It also does not establish that a particular installation has a given group structure, background-check provider, workflow, notification job, mobile shell, or plugin.

The supplied evidence does not describe the detailed configuration or enforcement behavior of Rock’s built-in Group Requirements feature. It supports LMS-based training patterns and one background-check provider migration warning, but not a complete requirements engine guide. Those limits are preserved below rather than filled by inference.

## Mental Model

### Policy, team, assignment, response, and attendance

Treat serving operations as five connected records or decisions:

- **Policy layer:** The group type enables scheduling, RSVP, and attendance behavior and can provide inherited communication, reminder, decline, and notification settings.
- **Team layer:** The group carries the people, operational identity, schedule coordinator, and any group-specific overrides.
- **Assignment layer:** A volunteer is placed at a location or position for a schedule.
- **Response layer:** The volunteer’s schedule can be pending, confirmed, declined, or unavailable. The v19 Schedule Toolbox displays those states and allows supported transitions such as accepting, declining, or cancelling a prior confirmation. [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox)
- **Attendance layer:** After the event, Rock records who actually attended or that the group did not meet. This is separate from the scheduling response. [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance)

This separation matters operationally. Rock v18.3 fixed the attendance-reminder job so scheduling- and RSVP-related attendance records would not suppress a reminder unless at least one person actually attended or the group was marked as not meeting. That release note is direct evidence that scheduling or RSVP tracking must not be interpreted as completed attendance. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Group Scheduling and Group RSVP are related but different

Group Scheduling is the volunteer-placement workflow: configure where and when help is needed, place volunteers, request confirmation, monitor responses, and send schedule-specific communications. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Group RSVP is an occurrence-based invitation workflow tied directly to a group. It requires an RSVP-enabled group type, an existing group, and at least one occurrence before RSVP messages can be sent. It can collect accept or decline responses and optional decline reasons. [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp), [Add RSVP Occurrences](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences)

Do not assume that enabling one feature configures the other.

### Serving status is not volunteer eligibility

Being a group member, being scheduled, accepting an assignment, completing training, and being eligible to serve are different conditions. The evidence supports connecting LMS completion with groups, group sync, and workflow actions as an implementation pattern, but it does not establish a universal automatic eligibility rule. Approved claim `claim:4bc0aee305fa6b1bd524` was supported by a bounded read-only structural review of LMS, group-member, and workflow-action surfaces; that review did not verify a particular ministry’s implementation. [Community LMS session at 26:43](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

## Serving Teams And Roles

### Establish the operating group structure

Before working on an individual schedule, identify:

- The group type governing the team.
- The specific group representing the team.
- The active team members.
- The locations or positions associated with the group.
- The schedules associated with those locations.
- The group’s schedule coordinator.
- Any settings inherited from the group type and any group-level overrides.

The official v19 scheduling documentation describes named locations and schedules as prerequisites for volunteer scheduling. Locations may represent rooms, areas, or serving positions such as Audio or Piano. It recommends one named schedule for each time; the same time can be reused across sites when appropriate. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Do not infer configuration from a group or role name. A team named “Ushers,” for example, is not proven to be schedulable until its group type, group-location associations, schedules, and scheduling settings have been inspected.

### Distinguish operational roles

The evidence explicitly identifies two role-like responsibilities:

- A **Schedule Coordinator** is the person configured to receive selected accept, decline, or self-schedule notifications for a group.
- A group role marked **Is Leader** can determine who receives an attendance digest for child attendance groups in the required digest hierarchy.

Schedule Coordinator notification options can be set as group-type defaults and overridden at the group level. Selecting no group-level options uses the group-type defaults; selecting `None` disables the otherwise inherited notifications for that group. [Managing Schedule Coordinator Notifications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications)

The attendance digest uses a specific three-level structure: one parent group, region or area groups whose leaders receive the digest, and attendance groups beneath those regions. The leader of an attendance group can also be contacted from the digest. [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email)

Do not assume that every group leader is the Schedule Coordinator or that an `Is Leader` role automatically grants access to every scheduling, attendance, or reporting page. Page, block, group, and data permissions remain separate security concerns.

### Be precise when identifying volunteers in reports

The v19 Volunteer Generosity report uses a report-specific definition: an active person with at least one recorded attendance in the prior year in a group whose group type purpose is `Serving Area`. The report can filter by attendance date range, campus, and team and shows the relationship between serving and giving rather than exact contribution amounts. [Volunteer Generosity](https://community.rockrms.com/documentation/church-management/finance/finance-reports/volunteer-generosity)

Do not generalize that report definition into a universal eligibility or roster rule. A person can be on a serving-team roster without satisfying that report’s attendance-based definition.

## Schedules And Confirmations

### Configure the scheduling foundation

For documented v19 Group Scheduling:

1. Configure the named locations or positions.
2. Configure accurate named schedules.
3. Associate the applicable locations and schedules with the serving groups.
4. Enable `Scheduling Enabled` on the governing group type.
5. Select the confirmation and reminder System Communications.
6. Set confirmation and reminder offsets.
7. Choose `Ask` or `Auto Accept` confirmation logic.
8. Decide whether declines require a reason.
9. Configure an optional cancellation workflow.
10. Configure coordinator notification defaults and any justified group overrides.

These settings and their roles are described in the official scheduling configuration article. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

The decline reasons available to volunteers come from the `Group Schedule Decline Reason` defined type when the group type requires a reason. A cancellation workflow may be launched when a scheduled person indicates they cannot serve. The evidence does not specify what that workflow should do; its behavior must be inspected rather than inferred.

### Choose confirmation logic deliberately

With `Ask`, the volunteer is asked to accept or decline. With `Auto Accept`, assignments are treated as accepted and the confirmation message contains only a decline option. Rock’s documentation warns that changing from `Ask` to `Auto Accept` while confirmations are already in flight can leave an unconfirmed person with a message that offers only Decline and no way to Accept. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

Treat confirmation-logic changes as a controlled migration:

- Inspect outstanding pending assignments.
- Review the confirmation communication.
- Test with a bounded recipient set.
- Avoid changing the logic immediately before a major serving date.
- Verify the resulting volunteer experience rather than relying on the saved setting alone.

### Send confirmation and schedule communications

Rock v19 documents three routes:

- Send confirmation requests from the Group Scheduler.
- Let the `Send Group Schedule Notifications` job send confirmation and reminder communications based on group-type settings.
- Create a targeted one-time communication through Group Schedule Communication.

The documented default job schedule is daily at 4:00 p.m.; its execution time can be changed in Jobs Administration. Rock supplies Scheduling Confirmation Email and Group Attendance Reminder system communications, which may be customized. [Use Group Scheduling Communications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications)

The Group Schedule Communication page can narrow recipients by groups, child groups, invitation status, locations, schedules, and week before opening the Communication Wizard with the recipient list. [Use Group Scheduling Communications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications)

Email and SMS delivery have additional conditions. For SMS, messaging must be configured, the person must have an SMS-enabled phone number, and the selected System Communication must support SMS. Rock determines the medium from the group member’s communication preference or, when absent, the person’s profile preference. [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule)

### Notify the coordinator of schedule changes

Coordinator notifications can be enabled for any combination of:

- Accept
- Decline
- Self-schedule

The group must have a Schedule Coordinator, and the effective notification options must allow the relevant event. Rock’s documented `Scheduling Response Email` System Communication contains the logic for the response-specific coordinator message. [Managing Schedule Coordinator Notifications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications)

A missing coordinator alert should be diagnosed as configuration or delivery behavior, not as proof that no volunteer action occurred.

### Support volunteer self-service

In v19, the Schedule Toolbox is available from the public-facing My Account area. It can show pending, confirmed, declined, and unavailable engagements. Depending on block settings, volunteers may:

- Accept or decline assignments.
- Cancel a prior confirmation.
- Set periods of unavailability.
- Switch among schedulable family members.
- Download an `.ics` calendar file.
- Copy a calendar subscription link.

Calendar options are not available until the person has an actual confirmed schedule. Cancelling a confirmed assignment changes it to declined, and a reason is required when the group type requires one. Schedule Toolbox actions and labels can be changed or disabled through block settings. [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox)

Group Scheduling is not limited to weekend services; the official documentation also identifies uses such as VBS, camps, recurring gatherings, and special events. [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox)

## RSVP-Based Serving Invitations

### Enable RSVP at the correct level

RSVP is enabled on a group type and becomes available to groups of that type. An actual group must exist even if it initially has no members, because people who accept can be added to that group. [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp)

At the group-type level, configure:

- `Group RSVP Enabled`.
- An optional RSVP reminder System Communication.
- RSVP reminder offset days.

Only System Communications in the `RSVP Confirmation` category are available for the reminder selection. Leaving the communication blank or setting the offset to `0` allows those values to be managed on individual groups; a nonzero group-type offset is inherited and cannot be changed per group. [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp)

After RSVP is enabled, the Group Viewer exposes the RSVP list and group-level reminder settings where inheritance permits them. [Use the Group Viewer with RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp)

### Create and review an occurrence

At least one occurrence is required before sending an RSVP request. An occurrence can include:

- A name visible to invitees.
- A date.
- An optional check-in schedule.
- A location.
- Custom accept and decline messages.
- Optional decline reasons.

Available decline reasons are maintained under the `Group RSVP Decline Reason` defined type. [Add RSVP Occurrences](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences)

After sending the request, monitor the occurrence from RSVP Detail. That page shows occurrence information, response totals, invitees, and responses. Authorized operators can update a response or add a decline note when a person responds through another channel. Decline-reason fields appear only when they were enabled for the occurrence. [View RSVP Details](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details)

If the sender used `Register Recipients`, everyone from the communication appears on the RSVP detail list. Otherwise, the list contains only people who responded. A “missing” nonrespondent may therefore reflect how the communication was created rather than a failed response record. [View RSVP Details](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details)

## Volunteer Requirements And Training

### Use the evidence-supported LMS model

The approved evidence describes Rock LMS as a hierarchy of programs, courses, class instances, learning plans, activities, and learning participants. The program determines whether the learning experience is on-demand or based on an academic calendar. Approved claim `claim:dd3b03571388d00cc80b` was structurally verified against the corresponding LMS surfaces in a bounded read-only review; that verified the feature surface, not any particular volunteer-training program. [Community LMS session at 02:52](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

A class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities. Training design must therefore identify both the volunteer’s required action and the staff member’s review responsibility. Approved claim `claim:882208fdf2bb82703931` was supported by structural verification of activity, participant, completion, grading, file, and notification surfaces. [Community LMS session at 07:17](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

Existing training videos can be turned into LMS activities, but a video asset alone does not define completion, sequencing, or facilitator review. Those rules should follow the intended readiness outcome. Approved claim `claim:c538cf61594b1114dc41` was structurally verified against LMS course, class, activity, completion, and workflow surfaces, not against a particular deployment. [Community LMS migration session at 04:02](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz)

### Connect completion to operations intentionally

LMS activity completion can interact with groups, group sync, and workflow actions, making it useful for volunteer onboarding and follow-up. This is an approved, community-reviewed implementation pattern, not a promise that an LMS completion automatically changes group membership or eligibility in every installation. [Community LMS session at 26:43](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

For each training requirement, define:

- The precise learner action.
- Whether completion is automatic or facilitator-scored.
- The person responsible for review.
- The intended operational result.
- Whether a group sync or workflow performs that result.
- How exceptions, expiration, or retraining will be handled.
- What evidence an operator must inspect before scheduling the person.

Do not label a volunteer “approved” merely because an activity has a completion row. Eligibility may also depend on ministry policy, background checks, staff review, group membership, or version-specific integrations not established by this pack.

### Train staff before volunteer rollout

Official approved guidance recommends training and activating staff before expecting them to train volunteers. Staff-first sequencing creates training multipliers and reduces the risk that inconsistent volunteer practice degrades data quality. [Rock Cast episode 214 at 40:09](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s)

A bounded rollout should therefore validate the staff workflow first: enroll, complete, review, trigger any operational action, inspect the resulting group or workflow state, and rehearse exception handling before inviting the volunteer population.

### Treat background-check providers as versioned dependencies

The supplied Rock v20 release-page excerpt warns that the legacy Protect My Ministry v1 integration cannot submit new requests after upgrading and directs installations to move to Checkr or a plugin provider before the upgrade. The same release page identifies v20.0 as alpha at the captured time. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

This evidence does not document the full background-check setup, status model, permissions, or eligibility enforcement. Verify the installed Rock version, active provider, plugin compatibility, existing requests, and migration guidance before treating background-check status as part of a serving automation.

## Attendance And Follow-Up

### Enable attendance deliberately

A group can take attendance only when `Takes Attendance` is enabled on its group type. A group schedule is not required, but a schedule simplifies entry by guiding operators to the expected meeting dates. Group-type schedule exclusions can prevent attendance reminders on dates when groups are not expected to meet. The group type can also enable attendance reminders to leaders. [Configure Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance)

This means a missing attendance control should be investigated at the group-type level before assuming a page or browser problem.

### Record what actually happened

For a group configured to take attendance, the internal Group Viewer provides an attendance grid and an entry page. Operators can:

- Select the attendance date.
- Review the named schedule when present.
- Mark that the group did not meet.
- Select an attendance type or location when enabled.
- Record attendance notes when enabled.
- Print a roster.
- Mark the attending members.

The `We Did Not Meet` state is distinct from an occurrence with no recorded attendees. Attendance can also be delegated through the Group Leader Toolbox. [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance)

Do not convert every difference between confirmed assignments and recorded attendance into a “no-show.” First account for an unentered occurrence, a group that did not meet, a late cancellation, an incorrect date, schedule, or location, and delayed data entry.

### Use Rapid Attendance Entry for high-volume entry

Rapid Attendance Entry starts by selecting the group and attendance date. Location and schedule choices appear according to the selected group’s configuration. The block can also be configured for notes, person updates, prayer requests, and workflows. When it launches a workflow, Rock passes the person as the workflow entity and can populate matching Group, Location, and Schedule attributes. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

Because the block exposes more than attendance, review its settings and permissions before delegating it. Do not assume that every field or action shown in the documentation is enabled in the target installation.

### Use reminders and digests for data completion

Attendance reminders depend on the group type, schedule, exclusion dates, reminder configuration, and scheduled job behavior. Rock v18.3 fixed a case where scheduling- or RSVP-related tracking records could incorrectly suppress leader reminders. Confirm the installed patch level when diagnosing that symptom. [Configure Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

The Group Attendance Digest can summarize multiple attendance groups, but it is designed for the documented three-level hierarchy. Do not enable it for an arbitrary tree and assume recipients or rollups will be correct. [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email)

### Build follow-up from verified states

A safe follow-up sequence is:

1. Verify that the occurrence existed for the intended date, schedule, location, and group.
2. Verify whether the group met.
3. Verify actual attendance entry.
4. Inspect the volunteer’s scheduling response separately.
5. Treat unexplained differences as review candidates.
6. Launch or record follow-up only after the operational meaning is known.

The supplied evidence does not establish a core, automatic volunteer no-show workflow. If an installation has one, inspect its criteria, workflow actions, security, communication templates, and duplicate-prevention behavior before relying on it.

## Reporting And Operational Visibility

The v19 Volunteer Generosity report can filter serving-related insight by attendance date range, campus, and team. It shows whether volunteers gave during rolling monthly periods but does not expose exact donation amounts in this report. Its definition of a volunteer depends on active status, serving attendance within the prior year, and a group type whose purpose is `Serving Area`. [Volunteer Generosity](https://community.rockrms.com/documentation/church-management/finance/finance-reports/volunteer-generosity)

When embedding Power BI or a similar reporting product in Rock, pair the Rock page and block with appropriate Rock security roles and separately verify the external reporting license. Approved claim `claim:60d40983fd53c0173dd9` was supported by a bounded read-only review of Rock Page, Block, and Auth surfaces; it did not verify external BI licensing or a particular dashboard’s authorization. [Community reporting session at 49:32](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

Do not treat access to a Rock page as proof that the external provider will authorize the viewer, and do not treat provider authorization as proof that the Rock page is appropriately secured.

## Relationship-Care Follow-Up With Outreach Toolbox

Outreach Toolbox is adjacent to volunteer operations rather than a replacement for Group Scheduling. Official approved evidence presents it as a Rock Mobile v19 signed-in experience for maintaining personal outreach contacts and scheduled prayer or connection touchpoints. Current mobile-shell support, page placement, authentication, and configuration must be verified before rollout. Approved claim `claim:483a11b884e0e69ffd4d`. [Outreach Toolbox v19 overview](https://www.youtube.com/watch?v=LNcx8t0mlQ4)

Its dashboard can surface contacts due for outreach or prayer, giving the signed-in user a list of current relationship-care actions. Availability and permissions remain deployment conditions. Approved claim `claim:54aeb223a9029e9f7707`. [Outreach Toolbox dashboard](https://www.youtube.com/shorts/c6T9Ha13jKE)

Onboarding can collect assignment days and reminder preferences, while configurable jobs determine reminder time-of-day values. Operational use requires testing the job schedule and push delivery in the target mobile environment. Approved claim `claim:9c8ce297c9c4a4cda982`. [Outreach Toolbox at 01:04](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s)

The feature can track contact-specific prayer and connection cadences, completed touchpoint history, periodic pulse updates, and configurable milestone prompts. Before ministry use, review who can see contact data and which block settings are active. Approved claim `claim:e704f98991439e3e1576`. [Outreach Toolbox at 07:56](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s)

Do not use Outreach Toolbox reminders as evidence of a serving assignment, confirmation, attendance record, or completed volunteer follow-up unless the organization has explicitly designed and verified that connection.

## Community Implementation Patterns

The following are community examples, not official Rock behavior or endorsed implementation designs.

A community recipe for adding fifth-week behavior to member schedule templates describes A/B rotation, every-other-week schedules, and manually maintained specific-date schedules. It notes that schedule templates are day-of-week-sensitive and recommends clear names. Its fifth-week-only pattern requires ongoing date maintenance. Evaluate the pattern against the target version and calendar before adopting it. [Community recipe: Group Member Schedule Templates](https://community.rockrms.com/recipes/356)

Another community recipe exposes a serving schedule on an external group-toolbox page using copied pages, a customized Lava file, Dynamic Data, a page-parameter filter, and SQL. The recipe itself warns that community recipes are not reviewed or endorsed by the Rock core team and may affect performance or security. Do not copy its SQL or page design without security review, parameter validation, upgrade planning, and testing against the installed schema. [Community recipe: View Serving Schedule on External Page](https://community.rockrms.com/recipes/459)

A community Q&A response describes creating separate sign-up group types for campus and service-time combinations, then limiting the Serving Finder page to the relevant sign-up group. This is an anecdotal configuration pattern, not verified core guidance. Before following it, compare the administrative overhead and reporting impact with the target installation’s existing group-type design. [Community Q&A: Limit sign-up registration by schedule or campus](https://community.rockrms.com/ask/using/2808)

## Version And Authority Caveats

- Most official configuration documentation in this pack is scoped to Rock v19. Verify the target installation’s exact version and the selected documentation version before applying labels, paths, defaults, or block behavior.
- Rock v19.3 fixed the RSVP Response heading so an Accept or Decline link uses the attendance occurrence name rather than generic RSVP text. If the wrong heading appears, confirm the installed patch level before customizing the block. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Rock v18.3 fixed attendance reminders that could be suppressed by scheduling- or RSVP-related tracking records. Older installations may reproduce that historical defect. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- The captured release page identifies Rock v20.0 as alpha and includes a migration warning for legacy Protect My Ministry v1 background checks. Pre-release behavior should not be described as installed or production-ready without target-environment verification. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- LMS claims in this guide are community-reviewed implementation guidance with approved structural verification. That verification established relevant feature surfaces in a reviewed installation, not a universal volunteer-training configuration.
- Outreach Toolbox claims come from official v19 preview material but remain conditional on mobile shell, authentication, page and block configuration, jobs, push delivery, and permissions.
- Community recipes and Q&A are examples. They are not official product guarantees and should be reviewed for security, performance, maintainability, and version compatibility.
- Supplied source-code excerpts reference immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` on the public Rock repository. They can clarify implementation vocabulary but do not prove what code or configuration is installed on a target instance.

## Troubleshooting Decision Tree

### The team does not appear in Group Scheduling

1. Confirm that the operator is inspecting the intended group and group type.
2. Inspect whether `Scheduling Enabled` is active on that group type.
3. Confirm that the required named locations or positions exist.
4. Confirm that the required named schedules exist and have accurate times.
5. Confirm that the locations and schedules are associated with the group.
6. Inspect the scheduler’s current group and location selections.
7. If all configuration appears correct, verify permissions and the installed version before changing data.

Source: [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule).

### A volunteer received no confirmation or reminder

1. Determine whether the communication was expected from a manual scheduler action or the scheduled notification job.
2. Inspect the group type’s confirmation and reminder communications.
3. Inspect the confirmation and reminder offset days.
4. Confirm whether the assignment had already received the relevant communication.
5. Inspect the `Send Group Schedule Notifications` job, including its schedule and recent result.
6. For SMS, verify SMS configuration, an SMS-enabled number, the System Communication medium, and effective communication preference.
7. Distinguish “no eligible recipients” from “eligible recipients found but delivery failed.”
8. Stop before resending broadly if prior delivery cannot be determined.

Sources: [Use Group Scheduling Communications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications), [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule). The distinction between eligible-recipient count, sent count, warnings, and errors is also present in the public implementation contract at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. [GroupSchedulerSendConfirmationsResponseBag.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs)

### A volunteer cannot accept an assignment

1. Inspect the current assignment state in Schedule Toolbox.
2. Inspect whether confirmation logic is `Ask` or `Auto Accept`.
3. If it is `Auto Accept`, verify whether the assignment is already treated as accepted and only Decline should be offered.
4. Determine whether confirmation logic changed after the assignment was created but before the message was received.
5. Review Schedule Toolbox block settings for disabled actions or changed labels.
6. Test with a bounded assignment before changing confirmation logic again.

Sources: [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule), [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox).

### The Schedule Coordinator was not alerted

1. Confirm that the group has a Schedule Coordinator.
2. Identify the event: Accept, Decline, or Self-schedule.
3. Inspect the group-level notification options.
4. If no group-level options are selected, inspect the group-type defaults.
5. If `None` is selected at group level, recognize that inherited notifications are disabled.
6. Inspect the Scheduling Response Email System Communication and its delivery result.
7. Verify the coordinator’s reachable address before replaying any notification.

Source: [Managing Schedule Coordinator Notifications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications).

### RSVP features are missing

1. Confirm that an actual group exists.
2. Inspect the group type and enable `Group RSVP Enabled` if authorized.
3. Return to the group in Group Viewer and look for the RSVP list.
4. Create at least one occurrence before attempting to send an RSVP request.
5. Inspect inherited versus group-level reminder communication and offset settings.
6. Verify the operator’s access if the controls remain absent.

Sources: [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp), [Use the Group Viewer with RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp).

### An RSVP invitee is missing from the response list

1. Open the correct occurrence’s RSVP Detail page.
2. Verify whether the person actually responded.
3. Determine whether `Register Recipients` was used when the request was sent.
4. If it was not used, expect nonrespondents to be absent from the list.
5. If the person responded through another channel, update the response only after confirming identity and occurrence.
6. Do not resend to the full audience merely to populate the list.

Source: [View RSVP Details](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details).

### The attendance button is missing

1. Confirm that the group belongs to the expected group type.
2. Inspect the group type’s Attendance / Check-in settings.
3. Confirm that `Takes Attendance` is enabled.
4. Reload the group in Group Viewer.
5. If still absent, verify page, block, and operator security without altering the group structure.

Sources: [Configure Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance), [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance).

### An attendance reminder was not sent

1. Confirm that attendance reminders are enabled for the group type.
2. Confirm that the group was scheduled to meet.
3. Inspect group and group-type exclusion dates.
4. Determine whether actual attendance was entered or the group was marked as not meeting.
5. Do not treat scheduling or RSVP response records as actual attendance.
6. Confirm the installed Rock version and whether the v18.3 reminder fix applies.
7. Inspect the reminder job and delivery result.

Sources: [Configure Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance), [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### A confirmed volunteer appears absent

1. Confirm the group, occurrence date, schedule, and location.
2. Confirm whether the team met.
3. Confirm that attendance entry is complete.
4. Inspect whether the volunteer later cancelled or declined.
5. Correct data-entry errors before starting follow-up.
6. Treat the remaining difference as a follow-up candidate, not a proven no-show.
7. Inspect any local no-show workflow before launching or replaying it.

Sources: [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox), [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance).

### Rapid Attendance Entry lacks an expected location, schedule, or action

1. Confirm the selected group.
2. Inspect the locations and schedules configured for that group.
3. Remember that a schedule selector appears only when multiple schedules apply to the selected location.
4. Inspect the Rapid Attendance Entry block settings.
5. Confirm whether attendance, notes, workflows, and related actions are enabled.
6. Verify campus filtering when expected locations are absent.
7. Stop before adding duplicate people or families; search thoroughly first.

Source: [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry).

### Training completion did not change serving eligibility

1. Confirm the correct person, learning participant, class, and activity.
2. Inspect whether the activity is complete and whether facilitator scoring is still required.
3. Identify the intended downstream mechanism: group sync, workflow action, or staff review.
4. Inspect whether that mechanism ran and whether it encountered an exception.
5. Confirm that ministry policy permits the expected status change.
6. Do not manually mark the person eligible until all non-LMS requirements are known.

Sources: approved claims `claim:882208fdf2bb82703931` and `claim:4bc0aee305fa6b1bd524`, supported by [the community LMS session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN).

### Outreach Toolbox reminders are not arriving

1. Confirm that the environment supports the documented v19 Rock Mobile experience.
2. Confirm that the person is signed in.
3. Inspect page placement, block settings, and authentication.
4. Confirm the person’s assignment days and reminder preferences.
5. Inspect the job’s configured time and recent execution.
6. Test push-notification delivery in the target mobile environment.
7. Inspect permissions for contact and touchpoint data.
8. Do not infer a completed follow-up from a scheduled or attempted notification.

Sources: approved claims `claim:483a11b884e0e69ffd4d`, `claim:9c8ce297c9c4a4cda982`, and `claim:e704f98991439e3e1576`, supported by [the official v19 walkthrough](https://www.youtube.com/watch?v=LNcx8t0mlQ4).

## Agent Task Recipes

### Recipe: Configure a serving team for scheduling

**Outcome:** A bounded serving group is ready for assignments at verified locations and times.

1. Identify the intended group type and group.
2. Inspect existing named locations and schedules before creating anything.
3. Add only the missing locations or positions and schedules.
4. Associate them with the serving group.
5. Enable Group Scheduling on the group type.
6. Select confirmation and reminder System Communications.
7. Set the confirmation and reminder offsets.
8. Choose `Ask` or `Auto Accept`.
9. Configure decline-reason and cancellation-workflow behavior.
10. Assign a Schedule Coordinator and choose notification events.
11. Test one assignment through the volunteer-facing Schedule Toolbox.
12. Verify the resulting assignment state and communication outcome.

**Inspect:**

- Group-type defaults.
- Group-level overrides.
- Schedule accuracy.
- Location meaning.
- Volunteer communication preference.
- Schedule Toolbox block settings.

**Do not assume:**

- A group name makes it schedulable.
- A saved assignment was communicated.
- An accepted assignment is attendance.

**Stop when:**

- The correct test assignment appears in the volunteer experience.
- Its response state is visible.
- The intended communication result has been verified.

Source: [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule).

### Recipe: Send and triage volunteer confirmations

**Outcome:** The intended volunteers receive a confirmation request without an uncontrolled duplicate send.

1. Select the correct groups, locations, schedules, and week.
2. Review current assignment states.
3. Determine whether the scheduled job has already sent the request.
4. Preview the confirmation communication and its response links.
5. Send only to the bounded eligible set.
6. Compare eligible-recipient count with sent count.
7. Review warnings and errors.
8. Monitor pending, confirmed, declined, and unavailable states.
9. Route declines or cancellations according to the configured workflow.
10. Verify coordinator notification separately.

**Inspect:**

- Prior communication state.
- Confirmation logic.
- Delivery medium.
- Response state.
- Coordinator alert result.

**Stop when:**

- Each intended assignment has a known send status.
- Failures are isolated.
- No duplicate broad resend is required.

Sources: [Use Group Scheduling Communications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications), [Managing Schedule Coordinator Notifications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications).

### Recipe: Configure an RSVP-based serving invitation

**Outcome:** A group occurrence can collect and display bounded accept or decline responses.

1. Confirm that RSVP is the intended workflow rather than Group Scheduling.
2. Confirm that the target group exists.
3. Enable RSVP on the group type.
4. Configure the reminder communication and offset at either group-type or group level.
5. Create the occurrence with its date, optional schedule, and location.
6. Add custom response messages when needed.
7. Enable and select decline reasons only when the ministry will use them.
8. Send the RSVP request and decide whether to register all recipients.
9. Monitor RSVP Detail.
10. Record verified phone or in-person response changes when authorized.

**Do not assume:**

- RSVP enables scheduling.
- A nonrespondent will appear when recipients were not registered.
- An acceptance proves attendance.

**Stop when:**

- The occurrence is correct.
- The bounded request is sent.
- Response-list behavior matches the chosen recipient-registration method.

Sources: [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp), [Add RSVP Occurrences](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences), [View RSVP Details](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details).

### Recipe: Close out serving attendance

**Outcome:** The occurrence records who served or that the team did not meet, with discrepancies ready for human review.

1. Open the correct group attendance occurrence.
2. Verify the date, schedule, and location.
3. Mark `We Did Not Meet` if that is what occurred.
4. Otherwise, record actual attendees.
5. Add only appropriate operational notes.
6. Compare the completed attendance list with confirmed assignments.
7. Investigate late changes and data-entry omissions.
8. Produce a bounded follow-up list of unresolved differences.
9. Launch follow-up only after confirming each difference’s meaning.

**Do not assume:**

- Pending means absent.
- Confirmed means attended.
- No attendance rows means the team met with zero volunteers.

**Stop when:**

- Attendance or `Did Not Meet` is recorded.
- Unresolved differences are identified without being mislabeled as no-shows.

Source: [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance).

### Recipe: Build an LMS-based volunteer training path

**Outcome:** A volunteer completes defined learning activities and reaches an explicitly reviewed operational result.

1. Define the readiness outcome before building activities.
2. Choose the appropriate program mode: on-demand or academic-calendar based.
3. Place the training in the relevant program, course, and class structure.
4. Create activities for the required learner actions.
5. Define completion, ordering, scoring, file, and facilitator-review expectations.
6. Assign staff responsibility for manual review.
7. Define any group sync or workflow action that should follow completion.
8. Test with a staff participant first.
9. Verify the completion record and downstream operational result independently.
10. Train the staff who will support volunteers.
11. Roll out to a bounded volunteer cohort.
12. Monitor exceptions before scaling.

**Inspect:**

- Completion rules.
- Facilitator-scored work.
- Workflow or group-sync result.
- Remaining non-LMS requirements.

**Do not assume:**

- Watching a video is sufficient.
- Completion automatically grants eligibility.
- Structural feature availability proves local configuration.

**Stop when:**

- Staff have reproduced the full path.
- Learner and reviewer responsibilities are documented.
- The downstream result has been independently verified.

Sources: approved claims `claim:dd3b03571388d00cc80b`, `claim:882208fdf2bb82703931`, `claim:c538cf61594b1114dc41`, `claim:4bc0aee305fa6b1bd524`, and `claim:c8c3a60f71790dd3616d`, supported by [the LMS session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN), [the LMS migration session](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz), and [Rock Cast episode 214](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s).

### Recipe: Configure an attendance digest

**Outcome:** Leaders at the intended regional level receive attendance summaries for their child attendance groups.

1. Confirm that the group hierarchy has all three required levels.
2. Identify the single top parent group.
3. Identify the region or area groups.
4. Confirm that intended recipients have a role marked `Is Leader` in those groups.
5. Confirm the child attendance groups where attendance is recorded.
6. Configure the Send Group Attendance Digest job for the top parent.
7. Run a bounded test.
8. Verify each recipient and the child groups represented.
9. Confirm the attendance-group leader link routes to the intended person.

**Stop when:**

- The recipient and group rollup match the intended hierarchy.
- No unintended group or leader is exposed.

Source: [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email).

### Recipe: Secure an embedded volunteer dashboard

**Outcome:** The Rock page and external reporting provider both authorize only the intended viewers.

1. Identify the Rock page and report block.
2. Inspect Rock page and block authorization.
3. Define the intended security roles.
4. Verify the external reporting product’s licensing and identity requirements.
5. Test with an authorized user.
6. Test with an unauthorized user.
7. Confirm that direct report access cannot bypass the intended controls.
8. Review the displayed volunteer and financial fields for minimum necessary exposure.

**Do not assume:**

- Rock authorization grants a provider license.
- A provider license grants Rock-page access.
- A successful administrator test proves ordinary-user access.

**Stop when:**

- Both authorization layers have been tested.
- Unauthorized access is rejected.
- The displayed data is appropriate for the audience.

Source: approved claim `claim:60d40983fd53c0173dd9`, supported by [the community reporting session](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz).

### Recipe: Pilot Outreach Toolbox for relationship-care follow-up

**Outcome:** A bounded group of signed-in mobile users can see, receive, complete, and review configured outreach touchpoints.

1. Confirm the target Rock server and mobile-shell versions.
2. Verify signed-in access and page placement.
3. Review block settings and contact-data permissions.
4. Configure assignment days and reminder preferences for test users.
5. Inspect the reminder job and time-of-day configuration.
6. Create bounded prayer and connection cadences.
7. Test dashboard visibility.
8. Test push delivery in the real target mobile environment.
9. Complete a touchpoint and verify history and pulse behavior.
10. Review who can see the resulting contact data before expanding access.

**Do not assume:**

- Previewed v19 behavior exists in every mobile deployment.
- A successful job run proves push delivery.
- A scheduled touchpoint is a completed action.

**Stop when:**

- Access, delivery, completion history, and permissions have each been verified.

Sources: approved claims `claim:483a11b884e0e69ffd4d`, `claim:54aeb223a9029e9f7707`, `claim:9c8ce297c9c4a4cda982`, and `claim:e704f98991439e3e1576`, supported by [the official Outreach Toolbox walkthrough](https://www.youtube.com/watch?v=LNcx8t0mlQ4) and [dashboard preview](https://www.youtube.com/shorts/c6T9Ha13jKE).

## Known Gaps And Live Verification

No live review of the target installation was supplied for this guide. Before relying on it operationally, verify:

- The installed Rock version and patch level.
- The intended group types, groups, members, roles, and group-type inheritance.
- Scheduling, RSVP, attendance, decline, and coordinator settings.
- Group-location and schedule associations.
- Page, block, group, workflow, attendance, and report permissions.
- The effective confirmation, reminder, RSVP, coordinator, and digest System Communications.
- Job schedules, execution results, eligible-recipient counts, sends, warnings, and errors.
- Email and SMS provider configuration and actual delivery.
- Schedule Toolbox block settings and the signed-in volunteer experience.
- Attendance-entry responsibility and the meaning of any local no-show logic.
- The exact configuration and enforcement behavior of built-in Group Requirements.
- The active background-check provider, plugin version, provider status mapping, and upgrade path.
- LMS program, course, class, activity, participant, completion, grading, notification, group-sync, and workflow configuration.
- Whether an LMS completion actually changes group membership or eligibility.
- External BI licensing and both Rock-side and provider-side authorization.
- Rock Mobile shell support, Outreach Toolbox page placement, authentication, block settings, jobs, push delivery, and contact-data visibility.
- The security, performance, parameter handling, schema compatibility, and upgrade impact of any community Lava, SQL, page, or schedule-template pattern.

The pack does not establish:

- A universal serving-team group architecture.
- A universal definition of volunteer eligibility.
- A complete built-in Group Requirements workflow.
- A core automatic volunteer no-show workflow.
- A universal mapping from training completion to serving approval.
- Successful communication or push delivery in a target environment.
- That an embedded report’s external license has been granted.
- That v20 alpha behavior is appropriate for production use.

## Source Map

### Approved answer-bearing claims

- `claim:4bc0aee305fa6b1bd524` — Community-reviewed, structurally live-verified implementation pattern connecting LMS activity completion with groups, group sync, and workflow actions. [Source at 26:43](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)
- `claim:60d40983fd53c0173dd9` — Community-reviewed, structurally live-verified guidance for pairing embedded BI pages with Rock authorization and external licensing checks. [Source at 49:32](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)
- `claim:882208fdf2bb82703931` — Community-reviewed, structurally live-verified guidance for learner activities and facilitator responsibilities. [Source at 07:17](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)
- `claim:c538cf61594b1114dc41` — Community-reviewed, structurally live-verified guidance for restructuring existing video content into intentional LMS activities. [Source at 04:02](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz)
- `claim:dd3b03571388d00cc80b` — Community-reviewed, structurally live-verified LMS hierarchy and delivery-mode guidance. [Source at 02:52](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)
- `claim:483a11b884e0e69ffd4d` — Official v19 Outreach Toolbox scope and rollout conditions. [Official walkthrough](https://www.youtube.com/watch?v=LNcx8t0mlQ4)
- `claim:54aeb223a9029e9f7707` — Official Outreach Toolbox dashboard preview. [Official short](https://www.youtube.com/shorts/c6T9Ha13jKE)
- `claim:9c8ce297c9c4a4cda982` — Official Outreach Toolbox onboarding, reminder preference, and job caveat. [Source at 01:04](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=64s)
- `claim:c8c3a60f71790dd3616d` — Official staff-first training guidance. [Source at 40:09](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s)
- `claim:e704f98991439e3e1576` — Official Outreach Toolbox cadence, history, pulse, milestone, and privacy caveat. [Source at 07:56](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s)

### Official documentation and release evidence

- [Configure Group Schedule](https://community.rockrms.com/documentation/engagement/groups/group-schedules/configure-group-schedule) — v19 scheduling prerequisites, group-type settings, communications, declines, workflows, confirmation logic, SMS conditions, and coordinator options.
- [View your Schedule (Toolbox)](https://community.rockrms.com/documentation/engagement/groups/group-schedules/view-your-schedule-toolbox) — v19 volunteer schedule states, availability, calendar tools, family switching, and block-setting caveats.
- [Use Group Scheduling Communications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/use-group-scheduling-communications) — v19 manual, job-based, and targeted scheduling communications.
- [Managing Schedule Coordinator Notifications](https://community.rockrms.com/documentation/engagement/groups/group-scheduler-page/managing-schedule-coordinator-notifications) — v19 coordinator defaults, overrides, and response notifications.
- [Enable Group RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/enable-group-rsvp) — v19 RSVP enablement and reminder inheritance.
- [Use the Group Viewer with RSVP](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/use-the-group-viewer-with-rsvp) — v19 RSVP list and group-level reminder settings.
- [Add RSVP Occurrences](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/add-rsvp-occurrences) — v19 occurrence, location, schedule, messaging, and decline-reason fields.
- [View RSVP Details](https://community.rockrms.com/documentation/engagement/groups/group-rsvp/view-rsvp-details) — v19 response monitoring and recipient-registration behavior.
- [Configure Group Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/configure-group-attendance) — v19 attendance enablement, schedules, exclusions, and reminders.
- [Entering Attendance](https://community.rockrms.com/documentation/engagement/groups/group-attendance/entering-attendance) — v19 internal entry, did-not-meet state, notes, roster, and leader-toolbox delegation.
- [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry) — v19 rapid entry, conditional fields, workflows, and block settings.
- [Use the Group Attendance Digest Email](https://community.rockrms.com/documentation/engagement/groups/group-attendance/use-the-group-attendance-digest-email) — v19 required digest hierarchy and leader recipients.
- [Volunteer Generosity](https://community.rockrms.com/documentation/church-management/finance/finance-reports/volunteer-generosity) — v19 report behavior and report-specific volunteer definition.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — v18.3 attendance-reminder fix, v19.3 RSVP-heading fix, and captured v20 alpha/background-check migration caveat.

### Public implementation evidence

- [ToolboxScheduleRowConfirmationStatus.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Enums/Blocks/Group/Scheduling/ToolboxScheduleRowConfirmationStatus.cs) — implementation vocabulary for pending, confirmed, declined, and unavailable schedule rows.
- [GroupSchedulerSendConfirmationsResponseBag.cs at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Group/Scheduling/GroupScheduler/GroupSchedulerSendConfirmationsResponseBag.cs) — implementation contract distinguishing eligible recipients, sent count, warnings, and errors.
- [vCheckin_GroupTypeAttendance.sql at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/database/Views/vCheckin_GroupTypeAttendance.sql) — backward-compatibility view showing attended records joined through attendance occurrences, people, and groups. This is implementation evidence, not a recommended reporting interface.

### Community examples

- [Group Member Schedule Templates: fifth-week and Auto-Schedule](https://community.rockrms.com/recipes/356) — unendorsed community scheduling-template patterns.
- [View Serving Schedule on External Page](https://community.rockrms.com/recipes/459) — unendorsed community Lava, Dynamic Data, page, and SQL pattern.
- [Limit sign-up registration by schedule or campus](https://community.rockrms.com/ask/using/2808) — anecdotal community group-type and Serving Finder pattern.