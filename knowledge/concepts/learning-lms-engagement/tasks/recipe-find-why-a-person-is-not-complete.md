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

- https://www.triumph.tech/resources/github-spotlight-11142025
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/documentation/bookcontent/39
- https://community.rockrms.com/recipes/482
