---
concept_id: learning-lms-engagement
task_id: recipe-find-why-a-person-is-not-complete
title: Recipe: Find Why A Person Is Not Complete
generated: true
---

# Recipe: Find Why A Person Is Not Complete

Determine whether the missing completion is caused by enrollment, activity completion, program rollup, workflow timing, or reporting filters.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Learning Class`
- `Learning Class Activity`
- `Learning Class Activity Completion`
- `Learning Program Completion`
- `Learning Course Requirement`
- `Workflow`

## Entities And Tables

- `Person`
- `LearningClass`
- `LearningClassActivity`
- `LearningClassActivityCompletion`
- `LearningProgramCompletion`
- `LearningCourseRequirement`
- `Workflow`

## Steps

1. Confirm the person is the intended learner and is attached to the expected class or program.
2. Inspect required activities and their completion records before checking program rollups.
3. Check whether course requirements or workflows are waiting on another Rock entity.
4. Compare the live completion rows with the report or data view that raised the issue.
5. Separate LMS completion from serving approval or group requirement state.

## Do Not Assume

- Do not infer completion from attendance, registration, or group membership alone.
- Do not mark a person complete until the required activity and rollup records agree.

## Source Links

- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/lms-behind-the-scenes
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/configure-program
- https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/edit-the-class
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/documentation/engagement/learning-management-system/create-a-learning-program/create-a-course
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/classes
- https://community.rockrms.com/documentation/engagement/learning-management-system/advanced-lms/configure-grading-systems
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs
- https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/X6mkVpZBJW
