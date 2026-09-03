---
concept_id: learning-lms-engagement
title: Learning, LMS, And Engagement Agent Cheatsheet
generated: true
---

# Learning, LMS, And Engagement Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Audit One LMS Program](tasks/recipe-audit-one-lms-program.md) | `Learning Program`, `Learning Course`, `Learning Class`, `Learning Class Activity`, `Learning Class Activity Completion`, `System Communication` | `LearningProgram`, `LearningCourse`, `LearningClass`, `LearningClassActivity`, `LearningClassActivityCompletion`, `Person` |
| [Recipe: Find Why A Person Is Not Complete](tasks/recipe-find-why-a-person-is-not-complete.md) | `Person`, `Learning Class`, `Learning Class Activity`, `Learning Class Activity Completion`, `Learning Program Completion`, `Learning Course Requirement`, `Workflow` | `Person`, `LearningClass`, `LearningClassActivity`, `LearningClassActivityCompletion`, `LearningProgramCompletion`, `LearningCourseRequirement`, `Workflow` |
| [Recipe: Prepare A Course For Launch](tasks/recipe-prepare-a-course-for-launch.md) | `Learning Program`, `Learning Course`, `Learning Class`, `Learning Semester`, `Learning Class Activity`, `Learning Participant`, `System Communication` | `LearningProgram`, `LearningCourse`, `LearningClass`, `LearningSemester`, `LearningClassActivity`, `LearningParticipant` |
| [Recipe: Build A Step Journey From Training](tasks/recipe-build-a-step-journey-from-training.md) | `Learning Class Activity Completion`, `Learning Program Completion`, `Step Program`, `Step Type`, `Step`, `Data View`, `Workflow` | `LearningClassActivityCompletion`, `LearningProgramCompletion`, `StepProgram`, `StepType`, `Step`, `DataView`, `Workflow` |
| [Recipe: Review Upgrade Risk](tasks/recipe-review-upgrade-risk.md) | `Rock Version`, `Learning Course`, `Learning Class Activity Completion`, `Step Program`, `Group Member Requirement`, `Workflow`, `System Communication` | `LearningCourse`, `LearningClassActivityCompletion`, `StepProgram`, `GroupMemberRequirement`, `Workflow` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Data View` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Group Member Requirement` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `GroupMemberRequirement` | `GroupMember`, `Person`, `Group` | Keep LMS completion separate from serving eligibility unless a requirement explicitly connects them. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Class` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Class Activity` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Class Activity Completion` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Course` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Course Requirement` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Participant` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Program` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Program Completion` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Learning Semester` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `LearningClass` | `LearningCourse`, `LearningClassActivity`, `LearningClassActivityCompletion`, `LearningParticipant` | Inspect class status, semester, participants, activities, and workflow side effects when troubleshooting completion. |
| `LearningClassActivity` | `LearningClass`, `LearningClassActivityCompletion` | Check activity configuration and completion rules before assuming a learner failed to finish the course. |
| `LearningClassActivityCompletion` | `LearningClassActivity`, `LearningClass`, `Person` | Use this to diagnose missing activity completion before escalating to program or step logic. |
| `LearningCourse` | `LearningProgram`, `LearningClass`, `LearningCourseRequirement` | Confirm whether a question is about the course definition, a class instance, or a person's completion state. |
| `LearningCourseRequirement` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `LearningParticipant` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `LearningProgram` | `LearningCourse`, `LearningClass`, `LearningProgramCompletion` | Verify active course/class structure and completion semantics before treating LMS completion as ministry qualification. |
| `LearningProgramCompletion` | `LearningProgram`, `Person`, `LearningClassActivityCompletion` | Confirm which activity and course completions roll up to the program before reporting someone as complete. |
| `LearningSemester` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Rock Version` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Step Program` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Step Type` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `StepProgram` | `StepType`, `Step`, `Person` | Do not equate a training completion with a Step unless the workflow or data view explicitly writes it. |
| `StepType` | `StepProgram`, `Step` | Check prerequisites, filters, workflows, and achievement behavior when a badge or step is missing. |
| `System Communication` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.1` | core | Added the new Content Article Learning Activity type, allowing individuals to complete training by reading content articles. Also added support for SMS notifications to alert individuals about new learning activities. Improved the Completio |
| `17.0` | core | Added the Learning Management System (LMS) that provides tools to create and manage educational content, training programs, and courses within your organization. |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `scope-and-boundaries` | community-supported | community-supported |
| `courses-and-lessons-revise-a-class-without-disrupting-the-current-one` | normal | live verification |
| `activity-design-and-staff-responsibilities-file-upload` | normal | live verification |
| `requirements-and-completion-course-requirements` | high | live verification |
| `requirements-and-completion-grading-systems-and-class-completion` | normal | live verification |
| `engagement-journeys-and-learner-access` | normal | live verification |
| `groups-workflows-and-operational-follow-up` | normal | live verification |
| `notifications-and-communications` | normal | live verification |
| `staff-enablement-and-change-management` | citation-only | live verification |
| `troubleshooting-decision-tree-a-learner-cannot-find-a-program-or-course` | normal | live verification |
| `troubleshooting-decision-tree-a-learner-is-blocked-from-enrollment` | normal | live verification |
| `troubleshooting-decision-tree-a-facilitator-cannot-open-lms-administration-pages` | normal | live verification |
| `troubleshooting-decision-tree-an-activity-is-submitted-but-still-incomplete` | normal | live verification |
| `troubleshooting-decision-tree-a-failed-learner-is-marked-complete` | normal | live verification |
| `troubleshooting-decision-tree-program-completion-is-not-updating` | normal | live verification |
| `troubleshooting-decision-tree-learning-notifications-are-delayed-or-absent` | normal | live verification |
| `troubleshooting-decision-tree-an-lms-dashboard-is-slow` | citation-only | live verification |
| `agent-task-recipes-recipe-create-a-self-paced-volunteer-training-course` | normal | live verification |
| `agent-task-recipes-recipe-prepare-an-academic-calendar-class` | normal | live verification |
| `agent-task-recipes-recipe-connect-course-completion-to-operational-follow-up` | normal | live verification |
| `agent-task-recipes-recipe-roll-out-training-for-a-changed-rock-interface` | citation-only | live verification |
| `agent-task-recipes-recipe-build-a-bounded-lms-completion-report` | normal | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
