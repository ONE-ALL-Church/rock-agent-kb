---
concept_id: learning-lms-engagement
task_id: recipe-build-a-step-journey-from-training
title: Recipe: Build A Step Journey From Training
generated: true
---

# Recipe: Build A Step Journey From Training

Connect training completion to an engagement journey only through explicit workflows, data views, or step-writing logic.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Learning Class Activity Completion`
- `Learning Program Completion`
- `Step Program`
- `Step Type`
- `Step`
- `Data View`
- `Workflow`

## Entities And Tables

- `LearningClassActivityCompletion`
- `LearningProgramCompletion`
- `StepProgram`
- `StepType`
- `Step`
- `DataView`
- `Workflow`

## Steps

1. Define which completion event should create or update the engagement step.
2. Inspect the Step Program and Step Type before configuring workflow or data view logic.
3. Verify prerequisites, badge or achievement display behavior, and reporting scope.
4. Test with a known learner and confirm both completion and Step records exist.
5. Document the boundary between training history and engagement journey state.

## Do Not Assume

- Do not assume a completed training automatically creates a Step.
- Do not troubleshoot badge display until the Step row and Step Type are verified.

## Source Links

- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses
- https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems
- https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/intro-to-the-learning-hub
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/on-demand-class-workspace-example
- https://community.rockrms.com/documentation/engagement/learning-management-system/lms-learning-hub/academic-calendar-class-workspace-example
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs
