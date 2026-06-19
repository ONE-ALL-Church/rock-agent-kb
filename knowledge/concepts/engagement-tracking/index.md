---
id: concept-engagement-tracking
title: Engagement Tracking
generated: true
last_built: 2026-06-18T23:01:19+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 80
depends_on_topics:
  - people
  - groups
  - workflows
  - communications
  - data-views
  - reports
  - security
  - learning-lms-engagement
---

# Engagement Tracking

Steps, step programs, streaks, assessments, achievements, engagement tools, journey-style tracking, completion signals, and related reporting.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Engagement Tracking` spans people, groups, workflows, communications, data-views, reports. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_rocku, triumph_resources, rock_model_map, rock_core_release_notes, rock_recipes.
- Related tags found in source records: operations, usage, admin, check-in, workflow, sql, development, lava.
- Source detail types include: documentation_article, question, recipe, training, triumph_resources.

## Source Coverage

- `rock_core_release_notes`: 2
- `rock_documentation`: 72
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 1
- `rock_rocku`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Fundamentals | rock_documentation | [Intro to Steps](/documentation/engagement/steps/fundamentals/intro-to-steps?Version=v19.0) [About Steps](/documentation/engagement/steps/fundamentals/about-steps?Version=v19.0) [About Step Programs](/documentation/engagement/steps/fundamentals/about-step-programs?Version=v19.0) [About Step Types](/documentation/engagement/steps/fundamentals/about-step-types?Version=v19.0) [Move a Step... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals) |
| Achievements | rock_documentation | [Intro to Achievements](/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements?Version=v19.0) [Achievement Types](/documentation/engagement/additional-engagement-tools/achievements/achievement-types?Version=v19.0) [Add Achievement Types](/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types?Version=v19.0) [Add Achievement... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements) |
| Configure Steps in Achievement Types | rock_documentation | No, you haven’t jumped to the wrong guide, *Achievements* and *Steps* can work together! Rock lets you add step data automatically using achievements. When the achievement has been successfully accomplished, a step gets added. You can access the configuration described below when creating or editing an achievement type. 1. **Add Step on Success** - The step features for the achievement type will only work if the... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types) |
| Streaks | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Streak Types](?Version=v19.0#streak-types) [Streak Enrollment](?Version=v19.0#streak-enrollment) ### Overview Articles [Intro to Streaks](/documentation/engagement/streaks/overview/intro-to-streaks?Version=v19.0) [Streaks Maps](/documentation/engagement/streaks/overview/streaks-maps?Version=v19.0) ### Streak Types Articles [Intro to Streak... | [source](https://community.rockrms.com/documentation/engagement/streaks) |
| Steps | rock_documentation | SECTIONS [Fundamentals](?Version=v19.0#fundamentals) [Configure Steps](?Version=v19.0#configure-steps) [Steps Charts](?Version=v19.0#steps-charts) ### Fundamentals Articles [Intro to Steps](/documentation/engagement/steps/fundamentals/intro-to-steps?Version=v19.0) [About Steps](/documentation/engagement/steps/fundamentals/about-steps?Version=v19.0) [About Step... | [source](https://community.rockrms.com/documentation/engagement/steps) |
| Streak Types | rock_documentation | [Intro to Streak Types](/documentation/engagement/streaks/streak-types/intro-to-streak-types?Version=v19.0) [Add a New Streak Type](/documentation/engagement/streaks/streak-types/add-a-new-streak-type?Version=v19.0) [Streak Type Detail](/documentation/engagement/streaks/streak-types/streak-type-detail?Version=v19.0) [Rebuild Streak... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types) |
| Streak Enrollment | rock_documentation | [Intro to Streak Enrollment](/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment?Version=v19.0) [Manually Track Streaks](/documentation/engagement/streaks/streak-enrollment/manually-track-streaks?Version=v19.0) [Individually Rebuilding Streaks](/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks?Version=v19.0) [Exclude a... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment) |
| Administer Assessments | rock_documentation | [Send Requests](/documentation/engagement/assessments/administer-assessments/send-requests?Version=v19.0) [Take Assessments](/documentation/engagement/assessments/administer-assessments/take-assessments?Version=v19.0) [Retake Assessments](/documentation/engagement/assessments/administer-assessments/retake-assessments?Version=v19.0) [View Assessment... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments) |
| Streak Type Detail | rock_documentation | After saving your new streak type, you’ll be brought to the streak type detail page. You can also access this page by clicking on a streak type from the list (see [Streak Types](/documentation/engagement/streaks/streak-types)). We’ll look closely at the detail block before moving down the page to check out the list block at the bottom. 1. **Streak Type Information** - Along the left side of the block, you can see... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail) |
| Edit Step Types | rock_documentation | From the *Step Type* page click the Edit button to change the step type settings. 1. **Name** - Provide the name of the step type. 2. **Active**- Set the step type to active or inactive. 3. **Description**- Provide a description for the step type. 4. **Highlight Color**- Choose the color to use for the *step type*. This color appears in the charts and in each chart legend where *Step Types* are displayed. 5.... | [source](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types) |
| Assessments | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Administer Assessments](?Version=v19.0#administer-assessments) [Available Assessments](?Version=v19.0#available-assessments) ### Overview Articles [About Assessments](/documentation/engagement/assessments/overview/about-assessments?Version=v19.0) ### Administer Assessments Articles [Send... | [source](https://community.rockrms.com/documentation/engagement/assessments) |
| Additional Engagement Tools | rock_documentation | SECTIONS [Achievements](?Version=v19.0#achievements) [Reminders](?Version=v19.0#reminders) [Following](?Version=v19.0#following) [Interactive Experiences](?Version=v19.0#interactive-experiences) [Sign-Ups](?Version=v19.0#sign-ups) ### Achievements Articles [Intro to Achievements](/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements?Version=v19.0) [Achievement... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Step Program Completion](../../model-map/models/step-program-completion.md) | Engagement | 19.1.8 | 47 | 16 | 32 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Attempt](../../model-map/models/achievement-attempt.md) | Engagement | 19.1.8 | 44 | 16 | 29 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Type](../../model-map/models/achievement-type.md) | Engagement | 19.1.8 | 72 | 33 | 56 | 24 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Type Prerequisite](../../model-map/models/achievement-type-prerequisite.md) | Engagement | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step](../../model-map/models/step.md) | Engagement | 19.1.8 | 62 | 24 | 46 | 22 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step Program](../../model-map/models/step-program.md) | Engagement | 19.1.8 | 50 | 19 | 34 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step Status](../../model-map/models/step-status.md) | Engagement | 19.1.8 | 46 | 16 | 30 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step Type](../../model-map/models/step-type.md) | Engagement | 19.1.8 | 70 | 33 | 55 | 22 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Step Type Prerequisite](../../model-map/models/step-type-prerequisite.md) | Engagement | 19.1.8 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step Workflow](../../model-map/models/step-workflow.md) | Engagement | 19.1.8 | 42 | 12 | 27 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Step Workflow Trigger](../../model-map/models/step-workflow-trigger.md) | Engagement | 19.1.8 | 47 | 16 | 32 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Streak](../../model-map/models/streak.md) | Engagement | 19.1.8 | 53 | 22 | 38 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable scraped Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Achievement Attempt.AchievementType` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.AttributeValues` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.Attributes` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.CreatedByPersonId` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.CreatedByPersonName` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.EntityStringValue` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.IdKey` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.ModifiedAuditValuesAlreadyUpdated` is Lava-marked but not database-marked in the scraped Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 18.1 | Engagement | Added new "Core Steps" Step Program with system-protected Step Types, including initial "eRA" type. Added the ability to transfer Step Types from one Step Program to another. | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Engagement | Fixed an issue where editing a Step Program removed the Step Type association from its workflow triggers, and also addressed Step Type-level triggers being incorrectly displayed on the Step Program Detail. Fixes: #6753 | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Steps

Keywords: `step, steps, step program, step type`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Fundamentals | rock_documentation | [Intro to Steps](/documentation/engagement/steps/fundamentals/intro-to-steps?Version=v19.0) [About Steps](/documentation/engagement/steps/fundamentals/about-steps?Version=v19.0) [About Step Programs](/documentation/engagement/steps/fundamentals/about-step-programs?Version=v19.0) [About Step Types](/documentation/engagement/steps/fundamentals/about-step-types?Version=v19.0) [Move a Step... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals) |
| Steps | rock_documentation | SECTIONS [Fundamentals](?Version=v19.0#fundamentals) [Configure Steps](?Version=v19.0#configure-steps) [Steps Charts](?Version=v19.0#steps-charts) ### Fundamentals Articles [Intro to Steps](/documentation/engagement/steps/fundamentals/intro-to-steps?Version=v19.0) [About Steps](/documentation/engagement/steps/fundamentals/about-steps?Version=v19.0) [About Step... | [source](https://community.rockrms.com/documentation/engagement/steps) |
| Edit Step Types | rock_documentation | From the *Step Type* page click the Edit button to change the step type settings. 1. **Name** - Provide the name of the step type. 2. **Active**- Set the step type to active or inactive. 3. **Description**- Provide a description for the step type. 4. **Highlight Color**- Choose the color to use for the *step type*. This color appears in the charts and in each chart legend where *Step Types* are displayed. 5.... | [source](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-types) |
| About Steps | rock_documentation | You can access your step programs under: `People > Engagement > Steps.` This is also where you’ll go to create new programs, which we’ll cover later in the [Editing Step Programs](/documentation/engagement/steps/configure-steps/edit-step-programs) article. 1. **Name** - The name of the step program. 2. **Category** - Categories are a great way to group and organize your programs. You can view and manage step program... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-steps) |
| Steps Badges | rock_documentation | You have the option of displaying badges for your step programs, to quickly and easily view an individual’s progress from places like the *Person Profile* page or Connection Requests. To add Steps badges, first navigate to `Admin Tools > Settings > General > Badges` and add a row to the badge list. A single badge should be set up for the entire program (and not one badge for each step in the program) using the page... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals/steps-badges) |
| Configure Steps | rock_documentation | [Edit Step Programs](/documentation/engagement/steps/configure-steps/edit-step-programs?Version=v19.0) [Edit Step Types](/documentation/engagement/steps/configure-steps/edit-step-types?Version=v19.0) | [source](https://community.rockrms.com/documentation/engagement/steps/configure-steps) |
| About Step Types | rock_documentation | Next, let's shift our focus to one of the individual step types within our example program. The layout of the *Step Type* page is very similar to the *Step Program* page. You’ll see a familiar detail block at the top, followed by a list of step participants below. From here you can maintain the list of participants and view their progress as they start and finish the step. 1. **Name and Description** - The name of... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals/about-step-types) |
| Steps Charts | rock_documentation | [Intro to Step Charts](/documentation/engagement/steps/steps-charts/intro-to-step-charts?Version=v19.0) [Chart Types](/documentation/engagement/steps/steps-charts/chart-types?Version=v19.0) | [source](https://community.rockrms.com/documentation/engagement/steps/steps-charts) |
| Use Step Entry | rock_documentation | Shepherding individuals through your program can be done either from the *Step Types* page or from the *Person Profile* page. Whichever path you take, you’ll wind up at a *Step Entry* page like the one pictured below. This is where you'll maintain step type information for an individual. 1. **Person** - In this example we’re adding a step from within the *Steps* area, so we need to provide a person. Steps entered... | [source](https://community.rockrms.com/documentation/engagement/steps/fundamentals/use-step-entry) |
| Edit Step Programs | rock_documentation | Let’s go back to the *Step Program* page to see how we can edit our programs. Clicking the Edit button lets you update the program and its configurable settings. Trailblazer 1. **Name** - Provide the name of the program. 2. **Active** - Set the program to active or inactive. 3. **Description**- Add a meaningful description of the program. 4. **Icon CSS Class**- Choose the *CSS icon* to use for the program. 5.... | [source](https://community.rockrms.com/documentation/engagement/steps/configure-steps/edit-step-programs) |

### Streaks

Keywords: `streak, streaks, engagement streak`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Streaks | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Streak Types](?Version=v19.0#streak-types) [Streak Enrollment](?Version=v19.0#streak-enrollment) ### Overview Articles [Intro to Streaks](/documentation/engagement/streaks/overview/intro-to-streaks?Version=v19.0) [Streaks Maps](/documentation/engagement/streaks/overview/streaks-maps?Version=v19.0) ### Streak Types Articles [Intro to Streak... | [source](https://community.rockrms.com/documentation/engagement/streaks) |
| Streak Types | rock_documentation | [Intro to Streak Types](/documentation/engagement/streaks/streak-types/intro-to-streak-types?Version=v19.0) [Add a New Streak Type](/documentation/engagement/streaks/streak-types/add-a-new-streak-type?Version=v19.0) [Streak Type Detail](/documentation/engagement/streaks/streak-types/streak-type-detail?Version=v19.0) [Rebuild Streak... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types) |
| Streak Enrollment | rock_documentation | [Intro to Streak Enrollment](/documentation/engagement/streaks/streak-enrollment/intro-to-streak-enrollment?Version=v19.0) [Manually Track Streaks](/documentation/engagement/streaks/streak-enrollment/manually-track-streaks?Version=v19.0) [Individually Rebuilding Streaks](/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks?Version=v19.0) [Exclude a... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment) |
| Streak Type Detail | rock_documentation | After saving your new streak type, you’ll be brought to the streak type detail page. You can also access this page by clicking on a streak type from the list (see [Streak Types](/documentation/engagement/streaks/streak-types)). We’ll look closely at the detail block before moving down the page to check out the list block at the bottom. 1. **Streak Type Information** - Along the left side of the block, you can see... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/streak-type-detail) |
| Intro to Streak Types | rock_documentation | The streak type tells the system where and when to look for streaks. For example, do you want to track weekend attendance at the Main Campus since it opened? Or do you want to track small group attendance at the West Campus starting six months ago? All that gets built into the streak type setup. A streak type also contains the people for whom you want to track streaks. To manage your *Streak Types*, head to `People... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/intro-to-streak-types) |
| Manually Track Streaks | rock_documentation | We know from attendance records that Ted should have streak numbers higher than zero. But we’re taking the manual path, so we need to manually feed that into Ted’s streak data. Take a look at how the page changes after selecting the “Sep 05” week in the engagement map. 1. **Engagement Graph** - With an engagement manually recorded, now we have some streak data. You can see a blue bar has been added near the end of... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks) |
| Add a New Streak Type | rock_documentation | Adding new streak types may look like a simple task because there aren’t a ton of fields. While it’s true that the setup is simple, don’t take it lightly. Before you start, it’s best to have a plan in mind for why and how you want to use the streak type. In this example we’ll be tracking streaks for our “ASU Student Group”, a small group that meets weekly on Saturdays. Everything related to the group has already... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/add-a-new-streak-type) |
| Individually Rebuilding Streaks | rock_documentation | Let’s see how Ted’s data has changed after clicking the Rebuild button. Warning **Individual Rebuild**The rebuild process will delete the individual’s engagement map data and rebuild it from attendance records. Any manual changes you’ve made to the engagement map will be lost. 1. **Engagement Graph** - At the top of the block, we see several new bars have popped up. From left to right, this graph shows: 1. Two... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/individually-rebuilding-streaks) |
| Rebuild Streak Type | rock_documentation | We’ve already covered streak types, but we didn’t go into detail on what happens when you use the *Rebuild* feature. Now that you’ve seen what rebuilding an individual’s enrollment looks like, you can apply those concepts to rebuilding the streak type. Let’s go back in time to when we first added our new streak type. As a reminder, this is how the page originally looked before we added Ted: 1. **Start Date** - Note... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-types/rebuild-streak-type) |
| Exclude a Date | rock_documentation | Looking at the *Engagement Map*, we can see Ted didn’t attend the week of August 22nd. We know Ted’s car broke down in a storm that week, and we’re feeling generous, so we’ve decided to ignore that absence in Ted’s streak data. All we need to do is select the "Aug 22" week in the exclusion map and click the Save button. Now it’s like the absence never happened. 1. **Engagement Graph**- You might notice the... | [source](https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/exclude-a-date) |

