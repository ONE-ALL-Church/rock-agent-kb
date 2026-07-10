---
id: authored-engagement-tracking
title: Engagement Tracking
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Engagement Tracking

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Engagement Tracking index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Engagement Tracking in Rock RMS is not one feature. It is a family of tools for representing movement, participation, completion, and readiness across a person’s relationship with the organization. The main pieces are:

- **Steps**: configured ministry journeys made of Step Programs, Step Types, Step Statuses, and individual Step records. Use them when the organization wants to track that a person started, completed, or repeated a meaningful ministry action such as baptism, membership, serving onboarding, training, or a discipleship milestone. See the official [Steps documentation](https://community.rockrms.com/documentation/engagement/steps).
- **Streaks**: attendance-pattern tracking built around occurrence, engagement, and exclusion maps. Use them when the question is not merely “did this person attend?” but “how consistently has this person been participating?” See [Streaks](https://community.rockrms.com/documentation/engagement/streaks) and [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps).
- **Assessments**: built-in tools for collecting structured self-assessment results such as DISC, Spiritual Gifts, Motivators, Emotional Intelligence, and Conflict Profile. Use them for volunteer placement, staff development, leadership coaching, and search/reporting against assessment-derived attributes. See [Assessments](https://community.rockrms.com/documentation/engagement/assessments).
- **Achievements**: configurable goals evaluated against engagement or interaction data, with attempts, badges, workflows, prerequisites, and optional Step creation on success. Use them when an agent needs to recognize patterns automatically, such as completing a Step Program or maintaining a streak. See [Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements).
- **Related engagement surfaces**: Reminders, Following, Interactive Experiences, Sign-Ups, Learning LMS engagement, Communications, Groups, Data Views, Reports, and Security all intersect with engagement work. The official engagement navigation lists these under [Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools).

For agents doing real Rock work, the most important rule is to identify the **engagement signal** before touching configuration. A Step is a record of a person’s movement through a configured program. A Streak is a computed or manually adjusted attendance pattern. An Assessment is a structured result stored against the person and surfaced through history, attributes, and Data Views. An Achievement is an automation layer that evaluates source data and creates attempts, badge output, workflow activity, and sometimes Steps.

Do not assume every engagement feature is present or configured the same way in every Rock instance. Before changing production data, inspect the live Rock version, enabled pages, block types, entity records, security, categories, workflow triggers, Step statuses, Achievement components, and relevant system jobs. Some features have important version caveats, including v18.1 additions for Core Steps, Step Analytics, Step Type transfer, and LMS engagement changes, plus v18.3 fixes for Achievement Type saving, Achievement Attempt workflow timing, and Step Program workflow trigger associations in the [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 2. Scope And Terminology

This guide covers the engagement-tracking layer around Steps, Step Programs, Step Types, Streaks, Assessments, Achievements, completion signals, journey-style tracking, and reporting. It also explains how these features connect to People, Groups, Workflows, Communications, Data Views, Reports, Security, and Learning LMS engagement.

The guide does not replace live-instance review. Rock organizations frequently customize page routes, block settings, Step statuses, categories, attributes, badges, workflows, and security. When a fact depends on the local instance, this guide says what to inspect.

Core terms:

**Person**
The human record being tracked. Many engagement entities reference a `PersonAlias` rather than the `Person` row directly. In source snippets, Step Program Completion and Achievement examples reference `PersonAlias` or an achiever entity rather than only a person ID. See the Step Program Completion model in [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs).

**Step Program**
A configured collection of Step Types that represents a journey or program. Rock’s documentation describes Step Programs as the organizing container for individual activities and accomplishments, and the admin area is reached from `People > Engagement > Steps` in the v19 docs. See [Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps) and [About Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-steps).

**Step Type**
A configured activity, milestone, or ongoing engagement inside a Step Program. It has display settings, status behavior, attributes, workflow triggers, and advanced settings. See [About Step Types](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-step-types) and [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types).

**Step**
The actual person-specific record that a person started, completed, or is otherwise associated with a Step Type. Step entry supports person, campus, date fields, status, and attributes depending on Step Type configuration. See [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry).

**Step Status**
A configured status in a Step Program. Step statuses can represent started, in progress, completed, or custom states. Source-code view models expose whether a status is a completion status, which matters for completion reporting and workflows. See [`StepStatusBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/StepTypeDetail/StepStatusBag.cs).

**Step Program Completion**
A derived model representing that a person completed a full set of completed Steps for a Step Program. The source model explains that Rock records completion when there is a completed Step for each Step Type in the program and uses the newest completed Step for each type in that completion set. See [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs) and the [Model Map](https://community.rockrms.com/ModelMap) record for Step Program Completion.

**Streak Type**
A configured streak definition that tells Rock what population and attendance pattern to evaluate. The official docs frame it as the configuration that defines where and when to look for streaks, such as weekend attendance or small group attendance, and who should be tracked. See [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types).

**Occurrence Map**
A Streak map defining when engagement could have happened. It is the schedule frame against which participation and absence are judged. See [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps).

**Engagement Map**
A person-specific Streak map indicating when the person did or did not participate.

**Exclusion Map**
A Streak map indicating dates to ignore for streak-count purposes. Exclusions change streak calculations but do not erase the underlying attendance record. See [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date).

**Assessment Type**
A configured assessment definition under `Admin Tools > System Settings > Assessment Types`, including retake timing and whether a request is required. See [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments).

**Assessment Request**
An invitation for a person to complete one or more assessments. Requests can be sent from a person profile or through communications to groups using Lava patterns described in the docs. See [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests).

**Achievement Type**
A configured goal definition. It includes the achievement component, source entity type, achiever entity type, active state, workflow hooks, badge Lava, prerequisites, limits, category, display settings, and optional Step creation. See [Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements), [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types), and [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

**Achievement Attempt**
A tracked attempt by an achiever to meet an Achievement Type. Attempts can be in progress, successful, or unsuccessful as an operational concept, even where the docs describe that there is not a formal status field exposed in the same way. See [Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts).

## 3. Engagement Tracking Mental Model

Think of Rock engagement as four layers.

The first layer is **raw activity**. Attendance records, group membership, communication activity, LMS activity completion, interactive experience responses, and manually entered records all describe what happened. In this layer, agents ask: What was observed? Where is the source record? Is it person-specific? Is it campus-specific? Is it tied to a group, schedule, occurrence, workflow, or class?

The second layer is **structured journey tracking**. Steps turn raw or staff-entered signals into a defined ministry path. A person can have a Step in a Step Type, with a date or date range, status, campus, attributes, and possibly workflows. Step Programs create the larger structure. This is the layer for “has this person taken the next action we care about?” The official Steps docs describe program navigation, program categories, Step Type counts, and Steps Taken counts under `People > Engagement > Steps` in [About Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-steps).

The third layer is **pattern recognition**. Streaks and Achievements look across multiple records or periods and produce a higher-level signal. A Streak answers consistency questions: how many eligible periods in a row did the person engage? An Achievement answers goal questions: did the achiever satisfy configured conditions, and should Rock record an attempt, badge, workflow, or Step? Streaks depend heavily on maps; Achievements depend heavily on components, source entities, and processing. See [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps) and [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs).

The fourth layer is **activation and reporting**. Engagement data becomes operational only when it appears in Person Profile badges, grids, charts, Data Views, reports, workflows, communications, dashboards, or staff processes. Step badges can surface program progress on a Person Profile or connection-related screens, according to [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges). Step charts expose trends, totals, campuses, statuses, and flow perspectives in [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types). Assessment results can be searched through Data Views, as the Spiritual Gifts and Emotional Intelligence articles describe for assessment-derived attributes: [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts) and [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence).

An agent should therefore diagnose engagement tasks in this order:

1. Identify the underlying source signal.
2. Identify the engagement abstraction that should represent it.
3. Verify configuration and entity relationships.
4. Verify security and page/block access.
5. Verify automation, jobs, workflows, and version caveats.
6. Verify reporting and staff-facing surfaces.
7. Make changes only after rollback/readback strategy is clear.

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. **Official Rock documentation** for administrator workflows, navigation, configuration fields, and intended usage. The pack’s strongest sources are the v19 official docs for [Steps](https://community.rockrms.com/documentation/engagement/steps), [Streaks](https://community.rockrms.com/documentation/engagement/streaks), [Assessments](https://community.rockrms.com/documentation/engagement/assessments), and [Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements).
2. **Rock source code** for entity fields, API/code-generation markers, security inheritance, validation, view-model properties, and implementation landmarks. Use snippets such as [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs), [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs), [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs), and [`StepProgramStepTypeFieldType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/StepProgramStepTypeFieldType.cs).
3. **Release notes** for version-sensitive behavior. The source pack includes v18.1 and v18.3 changes from the [Rock Core Release Notes](https://www.rockrms.com/releasenotes), including Core Steps, Step Type transfer, Step Analytics, Achievement Type fixes, Achievement Attempt workflow timing, and Step Program workflow-trigger association fixes.
4. **Model Map** for reporting/model availability and naming. The pack identifies “Step Program Completion” as a model in the Engagement category via the [Model Map](https://community.rockrms.com/ModelMap).
5. **RockU** for training coverage. The pack records an Engagement training section that includes Step Programs, Adding Steps, Steps Badges, Step Flow legacy, Step Charts, Step Types, and Steps Overview at [RockU Engagement](https://community.rockrms.com/rocku/engagement), but the hydrated page returned limited usable content, so treat it as a training pointer rather than a source for precise configuration details.
6. **Community recipes and Q&A** for examples and edge cases only. The recipe for [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233) is useful as a historical-data migration pattern, but the page itself warns that recipes are community contributed and not core-reviewed. Use community content only after official docs and source-code records.

How to use this guide:

- Use the section headings to orient an agent in live work.
- Use citations to jump to the official or source-code record.
- When an instruction says “inspect,” perform live readback in the target Rock instance before deciding.
- For public documentation work, keep source quotations short and synthesize in your own words.
- For production operations, avoid SQL writes unless explicitly authorized, and prefer UI/API-supported operations where possible.

## 5. Core Configuration And Data Model

### Steps Configuration

The Steps administrative surface is under `People > Engagement > Steps` in the v19 documentation. From there, administrators manage Step Programs, Step Types, participant lists, metrics, charts, and Step entry workflows. See [About Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-steps).

A Step Program typically includes:

- **Name**: the public/admin name of the program.
- **Active**: whether the program is available for tracking.
- **Description**: context for admins and staff.
- **Icon CSS Class**: display icon for the program.
- **Category**: grouping managed through Category Manager for the Step Program entity type.
- **Completion Flow**: rules controlling how participants progress through Step Types.
- **Default List View**: grid/list presentation behavior.
- **Statuses**: Step statuses for the program.
- **Entity Attributes**: attributes attached to Step records or related entities depending on configuration.
- **Workflows**: workflow triggers associated with program-level or status-related events.

These fields are described in [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs). The release notes include a v18.3 bug fix where editing a Step Program could remove Step Type associations from workflow triggers, and Step Type-level triggers could appear incorrectly on the Step Program Detail block. If troubleshooting workflow triggers in v18.0-v18.2-era systems or recently upgraded environments, verify this against the [Release Notes](https://www.rockrms.com/releasenotes).

A Step Type typically includes:

- **Name**.
- **Active**.
- **Description**.
- **Highlight Color** for charts and legends.
- **Icon** or CSS icon.
- **Show Count on Badge**, which affects badge display for that Step Type.
- **Engagement Type**, such as milestone versus ongoing engagement.
- **Impact Weight**, used where the configured engagement model considers relative importance.
- **Step Attributes**.
- **Workflows**.
- **Advanced Settings**.

See [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types). Some specific field names and exact options can vary by version, so inspect the live Step Type edit block when writing operational instructions for a local instance.

A Step record entered for a person can include:

- Person.
- Campus.
- Date, Start Date, or End Date depending on whether the Step spans time.
- Status.
- Step attributes, if configured.
- Context from the page path, such as entering from a Step Type page versus a Person Profile.

The official [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry) article explains that person may be pre-filled when entering from the Person Profile, while Step-area entry requires selecting a person.

### Step Status And Completion

Step statuses are program-specific status records that determine whether a Step is counted as complete. The source view models expose this in a compact way: the Step Type Detail status bag has a `stepStatus` and an `isCompletionStatus` flag in [`StepStatusBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/StepTypeDetail/StepStatusBag.cs). The TypeScript version mirrors that shape in [`stepStatusBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/StepTypeDetail/stepStatusBag.d.ts).

Operational implication: do not infer completion from a status name alone. Inspect whether the status is configured as a completion status. A status named “Done” or “Completed” may be obvious to staff, but reporting and model behavior should be verified against the configuration.

### Step Program Completion Model

The Step Program Completion model is important for analytics and reporting. The source describes it as a record of completing a Step Program for a person. Rock’s rule, based on the source snippet, is to create a completion when there is a completed Step for each Step Type in the program, using the newest completed Step for each type as the completion set. See [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs).

The model includes at least these properties in the source snippet:

- `StepProgramId`.
- `PersonAliasId`.
- `CampusId`.
- `StartDateTime`.
- `EndDateTime`.
- Navigation to `StepProgram`.
- Navigation to `PersonAlias`.
- Navigation to `Campus`.
- A collection of related `Steps`.

The source also marks `StepProgramCompletion` with Rock domain `Engagement`, table name `StepProgramCompletion`, REST code generation, and a system entity type GUID. The logic file sets `ParentAuthority` to the related Step Program when present, which matters for security inheritance. See [`StepProgramCompletion.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs).

Live verification: before building reports against Step Program Completion, inspect the local Rock version and schema. Confirm the model exists, confirm security behavior for the current user, confirm program statuses mark completion correctly, and confirm whether archived/inactive Step Types should be included in the local reporting question.

### Streaks Configuration

Streaks are configured under `People > Engagement > Streaks` in the v19 documentation. See [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types).

A Streak Type defines:

- The name and active state.
- The population to track.
- The relevant attendance source and schedule frame.
- The start date.
- The map and enrollment behavior.
- Related achievements.
- Occurrence map editing.
- Location exclusions.
- Enrollment list.

The [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail) article identifies key areas such as Streak Type information, Achievements, Occurrence Map Editor, Location Exclusions, and Streak Type Enrollment.

Streaks use three map concepts:

- **Occurrence Map**: when participation could have occurred.
- **Engagement Map**: when the person engaged.
- **Exclusion Map**: dates ignored for streak calculation.

These are defined operationally in [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps). An agent should always check maps before concluding that streak numbers are wrong.

### Assessments Configuration

Assessment administration has three major areas:

- Overview.
- Administer Assessments.
- Available Assessments.

See [Assessments](https://community.rockrms.com/documentation/engagement/assessments).

Rock’s built-in assessment set in the v19 docs includes:

- DISC Personality Assessment.
- Spiritual Gifts.
- Motivators.
- Emotional Intelligence.
- Conflict Profile.

See [Available Assessments](https://community.rockrms.com/documentation/engagement/assessments/available-assessments).

Assessment Type configuration lives under `Admin Tools > System Settings > Assessment Types`, according to [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments). Important configuration includes the retake interval and whether a formal request is required. The docs state the default retake interval is 365 days, but agents should inspect the live Assessment Type before telling a user they can or cannot retake an assessment.

Assessment history is visible from a person’s Person Profile under the History tab. The history list can include assessment name, pending/complete status, requested date, requester, and other request/result details depending on the block and version. See [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history).

### Achievements Configuration

Achievements are managed under `People > Engagement > Achievements` in the v19 documentation. See [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types).

An Achievement Type includes:

- Name.
- Active state.
- Description.
- Category.
- Achievement component/entity type.
- Source entity type.
- Achiever entity type.
- Maximum accomplishments allowed.
- Over-achievement behavior.
- Prerequisite achievements.
- Workflow launch settings for start, success, and failure.
- Badge Lava template.
- Results Lava template.
- Custom summary Lava template.
- Highlight color and icon.
- Public/display flags.
- Optional image files.
- Optional Step creation on success.

The source-code view model confirms many of these fields in [`AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs) and [`achievementTypeBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/AchievementTypeDetail/achievementTypeBag.d.ts). The entity model confirms fields such as `Name`, `Description`, `ComponentConfigJson`, `SourceEntityTypeId`, `AchieverEntityTypeId`, `ComponentEntityTypeId`, workflow type IDs, `AchievementStepTypeId`, `AchievementStepStatusId`, and Lava template fields in [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

An important validation rule appears in [`AchievementType.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.Logic.cs): if `MaxAccomplishmentsAllowed` is greater than 1, `AllowOverAchievement` cannot be true. An agent configuring achievements should check this before assuming a save failure is a generic UI problem.

Achievements can add Steps automatically when an achievement succeeds. The official [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types) article identifies the relevant fields: enable Add Step on Success, choose Step Program, choose Step Type, and choose Step Status. The source-code view model also exposes `addStepOnSuccess`, `stepProgram`, `achievementStepType`, and `achievementStepStatus`.

## 6. Primary Entities And Relationships

### Person, PersonAlias, And Engagement Records

Rock often stores engagement records against a `PersonAlias` rather than directly against a `Person`. The Step Program Completion source includes `PersonAliasId`, and Achievement source comments mention the original achiever was a `PersonAlias` through Streak. See [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs) and [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

Agent implication: when reconciling records, do not join only on person ID without checking aliases. In a live SQL or API investigation, inspect PersonAlias records and any merged-person history if data appears split across people.

### Step Program To Step Type

A Step Program owns many Step Types. The Step Program page shows Step Type counts and completed Step counts in the docs, and the source test creates a Step Program with many Step Types and Steps in [`StepProgramAchievementTests.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Engagement/Achievements/StepProgramAchievementTests.cs). The UI selection model also reflects this relationship: Step Type selection can be filtered by Step Program in [`StepProgramStepTypePicker.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs).

### Step Type To Step

A Step Type can have many Step records. Each Step belongs to a person alias and can be dated, statused, attributed, and related to completion. The exact columns should be confirmed in the live schema or API model for the target Rock version.

### Step Program Completion To Step Program, PersonAlias, Campus, And Steps

`StepProgramCompletion` relates to:

- One Step Program.
- One PersonAlias.
- Optional Campus.
- A collection of Steps used for the completion set.

The source model also declares `ParentAuthority => StepProgram`, so Step Program security can affect the completion record’s security authority. See [`StepProgramCompletion.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs).

### Streak Type To Enrollments And Maps

A Streak Type defines the tracking rules. Enrollments attach people to the Streak Type, each with an enrollment date. The [Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment) article emphasizes that each individual can have a different enrollment date. Maps then drive current and longest streak calculations.

### Achievement Type To Component, Source Entity, Achiever Entity, Attempts, Workflows, And Steps

An Achievement Type is component-based. Source code shows `ComponentEntityTypeId`, `SourceEntityTypeId`, and `AchieverEntityTypeId` on the entity model. It also has workflow type IDs for start, success, and failure, and optional Step Type and Step Status IDs for Step creation. See [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

Achievement processing is component-based. [`AchievementTypeService.Process`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs) gets the Achievement Type cache, resolves the achievement component, gets source entities, then processes each source entity with its own data context and saves changes. Operationally, this means a processing failure may be caused by cache resolution, component resolution, source query behavior, or per-source processing.

### Assessments To Person History And Attributes

Assessment request and result history appears on Person Profile History according to [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history). Specific assessment results can also be searchable through Data Views, as documented for [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts), [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence), and [Conflict Profile](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile).

Live verification: inspect the local attribute definitions and person attribute values before relying on a result field name in a Data View. Names, keys, security, and visibility can differ by version or customization.

## 7. Common Engagement Tracking Workflows

### Workflow: Build A Discipleship Step Program

Use Steps when the organization has a defined ministry journey.

1. Define the ministry journey in operational terms: what must a person do, in what order, and what counts as completion?
2. Create or edit a Step Program under `People > Engagement > Steps`, following [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs).
3. Assign a meaningful category from Category Manager if the organization will maintain many programs.
4. Choose a completion flow. Use strict linear flow only when Steps must be completed in order. If the local UI exposes custom prerequisites, verify each prerequisite before launch.
5. Create Step Types for each action, following [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types).
6. Configure statuses and mark the correct statuses as completion statuses.
7. Add Step attributes only when the data will be used operationally.
8. Configure workflows for staff notification, next-step automation, or external processes.
9. Configure Step badges if staff need profile-level visibility, following [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges).
10. Validate charts and reports after test entries.

Operational guardrail: do not over-model. If a Step Type will never drive reporting, workflow, staff action, or person care, it may belong as a note, group membership, or workflow state instead of a Step.

### Workflow: Enter An Individual Step

Use manual Step Entry when a staff person is recording a single person’s progress.

1. Open the person from Person Profile or open the Step Type participant list.
2. Launch Step Entry.
3. Verify the person if not pre-filled.
4. Choose campus if the Step should be campus-specific.
5. Set the correct date fields. If the Step spans time, use Start and End Date; otherwise use the single Date field as exposed by the block.
6. Choose the correct status.
7. Fill Step attributes.
8. Save, then verify the Step appears in the Step Type list, Person Profile, badge, and chart if applicable.

The official entry fields are described in [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry).

### Workflow: Bulk Add Or Update Steps

Use bulk entry when records are known and consistent across many people. The v19 docs describe two paths: selecting people from a list grid and using the bulk update icon, or using bulk entry mode from Step Program or Step Type pages. See [Use Bulk Entry With Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps).

Agent checklist:

1. Confirm the population with a Data View or grid filter.
2. Export or otherwise record a pre-change count if the work is high impact.
3. Confirm whether the Step Type allows multiple Steps per person.
4. Confirm completion status and dates.
5. If using historical dates, do not use a workflow/action pattern that stamps today’s date unless that is acceptable.
6. Run a small pilot batch first.
7. Verify duplicate prevention.
8. Verify charts and sample Person Profiles after bulk entry.

The community recipe [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233) illustrates a historical-data migration approach using Data Views and workflow batches, with cautions about duplicate Steps, timeouts, and Step Types that do not allow multiple Steps. Because it is a community recipe, treat it as a pattern to adapt, not a core-supported procedure.

### Workflow: Configure A Streak Type

Use Streaks when the organization wants attendance consistency.

1. Define the engagement event: weekend attendance, group attendance, class attendance, serving attendance, or another participation signal.
2. Define the population: all attenders, group members, campus-specific people, or another tracked subset.
3. Define the schedule frame: weekly, service-specific, group schedule, or another occurrence pattern.
4. Create the Streak Type under `People > Engagement > Streaks`, following [Add a New Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type).
5. Review the Streak Type Detail page, including Achievements, Occurrence Map Editor, Location Exclusions, and Enrollment, following [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail).
6. Rebuild only after understanding data loss implications for maps and enrollment.
7. Validate a known person’s attendance against their current and longest streak values.

### Workflow: Send Assessment Requests

Use assessment requests when the organization wants a person or group to take one or more built-in assessments.

1. For an individual, open the Person Profile, use the Actions button, and choose Request Assessment as described in [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests).
2. Select one or more assessments.
3. Add a message.
4. Send and verify the request appears in assessment history.
5. For groups, use the communication/Lava approach documented in the same article, but inspect the current communication template and assessment link behavior in the local instance before sending broadly.
6. After completion, review Person Profile History and any assessment-result attributes.

### Workflow: Configure An Achievement That Adds A Step

Use this when the achievement is the detection logic and the Step is the durable journey record.

1. Create or edit the Achievement Type under `People > Engagement > Achievements`.
2. Choose the correct achievement component and source.
3. Configure maximum accomplishments and over-achievement behavior.
4. Enable Add Step on Success.
5. Select the Step Program.
6. Select the Step Type.
7. Select the Step Status.
8. Configure success workflow only if downstream action is needed.
9. Process or trigger the achievement.
10. Verify the Achievement Attempt and the created Step on a sample person.

See [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types) and the source-code fields in [`AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs).

## 8. Steps Deep Dive

### What Steps Are For

Steps are Rock’s structured way to represent movement through a ministry path. They are not merely notes. They are configured engagement records with display, status, charting, workflow, badge, and reporting behavior. The official [Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps) frames a Step Program as the larger path and Step Types as the individual actions or accomplishments inside it.

A useful Step Program has three qualities:

1. It represents a meaningful journey.
2. It has staff action attached to it.
3. Its data will be reported, surfaced, or automated.

Poor Step Programs usually fail one of those tests. Examples include creating Step Types for every minor interaction, using Steps as a generic note system, or adding Steps that no team owns.

### Program Design

A good Step Program design starts with the end state. Ask:

- What does completion mean?
- Does every Step Type need to be completed?
- Can Steps be completed out of order?
- Can a person repeat a Step Type?
- Should completion be campus-specific?
- Which team owns each Step Type?
- Which statuses count as complete?
- Which attributes are required?
- Which workflows should fire?
- Which staff roles need visibility?

Step Program configuration includes name, active flag, description, icon CSS class, category, completion flow, default list view, statuses, entity attributes, and workflows, according to [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs).

### Completion Flow And Prerequisites

Completion flow defines how participants move through the program. The official docs identify completion flow as a key Step Program setting in [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs), and [Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps) calls out prerequisites and completion flow as core concepts.

For agents, the practical issue is enforcement versus reporting. A linear program may prevent or discourage out-of-order completion depending on configuration and UI behavior. A more flexible program may still report completion when all required Step Types have completion statuses. Before answering a local question, inspect:

- Step Program completion flow.
- Step Type prerequisites.
- Step Type active state.
- Step statuses and completion flags.
- Whether the UI allows staff to override order.
- Whether historical Step records predate current prerequisites.

Special caution: moving a Step Type can remove prerequisites, according to [Move a Step Type](https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type). If a program depends on prerequisites, document them before transfer and verify them after transfer.

### Step Type Design

A Step Type should represent a distinct action or milestone. Configuration fields include name, active state, description, highlight color, icon, badge-count behavior, engagement type, attributes, workflows, and advanced settings. See [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types).

Design guidance:

- Use a clear name staff will recognize in grids and badges.
- Use description for operational clarity, not marketing copy.
- Use highlight colors consistently because charts and legends use them.
- Use icons only where they help recognition.
- Enable badge counts only when repeated completions are meaningful.
- Treat engagement type and impact weight as reporting-sensitive settings.
- Keep attributes minimal and reportable.
- Test workflow triggers after any configuration change.

### Step Entry

Step Entry is the staff-facing record maintenance page. The docs identify key fields such as Person, Campus, date fields, and status. See [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry).

Date behavior matters. Some Steps are point-in-time milestones, such as baptism. Others span time, such as class attendance, training, mentoring, or onboarding. Agents should inspect the Step Type configuration to determine whether Rock will show Start Date and End Date or a single Date field.

Campus behavior matters too. If a Step is tied to a person’s campus or ministry campus, reports may need campus filtering. The [About Step Programs](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-step-programs) article describes campus selection affecting metrics, charts, and Step Type information on the Step Program page.

### Bulk Entry

Bulk Step entry is powerful but risky. [Use Bulk Entry With Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps) describes bulk update from grids and bulk entry mode from Step Program or Step Type pages.

Primary risks:

- Duplicate Steps where multiple completions are not allowed.
- Wrong completion date.
- Wrong campus.
- Wrong status.
- Missing required attributes.
- Workflows firing for large groups.
- Data View population changing between review and execution.

For historical imports, use a staged process. The community recipe [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233) notes that some automation patterns populate completion date with the current date and that workflow batches can time out around larger populations. Treat those numbers as anecdotal and instance-dependent, but the risks are real.

### Step Badges

Step badges surface program progress on places like Person Profile and Connection Requests, according to [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges). The docs recommend creating a single badge for the entire Step Program rather than one badge per Step Type. Configuration includes:

- Name.
- Description.
- Entity Type: Person.
- Badge Type: Steps.
- Step Program.

Agent guidance:

- Use badges for staff-actionable journeys.
- Avoid overloading Person Profile with too many Step badges.
- Confirm the badge is secured appropriately.
- Verify whether counts display as intended for Step Types with Show Count on Badge.
- Validate on a person with no Steps, partial Steps, and completed Steps.

### Step Charts

Step charts help administrators interpret Step activity. The official docs identify chart filters and chart types in [Intro to Step Charts](https://community.rockrms.com/documentation/engagement/steps/steps-charts/intro-to-step-charts) and [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types). Chart perspectives include:

- Trends.
- Totals.
- Campuses.
- Flow.
- Line and bar presentations.
- Timeframe filters.
- Campus, measure, and status filters.

Use charts to answer operational questions:

- Are completions increasing or decreasing?
- Which Step Types are bottlenecks?
- Are campuses behaving differently?
- Are people starting but not completing?
- Did a campaign create a spike?
- Did a workflow or staff process stop creating Steps?

Do not use charts as the only audit source. For discrepancies, inspect underlying Step records, statuses, campus values, date ranges, active/inactive Step Types, and report filters.

### Moving Step Types

Rock v18.1 release notes added the ability to transfer Step Types from one Step Program to another, and the docs include [Move a Step Type](https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type). The move process asks for a destination Step Program and status remapping.

Operational risks:

- Statuses may not mean the same thing across programs.
- Prerequisites can be lost.
- Reports referencing the old program may break or change meaning.
- Workflows tied to the old Step Program or Step Type may need review.
- Badges and charts can shift.
- Staff may lose expected navigation paths.

Before moving a Step Type:

1. Record the current Step Program, Step Type, statuses, prerequisites, workflows, attributes, badge settings, and reports.
2. Identify all Data Views and reports referencing the Step Type.
3. Map old statuses to semantically equivalent new statuses.
4. Test with a non-production clone if the Step Type has many records.
5. After moving, verify sample records and Step Program Completion behavior.

### Core Steps

The v18.1 release notes added a “Core Steps” Step Program with system-protected Step Types, including an initial `eRA` type, and Step Type transfer support. See the [Release Notes](https://www.rockrms.com/releasenotes). Agents should treat system-protected Step Types differently from locally created ministry Step Types. Before editing, moving, deleting, or automating Core Steps:

- Inspect whether the Step Program or Step Type is system-protected.
- Inspect source or release notes for intended use.
- Confirm whether UI disables certain edits.
- Avoid direct database modification.
- Verify whether upgrades expect the records to remain intact.

## 9. Streaks Deep Dive

### What Streaks Are For

Streaks are built to analyze consistency in attendance or participation. [Intro to Streaks](https://community.rockrms.com/documentation/engagement/streaks/overview/intro-to-streaks) describes Streaks as a way to take attendance data further by identifying meaningful engagement patterns. The docs also note that Streaks were still evolving at the time of that documentation, so agents should verify feature availability in the live Rock version.

Use Streaks when:

- The question is about consecutive participation.
- Attendance records are the source of truth.
- A ministry wants current and longest streaks.
- Staff need to find people at risk of disengagement.
- Achievements should be based on consecutive attendance.

Do not use Streaks when:

- There is no reliable occurrence schedule.
- Attendance data is incomplete and cannot be rebuilt.
- Manual exceptions are frequent enough to undermine trust.
- The desired outcome is a one-time milestone better represented as a Step.

### Streak Maps

Streak maps are the core model. [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps) identifies three map types:

- Occurrence: when participation could have happened.
- Engagement: when a person participated.
- Exclusion: when an absence should be ignored for streak calculation.

This creates a precise mental model:

- Occurrence says, “There was an opportunity.”
- Engagement says, “This person participated.”
- Exclusion says, “Do not penalize this date for streak purposes.”

If a streak number looks wrong, inspect maps before assuming a bug.

### Streak Type Setup

A Streak Type tells Rock where and when to look for streaks and who is included. [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types) gives examples such as weekend attendance at a campus or small group attendance from a certain start date.

Key setup questions:

- What attendance source is used?
- Which campus, location, group, group type, or schedule is in scope?
- When should tracking begin?
- Who should be enrolled?
- Are historical attendance records complete?
- Are location exclusions needed?
- Should achievements be tied to this Streak Type?
- Who may view or edit it?

The [Add a New Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type) article warns not to treat setup lightly even if the UI looks simple. That is operationally correct: a bad Streak Type can produce authoritative-looking but misleading numbers.

### Enrollment

Streak enrollment connects individuals to a Streak Type. [Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment) explains that each person can have a different enrollment date. This matters because two people in the same Streak Type can have different valid tracking windows.

When debugging enrollment:

- Confirm the person is enrolled in the Streak Type.
- Confirm enrollment date.
- Confirm attendance exists after the enrollment date.
- Confirm the occurrence map includes the relevant periods.
- Confirm engagement map reflects attendance or manual updates.
- Confirm exclusion map does not hide absences unexpectedly.

### Manual Tracking

Manual tracking lets staff update engagement or exclusion maps. [Manually Track Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks) describes selecting a period in the engagement map and saving; the docs also advise saving and refreshing to verify the page.

Manual tracking is appropriate for corrections, imports, and exceptional cases. It is not a substitute for reliable attendance. If staff are manually updating many streak maps every week, the attendance process is probably the real issue.

### Rebuild Behavior

Streak rebuilds can be destructive to manual map changes. [Individually Rebuilding Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks) warns that an individual rebuild deletes the individual’s engagement map data and rebuilds from attendance records. [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type) extends the concept to a whole Streak Type and warns that occurrence and enrollment data can be affected.

Before using rebuild:

1. Identify whether changes are individual or type-wide.
2. Record current enrollment counts and sample map values.
3. Identify manual map changes that would be lost.
4. Confirm attendance records are complete.
5. Run in a test environment if the Streak Type is important.
6. After rebuild, verify current streak, longest streak, enrollment date, and maps for known sample people.

### Excluding Dates

Exclusions ignore a date for streak-count purposes but do not erase attendance reality. [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date) describes a case where excluding an absence increases longest streak even though the engagement graph still reflects attendance data.

Agent implication: if a leader asks why the graph and streak count seem inconsistent, inspect the exclusion map. The graph can still show the missed occurrence while the streak calculation ignores it.

### Streaks And Achievements

Streak Types can connect to Achievements from the Streak Type Detail page, according to [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail). Source code also notes that the original Achievement sources were Streaks in [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs) and [`achievementTypeBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/AchievementTypeDetail/achievementTypeBag.d.ts).

Use this relationship for goals like:

- Attend three weekends in a row.
- Maintain a small-group streak.
- Return after a period of absence.
- Complete a consistency-based milestone that then adds a Step.

## 10. Assessments Deep Dive

### What Assessments Are For

Assessments help an organization understand people’s wiring, gifts, motivations, emotional intelligence, and conflict patterns. [About Assessments](https://community.rockrms.com/documentation/engagement/assessments/overview/about-assessments) describes their use for understanding strengths, calling, fit, and guidance.

Assessments should be handled with care. They can support coaching, placement, and team formation, but they should not be treated as perfect psychological truth or as the sole basis for sensitive decisions.

### Built-In Assessments

The v19 docs list five available assessments in [Available Assessments](https://community.rockrms.com/documentation/engagement/assessments/available-assessments):

- DISC Personality Assessment.
- Spiritual Gifts.
- Motivators.
- Emotional Intelligence.
- Conflict Profile.

A Triumph resource also notes that those five assessments are built into Rock’s core product in [Triumph's Top 8 Personality Assessments](https://www.triumph.tech/resources/sparks-top-8-personality-assessments), but official Rock docs should be preferred for configuration and behavior.

### Taking Assessments

[Take Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/take-assessments) states that assessments are taken similarly, but questions and answer types vary by assessment and are not configurable. It also emphasizes present-state answering and a consistent environment.

Agent guidance for assessment support:

- Do not promise that questions can be customized unless verified in the live Assessment Type and current Rock version.
- If a user asks to retake, check retake interval and request-required settings.
- If a link fails, inspect request status, person login identity, public page access, and security.
- If results are missing, inspect completion status and person assessment history.

### Sending Requests

Requests can be sent individually from a Person Profile using the Actions button, or to groups through communication/Lava patterns described in [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests).

Before sending to a large group:

1. Verify the sender has communication rights.
2. Verify the recipients are correct.
3. Test one person’s link.
4. Confirm whether formal requests are required for that Assessment Type.
5. Confirm retake eligibility.
6. Confirm the message does not expose private context.
7. Confirm tracking and analytics expectations for workflow-sent communications separately; the source pack includes an unanswered Q&A about Mailgun tracking for workflow emails at [Mailgun Tracking Not Working for Workflow Emails](https://community.rockrms.com/ask/using/2824), so do not infer workflow email analytics behavior from the Communication Wizard without testing.

### Retakes

[Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments) says the Assessment Type controls how much time must pass before the same person can retake an assessment, and the default is 365 days. It also notes that an assessment can be configured to require a formal request.

Troubleshooting retakes:

- Inspect `Admin Tools > System Settings > Assessment Types`.
- Confirm the retake interval.
- Confirm whether a formal request is required.
- Check the person’s last completion date.
- Check whether the person is using the correct identity/login.
- Check whether the request is pending, complete, expired, or missing.
- Confirm whether staff are looking at the same assessment type if custom or versioned types exist.

### Assessment History

A person’s assessment history is visible from Person Profile History according to [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history). The docs identify fields such as assessment name, status, requested date, and requester.

Operationally, assessment history is the first place to inspect for:

- Was a request sent?
- Did the person complete it?
- Was it self-initiated or request-based?
- Which staff person requested it?
- Are there multiple requests for the same assessment?
- Is the result present but not appearing in a report?

### Assessment Results And Data Views

Some assessment results are searchable through Data Views. The Spiritual Gifts article gives an example of searching for people whose dominant gifts include Hospitality in [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts). The Emotional Intelligence article gives an example of searching for people with high Others-Awareness in [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence). The Conflict Profile article also marks SQL/Data View relevance in the pack and describes result rankings and themes in [Conflict Profile](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile).

Live verification: inspect the actual Person Attribute keys and values created by the assessment in the local instance. Use the Data View builder rather than hard-coded assumptions when possible.

## 11. Achievements Deep Dive

### What Achievements Are For

Achievements define goals measured against engagement and interaction data. [Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements) describes Achievement Types as configured goals and Achievement Attempts as the individual attempts to meet those goals.

Use Achievements when:

- A pattern should be evaluated automatically.
- Staff need badge output.
- A workflow should run when a goal starts, succeeds, or fails.
- Completing a goal should add a Step.
- Prerequisites should enforce a sequence of goals.

Do not use Achievements when:

- A simple Step is enough.
- The data source is unreliable.
- The success condition cannot be expressed by an available component.
- Staff need subjective approval more than automatic evaluation.

### Achievement Type Fields

The official [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types) article covers fields such as name, active state, description, and category. The source-code view model adds implementation detail for fields such as:

- `achievementEntityType`.
- `achievementStartWorkflowType`.
- `achievementSuccessWorkflowType`.
- `achievementFailureWorkflowType`.
- `achievementStepType`.
- `achievementStepStatus`.
- `addStepOnSuccess`.
- `allowOverAchievement`.
- `maxAccomplishmentsAllowed`.
- `prerequisites`.
- `resultsLavaTemplate`.
- `customSummaryLavaTemplate`.
- `sourceEntityTypeId`.
- `stepProgram`.

See [`AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs) and [`achievementTypeBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/AchievementTypeDetail/achievementTypeBag.d.ts).

### Attempts

[Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts) describes attempts as instances of individuals trying to meet an Achievement Type’s conditions. It also notes that attempts can be manually added or changed from the Achievement Type screen.

Agent guidance:

- Use attempts to inspect whether the achievement is working.
- Compare attempt state to source data.
- Verify target count and component configuration.
- Check whether an attempt is in progress, successful, or failed in operational terms.
- Review v18.3 release notes if success workflows appear to miss attempts under rapid processing.

The v18.3 release notes fixed a timing issue that could prevent Achievement Type configured workflows from running when many Achievement Attempts were recorded rapidly. See [Release Notes](https://www.rockrms.com/releasenotes).

### Prerequisites

Achievement Type advanced settings can include prerequisite achievements. [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings) says prerequisite Achievement Types must already exist before they can be selected.

Use prerequisites to enforce progression across goals. Before enabling them:

- Confirm the prerequisite is stable.
- Confirm existing achievers already have appropriate attempts.
- Decide whether historical achievers should be backfilled.
- Test a person with and without the prerequisite.
- Document the dependency to avoid accidental deletion or reconfiguration.

The source service deletes dependent prerequisite records when an Achievement Type is deleted because of circular-reference concerns in Entity Framework. See [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs). That means deletion is not just visual cleanup; it can remove dependency relationships.

### Workflow Launches

Advanced settings allow workflow launches when an achievement starts, succeeds, or fails, according to [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings). Source-code fields confirm `AchievementStartWorkflowTypeId`, `AchievementSuccessWorkflowTypeId`, and `AchievementFailureWorkflowTypeId` in [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

Workflow design guidance:

- Use start workflows for onboarding, notification, or opening a coaching process.
- Use success workflows for recognition, communication, Step creation validation, or next-step assignment.
- Use failure workflows sparingly; avoid noisy automation when attempts close unsuccessfully.
- Ensure workflows can handle the entity passed by the achievement process.
- Test rapid processing if the source can create many attempts at once.

### Badges And Lava

Achievement Type advanced settings include badge Lava templates, and the source view model includes badge/results/custom summary Lava fields. See [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings) and [`AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs).

Operational guidance:

- Keep badge Lava fast.
- Avoid leaking sensitive source data.
- Test empty, in-progress, successful, and failed states.
- Confirm security on pages where badge output appears.
- If using Lava to render assessment or Step data, inspect what objects are actually available in the Lava context.

### Add Step On Success

Achievements can create Steps when successfully accomplished. The official fields are:

- Add Step on Success.
- Step Program.
- Step Type.
- Step Status.

See [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types).

Agent checklist:

1. Confirm the achievement success condition.
2. Confirm Step Type allows the intended repeat behavior.
3. Confirm Step Status is a completion status if the Step should count as completed.
4. Confirm the Step Program selected matches the Step Type.
5. Test one achiever.
6. Verify no duplicate Step is created unexpectedly.
7. Verify Step badges and Step charts update.

### Processing

[`AchievementTypeService.Process`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs) shows the processing shape: resolve cache, resolve component, get source entities, process each source entity in its own RockContext, disable real-time events for the bulk process, and save changes.

Troubleshooting processing:

- If no attempts are created, check active state, component, source entity query, and target count.
- If attempts are created but workflows do not run, check workflow configuration, version caveats, and logs.
- If badge output fails, check Lava templates and the achievement component.
- If Step creation fails, check Step Program, Step Type, Step Status, duplicate rules, and security.
- If processing is slow, inspect source entity count and component logic.

## 12. Related Rock Areas: People, Groups, Workflows, Communications, Data Views, Reports, Security, Learning Lms Engagement

### People

Person Profile is a primary engagement surface. Agents should inspect:

- Person Profile badges.
- Actions menu for assessment requests.
- History tab for assessment request and completion history.
- Step lists or related tabs, depending on local page layout.
- Person aliases if records look duplicated.
- Security context for staff viewing sensitive assessment data.

### Groups

Groups influence engagement through attendance, membership, scheduling, sign-ups, and following. Streaks often depend on group attendance or campus-specific attendance. Sign-Ups use group types and project configuration, with docs pointing to group type behavior in [Configure Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups). Following can include groups, and following a group can place it within easy reach from a dashboard and interact with event registration notifications according to [Follow a Group](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/follow-a-group).

### Workflows

Workflows connect engagement data to action:

- Step Program workflow triggers.
- Step Type workflow triggers.
- Achievement start/success/failure workflows.
- Assessment request communications.
- Historical Step migration workflows.
- LMS activity completion workflows.

Version caveat: v18.3 fixed a Step Program editing bug related to Step Type association on workflow triggers and a rapid Achievement Attempt workflow timing issue. See [Release Notes](https://www.rockrms.com/releasenotes).

### Communications

Communications support assessment requests and engagement follow-up. [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests) references using Lava codes in communications to send assessment requests to groups. Agents should verify tracking expectations. The source pack includes an unanswered community Q&A about Mailgun tracking not working for workflow emails at [Mailgun Tracking Not Working for Workflow Emails](https://community.rockrms.com/ask/using/2824); because it has no answer, use it only as a reminder to test communication analytics in the actual channel.

### Data Views

Data Views are essential for:

- Identifying Step candidates.
- Preventing duplicate Step imports.
- Finding assessment-result matches.
- Targeting communications.
- Reporting engagement gaps.
- Building Achievement source populations, where applicable.

Assessment docs explicitly mention Data View search examples for Spiritual Gifts and EQ in [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts) and [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence).

### Reports

Reports should be built from the right layer:

- Use raw attendance for attendance counts.
- Use Streaks for consistency.
- Use Steps for journey progress.
- Use Step Program Completion for complete-program outcomes where available.
- Use assessment attributes/history for assessment results.
- Use Achievement Attempts for goal progress and success rates.

Do not mix layers without naming the definition. “Engaged” can mean attendance, a current streak, completed Steps, an Achievement, or a staff-defined Data View.

### Security

Security touches:

- Step Programs and Step Program Completion parent authority.
- Step badges.
- Assessment history and result attributes.
- Achievement Type management.
- Following event subscription visibility.
- Sign-Up permissions.
- LMS public block display.

Source code shows Step Program Completion inherits parent authority from Step Program when present in [`StepProgramCompletion.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs). Following event docs say subscription availability depends on View access to the Following Event in [Configure Follow Events](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/configure-follow-events). Sign-Up permissions are covered separately in [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions).

### Learning LMS Engagement

The release notes identify several Learning LMS engagement changes in v18.1 and v18.3:

- v18.1 added Content Article Learning Activity type.
- v18.1 added SMS notifications for new learning activities.
- v18.1 improved Completion Grading System status labels and feedback.
- v18.1 added public external block security for LMS programs, courses, and classes.
- v18.1 updated LMS Activity completion workflow to pass `LearningClassActivityCompletion` as the entity instead of the student.
- v18.3 added Smart Scroll to the Public Learning Class Workspace block.

See [Release Notes](https://www.rockrms.com/releasenotes).

Agent implication: Learning engagement can create completion signals and workflows that resemble Steps or Achievements, but it is not the same model. Inspect LMS entities, completion workflows, and public block security before joining Learning data to Step or Achievement reports.

## 13. Administration And Operational Guardrails

### Configuration Guardrails

- Use active/inactive rather than deleting when records have history.
- Document Step Program and Achievement dependencies.
- Keep categories meaningful.
- Avoid duplicate Step Types with similar names.
- Use consistent status semantics across Step Programs.
- Use explicit completion statuses.
- Test badges and charts after configuration.
- Use workflows only where action is needed.
- Keep Lava templates efficient and secure.

### Data-Change Guardrails

Before bulk entry, migration, rebuild, or achievement processing:

1. Identify the exact records in scope.
2. Export or record pre-change counts.
3. Validate a sample set.
4. Confirm duplicate rules.
5. Confirm workflow side effects.
6. Confirm staff communication expectations.
7. Run a small pilot.
8. Verify readbacks after the operation.

### Rebuild Guardrails

For Streak rebuilds:

- Assume manual engagement map changes can be lost.
- Confirm attendance source completeness.
- Record sample streak values before rebuild.
- Verify current and longest streak after rebuild.
- Communicate expected changes to staff.

See [Individually Rebuilding Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks) and [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type).

### Version Guardrails

Always inspect the Rock version. v18.1 and v18.3 changed engagement behavior materially. The [Release Notes](https://www.rockrms.com/releasenotes) include:

- Core Steps Step Program with system-protected Step Types.
- Step Type transfer.
- Step Analytics.
- Achievement Type creation repair after a block bug.
- Achievement Attempt workflow timing fix.
- Step Program workflow trigger association fix.
- LMS engagement changes.

### Public-Safe Documentation Guardrails

For public knowledge-base work, avoid including:

- Private SQL.
- Live instance URLs.
- Raw transcripts.
- Internal implementation logs.
- Secrets.
- Local file paths.
- Private source paths.
- Sensitive assessment results.
- Person-identifying examples.

Use public source links and general procedures.

## 14. Developer, API, Lava, And Source-Code Landmarks

### Source Repository

The Rock source repository is [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock). Source-code snippets in the pack are from the `develop` branch.

### Step Program Completion

- [`Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs): entity model for Step Program Completion, with Step Program, PersonAlias, Campus, date fields, and related Steps.
- [`Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs): security parent authority points to Step Program when present.

### Step Program And Step Type Picker

- [`Rock/Attribute/StepProgramStepTypeFieldAttribute.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Attribute/StepProgramStepTypeFieldAttribute.cs): field attribute for selecting zero or one Step Type filtered by Step Program; source comment says stored as `StepProgram.Guid|StepType.Guid`.
- [`Rock/Field/Types/StepProgramStepTypeFieldType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/StepProgramStepTypeFieldType.cs): field type supporting WebForms and Obsidian, parsing delimited GUIDs and returning display text.
- [`Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs): composite picker that selects a Step Program and then a Step Type filtered by that program.
- [`Rock.JavaScript.Obsidian/Framework/FieldTypes/stepProgramStepTypeField.partial.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/FieldTypes/stepProgramStepTypeField.partial.ts): Obsidian field type model.
- [`stepProgramStepTypeFieldComponents.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/FieldTypes/stepProgramStepTypeFieldComponents.ts): Obsidian edit component using `StepProgramStepTypePicker`.

### Step Status View Models

- [`Rock.ViewModels/Blocks/Engagement/StepTypeDetail/StepStatusBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/StepTypeDetail/StepStatusBag.cs): status bag with Step Status and completion flag.
- [`Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/StepTypeDetail/stepStatusBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/StepTypeDetail/stepStatusBag.d.ts): TypeScript version.
- [`Rock.ViewModels/Blocks/Engagement/StepProgramDetail/StepStatusBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/StepProgramDetail/StepStatusBag.cs): Step Program Detail workflow trigger status model.

### Achievement Models And Services

- [`Rock/Model/Engagement/AchievementType/AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs): entity model with source entity, achiever entity, component, workflow hooks, Step creation fields, Lava templates, and other configuration.
- [`AchievementType.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.Logic.cs): cache update and validation logic, including max accomplishments versus over-achievement validation.
- [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs): delete handling for prerequisites and component-based processing.
- [`Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs): block view model for Achievement Type Detail.
- [`achievementTypeBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/AchievementTypeDetail/achievementTypeBag.d.ts): TypeScript view model with Step, workflow, Lava, public, and prerequisite fields.

### Lava Landmarks

Lava appears in:

- Assessment request communications, per [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests).
- Achievement badge/results/custom summary templates, per [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings) and source view models.
- Community workflow examples such as [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233).

When using Lava, inspect the actual merge fields available in the block, communication, workflow action, or badge context. Do not assume a Lava object exists because a similarly named entity exists in the database.

### API Notes

The source marks `AchievementType` with `[CodeGenerateRest( DisableEntitySecurity = true )]` and `StepProgramCompletion` with `[CodeGenerateRest]` in their model snippets. This is a source-code signal that generated REST surfaces may exist, but agents should inspect the live API, security, and version before using endpoints. Source links: [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs) and [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs).

## 15. Reporting, Analytics, And Model Map

### Reporting Layers

Use the right reporting layer:

- **Attendance**: raw participation counts and occurrence detail.
- **Streaks**: consecutive engagement and consistency.
- **Steps**: journey progress and ministry milestones.
- **Step Program Completion**: full-program completion outcomes.
- **Assessments**: result attributes and assessment history.
- **Achievements**: goal attempts, success, badges, workflow side effects.
- **LMS completion**: learning progress and class activity completion.

### Step Charts

Step charts include trends, totals, campuses, and flow chart perspectives in [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types). Use them for operational review, not as a substitute for data audits.

Suggested review questions:

- Which Step Types have high starts and low completions?
- Which campuses have different completion patterns?
- Did campaign timing align with completion spikes?
- Are inactive Step Types still affecting totals?
- Are completion statuses configured correctly?
- Are date filters hiding older records?

### Model Map

The source pack identifies [Step Program Completion](https://community.rockrms.com/ModelMap) as a model in the Engagement category. Use Model Map as a public reference for model availability and naming, then inspect source or live schema for fields and relationships.

### Data View Reporting

Useful Data Views include:

- People with no Step in a required Step Type.
- People with a completed Step but missing follow-up.
- People with assessment result values matching serving criteria.
- People with current streak below threshold.
- People with Achievement Attempts in progress too long.
- People who completed LMS activity but have not completed the corresponding Step.

Before using Data Views operationally, verify:

- Attribute keys and values.
- Security.
- Campus filters.
- Active/inactive records.
- Merged-person alias behavior.
- Time zone/date boundaries.
- Whether completion statuses are being used rather than status names.

## 16. Version And Release Caveats

### v18.1 Engagement Changes

The [Release Notes](https://www.rockrms.com/releasenotes) identify these v18.1 engagement-related changes:

- Added Content Article Learning Activity type.
- Added SMS notifications for new learning activities.
- Improved Completion Grading System labels and feedback.
- Added Core Steps Step Program with system-protected Step Types, including initial `eRA` type.
- Added Step Type transfer between Step Programs.
- Added Step Analytics, including trends, totals, statuses, and campuses.
- Added security for public LMS program, course, and class display.
- Updated LMS Activity completion workflow to pass `LearningClassActivityCompletion` as the entity instead of Student.

Agent implications:

- Do not assume Core Steps are editable like custom Step Programs.
- Do not assume older instances have Step Type transfer or Step Analytics.
- Review LMS workflow actions after upgrade if they expected Student as entity.
- Validate public LMS security after upgrading or adding public blocks.

### v18.3 Engagement Fixes

The [Release Notes](https://www.rockrms.com/releasenotes) identify v18.3 fixes:

- Achievement Type Detail could save newly created Achievement Types without important settings; a post-update job repairs affected records.
- Achievement Type workflows could fail to run when many Achievement Attempts were recorded rapidly; attempts are now saved before workflows trigger.
- Editing a Step Program could remove Step Type association from workflow triggers, and Step Type-level triggers could display incorrectly on Step Program Detail.

Agent implications:

- If an Achievement Type was created during an affected version window, inspect whether its component/settings were repaired.
- If success/failure workflows appear inconsistent around bulk processing, check version and logs.
- If Step Program workflow triggers look wrong, check whether the instance includes the v18.3 fix.
- If the instance is on a beta or pre-release branch, verify behavior directly.

### v19 Documentation

Most official documentation records in the pack are v19.0 pages. The release notes page indicates v19.1 released June 11, 2026. Because documentation and installed Rock version may differ, inspect the local instance version before applying v19.0 instructions to older systems.

## 17. Implementation Playbooks

### Playbook: New Step Program For Volunteer Onboarding

1. Define the onboarding journey.
2. Decide required Steps: application, background check, interview, training, placement.
3. Create Step Program: “Volunteer Onboarding.”
4. Add category: “Serving” or local equivalent.
5. Configure completion flow.
6. Add statuses: Started, In Progress, Complete, Deferred, Not Approved, or local equivalents.
7. Mark only appropriate statuses as completion statuses.
8. Create Step Types.
9. Add attributes only where needed, such as ministry area, reviewer, or training provider.
10. Configure workflows for staff notification and next-step reminders.
11. Add a Person badge if staff need profile visibility.
12. Create Data Views for incomplete onboarding.
13. Test with a sample person.
14. Verify Step charts and badge output.
15. Document ownership and maintenance.

Sources: [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs), [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types), [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges).

### Playbook: Historical Baptism Step Import

1. Identify the historical source field or attribute.
2. Create a Data View for people with the historical date.
3. Create a Data View excluding people who already have the target Step.
4. Confirm Step Type duplicate settings.
5. Build a workflow or use bulk entry with the historical date preserved.
6. Process in batches.
7. Verify sample person records.
8. Compare source count to Step count.
9. Review workflow errors.
10. Deactivate temporary Data Views or label them clearly.

Use the community recipe [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233) only as a pattern, because it is not core-reviewed and must be adapted to the local instance.

### Playbook: Weekend Attendance Streak

1. Define campus and attendance scope.
2. Confirm attendance records are reliable.
3. Create Streak Type.
4. Set start date.
5. Configure occurrence source.
6. Rebuild if using historical attendance, after recording pre-change data.
7. Inspect known attenders.
8. Add exclusions only with a policy.
9. Connect achievements if needed.
10. Build reports for current streak and longest streak.

Sources: [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types), [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps), [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type).

### Playbook: Assessment-Driven Volunteer Placement

1. Identify which assessment results matter for the role.
2. Confirm the assessment exists and is active.
3. Send assessment requests to candidates.
4. Verify completions in Person Profile History.
5. Build a Data View against result attributes.
6. Review the result with human judgment.
7. Add a Step or workflow action only if placement is approved.
8. Secure assessment result visibility.

Sources: [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests), [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history), [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts), [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence).

### Playbook: Achievement For Consistent Attendance That Adds A Step

1. Configure or verify the Streak Type.
2. Create Achievement Type.
3. Choose the correct achievement component/source.
4. Set target criteria.
5. Set max accomplishments and over-achievement behavior.
6. Configure success workflow if needed.
7. Enable Add Step on Success.
8. Choose Step Program, Step Type, and Step Status.
9. Test with one source entity/person.
10. Verify Achievement Attempt, Step creation, badge, and charts.

Sources: [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types), [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings), [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs).

## 18. Troubleshooting Decision Tree

### A Step Is Missing From A Person

1. Was the Step entered for the correct person alias?
2. Is the Step Type active?
3. Is the Step Program active?
4. Is the user looking at the correct campus filter?
5. Is the date outside the selected chart/list timeframe?
6. Was the Step entered with a non-completion status?
7. Does security hide the Step or badge?
8. Was the Step Type moved to another program?
9. Did a bulk import fail or skip duplicates?
10. Inspect the Step Type participant list and Person Profile.

Sources: [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry), [Move a Step Type](https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type).

### Step Program Completion Looks Wrong

1. Confirm each required Step Type has a completed Step.
2. Confirm statuses are marked as completion statuses.
3. Confirm inactive Step Types should or should not count.
4. Confirm person alias identity.
5. Confirm campus expectations.
6. Inspect the Step Program Completion model in the live instance.
7. Compare source-code rule in [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs).

### Streak Count Looks Wrong

1. Confirm the person is enrolled.
2. Confirm enrollment date.
3. Confirm occurrence map includes the relevant dates.
4. Confirm attendance source records exist.
5. Confirm engagement map.
6. Confirm exclusion map.
7. Check whether manual edits were overwritten by rebuild.
8. Check whether location exclusions apply.
9. Refresh after map changes.
10. Rebuild only after backing up current map expectations.

Sources: [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps), [Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment), [Individually Rebuilding Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks), [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date).

### Assessment Cannot Be Retaken

1. Inspect Assessment Type configuration.
2. Check retake interval.
3. Check last completion date.
4. Check whether formal request is required.
5. Check whether a pending request exists.
6. Confirm the person is using the right account.
7. Confirm the assessment page is accessible.

Source: [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments).

### Assessment Results Are Not Reportable

1. Confirm the assessment is complete.
2. Check Person Profile History.
3. Inspect person attributes created by the assessment.
4. Confirm attribute security.
5. Confirm Data View filter is using the right attribute and value.
6. Confirm whether result values are high/medium/low, list values, text, or structured output.
7. Test with a known person.

Sources: [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history), [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts), [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence).

### Achievement Does Not Create Attempts

1. Confirm Achievement Type is active.
2. Confirm component entity type is configured.
3. Confirm source entity type.
4. Confirm target count.
5. Confirm source entities query returns records.
6. Check processing job/logs.
7. Check version caveats.
8. Inspect [`AchievementTypeService.Process`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs).

### Achievement Saves But Behaves Incorrectly

1. Check whether it was created during a version affected by the v18.3 repaired Achievement Type Detail bug.
2. Inspect component configuration JSON.
3. Confirm prerequisites.
4. Confirm max accomplishments and over-achievement validation.
5. Confirm workflows.
6. Confirm Step creation fields.
7. Confirm badge Lava.
8. Review [Release Notes](https://www.rockrms.com/releasenotes).

### Achievement Success Workflow Does Not Run

1. Confirm success attempt exists.
2. Confirm success workflow type is set.
3. Confirm workflow security and activation.
4. Check logs.
5. Check whether many attempts were created rapidly.
6. Verify instance includes the v18.3 timing fix from [Release Notes](https://www.rockrms.com/releasenotes).

### Step Is Not Added When Achievement Succeeds

1. Confirm Add Step on Success is enabled.
2. Confirm Step Program is selected.
3. Confirm Step Type is selected.
4. Confirm Step Status is selected.
5. Confirm Step Status is valid for the Step Program.
6. Confirm duplicate rules allow the Step.
7. Confirm Achievement Attempt is successful.
8. Confirm workflow or processing logs.
9. See [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types).

## 19. Agent Task Recipes

### Recipe: Audit A Step Program

Return:

- Program name, ID/GUID if available, active state, category.
- Step Types and active state.
- Statuses and which count as completion.
- Completion flow and prerequisites.
- Attributes.
- Workflow triggers.
- Badge configuration.
- Chart counts.
- Sample person verification.
- Reports/Data Views depending on the program.
- Version caveats.

Primary sources: [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs), [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types).

### Recipe: Diagnose Step Badge Display

Inspect:

- Badge list under `Admin Tools > Settings > General > Badges`.
- Entity Type is Person.
- Badge Type is Steps.
- Step Program selected.
- Step Type Show Count on Badge settings.
- Person has expected Step records.
- Security.
- Person Profile block/zone where badges render.

Source: [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges).

### Recipe: Review A Streak Type Before Rebuild

Capture:

- Streak Type settings.
- Enrollment count.
- Start date.
- Occurrence map summary.
- Location exclusions.
- Sample person current/longest streak.
- Manual map edits, if known.
- Attendance source completeness.
- Achievement dependencies.

Sources: [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail), [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type).

### Recipe: Verify Assessment Request Flow

Check:

- Assessment Type settings.
- Retake interval.
- Requires request setting.
- Person Profile Actions menu.
- Request message.
- Person Profile History.
- Completion status.
- Result attributes.
- Data View search.

Sources: [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests), [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments), [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history).

### Recipe: Audit Achievement Type

Return:

- Name, active state, category.
- Component/entity type.
- Source entity type.
- Achiever entity type.
- Target count.
- Max accomplishments.
- Over-achievement setting.
- Prerequisites.
- Start/success/failure workflows.
- Badge/results/custom summary Lava.
- Add Step on Success fields.
- Attempt counts and sample attempts.
- Version caveats.

Sources: [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types), [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings), [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs).

### Recipe: Explain Engagement Data To A Ministry User

Use plain definitions:

- Steps show where someone is in a configured ministry path.
- Streaks show consistency over eligible attendance periods.
- Assessments show self-assessment results and history.
- Achievements show whether a configured goal has been attempted or met.
- Reports depend on which of those definitions the ministry means by “engaged.”

Then ask for the operational decision they need to make. That determines the correct data source.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `4`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | When the Steps Automation job processes a step type's Auto-Complete Data View, it honors prerequisite steps and the Allow Multiple setting before creating or completing step records. | [source](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types) |
| official | behavior | A streak type defines the engagement source, time pattern and start date Rock uses to calculate streaks, as well as the population enrolled for tracking. | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types) |
| official | configuration | Whether a person can retake an assessment is controlled by the assessment type's minimum-days interval and, when enabled, its requirement that an assessment request exist. | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments) |
| official | configuration | An achievement type cannot simultaneously track overachievement and cap the number of accomplishments because Rock must decide whether excess events extend progress or start another accomplishment. | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types) |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 20. Source Map And Dependency Notes

### Primary Official Documentation

- [Steps](https://community.rockrms.com/documentation/engagement/steps): top-level Steps documentation.
- [Intro to Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/intro-to-steps): core Steps concepts, Core Steps, engagement type, impact weight, prerequisites, completion flow.
- [About Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-steps): Step Program list and navigation.
- [About Step Programs](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-step-programs): program page, campus filter, metrics, chart behavior.
- [About Step Types](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-step-types): Step Type page and participant progress.
- [Use Step Entry](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry): person, campus, date/status entry behavior.
- [Use Bulk Entry With Steps](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-bulk-entry-with-steps): bulk update paths.
- [Steps Badges](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges): badge setup.
- [Move a Step Type](https://community.rockrms.com/documentation/engagement/steps/fundamentals/move-a-step-type): Step Type transfer and status remap cautions.
- [Edit Step Programs](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs): program settings.
- [Edit Step Types](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types): Step Type settings.
- [Intro to Step Charts](https://community.rockrms.com/documentation/engagement/steps/steps-charts/intro-to-step-charts): chart filters.
- [Chart Types](https://community.rockrms.com/documentation/engagement/steps/steps-charts/chart-types): trends, totals, campuses, flow.

### Streak Sources

- [Streaks](https://community.rockrms.com/documentation/engagement/streaks): top-level Streaks docs.
- [Intro to Streaks](https://community.rockrms.com/documentation/engagement/streaks/overview/intro-to-streaks): concept and caveats.
- [Streaks Maps](https://community.rockrms.com/documentation/engagement/streaks/overview/streaks-maps): occurrence, engagement, exclusion maps.
- [Intro to Streak Types](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types): Streak Type purpose.
- [Add a New Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type): setup planning.
- [Streak Type Detail](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail): detail page, achievements, map editor, exclusions, enrollment.
- [Rebuild Streak Type](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type): rebuild behavior.
- [Intro to Streak Enrollment](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment): enrollment dates and person-level detail.
- [Manually Track Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks): manual engagement map edits.
- [Individually Rebuilding Streaks](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks): individual rebuild warning.
- [Exclude a Date](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date): exclusion behavior.

### Assessment Sources

- [Assessments](https://community.rockrms.com/documentation/engagement/assessments): top-level docs.
- [About Assessments](https://community.rockrms.com/documentation/engagement/assessments/overview/about-assessments): purpose and organizational use.
- [Send Requests](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests): individual and group requests.
- [Take Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/take-assessments): taking guidance and non-configurable questions.
- [Retake Assessments](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments): Assessment Type settings and default retake interval.
- [View Assessment History](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history): Person Profile History.
- [Available Assessments](https://community.rockrms.com/documentation/engagement/assessments/available-assessments): assessment list.
- [DISC Personality Assessment](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/disc-personality-assessment).
- [Spiritual Gifts](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/spiritual-gifts).
- [Motivators](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/motivators).
- [Emotional Intelligence](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/emotional-intelligence).
- [Conflict Profile](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile).

### Achievement Sources

- [Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements): top-level Achievements docs.
- [Intro to Achievements](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements): terms and concept.
- [Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types): example detail page.
- [Add Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types): configuration fields.
- [Add Achievement Attempts](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts): attempts.
- [Achievement Type Advanced Settings](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings): prerequisites, workflows, badges.
- [Configure Steps in Achievement Types](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types): Add Step on Success.

### Related Engagement Sources

- [Additional Engagement Tools](https://community.rockrms.com/documentation/engagement/additional-engagement-tools): Achievements, Reminders, Following, Interactive Experiences, Sign-Ups.
- [Following](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following).
- [How to Follow](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/how-to-follow).
- [Configure Follow Events](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/configure-follow-events).
- [Follow a Group](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following/follow-a-group).
- [Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups).
- [Configure Sign-Ups](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups).
- [Configure Sign-Up Permissions](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-up-permissions).
- [Interactive Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences).
- [Intro to Interactive Experiences](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/interactive-experiences/intro-to-interactive-experiences).
- [Reminders](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/reminders).

### Training, Release, Model, And Community Sources

- [RockU Engagement](https://community.rockrms.com/rocku/engagement): training index pointer; hydrated excerpt was limited.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): version caveats for v18.1, v18.3, v19.1.
- [Model Map](https://community.rockrms.com/ModelMap): Step Program Completion model reference.
- [Adding People to Steps with Historical Data](https://community.rockrms.com/recipes/233): community recipe for historical Step migration; use cautiously.
- [Triumph's Top 8 Personality Assessments](https://www.triumph.tech/resources/sparks-top-8-personality-assessments): supplemental resource noting built-in Rock assessments; prefer official docs for behavior.
- [Mailgun Tracking Not Working for Workflow Emails](https://community.rockrms.com/ask/using/2824): unanswered community Q&A; use only as a reminder to verify workflow communication analytics in the live instance.

### Source-Code Sources

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): source repository.
- [`StepProgramCompletion.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.cs): Step Program Completion entity.
- [`StepProgramCompletion.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/StepProgramCompletion/StepProgramCompletion.Logic.cs): security parent authority.
- [`StepProgramStepTypeFieldAttribute.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Attribute/StepProgramStepTypeFieldAttribute.cs): Step Program/Step Type field attribute.
- [`StepProgramStepTypeFieldType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Field/Types/StepProgramStepTypeFieldType.cs): field parsing and display.
- [`StepProgramStepTypePicker.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Web/UI/Controls/Pickers/StepProgramStepTypePicker.cs): picker control.
- [`AchievementType.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.cs): Achievement Type entity.
- [`AchievementType.Logic.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementType.Logic.cs): cache and validation.
- [`AchievementTypeService.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Engagement/AchievementType/AchievementTypeService.cs): processing and prerequisite delete handling.
- [`AchievementTypeBag.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Engagement/AchievementTypeDetail/AchievementTypeBag.cs): block view model.
- [`achievementTypeBag.d.ts`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Engagement/AchievementTypeDetail/achievementTypeBag.d.ts): TypeScript view model.
- [`StepProgramAchievementTests.cs`](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Tests.Integration/Engagement/Achievements/StepProgramAchievementTests.cs): integration-test landmark for Step Program achievements.

### Dependency Notes

Engagement Tracking depends on:

- **People** for Person/Profile/Alias identity.
- **Groups** for membership, attendance, scheduling, Sign-Ups, and group following.
- **Workflows** for automation triggered by Steps, Achievements, assessment communications, and LMS completion.
- **Communications** for assessment requests and engagement follow-up.
- **Data Views** for segmentation, reporting, and duplicate prevention.
- **Reports** for operational dashboards and leadership metrics.
- **Security** for badges, results, public LMS blocks, following events, Sign-Up permissions, and engagement records.
- **Learning LMS Engagement** for learning activity completion and class engagement signals.

When source material is thin or version-sensitive, verify in the live instance instead of inventing behavior. Inspect page routes, block settings, entity records, Rock version, release notes, schema/model fields, security, workflow triggers, system jobs, and sample person readbacks before making operational claims.
