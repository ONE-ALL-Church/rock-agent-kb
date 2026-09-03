---
id: authored-learning-lms-engagement
title: Learning, LMS, And Engagement
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "7e25b9ee377b7e0528fce8f36855448eafd345fba24f6e4d8297f5aaf119475d"
---

# Learning, LMS, And Engagement

## Agent Summary

Rock’s Learning Management System provides a structured way to assign training, deliver educational content, track progress, and retain completion records. Its core hierarchy is:

**Program → Course → Class → Learning Plan → Activity → Participant completion**

A program uses either **On-Demand** mode for continuously available, self-paced learning or **Academic Calendar** mode for semester-bound classes with dates and additional academic features. Learning plans belong to class instances rather than directly to courses, allowing future classes to change without rewriting the activity plan of an existing or completed class. [Intro to LMS](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms), [Create the Learning Plan](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan)

When handling an LMS request, an agent should first identify:

1. The installed Rock version.
2. The program and its configuration mode.
3. The course and specific class instance.
4. Whether the request concerns configuration, day-to-day administration, learner access, grading, completion, notification delivery, or reporting.
5. The acting person’s LMS roles and object-level permissions.
6. Whether the requested outcome depends on a background job, workflow, group operation, communication configuration, or live completion record.

Do not equate enrollment, activity submission, a passing grade, class completion, course completion, and program completion. The supplied evidence describes these as related but distinct surfaces, with program completion optionally maintained by a background job. [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program), [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class)

## Scope And Boundaries

This guide covers evidence-supported LMS operations:

- Programs, courses, class instances, semesters, learning plans, and activities.
- Prerequisites and course equivalencies.
- Enrollment-facing publication through the Learning Hub.
- Activity completion, grading, facilitator review, course and program completion behavior.
- LMS security roles and inherited permissions.
- Learning notifications and their background job.
- Supported connections to groups, workflows, communications, and reporting.
- Staff training and change enablement around Rock adoption and upgrades.

This guide does not establish general behavior for Rock Step Programs, streaks, achievement types, or every form of engagement journey. Those terms occur in the concept’s routing vocabulary, but the supplied answer-bearing evidence does not explain their mechanics. They remain a documented gap rather than a basis for inferred guidance.