### Assessments

Keywords: `assessment, assessments, retake, assessment type`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Administer Assessments | rock_documentation | [Send Requests](/documentation/engagement/assessments/administer-assessments/send-requests?Version=v19.0) [Take Assessments](/documentation/engagement/assessments/administer-assessments/take-assessments?Version=v19.0) [Retake Assessments](/documentation/engagement/assessments/administer-assessments/retake-assessments?Version=v19.0) [View Assessment... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments) |
| Assessments | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Administer Assessments](?Version=v19.0#administer-assessments) [Available Assessments](?Version=v19.0#available-assessments) ### Overview Articles [About Assessments](/documentation/engagement/assessments/overview/about-assessments?Version=v19.0) ### Administer Assessments Articles [Send... | [source](https://community.rockrms.com/documentation/engagement/assessments) |
| Available Assessments | rock_documentation | [DISC Personality Assessment](/documentation/engagement/assessments/available-assessments/disc-personality-assessment?Version=v19.0) [Spiritual Gifts](/documentation/engagement/assessments/available-assessments/spiritual-gifts?Version=v19.0) [Motivators](/documentation/engagement/assessments/available-assessments/motivators?Version=v19.0) [Emotional... | [source](https://community.rockrms.com/documentation/engagement/assessments/available-assessments) |
| Retake Assessments | rock_documentation | After an assessment has been taken it's possible to take it again, but you may need to adjust some configuration to allow it. # Assessment Type Configuration The Assessment Type configuration can be accessed by navigating to `Admin Tools > System Settings > Assessment Types`. From there you can select an assessment type to view or edit its settings. Each Assessment Type has a setting which controls how much time... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments) |
| View Assessment History | rock_documentation | A history of assessments can be viewed from an individual's *Person Profile* page under the *History* tab. This history includes assessments that were taken with or without a formal request. 1. **Assessment** - The name of the assessment is displayed here. The same assessment will appear in the list more than once if multiple requests exist. 2. **Status** - The status column will display either "Pending" or... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history) |
| Take Assessments | rock_documentation | The assessments are all taken in a similar way; however, each assessment will vary on the questions and type of answers provided. These are not configurable. The assessments were heavily researched and designed to meet a huge audience. It’s essential to keep a few things in mind while taking these assessments. One is to reflect on who you are at the time of taking the assessment. It is tempting to answer questions... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/take-assessments) |
| Send Requests | rock_documentation | Before we get into each assessment one by one, let’s take a look at how requests are sent to groups or individuals. Out of the box, Rock comes with these assessments ready to go, so you don’t have to do any background work. # Individual Requests One way to send a request is through a person’s profile page. This is done by clicking the Actions button located below the person's photo. Click on the button and choose... | [source](https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/send-requests) |
| Conflict Profile | rock_documentation | The Conflict Engagement Assessment is a measure of how individuals see themselves responding to conflict in a given setting. This may or may not be a fully accurate picture, depending on their self-awareness during a conflict. Most people feel comfortable using a few approaches based on what they saw demonstrated early in their lives. And most people have different natural responses in different settings. However,... | [source](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/conflict-profile) |
| DISC Personality Assessment | rock_documentation | The DISC assessment is like many other quadrant-style personality profiles. You may have seen some that divide all personalities into four types or combinations of those types. Some tests show results as colors or animals. DISC takes that same concept but uses letters to stand for each personality type. Here's a quick look at the four main types and some adjectives that describe them: * D: dominant, driving,... | [source](https://community.rockrms.com/documentation/engagement/assessments/available-assessments/disc-personality-assessment) |
| About Assessments | rock_documentation | We are all uniquely wired and given specific gifts, abilities, ways of thinking, and ways of solving problems. In Rock we have implemented five assessments to empower your organization to understand your people more. The results that come from these assessments can greatly help your workers better understand their strengths, calling and fill needs based on your greater understanding of your organization’s members.... | [source](https://community.rockrms.com/documentation/engagement/assessments/overview/about-assessments) |

### Achievements

Keywords: `achievement, achievements, badge, achievement type`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Achievements | rock_documentation | [Intro to Achievements](/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements?Version=v19.0) [Achievement Types](/documentation/engagement/additional-engagement-tools/achievements/achievement-types?Version=v19.0) [Add Achievement Types](/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types?Version=v19.0) [Add Achievement... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements) |
| Configure Steps in Achievement Types | rock_documentation | No, you haven’t jumped to the wrong guide, *Achievements* and *Steps* can work together! Rock lets you add step data automatically using achievements. When the achievement has been successfully accomplished, a step gets added. You can access the configuration described below when creating or editing an achievement type. 1. **Add Step on Success** - The step features for the achievement type will only work if the... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/configure-steps-in-achievement-types) |
| Additional Engagement Tools | rock_documentation | SECTIONS [Achievements](?Version=v19.0#achievements) [Reminders](?Version=v19.0#reminders) [Following](?Version=v19.0#following) [Interactive Experiences](?Version=v19.0#interactive-experiences) [Sign-Ups](?Version=v19.0#sign-ups) ### Achievements Articles [Intro to Achievements](/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements?Version=v19.0) [Achievement... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools) |
| Add Achievement Types | rock_documentation | To get started with achievements, navigate to `People > Engagement > Achievements`. You’ll be brought to the *Achievement Types* page pictured below. From here you can add as many achievement types as you want or look at the attempts for an existing achievement type, as described in the prior section. Let’s look at what makes an achievement type work. 1. **Name** - Provide a name for the new achievement type. 2.... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-types) |
| Achievement Type Advanced Settings | rock_documentation | You can access the advanced settings while creating or editing an achievement type. As described below, you can use this configuration to do things like create achievement badges or add prerequisite achievements. 1. **Prerequisite Achievements**- You can optionally specify other achievements that must be earned before this achievement can be earned. The other Achievement Type must already be configured in order to... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-type-advanced-settings) |
| Add Achievement Attempts | rock_documentation | Now that the Achievement Type is set up, we can start tracking attempts. Attempts, as you might have guessed, are instances of individuals trying to meet the conditions of the Achievement Type. Although there isn’t a formal “status” for attempts, they can be thought of as either successful, unsuccessful or in progress. If the person satisfies the achievement type’s conditions, then the attempt is *Successful*. If... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/add-achievement-attempts) |
| Achievement Types | rock_documentation | Let’s look at an example achievement type with some data already added, so you can get an idea of what to expect. In this example we’re tracking an achievement that’s earned when a person has attended ten times consecutively. In later sections we’ll go into the details and cover how this all gets set up. 1. **Successful Attempts Graph** - This graph shows the number of successfully completed attempts toward this... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/achievement-types) |
| Intro to Achievements | rock_documentation | > *"What you get by achieving your goals is not as important as what you become by achieving your goals."* -Henry David Thoreau With Achievements you can define goals that are measured against things like engagement and interaction data. For instance, you may want to recognize when a person has attended services three times in a row in a single month. You could wade through the raw data looking for that kind of... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/achievements/intro-to-achievements) |
| Following | rock_documentation | [Intro to Following](/documentation/engagement/additional-engagement-tools/following/intro-to-following?Version=v19.0) [How to Follow](/documentation/engagement/additional-engagement-tools/following/how-to-follow?Version=v19.0) [Configure Follow Events](/documentation/engagement/additional-engagement-tools/following/configure-follow-events?Version=v19.0) [Person History Following... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/following) |
| Sign-Ups | rock_documentation | [Intro to Sign-Ups](/documentation/engagement/additional-engagement-tools/sign-ups/intro-to-sign-ups?Version=v19.0) [Manage Sign-Ups](/documentation/engagement/additional-engagement-tools/sign-ups/manage-sign-ups?Version=v19.0) [Configure Sign-Ups](/documentation/engagement/additional-engagement-tools/sign-ups/configure-sign-ups?Version=v19.0) [Group Registration and Attendance for... | [source](https://community.rockrms.com/documentation/engagement/additional-engagement-tools/sign-ups) |


## Rebuild Dependencies

- Source records: `91`
- Approved claims: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
