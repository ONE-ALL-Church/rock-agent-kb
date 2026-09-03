---
concept_id: learning-lms-engagement
task_id: recipe-review-upgrade-risk
title: Recipe: Review Upgrade Risk
generated: true
---

# Recipe: Review Upgrade Risk

Review LMS, engagement, requirement, workflow, and communication behavior against current release notes and source-code caveats.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Rock Version`
- `Learning Course`
- `Learning Class Activity Completion`
- `Step Program`
- `Group Member Requirement`
- `Workflow`
- `System Communication`

## Entities And Tables

- `LearningCourse`
- `LearningClassActivityCompletion`
- `StepProgram`
- `GroupMemberRequirement`
- `Workflow`

## Steps

1. Identify the current and target Rock versions.
2. Review release notes for LMS, Step, requirement, workflow, and communication changes.
3. Spot-check source-code landmarks for renamed or changed model behavior.
4. List affected programs, classes, Step Programs, and requirement gates before upgrading.
5. Validate a representative learner path after the upgrade.

## Do Not Assume

- Do not rely on old task-card behavior after an LMS or Step-related release.
- Do not merge upgrade guidance until release-note and live-record checks agree.

## Source Links

- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-security
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub
- https://community.rockrms.com/documentation/engagement/learning-management-system/overview/intro-to-lms
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/facilitators
- https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class
