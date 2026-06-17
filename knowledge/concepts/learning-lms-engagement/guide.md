---
id: authored-learning-lms-engagement
title: Learning, LMS, And Engagement
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Learning, LMS, And Engagement

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Learning, LMS, And Engagement index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS learning work splits into two related but different systems: the Learning Management System and the broader Engagement toolset.

The Learning Management System, introduced in Rock v17.0, is the purpose-built area for structured educational programs, courses, classes, class activities, completion tracking, and training records. Rock’s official LMS documentation describes it as a way to create and manage educational content, training programs, and courses, with assignment, progress tracking, and durable training records inside Rock ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354); [Rock Core Release Notes](https://www.rockrms.com/releasenotes)). RockU also has a dedicated LMS training path covering overview, program creation, administration, activities, and academic calendar operation ([LMS RockU](https://community.rockrms.com/rocku/lms)).

Engagement is the wider ministry-process layer. It includes Connections, Steps, Step Programs, Streaks, Achievements, Sign-Ups, Reminders, and analytics. Rock’s Engagement manual positions these tools around moving people through ministry processes, measuring participation, and making next actions visible to staff ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). RockU’s Engagement track separately covers Steps, Step Programs, Step Types, Step Charts, Badges, Connections, Sign-Ups, Reminders, and operational views ([Engagement RockU](https://community.rockrms.com/rocku/engagement)).

Use LMS when the unit of work is training content: a learner joins a class, completes activities, meets course requirements, and earns completion status. Use Engagement Steps when the unit of work is a ministry milestone: a person attended orientation, completed baptism, joined a team, served for the first time, completed a giving milestone, or moved through a discipleship pathway. Use Group Requirements when eligibility is about whether someone is allowed or ready to participate in a group role or placement. Use Workflows when the process needs custom approval, reminders, signatures, review, or exception handling.

For agents, the safest operational rule is this:

- LMS answers “What training was assigned, attempted, and completed?”
- Steps answer “What engagement milestone happened for this person?”
- Requirements answer “Is this person eligible for this course, group, role, placement, or next step?”
- Reports and Data Views answer “Who matches the current operational condition?”
- Workflows answer “What custom process should run when the condition changes?”

Do not assume every Rock instance has the same LMS pages, block settings, activity types, or system communications. The source pack confirms major LMS behavior for v17.0 and v18.1, but local Rock configuration can rename pages, secure blocks, remove navigation items, customize communications, and add organization-specific workflows. When facts depend on the instance, inspect the current Rock version, the LMS program configuration, the class workspace, block settings, system communications, security roles, and relevant model rows before taking action.

## 2. Scope And Terminology

This guide covers Rock RMS learning and engagement concepts that an agent needs for real administration, implementation, reporting, troubleshooting, and source-code orientation.

The scope includes:

- LMS programs, courses, classes, learning plans, activities, announcements, academic calendar behavior, on-demand behavior, completion tracking, and learner-facing pages.
- LMS requirements and completion models, especially course requirements and activity completions.
- Engagement journeys using Steps, Step Programs, Step Types, Step Charts, Badges, Streaks, Achievements, and related analytics.
- Reporting and administration patterns for LMS and Engagement.
- Related Rock areas that frequently affect learning work: People, Groups, Communications, Workflows, Event Registration, Data Views, Reports, Security, and Platform Configuration.
- Developer, API, Lava, Model Map, and source-code landmarks from the provided source pack.

Use the following working vocabulary.

**Program** is the top-level LMS container. A program groups courses and determines major operating behavior such as administration mode and, depending on setup, academic calendar behavior. Official LMS docs frame program creation as the first step in building a learning program ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

**Course** is the reusable learning subject inside a program. It usually represents the training topic: onboarding, ministry safety, leadership foundations, theological basics, volunteer training, or staff certification. Courses can have requirements. The source-code model map includes `Learning Course` and `Learning Course Requirement` as LMS models ([Model Map](https://community.rockrms.com/ModelMap)).

**Class** is the deliverable instance of a course. The official docs make an important architectural point: learning plans are tied to classes, not directly to courses, so existing class assignments are not destabilized when course-level material changes later ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). Treat the class as the learner-facing and completion-bearing operating unit.

**Learning Plan** is the ordered activity structure for a class. It contains the activities students complete. The official LMS walkthrough shows activity setup with a Video Watch activity, a Media Account selection, a completion threshold, and optional points ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

**Activity** is a learner task inside a class learning plan. Activity behavior varies by activity type. The official docs explicitly warn that some fields are shared across activity types while others are unique to the selected type ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). Rock v18.1 adds a Content Article learning activity type and SMS notifications for new activities ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Completion** is the recorded outcome of a learner’s work. The Model Map names `Learning Class Activity Completion` and `Learning Program Completion` as LMS models ([Model Map](https://community.rockrms.com/ModelMap)). A v19-era source note says the LMS Activity Completion workflow was updated to use the `Learning Class Activity Completion` entity instead of the Student group member entity, which matters for workflow triggers and entity-attribute assumptions ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)).

**Requirement** is a rule that must be satisfied before or during participation. LMS course requirements are represented by `LearningCourseRequirement`. Group requirements are a separate Rock feature that can affect placement and connection automation ([LearningCourseRequirement source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs); [Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

**Step** is an engagement event or milestone associated with a person. Steps live in Step Programs and Step Types. RockU’s Engagement catalog includes Steps Overview, Adding Steps, Step Types, Step Programs, Step Charts, and Steps Badges ([Engagement RockU](https://community.rockrms.com/rocku/engagement)).

**Achievement** is an engagement record that tracks progress toward a configured goal. The Engagement docs describe achievement progress, person navigation, overachievement, and achievement type configuration under People > Engagement > Achievements ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

**Data View** is a reusable query definition over a Rock entity type. It is crucial for reporting, communication audiences, connection automation, and operational targeting. Rock source shows `DataViewService.GetByEntityTypeId` returning Data Views for a specified entity type, ordered by name ([DataViewService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewService.cs)).

## 3. Learning, LMS, And Engagement Mental Model

Think of Rock learning and engagement as layered systems.

The bottom layer is **People**. All learning and engagement ultimately attach to person records, often through group membership, class enrollment, connection requests, communication recipients, or workflow attributes. If the person record is merged, duplicated, inactive, deceased, security-restricted, or missing communication channels, downstream learning behavior can appear broken.

The next layer is **containers**. LMS uses programs, courses, and classes. Engagement uses step programs and step types. Groups use group types, groups, roles, and requirements. Event Registration uses registration instances, registrants, forms, fees, eligibility rules, and signature documents. Each container defines configuration, security, visibility, and operational meaning.

The next layer is **actions**. In LMS, actions are activities, assessments, assignments, content reads, video watches, announcements, and completions. In Engagement, actions are steps, connection activities, sign-ups, reminders, achievements, and streak activity. In Groups, actions include joining, being scheduled, meeting requirements, and completing role-specific prerequisites.

The next layer is **state**. LMS state includes enrollment, activity availability, activity completion, grade or completion status, class completion, and program completion. Engagement state includes connection request status/state, step records, achievement attempts, streak state, and analytics totals. Group state includes membership status, role, requirement status, scheduling availability, and placement eligibility.

The top layer is **automation and visibility**. Data Views, Reports, dashboards, Communication Flows, Workflows, System Communications, badges, analytics charts, and external pages make the state actionable.

An agent should rarely begin by editing configuration. Start by identifying the layer where the problem lives:

1. Is the person known and eligible?
2. Is the container active, visible, secured correctly, and connected to the right page or block?
3. Is the action available to that person at this time?
4. Was state recorded on the expected entity?
5. Is reporting looking at the same entity and status that the feature writes?
6. Did workflow or communication automation run, fail, or target the wrong entity?

That layered mental model prevents common mistakes, such as troubleshooting a learner-facing page when the class is inactive, editing a course when the class-level learning plan is what learners actually see, or building a Data View over Person when the needed condition is stored on `LearningClassActivityCompletion`.

## 4. Source Authority And How To Use This Guide

Use source authority in this order.

First, use official Rock documentation and release notes for supported behavior, version timing, and configuration surfaces. The official LMS manual is the primary source for LMS concepts and workflows ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). The official Engagement manual is the primary source for Steps, Connections, Achievements, Streaks, and engagement administration ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). Rock Core Release Notes are the primary source for version-specific additions and breaking changes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Second, use RockU as operational training context. RockU LMS confirms that Rock provides training paths for overview, program creation, administration, activities, and academic calendar usage ([LMS RockU](https://community.rockrms.com/rocku/lms)). RockU Engagement confirms the operating surfaces staff are trained to use for Steps, Step Programs, Step Charts, Badges, Connections, Reminders, Sign-Ups, and related tools ([Engagement RockU](https://community.rockrms.com/rocku/engagement)).

Third, use Model Map and source-code records for entity names, API paths, block names, data selectors, and implementation clues. Model Map records in the pack identify LMS models including `Learning Class`, `Learning Class Activity`, `Learning Class Activity Completion`, `Learning Class Announcement`, `Learning Class Content Page`, `Learning Course`, `Learning Course Requirement`, and `Learning Program Completion` ([Model Map](https://community.rockrms.com/ModelMap)). Source snippets show REST controller routes, security annotations, view model fields, and reporting components.

Fourth, use community recipes and Q&A only as examples. A recipe about resending group requirement workflows explicitly warns that community recipes are contributed and not reviewed or endorsed by the Rock core team ([Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)). Use them to understand possible pain points, not to establish core behavior.

When this guide says “inspect in a live instance,” it means the provided source pack does not prove the exact local behavior. Agents should inspect the local Rock version, page/block configuration, entity rows, system communications, security settings, and workflow definitions before making changes.

## 5. Core Configuration And Data Model

The LMS configuration model starts with program structure.

A basic LMS implementation follows this chain:

`Learning Program -> Learning Course -> Learning Class -> Learning Plan -> Learning Class Activity -> Learning Class Activity Completion`

The official walkthrough creates a program, then a course, then edits a class, then creates a learning plan for that class ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). The docs’ statement that learning plans are tied to classes, not courses, is operationally central. If an agent is asked to add, remove, or reorder learner activities, inspect the class learning plan first. Do not assume editing the course will affect existing class work.

The Model Map and source pack confirm these LMS models:

- `Learning Class` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Class Activity` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Class Activity Completion` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Class Announcement` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Class Content Page` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Course` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Course Requirement` ([Model Map](https://community.rockrms.com/ModelMap))
- `Learning Program Completion` ([Model Map](https://community.rockrms.com/ModelMap))

The source-code record for `LearningCourseRequirementBag` shows the fields surfaced to the LMS course requirement block view model:

- `LearningCourseIdKey`
- `RequiredLearningCourseCode`
- `RequiredLearningCourseIdKey`
- `RequiredLearningCourseName`
- `RequirementType`

That confirms course requirements can refer from one course to another required course and carry a requirement type enum. It does not prove every UI behavior or every requirement type label in a live instance; inspect the LMS course requirement editor and enum values in the target Rock version before documenting a local policy ([LearningCourseRequirementsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs)).

The source-code record for the REST v2 controller shows `LearningCourseRequirementsController` at `api/v2/models/learningcourserequirements`. It exposes authenticated CRUD-style model endpoints, with read secured by `EXECUTE_READ` or `EXECUTE_UNRESTRICTED_READ` and write secured by `EXECUTE_WRITE` or `EXECUTE_UNRESTRICTED_WRITE` ([LearningCourseRequirementsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs)). Treat this as a developer landmark, not a recommendation to automate writes. API access depends on authentication, authorization, Rock version, and local security policy.

For reporting, the `HasCompletedCourseSelect` data select applies to `Person`, lives in the `LMS` section, returns a boolean column named `HasCompletedCourse`, and builds program options from active learning programs where completion status is tracked. It filters courses by active courses in the selected program and orders them by course order and name ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)). This source record is especially useful for agents building reports: completion reporting may only show expected options when the program is active and completion tracking is enabled.

## 6. Primary Entities And Relationships

### LMS Entity Relationships

A Learning Program is the administrative boundary for related learning. It defines the course catalog for a ministry area, training domain, or organizational program. Depending on mode, it may support continuously available on-demand classes or calendar-driven academic terms.

A Learning Course belongs to a Learning Program. It defines the topic, course code, name, ordering, image/content presentation, and requirement relationships. Because course requirements can reference required courses, agents should expect prerequisite-style dependency chains.

A Learning Class is a concrete delivery instance of a Learning Course. The class is where learners actually interact with the learning plan. A course can have multiple classes over time, especially if one course is offered in multiple semesters, cohorts, campuses, languages, or formats.

A Learning Plan belongs to a class. It is not a course-level global template according to the official docs. This protects existing class assignments from course changes ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

A Learning Class Activity belongs to the class learning plan. Activities can vary by type. The official walkthrough gives a Video Watch example with Media Account, Completion Threshold, and optional points. Rock v18.1 adds Content Article as an activity type and SMS notifications for new learning activities ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354); [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

A Learning Class Activity Completion records that a learner completed an activity. Version caveat: v18-era source commentary says LMS Activity Completion workflows use `Learning Class Activity Completion` rather than Student group member as the entity. If a workflow was built before that change, verify the workflow’s entity type and attribute assumptions ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)).

A Learning Program Completion records program-level completion. The pack confirms the model exists in the LMS category but does not provide its full property map. Inspect Model Map, entity schema, or the database in the target instance before writing SQL against it ([Model Map](https://community.rockrms.com/ModelMap)).

### Engagement Entity Relationships

A Step Program is a container for a journey or ministry pathway. Examples might include discipleship, serving, giving, group life, or assimilation. RockU includes both legacy and current Step Program training, which means agents should check whether a local instance is using newer Step Program surfaces or older legacy pages before giving UI instructions ([Engagement RockU](https://community.rockrms.com/rocku/engagement)).

A Step Type is a configured milestone inside a Step Program. RockU has separate Step Types training, which indicates Step Type configuration is a first-class administrative task ([Step Types via Engagement RockU](https://community.rockrms.com/rocku/engagement)).

A Step is the person-specific record that the milestone occurred. Adding Steps is a trained operational workflow in RockU ([Adding Steps](https://community.rockrms.com/rocku/engagement/adding-steps)).

Badges display step status or related engagement state on person-facing or staff-facing surfaces. RockU includes Steps Badges training ([Steps Badges](https://community.rockrms.com/rocku/engagement/steps-badges)).

Step Charts and Step Analytics provide reporting views. The v18.1 Engagement docs mention Step Analytics updates for KPIs, trends, campuses, totals, and flow; they also mention Core Steps, moving Step Types between programs, Completion Flow, Milestones, Rhythms, Impact Weight, and CTA paths ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

Achievements track progress toward configured goals. The Engagement docs describe achievement progress, person navigation, and overachievement behavior, and place Achievement Type configuration under People > Engagement > Achievements ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

### Requirements Entity Relationships

LMS Course Requirements are course-to-course requirement records. Source-code view model fields confirm a requirement row has a course with requirements, a required course, a required course code/name, and a requirement type ([LearningCourseRequirementsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs)).

Group Requirements are separate from LMS course requirements. They can be checked during connection placement and automation. The Engagement docs describe a Group Requirements Filter with options such as Ignore, Must Meet, and Does Not Meet for connection request automation, and warn that group or group type requirements are checked when saving a placement group ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). RockU also has Group Requirements training ([Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements)).

Do not merge these concepts. A person can meet LMS course requirements but fail a group requirement, or satisfy group requirements while still lacking course completion. If a ministry process needs both, model both explicitly and report them separately.

## 7. Common Learning, LMS, And Engagement Workflows

### Create An On-Demand Training Program

Use on-demand mode when learners can enter at any time and complete content at their own pace. The official LMS docs state that Rock LMS supports an On-Demand mode for continuously running classes not tied to a specific time frame ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

Operational sequence:

1. Create the Learning Program.
2. Create one or more Learning Courses.
3. Create or edit the Learning Class for each course.
4. Build the class learning plan.
5. Add activities in the desired sequence.
6. Configure completion thresholds, grading behavior, points, or activity-specific fields.
7. Confirm learner-facing visibility in the Learning Hub or Learn page.
8. Test as a learner who is not an administrator.
9. Confirm completion records are written on expected LMS entities.
10. Build reporting and staff dashboards.

Before go-live, inspect whether the program is active, whether completion status is tracked, whether courses are active, whether classes are visible externally, and whether security allows the intended audience to enroll or access content.

### Create An Academic Calendar Program

Use academic calendar behavior when classes run in structured terms, semesters, cohorts, or date windows. The LMS documentation includes Academic Calendar Configuration Mode and Academic Calendar sections, and RockU has a dedicated LMS Academic Calendar lesson ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354); [LMS - Academic Calendar](https://community.rockrms.com/rocku/lms/lms-academic-calendar)).

Operational sequence:

1. Confirm the program’s administration mode and calendar mode.
2. Define the academic calendar structure.
3. Configure semesters or terms if the local mode requires them.
4. Create courses.
5. Create classes for the relevant term or window.
6. Configure learning plans for those class instances.
7. Confirm class availability, due dates, and activity scheduling.
8. Test learner access before, during, and after the expected date window.
9. Confirm reports distinguish current term learners from historical learners.

When source material is thin, verify in the target instance: semester field names, class date behavior, whether activity due dates block completion or only affect grading labels, and whether calendar mode changes are allowed after learners have begun.

### Assign Training To Volunteers Or Staff

LMS is usually the right system when the organization needs training records. Group Requirements are usually the right system when the organization needs eligibility checks before someone serves, joins, or is scheduled.

A robust implementation often uses both:

- LMS course for the training itself.
- LMS completion report to identify who completed it.
- Group Requirement to prevent placement or flag missing eligibility.
- Workflow to notify, remind, or escalate.
- Data View to produce the operational list.
- Communication to invite people into the class or remind incomplete learners.

Agents should inspect whether the group requirement already exists before building a new LMS-only report. If the requirement is tied to a group type, changing it can affect many groups.

### Record A Ministry Milestone

Use Engagement Steps when the event is a milestone, not a course activity. Examples: “Attended Next Steps,” “Completed Baptism Class,” “Joined A Group,” “Started Serving,” “Completed First Serve,” or “Completed Membership Covenant.”

Operational sequence:

1. Identify the Step Program.
2. Identify the Step Type.
3. Confirm whether steps should be manually added, workflow-created, event-created, group-driven, or imported.
4. Confirm campus behavior.
5. Add or automate the step.
6. Verify it appears on person profile badges, step charts, or analytics.
7. Confirm whether the step should trigger an achievement, communication, connection request, or workflow.

RockU’s Steps Overview, Adding Steps, Step Types, Step Programs, Step Charts, and Steps Badges lessons are the training context for these operations ([Steps Overview](https://community.rockrms.com/rocku/engagement/steps-overview); [Adding Steps](https://community.rockrms.com/rocku/engagement/adding-steps); [Steps Badges](https://community.rockrms.com/rocku/engagement/steps-badges)).

### Automate Follow-Up From Learning Completion

Common paths:

- Activity completed -> workflow sends staff notification.
- Course completed -> person enters a Data View.
- Program completed -> achievement attempt updates.
- Course completed -> group requirement now met.
- Course not completed after due date -> reminder communication.
- Required training expired or missing -> scheduling warning or blocked placement.

Before building automation, verify which entity the trigger uses. For LMS Activity Completion workflows, source commentary warns that workflows use the `Learning Class Activity Completion` entity in newer behavior rather than the Student group member entity ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)). For course completion reporting, inspect the reporting component and model rows rather than assuming a person attribute was set.

## 8. Courses And Lessons Deep Dive

Rock LMS course design should begin with the operational outcome, not the content library.

A strong course has:

- A clear program owner.
- A defined audience.
- A stable completion meaning.
- A known renewal or expiration policy, if any.
- A class strategy: on-demand, cohort, semester, campus-specific, or role-specific.
- A learning plan that maps directly to the completion meaning.
- Reporting that answers who is not started, in progress, complete, failed, late, or blocked.

The official LMS walkthrough models a basic build path: program, course, class, learning plan, activity ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). Agents should preserve that structure when implementing. Do not treat courses as pages. Courses are configuration objects in a larger completion system.

### Course Configuration Checks

When inspecting a course, gather:

- Program name and status.
- Course name.
- Course code, if used.
- Course active/inactive state.
- Course order within the program.
- Course image or visual assets.
- Course requirements.
- Existing classes attached to the course.
- Whether learners are enrolled in active or historical classes.
- Whether course changes are intended to affect new learners only or existing learners too.

The source-code reporting component orders courses by `Order` and then `Name` when building course options for a selected program ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)). This means course order is not only cosmetic; it can influence admin selection lists and learner navigation.

### Class Design

Because learning plans are tied to classes, class design is where content changes become operational. If a class has active learners, adding, deleting, or reordering activities can affect completion status, learner expectations, due dates, and reporting.

Before editing a class learning plan, inspect:

- Number of enrolled students.
- Number of completed students.
- Number of in-progress students.
- Activity completion rows already recorded.
- Whether activity completion is required for course completion.
- Whether workflows depend on activity IDs or completion events.
- Whether announcements have already been sent.
- Whether system communications mention old activity names.

When a course needs a new curriculum version, prefer creating a new class if existing learners must preserve the old plan. The official class-level learning plan design exists to avoid disrupting existing and completed class assignments ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

### Learning Plan Activity Design

Activities should be granular enough to report progress but not so granular that learners and staff drown in status noise.

For each activity, record:

- Activity type.
- Title.
- Instructions.
- Required/optional status, if present in the local UI.
- Completion threshold or grading rule.
- Points, if used.
- Due date or availability behavior, if used.
- Source content reference, such as media, content article, assessment, assignment, or page.
- Workflow or communication triggers.
- Whether completion is automatic, manual, graded, or learner-submitted.

The LMS docs show a Video Watch activity configured from a Media Account with a 95% completion threshold and optional points ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)). Rock v18.1 adds Content Article activity support ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If a local instance is earlier than v18.1, verify whether Content Article exists before recommending it.

### Lessons Versus Activities

The source pack uses “courses” and “activities” as Rock LMS terms. The user-facing idea of a “lesson” may map to one activity, a group of activities, a content page, or a class session depending on local configuration. Do not assume “lesson” is a native entity unless the live instance or Model Map shows one. In the provided pack, Model Map records include `Learning Class Content Page` and `Learning Class Activity`, not a separate `Learning Lesson` model ([Model Map](https://community.rockrms.com/ModelMap)).

For agent work, translate “lesson” requests into inspection questions:

- Is the user asking about a class activity?
- Is there a content page inside the class?
- Is the “lesson” a content article activity?
- Is it a video, assignment, assessment, or external page?
- Is it a page route, a block, or an LMS entity?
- Does completion attach to the activity, the class, or the course?

## 9. Requirements And Completion Deep Dive

Requirements and completion are where learning becomes operationally enforceable.

### LMS Course Requirements

The `LearningCourseRequirementBag` source record confirms that a course requirement connects the course being configured with another required course. It includes both identifiers and display fields for the required learning course, plus `RequirementType` ([LearningCourseRequirementsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs)).

Before relying on requirements, inspect:

- Which course owns the requirement.
- Which course is required.
- Whether the required course is active.
- Whether the required course’s program is active.
- Whether completion tracking is enabled for the program.
- Requirement type value and meaning.
- Whether requirements are enforced at enrollment, display, completion, or reporting.
- Whether existing learners were grandfathered.

The source pack does not prove exactly when LMS course requirements are enforced in every UI path. Verify in the live class enrollment flow and learner page before promising that a requirement blocks enrollment.

### Completion Tracking

Completion can exist at multiple levels:

- Activity completion.
- Class completion.
- Course completion.
- Program completion.
- Achievement completion.
- Group requirement satisfaction.

The reporting source `HasCompletedCourseSelect` shows that Rock can present a Person-level reporting column for completed learning courses. It builds program options from active programs where completion status is tracked ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)). If a course does not appear in report configuration, inspect program active state and completion tracking first.

The Model Map confirms `Learning Class Activity Completion` and `Learning Program Completion` models. The pack does not provide full database columns. When writing SQL, API queries, or Lava against completions, inspect the target instance’s schema, Model Map details, or REST response shape first ([Model Map](https://community.rockrms.com/ModelMap)).

### Activity Completion Workflows

Version caveat is significant here. A source note reports that LMS Activity Completion workflow behavior was updated so the workflow uses `Learning Class Activity Completion` rather than the Student group member entity ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)). This affects:

- Workflow entity type.
- Available merge fields.
- Entity attribute values.
- Lava references.
- Existing custom workflow logic.
- Tests that previously selected a group member as the trigger entity.

When troubleshooting completion workflows:

1. Open the workflow type.
2. Confirm trigger source and entity type.
3. Confirm the entity is `LearningClassActivityCompletion` or the local equivalent.
4. Inspect workflow attributes.
5. Inspect whether the activity completion row exists.
6. Check workflow logs and exception logs.
7. Confirm security allows the workflow action to read the related person, class, activity, and course.
8. If upgraded from earlier versions, compare workflow assumptions to current release notes.

### Group Requirements As A Parallel System

Group requirements are not LMS course requirements, but they frequently interact with learning. A volunteer safety course may be recorded in LMS, then referenced by a group requirement that determines whether someone can serve.

The Engagement docs describe group requirement behavior inside connection placement automation. The Group Requirements Filter can be set to Ignore, Must Meet, or Does Not Meet. If a connection request has a placement group, Rock can evaluate group or group type requirements against the requestor before automation proceeds ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

A community recipe about resending group requirement helper workflows highlights a real operational pain point: requirement workflows tied to signatures or manual sending may need staff-friendly resend paths. Because this is a community recipe, treat it as an example and review carefully before implementation ([Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)).

## 10. Engagement Journeys Deep Dive

Engagement journeys are best modeled as visible milestones, not hidden reports.

A Step Program should represent a coherent journey: assimilation, discipleship, serving, groups, giving, leadership development, or care. Step Types represent the milestones. Step records represent what actually happened for a person.

RockU’s Engagement curriculum confirms the major staff operations around Steps: overview, adding steps, badges, step programs, step charts, and step types ([Engagement RockU](https://community.rockrms.com/rocku/engagement)). The official Engagement docs show v18.1 enhancements to Step Analytics, Core Steps, Step Type movement between programs, Completion Flow, Milestones, Rhythms, Impact Weight, and CTA paths ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

### Step Program Design

Good Step Programs are stable. Changing the meaning of an existing Step Type can corrupt historical reporting. If the ministry meaning changes, consider creating a new Step Type rather than renaming the old one.

For each Step Program, document:

- Ministry owner.
- Intended audience.
- Step Types.
- Whether order matters.
- Whether completion flow is configured.
- Campus behavior.
- Badge behavior.
- Reporting dashboards.
- CTA paths.
- Workflows triggered by steps.
- Data Views and reports that depend on the program.

### Step Types

For each Step Type, inspect:

- Name.
- Program.
- Active state.
- Order.
- Whether it is a milestone.
- Rhythm settings, if present.
- Impact weight, if present.
- CTA path, if present.
- Badge display.
- Security.
- Automation sources.
- Historical data volume.

Because v18.1 introduced or changed several step-related settings, verify the target Rock version and UI before documenting exact field labels ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)).

### Adding Steps

Steps can be added manually or automated. RockU has a dedicated Adding Steps lesson ([Adding Steps](https://community.rockrms.com/rocku/engagement/adding-steps)). Manual entry is useful for staff correction and one-off ministry updates. Automation is better for consistent milestone recording from registrations, workflows, group joins, attendance, or LMS completion.

When adding a step manually, verify:

- Correct person.
- Correct Step Program.
- Correct Step Type.
- Correct date.
- Correct campus.
- Duplicate existing steps.
- Whether the step should trigger workflows or achievement updates.

When automating steps, verify:

- Trigger condition.
- Idempotency.
- Duplicate handling.
- Date source.
- Campus source.
- Security context.
- Error logging.
- Rollback or correction path.

### Badges

Badges make engagement state visible on staff-facing surfaces. RockU includes Steps Badges training ([Steps Badges](https://community.rockrms.com/rocku/engagement/steps-badges)). Use badges for operationally important milestones, not every possible activity. Too many badges make staff profiles harder to scan.

Badge troubleshooting checklist:

- Is the badge configured and active?
- Is the person in the expected audience?
- Does the person have the underlying step or achievement?
- Does the badge query use the correct Step Program and Step Type?
- Is the badge secured to the current user?
- Is page/block cache hiding a recent update?
- Is the profile page using a customized badge list?

### Achievements And Streaks

Achievements track progress toward goals. The Engagement docs describe achievement progress and allow for overachievement when configured ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). Use Achievements when the ministry wants “progress toward a goal,” not just “this milestone happened.”

Examples:

- Attend four classes in a quarter.
- Serve three times in a month.
- Complete a multi-step journey.
- Maintain a participation streak.
- Reach a giving or attendance consistency milestone.

Before configuring achievements, inspect:

- Achievement Type settings.
- Source data.
- Progress calculation.
- Whether overachievement is allowed.
- Workflows triggered by attempts.
- Timing behavior for rapid attempt creation.
- Analytics expectations.

Release notes in the pack mention a fix where Achievement Type detail could save newly created Achievement Types without important settings, plus a post-update repair job, and a timing issue around workflows when many `AchievementAttempts` were recorded quickly ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If achievements behave inconsistently after an upgrade, check release notes, post-update jobs, and workflow timing.

## 11. Reporting And Administration Deep Dive

Reporting is not an afterthought in LMS and Engagement. It is how staff find incomplete learners, blocked volunteers, late assignments, successful courses, and journey drop-off.

### LMS Reporting

Common LMS reports:

- Active learners by program.
- Active learners by course.
- Active learners by class.
- Completion status by course.
- Completion status by program.
- Activity completions by class.
- Incomplete required activities.
- Learners with missing prerequisites.
- Learners who completed course but are not in target group.
- Learners who completed training but still fail group requirements.
- Learners whose completion workflow failed.

Use the `Has Completed Course` data select when a Person report needs a boolean course completion column. Source code shows it applies to `Person`, lives in the `LMS` section, and returns a boolean column named `HasCompletedCourse` ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)).

If a report cannot find the target course:

1. Confirm the program is active.
2. Confirm completion tracking is enabled.
3. Confirm the course is active.
4. Confirm the course belongs to the selected program.
5. Confirm the reporting component exists in the current Rock version.
6. Confirm the current user has security to see the program/course.
7. Inspect whether the report is using Person, Group Member, Learning Class, or Completion entity.

### Engagement Reporting

Common Engagement reports:

- Step completions by program.
- Step completions by type.
- Step completions by campus.
- Step flow from one milestone to another.
- Step trends over time.
- People missing a next step.
- Achievement progress.
- Streak continuity.
- Connection request state/status.
- Placement group requirement failures.
- Sign-up conversion.
- Reminder effectiveness.

The Engagement docs identify Step Analytics updates for KPIs, Trends, Campuses, Totals, and Flow in Rock v18.1 ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). RockU includes Step Charts training ([Engagement RockU](https://community.rockrms.com/rocku/engagement)). Use built-in analytics where possible before building custom SQL.

### Data Views

Data Views are a common dependency for reporting, communication targeting, and automation. Source code confirms `DataViewService.GetByEntityTypeId` returns Data Views associated with a specified entity type and orders them by name ([DataViewService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewService.cs)).

Important Data View rules for agents:

- Match the Data View entity type to the automation field. If a connection automation asks for a Connection Request Data View, a Person Data View will not appear.
- Avoid recursive Data View dependencies. Source code includes logic to detect a Data View used inside its own child filters through another Data View filter path ([DataViewService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewService.cs)).
- Prefer built-in LMS reporting components for course completion before writing SQL.
- When using Data Views for Communication Flows, confirm the conversion goal entity and settings. Source snippets show Communication Flow settings for “Entered Data View” store a Data View list item ([communicationFlowDetailEnteredDataViewSettingsBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailEnteredDataViewSettingsBag.d.ts)).

### Administration

Administrative review should include:

- Program owners.
- Course owners.
- Class facilitators.
- Security roles.
- External access.
- System communications.
- Completion workflows.
- Reports and dashboards.
- Data retention expectations.
- Upgrade caveats.
- Testing accounts.
- Staff training materials.

Rock’s LMS docs include Program Administration Modes, Security, External Site Access, Facilitators, Configure Program, Semesters, and Courses headings, which indicates LMS administration spans configuration, permission, external visibility, and people assignment ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

## 12. Related Rock Areas: People, Groups, Communications, Workflows, Event Registration, Data Views, Reports, Security, Platform Configuration

### People

People are the primary audience and reporting subject. Before troubleshooting a learner or engagement journey, inspect:

- Person record status.
- Duplicate records.
- Family relationships.
- Primary alias.
- Campus.
- Communication channels.
- Security restrictions.
- Existing group memberships.
- Existing step records.
- Existing LMS completions.

### Groups

Groups often determine ministry eligibility and operational assignment. Group Requirements can be checked during connection placement and group operations ([Engagement](https://community.rockrms.com/documentation/bookcontent/39); [Group Requirements](https://community.rockrms.com/rocku/groups/group-requirements)).

Use Groups when the outcome is membership, serving, scheduling, role assignment, or placement. Use LMS when the outcome is training completion. Connect them through Data Views, requirements, and workflows.

### Communications

Learning systems depend on communication for invitations, announcements, reminders, and activity notifications. Rock v18.1 adds SMS notifications for new learning activities and updates the Learning Activity Available system communication message body/SMS message according to release notes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Before upgrading or editing communications:

- Inspect System Communications.
- Save customized templates before upgrade if release notes warn they may be overwritten.
- Verify email and SMS transport.
- Verify recipient communication preferences.
- Verify unsubscribe/compliance behavior.
- Test as a real learner.

Some RockU communication lessons in the pack are labeled legacy. If using them as background, confirm the current communication surface before following old implementation steps ([Communication Preferences Legacy](https://community.rockrms.com/rocku/communication/communication-preferences-legacy)).

### Workflows

Use workflows for custom process logic:

- Enrollment approval.
- Requirement exceptions.
- Signature documents.
- Reminder schedules.
- Staff review.
- Completion notifications.
- Step automation.
- Escalation.
- Cleanup or resend utilities.

For LMS Activity Completion workflows, verify entity type after upgrades because newer behavior uses `Learning Class Activity Completion` ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)).

Legacy workflow training should be treated carefully. The pack notes that Text to Workflow functionality has been replaced by SMS Pipeline features ([Text to Workflow Legacy](https://community.rockrms.com/rocku/workflows/text-to-workflow)).

### Event Registration

Event Registration often feeds learning and engagement. A class may be promoted through an event, a milestone may be recorded after registration, or eligibility may control who can sign up.

Source snippets show Registration Entry view models include registrant eligibility, family member ineligibility, forms, fields, fees, sessions, payment controls, and related structures ([registrantEligibilityBag.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationEntry/registrantEligibilityBag.d.ts); [registrationEntryInitializationBox.d.ts](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Event/RegistrationEntry/registrationEntryInitializationBox.d.ts)). Use those as developer landmarks. For live configuration, inspect the registration template and instance.

### Security

Security controls who can administer programs, view classes, enroll, complete activities, see reports, run workflows, and access API endpoints.

The REST v2 source record for `LearningCourseRequirementsController` shows read/write endpoint security using execute read/write and unrestricted read/write actions ([LearningCourseRequirementsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs)). In the UI, block and entity security may further restrict access.

Before reporting an LMS bug, test with:

- Rock admin.
- Program administrator/facilitator.
- Intended learner.
- Anonymous external visitor, if applicable.
- A learner with no group membership.
- A learner who fails requirements.

### Platform Configuration

Platform-level dependencies include:

- Rock version.
- Enabled jobs.
- System communications.
- SMS/email transports.
- Media accounts.
- Content channels/articles.
- Page routes.
- Block settings.
- Entity attributes.
- Security roles.
- Lava-enabled fields.
- REST API security.
- Cache behavior.

LMS uses media/content/communications/platform features; Engagement uses reporting/workflow/security/communication features. Troubleshooting should include platform checks, not just LMS screens.

## 13. Administration And Operational Guardrails

### Guardrail 1: Do Not Edit Active Learning Plans Blindly

Learning plans are tied to classes and may have active learner completions. Before editing activities, capture current class state and decide whether to create a new class instead. The official class-level learning plan design exists to avoid disrupting existing learners ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

### Guardrail 2: Treat Requirements As Policy

Course requirements and group requirements can block people or create staff warnings. Require ministry-owner signoff before changing them. Document why the requirement exists, who owns it, and what exception path exists.

### Guardrail 3: Verify Entity Types Before Automating

Do not assume a workflow receives Person, Group Member, or Student. LMS activity completion workflows may use `Learning Class Activity Completion` in newer behavior ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)). Data Views and Reports must match entity types.

### Guardrail 4: Preserve Customized System Communications

Release notes warn that the Learning Activity Available System Communication email body and associated SMS message may be updated and customized content should be saved before updating ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Before upgrades, inspect and export customized system communications.

### Guardrail 5: Separate Training Completion From Ministry Qualification

Completing a course may be one part of qualification. A person may also need background checks, signed documents, age/grade eligibility, leader approval, group placement, or campus-specific requirements.

### Guardrail 6: Use Built-In Reporting Before Custom SQL

Rock includes LMS reporting components such as `Has Completed Course` for Person reports ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)). Use built-ins first, then add custom reports when the built-ins do not answer the operational question.

### Guardrail 7: Mark Legacy Training As Legacy

Several RockU items in the pack are labeled legacy, including Step Flow legacy and Text to Workflow legacy ([Step Flow Legacy](https://community.rockrms.com/rocku/engagement/step-flow); [Text to Workflow Legacy](https://community.rockrms.com/rocku/workflows/text-to-workflow)). Verify current replacements before implementing.

## 14. Developer, API, Lava, And Source-Code Landmarks

### Source Repository

Rock source code is available in the SparkDevNetwork/Rock repository ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)). Use source snippets as implementation landmarks, but verify branch/version alignment with the local Rock instance. The source pack uses the `develop` branch, which may include behavior newer than production releases.

### LMS API Landmarks

`LearningCourseRequirementsController` exists in REST v2 at:

`api/v2/models/learningcourserequirements`

The controller supports authenticated read and write operations with execute read/write security actions ([LearningCourseRequirementsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs)).

A generated legacy REST controller also exists for Learning Course Requirements under `Rock.Rest.Controllers`, backed by `LearningCourseRequirementService` ([LearningCourseRequirementsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Controllers/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs)).

The service class `LearningCourseRequirementService` extends Rock’s generic service and exposes generated attribute-query support for `LearningCourseRequirementAttributeValues` ([LearningCourseRequirementService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/LearningCourseRequirementService.CodeGenerated.cs)).

### Reporting Landmarks

`HasCompletedCourseSelect` is a Person data select in the LMS section. It builds program options from active programs where completion status is tracked, course options from active courses in the selected program, and exposes a boolean “Has Completed Course” column ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)).

`DataViewService` provides entity-type-based Data View lookup and recursion checks for Data View nesting ([DataViewService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewService.cs)).

`DataViewSearch` has a block setting called “DataView URL Format” with Lava support and a default URL pattern of `/reporting/dataViews?DataViewId={{ DataView.Id }}` in the source snippet ([DataViewSearch.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs)).

### Lava Landmarks

Use Lava carefully with LMS and Engagement because many objects are entity-specific. If a field stores a related entity, inspect whether the Lava filter returns an object, ID, GUID, or formatted value.

A community Q&A about linking content channel items to event details shows a common pattern: the correct route parameter may be an occurrence ID rather than the broader event item ID, depending on the site route ([Content Channel Event Item Link](https://community.rockrms.com/ask/developing/2786)). Apply that lesson broadly: verify the target page route and expected key before building links from LMS content, event registration, or content channels.

## 15. Reporting, Analytics, And Model Map

Model Map is useful for confirming entity existence and category. The source pack identifies several LMS models in the LMS category ([Model Map](https://community.rockrms.com/ModelMap)). However, the provided Model Map excerpts do not include full property lists. Use Model Map as a starting point, then inspect live schema, REST output, or source code for exact columns and navigation properties.

For LMS analytics, answer these questions:

- How many learners started?
- How many completed?
- How many are stuck on each activity?
- Which activities have the highest failure or late rate?
- Which courses have prerequisites blocking enrollment?
- Which programs produce completions that matter to Groups or Engagement?
- Which completion workflows failed?
- Which communications were sent and delivered?

For Engagement analytics, answer these questions:

- How many people completed each Step Type?
- How many moved from one Step Type to the next?
- Where does the journey lose people?
- Which campuses differ from the trend?
- Which steps are stale or missing?
- Which achievements are in progress or overachieved?
- Which badges are operationally useful?
- Which CTAs are producing movement?

The v18.1 Engagement docs specifically identify Step Analytics dimensions of KPIs, Trends, Campuses, Totals, and Flow ([Engagement](https://community.rockrms.com/documentation/bookcontent/39)). Build custom analytics only when those built-in dimensions do not answer the ministry question.

## 16. Version And Release Caveats

### Rock v17.0

Rock v17.0 introduced the Learning Management System as a core feature for educational content, training programs, and courses ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). The official LMS manual also notes the feature starts in v17 ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)).

If a local instance is earlier than v17, do not assume LMS exists. Look for plugin or custom training implementations instead.

### Rock v18.1

Rock v18.1 adds or updates several relevant LMS and Engagement features:

- LMS Content Article activity type.
- SMS notifications for new learning activities.
- Completion grading system display improvements.
- Step Analytics updates.
- Core Steps and eRA step type.
- Moving Step Types between programs.
- Completion Flow for Steps.
- Step Milestones, Rhythms, Impact Weight, and CTA paths.

These are cited in the LMS manual, Engagement manual, and release notes ([Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354); [Engagement](https://community.rockrms.com/documentation/bookcontent/39); [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

If the instance is v17.x or early v18, verify which of these are present before using them.

### Rock v18.3 And v19.1 Release Notes In Pack

The hydrated release notes page includes headings for Rock v19.1 released May 20, 2026 as Beta and Rock v18.3 released May 20, 2026 as Alpha, plus fixes involving group requirements, achievements, assignments, and LMS communications ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Because alpha/beta release notes can change and production instances may not run those versions, verify local version before applying those caveats.

Important caveats from the pack:

- Group requirement calculation performance and deletion/reevaluation fixes are noted.
- Achievement Type save repair and rapid workflow triggering fixes are noted.
- Assignments submitted before due date but graded later had a late-marking fix.
- Learning Activity Available system communication content may be overwritten on update.
- LMS Activity Completion workflow entity assumptions may need review.

### Develop Branch Caveat

GitHub source snippets come from the `develop` branch. Do not assume they exactly match a production Rock instance. Use them to locate concepts and likely implementation paths, then verify against the installed Rock version.

## 17. Implementation Playbooks

### Playbook: Launch A Volunteer Training LMS Program

1. Define the training policy.
2. Identify the people or group roles affected.
3. Create the Learning Program.
4. Create each Learning Course.
5. Add course requirements only where prerequisite completion is truly required.
6. Create on-demand classes for evergreen training.
7. Build class learning plans.
8. Add activities.
9. Configure completion thresholds and grading rules.
10. Configure announcements and activity notifications.
11. Test learner access from internal and external pages.
12. Build a Person report using LMS completion fields.
13. Add or update Group Requirements if completion affects serving eligibility.
14. Build reminder communications for incomplete learners.
15. Document owner, review cycle, and upgrade caveats.

Verify live:

- Program active.
- Completion status tracked.
- Course active.
- Class visible.
- Activities completable.
- Completion row created.
- Report shows expected status.
- Group requirement changes after completion, if configured.
- SMS/email sends correctly.

### Playbook: Add A New Course Requirement

1. Identify the dependent course.
2. Identify the required course.
3. Confirm both are active and in the intended program relationship.
4. Inspect existing learners and completions.
5. Choose requirement type.
6. Configure requirement.
7. Test as a learner who has completed the required course.
8. Test as a learner who has not completed it.
9. Confirm reporting.
10. Notify staff of changed enrollment or completion behavior.

If enforcement behavior is unclear, inspect the live LMS enrollment and class access flow. The source pack confirms requirement models and fields, but not every UI enforcement moment.

### Playbook: Convert A Training Completion Into An Engagement Step

1. Identify LMS completion source: activity, course, class, or program.
2. Identify target Step Program and Step Type.
3. Decide whether completion should create one step ever or repeated steps.
4. Build or inspect workflow trigger.
5. Confirm trigger entity type.
6. Add duplicate protection.
7. Set step date from completion date.
8. Set campus from person, class, or configured default.
9. Test with a controlled learner.
10. Verify step badge and analytics.

Do not attach the step to a course name if the ministry meaning is broader. Use stable Step Types.

### Playbook: Build A Learning Dashboard

Include:

- Programs active.
- Courses active.
- Classes active.
- Learners enrolled.
- Learners not started.
- Learners in progress.
- Learners complete.
- Activity completion bottlenecks.
- Requirement failures.
- Workflow failures.
- Communication delivery status.
- Group eligibility exceptions.

Start with built-in LMS data selects and reports. Add SQL only when required. If SQL is needed, inspect model schema before writing.

### Playbook: Upgrade Review For LMS And Engagement

Before upgrade:

1. Record Rock version.
2. Export or document customized system communications.
3. List LMS workflows.
4. List activity completion workflows and entity assumptions.
5. List active programs/classes.
6. List Step Programs and Achievement Types.
7. Review release notes for LMS, Engagement, Group, Communication, Workflow, Reporting, and Security.
8. Test upgrade in a non-production environment.
9. Verify completion workflows, activity notifications, and reports after upgrade.

Special attention: Rock release notes warn that Learning Activity Available communication content may be updated and custom content should be preserved ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 18. Troubleshooting Decision Tree

### Learner Cannot See A Course

Check:

1. Is the program active?
2. Is the course active?
3. Is the class active?
4. Is the class in the correct mode or term?
5. Is the learner eligible?
6. Are course requirements blocking access?
7. Is the external Learning Hub page configured?
8. Does the learner have security to view the page/block?
9. Is the class meant for external access?
10. Is the learner logged in as the correct person?

### Learner Completed Activity But Course Did Not Complete

Check:

1. Does the activity completion row exist?
2. Was the threshold met?
3. Is the activity required?
4. Are there other incomplete activities?
5. Is grading pending?
6. Was the submission late or marked incomplete?
7. Did a workflow fail?
8. Is the report looking at course completion while only activity completion exists?
9. Is completion tracking enabled at the program level?
10. Is the report filtered to the correct class or course?

### Course Does Not Appear In Reporting

Check:

1. Is the program active?
2. Is completion status tracked?
3. Is the course active?
4. Does the report component use the correct program?
5. Does the current user have security?
6. Is the report using Person-level LMS data select?
7. Is the class completed but course completion not recorded?
8. Is the Rock version new enough for the reporting component?

The `HasCompletedCourseSelect` source specifically filters program options to active programs with completion tracking enabled and course options to active courses in the selected program ([HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)).

### Completion Workflow Did Not Run

Check:

1. Does the completion row exist?
2. Is the workflow configured on the activity/course/program?
3. What entity type does the workflow expect?
4. Does the entity match current Rock behavior?
5. Are workflow triggers active?
6. Did the workflow error?
7. Did security block reads?
8. Was the workflow configured before an upgrade?
9. Are there exception log entries?
10. Did many completions happen at once?

Review the v19-era caveat about activity completion workflows using `Learning Class Activity Completion` ([GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)).

### Group Requirement Still Fails After LMS Completion

Check:

1. Is the group requirement actually based on LMS completion?
2. Is it based on the correct course?
3. Is it checking course, class, program, or activity completion?
4. Did completion status write correctly?
5. Has the group requirement calculation job run?
6. Is the group requirement inherited from group type?
7. Is the person in the correct group role?
8. Is a manual requirement involved?
9. Are workflows tied to the old state?
10. Does release note history mention group requirement calculation fixes for the local version?

### Step Badge Not Showing

Check:

1. Does the person have the step?
2. Is the step in the expected Step Program?
3. Is the Step Type correct?
4. Is campus filtering involved?
5. Is the badge active?
6. Is the badge on the profile page?
7. Does the current user have security?
8. Is cache stale?
9. Was the step added to a legacy program or moved type?
10. Is the badge configured for the right source?

### Announcement Or Activity Notification Not Sent

Check:

1. Is the announcement configured to send immediately or scheduled?
2. Is the learner enrolled?
3. Does the learner have email/SMS channels?
4. Is the relevant system communication active?
5. Was the system communication customized and overwritten during upgrade?
6. Are communication transports healthy?
7. Is SMS notification supported in the local Rock version?
8. Are communication preferences blocking delivery?
9. Are there communication errors?
10. Was the activity actually newly available?

Rock v18.1 added SMS notifications for new learning activities ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 19. Agent Task Recipes

### Recipe: Audit One LMS Program

Collect:

- Program name, ID/GUID, active status.
- Administration mode.
- Calendar mode.
- Completion tracking setting.
- Courses and active state.
- Classes and learner counts.
- Learning plan activity counts.
- Completion workflows.
- Announcements.
- External access pages.
- Security roles.
- Reports and Data Views.

Output:

- What is active.
- What learners can see.
- What completion means.
- What automation runs.
- What needs review.

### Recipe: Find Why A Person Is Not Complete

Inspect:

- Person record.
- Enrollment/class membership.
- Course requirements.
- Activity list.
- Activity completions.
- Grades/submissions.
- Course completion status.
- Program completion status.
- Workflow logs.
- Reporting filters.

Report:

- The first missing condition.
- The entity where it is stored.
- The staff action needed.
- Whether the issue is learner action, configuration, grading, workflow, reporting, or version behavior.

### Recipe: Prepare A Course For Launch

Verify:

- Course owner.
- Course description and code.
- Image/content.
- Class created.
- Learning plan complete.
- Activities tested.
- Completion threshold tested.
- Announcement tested.
- Learner page tested.
- Completion report tested.
- Security tested.
- Staff support path documented.

### Recipe: Build A Step Journey From Training

Map:

- Training course -> Step Program.
- Course completion -> Step Type.
- Completion date -> Step date.
- Learner campus -> Step campus.
- Workflow -> duplicate-safe step creation.
- Badge -> staff visibility.
- Step Chart -> leadership reporting.

Test:

- First completion.
- Duplicate completion.
- Incomplete learner.
- Learner with missing campus.
- Workflow failure.
- Report appearance.

### Recipe: Review Upgrade Risk

Inspect:

- Current Rock version.
- Target Rock version.
- LMS release notes.
- Engagement release notes.
- Group requirement release notes.
- Communication release notes.
- Workflow release notes.
- Customized system communications.
- Completion workflows.
- Achievement workflows.
- Reports using LMS/Step entities.

Produce:

- Upgrade risks.
- Required pre-upgrade exports.
- Post-upgrade tests.
- Rollback considerations.
- Staff-facing behavior changes.























<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `23`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| community-reviewed | implementation_pattern | LMS activity completion can interact with existing Rock concepts such as groups, group sync, and workflow actions, which makes LMS useful for volunteer training and operational follow-up. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | For dashboard speed, expensive journey analytics can be calculated into a persisted dataset on a schedule rather than recalculating all historical engagement data on each page load. | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | An LMS class can combine content acknowledgements, required video watching, quizzes, file uploads, and facilitator-scored activities, so training design should define both learner actions and staff review responsibilities. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | Existing training videos can become Rock LMS activities, but completion, sequencing, and facilitator review should be configured intentionally around the desired learner outcome. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Rock LMS organizes training into programs, courses, class instances, learning plans, activities, and learning participants, with the program deciding whether the experience is on-demand or academic-calendar based. | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) |
| community-reviewed | operational_guidance | AI coaching should be framed as an assisted resource-routing layer with reviewable prompts, ministry-approved categories, and clear human oversight. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | Publishing a ministry dashboard can change behavior when it exposes underused content or completion gaps; teams can then adjust marketing, launch timing, content length, and follow-up strategy based on observed engagement. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | Journey reporting may need to join content-channel items, generated groups, group members, notes/comments, and attendance-style completion events because the ministry experience spans both content and group participation models. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) |
| community-reviewed | operational_guidance | When moving from another LMS into Rock, plan for differences in platform logic instead of assuming videos and lessons can be imported without redesign. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) |
| community-reviewed | operational_guidance | Online next-step pathways can combine dashboards, content, and LMS when the church defines the discipleship path being supported. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) |
| community-reviewed | operational_guidance | A binge-style content idea can become a structured learning path when the church defines sequence, purpose, and completion signals rather than only embedding videos. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| community-reviewed | operational_guidance | Early LMS work should start with a few clear training use cases, such as volunteer or staff onboarding, before attempting a large content migration. _(live verification recommended)_ | [source](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/pLPbvokPR4) |
| More |  | 11 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->









































<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `12`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Communication Preferences [Legacy] Transcript Insight](https://community.rockrms.com/rocku/communication/communication-preferences-legacy) | approved_for_public_distillation | 3 | media-insight:424563b14f71f033 |
| [Group Requirements Transcript Insight](https://community.rockrms.com/rocku/groups/group-requirements) | approved_for_public_distillation | 3 | media-insight:9a2fef11fd30a564 |
| [LMS - Activities Transcript Insight](https://community.rockrms.com/rocku/lms/lms-activities) | approved_for_public_distillation | 3 | media-insight:2a0b01a118d004aa |
| [LMS - Administration Transcript Insight](https://community.rockrms.com/rocku/lms/lms-administration) | approved_for_public_distillation | 3 | media-insight:f0c688c9ed0d7ed7 |
| [LMS - Create a Program Transcript Insight](https://community.rockrms.com/rocku/lms/lms-create-a-program) | approved_for_public_distillation | 3 | media-insight:d3591980e5622db9 |
| [Labels [Legacy] Transcript Insight](https://community.rockrms.com/rocku/check-in/labels-legacy) | approved_for_public_distillation | 3 | media-insight:a8ed08ea505e5367 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) | approved_for_public_distillation | 4 | media-insight:51fb82169d3a4818 |
| [Media Watch Transcript Insight](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/X9mQdX8BQo) | approved_for_public_distillation | 3 | media-insight:927b060aba73b666 |
| More |  | 4 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->























## 20. Source Map And Dependency Notes

Primary LMS sources:

- Official LMS manual: [Learning Management System](https://community.rockrms.com/documentation/bookcontent/43/354)
- LMS RockU training index: [LMS](https://community.rockrms.com/rocku/lms)
- LMS Overview: [LMS - Overview](https://community.rockrms.com/rocku/lms/lms-overview)
- LMS Create a Program: [LMS - Create a Program](https://community.rockrms.com/rocku/lms/lms-create-a-program)
- LMS Administration: [LMS - Administration](https://community.rockrms.com/rocku/lms/lms-administration)
- LMS Activities: [LMS - Activities](https://community.rockrms.com/rocku/lms/lms-activities)
- LMS Academic Calendar: [LMS - Academic Calendar](https://community.rockrms.com/rocku/lms/lms-academic-calendar)
- Rock release notes: [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

Primary Engagement sources:

- Official Engagement manual: [Engagement](https://community.rockrms.com/documentation/bookcontent/39)
- Engagement RockU index: [Engagement](https://community.rockrms.com/rocku/engagement)
- Steps Overview: [Steps Overview](https://community.rockrms.com/rocku/engagement/steps-overview)
- Adding Steps: [Adding Steps](https://community.rockrms.com/rocku/engagement/adding-steps)
- Steps Badges: [Steps Badges](https://community.rockrms.com/rocku/engagement/steps-badges)
- Step Flow legacy: [Step Flow [Legacy]](https://community.rockrms.com/rocku/engagement/step-flow)
- Step Programs legacy: [Step Programs [Legacy]](https://community.rockrms.com/rocku/engagement/step-programs-legacy), used only as historical training context; verify current Step Program screens before giving UI instructions.

Primary source-code landmarks:

- Rock repository: [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)
- Course requirement view model: [LearningCourseRequirementsBag.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs)
- Course requirements REST v2 controller: [LearningCourseRequirementsController.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs)
- Course requirement service: [LearningCourseRequirementService.CodeGenerated.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/LearningCourseRequirementService.CodeGenerated.cs)
- Person LMS report select: [HasCompletedCourseSelect.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)
- Data View service: [DataViewService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataView/DataViewService.cs)
- Data View Search block: [DataViewSearch.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs)

Secondary and cautionary sources:

- Community recipe for group requirement workflow resend: [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482)
- Community Q&A for route/entity linking caution: [Content Channel Event Item Link](https://community.rockrms.com/ask/developing/2786)
- Triumph GitHub Spotlight with LMS workflow caveat: [GitHub Spotlight: 11/14/2025](https://www.triumph.tech/resources/github-spotlight-11142025)
- Legacy label training overlap: [Labels [Legacy]](https://community.rockrms.com/rocku/check-in/labels-legacy), included only as a reminder that training and operational artifacts may involve adjacent systems; do not use it as LMS implementation authority.

Dependency notes:

- LMS depends heavily on People, Communications, Security, Reporting, Media/Content, Workflows, and Platform Configuration.
- Learning-related qualification often depends on Groups and Group Requirements.
- Event Registration can create learning audiences or engagement milestones but is not itself LMS.
- Data Views are central to reporting and automation, but only when the entity type matches the target feature.
- Release notes must be checked before changing LMS communications, activity completion workflows, group requirements, achievements, or Step Analytics behavior.
- When source material is thin, inspect the live Rock instance instead of assuming behavior: version, page routes, block settings, entity schema, security, system communications, workflows, jobs, and actual completion rows.
