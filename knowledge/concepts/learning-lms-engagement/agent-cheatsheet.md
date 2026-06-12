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
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Data View` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `DataView` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
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
| `generated-model-map-pointers` | citation-only | live verification |
| `1-executive-summary-for-agents` | high | live verification |
| `3-learning-lms-and-engagement-mental-model` | needs-citation | needs-citation |
| `4-source-authority-and-how-to-use-this-guide` | high | live verification |
| `5-core-configuration-and-data-model` | high | live verification |
| `6-primary-entities-and-relationships-lms-entity-relationships` | high | live verification |
| `7-common-learning-lms-and-engagement-workflows-create-an-on-demand-training-program` | normal | live verification |
| `7-common-learning-lms-and-engagement-workflows-create-an-academic-calendar-program` | normal | live verification |
| `7-common-learning-lms-and-engagement-workflows-assign-training-to-volunteers-or-staff` | needs-citation | live verification |
| `7-common-learning-lms-and-engagement-workflows-record-a-ministry-milestone` | citation-only | live verification |
| `7-common-learning-lms-and-engagement-workflows-automate-follow-up-from-learning-completion` | citation-only | live verification |
| `8-courses-and-lessons-deep-dive-course-configuration-checks` | normal | live verification |
| `8-courses-and-lessons-deep-dive-class-design` | normal | live verification |
| `8-courses-and-lessons-deep-dive-learning-plan-activity-design` | high | live verification |
| `8-courses-and-lessons-deep-dive-lessons-versus-activities` | citation-only | live verification |
| `9-requirements-and-completion-deep-dive-lms-course-requirements` | normal | live verification |
| `9-requirements-and-completion-deep-dive-completion-tracking` | normal | live verification |
| `9-requirements-and-completion-deep-dive-activity-completion-workflows` | citation-only | live verification |
| `10-engagement-journeys-deep-dive-step-types` | normal | live verification |
| `10-engagement-journeys-deep-dive-adding-steps` | citation-only | live verification |
| `10-engagement-journeys-deep-dive-achievements-and-streaks` | high | live verification |
| `11-reporting-and-administration-deep-dive-lms-reporting` | normal | live verification |
| `11-reporting-and-administration-deep-dive-administration` | normal | live verification |
| `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-people` | structural | live verification |
| `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-communications` | normal | live verification |
| `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-workflows` | citation-only | live verification |
| `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-event-registration` | normal | live verification |
| `12-related-rock-areas-people-groups-communications-workflows-event-registration-data-views-reports-security-platform-configuration-security` | normal | live verification |
| `13-administration-and-operational-guardrails-guardrail-3-verify-entity-types-before-automating` | citation-only | live verification |
| `13-administration-and-operational-guardrails-guardrail-4-preserve-customized-system-communications` | normal | live verification |
| `13-administration-and-operational-guardrails-guardrail-7-mark-legacy-training-as-legacy` | citation-only | live verification |
| `14-developer-api-lava-and-source-code-landmarks-source-repository` | normal | live verification |
| `14-developer-api-lava-and-source-code-landmarks-lava-landmarks` | community-supported | live verification |
| `15-reporting-analytics-and-model-map` | normal | live verification |
| `16-version-and-release-caveats-rock-v17-0` | high | live verification |
| `16-version-and-release-caveats-rock-v18-1` | high | live verification |
| `16-version-and-release-caveats-rock-v18-3-and-v19-1-release-notes-in-pack` | normal | live verification |
| `16-version-and-release-caveats-develop-branch-caveat` | structural | live verification |
| `17-implementation-playbooks-playbook-launch-a-volunteer-training-lms-program` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-add-a-new-course-requirement` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-convert-a-training-completion-into-an-engagement-step` | needs-citation | live verification |
| `17-implementation-playbooks-playbook-build-a-learning-dashboard` | structural | live verification |
| `17-implementation-playbooks-playbook-upgrade-review-for-lms-and-engagement` | normal | live verification |
| `18-troubleshooting-decision-tree-group-requirement-still-fails-after-lms-completion` | needs-citation | needs-citation |
| `19-agent-task-recipes-recipe-find-why-a-person-is-not-complete` | structural | live verification |
| `19-agent-task-recipes-recipe-prepare-a-course-for-launch` | structural | live verification |
| `19-agent-task-recipes-recipe-build-a-step-journey-from-training` | structural | live verification |
| `19-agent-task-recipes-recipe-review-upgrade-risk` | structural | live verification |
| `20-source-map-and-dependency-notes` | high | live verification |
