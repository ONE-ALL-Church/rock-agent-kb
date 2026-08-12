---
id: concept-learning-lms-engagement
title: Learning, LMS, And Engagement
generated: true
last_built: 2026-08-12T12:50:00+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 38
source_freshness_status: complete
source_last_checked_at: 2026-08-12T06:18:48+00:00
source_native_migration_status: not_started
source_native_article_coverage: 0/32
legacy_summary_retirement_coverage: 0/32
depends_on_topics:
  - people
  - groups
  - communications
  - workflows
  - event-registration
  - data-views
  - reports
  - security
  - platform-configuration
---

# Learning, LMS, And Engagement

Learning programs, LMS courses, lessons, requirements, completion tracking, engagement journeys, and learning-related reporting.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Learning, LMS, And Engagement` spans people, groups, communications, workflows, event-registration, data-views. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_rocku, rock_model_map, rock_recipes, rock_core_release_notes, rock_qa.
- Related tags found in source records: operations, usage, admin, workflow, development, lava, security, releases.
- Source detail types include: documentation_article, question, recipe, training, triumph_resources.

## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | operational_guidance | Training staff to use Rock correctly reduces the likelihood that teams adopt disconnected tools whose data and workflows fragment the church's system of record. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | operational_guidance | When work must survive a conversation, prefer an agent workflow that creates a durable file or handoff artifact instead of leaving the result only inside a transient chat thread. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | operational_guidance | Rock's LMS can assign curricula by staff role and track completion, allowing churches to make required Rock training specific and accountable. Verify the current LMS configuration and permissions in the installed version. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | operational_guidance | Train and activate staff before expecting them to train volunteers. Staff-first sequencing creates training multipliers and reduces the risk that inconsistent volunteer practices damage data quality. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | operational_guidance | Before staff encounter a changed Rock interface, a short targeted video can prevent avoidable support tickets and reduce surprise. The training should be prepared and distributed as part of the upgrade plan. | [source](https://www.youtube.com/watch?v=bu5nPeAVCAo) |
| official | release_caveat | Before deploying the redesigned v19 Connections experience, show staff the new interface and provide brief training instead of surprising active connectors with a major workflow change. | [source](https://www.youtube.com/watch?v=edanHiYSDIM) |
| community-reviewed | implementation_pattern | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | For dashboard speed, expensive journey analytics can be calculated into a persisted dataset on a schedule rather than recalculating all historical engagement data on each page load. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Rock LMS organizes training into programs, courses, class instances, learning plans, activities, and learning participants, with the program deciding whether the experience is on-demand or academic-calendar based. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | release_caveat | Before deploying the redesigned v19 Connections experience, show staff the new interface and provide brief training instead of surprising active connectors with a major workflow change. | [source](https://shows.acast.com/rock-cast/episodes/3-underrated-features-ep-217) |

## Source Coverage

- `rock_core_release_notes`: 2
- `rock_documentation`: 30
- `rock_model_map`: 12
- `rock_qa`: 1
- `rock_recipes`: 1
- `rock_rocku`: 1
- `sparkdevnetwork_rock`: 1
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Create a Program | rock_documentation | Let's walk through the process of creating a simple learning program using the *On-Demand* mode. We'll create a program, a [course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course), a [class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class), and a [learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program) |
| LMS Learning Hub | rock_documentation | [Intro to the Learning Hub](/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub?Version=v19.0) [On-Demand Class Workspace Example](/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example?Version=v19.0) [Academic Calendar Class Workspace... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub) |
| Create a Learning Program | rock_documentation | [Create a Program](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program?Version=v19.0) [Create a Course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course?Version=v19.0) [Edit the Class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class?Version=v19.0) [Create the Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program) |
| Intro to the Learning Hub | rock_documentation | When you build classes and programs in Rock's Learning Management System, the Learning Hub is where your people actually find them. It is the front door to everything you have published, sitting at the `/learn` page on your Rock site. The Hub automatically showcases every Learning program and course you have marked as Public, so making a course available is as simple as flipping its visibility. See [Create a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub) |
| Learning Management System | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Create a Learning Program](?Version=v19.0#create-a-learning-program) [LMS Learning Hub](?Version=v19.0#lms-learning-hub) [Program Administration](?Version=v19.0#program-administration) [Activities](?Version=v19.0#activities) [Advanced LMS](?Version=v19.0#advanced-lms) ### Overview Articles [Intro to... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system) |
| Academic Calendar Class Workspace Example | rock_documentation | The workspace for a class under a program using the Academic Calendar mode looks slightly different. It includes a tab bar at the top that shows an overview of the class and class progress, along with tabs for Activities/Assignments and the class Syllabus. 1. **Communication Preferences** - This option appears for students when *Send Notification Communications* is turned on for any class activity. It lets them... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example) |
| LMS Behind the Scenes | rock_documentation | ## The Inner Workings of Learning Classes If you were to peek behind the curtains of Rock, you would discover that a *Learning Class* is essentially a specialized type of *Group*. What does this mean? For one, *Students* and *Facilitators* are simply a specific type of *GroupMember*. That means you can leverage many of Rock's features that work with groups and group members. * Learning Class Group * Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes) |
| Edit the Class | rock_documentation | Once you save your course, an initial class will be *automatically* created for you. Select this class so we can set up the required learning activities and assign a facilitator (if needed) to oversee grading for the class. First, edit the "Initial Class" to rename it to something more appropriate. Next, choose a grading system that suits your needs. For *On-Demand* classes, the *Completion* grading system is... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class) |
| Courses | rock_documentation | Courses are a specific type of class that is offered in the program. You can create one or more instances of these depending on the settings or desired class size. 1. **Overview / Description** - Use the Description tab to edit the course description, which appears on the public Learning Hub page to provide individuals with a detailed understanding of the course. 2. **Requirements** - Specify prerequisites or... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) |
| Create the Learning Plan | rock_documentation | Next, let's set up a quick [Video Watch](/documentation/engagement/learning-management-system/activities/video-watch-activity) activity as the learning plan for our class. Here, we've selected the *Video Watch* Activity Type and chosen a video from our Media Account. The *Completion Threshold* is set to 95%, requiring students to watch at least that much before progressing to the next activity. You can also assign a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan) |
| Intro to LMS | rock_documentation | The Learning Management System (LMS) in Rock RMS provides tools to create and manage educational content, training programs, and courses within your organization. This will allow you to assign training, track progress, and maintain training records. Rock's LMS is designed to support two distinct scenarios: 1. **On-Demand:** This mode is designed for flexibility, allowing classes to run continuously without being... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms) |
| Classes | rock_documentation | A class represents a specific instance of a course offered during a particular time period. Each class has its own Learning Plans, students, and facilitator(s). 1. **Semester** - Visible only in *Academic Calendar* programs, this field specifies the semester during which the class takes place. 2. **Grading System** - Defines or overrides the default grading system for the class. Note that the grading system cannot... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Learning Class Activity Completion](../../model-map/models/learning-class-activity-completion.md) | LMS | 19.2.0 | 65 | 32 | 42 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Course Requirement](../../model-map/models/learning-course-requirement.md) | LMS | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Class](../../model-map/models/learning-class.md) | LMS | 19.2.0 | 126 | 64 | 99 | 35 | 5 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Class Activity](../../model-map/models/learning-class-activity.md) | LMS | 19.2.0 | 62 | 31 | 40 | 15 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Class Announcement](../../model-map/models/learning-class-announcement.md) | LMS | 19.2.0 | 45 | 17 | 30 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Class Content Page](../../model-map/models/learning-class-content-page.md) | LMS | 19.2.0 | 41 | 13 | 26 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Course](../../model-map/models/learning-course.md) | LMS | 19.2.0 | 58 | 25 | 40 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Program Completion](../../model-map/models/learning-program-completion.md) | LMS | 19.2.0 | 47 | 17 | 32 | 15 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Attempt](../../model-map/models/achievement-attempt.md) | Engagement | 19.2.0 | 44 | 16 | 29 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Type](../../model-map/models/achievement-type.md) | Engagement | 19.2.0 | 72 | 33 | 56 | 24 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Achievement Type Prerequisite](../../model-map/models/achievement-type-prerequisite.md) | Engagement | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Learning Activity](../../model-map/models/learning-activity.md) | LMS | 19.2.0 | 43 | 14 | 27 | 13 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Achievement Attempt.AchievementType` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Achievement Attempt.ModifiedAuditValuesAlreadyUpdated` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 18.1 | Engagement | Added the new Content Article Learning Activity type, allowing individuals to complete training by reading content articles. Also added support for SMS notifications to alert individuals about new learning activities. Improved the Completion Grading System to provide clearer status labels and feedback. | [source](https://www.rockrms.com/releasenotes) |
| 17.0 | Engagement | Added the Learning Management System (LMS) that provides tools to create and manage educational content, training programs, and courses within your organization. | [source](https://www.rockrms.com/releasenotes) |

## Repository Landmarks

| Repository | Language | Inclusion Reason | Citation |
| --- | --- | --- | --- |
| SparkDevNetwork/Rock | C# | registered source repository | [source](https://github.com/SparkDevNetwork/Rock) |

## Subguides

### Courses And Lessons

Keywords: `course, courses, lesson, lessons, class, classes, learning`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Create a Program | rock_documentation | Let's walk through the process of creating a simple learning program using the *On-Demand* mode. We'll create a program, a [course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course), a [class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class), and a [learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program) |
| LMS Learning Hub | rock_documentation | [Intro to the Learning Hub](/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub?Version=v19.0) [On-Demand Class Workspace Example](/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example?Version=v19.0) [Academic Calendar Class Workspace... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub) |
| Create a Learning Program | rock_documentation | [Create a Program](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program?Version=v19.0) [Create a Course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course?Version=v19.0) [Edit the Class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class?Version=v19.0) [Create the Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program) |
| Intro to the Learning Hub | rock_documentation | When you build classes and programs in Rock's Learning Management System, the Learning Hub is where your people actually find them. It is the front door to everything you have published, sitting at the `/learn` page on your Rock site. The Hub automatically showcases every Learning program and course you have marked as Public, so making a course available is as simple as flipping its visibility. See [Create a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub) |
| Learning Management System | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Create a Learning Program](?Version=v19.0#create-a-learning-program) [LMS Learning Hub](?Version=v19.0#lms-learning-hub) [Program Administration](?Version=v19.0#program-administration) [Activities](?Version=v19.0#activities) [Advanced LMS](?Version=v19.0#advanced-lms) ### Overview Articles [Intro to... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system) |
| Academic Calendar Class Workspace Example | rock_documentation | The workspace for a class under a program using the Academic Calendar mode looks slightly different. It includes a tab bar at the top that shows an overview of the class and class progress, along with tabs for Activities/Assignments and the class Syllabus. 1. **Communication Preferences** - This option appears for students when *Send Notification Communications* is turned on for any class activity. It lets them... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example) |
| LMS Behind the Scenes | rock_documentation | ## The Inner Workings of Learning Classes If you were to peek behind the curtains of Rock, you would discover that a *Learning Class* is essentially a specialized type of *Group*. What does this mean? For one, *Students* and *Facilitators* are simply a specific type of *GroupMember*. That means you can leverage many of Rock's features that work with groups and group members. * Learning Class Group * Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes) |
| Edit the Class | rock_documentation | Once you save your course, an initial class will be *automatically* created for you. Select this class so we can set up the required learning activities and assign a facilitator (if needed) to oversee grading for the class. First, edit the "Initial Class" to rename it to something more appropriate. Next, choose a grading system that suits your needs. For *On-Demand* classes, the *Completion* grading system is... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class) |
| Courses | rock_documentation | Courses are a specific type of class that is offered in the program. You can create one or more instances of these depending on the settings or desired class size. 1. **Overview / Description** - Use the Description tab to edit the course description, which appears on the public Learning Hub page to provide individuals with a detailed understanding of the course. 2. **Requirements** - Specify prerequisites or... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) |
| Create the Learning Plan | rock_documentation | Next, let's set up a quick [Video Watch](/documentation/engagement/learning-management-system/activities/video-watch-activity) activity as the learning plan for our class. Here, we've selected the *Video Watch* Activity Type and chosen a video from our Media Account. The *Completion Threshold* is set to 95%, requiring students to watch at least that much before progressing to the next activity. You can also assign a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan) |

### Requirements And Completion

Keywords: `requirement, requirements, completion, completed, training`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Create a Program | rock_documentation | Let's walk through the process of creating a simple learning program using the *On-Demand* mode. We'll create a program, a [course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course), a [class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class), and a [learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program) |
| Edit the Class | rock_documentation | Once you save your course, an initial class will be *automatically* created for you. Select this class so we can set up the required learning activities and assign a facilitator (if needed) to oversee grading for the class. First, edit the "Initial Class" to rename it to something more appropriate. Next, choose a grading system that suits your needs. For *On-Demand* classes, the *Completion* grading system is... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class) |
| Courses | rock_documentation | Courses are a specific type of class that is offered in the program. You can create one or more instances of these depending on the settings or desired class size. 1. **Overview / Description** - Use the Description tab to edit the course description, which appears on the public Learning Hub page to provide individuals with a detailed understanding of the course. 2. **Requirements** - Specify prerequisites or... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) |
| Create the Learning Plan | rock_documentation | Next, let's set up a quick [Video Watch](/documentation/engagement/learning-management-system/activities/video-watch-activity) activity as the learning plan for our class. Here, we've selected the *Video Watch* Activity Type and chosen a video from our Media Account. The *Completion Threshold* is set to 95%, requiring students to watch at least that much before progressing to the next activity. You can also assign a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan) |
| Intro to LMS | rock_documentation | The Learning Management System (LMS) in Rock RMS provides tools to create and manage educational content, training programs, and courses within your organization. This will allow you to assign training, track progress, and maintain training records. Rock's LMS is designed to support two distinct scenarios: 1. **On-Demand:** This mode is designed for flexibility, allowing classes to run continuously without being... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms) |
| Create a Course | rock_documentation | When you're in *Configure Program* mode, you can create a course. Click the button to open a form where you can name the course. If you want to provide a more in-depth description, you can add it under the Description tab. Here, we're creating the Child Protection and Safety course, and for this example, we will prevent people from enrolling unless they've already completed the 'Bible Study Essentials' course. This... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course) |
| Configure Program | rock_documentation | This is the mode used when setting up new courses, semesters, classes and class learning plans. 1. **Overview / Description**- Edit the program's description under the Description tab. 2. **Enforce Public Security** - When enabled, programs and courses on the external site are only visible to people with *View* security for the program. You can set this by clicking on the *Learn* page. People already enrolled will... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program) |
| Configure Grading Systems | rock_documentation | Found under `Admin Tools > Settings`, this is where you can define or customize the grading system to fit your needs. For example, Rock ships with the "Rigorous" Letter Grade system. In less rigorous organizations, when using the Letter Grade system, one must only reach a 90% or higher grade to receive a "A" grade. This is where you can make those adjustments. Note **Completion Grading Systems**If your course uses a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems) |
| Assessment Activity | rock_documentation | For the Assessment activity type, you'll see a form for adding items such as a *Multiple Choice* question, a *Section* separator, or a *Short Answer* item. You can add as many items as you need. With the Multiple Choice type of question, you can supply the correct answer so the assessment can be graded automatically. However, adding a Short Answer type will require a Facilitator to score each participant's answers.... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/assessment-activity) |
| Video Watch Activity | rock_documentation | The Video Watch activity lets you share a video from your Digital Media Accounts in Rock. You can set how much of the video a student needs to watch before they can mark it as completed. See the [Digital Media](/documentation/digital-publishing/content-management/digital-media) article of the Content Management guide. | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/video-watch-activity) |

### Engagement Journeys

Keywords: `engagement, journey, journeys, step, steps, streak, achievement`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Create a Program | rock_documentation | Let's walk through the process of creating a simple learning program using the *On-Demand* mode. We'll create a program, a [course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course), a [class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class), and a [learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program) |
| LMS Learning Hub | rock_documentation | [Intro to the Learning Hub](/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub?Version=v19.0) [On-Demand Class Workspace Example](/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example?Version=v19.0) [Academic Calendar Class Workspace... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub) |
| Create a Learning Program | rock_documentation | [Create a Program](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program?Version=v19.0) [Create a Course](/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course?Version=v19.0) [Edit the Class](/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class?Version=v19.0) [Create the Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program) |
| Intro to the Learning Hub | rock_documentation | When you build classes and programs in Rock's Learning Management System, the Learning Hub is where your people actually find them. It is the front door to everything you have published, sitting at the `/learn` page on your Rock site. The Hub automatically showcases every Learning program and course you have marked as Public, so making a course available is as simple as flipping its visibility. See [Create a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub) |
| Learning Management System | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Create a Learning Program](?Version=v19.0#create-a-learning-program) [LMS Learning Hub](?Version=v19.0#lms-learning-hub) [Program Administration](?Version=v19.0#program-administration) [Activities](?Version=v19.0#activities) [Advanced LMS](?Version=v19.0#advanced-lms) ### Overview Articles [Intro to... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system) |
| Academic Calendar Class Workspace Example | rock_documentation | The workspace for a class under a program using the Academic Calendar mode looks slightly different. It includes a tab bar at the top that shows an overview of the class and class progress, along with tabs for Activities/Assignments and the class Syllabus. 1. **Communication Preferences** - This option appears for students when *Send Notification Communications* is turned on for any class activity. It lets them... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example) |
| LMS Behind the Scenes | rock_documentation | ## The Inner Workings of Learning Classes If you were to peek behind the curtains of Rock, you would discover that a *Learning Class* is essentially a specialized type of *Group*. What does this mean? For one, *Students* and *Facilitators* are simply a specific type of *GroupMember*. That means you can leverage many of Rock's features that work with groups and group members. * Learning Class Group * Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes) |
| Edit the Class | rock_documentation | Once you save your course, an initial class will be *automatically* created for you. Select this class so we can set up the required learning activities and assign a facilitator (if needed) to oversee grading for the class. First, edit the "Initial Class" to rename it to something more appropriate. Next, choose a grading system that suits your needs. For *On-Demand* classes, the *Completion* grading system is... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class) |
| Courses | rock_documentation | Courses are a specific type of class that is offered in the program. You can create one or more instances of these depending on the settings or desired class size. 1. **Overview / Description** - Use the Description tab to edit the course description, which appears on the public Learning Hub page to provide individuals with a detailed understanding of the course. 2. **Requirements** - Specify prerequisites or... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) |
| Create the Learning Plan | rock_documentation | Next, let's set up a quick [Video Watch](/documentation/engagement/learning-management-system/activities/video-watch-activity) activity as the learning plan for our class. Here, we've selected the *Video Watch* Activity Type and chosen a video from our Media Account. The *Completion Threshold* is set to 95%, requiring students to watch at least that much before progressing to the next activity. You can also assign a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan) |

### Reporting And Administration

Keywords: `report, reporting, dashboard, administration, configuration, lms`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| LMS Learning Hub | rock_documentation | [Intro to the Learning Hub](/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub?Version=v19.0) [On-Demand Class Workspace Example](/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example?Version=v19.0) [Academic Calendar Class Workspace... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub) |
| Intro to the Learning Hub | rock_documentation | When you build classes and programs in Rock's Learning Management System, the Learning Hub is where your people actually find them. It is the front door to everything you have published, sitting at the `/learn` page on your Rock site. The Hub automatically showcases every Learning program and course you have marked as Public, so making a course available is as simple as flipping its visibility. See [Create a... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub) |
| Learning Management System | rock_documentation | SECTIONS [Overview](?Version=v19.0#overview) [Create a Learning Program](?Version=v19.0#create-a-learning-program) [LMS Learning Hub](?Version=v19.0#lms-learning-hub) [Program Administration](?Version=v19.0#program-administration) [Activities](?Version=v19.0#activities) [Advanced LMS](?Version=v19.0#advanced-lms) ### Overview Articles [Intro to... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system) |
| Academic Calendar Class Workspace Example | rock_documentation | The workspace for a class under a program using the Academic Calendar mode looks slightly different. It includes a tab bar at the top that shows an overview of the class and class progress, along with tabs for Activities/Assignments and the class Syllabus. 1. **Communication Preferences** - This option appears for students when *Send Notification Communications* is turned on for any class activity. It lets them... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example) |
| LMS Behind the Scenes | rock_documentation | ## The Inner Workings of Learning Classes If you were to peek behind the curtains of Rock, you would discover that a *Learning Class* is essentially a specialized type of *Group*. What does this mean? For one, *Students* and *Facilitators* are simply a specific type of *GroupMember*. That means you can leverage many of Rock's features that work with groups and group members. * Learning Class Group * Learning... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes) |
| Courses | rock_documentation | Courses are a specific type of class that is offered in the program. You can create one or more instances of these depending on the settings or desired class size. 1. **Overview / Description** - Use the Description tab to edit the course description, which appears on the public Learning Hub page to provide individuals with a detailed understanding of the course. 2. **Requirements** - Specify prerequisites or... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) |
| Intro to LMS | rock_documentation | The Learning Management System (LMS) in Rock RMS provides tools to create and manage educational content, training programs, and courses within your organization. This will allow you to assign training, track progress, and maintain training records. Rock's LMS is designed to support two distinct scenarios: 1. **On-Demand:** This mode is designed for flexibility, allowing classes to run continuously without being... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms) |
| Classes | rock_documentation | A class represents a specific instance of a course offered during a particular time period. Each class has its own Learning Plans, students, and facilitator(s). 1. **Semester** - Visible only in *Academic Calendar* programs, this field specifies the semester during which the class takes place. 2. **Grading System** - Defines or overrides the default grading system for the class. Note that the grading system cannot... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes) |
| On-Demand Class Workspace Example | rock_documentation | A set of learning plan activities might look like this in the student's *Class Workspace.* 1. **Communication Preferences** - This option appears for students when *Send Notification Communications* is turned on for any class activity. It lets them choose how they prefer to receive updates on new activities, by email or text, so they stay in the loop. | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example) |
| Program Administration | rock_documentation | [Intro to Program Administration](/documentation/engagement/learning-management-system/program-administration/intro-to-program-administration?Version=v19.0) [Configure Security](/documentation/engagement/learning-management-system/program-administration/configure-security?Version=v19.0) [Facilitators](/documentation/engagement/learning-management-system/program-administration/facilitators?Version=v19.0) [Configure... | [source](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration) |


## Source Lifecycle

- Official article records routed here: `32`
- Upstream check range: `2026-08-12T06:18:46+00:00` through `2026-08-12T06:18:48+00:00`
- Source-native typed articles: `0` of `32`
- Legacy source summaries retired: `0`; still active: `32`
- Migration status: `not_started`

A recent source check or concept rebuild does not imply that every legacy summary has been replaced by reviewed source-native artifacts.

## Rebuild Dependencies

- Source records: `49`
- Approved claims: `12`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