Group requirements are also outside the LMS course-requirement model. A supplied community recipe discusses resetting a group-requirement workflow, but it is explicitly community-contributed, uses SQL deletion, and does not establish LMS requirement behavior. It should not be treated as an LMS procedure. [Community recipe disclaimer and example](https://community.rockrms.com/recipes/482)

## Mental Model

A **program** is the top-level container for related courses. It also controls the learning mode and can define defaults or automation such as the grading system, an activity-available communication template, program-completion tracking, and a completion workflow. [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program)

A **course** represents the type of learning being offered. It can have a public description, prerequisites or equivalencies, a course code, credits, a completion workflow, and a historical-access setting. One course can have multiple class instances. [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses)

A **class** is a specific occurrence of a course. Each class owns its learning plans, enrolled students, facilitators, and grading configuration. In Academic Calendar mode, the class is associated with a semester. [Classes](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes)

A **learning plan** is the ordered collection of activities for a class. Because the plan belongs to the class, an organization can preserve one class’s assignments while creating a revised class for future learners. [Create the Learning Plan](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan)

An **activity** is the unit of learner action: acknowledge content, read an article, watch a video, complete an assessment, upload a file, or perform work scored through a point assessment. Different activity types impose different learner, automation, and facilitator responsibilities. [Intro to Activities](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/intro-to-activities)

A **learning participant** is a student or facilitator associated with a learning class. Behind the scenes, a learning class is a specialized group, while students and facilitators correspond to specialized group members. This enables supported group and workflow features, but Rock’s documentation warns against custom SQL that manipulates the links between LMS and group records because Rock manages those relationships in code. [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes)

## Courses And Lessons

### Choose the program mode first

Use **On-Demand** mode when learners should join and work at their own pace without a fixed semester. Use **Academic Calendar** mode when the program needs semester dates, enrollment deadlines, a syllabus-oriented workspace, announcements, and time-bound class administration. The official v19 documentation recommends keeping simpler or continuously available training On-Demand. [Intro to LMS](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms)

Academic Calendar programs add semesters with start, end, and enrollment-close dates. The close date prevents new enrollment in associated classes after the deadline. Academic classes also expose additional workspace areas, including content and, when enabled at the course, announcements. [Configure Academic Calendar](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/configure-academic-calendar)

Do not choose Academic Calendar merely because a course has several lessons. Choose it only when the calendar-bound behavior is part of the intended experience.

### Build the hierarchy in configuration order

For a new program:

1. Go to `People > Learn` and create the program.
2. Select On-Demand or Academic Calendar mode.
3. Work in **Configure Program** mode.
4. Create the course and its description.
5. Configure course requirements where needed.
6. Edit the initial class Rock creates with the course.
7. Select the class grading system.
8. Build the class learning plan.
9. Add facilitators and students or prepare public enrollment.
10. Publish only after learner access, security, activities, and staff responsibilities have been reviewed. [Create a Program](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program), [Create a Course](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course), [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class)

Saving a new course automatically creates an initial class. Rename and configure that class rather than assuming the course itself is the learner-facing delivery instance. [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class)

### Revise a class without disrupting the current one

The class Copy action duplicates the class and its learning-plan activities but excludes students and facilitators. For an always-active On-Demand course, keep the new copy non-public while revising it. When it is ready, publish the new class and remove public visibility from the old class as appropriate. [Classes](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes)

Before switching visibility, verify the copied class’s facilitators, grading system, activity ordering, completion rules, communications, and enrollment experience. Copying is not evidence that those operational assignments are complete.

## Activity Design And Staff Responsibilities

An LMS class can combine content acknowledgments, video thresholds, assessments, file submissions, and facilitator-scored work. Training design must therefore define both what the learner does and what staff must review. This is a reviewed community implementation pattern supported by the supplied structural verification, not evidence that every installation has a particular class configured this way. [Community LMS walkthrough at 07:17](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

### Acknowledgment

Use an Acknowledgment activity when the learner must affirm a configured statement, such as a code of conduct or syllabus. The activity can display content and custom confirmation text beside the acknowledgment checkbox. [Acknowledgment Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/acknowledgment-activity)

Do not present an acknowledgment record as proof of comprehension or as a substitute for a separate legal or policy process unless that interpretation has been independently approved.

### Content article

A Content Article activity can present text or video and allow personal notes or a response to a reflection prompt. The documented notes are ungraded and private to the student. [Content Article Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/content-article-activity)

Content Article was added in Rock v18.1, along with SMS learning-activity notifications and improvements to Completion grading labels and feedback. Confirm version applicability before expecting these features on an older installation. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)

### Video watch

A Video Watch activity uses media from Rock’s Digital Media Accounts and can require the learner to watch a configured portion before completion. A documented example uses a 95% threshold, but that number is an example rather than a universal recommendation. [Video Watch Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/video-watch-activity), [Create the Learning Plan](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan)

Existing training videos can be incorporated into LMS activities, but the agent should not treat conversion of a video into an activity as the whole training design. Confirm the desired completion threshold, sequence, follow-up, and facilitator responsibility. [Reviewed community training pattern at 04:02](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz)

### Assessment

Assessment activities can contain multiple-choice questions, section separators, and short-answer questions. Multiple-choice answers can be scored automatically when a correct answer is configured. Short-answer items require facilitator scoring. Question weights, together with the multiple-choice weight, must total 100%. Result-display settings control whether learners see a summary and missed-question details after completion. [Assessment Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/assessment-activity)

Before launch, calculate the facilitator workload created by short-answer questions. An assessment that submits successfully may still be awaiting human review.

### File upload

A File Upload activity collects a learner’s file. Instructions and a grading rubric can be provided, with separate options for showing the rubric during upload and facilitator scoring. [File Upload Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/file-upload-activity)

Verify the organization’s accepted content, review ownership, retention expectations, and access permissions before using uploads for sensitive material. The supplied evidence does not define file-type restrictions or retention policy.

### Point assessment

A Point Assessment activity supports work that does not require a digital submission, such as a physical demonstration or in-person presentation. Its rubric guides facilitator scoring. [Point Assessment Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/point-assessment-activity)

Do not expect an uploaded artifact from this activity type. The operational record depends on the facilitator completing the scoring step.

## Requirements And Completion

### Course requirements

A course can define another course as a prerequisite or identify an equivalent course that fulfills its requirement. A prerequisite can prevent enrollment until the required course has been completed. [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses), [Create a Course](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course)

Public source code at immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` also shows a learning-course-requirement representation containing the course with requirements, the required course’s code, identifier and name, and a requirement type. This clarifies the implementation surface but does not prove which requirements are configured in an installation. [LearningCourseRequirementBag source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs)

When diagnosing eligibility, inspect the exact course requirement and the learner’s relevant completion record. Do not substitute group requirements, event-registration eligibility, or similarly named records.

### Grading systems and class completion

Rock documents Completion, Pass/Fail, and Letter Grade systems, and allows grading systems to be customized. A grading system with one scale is treated as a completion type, and its configured name becomes the finished-course label. [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class), [Configure Grading Systems](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems)

The class grading system cannot be changed after students begin completing assignments. Select and test it before learner activity begins. [Classes](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes)

For grading systems other than Completion, the documented behavior marks the class complete even when the participant fails. Rock intentionally leaves retake handling flexible. The documentation suggests organization-defined handling through a workflow reset, a Lava-based retry interface, or an administrative process. Treat any of these as a designed extension requiring review and testing, not as an automatic LMS feature. [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class)

### Course and program completion automation

A course can launch an optional workflow when an individual completes it. A program can also define a completion workflow. These hooks can support operational follow-up, but their presence does not prove a workflow is configured, enabled, authorized, or producing the intended result. [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses), [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program)

Program-level completion tracking must be enabled with **Track Program Status**. When enabled, the **Update Program Completions** job creates Learning Program Completion records. [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program), [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes)

The supplied Model Map record identifies **Learning Class Activity Completion** as an LMS model, but the record provides no field-level behavior. Do not infer completion semantics from the model name alone. [Rock Model Map](https://community.rockrms.com/ModelMap)

## Engagement Journeys And Learner Access

Within the evidence available here, the supported engagement journey is the LMS lifecycle:

**Discover → Review course → Meet requirements → Enroll → Enter class workspace → Complete activities → Receive grading or facilitator review → Complete class/course → Trigger follow-up or program completion**

The Learning Hub at `/learn` is the documented external entry point. It lists programs and courses marked Public. A signed-in learner can see completed or current enrollment indicators, inspect course details, enroll in open classes, and use the Class Workspace after enrollment. [Intro to the Learning Hub](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub)

Public visibility and security are separate concerns. Leaving a program or course non-public keeps it out of the Learning Hub while it is being prepared. If **Enforce Public Security** is enabled, external visibility also depends on View permission for the program; already-enrolled people retain access according to the documented program setting. [Intro to the Learning Hub](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub), [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program)

On-Demand and Academic Calendar classes provide different workspace experiences. Academic Calendar workspaces include class overview and progress, activities or assignments, and syllabus-oriented navigation. Both modes can expose communication preferences when an activity has **Send Notification Communications** enabled. [On-Demand Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example), [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example)

## Groups, Workflows, And Operational Follow-Up

A learning class is implemented as a specialized group, and students and facilitators are specialized group members. Rock documents the supported use of group-aware features, including a workflow action such as **Group Member Add From Attribute** to place students or facilitators into a class. It simultaneously warns against custom SQL that manipulates the LMS-to-group relationship. [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes)

Reviewed community evidence describes LMS completion interacting with groups, group sync, and workflow actions for volunteer training and follow-up. The supplied read-only verification confirmed that the relevant LMS activity, completion, group, group-member, and workflow-action surfaces existed in one connected instance; it did not verify a specific implementation or make that instance’s configuration universal. [Reviewed community LMS walkthrough at 26:43](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN)

For a completion-driven operational process:

1. Decide whether the authoritative trigger is an activity, course, or program completion.
2. Configure the corresponding supported workflow hook.
3. Define the exact group or downstream state the workflow should affect.
4. Test with a non-production learner record or approved test path.
5. Verify both the LMS completion record and the downstream workflow result.
6. Preserve a durable configuration or handoff artifact describing the trigger, expected side effects, owner, and recovery procedure.

The durable-artifact step follows official operational guidance that work intended to survive a conversation should be captured in a file or handoff rather than existing only in a transient chat. [Official guidance at 11:53](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=713s)

## Security And Facilitation

Rock v19 documentation identifies two LMS roles:

- **RSR - LMS Administration** for broad LMS administration. Grade viewing and editing are controlled separately by **View Grades** and **Edit Grades** actions.
- **RSR - LMS Workers** for internal LMS access by facilitators, program editors, and course editors. [Configure Security](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security)

A facilitator assigned to a class automatically gains permission to view and edit that class’s grades, but still needs **RSR - LMS Workers** to access internal class and program pages. Security inherits from program to course and from course to class, allowing permissions to be placed at the highest appropriate level. [Configure Security](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security)

If **Enforce Public Security** is used, the documentation warns that a person with external program access could see sensitive program information if they can also reach an insufficiently secured internal site. Secure the internal `People > Learn` page in addition to configuring program visibility. [Configure Security](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security)

Facilitators work primarily in **Program Overview** mode, which supports grading, comment review, and progress monitoring. **Configure Program** mode is for structural changes to courses, classes, semesters, and learning plans and appears only when the person has permission. [Intro to Program Administration](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/intro-to-program-administration)

Facilitator dashboards indicate activities requiring action and student comments. A healthy training launch therefore needs a named review cadence and sufficient facilitators, not merely assigned role membership. [Facilitators](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/facilitators)

## Notifications And Communications

Programs can specify an **Activity Available Communication Template**, and activities can be configured to send notification communications. Learners then receive a communication-preference option for email or text in the Class Workspace. [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program), [On-Demand Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example)

The **Send Learning Activity Notifications** background job sends notices for newly available activities. The documented v19 Academic Calendar example says the job runs once daily by default; running it manually can send an announcement immediately. Treat the actual schedule as installation configuration and inspect it live. [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes), [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example)

For SMS, the **Learning Activity Available** system communication needs a From Number. If it is missing, the notification job raises the documented “A From Number was not provided” warning. [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example)

## Reporting And Administration

Use **Configure Program** mode for structural changes and **Program Overview** for daily administration. Keeping those concerns separate limits accidental changes while facilitators are grading or monitoring learners. [Intro to Program Administration](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/intro-to-program-administration)

Public source code at immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3` includes an LMS person-reporting selector labeled **Has Completed Course**. Its configuration loads active programs for which completion status is tracked, then offers courses and completion-status options. This is implementation evidence for a reporting surface, not proof that a particular report or Data View has already been configured. [HasCompletedCourseSelect source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs)

For expensive historical journey analytics, reviewed community guidance supports calculating results into a persisted dataset on a schedule instead of recomputing the entire history on each dashboard load. The supplied public-safe verification confirmed the structural presence of persisted-dataset and scheduling surfaces in one instance, not any organization’s dataset contents or refresh configuration. [Reviewed community analytics guidance at 02:05](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

Use that pattern only after defining:

- The precise completion or engagement question.
- The source records and time boundary.
- The refresh schedule and acceptable data latency.
- The owner responsible for failed refreshes.
- The distinction between cached reporting output and current transactional state.

## Staff Enablement And Change Management

Rock’s LMS can assign curricula by staff role and track completion, making required Rock training specific and accountable. Before relying on that pattern, verify the installed LMS configuration, course visibility, permissions, enrollment process, and completion behavior. [Official guidance at 33:03](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1983s)

Train and activate staff before expecting them to train volunteers. Staff-first sequencing creates training multipliers and reduces the risk that inconsistent volunteer practices damage data quality. More broadly, training staff to use Rock correctly reduces the likelihood that teams adopt disconnected tools that fragment data and workflows outside the system of record. [Official guidance at 40:09](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s), [official guidance at 34:02](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2042s)

Include targeted training in upgrade plans before staff encounter a changed interface. A short video can reduce surprise and avoidable support requests. The v19 Connections redesign is one supplied release-specific example: active connectors should see the new interface and receive brief training before deployment. This guide does not restate the Connections workflow itself. [Official guidance at 28:34](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s), [v19 Connections training caveat at 01:31](https://www.youtube.com/watch?v=edanHiYSDIM&t=91s)

## Version And Authority Caveats

- Rock’s LMS was introduced in v17.0. Content Article activities, SMS learning notifications, and Completion grading improvements were added in v18.1. [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- Most detailed official LMS documentation supplied to this guide is scoped to v19.0. Confirm the installed version before expecting the same fields, roles, pages, labels, or behavior.
- The official documentation is authoritative for documented v19 behavior. Approved official media claims support staff-training and change-management guidance.
- Community-reviewed claims describe operational patterns and examples. They do not prove that a particular organization has implemented those patterns.
- Supplied read-only verification confirms only structural feature surfaces in the reviewed instance. It does not establish universal configuration, record contents, workflow success, or notification delivery.
- Public GitHub excerpts use immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They clarify implementation at that commit but do not prove behavior in another version or installation.
- Rock U provides official training modules covering LMS overview, program creation, administration, activities, and Academic Calendar mode. The supplied listing establishes module availability, not the detailed behavior inside each video. [Rock U LMS](https://community.rockrms.com/rocku/lms)

## Troubleshooting Decision Tree

### A learner cannot find a program or course

1. Confirm the learner is using the external Learning Hub at `/learn`.
2. Inspect whether the program and course are marked Public.
3. If **Enforce Public Security** is enabled, inspect the learner’s View access to the program.
4. Confirm that the intended class is public and open for enrollment.
5. If a class was copied, verify that the new class—not only the old one—was published after preparation.
6. If the learner is already enrolled, test the Class Workspace path separately from public discovery. [Intro to the Learning Hub](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub), [Classes](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes)

### A learner is blocked from enrollment

1. Identify the exact course and class.
2. Inspect the course’s prerequisite and equivalency requirements.
3. Verify the learner’s completion record for the required course; do not infer it from attendance, enrollment, or a similarly named group requirement.
4. For Academic Calendar mode, inspect the semester’s enrollment-close date.
5. Confirm the class remains open and public.
6. Stop when the unmet requirement or closed enrollment boundary is identified; changing it requires an authorized configuration decision. [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses), [Configure Academic Calendar](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/configure-academic-calendar)

### A facilitator cannot open LMS administration pages

1. Confirm the person is assigned as a facilitator to the intended class.
2. Confirm membership in **RSR - LMS Workers**.
3. Inspect security inherited from program to course to class.
4. Confirm the internal `People > Learn` page is accessible.
5. Distinguish page access from grade access; inspect **View Grades** and **Edit Grades** only when access is needed beyond the facilitator’s automatically granted class permissions. [Configure Security](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security)

### An activity is submitted but still incomplete

1. Identify the activity type.
2. For Video Watch, inspect the configured completion threshold and the learner’s recorded viewing progress.
3. For Assessment, determine whether short-answer items await facilitator scoring.
4. For File Upload or Point Assessment, check the facilitator’s action-required queue.
5. Confirm the class grading system and required activities.
6. Do not mark completion manually until the expected learner and facilitator actions are understood. [Video Watch Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/video-watch-activity), [Assessment Activity](https://community.rockrms.com/documentation/engagement/learning-management-system/activities/assessment-activity), [Facilitators](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/facilitators)

### A failed learner is marked complete

1. Inspect the class grading system.
2. Confirm whether it is Pass/Fail or Letter Grade rather than Completion.
3. Recognize that the documented LMS behavior can mark the class complete despite failure.
4. Determine the organization’s approved retake policy.
5. Use only an approved workflow, Lava interface, or administrative reset process.
6. Stop before inventing or deploying a reset mechanism without review. [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class)

### Program completion is not updating

1. Confirm **Track Program Status** is enabled.
2. Inspect the **Update Program Completions** job and its schedule.
3. Check the job’s latest run and error state.
4. Verify that underlying course and class completion conditions are satisfied.
5. Distinguish a delayed background update from missing transactional completion.
6. If a program-completion workflow is configured, verify its result separately after the completion record updates. [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program), [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes)

### Learning notifications are delayed or absent

1. Confirm **Send Notification Communications** is enabled on the relevant activity.
2. Confirm the program has the intended Activity Available Communication Template.
3. Inspect the **Send Learning Activity Notifications** job, schedule, and latest result.
4. For immediate Academic Calendar announcements, run the job only with appropriate operational authorization.
5. For SMS, verify the **Learning Activity Available** system communication has a From Number.
6. Verify recipient communication preferences and actual delivery separately from job success. [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example), [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program)

### An LMS dashboard is slow

1. Define the exact metric and reporting period.
2. Determine whether the page recomputes historical engagement data on every request.
3. Inspect existing Data Views, reports, or persisted datasets before creating duplicates.
4. If computation is expensive and some latency is acceptable, evaluate a scheduled persisted dataset.
5. Set a refresh cadence and disclose the resulting data freshness.
6. Verify job duration, failure handling, and dashboard read performance before calling the issue resolved. [Reviewed community analytics guidance at 02:05](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

## Agent Task Recipes

### Recipe: Create a self-paced volunteer training course

**Outcome:** A private, review-ready On-Demand class with an intentional activity plan and named staff responsibilities.

1. Confirm the installed version and LMS administrator access.
2. Create or select the Volunteer Training program in On-Demand mode.
3. In Configure Program mode, create the course and learner-facing description.
4. Add only evidence-based prerequisites or equivalencies.
5. Rename and configure the automatically created initial class.
6. Select the grading system before any learner begins work.
7. Build the class learning plan using activity types matched to the desired outcomes.
8. Assign facilitators for every activity requiring manual review.
9. Configure course or program completion workflows only when the downstream outcome is defined.
10. Keep the program, course, and class non-public during review.
11. Test discovery, enrollment, learner activity, facilitator review, completion, and follow-up with an approved test path.
12. Publish only after security and staff ownership are confirmed. [Create a Program](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program), [Create the Learning Plan](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan)

**Inspect:**

- Program mode and visibility.
- Course requirements.
- Class grading system.
- Activity sequence and thresholds.
- Facilitator assignments.
- Completion automation.
- External and internal security.

**Do not assume:**

- A video alone defines a complete training outcome.
- An assigned facilitator can access internal LMS pages without the worker role.
- A workflow hook proves successful downstream execution.

**Stop when:**

- The grading or retake policy is undecided.
- No owner exists for manual review.
- Publishing would expose unfinished content or improperly secured pages.

### Recipe: Prepare an Academic Calendar class

**Outcome:** A semester-bound class with controlled enrollment and an operational notification plan.

1. Confirm that semester-based delivery is actually required.
2. Configure the program in Academic Calendar mode.
3. Create the semester with start, end, and enrollment-close dates.
4. Associate the class with the semester.
5. Configure the course’s announcement setting when announcements are needed.
6. Prepare syllabus, content, and activities for the Academic Calendar workspace.
7. Configure activity notifications and the communication template.
8. Verify email or SMS preferences appear for an approved test learner.
9. Inspect the notification job schedule and SMS From Number where applicable.
10. Test enrollment before and after the intended boundary without altering production dates merely for testing. [Configure Academic Calendar](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/configure-academic-calendar), [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example)

**Do not assume:**

- Academic Calendar mode is better for ordinary self-paced training.
- Creating a semester automatically validates notification delivery.
- Job success proves receipt by the learner.

### Recipe: Assign role-specific staff training

**Outcome:** Staff receive accountable curricula matched to their responsibilities before they train volunteers.

1. Define the staff roles and the Rock tasks each role must perform.
2. Map each role to the smallest appropriate course set.
3. Configure prerequisites where one course must precede another.
4. Assign or enroll the target staff through supported LMS and group operations.
5. Track course completion rather than treating enrollment as completion.
6. Establish the completion deadline, facilitator owner, and escalation path.
7. Train staff first and confirm they can execute the real workflow.
8. Release volunteer training only after staff readiness is verified.
9. Store a durable handoff containing the curriculum map, owners, completion definition, and current status. [Official role-based LMS guidance at 33:03](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1983s), [staff-first guidance at 40:09](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=2409s)

### Recipe: Connect course completion to operational follow-up

**Outcome:** A supported workflow responds to a clearly defined LMS completion event.

1. Choose the correct event boundary: course completion or program completion.
2. Inspect the existing Completion Workflow Type before creating anything new.
3. Define the exact downstream outcome, such as a reviewed group-membership change or follow-up workflow.
4. Configure the supported workflow hook.
5. Use Rock’s group and workflow features; do not manipulate LMS/group linkage through custom SQL.
6. Complete the learning path with an approved test participant.
7. Verify the completion record.
8. Verify the workflow instance and downstream state separately.
9. Record failure recovery and ownership in a durable handoff. [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses), [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes)

**Stop when:**

- The requested trigger cannot be distinguished from enrollment or activity submission.
- The downstream mutation has not been authorized.
- Testing confirms the LMS record but not the workflow result.

### Recipe: Roll out training for a changed Rock interface

**Outcome:** Affected staff see and practice the changed workflow before production use.

1. Identify the exact version and affected interface.
2. Identify the staff roles that use it.
3. Record the old-to-new task changes in a durable artifact.
4. Produce a short, task-focused walkthrough showing the new interface.
5. Enroll or distribute the training before deployment.
6. Provide a safe practice route when available.
7. Track completion for required staff.
8. Confirm support ownership for launch day.
9. Recheck release applicability immediately before rollout. [Official upgrade-training guidance at 28:34](https://www.youtube.com/watch?v=bu5nPeAVCAo&t=1714s)

**Do not assume:**

- A release note has trained active users.
- Sending a video proves it was watched or understood.
- The v19 Connections example applies to unrelated interfaces without separate evidence.

### Recipe: Build a bounded LMS completion report

**Outcome:** A report answers one defined completion question with an explicit freshness boundary.

1. State the question, population, course or program, status, and date boundary.
2. Confirm program-completion tracking is enabled if the report depends on program status.
3. Inspect existing reports and Data Views before adding a new artifact.
4. Use the supported course-completion reporting surface where it matches the question.
5. Validate sample records against the LMS administration view.
6. If historical computation is too expensive for page-time execution, evaluate a persisted dataset and schedule.
7. Display the refresh time or expected latency.
8. Verify both correctness and acceptable performance. [HasCompletedCourseSelect source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs), [reviewed persisted-dataset guidance](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW)

## Known Gaps And Live Verification

The following checks require installation-specific, bounded verification before an agent gives a definitive operational answer:

- Installed Rock version and whether the expected LMS features are present.
- Program mode, public state, **Enforce Public Security**, completion tracking, grading defaults, and workflow hooks.
- Course requirements, equivalencies, historical-access setting, announcements, and completion workflow.
- Class visibility, semester, grading system, activity ordering, facilitators, students, and enrollment state.
- Actual completion records for the affected learner.
- Background-job schedules, last runs, errors, and resulting records.
- Communication templates, SMS From Number, recipient preferences, and provider delivery.
- Internal page security, LMS roles, inherited object security, and grade permissions.
- Workflow configuration and the downstream result of a completion event.
- Existing Data Views, reports, persisted datasets, refresh schedules, and dashboard latency.
- Plugin-provided activity types or schema extensions; none are established by this pack.
- Retake policy and the organization’s approved implementation.
- Data retention, file restrictions, and privacy policy for learner uploads.
- General Step Program, streak, achievement, or non-LMS engagement-journey behavior.

The evidence pack includes reviewed public-safe conclusions from prior read-only structural probes. Those conclusions support the existence of certain LMS, group, workflow, persisted-dataset, and scheduling surfaces in the reviewed environment. They do not verify the reader’s installation, any current configuration, or a specific organization’s learner data.

## Source Map

### Official documentation

- [Learning Management System](https://community.rockrms.com/documentation/engagement/learning-management-system) — v19 documentation index.
- [Intro to LMS](https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms) — modes, hierarchy, activity types, grading, and internal/external surfaces.
- [Create a Program](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-program) — initial program workflow and administration modes.
- [Create a Course](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course) — course creation and prerequisite example.
- [Edit the Class](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class) — initial class, grading systems, completion behavior, and retakes.
- [Create the Learning Plan](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-the-learning-plan) — class-owned plans, video threshold example, facilitators, and enrollment.
- [Configure Academic Calendar](https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/configure-academic-calendar) — semesters, dates, enrollment closing, content, and announcements.
- [Intro to the Learning Hub](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub) — publication, discovery, enrollment, and Class Workspace.
- [Academic Calendar Class Workspace Example](https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example) — workspace, notification timing, and SMS configuration.
- [Configure Security](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security) — LMS roles, grade permissions, inheritance, and page-security warning.
- [Configure Program](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program) — visibility, modes, completion tracking, communications, grading, and workflows.
- [Courses](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses) — requirements, equivalencies, completion workflow, and historical access.
- [Classes](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes) — class ownership, grading lock, and cloning.
- [Facilitators](https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/facilitators) — worker access and review indicators.
- [LMS Behind the Scenes](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes) — group relationships, SQL warning, and background jobs.
- [Activities](https://community.rockrms.com/documentation/engagement/learning-management-system/activities) — official activity documentation index.
- [Configure Grading Systems](https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems) — grading customization and completion-scale behavior.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — v17.0 LMS introduction and v18.1 LMS additions.
- [Rock U LMS](https://community.rockrms.com/rocku/lms) — official LMS training-module index.

### Approved operational claims and reviewed examples

- [Community LMS walkthrough](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/qMlA3ybBEN) — reviewed examples of LMS structure, mixed activities, groups, workflows, and volunteer-training follow-up.
- [Community video-training pattern](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDq4MBqz) — reviewed guidance for converting existing video into intentional training.
- [Community journey-analytics pattern](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW) — reviewed persisted-dataset guidance.
- [Official staff-training discussion](https://www.youtube.com/watch?v=bu5nPeAVCAo) — role-based curricula, staff-first training, durable artifacts, and upgrade enablement.
- [Official v19 Connections training caveat](https://www.youtube.com/watch?v=edanHiYSDIM&t=91s) — release-specific example of training users before an interface change.

### Implementation evidence

- [LearningCourseRequirementBag at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs) — course-requirement representation.
- [HasCompletedCourseSelect at immutable commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs) — person reporting selector for completed learning courses.
- [Learning Class Activity Completion Model Map](https://community.rockrms.com/ModelMap) — model-category identification only.