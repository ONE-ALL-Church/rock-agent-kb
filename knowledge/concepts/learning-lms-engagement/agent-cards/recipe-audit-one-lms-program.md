---
concept_id: learning-lms-engagement
task_id: recipe-audit-one-lms-program
title: Recipe: Audit One LMS Program
generated: true
---

# Recipe: Audit One LMS Program

Trace a program from source content through courses, classes, activities, completion, communications, and reporting.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Learning Program`
- `Learning Course`
- `Learning Class`
- `Learning Class Activity`
- `Learning Class Activity Completion`
- `System Communication`

## Entities And Tables

- `LearningProgram`
- `LearningCourse`
- `LearningClass`
- `LearningClassActivity`
- `LearningClassActivityCompletion`
- `Person`

## Steps

1. Identify the program, course, class, semester, and activity records involved.
2. Confirm whether the program is scheduled, self-paced, or hybrid before interpreting completion.
3. Inspect activity completion rows and program/course rollup behavior.
4. Review communications, workflows, and reporting dependencies tied to the program.
5. Cite the exact source and live record boundary before recommending changes.

## Do Not Assume

- Do not assume a course definition proves a specific learner completed the work.
- Do not treat a training program as a serving eligibility gate without the requirement record.

## Source Links

- https://community.rockrms.com/documentation/bookcontent/43/354
- https://github.com/SparkDevNetwork/Rock
- https://www.triumph.tech/resources/github-spotlight-11142025
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/rocku/engagement
- https://community.rockrms.com/ModelMap
- https://community.rockrms.com/rocku/lms
- https://community.rockrms.com/documentation/bookcontent/39
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs
- https://community.rockrms.com/rocku/lms/lms-academic-calendar
- https://community.rockrms.com/rocku/lms/lms-create-a-program
- https://community.rockrms.com/rocku/lms/lms-overview
