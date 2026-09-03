---
id: authored-engagement-tracking
title: Engagement Tracking
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "34d5ec693c797f6c897e84b6a832dfe7d7dbbf75e13da43403b965795d9c0001"
---

# Engagement Tracking

## Agent Summary

Rock provides several related but distinct ways to represent engagement:

- **Steps** record progress through an organizational journey. Completion requires both a completion date and a status configured as complete. Programs control ordering and prerequisites, while step types control repeatability, dates, attributes, automation and other behavior. ([Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps), [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs))
- **Streaks** calculate consecutive participation from occurrence, engagement and exclusion maps. Enrollment dates, exclusions and rebuild behavior materially affect the result. ([Intro to Streaks](https://community.rockrms.com/documentation/engagement/streaks/overview/intro-to-streaks), [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps))
- **Assessments** collect built-in assessment results, preserve requested and self-initiated history, and expose result attributes for person Data Views. Retakes depend on the assessment type’s minimum-days and request requirements. ([Intro to Assessments](https://community.rockrms.com/documentation/engagement/assessments/overview/intro-to-assessments), [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments))
- **Achievements** evaluate goals against engagement or interaction data and track attempts from start through success or failure. They can launch workflows and create Steps after success. ([Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements), [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types))
- **Reminders, Following, Interactive Experiences and Sign-Ups** support follow-up, personalized notifications, live participation and short-term opportunities. They have their own job, permission, communication, mobile and page-configuration dependencies. ([Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools))

An agent should first identify which record represents the desired outcome. Do not use an Achievement as if it were a manually curated journey record, a Step as if it proved consecutive attendance, or a Sign-Up registration as if it represented a completed Step.

## Scope And Boundaries

This guide covers configuration and operations for Steps, Streaks, Assessments, Achievements, Reminders, Following, Interactive Experiences and Sign-Ups. It also covers the evidence-supported connections among those tools, including Achievement-to-Step creation, Data View segmentation of assessment results, workflow launches and attendance-driven streak calculation. ([Steps](https://community.rockrms.com/documentation/engagement/steps), [Streaks](https://community.rockrms.com/documentation/engagement/streaks), [Assessments](https://community.rockrms.com/documentation/engagement/assessments), [Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools))

Related concepts retain ownership of their specialized concerns:

- Person matching, aliases and profile administration belong with People.
- Group structure, attendance collection and group security belong with Groups and Check-in.
- Workflow construction belongs with Workflows.
- Communication transport, deliverability and consent belong with Communications.
- General Data View and reporting design belong with Data Views and Reports.
- Page, block, entity and role authorization belong with Security.
- Course and learning-activity completion belongs with LMS engagement.

This evidence pack contains no reviewed live-instance conclusion. Therefore, installed version, configured jobs, page blocks, security assignments, communication transport, mobile setup, geofences and actual organization data must be verified separately before an agent claims that a feature works in a particular installation.

## Mental Model

Treat engagement tracking as a chain from source evidence to calculated or curated outcomes:

1. **Activity evidence** originates in records such as attendance, interactions, giving, assessment responses or manually entered participation.
2. **Interpretation rules** define what the evidence means. Step prerequisites, streak frequencies, occurrence maps, assessment-type policies and Achievement conditions all belong here.
3. **Entity-level state** records a person’s Step, streak enrollment, assessment history or Achievement attempt.
4. **Completion and progress signals** expose the result through statuses, dates, percentages, badges, charts, Data Views, workflows or communications.
5. **Operational responses** use those signals to support follow-up, celebrate progress, send reminders or guide placement.

These layers are not interchangeable. For example, a streak exclusion changes streak calculation without changing underlying attendance, while an Achievement rebuild recalculates attempts rather than modifying the source participation records. ([Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date), [Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types))

## Steps

### Programs, types and completion

A Step Program groups Step Types and defines shared statuses, presentation and progression rules. Its Completion Flow has three supported modes:

- **Linear (Required):** steps must be completed in sequence, and custom prerequisites are removed.
- **Linear (Preferred):** the sequence is preferred rather than mandatory, while configured prerequisites remain enforced.
- **Non-Linear:** sequence controls display order only, while configured prerequisites remain enforced.

A Step is complete only when it has both a completion date and a status whose configuration marks it complete. A date by itself is not sufficient. For a Rhythm engagement type, Rock does not automatically change the status: In Progress represents an active rhythm, and Completed indicates that the rhythm has ended. ([Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps), [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs))

At the Step Type level, configuration controls prerequisites, whether multiple completions are allowed, whether the activity spans time and whether its date is required. A type that spans time uses separate start and end dates. A type that does not span time uses one date, which Rock treats and displays as the completion date. ([Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types), [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry))

### Entry, attributes and history

An individual Step can be maintained from a Step Type or a person profile. Step Entry supports the person, optional campus, applicable dates, status, note and configured Step Attributes. Changes to a person’s Step record are included in Person History on the profile’s History tab. ([Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry))

On a Step Type’s participant list:

- The start-date column appears only when the type spans time.
- The single date for a type that does not span time appears as the completion date.
- A Step Attribute appears in the grid when **Show in Grid** is enabled.

These display rules should be checked before concluding that a date or attribute is absent from the underlying record. ([Intro to Step Types](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-types))

### Bulk entry and automation

Rock supports two bulk-maintenance paths: updating selected people from a list grid and using bulk entry from a Step Program or Step Type page. A Step Attribute with **Show on Bulk** enabled can be assigned once to all selected people. Without that setting, the attribute remains available but must be entered separately for each person. ([Use Bulk Entry With Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps))

A Step Type can use an Auto-Complete Data View. When the Steps Automation job processes it, Rock still honors prerequisites and **Allow Multiple** before creating or completing Step records. Data View membership alone therefore does not guarantee that a new Step will be produced. ([Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types))

A reviewed community recipe describes a historical-data migration pattern using Data Views and a workflow so the source attribute’s historical date can be retained. It warns about duplicates, timeouts and failures when multiple completions are disallowed. This is a community example written for older Rock versions, not official current behavior or a generally safe migration procedure. ([Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233))

### Workflows and permissions

Official documentation supports attaching workflows at either the Step Program or Step Type level. Program workflows apply across the program; type-level workflows apply only to that Step Type. Documented program triggers include Step Completed, Status Changed and Manual. Adding Steps from a person profile also depends on Edit permission for the Steps block. ([Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs), [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types))

Rock 18.3 fixed a high-severity issue in which editing a Step Program could remove the Step Type association from workflow triggers and could display type-level triggers on the program detail page. Rock 19.5 also fixed a program Status Changed trigger configured with a From status of Any firing on unrelated Step saves. Verify the installed version when investigating either symptom. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### Badges, metrics and charts

To display a program’s progress as a badge, configure one Person badge of type Steps for the entire Step Program, then add that badge to the Person Profile page’s badge container. A Step Type’s **Show Count on Badge** setting affects only badges using Normal display mode. ([Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges))

Program Started and Completed totals count Step occurrences, not distinct people. A person can therefore contribute more than once when the Step Type allows multiple completions. Average completion time is measured from the earliest Step start date through the latest Step end date in the program. ([Intro to Step Programs](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-programs))

Chart interpretation depends on configuration:

- A Step Program Trends chart includes completed Step Types.
- A Step Type chart can display either started or completed activity.
- Completed-status filters plot completion dates; other status filters plot start dates.
- Impact-adjusted measures multiply each Step Type’s completion count by its configured Impact Weight.
- A Step Flow chart’s maximum-level setting truncates the visible sequence. Absence after the final displayed level does not prove that people stopped progressing.

([Intro to Step Charts](https://community.rockrms.com/documentation/engagement/steps/steps-charts/intro-to-step-charts), [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types))

### Moving Step Types and completion records

Moving a Step Type to another program preserves its Step data but removes its prerequisites and Step Attributes; those configurations must be rebuilt in the destination. Existing Program Completions are not recalculated or moved and remain associated with the programs where they were recorded. ([Move a Step Type](https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type))

Rock 18.1 introduced the ability to transfer Step Types and added a system-protected Core Steps program with initial system-protected types. Confirm version and protection state before planning a transfer. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

As an implementation observation, Rock’s public source at commit `471fd303d111b2e46218228dbc1e93dba8856fa3` describes a Step Program Completion record as representing the point at which a person has a complete set of completed Steps, using the newest completed Step for each type. The same source makes that completion record inherit its security authority from its Step Program. This is code evidence from that commit, not proof of an installation’s version, data or authorization configuration. ([StepProgramCompletion.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs), [StepProgramCompletion.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs))

## Streaks

### Types and maps

A Streak Type defines the engagement source, activity target, frequency, start date and tracked population. Rock can calculate streaks from attendance or other engagement data to identify consecutive instances of participation. ([Intro to Streaks](https://community.rockrms.com/documentation/engagement/streaks/overview/intro-to-streaks), [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types))

The calculation uses three maps:

- The **occurrence map** identifies eligible days or weeks when participation could occur.
- The **engagement map** identifies the individual’s participation.
- The **exclusion map** identifies excused absences.

An exclusion can apply to an individual or a location. It causes an absence to be ignored, but it does not prevent recorded participation on that date from contributing positively to the streak. ([Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps))

A Streak Type’s start date and frequency cannot be manually changed after the type is saved; correcting either generally requires a new Streak Type. If **Sync Linked Activity** is enabled, qualifying attendance or interaction records update the engagement map, and additions to the engagement map create corresponding attendance or interaction records. Verify this setting before making a supposedly map-only correction. ([Add a New Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type))

### Enrollment and exclusions

The enrollment date forms an individual lower boundary: engagements and absences before it are ignored. The date cannot be manually changed after the enrollment is saved. Manually enrolling someone does not populate historical attendance into the engagement map; an individual rebuild is required to derive that map from configured engagement data. ([Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail), [Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment))

An individual exclusion affects only that enrollee. The exclusion does not change underlying attendance, so the engagement graph or map may still display an absence even while the calculated streak spans the excluded date. A manually excluded date neither contributes to nor interrupts the streak. ([Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment), [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date))

Manual engagement-map additions update streak metrics after saving. After changing an engagement or exclusion map, save and refresh the page to confirm the displayed result. Occurrence-map changes have a different timing dependency: participant displays are not updated until the nightly cleanup job runs. ([Manually Track Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks), [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail))

### Rebuild boundaries

An individual rebuild recalculates current and longest streaks from attendance, constrains enrollment to no earlier than the Streak Type start date and includes only dates enabled by the occurrence map. It deletes the person’s existing engagement map before recreating it, so manual engagement-map edits are lost. ([Rebuild Streaks Individually](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually))

A Streak Type rebuild has a wider destructive boundary: it deletes and regenerates occurrence and enrollment map data from attendance records, discarding manual changes to both. For an attendance-based type, Rock derives the type start date, enrolled people, individual enrollment dates, engagement counts and applicable occurrence weeks from attendance. Weeks recorded as Didn’t Meet are excluded from the occurrence map and do not count as attendance gaps. ([Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type))

## Assessments

### Requests, completion and history

From a person profile, **Request Assessment** can send one or more assessment requests with a custom message. For a larger audience, a communication can construct each assessment’s external URL from the public application root and the recipient’s URL-encoded person key. Recipients can also find requests on the external My Account page. ([Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests))

Built-in assessment questions and answer formats are not configurable. For more consistent results, participants should answer according to their present characteristics and keep the same environmental context throughout the assessment. ([Take Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/take-assessments))

The person profile’s History tab lists requested and self-initiated assessments. Self-initiated entries have no request date or requester. A request can be canceled or deleted only before the assessment is completed. ([View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history))

### Retake controls

Retake eligibility is controlled by two Assessment Type settings:

1. **Minimum Days to Re-take** establishes the interval after completion.
2. **Requires Request**, when enabled, requires a request for both initial and repeat access.

The documented default interval in the supplied Rock 19 material is 365 days, but an agent should inspect the installed Assessment Type instead of assuming that default remains configured. Eligible external users can access a retake from My Account or from the assessment results page. ([Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments))

### Result interpretation and segmentation

Assessment results can be used in person Data Views, allowing organizations to form groups or reports from assessment responses. The evidence specifically supports these built-in result models:

- **DISC:** participants choose the statement most like and least like them from each four-statement set. Results are shown as a personality-type bar graph with supporting details. Rock simplifies each DISC scale to four levels and maps results to 16 one- or two-letter personality types. ([DISC Personality Assessment](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/disc-personality-assessment))
- **Spiritual Gifts:** results classify gifts as dominant, supportive and other; the resulting attributes can be queried with person Data Views. ([Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts))
- **Motivators:** results include growth propensity, a composite score, ranked motivators and leading themes. When using these results for service placement, official guidance recommends considering roles aligned with the person’s five to seven highest motivators and avoiding roles centered on the five to seven lowest when practical. ([Motivators](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/motivators))
- **Emotional Intelligence:** each question accepts one of five frequency responses. Results cover Self-Awareness, Self-Regulating, Others-Awareness, Others-Regulating, EQ in Problem Solving and EQ Under Stress. These measurements are searchable person attributes, so a Data View can filter for a measurement and rating such as High Others-Awareness. ([Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence))
- **Conflict Engagement:** results rank five modes and three themes as high, medium or low and display mode and theme graphs. Result attributes support filters such as a High Solving theme. ([Conflict Profile](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile))

Use these results as the assessment defines them. The evidence does not support treating any score as a clinical diagnosis or as a universal placement decision.

## Achievements

### Types, attempts and progress

An Achievement Type defines a goal that Rock can evaluate automatically from engagement or interaction data. The documented configuration can use sources including giving, Step Program completion, interactions, accumulative Streak engagement and consecutive Streak engagement. An Achievement Attempt records an entity’s progress toward the goal. ([Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements), [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types))

An attempt closes when it succeeds or fails. After a failure, Rock can start a new attempt when the entity next performs the activity that begins the goal. Attempt progress is stored as a decimal fraction: `0.5` means 50 percent, and `1` means complete and successful. If **Allow Overachievement** is enabled, displayed progress may exceed 100 percent. ([Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements), [Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts), [Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types))

An Achievement Type cannot simultaneously track overachievement and cap the number of accomplishments. Rock must interpret excess qualifying events either as progress beyond 100 percent or as another accomplishment. ([Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types))

### Workflows, badges and Step integration

An Achievement Type can launch distinct workflows when an attempt starts, succeeds or fails. When no badge Lava template is supplied, Rock uses the Achievement icon; Step Program Completion uses the Step Program icon instead. If neither applicable icon is configured, Rock uses the default Achievement badge icon. ([Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings))

With **Add Step on Success** enabled, successful completion can create a Step in the selected program and type with the selected status. Rock uses the Achievement completion date as the configured Step start or end date, respects Step prerequisites and creates repeated Steps for recurring Achievements only when the Step Type permits multiple completions. ([Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types))

### Overrides and rebuilds

Although normal processing is automated, an operator can manually add or edit an individual attempt, including start date, end date and progress. Because a progress value of `1` makes the attempt successful, an override changes more than presentation and should be treated as an outcome-changing operation. ([Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts))

Rebuilding an Achievement Type deletes and recalculates each person’s attempt data occurring after that person’s latest successful attempt. Determine the affected population and preserve review evidence before using this operation. ([Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types))

## Reminders

A Reminder Type defines the entity that can receive reminders and may be secured to particular roles or people. Manual creation requires both a type for the current entity and a page that supplies that entity as context. A workflow action can also create reminders automatically. ([Configure Reminder Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-reminder-types), [Add a Reminder](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/add-a-reminder))

A type can notify through either a communication or a workflow. It can include the reminder note in email and can complete the reminder automatically after notification; otherwise, the reminder remains active. Communication notification sends the assigned person the system communication selected by the Process Reminders job when the reminder date arrives. The documented default template is Reminder Notification. Workflow notification launches the configured workflow and supplies attributes keyed for the reminder, reminder type, person, entity type and entity. ([Configure Reminder Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-reminder-types), [Configure Notification Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-notification-types))

The Process Reminders job can include or exclude selected types. **Max Reminders Per Entity Type** limits how many reminders for each entity type appear in the notification communication. Processing triggers the configured communication or workflow, may complete reminders when the type requests it and refreshes the active-reminder count shown in page headers. ([Use the Process Reminders System Job](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/use-the-process-reminders-system-job))

In Rock 19.0, a reminder is due when its date has arrived and a communication or workflow has issued it; an active reminder with a future date is not due. Users can open Reminders from the page header, filter by status, type, date or entity and mark an item complete. A repeating reminder schedules its next occurrence from the completion date of the current occurrence, not the original due date. A blank repeat count makes recurrence indefinite. ([Intro to Reminders](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/intro-to-reminders), [Add a Reminder](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/add-a-reminder))

## Following

Users can follow a person from the profile, add or remove followed people through bulk updates and manage the list under **My Settings > Following**. Under **Following Settings**, each user chooses which enabled events should produce notifications. Rock checks followed people daily and emails personalized matches. Administrators can define additional event types. ([How to Follow](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/how-to-follow), [Intro to Following](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/intro-to-following))

A user needs View permission for a Following Event to subscribe. If that permission is gone when notifications are generated, the event is omitted. Following Event evaluation does not enforce the security of related notes or groups, so an event that represents sensitive records must be secured consistently with those records. ([Configure Follow Events](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/configure-follow-events))

A Person History event can match configured demographic-history fields, old and new values, the person who made the change and a maximum lookback period. With **Match Both**, old and new values must match together. Without it, either side may match; a blank old or new value acts as a wildcard for that side. ([Person History Following Event](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/person-history-following-event))

Following a group makes it available from the follower’s My Dashboard. An event registration that places registrants in a group can notify every person following that group. Following Suggestions must be active to run. **Reminded Days** controls when an unfollowed suggestion can be presented again, while a blank value prevents reminders. The built-in In Group Together and In Followed Group suggestion types can limit followers and suggested people by configured group type, group, group role or security role. ([Follow a Group](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/follow-a-group), [Following Suggestions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/following-suggestions))

## Interactive Experiences

Interactive Experiences accept anonymous or personalized answers through Rock Mobile and expose submitted responses for live monitoring. The Experience Manager lets an operator monitor participation, change which actions participants see in real time and preview the participant view. ([Intro to Interactive Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/intro-to-interactive-experiences), [Use the Experience Manager](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/use-the-experience-manager))

The administrator controls when a question is shown and closed. When moderation is enabled, responses requiring approval are excluded from the real-time visualizer until approved. The manager supports approving or rejecting them. The presenter view can show incoming responses in real time, select a question and optionally filter responses by campus. Results can be rendered graphically or as a word cloud whose word size reflects response count. ([Handle Experience Questions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/handle-experience-questions), [Use the Experience Visualizer](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/use-the-experience-visualizer))

A schedule can restrict visibility through a Data View or required group membership. Campus association can use nearby campus geofences, the participant’s current geofence or the campus on the person record. Either geofence-based mode requires campus geofences to be configured. ([Administer Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/administer-experiences))

## Sign-Ups

Sign-Ups support short-term opportunities, including uses beyond serving projects, and can enforce participation thresholds. On the external Sign-Ups Finder, guests can filter by date and location, inspect an opportunity and register themselves and additional people without an event registration template. ([Intro to Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/intro-to-sign-ups))

In Rock 19.0, a Sign-Up project is the underlying group. People registered for different opportunities in the same project are added to that shared group. A Sign-Up Overview communication sends each recipient one message even when the recipient is registered for several selected opportunities; its `Opportunities` Lava collection can be iterated to include each registration. ([Manage Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/manage-sign-ups))

The default registration and reminder communications use SMS as well as email. An organization phone number must be configured on those system communications to avoid send errors. A custom Sign-Up group type must inherit from the Sign-Up Group type, be allowed as a child of the original type, provide at least one group-schedule option and a location-selection mode, and be included in the Sign-Up Finder block’s Project Types setting. ([Configure Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups))

To register an existing group’s members, use a Sign-Up Register block in Group mode and route the project, location, schedule and group through their IdKey values; the project parameter represents the Sign-Up group. A Sign-Up Attendance Detail page identifies project, location and schedule by IdKey and the occurrence by a `yyyy-MM-dd` attendance date. Attendance reminder links can be generated through the Group Attendance Reminder system communication. ([Group Registration and Attendance for Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/group-registration-and-attendance-for-sign-up))

Manage Members, Edit or Schedule permission at the project or group-type level permits adding and removing attendees. Creating a Sign-Up group requires Edit permission for the Project Type group attribute; creating one at the top level also requires Edit permission on the Sign-Up Groups block. ([Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions))

## Version And Authority Caveats

Most official documentation captured in this evidence pack was hydrated against the documentation’s current v19.0 presentation. Claims without explicit version scope should not be treated as proven for every earlier or later release.

Explicitly versioned evidence includes:

- Rock 18.1 added the Core Steps program and Step Type transfer capability.
- Rock 18.3 fixed Step Program editing and workflow-trigger association problems.
- Rock 19.0 evidence describes current Reminder and Sign-Up behavior in those articles.
- Rock 19.5 fixed large Achievement Type pages timing out, Sign-Up Finder group-security filtering, unintended Step Status Changed workflow launches and a `modifystep` creation error.
- Rock 20.0 was shown as Alpha in the captured release notes and included a fix preventing deletion of system-level Step Type attributes from the Step Type editor.

([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

The Outreach Toolbox evidence is a medium-confidence official video statement about Rock v19. It describes contact-specific prayer and connection cadences, completed touchpoint history, periodic pulse updates and configurable milestone prompts. Before ministry use, review who can see the contact data and which block settings are enabled. It should not be assumed available or configured from this guide alone. ([Outreach Toolbox is Here in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s))

The supplied community historical-data recipe is an example rather than official behavior. The unanswered Q&A record about Mailgun tracking provides no approved resolution and is not used as troubleshooting evidence.

## Troubleshooting Decision Tree

### A Step has a completion date but is not counted as complete

1. Inspect the Step’s current status.
2. Confirm that the status is configured as an **Is Complete** status in the Step Program.
3. Confirm that both the completion date and completion status are present.
4. If a workflow should have launched, inspect the program- or type-level trigger and installed Rock version.
5. Stop when both completion signals are correct and the expected downstream behavior has been rechecked. ([Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs))

### Step automation did not create or complete a record

1. Confirm the person currently qualifies for the Auto-Complete Data View.
2. Confirm the Steps Automation job has processed the Step Type.
3. Inspect unmet prerequisite Steps.
4. If a record already exists, inspect **Allow Multiple** before expecting another occurrence.
5. Do not assume Data View membership overrides prerequisites or repeat limits. ([Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types))

### A Steps badge appears but its count does not

1. Confirm the badge is a Person badge of type Steps and points to the complete program.
2. Confirm the badge was added to the Person Profile badge container.
3. Confirm the Step Type has **Show Count on Badge** enabled.
4. Confirm the badge uses Normal display mode; the setting does not affect other modes. ([Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges))

### Step metrics or charts appear inflated or use unexpected dates

1. Determine whether the metric counts Step occurrences or distinct people.
2. Check whether the Step Type permits multiple completions.
3. Inspect the chart’s status filter: completed statuses use completion dates; other statuses use start dates.
4. For impact measures, inspect every applicable Step Type’s Impact Weight.
5. For a Step Flow chart, inspect the maximum displayed level before interpreting apparent drop-off. ([Intro to Step Programs](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-step-programs), [Intro to Step Charts](https://community.rockrms.com/documentation/engagement/steps/steps-charts/intro-to-step-charts), [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types))

### A manually enrolled person has a streak of zero

1. Confirm the person’s enrollment date.
2. Inspect the occurrence map for eligible dates after enrollment.
3. Determine whether the engagement map contains participation.
4. If historical attendance should populate the map, consider an individual rebuild.
5. Before rebuilding, record any manual engagement-map changes because the rebuild deletes them. ([Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment), [Rebuild Streaks Individually](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually))

### A Streak Type map was changed but participant totals have not updated

1. Distinguish an occurrence-map edit from an individual engagement- or exclusion-map edit.
2. For an individual map edit, save and refresh the page.
3. For an occurrence-map edit, confirm that the nightly cleanup job has run.
4. Inspect enrollment dates because earlier dates remain outside each person’s calculation. ([Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail), [Manually Track Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks))

### A streak spans a date that still looks absent

1. Inspect the person’s exclusion map and applicable location exclusions.
2. Confirm whether that date was excluded.
3. Do not treat the visible absence as proof of a calculation error: exclusions do not alter attendance data.
4. Confirm that the excluded date neither added to nor interrupted the calculated streak. ([Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date))

### A person cannot retake an assessment

1. Inspect **Minimum Days to Re-take** on the installed Assessment Type.
2. Compare the previous completion date with that interval.
3. Inspect **Requires Request**.
4. If a request is required, confirm that a valid pending request exists.
5. Check the external My Account and results-page paths only after the policy conditions pass. ([Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments))

### An assessment request cannot be canceled

1. Open the person’s assessment history.
2. Confirm whether the entry is requested or self-initiated.
3. Inspect its completion status and completion date.
4. Stop if the assessment is complete; completed requests cannot be deleted or canceled through this operation. ([View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history))

### Achievement progress or attempt state looks wrong

1. Interpret stored progress as a decimal fraction, not a whole-number percentage.
2. Check whether `1` has made the attempt successful.
3. Inspect whether **Allow Overachievement** permits display above 100 percent.
4. Confirm that overachievement and Max Accomplishments are not being expected simultaneously.
5. Determine whether the attempt is still open, closed successfully or closed unsuccessfully.
6. Consider a rebuild only after documenting that it recalculates attempt data after each person’s latest success. ([Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts), [Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types))

### A Reminder was created but no notification occurred

1. Confirm the Reminder Type’s entity type, security and notification mode.
2. Confirm that the reminder date has arrived.
3. Confirm that the Process Reminders job includes the type and does not exclude it.
4. For Communication mode, inspect the job’s selected system communication.
5. For Workflow mode, inspect the configured workflow and expected supplied attributes.
6. Check whether automatic completion changed the reminder’s status after notification. ([Configure Notification Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-notification-types), [Use the Process Reminders System Job](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/use-the-process-reminders-system-job))

### A Following notification is missing

1. Confirm that the recipient follows the person or group.
2. Confirm that the event is enabled in the recipient’s Following Settings.
3. Confirm that the recipient has View permission for the Following Event at generation time.
4. Inspect the event’s filters and lookback window.
5. Account for daily evaluation rather than assuming immediate delivery.
6. For Person History matching, inspect Match Both and blank-value wildcard behavior. ([How to Follow](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/how-to-follow), [Configure Follow Events](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/configure-follow-events), [Person History Following Event](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/person-history-following-event))

### An Interactive Experience response is missing from the visualizer

1. Confirm that the question is currently shown and not closed.
2. Confirm that the response was submitted to the intended experience.
3. If moderation is enabled, inspect whether the response awaits approval or was rejected.
4. Inspect campus filtering in the manager or presenter view.
5. If audience restrictions are involved, inspect the schedule’s Data View or group-membership condition. ([Intro to Interactive Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/intro-to-interactive-experiences), [Use the Experience Manager](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/use-the-experience-manager))

### A Sign-Up communication or attendance link fails

1. For registration or reminder communication errors, confirm that an organization phone number is configured for the SMS-enabled system communication.
2. For a registration route, verify project, location, schedule and, when applicable, group IdKeys.
3. Remember that the project parameter represents the Sign-Up group.
4. For attendance, confirm the occurrence date uses `yyyy-MM-dd`.
5. Inspect project or group-type permissions before changing attendee records. ([Configure Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups), [Group Registration and Attendance for Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/group-registration-and-attendance-for-sign-up), [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions))

## Agent Task Recipes

### Recipe: Configure a Step journey with reliable completion signals

**Outcome:** A Step Program whose order, prerequisites and completion semantics match the intended journey.

1. Define the journey’s Step Types and decide whether sequence is required, preferred or display-only.
2. Select the corresponding Completion Flow.
3. Configure statuses and identify which statuses are complete.
4. Configure each type’s prerequisites, repeatability and spans-time behavior.
5. Add only the Step Attributes needed for the operational record; enable Show in Grid or Show on Bulk where appropriate.
6. Test one participant record with the intended date and status combination.
7. Verify the change in Person History.

**Inspect:**

- Completion Flow and prerequisites.
- Complete-status configuration.
- Date requirements and Allow Multiple.
- Steps block Edit permission.

**Do not assume:**

- A completion date alone means complete.
- A prerequisite survives moving the Step Type to another program.

([Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs), [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types), [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry))

### Recipe: Bulk-record a Step

**Outcome:** Multiple selected people receive the intended Step data without silently losing per-person attribute differences.

1. Choose either selected-person grid update or Step Program/Step Type bulk entry.
2. Confirm the target program, type, status and applicable date fields.
3. Apply shared attributes only when Show on Bulk is enabled and one value is correct for every selected person.
4. Enter differing attribute values separately for each person.
5. Verify sample records and their profile history.

**Stop when:** The selected people have the intended records and a sample confirms dates, status and attributes. ([Use Bulk Entry With Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps), [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry))

### Recipe: Automate Step completion from a Data View

**Outcome:** The Steps Automation job creates or completes qualifying records while preserving journey rules.

1. Build and validate the person Data View.
2. Assign it as the Step Type’s Auto-Complete Data View.
3. Inspect prerequisites and Allow Multiple.
4. Run or wait for the configured Steps Automation job according to the installation’s operating procedure.
5. Verify qualifying, prerequisite-blocked and already-completed examples.

**Do not assume:** Every person in the Data View receives a new record; prerequisites and repeat limits remain active. ([Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types))

### Recipe: Build a Streak Type safely

**Outcome:** A Streak Type calculates the intended cadence from the intended source.

1. Define the activity source, target population, frequency and earliest applicable date.
2. Decide whether enrollment is required.
3. Decide whether Sync Linked Activity’s bidirectional behavior is appropriate.
4. Configure and inspect the occurrence map.
5. Enroll a small test population.
6. Verify engagement, non-engagement and exclusion examples.
7. Confirm the operational job timing before expanding use.

**Stop when:** The test cases produce the intended current and longest streaks.

**Do not assume:** Start date or frequency can be corrected later; both are locked after save. ([Add a New Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type), [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps))

### Recipe: Correct one person’s streak

**Outcome:** A bounded correction is made without unnecessarily rebuilding the entire Streak Type.

1. Inspect the occurrence map and the person’s enrollment date.
2. Compare attendance with the engagement map.
3. Add or remove an engagement only if the map should differ from the source-driven result.
4. Add an individual exclusion when an absence should be ignored for that person.
5. Save and refresh.
6. Verify current streak, longest streak and engagement count.

**Do not assume:** An exclusion removes or changes attendance.

**Stop when:** The person’s calculated values match the intended maps. ([Manually Track Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks), [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date))

### Recipe: Rebuild a Streak with a controlled boundary

**Outcome:** Attendance-derived streak data is regenerated at the smallest necessary scope.

1. Decide whether the problem affects one enrollment or the entire Streak Type.
2. Record existing manual map adjustments in the affected scope.
3. Confirm the Streak Type start date and occurrence map.
4. Use individual rebuild for one person; use type rebuild only for a type-wide regeneration need.
5. Verify enrollment dates, maps, current streaks and longest streaks after completion.
6. Reapply only reviewed manual exceptions that remain valid.

**Stop when:** Rebuilt data is verified and expected manual changes have been reconciled. ([Rebuild Streaks Individually](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually), [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type))

### Recipe: Request and monitor assessments

**Outcome:** The intended people receive valid assessment requests and their completion state can be reviewed.

1. For one person, use Request Assessment from the profile, select one or more assessments and provide the custom message.
2. For many people, use a communication that generates the assessment’s external URL from the public application root and each recipient’s URL-encoded person key.
3. Tell recipients that requests are also available from My Account.
4. Review pending and complete entries on person assessment histories.
5. Cancel an incorrect request only while it remains incomplete.

**Inspect:**

- Assessment Type request requirement.
- Public application root and recipient key handling.
- Requested versus self-initiated history.

([Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests), [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history))

### Recipe: Build an assessment-result segment

**Outcome:** A person Data View identifies people with a specified supported assessment result.

1. Select the assessment and exact result measurement or attribute.
2. Choose the documented rating or result condition.
3. Build the person Data View filter.
4. Validate sample included and excluded records.
5. Use the resulting population for the separately governed grouping or reporting task.

**Do not assume:** Similar-looking measurements across different assessments have the same meaning. ([Intro to Assessments](https://community.rockrms.com/documentation/engagement/assessments/overview/intro-to-assessments), [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence), [Conflict Profile](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile))

### Recipe: Connect an Achievement to workflows and Steps

**Outcome:** A successful Achievement produces the intended follow-up and journey record.

1. Define the Achievement source, target and success conditions.
2. Choose either overachievement or capped accomplishments.
3. Configure start, success and failure workflows as needed.
4. Enable Add Step on Success.
5. Select the Step Program, Step Type and status.
6. Confirm that the target Step’s prerequisites and Allow Multiple behavior match recurring Achievement behavior.
7. Test start, success and failure paths with bounded records.
8. Verify the attempt, workflow result and generated Step independently.

**Do not assume:** Achievement success overrides Step prerequisites or repeat limits. ([Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types), [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings), [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types))

### Recipe: Configure Reminder processing

**Outcome:** A context-valid reminder produces the intended communication or workflow at its reminder date.

1. Define the Reminder Type’s entity and security.
2. Choose Communication or Workflow notification.
3. Configure note inclusion and automatic completion deliberately.
4. For Communication, select the system communication in the Process Reminders job.
5. For Workflow, configure the workflow to receive the supplied reminder-related attributes.
6. Include the type in job processing and set any per-entity limit.
7. Test a bounded reminder and verify delivery or workflow launch, completion behavior and header count.

([Configure Reminder Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-reminder-types), [Configure Notification Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/configure-notification-types), [Use the Process Reminders System Job](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders/use-the-process-reminders-system-job))

### Recipe: Configure a secure Following event

**Outcome:** Authorized subscribers receive the intended daily event without exposing related sensitive context.

1. Define the event and its matching conditions.
2. Secure View permission to the intended subscribers.
3. Review the security of related notes, groups and represented records separately.
4. Enable the event in a test subscriber’s Following Settings.
5. Validate matching and non-matching examples.
6. Verify the next daily notification output.

**Stop when:** The correct subscriber receives only authorized event information. ([Configure Follow Events](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/configure-follow-events), [How to Follow](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/how-to-follow))

### Recipe: Operate a moderated Interactive Experience

**Outcome:** Participants receive the intended actions while only approved responses appear publicly.

1. Configure the schedule and any Data View, group or campus restrictions.
2. Preview the participant experience.
3. Open the intended question.
4. Monitor incoming responses.
5. Approve or reject responses requiring moderation.
6. Select the presenter question and campus filter.
7. Close the question when participation should end.
8. Verify graphical or word-cloud output from approved responses.

([Administer Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/administer-experiences), [Use the Experience Manager](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/use-the-experience-manager), [Use the Experience Visualizer](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/use-the-experience-visualizer))

### Recipe: Configure a Sign-Up registration and attendance route

**Outcome:** Guests or an existing group can register, and authorized operators can record attendance.

1. Confirm the project’s underlying group and opportunity structure.
2. For a custom project type, verify inheritance, child-type allowance, schedule option, location mode and Finder inclusion.
3. Configure the external Finder for guest self-registration, or configure Sign-Up Register in Group mode for an existing group.
4. Pass the required project, location, schedule and group IdKeys.
5. Configure the attendance page with the required IdKeys and a `yyyy-MM-dd` occurrence date.
6. Configure the Group Attendance Reminder communication when reminder links are needed.
7. Verify the organization phone number on SMS-enabled registration and reminder communications.
8. Test with an account holding the intended project or group-type permissions.

([Configure Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups), [Group Registration and Attendance for Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/group-registration-and-attendance-for-sign-up), [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions))

## Known Gaps And Live Verification

No live Rock instance was reviewed for this guide. Before operational use, verify:

- The installed Rock version and whether relevant release fixes are present.
- Availability and configuration of the Steps Automation, nightly cleanup and Process Reminders jobs.
- Actual Step Program statuses, prerequisites, attributes, workflow triggers and block permissions.
- Streak Type sources, synchronization, start dates, occurrence maps, enrollment dates and manual exceptions.
- Assessment Type retake intervals, request requirements, external paths and access controls.
- Achievement event providers, attempt volume, workflow configuration, badge templates and Step integration.
- Reminder entity context, security, notification communication and workflow attribute mapping.
- Following Event visibility and the security of related notes or groups.
- Rock Mobile configuration, audience restrictions, campus data and geofences for Interactive Experiences.
- Sign-Up project types, page blocks, IdKey routes, communication phone numbers and attendee-management permissions.
- Outreach Toolbox availability, block settings and contact-data visibility.

The evidence pack does not establish:

- A universal configuration for any organization.
- Current behavior for every Rock version.
- Installation-specific record counts or data quality.
- Successful job execution, communication delivery, workflow completion or mobile presentation.
- A safe automated method for historical Step migration.
- A resolved answer for workflow-email analytics in the supplied unanswered community Q&A.
- That built-in assessment questions can be customized; official documentation says their questions and answer formats are not configurable. ([Take Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/take-assessments))

## Source Map

### Official engagement documentation

- [Steps](https://community.rockrms.com/documentation/engagement/steps): program, type, entry, automation, badge and chart documentation.
- [Streaks](https://community.rockrms.com/documentation/engagement/streaks): maps, type configuration, enrollment, exclusions and rebuilds.
- [Assessments](https://community.rockrms.com/documentation/engagement/assessments): requests, retakes, history and built-in assessment results.
- [Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements): types, attempts, workflows, badges and Step creation.
- [Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools): Reminders, Following, Interactive Experiences and Sign-Ups.

### Version and implementation evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): version-specific additions and fixes.
- [StepProgramCompletion.cs at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs): implementation description of Step Program Completion records.
- [StepProgramCompletion.Logic.cs at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs): implementation evidence for inherited security authority.
- [Outreach Toolbox is Here in v19](https://www.youtube.com/watch?v=LNcx8t0mlQ4&t=476s): version-oriented overview of Outreach Toolbox tracking.

### Community example

- [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233): reviewed community migration pattern retained only as a historical example, not official Rock behavior.